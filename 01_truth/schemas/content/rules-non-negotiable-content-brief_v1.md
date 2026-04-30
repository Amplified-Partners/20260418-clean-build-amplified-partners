---
title: "Rules Non-Negotiable Content Brief"
id: "rules-non-negotiable-content-brief"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "Rules-non-negotiable-content-brief.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Rules: Non-Negotiable Rules — The Rule Book
# Content Brief — For Content Creators
# Amplified Partners

## DOCUMENT METADATA
```json
{
  "document_id": "Rules-content",
  "title": "Non-Negotiable Rules — Content Brief",
  "version": "1.0.0",
  "date": "2026-03-16",
  "author": "Perplexity Computer",
  "for": "Content creators (human or AI) writing about Amplified's non-negotiable rules and physical enforcement architecture",
  "tone": "Human, warm, Ewan's voice where possible. The story, not the spec.",
  "parent": "Rules-non-negotiable-master-reference.md"
}
```

---

## 1. THE STORY — WHY THIS MATTERS

### The Core Narrative

Every tech company has rules. Privacy policies. Terms of service. Data handling guidelines. Employee handbooks full of best practices.

And every tech company has the same problem: rules get broken.

Not maliciously. Not usually. They get broken because someone was in a hurry. Because a new developer didn't read the documentation. Because deadline pressure made the "quick fix" more attractive than the right fix. Because at 3am on a Sunday, nobody's checking whether the policy is being followed.

Amplified doesn't have rules. Amplified has walls.

> "Physical enforcement, not instructions — CAN'T, not please don't."

That's not a slogan. It's the single most important design principle in the entire system. Every one of Amplified's ten non-negotiable rules is enforced not by asking people to follow them, but by making it physically impossible to break them.

You can't store a staff member's name in the database — because the database has no field for it. You can't see individual performance data — because individual data is aggregated before it reaches the database. You can't access the training system from a work computer — because the system blocks corporate IP addresses.

Not "please don't." CAN'T.

### Why Physical Enforcement Beats Policy

Consider two approaches to the same rule: "Don't store individual staff identifiers."

**The policy approach:** Write it in the handbook. Train developers. Add it to code review checklists. Hope everyone remembers. Hope no one adds a "temporary" staff_id column "just for debugging." Hope that column doesn't persist for six months until someone accidentally queries it in a dashboard.

**The physical approach:** The database schema has no column for staff identifiers. A developer tries to add one. The schema migration is rejected by an automated validator. The column never exists. No query can extract what was never stored.

The policy approach requires everyone to remember, every time, forever. The physical approach requires no one to remember anything. The system itself embodies the rule.

> "I do not like quick fixers. I like complete, robust, long-term fixes."

Physical enforcement is the ultimate long-term fix. It works on day one and day one thousand. It works when the original team has moved on. It works when no one is watching.

### The Trust Architecture of Rules

Here's what most people miss about Amplified's rules: they don't restrict the system. They enable it.

Without R1 (data belongs to the client), no business owner would trust you with their customers' voices. Without R3 (no staff voice captured), no employee would accept a microphone in their workplace. Without R6 (aggregate only), every team meeting becomes a performance review. Without R8 (kill switch), the whole system feels irreversible and frightening.

The rules aren't constraints on an otherwise powerful system. The rules ARE what makes the system possible. Remove the rules and you don't get a more capable product — you get a product nobody will use.

Every rule answers one question: "What would make someone say 'no' to this system?" And then it makes that concern physically impossible.

---

## 2. CONTENT ANGLES

### Angle 1: "CAN'T, Not Please Don't — Why Amplified Has Walls Instead of Rules"

**Hook:** Most privacy policies are promises. Amplified's are architecture.

**Key points:**
- 10 non-negotiable rules, each enforced by making violation physically impossible
- No staff name field in the database — not because there's a rule against it, but because the field doesn't exist
- The distinction between "we won't" and "we can't" is the entire trust proposition
- Physical enforcement works at 3am, under deadline pressure, with a new team
- "Instructions get forgotten. Policies get ignored. Physical enforcement endures."
- Five enforcement layers: database schema, network architecture, processing pipeline, API validation, system architecture

