# Huf Haus — Fifteen Code Shapes

TIER: STRUCTURED  
STATUS: DRAFT  
SOURCE: Ewan Bramley shape taxonomy (2026-05-17) + Devon-58ca doctrine sessions  
PRINCIPLE: The shape name IS the proforma. Name it, the checklist appears. Vellum pre-fills what it knows. Vellum guesses where it can. A guess is better than a blank space — it gives a sharper research. The agent fills only what's genuinely new.

---

## How this document works

Every Python file in the Amplified system is exactly one of fifteen shapes. If a file is two shapes, it's two files.

Each shape defines:

1. **What it is** — one sentence
2. **What it does** — verbs only
3. **Enforced checklist** — terminology demands these. Cannot submit without them.
4. **Vellum pre-fill rules** — what Vellum fills from prior records and context. Where it can't know, it guesses. Guess > blank.
5. **Five shaped questions** — pre-empt 90% of the problems. Not open-ended. Shaped to extract what's needed.
6. **Three flags** — escalation paths baked into every form
7. **What it must NOT do** — hard boundaries
8. **Contract** — input type, output type, error behaviour
9. **Skeleton** — 15-25 lines. The template. Fill in the domain logic.
10. **Nuance** — where this shape gets tricky. Where the judgment lives.

### The three flags (every shape)

```
[ ] Needs a research — touches something unsolved. Routes to research pass before build.
[ ] Needs a tool — needs an external tool, library, or connector we don't have. Routes to tooling.
[ ] Needs a genius — an expert has declared this is a bastard. Routes to the best available
    mind on the planet, human or AI. Capitalisation, not species. Severity flag. There are
    geniuses at the end of a world where seven billion humans is soon to become billions of agents.
```

### Pre-fill principle

```
Vellum fills what it knows (from prior records, from context).
Vellum guesses what it doesn't know (a guess gives sharper research than a blank).
The form shows only what's unfilled or flagged as a guess.
The agent's job shrinks to the minimum novel contribution.
Forms become a joy.
```

---

## 1. entry

### What it is

The door where data enters the system.

### What it does

- Receives raw input (HTTP, CLI, message queue, file drop, webhook)
- Validates shape (is this even the right format?)
- Timestamps arrival
- Assigns tracking ID
- Hands off to the pipe

### Enforced checklist

```
[ ] Input source defined (HTTP / CLI / queue / file / webhook / voice)
[ ] Input schema referenced (which model validates this?)
[ ] Rate limit defined
[ ] Authentication method defined (API key / token / none / internal-only)
[ ] Tracking ID generation method defined
[ ] Error response shape defined
[ ] Logging on receipt (what gets logged before processing)
```

### Vellum pre-fill rules

- If similar entry exists (e.g. another HTTP endpoint), pre-fill: auth method, rate limit pattern, error response shape, logging pattern
- Guess: input schema from the ticket description or linked model shape
- Guess: rate limit from the median of existing entries

### Five shaped questions

