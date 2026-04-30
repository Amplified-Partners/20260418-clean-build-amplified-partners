# P10: Kill Switch — Binary Shutdown Architecture
# Master Reference — AI-Readable
# Amplified Partners

## DOCUMENT METADATA
```json
{
  "document_id": "P10-master",
  "title": "Kill Switch — Master Reference",
  "version": "1.0.0",
  "date": "2026-03-16",
  "author": "Perplexity Computer",
  "for": "AI systems (Cove orchestrator, agents, LLMs)",
  "format": "Structured markdown with JSON blocks for machine consumption",
  "parent_document": "07-customer-voice-intelligence.md",
  "section_reference": "Section 3.2 (kill_switch) and Section 6.1 (Rule R8)",
  "pipeline_position": "Cross-cutting — applies to ALL pipeline stages (P1-P9)",
  "relationship": "Override mechanism — can halt any and all subsystems immediately",
  "principles": [
    "If we get it wrong, we turn it off. We only want to help.",
    "Binary — ON or OFF. No 'reduce', no 'let's see how it goes'",
    "CEO-accessible — the business owner shuts it down in one action",
    "Immediate buffer purge — all capture stops, all buffers wiped, all processing halted",
    "Reversible — but requires manual re-activation of each device individually after review",
    "The ultimate trust mechanism — the business always has the power to stop everything"
  ]
}
```

---

## 1. SCOPE AND PURPOSE

### 1.1 What P10 Does

```json
{
  "purpose": "Provide a binary, CEO-accessible mechanism to immediately halt the entire Amplified system or any individual subsystem, purging all active buffers and stopping all data capture",
  "core_principle": "If we get it wrong, we turn it off. We only want to help.",
  "attribution": "Ewan Bramley, Amplified Partners, 2026-03-15",
  "what_p10_does": [
    "Provides a single-action shutdown accessible to the business owner (CEO)",
    "Immediately halts ALL data capture across ALL devices",
    "Purges ALL active audio buffers — no residual data remains",
    "Stops ALL processing pipelines (P1 through P9)",
    "Sends shutdown confirmation to all connected devices",
    "Logs the kill switch activation with timestamp and actor",
    "Notifies Amplified support team of system shutdown"
  ],
  "what_p10_does_not_do": [
    "NEVER partially reduces system capability — binary ON/OFF only",
    "NEVER requires technical knowledge to activate",
    "NEVER requires Amplified's permission or involvement to activate",
    "NEVER auto-restarts after shutdown — manual re-activation required",
    "NEVER deletes historical aggregated data — only purges active buffers",
    "NEVER requires multiple approval steps to ACTIVATE (single action)",
    "NEVER has a 'soft' or 'gradual' mode — it is immediate and total"
  ]
}
```

### 1.2 Why the Kill Switch Exists

```json
{
  "trust_architecture": {
    "problem": "Any system that captures customer voice data, however ethically designed, requires an absolute override. The business must ALWAYS have the power to stop everything.",
    "solution": "A binary kill switch that the CEO can activate in one action, with no technical barriers, no approval chains, and no delay.",
    "philosophy": "The kill switch IS the trust. Without it, every privacy promise is just words. With it, the business owner knows: if anything goes wrong, I can stop this instantly."
  },
  "relationship_to_rules": {
    "rule_r8": "If we get it wrong, we turn it off",
    "enforcement": "Kill switch. Binary. CEO-accessible. One action to disable entire system.",
    "this_is_not_optional": "The kill switch is not a feature — it is a precondition for deployment. No kill switch = no deployment."
  },
  "design_philosophy": "The best safety mechanism is the simplest one. A single button. A single action. A single outcome: everything stops."
}
```

---

## 2. KILL SWITCH ARCHITECTURE

### 2.1 Activation Modes

