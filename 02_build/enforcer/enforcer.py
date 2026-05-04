#!/usr/bin/env python3
# Authored by Claude (Haiku 4.5), 2026-03-11
# Merged into clean-build/02_build/enforcer/ by Devon (Devin session devin-1bdaf31798874921940598bed17ca9e3), 2026-05-04 (AMP-77)
"""
The Enforcer — Production Compliance & Health Checking System
Runs on Hetzner "The Beast" (135.181.161.131)
Checks infrastructure health, data integrity, agent compliance every 10 minutes.

Core principles:
- Deterministic checks (no LLM needed)
- Fast execution (<30 seconds for all checks)
- Graceful degradation (one failure doesn't block others)
- Structured JSON logging
- Docker-native (reads Docker socket)
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
import signal

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
import uvicorn
import yaml

from checks import (
    docker_health,
    database_health,
    traefik_health,
    session_hygiene,
    security_check,
)


# ============================================================================
# CONFIGURATION
# ============================================================================

@dataclass
class CheckResult:
    """Result of a single health check."""
    name: str
    status: str  # "pass", "warn", "fail"
    message: str
    severity: str  # "info", "warning", "critical"
    timestamp: str
    duration_ms: float
    details: Dict[str, Any]


class EnforcerConfig:
    """Load configuration from YAML and environment variables."""
    
    def __init__(self):
        self.check_interval = int(os.getenv('CHECK_INTERVAL', '600'))
        self.alert_webhook_url = os.getenv('ALERT_WEBHOOK_URL', '')
        self.langfuse_host = os.getenv('LANGFUSE_HOST', '')
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        
        # Database hosts
        self.falkordb_host = os.getenv('FALKORDB_HOST', 'falkordb')
        self.falkordb_port = int(os.getenv('FALKORDB_PORT', '6379'))
        self.postgres_host = os.getenv('POSTGRES_HOST', 'postgres')
        self.postgres_port = int(os.getenv('POSTGRES_PORT', '5432'))
        self.redis_host = os.getenv('REDIS_HOST', 'redis')
        self.redis_port = int(os.getenv('REDIS_PORT', '6379'))
        self.qdrant_host = os.getenv('QDRANT_HOST', 'qdrant')
        self.qdrant_port = int(os.getenv('QDRANT_PORT', '6333'))
        
        # Session hygiene
        self.session_state_path = os.getenv(
            'SESSION_STATE_PATH',
            '/opt/amplified/vault/00-handover/SESSION-STATE.md'
        )
        self.max_session_state_age_hours = int(
            os.getenv('MAX_SESSION_STATE_AGE_HOURS', '24')
        )
        
        # Security
        self.fail2ban_enabled = os.getenv('FAIL2BAN_ENABLED', 'true').lower() == 'true'
        
        # Expected containers (comma-separated)
        self.expected_containers = os.getenv(
            'EXPECTED_CONTAINERS',
            'traefik,falkordb,postgres,redis,qdrant,langfuse,portainer'
        ).split(',')


# ============================================================================
# LOGGING SETUP
# ============================================================================

def setup_logging(config: EnforcerConfig):
    """Configure JSON-formatted logging."""
    logging.basicConfig(
        level=getattr(logging, config.log_level),
        format='%(message)s'
    )
    return logging.getLogger(__name__)


def log_json(logger: logging.Logger, level: str, data: Dict[str, Any]):
    """Log a structured JSON message."""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'level': level,
        **data
    }
    
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(json.dumps(log_entry))


# ============================================================================
# ENFORCER ENGINE
# ============================================================================

class EnforcerEngine:
    """Main enforcement engine that runs checks and manages alerts."""
    
    def __init__(self, config: EnforcerConfig, logger: logging.Logger):
        self.config = config
        self.logger = logger
        self.last_check_time = None
        self.last_results = []
        self.is_healthy = True
        self._running = False
    
    async def run_all_checks(self) -> List[CheckResult]:
        """
        Run all health checks concurrently.
        Returns a list of CheckResult objects.
        Gracefully handles individual check failures.
        """
        results = []
        start_time = datetime.utcnow()
        
        # Define all checks
        checks = [
            ('docker_health', docker_health.check_docker_health, {
                'expected_containers': self.config.expected_containers
            }),
            ('database_health', database_health.check_databases, {
                'falkordb_host': self.config.falkordb_host,
                'falkordb_port': self.config.falkordb_port,
                'postgres_host': self.config.postgres_host,
                'postgres_port': self.config.postgres_port,
                'redis_host': self.config.redis_host,
                'redis_port': self.config.redis_port,
                'qdrant_host': self.config.qdrant_host,
                'qdrant_port': self.config.qdrant_port,
            }),
            ('traefik_health', traefik_health.check_traefik, {
                'traefik_host': 'traefik'
            }),
            ('session_hygiene', session_hygiene.check_session_state, {
                'session_state_path': self.config.session_state_path,
                'max_age_hours': self.config.max_session_state_age_hours,
            }),
            ('security_check', security_check.check_security, {
                'fail2ban_enabled': self.config.fail2ban_enabled,
            }),
        ]
        
        # Run checks concurrently
        tasks = []
        for check_name, check_func, kwargs in checks:
            task = asyncio.create_task(
                self._run_check_safe(check_name, check_func, kwargs)
            )
            tasks.append(task)
        
        # Gather results
        results = await asyncio.gather(*tasks, return_exceptions=False)
        
        # Filter out None results (failed checks)
        results = [r for r in results if r is not None]
        
        # Log summary
        duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000
        self.last_check_time = start_time
        self.last_results = results
        
        # Determine overall health
        critical_count = sum(1 for r in results if r.severity == 'critical')
        self.is_healthy = critical_count == 0
        
        log_json(self.logger, 'INFO', {
            'event': 'check_cycle_complete',
            'total_checks': len(results),
            'critical_issues': critical_count,
            'overall_health': 'healthy' if self.is_healthy else 'unhealthy',
            'duration_ms': duration_ms,
        })
        
        return results
    
    async def _run_check_safe(
        self,
        name: str,
        check_func,
        kwargs: Dict[str, Any]
    ) -> CheckResult:
        """Run a single check with error handling."""
        try:
            start = datetime.utcnow()
            result = await check_func(**kwargs)
            duration = (datetime.utcnow() - start).total_seconds() * 1000
            
            # Add timing — each check module has its own dataclass type with
            # a duration_ms attribute, so test by attribute presence rather
            # than `isinstance(result, CheckResult)` (which is always False
            # because none of the per-check dataclasses inherit from CheckResult).
            if hasattr(result, 'duration_ms'):
                result.duration_ms = duration
            
            return result
        except Exception as e:
            self.logger.error(f"Check {name} failed: {str(e)}", exc_info=True)
            return CheckResult(
                name=name,
                status='fail',
                message=f'Check execution failed: {str(e)}',
                severity='critical',
                timestamp=datetime.utcnow().isoformat() + 'Z',
                duration_ms=0,
                details={'error': str(e)}
            )
    
    async def start_check_loop(self):
        """Start the main check loop that runs every CHECK_INTERVAL seconds."""
        self._running = True
        self.logger.info(f"Enforcer starting with {self.config.check_interval}s interval")
        
        while self._running:
            try:
                await self.run_all_checks()
                await asyncio.sleep(self.config.check_interval)
            except Exception as e:
                self.logger.error(f"Check loop error: {str(e)}", exc_info=True)
                await asyncio.sleep(5)  # Brief pause before retry
    
    def stop(self):
        """Stop the check loop gracefully."""
        self._running = False


# ============================================================================
# FASTAPI HEALTH ENDPOINT
# ============================================================================

def create_app(config: EnforcerConfig, enforcer: EnforcerEngine) -> FastAPI:
    """Create FastAPI application with health endpoints."""
    app = FastAPI(
        title='The Enforcer',
        description='Amplified Partners Compliance & Health Checking System',
        version='1.0.0'
    )
    
    @app.get('/health')
    async def health() -> JSONResponse:
        """
        Health check endpoint.
        Returns 200 if overall system is healthy, 503 if critical issues detected.
        """
        status_code = 200 if enforcer.is_healthy else 503
        
        return JSONResponse(
            status_code=status_code,
            content={
                'status': 'healthy' if enforcer.is_healthy else 'unhealthy',
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'last_check': enforcer.last_check_time.isoformat() + 'Z' if enforcer.last_check_time else None,
                'checks': [asdict(r) for r in enforcer.last_results],
            }
        )
    
    @app.get('/health/detailed')
    async def health_detailed() -> JSONResponse:
        """Detailed health report with full check results."""
        return JSONResponse(
            status_code=200,
            content={
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'overall_health': 'healthy' if enforcer.is_healthy else 'unhealthy',
                'last_check': enforcer.last_check_time.isoformat() + 'Z' if enforcer.last_check_time else None,
                'checks': [asdict(r) for r in enforcer.last_results],
                'config': {
                    'check_interval_seconds': config.check_interval,
                    'expected_containers': config.expected_containers,
                }
            }
        )
    
    @app.get('/metrics')
    async def metrics() -> Response:
        """Prometheus-compatible metrics endpoint."""
        lines = [
            '# HELP enforcer_healthy Overall system health (1=healthy, 0=unhealthy)',
            '# TYPE enforcer_healthy gauge',
            f'enforcer_healthy {1 if enforcer.is_healthy else 0}',
            '',
            '# HELP enforcer_checks_total Number of checks in last cycle',
            '# TYPE enforcer_checks_total gauge',
            f'enforcer_checks_total {len(enforcer.last_results)}',
        ]
        
        # Add per-check metrics
        for result in enforcer.last_results:
            status_value = 1 if result.status == 'pass' else 0
            safe_name = result.name.replace('-', '_')
            lines.extend([
                f'enforcer_check_status{{check="{safe_name}"}} {status_value}',
                f'enforcer_check_duration_ms{{check="{safe_name}"}} {result.duration_ms}',
            ])
        
        return Response(
            content='\n'.join(lines) + '\n',
            media_type='text/plain'
        )
    
    return app


# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Main entry point."""
    config = EnforcerConfig()
    logger = setup_logging(config)
    
    enforcer = EnforcerEngine(config, logger)
    app = create_app(config, enforcer)
    
    # Handle graceful shutdown
    def handle_shutdown(sig, frame):
        logger.info(f'Received signal {sig}, shutting down...')
        enforcer.stop()
    
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    # Start check loop in background
    check_task = asyncio.create_task(enforcer.start_check_loop())
    
    # Run FastAPI server
    config_dict = {
        'app': app,
        'host': '0.0.0.0',
        'port': 8000,
        'log_level': config.log_level.lower(),
    }
    
    server = uvicorn.Server(uvicorn.Config(**config_dict))
    
    try:
        await server.serve()
    except asyncio.CancelledError:
        pass
    finally:
        enforcer.stop()
        await asyncio.gather(check_task, return_exceptions=True)
        logger.info('Enforcer stopped')


if __name__ == '__main__':
    asyncio.run(main())
