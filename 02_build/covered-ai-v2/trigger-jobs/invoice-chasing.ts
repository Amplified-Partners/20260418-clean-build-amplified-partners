/**
 * Covered AI - Invoice Chasing & Cash Flow Jobs
 *
 * Jobs for sending invoices, automated reminders, and metrics calculation.
 */

import { task, schedules } from "@trigger.dev/sdk/v3";
import { ActionLog } from "./lib/action-logger";

interface Invoice {
  id: string;
  clientId: string;
  invoiceNumber: string;
  customerName: string;
  customerEmail: string;
  customerPhone?: string;
  amount: number;
  description: string;
  dueDate: string;
  status: string;
  sentAt?: string;
  reminder1SentAt?: string;
  reminder2SentAt?: string;
  finalNoticeSentAt?: string;
}

interface Client {
  id: string;
  businessName: string;
  ownerName: string;
  email: string;
  phone: string;
}

const API_URL = process.env.API_URL || "http://localhost:8000";
const RESEND_API_KEY = process.env.RESEND_API_KEY;
const RESEND_FROM_EMAIL = process.env.RESEND_FROM_EMAIL || "Covered AI <onboarding@resend.dev>";

// =============================================================================
// SEND INVOICE JOB
// =============================================================================

export const sendInvoiceJob = task({
  id: "send-invoice",
  retry: {
    maxAttempts: 3,
  },
  run: async (payload: { invoiceId: string }) => {
    const { invoiceId } = payload;

    console.log(`📧 Sending invoice ${invoiceId}`);

    // 1. Fetch invoice details
    const invoice = await fetchInvoice(invoiceId);
    if (!invoice) {
      throw new Error(`Invoice ${invoiceId} not found`);
    }

    const client = await fetchClient(invoice.clientId);
    if (!client) {
      throw new Error(`Client ${invoice.clientId} not found`);
    }

    // 2. Log autonomous action
    const action = await ActionLog.invoiceSent(
      invoice.clientId,
      invoiceId,
      invoice.customerName,
      invoice.amount
    );

    // 3. Send email via Resend
    const emailResult = await sendInvoiceEmail(invoice, client);

    if (!emailResult.success) {
      await action.fail(emailResult.error);
      throw new Error(`Failed to send invoice email: ${emailResult.error}`);
    }

    // 4. Update invoice status
    await updateInvoiceStatus(invoiceId, "SENT", { sentAt: new Date().toISOString() });

    // 5. Mark action as successful
    await action.success(`Email delivered to ${invoice.customerEmail}`);

    console.log(`✅ Invoice ${invoice.invoiceNumber} sent to ${invoice.customerEmail}`);

    return {
      success: true,
      invoiceNumber: invoice.invoiceNumber,
      sentTo: invoice.customerEmail,
    };
  },
});

// =============================================================================
// INVOICE REMINDER SEQUENCE (SCHEDULED)
// =============================================================================

