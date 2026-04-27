/**
 * Weekly Summary Job
 * Sends weekly email summaries to business owners every Monday at 8am
 */
import { schedules } from "@trigger.dev/sdk/v3";
import { PrismaClient } from "@prisma/client";
import { Resend } from "resend";
import { WeeklySummaryEmail } from "../emails/weekly-summary";

const prisma = new PrismaClient();
const resend = new Resend(process.env.RESEND_API_KEY);

interface WeeklyStats {
  callsHandled: number;
  jobsCompleted: number;
  revenueCollected: number;
  newCustomers: number;
  reviewsReceived: number;
}

function generateInsight(stats: WeeklyStats): string {
  if (stats.callsHandled > 50) {
    return "Busy week! Gemma handled a high volume of calls for you.";
  }
  if (stats.revenueCollected > 5000) {
    return "Great revenue week! Your cash flow is looking healthy.";
  }
  if (stats.reviewsReceived >= 3) {
    return "Nice work on the reviews! Social proof builds trust.";
  }
  if (stats.newCustomers >= 5) {
    return "Strong customer acquisition this week. Keep it up!";
  }
  return "Steady week. Small consistent progress adds up!";
}

function formatDate(date: Date): string {
  return date.toLocaleDateString("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export const generateWeeklySummary = schedules.task({
  id: "generate-weekly-summary",
  cron: "0 8 * * 1", // Monday 8am
  run: async () => {
    const now = new Date();
    const weekStart = new Date(now);
    weekStart.setDate(weekStart.getDate() - 7);

    const clients = await prisma.client.findMany({
      where: {
        subscriptionStatus: "active",
      },
    });

    let sent = 0;

    for (const client of clients) {
      // Check if notification email is set
      const email = client.notificationEmail || client.email;
      if (!email) continue;

      // Gather stats
      const [calls, jobs, invoices, customers, reviews] = await Promise.all([
        prisma.call.count({
          where: { clientId: client.id, createdAt: { gte: weekStart } },
        }),
        prisma.job.count({
          where: {
            clientId: client.id,
            status: "completed",
            completedAt: { gte: weekStart },
          },
        }),
        prisma.invoice.aggregate({
          where: {
            clientId: client.id,
            status: "paid",
            paidAt: { gte: weekStart },
          },
          _sum: { totalAmount: true },
        }),
        prisma.customer.count({
          where: { clientId: client.id, createdAt: { gte: weekStart } },
        }),
        prisma.review.count({
          where: {
            clientId: client.id,
            createdAt: { gte: weekStart },
          },
        }),
      ]);

      const stats: WeeklyStats = {
        callsHandled: calls,
        jobsCompleted: jobs,
        revenueCollected: invoices._sum.totalAmount || 0,
        newCustomers: customers,
        reviewsReceived: reviews,
      };

      // Generate insight
      const insight = generateInsight(stats);

      try {
        await resend.emails.send({
          from: "Gemma <gemma@covered.ai>",
          to: email,
          subject: `Your week with Covered AI`,
          react: WeeklySummaryEmail({
            businessName: client.businessName,
            ownerName: client.ownerName || "there",
            weekEnding: formatDate(now),
            stats,
            insight,
            dashboardLink: `${process.env.APP_URL || "https://app.covered.ai"}/dashboard`,
          }),
        });

        sent++;
      } catch (error) {
        console.error(`Failed to send weekly summary to ${email}:`, error);
      }
    }

    return { sent };
  },
});
