---
title: "so github mcp"
id: "perplexity-github-mcp-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "perplexity-session"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# so github mcp

GitHub MCP is exactly what you want if the goal is “let Kilo see and operate on all my GitHub repos like a power user,” rather than just cloning them locally.[^1][^2]

## What “GitHub MCP” Actually Is

- MCP = **Model Context Protocol**: a standard that lets an AI agent talk to external tools/services in a structured way.[^3]
- **GitHub MCP server** is GitHub’s official MCP endpoint that exposes tools for:
    - Reading repos and files.
    - Managing issues and pull requests.
    - Creating branches, commits, etc.[^4][^2]
- Kilo Code is an MCP host: it can connect to any MCP server, including GitHub’s.[^5][^3]

So instead of just “seeing” code, Kilo gets a whole toolbelt for working inside GitHub.

## What You Gain By Wiring It Up

Once configured in Kilo:

- You can ask Kilo things like:
    - “Scan all my business-related repos and list where my ‘principles’ docs live.”
    - “Open PRs to add a unified `PRINCIPLES.md` to each repo.”
    - “Search across repos for references to X and summarise how I implemented it.”
- The agent can:
    - Fetch repo trees and file contents directly via MCP tools.
    - Create issues/PRs to align code and docs with your synthesized framework.[^2][^1]

This fits your plan where the synthesis produces **principles + systems**, and then Kilo pushes those into your actual codebases and docs as living artefacts.

## How to Set It Up in Kilo (High Level)

The flow is roughly:

1. **Install / point to the GitHub MCP server**
    - The official server is at `github/github-mcp-server` on GitHub.[^2]
2. **Add it to Kilo’s MCP config**
    - Open MCP settings in Kilo and edit the global or project config (`mcp_settings.json` or `.kilocode/mcp.json`).[^5]
    - Add a server entry, e.g. (pattern, not exact; follow Kilo’s UI prompts and the GitHub MCP README):
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "requestInit": {
        "headers": {
          "Authorization": "Bearer YOUR_GITHUB_PAT"
        }
      }
    }
  }
}
```

- The exact URL/auth pattern comes from the GitHub MCP docs; you’ll use a GitHub PAT or OAuth flow.[^6][^7]

3. **Authenticate**
    - In Kilo’s MCP UI you hit “Auth” or similar to log into GitHub / approve scopes.[^6][^5]
4. **Use the tools in a mode**
    - In your custom modes (e.g. the orchestrator or rubric-evaluator), allow the GitHub MCP tools.[^3][^5]
    - Then you can say: “Use the GitHub tools to list my repos matching ‘consultancy’ and pull any `principles` files into the current workspace.”

## How This Fits Your Big Plan

For the **synthesis** phase:

- Still best to pull everything you care about (from GitHub included) into a local “knowledge workspace” so Kilo can crunch it with Memory Bank and your rubric.[^8][^9]

For the **deployment** phase:

- GitHub MCP is ideal to:
    - Materialise your principles into each repo.
    - Keep your business framework in lockstep with your actual products and automations.
    - Let Kilo refactor code/processes so they reflect the final synthesis, directly via PRs.[^1][^2]

If you like, next step can be: write a concrete `mcp.json` / `mcp_settings.json` template plus a first “sync principles into repos” prompt you can drop straight into Kilo.
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17]</span>

<div align="center">⁂</div>

[^1]: https://www.youtube.com/watch?v=egXvZ7_hEAI

[^2]: https://github.com/github/github-mcp-server

[^3]: https://kilo.ai/docs/features/mcp/overview

[^4]: https://docs.github.com/copilot/customizing-copilot/using-model-context-protocol

[^5]: https://kilo.ai/docs/features/mcp/using-mcp-in-kilo-code

[^6]: https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/set-up-the-github-mcp-server

[^7]: https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/use-the-github-mcp-server

[^8]: https://kilo.ai/docs/advanced-usage/large-projects

[^9]: https://kilo.ai/docs/features/codebase-indexing

[^10]: https://github.com/Kilo-Org/kilo-dev-mcp-server

[^11]: https://github.com/Kilo-Org/kilocode

[^12]: https://github.com/Kilo-Org

[^13]: https://github.com/Kilo-Org/kilo-dev-mcp-server/pulls

[^14]: https://github.com/Kilo-Org/kilocode/issues/3555

[^15]: https://www.youtube.com/watch?v=w67eZrzrsU8\&vl=en

[^16]: https://modelcontextprotocol.io/docs/develop/build-server

[^17]: https://github.com/Kilo-Org/kilocode/issues/645

