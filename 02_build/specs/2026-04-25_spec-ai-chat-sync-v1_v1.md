---
title: AI Chat Sync - Product Specification
version: 1.0.0
date: 2025-12-14
status: READY TO BUILD
author: Claude + Ewan
---

# AI Chat Sync

## Overview

A local-first tool that automatically syncs conversations from multiple AI platforms into a unified knowledge pipeline. Runs on schedule, pulls new chats, outputs structured markdown for downstream processing.

---

## Problem Statement

AI conversations contain valuable thinking, decisions, and context. Currently:
- No bulk export across platforms
- Manual one-by-one export via extensions
- No automatic sync
- Knowledge trapped in silos

## Solution

Headless browser automation that:
1. Authenticates to each platform (session persistence)
2. Pulls conversations incrementally (only new/changed)
3. Outputs standardised markdown with metadata
4. Triggers downstream atomisation pipeline

---

## Supported Platforms (MVP)

| Platform | Auth Method | Chat List URL | Priority |
|----------|-------------|---------------|----------|
| Claude | Email/Google SSO | claude.ai/chats | P0 |
| ChatGPT | Email/Google SSO | chat.openai.com | P0 |
| Perplexity | Email/Google SSO | perplexity.ai/library | P1 |
| Gemini | Google SSO | gemini.google.com | P2 |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AI Chat Sync                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │
│  │ Claude  │  │ ChatGPT │  │Perplexity│ │ Gemini  │   │
│  │ Adapter │  │ Adapter │  │ Adapter │  │ Adapter │   │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘   │
│       │            │            │            │         │
│       └────────────┴─────┬──────┴────────────┘         │
│                          │                             │
│                   ┌──────▼──────┐                      │
│                   │   Sync      │                      │
│                   │   Engine    │                      │
│                   └──────┬──────┘                      │
│                          │                             │
│         ┌────────────────┼────────────────┐            │
│         │                │                │            │
│   ┌─────▼─────┐   ┌──────▼──────┐  ┌─────▼─────┐      │
│   │  Session  │   │   State     │  │  Output   │      │
│   │  Manager  │   │   Store     │  │  Writer   │      │
│   └───────────┘   └─────────────┘  └───────────┘      │
│                                                         │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
                   ~/ai-exports/{provider}/
                           │
                           ▼
                   [Existing Watcher]
                           │
                           ▼
                   /Knowledge/02-atoms/
```

---

## Directory Structure

```
ai-chat-sync/
├── README.md
├── package.json
├── tsconfig.json
├── .env.example
├── .gitignore
│
├── src/
│   ├── index.ts              # CLI entry point
│   ├── config.ts             # Configuration loader
│   │
│   ├── adapters/             # Platform-specific scrapers
│   │   ├── base.ts           # Abstract adapter interface
│   │   ├── claude.ts
│   │   ├── chatgpt.ts
│   │   ├── perplexity.ts
│   │   └── gemini.ts
│   │
│   ├── engine/
│   │   ├── sync.ts           # Main sync orchestrator
│   │   ├── scheduler.ts      # Cron scheduling
│   │   └── dedup.ts          # Deduplication logic
│   │
│   ├── auth/
│   │   ├── session.ts        # Session persistence
│   │   └── browser.ts        # Playwright browser setup
│   │
│   ├── output/
│   │   ├── writer.ts         # Markdown file writer
│   │   └── formatter.ts      # Standardised output format
│   │
│   └── state/
│       ├── store.ts          # SQLite state management
│       └── models.ts         # Data models
│
├── data/
│   ├── sessions/             # Browser session storage
│   ├── state.db              # Sync state database
│   └── sync.log              # Operation logs
│
└── scripts/
    ├── setup.sh              # Initial setup
    ├── sync.sh               # Manual sync trigger
    └── install-schedule.sh   # Install cron/launchd
```

---

## Core Components

### 1. Adapter Interface

Each platform adapter must implement:

```typescript
interface PlatformAdapter {
  name: string;
  baseUrl: string;
  
  // Authentication
  isLoggedIn(page: Page): Promise<boolean>;
  login(page: Page): Promise<void>;
  
  // Data extraction
  getConversationList(page: Page): Promise<ConversationMeta[]>;
  getConversation(page: Page, id: string): Promise<Conversation>;
  
