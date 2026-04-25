---
title: "Beast Security Architecture v2"
id: "beast-security-architecture-v2"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "beast-security-architecture-v2.pdf"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

The Beast
Infrastructure Security Architecture v2.0
Unified Security Framework for Amplified Partners
Beast (Hetzner AX162-R)  ·  Mac Mini  ·  MacBook Air M4  ·  Beelink N150  ·  iPhone 16
14 March 2026
CONFIDENTIAL
Reconciled with Secrets Management v2.0 deployment plan,
Linear project audit (40+ issues), and GitHub infrastructure audit (15 repos)

CONFIDENTIAL
2
Table of Contents
1.
Executive Summary
3
2.
Project Landscape
5
3.
Layer 1: Host & OS Hardening
8
4.
Layer 2: Docker Container Hardening
10
5.
Layer 3: Traefik Reverse Proxy
13
6.
Layer 4: Secret Management (Reconciled with v2.0)
15
7.
Layer 5: Network Security — VPN Mesh
21
8.
Layer 6: Continuous Monitoring
23
9.
Layer 7: Data Protection — P2 Tokenisation
26
10.
Layer 8: Syncthing Security
28
11.
Layer 9: Compliance Framework
29
12.
Layer 10: Endpoint Security
32
13.
SearXNG Status
33
14.
Gap Analysis & Recommendations
34
15.
Implementation Roadmap
37
A.
Appendix A: Complete Linear Issue Map
39
B.
Appendix B: GitHub Repo Security Summary
40
C.
Appendix C: Docker Container Inventory
41
D.
Appendix D: Issues Log
42

CONFIDENTIAL
3
1. Executive Summary
This document presents the reconciled infrastructure security architecture for Amplified Partners
(trading as "The Beast"), consolidating the 10-layer defence-in-depth framework with the Secrets
Management v2.0 deployment plan, a full Linear project audit covering 40+ issues across 9 projects,
and a GitHub infrastructure audit spanning 15 repositories.
Scope
•
5 devices: Beast (Hetzner AX162-R), Mac Mini, MacBook Air M4, Beelink N150, iPhone 16
•
35+ Docker containers on Beast, all on the amplified-net Docker network
•
15 GitHub repositories with 4 docker-compose files, 5 Dockerfiles, 5 .env.example files, 4
Railway configs
•
40+ Linear issues across 9 projects affecting security posture
•
10-layer defence-in-depth from hardware to compliance
Key Findings
CRITICAL: SearXNG is WORKING (curl workaround documented). Notion remains
DISCONNECTED. No Linear issues exist for Vaultwarden, Infisical, WireGuard, NetBird,
CrowdSec, or Wazuh deployment — these are the primary gaps.
Compliance Targets
•
Exceed UK GDPR requirements with tokenisation + encryption + consent framework
•
Exceed HIPAA safeguards via P2 tokenisation of PHI and full audit logging
•
UK Cyber Essentials Plus — MFA mandatory from April 2026 (COV-82 is URGENT)
•
SOC 2 Type II alignment for enterprise client confidence
Layer Readiness Summary
Layer
Component
Status
Readiness
1
Host & OS Hardening
Planned
30%
2
Docker Container Hardening
Partially Done
65%
3
Traefik Reverse Proxy
Deployed, needs hardening
50%
4
Secret Management
NOT DEPLOYED — Critical gap
5%
5
Network Security (VPN)
NOT DEPLOYED
0%

CONFIDENTIAL
4
Layer
Component
Status
Readiness
6
Continuous Monitoring
Enforcer in progress
25%
7
Data Protection (P2)
Research complete
10%
8
Syncthing Security
Deployed, needs hardening
40%
9
Compliance Framework
Framework designed, registration
pending
35%
10
Endpoint Security
Partial (macOS audit pending)
20%
1. Layer readiness percentages are estimates based on Linear issue status and infrastructure audit

CONFIDENTIAL
5
2. Project Landscape
The following analysis is derived from a comprehensive audit of 40+ Linear issues across 9 projects
and 15 GitHub repositories. Every issue with security implications is catalogued below.
Active/Urgent Security Issues
ID
Title
Status
Priority
COV-203
Security & Privacy Enforcer: UK GDPR + ICO + AI Act
Backlog
1 Urgent
COV-82
Enable MFA on all cloud services
Todo
1 Urgent
COV-124
Staff Consent and Privacy Model
Todo
1 Urgent
COV-274
Three-layer prompt architecture — security
enforcement
Backlog
1 Urgent
COV-269
MASTER SPEC: 9 Layers, 8 Phases, 35 Days
Backlog
1 Urgent
COV-262
Temporal Worker Container on Beast
Backlog
1 Urgent
COV-170
BLOCKER: Vault not in FalkorDB/GitHub
In Progress
1 Urgent
COV-214
The Enforcer v1.0 — Health & Compliance
In Progress
2 High
COV-83
Verify macOS security for Cyber Essentials
Todo
2 High
COV-87
Register Cyber Essentials self-assessment
Todo
2 High
COV-85
Solicitor review of privacy templates
Todo
2 High
COV-99
Cyber Essentials deep research
In Progress
2 High
COV-215
Base Layer Services — secrets blocker
In Progress
2 High
Completed Security Work
ID
Title
Notes
COV-95
Security & Privacy Framework
8 Huang principles,
MAESTRO-informed
COV-172
Vault pushed to GitHub
5,081 files, sanitised
COV-81
Docker Compose hardening
Read-only, cap-drop,
no-new-privileges, pinned versions
COV-80
Docker container security verification
Complete
COV-77
Python dependency vulnerability scanning
Complete
COV-79
API key rotation policy
Policy defined
COV-75
Cyber Essentials readiness assessment
Complete
COV-74
Client privacy templates
DPA, Privacy Notice, Consent Form
COV-231
SearXNG deployed
Working on Beast

