import { schedules, logger } from "@trigger.dev/sdk/v3";
import { PrismaClient } from "@prisma/client";
import { sendInvoiceReminder } from "./send-invoice-reminder";

const prisma = new PrismaClient();

export const checkOverdueInvoices = schedules.task({
  id: "check-overdue-invoices",
  // Run daily at 9am UTC
  cron: "0 9 * * *",
  run: async () => {
    logger.info("Starting daily overdue invoice check");

    const now = new Date();
    const results = {
      processed: 0,
      markedOverdue: 0,
      reminder1Sent: 0,
      reminder2Sent: 0,
      finalNoticeSent: 0,
      errors: [] as string[],
    };

    try {
      // Find all invoices that are sent/reminded but past due date
      const overdueInvoices = await prisma.invoice.findMany({
        where: {
          status: { in: ["SENT", "REMINDED", "OVERDUE"] },
          dueDate: { lt: now },
        },
        include: {
          client: {
            select: {
              id: true,
              businessName: true,
              autoChaseEnabled: true,
              reminder1Days: true,
              reminder2Days: true,
              reminder3Days: true,
            },
          },
        },
      });

      logger.info(`Found ${overdueInvoices.length} overdue invoices`);

      for (const invoice of overdueInvoices) {
        results.processed++;

        try {
          // Calculate days past due
          const dueDate = new Date(invoice.dueDate);
          const daysPastDue = Math.floor(
            (now.getTime() - dueDate.getTime()) / (1000 * 60 * 60 * 24)
          );

          // Mark as OVERDUE if not already
          if (invoice.status !== "OVERDUE") {
            await prisma.invoice.update({
              where: { id: invoice.id },
              data: { status: "OVERDUE" },
            });
            results.markedOverdue++;
            logger.info(`Marked invoice ${invoice.invoiceNumber} as OVERDUE`, {
              daysPastDue,
            });
          }

          // Skip auto-chase if disabled for this client
          if (!invoice.client.autoChaseEnabled) {
            logger.info(
              `Auto-chase disabled for client ${invoice.client.businessName}, skipping reminders`
            );
            continue;
          }

          // Determine which reminder to send based on client settings
          const client = invoice.client;

          // Final notice (reminder 3)
          if (
            daysPastDue >= client.reminder3Days &&
            !invoice.finalNoticeSentAt
          ) {
            logger.info(
              `Triggering final notice for invoice ${invoice.invoiceNumber}`,
              { daysPastDue, threshold: client.reminder3Days }
            );

            await sendInvoiceReminder.trigger({
              invoiceId: invoice.id,
              reminderType: "final",
            });
            results.finalNoticeSent++;
          }
          // Reminder 2
          else if (
            daysPastDue >= client.reminder2Days &&
            !invoice.reminder2SentAt
          ) {
            logger.info(
              `Triggering reminder 2 for invoice ${invoice.invoiceNumber}`,
              { daysPastDue, threshold: client.reminder2Days }
            );

            await sendInvoiceReminder.trigger({
              invoiceId: invoice.id,
              reminderType: 2,
            });
            results.reminder2Sent++;
          }
          // Reminder 1
          else if (
            daysPastDue >= client.reminder1Days &&
            !invoice.reminder1SentAt
          ) {
            logger.info(
              `Triggering reminder 1 for invoice ${invoice.invoiceNumber}`,
              { daysPastDue, threshold: client.reminder1Days }
            );

            await sendInvoiceReminder.trigger({
              invoiceId: invoice.id,
              reminderType: 1,
            });
            results.reminder1Sent++;
          }
        } catch (err) {
          const errorMsg = `Error processing invoice ${invoice.invoiceNumber}: ${err}`;
          logger.error(errorMsg);
          results.errors.push(errorMsg);
        }
      }

      logger.info("Daily overdue invoice check completed", results);

      return results;
    } catch (err) {
      logger.error("Failed to complete overdue invoice check", { error: err });
      throw err;
    } finally {
      await prisma.$disconnect();
    }
  },
});
