"""
Tests for the Huf Haus shape system.

Proves that every shape base class works: registration, contracts,
decorators, error handling, and the registry.

Authored by Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1
"""

from __future__ import annotations

import dataclasses
import sys
import os
import time
import unittest

# Ensure the shapes package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from shapes import (
    AgentBase,
    AgentError,
    ConfigBase,
    ConfigError,
    ConnectorBase,
    ConnectorError,
    EntryBase,
    EntryError,
    GlueBase,
    GuardBase,
    GuardHalt,
    ModelBase,
    OrchestratorBase,
    PipelineBase,
    PipelineError,
    ScorerBase,
    ServiceBase,
    ShapeKind,
    StoreBase,
    TelemetryBase,
    TestBase,
    TrafficLight,
    ValidatedInput,
    WorkerBase,
    WorkerResult,
    WorkflowResult,
    REGISTRY,
    METRICS,
    monitored,
    tracked,
    validated,
    retryable,
    circuit_breaker,
    no_bypass,
    epistemic,
    reader_first,
    confidence_floor,
    hash_protected,
    transactional,
    debt_tracked,
    step,
    workflow,
    signal_classifier,
    field,
    setting,
    secret,
)


# ===================================================================
# Concrete implementations for testing
# ===================================================================


@dataclasses.dataclass
class SampleInput:
    name: str
    value: int


class SampleEntry(EntryBase):
    source = "test"
    auth = "none"
    rate_limit = "100/min"
    input_model = SampleInput

    @monitored
    @validated
    def receive(self, raw: bytes) -> ValidatedInput:
        parsed = self.parse(raw)
        ctx = self.tracking_context()
        return ValidatedInput(
            data=parsed,
            tracking_id=ctx.tracking_id,
            received_at=ctx.received_at,
            input_hash=self.hash(parsed),
        )


@epistemic(tier="structured", canon_ref="threshold_detection")
class SampleService(ServiceBase):
    input_model = SampleInput
    output_model = dict

    @monitored
    def execute(self, input_data: SampleInput) -> dict:
        return {"result": input_data.value * 2, "name": input_data.name}


class SampleWorker(WorkerBase):
    task_source = "test_queue"
    retry_policy = "3x_exponential"
    timeout = "1m"
    concurrency = 2

    @monitored
    def execute(self, task: dict) -> WorkerResult:
        return WorkerResult(
            status="complete",
            processed=1,
            tracking_id=self.generate_id(),
        )


class SampleConnector(ConnectorBase):
    external_system = "test_api"
    auth = "api_key"
    rate_limit = "60/min"
    timeout = "10s"
    circuit_breaker_threshold = 3

    @monitored
    @circuit_breaker(threshold=3, reset_timeout=0.1)
    def to_internal(self, raw: dict) -> SampleInput:
        return SampleInput(name=raw["name"], value=raw["value"])

    def to_external(self, internal: SampleInput) -> dict:
        return {"name": internal.name, "value": internal.value}


@dataclasses.dataclass
class SampleModel(ModelBase):
    name: str = field(required=True, description="The entity name", min_length=1)
    value: int = field(required=True, description="The entity value", gt=0)
    version = 1


class SampleStore(StoreBase):
    engine = "memory"
    model = SampleInput
    table = "samples"

    def __init__(self) -> None:
        super().__init__()
        self._data: dict[str, SampleInput] = {}

    @transactional
    def insert(self, record: SampleInput) -> str:
        record_id = self.generate_id()
        self._data[record_id] = record
        return record_id

    def get_by_id(self, record_id: str) -> SampleInput | None:
        return self._data.get(record_id)

    def query(self, where: str, **params) -> list[SampleInput]:
        return list(self._data.values())


class SamplePipeline(PipelineBase):
    input_model = dict
    output_model = dict

    @step(order=1)
    def normalise(self, data: dict) -> dict:
        return {k.lower(): v for k, v in data.items()}

    @step(order=2)
    def enrich(self, data: dict) -> dict:
        data["enriched"] = True
        return data

    @step(order=3)
    def validate_output(self, data: dict) -> dict:
        if "enriched" not in data:
            raise PipelineError("Missing enrichment")
        return data


