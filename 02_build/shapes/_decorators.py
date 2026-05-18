"""
Decorators for the Huf Haus shape system.

These are the Huf Haus pre-wires — the pipes and electrics already in the wall.
Each decorator is baked into the shape template. Zero extra work on site.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
Source architect: Ewan Bramley (monitoring doctrine, 2026-05-17)
"""

from __future__ import annotations

import dataclasses
import datetime as dt
import functools
import uuid
import hashlib
import json
import logging
import threading
import time
from collections import defaultdict
from typing import Any

from ._types import GuardHalt, ShapeError, TrafficLight

log = logging.getLogger("amplified.shapes")


# ---------------------------------------------------------------------------
# Telemetry storage — thread-safe, in-memory for reference implementation
# ---------------------------------------------------------------------------


class _MetricsStore:
    """Thread-safe metrics accumulator. Production replaces with Vellum sink."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.timings: dict[str, list[float]] = defaultdict(list)
        self.call_counts: dict[str, int] = defaultdict(int)
        self.error_counts: dict[str, int] = defaultdict(int)
        self.last_error: dict[str, str] = {}

    def record_call(self, name: str, duration: float, error: str | None = None) -> None:
        with self._lock:
            self.timings[name].append(duration)
            self.call_counts[name] += 1
            if error:
                self.error_counts[name] += 1
                self.last_error[name] = error

    def get_stats(self, name: str) -> dict[str, Any]:
        with self._lock:
            times = self.timings.get(name, [])
            return {
                "call_count": self.call_counts.get(name, 0),
                "error_count": self.error_counts.get(name, 0),
                "avg_time": sum(times) / len(times) if times else 0.0,
                "max_time": max(times) if times else 0.0,
                "last_error": self.last_error.get(name),
            }


METRICS = _MetricsStore()


# ---------------------------------------------------------------------------
# @monitored — tracks timing, call count, error rate
# ---------------------------------------------------------------------------


def monitored(fn: Any) -> Any:
    """Baked-in monitoring. Tracks timing, call frequency, error rate.

    The wall arrives with the sensor in it. No extra work on site.
    Signals route through the metrics store → Vellum (reader-first).
    """

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        name = f"{fn.__qualname__}"
        start = time.monotonic()
        error_msg = None
        try:
            result = fn(*args, **kwargs)
            return result
        except Exception as exc:
            error_msg = str(exc)
            raise
        finally:
            duration = time.monotonic() - start
            METRICS.record_call(name, duration, error_msg)
            log.debug(
                "MONITOR %s: %.4fs%s",
                name,
                duration,
                f" ERROR: {error_msg}" if error_msg else "",
            )

    wrapper._monitored = True  # type: ignore[attr-defined]
    return wrapper


# ---------------------------------------------------------------------------
# @tracked — assigns tracking IDs
# ---------------------------------------------------------------------------


def tracked(fn: Any) -> Any:
    """Assigns a tracking ID to the operation. Every data movement is traceable."""

    import uuid

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        tracking_id = str(uuid.uuid4())
        log.debug("TRACK %s: tracking_id=%s", fn.__qualname__, tracking_id)
        # Inject tracking_id into kwargs if the function accepts it
        import inspect

        sig = inspect.signature(fn)
        if "tracking_id" in sig.parameters:
            kwargs["tracking_id"] = tracking_id
        result = fn(*args, **kwargs)
        return result

    wrapper._tracked = True  # type: ignore[attr-defined]
    return wrapper


# ---------------------------------------------------------------------------
# @validated — validates input against model
# ---------------------------------------------------------------------------


def validated(fn: Any) -> Any:
    """Validates input before processing. Shape, not content — content is the guard's job."""

    @functools.wraps(fn)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        input_model = getattr(self, "input_model", None)
        if input_model is not None and args:
            raw = args[0]
            if isinstance(raw, (bytes, str)):
                log.debug("VALIDATE %s: raw input, schema check deferred to parse", fn.__qualname__)
            elif hasattr(input_model, "__dataclass_fields__"):
                if not isinstance(raw, input_model):
                    raise ShapeError(
                        f"Input type mismatch: expected {input_model.__name__}, "
                        f"got {type(raw).__name__}",
                        shape_kind="entry",
                    )
        return fn(self, *args, **kwargs)

    wrapper._validated = True  # type: ignore[attr-defined]
    return wrapper


# ---------------------------------------------------------------------------
# @retryable — retry with exponential backoff
# ---------------------------------------------------------------------------


