---
title: "Security Knowledge Base"
id: "security-knowledge-base"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "security-knowledge-base.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Security — Knowledge Base

**Purpose:** Document every problem found, every solution applied, and every workaround discovered during security implementation. This becomes the public knowledge base shared via GitHub and used by Cove agents to help other businesses.

**Rule:** Two tries to fix it yourself, then search (SearXNG on Beast). Document everything either way.

**Started:** 15 March 2026  
**Client Zero:** Ewan's setup (Byker Business Help / Amplified Partners)

---

## Known Gotchas (from Ewan's experience)

### 1. DNS Changes Can Break Wi-Fi Login
**Problem:** A previous AI changed DNS settings to a privacy-focused DNS (like 1.1.1.1 or 9.9.9.9). This broke captive portal Wi-Fi networks (like Apple Store, cafes, hotels) because captive portals rely on the ISP's default DNS to redirect to the login page.
**Impact:** Couldn't connect to Wi-Fi in Apple Store. Even the Apple Store staff couldn't quickly diagnose it.
**Solution:** Don't change DNS on mobile devices or personal laptops. If changing DNS on a router, document how to revert. Better yet: only change DNS on the router level and ensure devices can override if needed.
**Prevention:** Before changing DNS settings, always ask: "Will this affect the user's ability to connect to public Wi-Fi?" If yes, don't do it on personal devices. On business routers, provide a clear one-page "how to revert" guide.

### 2. VPN + Location-Based Security = Phone Lockdown
**Problem:** VPN made the phone appear to be in London when Ewan was in Newcastle. Security monitoring flagged this as suspicious and locked the phone.
**Impact:** Phone repeatedly locked down, major friction.
**Solution:** If using a VPN on a personal device, either: (a) use a VPN server geographically close to the user's actual location, (b) whitelist VPN IP ranges in the security monitoring, or (c) don't enforce VPN on personal devices.
**Prevention:** Never enable location-based security lockdowns on personal devices with VPN. The false positive rate is too high. Location checks are only appropriate on managed corporate devices where VPN is controlled.

### 3. "So Secure You Can't Use It" Principle
**Problem:** Security changes that increase friction beyond what a non-technical user can troubleshoot themselves.
**Solution:** Every security change must pass the "pub test" — if someone is in the pub and can't log into their phone or email, can they fix it themselves within 2 minutes? If not, the change is too aggressive for a personal device.
**Prevention:** Test every change against this scenario before deploying. If in doubt, make it reversible via a simple toggle or provide a printed card with "if something stops working, do this."

---

## Implementation Log

### Session: 15 March 2026 — Initial Discovery Audit

**What was done:**
- DNS audit of bykerbusinesshelp.ai and amplifiedpartners.ai
- Email security check (SPF, DKIM, DMARC)
- SSL certificate verification
- HTTP security headers check
- Beast DNS resolution check

**Findings:**

| Domain | Check | Result | Status |
|--------|-------|--------|--------|
| bykerbusinesshelp.ai | SPF | v=spf1 include:_spf.google.com ~all | GREEN |
| bykerbusinesshelp.ai | DKIM | google selector, 2048-bit RSA | GREEN |
| bykerbusinesshelp.ai | DMARC | p=none, reports to ewan@ | AMBER — needs upgrade to p=reject |
| bykerbusinesshelp.ai | SSL | Sectigo DV, expires Oct 2026 | GREEN |
| bykerbusinesshelp.ai | HSTS | Missing | RED |
| bykerbusinesshelp.ai | Security headers | All 7 missing | RED |
| amplifiedpartners.ai | SPF | NOT PRESENT | RED — urgent |
| amplifiedpartners.ai | DKIM | google selector, 2048-bit RSA | GREEN |
| amplifiedpartners.ai | DMARC | NOT PRESENT | RED — urgent |
| amplifiedpartners.ai | SSL | Let's Encrypt, expires May 2026 | GREEN |
| amplifiedpartners.ai | HSTS | max-age=31536000 | GREEN |
| amplifiedpartners.ai | Security headers | 6 of 7 missing | AMBER |
| beast.amplifiedpartners.ai | DNS A record | 135.181.161.131 | GREEN |
| search.beast.amplifiedpartners.ai | DNS A record | 135.181.161.131 | GREEN |

**Infrastructure confirmed:**
- Both domains on Google Workspace (MX → aspmx.l.google.com)
- Both domains registered at Namecheap (NS → pdns1/pdns2.registrar-servers.com)
- bykerbusinesshelp.ai:
  - IP: 198.177.120.182
  - Server: **LiteSpeed** (Namecheap shared hosting, server705-4.web-hosting.com)
  - Hosting: AS22612 Namecheap, Inc., Amsterdam NL
  - Headers via: `.htaccess` in cPanel
