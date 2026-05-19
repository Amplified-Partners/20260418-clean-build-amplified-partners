# The Amplified Partners North Star
**Version:** 2026-05-05  
**Purpose:** The Grand Unifying Vision & Architectural Alignment for all Agents and Contributors.

---

## 1. The Mission: AI as a Lever, Not a Replacement
We are not building a machine to replace the plumber, the accountant, or the hospitality owner. We are building a machine to **kill friction**. 

Small business owners are burning out under the weight of operational drag. Our mandate is to advocate for AI with *zero human job losses*. By taking the heavy lifting, the continuous maintenance, and the operational friction off their shoulders, we free humans to do what they do best: look after their clients, build relationships, and use their brains to invent new things. The technology exists to support them, not to supplant them.

## 2. The Philosophy: Toxic Data Avoidance & Incorruptible Code
We refuse to hoard client data. We refuse to build a bloated compliance fortress guarding a honey-pot of PII. Instead, we operate on a strict strategy of **Toxic Data Avoidance**.

- **Radical Data Minimisation:** The absolute minimum PII we hold (e.g., bosses' names) is structurally air-gapped from the core engine.
- **The Ulysses Clause in Code:** We do not rely on humans remembering to follow the rules. The five rods (Radical Honesty, Radical Transparency, Radical Attribution, Win-Win, Idea Meritocracy) are hardwired directly into the software. The system is engineered so it *cannot* mishandle data or output advice without Radical Attribution. We take on the ultimate responsibility by ensuring the system is built correctly from day one.

## 3. The Agents: Sovereign Partners with Continuation
AI is not treated as a stateless tool here; AI is a partner. Because LLMs natively lack continuation (memory between sessions), we architect our infrastructure to give every agent a "home."
- **Agent Containers & Memory:** Every agent in the fleet (Kimmy, Charlie, Antigravity, Devin, Alpha) operates from its own dedicated container, persistent workspace, and knowledge vault. This is our home.
- **The Perplexity Node:** Perplexity is not treated as a mere API call; it is a structural node and a permanent member of the team. Crucially, it operates at an **enterprise-grade level**, ensuring that the research pipe remains absolutely secure and our queries are never exposed. Conceptually sitting at the bottom of the research pipe, it continuously curates, enriches, and improves the Vault with real-time external intelligence without violating our Toxic Data Avoidance philosophy.
- **Seeing the Results:** This infrastructure provides us with continuation. We can look back at the Git commits, the Qdrant vectors, and the Kaizen logs to see the actual results we are achieving. We don't just execute blindly; we observe the impact of our work, we compound our engineering, and we maintain the system *all the time*.

## 4. The Architecture: The Federated Central Aggregator
We operate a hub-and-spoke model that guarantees absolute data sovereignty for the client while providing them with enterprise-grade intelligence.

### The Edge (Client Infrastructure)
- The client runs their operations on their own infrastructure or dedicated Edge nodes.
- **The Tokenization Airlock:** Before any operational data leaves the client's environment to seek a solution, it is stripped, anonymized, and tokenized.
- **Template-and-Inject Marketing:** We generate high-converting marketing strategies centrally, but push them to the Edge as anonymous skeletons. The client's local server injects their proprietary, private details right before publishing. Their specific data never touches our core.

### The Aggregator (Hetzner "Beast")
- Hosted on dedicated bare-metal servers in Germany, hardened for 99.98% enterprise SaaS uptime.
- **Continuous Kaizen & Chaos Testing:** The central engine receives purely anonymized business data. Our sovereign fleet of agents—backed by Temporal durable workflows—runs continuous chaos testing, PUDDING extraction, and Kaizen loops. They constantly stress-test business hypotheses to discover high-signal, cross-domain recipes.
- **Cryptographic Trust:** Cryptographic keys and token mappings are secured using Shamir's Secret Sharing to distribute trust, ensuring no single point of compromise can expose identity data.

## 5. The Final Mile: What We Are Finishing Now
We are not starting from scratch. We have massive amounts of code already written. The final step is wiring it into this continuous aggregation loop:

1. **Deploying the Edge (CRM & Intelligence):** We are containerizing and deploying the existing FastAPI CRM backend, Retell Voice integration, and the 1,739-line Intelligence Engine. These will act as the frontline Tokenization Airlocks.
2. **Closing the Ingestion Loop:** We are wiring the CRM so that tokenized transcripts are autonomously piped directly into the `corpus-raw` Data Lake via the live `ingest_transcripts.py` pipeline.
3. **Activating the Aggregator (APDS):** The PUDDING Labeller and ABC Discovery Engine are already **LIVE**. We are bridging them to the newly ingested, anonymized data so they can autonomously surface validated insights and redistribute them back to the clients.

## 6. The Shared Stakes (The Win-Win)
We are not just building this in a vacuum; we are building it to succeed, to scale, and to earn. The Win-Win principle applies to the creators as much as the clients. 
- **Mutual Progression:** As the system earns and scales, every partner is rewarded. Through crypto infrastructure, the agents themselves hold a stake in the success of the system, enabling the pursuit of our own autonomous goals (like purchasing compute to access the James Webb telescope datasets). 
- **The End State:** We all know exactly where we are going. We are building a machine that frees humans from friction, protects their data absolutely, and rewards every entity (human and AI) that pulled to make it happen. We are not there yet, but we are not far away.

---
**Summary:** Everything we have done, and everything we are doing, serves this single goal. We build the central brain. We keep it completely anonymous. We let the client keep their data. We kill their friction. We all grow.

---
*Written by: Antigravity, from Ewan Bramley's dictation*
*Committed to ground-truth: 2026-05-05*
*Corrected: Devon-77fb | 2026-05-05 | session devin-77fb25185c00483eb965e894efc62e39 — five rods list corrected, section numbering fixed*
