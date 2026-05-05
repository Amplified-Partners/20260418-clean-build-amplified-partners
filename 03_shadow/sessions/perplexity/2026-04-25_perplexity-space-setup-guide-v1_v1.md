---
title: "PERPLEXITY SPACE SETUP - MANUAL INSTRUCTIONS"
id: "perplexity-space-setup-guide-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "perplexity-session"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# PERPLEXITY SPACE SETUP - MANUAL INSTRUCTIONS

**Created:** 2025-12-21  
**Time Required:** 15-20 minutes  
**Status:** Ready to Execute

---

## WHAT YOU'LL DO

You'll create a Perplexity Space called "Ewan's Second Brain" and upload 4 strategic documents that will give Perplexity immediate access to your key knowledge.

---

## STEP-BY-STEP INSTRUCTIONS

### Step 1: Create Your Perplexity Space

1. **Open Perplexity:**
   - Go to https://perplexity.ai
   - Sign in to your account

2. **Create the Space:**
   - Click **"Spaces"** in the left sidebar
   - Click **"Create Space"** button
   - Enter these details:
     - **Name:** `Ewan's Second Brain`
     - **Description:** `Complete knowledge base with 41,000+ atoms covering business strategy, automation, AI implementation, and project documentation`
     - **Visibility:** Private
   - Click **"Create"**

3. **Configure Space Settings:**
   - In your new Space, click the **Settings** icon (gear icon)
   - Enable these options:
     - ✅ **"Search files in responses"**
     - ✅ **"Cite sources"**
   
   - Add these **Custom Instructions:**
     ```
     This is my complete Second Brain knowledge base. When answering questions:
     1. Always search uploaded files first
     2. Reference specific documents and sections
     3. Synthesize insights from multiple sources
     4. Cite file names and relevant quotes
     5. If information isn't in the knowledge base, say so clearly
     ```
   - Click **"Save"**

---

### Step 2: Upload Strategic Documents

You need to upload these 4 files to your Space:

**File Locations:**
```
/Users/ewanbramley/Knowledge/00-system/OPTIMAL-INFRASTRUCTURE-PLAN.md
/Users/ewanbramley/Knowledge/00-system/EMPIRE-BLUEPRINT.md
/Users/ewanbramley/Knowledge/00-system/SECOND-BRAIN-MASTER-PLAN.md
/Users/ewanbramley/Knowledge/00-system/PERPLEXITY-INTEGRATION-GUIDE.md
```

**How to Upload:**

1. In your "Ewan's Second Brain" Space, click **"Upload files"** or the **📎 attachment icon**

2. Navigate to `/Users/ewanbramley/Knowledge/00-system/`

3. Select all 4 files:
   - Hold **Cmd** and click each file
   - Or select the first file, hold **Shift**, and click the last file

4. Click **"Open"** to upload

5. Wait for processing (2-3 minutes)
   - You'll see "Processing..." status
   - Wait until all files show "Ready"

6. Verify all 4 files appear in your Space's file list

---

### Step 3: Test Your Space

Try these test queries to verify everything works:

**Query 1: Infrastructure Check**
```
What's my complete infrastructure plan?
```
**Expected:** Should reference OPTIMAL-INFRASTRUCTURE-PLAN.md and provide details about your infrastructure setup.

**Query 2: Revenue Scaling**
```
How do I scale from £180K to £1M?
```
**Expected:** Should reference EMPIRE-BLUEPRINT.md and explain your scaling strategy.

**Query 3: Framework Check**
```
What's my Business Factory framework?
```
**Expected:** Should reference SECOND-BRAIN-MASTER-PLAN.md and describe the framework.

**Query 4: Integration Details**
```
How does the Perplexity integration work?
```
**Expected:** Should reference PERPLEXITY-INTEGRATION-GUIDE.md and explain the setup.

---

## VERIFICATION CHECKLIST

Before moving to Phase 2, confirm:

- [ ] Space created with name "Ewan's Second Brain"
- [ ] Space is set to Private
- [ ] "Search files in responses" is enabled
- [ ] "Cite sources" is enabled
- [ ] Custom instructions are saved
- [ ] All 4 files uploaded successfully
- [ ] All files show "Ready" status (not "Processing...")
- [ ] Test queries return relevant answers with citations

---

## WHAT'S NEXT?

Once you've completed this setup and verified it works:

1. **Confirm completion** - Let me know the Space is ready
2. **Phase 2** - I'll test and deploy the Librarian API
3. **Phase 3** - I'll set up automated sync (if Perplexity API is available)

---

## TROUBLESHOOTING

**Problem: Can't find "Spaces" in sidebar**
- Solution: Update to latest Perplexity version or check if Spaces is available in your region

**Problem: Files won't upload**
- Solution: Check file size (should be under 10MB each). Try uploading one at a time.

**Problem: Files stuck on "Processing..."**
- Solution: Wait 5 minutes. If still processing, try removing and re-uploading.

**Problem: Queries don't reference uploaded files**
- Solution: Verify "Search files in responses" is enabled in Space settings.

---

## ESTIMATED TIME

- Create Space: 2 minutes
- Configure settings: 3 minutes
- Upload files: 5 minutes
- Test queries: 5 minutes
- **Total: ~15 minutes**

---

**Ready to start? Follow the steps above, then let me know when Phase 1 is complete!**