  // Selectors (isolated for easy updates)
  selectors: {
    chatList: string;
    chatItem: string;
    messageContainer: string;
    userMessage: string;
    assistantMessage: string;
    timestamp?: string;
  };
}

interface ConversationMeta {
  id: string;
  title: string;
  updatedAt: Date;
  url: string;
}

interface Conversation {
  id: string;
  title: string;
  platform: string;
  createdAt: Date;
  updatedAt: Date;
  messages: Message[];
  url: string;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}
```

### 2. Session Manager

```typescript
interface SessionManager {
  // Get browser context with persistent session
  getContext(platform: string): Promise<BrowserContext>;
  
  // Save session after successful login
  saveSession(platform: string, context: BrowserContext): Promise<void>;
  
  // Check if session is still valid
  validateSession(platform: string): Promise<boolean>;
  
  // Clear expired session
  clearSession(platform: string): Promise<void>;
}
```

**Session Storage:**
- Location: `./data/sessions/{platform}/`
- Contains: cookies, localStorage, sessionStorage
- Encrypted at rest (optional)

### 3. State Store

SQLite database tracking sync state:

```sql
-- Conversations we know about
CREATE TABLE conversations (
  id TEXT PRIMARY KEY,
  platform TEXT NOT NULL,
  title TEXT,
  url TEXT,
  content_hash TEXT,
  first_seen_at DATETIME,
  last_synced_at DATETIME,
  updated_at DATETIME,
  message_count INTEGER,
  exported_path TEXT
);

-- Sync run history
CREATE TABLE sync_runs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  platform TEXT,
  started_at DATETIME,
  completed_at DATETIME,
  status TEXT,
  conversations_found INTEGER,
  conversations_new INTEGER,
  conversations_updated INTEGER,
  error_message TEXT
);

-- Index for incremental sync
CREATE INDEX idx_conversations_platform_updated 
ON conversations(platform, updated_at);
```

### 4. Sync Engine

```typescript
interface SyncEngine {
  // Sync single platform
  syncPlatform(platform: string, options?: SyncOptions): Promise<SyncResult>;
  
  // Sync all platforms
  syncAll(options?: SyncOptions): Promise<SyncResult[]>;
  
  // Get sync status
  getStatus(): Promise<SyncStatus>;
}

interface SyncOptions {
  force?: boolean;        // Ignore last sync, pull everything
  since?: Date;           // Only conversations after this date
  limit?: number;         // Max conversations to sync
  dryRun?: boolean;       // Don't write files, just report
}

interface SyncResult {
  platform: string;
  success: boolean;
  conversationsFound: number;
  conversationsNew: number;
  conversationsUpdated: number;
  conversationsSkipped: number;
  duration: number;
  error?: string;
}
```

### 5. Output Writer

Output format (markdown with frontmatter):

```markdown
---
id: conv_abc123
title: "Building a Knowledge Pipeline"
platform: claude
url: https://claude.ai/chat/abc123
created_at: 2025-12-14T10:30:00Z
updated_at: 2025-12-14T14:45:00Z
message_count: 24
synced_at: 2025-12-14T20:00:00Z
tags:
  - ai-chat
  - claude
  - auto-synced
---

# Building a Knowledge Pipeline

**User (10:30):**
How should I structure my knowledge base?

**Claude (10:31):**
Here's a recommended structure...

**User (10:35):**
What about atomisation?

**Claude (10:36):**
Atomisation breaks content into...
```

---

## CLI Interface

```bash
# Full sync (all platforms)
ai-sync

# Sync specific platform
ai-sync --platform claude
ai-sync -p chatgpt

# Force full resync (ignore state)
ai-sync --force
ai-sync -f

# Sync only recent (last 7 days)
ai-sync --since 7d

# Dry run (no file writes)
ai-sync --dry-run

# Check status
ai-sync status

# Re-authenticate platform
ai-sync auth claude

# View logs
ai-sync logs
ai-sync logs --platform claude --tail 50

# Install scheduled sync
ai-sync schedule install
ai-sync schedule remove
ai-sync schedule status
```

---

## Configuration

`.env` file:

```bash
# Output directory (where watcher picks up)
OUTPUT_DIR=~/ai-exports

# State database location  
DATA_DIR=./data

# Sync schedule (cron format)
SYNC_SCHEDULE="0 2 * * *"  # 2am daily

