import { schedules, task } from "@trigger.dev/sdk/v3";

const API_URL = process.env.API_URL || "http://localhost:8000";

/**
 * Process Client Check-ins
 *
 * Runs daily at 9am to find clients who need a check-in
 * and sends them appropriate emails based on their signup date.
 */
export const processClientCheckins = schedules.task({
  id: "process-client-checkins",
  cron: "0 9 * * *", // Daily at 9am
  run: async () => {
    console.log("Processing client check-ins...");

    try {
      // Fetch clients due for check-in
      const response = await fetch(
        `${API_URL}/api/v1/clients?needs_checkin=true`
      );

      if (!response.ok) {
        console.error("Failed to fetch clients:", response.status);
        return { processed: 0, error: `HTTP ${response.status}` };
      }

      const data = await response.json();
      const clients = data.clients || [];

      console.log(`Found ${clients.length} clients due for check-in`);

      let processed = 0;

      for (const client of clients) {
        try {
          // Calculate days since signup
          const signupDate = new Date(client.createdAt);
          const now = new Date();
          const daysSinceSignup = Math.floor(
            (now.getTime() - signupDate.getTime()) / (1000 * 60 * 60 * 24)
          );

          // Trigger appropriate check-in based on days
          await sendClientCheckin.trigger({
            clientId: client.id,
            daysSinceSignup,
            clientEmail: client.email,
            businessName: client.businessName,
            ownerName: client.ownerName,
          });

          processed++;
        } catch (err) {
          console.error(`Error processing client ${client.id}:`, err);
        }
      }

      return { processed, total: clients.length };
    } catch (error) {
      console.error("Check-in processing error:", error);
      return {
        processed: 0,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  },
});

/**
 * Send Client Check-in
 *
 * Individual task to send a check-in email to a specific client.
 * Triggered by the scheduled task or manually.
 */
export const sendClientCheckin = task({
  id: "send-client-checkin",
  run: async (payload: {
    clientId: string;
    daysSinceSignup: number;
    clientEmail: string;
    businessName: string;
    ownerName: string;
  }) => {
    const { clientId, daysSinceSignup, clientEmail, businessName, ownerName } =
      payload;

    console.log(
      `Sending check-in for client ${clientId} (day ${daysSinceSignup})`
    );

    // Determine which email to send based on days since signup
    let emailType: "day3" | "day7" | "day14" | "day30" | null = null;

    if (daysSinceSignup === 3) {
      emailType = "day3";
    } else if (daysSinceSignup === 7) {
      emailType = "day7";
    } else if (daysSinceSignup === 14) {
      emailType = "day14";
    } else if (daysSinceSignup === 30) {
      emailType = "day30";
    }

    if (!emailType) {
      console.log(`No check-in email for day ${daysSinceSignup}`);
      return { sent: false, reason: "not a check-in day" };
    }

    // Get email content
    const emailContent = getCheckinEmailContent(
      emailType,
      ownerName,
      businessName
    );

    // Send email via API
    try {
      const response = await fetch(`${API_URL}/api/v1/emails/send`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          to: clientEmail,
          subject: emailContent.subject,
          html: emailContent.html,
          template: `checkin_${emailType}`,
          client_id: clientId,
        }),
      });

      if (!response.ok) {
        console.error("Failed to send check-in email:", response.status);
        return { sent: false, error: `HTTP ${response.status}` };
      }

      // Update next check-in date
      await updateNextCheckin(clientId, daysSinceSignup);

      return {
        sent: true,
        clientId,
        emailType,
        daysSinceSignup,
      };
    } catch (error) {
      console.error("Error sending check-in email:", error);
      return {
        sent: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  },
});

/**
 * Get check-in email content based on type
 */
function getCheckinEmailContent(
  type: "day3" | "day7" | "day14" | "day30",
  ownerName: string,
  businessName: string
): { subject: string; html: string } {
  const firstName = ownerName.split(" ")[0] || ownerName;

  const emails = {
    day3: {
      subject: `How are the first few days going, ${firstName}?`,
      html: `
        <html>
        <body style="font-family: sans-serif; line-height: 1.6; color: #333;">
          <p>Hi ${firstName},</p>

          <p>It's been 3 days since Gemma started answering calls for ${businessName}. How's it going so far?</p>

          <p>I just wanted to check in and see if:</p>
          <ul>
            <li>Gemma is answering calls correctly</li>
            <li>You're receiving the lead notifications</li>
            <li>There's anything you'd like to adjust</li>
          </ul>

          <p>If everything's working well, great! If you have any questions or feedback, just reply to this email.</p>

          <p>Ewan<br>Covered AI</p>
        </body>
        </html>
      `,
    },
    day7: {
      subject: `Week 1 complete! How many calls has Gemma handled?`,
      html: `
        <html>
        <body style="font-family: sans-serif; line-height: 1.6; color: #333;">
          <p>Hi ${firstName},</p>

          <p>Congratulations on your first week with Covered AI!</p>

          <p>I'd love to hear how it's going. Some things to check:</p>
          <ul>
            <li>Have you seen leads come through your dashboard?</li>
            <li>Are the call summaries helpful?</li>
            <li>Has Gemma saved you time?</li>
          </ul>

          <p><strong>Quick tip:</strong> You can listen to call recordings and read transcripts in your dashboard - great for seeing exactly what Gemma is saying to your customers.</p>

          <p>
            <a href="https://app.covered.ai/dashboard"
               style="display: inline-block; background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px;">
              View Your Dashboard
            </a>
          </p>

          <p>Ewan<br>Covered AI</p>
        </body>
        </html>
      `,
    },
    day14: {
      subject: `2 weeks in - quick question for you`,
      html: `
        <html>
        <body style="font-family: sans-serif; line-height: 1.6; color: #333;">
          <p>Hi ${firstName},</p>

          <p>You've been using Covered AI for 2 weeks now. I hope Gemma has been helpful!</p>

          <p>I have one quick question: <strong>What's the biggest benefit you've noticed so far?</strong></p>

          <p>Is it:</p>
          <ul>
            <li>Never missing a call</li>
            <li>More time to focus on jobs</li>
            <li>Better lead capture</li>
            <li>Something else?</li>
          </ul>

          <p>Just reply to this email - I read every response and your feedback helps us improve.</p>

          <p>Ewan<br>Covered AI</p>
        </body>
        </html>
      `,
    },
    day30: {
      subject: `Your first month with Gemma - let's chat`,
      html: `
        <html>
        <body style="font-family: sans-serif; line-height: 1.6; color: #333;">
          <p>Hi ${firstName},</p>

          <p>It's been a month since ${businessName} started using Covered AI. Time flies!</p>

          <p>I'd love to hear how things are going and if there's anything we can do better.</p>

          <p>Would you be up for a quick 10-minute call? I'll share some tips for getting even more value from Gemma, and you can ask any questions you have.</p>

          <p>
            <a href="https://calendly.com/covered-ai/checkin"
               style="display: inline-block; background: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 6px;">
              Book a Quick Call
            </a>
          </p>

          <p>Or just reply to this email if you prefer.</p>

          <p>Ewan<br>Covered AI</p>
        </body>
        </html>
      `,
    },
  };

  return emails[type];
}

/**
 * Update the next check-in date for a client
 */
async function updateNextCheckin(
  clientId: string,
  currentDay: number
): Promise<void> {
  // Determine next check-in day
  let nextCheckinDays: number;

  if (currentDay < 7) {
    nextCheckinDays = 7 - currentDay;
  } else if (currentDay < 14) {
    nextCheckinDays = 14 - currentDay;
  } else if (currentDay < 30) {
    nextCheckinDays = 30 - currentDay;
  } else {
    // No more scheduled check-ins after day 30
    nextCheckinDays = 0;
  }

  if (nextCheckinDays > 0) {
    const nextCheckin = new Date();
    nextCheckin.setDate(nextCheckin.getDate() + nextCheckinDays);

    await fetch(`${API_URL}/api/v1/clients/${clientId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nextCheckinAt: nextCheckin.toISOString(),
        lastCheckinAt: new Date().toISOString(),
      }),
    });
  }
}
