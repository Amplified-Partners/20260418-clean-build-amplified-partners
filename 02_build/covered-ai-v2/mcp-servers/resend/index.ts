/**
 * Covered AI - Resend MCP Server
 *
 * MCP server providing email tools via Resend.
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
    name: "covered-ai-resend",
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
        name: "send_email",
        description: "Send an email with custom HTML content",
        inputSchema: {
          type: "object",
          properties: {
            to: {
              oneOf: [
                { type: "string" },
                { type: "array", items: { type: "string" } },
              ],
              description: "Recipient email address(es)",
            },
            subject: {
              type: "string",
              description: "Email subject line",
            },
            html: {
              type: "string",
              description: "Email HTML content",
            },
            text: {
              type: "string",
              description: "Plain text version (optional)",
            },
            from: {
              type: "string",
              description: "Sender address (optional, uses default)",
            },
            replyTo: {
              type: "string",
              description: "Reply-to address (optional)",
            },
          },
          required: ["to", "subject", "html"],
        },
      },
      {
        name: "send_template",
        description: "Send an email using a pre-defined template",
        inputSchema: {
          type: "object",
          properties: {
            to: {
              oneOf: [
                { type: "string" },
                { type: "array", items: { type: "string" } },
              ],
              description: "Recipient email address(es)",
            },
            template: {
              type: "string",
              enum: [
                "acknowledgment",
                "social-proof",
                "video-intro",
                "case-study",
                "faq",
                "review-request",
                "re-engage",
                "long-nurture",
              ],
              description: "Template name",
            },
            data: {
              type: "object",
              description: "Template variables",
              properties: {
                customer_name: { type: "string" },
                business_name: { type: "string" },
                owner_name: { type: "string" },
                job_type: { type: "string" },
                video_url: { type: "string" },
                thumbnail_url: { type: "string" },
                review_link: { type: "string" },
              },
            },
            from: {
              type: "string",
              description: "Sender address (optional)",
            },
            replyTo: {
              type: "string",
              description: "Reply-to address (optional)",
            },
          },
          required: ["to", "template", "data"],
        },
      },
      {
        name: "get_email_status",
        description: "Get delivery status of an email",
        inputSchema: {
          type: "object",
          properties: {
            emailId: {
              type: "string",
              description: "Resend email ID",
            },
          },
          required: ["emailId"],
        },
      },
      {
        name: "list_templates",
        description: "List available email templates",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "preview_template",
        description: "Preview a compiled template with sample data",
        inputSchema: {
          type: "object",
          properties: {
            template: {
              type: "string",
              description: "Template name",
            },
            data: {
              type: "object",
              description: "Sample data for template variables",
            },
          },
          required: ["template", "data"],
        },
      },
      {
        name: "send_batch",
        description: "Send multiple emails in batch",
        inputSchema: {
          type: "object",
          properties: {
            emails: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  to: { type: "string" },
                  subject: { type: "string" },
                  html: { type: "string" },
                  from: { type: "string" },
                },
                required: ["to", "subject", "html"],
              },
              description: "Array of emails to send",
            },
          },
          required: ["emails"],
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
      case "send_email":
        result = await tools.sendEmail(args as tools.SendEmailParams);
        break;

      case "send_template":
        result = await tools.sendTemplate(args as tools.SendTemplateParams);
        break;

      case "get_email_status":
        result = await tools.getEmailStatus(args as tools.GetEmailStatusParams);
        break;

      case "list_templates":
        result = await tools.listTemplates();
        break;

      case "preview_template":
        result = await tools.previewTemplate(
          args.template as string,
          args.data as Record<string, any>
        );
        break;

      case "send_batch":
        result = await tools.sendBatch(args.emails as any[]);
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
  console.error("Covered AI Resend MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
