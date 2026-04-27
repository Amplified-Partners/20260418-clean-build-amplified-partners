/**
 * Send Invoice Job
 * Generates PDF (if needed) and sends invoice email to customer
 */
import { task, logger } from "@trigger.dev/sdk/v3";
import { PrismaClient } from "@prisma/client";
import { Resend } from "resend";
import { render } from "@react-email/render";
import React from "react";
import { generateInvoicePdf } from "./generate-invoice-pdf";
import { InvoiceEmail } from "./lib/email/invoice-email";

const prisma = new PrismaClient();
const resend = new Resend(process.env.RESEND_API_KEY);

// Base URLs for invoice viewing
const APP_URL = process.env.NEXT_PUBLIC_APP_URL || "https://app.covered.ai";

interface SendInvoiceInput {
  invoiceId: string;
  regeneratePdf?: boolean;
}

export const sendInvoice = task({
  id: "send-invoice",
  run: async (payload: SendInvoiceInput) => {
    const { invoiceId, regeneratePdf = false } = payload;

    logger.info("Starting send invoice job", { invoiceId });

    // Fetch invoice with client data
    const invoice = await prisma.invoice.findUnique({
      where: { id: invoiceId },
      include: {
        client: true,
      },
    });

    if (!invoice) {
      throw new Error(`Invoice ${invoiceId} not found`);
    }

    if (invoice.status === "PAID") {
      logger.info("Invoice already paid, skipping send", { invoiceId });
      return {
        success: false,
        reason: "Invoice already paid",
      };
    }

    if (!invoice.customerEmail) {
      throw new Error(`Invoice ${invoiceId} has no customer email`);
    }

    // Step 1: Generate PDF if not exists
    logger.info("Ensuring PDF exists", { invoiceId });

    const pdfResult = await generateInvoicePdf.triggerAndWait({
      invoiceId,
      regenerate: regeneratePdf,
    });

    if (!pdfResult.ok) {
      throw new Error(`Failed to generate PDF: ${pdfResult.error}`);
    }

    const { pdfUrl, viewToken } = pdfResult.output;

    // Step 2: Build email data
    const viewUrl = `${APP_URL}/invoices/view/${viewToken}`;
    const paymentUrl = invoice.paymentLinkUrl || undefined;

    // Format amount as currency
    const formattedAmount = `£${Number(invoice.amount).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",")}`;

    // Format due date
    const dueDate = invoice.dueDate.toLocaleDateString("en-GB", {
      day: "numeric",
      month: "long",
      year: "numeric",
    });

    logger.info("Rendering email template", {
      customerName: invoice.customerName,
      invoiceNumber: invoice.invoiceNumber,
    });

    // Step 3: Render email HTML
    const emailHtml = await render(
      React.createElement(InvoiceEmail, {
        businessName: invoice.client.businessName,
        businessLogoUrl: invoice.client.logoUrl || undefined,
        customerName: invoice.customerName,
        invoiceNumber: invoice.invoiceNumber,
        amount: formattedAmount,
        dueDate,
        paymentUrl,
        viewUrl,
        pdfUrl,
      })
    );

    // Step 4: Send email via Resend
    logger.info("Sending email via Resend", {
      to: invoice.customerEmail,
      from: invoice.client.email,
    });

    const fromEmail = invoice.client.email || "invoices@covered.ai";
    const fromName = invoice.client.businessName;

    const emailResult = await resend.emails.send({
      from: `${fromName} <${fromEmail}>`,
      to: invoice.customerEmail,
      subject: `Invoice ${invoice.invoiceNumber} from ${invoice.client.businessName}`,
      html: emailHtml,
      // Attach PDF
      attachments: pdfUrl ? [
        {
          filename: `${invoice.invoiceNumber}.pdf`,
          path: pdfUrl,
        },
      ] : undefined,
      // Reply-to the business
      replyTo: invoice.client.email,
      // Headers for better deliverability
      headers: {
        "X-Entity-Ref-ID": invoice.id,
      },
    });

    if (emailResult.error) {
      logger.error("Failed to send email", {
        error: emailResult.error,
        invoiceId,
      });
      throw new Error(`Failed to send email: ${emailResult.error.message}`);
    }

    // Step 5: Update invoice status
    await prisma.invoice.update({
      where: { id: invoiceId },
      data: {
        status: "SENT",
        sentAt: new Date(),
      },
    });

    // Step 6: Log the notification
    await prisma.notification.create({
      data: {
        clientId: invoice.clientId,
        type: "invoice_sent",
        channel: "email",
        recipient: invoice.customerEmail,
        subject: `Invoice ${invoice.invoiceNumber}`,
        message: `Invoice for ${formattedAmount} sent to ${invoice.customerName}`,
        status: "sent",
        sentAt: new Date(),
        externalId: emailResult.data?.id,
      },
    });

    // Step 7: Log autonomous action
    await prisma.autonomousAction.create({
      data: {
        clientId: invoice.clientId,
        actionType: "INVOICE_SENT",
        description: `Sent invoice ${invoice.invoiceNumber} (${formattedAmount}) to ${invoice.customerName}`,
        triggerId: invoice.id,
        triggerType: "invoice",
        triggerReason: "Invoice ready to send",
        decision: "send_invoice",
        confidence: 1.0,
        outcome: "SUCCESS",
        outcomeDetails: `Email delivered to ${invoice.customerEmail}`,
        outcomeAt: new Date(),
      },
    });

    logger.info("Invoice sent successfully", {
      invoiceId,
      invoiceNumber: invoice.invoiceNumber,
      emailId: emailResult.data?.id,
    });

    return {
      success: true,
      invoiceNumber: invoice.invoiceNumber,
      emailId: emailResult.data?.id,
      sentTo: invoice.customerEmail,
      pdfUrl,
      viewUrl,
    };
  },
});

export type { SendInvoiceInput };
