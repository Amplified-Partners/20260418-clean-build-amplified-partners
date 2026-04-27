/**
 * Email Service - Renders React Email templates and sends via Resend
 */

import { Resend } from "resend";
import { render } from "@react-email/components";
import {
  InvoiceEmail,
  InvoiceReminderEmail,
  QuoteEmail,
  ReviewRequestEmail,
  LeadAcknowledgmentEmail,
} from "../../emails";

// Initialize Resend client
const resend = new Resend(process.env.RESEND_API_KEY);

// Default from address
const DEFAULT_FROM = process.env.EMAIL_FROM || "Covered AI <noreply@covered.ai>";

// Types
interface SendEmailOptions {
  to: string | string[];
  subject: string;
  html: string;
  from?: string;
  replyTo?: string;
  tags?: { name: string; value: string }[];
}

interface EmailResult {
  success: boolean;
  id?: string;
  error?: string;
}

// Base send function
async function sendEmail(options: SendEmailOptions): Promise<EmailResult> {
  try {
    const { data, error } = await resend.emails.send({
      from: options.from || DEFAULT_FROM,
      to: options.to,
      subject: options.subject,
      html: options.html,
      replyTo: options.replyTo,
      tags: options.tags,
    });

    if (error) {
      console.error("Email send error:", error);
      return { success: false, error: error.message };
    }

    return { success: true, id: data?.id };
  } catch (error) {
    console.error("Email send exception:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

// Invoice Email
interface SendInvoiceEmailParams {
  to: string;
  customerName: string;
  businessName: string;
  invoiceNumber: string;
  invoiceDate: string;
  dueDate: string;
  lineItems: { description: string; amount: number }[];
  subtotal: number;
  vatRate: number;
  vatAmount: number;
  total: number;
  paymentLink?: string;
  businessPhone?: string;
  businessEmail?: string;
  replyTo?: string;
}

export async function sendInvoiceEmail(
  params: SendInvoiceEmailParams
): Promise<EmailResult> {
  const html = await render(
    InvoiceEmail({
      customerName: params.customerName,
      businessName: params.businessName,
      invoiceNumber: params.invoiceNumber,
      invoiceDate: params.invoiceDate,
      dueDate: params.dueDate,
      lineItems: params.lineItems,
      subtotal: params.subtotal,
      vatRate: params.vatRate,
      vatAmount: params.vatAmount,
      total: params.total,
      paymentLink: params.paymentLink,
      businessPhone: params.businessPhone,
      businessEmail: params.businessEmail,
    })
  );

  return sendEmail({
    to: params.to,
    subject: `Invoice ${params.invoiceNumber} from ${params.businessName}`,
    html,
    replyTo: params.replyTo || params.businessEmail,
    tags: [
      { name: "type", value: "invoice" },
      { name: "invoice_number", value: params.invoiceNumber },
    ],
  });
}

// Invoice Reminder Email
interface SendInvoiceReminderEmailParams {
  to: string;
  customerName: string;
  businessName: string;
  invoiceNumber: string;
  dueDate: string;
  total: number;
  isOverdue: boolean;
  daysOverdue?: number;
  paymentLink?: string;
  businessPhone?: string;
  businessEmail?: string;
  replyTo?: string;
}

export async function sendInvoiceReminderEmail(
  params: SendInvoiceReminderEmailParams
): Promise<EmailResult> {
  const html = await render(
    InvoiceReminderEmail({
      customerName: params.customerName,
      businessName: params.businessName,
      invoiceNumber: params.invoiceNumber,
      dueDate: params.dueDate,
      total: params.total,
      isOverdue: params.isOverdue,
      daysOverdue: params.daysOverdue,
      paymentLink: params.paymentLink,
      businessPhone: params.businessPhone,
      businessEmail: params.businessEmail,
    })
  );

  const subject = params.isOverdue
    ? `Overdue: Invoice ${params.invoiceNumber} from ${params.businessName}`
    : `Reminder: Invoice ${params.invoiceNumber} due soon`;

  return sendEmail({
    to: params.to,
    subject,
    html,
    replyTo: params.replyTo || params.businessEmail,
    tags: [
      { name: "type", value: params.isOverdue ? "invoice_overdue" : "invoice_reminder" },
      { name: "invoice_number", value: params.invoiceNumber },
    ],
  });
}

// Quote Email
interface SendQuoteEmailParams {
  to: string;
  customerName: string;
  businessName: string;
  quoteNumber: string;
  title: string;
  description?: string;
  lineItems: { description: string; quantity: number; unitPrice: number; total: number }[];
  subtotal: number;
  vatRate: number;
  vatAmount: number;
  total: number;
  validUntil: string;
  viewLink?: string;
  acceptLink?: string;
  businessPhone?: string;
  businessEmail?: string;
  personalMessage?: string;
  replyTo?: string;
}

export async function sendQuoteEmail(
  params: SendQuoteEmailParams
): Promise<EmailResult> {
  const html = await render(
    QuoteEmail({
      customerName: params.customerName,
      businessName: params.businessName,
      quoteNumber: params.quoteNumber,
      title: params.title,
      description: params.description,
      lineItems: params.lineItems,
      subtotal: params.subtotal,
      vatRate: params.vatRate,
      vatAmount: params.vatAmount,
      total: params.total,
      validUntil: params.validUntil,
      viewLink: params.viewLink,
      acceptLink: params.acceptLink,
      businessPhone: params.businessPhone,
      businessEmail: params.businessEmail,
      personalMessage: params.personalMessage,
    })
  );

  return sendEmail({
    to: params.to,
    subject: `Quote ${params.quoteNumber}: ${params.title} from ${params.businessName}`,
    html,
    replyTo: params.replyTo || params.businessEmail,
    tags: [
      { name: "type", value: "quote" },
      { name: "quote_number", value: params.quoteNumber },
    ],
  });
}

// Review Request Email
interface SendReviewRequestEmailParams {
  to: string;
  customerName: string;
  businessName: string;
  jobTitle: string;
  completedDate: string;
  reviewLink: string;
  businessPhone?: string;
  businessEmail?: string;
  replyTo?: string;
}

export async function sendReviewRequestEmail(
  params: SendReviewRequestEmailParams
): Promise<EmailResult> {
  const html = await render(
    ReviewRequestEmail({
      customerName: params.customerName,
      businessName: params.businessName,
      jobTitle: params.jobTitle,
      completedDate: params.completedDate,
      reviewLink: params.reviewLink,
      businessPhone: params.businessPhone,
      businessEmail: params.businessEmail,
    })
  );

  return sendEmail({
    to: params.to,
    subject: `How was your experience with ${params.businessName}?`,
    html,
    replyTo: params.replyTo || params.businessEmail,
    tags: [{ name: "type", value: "review_request" }],
  });
}

// Lead Acknowledgment Email
interface SendLeadAcknowledgmentEmailParams {
  to: string;
  customerName: string;
  businessName: string;
  ownerName?: string;
  jobType: string;
  urgency: "emergency" | "urgent" | "routine";
  callbackTime?: string;
  businessPhone?: string;
  businessEmail?: string;
  vertical?: string;
  replyTo?: string;
}

export async function sendLeadAcknowledgmentEmail(
  params: SendLeadAcknowledgmentEmailParams
): Promise<EmailResult> {
  const html = await render(
    LeadAcknowledgmentEmail({
      customerName: params.customerName,
      businessName: params.businessName,
      ownerName: params.ownerName,
      jobType: params.jobType,
      urgency: params.urgency,
      callbackTime: params.callbackTime,
      businessPhone: params.businessPhone,
      businessEmail: params.businessEmail,
      vertical: params.vertical,
    })
  );

  const subject =
    params.urgency === "emergency"
      ? `Urgent: We're handling your ${params.jobType} - ${params.businessName}`
      : `We've received your ${params.jobType} request - ${params.businessName}`;

  return sendEmail({
    to: params.to,
    subject,
    html,
    replyTo: params.replyTo || params.businessEmail,
    tags: [
      { name: "type", value: "lead_acknowledgment" },
      { name: "urgency", value: params.urgency },
    ],
  });
}

// Export all functions
export const emailService = {
  sendInvoiceEmail,
  sendInvoiceReminderEmail,
  sendQuoteEmail,
  sendReviewRequestEmail,
  sendLeadAcknowledgmentEmail,
};

export default emailService;
