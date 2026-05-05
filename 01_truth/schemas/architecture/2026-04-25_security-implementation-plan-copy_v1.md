---
title: "Check: caps dropped?"
id: "security-implementation-plan-copy"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "implementation-plan"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

Security
Implementation Plan
Cove-Orchestrated Deployment
From the Security Architecture v2.0 to Production Reality
14 March 2026
CONFIDENTIAL


CONFIDENTIAL
2
Table of Contents
1. Strategic Overview
3
2. Current State: What Exists Today
4
3. The Implementation Philosophy
5
4. Security Architecture as Cove Reference Document
5
5. Phased Implementation Plan
7
5.1 Phase 0: Human Actions (URGENT)
7
5.2 Phase 1: Secrets Foundation
8
5.3 Phase 2: Network + Monitoring
10
5.4 Phase 3: Cove Security Integration
11
5.5 Phase 4: Advanced Security
12
6. Dependency Map
13
7. Cove Temporal Workflows to Build
14
8. Linear Issues to Create
15
9. What Perplexity Can Do Next
17
10. Risk Register
18
11. Timeline Summary
19
Appendix: Master Build Spec Integration
20


CONFIDENTIAL
3
1. Strategic Overview
The Problem
The security architecture v2.0 is a 37-page blueprint. It identifies 10 layers, 6 critical gaps, and
recommends 10 new Linear issues. But a document doesn't make you secure — implementation
does.
There are 9 active Linear projects, 35+ Docker containers, 40+ tracked issues, and multiple
parallel builds (Cove Temporal workers, Enforcer v1.0, multi-team build orchestrator, product
development). Security cannot be bolted on as a separate workstream — it must be woven into
everything.
The Solution
• Use Cove (the Temporal-based orchestration platform already running on Beast) to execute
the security implementation as a series of traceable, auditable, deterministic workflows.
• The security architecture PDF becomes a reference document that Cove's agents (Builder,
Security, Enforcer) use as their ground truth for every build.
• Nothing gets deployed without passing security gates defined in this document.
Why Cove Is the Right Tool
• Already deployed on Beast with Temporal workers
• LangGraph-based agent teams (Builder, Security, Enforcer, Kaizen) already designed
• Deterministic workflows with full audit trails — exactly what security needs
• The Enforcer agent (COV-214, In Progress) already does health checking — extend it to
security compliance
• The Kaizen loop means security posture improves automatically over time
Key Distinction
This document is about HOW to implement, not WHAT to implement. The "what" is defined in
the Security Architecture v2.0 PDF — the canonical source of truth. This plan translates that
architecture into phased, Cove-orchestrated deployment workflows.


CONFIDENTIAL
4
2. Current State: What Exists Today
Cove Infrastructure (Live on Beast)
• Temporal server + workers running in Docker
• FastAPI gateway (7 endpoints, built in session with Perplexity)
• PlannerWorkflow: Linear issue → architect decomposition → ProjectOrchestrator
• Kaizen module: metrics collection, retrospectives, quality scoring
• API gateway with Bearer token + Linear HMAC-SHA256 + Telegram webhook auth
• Intelligence pipeline running every 6 hours
• Layer 0 Amplified Laws deployed (immutable ethical constraints)
The Enforcer (COV-214, In Progress)
• 17 files, ~2,500 lines Python + FastAPI
• 5 deterministic health checks: Docker containers, databases, Traefik routing, session hygiene,
security (fail2ban/firewall)
• Runs every 10 minutes, all checks concurrent, <30s total
• JSON structured logging, Prometheus metrics, webhook alerts
Security Gaps (from v2.0)
Critical Gaps Identified in v2.0
Layer 4 (Secrets): No Vaultwarden, no Infisical — .env files everywhere
Layer 5 (Network): No VPN mesh — all services exposed to public internet
Layer 6 (Monitoring): No SIEM — only Enforcer health checks
Layer 3 (Traefik): No security headers, no CrowdSec, no rate limiting
Layer 9 (Compliance): MFA not enabled, Cyber Essentials not registered
Layer 10 (Endpoints): macOS audit not done
Active Parallel Projects That Affect Security
Project
Status
Security Impact
Multi-Team Build Orchestrator
(COV-262/265)
Backlog
Git worktrees on Beast need isolation, secret injection
Finance Engine (COV-254)
Deployed
Handles financial data — needs P2 tokenization
OpenClaw Agent Service
(COV-233)
Deployed
8 LLM models via LiteLLM — API key management critical


