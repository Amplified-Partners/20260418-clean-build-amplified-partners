import { task, logger } from "@trigger.dev/sdk/v3";
import { Resend } from "resend";
import { render } from "@react-email/components";
import { PrismaClient } from "@prisma/client";
import { InvoiceReminder1Email } from "./lib/email/invoice-reminder-1";
import { InvoiceReminder2Email } from "./lib/email/invoice-reminder-2";
import { InvoiceReminderFinalEmail } from "./lib/email/invoice-reminder-final";

const prisma = new PrismaClient();

export interface SendInvoiceReminderInput {
  invoiceId: string;
  reminderType: 1 | 2 | "final";
}

export const sendInvoiceReminder = task({
  id: "send-invoice-reminder",
  run: async (payload: SendInvoiceReminderInput) => {
    const { invoiceId, reminderType } = payload;

    logger.info("Starting invoice reminder send", { invoiceId, reminderType });

    // Fetch invoice with client
    const invoice = await prisma.invoice.findUnique({
      where: { id: invoiceId },
      include: { client: true },
    });

    if (!invoice) {
      throw new Error(`Invoice not found: ${invoiceId}`);
    }

    if (invoice.status === "PAID") {
      logger.info("Invoice already paid, skipping reminder", { invoiceId });
      return { success: true, skipped: true, reason: "already_paid" };
    }

    if (invoice.status === "CANCELLED" || invoice.status === "WRITTEN_OFF") {
      logger.info("Invoice cancelled/written off, skipping reminder", { invoiceId });
      return { success: true, skipped: true, reason: "cancelled" };
    }

    // Check if reminder already sent
    if (
      (reminderType === 1 && invoice.reminder1SentAt) ||
      (reminderType === 2 && invoice.reminder2SentAt) ||
      (reminderType === "final" && invoice.finalNoticeSentAt)
    ) {
      logger.info("Reminder already sent, skipping", { invoiceId, reminderType });
      return { success: true, skipped: true, reason: "already_sent" };
    }

    const client = invoice.client;

    // Calculate days past due
    const now = new Date();
    const dueDate = new Date(invoice.dueDate);
    const daysPastDue = Math.floor((now.getTime() - dueDate.getTime()) / (1000 * 60 * 60 * 24));

    // Prepare email data
    const emailData = {
      businessName: client.businessName,
      businessLogoUrl: client.logoUrl,
      customerName: invoice.customerName,
      invoiceNumber: invoice.invoiceNumber,
      amountDue: `£${Number(invoice.amount).toFixed(2)}`,
      dueDate: dueDate.toLocaleDateString("en-GB", {
        day: "numeric",
        month: "long",
        year: "numeric",
      }),
      daysPastDue,
      paymentLinkUrl: invoice.paymentLinkUrl,
      viewInvoiceUrl: `${process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"}/invoices/view/${invoice.viewToken}`,
    };

    // Render appropriate email template
    let emailHtml: string;
    let subject: string;

    switch (reminderType) {
      case 1:
        emailHtml = await render(InvoiceReminder1Email(emailData));
        subject = `Friendly reminder: Invoice ${invoice.invoiceNumber} is overdue`;
        break;
      case 2:
        emailHtml = await render(InvoiceReminder2Email(emailData));
        subject = `Important: Invoice ${invoice.invoiceNumber} - payment required`;
        break;
      case "final":
        emailHtml = await render(InvoiceReminderFinalEmail(emailData));
        subject = `FINAL NOTICE: Invoice ${invoice.invoiceNumber} - immediate payment required`;
        break;
    }

    // Send email via Resend
    const resend = new Resend(process.env.RESEND_API_KEY);

    try {
      const { data, error } = await resend.emails.send({
        from: `${client.businessName} <invoices@covered.ai>`,
        to: invoice.customerEmail,
        subject,
        html: emailHtml,
      });

      if (error) {
        logger.error("Failed to send reminder email", { error });
        throw new Error(`Resend error: ${error.message}`);
      }

      logger.info("Reminder email sent successfully", {
        messageId: data?.id,
        reminderType,
      });

      // Update invoice with reminder sent timestamp
      const updateData: Record<string, Date> = {};
      if (reminderType === 1) updateData.reminder1SentAt = now;
      else if (reminderType === 2) updateData.reminder2SentAt = now;
      else updateData.finalNoticeSentAt = now;

      await prisma.invoice.update({
        where: { id: invoiceId },
        data: {
          ...updateData,
          status: "REMINDED",
        },
      });

      // Log notification
      await prisma.notification.create({
        data: {
          clientId: invoice.clientId,
          type: `invoice_reminder_${reminderType}`,
          channel: "email",
          recipient: invoice.customerEmail,
          subject,
          message: `Payment reminder sent for invoice ${invoice.invoiceNumber}`,
          status: "sent",
          sentAt: now,
        },
      });

      // Log autonomous action
      const reminderLabel = reminderType === "final" ? "final notice" : `reminder ${reminderType}`;
      await prisma.autonomousAction.create({
        data: {
          clientId: invoice.clientId,
          actionType: "PAYMENT_REMINDER",
          description: `Auto-chase ${reminderLabel} sent for invoice ${invoice.invoiceNumber} (${daysPastDue} days overdue)`,
          triggerId: invoiceId,
          triggerType: "auto_chase",
          triggerReason: `Invoice ${daysPastDue} days past due`,
          decision: `send_reminder_${reminderType}`,
          confidence: 1.0,
          outcome: "SUCCESS",
          outcomeDetails: `Email sent to ${invoice.customerEmail}`,
          outcomeAt: now,
        },
      });

      return {
        success: true,
        invoiceId,
        reminderType,
        daysPastDue,
        emailId: data?.id,
      };
    } catch (err) {
      logger.error("Failed to send invoice reminder", { error: err });
      throw err;
    } finally {
      await prisma.$disconnect();
    }
  },
});
