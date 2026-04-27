/**
 * Covered AI - Daily Health Score Calculator
 *
 * Calculates health scores for all customers daily.
 * Triggers interventions for at-risk accounts.
 *
 * Based on enterprise agency operations best practices:
 * - Usage: 0-30 points (call volume)
 * - Engagement: 0-25 points (portal activity)
 * - Sentiment: 0-25 points (feedback, NPS)
 * - Payment: 0-20 points (billing status)
 */

import { task } from "@trigger.dev/sdk/v3";

const API_URL = process.env.API_URL || "http://localhost:8000";

interface Customer {
  id: string;
  businessName: string;
  email: string;
  phone: string;
  plan: string;
  createdAt: string;
  lastLoginAt: string | null;
  npsScore: number | null;
}

interface HealthMetrics {
  usage: number;      // 0-30
  engagement: number; // 0-25
  sentiment: number;  // 0-25
  payment: number;    // 0-20
  total: number;      // 0-100
}

interface CallStats {
  total: number;
  lastWeek: number;
  lastMonth: number;
}

interface PaymentStatus {
  status: 'current' | 'late' | 'failed' | 'disputed';
  latePayments: number;
  failedPayments: number;
}

// ============================================================================
// HEALTH SCORE CALCULATION
// ============================================================================

function calculateUsageScore(callsPerWeek: number): number {
  // 0 calls = 0 points
  // 1-2 calls = 10 points
  // 3-5 calls = 20 points
  // 6+ calls = 30 points
  if (callsPerWeek === 0) return 0;
  if (callsPerWeek <= 2) return 10;
  if (callsPerWeek <= 5) return 20;
  return 30;
}

function calculateEngagementScore(
  lastLoginDaysAgo: number | null,
  settingsUpdated: boolean,
  supportTickets: number,
  feedbackGiven: boolean
): number {
  let score = 0;
  
  // Portal login (weekly) = 5 points
  if (lastLoginDaysAgo !== null && lastLoginDaysAgo <= 7) {
    score += 5;
  }
  
  // Settings update = 5 points
  if (settingsUpdated) {
    score += 5;
  }
  
  // Support ticket opened = 5 points (shows engagement, not necessarily bad)
  if (supportTickets > 0) {
    score += 5;
  }
  
  // Feedback submitted = 10 points
  if (feedbackGiven) {
    score += 10;
  }
  
  return Math.min(score, 25);
}

function calculateSentimentScore(
  npsScore: number | null,
  complaints: number,
  referrals: number,
  positiveInteractions: number
): number {
  let score = 12; // Start neutral
  
  // NPS impact
  if (npsScore !== null) {
    if (npsScore >= 9) score += 13;      // Promoter: +13
    else if (npsScore >= 7) score += 5;   // Passive: +5
    else score -= 10;                      // Detractor: -10
  }
  
  // Complaints: -10 each
  score -= complaints * 10;
  
  // Referrals: +15 each
  score += referrals * 15;
  
  // Positive support interactions: +5 each
  score += positiveInteractions * 5;
  
  return Math.max(0, Math.min(score, 25));
}

function calculatePaymentScore(status: PaymentStatus): number {
  if (status.status === 'disputed') return -20;
  if (status.failedPayments > 0) return -10;
  if (status.latePayments >= 2) return 0;
  if (status.latePayments === 1) return 10;
  return 20; // Always on-time
}

function determineRiskLevel(score: number): 'critical' | 'warning' | 'healthy' | 'champion' {
  if (score < 30) return 'critical';
  if (score < 60) return 'warning';
  if (score < 80) return 'healthy';
  return 'champion';
}

// ============================================================================
// INTERVENTION TRIGGERS
// ============================================================================

async function triggerIntervention(
  customerId: string,
  riskLevel: 'critical' | 'warning',
  score: number,
  metrics: HealthMetrics
): Promise<void> {
  console.log(`🚨 Triggering ${riskLevel} intervention for customer ${customerId}`);
  
  // Send Slack alert to success team
  const slackWebhook = process.env.SLACK_SUCCESS_WEBHOOK;
  if (slackWebhook) {
    await fetch(slackWebhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text: `${riskLevel === 'critical' ? '🔴' : '🟡'} Health Alert`,
        blocks: [
          {
            type: 'section',
            text: {
              type: 'mrkdwn',
              text: `*${riskLevel.toUpperCase()} Health Alert*\nCustomer: ${customerId}\nScore: ${score}/100`
            }
          },
          {
            type: 'section',
            fields: [
              { type: 'mrkdwn', text: `*Usage:* ${metrics.usage}/30` },
              { type: 'mrkdwn', text: `*Engagement:* ${metrics.engagement}/25` },
              { type: 'mrkdwn', text: `*Sentiment:* ${metrics.sentiment}/25` },
              { type: 'mrkdwn', text: `*Payment:* ${metrics.payment}/20` }
            ]
          },
          {
            type: 'actions',
            elements: [
              {
                type: 'button',
                text: { type: 'plain_text', text: 'View Customer' },
                url: `https://admin.covered.ai/customers/${customerId}`
              }
            ]
          }
        ]
      })
    });
  }
  
  // Create task in CRM/project management
  // TODO: Integrate with Monday.com, Asana, or internal task system
  
  // Log the intervention trigger
  await fetch(`${API_URL}/api/v1/health-scores/${customerId}/intervention`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      riskLevel,
      score,
      metrics,
      triggeredAt: new Date().toISOString()
    })
  });
}

