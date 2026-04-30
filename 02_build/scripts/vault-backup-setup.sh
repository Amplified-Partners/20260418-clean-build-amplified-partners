#!/bin/bash
# ============================================================
# Vault Backup — Mac Mini → Beast (Hetzner)
#
# Syncs ~/vault/ to Beast every 6 hours via cron.
# First run: full copy (~60MB). After that: incremental diffs only.
#
# Run this script ONCE on Mac Mini to set it up.
# ============================================================

set -e

BEAST="root@beast.amplifiedpartners.ai"
REMOTE_DIR="/opt/backups/vault"
LOCAL_VAULT="$HOME/vault"

echo "=== Amplified Partners Vault Backup Setup ==="
echo ""

# 1. Create remote backup directory
echo "[1/4] Creating backup directory on Beast..."
ssh "$BEAST" "mkdir -p $REMOTE_DIR"

# 2. Test rsync
echo "[2/4] Running initial sync (this copies everything)..."
rsync -avz --delete \
    --exclude='.DS_Store' \
    --exclude='*.tmp' \
    "$LOCAL_VAULT/" \
    "$BEAST:$REMOTE_DIR/"

echo "Initial sync complete."

# 3. Create the cron script
echo "[3/4] Creating backup script..."
cat > "$HOME/.backup-vault.sh" << 'SCRIPT'
#!/bin/bash
# Automated vault backup to Beast
LOGFILE="$HOME/.vault-backup.log"
echo "$(date): Starting vault backup" >> "$LOGFILE"
rsync -az --delete \
    --exclude='.DS_Store' \
    --exclude='*.tmp' \
    "$HOME/vault/" \
    "root@beast.amplifiedpartners.ai:/opt/backups/vault/" \
    >> "$LOGFILE" 2>&1
echo "$(date): Backup complete" >> "$LOGFILE"
SCRIPT
chmod +x "$HOME/.backup-vault.sh"

# 4. Add to crontab (every 6 hours)
echo "[4/4] Setting up cron job (every 6 hours)..."
CRON_LINE="0 */6 * * * $HOME/.backup-vault.sh"
(crontab -l 2>/dev/null | grep -v "backup-vault" ; echo "$CRON_LINE") | crontab -

echo ""
echo "=== DONE ==="
echo "Vault backed up to Beast at $REMOTE_DIR"
echo "Cron runs every 6 hours. Logs at ~/.vault-backup.log"
echo ""
echo "To backup other things, add more rsync lines to ~/.backup-vault.sh"
echo "For example:"
echo "  rsync -az ~/agent-stack/ root@beast.amplifiedpartners.ai:/opt/backups/agent-stack/"
echo "  rsync -az ~/amplified-unified/ root@beast.amplifiedpartners.ai:/opt/backups/amplified-unified/"