CONFIDENTIAL
5
Project
Status
Security Impact
Intelligence Pipeline (COV-275)
Deployed
Runs every 6h — needs audit logging
Staff Consent Model (COV-124)
Todo, Urgent
Privacy framework for agent interactions
Base Layer Services (COV-215)
In Progress
Blocked by secrets — Vaultwarden/Infisical unblocks this
Prompt Architecture (COV-274)
Backlog,
Urgent
Layer 0 Laws need enforcement pipeline
Master Build Spec (COV-269)
Backlog,
Urgent
9-layer, 35-day build — security must be embedded
3. The Implementation Philosophy
Three principles govern every decision in this plan:
1. SECURITY FIRST, THEN BUILD
• Phase 0 (human actions) and Phase 1 (secrets + network) MUST complete before any new
service is deployed
• Every Cove workflow must check "are secrets in Infisical?" before running
• The security architecture PDF is committed to the amplified-partners repo as the canonical
reference
2. COVE ENFORCES, HUMANS DECIDE
• Cove orchestrates security checks, not security decisions
• Every deployment workflow includes a security gate (automated checks + human approval for
production)
• The Enforcer runs continuously; humans respond to escalations
3. EVERYTHING IS AUDITABLE
• Every security change is a Temporal workflow with full audit trail
• Every secret rotation is logged in Infisical with timestamp and actor
• Every compliance check result is stored in PostgreSQL for Cyber Essentials evidence
4. The Security Architecture as Cove
Reference Document
The v2.0 PDF must become a living, machine-readable reference that Cove consults on every
build. Here is how to embed it into Cove's workflow:
Step 1: Commit to Repo
• Push beast-security-architecture-v2.pdf to amplified-partners/docs/security/
• Create a SECURITY-POLICY.md that extracts the machine-readable rules from the PDF:


CONFIDENTIAL
6
• Required container hardening flags (--cap-drop ALL, --no-new-privileges, --read-only)
• Required Traefik middleware (security headers, rate limiting, HSTS)
• Required secrets injection pattern (Infisical Machine Identity, not .env)
• Required audit logging format
• Required compliance checks for Cyber Essentials
Step 2: Build Security Gate Activity
Create a Temporal activity check_security_compliance() that reads SECURITY-POLICY.md rules,
validates a deployment against each rule, and returns pass/fail with specific violations. This
becomes mandatory in every Cove deployment workflow.
@activity.defn
async def check_security_compliance(deployment_config: dict) -> SecurityReport:
    """Validate a deployment against SECURITY-POLICY.md rules."""
    # Check: caps dropped?
    # Check: read-only filesystem?
    # Check: secrets from Infisical (not .env)?
    # Check: Traefik labels include security headers?
    # Check: resource limits set?
    # Check: non-root user?
    return SecurityReport(passed=True/False, violations=[...])
Step 3: Enforcer Extension
Extend The Enforcer (COV-214) with security compliance checks beyond health:
• Container hardening verification (are caps dropped? is read-only set?)
• TLS certificate validity
• Infisical connectivity (are secrets reachable?)
• CrowdSec health (is threat intelligence active?)
• Wazuh agent status (are all devices reporting?)
Step 4: Kaizen Integration
• The Kaizen module already collects build metrics
• Add security metrics: containers passing hardening, secrets in Infisical vs .env, CVE count
from Trivy, CrowdSec blocked IPs
• Weekly security retrospective: what improved, what degraded, what's still open
5. Phased Implementation Plan
The implementation is divided into five phases with strict dependencies. Each phase builds on the
previous one, with Cove orchestrating the automated components.