**Format:** Thought leadership article, keynote talking point, trust architecture explainer

### Angle 2: "The Ten Rules That Make Everything Possible"

**Hook:** Amplified's non-negotiable rules aren't limitations — they're the reason the product exists.

**Key points:**
- R1: Data belongs to the client → Businesses say yes because they own everything
- R3: No staff voice captured → Staff say yes because they're not being monitored
- R5: Four-word identifier → Identity is impossible to resolve, even if you wanted to
- R6: Aggregate only → Individual data doesn't exist in the database to query
- R8: Kill switch → The ultimate "we trust you more than you trust us"
- R10: Support, not judgment → The system can only produce supportive output
- Each rule removes a specific objection. Together, they remove every objection.

**Format:** Product positioning piece, sales enablement, conference talk

### Angle 3: "The Rule That Enforces All Other Rules"

**Hook:** Rule R8 — the kill switch — is unique. It's both a rule and an enforcement mechanism. It's the rule that says: if any other rule fails, everything stops.

**Key points:**
- R8 is the meta-rule: it enforces R1-R7 and R9-R10
- If data somehow leaves client infrastructure (violating R1) → kill switch
- If staff voice is somehow captured (violating R3) → kill switch
- If individual data appears in a dashboard (violating R6) → kill switch
- Physical enforcement at every level, with the kill switch as the final backstop
- "We built ten walls. And behind all ten, we built an off switch."

**Format:** Trust architecture deep-dive, CTO-audience technical blog, security white paper

### Angle 4: "How Each Rule Enables Rather Than Restricts"

**Hook:** The ten non-negotiable rules sound like constraints. But each one is actually an enabler — removing a specific fear that would otherwise block adoption.

**Key points:**
- R1 (client owns data) → Enables: business owner confidence, regulatory compliance
- R2 (no raw audio) → Enables: legal simplicity, no discovery risk
- R3 (no staff voice) → Enables: staff acceptance, union support, RIPA simplicity
- R4 (personal phone only) → Enables: staff autonomy, employer can't monitor training
- R5 (four-word identifier) → Enables: complete anonymity, genuine self-determination
- R6 (aggregate only) → Enables: team support without individual blame
- R7 (violence → police) → Enables: duty of care, staff physical safety
- R8 (kill switch) → Enables: trust through reversibility, CEO confidence
- R9 (customer-centric) → Enables: honest framing, staff trust
- R10 (support, not judgment) → Enables: system feels helpful, not threatening

**Format:** Feature matrix, product one-pager, investor deck slide

### Angle 5: "Five Layers Deep — The Enforcement Architecture"

**Hook:** Amplified doesn't enforce its rules in one place. It enforces them in five separate layers — so even if one layer fails, the others catch it.

**Key points:**
- Layer 1 — Database schema: CHECK constraints, FORBIDDEN_COLUMNS, no identity fields
- Layer 2 — Network architecture: IP blocking, device fingerprinting, data residency
- Layer 3 — Processing pipeline: aggregation before storage, buffer overwrite, speaker diarisation
- Layer 4 — API and output validation: template system, blocked terms, output filters
- Layer 5 — System architecture: independent kill switch, automated violence detection
- Defence in depth: any single layer failure is caught by the others
- "The system doesn't rely on any one wall. It relies on all five."

**Format:** Technical architecture blog, security audit overview, compliance documentation

---

## 3. KEY STATISTICS AND CITATIONS

