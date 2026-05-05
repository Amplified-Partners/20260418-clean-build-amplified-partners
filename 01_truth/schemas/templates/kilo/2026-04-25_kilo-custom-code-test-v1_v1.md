---
title: "Kilo Code - Custom Code Speed Test"
id: "kilo-custom-code-test-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "agent-tooling"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Kilo Code - Custom Code Speed Test

**Objective:** Measure how quickly Kilo Code can write production-ready custom code. Real problem. Real constraints. Real timeline.

---

## Test Scenario: Newcastle SME Custom Development

**Context:** You're building custom solutions for Newcastle SMEs who need functionality that off-the-shelf tools don't cover. You need to know: How fast can Kilo Code write real, working code?

This test measures your speed on a **realistic, moderate-complexity custom build** that requires:
- Backend logic (data processing, validation)
- Integration thinking (APIs, databases)
- Error handling & edge cases
- Clean, maintainable code
- Testing

---

## The Test: Invoice Processing & Categorization Service

### **Briefing**

A Newcastle accountancy firm processes 50-200 invoices per day. They need a **custom Python backend** that:

1. **Receives invoice data** via REST API (JSON input)
2. **Extracts/validates** key fields:
   - Vendor name
   - Amount (£)
   - Date (YYYY-MM-DD)
   - Invoice number
   - Description/items
3. **Categorizes expense** (Office Supplies / Travel / Professional Services / Equipment / Other)
4. **Validates against rules:**
   - Amount must be > £0
   - Date must be recent (within last 90 days)
   - Vendor name cannot be blank
   - Duplicate check (same vendor + amount + date within 24 hours = likely duplicate)
5. **Returns structured response:**
   ```json
   {
     "status": "success" | "error",
     "invoice_id": "generated UUID",
     "vendor": "string",
     "amount": number,
     "date": "YYYY-MM-DD",
     "category": "string",
     "is_duplicate": boolean,
     "validation_errors": ["list of issues"],
     "processed_at": "ISO timestamp"
   }
   ```
