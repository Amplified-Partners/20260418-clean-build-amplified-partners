---
title: "Make_Enterprise_Briefing"
id: "make-enterprise-briefing"
version: 1
created: 2026-04-25
last_validated: 2026-04-25
type: document
topic_type: reference
status: imported
source_file: "Make_Enterprise_Briefing.pdf"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

MAKE.COM ENTERPRISE BRIEFING – PREIMEETING DOCUMENT
Purpose:
Provide Make.com with a clear, structured overview of the planned MSP (Managed Service
Provider) architecture, client model, governance, and operational requirements before Monday’s
call.
1. Overview
The BusinessFactory.ai / Byker Business Assist platform will operate as a national MSP automation
service for small businesses. The service provides standardised automation packs, onboarding
workflows, sentiment analysis, and AI-assisted client support. Make.com Enterprise will be the
central automation engine governed by strict compliance, stagingItoIproduction workflows, and
usageIbased client tiers.
2. Required Enterprise Architecture
• One Main Organisation (core automation, staging, production).
• PerIClient Child Organisations (fully isolated workspaces).
• APIIdriven organisation creation for each new client.
• Usage limits per client based on subscription tier.
• EnterpriseIlevel SLAs, governance, and audit logs.
3. Technical Requirements
• Automated client provisioning:
- Create child org via API
- Create teams (STAGING, PRODUCTION)
- Apply usage limits
- Import JSON blueprints for core scenarios
• Core scenarios to deploy per client:
- Lead capture & CRM sync
- VBaaS automation bundle
- Sentiment analysis scoring
- FinanceOps (Tide → Stripe → Xero)
- Reputation engine workflows
• Strict staging → production deployment path.
• Automated daily health checks.
• Make engineers available for validation and review.
4. Governance & Compliance
• Data isolation guaranteed per client (separate orgs).
• Audit logging via Make + internal Regulus-Watch.
• Role-based access control (limited to Ewan + AI agents).
• Release Ticket approval before scenario promotion.
• UK/EU data hosting preferred.

• Documentation requested:
- DPA + SCCs
- Sub-processor list
- API rate limits
- Enterprise SLA details
5. Client Model
Three subscription tiers defined by automation volume:
• Tier 1: Starter (10–25k ops/month)
• Tier 2: Growth (25–50k ops/month)
• Tier 3: Performance (50–100k ops/month)
Each client receives:
• Automated onboarding journey
• Core operational automations
• SentimentOps integration
• VBaaS dashboard sync
6. Scalability Requirements
Forecast:
• 2026: 30–50 clients
• 2027: 100–150 clients
• 2028: 200–300 clients
Require:
• Support for hundreds of client orgs
• API provisioning at scale
• Clear pricing structure for high-volume MSP usage
7. Funding & Build Expectations
• Founder-funded with runway secured.
• Seeking clarity on:
- Annual Enterprise cost
- PerIclient usage pricing
- Professional services or engineering involvement
- Expected limits for large MSP deployments
8. Requested Outcome for Monday Meeting
• Confirm Make.com Enterprise supports full MSP model.
• Review architecture and API requirements.
• Provide detailed pricing and usage structure.
• Establish timeline for deployment and technical validation.