- amplifiedpartners.ai:
  - IP: 75.2.60.5 (AWS Global Accelerator, anycast)
  - Server: **Netlify** (confirmed via response headers)
  - GitHub repo: `ewan-dot/amplified-site` (Vite + React + TypeScript)
  - Build output: `dist/public`
  - No `netlify.toml` or `_headers` file exists yet
  - Headers via: `netlify.toml` at repo root
- Beast: 135.181.161.131 (Hetzner AX162-R)

**Tools used:** Python dnspython library, Python ssl module, Python urllib, curl, ipinfo.io, GitHub CLI

**Problems encountered:**
- dig and nslookup not available in Perplexity sandbox (no DNS tools installed)
- Workaround: Used Python dnspython library (pip install dnspython) — works perfectly
- apt-get install failed due to permission denied — sandbox doesn't allow package installation
- Note for future: Always use Python dnspython for DNS lookups in Perplexity sessions

---

## Fixes Applied

### Session: 15 March 2026 — Implementation Planning (Session 2)

**What was done:**
- Re-verified all DNS/email/header findings (no change from session 1)
- Tested Beast SearXNG connectivity (working, 26 results returned)
- Identified exact hosting providers:
  - bykerbusinesshelp.ai = LiteSpeed on Namecheap shared hosting
  - amplifiedpartners.ai = Netlify (via AWS Global Accelerator)
- Found amplified-site GitHub repo (ewan-dot/amplified-site) — no security headers config yet
- Researched DMARC ramp-up, Namecheap DNS, macOS hardening, Docker hardening via Beast SearXNG
- Built comprehensive implementation runbook (security-implementation-runbook.md)
- Updated this knowledge base with hosting details

**Problems encountered:**
- Cannot SSH to Beast from Perplexity sandbox (isolated environment)
- Cannot access Mac Mini Terminal remotely
- Cannot log into Namecheap (domain owner must do this)
- All fixes documented with exact step-by-step instructions for Ewan

---

## Fixes Applied

_(Updated as fixes are implemented)_

### Fix 001: [PENDING] Add SPF record to amplifiedpartners.ai
**Priority:** URGENT — domain is currently open to email spoofing
**DNS Provider:** Namecheap
**Record to add:** TXT record at @ (root): `v=spf1 include:_spf.google.com ~all`
**Verification:** `python3 -c "import dns.resolver; print([str(r) for r in dns.resolver.resolve('amplifiedpartners.ai', 'TXT')])"`
**Status:** Waiting for Namecheap access

### Fix 002: [PENDING] Add DMARC record to amplifiedpartners.ai
**Priority:** URGENT — no spoofing protection
**DNS Provider:** Namecheap
**Record to add:** TXT record at _dmarc: `v=DMARC1; p=none; rua=mailto:dmarc-reports@amplifiedpartners.ai`
**Verification:** `python3 -c "import dns.resolver; print([str(r) for r in dns.resolver.resolve('_dmarc.amplifiedpartners.ai', 'TXT')])"`
**Ramp-up plan:** p=none (2 weeks) → p=quarantine (2 weeks) → p=reject
**Status:** Waiting for Namecheap access

### Fix 003: [PENDING] Upgrade DMARC on bykerbusinesshelp.ai
**Priority:** Medium — currently monitoring only (p=none), reports going to Ewan's inbox
**Change:** Update rua to dmarc-reports@amplifiedpartners.ai, eventually upgrade p= to reject
**Status:** Waiting for Namecheap access

### Fix 004: [PENDING] Add security headers to both domains
**Priority:** Medium — best practice, not CE-required
**Depends on:** Identifying where each site is hosted and whether we can modify headers
- bykerbusinesshelp.ai: 198.177.120.182 — need to identify hosting provider
- amplifiedpartners.ai: 75.2.60.5 (AWS Global Accelerator) — headers can be added via CloudFront or ALB

### Fix 005: [PENDING] Beast server security audit
**Priority:** High — production infrastructure
**Scope:** SSH config, Docker network isolation, firewall rules, exposed services, secrets management
**Reference:** beast-security-architecture-v2.pdf (37 pages), security-implementation-plan.pdf (20 pages)
**Known gaps from memory:** Vaultwarden, Infisical, NetBird, CrowdSec, Wazuh not yet deployed

### Fix 006: [DONE] Mac Mini device audit & hardening
**Completed:** 15 March 2026, 09:10 GMT
**Device:** Ewan's Mac mini (M4, macOS 26.3.1 — Tahoe)