CONFIDENTIAL
6
ID
Title
Notes
COV-244
SearXNG-first search policy
Active policy

CONFIDENTIAL
7
9 Linear Projects (all affect security posture)
The following projects are tracked in Linear. Each has implications for the security architecture,
ranging from infrastructure deployment to governance and compliance.
•
Multi-Team Build Orchestrator
•
Product R&D;
•
Governance & Principles
•
Marketing & Content
•
First Client
•
Product Development
•
Knowledge System
•
Infrastructure
•
Lucy's App
GitHub Infrastructure (15 repos)
•
4 docker-compose files (all in amplified-partners)
•
5 Dockerfiles across 3 repos
•
5 .env.example files across 5 repos
•
4 Railway configs (byker-production, amplified-crm, amplified-partners x2)
•
No Traefik/Vaultwarden/Infisical/SearXNG configs in code — all deployed directly on Beast
•
anthropic-token-proxy (public) — security-relevant API proxy
AUDIT NOTE: Traefik, Vaultwarden, Infisical, and SearXNG configs are NOT in any
repository — they are deployed directly on Beast. Consider adopting a GitOps approach
to ensure all infrastructure configuration is version-controlled and auditable.

CONFIDENTIAL
8
3. Layer 1: Host & OS Hardening
Related Linear Issues: COV-27 (Hetzner server audit, Todo), COV-189 (Hetzner Production
Environment, Todo)
The Beast runs on a Hetzner AX162-R dedicated server. Host-level hardening is the first line of
defence, covering SSH access, firewall configuration, and kernel-level protections.
SSH Hardening
•
Non-standard SSH port to reduce automated scanning noise
•
Ed25519 key-only authentication — disable password authentication entirely
•
Disable root login via SSH (PermitRootLogin no)
•
Deploy Fail2ban with aggressive banning (3 attempts, 24-hour ban)
•
Restrict SSH to specific IP ranges via firewall rules
Firewall Configuration
•
UFW/nftables — whitelist-only approach, deny all inbound by default
•
Hetzner Cloud Firewall — additional network-level firewall as defence in depth
•
Expose only required ports: 80/443 (Traefik), SSH (non-standard port)
•
Egress filtering where practical
Kernel Hardening
•
sysctl hardening: enable ASLR (randomize_va_space=2), SYN cookies, disable ICMP redirects
•
Disable IPv6 if not required
•
Mount /tmp and /var/tmp with noexec,nosuid,nodev
•
Automatic security updates via unattended-upgrades
Recommended sysctl Parameters
Parameter
Value
Purpose
net.ipv4.tcp_syncookies
1
SYN flood protection
net.ipv4.conf.all.accept_redirects
0
Disable ICMP redirects
net.ipv4.conf.all.send_redirects
0
Prevent redirect attacks
kernel.randomize_va_space
2
Full ASLR (Address Space Layout
Randomisation)
net.ipv4.icmp_echo_ignore_broadcasts
1
Prevent Smurf attacks
net.ipv4.conf.all.rp_filter
1
Reverse path filtering
fs.suid_dumpable
0
Disable core dumps for SUID binaries

CONFIDENTIAL
9
Parameter
Value
Purpose
kernel.dmesg_restrict
1
Restrict dmesg access
Automatic Security Updates
•
unattended-upgrades — automatic installation of security patches
•
Configure to install security updates only (not all updates) for stability
•
Enable email notifications for applied updates
•
Schedule reboot window for kernel updates (e.g. Sunday 03:00 UTC)
1. Hetzner Dedicated Server Security Guide, https://danieltenner.com/2017/02/01/the-hetzner-survival-guide/
2. Hetzner Community: nftables Configuration, https://community.hetzner.com/tutorials/linux-setup-gre-tunnel

CONFIDENTIAL
10
4. Layer 2: Docker Container Hardening
Related Linear Issues: COV-81 (Done), COV-80 (Done), COV-254 (Finance Engine deployed),
COV-233 (OpenClaw deployed)
Current state: 35 containers running on Beast via the amplified-net Docker network. Docker Compose
hardening (COV-81) has been completed, establishing read-only root filesystems, capability dropping,
no-new-privileges, and pinned image versions.
Runtime Security
•
Run all containers as non-root users
•
Drop ALL capabilities and add back only what is needed (cap_drop: ALL, cap_add: [specific])
•
--no-new-privileges flag on every container
•
Read-only root filesystem with tmpfs mounts for /tmp where needed
•
Resource limits: memory limits, CPU quotas, PIDs limits to prevent fork bombs
Linux Security Modules
•
AppArmor profiles — custom profiles per container workload
•
Seccomp profiles — restrict system calls to minimum required set
•
Default Docker seccomp profile blocks 44+ dangerous syscalls
Network Isolation
•
Isolated frontend/backend Docker networks
•
Internal networks for database containers (no external access)
•
Never use --network host
•
Traefik as sole ingress point for HTTP/HTTPS traffic
Image Security
•
Trivy scanning — scan all images before deployment and on daily schedule
•
Use minimal base images (Alpine, distroless, slim variants)
•
Pin image versions — never use :latest in production
•
Enable Docker Content Trust (DCT) for signed images where available
1. Appsecco: Docker Security Best Practices, https://blog.appsecco.com/a-practical-guide-to-writing-secure-dockerfiles-bf561224dd80
2. InfoSec Write-ups: Docker Hardening,
https://infosecwriteups.com/docker-security-best-practices-a-complete-guide-to-securing-your-containers-f56657e0e596

