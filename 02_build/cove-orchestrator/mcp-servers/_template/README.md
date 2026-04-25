# FastMCP Server Template

## Quick Start

```bash
# 1. Copy template
cp -r _template/ myservice-mcp/

# 2. Edit server.py
#    - Change SERVICE_NAME
#    - Set API_BASE_URL / API_KEY env var names
#    - Replace example tools with real ones
#    - Add Pydantic input models per tool

# 3. Install deps
pip install "mcp[cli]" httpx pydantic

# 4. Test
python -m myservice_mcp.server

# 5. Test with MCP Inspector
npx @modelcontextprotocol/inspector python -m myservice_mcp.server
```

## Pattern Checklist

- [ ] SERVICE_NAME set (lowercase, no hyphens)
- [ ] All tools prefixed with `{service}_`
- [ ] Every tool has Pydantic input model
- [ ] Every tool has annotations (readOnlyHint, destructiveHint, etc.)
- [ ] Both JSON and Markdown response formats supported
- [ ] Pagination on any list endpoint
- [ ] Actionable error messages (not just stack traces)
- [ ] API key from env var (never hardcoded)
- [ ] Shared httpx.AsyncClient (not new client per request)
