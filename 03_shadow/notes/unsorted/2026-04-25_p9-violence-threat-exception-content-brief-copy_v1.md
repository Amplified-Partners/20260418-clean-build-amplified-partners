---
title: "P9: Violence/Threat Exception — The Only Exception"
id: "p9-violence-threat-exception-content-brief-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# P9: Violence/Threat Exception — The Only Exception
# Content Brief — For Content Creators
# Amplified Partners

## DOCUMENT METADATA
```json
{
  "document_id": "P9-content",
  "title": "Violence/Threat Exception — Content Brief",
  "version": "1.0.0",
  "date": "2026-03-16",
  "author": "Perplexity Computer",
  "for": "Content creators (human or AI) writing about Amplified's violence/threat exception",
  "tone": "Human, warm, Ewan's voice where possible. The story, not the spec.",
  "parent": "P9-violence-threat-exception-master-reference.md"
}
```

---

## 1. THE STORY — WHY THIS MATTERS

### The Core Narrative

Every privacy promise has a test. Not a technical test — a moral one.

Amplified's entire architecture is built on a single promise: we CAN'T access your data. Not "we won't" — we CAN'T. Physical enforcement. No back doors. No exceptions.

Except one.

If someone threatens violence during a customer interaction — genuine, credible, "I'm going to hurt you" violence — the system does what any responsible person would do. It calls the police. Anonymously. No names. No identity. Just: "There was a threat of violence at this location, at this time. This is the nature of the threat."

That's it. That's the only exception. And it has to exist.

### The Moral Case

Here's the thought experiment that makes this clear:

Imagine the system detects a customer saying "I'm going to come back and hurt you" to a staff member. The system has heard it. The system has classified it with 95%+ confidence as a genuine threat. And the system... does nothing. Because privacy.

That's not a privacy-first system. That's a cowardly system. A system that hides behind its own architecture while someone is in danger.

Duty of care isn't optional. It's not something you weigh against other priorities. When someone's safety is genuinely threatened, you act. You just do it in a way that protects as much privacy as possible — which means anonymised reporting.

### Why ONLY Violence

This is where the discipline comes in. Because once you create one exception, the temptation is to create more. "What about fraud?" "What about mental health crises?" "What about someone saying something illegal?"

No. No. And no.

The exception is violence and threats of violence. Full stop. Nothing else. Because every additional exception erodes the privacy promise. And the privacy promise is what makes the entire system trustworthy.

> "Violence/threats immediately reported to police. Anonymised. This is the ONLY exception."

That word "only" is doing enormous work. It means the system won't report fraud. It won't diagnose mental health conditions. It won't be a surveillance tool for law enforcement. It detects threats to safety, and it acts. Nothing more.

### The Trust Architecture

Counter-intuitively, the violence exception actually STRENGTHENS trust. Here's why:

When you tell staff and customers "this system protects your privacy absolutely, with one exception — if someone threatens violence, we report it anonymously to police" — that sounds reasonable. That sounds like what a responsible person would do. That sounds like duty of care.

If you said "this system protects your privacy absolutely, with NO exceptions, even if someone threatens to kill you" — that sounds negligent. That sounds like you're hiding behind your architecture. That sounds like you care more about your product than about people.

The exception proves the system is built by humans who understand human reality. Not by technologists who worship their own privacy architecture.

---

## 2. CONTENT ANGLES

### Angle 1: "The Only Exception — Why a Privacy-First System Still Needs a Safety Valve"

**Hook:** What happens when an AI system built to protect privacy detects a genuine threat to someone's life? The answer reveals everything about the system's values.

**Key points:**
- Amplified's privacy architecture is physically enforced — CAN'T, not "please don't"
- One exception exists: genuine threats of violence, reported anonymously to police
- The exception is NARROW: only violence. Not rudeness, not complaints, not frustration
- Anonymised reporting means privacy is preserved even in the exception
- Duty of care is non-negotiable — doing nothing when someone is threatened is a moral failure
- The narrow exception strengthens trust — it shows the system is built by responsible humans