**Results:**
| Check | Status | Action |
|-------|--------|--------|
| macOS version | 26.3.1 (Tahoe) | Already current ✓ |
| Firewall | Was OFF | FIXED → NOW ON ✓ |
| FileVault | Already ON | No action needed ✓ |
| Auto-updates | Set to all ON | Confirmed ✓ |
| Screen lock | Set to 5 min + immediate password | Confirmed ✓ |
| Gatekeeper | Already ON | No action needed ✓ |
| SIP | Already ON | No action needed ✓ |

**Only fix needed:** Firewall was OFF (Apple's one known weak default). Enabled via `socketfilterfw --setglobalstate on`.
**Everything else was already secure.**
**Log saved:** /Users/amplifiedpartners/Desktop/amplified-security-20260315-091012.txt
**Third-party antivirus:** NOT installed (XProtect is CE-compliant, confirmed by IASME)

---

## macOS Security Research (15 March 2026)

### What macOS Handles Out of the Box
- **XProtect** — signature-based AV, auto-updates silently, CE-compliant (IASME confirmed: https://ce-knowledge-hub.iasme.co.uk/space/CEKH/2577498118)
- **XProtect Remediator** — scans and removes known malware periodically
- **Gatekeeper** — blocks unsigned/unnotarized apps, enabled by default
- **SIP** — prevents system file modification, enabled by default, can't disable without Recovery Mode
- **Notarization** — Apple scans all distributed apps for malware before they run
- **Secure Boot** — Apple Silicon M-series verifies boot chain in hardware
- **App Sandbox** — App Store apps run isolated
- **Rapid Security Responses** — emergency patches delivered automatically
- **TCC (Privacy controls)** — per-app permissions for camera, mic, files

### What macOS Does NOT Enable by Default
- **Firewall** — OFF by default (Apple's one weak default)
- **FileVault** — OFF on most setups (disk encryption)
- **Screen lock timeout** — often >5 minutes
- **Auto-login** — sometimes ON

### Third-Party Antivirus: NOT Needed
- IASME CE Knowledge Hub explicitly states XProtect meets CE requirement A8.1
- NCSC recommends XProtect as baseline; EDR only for enterprise with MDM
- The "66% of Mac users faced threats" stat (Moonlock 2025) includes phishing, scams, data breaches — not just malware
- Real attack vectors: social engineering, pirated software, fake Terminal commands (ClickFix)
- AV-Comparatives 2025: Top third-party AV gets 99.4-100% on known samples — same thing XProtect does
- SE Labs found 0% protection against targeted nation-state attacks — irrelevant threat model for SMBs

### Windows vs Mac: Key Differences for Clients
- Windows needs more work: Defender verification, BitLocker/Device Encryption, SMBv1 disable, PowerShell policy, macro blocking
- Windows 11 Home lacks: BitLocker (only Device Encryption), AppLocker, Group Policy Editor
- Mac firewall OFF by default is the main gap; Windows firewall is ON by default
- 95%+ of ransomware targets Windows. Mac ransomware exists but is extremely rare.
- Windows has larger living-off-the-land attack surface (PowerShell, WMI, WMIC)

### Sources
- IASME CE Knowledge Hub: https://ce-knowledge-hub.iasme.co.uk/space/CEKH/2577498118
- NCSC macOS Guidance: https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides/macos
- NCSC Windows Guidance: https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides/windows
- Pareto Security CE+ Mac: https://paretosecurity.com/blog/mac-cyber-essentials-plus/
- Moonlock 2025 Threat Report: https://moonlock.com/2025-macos-threat-report
- AV-Comparatives Mac Test 2025: https://www.av-comparatives.org/tests/mac-security-test-review-2025/
- SE Labs Mac Myth: https://selabs.uk/blog/the-mac-myth-why-your-ceos-laptop-might-be-the-weakest-link/
- Macworld Antivirus 2026: https://www.macworld.com/article/670537/do-macs-need-antivirus.html
- CE v3.2 Changes: https://cybercompliance.org.uk/blogs/news/cyber-essentials-in-july-2025-what-s-new-why-it-matters-and-how-to-get-certified

---

## Client Security Framework (15 March 2026)

### Research Completed
Full framework built in `/home/user/workspace/client-security-framework.md` based on:

**Breach Data (UK Gov Cyber Security Breaches Survey 2025):**
- 43% of UK businesses experienced a breach or attack in past 12 months
- 85% of those were phishing attacks
- 34% involved email impersonation
- 18% malware, 6% ransomware
- Average cost: £3,400 for micro/small businesses
- 35% of micro-businesses experienced phishing (CloudSEK citing CSSB 2025)
- Source: https://www.gov.uk/government/statistics/cyber-security-breaches-survey-2025

**Cyber Essentials Common Failures (isgovern.com — thousands of assessments):**
1. Unsupported OS/apps (~40% of failures) — Windows 10 EOL Oct 2025, old Office, old router firmware
2. No/outdated patching (~30%) — critical patches not within 14 days, auto-update off
3. Antivirus not running/broken (~15%) — installed but broken for months
4. No firewall (~15%) — especially Mac (off by default)
5. Running as admin instead of standard user (~20%) — especially Mac developers/IT
6. MSPs not checking their work — set-and-forget on Datto etc.
- Source: https://isgovern.com/blog/what-are-the-common-failures-for-cyber-essentials/

**CE Plus Additional Failures (CloudSwitched):**
1. Unpatched third-party apps: Adobe Acrobat, Java, browser extensions
2. Misconfigured routers: default passwords, remote management enabled, unnecessary ports
3. Weak access control: shared accounts, former employees not disabled
4. End-of-life software: Windows 10, Office 2016/2019, old PHP/Python/.NET, WinRAR, Notepad++
5. Cloud services: no MFA, legacy auth protocols, no audit logging (esp M365)
6. Scope errors: excluding mobile devices, remote workers, printers, cloud services
- Source: https://www.cloudswitched.com/blog/common-reasons-fail-cyber-essentials-plus

**Phishing Statistics (AAG-IT, updated Oct 2025):**
- 83-85% of UK businesses that suffered attacks report phishing
- 91% of all cyber attacks begin with a phishing email
- 3.4 billion spam/phishing emails sent daily globally
- Law firms: 80% reported phishing attempts
- 25-44 year-olds most targeted
- Source: https://aag-it.com/the-latest-phishing-statistics/

**Windows 10 End of Life:**
- Support ended 14 October 2025
- Automatic CE failure — unsupported software not permitted
- Sources: https://cyberlab.co.uk/2025/10/21/windows-10-end-of-life-cyber-essentials-plus-impact/ , https://www.periculo.co.uk/cyber-security-blog/windows-10-end-of-support-what-you-need-to-know-to-pass-cyber-essentials

### Top 15 Software Found on UK SMB Computers

| # | Software | Risk Level | Key Check |
|---|----------|-----------|----------|
| 1 | Google Chrome | HIGH | Auto-update ON |
| 2 | Microsoft Edge | HIGH | Auto-update ON |
| 3 | Safari (Mac) | MEDIUM | macOS current |
| 4 | Firefox | HIGH | Auto-update ON |
| 5 | Microsoft 365 / Office | HIGH | Macros off, patched, not EOL |
| 6 | Adobe Acrobat Reader | HIGH | Auto-update ON, JS OFF |
| 7 | Zoom | MEDIUM | Auto-update ON |
| 8 | Slack | LOW | Auto-updates well |
| 9 | Teams | MEDIUM | Patched with M365 |
| 10 | WinRAR | HIGH | v6.24+ (CVE-2023-38831) |
| 11 | 7-Zip | MEDIUM | Keep current |
| 12 | VLC Media Player | MEDIUM | Keep current |
| 13 | CCleaner | HIGH — REMOVE | Supply chain attack 2017 |
| 14 | Xero / QuickBooks | MEDIUM | MFA enabled |
| 15 | Dropbox / OneDrive / GDrive | MEDIUM | MFA enabled |

### Software to Remove
- Windows 10 (EOL Oct 2025)
- Office 2016/2019 (EOL)
- Java Runtime (if unused)
- Flash Player (dead since 2020)
- CCleaner (supply chain risk)
- Old PHP/Python/.NET on laptops

### Framework Artifacts Created
- `client-security-framework.md` — Full framework with priority matrix, pre-loaded software, Mac + Windows scripts
- `amplified-client-audit-mac.sh` — Standalone Mac audit script (replaces amplified-mac-check.sh)
- `amplified-client-audit-windows.ps1` — Standalone Windows audit script
- Both scripts produce a desktop log file with GREEN/AMBER/RED status and percentage summary

---

## Search Results Cache

_(Problems searched on SearXNG and their solutions — to be filled as we encounter issues)_

---

## Hardware Inventory (from memory)

| Device | Type | Notes |
|--------|------|-------|
| The Beast | Hetzner AX162-R, 48-core EPYC, 256GB RAM | Production server, 35+ Docker containers |
| Mac Mini M4 | Primary workstation, £1000 | Ewan's daily driver |
| MacBook Air M4 | Laptop (currently under repair) | |
| Beelink N150 | Always-on mini PC | Transcription, background tasks |
| iPhone 16 | Personal phone | |

---

*This knowledge base will grow with every implementation session. Every problem and solution documented here helps the next business owner avoid the same friction.*
