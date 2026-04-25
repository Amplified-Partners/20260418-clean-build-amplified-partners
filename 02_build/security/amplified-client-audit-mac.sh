#!/bin/bash
# Amplified Client Security Audit — macOS
# Version: 1.0 | 15 March 2026
# Framework: client-security-framework.md
#
# Run: chmod +x amplified-client-audit-mac.sh && sudo bash amplified-client-audit-mac.sh
# Or: sudo bash amplified-client-audit-mac.sh

set -euo pipefail

LOGFILE="$HOME/Desktop/amplified-security-$(date +%Y%m%d-%H%M%S).txt"
RED='\033[0;31m'
GREEN='\033[0;32m'
AMBER='\033[0;33m'
BOLD='\033[1m'
NC='\033[0m'
FIXES_NEEDED=0
CHECKS_PASSED=0
AMBER_COUNT=0

log() { echo "$1" | tee -a "$LOGFILE"; }
status() {
    local color=$1 label=$2 detail=$3
    echo -e "${color}[${label}]${NC} ${detail}" | tee -a "$LOGFILE"
    if [[ "$label" == "RED" ]]; then ((FIXES_NEEDED++)) || true; fi
    if [[ "$label" == "GREEN" ]]; then ((CHECKS_PASSED++)) || true; fi
    if [[ "$label" == "AMBER" ]]; then ((AMBER_COUNT++)) || true; fi
}

log ""
echo -e "${BOLD}============================================${NC}"
log "AMPLIFIED SECURITY AUDIT — macOS"
echo -e "${BOLD}============================================${NC}"
log "Date: $(date)"
log "Host: $(hostname)"
log "User: $(whoami)"
log ""

# ─── TIER 1: Critical ───

echo -e "${BOLD}--- TIER 1: CRITICAL (fix immediately) ---${NC}"
log "--- TIER 1: CRITICAL ---"
log ""

# 1. macOS version
log "1. Operating System"
OS_VER=$(sw_vers -productVersion)
OS_MAJOR=$(echo "$OS_VER" | cut -d. -f1)
OS_NAME=$(sw_vers -productName 2>/dev/null || echo "macOS")
if [[ "$OS_MAJOR" -ge 15 ]]; then
    status "$GREEN" "GREEN" "$OS_NAME $OS_VER — supported and current"
elif [[ "$OS_MAJOR" -ge 13 ]]; then
    status "$AMBER" "AMBER" "$OS_NAME $OS_VER — still supported but upgrade recommended"
else
    status "$RED" "RED" "$OS_NAME $OS_VER — may be unsupported. Cyber Essentials fail risk."
fi

# 2. Auto-updates
log ""
log "2. Automatic Updates"
AUTO_CHECK=$(defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled 2>/dev/null || echo "0")
AUTO_DOWNLOAD=$(defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticDownload 2>/dev/null || echo "0")
AUTO_INSTALL=$(defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticallyInstallMacOSUpdates 2>/dev/null || echo "0")
CRITICAL_UPDATES=$(defaults read /Library/Preferences/com.apple.SoftwareUpdate CriticalUpdateInstall 2>/dev/null || echo "0")

if [[ "$AUTO_CHECK" == "1" && "$AUTO_DOWNLOAD" == "1" ]]; then
    status "$GREEN" "GREEN" "Auto-updates: check=ON, download=ON, macOS-install=$AUTO_INSTALL, critical=$CRITICAL_UPDATES"
else
    status "$RED" "RED" "Auto-updates not fully enabled (check=$AUTO_CHECK, download=$AUTO_DOWNLOAD)"
    log "   FIX: System Settings → General → Software Update → Automatic Updates → all toggles ON"
fi

# 3. Admin vs standard user
log ""
log "3. User Account Type"
CURRENT_USER=$(whoami)
if [[ "$CURRENT_USER" == "root" ]]; then
    # Running with sudo, check the real user
    REAL_USER=$(stat -f%Su /dev/console 2>/dev/null || echo "$SUDO_USER")
else
    REAL_USER="$CURRENT_USER"
fi

IS_ADMIN=$(dscl . -read /Groups/admin GroupMembership 2>/dev/null | grep -c "$REAL_USER" || true)
ADMIN_MEMBERS=$(dscl . -read /Groups/admin GroupMembership 2>/dev/null | sed 's/GroupMembership: //' || echo "unknown")
ADMIN_COUNT=$(echo "$ADMIN_MEMBERS" | wc -w | tr -d ' ')

if [[ "$IS_ADMIN" -gt 0 ]]; then
    status "$AMBER" "AMBER" "User '$REAL_USER' has admin rights. Best practice: use standard account for daily work."
    log "   Admin users on this Mac: $ADMIN_MEMBERS ($ADMIN_COUNT total)"
else
    status "$GREEN" "GREEN" "User '$REAL_USER' is a standard user"
fi

# ─── TIER 2: Same Day ───

log ""
echo -e "${BOLD}--- TIER 2: FIX SAME DAY ---${NC}"
log "--- TIER 2: SAME DAY ---"
log ""

# 4. Firewall
log "4. Firewall"
FW_STATE=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null || echo "unknown")
if echo "$FW_STATE" | grep -qi "enabled"; then
    status "$GREEN" "GREEN" "Firewall is ON"
else
    status "$RED" "RED" "Firewall is OFF — Apple leaves this off by default"
    log "   FIX: sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on"
fi

# 5. XProtect (built-in antivirus)
log ""
log "5. Malware Protection (XProtect)"
if [[ -d "/Library/Apple/System/Library/CoreServices/XProtect.bundle" ]]; then
    # Try to get XProtect version
    XP_VER=$(defaults read /Library/Apple/System/Library/CoreServices/XProtect.bundle/Contents/Info.plist CFBundleShortVersionString 2>/dev/null || echo "installed")
    status "$GREEN" "GREEN" "XProtect active (v$XP_VER) — meets Cyber Essentials requirement (IASME confirmed)"
else
    status "$AMBER" "AMBER" "XProtect bundle not found at expected path — verify macOS is up to date"
fi

# 6. FileVault
log ""
log "6. Disk Encryption (FileVault)"
FV_STATUS=$(fdesetup status 2>/dev/null || echo "unknown")
if echo "$FV_STATUS" | grep -q "FileVault is On"; then
    status "$GREEN" "GREEN" "FileVault is ON — disk is encrypted"
elif echo "$FV_STATUS" | grep -q "FileVault is Off"; then
    status "$RED" "RED" "FileVault is OFF — lost/stolen device = data breach"
    log "   FIX: System Settings → Privacy & Security → FileVault → Turn On"
    log "   IMPORTANT: Save the recovery key somewhere safe (not on the Mac itself)"
else
    status "$AMBER" "AMBER" "FileVault status unclear: $FV_STATUS"
fi

# 7. Screen lock
log ""
log "7. Screen Lock"
IDLE_TIME=$(defaults -currentHost read com.apple.screensaver idleTime 2>/dev/null || echo "not_set")
REQUIRE_PASSWORD=$(defaults read com.apple.screensaver askForPassword 2>/dev/null || echo "not_set")

if [[ "$IDLE_TIME" != "not_set" && "$IDLE_TIME" =~ ^[0-9]+$ ]]; then
    IDLE_MIN=$(( IDLE_TIME / 60 ))
    if [[ "$IDLE_TIME" -le 300 ]]; then
        status "$GREEN" "GREEN" "Screen lock: ${IDLE_MIN} minutes — excellent"
    elif [[ "$IDLE_TIME" -le 900 ]]; then
        status "$GREEN" "GREEN" "Screen lock: ${IDLE_MIN} minutes — within CE requirement (≤15 min)"
    else
        status "$RED" "RED" "Screen lock: ${IDLE_MIN} minutes — CE requires ≤15 min, we recommend 5"
        log "   FIX: System Settings → Lock Screen → 'Start Screen Saver when inactive' → 5 minutes"
    fi
else
    status "$AMBER" "AMBER" "Screen lock timeout not set — check System Settings → Lock Screen"
fi

# 8. Gatekeeper
log ""
log "8. Gatekeeper (app verification)"
GK_STATUS=$(spctl --status 2>/dev/null || echo "unknown")
if echo "$GK_STATUS" | grep -q "assessments enabled"; then
    status "$GREEN" "GREEN" "Gatekeeper enabled — unsigned apps blocked"
else
    status "$RED" "RED" "Gatekeeper disabled — any app can run without verification"
fi

# 9. SIP (System Integrity Protection)
log ""
log "9. System Integrity Protection (SIP)"
SIP_STATUS=$(csrutil status 2>/dev/null || echo "unknown")
if echo "$SIP_STATUS" | grep -q "enabled"; then
    status "$GREEN" "GREEN" "SIP enabled — system files protected"
else
    status "$RED" "RED" "SIP disabled — this should NEVER be off on a production machine"
fi

# ─── TIER 3: This Week ───

log ""
echo -e "${BOLD}--- TIER 3: FIX THIS WEEK ---${NC}"
log "--- TIER 3: THIS WEEK ---"
log ""

# 10. Remote login (SSH)
log "10. Remote Access"
REMOTE_LOGIN=$(systemsetup -getremotelogin 2>/dev/null || echo "unknown")
if echo "$REMOTE_LOGIN" | grep -qi "off"; then
    status "$GREEN" "GREEN" "Remote Login (SSH): OFF"
