---
title: "ISO 9001-Style Quality Frameworks for AI System Building"
id: "research-iso9001-ai-frameworks-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# ISO 9001-Style Quality Frameworks for AI System Building
## Research Report for Amplified Partners — AI Operating System for SMBs

**Prepared for:** Ewan Bramley, Amplified Partners (Newcastle, UK)  
**Date:** March 2026  
**Context:** Building an AI-powered operating system for SMBs, with a vault of 4,787 documents (3.3M words) being extracted and organised. The goal is to create an ISO 9001-style skeleton framework covering BOTH the AI build process and coding standards.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [The Standards Landscape](#2-the-standards-landscape)
3. [ISO/IEC 90003 — ISO 9001 for Software](#3-isoiec-90003--iso-9001-for-software)
4. [ISO/IEC 42001 — The AI Management System Standard](#4-isoiec-42001--the-ai-management-system-standard)
5. [ISO/IEC 25010 — Software Quality Model](#5-isoiec-25010--software-quality-model)
6. [NIST AI Risk Management Framework](#6-nist-ai-risk-management-framework)
7. [CMMI — Process Maturity for Software](#7-cmmi--process-maturity-for-software)
8. [MLOps Quality Frameworks](#8-mlops-quality-frameworks)
9. [Open-Source and Lightweight Alternatives](#9-open-source-and-lightweight-alternatives)
10. [Agentic AI Standards (Emerging)](#10-agentic-ai-standards-emerging)
11. [One Document or Two? The Key Strategic Decision](#11-one-document-or-two-the-key-strategic-decision)
12. [Recommended Skeleton Framework](#12-recommended-skeleton-framework)
13. [Framework as a Product](#13-framework-as-a-product)
14. [Practical Recommendations for Amplified Partners](#14-practical-recommendations-for-amplified-partners)

---

## 1. Executive Summary

**The bottom line:** There is no single existing framework that perfectly covers both the AI *build process* and *coding standards* in one document designed for a small AI consultancy. However, the ingredients for a compelling, dual-purpose framework already exist and can be synthesised from several sources.

### Key findings:

| Question | Answer |
|---|---|
| Does ISO 9001 adapt to software? | Yes — via ISO/IEC 90003 (guidance) and ISO/IEC 12207 (lifecycle) |
| Does ISO 9001 adapt to AI? | Yes — ISO/IEC 42001 (2023) is the direct answer; it's certifiable |
| Should it be one document or two? | **Two documents, one governance wrapper** (see Section 11) |
| Best open-source alternative? | GSTT-CSC QMS Template (GitHub) for structure; NIST AI RMF for AI governance |
| Can it become a product? | Yes — high product potential; market is underserved at SMB level |

### The strategic insight:

ISO/IEC 42001 (published December 2023) is the world's first certifiable AI management system standard. It uses the exact same high-level structure (Annex SL) as ISO 9001, meaning both can be integrated into a single Quality Management System. This creates a path for Amplified Partners to:

1. Build a framework that is *demonstrably aligned* with both ISO 9001 and ISO 42001
2. Avoid the cost of full certification while still being audit-ready
3. Package and sell that framework to other small AI consultancies

---

## 2. The Standards Landscape

The following map shows how the major standards relate to each other and to Amplified Partners' specific need.

```
┌─────────────────────────────────────────────────────────────┐
│                    ISO 9001:2015                             │
│           (Core Quality Management System)                  │
│           PDCA · Process Approach · Risk Thinking           │
└───────────────┬───────────────────────┬─────────────────────┘
                │                       │
    ┌───────────▼──────────┐ ┌─────────▼──────────────────┐
    │  ISO/IEC 90003:2014  │ │   ISO/IEC 42001:2023        │
    │  (ISO 9001 applied   │ │   (AI Management System)    │
    │   to software)       │ │   First certifiable AI std  │
    └──────────┬───────────┘ └─────────┬──────────────────┘
               │                       │
    ┌──────────▼───────────┐ ┌─────────▼──────────────────┐
    │  ISO/IEC 25010:2023  │ │   NIST AI RMF (2023)        │
    │  (Software Product   │ │   (Govern·Map·Measure       │
    │   Quality Model)     │ │    Manage)                  │
    └──────────────────────┘ └─────────┬──────────────────┘
                                       │
                             ┌─────────▼──────────────────┐
                             │  NIST AI Agent Standards    │
                             │  Initiative (Feb 2026)      │
                             │  (Emerging: identity,       │
                             │   interop, security)        │
                             └────────────────────────────┘
```

**Also relevant:**
- **CMMI (Capability Maturity Model Integration)** — process maturity in 5 levels, widely used in software/engineering
- **MLOps (Google/Clarifai)** — 3-level operational maturity for ML pipelines
- **ISO/IEC 12207** — Software life cycle processes (referenced by ISO/IEC 90003)

---

## 3. ISO/IEC 90003 — ISO 9001 for Software

**What it is:** A guidance document (not itself certifiable) that maps ISO 9001:2015 requirements onto software development, operation, and maintenance. Published as ISO/IEC 90003:2014 (still current). [(ISO standard page)](https://www.iso.org/standard/66240.html)

**What it adds to ISO 9001:**
- Maps the Plan-Do-Check-Act (PDCA) cycle onto the Software Development Life Cycle (SDLC)
- Explicitly covers acquisition, supply, development, operation, and maintenance of software
- References ISO/IEC 12207 (software lifecycle) for additional process guidance
- Addresses traceability, version control, configuration management, and validation — software-specific concerns absent from base ISO 9001

**Practical implications for Amplified Partners:**

| ISO 9001 Clause | ISO/IEC 90003 Software Translation |
|---|---|
| 7.5 Documented Information | Code documentation, config files, requirements traceability |
| 8.3 Design & Development | SDLC stages: planning → design → coding → testing → deployment |
| 8.5 Production & Service Provision | CI/CD pipelines, release management |
| 8.6 Release of Products | Software release gates, acceptance criteria |
| 9.1 Monitoring & Measurement | Test coverage, code quality metrics, defect rates |
| 10.2 Corrective Action | Bug tracking, root cause analysis, patch management |

**Key limitation:** ISO/IEC 90003:2014 predates modern AI/ML systems and does not address model training, data provenance, or algorithmic bias. It is best used as the *coding standards backbone*, not the AI build process backbone.

**Source:** [Walturn guide to ISO 9001 and 90003](https://www.walturn.com/insights/understanding-iso-9001-and-90003-for-software-quality-management)

---

## 4. ISO/IEC 42001 — The AI Management System Standard

**What it is:** Published December 2023, this is the world's first international standard for Artificial Intelligence Management Systems (AIMS). It is certifiable, follows the same Annex SL high-level structure as ISO 9001, and is explicitly designed to integrate with it. [(ISO standard page)](https://www.iso.org/standard/42001)

**Why it matters for Amplified Partners:** It was built precisely for organisations that "provide or utilise AI-based products or services." An AI operating system for SMBs falls squarely in scope.

### Full Clause Structure

| Clause | Title | Key Requirements |
|---|---|---|
| 4 | Context | Understand organisation, interested parties, determine AIMS scope |
| 5 | Leadership | AI policy, named roles/responsibilities, governance commitment |
| 6 | Planning | Risk assessment, impact assessment, objectives and planning for changes |
| 7 | Support | Resources, competence, communication, documented information |
| 8 | Operation | Operational risk assessment and treatment, impact assessment |
| 9 | Performance Evaluation | Monitoring, internal audit, management review |
| 10 | Improvement | Nonconformity, corrective action, continual improvement |

### Full Annex A Controls (the "what to implement" list)

| Control | Name | Key Sub-Controls |
|---|---|---|
| A.2 | Policies Related to AI | AI policy, alignment with other policies, review cycle |
| A.3 | Internal Organisation | AI roles/responsibilities, reporting mechanisms |
| A.4 | Resources for AI Systems | Data resources, tooling, computing, human expertise |
| A.5 | Assessing Impacts of AI | Impact assessment process, individual/societal impacts |
| A.6 | AI System Life Cycle | Development objectives, requirements, design docs, V&V, deployment, monitoring, technical documentation, event logs |
| A.7 | Data for AI Systems | Data quality, acquisition, provenance, preparation |
| A.8 | Information for Interested Parties | User documentation, external reporting, incident comms |
| A.9 | Use of AI Systems | Responsible use processes, intended use definition, human oversight |
| A.10 | Third-Party & Customer Relationships | Responsibility allocation, supplier standards, customer needs |

**Specific relevance to the Amplified Partners build:**

| Your Build Activity | Applicable ISO 42001 Control |
|---|---|
| Document extraction (4,787 docs) | A.7.3 Acquisition of data, A.7.4 Quality of data, A.7.5 Data provenance |
| Document labelling | A.7.6 Data preparation, A.6.2.3 Documentation of design |
| Content routing / classification | A.6.2.2 Requirements & specification, A.9.4 Intended use |
| Agent configuration | A.6.2.5 AI system deployment, A.4.4 Tooling resources |
| Model monitoring | A.6.2.6 Operation and monitoring, A.6.2.8 Event logs |
| SMB client delivery | A.10 Third-party and customer relationships |

**Key differentiator from ISO 9001:** ISO 42001 introduces requirements that don't exist in basic quality management: [(ISMS.online comparison)](https://www.isms.online/iso-42001/vs-iso-9001/)
- Named human stewards for every AI accountability domain
- Ongoing bias checks (mandatory, cyclic)
- Data provenance chain-of-custody
- Live explainability records for audit
- Stakeholder engagement proof for regulatory and societal concerns

**Sources:** [KPMG guide to ISO 42001](https://kpmg.com/ch/en/insights/artificial-intelligence/iso-iec-42001.html), [EY guide](https://www.ey.com/en_us/insights/ai/iso-42001-paving-the-way-for-ethical-ai), [Iterasec implementation guide](https://iterasec.com/blog/iso-iec-42001-implementation-guide/)

---

## 5. ISO/IEC 25010 — Software Quality Model

**What it is:** The international standard for software and systems quality characteristics. Updated November 2023 (version 2023), it defines nine quality characteristics that should be designed and tested for — not a process standard, but a *product quality vocabulary*. [(ISO page)](https://www.iso.org/obp/ui/en/) [(arc42 update guide)](https://quality.arc42.org/articles/iso-25010-update-2023)

**The nine quality characteristics (2023 update):**

| Characteristic | Sub-characteristics | Relevance to AI OS |
|---|---|---|
| Functional suitability | Completeness, correctness, appropriateness | Does the AI do what it claims? |
| Performance efficiency | Time behaviour, resource utilisation, capacity | Agent response times, token costs |
| Compatibility | Coexistence, interoperability | Integration with SMB tools |
| Interaction capability (formerly Usability) | Learnability, operability, inclusivity, self-descriptiveness | SMB operator UX |
| Reliability | Maturity, availability, fault tolerance, faultlessness (new) | Uptime guarantees, graceful degradation |
| Security | Confidentiality, integrity, non-repudiation, accountability, authenticity, resistance (new) | Client data protection |
| Maintainability | Modularity, reusability, analysability, modifiability, testability | Ability to update agents/models |
| Flexibility (formerly Portability) | Adaptability, scalability (new), installability, replaceability | Scaling from one to many SMB clients |
| Safety (new in 2023) | Operational constraint satisfaction, risk identification, safe failure, hazard warning | AI action safety for autonomous agents |

**Key new additions in 2023:** Safety (critical for agentic systems), scalability, resistance, faultlessness. These additions make the 2023 version significantly more relevant to AI systems than the 2011 version.

**How to use this:** ISO/IEC 25010 provides the *acceptance criteria vocabulary* for coding standards. Every quality gate and test specification in the coding standards framework should map to one or more of these nine characteristics.

**Example mappings for AI OS:**
- Unit test coverage → Reliability (faultlessness)
- Latency benchmarks → Performance efficiency
- Role-based access control → Security (accountability)
- Model output logging → Maintainability (analysability) + Safety
- Modular agent design → Maintainability (modularity) + Flexibility

**Source:** [Pacific Certifications ISO 25010 guide](https://blog.pacificcert.com/iso-25010-software-product-quality-model/)

---

## 6. NIST AI Risk Management Framework

**What it is:** Published January 2023 by the US National Institute of Standards and Technology. Voluntary, non-certifiable, but becoming de facto standard for responsible AI in the US. Structured around four core functions. Updated in 2025 with a Generative AI Profile. [(NIST AI RMF page)](https://www.nist.gov/itl/ai-risk-management-framework)

**The four functions:**

```
┌─────────────────────────────────────────────────────────┐
│                     GOVERN                              │
│   Culture, roles, policies, processes, accountability   │
│   (Foundation — runs across all other functions)        │
└───────────────────────────────────────────────────────── ┘
          ▼                    ▼                    ▼
      ┌───────┐          ┌─────────┐          ┌────────┐
      │  MAP  │          │ MEASURE │          │ MANAGE │
      │Context│          │ Assess  │          │Mitigate│
      │Stakes │          │ Monitor │          │Improve │
      │holder │          │ Measure │          │        │
      └───────┘          └─────────┘          └────────┘
```

**Govern function (19 sub-categories):** Establishes AI risk culture, cross-functional roles, policies, third-party oversight, and continuous improvement cycles.

**Map function:** Categorise AI systems, document capabilities/limitations, identify stakeholders, document benefits and risks.

**Measure function:** Quantitative and qualitative assessment of risks, trustworthiness characteristics, performance metrics.

**Manage function:** Prioritise and act on risks through mitigation, transfer, avoidance, or acceptance. Incident response planning.

**2025 updates relevant to Amplified Partners:** [(I.S. Partners analysis)](https://www.ispartnersllc.com/blog/nist-ai-rmf-2025-updates-what-you-need-to-know-about-the-latest-framework-changes/)
- Generative AI Profile: guidance specifically for LLM/GenAI hallucinations, data leakage, synthetic content
- New threat categories: poisoning attacks, evasion attacks, data extraction, model manipulation
- AI Bill of Materials (AI-BOM): inventory of models, data, and vendors
- Model provenance and third-party model assessment
- Alignment with Cybersecurity Framework (CSF) for unified governance

**NIST AI RMF vs ISO 42001 at a glance:**

| | NIST AI RMF | ISO 42001 |
|---|---|---|
| Type | Voluntary guidance | Certifiable standard |
| Certification | No | Yes |
| Geographic focus | US-centric | International |
| Flexibility | High (profile-based) | Lower (requirements-based) |
| Best for | Risk-first thinking, US contracts | Formal governance, EU/global |
| Cost | Free | ~£1,200 for standard + audit costs |

**Recommendation:** Use NIST AI RMF as the *risk thinking methodology* inside the framework, and ISO 42001's clause structure as the *organising skeleton*.

**Source:** [StandardFusion comparison](https://www.standardfusion.com/blog/key-differences-between-iso-42001-and-nist-ai-rmf)

---

## 7. CMMI — Process Maturity for Software

**What it is:** Capability Maturity Model Integration — a process improvement framework originally developed for US defence software. Five maturity levels from "Initial/chaotic" (Level 1) to "Optimising" (Level 5). Widely used in software and engineering. [(PopularCert comparison)](https://popularcert.com/iso-9001-vs-cmmi-difference-quality-management-certification/)

**The five maturity levels:**

| Level | Name | Description | Typical cost to achieve |
|---|---|---|---|
| 1 | Initial | Ad hoc, unpredictable | Starting point |
| 2 | Managed | Basic project management in place | 6-12 months |
| 3 | Defined | Standardised processes across org | 18-24 months |
| 4 | Quantitatively Managed | Data-driven decisions | 24-36 months |
| 5 | Optimising | Continuous process optimisation | 36+ months |

**CMMI vs ISO 9001 for Amplified Partners:**

| Dimension | CMMI | ISO 9001 |
|---|---|---|
| Certification | SCAMPI appraisal (level rating) | Third-party certification |
| Time to implement | 18-36 months | 6-18 months |
| Cost | Often >£400K for full appraisal | £50K-£200K typical |
| Prescriptiveness | High (22 process areas) | Lower (principle-based) |
| SMB suitability | Low — designed for large contractors | Medium — flexible |

**Verdict:** CMMI is too heavyweight and too expensive for a small AI consultancy. However, **CMMI's maturity level concept** is very useful as a growth framework. The Amplified Partners framework could adopt a "maturity ladder" inspired by CMMI (e.g., Level 1 = basic; Level 3 = defined processes) without incurring CMMI appraisal costs.

---

## 8. MLOps Quality Frameworks

**What it is:** The operational practice of applying DevOps principles (CI/CD, automation, monitoring) to machine learning pipelines. Google's MLOps guide defines three maturity levels that map closely to what Amplified Partners needs for its AI build process. [(Google MLOps guide)](https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning)

**The three MLOps levels:**

| Level | Name | Key Characteristics | Quality Gates |
|---|---|---|---|
| **Level 0** | Manual Process | Notebooks, hand-off between data science and engineering | None — human review only |
| **Level 1** | ML Pipeline Automation | Orchestrated training, CT (continuous training), data/model validation | Data schema validation, model comparison vs baseline, drift detection |
| **Level 2** | CI/CD Pipeline Automation | Full source control, automated build/test/deploy for pipelines | Unit tests, integration tests, API/load testing, staged deployment (dev → pre-prod → prod) |

**Quality gates at Level 2 (recommended target for Amplified Partners):**

```
Code commit
    ↓
CI: Unit tests + data schema validation + convergence check + NaN detection
    ↓
Model validation: Holdout eval + baseline comparison + segment consistency
    ↓
CD: Infrastructure compatibility + API/performance test + data validation
    ↓
Staged deployment: Dev → Pre-prod (manual approval) → Prod
    ↓
Monitoring: Drift detection → retrain trigger
```

**Key MLOps quality concepts for AI OS build:**

| Concept | Why it matters for document extraction/agent build |
|---|---|
| **Data versioning** (DVC/Git-LFS) | Track which version of your 4,787-doc vault trained which model |
| **Data validation** (Great Expectations) | Enforce schema on extracted documents before labelling |
| **Model registry** (MLflow) | Track all agent versions with performance metadata |
| **Feature store** | Consistent document embeddings across agents |
| **Metadata lineage** | Audit trail: which docs → which labels → which agent outputs |
| **Containerisation** (Docker/Kubernetes) | Reproducible builds, dev-prod parity |

**Source:** [Clarifai MLOps best practices](https://www.clarifai.com/blog/mlops-best-practices), [ThirstySprout MLOps guide](https://www.thirstysprout.com/post/mlops-best-practices)

---

## 9. Open-Source and Lightweight Alternatives

### 9.1 GSTT-CSC QMS Template (GitHub)

**URL:** https://github.com/GSTT-CSC/QMS-Template  
**What it is:** An open-source (Apache 2.0) ISO 13485-compliant QMS template built by Guy's and St Thomas' NHS Foundation Trust's Clinical Scientific Computing team for Software as a Medical Device (SaMD) and AI as a Medical Device (AIaMD). Survived 18 internal audits and 3 external audits by UK notified bodies.

**Why it's relevant:** While ISO 13485 (medical devices) is different from ISO 9001, the document structure is identical in principle. This is the most complete, battle-tested open-source QMS template available and includes an MLOps SOP.

**Key documents in the template:**

| Document Type | Examples |
|---|---|
| Policies/Plans (PL) | Quality Manual, Process Interaction Diagram |
| Procedures/SOPs (PR) | Design & Development, Clinical Risk Management, Verification & Validation, MLOps, Change Management, Internal Audit, GitHub PR Reviews |
| Forms/Templates (F) | Training Log, Incident Report, Software Validation, Hazard Log, Cyber Security, Requirements Template |
| Instructions (I) | Roles, Third-Party Software, Authorisation Log |

**Adaptation effort to ISO 9001/42001:** The clause numbering and medical-device specific requirements need replacing, but the structural pattern — especially the MLOps SOP (PR-008) and design/development SOP (PR-001) — can be directly adapted.

### 9.2 LightSME / LightStartup Framework

**What it is:** Academic framework (published 2023-2024) specifically designed for SME and startup quality management. Based on ISO/IEC 33000 (process assessment), not ISO 9001, but provides a lightweight maturity model adapted for companies too small for full CMMI or ISO implementation.

**Value:** Provides academic validation for the principle that a "lightweight, consistent, formalised process model" can work for startups without full certification overhead. Reduced process set (~34% fewer processes than full ISO/IEC 33000).

### 9.3 OpenRegulatory / Formwork

**URL:** https://openregulatory.com  
**What it is:** A startup offering free/low-cost QMS software using open tools (GitHub, Google Drive, SharePoint) as the infrastructure. Particularly focused on medical software but provides practical templates for any regulated software.

**Key insight from their research:** GitHub can effectively serve as a QMS backbone for technically-minded teams (version control of QMS documents, PR reviews as approval records, issues as CAPA tracker). This is directly applicable to Amplified Partners.

### 9.4 Using GitHub/GitLab as a Lightweight QMS

For a small technical team, the following mapping works well without expensive QMS software:

| QMS Requirement | GitHub/GitLab Implementation |
|---|---|
| Document control (version history) | Git commits + branch protection |
| Approval/sign-off | Pull Request reviews with required approvers |
| Change management | PR descriptions with change rationale |
| CAPA / corrective actions | GitHub Issues with labels + close criteria |
| Internal audits | Scheduled audit issues with checklists |
| Non-conformity records | Issues tagged 'non-conformity' |
| Management review inputs | Quarterly milestone reviews |
| Training records | GitHub Wiki or Notion linked from repo |

**Source:** [OpenRegulatory free QMS guide](https://openregulatory.com/articles/free-qms-software)

---

## 10. Agentic AI Standards (Emerging)

### 10.1 NIST AI Agent Standards Initiative

**Announced:** February 17, 2026 — very new. NIST launched the AI Agent Standards Initiative through its Center for AI Standards and Innovation (CAISI). [(NIST announcement)](https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure)

**Three pillars:**
1. Industry-led technical standards for AI agents (international standards leadership)
2. Open-source protocol development for agent interoperability
3. Research in AI agent security and identity

**Current deliverables:**
- RFI on AI Agent Security (closed March 2026)
- Draft Concept Paper: AI Agent Identity and Authorization
- Listening sessions with sector-specific stakeholders

**What this means for Amplified Partners:** There are currently *no* published standards specifically for agentic AI systems. The 2025 AI Agent Index found that only 15/30 major agent developers had published safety or trust frameworks, and 10/30 had none at all. This is a gap and an opportunity.

### 10.2 Emerging Agent-Specific Quality Concepts

From the 2025 AI Agent Index research:

| Quality Dimension | Status | Applicable to AP |
|---|---|---|
| Agent safety frameworks | Only ~50% of enterprise agents have these | Yes — build one |
| Guardrails/evaluation layers | Input sanitisation, output validation, tool-use policies | Yes — critical for document agents |
| Observability/tracing | OpenTelemetry integration; LangSmith for LangGraph | Yes — essential for debugging |
| Interoperability (MCP/A2A protocols) | Emerging in 2025 | Plan for, not yet required |
| Identity and authorisation | NIST draft standard expected 2026 | Monitor |

**Key frameworks referenced by enterprise agent developers:**
- Anthropic's Responsible Scaling Policy
- OpenAI's Preparedness Framework
- Microsoft's Responsible AI Standard
- ISO/IEC 42001 (increasingly adopted)
- SOC 2, ISO 27001 (infrastructure/security)

---

## 11. One Document or Two? The Key Strategic Decision

### The question framed clearly

Amplified Partners has two distinct but related quality needs:

**Build Process Framework (BPF):** How to assemble the AI system itself — document extraction, labelling, content routing, agent configuration, model management. This is about *what you build and how you build it*.

**Coding Standards Framework (CSF):** How to structure and deliver the code — naming conventions, repository structure, testing requirements, review processes, CI/CD gates. This is about *how you write and ship code*.

### Analysis

| Consideration | One Document | Two Documents |
|---|---|---|
| Audience | Mixed — engineers AND AI/data team AND client-facing | Separated — CSF for engineers; BPF for AI/data team + clients |
| Update frequency | Build process changes much more often than coding standards | Each can evolve independently |
| Auditability | One audit covers everything | Two cleaner audits with tighter scope |
| Onboarding | New hires get one document (simpler) | New hires get relevant document only (less overwhelming) |
| Client trust / marketing | Single "quality framework" is more impressive | Two specialist frameworks are more credible |
| ISO 42001 alignment | Harder to map clearly | BPF maps to ISO 42001; CSF maps to ISO/IEC 90003 |
| Product potential | One document is easier to sell/license | Two modular documents are more flexible for licensing |

### Recommendation: **Two documents, one governance wrapper**

The recommended structure is:

```
┌───────────────────────────────────────────────────────────┐
│           AMPLIFIED PARTNERS QUALITY POLICY               │
│    (1-page wrapper — ISO 9001/42001 governance layer)     │
│    Covers: Leadership commitment, scope, review cadence   │
└───────────────────────────────────────────────────────────┘
              │                           │
┌─────────────▼──────────┐  ┌────────────▼───────────────┐
│  DOCUMENT 1:           │  │  DOCUMENT 2:               │
│  AI BUILD PROCESS      │  │  CODING STANDARDS          │
│  FRAMEWORK (ABPF)      │  │  FRAMEWORK (CSF)           │
│                        │  │                            │
│  ISO 42001 aligned     │  │  ISO/IEC 90003 aligned     │
│  NIST AI RMF informed  │  │  ISO/IEC 25010 referenced  │
│                        │  │  MLOps Level 2 quality     │
│  Covers:               │  │  gates included            │
│  · Data ingestion      │  │                            │
│  · Labelling protocol  │  │  Covers:                   │
│  · Content routing     │  │  · Repo structure          │
│  · Agent config        │  │  · Naming conventions      │
│  · Model governance    │  │  · Testing standards       │
│  · Deployment ops      │  │  · PR/review process       │
│  · Bias monitoring     │  │  · CI/CD gates             │
│  · Client delivery     │  │  · Documentation standards │
└────────────────────────┘  └────────────────────────────┘
```

**Why the wrapper matters:** The single-page Quality Policy (analogous to ISO 9001 Clause 5.2) ties the two documents together under a unified governance posture. This means:
- A single internal audit covers both documents with one system
- Future ISO 9001 or ISO 42001 certification is achievable without restructuring
- The framework is perceived as a *system*, not two disconnected documents

---

## 12. Recommended Skeleton Framework

### DOCUMENT 1: AI Build Process Framework (ABPF)

Structured around ISO 42001's Annex A controls, adapted for a small AI consultancy:

```
AMPLIFIED PARTNERS
AI BUILD PROCESS FRAMEWORK (ABPF) v1.0

PART 1: FOUNDATION
  1.1  Scope and Purpose
  1.2  Definitions (AI system, agent, document vault, extraction pipeline...)
  1.3  Reference Standards (ISO 42001, NIST AI RMF, ISO 25010)
  1.4  Roles and Responsibilities (AI Policy Owner, Data Steward, Agent Lead)
  1.5  Review and Update Cadence

PART 2: DATA GOVERNANCE (maps to ISO 42001 A.7)
  2.1  Document Vault Management
       - Source classification and ingestion criteria
       - Document registration and unique ID assignment
       - Metadata schema requirements
  2.2  Extraction Standards
       - OCR/extraction tool standards
       - Extraction quality scoring thresholds
       - Failed extraction handling
  2.3  Labelling Protocol
       - Label taxonomy governance
       - Labeller qualification requirements
       - Inter-annotator agreement thresholds
       - Label quality audits
  2.4  Data Provenance
       - Document lineage logging (source → extracted → labelled → trained)
       - Version control for datasets
       - Data retirement and deletion procedures

PART 3: AI SYSTEM DESIGN & BUILD (maps to ISO 42001 A.6)
  3.1  Requirements Definition
       - Use case specification template
       - Intended use and limitations documentation
       - Stakeholder input requirements
  3.2  Architecture Standards
       - Agent design principles (modularity, single responsibility)
       - Content routing logic documentation
       - Knowledge base structure standards
  3.3  Development Process
       - Sprint/iteration structure
       - Design review gate criteria
       - Agent configuration documentation template
  3.4  Testing and Validation
       - Model performance acceptance criteria
       - Safety testing protocol for agents
       - User acceptance testing (UAT) with SMB clients
  3.5  Bias and Safety Assessment
       - Pre-deployment bias check protocol
       - Harm classification taxonomy
       - Human oversight requirements for high-risk outputs

PART 4: DEPLOYMENT AND OPERATIONS (maps to ISO 42001 A.6.2.5–6)
  4.1  Release Management
       - Staging environment requirements
       - Go/no-go release criteria
       - Rollback procedures
  4.2  Production Monitoring
       - Key performance indicators (accuracy, latency, cost/token)
       - Drift detection thresholds
       - Alert and escalation procedures
  4.3  Incident Management
       - Incident classification
       - Root cause analysis protocol
       - Corrective action and re-deployment

PART 5: CLIENT AND THIRD-PARTY (maps to ISO 42001 A.9, A.10)
  5.1  Client Onboarding
       - Data scope confirmation
       - Intended use agreement
       - Output limitations disclosure
  5.2  Third-Party AI Components
       - LLM provider governance (version pinning, change notification)
       - API dependency management
       - Vendor risk assessment for AI components
  5.3  Client Reporting
       - Performance reporting template
       - Issue communication protocol

PART 6: GOVERNANCE AND IMPROVEMENT (maps to ISO 42001 Clauses 9–10)
  6.1  Internal Audit Schedule
  6.2  Management Review Agenda Template
  6.3  Non-Conformity Register
  6.4  Continuous Improvement Log

APPENDICES
  A: Document Vault Metadata Schema
  B: Label Taxonomy (current version)
  C: Agent Configuration Template
  D: Pre-Deployment Bias Check Checklist
  E: ISO 42001 Clause-to-Section Cross-Reference
  F: NIST AI RMF Function-to-Section Cross-Reference
```

---

### DOCUMENT 2: Coding Standards Framework (CSF)

Structured around ISO/IEC 90003 and MLOps Level 2 quality gates:

```
AMPLIFIED PARTNERS
CODING STANDARDS FRAMEWORK (CSF) v1.0

PART 1: FOUNDATION
  1.1  Scope (languages covered, repo types, exclusions)
  1.2  Reference Standards (ISO/IEC 90003, ISO/IEC 25010, MLOps Level 2)
  1.3  Quality Characteristics (ISO 25010 mapping)
  1.4  Roles (Code Owner, Reviewer, Merge Authority)

PART 2: REPOSITORY STANDARDS
  2.1  Repository Structure
       - Monorepo vs polyrepo decision criteria
       - Standard folder structure template
       - Required root files (README, CHANGELOG, .gitignore, requirements.txt)
  2.2  Branching Strategy
       - Branch naming conventions
       - Protected branch rules
       - Feature → dev → staging → main flow
  2.3  Commit Standards
       - Conventional commits format
       - Minimum commit message requirements
       - Commit size guidelines

PART 3: CODE QUALITY STANDARDS
  3.1  Language-Specific Standards
       - Python: PEP8 + Black formatting, type hints required
       - JavaScript/TypeScript: ESLint config, Prettier
       - (Expand as applicable)
  3.2  Documentation Requirements
       - Docstring format (Google/NumPy style)
       - README completeness criteria
       - API documentation standards
  3.3  Security Standards
       - No credentials in code (pre-commit hook enforcement)
       - Dependency scanning requirements (Dependabot/Snyk)
       - OWASP ML Top 10 checklist reference

PART 4: TESTING STANDARDS (maps to ISO 25010 Reliability + Maintainability)
  4.1  Test Coverage Requirements
       - Minimum unit test coverage: [define %]
       - Integration test requirements
       - ML-specific tests: data validation, model convergence, NaN checks
  4.2  Test Infrastructure
       - Test environment parity with production
       - Test data management (no real client data in tests)
       - Mock/stub standards for external services
  4.3  Data Quality Tests
       - Schema validation requirements (Great Expectations or equivalent)
       - Statistical profiling for ML inputs
       - Anomaly detection thresholds

PART 5: REVIEW AND APPROVAL (maps to ISO/IEC 90003 Section 8.3)
  5.1  Pull Request Standards
       - PR description template (what/why/how/test evidence)
       - Minimum reviewers required (by change type)
       - Review SLA (e.g., 24h response, 48h approval)
  5.2  Code Review Criteria
       - Functional correctness
       - Test coverage check
       - Documentation completeness
       - Security scan passing
       - No critical linting violations
  5.3  Merge Criteria
       - All CI checks green
       - Required approvals obtained
       - Changelog updated
       - Version bumped (if release)

PART 6: CI/CD QUALITY GATES (MLOps Level 2 pattern)
  6.1  Continuous Integration Pipeline
       - Linting (auto-fail on critical violations)
       - Unit tests + coverage report
       - Security scan (SAST)
       - Dependency vulnerability check
       - ML-specific: data schema validation, model smoke test
  6.2  Continuous Delivery Pipeline
       - Integration tests
       - Performance baseline comparison
       - Staging deployment + smoke test
       - Manual approval gate for production
  6.3  Monitoring and Alerting
       - Production error rate thresholds
       - Latency SLA monitoring
       - Model performance drift alert
       - Cost-per-inference monitoring

PART 7: RELEASE MANAGEMENT (maps to ISO/IEC 90003 Section 8.6)
  7.1  Versioning Standard (Semantic Versioning 2.0)
  7.2  Release Checklist Template
  7.3  Rollback Procedure
  7.4  Post-Release Review Template

APPENDICES
  A: PR Description Template
  B: Release Checklist
  C: ISO 25010 Quality Characteristic ↔ Test Type Mapping
  D: CI/CD Configuration Reference (GitHub Actions/GitLab CI examples)
  E: ISO/IEC 90003 Clause-to-Section Cross-Reference
```

---

### THE WRAPPER: Quality Policy (1 page)

```
AMPLIFIED PARTNERS
QUALITY POLICY v1.0

Amplified Partners builds AI-powered business operating systems for SMBs.
We commit to:

1. QUALITY: Delivering AI systems that are accurate, reliable, and fit
   for the intended use cases of our clients.

2. SAFETY: Ensuring all AI systems are safe for deployment, with
   appropriate human oversight and documented limitations.

3. TRANSPARENCY: Maintaining full traceability from data to output,
   and communicating clearly with clients about system capabilities.

4. IMPROVEMENT: Reviewing the effectiveness of our quality management
   framework quarterly and updating it in response to findings.

This policy is implemented through:
- The AI Build Process Framework (ABPF) — governing how we build AI
- The Coding Standards Framework (CSF) — governing how we write code

Both documents are controlled under version control, reviewed annually,
and governed by the Quality Policy Owner: [Name, Role].

Aligned with: ISO/IEC 42001:2023, ISO/IEC 90003:2014, NIST AI RMF 1.0

Signed: _______________  Date: _______________
```

---

## 13. Framework as a Product

### The market opportunity

The 2025 AI Agent Index found that only 15/30 major enterprise AI agent developers had published safety or trust frameworks — and these are the *largest* AI companies in the world. For small AI consultancies and AI-for-SMB builders, there is essentially no off-the-shelf quality framework that is:

- Designed for small teams (not large enterprise)
- Covers both the AI build process AND code quality in one system
- Aligned with ISO 42001 (but doesn't require costly certification)
- Practical and fillable, not just theoretical

This is a genuine product gap.

### What exists (and why it falls short)

| Existing option | Limitation for AI consultancies |
|---|---|
| ISO 9001 QMS software (QT9, Qualtrax, etc.) | £10K-£50K/year; not AI-specific |
| ISO 42001 implementation guides (KPMG, EY) | Designed for large enterprises; no code quality |
| GSTT-CSC QMS Template | Medical device focus; no coding standards |
| NIST AI RMF Playbook | No code quality; no implementation template |
| MLOps frameworks | No governance/compliance layer |

### Product concept

**"Amplified Quality System (AQS)"** — a dual-document framework skeleton, available as:

1. **Open-source starter** (GitHub): Basic skeleton with fill-in sections, version-controlled, community-improvable. Builds credibility and inbound attention.

2. **Paid consultancy add-on** (£2,500-£5,000): Pre-filled, customised implementation for another AI consultancy's specific stack and use case.

3. **Licensed template kit** (£500-£1,500/year): Pre-filled templates + annual update service + community access.

### Target buyers

- Small AI consultancies (5-20 people) building AI products for clients
- In-house AI teams at professional services firms (law, accountancy) deploying AI
- AI-for-SMB builders similar to Amplified Partners
- Any company wanting ISO 42001-readiness without expensive consultants

### Differentiating features

- First framework to explicitly cover both *build process* and *coding standards* in one system
- ISO 42001-aligned (the most current AI governance standard, published December 2023)
- Designed for teams of 2-10, not enterprises
- Practical: GitHub-native implementation, no QMS software required
- NIST AI RMF cross-reference built in (US market compatibility)

### Realistic caution

Before productising: The framework needs to be proven on the Amplified Partners AI OS build first. Using it internally for 6-12 months before selling creates:
- Real case study evidence
- Battle-tested templates (not theoretical)
- Genuine credibility with buyers

---

## 14. Practical Recommendations for Amplified Partners

### Immediate priorities (next 30 days)

1. **Adopt the two-document structure.** Build the Quality Policy wrapper and start filling in the AI Build Process Framework (ABPF). Focus first on Part 2 (Data Governance) since the document vault extraction is the active work.

2. **Start with the GSTT-CSC QMS template as a structural reference.** Their Design & Development SOP (PR-001), MLOps SOP (PR-008), and GitHub PR Review procedure (PR-017) are immediately adaptable. Fork the repo and adapt.

3. **Use GitHub as the QMS platform.** Store both framework documents in a private repo. Use PR reviews for any framework changes. Create Issues for non-conformities. Zero additional software cost.

4. **Define the data provenance schema first.** Before labelling begins at scale, document: what metadata you capture per document, what constitutes an "extraction failure," and how label versions are tracked. This is ISO 42001 A.7 in practice.

### Near-term priorities (30-90 days)

5. **Build the bias check checklist** (ABPF Appendix D). Before any AI outputs reach clients, define what "good output" looks like and what failure modes are acceptable. This is the most immediate risk mitigation.

6. **Implement CI/CD quality gates.** Start with the basics: linting, unit tests, and a smoke test for each agent. The CSF CI/CD section is a good forcing function for this.

7. **Do a NIST AI RMF "Map" exercise.** For your AI OS product, document the context, stakeholders, capabilities, and limitations in a structured way. This is 2 hours of structured thinking that pays dividends in client conversations and investor due diligence.

### Strategic decisions (90+ days)

8. **Consider ISO 42001 readiness, not certification.** Certification costs £5,000-£15,000+ for a small company and requires ongoing audit. Being "ISO 42001 aligned" (with your framework mapped against the standard) is sufficient for most client conversations and positions you for certification later if a client requires it.

9. **Share the framework publicly once internal.** Open-source the skeleton (without your specific configurations) to build reputation, attract talent, and create inbound for the product concept.

10. **Monitor the NIST AI Agent Standards Initiative.** This is very new (February 2026) and will generate voluntary standards for agentic AI over the next 12-18 months. Position the framework for update cycles when those emerge.

### What good looks like in 12 months

```
Amplified Partners Quality System
├── Quality Policy v1.2 (reviewed Q3 2026)
├── AI Build Process Framework v1.3
│   ├── 4,787 docs tracked in provenance log
│   ├── Pre-deployment bias check completed for v1 agents
│   └── ISO 42001 cross-reference validated by external review
├── Coding Standards Framework v1.1
│   ├── 85%+ test coverage on core modules
│   ├── CI/CD gates blocking all non-conformant merges
│   └── Zero security scan critical failures in production
├── Q1–Q3 Internal Audit Reports
├── 3 Non-conformity records + closed CAPAs
└── Management Review Minutes (Q2, Q3 2026)
```

---

## Sources

| Topic | Source | URL |
|---|---|---|
| ISO/IEC 90003 | ISO Standard Page | https://www.iso.org/standard/66240.html |
| ISO/IEC 90003 guide | Walturn | https://www.walturn.com/insights/understanding-iso-9001-and-90003-for-software-quality-management |
| ISO 42001 standard | ISO | https://www.iso.org/standard/42001 |
| ISO 42001 vs ISO 9001 | ISMS.online | https://www.isms.online/iso-42001/vs-iso-9001/ |
| ISO 42001 Annex A | ISMS.online | https://www.isms.online/iso-42001/annex-a-controls/ |
| ISO 42001 clause structure | Cyberzoni | https://cyberzoni.com/standards/iso-42001/ |
| ISO 42001 implementation | Iterasec | https://iterasec.com/blog/iso-iec-42001-implementation-guide/ |
| ISO 42001 AI lifecycle | AWS Security Blog | https://aws.amazon.com/blogs/security/ai-lifecycle-risk-management-iso-iec-420012023-for-ai-governance/ |
| ISO 42001 governance | KPMG | https://kpmg.com/ch/en/insights/artificial-intelligence/iso-iec-42001.html |
| ISO 42001 ethical AI | EY | https://www.ey.com/en_us/insights/ai/iso-42001-paving-the-way-for-ethical-ai |
| ISO 42001 vs NIST RMF | StandardFusion | https://www.standardfusion.com/blog/key-differences-between-iso-42001-and-nist-ai-rmf |
| ISO 42001 overlaps | Elevate | https://elevateconsult.com/insights/how-iso-42001-overlaps-with-iso-27001-and-iso-9001/ |
| ISO/IEC 25010:2023 | arc42 | https://quality.arc42.org/articles/iso-25010-update-2023 |
| ISO 25010 guide | Pacific Certifications | https://blog.pacificcert.com/iso-25010-software-product-quality-model/ |
| NIST AI RMF | NIST | https://www.nist.gov/itl/ai-risk-management-framework |
| NIST AI RMF 2025 updates | I.S. Partners | https://www.ispartnersllc.com/blog/nist-ai-rmf-2025-updates-what-you-need-to-know-about-the-latest-framework-changes/ |
| NIST AI Agent Standards | NIST | https://www.nist.gov/news-events/news/2026/02/announcing-ai-agent-standards-initiative-interoperable-and-secure |
| CMMI vs ISO 9001 | PopularCert | https://popularcert.com/iso-9001-vs-cmmi-difference-quality-management-certification/ |
| CMMI comparison | Core Business Solutions | https://www.thecoresolution.com/cmmi-and-iso-9001-comparison |
| MLOps maturity levels | Google Cloud | https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning |
| MLOps best practices | Clarifai | https://www.clarifai.com/blog/mlops-best-practices |
| MLOps production | ThirstySprout | https://www.thirstysprout.com/post/mlops-best-practices |
| Open-source QMS template | GSTT-CSC GitHub | https://github.com/GSTT-CSC/QMS-Template |
| Free QMS software | OpenRegulatory | https://openregulatory.com/articles/free-qms-software |
| QMS documentation structure | Advisera/9001Academy | https://advisera.com/9001academy/knowledgebase/how-to-structure-quality-management-system-documentation/ |
| Document processing governance | AWS ML Blog | https://aws.amazon.com/blogs/machine-learning/intelligent-governance-of-document-processing-pipelines-for-regulated-industries/ |
| 2025 AI Agent Index | arXiv | https://arxiv.org/html/2602.17753v1 |
| Agentic AI frameworks 2025 | Katara.ai | https://www.katara.ai/guides/agentic-ai-frameworks-2025-compare-build-benchmark |
| LightStartup framework | University of Hawaii | https://scholarspace.manoa.hawaii.edu/bitstreams/8267e43f-3076-4c47-ab6c-86b4a9a2d4d7/download |

---

*Document version: 1.0 | Research date: March 2026 | Prepared for: Amplified Partners*
