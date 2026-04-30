-- Migration 003: Email Agent Schema
-- Phase 3: Communication Layer — IMAP triage, draft generation, auto-handle

-- ─── Enums ─────────────────────────────────────────────────────────────
CREATE TYPE email_priority AS ENUM ('critical', 'urgent', 'normal', 'low');
CREATE TYPE email_action AS ENUM ('respond', 'delegate', 'archive', 'defer', 'escalate');
CREATE TYPE draft_status AS ENUM ('pending_review', 'approved', 'sent', 'rejected');

-- ─── Email Accounts (multi-account support) ─────────────────────────
CREATE TABLE email_accounts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email_address   TEXT NOT NULL UNIQUE,
    display_name    TEXT NOT NULL,
    imap_host       TEXT NOT NULL DEFAULT 'imap.gmail.com',
    imap_port       INT NOT NULL DEFAULT 993,
    smtp_host       TEXT NOT NULL DEFAULT 'smtp.gmail.com',
    smtp_port       INT NOT NULL DEFAULT 587,
    -- OAuth2 tokens stored encrypted; app password as fallback
    auth_method     TEXT NOT NULL DEFAULT 'oauth2' CHECK (auth_method IN ('oauth2', 'app_password')),
    enabled         BOOLEAN NOT NULL DEFAULT true,
    last_sync_at    TIMESTAMPTZ,
    last_sync_uid   BIGINT,  -- IMAP UID watermark for incremental fetch
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── Inbound Emails ─────────────────────────────────────────────────
CREATE TABLE emails_inbound (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id      UUID NOT NULL REFERENCES email_accounts(id),
    message_id      TEXT NOT NULL,          -- RFC 2822 Message-ID
    imap_uid        BIGINT NOT NULL,
    from_address    TEXT NOT NULL,
    from_name       TEXT,
    to_addresses    TEXT[] NOT NULL DEFAULT '{}',
    cc_addresses    TEXT[] NOT NULL DEFAULT '{}',
    subject         TEXT NOT NULL DEFAULT '',
    body_text       TEXT,                    -- plain text body
    body_html       TEXT,                    -- HTML body (stored, not processed)
    received_at     TIMESTAMPTZ NOT NULL,
    fetched_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    thread_id       TEXT,                    -- Gmail thread ID if available
    has_attachments BOOLEAN NOT NULL DEFAULT false,
    attachment_names TEXT[] NOT NULL DEFAULT '{}',
    raw_headers     JSONB,                   -- selected headers for analysis
    -- Triage results
    priority        email_priority,
    action          email_action,
    confidence      NUMERIC(3,2),            -- 0.00 - 1.00
    triage_reasoning TEXT,
    triaged_at      TIMESTAMPTZ,
    triaged_model   TEXT,
    -- Sender context
    sender_domain   TEXT GENERATED ALWAYS AS (
        split_part(from_address, '@', 2)
    ) STORED,
    is_known_contact BOOLEAN NOT NULL DEFAULT false,
    contact_context  TEXT,                    -- enriched from Graphiti
    -- State
    handled         BOOLEAN NOT NULL DEFAULT false,
    handled_at      TIMESTAMPTZ,
    handled_action  TEXT,                     -- what was actually done
    -- Dedup
    UNIQUE (account_id, message_id)
);

CREATE INDEX idx_emails_inbound_priority ON emails_inbound(priority) WHERE NOT handled;
CREATE INDEX idx_emails_inbound_action ON emails_inbound(action) WHERE NOT handled;
CREATE INDEX idx_emails_inbound_received ON emails_inbound(received_at DESC);
CREATE INDEX idx_emails_inbound_sender ON emails_inbound(sender_domain);
CREATE INDEX idx_emails_inbound_thread ON emails_inbound(thread_id) WHERE thread_id IS NOT NULL;

-- ─── Draft Responses ────────────────────────────────────────────────
CREATE TABLE email_drafts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    inbound_id      UUID NOT NULL REFERENCES emails_inbound(id) ON DELETE CASCADE,
    account_id      UUID NOT NULL REFERENCES email_accounts(id),
    to_addresses    TEXT[] NOT NULL,
    cc_addresses    TEXT[] NOT NULL DEFAULT '{}',
    subject         TEXT NOT NULL,
    body_text       TEXT NOT NULL,
    body_html       TEXT,
    tone            TEXT NOT NULL DEFAULT 'professional',
    draft_model     TEXT NOT NULL,
    status          draft_status NOT NULL DEFAULT 'pending_review',
    review_notes    TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    reviewed_at     TIMESTAMPTZ,
    sent_at         TIMESTAMPTZ
);

CREATE INDEX idx_email_drafts_status ON email_drafts(status) WHERE status = 'pending_review';

-- ─── Triage Rules (learnable) ───────────────────────────────────────
CREATE TABLE email_triage_rules (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    rule_name       TEXT NOT NULL,
    description     TEXT,
    -- Match criteria (any combination)
    match_sender    TEXT,                     -- regex or domain
    match_subject   TEXT,                     -- regex
    match_body      TEXT,                     -- keyword
    -- Assigned result
    assign_priority email_priority,
    assign_action   email_action,
    -- Auto-handle (skip LLM triage)
    auto_handle     BOOLEAN NOT NULL DEFAULT false,
    auto_label      TEXT,                     -- Gmail label to apply
    enabled         BOOLEAN NOT NULL DEFAULT true,
    hit_count       INT NOT NULL DEFAULT 0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ─── Pipeline Runs ──────────────────────────────────────────────────
CREATE TABLE email_pipeline_runs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id      UUID NOT NULL REFERENCES email_accounts(id),
    started_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    completed_at    TIMESTAMPTZ,
    emails_fetched  INT NOT NULL DEFAULT 0,
    emails_triaged  INT NOT NULL DEFAULT 0,
    drafts_created  INT NOT NULL DEFAULT 0,
    auto_handled    INT NOT NULL DEFAULT 0,
    errors          JSONB NOT NULL DEFAULT '[]'
);