CONFIDENTIAL
7
5.1 Phase 0: Human Actions — This Weekend
URGENT — REQUIRES EWAN'S PHYSICAL DEVICES AND ACCOUNTS
These actions cannot be automated. They require physical access to devices and cloud
accounts. Estimated total time: 2 hours. Complete this weekend before any automated
deployment begins.
Action
Time
Why It Can't Wait
Enable MFA on ALL cloud services
(COV-82)
30 min
Mandatory from April 2026, Cyber Essentials
blocker
Verify macOS security settings (COV-83)
15 min per
Mac
FileVault, Gatekeeper, screen lock,
auto-updates
Change router admin password, disable
UPnP (COV-84)
10 min
Network perimeter gap
Create separate admin account on macOS
(COV-86)
10 min per
Mac
Least privilege for Cyber Essentials
Register for Cyber Essentials (COV-87)
15 min
Before 28 April for v3.2 (simpler)
Deliverable: COV-82, COV-83, COV-84, COV-86, COV-87 marked Done in Linear.


CONFIDENTIAL
8
5.2 Phase 1: Secrets Foundation — Week 1
Critical Path
This is the critical path. Everything else depends on secrets being centralised. Estimated: 4-5
hours (2 hours human, 2-3 hours Cove-automated).
Day 1-2: Deploy Vaultwarden
• DNS: vault.beast.amplifiedpartners.ai → 135.181.161.131
• Docker: vaultwarden/server:latest on amplified-net
• Create admin account, disable signups
• Set up clients: Mac Mini (Homebrew), MacBook Air, Beelink (download), iPhone (App Store)
• Register 4 passkeys (one per device)
• Import all existing browser passwords
Cove's Role: DeployVaultwarden Temporal workflow — generates docker-compose, runs
DNS checks, verifies container health. Human must create account and register passkeys.
Day 2-3: Deploy Infisical
• DNS: secrets.beast.amplifiedpartners.ai → 135.181.161.131
• Docker: infisical + postgres + redis
• Generate bootstrap secrets (openssl rand), store at /opt/amplified/.bootstrap-secrets
• Create "Amplified Core" project
• Install CLI on Mac Mini, MacBook Air, Beelink
Cove's Role: DeployInfisical workflow — generate docker-compose, provision bootstrap
secrets, verify health. Human must create admin account and install CLI on endpoints.
Day 3-4: Consolidate + Migrate Secrets
• Pick canonical Anthropic key (consolidate from 2 different keys)
• Pick canonical OpenAI key
• Revoke non-canonical keys in provider consoles
• Add ALL canonical keys to Infisical
• Store Infisical admin password in Vaultwarden


CONFIDENTIAL
9
Cove's Role: MigrateSecrets workflow — for each of 29 containers: create Machine Identity,
update docker-compose to use infisical run, test startup, delete old .env. This is the ideal
Cove automation — repetitive, deterministic, verifiable.
Day 4-5: Clean Up
• Delete all .env files on Mac Mini and Beast
• Replace with .env.reference (variable names only, no values)
• Run git-secrets --install on all repos
Cove's Role: CleanupSecrets workflow — scan all repos for .env files, create .env.reference,
verify git-secrets hook installation.
Phase 1 Deliverable: Zero .env files. All secrets in Infisical. All passwords in Vaultwarden. Bootstrap
secrets in physical safe.