export const invoiceReminderSequence = schedules.task({
  id: "invoice-reminder-sequence",
  cron: "0 9 * * *", // Daily at 9am UTC
  run: async () => {
    console.log(`⏰ Running invoice reminder sequence`);

    // Fetch all unpaid invoices (SENT or REMINDED status)
    const unpaidInvoices = await fetchUnpaidInvoices();

    console.log(`📋 Found ${unpaidInvoices.length} unpaid invoices`);

    const results = {
      reminder1Sent: 0,
      reminder2Sent: 0,
      finalNoticeSent: 0,
      errors: 0,
    };

    for (const invoice of unpaidInvoices) {
      try {
        const client = await fetchClient(invoice.clientId);
        if (!client) continue;

        const sentDate = new Date(invoice.sentAt!);
        const now = new Date();
        const daysSinceSent = Math.floor((now.getTime() - sentDate.getTime()) / (1000 * 60 * 60 * 24));

        // Day 7: First reminder
        if (daysSinceSent >= 7 && !invoice.reminder1SentAt) {
          const action = await ActionLog.invoiceReminderSent(
            invoice.clientId,
            invoice.id,
            invoice.customerName,
            daysSinceSent,
            7
          );
          try {
            await sendReminder1(invoice, client);
            await updateInvoiceStatus(invoice.id, "SENT", { reminder1SentAt: now.toISOString() });
            await action.success(`Reminder 1 sent to ${invoice.customerEmail}`);
            results.reminder1Sent++;
            console.log(`📤 Reminder 1 sent for ${invoice.invoiceNumber}`);
          } catch (err) {
            await action.fail(String(err));
            throw err;
          }
        }
        // Day 14: Second reminder, status → REMINDED
        else if (daysSinceSent >= 14 && !invoice.reminder2SentAt) {
          const action = await ActionLog.invoiceReminderSent(
            invoice.clientId,
            invoice.id,
            invoice.customerName,
            daysSinceSent,
            14
          );
          try {
            await sendReminder2(invoice, client);
            await updateInvoiceStatus(invoice.id, "REMINDED", { reminder2SentAt: now.toISOString() });
            await action.success(`Reminder 2 sent to ${invoice.customerEmail}`);
            results.reminder2Sent++;
            console.log(`📤 Reminder 2 sent for ${invoice.invoiceNumber}`);
          } catch (err) {
            await action.fail(String(err));
            throw err;
          }
        }
        // Day 21: Final notice, status → OVERDUE
        else if (daysSinceSent >= 21 && !invoice.finalNoticeSentAt) {
          const action = await ActionLog.invoiceReminderSent(
            invoice.clientId,
            invoice.id,
            invoice.customerName,
            daysSinceSent,
            21
          );
          try {
            await sendFinalNotice(invoice, client);
            await updateInvoiceStatus(invoice.id, "OVERDUE", { finalNoticeSentAt: now.toISOString() });
            await action.success(`Final notice sent to ${invoice.customerEmail}`);
            results.finalNoticeSent++;
            console.log(`📤 Final notice sent for ${invoice.invoiceNumber}`);
          } catch (err) {
            await action.fail(String(err));
            throw err;
          }
        }
      } catch (error) {
        console.error(`❌ Error processing invoice ${invoice.id}:`, error);
        results.errors++;
      }
    }

    console.log(`✅ Reminder sequence complete:`, results);
    return results;
  },
});

// =============================================================================
// UPDATE CASH METRICS (SCHEDULED)
// =============================================================================

export const updateCashMetrics = schedules.task({
  id: "update-cash-metrics",
  cron: "0 * * * *", // Hourly
  run: async () => {
    console.log(`📊 Updating cash flow metrics`);

    // Get all clients with invoices
    const clients = await fetchClientsWithInvoices();

    for (const clientId of clients) {
      try {
        const metrics = await calculateClientMetrics(clientId);
        await saveClientMetrics(clientId, metrics);
        console.log(`   Updated metrics for client ${clientId}`);
      } catch (error) {
        console.error(`❌ Error updating metrics for client ${clientId}:`, error);
      }
    }

    console.log(`✅ Cash metrics updated for ${clients.length} clients`);
    return { clientsUpdated: clients.length };
  },
});

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

async function fetchInvoice(invoiceId: string): Promise<Invoice | null> {
  try {
    const response = await fetch(`${API_URL}/api/v1/invoices/${invoiceId}`);
    if (!response.ok) return null;
    return response.json();
  } catch {
    return null;
  }
}

async function fetchClient(clientId: string): Promise<Client | null> {
  try {
    const response = await fetch(`${API_URL}/api/v1/clients/${clientId}`);
    if (!response.ok) return null;
    return response.json();
  } catch {
    return null;
  }
}

async function fetchUnpaidInvoices(): Promise<Invoice[]> {
  try {
    const response = await fetch(`${API_URL}/api/v1/invoices?status=SENT,REMINDED`);
    if (!response.ok) return [];
    const data = await response.json();
    return data.invoices || [];
  } catch {
    return [];
  }
}