**Format:** Blog post, thought leadership, trust documentation

### Angle 2: "Duty of Care in the Age of AI — When Privacy Meets Safety"

**Hook:** For 30 years, workplace safety legislation has required employers to protect their people. What happens when an AI system can detect threats that humans might miss?

**Key points:**
- Health and Safety at Work Act 1974 creates a duty of care obligation
- AI systems that detect threats and do nothing may create a legal liability for the employer
- Amplified's approach: detect, anonymise, report — minimum necessary processing
- The human review gate prevents false positives from reaching police
- Conservative thresholds (95%+ confidence) protect innocent customers from false accusations
- The system is a supplementary safety layer, not a replacement for human judgment

**Format:** Legal/compliance brief, industry article, risk management content

### Angle 3: "False Positives Are Worse Than False Negatives — The Counter-Intuitive Safety Design"

**Hook:** In most safety systems, missing a real threat is the worst outcome. In Amplified's violence detection, a false alarm is worse. Here's why.

**Key points:**
- Most safety systems prioritise catching everything, accepting false alarms as the cost
- Amplified's system exists within a trust architecture — a false police report destroys that trust
- If the system calls police on a rude-but-not-threatening customer, the business loses faith in the entire platform
- A genuine threat that's missed will likely recur — the system gets another chance
- Trust, once lost, doesn't come back — so thresholds are deliberately conservative
- 95%+ confidence required before any action. Human review before police notification.
- This is the asymmetric cost model: false positive cost >> false negative cost

**Format:** Technical blog, product differentiation, design philosophy piece

### Angle 4: "What We Won't Report — The Discipline of the Narrow Exception"

**Hook:** The strength of Amplified's violence exception isn't what it covers — it's everything it deliberately excludes.

**Key points:**
- Customer is rude? Not an exception. Standard customer service.
- Customer mentions fraud? Not an exception. The system isn't law enforcement.
- Customer seems distressed? Not an exception. The system doesn't diagnose.
- Staff member sounds stressed on personal phone? Not an exception. Personal device data is inviolate.
- Business owner wants individual data for a disciplinary case? Not an exception. The system CAN'T provide it.
- Only actual threats of violence or physical harm trigger the exception
- This discipline is what makes the privacy promise credible

**Format:** FAQ-style content, trust documentation, sales enablement

---

## 3. KEY STATISTICS AND EVIDENCE

```json
{
  "statistics": [
    {
      "stat": "The system requires 95%+ confidence before taking any action on a detected threat",
      "context": "Conservative threshold designed to prevent false positives that destroy trust",
      "source": "System design specification"
    },
    {
      "stat": "Human review gate adds a 15-minute maximum window before any police notification",
      "context": "Safety officer reviews anonymised data to confirm or dismiss the detection",
      "source": "System operational procedure"
    },
    {
      "stat": "Imminent violence auto-escalation requires BOTH 98%+ NLP confidence AND acoustic corroboration",
      "context": "The only scenario that bypasses human review — active violence in progress",
      "source": "System design specification"
    },
    {
      "stat": "Health and Safety at Work Act 1974 — employers must ensure health, safety and welfare of employees",
      "context": "Legal foundation for duty of care obligation that the violence exception fulfils",
      "source_url": "https://www.legislation.gov.uk/ukpga/1974/37/contents"
    },
    {
      "stat": "UK GDPR Article 6(1)(d) permits processing necessary to protect vital interests",
      "context": "Data protection lawful basis for processing during genuine safety threats",
      "source_url": "https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/a-guide-to-lawful-basis/lawful-basis-for-processing/vital-interests/"
    }
  ]
}
```

---

## 4. COMPETITIVE POSITIONING

No competitor in the customer voice or employee listening space has a comparable architecture:

