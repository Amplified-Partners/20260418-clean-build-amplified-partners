---
title: "AI STACK AUDITOR - TECHNICAL SPECIFICATION"
id: "ai-stack-auditor-technical-spec"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "spec"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# AI STACK AUDITOR - TECHNICAL SPECIFICATION
**Project:** Subscription & SaaS Cost Audit Automation  
**Date:** 2026-01-13  
**Budget:** £500-1,000  
**Target:** £200-500/month savings identification

---

## 📋 PROJECT OVERVIEW

### Objective
Build a Python script that automatically audits AI/SaaS subscriptions by scanning emails, payment processors, and bank statements, then generates actionable cost-saving recommendations using Claude AI analysis.

### Success Criteria
- ✅ Captures 95%+ of actual subscriptions
- ✅ Identifies £200-500/month in potential savings
- ✅ Runs in <30 minutes monthly
- ✅ Produces clear, actionable recommendations

### Assumptions (Based on Brief)
1. **Email:** Gmail only (personal account)
2. **Payment Processors:** Stripe + PayPal APIs
3. **Bank Data:** Manual CSV upload (Barclays format)
4. **Timeframe:** 12 months historical analysis
5. **Automation:** 95% automated + 5% manual entry
6. **Usage:** Monthly recurring audit

---

## 🏗️ SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────┐
│                 AI STACK AUDITOR                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Gmail     │  │   Stripe     │  │   PayPal     │  │
│  │   Scanner   │  │   API        │  │   API        │  │
│  └──────┬──────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                │                  │           │
│         └────────────────┼──────────────────┘           │
│                          │                              │
│                   ┌──────▼───────┐                      │
│                   │  Data        │                      │
│                   │  Collector   │◄─────────┐           │
│                   └──────┬───────┘          │           │
│                          │             ┌────┴─────┐     │
│                   ┌──────▼───────┐    │ Bank CSV  │     │
│                   │  Deduplicator│    │ Parser    │     │
│                   └──────┬───────┘    └──────────┘     │
│                          │                              │
│                   ┌──────▼───────┐                      │
│                   │  Usage       │                      │
│                   │  Scorer      │                      │
│                   └──────┬───────┘                      │
│                          │                              │
│                   ┌──────▼───────┐                      │
│                   │  Claude AI   │                      │
│                   │  Analyzer    │                      │
│                   └──────┬───────┘                      │
│                          │                              │
│         ┌────────────────┴────────────────┐             │
│         │                                 │             │
│  ┌──────▼──────┐               ┌─────────▼────────┐    │
│  │  CSV        │               │  HTML Dashboard  │    │
│  │  Inventory  │               │  + Action Plan   │    │
│  └─────────────┘               └──────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📂 PROJECT STRUCTURE

```
ai-stack-auditor/
├── README.md                    # Setup and usage instructions
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
├── .gitignore                   # Git ignore rules
│
├── src/
│   ├── __init__.py
│   ├── main.py                  # Entry point and orchestration
│   ├── config.py                # Configuration management
│   │
│   ├── collectors/              # Data collection modules
│   │   ├── __init__.py
│   │   ├── gmail_scanner.py     # Gmail API integration
│   │   ├── stripe_client.py     # Stripe API integration
│   │   ├── paypal_client.py     # PayPal API integration
│   │   └── bank_parser.py       # CSV/PDF bank statement parser
│   │
│   ├── processors/              # Data processing
│   │   ├── __init__.py
│   │   ├── deduplicator.py      # Fuzzy matching & deduplication
│   │   ├── usage_scorer.py      # Calculate 0-10 usage scores
│   │   └── categorizer.py       # Categorize subscriptions
│   │
│   ├── analyzers/               # AI analysis
│   │   ├── __init__.py
│   │   └── claude_analyzer.py   # Claude API for recommendations
│   │
│   ├── generators/              # Output generation
│   │   ├── __init__.py
│   │   ├── csv_generator.py     # Generate inventory CSV
│   │   ├── dashboard_generator.py # Generate HTML dashboard
│   │   └── action_plan_generator.py # Generate action items
│   │
│   └── utils/                   # Shared utilities
│       ├── __init__.py
│       ├── logger.py            # Logging configuration
│       ├── validators.py        # Input validation
│       └── helpers.py           # Common helper functions
│
├── data/                        # Input data directory
│   ├── bank_statements/         # CSV/PDF bank statements
│   ├── manual_entries.json      # Manual subscription entries
│   └── .gitkeep
│
├── output/                      # Generated reports
│   ├── inventory.csv            # Current audit
│   ├── dashboard.html           # Visual dashboard
│   ├── action_plan.md           # Actionable recommendations
│   └── audit_history/           # Previous audits
│       └── 2026-01-13/
│
├── tests/                       # Unit and integration tests
│   ├── __init__.py
│   ├── test_collectors.py
│   ├── test_processors.py
│   └── test_generators.py
│
└── templates/                   # HTML/email templates
    └── dashboard_template.html  # Dashboard layout
```