CONFIDENTIAL
11
Docker Compose Hardening (Completed)
The following hardening measures were implemented as part of COV-81. All 35 containers on Beast
have been updated to comply with these standards.
Control
Implementation
Status
Read-only rootfs
read_only: true + tmpfs: /tmp
Done
Capability
dropping
cap_drop: [ALL]
Done
No new privileges
security_opt: [no-new-privileges:true]
Done
Pinned versions
All images use specific version tags
Done
Memory limits
mem_limit per container
Done
Health checks
HEALTHCHECK in Dockerfile or compose
Partial
Non-root users
USER directive in Dockerfile
Partial
Network isolation
Separate frontend/backend networks
Planned

CONFIDENTIAL
12
5. Layer 3: Traefik Reverse Proxy
Related Linear Issues: COV-229 (DNS wildcard, Done), COV-215 (Base layer services, In Progress)
Traefik serves as the single ingress point for all HTTP/HTTPS traffic to Beast. All services are exposed
via *.beast.amplifiedpartners.ai subdomains with automatic TLS certificate management through Let's
Encrypt.
TLS Configuration
•
TLS 1.2+ only — disable TLS 1.0 and 1.1
•
HSTS (HTTP Strict Transport Security) with max-age of 1 year and includeSubDomains
•
Let's Encrypt automatic certificate provisioning and renewal
•
Check for CVE-2025-66491 — Traefik vulnerability assessment needed
Security Headers Middleware
Header
Value
Purpose
Content-Security-Poli
cy
default-src 'self'; script-src 'self'
XSS prevention
X-Frame-Options
DENY
Clickjacking prevention
X-Content-Type-Opti
ons
nosniff
MIME-type sniffing prevention
Referrer-Policy
strict-origin-when-cross-origin
Referrer leakage prevention
Permissions-Policy
camera=(), microphone=(), geolocation=()
Feature restriction
X-XSS-Protection
1; mode=block
Legacy XSS filter
Additional Security Measures
•
Rate limiting — per-IP rate limits to prevent brute force and DDoS
•
IP whitelisting for admin endpoints (Traefik dashboard, Vaultwarden admin)
•
CrowdSec bouncer plugin — collaborative threat intelligence (see Layer 6)
•
Authentik/IdP integration for Single Sign-On (SSO) across services
1. xfuture-blog: Traefik Security Headers, https://xfuture-blog.de/traefik-security-headers/
2. Matt Dyson: CrowdSec + Traefik Integration, https://mattdyson.org/blog/2022/07/crowdsec-with-traefik/

CONFIDENTIAL
13
6. Layer 4: Secret Management
RECONCILED WITH SECRETS MANAGEMENT v2.0
Related Linear Issues: COV-215 (Secrets blocker, In Progress), COV-172 (Vault sanitised, Done),
COV-79 (API key rotation policy, Done)
This section integrates the detailed Vaultwarden + Infisical deployment plan from the Secrets
Management v2.0 document. It represents the most critical infrastructure gap in the current
architecture — secrets are scattered across 5 .env files on 2 machines, with duplicated keys, zero
access logging, no rotation, and no encryption at rest.
CRITICAL: Two different Anthropic API keys and two different OpenAI API keys exist
across .env files. There is no secret versioning, no audit trail, and no access control. This
is the single highest-risk gap in the entire infrastructure.
Current State: .env Audit
A comprehensive audit of all .env files reveals the following distribution of secrets across the
infrastructure:
Location
Contents
Risk
Mac Mini
/agent-stack/.env
Anthropic, OpenAI, xAI, GitHub PAT,
Telegram, Twilio, Railway DB
Plaintext on disk
Mac Mini
/amplified-unified/.env
DIFFERENT Anthropic key, DIFFERENT
OpenAI key
Two competing keys
Mac Mini ~/.env
Empty placeholder
Confusing
Beast /opt/backups/agent-
stack/.env
Copy of Mac keys + FalkorDB IP
Plaintext backup
Beast
cove-orchestrator/.env
GitHub PAT, Telegram, Cove API key
Yet another .env
SSH authorized_keys
6 entries (1 duplicate)
No rotation/audit

CONFIDENTIAL
14
Layer 4A: Vaultwarden (Human Passwords + Passkeys)
Vaultwarden is a lightweight, self-hosted Bitwarden-compatible server that will manage all
human-facing credentials, including passwords, TOTP seeds, and passkeys (WebAuthn PRF) for
biometric authentication across all devices.
Parameter
Value
Image
vaultwarden/server:latest
RAM
~50 MB
URL
vault.beast.amplifiedpartners.ai
Passkey Support
WebAuthn PRF — biometric on all devices
Authentication
Touch ID (Mac), Face ID (iPhone), Windows Hello (Beelink)
Signups
Disabled after initial account creation
Admin Panel
ADMIN_TOKEN secured, IP-restricted
Brute Force
Fail2ban integration
Per-Device Setup
Device
Client
Passkey Method
Mac Mini
Homebrew (brew install bitwarden-cli)
Touch ID
MacBook Air M4
Homebrew (brew install bitwarden-cli)
Touch ID
Beelink N150
Download from bitwarden.com
Windows Hello
iPhone 16
App Store (Bitwarden)
Face ID
4 registered passkeys, one per device. All biometric-enabled.
Layer 4B: Infisical (Machine Secrets)
Infisical is a self-hosted secrets management platform designed for machine-to-machine
authentication. Docker containers authenticate via Universal Auth (Client ID/Secret) and receive
short-lived tokens, eliminating the need for long-lived .env files.
Parameter
Value
Image
infisical/infisical:latest-postgres
URL
secrets.beast.amplifiedpartners.ai
Backing Services
PostgreSQL 16 + Redis 7
RAM (total)
~484 MB (256 app + 128 Postgres + 50 Redis + 50 Vaultwarden)
Auth Method
Universal Auth (Client ID/Secret → short-lived tokens)
CLI
Mac Mini (brew), MacBook Air (brew), Beelink (scoop)
iOS
Web dashboard for emergencies (no app needed)
Features
Secret versioning, audit trail, environment separation

