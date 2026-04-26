# Cove Orchestrator — Makefile
# One command to rule them all.

.PHONY: help setup up down logs db-migrate test lint clean

COMPOSE = docker compose -f docker/docker-compose.yml

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ─── Setup ───────────────────────────────────────────────────────────
setup: ## First-time setup: copy env, install deps, start everything
	@echo "🔧 Setting up Cove Orchestrator..."
	@test -f .env || cp .env.example .env && echo "  ✓ .env created (edit with your keys)"
	pip install -r requirements.txt
	@echo "  ✓ Python deps installed"
	$(COMPOSE) pull
	@echo "  ✓ Docker images pulled"
	$(COMPOSE) up -d postgres
	@echo "  ⏳ Waiting for PostgreSQL..."
	@sleep 5
	$(MAKE) db-migrate
	$(COMPOSE) up -d
	@echo "✅ Cove is running!"
	@echo "   Temporal UI: http://localhost:8080"
	@echo "   LiteLLM:     http://localhost:4000"
	@echo "   Langfuse:    http://localhost:3000"

# ─── Docker ──────────────────────────────────────────────────────────
up: ## Start all services
	$(COMPOSE) up -d

down: ## Stop all services
	$(COMPOSE) down

logs: ## Tail all logs
	$(COMPOSE) logs -f

logs-worker: ## Tail worker logs only
	$(COMPOSE) logs -f temporal-worker

rebuild: ## Rebuild and restart worker
	$(COMPOSE) build temporal-worker
	$(COMPOSE) up -d temporal-worker

# ─── Database ────────────────────────────────────────────────────────
db-migrate: ## Run database migrations
	@echo "📦 Running migrations..."
	@for f in db/migrations/*.sql; do \
		echo "  → $$f"; \
		PGPASSWORD=$${POSTGRES_PASSWORD:-cove_dev_2026} psql -h localhost -U cove -d cove -f $$f; \
	done
	@echo "✅ Migrations complete"

db-shell: ## Open psql shell
	PGPASSWORD=$${POSTGRES_PASSWORD:-cove_dev_2026} psql -h localhost -U cove -d cove

db-reset: ## Drop and recreate database (DESTRUCTIVE)
	@echo "⚠️  This will DELETE all data. Ctrl+C to abort."
	@sleep 3
	$(COMPOSE) exec postgres dropdb -U cove cove --if-exists
	$(COMPOSE) exec postgres createdb -U cove cove
	$(MAKE) db-migrate

# ─── Testing ─────────────────────────────────────────────────────────
test: ## Run all tests
	python -m pytest tests/ -v

lint: ## Run linter + formatter
	ruff check --fix .
	ruff format .

typecheck: ## Run mypy
	mypy --strict temporal/ agents/ mcp-servers/

# ─── MCP Servers ─────────────────────────────────────────────────────
mcp-telegram: ## Start Telegram MCP server (stdio)
	python -m mcp_servers.telegram_mcp.server

mcp-postgresql: ## Start PostgreSQL MCP server (stdio)
	python -m mcp_servers.postgresql_mcp.server

mcp-inspect-telegram: ## Inspect Telegram MCP with MCP Inspector
	npx @modelcontextprotocol/inspector python -m mcp_servers.telegram_mcp.server

mcp-nightscout: ## Start NightScout MCP server (stdio)
	python -m mcp_servers.nightscout_mcp.server

mcp-litellm: ## Start LiteLLM MCP server (stdio)
	python -m mcp_servers.litellm_mcp.server

mcp-langfuse: ## Start Langfuse MCP server (stdio)
	python -m mcp_servers.langfuse_mcp.server

mcp-github: ## Start GitHub MCP server (stdio)
	python -m mcp_servers.github_mcp.server

mcp-filesystem: ## Start Filesystem MCP server (stdio)
	python -m mcp_servers.filesystem_mcp.server

mcp-email: ## Start Email MCP server (stdio)
	python -m mcp_servers.email_mcp.server

mcp-linear: ## Start official Linear MCP server via npx (stdio)
	npx -y @modelcontextprotocol/server-linear

mcp-slack: ## Start official Slack MCP server via npx (stdio)
	npx -y @modelcontextprotocol/server-slack

# ─── NightScout ───────────────────────────────────────────────────────
nightscout-run: ## Run NightScout pipeline (one-shot)
	python -m nightscout run

nightscout-briefing: ## Generate morning briefing
	python -m nightscout briefing

nightscout-logs: ## Tail NightScout container logs
	$(COMPOSE) logs -f nightscout

nightscout-rebuild: ## Rebuild and restart NightScout
	$(COMPOSE) build nightscout nightscout-mcp
	$(COMPOSE) up -d nightscout nightscout-mcp

# ─── Cleanup ─────────────────────────────────────────────────────────
clean: ## Remove build artifacts and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