CONFIDENTIAL
10
5.3 Phase 2: Network + Monitoring — Week 2-3
With secrets centralised, Cove can now safely deploy monitoring and network infrastructure.
Estimated: 8-10 hours (1 hour human, 7-9 hours Cove-automated).
Week 2, Day 1-2: CrowdSec + Traefik Hardening
• Deploy CrowdSec container on Beast (amplified-net)
• Install Traefik bouncer plugin
• Add CrowdSec collections: traefik, http-cve, http-dos
• Add Traefik security headers middleware (CSP, HSTS, X-Frame-Options)
• Enable rate limiting on all public endpoints
• Check for CVE-2025-66491 (TLS verification bug)
Cove's Role: DeployCrowdSec workflow + HardenTraefik workflow. Both are deterministic
Docker + config deployments. Enforcer validates completion.
Week 2, Day 3-5: Wazuh SIEM Deployment
• Deploy Wazuh stack: Manager + Indexer (OpenSearch) + Dashboard on Beast
• Install Wazuh agent on Beast (local), Mac Mini, Beelink
• MacBook Air agent when returned from repair
• Configure Docker listener for container monitoring
• Enable File Integrity Monitoring (FIM) on critical paths
Cove's Role: DeployWazuh workflow — complex multi-container deployment, perfect for
Temporal orchestration. Includes health verification steps and agent enrollment.
Week 3, Day 1-3: NetBird VPN Mesh
• Deploy NetBird management server on Beast
• Enroll: Beast (hub), Mac Mini, MacBook Air, Beelink, iPhone
• Configure access policies: admin services only via VPN
• Restrict Vaultwarden and Infisical to VPN access only
• Harden Syncthing: disable global discovery, VPN-only traffic
Cove's Role: DeployNetBird workflow + NetworkLockdown workflow. After NetBird is live, a
second workflow restricts service access to VPN IPs.
Phase 2 Deliverable: CrowdSec blocking malicious IPs. Wazuh monitoring all devices. VPN mesh
securing inter-device traffic. Traefik hardened.


CONFIDENTIAL
11
5.4 Phase 3: Cove Security Integration — Week 3-4
This is where Cove becomes the security enforcement engine. Estimated: 6-8 hours (1 hour
human, 5-7 hours Cove-automated).
Step 1: Commit Security Policy to Repo
• Push SECURITY-POLICY.md + v2.0 PDF to amplified-partners
• SECURITY-POLICY.md contains machine-readable rules
Step 2: Build SecurityGate Temporal Activity
Create the check_security_compliance() Temporal activity as detailed in Section 4. This validates
every deployment against SECURITY-POLICY.md rules before proceeding.
Step 3: Wire SecurityGate into PlannerWorkflow
• Before ProjectOrchestrator launches a build, it runs check_security_compliance()
• If violations exist: workflow pauses, sends notification via Telegram/WhatsApp
• Human reviews violations, approves override or requires fix
• No code gets deployed to Beast without passing security checks
Step 4: Extend Enforcer
• Add Wazuh alert consumption
• Add CrowdSec metrics collection
• Add Trivy scan scheduling (daily image scans)
• Add Infisical health check
• All results feed into Prometheus + the Kaizen security dashboard
Step 5: Build SecurityRetrospective Kaizen Activity
• Weekly: collect security metrics from Enforcer + Wazuh + CrowdSec + Trivy
• Compare against last week: improved? degraded? new CVEs?
• Generate human-readable security report
• Store in PostgreSQL for Cyber Essentials audit evidence
Phase 3 Deliverable: Cove enforces security on every build. The Enforcer monitors continuously.
Kaizen improves security posture automatically.