async function fetchClientsWithInvoices(): Promise<string[]> {
  try {
    const response = await fetch(`${API_URL}/api/v1/invoices/clients-with-invoices`);
    if (!response.ok) return [];
    const data = await response.json();
    return data.clientIds || [];
  } catch {
    return [];
  }
}

async function updateInvoiceStatus(
  invoiceId: string,
  status: string,
  additionalFields: Record<string, string>
): Promise<void> {
  await fetch(`${API_URL}/api/v1/invoices/${invoiceId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status, ...additionalFields }),
  });
}

async function sendInvoiceEmail(invoice: Invoice, client: Client): Promise<{ success: boolean; error?: string }> {
  if (!RESEND_API_KEY) {
    return { success: false, error: "RESEND_API_KEY not configured" };
  }

  const html = generateInvoiceEmailHtml(invoice, client);

  try {
    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: RESEND_FROM_EMAIL,
        to: invoice.customerEmail,
        subject: `Invoice ${invoice.invoiceNumber} from ${client.businessName}`,
        html: html,
      }),
    });

    if (!response.ok) {
      const error = await response.text();
      return { success: false, error };
    }

    return { success: true };
  } catch (error) {
    return { success: false, error: String(error) };
  }
}

async function sendReminder1(invoice: Invoice, client: Client): Promise<void> {
  if (!RESEND_API_KEY) return;

  const html = generateReminder1Html(invoice, client);

  await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: RESEND_FROM_EMAIL,
      to: invoice.customerEmail,
      subject: `Friendly reminder: Invoice ${invoice.invoiceNumber}`,
      html: html,
    }),
  });
}

async function sendReminder2(invoice: Invoice, client: Client): Promise<void> {
  if (!RESEND_API_KEY) return;

  const html = generateReminder2Html(invoice, client);

  await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: RESEND_FROM_EMAIL,
      to: invoice.customerEmail,
      subject: `Invoice ${invoice.invoiceNumber} is now overdue`,
      html: html,
    }),
  });
}

async function sendFinalNotice(invoice: Invoice, client: Client): Promise<void> {
  if (!RESEND_API_KEY) return;

  const html = generateFinalNoticeHtml(invoice, client);

  await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: RESEND_FROM_EMAIL,
      to: invoice.customerEmail,
      subject: `Final notice: Invoice ${invoice.invoiceNumber}`,
      html: html,
    }),
  });
}

async function calculateClientMetrics(clientId: string): Promise<{
  totalOutstanding: number;
  totalOverdue: number;
  collectedThisMonth: number;
  collectedLastMonth: number;
  averageDSO: number;
}> {
  // Fetch all invoices for the client
  const response = await fetch(`${API_URL}/api/v1/invoices?clientId=${clientId}`);
  const data = await response.json();
  const invoices: Invoice[] = data.invoices || [];

  const now = new Date();
  const thisMonthStart = new Date(now.getFullYear(), now.getMonth(), 1);
  const lastMonthStart = new Date(now.getFullYear(), now.getMonth() - 1, 1);
  const lastMonthEnd = new Date(now.getFullYear(), now.getMonth(), 0);

  let totalOutstanding = 0;
  let totalOverdue = 0;
  let collectedThisMonth = 0;
  let collectedLastMonth = 0;
  let dsoSum = 0;
  let dsoCount = 0;

  for (const inv of invoices) {
    const amount = Number(inv.amount);

    // Outstanding: not paid, not cancelled, not written off
    if (!["PAID", "CANCELLED", "WRITTEN_OFF"].includes(inv.status)) {
      totalOutstanding += amount;

      // Overdue: due date passed
      if (new Date(inv.dueDate) < now) {
        totalOverdue += amount;
      }
    }

    // Collected this month
    if (inv.status === "PAID" && inv.sentAt) {
      const paidDate = new Date(inv.sentAt); // Using sentAt as proxy, should use paidAt
      if (paidDate >= thisMonthStart) {
        collectedThisMonth += amount;
      } else if (paidDate >= lastMonthStart && paidDate <= lastMonthEnd) {
        collectedLastMonth += amount;
      }

      // DSO calculation (days from sent to paid)
      if (inv.sentAt) {
        const sent = new Date(inv.sentAt);
        const daysToPayment = Math.floor((paidDate.getTime() - sent.getTime()) / (1000 * 60 * 60 * 24));
        if (daysToPayment >= 0) {
          dsoSum += daysToPayment;
          dsoCount++;
        }
      }
    }
  }

  const averageDSO = dsoCount > 0 ? Math.round(dsoSum / dsoCount) : 0;

  return {
    totalOutstanding,
    totalOverdue,
    collectedThisMonth,
    collectedLastMonth,
    averageDSO,
  };
}

async function saveClientMetrics(clientId: string, metrics: {
  totalOutstanding: number;
  totalOverdue: number;
  collectedThisMonth: number;
  collectedLastMonth: number;
  averageDSO: number;
}): Promise<void> {
  await fetch(`${API_URL}/api/v1/clients/${clientId}/cash-metrics`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(metrics),
  });
}

// =============================================================================
// EMAIL TEMPLATES
// =============================================================================

function generateInvoiceEmailHtml(invoice: Invoice, client: Client): string {
  const dueDate = new Date(invoice.dueDate).toLocaleDateString("en-GB", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  const amount = new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
  }).format(Number(invoice.amount));

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Invoice ${invoice.invoiceNumber}</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  <div style="background: #f8f9fa; border-radius: 8px; padding: 30px; margin-bottom: 20px;">
    <h1 style="margin: 0 0 10px 0; color: #1a1a1a; font-size: 24px;">Invoice ${invoice.invoiceNumber}</h1>
    <p style="margin: 0; color: #666;">From ${client.businessName}</p>
  </div>

  <p>Hi ${invoice.customerName},</p>

  <p>Please find your invoice details below:</p>

  <div style="background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; margin: 20px 0;">
    <table style="width: 100%; border-collapse: collapse;">
      <tr>
        <td style="padding: 8px 0; color: #666;">Invoice Number</td>
        <td style="padding: 8px 0; text-align: right; font-weight: 600;">${invoice.invoiceNumber}</td>
      </tr>
      <tr>
        <td style="padding: 8px 0; color: #666;">Description</td>
        <td style="padding: 8px 0; text-align: right;">${invoice.description}</td>
      </tr>
      <tr>
        <td style="padding: 8px 0; color: #666;">Due Date</td>
        <td style="padding: 8px 0; text-align: right;">${dueDate}</td>
      </tr>
      <tr style="border-top: 2px solid #e0e0e0;">
        <td style="padding: 16px 0 8px; color: #1a1a1a; font-weight: 600; font-size: 18px;">Amount Due</td>
        <td style="padding: 16px 0 8px; text-align: right; font-weight: 700; font-size: 24px; color: #2563eb;">${amount}</td>
      </tr>
    </table>
  </div>

  <div style="text-align: center; margin: 30px 0;">
    <a href="#" style="display: inline-block; background: #2563eb; color: #fff; padding: 14px 32px; border-radius: 6px; text-decoration: none; font-weight: 600;">Pay Now</a>
  </div>

  <p style="color: #666; font-size: 14px;">If you have any questions about this invoice, please contact ${client.businessName} at ${client.email} or ${client.phone}.</p>

  <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 30px 0;">

  <p style="color: #999; font-size: 12px; text-align: center;">
    This invoice was sent via Covered AI on behalf of ${client.businessName}.
  </p>
</body>
</html>
  `.trim();
}

function generateReminder1Html(invoice: Invoice, client: Client): string {
  const amount = new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
  }).format(Number(invoice.amount));

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  <h1 style="color: #1a1a1a; font-size: 22px;">Friendly Reminder</h1>

  <p>Hi ${invoice.customerName},</p>

  <p>Just a quick reminder that invoice <strong>${invoice.invoiceNumber}</strong> for <strong>${amount}</strong> is still awaiting payment.</p>

  <p>If you've already made the payment, please disregard this email. Otherwise, we'd appreciate it if you could settle this at your earliest convenience.</p>

  <div style="text-align: center; margin: 30px 0;">
    <a href="#" style="display: inline-block; background: #2563eb; color: #fff; padding: 14px 32px; border-radius: 6px; text-decoration: none; font-weight: 600;">Pay Now</a>
  </div>

  <p>Thanks for your business!</p>

  <p style="color: #666;">
    Best regards,<br>
    ${client.businessName}
  </p>