6. **Logs everything** (for audit trail, debugging, analytics)
7. **Handles errors gracefully:**
   - Malformed JSON → Return 400 with error message
   - Missing required fields → Return 400 with which fields missing
   - Database error → Return 500, log error, alert admin
   - Duplicate detected → Return 200 with is_duplicate: true (don't reject, just flag)

---

## Test Requirements

### **Part 1: What You're Building**

A **Python REST API service** (using Flask or FastAPI) with:

**Endpoints:**
- `POST /process-invoice` - Accept invoice data, return processed result
- `GET /invoice/<invoice_id>` - Retrieve previously processed invoice
- `GET /health` - Health check for monitoring

**Database:**
- PostgreSQL or SQLite (simple, local OK for test)
- Store all processed invoices with timestamp
- Query for duplicates by (vendor, amount, date)

**Processing Logic:**
- Validate all inputs
- Check for duplicates (exact match or "suspicious" matches)
- Categorize based on keywords in description
  - "office", "supplies", "stationery" → Office Supplies
  - "taxi", "hotel", "flight", "parking", "fuel" → Travel
  - "consulting", "accounting", "legal", "design" → Professional Services
  - "computer", "equipment", "furniture", "machinery" → Equipment
  - Default: Other
- Return structured response

**Error Handling:**
- Invalid JSON → 400 error with message
- Missing fields → 400 error listing what's missing
- Validation failed → 400 error explaining why
- Database error → 500 error, log details, notify admin (print to stdout for this test)
- Unexpected error → 500 error, log full stack trace

**Code Quality:**
- Clean, readable Python (PEP 8 style)
- Docstrings on functions
- Type hints where appropriate
- Comments on complex logic
- No hardcoded secrets (use environment variables)

---

### **Part 2: Sample Test Data**

Use these to validate your solution works:

**Test Case 1: Valid Invoice**
```json
{
  "vendor": "Office Depot",
  "amount": 150.50,
  "date": "2026-01-10",
  "invoice_number": "INV-2026-001",
  "description": "Office supplies: pens, paper, folders"
}
```
Expected: Success, category = "Office Supplies", is_duplicate = false

**Test Case 2: Travel Expense**
```json
{
  "vendor": "Travelodge Hotels",
  "amount": 89.99,
  "date": "2026-01-08",
  "invoice_number": "HOTEL-12345",
  "description": "Hotel accommodation, Manchester"
}
```
Expected: Success, category = "Travel", is_duplicate = false

**Test Case 3: Missing Field**
```json
{
  "vendor": "ABC Corp",
  "amount": 500,
  "date": "2026-01-12"
}
```
Expected: Error 400, message: "Missing required fields: invoice_number, description"

**Test Case 4: Invalid Amount**
```json
{
  "vendor": "Some Vendor",
  "amount": -50,
  "date": "2026-01-12",
  "invoice_number": "INV-999",
  "description": "Test"
}
```
Expected: Error 400, message: "Amount must be greater than 0"

**Test Case 5: Date Too Old**
```json
{
  "vendor": "Old Vendor",
  "amount": 100,
  "date": "2024-06-01",
  "invoice_number": "INV-OLD",
  "description": "Old invoice"
}
```
Expected: Error 400, message: "Date must be within last 90 days"

**Test Case 6: Duplicate Detection**
(Process Test Case 1, then submit identical data again)
Expected: Success, but is_duplicate = true

---

### **Part 3: Deliverables**

When complete, provide:

1. **Full Source Code**
   - `app.py` or `main.py` - Flask/FastAPI application
   - `models.py` - Database models (if needed)
   - `validators.py` - Validation logic
   - `requirements.txt` - Python dependencies
   - `.env.example` - Environment variables template
   - `README.md` - How to run it

2. **Testing Evidence**
   - Run your code against all 6 test cases
   - Show actual inputs → actual outputs
   - Prove it works (screenshots or terminal output)
   - Test edge cases (empty strings, unicode characters, large amounts)

3. **Documentation**
   - API endpoint documentation (what each endpoint does, required fields, response format)
   - Database schema (if using database)
   - Installation & setup instructions
   - How to test locally
   - How to deploy (basic Docker instructions appreciated but not required)

4. **Time Log**
   - When you started
   - When you finished
   - Actual time spent
   - Any blockers or challenges
   - What you'd improve for production

---

### **Part 4: Evaluation Criteria**

✅ **Works:** Code runs, all 6 test cases pass  
✅ **Handles errors:** Invalid inputs don't crash it, return sensible error messages  
✅ **Duplicate detection:** Actually works, tested  
✅ **Database logic:** Correctly stores and retrieves data  
✅ **Code quality:** Clean, readable, maintainable  
✅ **Production-ready:** Enough for a real customer to use (not perfect, but reliable)  
✅ **Speed:** How long did it actually take from start to finish?  
✅ **Communication:** Can someone else understand and modify your code?

---

## Timeline & Constraints

**Deadline:** [You set based on availability]

**Constraints:**
- Use Python (3.9+) with Flask or FastAPI
- Database: PostgreSQL or SQLite (local OK for test)
- No external ML/AI models—simple keyword matching for categorization is fine
- Code should be deployable (not just a one-off script)
- Must handle the error cases (don't assume perfect input)

**Estimated effort:** 4-8 hours for someone competent
- Design & setup: 30 min
- Core API: 2-3 hours
- Database & validation: 1-2 hours
- Testing & edge cases: 1-2 hours
- Documentation: 30 min

---

## Real-World Payoff

**After completion:**
- We know: "Custom code projects like this take ~X hours"
- We can estimate bigger projects: "20 endpoints = ~X weeks"
- We have a working template for invoice processing (reusable for other clients)
- We understand Kilo Code's approach: Do they think about scalability? Error handling? Testing?
- We know if they're reliable for custom development work

---

## How This Measures Real Ability

| Skill | What We See |
|-------|------------|
| **Backend thinking** | How they structure the code, separation of concerns |
| **Error handling** | Do they think about what could go wrong? |
| **Speed** | Fast = knows their tools, slow = learning as they go |
| **Quality** | Is it barely working or robust? |
| **Communication** | Can they explain their design? Can others maintain it? |
| **Problem-solving** | How do they handle the duplicate detection problem? Smart approach or brute force? |

---

## Questions Before Starting?

- Preferred framework: Flask or FastAPI? (FastAPI is faster to build, more modern)
- Database preference: PostgreSQL or SQLite? (SQLite is simpler for local testing)
- Should I provide starter code, or build from scratch?
- Any libraries you're comfortable with (ORM, validation, etc.)?

**Start timer when you begin. Document everything. Let's see the real speed and quality.**

---

**Test created:** January 12, 2026  
**Status:** Ready for execution  
**Purpose:** Measure speed and quality on realistic custom Python backend work