CONFIDENTIAL
12
5.5 Phase 4: Advanced Security — Week 5-8
With the foundation secure, advanced capabilities can be built. Estimated: 15-20 hours (2 hours
human, 13-18 hours Cove-automated).
Month 2, Week 1-2: P2 Tokenization
• Design token vault schema (PostgreSQL on Beast)
• Build tokenization service (FastAPI container)
• Integrate with Finance Engine (COV-254) — tokenize all PII before cloud API calls
• Integrate with CRM (amplified-crm) — tokenize client data
Cove's Role: Temporal workflow for tokenization service deployment + integration testing.
Month 2, Week 3-4: Sentinel AI Security Agent
• Build as Docker container on Beast
• Consumes: Wazuh alerts, CrowdSec events, Trivy scan results
• LLM-powered analysis (via LiteLLM/Ollama — keep it local)
• Automated responses: block IPs, isolate containers, trigger key rotation
• SOAR integration via Tracecat
Cove's Role: The Sentinel is essentially a specialised Cove agent — it runs as a Temporal
workflow that polls for security events and triggers response workflows.
Month 2, Week 4: Cyber Essentials Completion
• Compile all evidence from Wazuh + CrowdSec + Infisical + Enforcer logs
• Fill Cyber Essentials questionnaire (Cove can draft answers from collected evidence)
• Submit for review
Cove's Role: ComplianceReport workflow — gathers all evidence into a structured document
ready for submission.


CONFIDENTIAL
13
6. Dependency Map
Each phase has strict dependencies on the previous phase. No phase can begin until its
predecessor delivers its stated outputs. The diagram below shows the complete dependency
chain:
Phase 0 (Human)
├── MFA (COV-82) ─────────────────────────────┐
├── macOS Audit (COV-83) ─────────────────────┤
├── Router (COV-84) ──────────────────────────┤
├── Admin Account (COV-86) ───────────────────┤
└── Cyber Essentials Reg (COV-87) ────────────┤
                                               │
Phase 1 (Secrets) ◄────────────────────────────┘
├── Vaultwarden ──────────────────┐
├── Infisical ────────────────────┤
├── Secret Consolidation ─────────┤
└── .env Cleanup ─────────────────┤
                                   │
Phase 2 (Network + Monitoring) ◄───┘
├── CrowdSec + Traefik Hardening ──┐
├── Wazuh SIEM ────────────────────┤
├── NetBird VPN ───────────────────┤
└── Syncthing Hardening ───────────┤
                                    │
Phase 3 (Cove Integration) ◄────────┘
├── SECURITY-POLICY.md in repo
├── SecurityGate activity
├── Enforcer extension
└── Security Kaizen metrics
         │
Phase 4 (Advanced) ◄─────────────────
├── P2 Tokenization
├── Sentinel AI Agent
└── Cyber Essentials submission
Dependency Enforcement
Key constraint: Phase 0 items are human-only and must be completed before Cove can
begin Phase 1 automation. Each subsequent phase's Temporal workflows validate that
prerequisites from the prior phase are met before proceeding.


CONFIDENTIAL
14
7. Cove Temporal Workflows to Build
The following 15 Temporal workflows represent the complete automation surface for this security
implementation. Total estimated scope: ~4,900 lines of production code.
Workflow
Type
Ph.
LOC
Dependencies
DeployVaultwarden
Infrastructure
1
~200
DNS, Traefik
DeployInfisical
Infrastructure
1
~300
DNS, Traefik, Postgres
MigrateContainerSecrets
Migration
1
~500
Infisical running
CleanupDotEnv
Cleanup
1
~150
All secrets in Infisical
DeployCrowdSec
Infrastructure
2
~250
Traefik
HardenTraefik
Configuration
2
~200
CrowdSec
DeployWazuh
Infrastructure
2
~400
Docker, amplified-net
DeployNetBird
Infrastructure
2
~350
All services stable
NetworkLockdown
Configuration
2
~200
NetBird running
SecurityGateCheck
Activity
3
~300
SECURITY-POLICY.md
ExtendEnforcer
Enhancement
3
~400
Wazuh, CrowdSec, Infisical
SecurityRetrospective
Kaizen
3
~250
All Phase 2 services
DeployTokenizer
Infrastructure
4
~500
Infisical, PostgreSQL
BuildSentinel
Agent
4
~600
Wazuh, CrowdSec, LiteLLM
ComplianceReport
Report
4
~300
All evidence sources
Phase
Workflows
Total LOC
Phase 1: Secrets
4
~1,150
Phase 2: Network
5
~1,400
Phase 3: Integration
3
~950
Phase 4: Advanced
3
~1,400
TOTAL
15
~4,900