class SampleOrchestrator(OrchestratorBase):
    trigger = "test"
    timeout = "1m"

    @workflow
    def run(self, context: dict) -> WorkflowResult:
        result1 = self.call(lambda x: x * 2, context.get("value", 1))
        result2 = self.call(lambda x: x + 10, result1)
        return WorkflowResult(
            status="complete",
            steps_completed=self._steps_completed,
            steps_total=2,
            step_log=tuple(self._step_log),
        )


from shapes._types import Rule


@no_bypass
class SampleGuard(GuardBase):
    rules = [
        Rule(name="positive_value", severity="RED", check=lambda d: d.get("value", 0) > 0),
    ]

    def check(self, data: dict) -> dict:
        violations = self.evaluate_rules(data)
        if violations:
            self.log_reject("test", f"violations: {[r.name for r in violations]}")
            raise GuardHalt(
                f"Guard rejected: {[r.name for r in violations]}",
                violations=tuple(r.name for r in violations),
            )
        self.log_accept("test")
        return data


@epistemic(tier="measured", canon_ref="threshold_detection")
class SampleScorer(ScorerBase):
    input_model = dict
    output_range = (0.0, 1.0)
    formula_ref = "linear_threshold"
    green_threshold = 0.7
    amber_threshold = 0.4
    red_threshold = 0.2

    @monitored
    def score(self, input_data: dict) -> dict:
        value = input_data.get("value", 0)
        normalised = min(1.0, max(0.0, value / 100.0))
        return {
            "score": normalised,
            "status": self.threshold_status(normalised),
            "working": f"{value}/100",
        }


@reader_first
@confidence_floor(minimum=0.5)
class SampleAgent(AgentBase):
    purpose = "classify"
    model = "test:mock"
    reader_profile = "developer"

    @monitored
    def interpret(self, input_data: dict, reader=None) -> dict:
        confidence = 0.8
        self.validate_confidence(confidence)
        return {
            "classification": "positive" if input_data.get("value", 0) > 0 else "negative",
            "confidence": confidence,
            "reader": reader or self.reader_profile,
        }


@dataclasses.dataclass
class SampleConfig(ConfigBase):
    max_retries: int = setting(default=3, description="Maximum retry count", min_value=0, max_value=10)
    api_url: str = setting(default="http://localhost:8000", description="API endpoint")
    api_key: str = secret(env_var="TEST_API_KEY", description="API authentication key")


class SampleTelemetry(TelemetryBase):
    @signal_classifier
    def classify(self, metric_name: str):
        return super().classify(metric_name)


@debt_tracked(
    reason="SampleInput has no .to_dict(), SampleModel expects dict",
    removal_condition="SampleInput gets .to_dict() method",
    temporary=True,
)
class SampleGlue(GlueBase):
    source_shape = "SampleEntry"
    target_shape = "SampleService"
    mismatch_reason = "SampleInput has no .to_dict()"
    temporary = True
    removal_condition = "SampleInput gets .to_dict() method"

    def adapt(self, source_output: SampleInput) -> dict:
        return {"name": source_output.name, "value": source_output.value}


# ===================================================================
# Tests
# ===================================================================


class TestShapeRegistration(unittest.TestCase):
    """All shapes register themselves on subclass creation."""

    def test_all_fifteen_kinds_registered(self):
        registered = REGISTRY.get_all()
        registered_kinds = {e["kind"] for e in registered.values()}
        expected = {k.value for k in ShapeKind}
        missing = expected - registered_kinds
        self.assertEqual(missing, set(), f"Missing shape kinds in registry: {missing}")

    def test_count_by_kind(self):
        counts = REGISTRY.count_by_kind()
        for kind in ShapeKind:
            self.assertIn(
                kind.value,
                counts,
                f"Shape kind {kind.value} not found in registry counts",
            )

    def test_get_by_kind(self):
        entries = REGISTRY.get_by_kind(ShapeKind.ENTRY)
        self.assertTrue(len(entries) >= 1, "At least SampleEntry should be registered")
        names = [e["name"] for e in entries]
        self.assertIn("SampleEntry", names)


