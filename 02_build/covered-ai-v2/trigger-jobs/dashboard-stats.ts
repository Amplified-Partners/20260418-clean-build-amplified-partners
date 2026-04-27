/**
 * Covered AI - Dashboard Stats Jobs
 *
 * Jobs for calculating and caching dashboard statistics.
 */

import { task, schedules } from "@trigger.dev/sdk/v3";

const API_URL = process.env.API_URL || "http://localhost:8000";

// =============================================================================
// GENERATE ATTENTION ITEMS (every 15 minutes)
// =============================================================================

export const generateAttentionItems = schedules.task({
  id: "generate-attention-items",
  cron: "*/15 * * * *", // Every 15 minutes
  run: async () => {
    console.log("🔔 Generating attention items for all clients");

    const clients = await fetchAllClients();
    const results = { processed: 0, itemsCreated: 0, errors: 0 };

    for (const clientId of clients) {
      try {
        const items = await generateClientAttentionItems(clientId);
        results.itemsCreated += items;
        results.processed++;
      } catch (error) {
        console.error(`❌ Error generating attention items for ${clientId}:`, error);
        results.errors++;
      }
    }

    console.log(`✅ Generated ${results.itemsCreated} attention items for ${results.processed} clients`);
    return results;
  },
});

// =============================================================================
// CALCULATE TODAY STATS (hourly)
// =============================================================================

export const calculateTodayStats = schedules.task({
  id: "calculate-today-stats",
  cron: "0 * * * *", // Every hour
  run: async () => {
    console.log("📊 Calculating today stats for all clients");

    const clients = await fetchAllClients();
    const results = { processed: 0, errors: 0 };

    for (const clientId of clients) {
      try {
        await calculateClientDashboardStats(clientId);
        results.processed++;
      } catch (error) {
        console.error(`❌ Error calculating stats for ${clientId}:`, error);
        results.errors++;
      }
    }

    console.log(`✅ Calculated stats for ${results.processed} clients`);
    return results;
  },
});

// =============================================================================
// ON-DEMAND CALCULATION
// =============================================================================

export const calculateClientStatsOnDemand = task({
  id: "calculate-client-stats-on-demand",
  retry: { maxAttempts: 3 },
  run: async (payload: { clientId: string }) => {
    const { clientId } = payload;
    console.log(`📊 On-demand stats calculation for client ${clientId}`);

    await generateClientAttentionItems(clientId);
    await calculateClientDashboardStats(clientId);

    console.log(`✅ Stats calculated for client ${clientId}`);
    return { success: true };
  },
});

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

async function fetchAllClients(): Promise<string[]> {
  try {
    const response = await fetch(`${API_URL}/api/v1/clients`);
    if (!response.ok) return [];
    const data = await response.json();
    return (data.clients || []).map((c: { id: string }) => c.id);
  } catch {
    return [];
  }
}

interface Lead {
  id: string;
  customer_name?: string;
  caller_phone: string;
  urgency: string;
  status: string;
  created_at: string;
  job_type?: string;
}

interface Invoice {
  id: string;
  customer_name: string;
  customer_email: string;
  customer_phone?: string;
  amount: number;
  due_date: string;
  status: string;
}

interface Job {
  id: string;
  title: string;
  customer_id: string;
  scheduled_date: string;
  status: string;
  final_amount?: number;
  review_received: boolean;
  completed_at?: string;
}

// Priority scores
const PRIORITY = {
  emergency: 100,
  callback_due: 70,
  invoice_overdue: 50,
  lead_stale: 30,
};