CONFIDENTIAL
15
8. Linear Issues to Create
These 18 issues should be created in Linear to track the implementation. Each maps to a specific
phase and Cove workflow.
Phase 1 — Secrets
#
Title
Priority
Project
1
Deploy Vaultwarden on Beast
P1 (Urgent)
Infrastructure
2
Deploy Infisical on Beast
P1 (Urgent)
Infrastructure
3
Consolidate and rotate all exposed API keys
P1 (Urgent)
Infrastructure
4
Migrate 29 Docker containers to Infisical secrets injection
P2 (High)
Infrastructure
5
Delete all .env files + install git-secrets
P2 (High)
Infrastructure
6
Secure bootstrap secrets: encrypted USB + physical safe
P1 (Urgent)
Infrastructure
Phase 2 — Network + Monitoring
#
Title
Priority
Project
7
Deploy CrowdSec + Traefik bouncer on Beast
P2 (High)
Infrastructure
8
Harden Traefik: security headers, rate limiting, TLS
P2 (High)
Infrastructure
9
Deploy Wazuh SIEM stack on Beast
P2 (High)
Infrastructure
10
Deploy NetBird VPN mesh across 5 devices
P2 (High)
Infrastructure
11
Harden Syncthing: VPN-only, disable global discovery
P3 (Medium)
Infrastructure
Phase 3 — Cove Integration
#
Title
Priority
Project
12
Commit SECURITY-POLICY.md to amplified-partners repo
P2 (High)
Infrastructure
13
Build SecurityGate Temporal activity for Cove
P2 (High)
Multi-Team Build Orch.
14
Extend Enforcer with security compliance checks
P2 (High)
Infrastructure
15
Build Security Kaizen retrospective workflow
P3 (Medium)
Infrastructure
Phase 4 — Advanced


CONFIDENTIAL
16
#
Title
Priority
Project
16
Build P2 tokenization service on Beast
P3 (Medium)
Product R&D
17
Build Sentinel AI security agent
P3 (Medium)
Infrastructure
18
Complete Cyber Essentials self-assessment
P2 (High)
Governance & Principles


CONFIDENTIAL
17
9. What Perplexity Can Do Next
Each of the following is a concrete, scoped session. Hand the number to Perplexity and receive
deployable code or configuration:
#
Action
Output
1
Write the docker-compose files for
Vaultwarden and Infisical
Ready-to-deploy compose files with Traefik labels, resource
limits, and hardened container flags.
2
Write the SECURITY-POLICY.md
machine-readable rules file
Structured YAML/markdown rules extracted from the v2.0
architecture for Cove to parse.
3
Write the SecurityGate Temporal activity
code
Python activity that validates deployments against
SECURITY-POLICY.md rules.
4
Write the MigrateContainerSecrets
workflow code
Temporal workflow that migrates each of 29 containers from .env
to Infisical injection.
5
Write the CrowdSec + Traefik hardening
configuration
CrowdSec docker-compose + Traefik middleware configuration
for security headers and rate limiting.
6
Write the Wazuh docker-compose +
agent enrollment scripts
Full Wazuh stack deployment with agent enrollment automation.
7
Create all 18 Linear issues
programmatically
Script to create all issues via Linear API with correct priorities,
projects, and labels.
8
Write the Enforcer security extensions
Extended health checks for container hardening, TLS, Infisical,
CrowdSec, and Wazuh.
9
Write the Security Kaizen retrospective
activity
Weekly metrics collection and comparison workflow for
continuous security improvement.
10
Draft the Cyber Essentials questionnaire
answers
Pre-filled answers derived from collected evidence across all
monitoring systems.
Actionable Outputs
Each session produces deployable artifacts — not documentation. The output goes directly
into the amplified-partners repo and can be deployed by Cove's Temporal workflows.


