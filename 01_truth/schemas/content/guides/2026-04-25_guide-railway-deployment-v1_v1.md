---
title: "RAILWAY DEPLOYMENT GUIDE - LIBRARIAN API"
id: "guide-railway-deployment-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "guide"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# RAILWAY DEPLOYMENT GUIDE - LIBRARIAN API

**Created:** 2025-12-21  
**Time Required:** 10-15 minutes  
**Status:** Ready to Deploy

---

## WHAT YOU'LL DO

Deploy your Librarian API to Railway so it's accessible from anywhere, including Perplexity. The API provides search access to your 441,360 atoms.

---

## PREREQUISITES

✅ **Local API tested and working** (completed)
- API running on http://localhost:8000
- Search endpoint returning results
- Stats showing 441,360 atoms

---

## STEP 1: INSTALL RAILWAY CLI

Choose one method:

**Option A: Using npm (Recommended)**
```bash
npm install -g @railway/cli
```

**Option B: Using Homebrew**
```bash
brew install railway
```

**Verify Installation:**
```bash
railway --version
```

---

## STEP 2: LOGIN TO RAILWAY

```bash
railway login
```

This will:
1. Open your browser
2. Ask you to authorize the CLI
3. Return you to the terminal when complete

---

## STEP 3: PREPARE FOR DEPLOYMENT

First, stop your local API server (it's currently running):

```bash
# Press Ctrl+C in the terminal running the API
```

Then navigate to the scripts directory:

```bash
cd /Users/ewanbramley/Knowledge/.data/scripts
```

---

## STEP 4: INITIALIZE RAILWAY PROJECT

```bash
railway init
```

**Follow the prompts:**
- **Create new project or use existing?** → Create new project
- **Project name:** `librarian-api`
- **Region:** Choose closest to you (e.g., `us-west1` or `eu-west1`)

---

## STEP 5: DEPLOY THE API

```bash
railway up
```

**What happens:**
1. Railway detects Python project
2. Installs dependencies from `requirements.txt`
3. Builds and deploys your API
4. Provides a deployment URL

**Expected output:**
```
✓ Deployment successful
🎉 Deployment live at https://librarian-api-production-xxxx.up.railway.app
```

**⏱ This takes 2-3 minutes**

---

## STEP 6: CONFIGURE ENVIRONMENT

Set the PORT variable:

```bash
railway variables set PORT=8000
```

---

## STEP 7: GET YOUR DEPLOYMENT URL

```bash
railway domain
```

This shows your public URL. If no domain is set, create one:

```bash
railway domain create
```

**Save this URL** - you'll need it for testing and Perplexity integration.

---

## STEP 8: TEST DEPLOYED API

Replace `YOUR-RAILWAY-URL` with your actual URL:

**Test Health:**
```bash
curl https://YOUR-RAILWAY-URL/health
```

**Expected:** `{"status":"healthy","database":"connected"}`

**Test Search:**
```bash
curl -X POST "https://YOUR-RAILWAY-URL/search?query=automation&limit=3"
```

**Expected:** JSON with 3 automation-related results

**Test Stats:**
```bash
curl https://YOUR-RAILWAY-URL/stats
```

**Expected:** Stats showing 441,360 atoms

---

## STEP 9: VIEW LOGS (OPTIONAL)

Monitor your deployment:

```bash
railway logs
```

Press `Ctrl+C` to exit logs.

---

## API ENDPOINTS

Once deployed, your API provides:

### Health Check
```
GET https://YOUR-RAILWAY-URL/health
```

### Search Knowledge Base
```
POST https://YOUR-RAILWAY-URL/search?query=SEARCH_TERM&limit=10
```

### Get Specific Atom
```
GET https://YOUR-RAILWAY-URL/atom/ATOM_ID
```

### Get Statistics
```
GET https://YOUR-RAILWAY-URL/stats
```

### Get Recent Atoms
```
GET https://YOUR-RAILWAY-URL/recent?limit=20
```

### API Documentation
```
GET https://YOUR-RAILWAY-URL/docs
```

---

## IMPORTANT NOTES

### Database Location
⚠️ **Critical:** The API expects the database at:
```
/Users/ewanbramley/Knowledge/.data/librarian.db
```

This works locally but **won't work on Railway** because Railway doesn't have access to your local filesystem.

### Solutions:

**Option A: Upload Database to Railway (Recommended for testing)**
```bash
# Create a data directory in your project
mkdir -p /Users/ewanbramley/Knowledge/.data/scripts/data

# Copy database
cp /Users/ewanbramley/Knowledge/.data/librarian.db /Users/ewanbramley/Knowledge/.data/scripts/data/

# Update librarian-api.py to use relative path
# Change: LIBRARIAN_DB = KNOWLEDGE_ROOT / ".data" / "librarian.db"
# To: LIBRARIAN_DB = Path("./data/librarian.db")

# Redeploy
railway up
```

**Option B: Use Railway Volumes (Recommended for production)**
```bash
# Create a volume
railway volume create

# Mount it to your service
railway volume attach

# Update code to use volume path
```

**Option C: Use PostgreSQL (Best for production)**
- Set up Railway PostgreSQL
- Migrate from SQLite to PostgreSQL
- Update API to use PostgreSQL connection

---

## COST

**Railway Pricing:**
- **Hobby Plan:** $5/month
  - 500 hours of usage
  - $0.000231/GB-hour for RAM
  - Perfect for this API

**Estimated Monthly Cost:** ~$5-7/month

---

## TROUBLESHOOTING

### Deployment Fails
```bash
# Check logs
railway logs

# Common issues:
# 1. Missing requirements.txt → Already present ✓
# 2. Wrong Python version → Using Python 3.14 ✓
# 3. Port not set → Set with railway variables
```

### API Returns 500 Error
```bash
# Check if database path is correct
railway logs

# Look for: "Librarian database not found"
# Solution: Implement Option A, B, or C above
```

### Can't Access API
```bash
# Verify domain is set
railway domain

# Check service is running
railway status

# View recent logs
railway logs --tail 50
```

---

## NEXT STEPS

Once deployed and tested:

1. **Save your Railway URL** in a safe place
2. **Test all endpoints** to ensure they work
3. **Update Perplexity integration** with your Railway URL
4. **Set up monitoring** (Railway provides built-in metrics)

---

## UPDATING THE API

When you make changes to `librarian-api.py`:

```bash
cd /Users/ewanbramley/Knowledge/.data/scripts
railway up
```

Railway will automatically redeploy with your changes.

---

## RAILWAY DASHBOARD

Access your deployment dashboard:
```bash
railway open
```

Or visit: https://railway.app/dashboard

From the dashboard you can:
- View logs
- Monitor resource usage
- Manage environment variables
- View deployment history
- Set up custom domains

---

## SUCCESS CRITERIA

✅ Railway CLI installed and logged in
✅ Project created and deployed
✅ Health endpoint returns healthy status
✅ Search endpoint returns results
✅ Stats endpoint shows 441,360 atoms
✅ API accessible from public URL

---

**Your Librarian API is now live and accessible from anywhere!**

**Railway URL:** `https://YOUR-RAILWAY-URL`
**API Docs:** `https://YOUR-RAILWAY-URL/docs`