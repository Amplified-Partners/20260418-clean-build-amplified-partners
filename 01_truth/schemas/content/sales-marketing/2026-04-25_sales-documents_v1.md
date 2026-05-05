---
title: "Sales Documents"
id: "sales-documents"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "sales-marketing"
audience: "internal"
layer: "truth"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

/**
 * covered.AI Sales Documents
 * Discovery call framework, proposal templates, objection handling
 * 
 * Usage:
 * - Use discovery script for audit calls
 * - Select proposal based on client needs
 * - Reference objection handlers during calls
 */

// =====================================================
// DISCOVERY CALL FRAMEWORK
// =====================================================

const discoveryCall = {
  // PRE-CALL PREPARATION (5 minutes)
  preCall: {
    tasks: [
      "Review prospect LinkedIn profile",
      "Check form responses (if available)",
      "Prepare 2-3 specific questions",
      "Gather relevant case study",
      "Have audit template ready",
      "Set timer for call duration",
      "Close email/Slack notifications"
    ]
  },

  // CALL STRUCTURE
  structure: {
    // INTRO (2 minutes)
    intro: {
      duration: "2 minutes",
      script: `Hi [Name], I'm Ewan from covered.AI. Thanks for taking the time to chat today.

Just to set expectations: This is a free 30-minute call where I'll walk through your current processes, identify any leaks, and show you where you might be losing money or time.

I won't hard-sell you anything. If there's a fit, we'll talk about next steps. If not, you'll at least leave with some actionable insights.

Sound good?`
    },

    // BUILD RAPPORT (2 minutes)
    rapport: {
      duration: "2 minutes",
      script: `Before we dive in, tell me a bit about yourself.

How long have you been running [Company]?
What's the biggest change you've seen in the business since you started?
What made you decide to look into this now?`
    },

    // PAIN DISCOVERY (8-10 minutes)
    painDiscovery: {
      duration: "8-10 minutes",
      questions: [
        {
          question: "What's the biggest challenge you're facing right now?",
          probes: [
            "When did that start?",
            "How does that affect you day-to-day?",
            "What's that costing you?"
          ]
        },
        {
          question: "Roughly how many hours a week are you spending on admin and non-billable work?",
          probes: [
            "How does that make you feel?",
            "What would you do with 20 extra hours?"
          ]
        },
        {
          question: "Where does most of your time go?",
          categories: [
            "Invoicing and payment collection",
            "Lead follow-up and marketing",
            "Staff management and training",
            "Client work",
            "General admin"
          ]
        },
        {
          question: "How much do you have stuck in late payments right now?",
          probes: [
            "What's the oldest outstanding invoice?",
            "How do you typically follow up?"
          ]
        },
        {
          question: "If I could snap my fingers and fix ONE thing about your business, what would it be?"
        }
      ]
    },

    // SITUATION AUDIT (6-8 minutes)
    situationAudit: {
      duration: "6-8 minutes",
      script: `Let's walk through how things work currently. I'll ask some questions and take notes for the audit.

For invoicing:
- What system do you use?
- How often do invoices go out?
- What's your follow-up process?
- What's your current payment collection rate?

For leads:
- Where do your leads come from?
- How do you follow up initially?
- What's your current follow-up sequence?
- What's your lead conversion rate?

For processes:
- What repetitive tasks do you do daily/weekly?
- Are there documented processes for your team?
- What problems keep coming back?

[Take notes, identify 2-3 specific leaks, calculate rough money loss]

Based on what you've told me, I'm already seeing some opportunities. Let me put together a proper audit after the call.`
    },

    // PRESENT SOLUTION (4-6 minutes)
    presentSolution: {
      duration: "4-6 minutes",
      script: `Here's how we work. It's different from most consultants:

Step 1: Audit (Week 1)
We look at what you're already doing. No changes. We identify the leaks.

Step 2: Build (Weeks 2-4)
We automate the busywork—invoice reminders, lead follow-up, payment collection. Everything builds around your existing tools.

Step 3: Background (Weeks 5+)
The system runs automatically. Your team keeps working normally. You start seeing results.

Key difference: We don't retrain your team. We don't install new software. We don't disrupt your business.

[Reference relevant case study]

[Name from similar business] had [specific problem]. We fixed it in [timeframe]. Result: [specific outcome].

Does this approach sound like it could work for you?`
    },

    // HANDLE OBJECTIONS (2-3 minutes)
    objectionHandling: {
      duration: "2-3 minutes",
      commonObjections: [
        {
          objection: "Sounds too good to be true",
          response: "I get that. Most consultants over-promise. Here's what I do differently: I show you the audit first. You see the leaks yourself. Then we talk about fixing them. If there's no clear ROI, I tell you that. I don't want clients who aren't a fit."
        },
        {
          objection: "Worried about disruption",
          response: "That's our #1 priority. We specifically designed this to be zero-disruption. We work with your existing tools, your existing team, your existing processes. We just optimize them."
        },
        {
          objection: "Need to think about it",
          response: "Absolutely. This is an important decision. What specifically would you like to think about? [Listen] I can send over some case studies or answer any questions. When would be a good time to follow up?"
        },
        {
          objection: "No budget",
          response: "I understand. Let me ask: How much is [problem] costing you right now? If it's £8K/month in late payments, that's £96K/year. Our fee is a fraction of that. Let me show you the numbers."
        }
      ]
    },

    // NEXT STEPS (2 minutes)
    nextSteps: {
      duration: "2 minutes",
      script: `Great conversation, [Name].

Based on what you've shared, I can see [2-3 specific opportunities]. I want to put together a proper audit and proposal for you.

I'll send this over within 48 hours. It will include:
- Specific leaks I identified today
- Estimated impact if we fix them
- Investment options and timeline

Does email [email] work best?

In the meantime, feel free to reach out if you have any questions. I'm happy to chat.

Any questions before we wrap up?`
    },

    // CLOSE
    close: {
      script: `Thanks for your time today, [Name]. I appreciate you sharing so openly about your business. I'll be in touch soon with the audit.

Best of luck with [specific thing they mentioned]. Looking forward to connecting again.`
    }
  },

  // POST-CALL (5 minutes)
  postCall: {
    tasks: [
      "Send thank-you email immediately",
      "Add to CRM with notes",
      "Set follow-up reminder",
      "Create audit document within 48 hours",
      "Send proposal if audit shows opportunity"
    ]
  },

  // DISCOVERY QUESTIONS REFERENCE
  questions: [
    {
      category: "Business Overview",
      questions: [
        "Tell me about your business and how long you've been running it.",
        "How many staff do you have?",
        "What's your annual revenue range?",
        "Who are your ideal clients?"
      ]
    },
    {
      category: "Pain Points",
      questions: [
        "What's the biggest challenge you're facing right now?",
        "What's keeping you up at night?",
        "What have you already tried to fix this?",
        "What would success look like for you?"
      ]
    },
    {
      category: "Time",
      questions: [
        "How many hours a week are you working?",
        "What % of your time is billable vs. admin?",
        "If you got 20 hours back, what would you do with them?",
        "When did you last take a proper holiday?"
      ]
    },
    {
      category: "Money",
      questions: [
        "How much do you have stuck in late payments?",
        "What's your average payment collection rate?",
        "Where do you think you're losing money?",
        "What's your cost of acquiring a new lead?"
      ]
    },
    {
      category: "Readiness",
      questions: [
        "What's made you look into this now?",
        "What would you need to see to move forward?",
        "What's your timeline for making a decision?",
        "What's the biggest concern about working with someone like us?"
      ]
    }
  ]
};