async function generateClientAttentionItems(clientId: string): Promise<number> {
  // First, clear old resolved items (older than 24 hours)
  await clearOldAttentionItems(clientId);

  const items: AttentionItemCreate[] = [];

  // 1. Emergency leads
  const leads = await fetchLeads(clientId);
  const emergencyLeads = leads.filter(
    (l) => l.urgency === "emergency" && l.status === "new"
  );

  for (const lead of emergencyLeads) {
    items.push({
      clientId,
      itemType: "lead",
      itemId: lead.id,
      priority: PRIORITY.emergency,
      category: "emergency",
      title: `Emergency: ${lead.job_type || "Unknown job"}`,
      subtitle: lead.customer_name || lead.caller_phone,
      actionType: "call",
      actionLabel: "Call Now",
      actionData: { phone: lead.caller_phone },
    });
  }

  // 2. Urgent leads older than 1 hour (callback due)
  const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000);
  const callbackDueLeads = leads.filter(
    (l) =>
      l.urgency === "urgent" &&
      l.status === "new" &&
      new Date(l.created_at) < oneHourAgo
  );

  for (const lead of callbackDueLeads) {
    items.push({
      clientId,
      itemType: "lead",
      itemId: lead.id,
      priority: PRIORITY.callback_due,
      category: "callback_due",
      title: `Callback due: ${lead.job_type || "Unknown job"}`,
      subtitle: lead.customer_name || lead.caller_phone,
      actionType: "call",
      actionLabel: "Call Back",
      actionData: { phone: lead.caller_phone },
    });
  }

  // 3. Overdue invoices
  const invoices = await fetchInvoices(clientId);
  const overdueInvoices = invoices.filter(
    (i) =>
      (i.status === "SENT" || i.status === "REMINDED") &&
      new Date(i.due_date) < new Date()
  );

  for (const invoice of overdueInvoices) {
    items.push({
      clientId,
      itemType: "invoice",
      itemId: invoice.id,
      priority: PRIORITY.invoice_overdue,
      category: "invoice_overdue",
      title: `Overdue: £${invoice.amount.toFixed(0)}`,
      subtitle: invoice.customer_name,
      actionType: "chase",
      actionLabel: "Chase",
      actionData: {
        invoiceId: invoice.id,
        email: invoice.customer_email,
        phone: invoice.customer_phone,
      },
    });
  }

  // 4. Stale leads (older than 48 hours, still new)
  const twoDaysAgo = new Date(Date.now() - 48 * 60 * 60 * 1000);
  const staleLeads = leads.filter(
    (l) =>
      l.status === "new" &&
      l.urgency === "routine" &&
      new Date(l.created_at) < twoDaysAgo
  );

  for (const lead of staleLeads) {
    items.push({
      clientId,
      itemType: "lead",
      itemId: lead.id,
      priority: PRIORITY.lead_stale,
      category: "lead_stale",
      title: `Stale lead: ${lead.job_type || "Unknown job"}`,
      subtitle: lead.customer_name || lead.caller_phone,
      actionType: "view",
      actionLabel: "Review",
      actionData: { leadId: lead.id },
    });
  }

  // Upsert items (avoid duplicates)
  let created = 0;
  for (const item of items) {
    const success = await upsertAttentionItem(item);
    if (success) created++;
  }

  return created;
}

interface AttentionItemCreate {
  clientId: string;
  itemType: string;
  itemId: string;
  priority: number;
  category: string;
  title: string;
  subtitle?: string;
  actionType: string;
  actionLabel: string;
  actionData?: Record<string, any>;
}

async function upsertAttentionItem(item: AttentionItemCreate): Promise<boolean> {
  try {
    const response = await fetch(
      `${API_URL}/api/v1/dashboard/${item.clientId}/attention`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          item_type: item.itemType,
          item_id: item.itemId,
          priority: item.priority,
          category: item.category,
          title: item.title,
          subtitle: item.subtitle,
          action_type: item.actionType,
          action_label: item.actionLabel,
          action_data: item.actionData,
        }),
      }
    );
    return response.ok;
  } catch {
    return false;
  }
}

async function clearOldAttentionItems(clientId: string): Promise<void> {
  try {
    await fetch(`${API_URL}/api/v1/dashboard/${clientId}/attention/clear-old`, {
      method: "POST",
    });
  } catch {
    // Ignore errors
  }
}