---

## 🔧 TECHNICAL STACK

### Core Dependencies
```python
# requirements.txt

# Google APIs
google-auth==2.25.2
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
google-api-python-client==2.110.0

# Payment Processor APIs
stripe==7.9.0
paypal-checkout-serversdk==1.0.1

# AI Analysis
anthropic==0.8.1

# Data Processing
pandas==2.1.4
numpy==1.26.2
fuzzywuzzy==0.18.0
python-Levenshtein==0.23.0

# PDF/CSV Parsing
PyPDF2==3.0.1
pdfplumber==0.10.3
chardet==5.2.0

# Utilities
python-dotenv==1.0.0
requests==2.31.0
tqdm==4.66.1

# Visualization (for dashboard)
jinja2==3.1.2
plotly==5.18.0

# Testing
pytest==7.4.3
pytest-cov==4.1.0
```

---

## 🔐 SECURITY & PRIVACY

### API Keys (Environment Variables)
```bash
# .env.example

# Gmail API
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret
GMAIL_TOKEN_PATH=./credentials/gmail_token.json

# Stripe API
STRIPE_SECRET_KEY=sk_test_...
STRIPE_ACCOUNT_ID=acct_...

# PayPal API
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
PAYPAL_MODE=sandbox  # or 'live'

# Claude AI
ANTHROPIC_API_KEY=sk-ant-...

# Configuration
AUDIT_MONTHS_BACK=12
MIN_SUBSCRIPTION_AMOUNT=5.00
OUTPUT_DIR=./output
```

### Security Measures
1. **Gmail API:** Read-only scope (`gmail.readonly`)
2. **Local Storage:** All data processed locally, not sent to cloud
3. **API Keys:** Environment variables only, never committed
4. **Bank Data:** Processed in memory, deleted after audit
5. **Token Storage:** OAuth tokens stored in `./credentials/` (gitignored)

---

## 📊 DATA MODELS

### Subscription Record
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Literal

@dataclass
class Subscription:
    """Core subscription data model"""
    
    # Identification
    service_name: str
    service_url: Optional[str]
    category: str  # "AI", "SaaS", "Cloud", "Tools", etc.
    
    # Financial
    cost_monthly: float
    cost_annual: float
    currency: str = "GBP"
    billing_frequency: Literal["monthly", "annual", "quarterly", "one-time"]
    
    # Dates
    first_charged: datetime
    last_charged: datetime
    next_billing: Optional[datetime]
    
    # Payment
    payment_method: str  # "Stripe", "PayPal", "Direct Debit", "Card"
    payment_details: Optional[str]  # Last 4 digits, email, etc.
    
    # Status
    status: Literal["active", "canceled", "trial", "expired"]
    
    # Usage Analysis
    usage_score: float  # 0-10
    last_login: Optional[datetime]
    emails_count: int  # Emails from service in last 30 days
    
    # AI Recommendation
    ai_recommendation: Optional[Literal["KEEP", "REVIEW", "CANCEL", "CONSOLIDATE"]]
    ai_reasoning: Optional[str]
    consolidation_suggestion: Optional[str]
    
    # Metadata
    data_source: str  # "gmail", "stripe", "paypal", "bank", "manual"
    confidence: float  # 0-1 match confidence
```

### Usage Scoring Algorithm
```python
def calculate_usage_score(subscription: Subscription) -> float:
    """
    Calculate 0-10 usage score based on:
    - Email activity (30%)
    - Payment recency (30%)
    - Login frequency (25%)
    - Manual feedback (15%)
    """
    
    score = 0.0
    
    # Email activity (0-3 points)
    if subscription.emails_count > 10:
        score += 3.0
    elif subscription.emails_count > 5:
        score += 2.0
    elif subscription.emails_count > 0:
        score += 1.0
    
    # Payment recency (0-3 points)
    days_since_charge = (datetime.now() - subscription.last_charged).days
    if days_since_charge < 30:
        score += 3.0
    elif days_since_charge < 90:
        score += 2.0
    elif days_since_charge < 180:
        score += 1.0
    
    # Last login (0-2.5 points)
    if subscription.last_login:
        days_since_login = (datetime.now() - subscription.last_login).days
        if days_since_login < 7:
            score += 2.5
        elif days_since_login < 30:
            score += 1.5
        elif days_since_login < 90:
            score += 0.5
    
    # Manual feedback (0-1.5 points)
    # Will be added via manual review
    
    return round(score, 1)
