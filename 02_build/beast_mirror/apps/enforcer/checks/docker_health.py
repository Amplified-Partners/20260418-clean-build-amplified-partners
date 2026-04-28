"""Docker container health checks."""

import asyncio
import json
from dataclasses import dataclass
from typing import Dict, Any, List
from datetime import datetime

try:
    import docker
    from docker.errors import DockerException
except ImportError:
    docker = None


@dataclass
class DockerCheckResult:
    """Result of Docker health check."""
    name: str
    status: str  # "pass", "warn", "fail"
    message: str
    severity: str  # "info", "warning", "critical"
    timestamp: str
    duration_ms: float
    details: Dict[str, Any]


async def check_docker_health(expected_containers: List[str]) -> DockerCheckResult:
    """
    Check that all expected Docker containers are running.
    
    Args:
        expected_containers: List of container names to check (e.g., ['traefik', 'postgres'])
    
    Returns:
        DockerCheckResult with status and details
    """
    start = datetime.utcnow()
    
    if not docker:
        return DockerCheckResult(
            name='docker_health',
            status='fail',
            message='Docker client library not available',
            severity='critical',
            timestamp=datetime.utcnow().isoformat() + 'Z',
            duration_ms=0,
            details={'error': 'docker-py not installed'}
        )
    
    try:
        # Connect to Docker daemon via socket
        client = docker.from_env()
        
        # Get all running containers
        running = client.containers.list()
        running_names = {c.name for c in running}
        
        # Check expected containers
        missing = []
        unhealthy = []
        
        for container_name in expected_containers:
            if container_name not in running_names:
                missing.append(container_name)
            else:
                # Check container health
                container = client.containers.get(container_name)
                if container.status != 'running':
                    unhealthy.append(f'{container_name}:{container.status}')
        
        # Determine status
        if missing or unhealthy:
            issues = []
            if missing:
                issues.append(f"missing: {', '.join(missing)}")
            if unhealthy:
                issues.append(f"unhealthy: {', '.join(unhealthy)}")
            
            return DockerCheckResult(
                name='docker_health',
                status='fail',
                message=f'Docker issues detected: {"; ".join(issues)}',
                severity='critical',
                timestamp=datetime.utcnow().isoformat() + 'Z',
                duration_ms=(datetime.utcnow() - start).total_seconds() * 1000,
                details={
                    'total_containers': len(running),
                    'expected': len(expected_containers),
                    'missing': missing,
                    'unhealthy': unhealthy,
                    'running_containers': list(running_names),
                }
            )
        
        return DockerCheckResult(
            name='docker_health',
            status='pass',
            message=f'All {len(expected_containers)} expected containers running',
            severity='info',
            timestamp=datetime.utcnow().isoformat() + 'Z',
            duration_ms=(datetime.utcnow() - start).total_seconds() * 1000,
            details={
                'total_containers': len(running),
                'expected': len(expected_containers),
                'running': list(running_names),
            }
        )
    
    except DockerException as e:
        return DockerCheckResult(
            name='docker_health',
            status='fail',
            message=f'Docker daemon connection failed: {str(e)}',
            severity='critical',
            timestamp=datetime.utcnow().isoformat() + 'Z',
            duration_ms=(datetime.utcnow() - start).total_seconds() * 1000,
            details={'error': str(e)}
        )
    except Exception as e:
        return DockerCheckResult(
            name='docker_health',
            status='fail',
            message=f'Docker check failed: {str(e)}',
            severity='critical',
            timestamp=datetime.utcnow().isoformat() + 'Z',
            duration_ms=(datetime.utcnow() - start).total_seconds() * 1000,
            details={'error': str(e)}
        )
