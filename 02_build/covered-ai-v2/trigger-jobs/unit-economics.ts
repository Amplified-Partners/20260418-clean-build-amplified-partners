/**
 * Covered AI - Unit Economics Jobs (LTV:CAC)
 *
 * Jobs for tracking customer lifetime value and acquisition costs.
 */

import { task, schedules } from "@trigger.dev/sdk/v3";

interface Customer {
  id: string;
  clientId: string;
  name: string;
  phone: string;
  email?: string;
  totalJobs: number;
  totalRevenue: number;
  firstJobDate?: string;
  lastJobDate?: string;
  acquisitionSource?: string;
}

interface Job {
  id: string;
  clientId: string;
  customerId: string;
  finalAmount?: number;
  quotedAmount?: number;
  completedAt?: string;
}

interface UnitEconomics {
  totalCustomers: number;
  repeatCustomers: number;
  repeatRate: number;
  avgJobValue: number;
  avgJobsPerCustomer: number;
  customerLTV: number;
  totalMarketingSpend: number;
  newCustomersThisMonth: number;
  avgCAC: number;
  ltvCacRatio: number;
  ltvCacLastMonth: number;
  ltvCacTrend: string;
}

const API_URL = process.env.API_URL || "http://localhost:8000";

// =============================================================================
// UPDATE CUSTOMER LTV ON JOB COMPLETION
// =============================================================================

export const updateCustomerLTV = task({
  id: "update-customer-ltv",
  retry: {
    maxAttempts: 3,
  },
  run: async (payload: { jobId: string }) => {
    const { jobId } = payload;

    console.log(`📊 Updating customer LTV for job ${jobId}`);

    // 1. Fetch job details
    const job = await fetchJob(jobId);
    if (!job) {
      throw new Error(`Job ${jobId} not found`);
    }

    if (!job.customerId) {
      console.log(`Job ${jobId} has no customer, skipping LTV update`);
      return { success: false, reason: "no_customer" };
    }

    // 2. Get the job revenue (final or quoted)
    const revenue = job.finalAmount || job.quotedAmount || 0;

    // 3. Update customer stats
    const result = await updateCustomerStats(job.customerId, revenue, job.completedAt);

    console.log(`✅ Updated LTV for customer ${job.customerId}`);

    // 4. Trigger unit economics recalculation
    // Note: We'll let the scheduled job handle this to avoid too many calculations

    return {
      success: true,
      customerId: job.customerId,
      revenueAdded: revenue,
    };
  },
});

// =============================================================================
// CALCULATE UNIT ECONOMICS (SCHEDULED)
// =============================================================================

export const calculateUnitEconomics = schedules.task({
  id: "calculate-unit-economics",
  cron: "0 0 * * *", // Daily at midnight
  run: async () => {
    console.log(`📊 Calculating unit economics for all clients`);

    // Get all clients
    const clients = await fetchAllClients();

    const results = {
      clientsProcessed: 0,
      errors: 0,
    };

    for (const clientId of clients) {
      try {
        const metrics = await calculateClientUnitEconomics(clientId);
        await saveUnitEconomics(clientId, metrics);
        results.clientsProcessed++;
        console.log(`   Calculated metrics for client ${clientId}`);
      } catch (error) {
        console.error(`❌ Error calculating metrics for client ${clientId}:`, error);
        results.errors++;
      }
    }

    console.log(`✅ Unit economics calculated for ${results.clientsProcessed} clients`);
    return results;
  },
});

// =============================================================================
// ON-DEMAND CALCULATION
// =============================================================================

export const calculateClientMetricsOnDemand = task({
  id: "calculate-client-metrics-on-demand",
  retry: {
    maxAttempts: 3,
  },
  run: async (payload: { clientId: string }) => {
    const { clientId } = payload;

    console.log(`📊 On-demand metrics calculation for client ${clientId}`);

    const metrics = await calculateClientUnitEconomics(clientId);
    await saveUnitEconomics(clientId, metrics);

    console.log(`✅ Metrics calculated for client ${clientId}`);
    return { success: true, metrics };
  },
});

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

async function fetchJob(jobId: string): Promise<Job | null> {
  try {
    // We need to fetch from the client-scoped endpoint
    const response = await fetch(`${API_URL}/api/v1/jobs/${jobId}`);
    if (!response.ok) return null;
    return response.json();
  } catch {
    return null;
  }
}

async function updateCustomerStats(
  customerId: string,
  revenue: number,
  completedAt?: string
): Promise<void> {
  await fetch(`${API_URL}/api/v1/customers/${customerId}/add-job-revenue`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      revenue,
      completedAt: completedAt || new Date().toISOString(),
    }),
  });
}

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