def retryable(
    max_retries: int = 3,
    backoff_base: float = 1.0,
    retriable_exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Any:
    """Retry with exponential backoff. Workers and connectors wear this.

    Can be used as @retryable or @retryable(max_retries=5).
    """

    def decorator(fn: Any) -> Any:
        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: Exception | None = None
            for attempt in range(max_retries + 1):
                try:
                    return fn(*args, **kwargs)
                except retriable_exceptions as exc:
                    last_exc = exc
                    if attempt < max_retries:
                        wait = backoff_base * (2**attempt)
                        log.warning(
                            "RETRY %s: attempt %d/%d, waiting %.1fs: %s",
                            fn.__qualname__,
                            attempt + 1,
                            max_retries,
                            wait,
                            exc,
                        )
                        time.sleep(wait)
            raise last_exc  # type: ignore[misc]

        wrapper._retryable = True  # type: ignore[attr-defined]
        wrapper._max_retries = max_retries  # type: ignore[attr-defined]
        return wrapper

    # Allow @retryable without parentheses
    if callable(max_retries):
        fn = max_retries
        max_retries = 3
        return decorator(fn)

    return decorator


# ---------------------------------------------------------------------------
# @circuit_breaker — fail-open after N consecutive failures
# ---------------------------------------------------------------------------


def circuit_breaker(threshold: int = 5, reset_timeout: float = 60.0) -> Any:
    """Circuit breaker for connectors. Stops calling a failing external system.

    After `threshold` consecutive failures, the circuit opens for `reset_timeout` seconds.
    Can be used as @circuit_breaker or @circuit_breaker(threshold=10).
    """

    def decorator(fn: Any) -> Any:
        _failures = {"count": 0, "open_until": 0.0}
        _lock = threading.Lock()

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with _lock:
                if _failures["open_until"] > time.monotonic():
                    from ._types import ConnectorError

                    raise ConnectorError(
                        f"Circuit breaker OPEN for {fn.__qualname__}. "
                        f"Resets in {_failures['open_until'] - time.monotonic():.0f}s",
                        retry_eligible=False,
                    )

            try:
                result = fn(*args, **kwargs)
                with _lock:
                    _failures["count"] = 0
                return result
            except Exception as exc:
                with _lock:
                    _failures["count"] += 1
                    if _failures["count"] >= threshold:
                        _failures["open_until"] = time.monotonic() + reset_timeout
                        log.error(
                            "CIRCUIT OPEN %s: %d consecutive failures, open for %.0fs",
                            fn.__qualname__,
                            _failures["count"],
                            reset_timeout,
                        )
                raise

        wrapper._circuit_breaker = True  # type: ignore[attr-defined]
        return wrapper

    if callable(threshold):
        fn = threshold
        threshold = 5
        return decorator(fn)

    return decorator


# ---------------------------------------------------------------------------
# @no_bypass — prevents any override/skip mechanism on guards
# ---------------------------------------------------------------------------


def no_bypass(cls: type) -> type:
    """Class decorator for guards. There is no admin mode, no debug flag, no skip.

    Vellum records every accept and reject. The record is the evidence.
    """

    original_init = cls.__init__ if hasattr(cls, "__init__") else None

    def guarded_init(self: Any, *args: Any, **kwargs: Any) -> None:
        if kwargs.pop("skip_validation", False):
            raise GuardHalt(
                f"{cls.__name__}: @no_bypass — skip_validation is forbidden. "
                "There is no admin mode. There is no debug flag.",
            )
        if kwargs.pop("bypass", False):
            raise GuardHalt(
                f"{cls.__name__}: @no_bypass — bypass is forbidden.",
            )
        if original_init and original_init is not object.__init__:
            original_init(self, *args, **kwargs)

    cls.__init__ = guarded_init
    cls._no_bypass = True  # type: ignore[attr-defined]
    return cls


# ---------------------------------------------------------------------------
# @epistemic — declares epistemic tier for services and scorers
# ---------------------------------------------------------------------------


def epistemic(
    tier: str = "intuited",
    canon_ref: str = "",
    protected: str | list[str] | None = None,
    strict: bool = False,
) -> Any:
    """Declares the epistemic tier of a shape's output.

    tier: intuited | structured | measured | proven
    canon_ref: reference to the Logic Canon method, if any
    protected: method name(s) to wrap with runtime epistemic enforcement.
        None = metadata only (backward compatible, no runtime enforcement).
    strict: if True, bare values at protected boundary raise P0.
        if False (default), bare values auto-wrap as INTUITED with provenance note.
    """

    def decorator(cls: type) -> type:
        cls._epistemic_tier = tier  # type: ignore[attr-defined]
        cls._canon_ref = canon_ref  # type: ignore[attr-defined]
        cls._epistemic_strict = strict  # type: ignore[attr-defined]

        if protected is not None:
            methods = [protected] if isinstance(protected, str) else protected
            cls._epistemic_protected = tuple(methods)  # type: ignore[attr-defined]
            _wire_enforcement(cls, methods, tier, strict)
        else:
            cls._epistemic_protected = ()  # type: ignore[attr-defined]

        return cls

    return decorator


def _wire_enforcement(
    cls: type, methods: list[str], declared_tier: str, strict: bool
) -> None:
    """Wrap protected methods with epistemic boundary enforcement."""
    from ._epistemic import (
        EpistemicTier,
        PreconditionCheck,
        ShapeProvenance,
        StatusedOutput,
        ShapeAuditRecord,
        SHAPE_AUDIT_LOG,
        _demote,
    )
    from ._types import EpistemicViolation

    tier_enum = EpistemicTier.from_string(declared_tier)

    # We defer wrapping to __init_subclass__ time won't work here because
    # the class is being constructed. Instead we use __init_subclass__ hook
    # via a sentinel, OR we wrap directly on the class after definition.
    # Since @epistemic is a class decorator applied AFTER the class body,
    # we can wrap methods directly.

    for method_name in methods:
        original = getattr(cls, method_name, None)
        if original is None:
            continue

        def make_wrapper(orig_fn, m_name):
            @functools.wraps(orig_fn)
            def wrapper(self, *args, **kwargs):
                shape_name = type(self).__qualname__

                # 1. Collect input statuses from StatusedOutput args
                input_statuses: list[EpistemicTier] = []
                input_ids: list[str] = []
                unwrapped_args = []

                for arg in args:
                    if isinstance(arg, StatusedOutput):
                        input_statuses.append(arg.status)
                        input_ids.append(arg.output_id)
                        unwrapped_args.append(arg.value)
                    elif strict:
                        raise EpistemicViolation(
                            f"{shape_name}.{m_name}: bare value at protected boundary "
                            f"(type={type(arg).__name__}). All inputs to enforced "
                            "boundaries must be StatusedOutput. This is the laundering trap.",
                            declared_tier=declared_tier,
                            effective_tier="",
                            violation_type="bare_value",
                            shape_name=shape_name,
                            boundary_method=m_name,
                        )
                    else:
                        # Lenient mode: auto-wrap as INTUITED
                        input_statuses.append(EpistemicTier.INTUITED)
                        auto_id = str(uuid.uuid4())
                        input_ids.append(auto_id)
                        unwrapped_args.append(arg)

                # Unwrap StatusedOutput kwargs too
                unwrapped_kwargs = {}
                for k, v in kwargs.items():
                    if isinstance(v, StatusedOutput):
                        input_statuses.append(v.status)
                        input_ids.append(v.output_id)
                        unwrapped_kwargs[k] = v.value
                    elif strict and k != "tracking_id":
                        raise EpistemicViolation(
                            f"{shape_name}.{m_name}: bare kwarg '{k}' at protected boundary.",
                            declared_tier=declared_tier,
                            violation_type="bare_value",
                            shape_name=shape_name,
                            boundary_method=m_name,
                        )
                    else:
                        unwrapped_kwargs[k] = v

                # 2. Check for stale inputs (demote by one tier)
                for arg in args:
                    if isinstance(arg, StatusedOutput) and arg.is_stale():
                        idx = next(
                            i for i, a in enumerate(args) if a is arg
                        )
                        input_statuses[idx] = _demote(input_statuses[idx])

                # 3. Verify preconditions
                preconditions: tuple[PreconditionCheck, ...] = ()
                if hasattr(self, "verify_preconditions"):
                    preconditions = self.verify_preconditions()

                # 4. Apply min-rule
                input_floor = min(input_statuses, default=EpistemicTier.PROVEN)
                precondition_floor = (
                    tier_enum
                    if all(p.holds for p in preconditions)
                    else _demote(tier_enum)
                )
                effective = min(tier_enum, input_floor, precondition_floor)

                # 5. Check for over-claiming (gap >= 2 is P0)
                gap = tier_enum.value - effective.value
                if gap >= 2:
                    raise EpistemicViolation(
                        f"{shape_name}.{m_name}: declared {tier_enum.label()} but "
                        f"effective is {effective.label()}. Gap={gap} tiers (>= 2 = P0).",
                        declared_tier=declared_tier,
                        effective_tier=effective.label(),
                        violation_type="gap_exceeded",
                        shape_name=shape_name,
                        boundary_method=m_name,
                    )

                # 6. Execute the actual method
                raw_result = orig_fn(self, *unwrapped_args, **unwrapped_kwargs)

                # 7. Wrap output
                provenance = ShapeProvenance(
                    shape_name=shape_name,
                    method=m_name,
                    input_ids=tuple(input_ids),
                )
                output = StatusedOutput(
                    value=raw_result,
                    status=effective,
                    provenance=provenance,
                    preconditions=preconditions,
                )

                # 8. Write audit record
                import datetime as _dt

                SHAPE_AUDIT_LOG.write(
                    ShapeAuditRecord(
                        record_id=output.output_id,
                        timestamp=_dt.datetime.now(_dt.timezone.utc),
                        shape_name=shape_name,
                        method=m_name,
                        declared_status=tier_enum,
                        effective_status=effective,
                        input_statuses=tuple(input_statuses),
                        preconditions=preconditions,
                        reason=f"min({tier_enum.label()}, input_floor={input_floor.label()}, "
                               f"precondition_floor={precondition_floor.label()})",
                    )
                )

                return output

            return wrapper

        setattr(cls, method_name, make_wrapper(original, method_name))


# ---------------------------------------------------------------------------
# @reader_first — ensures output is formatted for the reader
# ---------------------------------------------------------------------------


def reader_first(cls: type) -> type:
    """Class decorator for agents. Output shaped for the reader, not the writer. Always."""

    cls._reader_first = True  # type: ignore[attr-defined]
    return cls


# ---------------------------------------------------------------------------
# @confidence_floor — rejects output below confidence threshold
# ---------------------------------------------------------------------------


def confidence_floor(minimum: float = 0.6) -> Any:
    """Class decorator for agents. Rejects output below confidence threshold."""

    def decorator(cls: type) -> type:
        cls._confidence_floor = minimum  # type: ignore[attr-defined]
        return cls

    return decorator


# ---------------------------------------------------------------------------
# @hash_protected — hashes specified fields to detect silent corruption
# ---------------------------------------------------------------------------


def hash_protected(preserve: str = "header") -> Any:
    """Method decorator for pipelines. Protect the label, work the specimen.

    Hashes the specified field before processing, verifies after.
    If the hash doesn't match, the pipeline stops.
    """

    def decorator(fn: Any) -> Any:
        @functools.wraps(fn)
        def wrapper(self: Any, data: Any, *args: Any, **kwargs: Any) -> Any:
            field_value = getattr(data, preserve, None)
            if field_value is not None:
                original_hash = hashlib.sha256(
                    json.dumps(field_value, default=str, sort_keys=True).encode()
                ).hexdigest()
            else:
                original_hash = None

            result = fn(self, data, *args, **kwargs)

            if original_hash is not None:
                result_field = getattr(result, preserve, None)
                if result_field is not None:
                    result_hash = hashlib.sha256(
                        json.dumps(result_field, default=str, sort_keys=True).encode()
                    ).hexdigest()
                    if result_hash != original_hash:
                        from ._types import PipelineError

                        raise PipelineError(
                            f"Hash protection violation: '{preserve}' was modified. "
                            "Protect the label, work the specimen.",
                            step_failed=fn.__qualname__,
                        )
            return result

        wrapper._hash_protected = True  # type: ignore[attr-defined]
        wrapper._protected_field = preserve  # type: ignore[attr-defined]
        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# @transactional — wraps in transaction boundary
# ---------------------------------------------------------------------------


def transactional(fn: Any) -> Any:
    """Marks a store method as transactional. All writes are atomic."""

    @functools.wraps(fn)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        log.debug("TRANSACTION BEGIN: %s", fn.__qualname__)
        try:
            result = fn(self, *args, **kwargs)
            log.debug("TRANSACTION COMMIT: %s", fn.__qualname__)
            return result
        except Exception:
            log.debug("TRANSACTION ROLLBACK: %s", fn.__qualname__)
            raise

    wrapper._transactional = True  # type: ignore[attr-defined]
    return wrapper


# ---------------------------------------------------------------------------
# @debt_tracked — marks glue as acknowledged debt
# ---------------------------------------------------------------------------


def debt_tracked(
    reason: str = "",
    removal_condition: str = "",
    temporary: bool = True,
) -> Any:
    """Class decorator for glue shapes. Makes debt visible.

    Shows up in Vellum as acknowledged debt with a removal condition.
    When the condition is met, the glue lights up RED: 'delete me.'
    """

    def decorator(cls: type) -> type:
        cls._debt_tracked = True  # type: ignore[attr-defined]
        cls._debt_reason = reason  # type: ignore[attr-defined]
        cls._removal_condition = removal_condition  # type: ignore[attr-defined]
        cls._temporary = temporary  # type: ignore[attr-defined]
        cls._debt_created = dt.datetime.now(dt.timezone.utc).isoformat()  # type: ignore[attr-defined]
        return cls

    return decorator


# ---------------------------------------------------------------------------
# @step — pipeline step ordering
# ---------------------------------------------------------------------------


def step(order: int) -> Any:
    """Marks a method as a pipeline step with explicit ordering."""

    def decorator(fn: Any) -> Any:
        fn._step_order = order  # type: ignore[attr-defined]
        fn._is_step = True  # type: ignore[attr-defined]

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            return fn(*args, **kwargs)

        wrapper._step_order = order  # type: ignore[attr-defined]
        wrapper._is_step = True  # type: ignore[attr-defined]
        return wrapper

    return decorator


# ---------------------------------------------------------------------------
# @workflow — orchestrator workflow marker
# ---------------------------------------------------------------------------


def workflow(fn: Any) -> Any:
    """Marks a method as the orchestrator's main workflow entry point."""

    fn._is_workflow = True  # type: ignore[attr-defined]

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)

    wrapper._is_workflow = True  # type: ignore[attr-defined]
    return wrapper


