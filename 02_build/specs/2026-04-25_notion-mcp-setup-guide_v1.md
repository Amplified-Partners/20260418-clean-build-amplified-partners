---
title: "Notion MCP Server Setup Guide"
id: "notion-mcp-setup-guide"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "setup-guide"
audience: "internal"
layer: "build"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Notion MCP Server Setup Guide

## Step 1: Create a Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click **"+ New integration"**
3. Fill in the details:
   - **Name**: Kilo Code MCP
   - **Associated workspace**: Select your workspace
   - **Logo**: (optional)
4. Click **"Submit"**
5. Copy the **"Internal Integration Token"** (starts with `secret_`)
   - ⚠️ Keep this token secure - don't commit it to git

## Step 2: Share Pages/Databases with Integration

The integration needs explicit access to pages/databases:

1. Open any Notion page or database you want to access via MCP
2. Click **"..."** menu (top right)
3. Scroll to **"Connections"**
4. Click **"Add connections"**
5. Select **"Kilo Code MCP"**
6. Click **"Confirm"**

Repeat for all pages/databases you want to access.

## Step 3: Configure MCP Server

Your Notion API token will be stored in `.kilocode/mcp.json` (this file is git-ignored).

The configuration looks like:
```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-notion"
      ],
      "env": {
        "NOTION_API_KEY": "your-token-here"
      }
    }
  }
}
```

## Step 4: Test the Connection

After configuration and restart, you can test with commands like:
- Search your workspace
- Query databases
- Read page content
- Create new pages

## Security Notes

- The API token is stored locally in `.kilocode/mcp.json`
- This file should be in `.gitignore`
- The token only has access to pages/databases you explicitly share
- You can revoke the integration anytime at https://www.notion.so/my-integrations