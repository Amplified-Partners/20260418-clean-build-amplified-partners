/**
 * Covered AI - Twilio MCP Server
 *
 * MCP server providing SMS and WhatsApp messaging tools.
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
    name: "covered-ai-twilio",
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
        name: "send_sms",
        description: "Send an SMS message to a phone number",
        inputSchema: {
          type: "object",
          properties: {
            to: {
              type: "string",
              description: "Recipient phone number (UK format accepted)",
            },
            message: {
              type: "string",
              description: "SMS message content (max 1600 chars for concatenated SMS)",
            },
            from: {
              type: "string",
              description: "Sender phone number (optional, uses default)",
            },
          },
          required: ["to", "message"],
        },
      },
      {
        name: "send_whatsapp",
        description: "Send a WhatsApp message to a phone number",
        inputSchema: {
          type: "object",
          properties: {
            to: {
              type: "string",
              description: "Recipient phone number (UK format accepted)",
            },
            message: {
              type: "string",
              description: "WhatsApp message content",
            },
            mediaUrl: {
              type: "string",
              description: "URL of media to attach (image, video, etc.)",
            },
          },
          required: ["to", "message"],
        },
      },
      {
        name: "get_calls",
        description: "Get recent call records",
        inputSchema: {
          type: "object",
          properties: {
            phoneNumber: {
              type: "string",
              description: "Filter by phone number",
            },
            limit: {
              type: "number",
              description: "Max number of records (default 20)",
            },
            startDate: {
              type: "string",
              description: "Filter by start date (ISO format)",
            },
            endDate: {
              type: "string",
              description: "Filter by end date (ISO format)",
            },
          },
        },
      },
      {
        name: "get_messages",
        description: "Get recent SMS/WhatsApp message records",
        inputSchema: {
          type: "object",
          properties: {
            to: {
              type: "string",
              description: "Filter by recipient phone number",
            },
            from: {
              type: "string",
              description: "Filter by sender phone number",
            },
            limit: {
              type: "number",
              description: "Max number of records (default 20)",
            },
            dateSent: {
              type: "string",
              description: "Filter by date sent (ISO format)",
            },
          },
        },
      },
      {
        name: "get_message_status",
        description: "Get delivery status of a specific message",
        inputSchema: {
          type: "object",
          properties: {
            sid: {
              type: "string",
              description: "Twilio message SID",
            },
          },
          required: ["sid"],
        },
      },
      {
        name: "lookup_phone_number",
        description: "Look up information about a phone number",
        inputSchema: {
          type: "object",
          properties: {
            phone: {
              type: "string",
              description: "Phone number to look up",
            },
          },
          required: ["phone"],
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
      case "send_sms":
        result = await tools.sendSms(args as tools.SendSmsParams);
        break;

      case "send_whatsapp":
        result = await tools.sendWhatsApp(args as tools.SendWhatsAppParams);
        break;

      case "get_calls":
        result = await tools.getCalls(args as tools.GetCallsParams);
        break;

      case "get_messages":
        result = await tools.getMessages(args as tools.GetMessagesParams);
        break;

      case "get_message_status":
        result = await tools.getMessageStatus(args.sid as string);
        break;

      case "lookup_phone_number":
        result = await tools.lookupPhoneNumber(args.phone as string);
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
  console.error("Covered AI Twilio MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
