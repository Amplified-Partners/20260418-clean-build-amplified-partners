---
title: "Customer Success & Onboarding System"
id: "customer-success-system"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Customer Success & Onboarding System
## Based on Agency Operations Best Practices

---

## Target Metrics (From Briefing)

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Delivery Margin | >50% | <40% |
| Net Profit Margin | 20-30% | <15% |
| Client Retention Rate | >90% | <85% |
| Onboarding Completion | >95% | <90% |
| Time to First Value | <24 hours | >48 hours |

---

## Onboarding Flow (White-Glove)

### Day 0: Sign-Up

**Trigger:** Customer completes payment

**Automated Actions:**
1. Welcome email sent (instant)
2. Slack notification to success team
3. Customer record created in CRM
4. Onboarding checklist initialized

**Success Team Actions:**
1. Personal welcome call within 2 hours
2. Gather: Current phone setup, call volume, pain points
3. Schedule number porting (if needed)
4. Set expectations: "Live within 24-48 hours"

---

### Day 1: Setup

**Customer Portal Actions:**
1. Business profile completion
   - Business name
   - Services offered
   - Operating hours
   - Emergency definitions
2. Greeting customization
   - First message preview
   - Review system prompt
3. Notification preferences
   - Primary phone for SMS
   - Email address
   - WhatsApp opt-in

**Backend Actions:**
1. Provision Vapi assistant with custom prompt
2. Configure Twilio phone number
3. Set up webhook endpoints
4. Test call (internal)

---

### Day 2: Go Live

**Checklist:**
- [ ] Test call completed successfully
- [ ] SMS notification received
- [ ] Email notification received
- [ ] Customer confirms greeting sounds right
- [ ] Number porting scheduled (if applicable)

**Go-Live Call:**
1. Walk through first test call together
2. Show how to access call logs
3. Explain SMS/email notification flow
4. Set up callback workflow
5. Answer any questions

**Success Milestone:** First real call handled

---

### Day 3-7: Early Success

**Daily Check-ins:**
- Day 3: "How's it going? Any calls yet?"
- Day 5: "Checking in - any feedback on Gemma?"
- Day 7: "First week done! Quick call to review?"

**Week 1 Review Call:**
1. Review call volume and outcomes
2. Gather feedback on Gemma's responses
3. Fine-tune any prompt issues
4. Celebrate wins (booked jobs, positive feedback)
5. Identify any friction points

---

### Day 8-30: Optimization

**Bi-weekly Check-ins:**
- Review metrics: calls, leads, conversions
- Adjust urgency thresholds if needed
- Add custom responses for common queries
- Introduce advanced features (if Pro plan)

**Day 30 Review:**
1. Full metrics review
2. ROI calculation with customer
3. Testimonial request (if positive)
4. Referral program introduction
5. Upsell conversation (if appropriate)

---

## Health Scoring System

### Score Calculation (0-100)

```typescript
interface HealthScore {
  usage: number;      // 0-30 points
  engagement: number; // 0-25 points
  sentiment: number;  // 0-25 points
  payment: number;    // 0-20 points
}

function calculateHealth(customer: Customer): number {
  const usage = calculateUsageScore(customer);       // Call volume vs expected
  const engagement = calculateEngagement(customer);   // Portal logins, support tickets
  const sentiment = calculateSentiment(customer);     // NPS, feedback, tone
  const payment = calculatePaymentScore(customer);    // On-time, failed, disputes
  
  return usage + engagement + sentiment + payment;
}
```

### Usage Score (0-30)

| Calls/Week | Score |
|------------|-------|
| 0 | 0 |
| 1-2 | 10 |
| 3-5 | 20 |
| 6+ | 30 |

**Alert:** Score = 0 for 2+ weeks → Churn risk

### Engagement Score (0-25)

| Activity | Points |
|----------|--------|
| Portal login (weekly) | 5 |
| Settings update | 5 |
| Support ticket opened | 5 |
| Feedback submitted | 10 |

**Alert:** No activity for 30 days → Churn risk

### Sentiment Score (0-25)

| Signal | Points |
|--------|--------|
| Positive support interaction | +10 |
| Complaint | -10 |
| Referral given | +15 |
| Negative review | -25 |
| NPS 9-10 | +25 |
| NPS 7-8 | +10 |
| NPS 0-6 | -15 |

### Payment Score (0-20)

| Status | Points |
|--------|--------|
| Always on-time | 20 |
| 1 late payment | 10 |
| 2+ late payments | 0 |
| Failed payment | -10 |
| Disputed charge | -20 |

---

## Intervention Triggers

### 🔴 Critical (Score < 30)

**Automated:**
1. Alert to success team (Slack + email)
2. Pause any marketing emails
3. Flag account in dashboard

**Human Action (within 24 hours):**
1. Personal call from success manager
2. Identify root cause
3. Offer: discount, feature unlock, or graceful exit
4. Document outcome

