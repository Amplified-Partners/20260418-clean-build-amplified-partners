---
title: "Hazel Parameters"
id: "hazel-parameters"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "2026-04-23-hazel-parameters-ewan-approval-sheet.md"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Hazel parameters — set by Rowan, approved by Ewan, executed by Ewan

**Document date (ISO 8601):** 2026-04-23  

**How this works:** I cannot tap the Hazel window on your Mac. What I *can* do is **fix every number and path here** so you squint once, say yes, then **match** Hazel to this sheet (or run the script). Your finger still owns **Install**, **Full Disk Access**, and **Save** in Hazel — that protects everyone.

---

## 1. Paths (edit only if you use different locations)

| Parameter | Value to use | Your OK? |
|-----------|----------------|----------|
| Downloads | `/Users/ewansair/Downloads` | [ ] |
| Desktop | `/Users/ewansair/Desktop` | [ ] |
| Quarantine parent (create in Finder first) | `/Users/ewansair/Downloads/_hazel-quarantine` | [ ] |

**Rule:** Put **nothing** canonical inside quarantine long-term. It is a holding pen until backup rhythm + your merge decisions.

---

## 2. Numbers (conservative on purpose)

| Parameter | Value | Meaning |
|-----------|------:|---------|
| `SCREENSHOT_AGE_DAYS` | **30** | Desktop `Screenshot*.png` older than this → *candidate* for a move rule only after you enable it |
| Zero-byte files | **match only** | Downloads, depth 1, size 0 — list is in latest dummy report |
| `(1)` duplicate files | **manual or Hazel Duplicate UI first** | Script already proved **3** byte-identical pairs; **no** auto-delete in any script I ship |

---

## 3. Dummy run command (no Hazel required)

```bash
cd /Users/ewansair/2026-04-26-Research
bash scripts/hazel-dummy-run-mac-air-1.sh
```

Open the newest file under `docs/_hazel-dummy-run-output/` and skim the tables. That is the **check** before you mirror anything in Hazel.

---

## 4. First Hazel rules after approval (mirror these exactly)

**Order:** enable **one** rule, run a week or a day, then add the next.

1. **Rule name:** `AP-Q1-zero-byte-downloads`  
   - Folder: Downloads (depth 1).  
   - If: size is 0, kind is file.  
   - Do: move into `…/_hazel-quarantine/zero-byte/`.  
   - Do **not** add Trash.

2. **Rule name:** `AP-Q2-old-screenshots-desktop`  
   - Folder: Desktop (depth 1).  
   - If: name matches `Screenshot*.png` OR `Screen Shot*.png`, modified date > 30 days ago.  
   - Do: move into `…/_hazel-quarantine/screenshots-YYYY-MM/`.  
   - Do **not** add Trash.

3. **Rule name:** defer `AP-dedupe-md` until you say — duplicates stay **review** in Hazel’s UI, not auto-annihilate.

---

## 5. Approval line (you type or tick)

When the table in §1 and numbers in §2 are correct for **this** Mac, write **one** line below (or tell me in chat) and only then turn rules on:

**I approve parameters as above on Mac Air 1 — Ewan — date: ________**

---

## Related

- Dummy run pack: [`2026-04-23-hazel-mac-air-1-dummy-run-pack.md`](2026-04-23-hazel-mac-air-1-dummy-run-pack.md)  
- Cross-Mac guardrails (later, when SSD + backup): [`2026-04-23-amplified-partners-cross-mac-automation-guardrails.md`](2026-04-23-amplified-partners-cross-mac-automation-guardrails.md)