| Feature | Amplified | Competitors |
|---------|-----------|-------------|
| Privacy-first with defined safety exception | Yes — single, narrow, anonymised exception | Most have broad data access, no need for exceptions |
| Anonymised threat reporting | Yes — no identity in any report | N/A — most capture identity by design |
| Conservative detection thresholds (95%+) | Yes — trust protection prioritised | Varies — most optimise for catch-all |
| Human review before escalation | Yes — safety officer gate | Varies — some auto-report |
| Transparent exception disclosure | Yes — disclosed at onboarding, daily, in docs | Varies — many buried in ToS |
| Physical enforcement of privacy beyond exception | Yes — CAN'T access, not "won't" | Rare — most rely on policy |

The violence exception demonstrates that Amplified's privacy architecture is thoughtful, not dogmatic. It accounts for real-world human safety needs while maintaining the strongest possible privacy protections.

---

## 5. EWAN'S QUOTES

```json
{
  "quotes": [
    {
      "quote": "Violence/threats immediately reported to police. Anonymised. This is the ONLY exception.",
      "context": "Defining the single exception to the privacy architecture",
      "use_for": "Core definition of P9, trust documentation"
    },
    {
      "quote": "If we get it wrong, we turn it off. We only want to help.",
      "context": "The broader system philosophy that contextualises the violence exception — the system exists to help, and it has the kill switch if it causes harm",
      "use_for": "Contextualising P9 within the broader trust architecture"
    },
    {
      "quote": "Physical enforcement, not instructions — CAN'T, not please don't.",
      "context": "The enforcement philosophy that applies to P9's anonymisation — the system CAN'T include identity in reports because the fields don't exist",
      "use_for": "Explaining why the anonymisation is trustworthy"
    },
    {
      "quote": "Support, not surveillance. Information, not accusation.",
      "context": "Even the violence exception follows this principle — the report is information for police to act on, not an accusation against an identified individual",
      "use_for": "Demonstrating philosophical consistency"
    }
  ]
}
```

---

## 6. VISUAL CONTENT SUGGESTIONS

### Infographic: "The Narrow Exception"
A visual showing the full scope of what the system monitors (customer sentiment, aggregate intelligence, team wellbeing) as a large area, with a tiny, clearly marked section labelled "Violence Exception" — visually demonstrating how narrow the exception is relative to the system's full scope.

### Flowchart: "From Detection to Report"
Detection → Pre-filter → Deep Classification (95%+ required) → Human Review → Anonymised Report → Police Notification. Show each stage as a gate that data must pass through, with "most detections filtered out here" annotations at each stage.

### Comparison: "What IS and ISN'T a Threat"
Two columns: Left shows in-scope triggers (explicit threats, weapon references, violent intent). Right shows out-of-scope (rudeness, complaints, frustration, idioms, sarcasm). Clear visual separation.

### Trust Diagram: "Why the Exception Strengthens the Promise"
A shield or lock icon with the text "Privacy Protected" — with a small, clearly marked emergency exit labelled "Violence Exception — Anonymised". The message: the emergency exit doesn't weaken the building. It makes it safer to be inside.

---

## 7. CONTENT CREATOR NOTES

### Tone Guidance
- This is a sensitive topic. Content should be measured, not dramatic.
- Avoid sensationalising violence or threat scenarios.
- Focus on the SYSTEM DESIGN and TRUST ARCHITECTURE, not on graphic descriptions of threats.
- Emphasise the conservative nature of the detection — the system is cautious, not aggressive.
- Frame the exception as responsible design, not as a surveillance capability.
- Never suggest the system is a replacement for human safety protocols — it's supplementary.

### What to Avoid
- Do not describe specific threat scenarios in marketing content.
- Do not suggest the system "catches criminals" — it reports anonymised threats to police.
- Do not frame this as a competitive feature — it's a responsibility, not a selling point.
- Do not minimise the privacy commitment by overemphasising the exception.
- Do not suggest the exception could or should be expanded.

### Key Message
The violence exception exists because Amplified is built by responsible people who understand that duty of care is non-negotiable. It's narrow, anonymised, and transparent. It's the exception that proves the rule — the privacy architecture is so strong that only the most extreme circumstance can override it, and even then, identity is protected.