1. What sends data to this entry? (Name the system, not "various sources")
2. What happens if the sender is unauthorized?
3. What is the maximum payload size this entry accepts?
4. Does this entry need to be idempotent? (Can the same message arrive twice safely?)
5. What downstream shape receives the handoff? (Name it)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT process business logic (that's a service)
- Must NOT write to persistence (that's a store)
- Must NOT transform data shape (that's a pipeline)

### Contract

```
Input:  Raw external data (bytes, JSON, form data, voice stream)
Output: ValidatedInput (typed, tracked, timestamped) → next shape
Error:  400/401/413/429 response to sender. Log. Do not propagate bad data.
```

### Skeleton

```python
from amplified.shapes import EntryBase, tracked, validated

class JobEntry(EntryBase):
    """Entry point for incoming job requests."""

    source = "http"
    auth = "api_key"
    rate_limit = "100/min"
    input_model = JobRequest  # references a model shape
    error_model = EntryError

    @tracked
    @validated
    def receive(self, raw: bytes) -> ValidatedInput:
        parsed = self.parse(raw)           # EntryBase provides parse()
        self.log_receipt(parsed.tracking_id)
        return ValidatedInput(
            data=parsed,
            tracking_id=self.generate_id(),
            received_at=self.now(),
        )
```

### Nuance

Entry shapes look simple but they're the attack surface. Every injection, every malformed payload, every DDoS hits the entry first. The checklist enforces defence-in-depth before anyone writes a line. The nuance is: entries must be paranoid but fast. Validate shape, not content — content validation belongs to the guard.

---

## 2. service

### What it is

A stateless container for business logic.

### What it does

- Receives typed input from another shape
- Applies business rules
- Returns typed output
- Does not hold state between calls
- Does not talk to databases directly (that's a store)

### Enforced checklist

```
[ ] Business rule documented (what decision does this service make?)
[ ] Input type defined (which model?)
[ ] Output type defined (which model?)
[ ] Statelessness confirmed (no instance variables holding request state)
[ ] Error cases enumerated (what can go wrong inside the logic?)
[ ] Epistemic tier declared (INTUITED / STRUCTURED / MEASURED / PROVEN)
[ ] Canon reference (if this implements a Logic Canon method, which one?)
```

### Vellum pre-fill rules

- If ticket references a Canon method, pre-fill: canon reference, epistemic tier, input/output types from the canon registry
- Guess: error cases from similar services in the same domain
- Guess: epistemic tier from the maturity of the referenced method

### Five shaped questions

1. What business decision does this service make? (One sentence, no jargon)
2. Can this service ever produce a different result for the same input? (If yes, it's not stateless — fix it)
3. What is the epistemic tier of the underlying logic? (Are we guessing, calculating, or proving?)
4. Who or what consumes the output? (Name the downstream shape)
5. What happens if this service is wrong? (Severity: irritation / money / safety)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT hold state between calls
- Must NOT read/write databases directly (use a store)
- Must NOT call external APIs directly (use a connector)

### Contract

```
Input:  Typed domain object (from a model shape)
Output: Typed result object (from a model shape)
Error:  Raises domain exception with context. Never swallows errors silently.
```

### Skeleton

```python
from amplified.shapes import ServiceBase, monitored, epistemic

@epistemic(tier="structured", canon_ref="cash_flow_forecast_v2")
class CashFlowService(ServiceBase):
    """Forecasts cash flow for the next quarter."""

    input_model = CashFlowInput
    output_model = CashFlowForecast

    @monitored
    def execute(self, input: CashFlowInput) -> CashFlowForecast:
        monthly = self.project_monthly(input.revenue_history, input.cost_history)
        gap = self.detect_gap(monthly, input.reserve_target)
        return CashFlowForecast(
            monthly_projections=monthly,
            gap_month=gap.month if gap else None,
            recommended_reserve=gap.amount if gap else 0,
            confidence=self.confidence(),
        )
```

### Nuance

Services are where the Logic Canon lives in code. The epistemic tier declaration is load-bearing — a service claiming MEASURED must have data behind it, not opinion. The nuance: services are easy to write and easy to lie in. The enforced tier declaration + Canon reference prevents "I reckon" from wearing the costume of "the maths says."

---

## 3. worker

### What it is

A background task executor that does work asynchronously.

### What it does

- Picks up tasks from a queue or schedule
- Executes work that doesn't need an immediate response
- Reports completion, failure, or progress
- Retries on transient failure
- Respects concurrency limits

### Enforced checklist

```
[ ] Task source defined (queue / schedule / trigger)
[ ] Retry policy defined (max retries, backoff strategy, dead letter)
[ ] Timeout defined (how long before this worker is considered stuck?)
[ ] Concurrency limit defined (how many can run in parallel?)
[ ] Idempotency confirmed (same task twice = same result)
[ ] Progress reporting method defined (how does the system know it's alive?)
[ ] Completion signal defined (what emits when done?)
```

### Vellum pre-fill rules

- Pre-fill: retry policy from the org default (3 retries, exponential backoff)
- Pre-fill: timeout from median of existing workers in the same domain
- Pre-fill: concurrency limit from infrastructure capacity
- Guess: task source from the ticket description
- Guess: completion signal pattern from similar workers

### Five shaped questions

1. What happens if this worker crashes mid-task? (Is the task recoverable?)
2. How long is too long? (At what point should the system assume this worker is dead?)
3. Can two instances of this worker fight over the same task? (Race condition check)
4. What should happen to the task if it fails after all retries? (Dead letter / alert / discard)
5. Does this worker need to run in order, or can tasks be parallel?

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT return results synchronously to a caller (that's a service)
- Must NOT hold a database connection open for the duration (use a store per operation)
- Must NOT silently discard failures

### Contract

```
Input:  Task message from queue/schedule (typed, with tracking ID)
Output: Completion event (success with result / failure with reason / progress update)
Error:  Retry per policy → dead letter → alert. Never silent failure.
```

### Skeleton

```python
from amplified.shapes import WorkerBase, monitored, retryable

class InvoiceChaserWorker(WorkerBase):
    """Chases unpaid invoices on schedule."""

    task_source = "schedule:daily_0800"
    retry_policy = "3x_exponential"
    timeout = "5m"
    concurrency = 1

    @monitored
    @retryable
    def execute(self, task: InvoiceChaseTask) -> WorkerResult:
        unpaid = self.store.get_unpaid(task.client_id, days_overdue=30)
        for invoice in unpaid:
            message = self.compose_chase(invoice)
            self.connector.send_whatsapp(task.client_phone, message)
        return WorkerResult(
            status="complete",
            processed=len(unpaid),
            tracking_id=task.tracking_id,
        )
```

### Nuance

Workers are where things go quietly wrong. A service fails loudly — the caller gets an error. A worker fails silently unless you've built the progress reporting and dead letter handling. The nuance: every worker needs a heartbeat (the system asks "are you alive?") and a dead man's switch (the system notices "you stopped talking"). Without both, a stuck worker is invisible.

---

## 4. connector

### What it is

The bridge to an external system.

### What it does

- Talks to APIs, databases, file systems, or services outside the Amplified boundary
- Handles authentication to the external system
- Handles rate limiting imposed by the external system
- Translates external data format into internal model
- Translates internal model into external data format

### Enforced checklist

```
[ ] External system named (Xero / WhatsApp / DeepSeek / Companies House / etc.)
[ ] Auth method defined (OAuth / API key / HMAC / none)
[ ] Rate limit documented (what does the external system allow?)
[ ] Retry policy defined (transient failure handling)
[ ] Timeout defined (how long to wait for external response?)
[ ] Data mapping defined (external format ↔ internal model)
[ ] Circuit breaker defined (at what point do we stop calling a failing system?)
[ ] PII boundary check (does any PII cross this connector? If yes → anonymisation required)
```

### Vellum pre-fill rules

- If connector to same external system exists, pre-fill: auth method, rate limits, retry policy, circuit breaker, data mapping patterns
- If external system is in the public API registry, pre-fill: rate limits, auth type, base URL
- Guess: timeout from the external system's documented SLA or 30s default
- Guess: PII boundary from the data types flowing through

### Five shaped questions

1. What happens when the external system is down? (Degrade / queue / fail / fallback)
2. Does any personally identifiable data cross this connector? (If yes, where is anonymisation?)
3. What is the cost per call? (Free / metered / expensive — affects rate limiting strategy)
4. Can the external system's response shape change without warning? (API versioning strategy)
5. What is the external system's SLA? (Affects our timeout and retry configuration)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT contain business logic (that's a service)
- Must NOT cache responses without explicit TTL (staleness is a lie)
- Must NOT expose raw external errors to internal consumers (translate them)

### Contract

```
Input:  Internal typed request (from a model shape)
Output: Internal typed response (translated from external format)
Error:  ConnectorError with: external_status, retry_eligible, human_readable_reason
```

### Skeleton

```python
from amplified.shapes import ConnectorBase, monitored, circuit_breaker

class XeroConnector(ConnectorBase):
    """Connects to Xero accounting API."""

    external_system = "xero"
    auth = "oauth2"
    rate_limit = "60/min"
    timeout = "15s"
    circuit_breaker_threshold = 5  # consecutive failures before open

    @monitored
    @circuit_breaker
    def get_invoices(self, org_id: str, since: date) -> list[Invoice]:
        raw = self.http.get(
            f"/api.xro/2.0/Invoices",
            params={"where": f'Date >= DateTime({since.isoformat()})'},
        )
        return [self.to_internal(inv) for inv in raw["Invoices"]]

    def to_internal(self, raw: dict) -> Invoice:
        return Invoice(**self.field_map.translate(raw))
```

### Nuance

Connectors are the most likely shape to break without anyone touching them. External APIs change, rate limits tighten, auth tokens expire, services go down. The nuance: a connector must be the most defensively written shape in the system. Assume the external system is hostile, flaky, and about to change its API tomorrow. The circuit breaker isn't optional — it's what stops a failing connector from taking down everything behind it.

---

## 5. model

### What it is

A data shape definition — the contract for what data looks like.

### What it does

- Defines the fields, types, and constraints of a data object
- Validates data against the shape
- Serialises / deserialises (Python ↔ JSON ↔ database)
- Documents the meaning of each field
- Enforces required vs optional

### Enforced checklist

```
[ ] All fields typed (no Any, no untyped dicts)
[ ] Required vs optional explicit for every field
[ ] Field descriptions present (one line each — what does this mean?)
[ ] Validation rules defined (min/max, format, allowed values)
[ ] Serialisation format confirmed (JSON / YAML / database row)
[ ] Version number present (models change — track it)
[ ] Epistemic tier of each field documented where relevant
```

### Vellum pre-fill rules

- If model extends or references an existing model, pre-fill: shared fields, types, descriptions, validation rules
- If ticket mentions domain entities, pre-fill: field names and types from the domain dictionary
- Guess: required vs optional from how similar models treat the same fields
- Guess: validation rules from the data type (email → email format, amount → positive number)

### Five shaped questions

1. What is the one thing this model represents? (If the answer has "and" in it, it's two models)
2. Which fields can change after creation, and which are immutable?
3. Is there a natural ordering to instances of this model? (Timestamp? Priority? Alphabetical?)
4. What existing model is this most similar to? (Avoid reinventing a shape that exists)
5. What breaks downstream if a field is null? (Identifies which fields are truly required)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT contain business logic (that's a service)
- Must NOT contain persistence logic (that's a store)
- Must NOT use Any or untyped dicts (the contract must be explicit)

### Contract

```
Input:  Raw data (dict, JSON, database row)
Output: Validated typed object / validation error with field-level detail
Error:  ValidationError listing every failing field with reason. Never partial validation.
```

### Skeleton

```python
from amplified.shapes import ModelBase, field

class Invoice(ModelBase):
    """A single invoice from a client's accounting system."""

    version = 2

    invoice_id: str = field(required=True, description="External system invoice ID")
    amount: Decimal = field(required=True, gt=0, description="Invoice amount in GBP")
    issued_date: date = field(required=True, description="Date invoice was issued")
    due_date: date = field(required=True, description="Date payment is due")
    paid_date: date | None = field(required=False, description="Date payment received, if paid")
    status: InvoiceStatus = field(required=True, description="Current invoice state")
    line_items: list[LineItem] = field(required=True, min_length=1, description="What was invoiced")
    notes: str = field(required=False, default="", description="Free text notes from source system")
```

### Nuance

Models look like the simplest shape but they're the most political. Every field is a decision about what matters. The nuance: models define the boundary of what the system can see. A field not in the model is invisible to everything downstream. Adding a field is cheap. Removing one is expensive. Get the initial shape right by asking "what decisions will be made from this data?" — if no decision uses a field, the field doesn't need to exist.

---

## 6. store

### What it is

The interface between the system and persistence.

### What it does

- Reads from a database, file system, or cache
- Writes to a database, file system, or cache
- Handles transactions and consistency
- Abstracts the storage engine from the rest of the system
- Manages migrations when schema changes

### Enforced checklist

```
[ ] Storage engine defined (PostgreSQL / SQLite / Redis / file system)
[ ] Read methods defined (what queries does this store answer?)
[ ] Write methods defined (what mutations does this store perform?)
[ ] Schema / table definition referenced (which model defines the shape?)
[ ] Migration strategy defined (how does schema change safely?)
[ ] Transaction boundary defined (what operations are atomic?)
[ ] Index strategy defined (what queries need to be fast?)
[ ] Backup / recovery documented (what happens if data is lost?)
```

### Vellum pre-fill rules

- Pre-fill: storage engine from the project default (PostgreSQL for production, SQLite for client-side)
- Pre-fill: schema from the referenced model shape
- Pre-fill: migration strategy from project convention (alembic / manual SQL)
- Guess: index strategy from the read methods (frequent query fields get indexed)
- Guess: transaction boundaries from the write methods (multi-write = transaction)

### Five shaped questions

1. How big will this data get? (10 rows / 10K rows / 10M rows — affects index and query strategy)
2. What is the read-to-write ratio? (Read-heavy = optimise queries. Write-heavy = optimise inserts.)
3. Can this data be reconstructed if lost? (If yes, backup is less critical. If no, it's essential.)
4. Does this store need to support concurrent access? (Multiple workers hitting the same table?)
5. What is the oldest data that still matters? (Retention / archival policy)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT contain business logic (that's a service)
- Must NOT expose raw SQL or database internals to consumers
- Must NOT skip migrations (schema drift is silent corruption)

### Contract

```
Input:  Typed query or typed mutation (from model shapes)
Output: Typed result set or write confirmation
Error:  StoreError with: operation, reason, retriable flag. Never raw database exceptions.
```

### Skeleton

```python
from amplified.shapes import StoreBase, monitored, transactional

class InvoiceStore(StoreBase):
    """Persistence layer for invoice data."""

    engine = "postgresql"
    model = Invoice
    table = "invoices"

    @monitored
    def get_unpaid(self, client_id: str, days_overdue: int) -> list[Invoice]:
        cutoff = self.now() - timedelta(days=days_overdue)
        return self.query(
            "status = :status AND due_date < :cutoff AND client_id = :client_id",
            status=InvoiceStatus.UNPAID, cutoff=cutoff, client_id=client_id,
        )

    @monitored
    @transactional
    def mark_paid(self, invoice_id: str, paid_date: date) -> Invoice:
        invoice = self.get_by_id(invoice_id)
        return self.update(invoice, paid_date=paid_date, status=InvoiceStatus.PAID)
```

### Nuance

Stores are where data integrity lives or dies. The nuance: the store must be the only way to touch the database. If any other shape reaches into the database directly, you've created an invisible mutation path — changes that bypass validation, logging, and transactions. The store is a bottleneck on purpose. All reads and writes go through the bottleneck, or the system can't trust its own data.

---

## 7. pipeline

### What it is

A multi-step transformation that turns data from one shape into another.

### What it does

- Takes input in one format
- Applies a sequence of transformations
- Produces output in a different format
- Each step is independently testable
- The whole pipeline is traceable (which steps ran, what changed)

### Enforced checklist

```
[ ] Input shape defined (which model enters?)
[ ] Output shape defined (which model exits?)
[ ] Steps listed in order (each step named and described)
[ ] Each step's input/output types defined
[ ] Error handling per step defined (fail step / fail pipeline / skip step)
[ ] Metadata protection confirmed (YAML/header preserved — protect the label, work the specimen)
[ ] Hash verification at boundaries (input hash, output hash, intermediate hashes where needed)
```

### Vellum pre-fill rules

- If similar pipeline exists, pre-fill: step pattern, error handling strategy, hash verification pattern
- Pre-fill: metadata protection from standard pipeline template (always on)
- Guess: steps from the delta between input model and output model
- Guess: error handling from the severity of the pipeline's domain

### Five shaped questions

1. What is the input shape and what is the output shape? (The delta defines the pipeline's job)
2. Can any step be skipped without corrupting the output? (Identifies optional vs required steps)
3. What is the largest input this pipeline will process? (Size affects streaming vs batch strategy)
4. If step 3 of 5 fails, what happens to the work done in steps 1-2? (Rollback or partial result?)
5. Does this pipeline modify metadata/headers, or only the body? (Metadata protection check)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT modify metadata without explicit declaration (protect the label)
- Must NOT contain business decisions (that's a service within a step)
- Must NOT write to persistence directly (hand off to a store at the end)

### Contract

```
Input:  Typed source data (from a model shape)
Output: Typed transformed data (from a different model shape) + transformation log
Error:  PipelineError with: step_failed, steps_completed, partial_output_if_any
```

### Skeleton

```python
from amplified.shapes import PipelineBase, step, monitored, hash_protected

class IngestionPipeline(PipelineBase):
    """Transforms raw voice transcript into vault-ready entry."""

    input_model = RawTranscript
    output_model = VaultEntry

    @step(order=1)
    def extract_metadata(self, raw: RawTranscript) -> MetadataExtracted:
        return MetadataExtracted(header=raw.header, body=raw.body, hash=self.hash(raw))

    @step(order=2)
    @hash_protected(preserve="header")
    def structure_body(self, data: MetadataExtracted) -> StructuredBody:
        return self.ai_interpret(data.body)  # 3 → 17 expansion

    @step(order=3)
    def validate_and_package(self, data: StructuredBody) -> VaultEntry:
        self.verify_header_hash(data)  # protect the label
        return VaultEntry(header=data.header, body=data.structured, hash=self.hash_all(data))
```

### Nuance

Pipelines are where the metadata/body rule lives in practice. "Protect the label, work the specimen." The nuance: every pipeline that touches content with YAML frontmatter or metadata headers MUST hash the metadata separately, process only the body, and verify the metadata hash hasn't changed. If it has, the pipeline stops. This prevents silent label corruption — the most dangerous form of data integrity failure because everything downstream trusts the label.

---

## 8. orchestrator

### What it is

The coordinator that decides what runs when.

### What it does

- Receives a high-level task or trigger
- Decomposes into steps
- Calls other shapes in the right order
- Handles branching logic (if X, do Y, else do Z)
- Tracks overall progress
- Reports completion or failure of the whole workflow

### Enforced checklist

```
[ ] Trigger defined (what starts this orchestrator?)
[ ] Step sequence defined (what shapes are called, in what order?)
[ ] Branching conditions defined (what decisions determine the path?)
[ ] Failure strategy defined (retry step / skip step / abort workflow / compensate)
[ ] Timeout for entire workflow defined
[ ] Progress reporting method defined
[ ] Completion criteria defined (how do we know it's done?)
[ ] Compensation actions defined (if step 3 fails after step 2 succeeded, what undoes step 2?)
```

### Vellum pre-fill rules

- If similar workflow exists, pre-fill: step sequence pattern, failure strategy, timeout
- Pre-fill: shapes involved from the ticket's linked shapes
- Guess: branching conditions from the domain logic
- Guess: compensation actions from the write operations in each step

### Five shaped questions

1. What triggers this orchestrator? (Event / schedule / manual / another orchestrator)
2. What is the longest this workflow should ever take? (Defines the timeout)
3. If step 3 fails, does step 2's work need to be undone? (Compensation strategy)
4. Can any steps run in parallel, or must they all be sequential?
5. Who or what needs to know when this workflow completes? (Notification / callback / record)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT contain business logic directly (call a service)
- Must NOT access databases directly (call a store through a service)
- Must NOT become a god object (if it coordinates more than 7 steps, decompose into sub-orchestrators)

### Contract

```
Input:  Trigger event (typed, with context)
Output: WorkflowResult (completed / failed / partial) with step-by-step log
Error:  WorkflowError with: steps_completed, step_failed, compensation_performed
```

### Skeleton

```python
from amplified.shapes import OrchestratorBase, workflow, monitored

class MorningBriefOrchestrator(OrchestratorBase):
    """Assembles and delivers the morning brief."""

    trigger = "schedule:daily_0700"
    timeout = "10m"

    @workflow
    @monitored
    def run(self, context: BriefContext) -> WorkflowResult:
        # Step 1: Gather data
        health = self.call(HealthCheckService, context.system_ids)
        invoices = self.call(InvoiceStore.get_overdue, context.client_id)
        signals = self.call(SignalStore.get_overnight, context.signal_types)

        # Step 2: Compose brief
        brief = self.call(BriefComposer, health, invoices, signals)

        # Step 3: Record in Vellum
        record = self.call(VellumRecorder, brief)

        # Step 4: Deliver to reader
        self.call(DeliveryConnector, record, context.reader_profile)

        return WorkflowResult(status="complete", steps=4, record_id=record.id)
```

### Nuance

Orchestrators are where complexity hides. They look simple — just call A, then B, then C. The nuance: orchestrators must be thin. Their only job is coordination. The moment business logic creeps into the orchestrator, you've created a shape that's impossible to test in isolation and impossible to reuse. If you're writing `if` statements about business rules inside an orchestrator, that logic belongs in a service. The orchestrator asks "what next?" — never "what's right?"

---

## 9. guard

### What it is

The shape that validates, rejects, and stops. The immune system.

### What it does

- Receives data from another shape
- Checks it against rules
- Passes valid data through unchanged
- Rejects invalid data with clear reasons
- Logs every accept and every reject
- Can halt propagation entirely (hard stop)

### Enforced checklist

```
[ ] Rules defined (what constitutes valid input?)
[ ] Rejection message template defined (clear, actionable, not cryptic)
[ ] Hard stop conditions defined (what triggers a full halt, not just rejection?)
[ ] Logging on accept confirmed (not just reject — accepts are evidence too)
[ ] Logging on reject confirmed (with reason, input snapshot, timestamp)
[ ] Bypass explicitly impossible (no admin override, no debug flag to skip)
[ ] GREEN/AMBER/RED/BLACK classification for each rule
```

### Vellum pre-fill rules

- Pre-fill: common rules from the data type (email format, positive numbers, non-empty strings)
- Pre-fill: GREEN/AMBER/RED/BLACK thresholds from org defaults
- Pre-fill: rejection message templates from existing guards
- Guess: hard stop conditions from the data sensitivity level
- Guess: rules from the downstream consumer's requirements

### Five shaped questions

1. What is the single worst thing that gets through if this guard doesn't exist? (Defines the guard's reason for being)
2. Is this a soft guard (reject and report) or a hard guard (reject and halt propagation)?
3. Can a legitimate input ever look like a violation? (False positive strategy)
4. What evidence does the rejection message need to include for someone to fix the input?
5. What traffic light colour is each rule? (GREEN pass / AMBER warn / RED reject / BLACK halt)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT transform data (it's a guard, not a pipeline — pass through or reject)
- Must NOT have a bypass mechanism (no --skip-validation flag, ever)
- Must NOT make business decisions (it enforces rules, it doesn't create them)

### Contract

```
Input:  Any typed data from another shape
Output: Same data, unchanged (passed through) OR Rejection with field-level reasons
Error:  GuardHalt for BLACK conditions. Rejection for RED. Warning record for AMBER.
```

### Skeleton

```python
from amplified.shapes import GuardBase, monitored, no_bypass

@no_bypass
class PiiGuard(GuardBase):
    """Rejects any data containing personally identifiable information."""

    rules = [
        Rule("no_names", pattern=NAME_PATTERN, severity="RED"),
        Rule("no_addresses", pattern=ADDRESS_PATTERN, severity="RED"),
        Rule("no_emails", pattern=EMAIL_PATTERN, severity="RED"),
        Rule("no_phones", pattern=PHONE_PATTERN, severity="RED"),
        Rule("anomalous_volume", check=volume_check, severity="BLACK"),
    ]

    @monitored
    def check(self, data: AnonymisedPacket) -> AnonymisedPacket:
        violations = self.evaluate_rules(data)
        if any(v.severity == "BLACK" for v in violations):
            raise GuardHalt("PII guard BLACK: anomalous volume detected", violations)
        if violations:
            raise Rejection("PII detected in anonymised packet", violations)
        self.log_accept(data.tracking_id)
        return data  # unchanged
```

### Nuance

Guards are the only shape where doing nothing IS the correct output. A guard that passes data through unchanged has done its job perfectly. The nuance: guards must be fast and simple. Complex guard logic is a sign that the guard should be split into multiple guards, each checking one thing. A guard with 20 rules is harder to debug than 4 guards with 5 rules each. And the `@no_bypass` decorator is real — there is no admin mode, no debug flag, no environment variable that skips the guard. Vellum records every accept and reject. The record is the evidence.

---

## 10. scorer

### What it is

The shape that measures and produces a number from inputs.

### What it does

- Takes structured input
- Applies a scoring formula or rubric
- Produces a numeric result with confidence
- Declares its epistemic tier (is this a guess, a calculation, or a proof?)
- Enables comparison (this score vs that score vs threshold)

### Enforced checklist

```
[ ] Scoring formula or rubric documented (show the maths or the rubric)
[ ] Input variables defined (what numbers/categories feed the score?)
[ ] Output range defined (0-100? 0-1? Unbounded?)
[ ] Confidence mechanism defined (how certain is this score?)
[ ] Epistemic tier declared (INTUITED / STRUCTURED / MEASURED / PROVEN)
[ ] Threshold definitions (what score = GREEN / AMBER / RED / BLACK?)
[ ] Canon reference (if this implements an armamentarium method, which one?)
[ ] Second-machine verification eligible? (Does this need independent check?)
```

### Vellum pre-fill rules

- If Canon method is referenced, pre-fill: formula, input variables, output range, epistemic tier, thresholds
- Pre-fill: confidence mechanism from the epistemic tier (MEASURED = CI, STRUCTURED = rubric)
- Guess: thresholds from the domain conventions (financial = tighter, operational = looser)
- Guess: second-machine eligibility from the score's downstream impact

### Five shaped questions

1. What formula produces this score? (Show the maths. No "it considers various factors.")
2. What is the confidence band on this score? (±5%? ±20%? Unknown?)
3. At what threshold does this score trigger an action? (The number that matters)
4. Can this score be independently verified by a second machine? (If high impact, it should be)
5. What changes between runs? (Same input = same score? Or does context change the result?)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT produce a score without declaring the formula
- Must NOT claim MEASURED or PROVEN without evidence to support the tier
- Must NOT hide the working (no interrogable working, no valid answer)

### Contract

```
Input:  Typed scoring input (variables from model shapes)
Output: Score (value, confidence, tier, formula_ref, threshold_status)
Error:  ScoringError if inputs are insufficient. Never a default score — refuse rather than guess.
```

### Skeleton

```python
from amplified.shapes import ScorerBase, monitored, epistemic, verifiable

@epistemic(tier="measured", canon_ref="altman_z_score_v1")
@verifiable(second_machine=True)
class DistressScorer(ScorerBase):
    """Calculates business distress probability using Altman Z-score variant."""

    input_model = FinancialSnapshot
    output_range = (0.0, 10.0)
    thresholds = {"GREEN": 3.0, "AMBER": 1.8, "RED": 1.0, "BLACK": 0.5}

    @monitored
    def score(self, input: FinancialSnapshot) -> ScoreResult:
        z = (1.2 * input.working_capital_ratio
             + 1.4 * input.retained_earnings_ratio
             + 3.3 * input.ebit_ratio
             + 0.6 * input.market_equity_ratio
             + 1.0 * input.sales_ratio)
        return ScoreResult(
            value=z,
            confidence=self.confidence_from_sample(input.sample_size),
            tier=self.declared_tier,
            formula_ref="altman_z_1968_sme_variant",
            status=self.threshold_status(z),
        )
```

### Nuance

Scorers are where the Logic Canon meets reality. The formula is published, cited, challengeable — "open source the armamentarium." The nuance: a scorer must never produce a number without showing how it got there. "No interrogable working, no valid answer." This isn't bureaucracy — it's what allows a second machine to verify, a human to challenge, and a Kaizen loop to improve the formula. A hidden formula is an unchallengeable oracle, and oracles are not allowed in this system.

---

## 11. agent

### What it is

The AI-powered reasoning shape. Interprets, proposes, translates.

### What it does

- Receives structured input
- Applies AI reasoning (LLM calls, pattern matching, classification)
- Proposes options (never commands)
- Translates between formats (3 → 17 inbound, 17 → 3 outbound)
- Declares confidence on every output
- Respects the reader-first principle (output shaped for the recipient, not the sender)

### Enforced checklist

```
[ ] AI model specified (which model? Which fallback chain?)
[ ] Purpose defined (interpret / translate / classify / propose / expand / compress)
[ ] Input format defined
[ ] Output format defined
[ ] Confidence mechanism defined (how does the agent declare certainty?)
[ ] Reader profile defined (who receives this output? Agent / Ewan / Bob / vault?)
[ ] Hallucination guard defined (what stops the agent from making things up?)
[ ] Context window budget defined (how much context does this agent need?)
[ ] Override by Python hard stop confirmed (AI never overrides Python live)
```

### Vellum pre-fill rules

- Pre-fill: model from the org default fallback chain (LiteLLM routing)
- Pre-fill: reader profile from the ticket's assignee or consumer
- Pre-fill: hallucination guard from org defaults (citation required, confidence floor)
- Guess: purpose from the ticket description
- Guess: context window budget from the input size and model limits

### Five shaped questions

1. What does this agent interpret that a Python rule couldn't? (If a rule can do it, use a rule)
2. Who is the reader? (The output format depends entirely on this answer)
3. What is the minimum confidence floor for this agent's output to be actionable?
4. What happens when the agent is wrong? (Severity: irritation / money / safety)
5. Is this a 3→17 expansion or a 17→3 compression? (Determines the agent's direction)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT override Python hard stops (Python stops the current run, AI improves the next)
- Must NOT produce unmarked opinions (every claim labelled with type and confidence)
- Must NOT claim higher epistemic status than INTUITED without promotion evidence
- Must NOT access databases directly (route through stores)

### Contract

```
Input:  Typed structured data + reader profile + context budget
Output: TypedProposal (options with confidence, reader-formatted) OR Translation (formatted for reader)
Error:  AgentError with: what_failed, confidence_at_failure, fallback_used
```

### Skeleton

```python
from amplified.shapes import AgentBase, monitored, reader_first, confidence_floor

@reader_first
@confidence_floor(minimum=0.6)
class BriefCompressor(AgentBase):
    """Compresses 17-field structured brief into 3-line reader summary."""

    purpose = "compress"  # 17 → 3
    model = "litellm:default_chain"
    reader_profile = "owner_whatsapp"

    @monitored
    def interpret(self, structured: StructuredBrief, reader: ReaderProfile) -> CompressedBrief:
        summary = self.llm.compress(
            input=structured,
            target_format=reader.preferred_format,
            max_lines=3,
            confidence_floor=self.confidence_floor,
        )
        return CompressedBrief(
            lines=summary.lines,
            confidence=summary.confidence,
            source_fields=summary.fields_used,
            reader=reader.id,
            tier="intuited",  # AI output is always INTUITED until promoted
        )
```

### Nuance

Agents are INTUITED by default. Always. Their output wears the lowest epistemic tier until a promotion gate lifts it. The nuance: agents are powerful but they are not truth. They interpret, propose, and translate — they do not decide, store, or enforce. "AI interprets. Python measures. Vellum records. Brain remembers. Human chooses." An agent that bypasses this chain is a loose cannon. The reader-first decorator ensures the output serves the reader, not the agent's convenience.

---

## 12. test

### What it is

The shape that proves the others work.

### What it does

- Exercises another shape with known inputs
- Asserts expected outputs
- Catches regressions
- Documents behaviour through examples
- Runs automatically on every change

### Enforced checklist

```
[ ] Shape under test identified (which shape does this test prove?)
[ ] Happy path tested (normal operation with valid input)
[ ] Error path tested (what happens with invalid input?)
[ ] Edge cases listed and tested
[ ] Test data defined (not random — deterministic, reproducible)
[ ] Assertion messages present (when a test fails, what does the message say?)
[ ] CI integration confirmed (does this test run automatically?)
```

### Vellum pre-fill rules

- Pre-fill: shape under test from the linked shape in the ticket
- Pre-fill: happy path test skeleton from the shape's contract (known input → expected output)
- Pre-fill: error path from the shape's error contract
- Guess: edge cases from the shape's type constraints (null, empty, max size, boundary values)
- Guess: test data from the shape's model (generate valid instance from model definition)

### Five shaped questions

1. What is the single most important behaviour this test proves? (The one assertion that matters most)
2. What input would break this shape if the guard wasn't there? (Test the guard, not just the happy path)
3. Is this test deterministic? (Same run = same result, every time. No randomness.)
4. How fast does this test run? (Under 1 second = unit. Over 1 second = integration. Over 10 = needs review.)
5. If this test fails, can a developer understand why from the failure message alone?

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT test implementation details (test behaviour, not how it's coded)
- Must NOT depend on external systems (mock connectors, use test stores)
- Must NOT be flaky (a test that sometimes passes and sometimes fails is worse than no test)

### Contract

```
Input:  Test fixtures (known inputs, expected outputs)
Output: Pass / Fail with assertion detail
Error:  Test failure with: what was expected, what was received, which assertion failed
```

### Skeleton

```python
from amplified.shapes import TestBase

class TestCashFlowService(TestBase):
    """Proves CashFlowService produces correct forecasts."""

    shape_under_test = CashFlowService

    def test_healthy_business_no_gap(self):
        input = CashFlowInput(
            revenue_history=[10000, 11000, 10500],
            cost_history=[7000, 7200, 7100],
            reserve_target=5000,
        )
        result = self.shape.execute(input)
        assert result.gap_month is None, "Healthy business should have no gap month"
        assert result.recommended_reserve == 0

    def test_struggling_business_detects_gap(self):
        input = CashFlowInput(
            revenue_history=[10000, 8000, 6000],  # declining
            cost_history=[9000, 9000, 9000],       # flat costs
            reserve_target=5000,
        )
        result = self.shape.execute(input)
        assert result.gap_month is not None, "Declining revenue should detect gap"
        assert result.recommended_reserve > 0, f"Expected reserve > 0, got {result.recommended_reserve}"
```

### Nuance

Tests are the only shape that is allowed to be boring. The nuance: a test should read like a specification. Someone who has never seen the code should be able to read the test and understand exactly what the shape does. Test names are sentences. Assertions have messages. Fixtures tell a story. The test is the documentation that can't lie — because it runs.

---

## 13. config

### What it is

Settings, thresholds, and environment values. The knobs.

### What it does

- Defines what changes without changing code
- Separates environment-specific values from logic
- Provides typed access to settings (not raw strings)
- Validates config on load (fail fast, not at runtime)
- Documents every setting with its purpose and default

### Enforced checklist

```
[ ] Every setting typed (str, int, float, bool, enum — no untyped values)
[ ] Every setting has a default or is explicitly required
[ ] Every setting has a one-line description
[ ] Environment source defined (env var / file / vault / hardcoded default)
[ ] Validation on load confirmed (bad config = crash on startup, not at 3am)
[ ] Secrets handling defined (secrets via env var reference, NEVER hardcoded values)
[ ] Change impact documented (what breaks if this setting changes?)
```

### Vellum pre-fill rules

- Pre-fill: settings from the shape they configure (e.g. a connector's config gets timeout, rate_limit, base_url)
- Pre-fill: defaults from org conventions (timeout=30s, rate_limit=100/min)
- Pre-fill: environment source from project convention (env vars for secrets, file for the rest)
- Guess: types from the setting names (timeout → int seconds, url → str URL, enabled → bool)
- Guess: descriptions from the setting names and context

### Five shaped questions

1. What happens if this config file is missing entirely? (Should the system crash or use all defaults?)
2. Which settings are secrets? (These MUST come from environment variables, never files in repo)
3. What is the blast radius of changing each setting? (Irritation / broken feature / system down)
4. Can any of these settings be changed at runtime, or only at startup?
5. What is the most likely setting to be wrong in a new deployment? (Put extra validation there)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT contain logic (config provides values, not behaviour)
- Must NOT contain secrets in plain text (env var references only)
- Must NOT fail silently on invalid values (crash loud, crash early)

### Contract

```
Input:  Environment variables + config file + defaults
Output: Typed, validated config object accessible by all shapes
Error:  ConfigError on startup with: which setting, what's wrong, what's expected
```

### Skeleton

```python
from amplified.shapes import ConfigBase, setting, secret

class XeroConfig(ConfigBase):
    """Configuration for Xero accounting connector."""

    base_url: str = setting(
        default="https://api.xero.com",
        description="Xero API base URL",
    )
    timeout: int = setting(
        default=15,
        description="Request timeout in seconds",
        min_value=1, max_value=120,
    )
    rate_limit: int = setting(
        default=60,
        description="Max requests per minute",
    )
    client_id: str = secret(
        env_var="XERO_CLIENT_ID",
        description="OAuth2 client ID for Xero",
    )
    client_secret: str = secret(
        env_var="XERO_CLIENT_SECRET",
        description="OAuth2 client secret for Xero",
    )
```

### Nuance

Config is where "it works on my machine" lives. The nuance: every config difference between environments is a potential bug. The config shape should make it impossible to run with invalid settings and trivial to see what's different between environments. The validation-on-load rule means you find config problems at deploy time (09:00, someone's watching) not at runtime (03:00, nobody's watching).

---

## 14. telemetry

### What it is

The sensors. What `@monitor` produces. The nervous system.

### What it does

- Emits measurements from other shapes (timing, counts, errors, memory)
- Structures measurements into Vellum-ready records
- Routes signals through the monitoring surface
- Classifies signals by network shape (load, drift, spike, cascade, etc.)
- Feeds the mycelial monitoring network

### Enforced checklist

```
[ ] Metric names defined (what is being measured?)
[ ] Metric types defined (counter / gauge / histogram / summary)
[ ] Emission frequency defined (every call / sampled / on change / on threshold)
[ ] Signal classification defined (which network shape does this metric detect?)
[ ] Routing defined (where does this telemetry go? Vellum / log / alert)
[ ] Retention defined (how long is this data kept?)
[ ] Alert threshold defined (at what value does this metric become AMBER / RED / BLACK?)
```

### Vellum pre-fill rules

- Pre-fill: metric names from the `@monitor` decorator on the source shape
- Pre-fill: metric types from convention (timing=histogram, errors=counter, queue_depth=gauge)
- Pre-fill: signal classification from the metric type (timing drift = "drift", error spike = "transient spike")
- Pre-fill: routing from org default (all telemetry → Vellum record)
- Guess: alert thresholds from the historical baseline of similar shapes

### Five shaped questions

1. What question does this metric answer? (Not "what does it measure" — what QUESTION does it answer?)
2. At what value does this metric indicate a problem? (The threshold that matters)
3. Is this a leading indicator or a trailing indicator? (Leading = early warning. Trailing = post-mortem.)
4. What is the cost of emitting this metric? (Free / cheap / expensive — affects sampling strategy)
5. Who needs to see this signal? (System / agent / Ewan / nobody until it goes RED)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT block the shape it's measuring (telemetry is non-blocking, always)
- Must NOT lose metrics silently (if the telemetry pipeline is down, buffer or alert)
- Must NOT create dashboards nobody looks at (data for attention, not theatre)

### Contract

```
Input:  Measurements from @monitor decorators on other shapes
Output: Structured telemetry records → Vellum monitoring surface
Error:  TelemetryError if emission fails. Never block the source shape.
```

### Skeleton

```python
from amplified.shapes import TelemetryBase, metric, signal_classifier

class ServiceTelemetry(TelemetryBase):
    """Telemetry collector for service shapes."""

    execution_time = metric(
        type="histogram",
        buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0],
        description="Service execution time in seconds",
    )
    error_count = metric(
        type="counter",
        description="Total service errors",
    )
    call_frequency = metric(
        type="counter",
        description="Total service calls",
    )

    @signal_classifier
    def classify(self, metrics: MetricSnapshot) -> SignalClassification:
        if self.is_spike(metrics.error_count, window="5m"):
            return SignalClassification(shape="transient_spike", severity="AMBER")
        if self.is_drift(metrics.execution_time, window="1h"):
            return SignalClassification(shape="drift", severity="AMBER")
        return SignalClassification(shape="normal", severity="GREEN")
```

### Nuance

Telemetry is where "data for attention, not theatre" lives. The nuance: every metric must answer a question that someone will act on. A metric nobody looks at is noise. A metric everybody looks at but nobody acts on is theatre. The telemetry shape's job isn't to produce numbers — it's to produce signals that route through Vellum to the right reader at the right time. The mycelial network detects weak signals across the organism. A single metric rarely matters. The pattern across metrics is the signal.

---

## 15. glue

### What it is

The adapter that connects shapes that don't naturally fit together.

### What it does

- Bridges two shapes with incompatible interfaces
- Translates one shape's output into another shape's expected input
- Exists because the real world is messy — not everything fits the taxonomy perfectly
- Should be temporary where possible (the goal is to fix the interface, not glue around it)
- Documents WHY the glue exists (the debt it represents)

### Enforced checklist

```
[ ] Source shape identified (what produces the output?)
[ ] Target shape identified (what expects the input?)
[ ] Mismatch documented (why don't these two shapes connect naturally?)
[ ] Transformation defined (what does the glue change?)
[ ] Temporary or permanent declared (is this glue meant to be removed?)
[ ] If temporary: removal condition defined (what needs to change for this glue to be deleted?)
[ ] If permanent: justification documented (why can't the interface be fixed?)
[ ] Technical debt ticket created (glue = acknowledged debt)
```

### Vellum pre-fill rules

- Pre-fill: source and target shapes from the ticket or the calling code
- Pre-fill: mismatch from the type difference between source output and target input
- Pre-fill: "temporary" as default (most glue should be temporary)
- Guess: transformation from the field mapping between source output and target input model
- Guess: removal condition from the source shape's roadmap

### Five shaped questions

1. Why can't the source shape's output be changed to match the target? (If it can, do that instead)
2. Why can't the target shape's input be changed to accept the source? (If it can, do that instead)
3. Is this glue hiding a design problem? (If yes, document the design problem, not just the glue)
4. How many other shapes use this same glue? (If more than 2, the interface should be fixed)
5. What is the removal condition? (When this is true, delete the glue)

### Three flags

```
[ ] Needs a research
[ ] Needs a tool
[ ] Needs a genius
```

### What it must NOT do

- Must NOT contain business logic (it translates, it doesn't decide)
- Must NOT become permanent without justification (glue is debt)
- Must NOT hide the mismatch (document it loudly — the mismatch is the signal)

### Contract

```
Input:  Output from source shape (typed)
Output: Input expected by target shape (typed, translated)
Error:  GlueError with: source_type, target_type, what_doesn't_fit
```

### Skeleton

```python
from amplified.shapes import GlueBase, monitored, debt_tracked

@debt_tracked(
    reason="Legacy Xero connector returns dict, new pipeline expects Invoice model",
    removal_condition="Xero connector migrated to new ConnectorBase (AMP-XXX)",
    temporary=True,
)
class XeroLegacyGlue(GlueBase):
    """Adapts legacy Xero dict output to Invoice model input."""

    source_shape = "XeroLegacyConnector"
    target_shape = "IngestionPipeline"

    @monitored
    def adapt(self, source_output: dict) -> Invoice:
        return Invoice(
            invoice_id=source_output["InvoiceID"],
            amount=Decimal(source_output["Total"]),
            issued_date=parse_xero_date(source_output["Date"]),
            due_date=parse_xero_date(source_output["DueDate"]),
            paid_date=parse_xero_date(source_output.get("FullyPaidOnDate")),
            status=map_xero_status(source_output["Status"]),
            line_items=self.map_line_items(source_output["LineItems"]),
        )
```

### Nuance

Glue is the only shape that should aspire to be deleted. Every other shape earns its place permanently. Glue earns its place temporarily — it exists because the world is messy and you can't fix everything at once. The nuance: glue that survives three months without a removal plan isn't glue anymore. It's architecture. If it's architecture, it should be a proper shape (connector, pipeline, whatever it actually is). The `@debt_tracked` decorator makes glue visible — it shows up in Vellum as acknowledged debt with a removal condition. When the condition is met, the glue lights up RED: "delete me."

---

## Shape × Colour mapping

Each shape has a natural colour from the Devon-58ca palette:

| Colour | Shapes | What the colour means |
|--------|--------|----------------------|
| **Blue** | model, config | Data definition — the contracts |
| **Green** | entry, connector | External boundary — where data enters/exits |
| **Red** | service, scorer, guard | Business logic — where decisions happen |
| **Yellow** | store, worker, pipeline | Infrastructure — where data moves and persists |
| **Purple** | agent, orchestrator | AI and coordination — where interpretation happens |
| **Grey** | test, telemetry, glue | Support — proves, measures, and adapts |

An agent sees the colour before reading the file. Knows what rules apply instantly.

---

## Shape × Pipe position

Where each shape sits in the flow:

```
INBOUND                                                          OUTBOUND
  │                                                                 │
  ▼                                                                 ▼
entry → guard → pipeline → service → store → Vellum → Brain → agent → entry (out)
  │                │           │                                │
  └── connector    └── scorer  └── worker                       └── connector
  │                                                                 │
  └── model (contracts throughout)                                  │
  └── config (knobs throughout)                                     │
  └── telemetry (sensors throughout)                                │
  └── orchestrator (coordinates throughout)                         │
  └── test (proves throughout)                                      │
  └── glue (adapts where needed)                                    │
```

---

## The Vellum proforma flow

When an agent needs to create a new file:

```
1. Agent declares: "I need to create a {shape}"
2. Vellum receives the shape name
3. Shape name triggers the enforced checklist (terminology enforces)
4. Vellum pre-fills everything it knows from:
   - Prior files of the same shape
   - Context from the ticket/task
   - Domain dictionary
   - Org conventions and defaults
5. Vellum guesses what it doesn't know (guess > blank)
6. Vellum presents the form with:
   - Pre-filled fields (confirmed or flagged as guess)
   - Five shaped questions for the free section
   - Three flags (needs research / needs tool / needs genius)
   - Empty fields only for genuinely novel content
7. Agent fills the minimum novel contribution
8. Guard validates the completed proforma
9. Vellum records the creation
10. The file is generated from the completed proforma
```

The form is 80% done before the agent opens it. The agent's job is the 20% that's actually new. Forms become a joy.

---

## Principles embedded

- **Huf Haus**: The wall arrives with pipes and electrics in. The template IS the wall. Fill in the room-specific logic.
- **Terminology enforces**: Name the shape, the checklist appears. No checklist, no submission. The name IS the rules.
- **Vellum pre-fills**: Everything it knows. Guesses where it can't. A guess gives sharper research than a blank space.
- **De-friction for agents**: The agent fills only what's genuinely new. The form shrinks to the novel contribution.
- **Three flags**: Needs a research. Needs a tool. Needs a genius. Honest escalation. Not failure — routing.
- **Needs a genius**: Capitalisation. An expert declared this is a bastard. Routes to the best available mind — human or AI. There are geniuses at the end of a world of billions of agents.
- **One shape per file**: If a file is two shapes, it's two files. No exceptions.
- **epistemic.py is Layer 0**: Every value wears its tier. Every boundary enforces the min-rule. Every violation halts.
- **Python is the pipe**: Shapes are Python. Python measures and moves. Vellum records what the shapes produce.
- **Reader-first**: Output shaped for the reader, not the writer. Always.
- **Consistency over correctness**: Same rules every time. A consistent system can be calibrated. A random system hides errors.

---

TIER: STRUCTURED  
Signed-by: Devon-58ca | 2026-05-17 | session devin-58caaceb8d3b48188ab11d10821038f1  
Source architect: Ewan Bramley (shape taxonomy, pre-fill principle, three flags, guess>blank, de-friction doctrine)  