# Platform toggles
ENABLE_CLAUDE=true
ENABLE_CHATGPT=true
ENABLE_PERPLEXITY=true
ENABLE_GEMINI=false

# Rate limiting (ms between requests)
REQUEST_DELAY=2000

# Browser settings
HEADLESS=true
BROWSER_TIMEOUT=30000

# Logging
LOG_LEVEL=info
LOG_FILE=./data/sync.log
```

---

## Platform Adapter Details

### Claude Adapter

```typescript
const claudeAdapter: PlatformAdapter = {
  name: 'claude',
  baseUrl: 'https://claude.ai',
  
  selectors: {
    chatList: '[data-testid="chat-list"]',
    chatItem: '[data-testid="chat-list-item"]',
    messageContainer: '[data-testid="conversation"]',
    userMessage: '[data-testid="user-message"]',
    assistantMessage: '[data-testid="assistant-message"]',
  },
  
  async getConversationList(page) {
    await page.goto('https://claude.ai/chats');
    await page.waitForSelector(this.selectors.chatList);
    
    return page.$$eval(this.selectors.chatItem, items => 
      items.map(item => ({
        id: item.getAttribute('data-conversation-id'),
        title: item.querySelector('.title')?.textContent,
        updatedAt: new Date(item.getAttribute('data-updated')),
        url: item.querySelector('a')?.href,
      }))
    );
  },
  
  // ... implementation
};
```

### ChatGPT Adapter

```typescript
const chatgptAdapter: PlatformAdapter = {
  name: 'chatgpt',
  baseUrl: 'https://chat.openai.com',
  
  selectors: {
    chatList: 'nav[aria-label="Chat history"]',
    chatItem: 'nav a[href^="/c/"]',
    messageContainer: 'main',
    userMessage: '[data-message-author-role="user"]',
    assistantMessage: '[data-message-author-role="assistant"]',
  },
  
  // ... implementation
};
```

### Perplexity Adapter

```typescript
const perplexityAdapter: PlatformAdapter = {
  name: 'perplexity',
  baseUrl: 'https://www.perplexity.ai',
  
  selectors: {
    chatList: '[data-testid="library-threads"]',
    chatItem: '[data-testid="thread-item"]',
    messageContainer: '[data-testid="thread-container"]',
    userMessage: '[data-testid="user-query"]',
    assistantMessage: '[data-testid="answer-content"]',
  },
  
  // ... implementation
};
```

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Auth expired | Log warning, skip platform, notify user |
| Rate limited | Exponential backoff, max 3 retries |
| Selector not found | Log error, continue to next conversation |
| Network timeout | Retry once, then skip |
| Platform down | Skip platform, log, continue others |

```typescript
class SyncError extends Error {
  constructor(
    message: string,
    public platform: string,
    public conversationId?: string,
    public recoverable: boolean = true,
  ) {
    super(message);
  }
}
```

---

## Scheduling

### macOS (launchd)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" 
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.ai-chat-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/node</string>
        <string>/path/to/ai-chat-sync/dist/index.js</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>2</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>/path/to/ai-chat-sync/data/sync.log</string>
    <key>StandardErrorPath</key>
    <string>/path/to/ai-chat-sync/data/sync-error.log</string>
</dict>
</plist>
```

### Linux (cron)

```bash
0 2 * * * cd /path/to/ai-chat-sync && /usr/bin/node dist/index.js >> data/sync.log 2>&1
```

---

## Deduplication Logic

```typescript
function shouldSync(
  existing: ConversationRecord | null, 
  found: ConversationMeta
): boolean {
  // New conversation
  if (!existing) return true;
  
  // Updated since last sync
  if (found.updatedAt > existing.lastSyncedAt) return true;
  
  // Never synced successfully
  if (!existing.exportedPath) return true;
  
  return false;
}

function computeContentHash(conversation: Conversation): string {
  const content = conversation.messages
    .map(m => `${m.role}:${m.content}`)
    .join('\n');
  return crypto.createHash('sha256').update(content).digest('hex').slice(0, 16);
}
```

---

## Integration Points

### Upstream (this tool outputs to)

```
~/ai-exports/
├── claude/
│   └── 2025-12-14-building-knowledge-pipeline-abc123.md
├── chatgpt/
│   └── 2025-12-14-react-debugging-help-xyz789.md
├── perplexity/
│   └── 2025-12-14-market-research-query-def456.md
└── gemini/
    └── 2025-12-14-code-review-session-ghi012.md
```