// ============================================================================
// MAIN JOB
// ============================================================================

export const calculateHealthScores = task({
  id: "calculate-health-scores",
  retry: {
    maxAttempts: 3,
  },
  run: async () => {
    console.log("📊 Starting daily health score calculation");
    
    // Fetch all active customers
    const customersResponse = await fetch(`${API_URL}/api/v1/customers?status=active`);
    if (!customersResponse.ok) {
      throw new Error("Failed to fetch customers");
    }
    const customers: Customer[] = await customersResponse.json();
    
    console.log(`Found ${customers.length} active customers`);
    
    const results = {
      processed: 0,
      critical: 0,
      warning: 0,
      healthy: 0,
      champion: 0,
      errors: 0
    };
    
    for (const customer of customers) {
      try {
        // Fetch metrics for this customer
        const [callStats, paymentStatus, activityLog] = await Promise.all([
          fetchCallStats(customer.id),
          fetchPaymentStatus(customer.id),
          fetchActivityLog(customer.id)
        ]);
        
        // Calculate each component
        const usage = calculateUsageScore(callStats.lastWeek);
        
        const lastLoginDaysAgo = customer.lastLoginAt
          ? Math.floor((Date.now() - new Date(customer.lastLoginAt).getTime()) / (1000 * 60 * 60 * 24))
          : null;
        
        const engagement = calculateEngagementScore(
          lastLoginDaysAgo,
          activityLog.settingsUpdated,
          activityLog.supportTickets,
          activityLog.feedbackGiven
        );
        
        const sentiment = calculateSentimentScore(
          customer.npsScore,
          activityLog.complaints,
          activityLog.referrals,
          activityLog.positiveInteractions
        );
        
        const payment = calculatePaymentScore(paymentStatus);
        
        const total = usage + engagement + sentiment + payment;
        
        const metrics: HealthMetrics = {
          usage,
          engagement,
          sentiment,
          payment,
          total
        };
        
        // Save health score
        await fetch(`${API_URL}/api/v1/health-scores`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            customerId: customer.id,
            score: total,
            components: metrics,
            calculatedAt: new Date().toISOString()
          })
        });
        
        // Determine risk level and trigger interventions
        const riskLevel = determineRiskLevel(total);
        results[riskLevel]++;
        
        if (riskLevel === 'critical' || riskLevel === 'warning') {
          await triggerIntervention(customer.id, riskLevel, total, metrics);
        }
        
        results.processed++;
        
      } catch (error) {
        console.error(`Error processing customer ${customer.id}:`, error);
        results.errors++;
      }
    }
    
    console.log("📊 Health score calculation complete:", results);
    
    // Send daily summary to Slack
    const slackWebhook = process.env.SLACK_SUCCESS_WEBHOOK;
    if (slackWebhook) {
      await fetch(slackWebhook, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: `📊 Daily Health Score Summary`,
          blocks: [
            {
              type: 'section',
              text: {
                type: 'mrkdwn',
                text: `*Daily Health Score Summary*\n${new Date().toLocaleDateString('en-GB')}`
              }
            },
            {
              type: 'section',
              fields: [
                { type: 'mrkdwn', text: `*🌟 Champions:* ${results.champion}` },
                { type: 'mrkdwn', text: `*🟢 Healthy:* ${results.healthy}` },
                { type: 'mrkdwn', text: `*🟡 Warning:* ${results.warning}` },
                { type: 'mrkdwn', text: `*🔴 Critical:* ${results.critical}` }
              ]
            }
          ]
        })
      });
    }
    
    return results;
  }
});

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

async function fetchCallStats(customerId: string): Promise<CallStats> {
  try {
    const response = await fetch(`${API_URL}/api/v1/customers/${customerId}/call-stats`);
    if (!response.ok) {
      return { total: 0, lastWeek: 0, lastMonth: 0 };
    }
    return response.json();
  } catch {
    return { total: 0, lastWeek: 0, lastMonth: 0 };
  }
}

async function fetchPaymentStatus(customerId: string): Promise<PaymentStatus> {
  try {
    const response = await fetch(`${API_URL}/api/v1/customers/${customerId}/payment-status`);
    if (!response.ok) {
      return { status: 'current', latePayments: 0, failedPayments: 0 };
    }
    return response.json();
  } catch {
    return { status: 'current', latePayments: 0, failedPayments: 0 };
  }
}

async function fetchActivityLog(customerId: string): Promise<{
  settingsUpdated: boolean;
  supportTickets: number;
  feedbackGiven: boolean;
  complaints: number;
  referrals: number;
  positiveInteractions: number;
}> {
  try {
    const response = await fetch(`${API_URL}/api/v1/customers/${customerId}/activity-log`);
    if (!response.ok) {
      return {
        settingsUpdated: false,
        supportTickets: 0,
        feedbackGiven: false,
        complaints: 0,
        referrals: 0,
        positiveInteractions: 0
      };
    }
    return response.json();
  } catch {
    return {
      settingsUpdated: false,
      supportTickets: 0,
      feedbackGiven: false,
      complaints: 0,
      referrals: 0,
      positiveInteractions: 0
    };
  }
}

// ============================================================================
// SCHEDULED TRIGGER
// ============================================================================

// This job should be scheduled to run daily at 6am
// Configure in trigger.config.ts:
// schedules: [
//   { cron: "0 6 * * *", task: "calculate-health-scores" }
// ]
