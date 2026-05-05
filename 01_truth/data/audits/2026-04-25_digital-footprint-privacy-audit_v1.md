---
title: "Digital Footprint Privacy & Security Audit Guide"
id: "digital-footprint-privacy-audit"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "audit"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Digital Footprint Privacy & Security Audit Guide
**For: Ewan Bramley (ewanbramley@gmail.com)**  
**Date Created:** 2025-12-29  
**Purpose:** Comprehensive manual privacy and security audit using free online tools

---

## 📋 Overview

This guide walks you through a complete privacy and security audit of your digital footprint. Follow each section in order, documenting your findings as you go. Set aside 3-4 hours to complete this thoroughly.

### What You'll Need
- ✅ Your email address: ewanbramley@gmail.com
- ✅ Access to your main email accounts
- ✅ A notebook or spreadsheet to track findings
- ✅ Your phone (for 2FA setup)

---

## 🔴 SECTION 1: Data Breach Check (Start Here - CRITICAL)

### Step 1.1: Check Have I Been Pwned
**Time: 5 minutes | Priority: CRITICAL**

1. Open your browser and go to: **https://haveibeenpwned.com**
2. Enter your email: **ewanbramley@gmail.com**
3. Click "pwned?"
4. **DOCUMENT RESULTS:**
   - [ ] How many breaches found? _____________
   - [ ] List each breach name and date:
     - ______________________________
     - ______________________________
     - ______________________________
   - [ ] What data was exposed in each? (passwords, emails, phone numbers, etc.)

5. **IMMEDIATE ACTIONS IF BREACHED:**
   - If passwords were exposed → Change passwords on those sites NOW
   - If credit card info exposed → Contact your bank
   - If personal info exposed → Note for identity monitoring