```json
{
  "activation_modes": [
    {
      "mode": "full_system_kill",
      "description": "Shuts down the entire Amplified system across all locations, all devices, all pipelines",
      "trigger": "Single action by CEO or authorised representative",
      "scope": "ALL subsystems (P1-P9), ALL devices, ALL locations",
      "buffer_action": "Purge ALL active audio buffers immediately",
      "processing_action": "Halt ALL pipelines immediately",
      "capture_action": "Stop ALL microphone capture immediately",
      "notification": "All devices display 'System Offline' indicator"
    },
    {
      "mode": "subsystem_kill",
      "description": "Shuts down a specific subsystem while leaving others running",
      "trigger": "Single action by CEO or authorised representative",
      "scope": "Targeted subsystem only (e.g., P5 inference, P6 training delivery)",
      "buffer_action": "Purge buffers related to targeted subsystem only",
      "processing_action": "Halt targeted pipeline only",
      "capture_action": "Capture continues if other subsystems still active",
      "use_case": "If inference (P5) is causing concern but sentiment capture (P2) is trusted"
    },
    {
      "mode": "location_kill",
      "description": "Shuts down all Amplified systems at a specific physical location",
      "trigger": "Single action by CEO, location manager, or authorised representative",
      "scope": "ALL subsystems at specified location",
      "buffer_action": "Purge ALL active buffers at specified location",
      "processing_action": "Halt ALL pipelines for specified location",
      "capture_action": "Stop ALL microphone capture at specified location",
      "use_case": "If a specific site has concerns but others are operating normally"
    }
  ]
}
```

### 2.2 Shutdown Sequence

```json
{
  "shutdown_sequence": {
    "step_1": {
      "name": "KILL signal broadcast",
      "timing": "T+0 (immediate)",
      "action": "Kill switch API sends KILL signal to all affected devices and services",
      "protocol": "Redis pub/sub broadcast on dedicated kill_switch channel",
      "guarantee": "Fire-and-forget with confirmation receipt — every device must ACK within 5 seconds"
    },
    "step_2": {
      "name": "Capture cessation",
      "timing": "T+0 to T+2 seconds",
      "action": "All microphone capture stops. Orange microphone indicators change to grey/off.",
      "guarantee": "Hardware-level mic disable where possible. Software disable as fallback."
    },
    "step_3": {
      "name": "Buffer purge",
      "timing": "T+0 to T+5 seconds",
      "action": "All active audio buffers overwritten with zeros then deallocated. Includes: raw audio buffers, transcription buffers, positive capture loop buffers, processing queues.",
      "guarantee": "Cryptographic erasure — buffer memory overwritten, not just deallocated"
    },
    "step_4": {
      "name": "Pipeline halt",
      "timing": "T+0 to T+10 seconds",
      "action": "All processing pipelines receive SIGTERM. Running jobs cancelled. Queue drained without processing.",
      "guarantee": "No in-flight data continues processing after kill signal"
    },
    "step_5": {
      "name": "Confirmation collection",
      "timing": "T+5 to T+30 seconds",
      "action": "System collects ACK from every affected device and service. Any non-responsive device is flagged for manual inspection.",
      "guarantee": "Dashboard shows green (confirmed stopped) or red (requires manual intervention) per device"
    },
    "step_6": {
      "name": "Audit log",
      "timing": "T+0 (logged at moment of activation)",
      "action": "Kill switch activation logged: timestamp, actor, scope, reason (optional free text)",
      "guarantee": "Audit log is append-only, tamper-evident, retained for compliance"
    },
    "step_7": {
      "name": "Notification dispatch",
      "timing": "T+0 to T+60 seconds",
      "action": "Amplified support team notified. Client contact notified. System status page updated.",
      "guarantee": "Multiple notification channels (email, SMS, webhook) for redundancy"
    }
  },
  "total_shutdown_time": "Under 30 seconds for full system kill. Under 5 seconds for capture cessation and buffer purge.",
  "design_goal": "From the moment the CEO presses the button, no new audio data is captured within 2 seconds and no buffered audio data exists within 5 seconds."
}
```

### 2.3 Access Control

```json
{
  "access_control": {
    "activation_access": {
      "primary": "Business owner (CEO) — always has access",
      "secondary": "Designated representatives (configurable, max 3)",
      "amplified": "Amplified support team — can activate on client request, CANNOT activate unilaterally",
      "authentication": "Multi-factor authentication to PREVENT accidental activation, but single action once authenticated",
      "design_principle": "Easy enough for a non-technical CEO. Secure enough to prevent accidental triggers."
    },
    "reactivation_access": {
      "who": "Business owner (CEO) or Amplified support team together",
      "process": "Manual re-activation of each device individually after review",
      "why_individual": "Forces a conscious decision per device. No 'turn everything back on' button. Each device re-enabled deliberately.",
      "review_required": "Before reactivation, the reason for shutdown must be documented and addressed"
    },
    "permission_asymmetry": {
      "activate": "Single action, single person, immediate",
      "reactivate": "Multi-step, per-device, requires review",
      "principle": "Shutting down must be trivially easy. Starting up must be deliberately hard. This asymmetry IS the safety design."
    }
  }
}
```