### Downstream (existing watcher consumes)

The existing file watcher at `/Documents/knowledge_pipeline/watcher.py`:
1. Detects new files in `~/ai-exports/`
2. Adds frontmatter, moves to `/Knowledge/labelled/AI-Chats/{Provider}/`
3. Runs atomiser to extract insights to `/Knowledge/02-atoms/`

**No changes needed to existing pipeline.**

---

## Testing Strategy

### Unit Tests

```typescript
describe('Claude Adapter', () => {
  it('extracts conversation list correctly', async () => {
    const html = loadFixture('claude-chat-list.html');
    const conversations = await adapter.parseConversationList(html);
    expect(conversations).toHaveLength(5);
    expect(conversations[0].title).toBe('Expected Title');
  });
  
  it('extracts messages with correct roles', async () => {
    const html = loadFixture('claude-conversation.html');
    const conversation = await adapter.parseConversation(html);
    expect(conversation.messages[0].role).toBe('user');
    expect(conversation.messages[1].role).toBe('assistant');
  });
});
```

### Integration Tests

```typescript
describe('Full Sync', () => {
  it('syncs new conversations only', async () => {
    // Setup: existing state with 5 conversations
    // Action: sync finds 7 conversations (5 existing + 2 new)
    // Assert: only 2 new files written
  });
  
  it('updates changed conversations', async () => {
    // Setup: conversation with hash X
    // Action: sync finds same conversation with hash Y
    // Assert: file updated, hash updated in state
  });
});
```

### E2E Tests (manual)

```bash
# Test auth flow
ai-sync auth claude --headless=false

# Test single conversation extraction
ai-sync --platform claude --limit 1 --dry-run

# Test full sync
ai-sync --dry-run
```

---

## Security Considerations

| Concern | Mitigation |
|---------|------------|
| Credentials in code | Never stored; browser session only |
| Session theft | Sessions stored locally, not transmitted |
| Data exfiltration | All data stays local, no external calls |
| Platform ToS | Grey area; mitigate by being polite (delays, no redistribution) |

---

## Dependencies

```json
{
  "dependencies": {
    "playwright": "^1.40.0",
    "better-sqlite3": "^9.0.0",
    "commander": "^11.0.0",
    "dotenv": "^16.0.0",
    "date-fns": "^2.30.0",
    "winston": "^3.11.0",
    "node-cron": "^3.0.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "@types/node": "^20.0.0",
    "@types/better-sqlite3": "^7.6.0",
    "vitest": "^1.0.0"
  }
}
```

---

## Build & Run

```bash
# Install
git clone <repo>
cd ai-chat-sync
npm install
npx playwright install chromium

# Configure
cp .env.example .env
# Edit .env with your settings

# Build
npm run build

# First run (will prompt for auth)
npm run sync

# Install schedule
npm run schedule:install
```

---

## Roadmap

### MVP (Week 1)
- [ ] Claude adapter working
- [ ] ChatGPT adapter working
- [ ] Basic CLI
- [ ] State persistence
- [ ] Output to ~/ai-exports/

### V1.0 (Week 2)
- [ ] Perplexity adapter
- [ ] Scheduling (launchd)
- [ ] Incremental sync
- [ ] Error recovery

### V1.1 (Week 3+)
- [ ] Gemini adapter
- [ ] Web UI for status
- [ ] Notification on auth expiry
- [ ] Export statistics

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Sync reliability | >95% successful runs |
| Time per conversation | <3 seconds |
| Auth persistence | >7 days between re-auth |
| Incremental efficiency | <10% of full sync time |

---

## Open Questions

1. **Handle rate limiting?** Start conservative (2s delay), adjust based on platform behavior
2. **What if UI changes?** Selectors in separate config, easy to update
3. **Multiple accounts?** V2 feature - separate session profiles

---

## Notes for Implementation

- Start with Claude adapter (most familiar, easiest to test)
- Use Playwright's codegen for initial selector discovery: `npx playwright codegen claude.ai`
- Test session persistence early - this is the key to low friction
- Keep adapters thin - most logic in shared engine

---

*Spec version 1.0.0 - Ready for implementation*

---
Signed-by: Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd
