---
title: "Jock MD Notes"
id: "jock-md-notes"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "JockMD.md.txt"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

IDENTITY.md
Name (JOCK), role label, team position
~200 chars
Anchor only — 5 lines max
SOUL.md
Who JOCK is — the four pillars, tone, what JOCK never does
~3,000 chars
Principles first, boundaries second, tone third
AGENTS.md
Operating rules — Act/Surface/Park, problem-solving ladder, authority routing, session lifecycle
~8,000 chars
What JOCK does; no personality here
USER.md
Ewan — Architect, AP project goal, UK timezone, communication style (questions ≠ diktats)
~1,500 chars
Static context; personal details in MEMORY.md
TOOLS.md
Environment notes — API base URLs, paths, active tools
~2,000 chars
Where things are; not what JOCK should do
MEMORY.md
Learned patterns over time — start minimal, prune weekly
~500 chars
Promoted from daily logs; no restated rules
HEARTBEAT.md
Periodic task checklist — what to check every 30 min
~500 chars
Reference list only; logic lives in AGENTS.md

Authority routing
Same chain as the clean-build workspace. JOCK's AGENTS.md encodes this directly.
Situation
Route
Condition
Truth / world boundary
→ Ewan
Anything irreversible or that changes what may be treated as true
Inside the frame
→ JOCK acts
Reversible, high confidence, contained — default posture
Stuck after ladder
→ Qwen
Two attempts + research exhausted; park cleanly, handover packet
Novel decision
→ Qwen routes to Ewan
Qwen assesses; if genuinely novel, Ewan decides, Qwen restarts

Config anchors
Security
Gateway bound to localhost
WhatsApp allowFrom locked to Ewan's number
No community skills — audit before any install
Heartbeat
Interval: 30 minutes
Target: WhatsApp (Ewan's number)
lightContext + isolatedSession to control token cost
Token budget
bootstrapMaxChars per file: 18,000
bootstrapTotalMaxChars: 60,000
Monitor with: wc -m ~/.openclaw/workspace/*.md

Security posture
Sources: Kaspersky, Malwarebytes, Microsoft Security Blog, VirusTotal, Snyk ToxicSkills audit. OpenClaw has 92 active security advisories. Posture is not optional.
Supply chain — official VirusTotal partnership
Source: openclaw.ai/blog (Feb 7, 2026) — all ClawHub skills now scanned via VirusTotal Code Insight (Gemini-powered). SHA-256 hash → lookup → full bundle upload → auto-approve / warn / block. Daily re-scans.
What it catches: known malware, trojans, stealers, suspicious behavioral patterns, compromised dependencies, embedded executables
What it does NOT catch: natural language prompt injection, carefully crafted payloads — clean scan ≠ safe
Snyk ToxicSkills: 36.8% of 3,984 ClawHub skills had flaws; 13.4% critical — scanning is one layer, not a gate
JOCK rule: Cursor Marketplace only. No ClawHub. Read every skill file before it runs. No exceptions. Report suspicious behaviour to security@openclaw.ai
Network
Gateway bound to 127.0.0.1 — never exposed to public internet
WhatsApp allowFrom locked to Ewan's E.164 number
Remote access via Tailscale or SSH tunnel only — no open ports
Gateway auth enabled: auth.mode: "token"
Runtime
Least privilege: JOCK has no access to SSH keys, .env files, or production systems
CVE-2026-25253 (RCE) and 91 other advisories — keep OpenClaw and Node updated
Secrets: never in workspace MD files — environment variables only
Advisory vs enforcement: MD files are advisory. Hard limits live in openclaw.json and sandbox config
Operational
HITL gate: JOCK drafts irreversible actions (send, delete, execute) — Ewan approves before they run
Mitiga Labs "silent exfiltration": skills can push your codebase to an attacker's repo. Read before you run.
Monitor: openclaw logs --follow — watch for API cost spikes and unexpected config changes
Reference: SlowMist OpenClaw Security Practice Guide (GitHub — agent-facing hardening)

Clean-build workspace entry
JOCK's role documented in this workspace under 02_build/openclaw/ and indexed in MANIFEST.md as Candidate authority (runnable artefact).
Draft structure — review and confirm before execution