# ---------------------------------------------------------------------------
# @signal_classifier — telemetry signal classification
# ---------------------------------------------------------------------------


def signal_classifier(fn: Any) -> Any:
    """Marks a method as a telemetry signal classifier."""

    fn._signal_classifier = True  # type: ignore[attr-defined]

    @functools.wraps(fn)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return fn(*args, **kwargs)

    wrapper._signal_classifier = True  # type: ignore[attr-defined]
    return wrapper


# ---------------------------------------------------------------------------
# field / setting / secret / metric — descriptor helpers
# ---------------------------------------------------------------------------


def field(
    required: bool = True,
    default: Any = dataclasses.MISSING,
    description: str = "",
    gt: float | None = None,
    min_length: int | None = None,
    **kwargs: Any,
) -> Any:
    """Model field descriptor. Documents and constrains a field."""

    metadata = {
        "required": required,
        "description": description,
        "gt": gt,
        "min_length": min_length,
        **kwargs,
    }
    if default is not dataclasses.MISSING:
        return dataclasses.field(default=default, metadata=metadata)
    if not required:
        return dataclasses.field(default=None, metadata=metadata)
    return dataclasses.field(metadata=metadata)


def setting(
    default: Any = dataclasses.MISSING,
    description: str = "",
    min_value: float | None = None,
    max_value: float | None = None,
) -> Any:
    """Config setting descriptor."""

    metadata = {
        "description": description,
        "min_value": min_value,
        "max_value": max_value,
        "source": "config",
    }
    if default is not dataclasses.MISSING:
        return dataclasses.field(default=default, metadata=metadata)
    return dataclasses.field(metadata=metadata)