CONFIDENTIAL
15
Secrets Inventory to Migrate
The following table catalogues every secret that must be migrated from .env files to Infisical.
Duplicate keys must be consolidated to a single canonical value.
Secret
Current Location
Infisical Project
ANTHROPIC_API_KEY
2 .env files (2 different keys!)
amplified-core / production
OPENAI_API_KEY
2 .env files (2 different keys!)
amplified-core / production
XAI_API_KEY
agent-stack .env
amplified-core / production
GITHUB_PAT
agent-stack + cove .env
amplified-core / production
TELEGRAM_BOT_TOKE
N
agent-stack + cove .env
amplified-core / production
TWILIO_ACCOUNT_SID
agent-stack .env
amplified-core / production
TWILIO_AUTH_TOKEN
agent-stack .env
amplified-core / production
DATABASE_URL
agent-stack .env
amplified-core / production
COVE_API_KEY
cove .env
cove-orchestrator / production
VAULTWARDEN_ADMI
N
(new — to be generated)
infrastructure / production
Bootstrap Problem (Critical)
THE SECRET ZERO PROBLEM: Four bootstrap secrets cannot be stored in the system
they protect. These must be stored at /opt/amplified/.bootstrap-secrets (chmod 600,
root-only) and backed up to an encrypted USB drive plus a printed copy in a physical
safe or solicitor's office. They must NEVER appear on GitHub, in any .env file, or in any
Docker image.
Secret
Purpose
Storage
INFISICAL_ENCRYPTION_
KEY
Encrypts Infisical database
/opt/amplified/.bootstrap-secrets
INFISICAL_AUTH_SECRET
JWT signing for Infisical
/opt/amplified/.bootstrap-secrets
INFISICAL_DB_PASSWORD
PostgreSQL access
/opt/amplified/.bootstrap-secrets
VAULTWARDEN_ADMIN_T
OKEN
Vaultwarden admin panel
/opt/amplified/.bootstrap-secrets

CONFIDENTIAL
16
5-Phase Migration Plan
The following phased migration plan was designed to minimise downtime and ensure no secret is lost
during the transition. Total estimated time: 4-5 hours.
Phase
Description
Time
Details
1
Vaultwarden
45 min
Deploy on Beast, set up 4 client devices + 4 passkeys
2
Infisical
30 min
Deploy on Beast, install CLI on 3 dev machines
3
Consolidate
1 hour
Pick canonical keys, revoke duplicates, add all to Infisical
4
Migrate
Docker
2-3 hours
Add Infisical to ~29 containers, remove .env refs
5
Clean Up
30 min
Delete all .env files, add .env.reference, git-secrets install
Resource Impact on Beast
Service
RAM
CPU
Disk
Vaultwarden
~50 MB
Negligible
~100 MB
Infisical (app)
~256 MB
Low
~500 MB
Infisical Postgres
~128 MB
Low
~200 MB
Infisical Redis
~50 MB
Negligible
~50 MB
Total
~484 MB
Minimal
~850 MB
NOT YET IN LINEAR: The following issues need to be created: Vaultwarden deployment,
Infisical deployment, Secret key consolidation/rotation, Docker container migration to
Infisical, .env cleanup, Bootstrap secrets secure storage.
Docker Container Integration Pattern
Each of the ~29 Docker containers that currently read from .env files must be migrated to use the
Infisical SDK or CLI. The recommended integration pattern uses Infisical's init-container approach:
•
Step 1: Create an Infisical Machine Identity for each container (or group of related containers)
•
Step 2: Configure Universal Auth credentials (Client ID + Client Secret) as environment
variables
•
Step 3: Use infisical run as the container entrypoint to inject secrets at runtime
•
Step 4: Remove all .env file references from docker-compose.yml
•
Step 5: Create .env.reference files documenting expected variables (without values)
Post-Migration Verification

CONFIDENTIAL
17
•
Verify all containers start successfully without .env files
•
Confirm Infisical audit log shows access from each container identity
•
Test secret rotation by changing one key and verifying propagation
•
Run git-secrets scan across all repositories to catch any remaining plaintext secrets
•
Delete all .env files from disk and from any backups
1. Infisical: Solving the Secret Zero Problem, https://infisical.com/blog/solving-secret-zero-problem
2. Infisical: Self-Hosting for Homelab, https://infisical.com/blog/self-hosting-infisical-homelab
3. Vaultwarden GitHub Repository, https://github.com/dani-garcia/vaultwarden

CONFIDENTIAL
18
7. Layer 5: Network Security — VPN Mesh
Related Linear Issues: None — not tracked yet. New issues must be created.
A VPN mesh network is essential for securing inter-device communication and enabling zero-trust
network access (ZTNA). NetBird is recommended over Headscale/Tailscale for its self-hosting
capability, open-source licence, and integration with SSO/MFA providers.
NetBird (Recommended)
•
WireGuard-based mesh VPN — peer-to-peer encrypted tunnels between all devices
•
Self-hostable management server on Beast
•
ZTNA — zero-trust network access with per-connection authentication
•
SSO/MFA integration — connects to Authentik or other IdP for authentication
•
Device posture checks — verify device compliance before granting access
•
Cross-platform: Linux (Beast), macOS (Mac Mini, MacBook Air), Windows (Beelink), iOS
(iPhone 16)
Why NetBird over Alternatives
Feature
NetBird
Headscale/Tailscale
WireGuard (raw)
Self-hosted
Yes (fully)
Headscale only
Yes
Management UI
Yes
Limited
None
SSO/MFA
Native
Plugin
Manual
Device posture
Yes
No
No
Ease of setup
Medium
Medium
Complex
Open source
Yes (BSD-3)
Yes
Yes (GPL)
Current stance (from Secrets Management v2.0): "No VPN required [currently]. For future
lockdown, add Tailscale/WireGuard and switch DNS to internal IPs." This document recommends
deploying NetBird as part of Phase 2 (Week 3-4) to establish the mesh before hardening Traefik
access controls.
Device Enrollment Plan
Device
OS
NetBird Client
Network Role
Beast (AX162-R)
Debian/Ubu
ntu
apt / Docker
Hub — management server +
peer
Mac Mini
macOS
brew install netbird
Peer — development
workstation
MacBook Air M4
macOS
brew install netbird
Peer — mobile development

CONFIDENTIAL
19
Device
OS
NetBird Client
Network Role
Beelink N150
Windows 11
MSI installer / scoop
Peer — secondary
workstation
iPhone 16
iOS 19
App Store (NetBird)
Peer — mobile access
1. NetBird Documentation, https://docs.netbird.io/

CONFIDENTIAL
20
8. Layer 6: Continuous Monitoring
Related Linear Issues: COV-214 (Enforcer v1.0, In Progress), COV-203 (Security Enforcer, Backlog)
Wazuh SIEM/XDR
Wazuh provides unified security monitoring across all devices and containers. It combines SIEM
(security information and event management), XDR (extended detection and response), file integrity
monitoring, vulnerability detection, and compliance auditing in a single platform.
•
Agent on every device — Beast, Mac Mini, MacBook Air, Beelink, iPhone (via syslog)
•
Docker listener — monitor container events, image pulls, configuration changes
•
File Integrity Monitoring (FIM) — detect unauthorised changes to critical files
•
Vulnerability detection — continuous CVE scanning across all hosts
•
Compliance monitoring — GDPR, HIPAA, PCI-DSS, CIS benchmark checks
CrowdSec
•
Traefik bouncer plugin — automatically block known malicious IPs at the reverse proxy
•
Collaborative IP reputation — community-shared threat intelligence
•
Parses access logs in real time to detect brute force, scanning, and application attacks
Vulnerability Scanning
Tool
Target
Frequency
Integration
Trivy
Docker images
Daily + pre-deploy
CI/CD pipeline
OpenVAS/GV
M
Network hosts
Weekly
Wazuh dashboard
Gitleaks
Git repositories
Pre-commit + CI
GitHub Actions

CONFIDENTIAL
21
AI Security Agent ("Sentinel")
A future-state LLM-powered security agent that will consume data from Wazuh, CrowdSec, and Trivy
to provide automated threat analysis and response recommendations. Integration with Tracecat or
Shuffle SOAR for automated playbooks.
The Enforcer (In Progress)
COV-214 — Already under development. The Enforcer is a Python+FastAPI application providing
continuous health and compliance monitoring:
Metric
Value
Codebase
17 files, ~2,500 lines Python
Framework
FastAPI
Health Checks
5 automated checks
Check Cycle
Every 10 minutes
Metrics
Prometheus-compatible
Status
In Progress
1. Wazuh Documentation, https://documentation.wazuh.com/
2. Trivy Documentation, https://trivy.dev/
3. Matt Dyson: CrowdSec Integration, https://mattdyson.org/blog/2022/07/crowdsec-with-traefik/

CONFIDENTIAL
22
9. Layer 7: Data Protection — P2
Tokenisation
Related Linear Issues: COV-170 (P2 tokenisation IP not in vault, In Progress), COV-171 (Tier 3
federated intelligence with P2), COV-175 (P2 as workstream)
P2 tokenisation is the proprietary data protection layer that replaces personally identifiable information
(PII) with cryptographically random tokens. The original data is stored in a secure token vault, and the
token is used in all downstream processing.
Tokenisation Architecture
•
Vaulted tokenisation — replaces PII with random tokens, mapping stored in secure vault
•
Format-preserving — SSN stays 9 digits, phone numbers stay 10 digits, etc.
•
HashiCorp Vault Transform engine or custom implementation
•
Hybrid approach: tokenise PII + encrypt at rest (AES-256) + TLS 1.2+ in transit
Data Protection Layers
Layer
Mechanism
Scope
At Rest
AES-256 encryption (LUKS on disk, encrypted DB
columns)
All persistent data
In Transit
TLS 1.2+ (Traefik terminates, internal mTLS
planned)
All network traffic
In
Processing
P2 Tokenisation — PII never enters AI models in
raw form
AI pipeline
At Deletion
Cryptographic erasure — destroy token vault keys
Right to erasure compliance
1. Akeyless: Tokenization Guide, https://www.akeyless.io/blog/what-is-tokenization/
2. Hoop.dev: Self-hosted Tokenization, https://hoop.dev/blog/self-hosted-tokenization

CONFIDENTIAL
23
10. Layer 8: Syncthing Security
Syncthing provides peer-to-peer file synchronisation for the Vault (knowledge base) across Beast,
Mac Mini, and MacBook Air. Hardening is required to prevent data leakage via global discovery and
relay servers.
Current Sync Topology
Beast ↔ Mac Mini ↔ MacBook Air — bidirectional sync of the Vault directory. All three devices
maintain a full copy of the knowledge base.
Hardening Measures
•
Untrusted device mode — encrypt data on remote devices, decrypt only locally
•
Folder passwords — additional encryption layer per synced folder
•
Disable global discovery — prevent device IDs from being announced publicly
•
VPN-only sync — once NetBird is deployed, restrict Syncthing to VPN mesh only
•
Disable relaying — prevent data from routing through third-party relay servers
•
Device authentication — manually approve all device connections
1. Syncthing: Untrusted Devices, https://docs.syncthing.net/users/untrusted.html