CONFIDENTIAL
18
10. Risk Register
Identified risks across all implementation phases, with impact assessment and mitigations:
Risk
Impact
Likelihood
Mitigation
Exposed API keys exploited before
rotation
Critical
Medium
Phase 0 priority: rotate immediately
MFA deadline missed (April 2026)
High
Low if actioned
now
Phase 0: 30 minutes, do this weekend
Infisical deployment fails
High
Low
Well-documented Docker deployment, fallback to
Docker secrets
Container migration breaks
services
High
Medium
Migrate one container at a time, test before
proceeding
VPN mesh causes connectivity
issues
Medium
Medium
Deploy NetBird last in Phase 2, test thoroughly
Wazuh resource overhead on
Beast
Low
Low
256GB RAM, Wazuh uses ~2GB — negligible
Cove SecurityGate too strict,
blocks builds
Medium
Medium
Human override with audit trail
Single point of failure: bootstrap
secrets
Critical
Low
Encrypted USB + printed copy in physical safe


CONFIDENTIAL
19
11. Timeline Summary
Phase
When
Duration
Human Time
Cove-Automated
0: Human Actions
This weekend
2 hours
2 hours
0
1: Secrets Foundation
Week 1
4-5 hours
2 hours
2-3 hours
2: Network + Monitoring
Week 2-3
8-10 hours
1 hour
7-9 hours
3: Cove Integration
Week 3-4
6-8 hours
1 hour
5-7 hours
4: Advanced Security
Week 5-8
15-20 hours
2 hours
13-18 hours
Effort Breakdown
Total Effort: ~35-45 hours over 8 weeks
Human effort: ~8 hours (18-23%)
Cove-automated: ~27-37 hours (77-82%)
The majority of implementation work is repetitive infrastructure deployment — exactly what
Temporal workflows excel at. Human time is concentrated in Phase 0 (physical device
access) and decision points (key consolidation, VPN policy, override reviews).
8-Week Visual Timeline
Phase
W1
W2
W3
W4
W5
W6
W7
W8
Phase 0
■■■
Phase 1
■■■
Phase 2
■■■
■■■
Phase 3
■■■
■■■
Phase 4
■■■
■■■
■■■
■■■


CONFIDENTIAL
20
Appendix: How This Connects to the
Master Build Spec (COV-269)
The Master Spec describes 9 layers over 35 days. This security implementation plan runs in
parallel and intersects at every layer:
Master Spec Layer
Status
Security Intersection
Layer 1: Infrastructure
Complete
Phase 1-2 security hardens this
Layer 2: Knowledge &
Memory
Complete
Phase 1 secrets protect FalkorDB/Graphiti credentials
Layer 3: Local AI
Complete
Phase 1 secrets protect Ollama/LiteLLM API keys
Layer 4: Search &
Intelligence
Pending
Phase 2 CrowdSec protects SearXNG
Layer 5: Agent
Orchestration
Pending
Phase 3 SecurityGate embedded in Cove
Layer 6: AI Executive Team
Pending
Phase 3 ensures all agents pass security
Layer 7: Communication
Agents
Pending
Phase 4 P2 tokenization for PII
Layer 8: Psychology Engine
Pending
Phase 3 consent framework (COV-124)
Layer 9: R&D Rubric Engine
Pending
Phase 3 Kaizen security metrics
Integration Principle
Security is not a separate workstream — it is embedded in every layer of the Master Build
Spec. As Cove builds each layer, the SecurityGate activity ensures compliance before
deployment. The Enforcer monitors continuously. The Kaizen loop drives improvement. The
architecture document defines what must be true. This plan defines how Cove makes it
true.