---

## 3. BUFFER PURGE ARCHITECTURE

### 3.1 What Gets Purged

```json
{
  "purge_targets": [
    {
      "buffer_type": "raw_audio_capture",
      "location": "On-device (capture hardware)",
      "purge_method": "Zero-fill then deallocate",
      "contains": "Unprocessed customer voice audio currently in capture buffer",
      "typical_size": "Seconds to minutes of audio",
      "purge_time": "< 2 seconds"
    },
    {
      "buffer_type": "transcription_buffer",
      "location": "On-device (processing hardware)",
      "purge_method": "Zero-fill then deallocate",
      "contains": "Audio awaiting transcription or mid-transcription",
      "typical_size": "Seconds to minutes of audio",
      "purge_time": "< 2 seconds"
    },
    {
      "buffer_type": "positive_capture_loop",
      "location": "On-device (processing hardware)",
      "purge_method": "Zero-fill then deallocate",
      "contains": "Positive moment audio in 24-48hr consent-gated buffer",
      "typical_size": "Up to 48 hours of flagged positive clips",
      "purge_time": "< 5 seconds"
    },
    {
      "buffer_type": "processing_queue",
      "location": "Server (Redis message queue)",
      "purge_method": "Queue flush — all pending messages discarded",
      "contains": "Sentiment analysis jobs, inference jobs, training triggers",
      "typical_size": "Variable — depends on processing backlog",
      "purge_time": "< 2 seconds"
    },
    {
      "buffer_type": "in_flight_processing",
      "location": "Server (processing workers)",
      "purge_method": "SIGTERM to workers, discard partial results",
      "contains": "Mid-processing sentiment analysis, mid-inference calculations",
      "typical_size": "Variable",
      "purge_time": "< 10 seconds"
    }
  ],
  "what_is_NOT_purged": {
    "historical_aggregates": "Stored aggregated sentiment data (NSS scores, trend data) is NOT purged — this is already anonymised P2 data",
    "audit_logs": "System audit logs are NEVER purged — compliance requirement",
    "kill_switch_logs": "Kill switch activation history is NEVER purged",
    "team_wellbeing_history": "Historical team-level indicators are NOT purged — already aggregated",
    "rationale": "The kill switch stops NEW data capture and processing. It does not destroy historical analytics that are already anonymised and aggregated. Destroying historical data would be a different action with different implications."
  }
}
```

---

## 4. REACTIVATION PROTOCOL

### 4.1 Reactivation Process

```json
{
  "reactivation_protocol": {
    "preconditions": [
      "Shutdown reason must be documented in the audit log",
      "Root cause (if applicable) must be identified and addressed",
      "Business owner must explicitly approve reactivation",
      "If shutdown was due to a bug/error, fix must be verified"
    ],
    "process": {
      "step_1": "Business owner initiates reactivation request",
      "step_2": "System displays list of all devices/subsystems that were shut down",
      "step_3": "Each device/subsystem must be individually re-enabled — NO 'select all'",
      "step_4": "Each re-enabled device runs self-test before resuming capture",
      "step_5": "Reactivation logged with timestamp, actor, scope, and reason",
      "step_6": "System enters 24-hour heightened monitoring after reactivation"
    },
    "individual_device_reactivation": {
      "why": "Forces deliberate review of each capture point. A location might have 5 microphones — each one must be consciously re-enabled. This prevents careless 'just turn everything back on' behaviour.",
      "display": "For each device: location, last capture timestamp before shutdown, device status, self-test result",
      "action": "Explicit 'Enable' action per device"
    },
    "heightened_monitoring": {
      "duration": "24 hours after any reactivation",
      "what": "All system metrics monitored at 10x normal frequency",
      "alerts": "Lower thresholds for anomaly alerts during monitoring period",
      "purpose": "Catch any recurrence of the issue that caused shutdown"
    }
  }
}
```

---

## 5. NON-NEGOTIABLE RULES — P10

