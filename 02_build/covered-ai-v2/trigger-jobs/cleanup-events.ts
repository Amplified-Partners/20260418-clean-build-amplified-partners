import { schedules } from "@trigger.dev/sdk/v3";

/**
 * Cleanup Old Events
 *
 * Runs daily at 3am to delete events older than 30 days.
 * This keeps the event log from growing indefinitely while
 * maintaining enough history for debugging.
 */
export const cleanupOldEvents = schedules.task({
  id: "cleanup-old-events",
  cron: "0 3 * * *", // Daily at 3am
  run: async () => {
    const apiUrl = process.env.API_URL || "http://localhost:8000";

    console.log("Starting event cleanup...");

    try {
      const response = await fetch(
        `${apiUrl}/api/v1/events/cleanup?days=30`,
        { method: "POST" }
      );

      if (!response.ok) {
        const error = await response.text();
        console.error(`Cleanup failed: ${response.status} - ${error}`);
        return {
          success: false,
          error: `HTTP ${response.status}: ${error}`,
        };
      }

      const result = await response.json();
      console.log(`Cleanup complete: ${result.message}`);

      return {
        success: true,
        deleted: result.message,
        days: result.days,
      };
    } catch (error) {
      console.error("Event cleanup error:", error);
      return {
        success: false,
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  },
});