```

---

## 🔄 WORKFLOW

### Phase 1: Data Collection (15 mins)
```python
# src/main.py

async def collect_data():
    """Orchestrate data collection from all sources"""
    
    logger.info("Starting data collection...")
    
    # Parallel collection
    tasks = [
        collect_gmail_receipts(),
        collect_stripe_subscriptions(),
        collect_paypal_subscriptions(),
        parse_bank_statements(),
        load_manual_entries()
    ]
    
    results = await asyncio.gather(*tasks)
    
    # Flatten and combine
    all_subscriptions = []
    for result in results:
        all_subscriptions.extend(result)
    
    logger.info(f"Collected {len(all_subscriptions)} potential subscriptions")
    return all_subscriptions
```

### Phase 2: Deduplication (5 mins)
```python
# src/processors/deduplicator.py

def deduplicate_subscriptions(subs: List[Subscription]) -> List[Subscription]:
    """
    Use fuzzy matching to deduplicate subscriptions from multiple sources
    Confidence threshold: 85%
    """
    
    unique_subs = []
    seen = set()
    
    for sub in subs:
        # Generate signature
        signature = generate_subscription_signature(sub)
        
        # Check for matches
        best_match = None
        best_score = 0
        
        for existing in unique_subs:
            score = fuzz.token_set_ratio(
                signature,
                generate_subscription_signature(existing)
            )
            
            if score > best_score:
                best_score = score
                best_match = existing
        
        if best_score > 85:
            # Merge with existing
            unique_subs.remove(best_match)
            merged = merge_subscriptions(best_match, sub)
            unique_subs.append(merged)
        else:
            # Add as new
            unique_subs.append(sub)
    
    return unique_subs
```

### Phase 3: AI Analysis (5 mins)
```python
# src/analyzers/claude_analyzer.py

async def analyze_subscription(sub: Subscription) -> dict:
    """
    Use Claude to analyze subscription and provide recommendation
    """
    
    prompt = f"""
Analyze this subscription and provide a recommendation:

Service: {sub.service_name}
Category: {sub.category}
Cost: £{sub.cost_monthly}/month (£{sub.cost_annual}/year)
Usage Score: {sub.usage_score}/10
Last Used: {sub.last_charged}
Emails (30d): {sub.emails_count}

Provide:
1. Recommendation (KEEP/REVIEW/CANCEL/CONSOLIDATE)
2. Brief reasoning (1-2 sentences)
3. If CONSOLIDATE, suggest alternative

Format as JSON:
{{
  "recommendation": "KEEP|REVIEW|CANCEL|CONSOLIDATE",
  "reasoning": "...",
  "alternative": "..." // if consolidate
}}
"""
    
    response = await client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return json.loads(response.content[0].text)
```

### Phase 4: Report Generation (5 mins)
```python
# src/generators/dashboard_generator.py

def generate_dashboard(subs: List[Subscription]) -> str:
    """
    Generate HTML dashboard with:
    - Cost summary
    - Category breakdown
    - Usage heatmap
    - Recommendations
    - Action items
    """
    
    template = jinja2.Template(open('templates/dashboard_template.html').read())
    
    context = {
        'total_monthly': sum(s.cost_monthly for s in subs),
        'total_annual': sum(s.cost_annual for s in subs),
        'subscriptions': subs,
        'by_category': group_by_category(subs),
        'recommendations': {
            'keep': [s for s in subs if s.ai_recommendation == 'KEEP'],
            'review': [s for s in subs if s.ai_recommendation == 'REVIEW'],
            'cancel': [s for s in subs if s.ai_recommendation == 'CANCEL'],
            'consolidate': [s for s in subs if s.ai_recommendation == 'CONSOLIDATE']
        },
        'potential_savings': calculate_savings(subs)
    }
    
    return template.render(context)