### 🟡 Warning (Score 30-60)

**Automated:**
1. Alert to success team
2. Trigger re-engagement email sequence

**Human Action (within 48 hours):**
1. Check-in call or email
2. Review recent calls/issues
3. Offer optimization session

### 🟢 Healthy (Score 60-80)

**Automated:**
1. Monthly check-in email
2. Feature tips drip

**Human Action:**
1. Quarterly business review
2. Referral request

### 🌟 Champion (Score 80+)

**Automated:**
1. Thank you note
2. Early access to new features
3. Referral program upgrade

**Human Action:**
1. Case study request
2. Testimonial video request
3. Speaking opportunity (if appropriate)

---

## Churn Prevention Playbook

### Signal: No Calls for 2 Weeks

**Day 1:** Email - "Everything okay?"
**Day 3:** SMS - "Quick check-in from Covered AI"
**Day 5:** Call from success manager
**Day 7:** Personal video message (Loom/HeyGen)
**Day 10:** Final "Is this still working for you?" email

### Signal: Failed Payment

**Hour 0:** Automatic retry
**Day 1:** Email - "Payment issue - quick fix"
**Day 3:** SMS - "Your Covered AI is paused"
**Day 5:** Call from success manager
**Day 7:** Service pause warning
**Day 14:** Service paused (not cancelled)

### Signal: Support Complaint

**Immediate:** Acknowledge within 2 hours
**Same day:** Escalate to success manager
**Next day:** Resolution call scheduled
**Post-resolution:** Follow-up to confirm satisfaction
**Day 7:** Check-in - "Everything still good?"

---

## Upsell Criteria

Only offer upsells when:

1. **Health score > 70** (customer is happy)
2. **At least 30 days as customer** (trust established)
3. **Relevant trigger event:**
   - High call volume → suggest Pro plan
   - Multiple locations mentioned → suggest Enterprise
   - Advanced questions → suggest features they don't have

**Never upsell:**
- During support interaction
- When health score is declining
- When payment issues exist
- Within 14 days of any complaint

---

## Success Metrics Dashboard

### Customer View

```
┌─────────────────────────────────────────┐
│  Your Covered AI Performance            │
├─────────────────────────────────────────┤
│  This Month                             │
│  ├── Calls Answered: 47                 │
│  ├── Leads Captured: 38                 │
│  ├── After-Hours: 12 (25%)              │
│  └── Emergency Routes: 2                │
│                                         │
│  Estimated Value                        │
│  ├── Leads @ £200 avg: £7,600           │
│  ├── Your Cost: £297                    │
│  └── ROI: 2,458%                        │
└─────────────────────────────────────────┘
```

### Internal View

```
┌─────────────────────────────────────────┐
│  Customer Health Overview               │
├─────────────────────────────────────────┤
│  🌟 Champions (80+): 12 (25%)           │
│  🟢 Healthy (60-80): 28 (58%)           │
│  🟡 Warning (30-60): 6 (13%)            │
│  🔴 Critical (<30): 2 (4%)              │
│                                         │
│  Actions Needed                         │
│  ├── Critical calls due: 2              │
│  ├── Warning check-ins: 3               │
│  ├── Upsell opportunities: 5            │
│  └── Testimonial requests: 4            │
└─────────────────────────────────────────┘
```

---

## Automation Jobs

### Daily
- Calculate health scores for all customers
- Send alerts for score changes
- Trigger intervention sequences

### Weekly
- Generate usage reports
- Identify upsell candidates
- Send engagement emails to healthy customers

### Monthly
- Generate ROI reports for customers
- Schedule QBR calls for champions
- Review churn patterns

---

## Quality Assurance

### Call Review Process (Sample 5%)

1. Random selection of calls weekly
2. Review against quality checklist:
   - [ ] Greeting correct
   - [ ] All required info captured
   - [ ] Emergency handled properly (if applicable)
   - [ ] Professional tone maintained
   - [ ] Call ended appropriately

3. Document issues and patterns
4. Update prompt if systemic issues found

### Customer Feedback Loop

1. NPS survey at Day 30, then quarterly
2. Post-support interaction rating
3. Annual satisfaction survey
4. Exit interview for churned customers

---

## SOPs

### SOP-001: New Customer Setup
1. Receive signup notification
2. Create CRM record
3. Send welcome email
4. Schedule onboarding call
5. Provision Vapi assistant
6. Configure phone number
7. Run test call
8. Complete go-live checklist
9. Schedule day 3 check-in

### SOP-002: Churn Risk Intervention
1. Receive health alert
2. Review customer history
3. Identify likely cause
4. Prepare talking points
5. Make personal call
6. Document outcome
7. Schedule follow-up
8. Update health score

### SOP-003: Escalation Handling
1. Receive escalation notification
2. Review full context
3. Respond within 2 hours
4. Escalate to Ewan if unresolved in 24h
5. Document resolution
6. Follow up within 7 days