</body>
</html>
  `.trim();
}

function generateReminder2Html(invoice: Invoice, client: Client): string {
  const amount = new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
  }).format(Number(invoice.amount));

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  <h1 style="color: #dc2626; font-size: 22px;">Invoice Overdue</h1>

  <p>Hi ${invoice.customerName},</p>

  <p>Our records show that invoice <strong>${invoice.invoiceNumber}</strong> for <strong>${amount}</strong> is now overdue.</p>

  <p>Please arrange payment as soon as possible to avoid any service disruption.</p>

  <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 16px; margin: 20px 0;">
    <p style="margin: 0; color: #991b1b;"><strong>Amount Due: ${amount}</strong></p>
  </div>

  <div style="text-align: center; margin: 30px 0;">
    <a href="#" style="display: inline-block; background: #dc2626; color: #fff; padding: 14px 32px; border-radius: 6px; text-decoration: none; font-weight: 600;">Pay Now</a>
  </div>

  <p>If you're experiencing difficulties with payment, please get in touch so we can discuss options.</p>

  <p style="color: #666;">
    Best regards,<br>
    ${client.businessName}<br>
    ${client.phone}
  </p>
</body>
</html>
  `.trim();
}

function generateFinalNoticeHtml(invoice: Invoice, client: Client): string {
  const amount = new Intl.NumberFormat("en-GB", {
    style: "currency",
    currency: "GBP",
  }).format(Number(invoice.amount));

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  <div style="background: #7f1d1d; color: #fff; padding: 20px; border-radius: 8px 8px 0 0; text-align: center;">
    <h1 style="margin: 0; font-size: 22px;">FINAL NOTICE</h1>
  </div>

  <div style="border: 2px solid #7f1d1d; border-top: none; border-radius: 0 0 8px 8px; padding: 20px;">
    <p>Dear ${invoice.customerName},</p>

    <p>Despite previous reminders, invoice <strong>${invoice.invoiceNumber}</strong> remains unpaid. This is your final notice before we escalate this matter.</p>

    <div style="background: #fef2f2; border: 1px solid #fecaca; border-radius: 8px; padding: 16px; margin: 20px 0;">
      <table style="width: 100%;">
        <tr>
          <td>Invoice Number:</td>
          <td style="text-align: right; font-weight: 600;">${invoice.invoiceNumber}</td>
        </tr>
        <tr>
          <td>Amount Due:</td>
          <td style="text-align: right; font-weight: 700; font-size: 20px; color: #dc2626;">${amount}</td>
        </tr>
      </table>
    </div>

    <p><strong>Please make payment within 7 days</strong> to avoid further action, which may include:</p>
    <ul>
      <li>Referral to a debt collection agency</li>
      <li>Impact on your credit rating</li>
      <li>Legal proceedings to recover the debt</li>
    </ul>

    <div style="text-align: center; margin: 30px 0;">
      <a href="#" style="display: inline-block; background: #7f1d1d; color: #fff; padding: 14px 32px; border-radius: 6px; text-decoration: none; font-weight: 600;">Pay Now to Resolve</a>
    </div>

    <p>If you believe this is an error or wish to discuss payment arrangements, please contact us immediately at ${client.phone}.</p>

    <p style="color: #666;">
      Regards,<br>
      ${client.businessName}
    </p>
  </div>
</body>
</html>
  `.trim();
}