class TestEntryShape(unittest.TestCase):
    def test_receive_valid_json(self):
        entry = SampleEntry()
        result = entry.receive(b'{"name": "test", "value": 42}')
        self.assertIsInstance(result, ValidatedInput)
        self.assertEqual(result.data.name, "test")
        self.assertEqual(result.data.value, 42)
        self.assertTrue(len(result.tracking_id) > 0)

    def test_receive_invalid_json(self):
        entry = SampleEntry()
        with self.assertRaises(EntryError):
            entry.receive(b"not json")

    def test_shape_kind(self):
        self.assertEqual(SampleEntry.shape_kind, ShapeKind.ENTRY)

    def test_monitoring_recorded(self):
        entry = SampleEntry()
        entry.receive(b'{"name": "test", "value": 1}')
        stats = METRICS.get_stats("SampleEntry.receive")
        self.assertGreater(stats["call_count"], 0)


class TestServiceShape(unittest.TestCase):
    def test_execute(self):
        svc = SampleService()
        result = svc.execute(SampleInput(name="foo", value=5))
        self.assertEqual(result["result"], 10)
        self.assertEqual(result["name"], "foo")

    def test_epistemic_tier(self):
        self.assertEqual(SampleService._epistemic_tier, "structured")
        self.assertEqual(SampleService._canon_ref, "threshold_detection")

    def test_confidence(self):
        svc = SampleService()
        self.assertEqual(svc.confidence(), 0.6)


class TestWorkerShape(unittest.TestCase):
    def test_execute(self):
        worker = SampleWorker()
        result = worker.execute({"task": "do_something"})
        self.assertIsInstance(result, WorkerResult)
        self.assertEqual(result.status, "complete")
        self.assertEqual(result.processed, 1)

    def test_heartbeat(self):
        worker = SampleWorker()
        self.assertTrue(worker.heartbeat())


class TestConnectorShape(unittest.TestCase):
    def test_to_internal(self):
        conn = SampleConnector()
        result = conn.to_internal({"name": "test", "value": 99})
        self.assertIsInstance(result, SampleInput)
        self.assertEqual(result.name, "test")
        self.assertEqual(result.value, 99)

    def test_to_external(self):
        conn = SampleConnector()
        result = conn.to_external(SampleInput(name="test", value=99))
        self.assertEqual(result, {"name": "test", "value": 99})

    def test_circuit_breaker_opens(self):
        call_count = 0

        class FailingConnector(ConnectorBase):
            external_system = "failing"

            @circuit_breaker(threshold=2, reset_timeout=0.1)
            def to_internal(self, raw):
                nonlocal call_count
                call_count += 1
                raise ConnectorError("always fails")

        conn = FailingConnector()
        for _ in range(2):
            with self.assertRaises(ConnectorError):
                conn.to_internal({})

        with self.assertRaises(ConnectorError) as ctx:
            conn.to_internal({})
        self.assertIn("Circuit breaker OPEN", str(ctx.exception))

        time.sleep(0.15)
        with self.assertRaises(ConnectorError) as ctx:
            conn.to_internal({})
        self.assertNotIn("Circuit breaker OPEN", str(ctx.exception))


class TestModelShape(unittest.TestCase):
    def test_validate_passes(self):
        m = SampleModel(name="test", value=5)
        errors = m.validate()
        self.assertEqual(errors, [])

    def test_validate_fails_gt(self):
        m = SampleModel(name="test", value=0)
        errors = m.validate()
        self.assertTrue(any("must be >" in e for e in errors))

    def test_validate_fails_min_length(self):
        m = SampleModel(name="", value=5)
        errors = m.validate()
        self.assertTrue(any("must be >=" in e for e in errors))

    def test_to_dict(self):
        m = SampleModel(name="test", value=5)
        d = m.to_dict()
        self.assertEqual(d["name"], "test")
        self.assertEqual(d["value"], 5)

    def test_field_descriptions(self):
        descs = SampleModel.field_descriptions()
        self.assertEqual(descs["name"], "The entity name")
        self.assertEqual(descs["value"], "The entity value")


