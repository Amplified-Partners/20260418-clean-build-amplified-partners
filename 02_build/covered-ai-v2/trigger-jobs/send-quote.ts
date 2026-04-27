/**
 * Covered AI - Send Quote Job
 *
 * Sends a quote email to a customer when triggered.
 */

import { task } from "@trigger.dev/sdk/v3";
import { ActionLog } from "./lib/action-logger";

interface Quote {
  id: string;
  clientId: string;
  quoteNumber: string;
  title: string;
  description?: string;
  customerName: string;
  customerEmail: string;
  customerPhone?: string;
  lineItems: Array<{
    description: string;
    quantity: number;
    unitPrice: number;
    total: number;
  }>;
  subtotal: number;
  vatRate: number;
  vatAmount: number;
  total: number;
  validUntil: string;
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
const RESEND_FROM_EMAIL = process.env.RESEND_FROM_EMAIL || "Covered AI <noreply@covered.ai>";

export const sendQuoteJob = task({
  id: "send-quote",
  retry: {
    maxAttempts: 3,
  },
  run: async (payload: { quoteId: string }) => {
    const { quoteId } = payload;

    console.log(`📧 Sending quote ${quoteId}`);

    // 1. Fetch quote details
    const quote = await fetchQuote(quoteId);
    if (!quote) {
      throw new Error(`Quote ${quoteId} not found`);
    }

    const client = await fetchClient(quote.clientId);
    if (!client) {
      throw new Error(`Client ${quote.clientId} not found`);
    }

    if (!quote.customerEmail) {
      return { sent: false, reason: "no_customer_email" };
    }

    // 2. Log autonomous action
    const action = await ActionLog.quoteSent(
      quote.clientId,
      quoteId,
      quote.customerName,
      quote.total
    );

    // 3. Send email via Resend
    if (!RESEND_API_KEY) {
      await action.fail("RESEND_API_KEY not configured");
      return { sent: false, reason: "no_api_key" };
    }

    const html = generateQuoteEmailHtml(quote, client);

    try {
      const response = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${RESEND_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          from: `${client.businessName} <noreply@covered.ai>`,
          to: quote.customerEmail,
          subject: `Quote ${quote.quoteNumber}: ${quote.title} from ${client.businessName}`,
          html,
          replyTo: client.email,
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        await action.fail(error);
        throw new Error(`Failed to send quote email: ${error}`);
      }

      // 4. Update quote status
      await updateQuoteStatus(quote.clientId, quoteId, "SENT");

      // 5. Mark action as successful
      await action.success(`Quote sent to ${quote.customerEmail}`);

      console.log(`✅ Quote ${quote.quoteNumber} sent to ${quote.customerEmail}`);

      return {
        success: true,
        quoteNumber: quote.quoteNumber,
        sentTo: quote.customerEmail,
      };
    } catch (error) {
      await action.fail(String(error));
      throw error;
    }
  },
});

// Helper functions
async function fetchQuote(quoteId: string): Promise<Quote | null> {
  try {
    // Need to get clientId first, or use a different endpoint
    const response = await fetch(`${API_URL}/api/v1/quotes/${quoteId}`);
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

async function updateQuoteStatus(clientId: string, quoteId: string, status: string): Promise<void> {
  await fetch(`${API_URL}/api/v1/clients/${clientId}/quotes/${quoteId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status, sentAt: new Date().toISOString() }),
  });
}

function generateQuoteEmailHtml(quote: Quote, client: Client): string {
  const validUntil = new Date(quote.validUntil).toLocaleDateString("en-GB", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" }).format(amount);

  const lineItemsHtml = quote.lineItems
    .map(
      (item) => `
      <tr>
        <td style="padding: 12px 0; border-bottom: 1px solid #e5e7eb;">${item.description}</td>
        <td style="padding: 12px 0; border-bottom: 1px solid #e5e7eb; text-align: center;">${item.quantity}</td>
        <td style="padding: 12px 0; border-bottom: 1px solid #e5e7eb; text-align: right;">${formatCurrency(item.unitPrice)}</td>
        <td style="padding: 12px 0; border-bottom: 1px solid #e5e7eb; text-align: right; font-weight: 500;">${formatCurrency(item.total)}</td>
      </tr>
    `
    )
    .join("");

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; background: #f6f9fc;">
  <div style="background: #ffffff; border-radius: 8px; overflow: hidden;">
    <!-- Header -->
    <div style="background: #0891b2; padding: 24px 32px;">
      <h1 style="color: #ffffff; margin: 0; font-size: 24px;">${client.businessName}</h1>
    </div>

    <!-- Quote Title -->
    <div style="padding: 32px; text-align: center;">
      <h2 style="color: #1f2937; font-size: 28px; margin: 0 0 8px;">Quote</h2>
      <p style="color: #6b7280; margin: 0;">#${quote.quoteNumber}</p>
    </div>

    <!-- Content -->
    <div style="padding: 0 32px 32px;">
      <p>Hi ${quote.customerName},</p>
      <p>Thank you for your enquiry. Please find our quote for <strong>${quote.title}</strong> below.</p>

      ${quote.description ? `<p style="color: #6b7280; font-size: 14px;">${quote.description}</p>` : ""}

      <!-- Validity Notice -->
      <div style="background: #fef3c7; border-radius: 8px; padding: 12px 16px; margin: 16px 0; text-align: center;">
        <p style="color: #92400e; margin: 0; font-size: 14px;">This quote is valid until <strong>${validUntil}</strong></p>
      </div>

      <!-- Line Items -->
      <table style="width: 100%; border-collapse: collapse; margin: 24px 0;">
        <thead>
          <tr style="border-bottom: 2px solid #e5e7eb;">
            <th style="padding: 12px 0; text-align: left; color: #6b7280; font-size: 12px; text-transform: uppercase;">Description</th>
            <th style="padding: 12px 0; text-align: center; color: #6b7280; font-size: 12px; text-transform: uppercase;">Qty</th>
            <th style="padding: 12px 0; text-align: right; color: #6b7280; font-size: 12px; text-transform: uppercase;">Unit Price</th>
            <th style="padding: 12px 0; text-align: right; color: #6b7280; font-size: 12px; text-transform: uppercase;">Total</th>
          </tr>
        </thead>
        <tbody>
          ${lineItemsHtml}
        </tbody>
      </table>

      <!-- Totals -->
      <table style="width: 100%; margin: 16px 0;">
        <tr>
          <td style="padding: 8px 0; color: #6b7280; text-align: right; padding-right: 16px;">Subtotal:</td>
          <td style="padding: 8px 0; text-align: right; width: 100px;">${formatCurrency(quote.subtotal)}</td>
        </tr>
        <tr>
          <td style="padding: 8px 0; color: #6b7280; text-align: right; padding-right: 16px;">VAT (${quote.vatRate * 100}%):</td>
          <td style="padding: 8px 0; text-align: right;">${formatCurrency(quote.vatAmount)}</td>
        </tr>
        <tr style="border-top: 2px solid #e5e7eb;">
          <td style="padding: 16px 0 8px; color: #1f2937; font-weight: 600; font-size: 16px; text-align: right; padding-right: 16px;">Quote Total:</td>
          <td style="padding: 16px 0 8px; text-align: right; color: #0891b2; font-weight: bold; font-size: 20px;">${formatCurrency(quote.total)}</td>
        </tr>
      </table>

      <!-- What's Next -->
      <div style="margin: 32px 0;">
        <h3 style="color: #1f2937; font-size: 16px; margin: 0 0 12px;">What happens next?</h3>
        <ol style="color: #6b7280; font-size: 14px; padding-left: 20px; margin: 0;">
          <li style="margin-bottom: 8px;">Review the quote details above</li>
          <li style="margin-bottom: 8px;">Reply to this email to accept or ask questions</li>
          <li>We'll contact you to schedule the work</li>
        </ol>
      </div>

      <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;">

      <p style="color: #6b7280; font-size: 14px;">
        Have questions? Contact us at ${client.email} or call ${client.phone}.
      </p>

      <p>
        Best regards,<br>
        ${client.ownerName} at ${client.businessName}
      </p>
    </div>
  </div>
</body>
</html>
  `.trim();
}

// Add to ActionLog
declare module "./lib/action-logger" {
  interface ActionLogType {
    quoteSent: (
      clientId: string,
      quoteId: string,
      customerName: string,
      amount: number
    ) => Promise<{ id: string; success: (details?: string) => Promise<void>; fail: (details?: string) => Promise<void>; partial: (details?: string) => Promise<void> }>;
  }
}

// Extend ActionLog with quoteSent
ActionLog.quoteSent = async (
  clientId: string,
  quoteId: string,
  customerName: string,
  amount: number
) => {
  const { logAction } = await import("./lib/action-logger");
  return logAction({
    clientId,
    actionType: "QUOTE_GENERATED",
    description: `Sent quote for £${amount.toFixed(2)} to ${customerName}`,
    triggerId: quoteId,
    triggerType: "quote",
    triggerReason: "Quote ready to send",
    decision: "send_quote",
    confidence: 1.0,
    modelUsed: "rule-based",
  });
};
