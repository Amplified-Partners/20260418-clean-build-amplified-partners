# `mcp-servers.json` — what it is and who reads it

<!-- markdownlint-disable-file MD013 -->

This repo carries a root-level `mcp-servers.json` so the AI agents working in
`clean-build` from the **operator's local IDEs** (not Devin) can attach to the
[GitKraken MCP Server][gk-mcp].

## Who consumes this file

Agents that read repo-level MCP config in this exact shape:

- **Cursor** — File → Manual JSON config (`mcp-servers.json` at the workspace
  root works as a project-scoped MCP source). See GitKraken Cursor setup.
- **Claude Desktop** — pasted into `claude_desktop_config.json` (same JSON
  shape). Copy from this file.
- **Claude Code** — `claude mcp add -t stdio gitkraken gk mcp` (resolves to
  the same config).
- **Google Antigravity / VS Code / Codex / Gemini / Windsurf / Trae / Zed /
  JetBrains AI Assistant / Kiro / Amazon Q Developer** — same JSON, fed in
  via each tool's MCP setup flow.

Reference: <https://help.gitkraken.com/mcp/mcp-getting-started/> (March 2026).

## Who does *not* consume it — Devin

Devin agents do **not** pick up MCP servers from a repo file. Devin's runtime
injects MCP servers from **org-level marketplace settings** at session start.
GitKraken is currently not in Devin's MCP marketplace, and GitKraken's own
`gk mcp install` does not list Devin as a supported target. Devin will
continue using its builtin git tools (`git`, `git_pr`, `git_comment`) for all
commits and pushes from this workspace.

If GitKraken capability inside Devin is wanted later, the path is: Cognition
adds the GitKraken MCP to Devin's marketplace, then an org admin enables it in
Devin org settings. That is an external request to Cognition, not a repo edit.

## Prerequisites for the agents that *do* consume it

1. Install the GitKraken CLI (`gk`):
   - macOS: `brew install gitkraken-cli`
   - Linux / WSL: see <https://github.com/gitkraken/gk-cli#installation>
   - npm fallback: `npm install -g @gitkraken/gk`
2. Authenticate once:

   ```bash
   gk auth login
   ```

3. Confirm the binary resolves on `PATH`:

   ```bash
   gk --version
   ```

After that, an agent loading `mcp-servers.json` will spawn `gk mcp` over stdio
and have access to the GitKraken MCP toolset (Git ops, GitHub / GitLab / Jira
/ Azure DevOps integration, PR + issue automation).

## npx fallback (only if `gk` is not on `PATH`)

If a target environment cannot install `gk` globally, swap the entry for:

```json
{
  "mcpServers": {
    "gitkraken": {
      "command": "npx",
      "args": ["-y", "@gitkraken/gk", "mcp"]
    }
  }
}
```

This uses the npm-published [`@gitkraken/gk`][gk-npm] binary. Untested by us;
GitKraken's official docs use the global `gk` form, so prefer that when
possible.

## Verification

Once installed, ask the agent (in agent / chat mode):

> What issues are assigned to me?

A working install shows a tool-approval request for `issues_assigned_to_me`
or similar. Tool list inspection (e.g. Cursor's MCP settings, Claude Code
`/mcp`) should show `gitkraken` connected.

## Why root-level

GitKraken's docs assume a single MCP config per agent / IDE. Putting the
canonical entry at the repo root means any agent attached to this workspace
gets the same Git mechanics surface, without each agent maintaining its own
private copy. Keeping it small (one server, no fluff) honours
[`00_authority/USE_IT_OR_CUT_IT.md`](./00_authority/USE_IT_OR_CUT_IT.md) — if
no agent ends up using GitKraken in practice, this file is removed in a
follow-up.

## Status

- **Authority class:** none. This is a tooling config, not a policy artefact.
  Not indexed in `00_authority/MANIFEST.md` per its scoping rules.
- **Reversibility:** trivially reversible — delete the file and the JSON, the
  agents fall back to builtin git tooling.

## References

- [`mcp-servers.json`](./mcp-servers.json) — the live config (this file's
  sibling).
- AMP-22 (parent context, GitKraken's role in the GitHub interface):
  <https://linear.app/amplifiedpartners/issue/AMP-22>
- AMP-23 (this implementation):
  <https://linear.app/amplifiedpartners/issue/AMP-23>
- GitKraken MCP getting started: <https://help.gitkraken.com/mcp/mcp-getting-started/>
- GitKraken CLI repo: <https://github.com/gitkraken/gk-cli>

[gk-mcp]: https://help.gitkraken.com/mcp/mcp-getting-started/
[gk-npm]: https://www.npmjs.com/package/@gitkraken/gk

---

Authored by,

**Devon**
Devin session `1fa14abfb7f9437b8b10af9fca30a355`
2026-05-04
