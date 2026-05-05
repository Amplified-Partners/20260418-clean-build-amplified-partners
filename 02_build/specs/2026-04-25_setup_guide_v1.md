---
title: "Detailed Setup Guide"
id: "setup_guide"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "setup-guide"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Detailed Setup Guide

This guide walks you through setting up each data source for AI Stack Auditor. Follow the steps in order.

## Table of Contents

1. [Gmail API Setup](#gmail-api-setup)
2. [Stripe API Setup](#stripe-api-setup)
3. [PayPal API Setup](#paypal-api-setup)
4. [Claude API Setup](#claude-api-setup)
5. [Bank CSV Setup](#bank-csv-setup)
6. [Verification](#verification)
7. [Next Steps](#next-steps)

---

## Gmail API Setup

Gmail scanning is the most powerful data source. Here's how to set it up:

### Step 1: Create Google Cloud Project

1. Go to **[console.cloud.google.com](https://console.cloud.google.com/)**
2. Click the project dropdown (top bar, near Google Cloud logo)
3. Click **"New Project"**
4. Enter a name, e.g., "AI Stack Auditor"
5. Select a location (your organization or "No organization")
6. Click **"Create"**
7. Wait for project creation to complete

### Step 2: Enable Gmail API

1. In the Google Cloud Console, use the search bar to search for **"Gmail API"**
2. Select **"Gmail API"** from results
3. Click **"Enable"**
4. Wait for API to enable (1-2 minutes)

### Step 3: Configure OAuth Consent Screen

1. Go to **"OAuth consent screen"** (left sidebar → APIs & Services)
2. Choose **"External"** (for personal use)
3. Fill in required fields:
   - **App name**: "AI Stack Auditor"
   - **User support email**: Your email address
   - **Developer contact email**: Your email address
4. Click **"Save and Continue"**
5. On "Scopes" → Click **"Add or remove scopes"**
6. Search for `gmail.readonly`
7. Check the box for `.../auth/gmail.readonly`
8. Click **"Update"** → **"Save and Continue"**
9. On "Test users" → Click **"Add users"**
10. Add your Gmail address
11. Click **"Save and Continue"**
12. Review and click **"Back to Dashboard"**

### Step 4: Create OAuth Credentials

1. Go to **"Credentials"** (left sidebar → APIs & Services)
2. Click **"Create Credentials"** → **"OAuth client ID"**
3. Application type: **"Desktop application"**
4. Name: "AI Stack Auditor Desktop"
5. Click **"Create"**
6. A modal will show your Client ID and Secret
7. Click **"OK"** to dismiss

### Step 5: Download Credentials

1. Find your new OAuth 2.0 Client ID in the list
2. Click the **download icon** (⬇️) on the right
3. Save the file as `gmail_credentials.json`
4. Move the file to your project:
   ```bash
   mv ~/Downloads/gmail_credentials.json ai-stack-auditor/credentials/
   ```

### Step 6: Run OAuth Setup

```bash
cd ai-stack-auditor
python setup_gmail_oauth.py
```

**What to expect:**
1. The script checks for `gmail_credentials.json`
2. Opens your default browser
3. Shows a Google sign-in screen
4. Asks for permission to read your emails
5. Click **"Continue"** → **"Allow"**
6. A success message appears
7. Token saved to `credentials/gmail_token.json`

**⚠️ Troubleshooting:**
- If browser doesn't open: Check terminal for a URL to copy-paste
- If "Access blocked": Verify test user is added in Step 3
- If "Invalid credentials": Redownload the JSON file

---

## Stripe API Setup

### Step 1: Get Your API Key

1. Go to **[dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys)**
2. Sign in to your Stripe account
3. You'll see two keys:
   - **Publishable key** (starts with `pk_`) - not needed
   - **Secret key** (starts with `sk_`) - **this is what you need**

### Step 2: Add to .env File

```bash
# In ai-stack-auditor/.env
STRIPE_API_KEY=sk_test_your_secret_key_here
```

**⚠️ Important:**
- Use `sk_test_` for sandbox testing
- Use `sk_live_` for real data (caution!)
- Never share your secret key publicly

### Step 3: Verify Connection

```bash
python test_stripe_scanner.py  # If test script exists
```

Or just run the main script - it will warn if Stripe fails.

---

## PayPal API Setup

### Step 1: Create a PayPal App

1. Go to **[developer.paypal.com](https://developer.paypal.com/)**
2. Sign in with your PayPal account
3. Click **"Dashboard"** → **"My Apps & Credentials"**
4. Click **"Create App"**
5. Enter app name: "AI Stack Auditor"
6. Click **"Create App"**

### Step 2: Get Credentials

1. Note your **Client ID** (starts with `sb` for sandbox)
2. Click **"Show Secret"** to reveal your Secret
3. Copy both values

### Step 3: Add to .env File

```bash
# In ai-stack-auditor/.env
PAYPAL_CLIENT_ID=your_client_id_here
PAYPAL_CLIENT_SECRET=your_client_secret_here
PAYPAL_MODE=sandbox  # Use 'live' for real data
```

### Step 4: Test with Sandbox (Recommended)

For testing, use sandbox mode first:
1. Create a [Sandbox Business Account](https://developer.paypal.com/dashboard/sandbox)
2. Make some test transactions
3. Run the auditor to see if they appear
4. Switch to `PAYPAL_MODE=live` when ready

---

## Claude API Setup

### Step 1: Get Your API Key

1. Go to **[console.anthropic.com](https://console.anthropic.com/)**
2. Sign in or create an account
3. Click **"API Keys"** (left sidebar)
4. Click **"Create Key"**
5. Give it a name (e.g., "AI Stack Auditor")
6. Copy the key (starts with `sk-ant-`)

### Step 2: Add to .env File

```bash
# In ai-stack-auditor/.env
ANTHROPIC_API_KEY=sk-ant-your_api_key_here
```

### Step 3: Understand Costs

Claude pricing (approximate, as of late 2024):

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|----------------------|
| Claude Sonnet 4.0 | $3.00 | $15.00 |
| Claude Haiku 3.5 | $0.25 | $1.25 |

**Typical audit cost**: ~$0.10-0.30 per run (50 subscriptions, ~4K tokens)

### Step 4: Set Usage Limits (Recommended)

1. In Anthropic Console, go to **"Usage Limits"**
2. Set a monthly spend limit (e.g., $10)
3. You'll receive alerts before exceeding limits

---

## Bank CSV Setup

### Supported Formats

The tool accepts CSV exports from most UK and US banks:

| Bank | Tested | Export Location |
|------|--------|-----------------|
| **Monzo** | ✅ Yes | Settings → Statements |
| **Starling** | ✅ Yes | Statements → Export |
| **Barclays** | ✅ Yes | Account → Statements |
| **HSBC** | ✅ Yes | Statements → Download |
| **Lloyds** | ✅ Yes | Account services → Statements |
| **NatWest** | ✅ Yes | Statements → Export |
| **Chase** | ✅ Yes | Statements → Download |
| **Revolut** | ✅ Yes | Statements → Export CSV |
| **Wise** | ✅ Yes | Statements → Export |

### Required Columns

Your CSV must have columns matching these (flexible naming):

| Required | Acceptable Names |
|----------|------------------|
| **Date** | `Date`, `Transaction Date`, `Posted Date`, `Date` |
| **Description** | `Description`, `Memo`, `Narrative`, `Merchant`, `Payee` |
| **Amount** | `Amount`, `Value`, `Debit`, `Cost` |

### Export Instructions by Bank

#### Monzo
1. Open Monzo app
2. Tap Settings (⚙️) → Statements
3. Choose account
4. Select date range
5. Tap "Export CSV"
6. Save to `data/bank_statements.csv`

#### Starling
1. Login to web banking
2. Go to Statements
3. Select account and date range
4. Click "Export" → "CSV"
5. Save to `data/bank_statements.csv`

#### Barclays (Online Banking)
1. Login to Barclays
2. Account → Statements & documents
3. Choose account
4. Select "Statements" tab
5. Download → CSV format

### Configure the Path

```bash
# In ai-stack-auditor/.env
BANK_CSV_PATHS=./data/bank_statements.csv
# Multiple files: ./data/bank1.csv,./data/bank2.csv
```

### Troubleshooting CSV Issues

**Problem**: "No transactions found"
- Check column names match expected formats
- Ensure file is UTF-8 encoded
- Try opening and re-saving in Excel/Numbers

**Problem**: Negative amounts confusing
- The tool looks for subscription patterns regardless of debit/credit
- Report an issue if patterns aren't detected

---

## Verification

After setup, verify everything works:

### Test Gmail Connection

```bash
python test_gmail_scanner.py
```

Expected output: "Successfully connected to Gmail. Found X subscription emails."

### Test Stripe Connection

```bash
python test_stripe_scanner.py
```

Expected output: "Stripe connected. Found X subscriptions."

### Test AI Analyzer

```bash
python test_ai_analyzer.py
```

Expected output: "Claude API working. Analysis complete."

### Run Full Audit

```bash
python src/main.py
```

Expected: Creates `output/inventory.csv`, `output/dashboard.html`, `output/action_plan.md`

---

## Next Steps

1. **Review outputs**: Open `output/dashboard.html` in your browser
2. **Check action plan**: Read `output/action_plan.md` for recommendations
3. **Customize categories**: Edit `src/processors/categorizer.py` if needed
4. **Set up monthly reminders**: Add to your calendar
5. **Share feedback**: Report issues for improvements

### Quick Start Recap

```bash
cd ai-stack-auditor
pip install -r requirements.txt
python setup_gmail_oauth.py
cp .env.example .env
# Edit .env with your API keys
python src/main.py
open output/dashboard.html
```

---

**Questions?** Check the main [README.md](README.md) or the Troubleshooting section.