def secret(env_var: str = "", description: str = "") -> Any:
    """Config secret descriptor. Secrets via env var reference, NEVER hardcoded."""

    return dataclasses.field(
        default="",
        metadata={
            "description": description,
            "env_var": env_var,
            "source": "secret",
            "secret": True,
        },
    )


def metric(
    type: str = "counter",
    description: str = "",
    buckets: list[float] | None = None,
) -> Any:
    """Telemetry metric descriptor."""

    return dataclasses.field(
        default=0,
        metadata={
            "metric_type": type,
            "description": description,
            "buckets": buckets,
        },
    )


# ---------------------------------------------------------------------------
# @spine — declares which Portable Spine principles a shape enforces
# ---------------------------------------------------------------------------


def spine(*principles: str) -> Any:
    """Declares which Portable Spine principles this shape structurally enforces.

    The nine principles are the boss. Not Ewan. Not any agent. Not any client.
    Every shape must declare at least one. Every principle must be covered
    by at least one shape. The registry verifies both at verification time.

    Usage:
        @spine("radical_honesty", "radical_transparency")
        class MyService(ServiceBase):
            ...
    """
    from ._types import SpinePrinciple

    resolved: tuple[SpinePrinciple, ...] = tuple(
        SpinePrinciple(p) for p in principles
    )
    if not resolved:
        from ._types import SpineViolation

        raise SpineViolation(
            "A shape with @spine() must declare at least one principle.",
            violation_type="empty_declaration",
        )

    def decorator(cls: type) -> type:
        cls._spine_principles = resolved  # type: ignore[attr-defined]
        return cls

    return decorator
