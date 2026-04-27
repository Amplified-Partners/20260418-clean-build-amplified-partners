/**
 * Covered AI - PostgreSQL MCP Server
 *
 * MCP server providing database access tools for Claude.
 * Tools: query_leads, create_lead, update_lead, get_dashboard_stats, etc.
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

import * as tools from "./tools";

const server = new Server(
  {
    name: "covered-ai-postgres",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "query_leads",
        description: "Query leads for a client with optional filters",
        inputSchema: {
          type: "object",
          properties: {
            clientId: { type: "string", description: "Client UUID" },
            status: {
              type: "string",
              enum: [
                "new",
                "contacted",
                "nurturing",
                "qualified",
                "booked",
                "converted",
                "dismissed",
                "lost",
              ],
              description: "Filter by lead status",
            },
            urgency: {
              type: "string",
              enum: ["emergency", "urgent", "routine"],
              description: "Filter by urgency level",
            },
            limit: { type: "number", description: "Max results (default 50)" },
            offset: { type: "number", description: "Pagination offset" },
          },
          required: ["clientId"],
        },
      },
      {
        name: "get_lead",
        description: "Get a single lead by ID with full details",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string", description: "Lead UUID" },
          },
          required: ["id"],
        },
      },
      {
        name: "create_lead",
        description: "Create a new lead from a phone call",
        inputSchema: {
          type: "object",
          properties: {
            clientId: { type: "string", description: "Client UUID" },
            callerPhone: { type: "string", description: "Caller phone number" },
            callId: { type: "string", description: "Vapi call ID" },
            callDuration: { type: "number", description: "Call duration in seconds" },
            recordingUrl: { type: "string", description: "Call recording URL" },
            transcript: { type: "string", description: "Call transcript" },
            summary: { type: "string", description: "AI-generated call summary" },
            customerName: { type: "string", description: "Customer name extracted from call" },
            address: { type: "string", description: "Service address" },
            postcode: { type: "string", description: "UK postcode" },
            jobType: { type: "string", description: "Type of job requested" },
            urgency: {
              type: "string",
              enum: ["emergency", "urgent", "routine"],
              description: "Job urgency level",
            },
          },
          required: ["clientId", "callerPhone"],
        },
      },
      {
        name: "update_lead",
        description: "Update lead status",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string", description: "Lead UUID" },
            status: {
              type: "string",
              enum: [
                "new",
                "contacted",
                "nurturing",
                "qualified",
                "booked",
                "converted",
                "dismissed",
                "lost",
              ],
              description: "New status",
            },
            dismissReason: { type: "string", description: "Reason for dismissal" },
          },
          required: ["id"],
        },
      },
      {
        name: "find_or_create_customer",
        description: "Find existing customer by phone or create new one",
        inputSchema: {
          type: "object",
          properties: {
            clientId: { type: "string", description: "Client UUID" },
            name: { type: "string", description: "Customer name" },
            phone: { type: "string", description: "Customer phone" },
            email: { type: "string", description: "Customer email" },
            address: { type: "string", description: "Customer address" },
            postcode: { type: "string", description: "UK postcode" },
          },
          required: ["clientId", "name", "phone"],
        },
      },
      {
        name: "create_job",
        description: "Create a new job from a lead",
        inputSchema: {
          type: "object",
          properties: {
            clientId: { type: "string", description: "Client UUID" },
            customerId: { type: "string", description: "Customer UUID" },
            leadId: { type: "string", description: "Lead UUID (optional)" },
            title: { type: "string", description: "Job title" },
            description: { type: "string", description: "Job description" },
            jobType: { type: "string", description: "Type of job" },
            address: { type: "string", description: "Job address" },
            postcode: { type: "string", description: "UK postcode" },
            scheduledDate: { type: "string", description: "ISO date string" },
            scheduledTime: { type: "string", description: "Time slot (e.g., '09:00-12:00')" },
            estimatedDuration: { type: "number", description: "Duration in minutes" },
            quotedAmount: { type: "number", description: "Quoted price" },
          },
          required: ["clientId", "customerId", "title", "address", "scheduledDate"],
        },
      },
      {
        name: "update_job",
        description: "Update job status",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string", description: "Job UUID" },
            status: {
              type: "string",
              enum: ["scheduled", "confirmed", "in_progress", "completed", "cancelled", "no_show"],
              description: "New status",
            },
            finalAmount: { type: "number", description: "Final price" },
          },
          required: ["id"],
        },
      },
      {
        name: "get_job",
        description: "Get a single job by ID with full details",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string", description: "Job UUID" },
          },
          required: ["id"],
        },
      },
      {
        name: "create_nurture_sequence",
        description: "Start a nurture sequence for a lead",
        inputSchema: {
          type: "object",
          properties: {
            leadId: { type: "string", description: "Lead UUID" },
          },
          required: ["leadId"],
        },
      },
      {
        name: "update_nurture_progress",
        description: "Record a nurture touch as sent",
        inputSchema: {
          type: "object",
          properties: {
            leadId: { type: "string", description: "Lead UUID" },
            touchNumber: { type: "number", description: "Touch number (1-12)" },
          },
          required: ["leadId", "touchNumber"],
        },
      },
      {
        name: "stop_nurture_sequence",
        description: "Stop a nurture sequence (e.g., when lead books)",
        inputSchema: {
          type: "object",
          properties: {
            leadId: { type: "string", description: "Lead UUID" },
            reason: { type: "string", description: "Reason for stopping" },
          },
          required: ["leadId", "reason"],
        },
      },
      {
        name: "get_dashboard_stats",
        description: "Get dashboard statistics for a client",
        inputSchema: {
          type: "object",
          properties: {
            clientId: { type: "string", description: "Client UUID" },
          },
          required: ["clientId"],
        },
      },
      {
        name: "get_client",
        description: "Get client details by ID",
        inputSchema: {
          type: "object",
          properties: {
            clientId: { type: "string", description: "Client UUID" },
          },
          required: ["clientId"],
        },
      },
      {
        name: "get_client_by_phone",
        description: "Get client by their Covered phone number",
        inputSchema: {
          type: "object",
          properties: {
            coveredNumber: { type: "string", description: "Covered phone number" },
          },
          required: ["coveredNumber"],
        },
      },
      {
        name: "create_notification",
        description: "Log a notification in the audit trail",
        inputSchema: {
          type: "object",
          properties: {
            clientId: { type: "string", description: "Client UUID" },
            leadId: { type: "string", description: "Lead UUID (optional)" },
            jobId: { type: "string", description: "Job UUID (optional)" },
            type: { type: "string", description: "Notification type" },
            channel: { type: "string", enum: ["email", "sms", "whatsapp"] },
            recipient: { type: "string", description: "Recipient phone/email" },
            subject: { type: "string", description: "Subject (for emails)" },
            message: { type: "string", description: "Message content" },
            externalId: { type: "string", description: "External message ID" },
          },
          required: ["clientId", "type", "channel", "recipient", "message"],
        },
      },
      {
        name: "update_notification_status",
        description: "Update notification delivery status",
        inputSchema: {
          type: "object",
          properties: {
            id: { type: "string", description: "Notification UUID" },
            status: { type: "string", enum: ["sent", "delivered", "failed"] },
            error: { type: "string", description: "Error message if failed" },
          },
          required: ["id", "status"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result: any;

    switch (name) {
      case "query_leads":
        result = await tools.queryLeads(args as tools.QueryLeadsParams);
        break;

      case "get_lead":
        result = await tools.getLead(args.id as string);
        break;

      case "create_lead":
        result = await tools.createLead(args as tools.CreateLeadParams);
        break;

      case "update_lead":
        result = await tools.updateLead(args as tools.UpdateLeadParams);
        break;

      case "find_or_create_customer":
        result = await tools.findOrCreateCustomer(args as tools.CreateCustomerParams);
        break;

      case "create_job":
        result = await tools.createJob({
          ...args,
          scheduledDate: new Date(args.scheduledDate as string),
        } as tools.CreateJobParams);
        break;

      case "update_job":
        result = await tools.updateJob(args as tools.UpdateJobParams);
        break;

      case "get_job":
        result = await tools.getJob(args.id as string);
        break;

      case "create_nurture_sequence":
        result = await tools.createNurtureSequence(
          args as tools.CreateNurtureSequenceParams
        );
        break;

      case "update_nurture_progress":
        result = await tools.updateNurtureProgress(
          args as tools.UpdateNurtureProgressParams
        );
        break;

      case "stop_nurture_sequence":
        result = await tools.stopNurtureSequence(
          args.leadId as string,
          args.reason as string
        );
        break;

      case "get_dashboard_stats":
        result = await tools.getDashboardStats(args.clientId as string);
        break;

      case "get_client":
        result = await tools.getClient(args.clientId as string);
        break;

      case "get_client_by_phone":
        result = await tools.getClientByPhone(args.coveredNumber as string);
        break;

      case "create_notification":
        result = await tools.createNotification(args as any);
        break;

      case "update_notification_status":
        result = await tools.updateNotificationStatus(
          args.id as string,
          args.status as "sent" | "delivered" | "failed",
          args.error as string | undefined
        );
        break;

      default:
        throw new Error(`Unknown tool: ${name}`);
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ error: message }),
        },
      ],
      isError: true,
    };
  }
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Covered AI PostgreSQL MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});

// Cleanup on exit
process.on("SIGINT", async () => {
  await tools.disconnect();
  process.exit(0);
});

process.on("SIGTERM", async () => {
  await tools.disconnect();
  process.exit(0);
});