```json
{
  "statistics": [
    {
      "stat": "10 non-negotiable rules, each with physical enforcement",
      "context": "Every rule is enforced by making violation architecturally impossible, not by policy or instruction",
      "source": "Amplified system architecture (Doc 07 Section 6.1)"
    },
    {
      "stat": "5 independent enforcement layers",
      "context": "Database schema, network architecture, processing pipeline, API validation, system architecture — defence in depth",
      "source": "Amplified enforcement architecture"
    },
    {
      "stat": "13+ FORBIDDEN_COLUMNS blocked from all database tables",
      "context": "staff_id, staff_name, employee_id, email, phone_number, and 8+ other identity-linked fields are permanently excluded from the schema",
      "source": "Amplified database schema specification (Rule R5)"
    },
    {
      "stat": "625 billion possible four-word identifiers",
      "context": "5,000-word dictionary, four words = 5000^4 combinations. Collision probability negligible. Unlinkable to real identity.",
      "source": "Amplified identity architecture (Rule R5)"
    },
    {
      "stat": "Zero individual-level data in persistent storage",
      "context": "Individual interaction data exists only in volatile memory during processing. Aggregated before database write. No query can extract what was never stored.",
      "source": "Amplified data architecture (Rule R6)"
    }
  ]
}
```

---

## 4. EWAN'S VOICE — KEY QUOTES

> "Physical enforcement, not instructions — CAN'T, not please don't."

This is the quote. If you remember nothing else about Amplified's approach, remember this. It's not a marketing line — it's the actual design philosophy that shapes every database schema, every API endpoint, every network configuration. The word "physical" matters: not policy enforcement, not contractual enforcement, not procedural enforcement. Physical. Architectural. The system is built so that rules cannot be violated, the same way a wall prevents you from walking through it.

> "I do not like quick fixers. I like complete, robust, long-term fixes."

Physical enforcement IS the long-term fix. A policy is a quick fix — it works until someone forgets it. A database constraint is a long-term fix — it works until someone redesigns the database, and even then the validator catches it. Ewan's impatience with "quick fixers" directly produced the most durable enforcement architecture in the industry.

> "Support, not surveillance. Information, not accusation."

Rules R9 and R10 in two sentences. The same customer sentiment data, framed one way, creates a support system. Framed another way, it creates a surveillance system. The framing isn't aesthetic — it's constitutional. The rules make it physically impossible for the system to produce surveillance-style output.

> "If we get it wrong, we turn it off. We only want to help."

Rule R8 — the meta-rule. The confidence to say "turn it off" comes from knowing the other nine rules are physically enforced. And the humility to say "we only want to help" comes from knowing that's genuinely the intent. R8 is what happens when someone truly believes in their rules: they're willing to stake the entire system on them.

> "We don't take anything of your voice off your phone. This is all about customers."

Rules R3 and R9 together. Not a cover story — a truthful description of the architecture. Staff voice is never captured from work devices (R3). Everything is framed around customers because that's what the system actually measures (R9). When the honest description IS the reassuring description, you've designed the system right.

---

## 5. THE RULE HIERARCHY — HOW RULES RELATE

```json
{
  "hierarchy": {
    "foundation": {
      "rule": "R1 — Data belongs to CLIENT",
      "why_foundational": "All other rules operate on data the client owns. Data ownership makes every other rule enforceable by the data owner."
    },
    "meta_rule": {
      "rule": "R8 — Kill switch",
      "why_meta": "If any rule from R1-R7 or R9-R10 is violated despite physical enforcement, R8 shuts everything down. It enforces all other rules."
    },
    "exception": {
      "rule": "R7 is the ONLY exception to R2",
      "why": "Violence detection may briefly retain audio for emergency services. Physical safety overrides data rules. This is the only case."
    },
    "pairs": [
      {
        "rules": "R3 + R4",
        "together": "Complete staff privacy boundary — no voice at work, training only on personal device"
      },
      {
        "rules": "R5 + R6",
        "together": "Complete identity protection — no identifier linkage, no individual-level data"
      },
      {
        "rules": "R9 + R10",
        "together": "Complete output safety — customer-centric framing, supportive language only"
      }
    ]
  }
}
```

---

## 6. COMPETITIVE POSITIONING