class TestStoreShape(unittest.TestCase):
    def test_insert_and_get(self):
        store = SampleStore()
        record = SampleInput(name="test", value=42)
        record_id = store.insert(record)
        self.assertTrue(len(record_id) > 0)
        retrieved = store.get_by_id(record_id)
        self.assertEqual(retrieved, record)

    def test_query(self):
        store = SampleStore()
        store.insert(SampleInput(name="a", value=1))
        store.insert(SampleInput(name="b", value=2))
        results = store.query("all")
        self.assertEqual(len(results), 2)


class TestPipelineShape(unittest.TestCase):
    def test_run_all_steps(self):
        pipe = SamplePipeline()
        result = pipe.run({"Name": "Test", "Value": 42})
        self.assertEqual(result["name"], "Test")
        self.assertEqual(result["value"], 42)
        self.assertTrue(result["enriched"])

    def test_step_order(self):
        pipe = SamplePipeline()
        steps = pipe._get_ordered_steps()
        self.assertEqual(len(steps), 3)
        self.assertEqual(steps[0][0], "normalise")
        self.assertEqual(steps[1][0], "enrich")
        self.assertEqual(steps[2][0], "validate_output")


class TestOrchestratorShape(unittest.TestCase):
    def test_run_workflow(self):
        orch = SampleOrchestrator()
        result = orch.run({"value": 5})
        self.assertIsInstance(result, WorkflowResult)
        self.assertEqual(result.status, "complete")
        self.assertEqual(result.steps_completed, 2)
        self.assertEqual(result.steps_total, 2)

    def test_step_log(self):
        orch = SampleOrchestrator()
        result = orch.run({"value": 3})
        self.assertEqual(len(result.step_log), 2)


class TestGuardShape(unittest.TestCase):
    def test_accepts_valid(self):
        guard = SampleGuard()
        result = guard.check({"value": 10})
        self.assertEqual(result, {"value": 10})

    def test_rejects_invalid(self):
        guard = SampleGuard()
        with self.assertRaises(GuardHalt) as ctx:
            guard.check({"value": -1})
        self.assertIn("positive_value", ctx.exception.violations)

    def test_no_bypass(self):
        with self.assertRaises(GuardHalt):
            SampleGuard(skip_validation=True)

        with self.assertRaises(GuardHalt):
            SampleGuard(bypass=True)

    def test_no_bypass_allows_false(self):
        guard = SampleGuard(skip_validation=False)
        self.assertIsNotNone(guard)


class TestScorerShape(unittest.TestCase):
    def test_score_high(self):
        scorer = SampleScorer()
        result = scorer.score({"value": 80})
        self.assertEqual(result["status"], "GREEN")
        self.assertAlmostEqual(result["score"], 0.8)

    def test_score_medium(self):
        scorer = SampleScorer()
        result = scorer.score({"value": 50})
        self.assertEqual(result["status"], "AMBER")

    def test_score_low(self):
        scorer = SampleScorer()
        result = scorer.score({"value": 25})
        self.assertEqual(result["status"], "RED")

    def test_score_critical(self):
        scorer = SampleScorer()
        result = scorer.score({"value": 0})
        self.assertEqual(result["status"], "BLACK")

    def test_epistemic_tier(self):
        self.assertEqual(SampleScorer._epistemic_tier, "measured")

    def test_confidence(self):
        scorer = SampleScorer()
        self.assertEqual(scorer.confidence(), 0.8)


class TestAgentShape(unittest.TestCase):
    def test_interpret(self):
        agent = SampleAgent()
        result = agent.interpret({"value": 5})
        self.assertEqual(result["classification"], "positive")
        self.assertEqual(result["confidence"], 0.8)

    def test_reader_first_flag(self):
        self.assertTrue(SampleAgent._reader_first)

    def test_confidence_floor_enforced(self):
        self.assertEqual(SampleAgent._confidence_floor, 0.5)

        agent = SampleAgent()
        with self.assertRaises(AgentError):
            agent.validate_confidence(0.3)

    def test_confidence_above_floor_passes(self):
        agent = SampleAgent()
        agent.validate_confidence(0.6)