// =====================================================
// SALES PROPOSAL TEMPLATE
// =====================================================

const proposalTemplate = {
  // DOCUMENT STRUCTURE
  structure: `
================================================================================
                        covered.AI
                   PROCESS OPTIMIZATION PROPOSAL
================================================================================

Prepared for: [Client Name]
Date: [Date]
Valid Until: [Date + 7 days]

Prepared by: Ewan Bramley, Founder, covered.AI
Contact: ewan@covered.ai | [Phone]

--------------------------------------------------------------------------------
EXECUTIVE SUMMARY
--------------------------------------------------------------------------------

Thank you for the opportunity to present this proposal. Based on our discovery 
call, I've identified [X] key areas where your business is losing time and money.

This proposal outlines a low-friction optimization approach designed to:
• Recover [X] hours per week
• Increase monthly revenue by £[X]
• Reduce late payments by [X]%
• Implement without disrupting your operations

All work is completed in [X] weeks using your existing tools and systems.

--------------------------------------------------------------------------------
CURRENT SITUATION
--------------------------------------------------------------------------------

Based on our conversation, I've identified the following areas for improvement:

[AREA 1 - e.g., Late Payments]
Current State: [Description of current process and problems]
Financial Impact: £[X]/month in uncollected revenue
Root Cause: [Why this is happening]

[AREA 2 - e.g., Lead Follow-up]
Current State: [Description]
Financial Impact: [X] leads lost/month
Root Cause: [Why this is happening]

[AREA 3 - e.g., Administrative Tasks]
Current State: [Description]
Time Impact: [X] hours/week
Root Cause: [Why this is happening]

IF NOTHING CHANGES:
• [Specific consequence of inaction]
• [Another consequence]
• [Financial impact over 12 months]

--------------------------------------------------------------------------------
PROPOSED SOLUTION
--------------------------------------------------------------------------------

covered.AI implements a 4-step optimization process:

STEP 1: AUDIT (Week 1)
• Deep-dive review of current processes
• Identify all time and money leaks
• Document current workflows
• Deliver: Comprehensive audit report

STEP 2: BUILD (Weeks 2-[X])
• Automate invoice reminders and payment collection
• Set up lead follow-up sequences
• Document key processes
• Build: Custom automation system

STEP 3: TEST (Week [X])
• Pilot with real data
• Refine based on feedback
• Train key team members (if needed)
• Deliver: Tested, working system

STEP 4: DEPLOY (Week [X+])
• Full rollout
• Monitor results
• Ongoing support
• Deliver: Fully operational system

DISRUPTION LEVEL: ZERO
• Your team keeps working normally
• No new software to learn
• No retraining required
• We work around your schedule

--------------------------------------------------------------------------------
INVESTMENT OPTIONS
--------------------------------------------------------------------------------

OPTION 1: BASIC - £2,997
Best for: Single-process optimization
Timeline: 4 weeks
Includes:
• Audit of 1 process area
• Automation of 1 workflow
• Basic setup and testing
• 30 days support

Expected Results:
• 5-10 hours/week saved
• £8K+ more collected monthly
• ROI within 60 days

OPTION 2: STANDARD - £3,997 [RECOMMENDED]
Best for: Comprehensive optimization
Timeline: 6 weeks
Includes:
• Audit of 2-3 process areas
• Automation of 2-3 workflows
• Full implementation
• 60 days support

Expected Results:
• 10-20 hours/week saved
• £12K+ more collected monthly
• ROI within 45 days

OPTION 3: PREMIUM - £4,997
Best for: Complete transformation
Timeline: 8 weeks
Includes:
• Audit of all process areas
• Automation of 3-5 workflows
• Full implementation
• 90 days support
• Monthly check-ins for 3 months

Expected Results:
• 20+ hours/week saved
• £15K+ more collected monthly
• Ongoing optimization

--------------------------------------------------------------------------------
PAYMENT TERMS
--------------------------------------------------------------------------------

• 50% upon acceptance of proposal
• 50% upon completion

Payment due within 7 days of invoice. Work begins upon receipt of first payment.

--------------------------------------------------------------------------------
RETURN ON INVESTMENT
--------------------------------------------------------------------------------

Based on your specific situation:

Current Loss: £[X]/month = £[X]/year
Investment: £[X]
ROI: [X]x in first year
Payback Period: [X] weeks

This is a conservative estimate. Actual results may be higher.

--------------------------------------------------------------------------------
WHY COVERED.AI
--------------------------------------------------------------------------------

1. 30 YEARS OPERATIONAL EXPERIENCE
I built and ran a successful business for 30 years. I understand your challenges 
because I lived them.

2. LOW-FRICTION APPROACH
We don't disrupt your business. We optimize around it.

3. PROVEN PROCESS
150+ UK SMBs have implemented our system. Results are consistent.

4. SPECIFIC OUTCOMES
We don't promise "improvements." We promise specific, measurable results.

5. HONEST PARTNERSHIP
If you're not a fit, I'll tell you. No hard sell.

--------------------------------------------------------------------------------
CASE STUDY: [Similar Client]
--------------------------------------------------------------------------------

Before:
• [X] hours/week on admin
• £[X] in late payments
• [Specific problems]

After:
• [Y] hours/week saved
• £[Z] more collected monthly
• [Specific outcome]

"[Quote from client]"

--------------------------------------------------------------------------------
NEXT STEPS
--------------------------------------------------------------------------------

1. Review this proposal
2. Let me know if you have any questions
3. Reply with "PROCEED" to accept and receive invoice
4. Schedule kickoff call

I have capacity for [X] new clients this month. I'll hold this proposal for 
7 days.

If you decide this isn't the right fit, no hard feelings. I appreciate the 
conversation and wish you the best with [Company].

--------------------------------------------------------------------------------

Questions? Reply to this email or call [Phone].

Best regards,

Ewan Bramley
Founder, covered.AI
`

  // ROI CALCULATOR
  roiCalculator: {
    inputs: {
      latePayments: "Current outstanding (£)",
      hoursOnAdmin: "Hours/week on admin",
      hourlyRate: "Your time value (£/hour)",
      leadConversionRate: "Current lead conversion (%)",
      leadsPerMonth: "New leads/month"
    },
    calculations: {
      latePaymentRecovery: "latePayments × 0.7 × 12", // 70% recoverable, annual
      timeSavings: "hoursOnAdmin × hourlyRate × 52", // Annual value
      leadRevenue: "leadsPerMonth × (targetConversion - currentConversion) × avgDealValue × 12"
    }
  }
};

