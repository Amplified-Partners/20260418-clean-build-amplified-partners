-- Cove Orchestrator — Initial Schema (COV-266)
-- Run order: 001 (no dependencies)
-- This is the foundation everything else builds on.

-- ─── Extensions ─────────────────────────────────────────────────────────────
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ─── Enums ──────────────────────────────────────────────────────────────────
CREATE TYPE agent_role AS ENUM ('coder', 'security', 'enforcer', 'architect', 'reviewer');
CREATE TYPE task_status AS ENUM ('pending', 'queued', 'running', 'awaiting_approval', 'approved', 'rejected', 'completed', 'failed', 'cancelled');
CREATE TYPE approval_tier AS ENUM ('auto', 'lint_only', 'agent_review', 'human_review', 'ewan_review', 'ewan_only');
CREATE TYPE approval_decision AS ENUM ('approved', 'rejected', 'commented', 'timeout');
CREATE TYPE model_tier AS ENUM ('cheap', 'medium', 'premium');

-- ─── Projects ───────────────────────────────────────────────────────────────
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    repo_url TEXT,
    default_branch TEXT DEFAULT 'main',
    description TEXT,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Build Tasks ────────────────────────────────────────────────────────────
-- Each task = one unit of work assigned to one agent
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
    linear_issue_id TEXT,                    -- e.g., COV-266
    title TEXT NOT NULL,
    description TEXT,
    status task_status DEFAULT 'pending',
    assigned_agent agent_role,
    model_tier model_tier DEFAULT 'medium',
    priority INT DEFAULT 3 CHECK (priority BETWEEN 1 AND 5),

    -- Git context
    branch_name TEXT,                        -- agent/coder/COV-266
    worktree_path TEXT,

    -- Temporal context
    workflow_id TEXT,
    workflow_run_id TEXT,

    -- Dependencies
    depends_on UUID[],                       -- Task IDs this depends on

    -- Results
    result JSONB,
    error_message TEXT,
    retry_count INT DEFAULT 0,
    max_retries INT DEFAULT 3,

    -- Timing
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_linear ON tasks(linear_issue_id);

-- ─── Approval Requests ──────────────────────────────────────────────────────
CREATE TABLE approvals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES tasks(id) ON DELETE CASCADE,
    tier approval_tier NOT NULL,

    -- What needs approval
    title TEXT NOT NULL,
    description TEXT,
    diff_summary TEXT,                       -- Git diff summary
    files_changed TEXT[],

    -- Telegram integration
    telegram_message_id BIGINT,
    telegram_chat_id TEXT,

    -- Decision
    decision approval_decision,
    decided_by TEXT,                          -- Username or agent ID
    decision_comment TEXT,
    decided_at TIMESTAMPTZ,

    -- Timeout
    timeout_minutes INT DEFAULT 60,
    expires_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_approvals_task ON approvals(task_id);
CREATE INDEX idx_approvals_pending ON approvals(decision) WHERE decision IS NULL;

-- ─── Agent Runs ─────────────────────────────────────────────────────────────
-- Every time an agent executes, log it here
CREATE TABLE agent_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL,
    agent_role agent_role NOT NULL,
    model_tier model_tier NOT NULL,
    model_name TEXT,                         -- Actual model used (e.g., claude-sonnet-4-20250514)

    -- LLM usage
    input_tokens INT DEFAULT 0,
    output_tokens INT DEFAULT 0,
    total_tokens INT DEFAULT 0,
    cost_usd NUMERIC(10, 6) DEFAULT 0,

    -- Langfuse trace
    langfuse_trace_id TEXT,

    -- Timing
    duration_ms INT,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,

    -- Result
    success BOOLEAN,
    error_message TEXT,
    tool_calls_count INT DEFAULT 0
);

CREATE INDEX idx_agent_runs_task ON agent_runs(task_id);
CREATE INDEX idx_agent_runs_date ON agent_runs(started_at);

-- ─── Budget Tracking ────────────────────────────────────────────────────────
CREATE TABLE budget_daily (
    date DATE PRIMARY KEY DEFAULT CURRENT_DATE,
    total_cost_usd NUMERIC(10, 4) DEFAULT 0,
    total_tokens BIGINT DEFAULT 0,
    run_count INT DEFAULT 0,
    breakdown_by_tier JSONB DEFAULT '{}',    -- {"cheap": 0.01, "medium": 0.50, "premium": 2.00}
    breakdown_by_agent JSONB DEFAULT '{}'    -- {"coder": 1.50, "security": 0.80}
);

-- ─── MCP Server Registry ───────────────────────────────────────────────────
-- Track which MCP servers are available and their health
CREATE TABLE mcp_servers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT UNIQUE NOT NULL,               -- e.g., telegram_mcp
    transport TEXT DEFAULT 'stdio',          -- stdio or http
    command TEXT,                             -- For stdio: python path
    url TEXT,                                -- For http: endpoint URL
    enabled BOOLEAN DEFAULT TRUE,
    health_status TEXT DEFAULT 'unknown',
    last_health_check TIMESTAMPTZ,
    config JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ─── Audit Log ──────────────────────────────────────────────────────────────
-- Everything that happens, for radical transparency
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    actor TEXT NOT NULL,                     -- Agent role, user email, or 'system'
    action TEXT NOT NULL,                    -- e.g., 'task.created', 'approval.approved'
    resource_type TEXT,                      -- e.g., 'task', 'approval', 'agent_run'
    resource_id TEXT,
    details JSONB DEFAULT '{}',
    task_id UUID REFERENCES tasks(id) ON DELETE SET NULL
);

CREATE INDEX idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_task ON audit_log(task_id);
CREATE INDEX idx_audit_action ON audit_log(action);

-- ─── Helper Functions ───────────────────────────────────────────────────────

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Auto-log to audit_log on task status change
CREATE OR REPLACE FUNCTION log_task_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO audit_log (actor, action, resource_type, resource_id, details, task_id)
        VALUES (
            COALESCE(NEW.assigned_agent::TEXT, 'system'),
            'task.status_changed',
            'task',
            NEW.id::TEXT,
            jsonb_build_object('from', OLD.status, 'to', NEW.status),
            NEW.id
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tasks_status_audit AFTER UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION log_task_status_change();