```

---

## 📈 OUTPUT SPECIFICATIONS

### 1. CSV Inventory
```csv
Service,Category,Cost/Month,Cost/Year,Last Used,First Charged,Payment Method,Status,Usage Score,Action
"Claude API","AI",£150.00,£1800.00,2026-01-12,2025-01-15,"Stripe *1234","active",9.5,"KEEP"
"Old SaaS Tool","Tools",£29.00,£348.00,2025-11-03,2024-03-10,"PayPal","active",2.1,"CANCEL"
"ChatGPT Plus","AI",£20.00,£240.00,2026-01-13,2023-06-01,"Card *5678","active",8.7,"KEEP"
```

### 2. HTML Dashboard
Key elements:
- **Header:** Total costs (monthly/annual), trend vs last month
- **Category Pie Chart:** Breakdown by subscription type
- **Usage Heatmap:** Visual grid of usage scores
- **Recommendations Table:** Sortable, filterable subscription list
- **Action Items:** Prioritized list with savings estimates

### 3. Action Plan (Markdown)
```markdown
# Subscription Audit - Action Plan
**Date:** 2026-01-13  
**Total Monthly Cost:** £347.00  
**Potential Savings:** £89.00/month (26%)

## 🔴 IMMEDIATE CANCELLATIONS (Save £54/mo)
1. **Old SaaS Tool** - £29/mo
   - Last used: 2 months ago
   - Usage score: 2.1/10
   - Action: Cancel immediately
   
2. **Unused Design Tool** - £25/mo
   - Last used: 4 months ago
   - Usage score: 1.3/10
   - Action: Cancel immediately

## 🟡 REVIEW IN 30 DAYS (£35/mo at risk)
1. **Marketing Platform** - £35/mo
   - Usage score: 4.5/10
   - Action: Track usage, decide by Feb 13

## 🔵 CONSOLIDATION OPPORTUNITIES (Save £50/mo)
1. **Replace 3 tools with Notion**
   - Current: Tool A (£15) + Tool B (£20) + Tool C (£15)
   - Alternative: Notion Team (£10/mo)
   - Savings: £40/mo

## ✅ KEEP (High Value)
- Claude API (9.5/10)
- ChatGPT Plus (8.7/10)
- GitHub Copilot (8.2/10)
```

---

## 🎯 IMPLEMENTATION PHASES

### Phase 1: Foundation (Days 1-2)
- [ ] Set up project structure
- [ ] Configure environment variables
- [ ] Implement base data models
- [ ] Set up logging and error handling
- [ ] Create test suite framework

### Phase 2: Data Collection (Days 3-5)
- [ ] Gmail API integration
- [ ] Stripe API integration
- [ ] PayPal API integration
- [ ] Bank statement parser (CSV)
- [ ] Manual entry system

### Phase 3: Processing (Days 6-7)
- [ ] Deduplication engine
- [ ] Usage scorer
- [ ] Categorization logic
- [ ] Data validation

### Phase 4: AI Analysis (Day 8)
- [ ] Claude API integration
- [ ] Recommendation engine
- [ ] Consolidation suggestions

### Phase 5: Output Generation (Days 9-10)
- [ ] CSV generator
- [ ] HTML dashboard (with Chart.js)
- [ ] Action plan generator
- [ ] Email summary (optional)

### Phase 6: Testing & Polish (Days 11-12)
- [ ] End-to-end testing with sample data
- [ ] Error handling refinement
- [ ] Documentation
- [ ] Deployment script for monthly cron

---

## 🚀 USAGE

### Initial Setup
```bash
# Clone repository
cd ~/Documents/ai-stack-auditor

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys

# Authenticate Gmail
python src/auth/gmail_setup.py

# Run initial audit
python src/main.py
```

### Monthly Audit
```bash
# Option 1: Manual run
python src/main.py

# Option 2: Cron job (macOS)
# Add to crontab:
# 0 9 1 * * cd ~/Documents/ai-stack-auditor && python src/main.py
```

### Output Location
```
output/
├── inventory.csv          # Latest audit
├── dashboard.html         # Open in browser
├── action_plan.md         # Review and execute
└── audit_history/
    └── 2026-01-13/       # Archived audits
```

---

## 📊 SUCCESS METRICS

### Capture Rate
- **Target:** 95%+ of actual subscriptions
- **Validation:** Manual cross-check against known subscriptions
- **Fallback:** Manual entry form for any gaps

### Accuracy
- **Target:** <5% false positives (non-subscriptions flagged)
- **Target:** >90% correct categorization
- **Target:** >85% deduplication accuracy

### Performance
- **Target:** <30 minutes total runtime
- **Gmail scan:** <10 minutes
- **API calls:** <5 minutes
- **Analysis:** <10 minutes
- **Report generation:** <5 minutes

### Savings Identification
- **Target:** Identify £200-500/month in potential savings
- **Breakdown:**
  - Unused subscriptions: £100-200/mo
  - Consolidation opportunities: £50-150/mo
  - Downgrade opportunities: £50-150/mo

---

## ⚠️ EDGE CASES & HANDLING

### 1. Annual Subscriptions
```python
# Normalize to monthly for comparison
if subscription.billing_frequency == "annual":
    subscription.cost_monthly = subscription.cost_annual / 12