// =====================================================
// OBJECTION HANDLING & CLOSING SCRIPTS
// =====================================================

const objectionHandling = {
  // COMMON OBJECTIONS
  objections: [
    {
      id: 1,
      objection: "Sounds too good to be true",
      category: "Skepticism",
      response: `I get it. There are a lot of people over-promising in this space.

Here's how I'm different: I show you the audit BEFORE you commit. You'll see the exact leaks in YOUR business with YOUR numbers. If I can't find £8K+ in recoverable revenue, I'll tell you that honestly.

I'm not selling a dream. I'm offering a specific fix to specific problems. The audit shows you exactly what I'd do and what it would cost.

Fair enough?`,
      probe: "What would you need to see to feel comfortable moving forward?"
    },
    {
      id: 2,
      objection: "I don't have the budget",
      category: "Cost",
      response: `I understand. Budget is always a consideration.

Let me ask: How much is [problem] costing you right now? If you're losing £8K/month to late payments, that's £96K/year. Our fee is around £4K for comprehensive optimization.

That's about 4% of what you're currently losing. Most clients see ROI within 60 days.

I'm not saying budget isn't real. I'm saying the question isn't "can I afford this?" It's "can I afford to keep losing [X]?"

Does that perspective help?`,
      alternatives: [
        "We could start with just the audit and one automation for £2,997",
        "We could phase this—audit first, then implementation",
        "Payment terms: 50% upfront, 50% on completion"
      ]
    },
    {
      id: 3,
      objection: "I'm worried about disruption",
      category: "Risk",
      response: `That's our #1 priority. Let me explain our approach:

We specifically built this to be zero-disruption:

1. We use YOUR existing tools. No new software.
2. We work AROUND your team. No retraining.
3. We build automation that runs in the background.
4. Your team keeps doing what they're doing.

One client said: "My team didn't even notice anything changed. The invoices just started getting paid faster."

We measure success by how little you notice us. Can you think of any other consultant who says that?`,
      probe: "What specifically would disrupt your operations?"
    },
    {
      id: 4,
      objection: "I need to think about it / talk to my partner",
      category: "Timing",
      response: `Absolutely. This is an important decision. You should think about it.

[If partner] That's smart. My partner would want to know the details too.

What I suggest: Review the case study I sent. Think about the specific numbers we discussed. When you two talk, ask yourself: What would it mean to get 20 hours/week back?

I'll follow up [specific day] to answer any questions. Does that work?`,
      followUp: {
        day5: "Quick email: Any questions about the proposal?",
        day10: "Scarcity message: I have one spot left this month",
        day15: "Phone call: Check-in, no pressure"
      }
    },
    {
      id: 5,
      objection: "What if it doesn't work?",
      category: "Risk",
      response: `Fair question. Here's what I say:

1. We specifically work on problems we know how to solve. If your situation is different, I'll tell you before we start.

2. We show you the audit first. You see the opportunity before you pay.

3. Our results are consistent. 150+ clients. Same approach. Similar outcomes.

4. I'm not going anywhere. If something goes wrong, you can reach me directly.

I can't promise perfection. I can promise that I'll be honest about what we can achieve and work hard to deliver it.

Does that address your concern?`
    },
    {
      id: 6,
      objection: "I'm not sure now is the right time",
      category: "Timing",
      response: `I understand. Timing matters.

Can I ask what's making you hesitant about the timing? Is it:
• The business is too busy right now?
• You want to wait until after [event]?
• Something else?

[Listen and address]

Here's my perspective: The problems we're talking about—late payments, lost leads, admin overload—they don't usually fix themselves. Every month you wait is another month of [specific cost].

But I'm not here to pressure you. I want you to make the right decision for your business.

What would make now feel like the right time?`
    }
  ],

  // CLOSING TECHNIQUES
  closingTechniques: [
    {
      name: "Assumptive Close",
      useWhen: "Objections resolved, positive body language",
      script: `Great. I'll go ahead and get the invoice ready. First payment is 50%—can I invoice you today or tomorrow? And we'll schedule the kickoff call for [next week]?`
    },
    {
      name: "Alternative Close",
      useWhen: "Undecided between options",
      script: `Based on what you've told me, I'd recommend the Standard package. But I want you to feel confident. Would you prefer to start with Basic and add on later, or go with Standard and get everything done at once?`
    },
    {
      name: "Takeaway Close",
      useWhen: "Price is main objection",
      script: `I understand. Let me be honest—if budget is the main concern, we could start with just the audit and one automation for £2,997. It's a smaller commitment and you can see the results before doing more. Would that work better for you?`
    },
    {
      name: "Question Close",
      useWhen: "Ready but hesitant",
      script: `If we could guarantee [specific result], would you want to move forward this week? What would need to be true for you to say yes today?`
    },
    {
      name: "Summary Close",
      useWhen: "End of call, positive outcome",
      script: `So to recap: You have [problem], we can fix it in [timeframe], it will cost [amount], and you'll get [result]. Everything we're talking about is in the proposal I'm sending over. Ready to move forward?`
    }
  ],

  // FOLLOW-UP SEQUENCE
  followUpSequence: [
    {
      day: 0,
      type: "Thank you",
      template: `Thanks for your time today, [Name]. Great conversation. I'll have the audit and proposal to you within 48 hours.

In the meantime, here's the case study I mentioned: [link]

Any questions before I send the formal proposal, just reply.

Looking forward to connecting again.`
    },
    {
      day: 5,
      type: "Questions check-in",
      template: `Hi [Name], just checking in. Did you get a chance to look at the proposal? Any questions I can answer?

No pressure at all—just wanted to make sure you have everything you need to make a decision.

Best,`
    },
    {
      day: 10,
      type: "Scarcity",
      template: `Hi [Name], I wanted to let you know—I have capacity for one more client this month, and I'm holding that spot until [end of week].

If you're still interested, I'd love to work together. If not, completely understand. Best of luck with [Company].

Talk soon,`
    },
    {
      day: 15,
      type: "Phone call",
      template: "[Call to check in, no agenda, just relationship building]",
      notes: "Don't pitch. Just ask how they're doing and if there's anything I can help with."
    },
    {
      day: 21,
      type: "Final",
      template: `Hi [Name], I've enjoyed our conversations and I believe we could really help [Company]. But I also respect your decision-making process.

I'll leave this here. If you decide down the road that now is the right time, reply to this email and I'll get you started.

Best of luck with everything.`
    }
  ]
};

