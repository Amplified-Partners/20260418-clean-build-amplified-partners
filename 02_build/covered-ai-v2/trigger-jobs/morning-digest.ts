/**
 * Morning Digest Job
 * Sends daily morning digest to business owners at 7am
 */
import { schedules } from "@trigger.dev/sdk/v3";
import { PrismaClient } from "@prisma/client";
import { Resend } from "resend";

const prisma = new PrismaClient();
const resend = new Resend(process.env.RESEND_API_KEY);

function formatCurrency(amount: number): string {
  return `£${amount.toLocaleString("en-GB", { minimumFractionDigits: 0 })}`;
}

export const sendMorningDigest = schedules.task({
  id: "send-morning-digest",
  cron: "0 7 * * *", // Daily at 7am
  run: async () => {
    const now = new Date();
    const yesterday = new Date(now);
    yesterday.setDate(yesterday.getDate() - 1);
    yesterday.setHours(0, 0, 0, 0);

    const todayStart = new Date(now);
    todayStart.setHours(0, 0, 0, 0);

    const clients = await prisma.client.findMany({
      where: {
        subscriptionStatus: "active",
      },
    });

    let sent = 0;

    for (const client of clients) {
      const email = client.notificationEmail || client.email;
      if (!email) continue;

      // Get yesterday's stats
      const [
        callsYesterday,
        jobsCompletedYesterday,
        revenueYesterday,
        newLeadsYesterday,
        pendingCallbacks,
        overdueInvoices,
        jobsToday,
      ] = await Promise.all([
        // Calls yesterday
        prisma.call.count({
          where: {
            clientId: client.id,
            createdAt: {
              gte: yesterday,
              lt: todayStart,
            },
          },
        }),

        // Jobs completed yesterday
        prisma.job.count({
          where: {
            clientId: client.id,
            status: "completed",
            completedAt: {
              gte: yesterday,
              lt: todayStart,
            },
          },
        }),

        // Revenue collected yesterday
        prisma.invoice.aggregate({
          where: {
            clientId: client.id,
            status: "paid",
            paidAt: {
              gte: yesterday,
              lt: todayStart,
            },
          },
          _sum: { totalAmount: true },
        }),

        // New leads yesterday
        prisma.lead.count({
          where: {
            clientId: client.id,
            createdAt: {
              gte: yesterday,
              lt: todayStart,
            },
          },
        }),

        // Pending callbacks
        prisma.call.count({
          where: {
            clientId: client.id,
            callbackRequired: true,
            callbackCompleted: false,
          },
        }),

        // Overdue invoices
        prisma.invoice.count({
          where: {
            clientId: client.id,
            status: { in: ["sent", "overdue"] },
            dueDate: { lt: todayStart },
          },
        }),

        // Jobs scheduled today
        prisma.job.count({
          where: {
            clientId: client.id,
            status: "scheduled",
            scheduledDate: {
              gte: todayStart,
              lt: new Date(todayStart.getTime() + 24 * 60 * 60 * 1000),
            },
          },
        }),
      ]);

      // Build morning digest email
      const hasUrgentItems = pendingCallbacks > 0 || overdueInvoices > 0;

      const html = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #374151; margin: 0; padding: 0; background-color: #f6f9fc;">
  <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background-color: #0891b2; padding: 24px 32px; border-radius: 8px 8px 0 0;">
      <h1 style="color: #ffffff; margin: 0; font-size: 20px;">Good morning, ${client.ownerName || "there"}!</h1>
    </div>

    <div style="background-color: #ffffff; padding: 32px; border-radius: 0 0 8px 8px;">
      <h2 style="margin: 0 0 16px; font-size: 16px; color: #6b7280;">Yesterday's Summary</h2>

      <table style="width: 100%; border-collapse: collapse; margin-bottom: 24px;">
        <tr>
          <td style="padding: 12px; background-color: #f9fafb; border-radius: 8px; text-align: center; width: 50%;">
            <div style="font-size: 24px; font-weight: bold; color: #1f2937;">${callsYesterday}</div>
            <div style="font-size: 14px; color: #6b7280;">Calls handled</div>
          </td>
          <td style="width: 8px;"></td>
          <td style="padding: 12px; background-color: #f9fafb; border-radius: 8px; text-align: center; width: 50%;">
            <div style="font-size: 24px; font-weight: bold; color: #1f2937;">${jobsCompletedYesterday}</div>
            <div style="font-size: 14px; color: #6b7280;">Jobs completed</div>
          </td>
        </tr>
        <tr><td colspan="3" style="height: 8px;"></td></tr>
        <tr>
          <td style="padding: 12px; background-color: #f9fafb; border-radius: 8px; text-align: center; width: 50%;">
            <div style="font-size: 24px; font-weight: bold; color: #1f2937;">${formatCurrency(revenueYesterday._sum.totalAmount || 0)}</div>
            <div style="font-size: 14px; color: #6b7280;">Collected</div>
          </td>
          <td style="width: 8px;"></td>
          <td style="padding: 12px; background-color: #f9fafb; border-radius: 8px; text-align: center; width: 50%;">
            <div style="font-size: 24px; font-weight: bold; color: #1f2937;">${newLeadsYesterday}</div>
            <div style="font-size: 14px; color: #6b7280;">New leads</div>
          </td>
        </tr>
      </table>

      ${
        hasUrgentItems
          ? `
      <div style="background-color: #fef3c7; border-radius: 8px; padding: 16px; margin-bottom: 24px;">
        <h3 style="margin: 0 0 8px; font-size: 14px; color: #92400e;">⚠️ Needs your attention</h3>
        ${pendingCallbacks > 0 ? `<p style="margin: 4px 0; font-size: 14px; color: #92400e;">• ${pendingCallbacks} pending callback${pendingCallbacks > 1 ? "s" : ""}</p>` : ""}
        ${overdueInvoices > 0 ? `<p style="margin: 4px 0; font-size: 14px; color: #92400e;">• ${overdueInvoices} overdue invoice${overdueInvoices > 1 ? "s" : ""}</p>` : ""}
      </div>
      `
          : ""
      }

      ${
        jobsToday > 0
          ? `
      <div style="background-color: #dbeafe; border-radius: 8px; padding: 16px; margin-bottom: 24px;">
        <h3 style="margin: 0 0 4px; font-size: 14px; color: #1e40af;">📅 Today</h3>
        <p style="margin: 0; font-size: 14px; color: #1e40af;">${jobsToday} job${jobsToday > 1 ? "s" : ""} scheduled</p>
      </div>
      `
          : ""
      }

      <div style="text-align: center;">
        <a href="${process.env.APP_URL || "https://app.covered.ai"}/dashboard"
           style="display: inline-block; background-color: #0891b2; color: #ffffff; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-weight: 600;">
          View Dashboard
        </a>
      </div>

      <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;">

      <p style="margin: 0; font-size: 14px; color: #6b7280;">
        Have a great day,<br>
        Gemma
      </p>
    </div>
  </div>
</body>
</html>`;

      try {
        await resend.emails.send({
          from: "Gemma <gemma@covered.ai>",
          to: email,
          subject: `☀️ Good morning! Here's your ${client.businessName} update`,
          html,
        });

        sent++;
      } catch (error) {
        console.error(`Failed to send morning digest to ${email}:`, error);
      }
    }

    return { sent };
  },
});
