---
title: "Amplified Security — Master Reference Document"
id: "amplified-security-everything-1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Amplified Security — Master Reference Document
**Date:** 17 March 2026  
**Compiled from:** 6 source documents covering all security research, processes, implementation work, and execution tools.

---

## Document Index

| Part | Source File | What It Covers |
|------|-------------|----------------|
| **Part 1** | client-security-framework.md | Reusable client framework: priority matrix, pre-loaded software knowledge for the top 15 apps found on UK SMB computers, Mac audit script, Windows audit script, cloud services checklist |
| **Part 2** | amplified-security-process.md | Full process sheet: 3-tier client communications, 5 Cyber Essentials controls with gap analysis templates, overnight deployment protocol (Nights 1–3 + passkey rollout), CE self-assessment checklist, security health report template, risk reduction quantification, Client Zero (Ewan's setup), automation targets, common SME IT stacks |
| **Part 3** | security-implementation-runbook.md | The runbook for Client Zero: all 10 fixes with exact commands, verification steps, rollback procedures, and estimated times — covering email security (DNS), security headers (Netlify + LiteSpeed/.htaccess), Mac Mini hardening, Beast server SSH hardening, Docker audit, UFW firewall |
| **Part 4** | security-knowledge-base.md | Knowledge base: known gotchas from Ewan's experience, implementation log (session notes), fixes applied with status, macOS security research, UK breach data and CE failure statistics, top 15 software pre-load, framework research sources |
| **Part 5** | mac-vs-windows-security-reality.md | Deep research: honest Mac vs Windows comparison, what macOS handles out of the box vs what Windows needs, the antivirus question settled, Beelink N150 Windows-specific risks, focused audit scripts for each platform |
| **Part 6** | security-execution-prompt-v2.md | Execution prompt for Perplexity Desktop: paste-ready tasks for Mac Mini check, Beast server audit, Netlify security headers deployment, with exact commands and clear "do NOT do" list |

---

## Table of Contents

1. [Part 1 — Client Security Framework v1.0](#part-1--client-security-framework-v10)
   - Priority Matrix (Tiers 1–3)
   - Pre-Loaded Software Knowledge (Top 15 + Software to Remove)
   - The Framework: How to Run a Client Security Check
   - Mac Audit Script
   - Windows Audit Script
   - Cloud Services Checklist
   - Frictionless Client Communication
2. [Part 2 — Security Process Sheet & Gap Analysis Tool](#part-2--security-process-sheet--gap-analysis-tool)
   - The Three Tiers of Client Communication
   - Security Process Sheet & Gap Analysis (5 CE Controls + Bonus)
   - Implementation Sequence — The Overnight Protocol
   - Cyber Essentials Self-Assessment Checklist
   - Security Health Report Template
   - Risk Reduction Quantification
   - Client Zero — Ewan's Setup
   - Appendices: Automation Targets, Common SME IT Stacks
3. [Part 3 — Security Implementation Runbook (Client Zero)](#part-3--security-implementation-runbook--client-zero)
   - Phase 1: Email Security (Fixes 001–003)
   - Phase 2: Security Headers (Fixes 004–005b)
   - Phase 3: Mac Mini Device Hardening (Fix 006)
   - Phase 4: Beast Server Security (Fixes 007–009)
   - Phase 5: Ongoing Monitoring & CE Preparation (Fix 010)
4. [Part 4 — Security Knowledge Base](#part-4--security-knowledge-base)
   - Known Gotchas
   - Implementation Log
   - Fixes Applied
   - macOS Security Research
   - Client Security Framework Research
   - Hardware Inventory
5. [Part 5 — Mac vs Windows: What Actually Needs Fixing](#part-5--mac-vs-windows-what-actually-needs-fixing)
   - What macOS Already Handles
   - What macOS Does NOT Handle by Default
   - The Antivirus Question (Settled)
   - The Beelink N150 (Windows) — Genuinely Different Story
   - Honest Summary: What to Do, What to Skip, What's Theatre
   - Focused Audit Scripts (Mac + Windows)
6. [Part 6 — Security Execution Prompt v2](#part-6--security-execution-prompt-v2)
   - Rules
   - Task 1: Mac Mini Security Check
   - Task 2: Beast Server Audit
   - Task 3: Netlify Security Headers
   - Task 4: Document What You Found
7. [Standalone Scripts Index](#standalone-scripts-index)

---

# Part 1 — Client Security Framework v1.0

**Purpose:** Reusable framework for securing any Amplified Partners client device. Pre-loaded with knowledge of the top software people actually use, prioritised by highest impact and most common failures.

**Philosophy:** Research first, fix what matters, don't blanket bomb. Low-hanging fruit and highest prize first.

**Created:** 15 March 2026  
**Sources:** UK Gov Cyber Security Breaches Survey 2025, IASME CE Knowledge Hub, isgovern.com CE failures data, CloudSwitched CE+ failures, AMVIA CE checklist 2025, AAG-IT phishing statistics, NCSC device guidance

---

## Priority Matrix: What Catches People Out Most

Ranked by (frequency of failure × impact of breach). Fix these first, in this order.

### TIER 1 — Fix Immediately (85%+ of breaches start here)

| # | Issue | Why It's #1 | % of CE Failures | Fix Time |
|---|-------|-------------|-------------------|----------|
| 1 | **Unsupported / end-of-life software** | CE automatic fail. 95%+ of ransomware targets unpatched Windows. Windows 10 EOL Oct 2025 = instant fail. | ~40% of all CE failures | 5-30 min |
| 2 | **Missing / broken patching** | High/critical patches must be applied within 14 days (CE requirement). Most MSPs set it and forget it. | ~30% of all CE failures | 5-15 min |
| 3 | **No MFA on cloud services** | 85% of breaches involve phishing → stolen credentials. MFA blocks 99.9% of credential attacks. | ~25% of CE+ failures | 5 min per service |
| 4 | **Running as admin (not standard user)** | Malware inherits whatever privilege the user has. Admin = game over. Very common on Macs with tech users. | ~20% of CE failures | 10 min |

### TIER 2 — Fix Same Day (the "forgot about it" category)

| # | Issue | Why It Matters | % of CE Failures | Fix Time |
|---|-------|----------------|-------------------|----------|
| 5 | **Firewall off** | Mac firewall OFF by default (Apple's one weak default). Windows usually ON but can be disabled. | ~15% | 10 sec |
| 6 | **Antivirus not running / broken** | Installed but broken for months is worse than not installed — gives false confidence. | ~15% | 5 min |
| 7 | **Weak passwords (< 8 chars, no MFA bypass)** | CE requires 8+ with MFA or 12+ without. Default router/device passwords = instant fail. | ~15% | 10 min |
| 8 | **Office macros enabled** | CE requires macros disabled unless business-critical. Default-enabled = automatic fail. | ~10% | 2 min |

### TIER 3 — Fix This Week (important but less urgent)

| # | Issue | Why It Matters | % of CE Failures | Fix Time |
|---|-------|----------------|-------------------|----------|
| 9 | **No disk encryption** | FileVault (Mac) or BitLocker/Device Encryption (Windows). Laptop stolen = data breach without it. | ~10% | 2 min + wait |
| 10 | **Screen lock > 15 min or absent** | CE requires ≤15 min (we recommend 5 min). Many default to "never". | ~5% | 10 sec |
| 11 | **Auto-run/auto-play enabled** | USB stick attack vector. Must be disabled. | ~5% | 1 min |
| 12 | **Cloud services misconfigured** | M365/Google Workspace: legacy auth enabled, no audit logging, excessive permissions. | ~10% of CE+ | 15 min |

---

## Pre-Loaded Software Knowledge

### The Top 15 Applications Found on UK Small Business Computers

These are the apps CE assessors most commonly find, and the ones most likely to cause a failure if out of date or misconfigured. The framework scripts check for all of these.

| # | Software | Category | Platform | CE Risk | What to Check |
|---|----------|----------|----------|---------|---------------|
| 1 | **Google Chrome** | Browser | Both | HIGH — must auto-update | Version current, auto-update ON |
| 2 | **Microsoft Edge** | Browser | Windows | HIGH — must auto-update | Version current, auto-update ON |
| 3 | **Safari** | Browser | Mac | MEDIUM — updates with macOS | macOS current = Safari current |
| 4 | **Firefox** | Browser | Both | HIGH — must auto-update | Version current, auto-update ON |
| 5 | **Microsoft 365 / Office** | Productivity | Both | HIGH — macros, patching, EOL | Version supported, macros off, auto-update ON |
| 6 | **Adobe Acrobat Reader** | PDF | Both | HIGH — common exploit target | Version current, auto-update ON, JavaScript OFF |
| 7 | **Zoom** | Communication | Both | MEDIUM — frequent updates | Version current, auto-update ON |
| 8 | **Slack** | Communication | Both | LOW — auto-updates well | Version current |
| 9 | **Teams** | Communication | Both | MEDIUM — bundled with M365 | Version current |
| 10 | **WinRAR** | Utility | Windows | HIGH — CVE-2023-38831 was catastrophic | Version current (must be 6.24+), or replace with 7-Zip |
| 11 | **7-Zip** | Utility | Windows | MEDIUM — less targeted | Version current |
| 12 | **VLC Media Player** | Media | Both | MEDIUM — past vulnerabilities | Version current |
| 13 | **CCleaner** | Utility | Windows | HIGH — supply chain attack in 2017 | Remove unless essential. If kept, version current. |
| 14 | **Xero / QuickBooks** | Accounting | Cloud | MEDIUM — MFA required | MFA enabled, strong password |
| 15 | **Dropbox / OneDrive / Google Drive** | Cloud Storage | Both | MEDIUM — sharing permissions | MFA enabled, sharing reviewed |

### Software That Should Be Removed

| Software | Why | Alternative |
|----------|-----|-------------|
| Windows 10 (after Oct 2025) | End of life = CE automatic fail | Upgrade to Windows 11 |
| Office 2016 / 2019 | End of support | Upgrade to Microsoft 365 |
| Java Runtime (if unused) | Massive attack surface, rarely needed | Remove unless specific app requires it |
| Flash Player | Dead since 2020 | Remove |
| CCleaner | Supply chain attack history, rarely needed | Remove (Windows built-in cleanup is fine) |
| Old PHP / Python / .NET | If on a laptop, probably forgotten from dev work | Remove or update |
| Internet Explorer | Dead | It's gone in Win 11, but legacy apps may call it |

---

## The Framework: How to Run a Client Security Check

### Step 1: Discovery (2 minutes)

Before touching anything, find out what we're working with:

**Ask the client (via email/form, not a call):**
1. What devices do you use for work? (computer, phone, tablet)
2. Mac or Windows? What model/year?
3. Do you use any personal devices for work email?
4. What cloud services? (Google Workspace, Microsoft 365, Xero, etc.)
5. Do you have a website? What's the domain?

**Or if we have access, run the audit script — it answers all of this automatically.**

### Step 2: Automated Audit (5 minutes Mac, 15 minutes Windows)

Run the appropriate script. It checks everything in the priority matrix above and produces a report showing:
- GREEN: Already correct, no action needed
- AMBER: Working but could be better
- RED: Must fix — either a CE fail point or high-risk

### Step 3: Fix (in priority order)

Work through RED items first, then AMBER. Never fix GREEN items — they're already right.

**Frictionless principle:** Every fix must pass the "pub test" — if the client is in the pub and something stops working, can they fix it in 2 minutes? If not, the fix is too aggressive.

### Step 4: Document

Log everything in the knowledge base:
- What was found
- What was fixed
- What was already fine
- Any client-specific quirks

### Step 5: Verify

Re-run the audit script to confirm all RED items are now GREEN.

---

## Mac Audit Script — Pre-Loaded Knowledge

```bash
#!/bin/bash
# Amplified Client Security Audit — macOS
# Version: 1.0 | Framework: client-security-framework.md
# Run with: sudo bash amplified-client-audit-mac.sh

set -euo pipefail

LOGFILE="$HOME/Desktop/amplified-security-$(date +%Y%m%d-%H%M%S).txt"
RED='\033[0;31m'
GREEN='\033[0;32m'
AMBER='\033[0;33m'
NC='\033[0m'
FIXES_NEEDED=0
CHECKS_PASSED=0

log() { echo "$1" | tee -a "$LOGFILE"; }
status() {
    local color=$1 label=$2 detail=$3
    echo -e "${color}[${label}]${NC} ${detail}" | tee -a "$LOGFILE"
    if [[ "$label" == "RED" ]]; then ((FIXES_NEEDED++)); fi
    if [[ "$label" == "GREEN" ]]; then ((CHECKS_PASSED++)); fi
}

log "============================================"
log "AMPLIFIED SECURITY AUDIT — macOS"
log "Date: $(date)"
log "Host: $(hostname)"
log "User: $(whoami)"
log "============================================"
log ""

# ─── TIER 1: Critical ───

log "--- TIER 1: CRITICAL CHECKS ---"
log ""

# 1. macOS version (supported?)
log "1. Operating System"
OS_VER=$(sw_vers -productVersion)
OS_MAJOR=$(echo "$OS_VER" | cut -d. -f1)
if [[ "$OS_MAJOR" -ge 15 ]]; then
    status "$GREEN" "GREEN" "macOS $OS_VER — supported and current"
elif [[ "$OS_MAJOR" -ge 13 ]]; then
    status "$AMBER" "AMBER" "macOS $OS_VER — still supported but upgrade recommended"
else
    status "$RED" "RED" "macOS $OS_VER — may be unsupported. CE fail risk."
fi

# 2. Auto-updates
log ""
log "2. Automatic Updates"
AUTO_CHECK=$(defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled 2>/dev/null || echo "0")
AUTO_DOWNLOAD=$(defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticDownload 2>/dev/null || echo "0")
AUTO_INSTALL=$(defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticallyInstallMacOSUpdates 2>/dev/null || echo "0")
if [[ "$AUTO_CHECK" == "1" && "$AUTO_DOWNLOAD" == "1" ]]; then
    status "$GREEN" "GREEN" "Auto-updates: check=$AUTO_CHECK, download=$AUTO_DOWNLOAD, install-macOS=$AUTO_INSTALL"
else
    status "$RED" "RED" "Auto-updates not fully enabled. check=$AUTO_CHECK, download=$AUTO_DOWNLOAD"
fi

# 3. Admin account check
log ""
log "3. User Account Type"
if dscl . -read /Groups/admin GroupMembership 2>/dev/null | grep -q "$(whoami)"; then
    ADMIN_COUNT=$(dscl . -read /Groups/admin GroupMembership 2>/dev/null | tr ' ' '\n' | grep -v "^GroupMembership:" | grep -v "^$" | wc -l | tr -d ' ')
    status "$AMBER" "AMBER" "Running as admin user ($(whoami)). Consider creating a standard user for daily use. $ADMIN_COUNT admin accounts found."
else
    status "$GREEN" "GREEN" "Running as standard user — good"
fi

# ─── TIER 2: Same Day ───

log ""
log "--- TIER 2: SAME DAY FIXES ---"
log ""

# 4. Firewall
log "4. Firewall"
FW_STATE=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null)
if echo "$FW_STATE" | grep -q "enabled"; then
    status "$GREEN" "GREEN" "Firewall is ON"
else
    status "$RED" "RED" "Firewall is OFF — Apple's one weak default"
    echo "   FIX: sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on"
fi

# 5. XProtect (antivirus)
log ""
log "5. Malware Protection (XProtect)"
XPROTECT_VER=$(system_profiler SPInstallHistoryDataType 2>/dev/null | grep -A2 "XProtect" | grep "Version" | tail -1 | awk '{print $NF}' || echo "unknown")
if [[ -f "/Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Info.plist" ]]; then
    status "$GREEN" "GREEN" "XProtect installed and active (CE-compliant per IASME)"
else
    status "$AMBER" "AMBER" "XProtect status unclear — verify in System Settings > Privacy & Security"
fi

# ─── TIER 2 continued ───

# 6. FileVault
log ""
log "6. Disk Encryption (FileVault)"
FV_STATUS=$(fdesetup status 2>/dev/null)
if echo "$FV_STATUS" | grep -q "FileVault is On"; then
    status "$GREEN" "GREEN" "FileVault is ON — disk encrypted"
else
    status "$RED" "RED" "FileVault is OFF — lost/stolen laptop = data breach"
    echo "   FIX: System Settings → Privacy & Security → FileVault → Turn On"
    echo "   IMPORTANT: Save the recovery key somewhere safe"
fi

# 7. Screen lock
log ""
log "7. Screen Lock"
IDLE_TIME=$(defaults -currentHost read com.apple.screensaver idleTime 2>/dev/null || echo "unknown")
if [[ "$IDLE_TIME" != "unknown" && "$IDLE_TIME" -le 900 ]]; then
    status "$GREEN" "GREEN" "Screen lock after ${IDLE_TIME}s ($(($IDLE_TIME / 60)) min)"
elif [[ "$IDLE_TIME" == "unknown" ]]; then
    status "$AMBER" "AMBER" "Screen lock timeout not readable — verify manually in System Settings → Lock Screen"
else
    status "$RED" "RED" "Screen lock is $IDLE_TIME seconds ($(($IDLE_TIME / 60)) min) — CE requires ≤15 min, we recommend 5 min"
fi

# 8. Gatekeeper
log ""
log "8. Gatekeeper"
GK_STATUS=$(spctl --status 2>/dev/null)
if echo "$GK_STATUS" | grep -q "assessments enabled"; then
    status "$GREEN" "GREEN" "Gatekeeper enabled"
else
    status "$RED" "RED" "Gatekeeper disabled — unsigned apps can run freely"
fi

# 9. SIP
log ""
log "9. System Integrity Protection"
SIP_STATUS=$(csrutil status 2>/dev/null)
if echo "$SIP_STATUS" | grep -q "enabled"; then
    status "$GREEN" "GREEN" "SIP enabled"
else
    status "$RED" "RED" "SIP disabled — system files unprotected. This should never be off."
fi

# ─── SOFTWARE INVENTORY ───

log ""
log "--- SOFTWARE INVENTORY (Pre-loaded knowledge) ---"
log ""

log "Installed Applications:"
ls /Applications/ 2>/dev/null | tee -a "$LOGFILE"

log ""
log "Homebrew packages (if installed):"
if command -v brew &>/dev/null; then
    brew list 2>/dev/null | tee -a "$LOGFILE"
else
    log "Homebrew not installed"
fi

# Check for known-risk software
log ""
log "--- KNOWN-RISK SOFTWARE CHECK ---"

# Chrome
if [[ -d "/Applications/Google Chrome.app" ]]; then
    CHROME_VER=$("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version 2>/dev/null | awk '{print $NF}' || echo "unknown")
    status "$GREEN" "GREEN" "Google Chrome installed (v$CHROME_VER) — verify auto-update in chrome://settings/help"
fi

# Firefox
if [[ -d "/Applications/Firefox.app" ]]; then
    status "$AMBER" "AMBER" "Firefox installed — verify auto-update enabled in Settings → General → Firefox Updates"
fi

# Adobe Reader
if [[ -d "/Applications/Adobe Acrobat Reader.app" ]] || [[ -d "/Applications/Adobe Acrobat DC" ]]; then
    status "$AMBER" "AMBER" "Adobe Acrobat/Reader installed — verify auto-update ON and JavaScript OFF in Preferences → JavaScript"
fi

# Zoom
if [[ -d "/Applications/zoom.us.app" ]]; then
    status "$AMBER" "AMBER" "Zoom installed — verify auto-update in Settings → General"
fi

# Office apps
for app in "Microsoft Word" "Microsoft Excel" "Microsoft PowerPoint" "Microsoft Outlook"; do
    if [[ -d "/Applications/${app}.app" ]]; then
        status "$AMBER" "AMBER" "${app} installed — verify macros disabled (Preferences → Security → Macro Security → Disable All)"
        break  # Only flag once for all Office apps
    fi
done

# Known-bad software
if [[ -d "/Applications/CCleaner.app" ]]; then
    status "$RED" "RED" "CCleaner installed — supply chain attack history (2017). Remove unless essential."
fi

# ─── SUMMARY ───

log ""
log "============================================"
log "SUMMARY"
log "============================================"
log "Checks passed (GREEN): $CHECKS_PASSED"
log "Fixes needed (RED): $FIXES_NEEDED"
log ""
if [[ $FIXES_NEEDED -eq 0 ]]; then
    log "✓ ALL CLEAR — No critical fixes needed"
else
    log "⚠ $FIXES_NEEDED items need attention — see RED items above"
fi
log ""
log "Full log saved to: $LOGFILE"
log "============================================"
```

---

## Windows Audit Script — Pre-Loaded Knowledge

```powershell
# Amplified Client Security Audit — Windows
# Version: 1.0 | Framework: client-security-framework.md
# Run as Administrator: Right-click PowerShell → Run as Administrator
# Then: Set-ExecutionPolicy Bypass -Scope Process -Force; .\amplified-client-audit-windows.ps1

$LogFile = "$env:USERPROFILE\Desktop\amplified-security-$(Get-Date -Format 'yyyyMMdd-HHmmss').txt"
$FixesNeeded = 0
$ChecksPassed = 0

function Log($msg) {
    Write-Host $msg
    Add-Content -Path $LogFile -Value $msg
}

function Status($color, $label, $detail) {
    $prefix = "[$label]"
    switch ($color) {
        "Red"    { Write-Host $prefix -ForegroundColor Red -NoNewline; Write-Host " $detail" }
        "Green"  { Write-Host $prefix -ForegroundColor Green -NoNewline; Write-Host " $detail" }
        "Yellow" { Write-Host $prefix -ForegroundColor Yellow -NoNewline; Write-Host " $detail" }
    }
    Add-Content -Path $LogFile -Value "$prefix $detail"
    if ($label -eq "RED") { $script:FixesNeeded++ }
    if ($label -eq "GREEN") { $script:ChecksPassed++ }
}

Log "============================================"
Log "AMPLIFIED SECURITY AUDIT — Windows"
Log "Date: $(Get-Date)"
Log "Host: $env:COMPUTERNAME"
Log "User: $env:USERNAME"
Log "============================================"
Log ""

# ─── TIER 1: Critical ───

Log "--- TIER 1: CRITICAL CHECKS ---"
Log ""

# 1. Windows version
Log "1. Operating System"
$OSInfo = Get-CimInstance Win32_OperatingSystem
$OSVersion = $OSInfo.Caption
$OSBuild = $OSInfo.BuildNumber
if ($OSVersion -match "Windows 11") {
    Status "Green" "GREEN" "$OSVersion (Build $OSBuild) — supported"
} elseif ($OSVersion -match "Windows 10") {
    Status "Red" "RED" "$OSVersion — END OF LIFE since October 2025. CE automatic fail. Must upgrade to Windows 11."
} else {
    Status "Red" "RED" "$OSVersion — likely unsupported. CE fail risk."
}

# 2. Windows Update
Log ""
Log "2. Windows Update Status"
try {
    $UpdateSession = New-Object -ComObject Microsoft.Update.Session
    $UpdateSearcher = $UpdateSession.CreateUpdateSearcher()
    $PendingUpdates = $UpdateSearcher.Search("IsInstalled=0 and IsHidden=0")
    $PendingCount = $PendingUpdates.Updates.Count

    # Check for auto-update setting
    $AU = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update" -Name "AUOptions" -ErrorAction SilentlyContinue).AUOptions
    $AutoUpdateEnabled = ($AU -eq 4 -or $AU -eq 3)  # 4 = auto install, 3 = auto download

    if ($PendingCount -eq 0 -and $AutoUpdateEnabled) {
        Status "Green" "GREEN" "Windows Update: fully patched, auto-update enabled"
    } elseif ($PendingCount -gt 0) {
        Status "Red" "RED" "$PendingCount pending updates. CE requires high/critical patches within 14 days."
    } else {
        Status "Yellow" "AMBER" "No pending updates but auto-update setting unclear"
    }
} catch {
    Status "Yellow" "AMBER" "Could not check Windows Update status — verify manually"
}

# 3. User Account Type
Log ""
Log "3. User Account Type"
$IsAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
$CurrentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
if ($IsAdmin) {
    Status "Yellow" "AMBER" "Running as Administrator ($CurrentUser). CE recommends standard user for daily work."
} else {
    Status "Green" "GREEN" "Running as standard user ($CurrentUser)"
}

# Count admin accounts
$Admins = net localgroup Administrators 2>$null | Where-Object { $_ -match '^\S' -and $_ -notmatch '^(The|Members|---|--)' -and $_ -ne '' -and $_ -ne 'Alias name' -and $_ -ne 'Comment' }
Log "   Admin accounts: $($Admins -join ', ')"

# ─── TIER 2: Same Day ───

Log ""
Log "--- TIER 2: SAME DAY FIXES ---"
Log ""

# 4. Firewall
Log "4. Firewall"
$FWProfiles = Get-NetFirewallProfile -ErrorAction SilentlyContinue
$AllOn = $true
foreach ($p in $FWProfiles) {
    if (-not $p.Enabled) {
        $AllOn = $false
        Status "Red" "RED" "Firewall profile '$($p.Name)' is OFF"
    }
}
if ($AllOn) {
    Status "Green" "GREEN" "All firewall profiles (Domain, Private, Public) are ON"
}

# 5. Windows Defender / Antivirus
Log ""
Log "5. Malware Protection"
try {
    $DefenderStatus = Get-MpComputerStatus -ErrorAction Stop
    $RealTime = $DefenderStatus.RealTimeProtectionEnabled
    $SigAge = $DefenderStatus.AntivirusSignatureAge  # days since last update
    $CloudProtection = $DefenderStatus.IoavProtectionEnabled

    if ($RealTime -and $SigAge -le 7) {
        Status "Green" "GREEN" "Windows Defender: real-time ON, signatures $SigAge day(s) old"
    } elseif (-not $RealTime) {
        Status "Red" "RED" "Windows Defender: real-time protection DISABLED"
        Log "   FIX: Settings → Privacy & security → Windows Security → Virus & threat protection → Turn ON"
    } elseif ($SigAge -gt 7) {
        Status "Red" "RED" "Windows Defender signatures are $SigAge days old — must be within 1 day for CE+"
    }

    if ($CloudProtection) {
        Status "Green" "GREEN" "Cloud-delivered protection: ON"
    } else {
        Status "Yellow" "AMBER" "Cloud-delivered protection: OFF — enable for better detection"
    }
} catch {
    # Third-party AV might be installed
    $AV = Get-CimInstance -Namespace "root/SecurityCenter2" -ClassName AntiVirusProduct -ErrorAction SilentlyContinue
    if ($AV) {
        Status "Yellow" "AMBER" "Third-party AV detected: $($AV.displayName -join ', '). Verify it's current and scanning."
    } else {
        Status "Red" "RED" "No antivirus detected. CE requires AV on all Windows endpoints."
    }
}

# 6. BitLocker / Device Encryption
Log ""
Log "6. Disk Encryption"
try {
    $BitLocker = Get-BitLockerVolume -MountPoint "C:" -ErrorAction Stop
    if ($BitLocker.ProtectionStatus -eq "On") {
        Status "Green" "GREEN" "BitLocker: ON (C: drive encrypted)"
    } else {
        Status "Red" "RED" "BitLocker: OFF — lost/stolen device = data breach"
        Log "   FIX (Pro/Enterprise): manage-bde -on C:"
        Log "   FIX (Home): Settings → Privacy & security → Device encryption → Turn ON"
    }
} catch {
    # Windows Home doesn't have BitLocker cmdlet — check Device Encryption
    $DevEncStatus = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\BitLocker" -Name "DeviceEncryptionStatus" -ErrorAction SilentlyContinue).DeviceEncryptionStatus
    if ($DevEncStatus -eq 1) {
        Status "Green" "GREEN" "Device Encryption: ON"
    } else {
        Status "Yellow" "AMBER" "Disk encryption status unclear — check Settings → Privacy & security → Device encryption"
    }
}

# 7. Screen Lock
Log ""
Log "7. Screen Lock"
$ScreenTimeout = (Get-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "ScreenSaveTimeOut" -ErrorAction SilentlyContinue).ScreenSaveTimeOut
if ($ScreenTimeout -and [int]$ScreenTimeout -le 900) {
    Status "Green" "GREEN" "Screen lock: $([math]::Round([int]$ScreenTimeout / 60)) minutes"
} elseif ($ScreenTimeout -and [int]$ScreenTimeout -gt 900) {
    Status "Red" "RED" "Screen lock: $([math]::Round([int]$ScreenTimeout / 60)) minutes — CE requires ≤15 min, we recommend 5"
} else {
    Status "Yellow" "AMBER" "Screen lock timeout not set via registry — check Power & battery settings"
}

# 8. Office Macros
Log ""
Log "8. Office Macro Security"
$MacroKey = "HKCU:\Software\Microsoft\Office\16.0\Word\Security"
if (Test-Path $MacroKey) {
    $VBAWarnings = (Get-ItemProperty -Path $MacroKey -Name "VBAWarnings" -ErrorAction SilentlyContinue).VBAWarnings
    # 1=all enabled, 2=disable with notification, 3=disable except signed, 4=disable all
    if ($VBAWarnings -ge 3) {
        Status "Green" "GREEN" "Office macros: restricted (VBAWarnings=$VBAWarnings)"
    } elseif ($VBAWarnings -eq 2) {
        Status "Yellow" "AMBER" "Office macros: disabled with notification — consider tightening to signed-only"
    } else {
        Status "Red" "RED" "Office macros: ENABLED — CE requires disabled unless business-critical"
    }
} else {
    Status "Yellow" "AMBER" "Office macro settings not found — may not have Office installed, or using default settings"
}

# ─── SOFTWARE INVENTORY ───

Log ""
Log "--- SOFTWARE INVENTORY (Pre-loaded knowledge) ---"
Log ""

# Get installed software
$InstalledSoftware = @()
$InstalledSoftware += Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName } | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate
$InstalledSoftware += Get-ItemProperty "HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName } | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate
$InstalledSoftware += Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue |
    Where-Object { $_.DisplayName } | Select-Object DisplayName, DisplayVersion, Publisher, InstallDate

Log "Total installed applications: $($InstalledSoftware.Count)"
Log ""

# Known-risk software checks
Log "--- KNOWN-RISK SOFTWARE CHECK ---"
Log ""

# WinRAR (CVE-2023-38831)
$WinRAR = $InstalledSoftware | Where-Object { $_.DisplayName -match "WinRAR" }
if ($WinRAR) {
    $WRVer = $WinRAR.DisplayVersion
    Status "Yellow" "AMBER" "WinRAR $WRVer installed — must be 6.24+ (CVE-2023-38831). Consider replacing with 7-Zip."
}

# CCleaner
$CCleaner = $InstalledSoftware | Where-Object { $_.DisplayName -match "CCleaner" }
if ($CCleaner) {
    Status "Red" "RED" "CCleaner installed — supply chain attack history. Remove unless essential."
}

# Java
$Java = $InstalledSoftware | Where-Object { $_.DisplayName -match "Java" -and $_.DisplayName -notmatch "JavaScript" }
if ($Java) {
    Status "Yellow" "AMBER" "Java Runtime detected: $($Java.DisplayName -join ', '). Remove if not needed — large attack surface."
}

# Adobe Reader/Acrobat
$Adobe = $InstalledSoftware | Where-Object { $_.DisplayName -match "Adobe (Acrobat|Reader)" }
if ($Adobe) {
    Status "Yellow" "AMBER" "Adobe Acrobat/Reader: $($Adobe.DisplayVersion). Verify auto-update ON and JavaScript disabled."
}

# Old Office
$Office = $InstalledSoftware | Where-Object { $_.DisplayName -match "Microsoft Office (2016|2019|2013|2010)" }
if ($Office) {
    Status "Red" "RED" "Old Office version detected: $($Office.DisplayName). End of support — CE fail. Upgrade to Microsoft 365."
}

# Zoom
$Zoom = $InstalledSoftware | Where-Object { $_.DisplayName -match "Zoom" }
if ($Zoom) {
    Status "Yellow" "AMBER" "Zoom $($Zoom.DisplayVersion) — verify auto-update enabled"
}

# Browsers
$Chrome = $InstalledSoftware | Where-Object { $_.DisplayName -match "Google Chrome" }
if ($Chrome) {
    Status "Green" "GREEN" "Google Chrome $($Chrome.DisplayVersion) — verify auto-update at chrome://settings/help"
}

$Firefox = $InstalledSoftware | Where-Object { $_.DisplayName -match "Mozilla Firefox" }
if ($Firefox) {
    Status "Yellow" "AMBER" "Firefox $($Firefox.DisplayVersion) — verify auto-update in Settings"
}

# Auto-run
Log ""
Log "9. AutoRun / AutoPlay"
$AutoRun = (Get-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" -Name "NoDriveTypeAutoRun" -ErrorAction SilentlyContinue).NoDriveTypeAutoRun
if ($AutoRun -eq 255) {
    Status "Green" "GREEN" "AutoRun: disabled for all drives"
} else {
    Status "Yellow" "AMBER" "AutoRun may be enabled — verify in Settings → Bluetooth & devices → AutoPlay"
}

# Full software list to log
Log ""
Log "--- FULL SOFTWARE LIST ---"
$InstalledSoftware | Sort-Object DisplayName | ForEach-Object {
    Log "  $($_.DisplayName) | v$($_.DisplayVersion) | $($_.Publisher)"
}

# ─── SUMMARY ───

Log ""
Log "============================================"
Log "SUMMARY"
Log "============================================"
Log "Checks passed (GREEN): $ChecksPassed"
Log "Fixes needed (RED): $FixesNeeded"
Log ""
if ($FixesNeeded -eq 0) {
    Log "ALL CLEAR — No critical fixes needed"
} else {
    Log "$FixesNeeded items need attention — see RED items above"
}
Log ""
Log "Full log saved to: $LogFile"
Log "============================================"
```

---

## Cloud Services Checklist

Run separately — these apply regardless of device type.

| Service | Check | How | Pass |
|---------|-------|-----|------|
| Google Workspace | MFA enabled all users | Admin console → Security → 2-Step Verification | Enforced |
| Google Workspace | Legacy apps blocked | Admin → Security → API controls | No legacy access |
| Microsoft 365 | MFA enabled all users | Entra ID → Security → MFA | Enforced |
| Microsoft 365 | Legacy authentication | Entra ID → Security → Conditional Access | Blocked |
| Microsoft 365 | Audit logging | Compliance center → Audit | ON |
| Xero | MFA | My Xero → Account → Security | ON |
| QuickBooks | MFA | Account → Sign in & security | ON |
| Dropbox | MFA | Settings → Security → 2-step verification | ON |
| Any cloud service | Password ≥ 8 (with MFA) or ≥ 12 (without) | — | Meets CE minimum |

---

## Frictionless Client Communication

**When reporting findings, use percentages, not fear:**

- WRONG: "Your computer is vulnerable to hackers and ransomware"
- RIGHT: "We checked 12 things. 10 were already fine. 2 needed a quick adjustment — both done now."

**When something isn't recognised:**
- Say: "Software not recognised" (not "unlicensed software detected")

**Status updates:**
- "Security check complete. 92% already good. 2 quick fixes applied. You're sorted."

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 15 Mar 2026 | Initial framework. Mac + Windows scripts. Pre-loaded top 15 software. Priority matrix from CE failure data + breach survey. |

---

# Part 2 — Security Process Sheet & Gap Analysis Tool

**Version:** 1.0  
**Date:** 15 March 2026  
**Classification:** INTERNAL — Amplified Partners  
**Purpose:** ISO 9001-style security process sheet, gap analysis template, and implementation guide  
**Usage:** One copy per client. Fill in "Current State" during discovery. Use "How We Get There" as the implementation runbook.

---

## How This Document Works

| Column | Purpose | Who fills it in |
|--------|---------|-----------------|
| **Security Control** | What the Cyber Essentials standard requires | Pre-filled (doesn't change) |
| **Ideal State** | What "good" looks like for a small business | Pre-filled (doesn't change) |
| **Current State** | What the client actually has right now | Filled during discovery audit |
| **Gap** | What's missing | Auto-determined from Current vs Ideal |
| **How We Get There** | Pre-worked implementation steps for common setups | Pre-filled with M365/Google/common router scenarios |
| **Client Effort** | What the client or their staff have to do | Pre-filled (almost always "nothing") |
| **Rollback Plan** | How we undo it if something breaks | Pre-filled |

---

## Part 1: The Three Tiers of Client Communication

Before any technical work, here's exactly how we talk to the client.

### Tier 1: The Silent Fix (Permission Only)

**When:** During onboarding, as part of the service introduction.  
**Who:** Business owner.  
**How:** Casual conversation, not a meeting. Part of normal onboarding chat.

**What we say (words matter — use these):**

> "As part of your service, we're going to do a quick security check on your IT. There are usually a few holes in everyone's setup that we can easily plug — nothing unusual, nothing to worry about. We do it overnight, so there's no disruption to your day. You won't notice any difference except things will be more secure. That alright?"

**Expected response:** "Yeah, fine."

**What we then do silently:**
- Email security (SPF/DKIM/DMARC)
- Firewall hardening
- Secure configuration
- Patch management
- Endpoint protection on managed devices

**What we give them after:** One-page Security Health Report (see template in Part 5).

### Tier 2: The Passkey Upgrade (Video + Small Ask)

**When:** After Tier 1 is complete and confirmed clean.  
**Who:** Business owner first, then staff.  
**How:** Short message with a 60-second video.

**What we say:**

> "Everything's done on the security side — your email, network, and devices are all sorted. Here's your report.
>
> There's one more thing that makes a big difference. Instead of passwords, your team can log in with their fingerprint or face. It's actually faster than typing a password, and it stops phishing attacks completely. Here's a quick video of what it looks like.
>
> [60-second video: someone tapping their fingerprint, getting straight in]
>
> If you're up for it, each person spends about 60 seconds setting it up. We'd suggest doing it at the start of a team meeting so everyone's together. Your call, no rush."

**If they say yes:** Roll out passkeys (see implementation steps in Part 3).  
**If they say not yet:** Fine. Tier 1 is still protecting them. Revisit in a month.

### Tier 3: The Cyber Essentials Nudge (Show, Don't Sell)

**When:** After Tier 1 (minimum) or Tier 2 (ideal) is complete.  
**Who:** Business owner.  
**How:** Show them the self-assessment checklist with ticks.

**What we say:**

> "By the way — because of the work we've already done, your setup now meets the Cyber Essentials standard. Have a look..."
>
> [Show them the checklist — see Part 4]
>
> - Firewalls? ✓
> - Secure configuration? ✓
> - Patch management? ✓
> - User access control? ✓
> - Malware protection? ✓
>
> "You've already passed. We can't award it ourselves — it's a government thing — but if you want the official certificate, a badge for your website, and free £25,000 cyber insurance, it costs £320-440 and you sign one form. We handle everything else. Completely up to you."

**If they want it:** We complete the IASME submission (see Part 4).  
**If they don't:** Fine. They're still secure. The ticks are still ticked.

---

## Part 2: Security Process Sheet & Gap Analysis

### Control 1: Firewall / Network Boundary

| | Detail |
|---|---|
| **Security Control** | Firewall / Internet Gateway Protection |
| **CE Requirement** | All devices that connect to the internet must be protected by a correctly configured firewall. Default admin passwords must be changed. Only necessary network services should be accessible from the internet. |
| **Ideal State** | Hardware firewall or ISP router with: admin password changed from default, UPnP disabled, remote management disabled (or restricted to specific IPs), only required ports open (typically 443 outbound only), firmware updated to latest version, Wi-Fi using WPA2/WPA3 with strong passphrase. |
| **Current State** | _(Fill during discovery)_ |
| **Gap** | _(Determined from above)_ |

**How We Get There — Common Scenarios:**

**Scenario A: ISP-provided router (BT, Sky, Virgin, etc.)**
1. Log into router admin panel (default IP usually 192.168.1.1 or 192.168.0.1)
2. Change admin password to a strong unique password (store in Amplified's password vault)
3. Disable UPnP (Universal Plug and Play)
4. Disable remote management / WAN access
5. Check port forwarding rules — remove any that aren't actively needed
6. Update firmware if available
7. Change Wi-Fi password to a strong passphrase (3+ random words)
8. Enable WPA3 if supported, otherwise WPA2-AES (never WPA/WEP/TKIP)
9. Disable WPS (Wi-Fi Protected Setup)
10. If router is ancient (no WPA2, no firmware updates): recommend replacement

**Scenario B: Dedicated firewall (pfSense, UniFi, Draytek, SonicWall)**
1. Same as above, plus:
2. Review firewall rules — deny all inbound by default, allow only specific required traffic
3. Enable IDS/IPS if available (Snort/Suricata on pfSense)
4. Configure DNS filtering (block known malicious domains)
5. Set up VLAN segmentation if hardware supports it (separate guest/IoT/business networks)

**Client Effort:** Nothing. We do this overnight.  
**Rollback:** Factory reset router and reconfigure from backup config (5-10 min). Wi-Fi password change requires telling the client the new password in advance.  
**Risk Level:** Low. Main risk is Wi-Fi password change causing confusion — communicate in advance.

---

### Control 2: Secure Configuration

| | Detail |
|---|---|
| **Security Control** | Secure Configuration of Devices and Software |
| **CE Requirement** | Computers and network devices must be configured to reduce vulnerabilities. Remove/disable unnecessary software, change default passwords, disable auto-run. |
| **Ideal State** | All devices: default accounts disabled or passwords changed, auto-run/autoplay disabled, screen lock enabled (max 15 minutes), unnecessary software removed, only licensed and supported OS versions in use, Bluetooth off when not needed. |
| **Current State** | _(Fill during discovery)_ |
| **Gap** | _(Determined from above)_ |

**How We Get There — Common Scenarios:**

**Scenario A: Windows 10/11 devices (most common)**
1. Via M365 Intune or Group Policy (if domain-joined):
   - Set screen lock timeout to 10 minutes
   - Disable autoplay/autorun
   - Enable BitLocker drive encryption
   - Disable guest account
   - Set minimum password length to 12 characters (transitional — passkeys replace this)
2. If no Intune/domain:
   - Remote into each device (with permission) or use RMM agent
   - Apply settings manually or via PowerShell script
3. Remove unnecessary software (bloatware, unused apps)
4. Check Windows edition is supported (no Windows 7/8, no Home edition in business ideally)

**Scenario B: Mac devices**
1. Via MDM (Jamf, Mosyle, or M365 Intune for Mac):
   - Enable FileVault encryption
   - Set screen lock timeout
   - Disable guest account
   - Enable firewall (System Preferences → Security & Privacy)
2. If no MDM: configure manually via System Preferences

**Scenario C: Mobile devices (BYOD)**
1. If company-issued: enroll in MDM, enforce passcode/biometric lock
2. If personal (BYOD): recommend (don't enforce) screen lock and OS updates
3. For M365/Google Workspace: use Conditional Access to require device compliance for data access

**Client Effort:** Nothing for managed devices. BYOD = "your phone, you do you" — we can help if they want.  
**Rollback:** Revert Group Policy / Intune policy (immediate). Individual settings reverted via script.  
**Risk Level:** Very low. Screen lock and encryption are invisible to users.

---

### Control 3: Patch Management / Software Updates

| | Detail |
|---|---|
| **Security Control** | Security Update Management |
| **CE Requirement** | All software must be licensed and supported. High/critical security patches must be applied within 14 days of release. Unsupported software must be removed. |
| **Ideal State** | Windows Update set to auto-install, Microsoft 365 apps on Current Channel, all third-party apps updated (browsers auto-update, Adobe/Java removed if not needed), no end-of-life OS (Windows 7/8, unsupported macOS). |
| **Current State** | _(Fill during discovery)_ |
| **Gap** | _(Determined from above)_ |

**How We Get There — Common Scenarios:**

**Scenario A: M365 / Intune managed**
1. Configure Windows Update for Business:
   - Feature updates: defer 30 days (stability)
   - Quality/security updates: defer 0 days (apply immediately)
   - Set active hours to avoid restart during business hours (9am-6pm)
   - Enforce restart deadline: 3 days after download
2. Configure M365 Apps updates: Current Channel, auto-install
3. Use Intune app deployment for third-party updates where possible

**Scenario B: No MDM / standalone devices**
1. Enable Windows Update auto-install on each device
2. Set active hours to business hours
3. Install Patch My PC, Chocolatey, or Ninite for third-party patching
4. Remove unsupported software (check Programs & Features for old versions)
5. If Windows 7/8 found: plan upgrade path (usually Windows 11, may need hardware)

**Scenario C: macOS**
1. Enable automatic updates in System Preferences
2. Ensure macOS version is within Apple's supported range (current minus 2 major versions)
3. App Store apps auto-update; non-App Store apps need manual check or Homebrew

**Client Effort:** Occasional "restart required" notification. That's it.  
**Rollback:** Uninstall specific Windows updates via `wusa.exe /uninstall /kb:XXXXXXX` (5-15 min). Rarely needed.  
**Risk Level:** Medium. Patches occasionally break things. This is why we deploy Tuesday night (after Patch Tuesday), not immediately. Health check Wednesday morning.

---

### Control 4: User Access Control / Authentication

| | Detail |
|---|---|
| **Security Control** | User Access Control |
| **CE Requirement** | Each user must have their own account. Admin accounts used only for admin tasks. MFA must be enabled on all cloud services and admin interfaces (mandatory from April 2026 v3.3). |
| **Ideal State** | Every user has individual account (no shared logins), admin accounts separate from daily-use accounts, MFA enabled on all cloud services (passkeys preferred), no default/shared passwords, account lockout after 10 failed attempts. |
| **Current State** | _(Fill during discovery)_ |
| **Gap** | _(Determined from above)_ |

**How We Get There — Common Scenarios:**

**Scenario A: Microsoft 365**
1. Audit user list: `Get-MsolUser -All | Select DisplayName, UserPrincipalName, isLicensed, BlockCredential`
2. Check for shared accounts (e.g., "info@", "admin@", "office@") — create individual accounts, convert shared ones to shared mailboxes
3. Check admin roles: only dedicated admin accounts should have Global Admin / Exchange Admin etc.
4. Create separate admin accounts for anyone who needs admin access (e.g., admin-ewan@domain.com)
5. Enable Security Defaults (free tier) or Conditional Access (Business Premium):
   - Require MFA for all users
   - Require MFA for all admin actions
   - Block legacy authentication protocols
6. **Passkey deployment** (Tier 2 — with boss permission):
   - Enable FIDO2 security key + passkey registration in Azure AD → Authentication Methods
   - Enable "Temporary Access Pass" for initial enrollment
   - Send each user a Temporary Access Pass via secure channel
   - User logs in with TAP, registers passkey (Face ID / fingerprint / Windows Hello)
   - One-time setup, ~60 seconds
   - After 48-hour grace period: disable password-only login

**Scenario B: Google Workspace**
1. Admin Console → Directory → Users: audit all accounts
2. Check for shared accounts — convert to Google Groups or shared drives
3. Admin Console → Security → Authentication → 2-Step Verification:
   - Set to "Enforced" for all OUs
   - Allow passkeys/security keys as primary method
4. Passkey deployment:
   - Enable passkeys in Admin Console → Security → Authentication → Passkeys
   - Users register at myaccount.google.com → Security → Passkeys
   - Same process: boss announces at meeting, each person takes 60 seconds

**Transitional password technique (for the 48-hour window):**
Teach users the "three random words + number" technique:
- Think of three random objects you can picture: e.g., purple, hammer, boat
- Stick a number on the end: purple-hammer-boat-7
- That's their temporary password. They'll use it for 2 days max, then passkeys take over.
- We can give them this in a simple card or one-pager.

**Client Effort:**  
- Tier 1 (MFA via Security Defaults): may get a one-time MFA prompt (authenticator app)
- Tier 2 (Passkeys): 60 seconds to register fingerprint/face. Done at a team meeting.  
**Rollback:** Disable Conditional Access policy or Security Defaults (immediate). Users revert to password-only login.  
**Risk Level:** Medium-Low. Main risk is someone not having their phone for MFA. Temporary Access Pass handles this. Passkey enrollment is lower risk because the old password still works during transition.

---

### Control 5: Malware Protection

| | Detail |
|---|---|
| **Security Control** | Malware Protection |
| **CE Requirement** | Anti-malware software must be installed on all devices, kept up to date, and configured to scan files automatically on access and prevent connections to malicious websites. |
| **Ideal State** | Windows Defender (built-in, free, excellent) enabled and updating on all Windows devices, real-time protection on, cloud-delivered protection on, automatic sample submission on. For higher tiers: Microsoft Defender for Business (EDR capabilities). macOS: built-in XProtect + optional Malwarebytes. |
| **Current State** | _(Fill during discovery)_ |
| **Gap** | _(Determined from above)_ |

**How We Get There — Common Scenarios:**

**Scenario A: Windows 10/11 (most clients)**
1. Check Windows Security → Virus & threat protection:
   - Real-time protection: ON
   - Cloud-delivered protection: ON
   - Automatic sample submission: ON
   - Tamper protection: ON
2. If third-party AV is installed (Norton, McAfee, AVG, etc.):
   - If it's a paid, current subscription: leave it (it's working)
   - If it's expired/free/bloatware: remove it, let Defender take over (Defender is better than expired Norton)
3. Via Intune: configure Defender Antivirus policy centrally
4. For M365 Business Premium clients: enable Defender for Business (EDR):
   - Onboard devices via Intune
   - Enable Attack Surface Reduction rules
   - Enable automated investigation and response

**Scenario B: macOS**
1. XProtect is built-in and auto-updates — check it's not disabled
2. Enable firewall in System Preferences → Security & Privacy
3. For additional protection: Malwarebytes for Mac (free for manual scans, paid for real-time)
4. Gatekeeper: ensure "App Store and identified developers" is enabled

**Scenario C: Mobile devices**
1. iOS: built-in security is excellent, no additional AV needed
2. Android: Google Play Protect enabled (Settings → Security → Google Play Protect)
3. For managed devices: Defender for Endpoint mobile (if M365 Business Premium)

**Client Effort:** Nothing. Defender runs silently. If we remove old AV bloatware, performance actually improves.  
**Rollback:** Re-install previous AV if needed (rare). Defender policies reverted via Intune.  
**Risk Level:** Very low. Defender is already installed on Windows 10/11 — we're just ensuring it's configured correctly.

---

### Bonus Control: Email Security (Not CE-required, but critical)

| | Detail |
|---|---|
| **Security Control** | Email Authentication & Anti-Phishing |
| **CE Requirement** | Not explicitly required by CE, but critical for preventing business email compromise (BEC), which is the #1 financial threat to SMEs. |
| **Ideal State** | SPF record published (specifying authorised mail servers), DKIM signing enabled, DMARC at p=reject (after ramp-up period), anti-phishing policies enabled in M365/Google. |
| **Current State** | _(Fill during discovery)_ |
| **Gap** | _(Determined from above)_ |

**How We Get There:**

**Phase 1 (Night 1): Foundation**
1. Check existing DNS records: `nslookup -type=txt domain.com` for SPF, `nslookup -type=txt _dmarc.domain.com` for DMARC
2. If no SPF: add `v=spf1 include:spf.protection.outlook.com ~all` (M365) or `v=spf1 include:_spf.google.com ~all` (Google)
3. If no DKIM: enable in M365 Defender portal or Google Admin Console
4. If no DMARC: add `v=DMARC1; p=none; rua=mailto:dmarc-reports@amplifiedpartners.ai; ruf=mailto:dmarc-forensics@amplifiedpartners.ai`

**Phase 2 (Week 2-3): Monitor**
5. Monitor DMARC reports for 2 weeks — check for legitimate senders failing authentication
6. Whitelist any legitimate third-party senders in SPF record
7. Move DMARC to `p=quarantine` (suspicious emails go to junk)

**Phase 3 (Week 4+): Enforce**
8. After 2 more clean weeks: move DMARC to `p=reject` (spoofed emails blocked entirely)
9. NEVER jump straight to `p=reject` — this can block legitimate email if SPF isn't complete

**Anti-phishing policies (M365):**
- Enable Safe Links (URL scanning in emails)
- Enable Safe Attachments (sandboxing)
- Enable impersonation protection (flag emails pretending to be the boss)
- Configure junk mail filtering

**Anti-phishing policies (Google Workspace):**
- Enable enhanced pre-delivery message scanning
- Enable external email warning banner
- Configure suspicious email warnings

**Client Effort:** Nothing. Emails continue working normally. Spam decreases.  
**Rollback:** Remove DNS records. TTL should be pre-lowered to 300 seconds before changes, so rollback propagates in ~5 minutes.  
**Risk Level:** Low if we follow the none → quarantine → reject ramp-up. High if we skip to reject (could block legitimate email).

---

## Part 3: Implementation Sequence — The Overnight Protocol

### Pre-Deployment (48-72 hours before)

1. **Lower DNS TTL** to 300 seconds on all records we'll modify (SPF, DKIM, DMARC)
2. **Take full configuration backup** of router/firewall
3. **Snapshot current state** in the process sheet (fill in "Current State" column)
4. **Notify boss** (Tier 1 conversation — "we're plugging a few holes overnight")
5. **Pre-stage all changes** — scripts written, tested, ready to execute

### Night 1: Email Security + Firewall (Lowest Risk)

| Time | Action | Health Check |
|------|--------|-------------|
| 23:00 | Deploy SPF record | Verify DNS propagation (dig/nslookup) |
| 23:15 | Enable DKIM signing | Send test email, verify DKIM header |
| 23:30 | Deploy DMARC at p=none | Verify DNS record resolves |
| 23:45 | Log into router, change admin password | Verify admin access with new creds |
| 00:00 | Disable UPnP, remote management, WPS | Verify LAN devices still connect |
| 00:15 | Update router firmware (if available) | Verify router comes back up, LAN works |
| 00:30 | Change Wi-Fi password (if needed) | Verify connection with new password |
| 01:00 | **Health check: send/receive test emails, verify all devices connect to Wi-Fi, verify internet access** | |
| 04:30 | **Decision point:** If any health check has failed and isn't resolved → rollback that specific change | |
| 05:00 | **Night 1 complete.** Log all changes in process sheet. | |

**If Wi-Fi password changed:** Text the new password to the boss at 07:00 with: "Morning — your Wi-Fi password has been updated as part of the security work. New password is: [password]. Everything else is the same."

### Night 2: Secure Configuration + Endpoint Protection

| Time | Action | Health Check |
|------|--------|-------------|
| 23:00 | Connect to each device (RMM agent or remote desktop) | Verify connection |
| 23:15 | Enable BitLocker / FileVault on each device | Verify encryption starts (doesn't require restart) |
| 23:30 | Set screen lock to 10 minutes | Verify policy applies |
| 23:45 | Disable autoplay/autorun | Verify setting |
| 00:00 | Remove bloatware / expired AV | Verify Defender activates |
| 00:15 | Configure Defender policies (real-time, cloud, tamper protection) | Verify Defender status: all green |
| 00:30 | Disable guest accounts, set account lockout policy | Verify |
| 01:00 | **Health check: all devices responsive, Defender reporting green, no user-facing changes** | |
| 04:30 | **Decision point** | |
| 05:00 | **Night 2 complete.** | |

### Night 3: Patch Management

| Time | Action | Health Check |
|------|--------|-------------|
| 23:00 | Inventory all installed software and versions | Log everything |
| 23:15 | Remove unsupported / end-of-life software | Verify removal |
| 23:30 | Configure Windows Update policies (auto-install, active hours, restart deadline) | Verify policy applies |
| 23:45 | Apply any outstanding critical/high patches | Monitor installation |
| 00:00-03:00 | Allow patches to install and devices to restart | Monitor progress |
| 03:00 | **Health check: all devices back online, all apps launch correctly** | |
| 04:30 | **Decision point** | |
| 05:00 | **Night 3 complete.** | |

**Risk note:** Night 3 is the highest risk night. Patches occasionally break applications. This is why we do it last — if a patch causes issues, we have the full next day to troubleshoot before the business opens.

### Day 4: Deliver Security Health Report

- Send the one-page report to the boss (see Part 5)
- Show green ticks for everything we've fixed
- No call needed — just the report via email or their preferred channel
- Include: "Everything's done. Here's what we found and fixed."

### Day 5+ (When Boss Agrees): Passkey Deployment (Tier 2)

Only after Tier 1 is confirmed clean and the boss has watched the video.

| Time | Action | Health Check |
|------|--------|-------------|
| Before meeting | Enable passkey registration in M365/Google admin | Verify setting is active |
| Team meeting (5 min) | Boss introduces: "We're upgrading our logins. Watch this 60-second video." | |
| After video | Each person opens their laptop/phone, follows the prompt | |
| 60 seconds per person | Tap fingerprint / face scan → passkey registered | Verify each user's passkey works |
| Same meeting | Anyone who struggles: give them a Temporary Access Pass, help them 1:1 | |
| 48 hours later | Grace period ends. Password-only login disabled for cloud services. | Verify all users can log in with passkey |

**If someone can't do passkeys** (very old device, no biometric sensor):
- Set up Microsoft Authenticator / Google Authenticator as fallback
- No one is ever locked out
- Flag the device for replacement at next hardware refresh

---

## Part 4: Cyber Essentials Self-Assessment Checklist

This is what we show the boss during Tier 3 (the nudge). Every tick should already be filled in by the time we show this.

### Firewall / Internet Gateway
- [ ] Firewall present on all internet-connected devices
- [ ] Default admin password changed
- [ ] Firewall rules: only necessary services accessible
- [ ] UPnP disabled
- [ ] Remote management disabled or restricted

### Secure Configuration
- [ ] Default/unnecessary user accounts removed or disabled
- [ ] Default passwords changed on all accounts and devices
- [ ] Autorun/autoplay disabled
- [ ] Screen lock enabled (15 minutes or less)
- [ ] Only necessary software installed
- [ ] All software licensed and supported

### Patch Management
- [ ] Operating systems within supported versions
- [ ] High/critical patches applied within 14 days
- [ ] Auto-updates enabled where possible
- [ ] No end-of-life software in use

### User Access Control
- [ ] Each user has individual account
- [ ] Admin privileges restricted to admin tasks only
- [ ] Separate admin accounts for admin users
- [ ] MFA enabled on all cloud services ← **Mandatory fail from April 2026 if missing**
- [ ] Account lockout configured (max 10 attempts)

### Malware Protection
- [ ] Anti-malware installed on all devices
- [ ] Anti-malware is up to date (auto-updating)
- [ ] Real-time / on-access scanning enabled
- [ ] Configured to prevent connections to malicious websites

**To get the official certificate:**
1. Client signs the board-level declaration (we prepare this — they just sign)
2. Client pays IASME £320-440+VAT (we handle the submission)
3. We fill in 90%+ of the questionnaire from our records
4. Client reviews and approves
5. Certificate issued (typically 1-3 business days)
6. Includes: certificate, badge for website, free £25,000 cyber liability insurance (businesses under £20m turnover)
7. Annual renewal — Amplified maintains evidence and coordinates

---

## Part 5: Security Health Report Template (One-Pager for the Boss)

```
╔══════════════════════════════════════════════════════════════╗
║                    SECURITY HEALTH REPORT                    ║
║                    [Client Business Name]                    ║
║                    Date: [DD/MM/YYYY]                        ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  OVERALL STATUS: [🟢 PROTECTED / 🟡 IN PROGRESS / 🔴 AT RISK] ║
║                                                              ║
║  ┌─────────────────────────┬──────────┬──────────┐          ║
║  │ Control                 │ Before   │ After    │          ║
║  ├─────────────────────────┼──────────┼──────────┤          ║
║  │ Email Security          │ 🔴 None   │ 🟢 Active │          ║
║  │ Firewall                │ 🟡 Default │ 🟢 Hardened│         ║
║  │ Device Security         │ 🔴 Basic  │ 🟢 Encrypted│        ║
║  │ Software Updates        │ 🟡 Manual │ 🟢 Auto    │         ║
║  │ Login Security          │ 🔴 Password│ 🟢 Passkey │         ║
║  │ Malware Protection      │ 🟡 Partial│ 🟢 Full    │         ║
║  └─────────────────────────┴──────────┴──────────┘          ║
║                                                              ║
║  WHAT WE DID:                                               ║
║  • Secured your email against spoofing and phishing         ║
║  • Hardened your network firewall                           ║
║  • Encrypted all business devices                           ║
║  • Enabled automatic security updates                       ║
║  • Upgraded logins to fingerprint/face (if Tier 2 done)     ║
║  • Installed enterprise-grade malware protection            ║
║                                                              ║
║  YOUR RISK REDUCTION: ~85-90%                               ║
║  (Based on NCSC Cyber Essentials controls coverage)          ║
║                                                              ║
║  CYBER ESSENTIALS READY: ✓ Yes                              ║
║  Want the certificate + free £25k insurance? Just say.      ║
║                                                              ║
║  Questions? Reply to this message or call [number].         ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Part 6: Risk Reduction Quantification

### What We Tell the Boss

**Headline:** "Your business is roughly 85-90% less likely to suffer a cyber incident."

**The breakdown:**

| Threat | Before Amplified | After Amplified | Risk Reduction |
|--------|-----------------|-----------------|----------------|
| Phishing attack succeeds | ~30% chance/year | ~1-2% with passkeys | ~95% |
| Ransomware infection | ~15% chance/year for SMEs | ~1-3% | ~85% |
| Data breach from stolen passwords | ~20% of breaches are credential-based | Near zero with passkeys | ~98% |
| Compliance failure | 100% (no certification) | 0% (CE certified) | 100% |
| Business email compromise | ~10% of UK SMEs/year | ~1-2% | ~85% |

**Sources:** UK Cyber Breaches Survey 2024, Verizon DBIR 2024, FIDO Alliance Passkey Index Oct 2025.

**For staff on the wireless network:**
- Every device connecting to business Wi-Fi gets endpoint protection
- Network segmented so a compromised personal phone can't reach business data
- Staff are protected whether in the office or working remotely

**Without passkeys (Tier 1 only):** ~60-70% risk reduction  
**With passkeys (Tier 2):** ~85-90% risk reduction  
**With CE certification (Tier 3):** Same security level + insurance + compliance proof

---

## Part 7: Client Zero — Ewan's Setup

### Purpose
Test the entire process on Ewan's Byker Business Help / Amplified Partners setup before rolling out to any client.

### What We're Testing
1. The discovery audit automation
2. The overnight deployment protocol
3. The passkey enrollment flow
4. The communication templates
5. The Cyber Essentials questionnaire process
6. Deliberately breaking things to test rollback
7. The one-page health report

### Ewan's Setup Details
_(To be filled during discovery)_

| Item | Detail |
|------|--------|
| Email provider | _(M365 / Google Workspace / other)_ |
| Domain(s) | bykerbusinesshelp.ai, amplifiedpartners.ai, others? |
| Number of users | _(count)_ |
| Devices | _(list: laptops, phones, tablets)_ |
| Router/firewall | _(make/model)_ |
| Current MFA | _(yes/no, what method)_ |
| Current AV | _(Defender / other)_ |
| Current email security | _(SPF/DKIM/DMARC status)_ |
| Cloud services in use | _(list)_ |
| Beast infrastructure | 135.181.161.131, Hetzner AX162-R, 35+ Docker containers |

### Client Zero Schedule

| Stage | What | When | Duration |
|-------|------|------|----------|
| 1 | Discovery audit (automated) | Can run now — no client involvement | ~15 min compute |
| 2 | Review findings with Ewan | After discovery | 10 min read |
| 3 | Night 1: Email + Firewall | First available evening | Overnight |
| 4 | Morning check: everything clean? | Next morning | 5 min |
| 5 | Night 2: Secure Config + Endpoint | Following evening | Overnight |
| 6 | Morning check | Next morning | 5 min |
| 7 | Night 3: Patch Management | Following evening | Overnight |
| 8 | Morning check | Next morning | 5 min |
| 9 | Passkey enrollment | When Ewan's ready | 60 seconds |
| 10 | Deliberately break things | After all deployed | 2-3 hours |
| 11 | CE self-assessment | After testing complete | 45 min (Amplified fills, Ewan reviews) |
| 12 | Write the playbook | After CE done | Becomes this document's final version |

### What Can Be Done Without Ewan Present

The discovery audit can run right now against publicly available information:
- DNS records (SPF, DKIM, DMARC) for bykerbusinesshelp.ai and amplifiedpartners.ai
- Port scan against public IPs
- SSL/TLS certificate checks
- Website security headers
- Public email configuration

This gives us the "Current State" for several controls without needing access to any internal systems.

---

## Appendix A: Automation Targets

### What Should Be Automated (Cove/Temporal)

| Task | Current Time | Automated Time | Notes |
|------|-------------|---------------|-------|
| DNS record audit (SPF/DKIM/DMARC) | 30 min manual | 30 seconds | dig/nslookup commands |
| Port scan | 20 min manual | 2 minutes | nmap with standard profiles |
| M365 user/MFA audit | 45 min manual | 1 minute | PowerShell / Graph API |
| Google Workspace audit | 45 min manual | 1 minute | Admin SDK API |
| Router config check | 30 min manual | Varies | Depends on router — may need manual |
| Defender status check | 15 min per device | 30 sec per device | Via Intune API or WMI |
| Patch status audit | 20 min per device | 1 min per device | Via Windows Update API |
| CE questionnaire pre-fill | 3-4 hours manual | 45 minutes | Template + auto-fill from audit data |
| Health report generation | 1 hour manual | 5 minutes | Template + data from audit |

**Total: from 10-15 hours manual to ~2 hours automated.**

### What Can't Be Automated (Requires Human)

- Physical router access (if no remote management)
- Boss permission conversation (Tier 1)
- Passkey enrollment decision (Tier 2)
- CE board declaration signature (Tier 3)
- IASME fee payment (client's card)
- Judgement calls on unusual configurations

---

## Appendix B: Common SME IT Stacks

Most small businesses in the UK fall into one of these patterns:

### Pattern 1: Microsoft 365 Business (60-70% of SMEs)
- Email: Exchange Online
- Files: OneDrive / SharePoint
- Devices: Windows 10/11 laptops
- Auth: Azure AD
- Best approach: Intune for device management, Conditional Access for MFA, Defender for endpoint

### Pattern 2: Google Workspace (20-25% of SMEs)
- Email: Gmail
- Files: Google Drive
- Devices: Mix of Windows/Mac/Chromebook
- Auth: Google Identity
- Best approach: Google Endpoint Management, Google 2SV enforcement, third-party EDR or Defender

### Pattern 3: Mixed / Minimal (10-15% of SMEs)
- Email: Various (GoDaddy, 123-reg, personal Gmail)
- Files: Local + Dropbox/iCloud
- Devices: Whatever they bought
- Auth: Nothing centralised
- Best approach: Migrate to M365 or Google Workspace first (separate project), then apply Pattern 1 or 2

### Pattern 4: Trades / Sole Trader (Amplified £99 tier)
- Email: Phone-based (Gmail/Outlook app)
- Files: Phone photos + maybe a laptop
- Devices: 1 phone + maybe 1 laptop
- Auth: Whatever the phone defaults to
- Best approach: Secure the email account (passkeys on phone), ensure phone has screen lock + encryption, check for obvious router issues at their premises

---

*Document version: 1.0 — Client Zero testing in progress. This document will be updated with findings from Ewan's setup and refined into the final playbook after testing is complete.*

---

# Part 3 — Security Implementation Runbook — Client Zero
## Ewan's Setup: Byker Business Help / Amplified Partners

**Version:** 1.0  
**Date:** 15 March 2026  
**Author:** Perplexity Computer (security session)  
**Rule:** Two tries to fix, then search SearXNG. Document everything.  
**Methodology:** Step by step, one bit at a time, noting problems for the next AI.

---

## Executive Summary

This runbook covers every security fix identified in the discovery audit, ordered by priority. Each step has exact commands, verification checks, rollback procedures, and estimated time. The entire plan is designed to be executed with zero friction to Ewan or his clients.

### Priority Order

| # | Fix | Priority | Time | Needs Ewan? | Status |
|---|-----|----------|------|-------------|--------|
| 1 | SPF record for amplifiedpartners.ai | URGENT | 5 min | YES — Namecheap login | PENDING |
| 2 | DMARC record for amplifiedpartners.ai | URGENT | 5 min | YES — Namecheap login | PENDING |
| 3 | DMARC upgrade for bykerbusinesshelp.ai | MEDIUM | 5 min | YES — Namecheap login | PENDING |
| 4 | Security headers — amplifiedpartners.ai (Netlify) | MEDIUM | 15 min | YES — or I can PR via GitHub | PENDING |
| 5 | Security headers — bykerbusinesshelp.ai (LiteSpeed) | MEDIUM | 15 min | YES — cPanel .htaccess | PENDING |
| 6 | Mac Mini device audit & hardening | MEDIUM | 45 min | YES — local access or SSH | PENDING |
| 7 | Beast server security audit | HIGH | 60 min | YES — SSH key | PENDING |
| 8 | Beast SSH hardening | HIGH | 30 min | YES — SSH access | PENDING |
| 9 | Beast Docker network isolation | MEDIUM | 45 min | YES — SSH access | PENDING |
| 10 | Beast firewall (UFW) | HIGH | 30 min | YES — SSH access | PENDING |

**Total estimated time: ~4.5 hours** (front-loaded: Fixes 1-3 take 15 minutes if Ewan does them live)

---

## Phase 1: Email Security (URGENT — Can Be Done Tonight)

These are the most critical fixes. amplifiedpartners.ai currently has NO SPF or DMARC, meaning anyone can send emails pretending to be @amplifiedpartners.ai.

### Fix 001: Add SPF Record to amplifiedpartners.ai

**Why:** Without SPF, anyone on the internet can forge emails from @amplifiedpartners.ai. Gmail and other providers may also start rejecting legitimate emails from this domain.

**Risk if we don't fix:** Someone sends a fake invoice from ewan@amplifiedpartners.ai to a client. Client pays the wrong person. This is the #1 attack vector for small businesses.

**What Ewan needs to do:**

1. Log into Namecheap: https://www.namecheap.com/myaccount/login/
2. Click **Domain List** on the left sidebar
3. Find **amplifiedpartners.ai** and click **Manage**
4. Click the **Advanced DNS** tab at the top
5. Click **Add New Record**
6. Set:
   - **Type:** TXT Record
   - **Host:** `@`
   - **Value:** `v=spf1 include:_spf.google.com ~all`
   - **TTL:** Automatic
7. Click **Save All Changes**

**Verification (run after 30 minutes):**
```bash
python3 -c "import dns.resolver; print([str(r) for r in dns.resolver.resolve('amplifiedpartners.ai', 'TXT')])"
```
Expected: Should show `v=spf1 include:_spf.google.com ~all` in the output.

**Rollback:** Delete the TXT record in Namecheap Advanced DNS.

**Time:** 5 minutes

**Notes:**
- Using `~all` (softfail) not `-all` (hardfail) for safety — legitimate mail still delivers even if misconfigured
- Once confirmed working for 2 weeks, can upgrade to `-all`
- Google Workspace DKIM is already configured and working (confirmed in audit)

---

### Fix 002: Add DMARC Record to amplifiedpartners.ai

**Why:** DMARC tells receiving mail servers what to do when they get email that fails SPF/DKIM checks. Without it, spoofed emails are silently delivered.

**What Ewan needs to do:**

1. Still in Namecheap Advanced DNS for amplifiedpartners.ai
2. Click **Add New Record**
3. Set:
   - **Type:** TXT Record
   - **Host:** `_dmarc`
   - **Value:** `v=DMARC1; p=none; rua=mailto:ewan@amplifiedpartners.ai`
   - **TTL:** Automatic
4. Click **Save All Changes**

**Verification (run after 30 minutes):**
```bash
python3 -c "import dns.resolver; print([str(r) for r in dns.resolver.resolve('_dmarc.amplifiedpartners.ai', 'TXT')])"
```
Expected: Should show the DMARC record.

**DMARC Ramp-Up Plan:**
| Week | Policy | What happens |
|------|--------|-------------|
| 1-2 | `p=none` | Monitor only — reports sent to ewan@amplifiedpartners.ai |
| 3-4 | `p=quarantine; pct=25` | 25% of failing emails go to spam |
| 5-6 | `p=quarantine; pct=100` | All failing emails go to spam |
| 7+ | `p=reject` | Failing emails are blocked entirely |

**How to upgrade (week 3):**
- Edit the _dmarc TXT record in Namecheap
- Change value to: `v=DMARC1; p=quarantine; pct=25; rua=mailto:ewan@amplifiedpartners.ai`

**Time:** 5 minutes

---

### Fix 003: Upgrade DMARC on bykerbusinesshelp.ai

**Why:** Currently set to `p=none` which is monitoring-only. DMARC reports are going to ewan@bykerbusinesshelp.ai. Should centralise reporting to amplifiedpartners.ai and eventually ramp to reject.

**Current record:** `v=DMARC1; p=none; rua=mailto:ewan@bykerbusinesshelp.ai`

**What Ewan needs to do:**

1. In Namecheap, go to **bykerbusinesshelp.ai** → **Manage** → **Advanced DNS**
2. Find the existing _dmarc TXT record
3. Edit the **Value** to: `v=DMARC1; p=none; rua=mailto:ewan@amplifiedpartners.ai`
4. Click **Save All Changes**

**Ramp-Up:** Same schedule as Fix 002 — start quarantine at week 3.

**Time:** 5 minutes

---

## Phase 2: Security Headers

### Understanding the Hosting

Before we can add security headers, we need to know where each site is hosted:

**bykerbusinesshelp.ai:**
- IP: 198.177.120.182
- Likely shared hosting (need to identify provider)
- All 7 security headers missing
- No HSTS

**amplifiedpartners.ai:**
- IP: 75.2.60.5 (AWS Global Accelerator)
- Served via AWS infrastructure
- HSTS already present (good)
- 6 of 7 headers missing

### Fix 004: Hosting Identified (RESOLVED)

**Discovery (15 March 2026):**

**bykerbusinesshelp.ai:**
- **Server:** LiteSpeed (response header: `server: LiteSpeed`, `x-turbo-charged-by: LiteSpeed`)
- **Hosting:** Namecheap shared hosting (server705-4.web-hosting.com)
- **IP:** 198.177.120.182 (AS22612 Namecheap, Inc., Amsterdam NL)
- **Headers can be added via:** `.htaccess` file in the site root
- **Access needed:** cPanel / File Manager (Namecheap hosting dashboard)

**amplifiedpartners.ai:**
- **Server:** Netlify (response header: `server: Netlify`)
- **CDN:** AWS Global Accelerator → Netlify Edge
- **IP:** 75.2.60.5 (anycast)
- **Headers can be added via:** `_headers` file in publish directory OR `netlify.toml`
- **Access needed:** Netlify dashboard or git repo that deploys to Netlify
- **HSTS already present** (max-age=31536000) — only 6 more headers needed

### Fix 005a: Security Headers for amplifiedpartners.ai (Netlify)

**Method:** Create a `_headers` file in the Netlify publish directory, or add to `netlify.toml`.

**Option A — `_headers` file (simplest):**

Create a file called `_headers` in the root of the Netlify site (same directory as index.html):

```
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https: data:; connect-src 'self' https:
```

Note: HSTS is already set by Netlify — no need to add it again.

**Option B — `netlify.toml` (if repo-based deploys):**

```toml
[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "SAMEORIGIN"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"
    Content-Security-Policy = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https: data:; connect-src 'self' https:"
```

**Deployment chain (confirmed via GitHub):**
- Repo: `ewan-dot/amplified-site` (Vite + React + TypeScript)
- Build output: `dist/public`
- No `netlify.toml` or `_headers` file exists yet
- No `public/` folder in the client directory

**Best approach:** Add a `netlify.toml` at the repo root. This is the cleanest method.

**What Ewan needs to do (or I can do via GitHub CLI):**
1. Add `netlify.toml` to the repo root with the headers config above
2. Commit and push
3. Netlify will auto-redeploy

**Or I can create a PR right now** — just say the word

**CSP Warning:** The Content-Security-Policy includes `'unsafe-inline'` and `'unsafe-eval'` because most website builders (React, Next.js, etc.) need them. If the site is static HTML only, these can be removed for tighter security. Test after deploying — if the site breaks, the CSP is too strict.

**Verification:**
```bash
curl -sI https://amplifiedpartners.ai | grep -iE "x-content|x-frame|content-security|x-xss|referrer|permissions"
```

**Time:** 15 minutes

---

### Fix 005b: Security Headers for bykerbusinesshelp.ai (Namecheap/LiteSpeed)

**Method:** Add an `.htaccess` file in the site's root directory on Namecheap shared hosting.

**What Ewan needs to do:**

1. Log into Namecheap hosting: https://www.namecheap.com/myaccount/login/
2. Go to **Hosting List** → find bykerbusinesshelp.ai → **Go to cPanel**
3. Open **File Manager** → navigate to the site's root directory (usually `public_html/`)
4. If `.htaccess` already exists, edit it. If not, create a new file called `.htaccess`
5. Add these lines (at the top or bottom, doesn't matter):

```apache
# Security Headers — Added by Amplified Security
<IfModule mod_headers.c>
  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set X-XSS-Protection "1; mode=block"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
  Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https: data:; connect-src 'self' https:"
</IfModule>
```

**LiteSpeed note:** LiteSpeed is Apache-compatible and supports `.htaccess` files with `mod_headers` directives. If it doesn't work, the hosting may have `mod_headers` disabled — contact Namecheap support.

**Verification:**
```bash
curl -sI https://bykerbusinesshelp.ai | grep -iE "strict-transport|x-content|x-frame|content-security|x-xss|referrer|permissions"
```

**Rollback:** Delete or comment out the added lines in `.htaccess`.

**Time:** 15 minutes

---

## Phase 3: Mac Mini Device Hardening

### Fix 006: Mac Mini Security Audit

This needs to be run locally on the Mac Mini. Ewan can either:
- Run the commands himself and paste the output
- Give us SSH access to the Mac Mini
- Share the screen via remote session

**Audit script (run in Terminal on Mac Mini):**

```bash
#!/bin/bash
echo "=== MAC MINI SECURITY AUDIT ==="
echo "Date: $(date)"
echo ""

echo "--- macOS Version ---"
sw_vers
echo ""

echo "--- FileVault Status ---"
fdesetup status
echo ""

echo "--- Firewall Status ---"
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
echo ""

echo "--- Screen Lock Settings ---"
sysadminctl -screenLock status 2>/dev/null || echo "Check: System Settings > Lock Screen"
echo ""

echo "--- Gatekeeper Status ---"
spctl --status
echo ""

echo "--- Auto-Update Status ---"
defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled 2>/dev/null
defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticDownload 2>/dev/null
echo ""

echo "--- SIP (System Integrity Protection) ---"
csrutil status
echo ""

echo "--- Remote Login (SSH) ---"
systemsetup -getremotelogin 2>/dev/null || echo "Check: System Settings > General > Sharing"
echo ""

echo "--- Sharing Services ---"
echo "Screen Sharing:"
defaults read /var/db/launchd.db/com.apple.launchd/overrides.plist com.apple.screensharing 2>/dev/null || echo "Check manually"
echo ""

echo "--- Admin Accounts ---"
dscl . -read /Groups/admin GroupMembership
echo ""

echo "--- Installed Browsers ---"
ls /Applications/ | grep -iE "chrome|firefox|safari|brave|edge|arc"
echo ""

echo "--- SSH Keys ---"
ls -la ~/.ssh/ 2>/dev/null
echo ""

echo "--- Listening Ports ---"
lsof -iTCP -sTCP:LISTEN -n -P 2>/dev/null | head -20
echo ""

echo "=== END AUDIT ==="
```

**What we're checking and why:**

| Check | What we want | CE Requirement? |
|-------|-------------|-----------------|
| macOS version | Latest (Sequoia 15.3+) | YES — must be supported OS |
| FileVault | ON | YES — encryption at rest |
| Firewall | ON | YES — boundary firewall |
| Screen lock | 5 min or less | YES — access control |
| Gatekeeper | Enabled | YES — malware protection |
| Auto-updates | ON | YES — patch management |
| SIP | Enabled | Best practice |
| SSH | OFF unless needed | Best practice |
| Admin accounts | Minimal | Best practice |

**Hardening steps (after audit):**

1. **If FileVault is OFF:**
   - System Settings → Privacy & Security → FileVault → Turn On
   - SAVE THE RECOVERY KEY — print it, store it somewhere physical
   - Encryption runs in background, no disruption

2. **If Firewall is OFF:**
   - System Settings → Network → Firewall → Turn On
   - Options: Allow built-in software, allow signed software
   - Zero friction — this just blocks unsolicited incoming connections

3. **Screen lock (if >5 min):**
   - System Settings → Lock Screen → Require password after screen saver or display off → Immediately
   - Start Screen Saver after → 5 minutes

4. **Auto-updates (if OFF):**
   - System Settings → General → Software Update → Automatic Updates → ON
   - Enable all sub-options (Check, Download, Install macOS, Install App Store, Install Security Responses)

**Time:** 45 minutes

---

## Phase 4: Beast Server Security

### Fix 007: Beast SSH Audit

**Needs:** SSH access to Beast (135.181.161.131)

**What we'll check:**

```bash
# SSH configuration
cat /etc/ssh/sshd_config | grep -E "PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|Port|MaxAuthTries|AllowUsers"

# Current authorized keys (clean up stale entries)
cat /root/.ssh/authorized_keys

# Active SSH sessions
who
last -10

# Fail2ban or similar
systemctl status fail2ban 2>/dev/null || echo "fail2ban not installed"

# Login attempts
grep "Failed password" /var/log/auth.log 2>/dev/null | tail -10
```

**What we want to see/fix:**

| Setting | Desired | Why |
|---------|---------|-----|
| PermitRootLogin | `prohibit-password` | Key-only root access |
| PasswordAuthentication | `no` | Force key-based auth |
| PubkeyAuthentication | `yes` | Allow SSH keys |
| MaxAuthTries | `3` | Limit brute force |
| Authorized keys | Only active, known keys | Remove stale sessions |

**Known state from memory:**
- 6 entries in authorized_keys (one duplicate)
- Keys for: Mac Mini, cowork sessions (x3), perplexity session
- Need to clean out stale session keys

**Hardening script:**
```bash
#!/bin/bash
echo "=== BEAST SSH HARDENING ==="

# Backup current config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%Y%m%d)

# Harden SSH
sed -i 's/^#*PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config
sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/^#*MaxAuthTries.*/MaxAuthTries 3/' /etc/ssh/sshd_config

# Test config before restarting
sshd -t && echo "Config OK" || echo "CONFIG ERROR — DO NOT RESTART"

# Only restart if config is valid
sshd -t && systemctl restart sshd
echo "SSH hardened. Test a new connection BEFORE closing this one."
```

**CRITICAL WARNING:** Always test SSH in a NEW terminal before closing the current session. If the config is wrong, you get locked out.

---

### Fix 008: Beast Firewall (UFW)

```bash
#!/bin/bash
echo "=== BEAST FIREWALL SETUP ==="

# Install UFW if not present
apt-get install -y ufw

# Default policies
ufw default deny incoming
ufw default allow outgoing

# Allow SSH (MUST do this before enabling)
ufw allow 22/tcp comment 'SSH'

# Allow HTTP/HTTPS (Traefik)
ufw allow 80/tcp comment 'HTTP'
ufw allow 443/tcp comment 'HTTPS'

# Allow Docker internal communication
# (UFW and Docker can conflict — see note below)

# Show rules before enabling
ufw status numbered

# Enable (will prompt — answer y)
ufw enable

echo "=== FIREWALL ENABLED ==="
ufw status verbose
```

**Docker + UFW Warning:**
Docker modifies iptables directly, which can bypass UFW rules. This is a known issue. Solutions:
1. Use `DOCKER_OPTS="--iptables=false"` (breaks Docker networking)
2. Use `ufw-docker` utility (recommended)
3. Accept that Docker ports are managed by Docker, not UFW

**We'll research this further before implementing.** The safest approach is:
- UFW for non-Docker services (SSH)
- Traefik as the single entry point for all Docker services
- No Docker services publish ports directly to 0.0.0.0

---

### Fix 009: Beast Docker Network Audit

```bash
#!/bin/bash
echo "=== DOCKER NETWORK AUDIT ==="

# List all networks
docker network ls

# Check which containers are on which networks
for net in $(docker network ls --format '{{.Name}}'); do
    echo "--- Network: $net ---"
    docker network inspect $net --format '{{range .Containers}}{{.Name}} {{end}}' 2>/dev/null
    echo ""
done

# Check for containers publishing ports to 0.0.0.0
echo "--- CONTAINERS WITH EXPOSED PORTS ---"
docker ps --format "table {{.Names}}\t{{.Ports}}" | grep "0.0.0.0"

# Check Traefik configuration
echo "--- TRAEFIK CONFIG ---"
cat /opt/amplified/traefik/traefik.yml 2>/dev/null || echo "Not found at expected path"
cat /opt/amplified/traefik/docker-compose.yml 2>/dev/null || echo "Not found"
```

**What we're looking for:**
- All services should be on `amplified-net` (internal Docker network)
- Only Traefik should publish ports 80/443 to 0.0.0.0
- No database ports (5432, 6379, etc.) should be exposed externally
- Ollama (11434) should NOT be on 0.0.0.0

---

## Phase 5: Ongoing Monitoring & CE Preparation

### Fix 010: Set Up DMARC Report Monitoring

After DMARC records are in place, aggregate reports will arrive at ewan@amplifiedpartners.ai. These are XML files that need parsing.

**Options:**
1. **Manual:** Read XML reports in email (tedious)
2. **Free service:** Use dmarcian.com free tier or mxtoolbox.com/dmarc
3. **Self-hosted:** Parse with a script on the Beast (long-term)

**Recommendation:** Start with manual review for 2 weeks. If volume is low (which it will be for these domains), Ewan can just check email. Once we move to p=quarantine, consider a proper monitoring tool.

---

### CE Readiness Checklist (from Process Sheet)

| CE Requirement | bykerbusinesshelp.ai | amplifiedpartners.ai | Beast | Mac Mini |
|---------------|---------------------|---------------------|-------|---------|
| Boundary firewall | ? (hosting) | HSTS ✓ | PENDING | PENDING |
| Secure configuration | ? | ? | PENDING | PENDING |
| Access control | Google Workspace | Google Workspace | SSH keys ✓ | PENDING |
| Malware protection | N/A (hosted) | N/A (hosted) | PENDING | PENDING |
| Patch management | N/A (hosted) | N/A (hosted) | PENDING | PENDING |
| Email security (SPF) | GREEN ✓ | RED — Fix 001 | N/A | N/A |
| Email security (DMARC) | AMBER | RED — Fix 002 | N/A | N/A |
| Email security (DKIM) | GREEN ✓ | GREEN ✓ | N/A | N/A |

---

## What I Can Do Right Now (Without Ewan)

| Action | Status |
|--------|--------|
| ✅ Fresh DNS/email/header audit | DONE — findings confirmed identical |
| ✅ Beast SearXNG connectivity test | DONE — working, 26 results |
| ✅ Research best practices for each fix | DONE |
| ✅ Build this implementation runbook | DONE |
| ✅ Update knowledge base | DOING NOW |
| ⏳ Identify hosting for bykerbusinesshelp.ai | Can try via HTTP response headers |
| ⏳ Check amplifiedpartners.ai hosting chain | Can try via HTTP response headers |

## What Needs Ewan

| Action | What Ewan needs to do | Time |
|--------|----------------------|------|
| Fix 001-003: DNS records | Log into Namecheap, add/edit 3 TXT records | 15 min |
| Fix 004-005: Security headers | Tell us where sites are hosted | 2 min |
| Fix 006: Mac Mini audit | Run audit script in Terminal OR give SSH | 10 min |
| Fix 007-010: Beast server | Provide SSH key for this Perplexity session | 5 min |

**Total Ewan time: ~30 minutes** (spread across sessions if needed)

---

## Problems Encountered This Session

| Problem | Solution | For Next AI |
|---------|----------|-------------|
| dig/nslookup not in Perplexity sandbox | Use Python dnspython library | Always use `pip install dnspython` |
| apt-get install fails (no sudo) | Python libraries via pip instead | Don't try to install system packages |
| fetch_url fails on Beast SearXNG | Use `bash` with `curl` instead | SearXNG skill documents this |
| Can't SSH to Beast from Perplexity sandbox | Need Ewan to paste outputs or add SSH key | Sandbox is isolated — no direct server access |
| Can't log into Namecheap | Give Ewan exact instructions with screenshots | DNS changes MUST be done by domain owner |

---

## Knowledge Base Updates

All findings from this session are documented in:
- `security-knowledge-base.md` — gotchas, fixes applied, search cache
- `discovery-audit-results.json` — raw DNS/SSL/header data
- This file (`security-implementation-runbook.md`) — the execution plan

---

*Every problem documented here helps the next business owner avoid the same friction.*

---

# Part 4 — Security Knowledge Base

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

---

# Part 5 — Mac vs Windows: What Actually Needs Fixing
## Honest Assessment for Amplified Partners Client Security

**Date:** 15 March 2026  
**Research sources:** NCSC, IASME CE Knowledge Hub, AV-Comparatives, Moonlock Lab, SE Labs, Apple Security Docs, Pareto Security, Macworld  
**Rule applied:** Research first, identify problems, find solutions, then act. Don't blanket bomb.

---

## The Bottom Line

**Macs are not invincible, but they're significantly more secure out of the box than Windows.** Most of the "Mac security hardening" advice online is either vendor-driven FUD (selling antivirus) or copy-paste from Windows checklists. A Mac Mini M4 running Sequoia with default settings is already doing 70% of what Cyber Essentials requires. A Beelink N150 running Windows 11 Home needs significantly more work.

---

## What macOS Already Handles (Out of the Box)

| Protection | macOS (Sequoia) | Enabled by Default? | Notes |
|-----------|----------------|-------------------|-------|
| **XProtect** (antivirus) | Signature-based malware scanning | YES — automatic, silent | Updates via background, no user action needed |
| **XProtect Remediator** | Removes known malware | YES — runs silently | Scans and cleans periodically |
| **Gatekeeper** | Blocks unsigned/unnotarized apps | YES | User must deliberately bypass via System Settings |
| **SIP** (System Integrity Protection) | Prevents system file modification | YES | Cannot be disabled without booting to Recovery |
| **App Sandbox** | Isolates App Store apps | YES (for App Store apps) | Each app runs in its own sandbox |
| **Notarization** | Apple scans all distributed apps for malware | YES | Apps outside App Store still get scanned |
| **Rapid Security Responses** | Emergency patches outside normal updates | YES | Delivered automatically |
| **Secure Boot** (Apple Silicon) | Verifies boot chain integrity | YES — hardware level | M4 chip handles this in silicon |
| **Memory protections** (ASLR, DEP) | Prevents exploitation | YES | Built into the architecture |
| **Privacy controls** (TCC) | Per-app permissions for camera, mic, files | YES | User must explicitly grant access |

**What this means:** A Mac Mini M4 sitting on Ewan's desk with factory settings already has more security than most Windows machines with third-party antivirus installed.

---

## What macOS Does NOT Handle by Default

These are the **only things that actually need checking or enabling:**

| Thing | Default State | Needs Action? | CE Required? |
|-------|--------------|---------------|-------------|
| **Firewall** | OFF | YES — turn it on | YES |
| **FileVault** (disk encryption) | OFF on most setups | MAYBE — check first | YES (for CE+, recommended for CE) |
| **Auto-updates** | Usually ON, but check | CHECK — verify it's on | YES |
| **Screen lock timeout** | Varies (often 20+ min) | CHECK — should be ≤5 min for CE | YES |
| **Auto-login** | Sometimes ON | CHECK — should be OFF | YES |
| **Sharing services** | Mostly OFF | CHECK — disable any that are on | Best practice |

That's it. That's the real list for a Mac. Six things to check, most of which are a single toggle.

---

## The Antivirus Question (Settled)

### Does a Mac need third-party antivirus?

**For Cyber Essentials:** NO. The [IASME CE Knowledge Hub](https://ce-knowledge-hub.iasme.co.uk/space/CEKH/2577498118) explicitly states:

> "Both Windows Defender and macOS XProtect can be used to meet the anti-malware requirement for question A8.1"

**XProtect is officially CE-compliant.** No third-party antivirus needed.

### What about XProtect's limitations?

Yes, XProtect is signature-based and misses zero-day threats. But here's the context:

- The [Moonlock 2025 threat report](https://moonlock.com/2025-macos-threat-report) headlines "66% of Mac users encountered a cyber threat" — but this includes **phishing, scam emails, data breaches, and account compromises**. Actual malware infection rates are not provided. Malware is listed as the **second** most common threat after personal data breaches.
- [AV-Comparatives 2025](https://www.av-comparatives.org/tests/mac-security-test-review-2025/) tested third-party AV against 899 Mac malware samples. They didn't test XProtect at all because it operates at a different layer (system-level, before apps run). The best third-party tools got 99.4-100% — but they're testing against **known malware samples**, which is exactly what XProtect does too.
- [SE Labs](https://selabs.uk/blog/the-mac-myth-why-your-ceos-laptop-might-be-the-weakest-link/) found 0% protection from macOS against 11 targeted attack scenarios — but these were **sophisticated, multi-stage, targeted attacks** mimicking nation-state actors. This is not the threat model for a small business in Newcastle.
- The **real attack vectors** for Macs in 2025-2026 are: fake software updates, malvertising, pirated apps, and social engineering (ClickFix scams where users paste commands into Terminal). None of these are stopped by antivirus — they're stopped by **not being daft**.

### For Ewan's clients:

| Client type | Recommendation |
|-------------|---------------|
| Mac user, App Store + trusted downloads only | XProtect is sufficient. No third-party AV needed. |
| Mac user, downloads from various sources | XProtect sufficient, but consider free Avast/AVG (100% detection in AV-Comparatives) |
| Mac user, handles highly sensitive data or crypto | Consider paid EDR (Intego, CrowdStrike) |
| Any user who installs pirated software | Software not recognised — address the root cause, not the symptom |

---

## The Beelink N150 (Windows) — Genuinely Different Story

The Beelink N150 runs **Windows 11 Home** with an Intel N150 processor. Windows needs significantly more attention:

| Thing | Windows Default | Action Needed | Mac Equivalent |
|-------|----------------|--------------|----------------|
| **Windows Defender** | ON and active | Verify it's on, real-time protection enabled | XProtect (already handled) |
| **Windows Firewall** | ON by default | Verify, check rules | Mac firewall is OFF by default — Windows wins here |
| **BitLocker** | OFF (Home edition may not have it) | PROBLEM — Win 11 Home has "Device Encryption" but not full BitLocker. Needs checking. | FileVault (needs enabling) |
| **Auto-updates** | Usually ON | Verify Windows Update settings | Same |
| **Screen lock** | Varies | Set timeout | Same |
| **Admin accounts** | First account is admin | Create standard user account for daily use | Mac is the same, but less risky due to SIP |
| **AppLocker** | Not available on Home | Can't use — Home edition limitation | Gatekeeper handles this |
| **Macro blocking** | Not blocked by default | Block Office macros from internet | Not applicable on Mac (no Office macro risk) |
| **SMB/NetBIOS** | ON | Should be disabled if not needed | Not applicable |
| **Remote Desktop** | Usually OFF | Verify OFF | Not applicable |
| **PowerShell execution policy** | Unrestricted | Should be restricted | Not applicable |
| **Third-party app control** | No built-in (no AppLocker on Home) | Manual vigilance | Gatekeeper + Notarization |

### Windows-Specific Risks That Don't Apply to Macs

1. **Ransomware:** 95%+ of ransomware targets Windows. Mac ransomware exists but is extremely rare.
2. **Active Directory attacks:** Not applicable to a standalone mini PC, but the Windows attack surface is fundamentally larger.
3. **Macro malware:** Office macros are one of the top infection vectors for Windows. macOS Office can run macros but it's far less common.
4. **Living-off-the-land:** PowerShell, WMI, WMIC — Windows has dozens of built-in tools that attackers abuse. macOS has some (Terminal, osascript) but the ecosystem is much smaller.
5. **Driver-level attacks:** Windows has a much larger driver attack surface. Apple Silicon Macs have a locked-down boot chain.
6. **Legacy protocol exposure:** SMB, NetBIOS, LLMNR — Windows exposes network protocols that Macs don't.

### Windows 11 Home Limitations for CE

- **No BitLocker** (only "Device Encryption" which requires TPM 2.0 and UEFI Secure Boot — the Beelink N150 may or may not have this)
- **No AppLocker** (application whitelisting)
- **No Group Policy Editor** (gpedit.msc — can't enforce policies)
- **No Hyper-V** (no Virtualization-Based Security)

For CE compliance, Windows 11 Home is acceptable but has limitations. If the Beelink is doing anything security-sensitive, Windows 11 Pro would be better.

---

## Honest Summary: What to Do, What to Skip, What's Theatre

### Mac Mini M4 (Ewan's Primary Workstation)

| Action | Do It? | Why |
|--------|--------|-----|
| Run audit to CHECK current state | YES | 2 minutes. Know what you're working with. |
| Turn on firewall (if off) | YES | One toggle. CE requires it. |
| Check FileVault (if off, enable) | YES | One toggle + save recovery key. CE requires encryption. |
| Verify auto-updates are on | YES | 10 seconds to check. |
| Set screen lock to ≤5 min | YES | One setting. |
| Disable auto-login (if on) | YES | One setting. |
| Disable sharing services | CHECK | Only if any are enabled. |
| Install third-party antivirus | NO — SKIP | Theatre. XProtect is CE-compliant. Apple says it's enough. IASME says it's enough. |
| Install third-party firewall | NO — SKIP | Theatre. macOS firewall is sufficient. |
| Change DNS settings | NO — SKIP | Known gotcha: breaks public Wi-Fi captive portals. |
| Install VPN | NO — SKIP | Known gotcha: causes location lockdowns. |
| Run a hardening script | NO — SKIP | Blanket bombing. Most settings are already correct. |
| Enable stealth mode on firewall | OPTIONAL | Hides the Mac from network scans. Nice-to-have, not required. |

**Total time for Mac: 5-10 minutes** (not 45 minutes as I previously estimated)

### Beelink N150 (Windows — Always-On Mini PC)

| Action | Do It? | Why |
|--------|--------|-----|
| Check Windows 11 version is current | YES | Must be supported version for CE. |
| Verify Windows Defender is active + real-time on | YES | Essential. CE requires malware protection. |
| Verify Windows Firewall is on | YES | Should be by default, but verify. |
| Check Device Encryption / BitLocker | YES | May not be available on Home. Need to check. |
| Verify auto-updates are on | YES | CE requires patching within 14 days. |
| Set screen lock timeout | YES | CE requires it. |
| Create standard user account | YES | Don't run daily tasks as admin. |
| Disable unnecessary services (SMB, NetBIOS if not needed) | YES | Windows-specific attack surface. |
| Block Office macros from internet | YES if Office installed | Top infection vector. |
| Check PowerShell execution policy | YES | Restrict if unrestricted. |
| Disable Remote Desktop (if on) | YES | Unless actively needed. |
| Install third-party antivirus | NO — SKIP | Windows Defender is CE-compliant and scores 99.8%+ in tests. |

**Total time for Windows: 20-30 minutes** (more work than Mac because more things are exposed by default)

### The Beast (Ubuntu Server)

Different category entirely — it's a server, not a workstation. The previous runbook covers this properly (SSH hardening, firewall, Docker audit). No desktop security frameworks apply.

---

## For Client Deployments: The Audit Script

The audit should be different for Mac vs Windows. Not a blanket script.

### Mac Audit (What Actually Matters)

```bash
#!/bin/bash
echo "=== MAC SECURITY CHECK ==="
echo "Only checking things that matter."
echo ""

# 1. Firewall
echo "1. Firewall:"
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# 2. FileVault
echo "2. FileVault:"
fdesetup status

# 3. macOS version (is it current?)
echo "3. macOS version:"
sw_vers | grep ProductVersion

# 4. Auto-updates
echo "4. Auto-updates:"
defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled 2>/dev/null && echo "  Check: ON" || echo "  Check: needs verification"

# 5. Gatekeeper (should always be on)
echo "5. Gatekeeper:"
spctl --status

# 6. SIP (should always be on)
echo "6. SIP:"
csrutil status

echo ""
echo "=== DONE ==="
echo "If 1-4 are green, this Mac is CE-compliant for device security."
echo "Items 5-6 should always be enabled — if they're not, something is wrong."
```

### Windows Audit (More to Check)

```powershell
Write-Host "=== WINDOWS SECURITY CHECK ===" -ForegroundColor Cyan

# 1. Windows version
Write-Host "`n1. Windows Version:"
(Get-ComputerInfo).WindowsProductName
(Get-ComputerInfo).OsVersion

# 2. Windows Defender
Write-Host "`n2. Windows Defender:"
Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated

# 3. Firewall
Write-Host "`n3. Firewall:"
Get-NetFirewallProfile | Select-Object Name, Enabled

# 4. BitLocker / Device Encryption
Write-Host "`n4. Disk Encryption:"
Get-BitLockerVolume -MountPoint C: -ErrorAction SilentlyContinue | Select-Object VolumeStatus, ProtectionStatus
if ($?) {} else { Write-Host "  BitLocker not available — check Device Encryption in Settings" }

# 5. Auto-updates
Write-Host "`n5. Auto-updates:"
$AU = (New-Object -ComObject Microsoft.Update.AutoUpdate).EnableService
Write-Host "  Auto Update enabled: $($AU)"

# 6. Admin account check
Write-Host "`n6. Current user is admin?"
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
Write-Host "  Running as admin: $isAdmin"

# 7. Remote Desktop
Write-Host "`n7. Remote Desktop:"
(Get-ItemProperty 'HKLM:\System\CurrentControlSet\Control\Terminal Server').fDenyTSConnections

# 8. SMB v1 (should be disabled)
Write-Host "`n8. SMB v1 (should be disabled):"
Get-SmbServerConfiguration | Select-Object EnableSMB1Protocol

Write-Host "`n=== DONE ===" -ForegroundColor Cyan
```

---

## What I Should Have Done Differently

My previous execution prompt was a blanket bomb:
- 45-minute Mac audit checking 15+ things when only 6 matter
- Recommending a hardening script when most settings are already correct
- Treating Mac and Windows identically when they have fundamentally different security postures
- Not distinguishing between CE requirements and nice-to-haves

**The right approach:** Run the focused audit (6 checks on Mac, 8 on Windows), fix only what's actually off, document what was already fine, move on.

---

## Sources

- [IASME CE Knowledge Hub — Malware Protection FAQ](https://ce-knowledge-hub.iasme.co.uk/space/CEKH/2577498118) — XProtect is CE-compliant
- [NCSC macOS Security Guidance](https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides/macos) — Official UK govt Mac recommendations
- [NCSC Windows Security Guidance](https://www.ncsc.gov.uk/collection/device-security-guidance/platform-guides/windows) — Official UK govt Windows recommendations
- [Pareto Security — Mac CE+ Requirements](https://paretosecurity.com/blog/mac-cyber-essentials-plus/) — Specific CE+ Mac checklist
- [Moonlock 2025 macOS Threat Report](https://moonlock.com/2025-macos-threat-report) — Actual threat statistics
- [AV-Comparatives Mac Security Test 2025](https://www.av-comparatives.org/tests/mac-security-test-review-2025/) — Detection rates
- [SE Labs — The Mac Myth](https://selabs.uk/blog/the-mac-myth-why-your-ceos-laptop-might-be-the-weakest-link/) — Targeted attack testing
- [Macworld — Do Macs Need Antivirus 2026](https://www.macworld.com/article/670537/do-macs-need-antivirus.html) — Consumer perspective
- [Cyber Compliance — CE v3.2 Changes](https://cybercompliance.org.uk/blogs/news/cyber-essentials-in-july-2025-what-s-new-why-it-matters-and-how-to-get-certified) — Current CE requirements

---

# Part 6 — Security Execution Prompt v2
## For Perplexity Desktop (Mac Mini)

**Date:** 15 March 2026  
**Context:** Security implementation for Ewan's setup (Client Zero). Research-first approach — only fix what needs fixing.

---

## Rules

1. Two tries to fix, then search SearXNG: `curl -s 'https://search.beast.amplifiedpartners.ai/search?q=YOUR+QUERY&format=json'`
2. Document every problem and solution
3. Don't blanket bomb. Check first, fix only what's off.
4. Mac and Windows are different — treat them differently.

---

## TASK 1: Mac Mini Security Check (5 minutes)

The Mac Mini M4 is already mostly secure out of the box. Only 6 things to check:

```bash
#!/bin/bash
echo "=== MAC MINI SECURITY CHECK ==="
echo "Date: $(date)"
echo ""

echo "1. Firewall:"
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

echo "2. FileVault:"
fdesetup status

echo "3. macOS version:"
sw_vers | grep ProductVersion

echo "4. Auto-updates:"
defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled 2>/dev/null && echo "  Auto-check: ON" || echo "  Auto-check: NEEDS VERIFICATION"
defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticDownload 2>/dev/null && echo "  Auto-download: ON" || echo "  Auto-download: NEEDS VERIFICATION"

echo "5. Gatekeeper:"
spctl --status

echo "6. SIP:"
csrutil status

echo ""
echo "=== RESULTS ==="
echo "Items 5-6 should always be enabled on Apple Silicon — if not, something is wrong."
echo "Items 1-4 are the only things that might need a toggle."
```

**Only fix what's actually off:**

| If this is off | Fix | Time |
|---------------|-----|------|
| Firewall | System Settings → Network → Firewall → Turn On | 10 sec |
| FileVault | System Settings → Privacy & Security → FileVault → Turn On. SAVE THE RECOVERY KEY. | 2 min |
| Auto-updates | System Settings → General → Software Update → Automatic Updates → all ON | 30 sec |
| Screen lock >5 min | System Settings → Lock Screen → set to 5 min | 10 sec |

**Do NOT install:** third-party antivirus, third-party firewall, VPN, or DNS changers. XProtect is CE-compliant (confirmed by IASME). The Mac's built-in security is doing the job.

---

## TASK 2: Beast Server Audit (SSH)

SSH from this Mac Mini:
```bash
ssh -i ~/.ssh/id_ed25519 root@135.181.161.131
```

Run the focused audit:
```bash
echo "=== BEAST SECURITY AUDIT ==="
echo "Date: $(date)"

echo "--- SSH Config (key settings only) ---"
grep -E "^PermitRootLogin|^PasswordAuthentication|^PubkeyAuthentication|^MaxAuthTries" /etc/ssh/sshd_config
echo "(If PasswordAuthentication is 'yes' or missing, that needs fixing)"

echo "--- Authorized Keys (count and list) ---"
wc -l /root/.ssh/authorized_keys
cat /root/.ssh/authorized_keys | awk '{print $NF}'

echo "--- Firewall ---"
ufw status 2>/dev/null || echo "UFW not installed"

echo "--- Containers with ports on 0.0.0.0 ---"
docker ps --format "{{.Names}}\t{{.Ports}}" | grep "0.0.0.0" | grep -v ":80->\|:443->"

echo "--- Failed SSH logins (last 24h) ---"
grep "Failed password" /var/log/auth.log 2>/dev/null | wc -l || echo "Check journalctl"

echo "=== END ==="
```

**Only fix what's actually wrong.** The key questions:
1. Is PasswordAuthentication set to `no`? If not, fix it.
2. Are there stale SSH keys? Remove them.
3. Are any Docker services exposing ports directly (not through Traefik)? If so, investigate.
4. Is UFW installed and enabled? If not, that's a genuine gap.

---

## TASK 3: Netlify Security Headers

Only if Tasks 1 and 2 are done. Add `netlify.toml` to the `amplified-site` repo:

```bash
cd ~/path/to/amplified-site  # or: git clone git@github.com:ewan-dot/amplified-site.git

cat > netlify.toml << 'EOF'
[build]
  publish = "dist/public"
  command = "npm run build"

[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    X-Frame-Options = "SAMEORIGIN"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "camera=(), microphone=(), geolocation=()"
    Content-Security-Policy = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' https: data:; connect-src 'self' https:; frame-ancestors 'self'"
EOF

git add netlify.toml
git commit -m "Add security headers via netlify.toml"
git push origin main
```

Verify after deploy:
```bash
curl -sI https://amplifiedpartners.ai | grep -iE "x-content|x-frame|content-security|x-xss|referrer|permissions"
```

If the site breaks, revert: `git revert HEAD && git push origin main`

---

## TASK 4: Document What You Found

Save a simple summary of what was already fine and what needed fixing. Don't overcomplicate it.

---

## What NOT To Do

- Do NOT install third-party antivirus on the Mac (XProtect is CE-compliant)
- Do NOT change DNS settings (breaks public Wi-Fi)
- Do NOT enable VPN on personal devices (causes location lockdowns)
- Do NOT touch Namecheap DNS (Ewan does that himself)
- Do NOT run blanket hardening scripts
- Do NOT "harden" things that are already working correctly

---

# Standalone Scripts Index

The following are **separate executable files** — they are not included in this document. They live alongside this document in the workspace and should be used as standalone tools.

| Script | Platform | Purpose | How to Run |
|--------|----------|---------|-----------|
| **amplified-client-audit-mac.sh** | macOS | Full client security audit — checks all CE requirements, produces GREEN/AMBER/RED report, saves log to Desktop | `sudo bash amplified-client-audit-mac.sh` |
| **amplified-client-audit-windows.ps1** | Windows | Full client security audit — checks all CE requirements, produces colour-coded report, saves log to Desktop | Run as Administrator: `Set-ExecutionPolicy Bypass -Scope Process -Force; .\amplified-client-audit-windows.ps1` |
| **just-run-this-v2.sh** | macOS | Quick Mac terminal paste — focused 6-check audit for Perplexity Desktop use, minimal output | Paste directly into Terminal |

These scripts are the **production tools** used for client engagements. The Mac and Windows audit scripts in Part 1 of this document are the source/reference versions — the standalone `.sh` and `.ps1` files are the deployed versions.