// =====================================================
// SALES METRICS & TRACKING
// =====================================================

const salesMetrics = {
  // FUNNEL METRICS
  funnel: {
    visitorsToEmail: "5%",
    emailToAudit: "5%",
    auditToShow: "90%",
    auditToProposal: "100%",
    proposalToAccept: "30%",
    acceptToOnboard: "95%"
  },

  // MONTHLY TARGETS
  targets: {
    visitors: 1000,
    emailSubscribers: 50,
    auditBookings: 5,
    auditsCompleted: 4,
    proposals: 4,
    clients: 1,
    revenue: "£3-5K"
  },

  // REVENUE PROJECTION
  projections: [
    { month: 1, clients: 0, revenue: "£0" },
    { month: 2, clients: 1, revenue: "£3-5K" },
    { month: 3, clients: 2, revenue: "£6-10K" },
    { month: 4, clients: 3, revenue: "£9-15K" },
    { month: 5, clients: 4, revenue: "£12-20K" },
    { month: 6, clients: 5, revenue: "£15-25K" },
    { month: 12, clients: 15, revenue: "£45-75K" }
  ],

  // WEEKLY ACTIVITY
  weekly: {
    linkedInPosts: 3,
    blogPosts: 2,
    emailsSent: 2,
    dmsSent: 50,
    discoveryCalls: 3
  }
};

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    discoveryCall,
    proposalTemplate,
    objectionHandling,
    salesMetrics
  };
}
