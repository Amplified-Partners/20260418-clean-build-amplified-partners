/**
 * Covered AI - HeyGen MCP Server
 *
 * MCP server providing AI video generation tools.
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
    name: "covered-ai-heygen",
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
        name: "create_video",
        description: "Create a personalized video from a template",
        inputSchema: {
          type: "object",
          properties: {
            templateId: {
              type: "string",
              description: "HeyGen template ID",
            },
            variables: {
              type: "object",
              description: "Template variables (e.g., customer_name, business_name)",
              additionalProperties: { type: "string" },
            },
            title: {
              type: "string",
              description: "Video title for reference",
            },
            test: {
              type: "boolean",
              description: "Use test mode (watermarked, faster)",
            },
          },
          required: ["templateId", "variables"],
        },
      },
      {
        name: "get_video_status",
        description: "Get the status of a video generation request",
        inputSchema: {
          type: "object",
          properties: {
            videoId: {
              type: "string",
              description: "HeyGen video ID",
            },
          },
          required: ["videoId"],
        },
      },
      {
        name: "get_video_url",
        description: "Get the URL of a completed video",
        inputSchema: {
          type: "object",
          properties: {
            videoId: {
              type: "string",
              description: "HeyGen video ID",
            },
          },
          required: ["videoId"],
        },
      },
      {
        name: "list_templates",
        description: "List available video templates",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "get_template_details",
        description: "Get details about a specific template",
        inputSchema: {
          type: "object",
          properties: {
            templateId: {
              type: "string",
              description: "HeyGen template ID",
            },
          },
          required: ["templateId"],
        },
      },
      {
        name: "list_avatars",
        description: "List available AI avatars",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "list_voices",
        description: "List available text-to-speech voices",
        inputSchema: {
          type: "object",
          properties: {},
        },
      },
      {
        name: "create_talking_avatar_video",
        description: "Create a video with an avatar speaking custom text",
        inputSchema: {
          type: "object",
          properties: {
            avatarId: {
              type: "string",
              description: "HeyGen avatar ID",
            },
            voiceId: {
              type: "string",
              description: "HeyGen voice ID",
            },
            script: {
              type: "string",
              description: "Text for the avatar to speak",
            },
            title: {
              type: "string",
              description: "Video title for reference",
            },
            test: {
              type: "boolean",
              description: "Use test mode (watermarked, faster)",
            },
          },
          required: ["avatarId", "voiceId", "script"],
        },
      },
      {
        name: "wait_for_video",
        description: "Poll until video is complete or times out",
        inputSchema: {
          type: "object",
          properties: {
            videoId: {
              type: "string",
              description: "HeyGen video ID",
            },
            maxWaitMs: {
              type: "number",
              description: "Max wait time in milliseconds (default 180000)",
            },
          },
          required: ["videoId"],
        },
      },
      {
        name: "get_template_for_vertical",
        description: "Get the recommended template ID for a business vertical",
        inputSchema: {
          type: "object",
          properties: {
            vertical: {
              type: "string",
              enum: [
                "trades",
                "vet",
                "dental",
                "aesthetics",
                "salon",
                "physio",
                "optometry",
                "fitness",
              ],
              description: "Business vertical",
            },
          },
          required: ["vertical"],
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
      case "create_video":
        result = await tools.createVideo(args as tools.CreateVideoParams);
        break;

      case "get_video_status":
        result = await tools.getVideoStatus(args as tools.GetVideoStatusParams);
        break;

      case "get_video_url":
        result = await tools.getVideoUrl(args.videoId as string);
        break;

      case "list_templates":
        result = await tools.listTemplates();
        break;

      case "get_template_details":
        result = await tools.getTemplateDetails(args.templateId as string);
        break;

      case "list_avatars":
        result = await tools.listAvatars();
        break;

      case "list_voices":
        result = await tools.listVoices();
        break;

      case "create_talking_avatar_video":
        result = await tools.createTalkingAvatarVideo(args as any);
        break;

      case "wait_for_video":
        result = await tools.waitForVideo(
          args.videoId as string,
          args.maxWaitMs as number | undefined
        );
        break;

      case "get_template_for_vertical":
        result = {
          vertical: args.vertical,
          templateId: tools.getTemplateForVertical(args.vertical as string),
        };
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
  console.error("Covered AI HeyGen MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error:", error);
  process.exit(1);
});