```json
{
  "competitive_comparison": [
    {
      "competitor_approach": "Privacy policy + terms of service",
      "companies": "Most SaaS platforms, enterprise software",
      "weakness": "Policies are promises. Promises can be broken — deliberately or accidentally.",
      "amplified_difference": "Physical enforcement. Rules are architecture, not promises."
    },
    {
      "competitor_approach": "Role-based access controls (RBAC)",
      "companies": "Enterprise platforms (Salesforce, SAP, Oracle)",
      "weakness": "Admin can always override. Data still exists — access is just gated.",
      "amplified_difference": "Data that shouldn't exist doesn't exist. No admin override possible because there's nothing to access."
    },
    {
      "competitor_approach": "Anonymisation layer over identifiable data",
      "companies": "Analytics platforms (Qualtrics, Medallia)",
      "weakness": "Raw identifiable data exists somewhere. Re-identification attacks are possible.",
      "amplified_difference": "Individual data is aggregated BEFORE storage. There is no identifiable layer to de-anonymise."
    },
    {
      "competitor_approach": "Client-configurable privacy settings",
      "companies": "Employee engagement platforms (Peakon, Culture Amp)",
      "weakness": "Settings can be changed. Defaults can be overridden. Configuration drift over time.",
      "amplified_difference": "Non-negotiable. No configuration. No override. The rules are the architecture."
    }
  ]
}
```

---

## 7. VISUAL CONTENT SUGGESTIONS

### Infographic: "Ten Walls, Not Ten Rules"
Visual of ten walls, each labelled with a rule (R1-R10). Behind all ten walls, the kill switch (R8) as a final barrier. Inside the walls: the system operates freely. Outside: the things that cannot happen. Emphasis on permanence — walls, not fences.

### Diagram: "Policy vs. Physical Enforcement"
Two-panel comparison. LEFT: Policy approach — handbook → training → checklist → hope → violation → incident response → policy update → repeat. RIGHT: Physical approach — design → build → done. The system embodies the rule. No cycle. No repeat. Visual weight should emphasise the simplicity of physical enforcement versus the fragility of policy.

### Matrix: "How Each Rule Enables Adoption"
10-row table. Column 1: Rule. Column 2: What it prevents. Column 3: What it enables. Column 4: Who it serves (business owner, staff, customers, regulators). Shows that every rule is an enabler, not a constraint.

### Architecture Diagram: "Five Layers Deep"
Concentric rings showing five enforcement layers. Innermost: database schema. Then: processing pipeline. Then: network architecture. Then: API validation. Outermost: system architecture (kill switch). Shows defence in depth — any single layer failure is caught by others.

---

## 8. CONTENT DO'S AND DON'TS

### DO:
- Frame rules as enablers, not restrictions — "these rules make the product possible"
- Use the "CAN'T, not please don't" framing — it's the clearest way to communicate the approach
- Emphasise that physical enforcement works without human oversight — it works at 3am on a Sunday
- Draw the distinction between "we won't" (promise) and "we can't" (architecture)
- Use Ewan's voice — direct, human, no corporate language
- Highlight rule pairs (R3+R4, R5+R6, R9+R10) to show how rules reinforce each other
- Mention R8 (kill switch) as the ultimate backstop — the rule that enforces all other rules
- Compare to physical engineering: fire doors, circuit breakers, railway dead man's switches

### DON'T:
- List the rules as if they're terms of service — they're architecture, not policy
- Suggest that rules exist because the system is dangerous — they exist because they make the system trustworthy
- Over-emphasise what the system CAN'T do — focus on what the rules ENABLE
- Use compliance language ("in accordance with," "pursuant to") — use human language
- Present rules as burdensome or limiting to the development team — they simplify, not complicate
- Suggest that rules could be relaxed for enterprise clients — non-negotiable means non-negotiable
- Frame R7 (violence exception) as a loophole — it's a duty of care obligation, the only valid exception to R2