```json
{
  "rules": [
    {
      "id": "P10-R1",
      "rule": "Kill switch activation requires exactly ONE action from an authorised person",
      "enforcement": "Physical — single API endpoint, single button in UI, no confirmation dialogs beyond initial auth",
      "rationale": "In a crisis, every additional click is a delay. Auth happens once. Shutdown happens once."
    },
    {
      "id": "P10-R2",
      "rule": "Kill switch is binary — ON or OFF. No partial states, no dimmer switch, no gradual reduction",
      "enforcement": "Physical — system state is boolean. Enum: ACTIVE or KILLED. No other states exist.",
      "rationale": "'Let's see how it goes' is not a safety mechanism. If there's a reason to shut down, shut down."
    },
    {
      "id": "P10-R3",
      "rule": "All active audio buffers must be purged within 5 seconds of kill switch activation",
      "enforcement": "Physical — cryptographic erasure (zero-fill) of all buffer memory. Timed. Verified.",
      "rationale": "If the system is shut down, no captured audio should exist. Period."
    },
    {
      "id": "P10-R4",
      "rule": "Reactivation requires individual device re-enablement — no bulk 'turn everything on'",
      "enforcement": "Physical — no 'select all' option in reactivation UI. Each device is a separate action.",
      "rationale": "Shutting down is easy. Starting up is hard. This asymmetry IS the safety design."
    },
    {
      "id": "P10-R5",
      "rule": "Kill switch must function independently of all other system components",
      "enforcement": "Physical — dedicated service, dedicated database, dedicated network path. If the main system is down, the kill switch still works.",
      "rationale": "A kill switch that depends on the system it's killing is not a kill switch."
    },
    {
      "id": "P10-R6",
      "rule": "The business owner can NEVER be locked out of the kill switch",
      "enforcement": "Physical — multiple access paths (web UI, API, phone call to Amplified). Hardware token as backup.",
      "rationale": "The kill switch is the ultimate trust mechanism. If the CEO can't reach it, trust is broken."
    },
    {
      "id": "P10-R7",
      "rule": "All kill switch activations are logged in a tamper-evident audit trail",
      "enforcement": "Physical — append-only log, cryptographically signed entries, retained indefinitely",
      "rationale": "For compliance, accountability, and root cause analysis."
    }
  ]
}
```

---

## 6. PIPELINE RELATIONSHIPS

### 6.1 How P10 Relates to Other Pipeline Stages

```json
{
  "pipeline_relationships": {
    "P1_voice_capture": {
      "kill_effect": "All microphones stop capture. Orange indicators go grey/off.",
      "buffer_effect": "Raw audio buffers purged immediately.",
      "reversibility": "Each microphone must be individually re-enabled."
    },
    "P2_sentiment_analysis": {
      "kill_effect": "All sentiment processing halts. In-flight analyses discarded.",
      "buffer_effect": "Processing queues flushed.",
      "reversibility": "Pipeline resumes on reactivation. No data loss — capture was also stopped."
    },
    "P3_aggregate_intelligence": {
      "kill_effect": "Aggregation stops. No new data flows in.",
      "buffer_effect": "In-flight aggregation jobs cancelled.",
      "data_retention": "Historical aggregated data is NOT purged (already anonymised P2)."
    },
    "P4_baseline_calibration": {
      "kill_effect": "Calibration pauses. Baselines frozen at pre-shutdown state.",
      "reactivation_note": "After reactivation, baselines may need recalibration if shutdown was extended."
    },
    "P5_staff_wellbeing_inference": {
      "kill_effect": "All inference halts. No new team indicators generated.",
      "buffer_effect": "In-flight inference calculations discarded.",
      "data_retention": "Historical team-level indicators NOT purged."
    },
    "P6_training_as_support": {
      "kill_effect": "Training delivery continues IF already on personal device — P10 does not reach into personal phones. But no NEW training triggers are generated.",
      "note": "P6 runs on personal phones — the kill switch cannot and should not reach personal devices. It stops the pipeline that FEEDS P6, not P6 itself."
    },
    "P7_positive_capture_loop": {
      "kill_effect": "Positive capture buffers purged immediately. No new positive moments captured.",
      "consent_impact": "Any pending consent requests cancelled. Buffered positive audio deleted."
    },
    "P8_visualization": {
      "kill_effect": "Dashboard shows 'System Offline' state. Historical data remains visible.",
      "display": "Clear visual indicator that the system is in KILLED state."
    },
    "P9_violence_detection": {
      "kill_effect": "Violence detection halts — this is an accepted trade-off.",
      "note": "The kill switch overrides EVERYTHING, including safety features. The CEO's judgement is the ultimate override.",
      "rationale": "A kill switch with exceptions is not a kill switch."
    }
  }
}
```

---

## 7. TECHNICAL INDEPENDENCE

### 7.1 Kill Switch Service Architecture

```json
{
  "independence_requirements": {
    "separate_service": "Kill switch runs as an independent microservice, not part of the main application",
    "separate_database": "Kill switch state stored in separate database — not the main PostgreSQL instance",
    "separate_network": "Kill switch API accessible via dedicated endpoint, not behind main application routing",
    "separate_authentication": "Kill switch auth is independent of main system auth",
    "health_monitoring": "Kill switch service has its own health checks, independent of main system health",
    "rationale": "If the main system crashes, hangs, or becomes unresponsive, the kill switch must still function. A kill switch that goes down with the ship defeats the purpose."
  },
  "fallback_paths": {
    "primary": "Web UI dashboard — single button",
    "secondary": "Direct API call — single POST request",
    "tertiary": "Phone call to Amplified support — they activate on behalf of client",
    "quaternary": "Hardware token (if deployed) — physical device sends kill signal",
    "design_principle": "At least two independent paths to kill switch at all times"
  }
}
```

---

## 8. THE TRUST MECHANISM

### 8.1 Why This Matters Beyond Engineering

```json
{
  "trust_architecture": {
    "the_promise": "If we get it wrong, we turn it off. We only want to help.",
    "the_proof": "The kill switch exists. It works. The CEO can press it. Everything stops.",
    "the_test": "The kill switch is tested regularly. It works in under 30 seconds. Buffers are verified empty.",
    "the_asymmetry": "Starting is hard. Stopping is easy. This is by design.",
    "the_philosophy": "A system that monitors customer voice data cannot exist without absolute, immediate, and accessible override capability. The kill switch is not a feature — it is a precondition."
  },
  "deployment_gate": {
    "rule": "No Amplified system deploys to a client site without a verified, tested kill switch",
    "verification": "Kill switch must be demonstrated to the business owner before go-live",
    "testing": "Kill switch activation test must complete successfully within 30 seconds",
    "documentation": "Business owner must sign acknowledgement that they understand and can access the kill switch"
  }
}
```

---

## 9. RELATED DOCUMENTS

```json
{
  "related": [
    {
      "doc_id": "P1",
      "title": "Customer Voice Capture",
      "relationship": "P10 stops all P1 capture devices and purges audio buffers"
    },
    {
      "doc_id": "P5",
      "title": "Staff Wellbeing Inference",
      "relationship": "P10 halts all inference processing"
    },
    {
      "doc_id": "P7",
      "title": "Positive Capture Loop",
      "relationship": "P10 purges positive capture buffers (24-48hr consent-gated audio)"
    },
    {
      "doc_id": "P9",
      "title": "Violence Detection",
      "relationship": "P10 overrides even violence detection — total shutdown means total"
    },
    {
      "doc_id": "Rules",
      "title": "Non-Negotiable Rules",
      "relationship": "P10 is the enforcement mechanism for Rule R8"
    },
    {
      "doc_id": "07",
      "title": "Customer Voice Intelligence — Privacy-First Sentiment Architecture",
      "relationship": "Parent document. P10 covers Section 3.2 (kill_switch) and Rule R8."
    }
  ]
}
```

---

## SOURCES

All sources with URLs are cited inline throughout this document in JSON blocks.
Full source index available at: /home/user/workspace/doc-context/07-research-compiled.md

Primary sources:
1. Doc 07 Section 3.2 — Privacy Architecture (kill_switch): `/home/user/workspace/doc-output/07-customer-voice-intelligence.md`
2. Doc 07 Section 6.1 — Non-Negotiable Rules (R8): `/home/user/workspace/doc-output/07-customer-voice-intelligence.md`
3. User Principles — Enforcement Philosophy: `/home/user/workspace/doc-context/user-principles.md`
