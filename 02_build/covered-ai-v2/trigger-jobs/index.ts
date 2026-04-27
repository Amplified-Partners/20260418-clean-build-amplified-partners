/**
 * Covered AI - Trigger.dev Job Exports
 */

// Lead & Customer Jobs
export { leadNurtureSequence } from "./lead-nurture";
export { reviewRequestJob } from "./review-request";
export { generateVideoJob } from "./video-generation";

// Invoice & Quote Jobs
export { sendInvoiceJob, invoiceReminderSequence, updateCashMetrics } from "./invoice-chasing";
export { sendQuoteJob } from "./send-quote";
export { generateInvoicePdf } from "./generate-invoice-pdf";
export { generateQuotePdf } from "./generate-quote-pdf";
export { sendInvoice } from "./send-invoice";
export { sendInvoiceReminder } from "./send-invoice-reminder";
export { checkOverdueInvoices } from "./check-overdue-invoices";

// Analytics Jobs
export { updateCustomerLTV, calculateUnitEconomics, calculateClientMetricsOnDemand } from "./unit-economics";
export { generateAttentionItems, calculateTodayStats, calculateClientStatsOnDemand } from "./dashboard-stats";
export { aggregateActionMetrics } from "./aggregate-action-metrics";

// Health & Retention Jobs
export { calculateHealthScores } from "./calculate-health-scores";

// Digest & Summary Jobs
export { generateWeeklySummary } from "./weekly-summary";
export { sendMorningDigest } from "./morning-digest";

// GEO Engine Jobs
export { generateGeoPages, generateGeoPageForClient, extractFaqsFromCalls, monitorAiCitations } from "./geo-page";

// Xero Integration Jobs
export { refreshXeroTokens, refreshSingleToken, manualTokenRefresh } from "./refresh-xero-tokens";

// Outreach & Demo Number Jobs
export { processOutreachQueue, expireDemoNumbers } from "./outreach-processor";

// Event Log Cleanup
export { cleanupOldEvents } from "./cleanup-events";

// Client Check-in Jobs
export { processClientCheckins, sendClientCheckin } from "./checkin-reminder";