async function calculateClientDashboardStats(clientId: string): Promise<void> {
  // Fetch data for calculations
  const [leads, jobs] = await Promise.all([
    fetchLeads(clientId),
    fetchJobs(clientId),
  ]);

  const now = new Date();
  const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const yesterdayStart = new Date(todayStart.getTime() - 24 * 60 * 60 * 1000);
  const weekStart = new Date(todayStart.getTime() - 7 * 24 * 60 * 60 * 1000);
  const lastWeekStart = new Date(weekStart.getTime() - 7 * 24 * 60 * 60 * 1000);

  // Calls today (leads created today)
  const callsToday = leads.filter(
    (l) => new Date(l.created_at) >= todayStart
  ).length;

  const callsYesterday = leads.filter(
    (l) =>
      new Date(l.created_at) >= yesterdayStart &&
      new Date(l.created_at) < todayStart
  ).length;

  const callsTodayTrend =
    callsYesterday > 0
      ? Math.round(((callsToday - callsYesterday) / callsYesterday) * 100)
      : 0;

  // Revenue this week (completed jobs)
  const completedThisWeek = jobs.filter(
    (j) => j.status === "completed" && j.completed_at && new Date(j.completed_at) >= weekStart
  );
  const revenueThisWeek = completedThisWeek.reduce(
    (sum, j) => sum + (j.final_amount || 0),
    0
  );

  const completedLastWeek = jobs.filter(
    (j) =>
      j.status === "completed" &&
      j.completed_at &&
      new Date(j.completed_at) >= lastWeekStart &&
      new Date(j.completed_at) < weekStart
  );
  const revenueLastWeek = completedLastWeek.reduce(
    (sum, j) => sum + (j.final_amount || 0),
    0
  );

  const revenueThisWeekTrend =
    revenueLastWeek > 0
      ? Math.round(((revenueThisWeek - revenueLastWeek) / revenueLastWeek) * 100)
      : 0;

  // Reviews this week
  const reviewsThisWeek = completedThisWeek.filter((j) => j.review_received).length;
  const reviewsLastWeek = completedLastWeek.filter((j) => j.review_received).length;

  const reviewsThisWeekTrend =
    reviewsLastWeek > 0
      ? Math.round(((reviewsThisWeek - reviewsLastWeek) / reviewsLastWeek) * 100)
      : 0;

  // All-time stats
  const totalCallsAnswered = leads.length;
  const totalLeadsCaptured = leads.filter(
    (l) => l.customer_name || l.caller_phone
  ).length;
  const totalJobsBooked = jobs.filter((j) => j.status !== "cancelled").length;
  const totalRevenue = jobs
    .filter((j) => j.status === "completed")
    .reduce((sum, j) => sum + (j.final_amount || 0), 0);

  // Time saved calculation (filtered calls * 5 min)
  const filteredCalls = totalCallsAnswered - totalLeadsCaptured;
  const totalTimeSavedHrs = Math.round((filteredCalls * 5) / 60);

  // Save stats
  await saveDashboardStats(clientId, {
    callsToday,
    callsTodayTrend,
    revenueThisWeek,
    revenueThisWeekTrend,
    reviewsThisWeek,
    reviewsThisWeekTrend,
    totalCallsAnswered,
    totalLeadsCaptured,
    totalJobsBooked,
    totalRevenue,
    totalTimeSavedHrs,
  });
}

async function fetchLeads(clientId: string): Promise<Lead[]> {
  try {
    const response = await fetch(
      `${API_URL}/api/v1/clients/${clientId}/leads?limit=1000`
    );
    if (!response.ok) return [];
    const data = await response.json();
    return data.leads || [];
  } catch {
    return [];
  }
}

async function fetchInvoices(clientId: string): Promise<Invoice[]> {
  try {
    const response = await fetch(
      `${API_URL}/api/v1/invoices?client_id=${clientId}`
    );
    if (!response.ok) return [];
    const data = await response.json();
    return data.invoices || [];
  } catch {
    return [];
  }
}

async function fetchJobs(clientId: string): Promise<Job[]> {
  try {
    const response = await fetch(
      `${API_URL}/api/v1/clients/${clientId}/jobs?limit=1000`
    );
    if (!response.ok) return [];
    const data = await response.json();
    return data.jobs || [];
  } catch {
    return [];
  }
}

interface DashboardStatsData {
  callsToday: number;
  callsTodayTrend: number;
  revenueThisWeek: number;
  revenueThisWeekTrend: number;
  reviewsThisWeek: number;
  reviewsThisWeekTrend: number;
  totalCallsAnswered: number;
  totalLeadsCaptured: number;
  totalJobsBooked: number;
  totalRevenue: number;
  totalTimeSavedHrs: number;
}

async function saveDashboardStats(
  clientId: string,
  stats: DashboardStatsData
): Promise<void> {
  try {
    await fetch(`${API_URL}/api/v1/dashboard/${clientId}/stats`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        calls_today: stats.callsToday,
        calls_today_trend: stats.callsTodayTrend,
        revenue_this_week: stats.revenueThisWeek,
        revenue_this_week_trend: stats.revenueThisWeekTrend,
        reviews_this_week: stats.reviewsThisWeek,
        reviews_this_week_trend: stats.reviewsThisWeekTrend,
        total_calls_answered: stats.totalCallsAnswered,
        total_leads_captured: stats.totalLeadsCaptured,
        total_jobs_booked: stats.totalJobsBooked,
        total_revenue: stats.totalRevenue,
        total_time_saved_hrs: stats.totalTimeSavedHrs,
      }),
    });
  } catch {
    // Ignore errors
  }
}