CONFIDENTIAL
24
11. Layer 9: Compliance Framework
Related Linear Issues: COV-203 (GDPR+ICO+AI Act), COV-87 (Cyber Essentials registration),
COV-85 (Solicitor review), COV-74 (Privacy templates, Done), COV-124 (Staff consent), COV-245 (19
research docs), COV-76 (Cloud services inventory)
UK GDPR — Exceeding Requirements
•
Data minimisation — collect only what is necessary, with explicit purpose limitation
•
Right to erasure — via P2 tokenisation, cryptographic erasure of token vault keys
•
DPIAs (Data Protection Impact Assessments) — required for AI processing of personal data
•
72-hour breach notification — automated detection (Wazuh) + notification pipeline
•
EU data sovereignty — Hetzner Falkenstein data centre (Germany)
HIPAA — Exceeding Safeguards
•
PHI tokenisation — P2 ensures protected health information never enters AI models raw
•
Full audit logging — Wazuh + Infisical audit trails for all access
•
Encryption everywhere — at rest (AES-256), in transit (TLS 1.2+), in processing (tokenisation)
•
Business Associate Agreements (BAAs) — template prepared (COV-74)
UK Cyber Essentials Plus
CRITICAL DEADLINE: MFA becomes mandatory with NO EXCEPTIONS from April 2026.
COV-82 (Enable MFA on all cloud services) must be completed immediately — estimated
effort is only 30 minutes with an authenticator app. Additionally, COV-87 (Register Cyber
Essentials) should be completed before 28 April 2026 to use the v3.2 requirements.
Control
Requirement
Current Status
1. Firewalls
Boundary firewalls and internet gateways
Hetzner firewall + UFW planned
2. Secure
Configuration
Remove unnecessary software, change
defaults
Docker hardening done, OS pending
3. User Access
Control
Restrict admin access, MFA
COV-82 — MFA NOT DONE
4. Malware
Protection
Anti-malware on all devices
macOS XProtect, Linux planned
5. Patch
Management
Apply patches within 14 days
Unattended-upgrades planned

CONFIDENTIAL
25
Compliance Readiness Matrix
The following matrix maps each compliance framework to the architecture layers that support it,
providing a traceability view for auditors and board review.
Framework
Key Requirement
Architecture Layer
Status
UK GDPR Art.
5
Data minimisation & purpose
limitation
L7 (P2 Tokenisation)
Research
complete
UK GDPR Art.
17
Right to erasure
L7 (Cryptographic erasure)
Planned
UK GDPR Art.
32
Security of processing
L1-L10 (all layers)
In progress
UK GDPR Art.
33
72-hour breach notification
L6 (Wazuh + alerting)
Planned
UK GDPR Art.
35
Data Protection Impact
Assessment
L9 (Governance)
Planned
HIPAA
§164.312
Access controls + audit logging
L4 (Infisical) + L6 (Wazuh)
Planned
HIPAA
§164.312
Encryption at rest and in transit
L1 (LUKS) + L3 (TLS)
Partial
CE Control 1
Boundary firewalls
L1 (UFW + Hetzner FW)
Planned
CE Control 2
Secure configuration
L1 + L2 (Docker hardening)
65%
CE Control 3
User access control + MFA
L4 (Vaultwarden) + MFA
COV-82
pending
CE Control 4
Malware protection
L10 (XProtect, AppArmor)
Partial
CE Control 5
Patch management
L1 (unattended-upgrades)
Planned
SOC 2 CC6
Logical & physical access
L4 + L5 + L10
Planned
SOC 2 CC7
System operations monitoring
L6 (Wazuh + Enforcer)
In progress
AI Act Art. 9
Risk management for AI systems
COV-274 + L7
Backlog
SOC 2 Type II Alignment
While formal SOC 2 certification is not immediately planned, the architecture is designed to align with
SOC 2 Trust Services Criteria (security, availability, confidentiality, processing integrity, privacy). The
combination of Wazuh monitoring, Infisical audit trails, and the compliance framework positions
Amplified Partners for future certification if required by enterprise clients.
1. NCSC: Cyber Essentials Requirements, https://www.ncsc.gov.uk/cyberessentials/overview
2. Cyber Compliance: CE Plus Requirements, https://www.cybercompliance.org.uk/cyber-essentials-plus
3. Secureframe: SOC 2 Compliance, https://secureframe.com/hub/soc-2/what-is-soc-2

CONFIDENTIAL
26
12. Layer 10: Endpoint Security
Related Linear Issues: COV-83 (macOS settings, Todo), COV-84 (Router admin password), COV-86
(Separate admin account)
Mac Mini & MacBook Air M4
•
FileVault — full-disk encryption (AES-XTS-128)
•
Gatekeeper — only allow signed applications
•
XProtect — built-in malware detection
•
Wazuh agent — endpoint detection and response
•
NetBird — VPN mesh client
•
Bitwarden — Vaultwarden client with Touch ID passkey
Beelink N150
•
LUKS encryption — full-disk encryption on Linux
•
Wazuh agent — endpoint detection and response
•
NetBird — VPN mesh client
•
AppArmor — mandatory access control
iPhone 16
•
iOS security — hardware Secure Enclave, Data Protection encryption
•
Bitwarden app — Vaultwarden client with Face ID passkey
•
NetBird mobile — VPN mesh client
•
Automatic iOS updates enabled

CONFIDENTIAL
27
13. SearXNG Status
FIXED — Working correctly as of 14 March 2026
Related Linear Issues: COV-231 (Deployed, Done), COV-244 (SearXNG-first policy, Done)
•
JSON API endpoint confirmed working: HTTP 200, valid JSON response
•
Issue identified: Perplexity Computer's fetch_url tool returns 403/errors — this is a tool-level
issue, NOT a SearXNG problem
•
Workaround: Use bash with curl instead of fetch_url for SearXNG queries
•
beast-searxng skill updated with the curl workaround documentation
•
Version: 2026.3.12+3d3a78f3a

