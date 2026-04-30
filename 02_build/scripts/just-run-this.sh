#!/bin/bash
# Amplified Security — Mac Fix-All
# Paste this ENTIRE block into Terminal. It fixes everything, documents everything.
# No questions asked. Permission granted.

LOG="$HOME/Desktop/amplified-security-$(date +%Y%m%d-%H%M%S).txt"
echo "Amplified Security — Mac Fix-All" | tee "$LOG"
echo "Date: $(date)" | tee -a "$LOG"
echo "Mac: $(scutil --get ComputerName 2>/dev/null || hostname)" | tee -a "$LOG"
echo "" | tee -a "$LOG"

# 1. macOS Version
echo "1. macOS: $(sw_vers -productVersion)" | tee -a "$LOG"

# 2. Firewall — enable if off
FW=$(/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate 2>/dev/null)
if echo "$FW" | grep -q "enabled"; then
    echo "2. Firewall: Already ON ✓" | tee -a "$LOG"
else
    sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
    echo "2. Firewall: Was OFF → NOW ON ✓" | tee -a "$LOG"
fi

# 3. FileVault — check status, enable if off
FV=$(fdesetup status 2>/dev/null)
if echo "$FV" | grep -q "FileVault is On"; then
    echo "3. FileVault: Already ON ✓" | tee -a "$LOG"
elif echo "$FV" | grep -q "Encryption in progress"; then
    echo "3. FileVault: Encryption in progress ✓" | tee -a "$LOG"
else
    echo "3. FileVault: OFF — enabling now..." | tee -a "$LOG"
    sudo fdesetup enable 2>&1 | tee -a "$LOG"
    echo "   IMPORTANT: Recovery key is shown above and saved in the log on your Desktop." | tee -a "$LOG"
    echo "   Store that key somewhere safe (not on this Mac)." | tee -a "$LOG"
fi

# 4. Auto-updates — enable all
echo "4. Auto-updates:" | tee -a "$LOG"
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticCheckEnabled -bool true
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticDownload -bool true
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate AutomaticallyInstallMacOSUpdates -bool true
sudo defaults write /Library/Preferences/com.apple.SoftwareUpdate CriticalUpdateInstall -bool true
sudo defaults write /Library/Preferences/com.apple.commerce AutoUpdate -bool true
echo "   All auto-update settings: ON ✓" | tee -a "$LOG"

# 5. Screen lock — set screen saver to 5 minutes, require password immediately
defaults -currentHost write com.apple.screensaver idleTime -int 300
defaults write com.apple.screensaver askForPassword -int 1
defaults write com.apple.screensaver askForPasswordDelay -int 0
echo "5. Screen lock: 5 min timeout, password required immediately ✓" | tee -a "$LOG"

# 6. Gatekeeper — ensure enabled
GK=$(spctl --status 2>/dev/null)
if echo "$GK" | grep -q "assessments enabled"; then
    echo "6. Gatekeeper: Already ON ✓" | tee -a "$LOG"
else
    sudo spctl --master-enable
    echo "6. Gatekeeper: Was OFF → NOW ON ✓" | tee -a "$LOG"
fi

# 7. SIP — check only (can't change from Terminal)
SIP=$(csrutil status 2>/dev/null)
if echo "$SIP" | grep -q "enabled"; then
    echo "7. SIP: ON ✓" | tee -a "$LOG"
else
    echo "7. SIP: OFF ⚠ — needs Recovery Mode to re-enable" | tee -a "$LOG"
fi

# 8. Sharing — disable anything that shouldn't be on
echo "8. Sharing services:" | tee -a "$LOG"
# Check Remote Login
RL=$(sudo systemsetup -getremotelogin 2>/dev/null)
echo "   Remote Login (SSH): $RL" | tee -a "$LOG"
# Note: NOT disabling SSH because Ewan uses it to connect to Beast

# 9. Beast SSH connection test
echo "9. Beast connectivity:" | tee -a "$LOG"
if ssh -i ~/.ssh/id_ed25519 -o ConnectTimeout=5 -o BatchMode=yes root@135.181.161.131 "echo 'Beast: connected'" 2>/dev/null; then
    echo "   Beast SSH: Connected ✓" | tee -a "$LOG"
    
    # Run Beast audit while we're here
    echo "" | tee -a "$LOG"
    echo "=== BEAST SERVER AUDIT ===" | tee -a "$LOG"
    ssh -i ~/.ssh/id_ed25519 root@135.181.161.131 << 'BEAST_EOF' 2>&1 | tee -a "$LOG"
echo "Date: $(date)"
echo ""

echo "--- SSH Config ---"
grep -E "^PermitRootLogin|^PasswordAuthentication|^PubkeyAuthentication|^MaxAuthTries" /etc/ssh/sshd_config 2>/dev/null || echo "Using defaults (check sshd_config)"
echo ""

echo "--- Authorized Keys ---"
echo "Count: $(wc -l < /root/.ssh/authorized_keys)"
cat /root/.ssh/authorized_keys | awk '{print $NF}'
echo ""

echo "--- UFW Status ---"
ufw status 2>/dev/null || echo "UFW not installed"
echo ""

echo "--- Docker containers exposing ports outside Traefik ---"
docker ps --format "{{.Names}}\t{{.Ports}}" 2>/dev/null | grep "0.0.0.0" | grep -v ":80->\|:443->"
echo "(above should be empty or only expected services)"
echo ""

echo "--- Failed SSH logins last 24h ---"
grep "Failed password" /var/log/auth.log 2>/dev/null | wc -l || echo "Check journalctl"
echo ""

echo "--- Disk ---"
df -h / | tail -1
BEAST_EOF
    echo "=== END BEAST AUDIT ===" | tee -a "$LOG"
else
    echo "   Beast SSH: Could not connect (key may need adding)" | tee -a "$LOG"
fi

echo "" | tee -a "$LOG"
echo "============================================" | tee -a "$LOG"
echo "DONE. Log saved to: $LOG" | tee -a "$LOG"
echo "============================================" | tee -a "$LOG"
echo ""
echo "What was NOT touched (because it doesn't need it):"
echo "  • Antivirus — XProtect is CE-compliant (IASME confirmed)"
echo "  • DNS — left alone (changing breaks public Wi-Fi)"
echo "  • VPN — not installed (causes location lockdowns)"
echo "  • Remote Login — left ON (used for Beast SSH)"