### Step 1.2: Check Password Security
1. While on Have I Been Pwned, scroll down to "Pwned Passwords"
2. Click "Pwned Passwords"
3. For each important password you use:
   - Enter the password (it's safe - uses k-anonymity)
   - If found → Change immediately
   - **DO NOT** test your current banking/email passwords here - change them as precaution

### Step 1.3: Additional Email Check
1. Go to: **https://cybernews.com/personal-data-leak-check/**
2. Enter: ewanbramley@gmail.com
3. Check results
4. Document any additional breaches not found in Step 1.1

**🚨 ACTION REQUIRED:** If you found ANY breaches, change those passwords before continuing.

---

## 🔍 SECTION 2: Search Engine Footprint Analysis

### Step 2.1: Google Search
**Time: 15 minutes**

**Search 1: Your Full Name**
1. Go to: **https://www.google.com**
2. Search: **"Ewan Bramley"** (with quotes)
3. Document first 5 pages:
   - [ ] Professional profiles (LinkedIn, etc.)
   - [ ] Social media accounts
   - [ ] Old forum posts
   - [ ] News mentions
   - [ ] Photos
   - [ ] Addresses or phone numbers (CRITICAL)
   - [ ] Anything embarrassing or unwanted

**Search 2: Your Email**
1. Search: **ewanbramley@gmail.com**
2. Document:
   - [ ] Any public profiles using this email
   - [ ] Forum registrations
   - [ ] Public documents
   - [ ] Data breach listings

**Search 3: Your Email Without Domain**
1. Search: **ewanbramley** (without @gmail.com)
2. Document:
   - [ ] Usernames on various sites
   - [ ] Social media handles
   - [ ] Gaming profiles
   - [ ] Any other accounts

**Search 4: Variations**
1. Search these variations:
   - "Ewan D Bramley"
   - "E Bramley"
   - Any nicknames you use
2. Document anything new

### Step 2.2: Bing Search
1. Go to: **https://www.bing.com**
2. Repeat all searches from Step 2.1
3. Note anything different from Google results

### Step 2.3: DuckDuckGo Search
1. Go to: **https://duckduckgo.com**
2. Repeat searches
3. Sometimes finds different results than Google/Bing

### Step 2.4: Image Search
1. Go to: **https://images.google.com**
2. Search: "Ewan Bramley"
3. Check if any images of you appear
4. Right-click on images → "Search image with Google" to find where they're posted

**TEMPLATE: Search Findings**
```
Date: _______________
Search Engine: _______________
Total Results: _______________

Concerning Findings:
1. _____________________________
2. _____________________________
3. _____________________________

Action Items:
- [ ] Remove from _______________
- [ ] Contact _________ to remove
- [ ] Request delisting from Google
```

---

## 🔐 SECTION 3: Google Account Security Audit

### Step 3.1: Security Checkup
**Time: 10 minutes**

1. Go to: **https://myaccount.google.com/security-checkup**
2. Log in if needed
3. Work through each section:

**Section A: Your Devices**
- [ ] Review all signed-in devices
- [ ] Remove any you don't recognize
- [ ] Remove old/unused devices

**Section B: Recent Security Activity**
- [ ] Check for suspicious sign-ins
- [ ] Note any unrecognized locations
- [ ] Document any unusual activity

**Section C: Recovery Info**
- [ ] Verify recovery email is current
- [ ] Verify recovery phone is current
- [ ] Add backup recovery options

**Section D: Screen Locks**
- [ ] Ensure all devices have screen locks
- [ ] Update if needed

### Step 3.2: Privacy Checkup
1. Go to: **https://myaccount.google.com/privacycheckup**
2. Work through all sections:

**Personalization & Data**
- [ ] Review "Web & App Activity" - Turn OFF if unwanted
- [ ] Review "Location History" - Turn OFF if unwanted
- [ ] Review "YouTube History" - Turn OFF if unwanted

**Activity Saved From Google Services**
- [ ] Check what data is saved
- [ ] Delete unwanted data

**Personal Info & Privacy Options**
- [ ] Who can see your email?
- [ ] Who can see your phone?
- [ ] Update privacy settings

### Step 3.3: Connected Apps & Sites
1. Go to: **https://myaccount.google.com/permissions**
2. Review EVERY app with access
3. For each app:
   - [ ] Do you still use it? If NO → Remove
   - [ ] Does it need these permissions? If NO → Remove
   - [ ] Is it from a trusted developer? If NO → Remove

**RULE:** When in doubt, remove it. You can always re-authorize later.

### Step 3.4: Data Download (Optional but Recommended)
1. Go to: **https://takeout.google.com**
2. Select data to download
3. Create archive
4. This shows what Google knows about you

---

## 📧 SECTION 4: Email Security Deep Dive

### Step 4.1: Gmail Security Settings
1. Go to: **https://mail.google.com**
2. Click Settings (gear icon) → "See all settings"
3. Go to "Forwarding and POP/IMAP" tab
   - [ ] Check if any forwarding is enabled
   - [ ] If YES and you didn't set it → DISABLE IMMEDIATELY (major security risk)
   - [ ] Document any forwarding addresses

4. Go to "Filters and Blocked Addresses" tab
   - [ ] Review all filters
   - [ ] Delete any you don't recognize
   - [ ] Look for filters that delete/forward emails

5. Go to "Accounts and Import" tab
   - [ ] Check "Send mail as"
   - [ ] Remove any you don't recognize

### Step 4.2: Check for Suspicious Activity
1. Scroll to bottom of Gmail inbox
2. Click "Details" (bottom right)
3. Review recent access:
   - [ ] Any unknown IP addresses?
   - [ ] Any unusual locations?
   - [ ] Any unauthorized access types?

### Step 4.3: Email Aliases & Forwarding
1. List all email addresses you own:
   - ewanbramley@gmail.com
   - _____________________
   - _____________________
2. For each one, repeat Steps 4.1 and 4.2

---

## 📱 SECTION 5: Account Inventory

### Step 5.1: Find Your Accounts (Multiple Methods)

**Method 1: Email Search**
1. In Gmail, search: "welcome" OR "verify" OR "confirmation"
2. Go back 5+ years
3. List every account signup email you find

**Method 2: Password Manager Check**
1. If you use Chrome: **chrome://settings/passwords**
2. If you use Safari: **Preferences → Passwords**
3. Export list of all saved passwords (don't include actual passwords)

**Method 3: Account Finder Tool**
1. Go to: **https://www.accountkiller.com/en**
2. Browse categories to jog your memory
3. List accounts you remember

**Method 4: Social Login Check**
1. Go to: **https://myaccount.google.com/permissions**
2. List all apps using "Sign in with Google"

### Step 5.2: Account Classification
For each account, categorize:

**CRITICAL ACCOUNTS** (need maximum security):
- [ ] Email accounts
- [ ] Banking/financial
- [ ] Payment services (PayPal, etc.)
- [ ] Password managers
- [ ] Cloud storage
- [ ] Social media (if important)

**ACTIVE ACCOUNTS** (use regularly):
- [ ] _____________________
- [ ] _____________________

**DORMANT ACCOUNTS** (don't use but want to keep):
- [ ] _____________________
- [ ] _____________________

**DEAD ACCOUNTS** (don't need - mark for deletion):
- [ ] _____________________
- [ ] _____________________

---

## 👥 SECTION 6: Social Media Privacy Audit

### Step 6.1: Facebook (if you have account)
1. Go to: **https://www.facebook.com/settings?tab=privacy**
2. Check each setting:
   - [ ] Who can see your future posts? → Friends only
   - [ ] Who can see your friends list? → Only me
   - [ ] Who can look you up using email? → Friends
   - [ ] Do you want search engines to link to your profile? → NO

3. Go to: **https://www.facebook.com/settings?tab=timeline**
   - [ ] Review what's on your timeline
   - [ ] Who can post on your timeline?
   - [ ] Review tags before they appear?

4. Go to: **https://www.facebook.com/settings?tab=apps**
   - [ ] Remove apps you don't use
   - [ ] Review permissions for remaining apps

### Step 6.2: LinkedIn
1. Go to: **Settings & Privacy** → **Visibility**
2. Check:
   - [ ] Who can see your email?
   - [ ] Who can see your connections?
   - [ ] Profile viewing options
   - [ ] Edit public profile - what shows in Google?

3. Go to: **Data Privacy**
   - [ ] Review data shared with third parties

### Step 6.3: Instagram (if applicable)
1. Go to Settings → Privacy
2. Check:
   - [ ] Account privacy (private vs public)
   - [ ] Story controls
   - [ ] Comment controls
   - [ ] Tags
   - [ ] Activity status

### Step 6.4: Twitter/X (if applicable)
1. Settings → Privacy and Safety
2. Check:
   - [ ] Protect your posts (private account)
   - [ ] Photo tagging
   - [ ] Discoverability
   - [ ] Data sharing

### Step 6.5: Other Platforms
Repeat similar checks for:
- [ ] TikTok
- [ ] Reddit
- [ ] YouTube
- [ ] Any others you use

---

## 🔑 SECTION 7: Password Security Overhaul

### Step 7.1: Password Audit
1. Go to: **https://myaccount.google.com/security-checkup**
2. Click "Password Manager"
3. Look for:
   - [ ] Weak passwords
   - [ ] Reused passwords
   - [ ] Compromised passwords

### Step 7.2: Password Strength Check
For your most important accounts, check if passwords meet:
- [ ] At least 12 characters long
- [ ] Mix of upper/lowercase
- [ ] Numbers included
- [ ] Special characters included
- [ ] NOT based on personal info
- [ ] NOT a common word
- [ ] UNIQUE (not used elsewhere)

### Step 7.3: Create Strong Passwords
**Method 1: Passphrase**
- Example: "Coffee-Dancing-Elephant-42-Purple!"
- Easy to remember, hard to crack

**Method 2: Password Generator**
1. Go to: **https://bitwarden.com/password-generator/**
2. Generate 16+ character passwords
3. Save in password manager

### Step 7.4: Change Critical Passwords
Change passwords on these accounts (if needed):
1. [ ] Primary email (ewanbramley@gmail.com)
2. [ ] Banking accounts
3. [ ] PayPal/payment services
4. [ ] iCloud/Apple ID
5. [ ] Amazon
6. [ ] Any account with payment info
7. [ ] Social media
8. [ ] Password manager itself

**IMPORTANT:** Use a unique password for EACH account.

---

## 🛡️ SECTION 8: Two-Factor Authentication (2FA)

### Step 8.1: Enable 2FA on Critical Accounts

**What is 2FA?**
Requires both password AND phone code to log in. Even if someone steals your password, they can't access your account.

**Priority Order:**
1. [ ] Email accounts (HIGHEST priority)
2. [ ] Banking/financial
3. [ ] Payment services
4. [ ] Password manager
5. [ ] Cloud storage
6. [ ] Social media
7. [ ] Other important accounts

**How to Enable (General Steps):**
1. Go to account Security Settings
2. Find "Two-Factor Authentication" or "2-Step Verification"
3. Choose method:
   - **Authenticator App** (BEST) - Google Authenticator, Authy
   - **SMS** (OKAY) - Text message codes
   - **Email** (WEAKEST) - Avoid if possible

### Step 8.2: Authenticator App Setup
1. Download: **Google Authenticator** (iOS/Android)
   - OR **Microsoft Authenticator**
   - OR **Authy**
2. For each account:
   - Scan QR code shown during 2FA setup
   - Save backup codes in safe place
   - Test that it works

### Step 8.3: Backup Codes
For each 2FA-enabled account:
- [ ] Download backup codes
- [ ] Print or save in secure location
- [ ] Store separately from devices

---

## 🔌 SECTION 9: Third-Party App Permissions

### Step 9.1: Google Account Apps
1. Already checked in Section 3.3
2. Double-check you removed unnecessary apps

### Step 9.2: Facebook App Permissions
1. Go to: **Settings → Apps and Websites**
2. For each app:
   - [ ] Do you still use it? Remove if not
   - [ ] What data does it access? Remove if excessive
   - [ ] Is it from trusted company? Remove if suspicious

### Step 9.3: Apple/iCloud Apps
1. Go to: **Settings → [Your Name] → Password & Security**
2. Review "Apps Using Apple ID"
3. Remove any you don't use

### Step 9.4: Microsoft Account Apps
1. Go to: **account.microsoft.com/privacy**
2. Check connected apps
3. Remove unnecessary ones

### Step 9.5: Twitter/X Apps
1. Settings → Security and account access → Apps and sessions
2. Review and revoke

---

## 🕵️ SECTION 10: Data Broker & People Search Sites

### Step 10.1: Check Your Presence
Check these free people search sites:

1. **Whitepages** - https://www.whitepages.com
   - [ ] Search your name
   - [ ] Found? Yes/No: ______
   - [ ] Info shown: ______________________

2. **Spokeo** - https://www.spokeo.com
   - [ ] Search your name and location
   - [ ] Found? Yes/No: ______
   - [ ] Info shown: ______________________

3. **BeenVerified** - https://www.beenverified.com
   - [ ] Search your name
   - [ ] Found? Yes/No: ______

4. **MyLife** - https://www.mylife.com
   - [ ] Search your name
   - [ ] Found? Yes/No: ______

5. **PeekYou** - https://www.peekyou.com
   - [ ] Search your name
   - [ ] Found? Yes/No: ______

### Step 10.2: Opt-Out Requests
For sites where you're found:

**General Opt-Out Process:**
1. Find "Opt Out" or "Remove My Information" link (usually in footer)
2. Search for your listing again
3. Follow their removal process (varies by site)
4. Document submission date
5. Check back in 72 hours to verify removal

**Note:** This is time-consuming but important. Budget 1-2 hours for this section.

### Step 10.3: UK-Specific Checks
Since you're UK-based:

1. **192.com** - https://www.192.com
   - [ ] Check if you're listed
   - [ ] Request removal if found

2. **Electoral Roll**
   - [ ] Check if you're on open register
   - [ ] Contact local council to opt out if desired

---

## 📊 SECTION 11: Set Up Ongoing Monitoring

### Step 11.1: Google Alerts
1. Go to: **https://www.google.com/alerts**
2. Create alerts for:
   - [ ] "Ewan Bramley"
   - [ ] ewanbramley@gmail.com
   - [ ] Your phone number
   - [ ] Your address (if concerned)
3. Set frequency: "As it happens" or "Daily"

### Step 11.2: Have I Been Pwned Notifications
1. Go to: **https://haveibeenpwned.com/NotifyMe**
2. Enter: ewanbramley@gmail.com
3. Confirm subscription
4. You'll be notified of future breaches

### Step 11.3: Credit Monitoring (Optional)
Consider signing up for:
- [ ] **Experian** (UK) - Free credit report
- [ ] **Equifax** (UK) - Free credit report
- [ ] **TransUnion** (UK) - Free credit report

### Step 11.4: Privacy.com Monitoring
1. Go to: **https://www.privacy.com** (US) or equivalent UK service
2. Consider virtual credit cards for online purchases

---

## 📝 SECTION 12: Document Your Findings

### Step 12.1: Create Master Report
Create a document with these sections:

**EXECUTIVE SUMMARY**
- Total breaches found: _______
- Critical issues found: _______
- Accounts requiring immediate action: _______
- Overall risk level: Low / Medium / High

**DETAILED FINDINGS**

**1. Data Breaches**
```
Breach Name: _______________
Date: _______________
Data Exposed: _______________
Action Taken: _______________
Date Resolved: _______________
```

**2. Exposed Personal Information**
- Where found: _______________
- Type of info: _______________
- Risk level: Low / Medium / High
- Action taken: _______________

**3. Vulnerable Accounts**
| Account | Issue | Risk | Action Taken | Date |
|---------|-------|------|--------------|------|
|         |       |      |              |      |

**4. Privacy Settings Updated**
- [ ] Google account
- [ ] Facebook
- [ ] LinkedIn
- [ ] Instagram
- [ ] Other: ______________

**5. Security Improvements**
- [ ] Passwords changed: _____ accounts
- [ ] 2FA enabled: _____ accounts
- [ ] Apps removed: _____ apps
- [ ] Accounts deleted: _____ accounts

**6. Ongoing Monitoring Setup**
- [ ] Google Alerts configured
- [ ] HIBP notifications enabled
- [ ] Credit monitoring active

### Step 12.2: Create Action Plan
**IMMEDIATE (Do Today):**
1. ______________________________
2. ______________________________
3. ______________________________

**SHORT-TERM (This Week):**
1. ______________________________
2. ______________________________
3. ______________________________

**ONGOING (Monthly):**
1. ______________________________
2. ______________________________
3. ______________________________

---

## ⚠️ RED FLAGS TO WATCH FOR

While conducting this audit, STOP and investigate immediately if you find:

🚨 **CRITICAL - Act Now:**
- Unknown forwarding rules in email
- Sign-ins from unknown locations
- Unknown devices with account access
- Financial accounts you didn't open
- Unfamiliar transactions

⚠️ **HIGH PRIORITY:**
- Passwords found in breaches
- Personal info on data broker sites
- Apps with excessive permissions
- Accounts without 2FA
- Weak/reused passwords

⚡ **MEDIUM PRIORITY:**
- Old inactive accounts
- Oversharing on social media
- Lack of privacy settings
- Too many connected apps

---

## ✅ FINAL CHECKLIST

Before considering this audit complete:

**Security Basics:**
- [ ] All breached passwords changed
- [ ] 2FA enabled on critical accounts
- [ ] Strong, unique passwords on important accounts
- [ ] Unknown apps/devices removed

**Privacy Settings:**
- [ ] Google privacy settings optimized
- [ ] Social media privacy locked down
- [ ] Search engine results reviewed
- [ ] Data broker opt-outs submitted

**Monitoring:**
- [ ] Google Alerts set up
- [ ] HIBP notifications enabled
- [ ] Monthly review scheduled

**Documentation:**
- [ ] All findings documented
- [ ] Action items prioritized
- [ ] Ongoing plan created

---

## 📅 RECOMMENDED SCHEDULE

**Monthly:**
- [ ] Review Google security checkup
- [ ] Check for new data breaches
- [ ] Review connected apps/permissions
- [ ] Check Google Alerts

**Quarterly:**
- [ ] Update important passwords
- [ ] Review social media privacy settings
- [ ] Check data broker sites again
- [ ] Review account inventory

**Annually:**
- [ ] Complete full audit (this document)
- [ ] Update security strategy
- [ ] Review and update 2FA methods

---

## 🆘 HELP & RESOURCES

**If You Find Evidence of Identity Theft:**
1. Contact Action Fraud (UK): 0300 123 2040
2. Report to local police
3. Contact your bank immediately
4. Place fraud alert on credit reports

**Additional Resources:**
- **UK Gov Cyber Aware:** https://www.ncsc.gov.uk/cyberaware
- **Action Fraud:** https://www.actionfraud.police.uk/
- **ICO (Data Protection):** https://ico.org.uk/

**Privacy Tools:**
- **Have I Been Pwned:** https://haveibeenpwned.com
- **Privacy Rights Clearinghouse:** https://privacyrights.org
- **Opt Out Prescreen (US):** https://www.optoutprescreen.com

---

## 📌 NOTES SECTION

Use this space to track additional findings, concerns, or actions:

```
Date: _______________
Finding: _______________________________________
_________________________________________________
_________________________________________________

Action Required: ________________________________
_________________________________________________

Status: [ ] Pending  [ ] In Progress  [ ] Complete

Date Resolved: _______________
```

---

**Audit Completed By:** _____________________  
**Date:** _____________________  
**Next Audit Due:** _____________________

---

*Remember: Your digital privacy is an ongoing process, not a one-time task. Schedule time monthly to maintain your security posture.*