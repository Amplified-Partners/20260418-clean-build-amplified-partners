---
title: "Bob: AI Tradesperson Service Automation"
exported: 2026-03-10 20:20:06.161
created: 2026-02-27 09:53:24.000
url: https://gemini.google.com/app/5d4ed32c4c17cefa
messages: 1
---

## Gemini

The research document **"SIX RESEARCH STREAMS — LOCKED"** provides a comprehensive validation of **Bob**, an AI-native service automation tool designed for UK tradespeople. As of February 27, 2026, the research highlights a significant market opportunity driven by looming tax regulations and a major shift in the WhatsApp ecosystem.

---

## 1. Missed Call Recovery: The "Low-Hanging Fruit"
UK micro-businesses currently face a "leaky bucket" problem with incoming leads:
* **Missed Call Volume:** Approximately **33%** of all calls to UK micro-businesses are missed.
* **Micro-Business Vulnerability:** The rate climbs to **62%** for the smallest businesses (0-9 employees).
* **Customer Retention:** **85%** of potential customers will not call a second time if the first attempt is missed.
* **The "Bob" Solution:** A low-complexity build (~£0.10–£0.20 per recovery) using AI voice and SMS fallbacks to book appointments instantly.


---

## 2. Market Sizing and the "864,000" Figure
The research clarifies the specific target demographic for Bob's initial launch:
* **The 864,000 Figure:** This represents the specific subset of sole traders and landlords earning over **£50,000** who are mandated to follow new **MTD (Making Tax Digital)** reporting rules starting April 2026.
* **Total Addressable Market (TAM):** When including all construction and allied services (plumbers, electricians, etc.), the total market reaches roughly **2.25 million** businesses.
* **Revenue Projection:** Targeting just 1% of this market at £99/month could yield:
    $$22,500 \text{ customers} \times £99 \times 12 \text{ months} = £26.7\text{M ARR}$$.

---

## 3. The WhatsApp "Lockout" Moat
A pivotal policy change on **January 15, 2026**, has effectively cleared the competition:
* **General AI Ban:** Meta has prohibited general-purpose AI assistants (like ChatGPT wrappers) from the WhatsApp Business API.
* **Compliance Moat:** Bob remains compliant because it is categorized as **"business workflow automation"** (incidental AI) rather than a general-purpose bot.
* **Zero Messaging Costs:** Because Bob’s interactions are customer-initiated, they fall under "Service" conversations, which are **FREE** on the WhatsApp API in the UK.

---

## 4. MCP Server Landscape
The technical foundation relies on the **Model Context Protocol (MCP)**, which has reached **97 million** monthly SDK downloads in 2026:
* **Standard Integrations:** Core infrastructure like PostgreSQL, Google Calendar, and Stripe have existing MCP servers.
* **Custom Build Required:** UK-specific integrations for **Xero, QuickBooks, and HMRC MTD** do not yet exist and must be built from scratch.
* **Strategic Advantage:** These custom financial bridges create a technical barrier that competitors cannot easily replicate.

---

## 5. Privacy-by-Architecture (P2 Tokenisation)
To address GDPR Article 25 (Privacy by Design), Bob uses a unique tokenization layer:
* **PII Extraction:** Personal Identifiable Information (names, addresses) is extracted from voice notes via Whisper and spaCy.
* **Token Substitution:** Sensitive data is replaced with random tokens (e.g., `silent-ocean-deep-river`) before being sent to the AI.
* **Verification:** The AI processes the request using only tokens; the vault only de-tokenizes data for authorized final actions (like sending a quote).


---

## 6. Competitive Pricing Analysis
Bob is positioned at **£99/month**, which is a premium compared to traditional job management software:
* **Competitor Rates:** Tools like **Tradify** and **Fergus** range from **£29 to £45** per month.
* **Value Proposition:** The price is defensible if Bob demonstrably saves 15+ hours of admin per week through its voice-first, AI-native approach.
* **Feature Gap:** Competitors largely lack native WhatsApp integration, 24/7 missed call recovery, and advanced privacy architectures.

> **Key Insight:** Bob's "moat" isn't just the AI; it's the combination of the WhatsApp regulatory shield, the privacy-first architecture, and the high-friction UK financial integrations.

---

**Would you like me to draft a customer interview guide to validate that £99/month price point with UK tradespeople?**