class TestConfigShape(unittest.TestCase):
    def test_describe(self):
        config = SampleConfig()
        desc = config.describe()
        self.assertIn("max_retries", desc)
        self.assertIn("api_url", desc)
        self.assertIn("api_key", desc)
        self.assertTrue(desc["api_key"]["secret"])

    def test_load_validates(self):
        config = SampleConfig(max_retries=3, api_url="http://localhost", api_key="test")
        config.load()

    def test_load_fails_on_out_of_range(self):
        config = SampleConfig(max_retries=99, api_url="http://localhost", api_key="test")
        with self.assertRaises(ConfigError):
            config.load()


class TestTelemetryShape(unittest.TestCase):
    def test_record_and_calibrate(self):
        tel = SampleTelemetry()
        for i in range(100):
            tel.record("test_metric", float(i))
        self.assertTrue(tel.is_calibrated("test_metric"))

    def test_not_calibrated_initially(self):
        tel = SampleTelemetry()
        tel.record("new_metric", 1.0)
        self.assertFalse(tel.is_calibrated("new_metric"))

    def test_classify_normal(self):
        tel = SampleTelemetry()
        for i in range(100):
            tel.record("steady", 50.0)
        classification = tel.classify("steady")
        self.assertEqual(classification.severity, "GREEN")

    def test_classify_uncalibrated(self):
        tel = SampleTelemetry()
        tel.record("fresh", 1.0)
        classification = tel.classify("fresh")
        self.assertEqual(classification.shape, "calibrating")


class TestGlueShape(unittest.TestCase):
    def test_adapt(self):
        glue = SampleGlue()
        result = glue.adapt(SampleInput(name="test", value=42))
        self.assertEqual(result, {"name": "test", "value": 42})

    def test_debt_tracked(self):
        self.assertTrue(SampleGlue._debt_tracked)
        self.assertTrue(len(SampleGlue._debt_created) > 0)

    def test_debt_report(self):
        glue = SampleGlue()
        report = glue.debt_report()
        self.assertEqual(report["source"], "SampleEntry")
        self.assertEqual(report["target"], "SampleService")
        self.assertTrue(report["temporary"])
        self.assertFalse(report["should_delete"])


class TestRetryableDecorator(unittest.TestCase):
    def test_retries_on_failure(self):
        call_count = 0

        @retryable(max_retries=2, backoff_base=0.01)
        def flaky():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("not yet")
            return "success"

        result = flaky()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 3)

    def test_gives_up_after_max(self):
        @retryable(max_retries=1, backoff_base=0.01)
        def always_fails():
            raise ValueError("nope")

        with self.assertRaises(ValueError):
            always_fails()


class TestMonitoredDecorator(unittest.TestCase):
    def test_records_metrics(self):
        @monitored
        def sample_fn():
            return 42

        result = sample_fn()
        self.assertEqual(result, 42)
        stats = METRICS.get_stats("TestMonitoredDecorator.test_records_metrics.<locals>.sample_fn")
        self.assertGreater(stats["call_count"], 0)

    def test_records_errors(self):
        @monitored
        def failing_fn():
            raise RuntimeError("boom")

        with self.assertRaises(RuntimeError):
            failing_fn()
        stats = METRICS.get_stats("TestMonitoredDecorator.test_records_errors.<locals>.failing_fn")
        self.assertGreater(stats["error_count"], 0)


class TestTrackedDecorator(unittest.TestCase):
    def test_injects_tracking_id(self):
        received_id = None

        @tracked
        def fn_with_tracking(tracking_id=None):
            nonlocal received_id
            received_id = tracking_id
            return tracking_id

        result = fn_with_tracking()
        self.assertIsNotNone(received_id)
        self.assertTrue(len(received_id) > 0)


class TestHashProtectedDecorator(unittest.TestCase):
    def test_detects_modification(self):
        @dataclasses.dataclass
        class WithHeader:
            header: dict
            body: str

        class ModifyingPipeline(PipelineBase):
            @hash_protected(preserve="header")
            def bad_step(self, data):
                return WithHeader(header={"changed": True}, body=data.body)

        pipe = ModifyingPipeline()
        data = WithHeader(header={"original": True}, body="test")
        with self.assertRaises(PipelineError) as ctx:
            pipe.bad_step(data)
        self.assertIn("Hash protection violation", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
