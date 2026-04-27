import { schedules, logger } from "@trigger.dev/sdk/v3";

const API_URL = process.env.API_URL || "https://covered-ai-production.up.railway.app";

/**
 * Process outreach email queue every hour
 * Sends up to 50 emails per run to maintain deliverability
 */
export const processOutreachQueue = schedules.task({
  id: "process-outreach-queue",
  // Run every hour
  cron: "0 * * * *",
  run: async () => {
    logger.info("Starting hourly outreach queue processing");

    try {
      const response = await fetch(
        `${API_URL}/api/v1/outreach/process-queue?limit=50`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API returned ${response.status}: ${errorText}`);
      }

      const result = await response.json();

      logger.info("Outreach queue processing completed", {
        sent: result.sent,
        message: result.message,
      });

      return {
        success: true,
        sent: result.sent,
        message: result.message,
      };
    } catch (err) {
      logger.error("Failed to process outreach queue", { error: err });
      throw err;
    }
  },
});

/**
 * Daily cleanup job for expired demo numbers
 * Runs at 3am UTC to release numbers that have passed their expiry date
 */
export const expireDemoNumbers = schedules.task({
  id: "expire-demo-numbers",
  // Run daily at 3am UTC
  cron: "0 3 * * *",
  run: async () => {
    logger.info("Starting daily demo number expiry check");

    try {
      const response = await fetch(
        `${API_URL}/api/v1/demo-numbers/expire`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`API returned ${response.status}: ${errorText}`);
      }

      const result = await response.json();

      logger.info("Demo number expiry check completed", {
        message: result.message,
      });

      return {
        success: true,
        message: result.message,
      };
    } catch (err) {
      logger.error("Failed to expire demo numbers", { error: err });
      throw err;
    }
  },
});