CONFIDENTIAL
28
14. Gap Analysis & Recommendations
This section identifies the critical gaps between the designed architecture and the current state of
deployment. Each gap is prioritised by risk level and effort required to remediate.
Critical Gaps (Not in Linear)
HIGHEST RISK: The following critical infrastructure components have NO corresponding
Linear issues. They must be created and scheduled immediately.
#
Gap
Risk Level
Effort
Impact
1
Vaultwarden deployment — no issue
exists
Critical
45 min
Human credential
security
2
Infisical deployment — no issue exists
Critical
30 min
Machine secret
management
3
WireGuard/NetBird VPN mesh — no
issue exists
High
2-3 hours
Network zero-trust
4
CrowdSec threat intelligence — no
issue exists
High
1-2 hours
Automated threat
blocking
5
Wazuh SIEM/XDR — no issue exists
High
3-4 hours
Unified monitoring
6
Secret key rotation (10 exposed keys)
Critical
1 hour
Active credential
exposure
Exposed keys requiring immediate rotation: Anthropic API Key (x2), OpenAI API Key (x2), xAI API
Key, GitHub PAT, Telegram Bot Token, Twilio SID + Auth Token, Railway DB URL, Cove API Key.
Risk Scoring Summary
The following risk scores are derived from a combination of likelihood (L), impact (I), and current
mitigation level (M). Score = L × I × (1 - M), where each factor is rated 1-5.
Risk Area
Likelihoo
d
Impact
Mitigatio
n
Score
Rating
Plaintext secrets in .env files
5
5
0%
25.0
Critical
Duplicate API keys (drift)
4
4
0%
16.0
Critical
No MFA on cloud services
4
5
0%
20.0
Critical
No VPN mesh (exposed
services)
3
4
20%
9.6
High
No SIEM/monitoring
3
5
10%
13.5
Critical
No CrowdSec (no IDS/IPS)
3
3
0%
9.0
High
Unversioned infra configs
2
4
0%
8.0
High

CONFIDENTIAL
29
Risk Area
Likelihoo
d
Impact
Mitigatio
n
Score
Rating
Syncthing global discovery
2
3
40%
3.6
Medium

CONFIDENTIAL
30
Urgent Human Actions Required
The following actions require human intervention and cannot be automated. They are ordered by
urgency and deadline.
#
Action
Linear
Issue
Effort
Deadline
1
Enable MFA on ALL cloud services
COV-82
30 min
Before April 2026
2
Verify macOS security settings
COV-83
15
min/device
This week
3
Change router admin password,
disable UPnP
COV-84
10 min
This week
4
Register for Cyber Essentials
COV-87
30 min
Before 28 April 2026
5
Solicitor review of
DPA/Privacy/Consent templates
COV-85
External
Week 2-3
6
Connect Notion to enable full
project visibility
N/A
5 min
Immediate
Recommended Linear Issues to Create
The following new Linear issues should be created in the Infrastructure project. Each represents a gap
between the designed architecture and current deployment state.
Proposed Title
Priority
Project
Est. Effort
Deploy Vaultwarden on Beast
Urgent
Infrastructure
45 min
Deploy Infisical on Beast
Urgent
Infrastructure
30 min
Consolidate and rotate all exposed API keys
Urgent
Infrastructure
1 hour
Migrate 29 Docker containers to Infisical
High
Infrastructure
2-3 hours
Deploy NetBird VPN mesh across 5 devices
High
Infrastructure
2-3 hours
Deploy CrowdSec + Traefik bouncer
High
Infrastructure
1-2 hours
Deploy Wazuh SIEM with agents on all
devices
High
Infrastructure
3-4 hours
Build Sentinel AI security agent
Medium
Product R&D;
1-2 weeks
Implement P2 tokenisation for PII
Medium
Product R&D;
1-2 weeks
Harden Syncthing: disable global discovery,
VPN-only
Medium
Infrastructure
30 min

CONFIDENTIAL
31
15. Implementation Roadmap
The following roadmap provides a phased approach to closing all identified security gaps. Each phase
builds on the previous, ensuring that foundational elements (secrets, credentials) are in place before
advanced capabilities (monitoring, AI security) are deployed.
Phase 0: Immediate (This Week)
HUMAN ACTION REQUIRED — These items cannot wait and require direct human
intervention. Total estimated time: 90 minutes.
Task
Owner
Time
Linear Issue
Enable MFA on all cloud services
HUMAN
30 min
COV-82
Rotate all exposed API keys
HUMAN +
AUTOMATED
30 min
New issue
needed
Verify macOS settings
HUMAN
15 min
COV-83
Change router admin password
HUMAN
10 min
COV-84
Phase 1: Foundation (Week 1-2)
Task
Time
Dependencies
Deploy Vaultwarden on Beast
45 min
Traefik DNS, Docker
Deploy Infisical on Beast
30 min
Traefik DNS, Postgres, Redis
Consolidate API keys
1 hour
Infisical running
Migrate Docker containers to Infisical
2-3 hours
All keys in Infisical
Clean up .env files
30 min
All containers migrated
Install git-secrets on all repos
30 min
None
Phase 2: Network & Monitoring (Week 3-4)
Task
Time
Dependencies
Deploy NetBird VPN mesh
2-3 hours
Phase 1 complete
Deploy CrowdSec + Traefik bouncer
1-2 hours
Traefik running
Deploy Wazuh SIEM with agents
3-4 hours
All devices accessible
Harden Traefik (TLS, headers, rate limiting)
1-2 hours
CrowdSec running
Harden Syncthing (VPN-only)
30 min
NetBird deployed

CONFIDENTIAL
32
Phase 3: Advanced Security (Week 5-8)
Task
Time
Dependencies
Build Sentinel AI security agent
1-2 weeks
Wazuh + CrowdSec + Trivy
Implement P2 tokenisation
1-2 weeks
Secret management in place
Complete Cyber Essentials self-assessment
2-4 hours
All controls implemented
SOC 2 Type II alignment work
Ongoing
All monitoring in place
Register Cyber Essentials
30 min
COV-87 — before 28 April
Timeline Summary
Week
Phase
Key Milestone
0 (Now)
Phase 0: Immediate
MFA enabled, keys rotated, macOS verified
1-2
Phase 1: Foundation
Vaultwarden + Infisical deployed, .env
eliminated
3-4
Phase 2: Network & Monitoring
VPN mesh, SIEM, IDS all operational
5-8
Phase 3: Advanced
AI security, tokenisation, Cyber Essentials
registered
8+
Ongoing
SOC 2 alignment, continuous improvement

