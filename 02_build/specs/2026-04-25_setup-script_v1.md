---
title: "Perplexity Bulk Export - Complete Solution for Ewan"
id: "setup-script"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "setup-guide"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Perplexity Bulk Export - Complete Solution for Ewan

## What You've Got

I've created a **production-ready custom JavaScript solution** for bulk exporting Perplexity threads daily. Two files have been prepared:

### 1. **perplexity_bulk_exporter.js** (387 lines)
- Complete Node.js automation script
- Handles Perplexity authentication with browser caching
- Extracts all threads from your library
- Exports each as individual Markdown file with metadata
- Supports daily scheduling via cron
- One-time export mode available
- Full error handling and logging

### 2. **perplexity_setup_guide.md** (453 lines)
- Step-by-step installation guide
- Configuration details (.env setup)
- Usage examples (one-time vs scheduled)
- Output format documentation
- How to run as system service (macOS/Linux/Windows)
- Troubleshooting guide
- Integration examples (Obsidian, Python, Cloud Storage)

---

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
mkdir perplexity-exporter
cd perplexity-exporter

npm init -y
npm install puppeteer-extra puppeteer-extra-plugin-stealth node-cron dotenv
```

### Step 2: Create `.env` File
```
PERPLEXITY_EMAIL=your@email.com
PERPLEXITY_PASSWORD=your_password
EXPORT_DIR=./perplexity_exports
SCHEDULE_TIME=0 3 * * *
```

### Step 3: Copy Script
Download `perplexity_bulk_exporter.js` to your directory

### Step 4: Run Now
```bash
# One-time export of all threads
node perplexity_bulk_exporter.js --run-now

# OR schedule daily exports (runs continuously)
node perplexity_bulk_exporter.js
```

---

## 📁 What Gets Exported

Each thread becomes a separate Markdown file:
```
perplexity_exports/
├── 2026-01-20_Understanding_AI_Models.md
├── 2026-01-20_Python_best_practices.md
├── 2026-01-20_Marketing_for_SMBs.md
└── .browser_profile/  (authentication cache)
```

**Format (with metadata):**
```markdown
---
title: Understanding AI Models
url: https://www.perplexity.ai/search/...
exported: 2026-01-20T06:15:23.456Z
wordCount: 2847
---

# Understanding AI Models

[Full conversation content]
```

---

## ⚙️ Configuration

### Cron Schedule Examples
```
0 3 * * *        → Daily at 3 AM UTC
0 0 * * *        → Daily at midnight
0 */6 * * *      → Every 6 hours
0 2 * * 0        → Weekly Sunday at 2 AM
*/30 * * * *     → Every 30 minutes
```

### Environment Variables
| Variable | Purpose |
|----------|---------|
| `PERPLEXITY_EMAIL` | Your Perplexity login |
| `PERPLEXITY_PASSWORD` | Your password |
| `EXPORT_DIR` | Where to save exports |
| `SCHEDULE_TIME` | Cron expression |

---

## 🔧 Advanced Usage

### Run as Background Service (macOS)
```bash
# Create launchd plist (see setup guide for details)
# Then:
launchctl load ~/Library/LaunchAgents/com.ewan.perplexity-exporter.plist
```

### Integrate with Obsidian
```env
EXPORT_DIR=/Users/ewan/Documents/Obsidian/MyVault/Perplexity
```

Then set Obsidian folder sync to watch this directory.

### Process with Python
```bash
# Export all threads, then process them
node perplexity_bulk_exporter.js --run-now && python3 process_exports.py
```

### Backup to Cloud
```env
EXPORT_DIR=/Users/ewan/Google\ Drive/Perplexity_Exports
# Or Dropbox, OneDrive, etc.
```

---

## 📊 Features

✅ **Fully Automated**
- Auto-login with credential caching
- No manual thread clicking needed
- Entire library exported in one run

✅ **Reliable**
- Handles authentication persistence
- Rate limiting between threads
- Comprehensive error handling
- Detailed logging with timestamps

✅ **Flexible Scheduling**
- Run immediately with `--run-now`
- Schedule daily at any time
- Continuous background process
- Can pause with Ctrl+C

✅ **Developer-Friendly**
- Clean, documented code
- Easy to customize
- Output as Markdown (processable)
- Works with your Python/Node.js stack

✅ **Production-Ready**
- Runs as system service
- Persistent authentication
- Configurable via .env
- Full error handling

---

## 🔒 Security

⚠️ **Best Practices:**
1. **Don't commit .env to Git** - Add to .gitignore
2. **Use strong password** - Or enable Perplexity tokens if available
3. **File permissions:** `chmod 600 .env`
4. **Local-only storage** - Threads exported to your machine

---

## 🐛 Troubleshooting

**"No threads found?"**
- Verify login works manually
- Check if you have created any threads
- Delete `.browser_profile/` to clear cache

**"Authentication failed?"**
- Verify email/password in .env
- Check for 2FA (may need manual approval)
- Try `--run-now` to see browser window

**"Port/process errors?"**
- Kill existing process: `pkill -f "node perplexity"`
- Check Node.js installed: `node --version`

**More troubleshooting** in `perplexity_setup_guide.md`

---

## 📋 Recommended Workflow

### For Personal Knowledge Base
1. Export daily at 3 AM (default)
2. Directory watched by Obsidian
3. Automatically appear in vault
4. Tag/organize as needed

### For AI Agency
1. Export daily to structured folder
2. Process with Python to extract:
   - Client topics
   - Research patterns
   - Citation sources
3. Feed into CRM or knowledge base

### For Backup/Compliance
1. Export to cloud storage (Google Drive)
2. Monthly automated backup
3. Searchable archive of all research

---

## 📞 Next Steps

1. **Download both files** from your export links
2. **Follow 5-minute setup** above
3. **Test with `--run-now`**
4. **Configure .env** for your schedule
5. **Set up as service** (optional, for continuous operation)
6. **Integrate** with Obsidian/Python/etc.

---

## 📚 Documentation

- **Setup & Installation**: perplexity_setup_guide.md
- **Script Source**: perplexity_bulk_exporter.js
- **General Guide**: perplexity-export.md (original comprehensive guide)

---

## Questions?

Refer to the **perplexity_setup_guide.md** FAQ section, or check the detailed documentation in the script comments.

**Recommendation**: Start with `node perplexity_bulk_exporter.js --run-now` to test immediately, then move to scheduled mode once you verify it works.
