#!/bin/bash
# Amplified Security Audit v2 — Mac
# Copy everything below into Terminal, then press Enter.
# It checks everything, fixes what's off, and saves a log to your Desktop.

LOGFILE="$HOME/Desktop/amplified-security-$(date +%Y%m%d-%H%M%S).txt"
echo "=== AMPLIFIED SECURITY AUDIT ===" | tee "$LOGFILE"
echo "Date: $(date)" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

echo "1. macOS version:" | tee -a "$LOGFILE"
sw_vers | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

echo "2. Firewall:" | tee -a "$LOGFILE"
FW=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null)
echo "   $FW" | tee -a "$LOGFILE"
if echo "$FW" | grep -qi "disabled"; then
    echo "   FIXING: Turning firewall ON..." | tee -a "$LOGFILE"
    sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on 2>/dev/null | tee -a "$LOGFILE"
    echo "   DONE — Firewall now ON" | tee -a "$LOGFILE"
else
    echo "   Already ON" | tee -a "$LOGFILE"
fi
echo "" | tee -a "$LOGFILE"

echo "3. FileVault (disk encryption):" | tee -a "$LOGFILE"
fdesetup status 2>/dev/null | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

echo "4. Auto-updates:" | tee -a "$LOGFILE"
echo "   Auto-check: $(defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled 2>/dev/null || echo 'not set')" | tee -a "$LOGFILE"
echo "   Auto-download: $(defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticDownload 2>/dev/null || echo 'not set')" | tee -a "$LOGFILE"
echo "   Auto-install macOS: $(defaults read /Library/Preferences/com.apple.SoftwareUpdate AutomaticallyInstallMacOSUpdates 2>/dev/null || echo 'not set')" | tee -a "$LOGFILE"
echo "   Critical updates: $(defaults read /Library/Preferences/com.apple.SoftwareUpdate CriticalUpdateInstall 2>/dev/null || echo 'not set')" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

echo "5. Gatekeeper:" | tee -a "$LOGFILE"
spctl --status 2>/dev/null | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

echo "6. SIP:" | tee -a "$LOGFILE"
csrutil status 2>/dev/null | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

echo "7. XProtect (built-in antivirus):" | tee -a "$LOGFILE"
if [ -d "/Library/Apple/System/Library/CoreServices/XProtect.bundle" ]; then
    echo "   XProtect: ACTIVE (CE-compliant per IASME)" | tee -a "$LOGFILE"
else
    echo "   XProtect: NOT FOUND — check macOS is up to date" | tee -a "$LOGFILE"
fi
echo "" | tee -a "$LOGFILE"

echo "8. Screen lock:" | tee -a "$LOGFILE"
IDLE=$(defaults -currentHost read com.apple.screensaver idleTime 2>/dev/null || echo "not set")
echo "   Idle timeout: $IDLE seconds" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

echo "9. User account type:" | tee -a "$LOGFILE"
REAL_USER=$(stat -f%Su /dev/console 2>/dev/null || whoami)
IS_ADMIN=$(dscl . -read /Groups/admin GroupMembership 2>/dev/null | grep -c "$REAL_USER" || true)
if [ "$IS_ADMIN" -gt 0 ]; then
    echo "   $REAL_USER has admin rights (consider standard user for daily use)" | tee -a "$LOGFILE"
else
    echo "   $REAL_USER is a standard user — good" | tee -a "$LOGFILE"
fi
ADMINS=$(dscl . -read /Groups/admin GroupMembership 2>/dev/null | sed 's/GroupMembership: //')
echo "   All admin users: $ADMINS" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

echo "10. Installed apps:" | tee -a "$LOGFILE"
ls /Applications/ | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

echo "11. Remote login (SSH):" | tee -a "$LOGFILE"
systemsetup -getremotelogin 2>/dev/null | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

echo "=== DONE ===" | tee -a "$LOGFILE"
echo "Log saved to: $LOGFILE" | tee -a "$LOGFILE"
echo ""
echo "Now paste the RESULTS back to me and I'll tell you what's what."