async function calculateClientUnitEconomics(clientId: string): Promise<UnitEconomics> {
  // Fetch all data needed for calculations
  const [customers, jobs, marketingSpend, previousMetrics] = await Promise.all([
    fetchCustomers(clientId),
    fetchCompletedJobs(clientId),
    fetchMarketingSpend(clientId),
    fetchPreviousMetrics(clientId),
  ]);

  const now = new Date();
  const thisMonthStart = new Date(now.getFullYear(), now.getMonth(), 1);

  // Total customers
  const totalCustomers = customers.length;

  // Repeat customers (more than 1 job)
  const repeatCustomers = customers.filter((c) => c.totalJobs > 1).length;

  // Repeat rate
  const repeatRate = totalCustomers > 0 ? repeatCustomers / totalCustomers : 0;

  // Average job value
  const totalRevenue = jobs.reduce((sum, j) => sum + (j.finalAmount || j.quotedAmount || 0), 0);
  const avgJobValue = jobs.length > 0 ? totalRevenue / jobs.length : 0;

  // Average jobs per customer
  const totalJobsCount = customers.reduce((sum, c) => sum + c.totalJobs, 0);
  const avgJobsPerCustomer = totalCustomers > 0 ? totalJobsCount / totalCustomers : 1;

  // Customer LTV = Avg Job Value × Avg Jobs Per Customer
  const customerLTV = avgJobValue * avgJobsPerCustomer;

  // Total marketing spend (all time)
  const totalMarketingSpendAmount = marketingSpend.reduce(
    (sum, m) => sum + Number(m.amount),
    0
  );

  // New customers this month
  const newCustomersThisMonth = customers.filter((c) => {
    if (!c.firstJobDate) return false;
    return new Date(c.firstJobDate) >= thisMonthStart;
  }).length;

  // Average CAC
  // Simple: Total marketing spend / total customers
  // Better: Rolling 3-month average
  const avgCAC = totalCustomers > 0 ? totalMarketingSpendAmount / totalCustomers : 0;

  // LTV:CAC Ratio
  const ltvCacRatio = avgCAC > 0 ? customerLTV / avgCAC : 0;

  // Trend calculation
  const ltvCacLastMonth = previousMetrics?.ltvCacRatio || 0;
  let ltvCacTrend: string = "stable";
  if (ltvCacRatio > ltvCacLastMonth * 1.05) {
    ltvCacTrend = "up";
  } else if (ltvCacRatio < ltvCacLastMonth * 0.95) {
    ltvCacTrend = "down";
  }

  return {
    totalCustomers,
    repeatCustomers,
    repeatRate,
    avgJobValue,
    avgJobsPerCustomer,
    customerLTV,
    totalMarketingSpend: totalMarketingSpendAmount,
    newCustomersThisMonth,
    avgCAC,
    ltvCacRatio,
    ltvCacLastMonth,
    ltvCacTrend,
  };
}

async function fetchCustomers(clientId: string): Promise<Customer[]> {
  try {
    const response = await fetch(`${API_URL}/api/v1/unit-economics/clients/${clientId}/customers`);
    if (!response.ok) return [];
    const data = await response.json();
    return data.customers || [];
  } catch {
    return [];
  }
}

async function fetchCompletedJobs(clientId: string): Promise<Job[]> {
  try {
    const response = await fetch(
      `${API_URL}/api/v1/unit-economics/clients/${clientId}/completed-jobs`
    );
    if (!response.ok) return [];
    const data = await response.json();
    return data.jobs || [];
  } catch {
    return [];
  }
}

async function fetchMarketingSpend(clientId: string): Promise<Array<{ amount: number }>> {
  try {
    const response = await fetch(
      `${API_URL}/api/v1/unit-economics/clients/${clientId}/marketing-spend`
    );
    if (!response.ok) return [];
    const data = await response.json();
    return data.spend || [];
  } catch {
    return [];
  }
}

async function fetchPreviousMetrics(
  clientId: string
): Promise<{ ltvCacRatio: number } | null> {
  try {
    const response = await fetch(
      `${API_URL}/api/v1/unit-economics/clients/${clientId}`
    );
    if (!response.ok) return null;
    return response.json();
  } catch {
    return null;
  }
}

async function saveUnitEconomics(
  clientId: string,
  metrics: UnitEconomics
): Promise<void> {
  await fetch(`${API_URL}/api/v1/unit-economics/clients/${clientId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(metrics),
  });
}
