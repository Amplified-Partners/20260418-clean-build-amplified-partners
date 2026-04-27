/**
 * Covered AI - Aggregate Action Metrics Job
 *
 * Daily job that aggregates autonomous action metrics for each client.
 * Creates ActionMetrics records for dashboard display and trend analysis.
 */

import { schedules } from "@trigger.dev/sdk/v3";

const API_URL = process.env.API_URL || "http://localhost:8000";

interface AutonomousAction {
  id: string;
  clientId: string;
  actionType: string;
  confidence: number;
  outcome: string;
  wasOverridden: boolean;
  executionTimeMs: number | null;
  tokenCount: number | null;
  costEstimate: number | null;
  createdAt: string;
}

interface ActionMetricsPayload {
  clientId: string;
  periodStart: string;
  periodEnd: string;
  periodType: string;
  totalActions: number;
  successCount: number;
  failedCount: number;
  overriddenCount: number;
  avgConfidence: number;
  lowConfidenceCount: number;
  actionBreakdown: Record<string, number>;
  avgExecutionMs: number;
  totalTokens: number;
  totalCost: number;
  accuracyRate: number;
}

// =============================================================================
// AGGREGATE METRICS (DAILY AT 1AM)
// =============================================================================

export const aggregateActionMetrics = schedules.task({
  id: "aggregate-action-metrics",
  cron: "0 1 * * *", // Daily at 1am UTC
  run: async () => {
    console.log("📊 Starting action metrics aggregation");

    // Calculate yesterday's date range
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    const periodStart = yesterday.toISOString();
    const periodEnd = today.toISOString();

    console.log(`   Period: ${yesterday.toDateString()} to ${today.toDateString()}`);

    // Get all clients with actions yesterday
    const clientIds = await getClientsWithActions(periodStart, periodEnd);
    console.log(`   Found ${clientIds.length} clients with actions`);

    let processed = 0;
    let errors = 0;

    for (const clientId of clientIds) {
      try {
        // Fetch actions for this client from yesterday
        const actions = await fetchClientActions(clientId, periodStart, periodEnd);

        if (actions.length === 0) continue;

        // Calculate metrics
        const metrics = calculateMetrics(clientId, actions, periodStart, periodEnd);

        // Save metrics
        await saveMetrics(metrics);

        processed++;
        console.log(`   ✓ Processed metrics for client ${clientId}: ${actions.length} actions`);
      } catch (error) {
        console.error(`   ✗ Error processing client ${clientId}:`, error);
        errors++;
      }
    }

    console.log(`✅ Action metrics aggregation complete: ${processed} clients processed, ${errors} errors`);

    return {
      processed,
      errors,
      period: {
        start: periodStart,
        end: periodEnd,
      },
    };
  },
});

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

async function getClientsWithActions(start: string, end: string): Promise<string[]> {
  try {
    // Get unique client IDs from actions table
    const response = await fetch(
      `${API_URL}/api/v1/actions/clients-with-actions?start=${encodeURIComponent(start)}&end=${encodeURIComponent(end)}`
    );

    if (!response.ok) {
      // Fallback: get all clients and filter
      const clientsResponse = await fetch(`${API_URL}/api/v1/clients`);
      if (!clientsResponse.ok) return [];
      const data = await clientsResponse.json();
      return (data.clients || []).map((c: { id: string }) => c.id);
    }

    const data = await response.json();
    return data.clientIds || [];
  } catch (error) {
    console.error("Error fetching clients with actions:", error);
    return [];
  }
}

async function fetchClientActions(
  clientId: string,
  start: string,
  end: string
): Promise<AutonomousAction[]> {
  try {
    const response = await fetch(
      `${API_URL}/api/v1/actions/clients/${clientId}?limit=1000`
    );

    if (!response.ok) return [];

    const data = await response.json();
    const actions: AutonomousAction[] = data.actions || [];

    // Filter to yesterday's actions
    return actions.filter((a) => {
      const createdAt = new Date(a.createdAt);
      return createdAt >= new Date(start) && createdAt < new Date(end);
    });
  } catch (error) {
    console.error(`Error fetching actions for client ${clientId}:`, error);
    return [];
  }
}

function calculateMetrics(
  clientId: string,
  actions: AutonomousAction[],
  periodStart: string,
  periodEnd: string
): ActionMetricsPayload {
  const total = actions.length;
  const successful = actions.filter((a) => a.outcome === "SUCCESS").length;
  const failed = actions.filter((a) => a.outcome === "FAILED").length;
  const overridden = actions.filter((a) => a.wasOverridden).length;
  const lowConfidence = actions.filter((a) => a.confidence < 0.7).length;

  const avgConfidence =
    total > 0 ? actions.reduce((sum, a) => sum + a.confidence, 0) / total : 0;

  const avgExecutionMs =
    total > 0
      ? actions.reduce((sum, a) => sum + (a.executionTimeMs || 0), 0) / total
      : 0;

  const totalTokens = actions.reduce((sum, a) => sum + (a.tokenCount || 0), 0);
  const totalCost = actions.reduce((sum, a) => sum + (a.costEstimate || 0), 0);

  // Action breakdown by type
  const actionBreakdown: Record<string, number> = {};
  for (const action of actions) {
    actionBreakdown[action.actionType] = (actionBreakdown[action.actionType] || 0) + 1;
  }

  // Accuracy rate: percentage not overridden
  const accuracyRate = total > 0 ? (total - overridden) / total : 1;

  return {
    clientId,
    periodStart,
    periodEnd,
    periodType: "day",
    totalActions: total,
    successCount: successful,
    failedCount: failed,
    overriddenCount: overridden,
    avgConfidence,
    lowConfidenceCount: lowConfidence,
    actionBreakdown,
    avgExecutionMs,
    totalTokens,
    totalCost,
    accuracyRate,
  };
}

async function saveMetrics(metrics: ActionMetricsPayload): Promise<void> {
  try {
    await fetch(`${API_URL}/api/v1/actions/metrics`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(metrics),
    });
  } catch (error) {
    console.error("Error saving metrics:", error);
    throw error;
  }
}
