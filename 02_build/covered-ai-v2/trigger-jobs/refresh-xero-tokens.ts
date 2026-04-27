/**
 * Xero Token Refresh Job
 * Runs hourly to refresh Xero access tokens before they expire
 */
import { schedules, task } from "@trigger.dev/sdk/v3";
import { PrismaClient } from "@prisma/client";
import { decrypt, encrypt } from "./lib/encryption";

const prisma = new PrismaClient();

const XERO_TOKEN_URL = "https://identity.xero.com/connect/token";

/**
 * Scheduled job to check and refresh expiring Xero tokens
 * Runs every hour at minute 30
 */
export const refreshXeroTokens = schedules.task({
  id: "refresh-xero-tokens",
  cron: "30 * * * *", // Every hour at :30
  run: async () => {
    console.log("Checking for Xero tokens that need refresh...");

    // Get all connections with tokens expiring in next 10 minutes
    const tenMinutesFromNow = new Date(Date.now() + 10 * 60 * 1000);

    const expiringConnections = await prisma.xeroConnection.findMany({
      where: {
        connected: true,
        tokenExpiresAt: {
          lte: tenMinutesFromNow,
        },
      },
    });

    console.log(`Found ${expiringConnections.length} tokens to refresh`);

    const results = {
      total: expiringConnections.length,
      refreshed: 0,
      failed: 0,
      errors: [] as string[],
    };

    for (const connection of expiringConnections) {
      try {
        await refreshSingleToken.trigger({
          connectionId: connection.id,
          clientId: connection.clientId,
        });
        results.refreshed++;
      } catch (error) {
        results.failed++;
        results.errors.push(
          `${connection.clientId}: ${error instanceof Error ? error.message : "Unknown error"}`
        );
      }
    }

    console.log(
      `Token refresh complete: ${results.refreshed} refreshed, ${results.failed} failed`
    );

    return results;
  },
});

/**
 * Task to refresh a single Xero token
 */
export const refreshSingleToken = task({
  id: "refresh-single-xero-token",
  run: async (payload: { connectionId: string; clientId: string }) => {
    const { connectionId, clientId } = payload;

    console.log(`Refreshing Xero token for client ${clientId}`);

    const connection = await prisma.xeroConnection.findUnique({
      where: { id: connectionId },
    });

    if (!connection || !connection.refreshToken) {
      throw new Error("Connection not found or missing refresh token");
    }

    const xeroClientId = process.env.XERO_CLIENT_ID;
    const xeroClientSecret = process.env.XERO_CLIENT_SECRET;

    if (!xeroClientId || !xeroClientSecret) {
      throw new Error("Xero credentials not configured");
    }

    // Decrypt the refresh token
    const refreshToken = decrypt(connection.refreshToken);

    // Request new tokens
    const authHeader = Buffer.from(
      `${xeroClientId}:${xeroClientSecret}`
    ).toString("base64");

    const response = await fetch(XERO_TOKEN_URL, {
      method: "POST",
      headers: {
        Authorization: `Basic ${authHeader}`,
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        grant_type: "refresh_token",
        refresh_token: refreshToken,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Token refresh failed for ${clientId}: ${errorText}`);

      // Mark connection as disconnected if refresh fails
      await prisma.xeroConnection.update({
        where: { id: connectionId },
        data: {
          connected: false,
          lastSyncError: `Token refresh failed: ${errorText.slice(0, 200)}`,
        },
      });

      throw new Error(`Token refresh failed: ${response.status}`);
    }

    const tokens = await response.json();

    // Calculate new expiry (usually 30 minutes from now)
    const expiresIn = tokens.expires_in || 1800;
    const tokenExpiresAt = new Date(Date.now() + expiresIn * 1000);

    // Update connection with new tokens
    await prisma.xeroConnection.update({
      where: { id: connectionId },
      data: {
        accessToken: encrypt(tokens.access_token),
        refreshToken: encrypt(tokens.refresh_token),
        tokenExpiresAt,
        lastSyncError: null,
      },
    });

    console.log(
      `Token refreshed successfully for ${clientId}, expires at ${tokenExpiresAt.toISOString()}`
    );

    return {
      clientId,
      tokenExpiresAt: tokenExpiresAt.toISOString(),
    };
  },
});

/**
 * Manual token refresh trigger
 * Can be called when a sync fails due to expired token
 */
export const manualTokenRefresh = task({
  id: "manual-xero-token-refresh",
  run: async (payload: { clientId: string }) => {
    const { clientId } = payload;

    const connection = await prisma.xeroConnection.findUnique({
      where: { clientId },
    });

    if (!connection) {
      throw new Error(`No Xero connection found for client ${clientId}`);
    }

    return refreshSingleToken.triggerAndWait({
      connectionId: connection.id,
      clientId,
    });
  },
});