```

### 2. Trial Periods
```python
# Flag trials separately
if subscription.status == "trial":
    # Check trial end date
    # Warn if trial ending soon
    # Flag for review before conversion
```

### 3. Shared/Family Plans
```python
# Manual entry required for split costs
# Example: Netflix family plan (£15/mo, 4 users = £3.75 each)
```

### 4. One-Time Purchases
```python
# Filter out or flag separately
if subscription.billing_frequency == "one-time":
    # Don't include in recurring cost analysis
    # But show in one-time expenses report
```

### 5. Failed Payment Methods
```python
# Gmail: Search for "payment failed" emails
# Mark subscription as "at risk"
# Flag for immediate action
```

---

## 🔍 TESTING STRATEGY

### Unit Tests
```python
# tests/test_deduplicator.py
def test_fuzzy_matching():
    """Test that 'ChatGPT Plus' and 'OpenAI ChatGPT' match"""
    assert match_score("ChatGPT Plus", "OpenAI ChatGPT") > 0.85

def test_signature_generation():
    """Test subscription signature generation"""
    sig = generate_subscription_signature(sub)
    assert "chatgpt" in sig.lower()
    assert "openai" in sig.lower()
```

### Integration Tests
```python
# tests/test_integration.py
def test_full_audit_flow():
    """Test complete audit with sample data"""
    # Run full audit
    result = run_audit(use_sample_data=True)
    
    # Verify outputs
    assert os.path.exists('output/inventory.csv')
    assert os.path.exists('output/dashboard.html')
    assert len(result.subscriptions) > 0
```

### Sample Data
Create `data/samples/` with:
- Sample Gmail receipts (JSON)
- Sample Stripe data
- Sample bank CSV
- Expected output for validation

---

## 💰 COST ANALYSIS

### One-Time Costs
- Development: In-house (no cost)
- Testing: In-house (no cost)
- **Total:** £0

### Monthly Operational Costs
- Claude API: ~£2-5 (100-250 subscriptions analyzed)
- Gmail API: FREE (quota: 1B requests/day)
- Stripe API: FREE
- PayPal API: FREE
- **Total:** £2-5/month

### ROI Calculation
- Monthly Cost: £5
- Savings Identified: £200-500
- **ROI: 4000-10000%**
- **Payback: Immediate**

---

## 🔮 FUTURE ENHANCEMENTS (Post-MVP)

### Phase 2 Features
1. **Browser Extension:** Auto-detect subscriptions from login activity
2. **Mobile App:** Track app subscriptions (iOS/Android)
3. **Team Sharing:** Multi-user audit (for businesses)
4. **Alerts:** Email when new subscription detected
5. **Forecasting:** Predict upcoming costs based on usage trends

### Advanced Analysis
1. **Usage Analytics:** Deeper integration with SaaS APIs
2. **Competitive Analysis:** Compare pricing vs alternatives
3. **Negotiation Scripts:** Auto-generate cancellation/downgrade emails
4. **ROI Calculator:** Calculate actual value vs cost per tool

---

## 📝 NOTES

### Gmail API Quotas
- **Quota:** 1 billion requests/day
- **Our Usage:** ~1,000 requests/month
- **Safe:** Yes, far below quota

### Rate Limiting
```python
# Implement exponential backoff
@retry(wait=wait_exponential(multiplier=1, min=2, max=10))
def api_call_with_retry():
    return api.call()
```

### Data Retention
- Keep last 12 months of audits
- Auto-archive older audits
- Maintain trend data for reporting

---

## ✅ DEFINITION OF DONE

The project is complete when:
- [ ] All 5 data sources integrated (Gmail, Stripe, PayPal, Bank CSV, Manual)
- [ ] Deduplication achieves >85% accuracy
- [ ] Claude AI recommendations working
- [ ] CSV inventory generated with all required fields
- [ ] HTML dashboard renders correctly with charts
- [ ] Action plan generates prioritized savings
- [ ] Captures 95%+ of subscriptions
- [ ] Identifies £200-500/month savings
- [ ] Runs in <30 minutes
- [ ] Complete documentation (README, setup guide)
- [ ] Works on macOS without errors
- [ ] Monthly cron job setup documented

---

## 🎯 NEXT STEPS

Once this spec is approved:
1. Review and confirm requirements
2. Switch to Code mode for implementation
3. Start with Phase 1: Foundation
4. Iterative development with testing
5. Deploy and run first audit
6. Refine based on real data

**Ready to proceed?**