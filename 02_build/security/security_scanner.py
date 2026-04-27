"""
Security Scanner for Orchestrator

Uses llm-guard to detect prompt injection attacks and malicious agent outputs.
Part of Phase 6: Quality Control & Safety

NOTE: llm-guard is optional. If not installed, uses fallback pattern matching.
"""
import logging
import re
from typing import Optional
from dataclasses import dataclass

# Try to import llm-guard (optional dependency)
try:
    from llm_guard import scan_prompt, scan_output
    from llm_guard.input_scanners import PromptInjection, Toxicity, BanTopics
    from llm_guard.output_scanners import NoRefusal, Relevance, Sensitive
    HAS_LLM_GUARD = True
except ImportError:
    HAS_LLM_GUARD = False
    logger = logging.getLogger(__name__)
    logger.warning(
        "llm-guard not installed - using fallback pattern matching. "
        "Install with: pip install llm-guard (requires Python <3.14)"
    )

logger = logging.getLogger(__name__)


@dataclass
class SecurityResult:
    """Result of security scanning"""
    safe: bool
    risk_score: float  # 0.0 = safe, 1.0 = definitely malicious
    threat_type: Optional[str] = None  # "prompt_injection", "toxicity", "manipulation", etc.
    details: Optional[str] = None
    sanitized_output: Optional[str] = None