CONFIDENTIAL
33
Appendix A: Complete Linear Issue Map
The following table maps each architecture layer to its relevant Linear issues, providing a complete
traceability matrix between the security architecture and project management.
Layer
Issue ID
Title
Status
Priority
1 Host
COV-27
Hetzner server audit
Todo
Medium
1 Host
COV-189
Hetzner Production Environment
Todo
Medium
2 Docker
COV-81
Docker Compose hardening
Done
High
2 Docker
COV-80
Docker container security
Done
High
2 Docker
COV-254
Finance Engine deployed
Done
Medium
2 Docker
COV-233
OpenClaw deployed
Done
Medium
3 Traefik
COV-229
DNS wildcard
Done
High
3 Traefik
COV-215
Base Layer Services
In Progress
High
4 Secrets
COV-215
Secrets blocker
In Progress
High
4 Secrets
COV-172
Vault sanitised
Done
High
4 Secrets
COV-79
API key rotation policy
Done
High
6 Monitori
ng
COV-214
The Enforcer v1.0
In Progress
High
6 Monitori
ng
COV-203
Security Enforcer
Backlog
Urgent
7 Data
COV-170
P2 tokenisation IP
In Progress
Urgent
7 Data
COV-171
Tier 3 federated intelligence
Backlog
Medium
7 Data
COV-175
P2 as workstream
Backlog
Medium
9 Complia
nce
COV-203
GDPR+ICO+AI Act
Backlog
Urgent
9 Complia
nce
COV-87
Cyber Essentials registration
Todo
High
9 Complia
nce
COV-85
Solicitor review
Todo
High
9 Complia
nce
COV-74
Privacy templates
Done
High
9 Complia
nce
COV-124
Staff consent
Todo
Urgent
9 Complia
nce
COV-82
Enable MFA
Todo
Urgent
10
Endpoint
COV-83
macOS security
Todo
High
10
Endpoint
COV-84
Router admin password
Todo
High

CONFIDENTIAL
34
Layer
Issue ID
Title
Status
Priority
10
Endpoint
COV-86
Separate admin account
Todo
High

CONFIDENTIAL
35
Appendix B: GitHub Repo Security
Summary
Security-relevant configuration across all 15 GitHub repositories in the Amplified Partners
organisation.
Repository
Visibility
.env.exampl
e
Docker
Railway
amplified-partners
Private
Yes
2 compose
files
2 configs
byker-production
Private
Yes
1 compose file
1 config
amplified-crm
Private
Yes
1 compose file
1 config
cove-orchestrator
Private
Yes
1 Dockerfile
No
agent-stack
Private
Yes
2 Dockerfiles
No
anthropic-token-proxy
Public
No
1 Dockerfile
No
amplified-unified
Private
No
1 Dockerfile
No
knowledge-system
Private
No
No
No
vault
Private
No
No
No
lucy-app
Private
No
No
No
marketing-site
Private
No
No
No
governance-docs
Private
No
No
No
product-rnd
Private
No
No
No
design-system
Private
No
No
No
internal-tools
Private
No
No
No
NOTE: anthropic-token-proxy is the only public repository. It is a security-relevant API
proxy and should be audited for hardcoded credentials, rate limiting, and input validation.
Traefik, Vaultwarden, Infisical, and SearXNG configs exist only on Beast — not in any
repository. A GitOps migration is recommended.

CONFIDENTIAL
36
Appendix C: Docker Container Inventory
35 containers on Beast — all connected via the amplified-net Docker network with Traefik as the
reverse proxy ingress point.
Category
Services
Count
Search
SearXNG
1
AI/ML
Ollama, OpenClaw
2
Finance
Finance Engine
1
Database
FalkorDB, PostgreSQL (multiple), Redis (multiple), Qdrant
6+
Orchestration
Temporal (server + workers)
3
Infrastructure
Traefik, Syncthing, Portainer
3
Application
Cove Orchestrator, Agent Stack, CRM services
8+
Monitoring
The Enforcer (planned: Wazuh, CrowdSec)
1+
Secrets
(planned)
Vaultwarden, Infisical, Infisical-Postgres, Infisical-Redis
0
(planned:
4)
Other
Various support containers
~10

CONFIDENTIAL
37
Appendix D: Issues Log
Known issues, workarounds, and audit observations as of 14 March 2026.
1. SearXNG — FIXED
The SearXNG JSON API is confirmed working (HTTP 200, valid JSON response). The issue was with
the fetch_url tool returning 403 errors — this is a tool-level limitation, not a SearXNG problem. The
workaround is to use bash with curl instead of fetch_url. The beast-searxng skill has been updated to
document this workaround.
2. Notion — DISCONNECTED
The Notion integration is disconnected. An authentication link was presented to the user but no
response has been received. Without Notion access, it is impossible to audit Notion pages for
security-relevant content, architecture decisions, or meeting notes.
3. GitOps Gap
Traefik, Vaultwarden, Infisical, and SearXNG configurations exist only on Beast as directly deployed
Docker containers — they are not tracked in any GitHub repository. This creates a disaster recovery
risk: if Beast's disk fails, these configurations would need to be recreated from memory or
documentation. A GitOps approach (storing all infrastructure as code in a private repository) is
strongly recommended.
End of document. This security architecture is a living document and should be updated as infrastructure
changes are made. Next review date: April 2026 (post-Cyber Essentials registration).