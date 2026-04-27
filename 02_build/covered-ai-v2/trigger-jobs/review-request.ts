/**
 * Covered AI - Review Request Job
 *
 * Triggered when a job is marked as completed.
 * Waits 2 hours, then sends a review request email.
 */

import { task, wait } from "@trigger.dev/sdk/v3";
import { ActionLog } from "./lib/action-logger";

interface Job {
  id: string;
  clientId: string;
  customerId: string;
  title: string;
  jobType?: string;
  completedAt: string;
}

interface Customer {
  id: string;
  name: string;
  email?: string;
  phone: string;
}

interface Client {
  id: string;
  businessName: string;
  googlePlaceId?: string;
}

const REVIEW_DELAY_HOURS = 2;

export const reviewRequestJob = task({
  id: "review-request",
  retry: {
    maxAttempts: 2,
  },
  run: async (payload: { job: Job; customer: Customer; client: Client }) => {
    const { job, customer, client } = payload;
    
    console.log(`⭐ Review request scheduled for job ${job.id}`);
    
    // Wait 2 hours after job completion
    console.log(`⏳ Waiting ${REVIEW_DELAY_HOURS} hours before sending`);
    await wait.for({ hours: REVIEW_DELAY_HOURS });
    
    // Check if client has Google Place ID
    if (!client.googlePlaceId) {
      console.log(`⚠️ No Google Place ID for client ${client.id}, skipping review request`);
      return { sent: false, reason: "no_place_id" };
    }
    
    // Check if customer has email
    if (!customer.email) {
      console.log(`⚠️ No email for customer ${customer.id}, skipping review request`);
      return { sent: false, reason: "no_email" };
    }
    
    // Generate review link
    const reviewLink = `https://search.google.com/local/writereview?placeid=${client.googlePlaceId}`;
    
    // Log autonomous action
    const action = await ActionLog.reviewRequestSent(
      client.id,
      job.id,
      customer.name
    );

    // Send review request email
    console.log(`📧 Sending review request to ${customer.email}`);

    const RESEND_API_KEY = process.env.RESEND_API_KEY;
    const API_URL = process.env.API_URL || "http://localhost:8000";

    if (!RESEND_API_KEY) {
      await action.fail("RESEND_API_KEY not configured");
      return { sent: false, reason: "no_api_key" };
    }

    try {
      const html = generateReviewRequestHtml(customer.name, client.businessName, job.title, reviewLink);

      // Send email via Resend
      const response = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${RESEND_API_KEY}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          from: `${client.businessName} <noreply@covered.ai>`,
          to: customer.email,
          subject: `How was your experience with ${client.businessName}?`,
          html,
        }),
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(`Resend error: ${error}`);
      }

      // Update job record
      await fetch(`${API_URL}/api/v1/clients/${job.clientId}/jobs/${job.id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          reviewRequested: true,
          reviewRequestedAt: new Date().toISOString(),
        }),
      });

      await action.success(`Review request sent to ${customer.email}`);
      console.log(`✅ Review request sent for job ${job.id}`);
      return { sent: true, to: customer.email, reviewLink };
    } catch (error) {
      await action.fail(String(error));
      console.error(`❌ Failed to send review request:`, error);
      throw error;
    }
  },
});

function generateReviewRequestHtml(
  customerName: string,
  businessName: string,
  jobTitle: string,
  reviewLink: string
): string {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  <div style="text-align: center; margin-bottom: 30px;">
    <span style="font-size: 36px; color: #fbbf24;">&#9733;&#9733;&#9733;&#9733;&#9733;</span>
  </div>

  <h1 style="color: #1a1a1a; font-size: 24px; text-align: center; margin-bottom: 10px;">How did we do?</h1>
  <p style="color: #666; text-align: center; margin-bottom: 30px;">Your feedback helps us improve</p>

  <p>Hi ${customerName},</p>

  <p>Thank you for choosing ${businessName} for your recent ${jobTitle}.</p>

  <p>We'd really appreciate it if you could take a moment to share your experience. Your review helps other customers and helps us continue to provide excellent service.</p>

  <div style="text-align: center; margin: 30px 0;">
    <a href="${reviewLink}" style="display: inline-block; background: #0891b2; color: #fff; padding: 16px 48px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 18px;">Leave a Review</a>
    <p style="color: #999; font-size: 13px; margin-top: 12px;">Takes less than 2 minutes</p>
  </div>

  <p style="color: #666; font-size: 14px;">Had an issue? We'd love the chance to make it right. Just reply to this email.</p>

  <p style="margin-top: 30px;">
    Thank you for your support,<br>
    <strong>The ${businessName} Team</strong>
  </p>
</body>
</html>
  `.trim();
}
