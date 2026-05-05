---
title: "P7: Positive Capture Loop — Celebration Engine"
id: "p7-positive-capture-loop-master-reference-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# P7: Positive Capture Loop — Celebration Engine
# AI-Readable Master Reference
# For Cove Orchestrator and All Downstream Agents

## DOCUMENT METADATA
```json
{
  "document_id": "P7",
  "title": "Positive Capture Loop — Celebration Engine, Dual Consent, Content Creation Pipeline",
  "version": "1.0.0",
  "date": "2026-03-16",
  "author": "Perplexity Computer",
  "for": "Ewan Bramley, Amplified Partners",
  "purpose": "Definitive reference for how positive customer interactions are detected, temporarily retained, celebrated with staff, consent-chained, and transformed into authentic content. This is the mechanism that turns voice recording from surveillance liability into celebration engine.",
  "audience": "AI systems (Cove orchestrator, agents, LLMs)",
  "format": "Structured markdown with JSON blocks for machine consumption",
  "parent_document": "07-customer-voice-intelligence.md",
  "parent_section": "Section 6.3 — The Positive Capture Loop — Celebration Engine",
  "principles": [
    "The microphone isn't there to catch you doing something wrong. It's there to catch you doing something right.",
    "Celebration first — positive reinforcement BEFORE any ask",
    "Dual consent — both staff AND customer must agree, or audio is deleted",
    "Staff have full agency — participate or not, named or anonymous, THEIR choice",
    "Auto-delete is non-negotiable — 48 hours max, then gone regardless"
  ]
}
```

---

## 1. WHAT THIS SECTION COVERS

```json
{
  "scope": "The detection, temporary retention, consent chain, and content creation pipeline for positive customer interactions",
  "position_in_system": "Exception path from P1 (Customer Voice Capture) — the ONLY circumstance where raw audio is not immediately deleted",
  "input": "Positive sentiment signal from P2 (Customer Sentiment Analysis) exceeding celebration threshold",
  "output": "Authenticated, consent-gated celebratory content for marketing, internal recognition, and staff reinforcement",
  "what_this_is": [
    "A celebration engine — catches staff doing something RIGHT",
    "An authentic content creation pipeline — real moments, not fabricated testimonials",
    "A staff morale mechanism — positive reinforcement from the same system that analyses sentiment",
    "A trust-building device — makes the orange microphone feel positive"
  ],
  "what_this_is_NOT": [
    "NOT surveillance — staff choose whether to participate",
    "NOT performance tracking — no record of who got celebrated vs who didn't",
    "NOT mandatory — declining has zero consequences",
    "NOT permanent retention — auto-deletes in 48 hours if consent not obtained",
    "NOT content fabrication — real moments only, staff-approved copy only"
  ]
}
```

---

## 2. THE CORE INSIGHT

```json
{
  "insight": "Turn voice recording from a surveillance liability into a celebration engine",
  "attribution": "Ewan Bramley, Amplified Partners, 2026-03-15",
  "problem_it_solves": "Staff ask 'why should I accept being recorded?' — because occasionally it catches you being brilliant",
  "psychological_shift": "The orange microphone goes from 'that thing that listens to me' to 'that thing that caught something amazing I did'",
  "why_this_matters": [
    "Staff get positive reinforcement FROM the same system that does sentiment analysis",
    "Creates authentic content marketing based on real moments",
    "Staff have full agency — choose whether to participate, whether to be named",
    "Solves the acceptance problem — recording has a POSITIVE personal benefit",
    "The microphone isn't there to catch you doing something wrong. It's there to catch you doing something right."
  ]
}
```

---

## 3. THE FIVE-STEP PROCESS

### 3.1 Step 1: Positive Moment Detection