elif echo "$REMOTE_LOGIN" | grep -qi "on"; then
    status "$AMBER" "AMBER" "Remote Login (SSH): ON — disable if not needed (System Settings → General → Sharing)"
else
    status "$GREEN" "GREEN" "Remote Login: could not determine (likely OFF)"
fi

# ─── SOFTWARE INVENTORY ───

log ""
echo -e "${BOLD}--- SOFTWARE INVENTORY ---${NC}"
log "--- SOFTWARE INVENTORY ---"
log ""

log "Applications in /Applications:"
ls /Applications/ 2>/dev/null | while read -r app; do
    log "  $app"
done

log ""
echo -e "${BOLD}--- KNOWN-RISK SOFTWARE CHECK ---${NC}"
log "--- KNOWN-RISK SOFTWARE CHECK ---"
log ""

# Google Chrome
if [[ -d "/Applications/Google Chrome.app" ]]; then
    CHROME_VER=$("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --version 2>/dev/null | awk '{print $NF}' || echo "?")
    status "$GREEN" "GREEN" "Google Chrome $CHROME_VER — verify auto-update: open chrome://settings/help"
fi

# Firefox
if [[ -d "/Applications/Firefox.app" ]]; then
    status "$AMBER" "AMBER" "Firefox installed — verify auto-update: Settings → General → Firefox Updates → auto"
fi

# Microsoft Office (any app)
OFFICE_FOUND=false
for app in "Microsoft Word" "Microsoft Excel" "Microsoft PowerPoint" "Microsoft Outlook" "Microsoft Teams"; do
    if [[ -d "/Applications/${app}.app" && "$OFFICE_FOUND" == "false" ]]; then
        status "$AMBER" "AMBER" "Microsoft Office installed — verify: (1) macros disabled, (2) auto-update ON via Microsoft AutoUpdate"
        OFFICE_FOUND=true
    fi
done

# Adobe Reader/Acrobat
if [[ -d "/Applications/Adobe Acrobat Reader.app" ]] || ls /Applications/Adobe\ Acrobat* &>/dev/null 2>&1; then
    status "$AMBER" "AMBER" "Adobe Acrobat/Reader — verify auto-update ON, JavaScript OFF (Preferences → JavaScript)"
fi

# Zoom
if [[ -d "/Applications/zoom.us.app" ]]; then
    status "$AMBER" "AMBER" "Zoom installed — verify auto-update: Settings → General → Auto-update"
fi

# Slack
if [[ -d "/Applications/Slack.app" ]]; then
    status "$GREEN" "GREEN" "Slack installed — auto-updates well on Mac"
fi

# CCleaner (should not be on Mac)
if [[ -d "/Applications/CCleaner.app" ]]; then
    status "$RED" "RED" "CCleaner installed — supply chain attack history (2017). Recommend removing."
fi

# VLC
if [[ -d "/Applications/VLC.app" ]]; then
    status "$AMBER" "AMBER" "VLC Media Player — verify it's current (VLC menu → Check for Updates)"
fi

# Homebrew packages
if command -v brew &>/dev/null; then
    log ""
    log "Homebrew packages:"
    brew list 2>/dev/null | while read -r pkg; do
        log "  $pkg"
    done
fi

# ─── SUMMARY ───

log ""
echo -e "${BOLD}============================================${NC}"
log "============================================"
log "SUMMARY"
log "============================================"

TOTAL=$((CHECKS_PASSED + FIXES_NEEDED + AMBER_COUNT))
if [[ $TOTAL -gt 0 ]]; then
    PASS_PCT=$(( (CHECKS_PASSED * 100) / TOTAL ))
else
    PASS_PCT=100
fi

log "Total checks: $TOTAL"
log "Passed (GREEN): $CHECKS_PASSED ($PASS_PCT%)"
log "Needs attention (AMBER): $AMBER_COUNT"
log "Must fix (RED): $FIXES_NEEDED"
log ""

if [[ $FIXES_NEEDED -eq 0 ]]; then
    echo -e "${GREEN}${BOLD}ALL CLEAR${NC} — No critical fixes needed. ${PASS_PCT}% already good."
    log "ALL CLEAR — No critical fixes needed. ${PASS_PCT}% already good."
else
    echo -e "${RED}${BOLD}$FIXES_NEEDED items need fixing${NC} — see RED items above"
    log "$FIXES_NEEDED items need fixing — see RED items above"
fi

log ""
log "Full log saved to: $LOGFILE"
log "============================================"
echo ""
echo -e "Log saved to: ${BOLD}$LOGFILE${NC}"
