---
title: "Amplified Partners - Connectors Security and P"
id: "amplified-partners---connectors-security-and-p"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "Amplified Partners - Connectors Security and P.docx"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

**AMPLIFIED PARTNERS**

Connectors, Permissions, Safety & IP Protection

Claude Desktop / Cowork Mode

Prepared for Ewan --- 19 March 2026 --- Internal: Radically Honest Assessment

**1. Where Your Data Lives and Flows**

MCP (Model Context Protocol) is an open standard that lets Claude talk to external services. There are two fundamentally different architectures:

**Local MCP Servers run on your machine.**

Data flows directly between your computer and the service. Desktop Commander, Apple Notes, iMessages, and local PDF Tools work this way.

**Remote MCP Servers are hosted services.**

Traffic routes through Anthropic's servers. Gmail, Google Calendar, Google Drive, Notion, and Linear fall into this category.

**Data Flow by Connector**

  ----------------------------- ----------------------------- ----------------------------------------
  **Connector**                 **Data Route**                **What Anthropic Sees**
  Email (Gmail)                 Through Anthropic servers     Email content during active queries
  Project Mgmt (Linear)         Through Anthropic servers     Issue content, comments during queries
  Calendar (Google Cal)         Through Anthropic servers     Event details during queries
  File Storage (Google Drive)   Through Anthropic servers     File content during active queries
  Notes/Docs (Notion)           Through Anthropic servers     Page content during queries
  Browser (Chrome connectors)   Mixed --- local + Anthropic   Page content, actions taken
  Local System (Desktop Cmd)    Local execution               Only what enters conversation
  PDF/Office Tools              Local execution               File content processed locally
  Prospecting (Vibe)            Through Anthropic servers     Search queries, business data
  Web/Hosting (Netlify, B12)    Through Anthropic servers     Deployment data, site content
  ----------------------------- ----------------------------- ----------------------------------------

**What Gets Stored:**

Tool call parameters and responses become part of your chat history. Anthropic logs tool parameters (not raw file contents) as telemetry.

**What's Ephemeral:**

File content from connectors is retrieved only during active queries --- no caching. OAuth tokens are removed when you disconnect a connector.

**2. Anthropic's Data Policies**

**Training Data Usage**

-   Consumer plans: Conversations CAN be used for training only if you opt in via Privacy Settings

-   Raw connector content is explicitly excluded from training data

-   Incognito chats are never used for training regardless of settings

-   Commercial plans (Team, Enterprise, API): Training is completely excluded

**Data Retention**

  --------------------------------- -----------------------------------
  **Scenario**                      **Retention**
  Standard (opt-out of training)    30 days after deletion
  Conversations (training opt-in)   Up to 5 years (de-identified)
  Violation content                 Up to 2 years
  Trust and safety scores           Up to 7 years
  Feedback (thumbs up/down)         5 years (de-linked from identity)
  --------------------------------- -----------------------------------

**What Anthropic Does NOT Do:**

-   Does not sell your data to third parties

-   Does not forward your IP address, user ID, or metadata to MCP servers

-   Does not let connectors access your chat history, memory, or uploaded files

Certifications: SOC 2 Type II, ISO 27001, GDPR compliance. These are real, audited certifications.

**3. IP Protection --- Honest Assessment**

**The Real Risks**

1.  Conversation Context Accumulation --- over long sessions, Claude holds a rich cross-section of your business

2.  Data Cross-Pollination --- combining data from multiple sources in one context increases exposure if compromised

3.  Third-Party Connector Trust --- each connector has its own developer and privacy policy

4.  Local MCP Servers Run With Your Privileges --- Desktop Commander can access anything on your machine

5.  Browser Connectors See Everything --- can read and interact with any page in your browser

**What's Genuinely Safe**

Your proprietary ideas in conversation are protected by retention policies. Client data via connectors is ephemeral. Business processes follow standard retention rules.

**Bottom Line:**

Your IP risk is comparable to any integrated cloud platform. Anthropic explicitly commits to not training on connector data. Risk is not zero, but manageable and within what any sensible cloud-using business already accepts.

**4. Permissions Audit**

-   Gmail --- Read access is broad. Can read any email. Don't search emails containing passwords or credentials.

-   Linear --- Read/write access. Can create and modify issues. Be deliberate about write vs read.

-   Google Calendar --- Read/write. Low risk overall.

-   Google Drive --- Broad read/search. Can't scope to specific folders.

-   Notion --- Full read/write. Like giving editor access to entire workspace.

-   Browser Connectors --- BROADEST permission set. Can see and interact with any page.

-   Desktop Commander --- Effectively user-level access. Most powerful connector. Review commands before approving.

-   iMessages --- Can read and send messages. Be careful with send capability.

-   Apple Notes --- Full access. Low risk unless you store credentials there.

-   Vibe Prospecting --- Search queries visible to third party.

-   Netlify/B12/Apify --- Apify runs on their infrastructure, not yours.

**5. Sensible Rules --- Practical Hygiene**

**Non-Negotiables**

1.  Opt out of model training. Go to Privacy Settings on claude.ai and disable Model Improvement.

2.  Use Incognito mode for sensitive work --- proprietary strategy, client details, competitive intelligence.

3.  Never paste credentials, API keys, or passwords into any conversation.

4.  Disconnect connectors you're not actively using.

**Smart Practices**

1.  Keep a dedicated browser profile for Claude's browser connectors.

2.  Review Desktop Commander commands before approving --- especially rm, mv, or network operations.

3.  Don't pull sensitive client data into casual conversations.

4.  Start new conversations for new topics to keep context clean.

5.  Periodically delete old conversations (30-day backend deletion after you delete).

6.  Document which connectors are enabled and why.

**When You Scale**

Consider upgrading to Team or Enterprise plan for zero training data usage and admin controls. Write a short Acceptable Use Policy. Audit quarterly.

Sources: Anthropic Connectors Directory FAQ, Anthropic Software Directory Policy, Privacy policies, MCP Security docs (Red Hat, Palo Alto Networks, modelcontextprotocol.io).