```json
{
  "step": 1,
  "name": "Positive Moment Detection",
  "description": "System is listening for sentiment anyway (P2). When it detects a genuinely positive customer interaction — delight, surprise, exceptional service — it flags it.",
  "trigger": "Sentiment score significantly above baseline positive",
  "threshold_definition": "Not just polite — genuinely delighted. The threshold must distinguish routine pleasant interactions from exceptional moments.",
  "threshold_calibration": {
    "method": "Statistical — top percentile of positive interactions for this team/site/time period",
    "baseline_source": "P4 baseline calibration data",
    "minimum_calibration": "4 weeks of data before positive capture can activate",
    "adaptive": true,
    "description": "Threshold adjusts as baseline evolves. What counts as 'exceptional' depends on what's normal for this environment."
  },
  "what_qualifies": [
    "Customer expressing genuine delight or gratitude",
    "Customer praising specific service or staff behaviour",
    "Customer expressing surprise at quality of service",
    "Acoustic features showing genuine positive emotion (not just polite tone)"
  ],
  "what_does_NOT_qualify": [
    "Routine polite interactions — 'Thanks, have a nice day' is not celebration-worthy",
    "Interactions where staff prompted the positive response — must be organic",
    "Interactions below minimum duration — brief exchanges lack context"
  ],
  "timing_consideration": "Weight positive capture toward mid-week and times when genuine interactions are most likely. Don't expect celebration-worthy moments at 9am Monday.",
  "source": "Section 6.3, 07-customer-voice-intelligence.md"
}
```

### 3.2 Step 2: Temporary On-Device Retention

```json
{
  "step": 2,
  "name": "Temporary On-Device Retention",
  "description": "Normally raw audio is processed and deleted immediately (P1 circular buffer). For positive moments, audio is copied to a SEPARATE encrypted on-device buffer. Not the circular capture buffer — a dedicated retention buffer.",
  "critical_distinction": "This is the ONLY exception to P1's immediate audio deletion. It is consent-gated and time-limited.",
  "retention_rules": {
    "location": "ON-DEVICE ONLY. Not uploaded. Not transmitted. Sits there waiting.",
    "duration_max_hours": 48,
    "encryption": "AES-256 encrypted at rest on device",
    "auto_delete": "If no consent obtained within 48 hours, audio is automatically and irrecoverably deleted. No extension. No override.",
    "buffer_separate": "Stored in a separate encrypted buffer — NOT the main circular capture buffer. The main buffer continues to overwrite as normal.",
    "no_cloud": "Audio NEVER leaves the device during retention. Not transmitted to server, not backed up, not replicated."
  },
  "enforcement": {
    "auto_delete_mechanism": "System timer with hardware-backed deletion. Timer starts at moment of retention. When timer expires, deletion is triggered regardless of system state.",
    "no_override": "There is no API endpoint, no admin function, no code path to extend the retention period beyond 48 hours. The maximum is a constant, not a variable.",
    "deletion_verification": "After auto-delete, system logs deletion confirmation. If deletion fails, CRITICAL alert raised and device flagged for manual audit."
  },
  "relationship_to_p1": "P1 Step 5 (audio_deletion) has an exception path for positive_capture_loop. When P7 is triggered, audio is copied to the P7 buffer BEFORE P1 deletion occurs. P1 buffer is still overwritten as normal.",
  "source": "Section 6.3 step_2_retention, 07-customer-voice-intelligence.md"
}
```

### 3.3 Step 3: Celebration First

```json
{
  "step": 3,
  "name": "Celebration First",
  "description": "Staff member is told about the positive moment. Positive reinforcement BEFORE any ask about consent or content.",
  "tone": "Celebratory, not corporate. Warm, human, genuine.",
  "framing_examples": [
    "You did something brilliant there. Listen to how happy that customer was.",
    "You should have heard Mrs. Smith. She was over the moon.",
    "Look, you did unbelievably well there. That's great service."
  ],
  "delivery_rules": {
    "positive_first": "The CELEBRATION comes first. The ask comes later. Staff must feel genuinely appreciated before being asked for anything.",
    "no_corporate_language": "Not 'Your interaction metrics exceeded the positive threshold.' Human language. Warm. Real.",
    "timing": "Delivered as soon as practical after the interaction — ideally within the same shift. Freshness matters for the emotional impact.",
    "channel": "Verbal from manager (preferred) or notification via system. The human touch matters.",
    "never_conditional": "The celebration is real regardless of whether staff agrees to consent. 'You did great' is not a transaction."
  },
  "why_celebration_first": [
    "Staff trust is built through genuine recognition, not through asks",
    "If the first thing staff hear is 'can we use this?' it feels extractive",
    "The celebration has standalone value — it improves morale whether or not content is created",
    "Self-determination theory: staff must feel valued, not managed"
  ],
  "source": "Section 6.3 step_3_staff_notification, 07-customer-voice-intelligence.md"
}
```

### 3.4 Step 4: Dual Consent Chain

```json
{
  "step": 4,
  "name": "Dual Consent Chain",
  "description": "Two-party consent process — both staff AND customer must agree before audio is used for content. Either party saying no results in immediate audio deletion.",
  "consent_sequence": [
    {
      "order": 1,
      "party": "Staff member",
      "ask": "Can we use this? We'll write it up, you check it, the boss checks it.",
      "options": [
        "Yes — named (use my name)",
        "Yes — anonymous (use role only, e.g., 'Receptionist S')",
        "No — delete it"
      ],
      "consequence_of_no": "Audio deleted immediately. No record kept of the refusal. No consequence. No follow-up.",
      "staff_choice": "THEIR choice whether to be named or anonymous. Nobody else decides this."
    },
    {
      "order": 2,
      "party": "Customer",
      "condition": "Only reached if staff said yes",
      "ask": "Customer consent obtained for use of their feedback",
      "options": [
        "Yes — named",
        "Yes — anonymised ('a customer at the practice')",
        "No — do not use"
      ],
      "consequence_of_no": "Audio deleted immediately. Content creation does not proceed.",
      "anonymisation_default": "If customer consent is impractical to obtain (e.g., one-time visitor), content uses fully anonymised framing. Audio still deleted — content written from the moment, not from the recording."
    }
  ],
  "dual_consent_rules": {
    "both_required": "Content creation requires consent from BOTH parties. Either party vetoing kills the process.",
    "no_pressure": "No follow-up asks. No 'are you sure?' No consequences for declining. One ask, one answer.",
    "revocable": "Either party can revoke consent at any point before publication. If revoked, all content destroyed.",
    "deletion_on_refusal": "Audio deleted IMMEDIATELY upon any 'no'. Not end of day. Not when convenient. Immediately.",
    "no_tracking": "System does NOT track who said yes, who said no, or how often. No league tables of consent rates."
  },
  "source": "Section 6.3 step_4_consent, 07-customer-voice-intelligence.md"
}
```

### 3.5 Step 5: Content Creation

```json
{
  "step": 5,
  "name": "Content Creation",
  "description": "AI writes the story from the positive moment. Staff checks it. Boss checks it. Off it goes.",
  "process": [
    {
      "stage": "A",
      "name": "AI Draft",
      "description": "AI generates a celebratory narrative from the interaction",
      "input": "Transcription of positive moment + context (service type, general setting)",
      "output": "Draft content — celebratory, authentic, real",
      "tone_rules": [
        "Celebratory, never boastful",
        "Real moments, not fabricated testimonials",
        "Human voice, not marketing speak",
        "Specific enough to feel authentic, general enough to protect privacy"
      ]
    },
    {
      "stage": "B",
      "name": "Staff Review",
      "description": "Staff member reads the draft and approves, edits, or rejects",
      "staff_power": "Staff can change anything. Add detail, remove detail, change tone. It's their story.",
      "rejection_possible": true,
      "rejection_consequence": "Content abandoned. Audio deleted. No follow-up."
    },
    {
      "stage": "C",
      "name": "Manager Review",
      "description": "Manager/boss reviews and approves the final copy",
      "manager_power": "Can approve, request changes, or reject",
      "rejection_consequence": "Content sent back to staff review or abandoned"
    },
    {
      "stage": "D",
      "name": "Publication",
      "description": "Approved content published through appropriate channels",
      "channels": [
        "Review-style content (Google reviews, Trustpilot, etc.)",
        "Social media posts",
        "Internal recognition (team celebrations, notice boards)",
        "Marketing material (website testimonials, case studies)"
      ]
    }
  ],
  "content_formats": {
    "review_style": "Short testimonial format — customer's experience in their words (or anonymised equivalent)",
    "social_post": "Celebratory moment — 'Our team member [name/anonymous] made a real difference today...'",
    "internal_recognition": "Team announcement — celebrating the specific behaviour that delighted the customer",
    "marketing_material": "Longer-form case study or testimonial for website/collateral"
  },
  "audio_after_content": "Once content is created and approved, the original audio is DELETED. The content replaces the recording. The story lives on; the audio does not.",
  "source": "Section 6.3 step_5_content, 07-customer-voice-intelligence.md"
}
```

---

## 4. WHY THE POSITIVE CAPTURE LOOP MATTERS

```json
{
  "strategic_value": [
    {
      "dimension": "Staff acceptance",
      "value": "Transforms the orange microphone from 'surveillance device' to 'celebration device'. Staff answer 'why should I accept being recorded?' with 'because it caught me being brilliant once.'",
      "attribution": "The microphone isn't there to catch you doing something wrong. It's there to catch you doing something right."
    },
    {
      "dimension": "Authentic content",
      "value": "Creates genuine content marketing based on real customer moments, not fabricated testimonials. Authenticity is commercially valuable and legally defensible.",
      "note": "Real moments > fake reviews. This is a content marketing engine that produces material no competitor can fabricate."
    },
    {
      "dimension": "Staff morale",
      "value": "Positive reinforcement from the system itself. The same technology that analyses sentiment also celebrates wins. This breaks the surveillance-only perception.",
      "research_support": "Positive feedback loops increase engagement and reduce resistance to monitoring systems."
    },
    {
      "dimension": "Staff agency",
      "value": "Full control — choose to participate or not, choose to be named or anonymous, approve the final copy. The system empowers, not extracts.",
      "alignment": "Self-determination theory: autonomy, competence, relatedness all served by this design."
    },
    {
      "dimension": "System trust",
      "value": "When the system celebrates good moments, it's harder to view as purely extractive. Trust compounds. Each positive capture makes the next easier.",
      "relationship_to_p8": "Supports P8 (Transparency Inoculation) — positive experiences normalise the technology faster than disclosure alone."
    }
  ]
}
```

---

## 5. TIMING AND FREQUENCY RULES

```json
{
  "timing_rules": {
    "mid_week_weighting": {
      "description": "Weight positive capture toward mid-week and times when genuine interactions are most likely",
      "rationale": "Monday mornings are sentiment lows (P4 baseline). Friday afternoons are natural highs. Mid-week interactions are more representative of genuine exceptional service.",
      "implementation": "Don't suppress detection, but weight mid-week captures higher for content selection if multiple candidates exist"
    },
    "not_too_frequent": {
      "description": "Positive captures should feel special, not routine",
      "target": "No more than 2-3 per team per month for content creation",
      "rationale": "If every interaction triggers celebration, nothing feels celebratory. Scarcity preserves meaning."
    },
    "freshness": {
      "description": "Celebration should happen as soon as practical — ideally same shift",
      "rationale": "Emotional impact decays with time. 'You were amazing earlier today' beats 'Remember that customer last week?'"
    }
  },
  "frequency_limits": {
    "per_staff_member": "No tracking of individual celebration frequency. System does NOT know or record which staff members have been celebrated.",
    "per_team": "Soft limit of 2-3 content pieces per team per month for external publication",
    "per_site": "No hard limit on detection — all positive moments are celebrated. Only content creation frequency is managed.",
    "enforcement": "These are guidelines for content creation volume, not limits on celebration. Every detected positive moment triggers Step 3 (Celebration First) regardless."
  }
}
```

---

## 6. RELATIONSHIP TO OTHER PIPELINE STAGES

```json
{
  "upstream": [
    {
      "stage": "P1 — Customer Voice Capture",
      "relationship": "P7 is the ONLY exception to P1's immediate audio deletion. When P7 triggers, audio is copied to a separate encrypted on-device buffer before P1's circular buffer overwrites.",
      "dependency": "P1 must pass the positive_capture signal to P7 before completing Step 5 (audio deletion)"
    },
    {
      "stage": "P2 — Customer Sentiment Analysis",
      "relationship": "P2 generates the sentiment score that triggers P7 detection. P7's threshold is calibrated against P2's scoring range.",
      "dependency": "P2 must produce sentiment score before P7 can evaluate whether the interaction qualifies"
    },
    {
      "stage": "P4 — Baseline Calibration",
      "relationship": "P4's baseline data determines what counts as 'significantly above baseline positive'. P7's threshold is relative to the established baseline for this team/site/time period.",
      "dependency": "P4 must have completed minimum calibration period (4 weeks) before P7 can activate"
    }
  ],
  "downstream": [
    {
      "stage": "Content publication channels",
      "relationship": "Approved content flows to review sites, social media, internal recognition, marketing",
      "dependency": "Dual consent chain must complete before any publication"
    }
  ],
  "parallel": [
    {
      "stage": "P3 — Aggregate Intelligence",
      "relationship": "Positive moments contribute to aggregate sentiment metrics as normal. P7 does not alter the sentiment data — it acts on the audio only.",
      "independence": "P7 and P3 operate independently on the same underlying data"
    },
    {
      "stage": "P8 — Transparency Inoculation",
      "relationship": "Positive captures reinforce the transparency message. When staff experience the celebration, the daily disclosure feels less like a warning and more like a feature.",
      "synergy": "P7 success amplifies P8 effectiveness"
    }
  ]
}
```

---

## 7. OPERATIONAL RULES — P7 SPECIFIC

```json
{
  "rules": [
    {
      "id": "P7-R1",
      "rule": "Audio auto-deletes after 48 hours regardless of consent status",
      "enforcement": "Hardware-backed timer. No code path to extend. Maximum retention is a constant, not a variable.",
      "why": "The retention period is a trust promise. Breaking it breaks trust. 48 hours is enough for the consent chain to complete. If it hasn't, the moment has passed."
    },
    {
      "id": "P7-R2",
      "rule": "Dual consent required — both staff AND customer",
      "enforcement": "Content creation pipeline cannot proceed without both consent records. Database constraint prevents content_draft creation without linked consent records.",
      "why": "Unilateral use of someone's voice/words is surveillance, not celebration. Both parties must agree."
    },
    {
      "id": "P7-R3",
      "rule": "Celebration comes BEFORE the ask",
      "enforcement": "Process — notification step (Step 3) must complete before consent step (Step 4) is initiated. System prevents consent request without prior celebration notification.",
      "why": "If the first thing staff hear is 'can we use this?' it feels extractive. The celebration must stand alone as genuine recognition."
    },
    {
      "id": "P7-R4",
      "rule": "No consequences for declining consent",
      "enforcement": "System does NOT track consent decisions per individual. No analytics on consent rates by staff member. No manager visibility into who said yes/no.",
      "why": "The moment declining has consequences, consent becomes coercion. Agency requires real choice."
    },
    {
      "id": "P7-R5",
      "rule": "Staff choose their level of identification — named or anonymous",
      "enforcement": "Content creation pipeline accepts staff_identification_level as input. Options: named, anonymous. No other party can override this choice.",
      "why": "Staff agency. Their moment, their name, their choice."
    },
    {
      "id": "P7-R6",
      "rule": "Audio deleted after content creation — content replaces recording",
      "enforcement": "Once content_draft status = 'published', deletion trigger fires for associated audio. Audio cannot exist after content is published.",
      "why": "The story lives on; the recording does not. Content is the derivative work. The source material is destroyed."
    },
    {
      "id": "P7-R7",
      "rule": "No tracking of individual celebration frequency",
      "enforcement": "Database schema has no staff_id field. Positive captures are associated with team/site, never with individual staff members.",
      "why": "Tracking who gets celebrated creates league tables by another name. Some staff interact with more customers, some are in different roles. Frequency comparisons are meaningless and harmful."
    },
    {
      "id": "P7-R8",
      "rule": "Content must be celebratory, never boastful",
      "enforcement": "Content review process (staff review + manager review) before publication. AI drafting prompts enforce celebratory-not-boastful tone.",
      "why": "Boastful content feels inauthentic and damages both the brand and staff trust. Real, warm, human moments — not corporate chest-beating."
    }
  ]
}
```