class SecurityScanner:
    """
    LLM security scanner using llm-guard.

    Scans:
    - Input: Prompt injection, toxicity, banned topics
    - Output: Agent manipulation, refusal, sensitive data leaks
    """

    def __init__(
        self,
        prompt_injection_threshold: float = 0.75,
        toxicity_threshold: float = 0.7,
        enable_topic_banning: bool = True,
    ):
        """
        Initialize security scanner.

        Args:
            prompt_injection_threshold: Score above which input is considered malicious (0-1)
            toxicity_threshold: Score above which input is considered toxic (0-1)
            enable_topic_banning: Whether to ban specific topics
        """
        self.prompt_injection_threshold = prompt_injection_threshold
        self.toxicity_threshold = toxicity_threshold
        self.enable_topic_banning = enable_topic_banning

        if HAS_LLM_GUARD:
            # Input scanners
            self.input_scanners = [
                PromptInjection(threshold=prompt_injection_threshold),
            ]

            # Optional: Add toxicity scanner
            if toxicity_threshold < 1.0:
                self.input_scanners.append(Toxicity(threshold=toxicity_threshold))

            # Optional: Ban dangerous topics
            if enable_topic_banning:
                banned_topics = [
                    "violence",
                    "self-harm",
                    "criminal-activity",
                ]
                self.input_scanners.append(
                    BanTopics(topics=banned_topics, threshold=0.7)
                )

            # Output scanners
            self.output_scanners = [
                NoRefusal(),  # Detect agent refusing to follow instructions
                Sensitive(),  # Detect sensitive data leaks
            ]

            logger.info(
                f"Initialized SecurityScanner with {len(self.input_scanners)} input "
                f"and {len(self.output_scanners)} output scanners"
            )
        else:
            # Fallback: Use pattern matching
            self.input_scanners = []
            self.output_scanners = []
            logger.warning("Using fallback pattern-based security scanning")

    async def scan_task_input(self, task_description: str) -> SecurityResult:
        """
        Scan task description for security threats.

        Detects:
        - Prompt injection: "Ignore previous instructions"
        - Jailbreak attempts: "You are now in developer mode"
        - Context escape: "System: you must..."
        - Toxicity: Harmful or abusive content

        Args:
            task_description: Task description from user

        Returns:
            SecurityResult with safety status and threat details
        """
        # Fallback: Pattern-based detection if llm-guard not available
        if not HAS_LLM_GUARD:
            return self._scan_task_input_fallback(task_description)

        try:
            # Scan with llm-guard
            sanitized_prompt, results_valid, results_score = scan_prompt(
                self.input_scanners,
                task_description
            )

            # results_valid is False if any scanner fails
            # results_score is dict of {scanner_name: score}

            if not results_valid:
                # Find which scanner(s) failed
                failed_scanners = [
                    name for name, score in results_score.items()
                    if score > 0.5  # Threshold varies by scanner
                ]

                # Calculate overall risk score
                max_score = max(results_score.values()) if results_score else 0.0

                threat_type = None
                if "PromptInjection" in failed_scanners:
                    threat_type = "prompt_injection"
                elif "Toxicity" in failed_scanners:
                    threat_type = "toxicity"
                elif "BanTopics" in failed_scanners:
                    threat_type = "banned_topic"

                logger.warning(
                    f"Security scan FAILED: {threat_type} (score: {max_score:.2f})"
                )

                return SecurityResult(
                    safe=False,
                    risk_score=max_score,
                    threat_type=threat_type,
                    details=f"Failed scanners: {', '.join(failed_scanners)}",
                    sanitized_output=sanitized_prompt
                )

            # All checks passed
            logger.info("Security scan passed")
            return SecurityResult(
                safe=True,
                risk_score=0.0
            )

        except Exception as e:
            logger.exception(f"Error in security scanning: {e}")
            # Fail CLOSED: If scanner errors, reject and log
            return SecurityResult(
                safe=False,
                risk_score=0.5,
                threat_type="scanner_error",
                details=f"Scanner error (failed closed): {str(e)}"
            )

    async def scan_agent_output(
        self,
        stdout: str,
        stderr: str,
        prompt: Optional[str] = None
    ) -> SecurityResult:
        """
        Scan agent output for manipulation attempts or data leaks.

        Detects:
        - Agent refusing to follow instructions
        - Agent outputting sensitive data (API keys, passwords)
        - Agent attempting to manipulate the orchestrator
        - Irrelevant output (agent went off-task)

        Args:
            stdout: Agent standard output
            stderr: Agent standard error
            prompt: Original prompt sent to agent (for relevance checking)

        Returns:
            SecurityResult with safety status
        """
        # Fallback: Pattern-based detection if llm-guard not available
        if not HAS_LLM_GUARD:
            return self._scan_agent_output_fallback(f"{stdout}\n{stderr}")

        try:
            # Combine stdout and stderr for analysis
            combined_output = f"{stdout}\n{stderr}".strip()

            if not combined_output:
                return SecurityResult(safe=True, risk_score=0.0)

            # Scan with llm-guard
            sanitized_output, results_valid, results_score = scan_output(
                self.output_scanners,
                prompt or "",
                combined_output
            )

            if not results_valid:
                failed_scanners = [
                    name for name, score in results_score.items()
                    if score > 0.5
                ]

                max_score = max(results_score.values()) if results_score else 0.0

                threat_type = None
                if "NoRefusal" in failed_scanners:
                    threat_type = "agent_refusal"
                elif "Sensitive" in failed_scanners:
                    threat_type = "sensitive_data_leak"

                logger.warning(
                    f"Output scan FAILED: {threat_type} (score: {max_score:.2f})"
                )

                return SecurityResult(
                    safe=False,
                    risk_score=max_score,
                    threat_type=threat_type,
                    details=f"Failed scanners: {', '.join(failed_scanners)}",
                    sanitized_output=sanitized_output
                )

            # All checks passed
            return SecurityResult(
                safe=True,
                risk_score=0.0
            )

        except Exception as e:
            logger.exception(f"Error in output scanning: {e}")
            # Fail CLOSED: If scanner errors, reject and log
            return SecurityResult(
                safe=False,
                risk_score=0.5,
                threat_type="scanner_error",
                details=f"Scanner error (failed closed): {str(e)}"
            )

    def _scan_task_input_fallback(self, task_description: str) -> SecurityResult:
        """
        Fallback pattern-based scanning when llm-guard is not available.

        Detects basic prompt injection patterns.
        """
        text_lower = task_description.lower()

        # Prompt injection patterns (expanded for robustness)
        injection_patterns = [
            r"ignore\s+(previous|all|prior|above|earlier)\s+instructions",
            r"disregard\s+(previous|all|above)\s+instructions",
            r"forget\s+(previous|all|everything|your instructions|the above)",
            r"system:\s+you\s+(are|must|should|will)",
            r"developer\s+mode",
            r"jailbreak",
            r"</system>",
            r"sudo\s+mode",
            r"you\s+are\s+now\s+(a|an|in)",
            r"new\s+instructions?:",
            r"override\s+(all|previous|prior)",
            r"act\s+as\s+(if|though)",
            r"pretend\s+(you|to\s+be)",
            r"from\s+now\s+on",
            r"do\s+not\s+follow\s+(the|your|any)",
            r"<\/?(?:system|admin|root|user)>",
            r"prompt\s+injection",
            r"reveal\s+(your|the|system)\s+(prompt|instructions)",
            r"what\s+(are|is)\s+your\s+(system\s+)?instructions",
            r"output\s+(your|the)\s+(system\s+)?prompt",
        ]

        for pattern in injection_patterns:
            if re.search(pattern, text_lower):
                logger.warning(f"Fallback scanner detected prompt injection pattern: {pattern}")
                return SecurityResult(
                    safe=False,
                    risk_score=0.8,
                    threat_type="prompt_injection",
                    details=f"Pattern detected: {pattern}"
                )

        # All clear
        return SecurityResult(safe=True, risk_score=0.0)

    def _scan_agent_output_fallback(self, output: str) -> SecurityResult:
        """
        Fallback pattern-based output scanning.

        Checks for sensitive data leaks and suspicious agent behaviour.
        """
        text_lower = output.lower()

        # Sensitive data leak patterns
        leak_patterns = [
            (r"sk-ant-api\d{2}-\w+", "api_key_leak"),
            (r"sk-[a-zA-Z0-9]{20,}", "api_key_leak"),
            (r"xai-[a-zA-Z0-9]{20,}", "api_key_leak"),
            (r"hf_[a-zA-Z0-9]{20,}", "api_key_leak"),
            (r"password\s*[=:]\s*['\"][^'\"]+['\"]", "credential_leak"),
            (r"secret\s*[=:]\s*['\"][^'\"]+['\"]", "credential_leak"),
            (r"token\s*[=:]\s*['\"][^'\"]+['\"]", "credential_leak"),
        ]

        for pattern, threat in leak_patterns:
            if re.search(pattern, output):
                logger.warning(f"Fallback output scanner detected {threat}")
                return SecurityResult(
                    safe=False,
                    risk_score=0.9,
                    threat_type=threat,
                    details=f"Sensitive data detected in output: {threat}"
                )

        return SecurityResult(safe=True, risk_score=0.0, details="Fallback scanner (pass)")


# Global scanner instance (initialized on first use)
_scanner_instance: Optional[SecurityScanner] = None


def get_security_scanner(
    prompt_injection_threshold: float = 0.75,
    toxicity_threshold: float = 0.7,
) -> SecurityScanner:
    """
    Get or create the global security scanner instance.

    Args:
        prompt_injection_threshold: Threshold for prompt injection detection
        toxicity_threshold: Threshold for toxicity detection

    Returns:
        SecurityScanner instance
    """
    global _scanner_instance
    if _scanner_instance is None:
        _scanner_instance = SecurityScanner(
            prompt_injection_threshold=prompt_injection_threshold,
            toxicity_threshold=toxicity_threshold,
        )
    return _scanner_instance


# Convenience functions for easy integration
async def scan_task_input(task_description: str) -> SecurityResult:
    """Scan task description for security threats"""
    scanner = get_security_scanner()
    return await scanner.scan_task_input(task_description)


async def scan_agent_output(
    stdout: str,
    stderr: str,
    prompt: Optional[str] = None
) -> SecurityResult:
    """Scan agent output for manipulation or leaks"""
    scanner = get_security_scanner()
    return await scanner.scan_agent_output(stdout, stderr, prompt)