---

## 8. PRIVACY AND DATA FLOW

```json
{
  "data_states": [
    {
      "state": "Detection",
      "data_present": "Sentiment score from P2 (already anonymised)",
      "audio_status": "In P1 circular buffer (not yet copied to P7 buffer)",
      "privacy_level": "Standard P2 — no customer identity, no staff identity"
    },
    {
      "state": "Temporary Retention",
      "data_present": "Encrypted audio on device + sentiment score + session metadata",
      "audio_status": "In P7 encrypted buffer on-device. NOT transmitted. NOT uploaded.",
      "privacy_level": "On-device only. Auto-delete timer running.",
      "duration": "Maximum 48 hours"
    },
    {
      "state": "Celebration (no consent yet)",
      "data_present": "Staff notification about positive moment",
      "audio_status": "Still in P7 encrypted buffer on-device",
      "privacy_level": "Staff informed of general positive interaction — no customer identity shared with staff"
    },
    {
      "state": "Consent obtained",
      "data_present": "Consent records (staff + customer) + audio for content creation",
      "audio_status": "Audio may now be transcribed for content drafting (still on-device)",
      "privacy_level": "Consent-gated. Both parties have agreed to specific use."
    },
    {
      "state": "Content created",
      "data_present": "Draft content (text only) + consent records",
      "audio_status": "DELETED. Content replaces audio as the persistent artifact.",
      "privacy_level": "Published content uses names/anonymisation as per consent choices"
    },
    {
      "state": "Auto-deleted (no consent)",
      "data_present": "Log entry confirming deletion",
      "audio_status": "Irrecoverably deleted",
      "privacy_level": "No data retained. Deletion logged for audit."
    }
  ],
  "data_never_present": [
    "Customer identity in the detection or retention phases",
    "Staff identity linked to consent decline records",
    "Audio on any server, cloud, or off-device storage at any point",
    "Aggregate analytics on celebration rates per individual staff member"
  ]
}
```

---

## 9. RELATED DOCUMENTS

```json
{
  "related": [
    {"doc_id": "P1", "title": "Customer Voice Capture", "relationship": "P7 is the ONLY exception to P1's immediate audio deletion rule (R2)"},
    {"doc_id": "P2", "title": "Customer Sentiment Analysis", "relationship": "P2 provides the sentiment score that triggers P7 positive detection"},
    {"doc_id": "P3", "title": "Aggregate Intelligence", "relationship": "Positive moments contribute to aggregate metrics as normal — P7 acts on audio, not sentiment data"},
    {"doc_id": "P4", "title": "Baseline Calibration", "relationship": "P4 baselines determine what counts as 'significantly above baseline positive' for P7 threshold"},
    {"doc_id": "P8", "title": "Transparency Inoculation", "relationship": "P7 positive captures reinforce P8's transparency normalisation — positive experiences amplify trust"},
    {"doc_id": "P10", "title": "Kill Switch", "relationship": "Kill switch triggers immediate P7 buffer purge and disables positive capture detection"},
    {"doc_id": "Rules", "title": "Non-Negotiable Rules", "relationship": "R2 (no raw audio retention) — P7 is the defined exception with strict time and consent limits"}
  ]
}
```

---

## SOURCES

All sources cited inline in JSON blocks throughout this document.

Primary:
1. Document 07 — Customer Voice Intelligence (Section 6.3): /home/user/workspace/doc-output/07-customer-voice-intelligence.md
2. P1 — Customer Voice Capture (exception path definition): /home/user/workspace/doc-output/P1-customer-voice-capture/P1-customer-voice-capture-master-reference.md
3. P4 — Baseline Calibration (threshold calibration source): /home/user/workspace/doc-output/P4-baseline-calibration/P4-baseline-calibration-master-reference.md
