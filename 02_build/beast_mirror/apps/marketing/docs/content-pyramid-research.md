# Content Pyramid Research — Standing on the Shoulders of Giants

**Date:** 2026-03-11
**Researcher:** Claude (Opus 4.6)
**Purpose:** Deep research into Gary Vee's content model, who executes it well, and how Amplified Partners makes it better.

---

## 1. THE GARY VEE MODEL (What He Does)

Gary Vaynerchuk's "reverse pyramid" model:

1. **Create one pillar piece** — a 30-60 minute video (keynote, vlog, Q&A)
2. **Team of ~20 people** slice it into 30+ micro-content pieces
3. **Distribute across every platform** — each piece native to its platform
4. **Listen to community response** — comments, shares, DMs
5. **Create community-driven micro-content** from the responses
6. **Second wave of distribution** from community reactions

**Results:** One keynote → 30+ pieces → 35 million+ views

**What makes it work:**
- Starts from authentic, unscripted content (Gary being Gary)
- Platform-native adaptation (not just cross-posting)
- Volume — he posts 80-100 pieces per day across platforms
- Team of 20+ editors, designers, strategists
- Feedback loop — community responses feed back into content

**What doesn't scale for SMBs:**
- Requires a 20-person content team
- Gary creates pillar content all day every day — it's his full-time job
- Budget is enormous (VaynerMedia is a $300M+ agency)
- The "just be authentic on camera" advice ignores that most people aren't natural performers

---

## 2. WHO'S DOING IT WELL (2025-2026)

### AI-Powered Implementations

**Make.com / n8n automation builders:**
- Substack → webhook → AI adaptation → auto-post to LinkedIn, Twitter, Instagram
- Preserves voice through custom system prompts
- One newsletter = 5 LinkedIn posts + 10 Substack Notes + 2 Twitter threads
- Cost: essentially free beyond the AI API calls

**HeyGen Blog-to-Video:**
- Paste a blog URL → AI generates a presenter-led video
- Avatar reads adapted script, not the raw article
- Multi-format output: full video + clips for Reels/TikTok/Shorts
- Strong for UGC-style social content

**Synthesia for structured content:**
- Better for training, onboarding, educational content
- More polished, professional look
- Multilingual support (relevant for Amplified's future growth)
- Less "social native" than HeyGen

**Content repurposing tools (2026 landscape):**
- Pictory, Vidyo.ai, Munch — AI-powered clip selection with "viral scores"
- Repurpose.io — multi-platform distribution automation
- ContentFries — specifically built for the Gary Vee model

### SMB-Specific Results

- Nashville real estate agency: **100% increase in weekly content output** with zero additional headcount using AI automation
- Content repurposing studios: Starting under $3,000, reaching $2-10K/month revenue
- SMBs doing 2 blog posts/month generating **8-10 additional pieces** across LinkedIn, email, paid channels — same investment, 5x distribution
- AI adoption in SMBs jumped from 40% to 58% in 2025 (Business.com survey)

---

## 3. THE GAPS (What Nobody's Doing Well)

1. **Voice preservation at scale** — Most AI repurposing loses the human voice. It becomes generic AI slop. The Make.com workflows use basic prompts that don't truly capture personality.

2. **Quality gates** — Everyone's focused on volume. Nobody's running content through rubrics before publishing. The assumption is "AI + human review = good enough."

3. **Feedback loops with teeth** — Gary Vee's team manually reviews what works and feeds it back. Nobody's automating the learning cycle — what performed well → why → how to do more of that.

4. **SMB context** — All the case studies are either Gary-scale (huge team) or solo creator (no business behind it). Nobody's building this for a plumber in Jesmond who needs 2 hours a month of marketing, not 20 hours a week.

5. **Pain point grounding** — Content gets created from "what should we post about" not "what are our customers actually struggling with right now." No research agent feeding real problems into the content machine.

6. **Compliance and ethics** — Zero attention to brand safety, no auto-fail for dodgy claims, no compliance checking. Just vibes.

---

## 4. THE AMPLIFIED MODEL (Making It Ours)

### What We Take (Standing on Shoulders)

| From | What We Take |
|------|-------------|
| Gary Vee | One pillar → many platform pieces. The reverse pyramid structure. |
| Make.com builders | Webhook-triggered automation. Substack RSS → pipeline trigger. |
| HeyGen | Blog-to-video for social clips. Avatar of Ewan for talking head content. |
| Synthesia | Polished training/onboarding videos from written content. |
| Content pyramid SEO | Pillar → derivative → micro structure for search authority. |
| n8n/automation community | Event-driven workflows, not just cron schedules. |

### What We Add (Making It Better)

1. **Ewan + Eli partnership** — The pillar isn't scripted video. It's a human-AI writing partnership. Ewan brings the experience, the voice, the insight. Eli (Claude) brings structure, research, and polish. The output is better than either could do alone.

2. **Research-grounded content** — Before any pillar piece is written, the research agent has already identified what SMBs are actually struggling with this week. The pillar addresses a real pain point, not a content calendar guess.

3. **The Enforcer** — Every atomized piece runs through three rubrics (tone, quality, compliance) before it goes anywhere. No AI slop gets published. If it scores below 7/10, it gets regenerated. If it scores below 8.5, a human reviews it.

4. **Brand voice fidelity** — The atomizer doesn't just summarise. It has the client's personality config, their avoid words, their local area, their tone. Dave at Jesmond Plumbing sounds like Dave, not like a marketing agency.

5. **Feedback loop with FalkorDB** — Every published piece gets tracked. Engagement data flows back into the knowledge graph. The research agent sees what topics resonated, what flopped, and adjusts the next cycle's research accordingly. The system gets smarter.

6. **Video from text, not video from video** — Gary starts with video because he's a performer. Most SMB owners aren't. We start with text (which Ewan is great at) and atomize into video via HeyGen/Synthesia. Lower barrier to entry, same multi-format output.

7. **SMB-native economics** — Gary needs 20 people. We need one person (Ewan) spending 2 hours writing one pillar piece with Eli. The machine handles the other 9+ pieces. Cost per piece drops from agency pricing ($200-500/piece) to API calls ($0.50-2/piece).

8. **Permission-based, value-first distribution** — Reddit posts are genuine answers with zero self-promotion. Email is personal and opt-in. Social is helpful, not salesy. Everything follows Amplified's principles: white hat, radically transparent, radically honest.

9. **Onboarding and training as a byproduct** — The Synthesia scripts aren't just marketing. They're onboarding videos for new clients, training content for SMB staff, how-to guides. The pillar content serves double duty.

10. **Open system** — Clients can see exactly what the engine does, how it works, why it made each decision. No black box. Ideas meritocracy — if the client has a better topic idea than the research agent, it goes in. The system serves them, not the other way round.

---

## 5. THE AMPLIFIED CONTENT FLOW

```
┌─────────────────────────────────────────┐
│         EWAN + ELI (CLAUDE)             │
│    Write one pillar piece together       │
│    Grounded in research agent findings   │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         CONTENT ATOMIZER                │
│    One piece → 10+ platform pieces       │
│    Each native to its platform           │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   ┌─────────┐ ┌────────┐ ┌──────────┐
   │ TEXT    │ │ VIDEO  │ │ SOCIAL   │
   │         │ │        │ │          │
   │ Substack│ │ HeyGen │ │ Facebook │
   │ Blog    │ │ Synth. │ │ Insta    │
   │ Email   │ │        │ │ Twitter  │
   │ LinkedIn│ │        │ │ GMB      │
   │ Reddit  │ │        │ │          │
   └────┬────┘ └───┬────┘ └────┬─────┘
        │          │           │
        └──────────┼───────────┘
                   ▼
┌─────────────────────────────────────────┐
│         THE ENFORCER                    │
│    Tone rubric → Quality rubric →       │
│    Compliance rubric → PASS/FAIL        │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         PUBLISHING AGENT                │
│    Cadence check → Format → Publish     │
│    Log to Langfuse → Track engagement   │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         FEEDBACK LOOP (FalkorDB)        │
│    What worked → Why → Inform next      │
│    research cycle. System gets smarter.  │
└─────────────────────────────────────────┘
```

---

## Sources

- [The GaryVee Content Strategy](https://garyvaynerchuk.com/the-garyvee-content-strategy-how-to-grow-and-distribute-your-brands-social-media-content/)
- [Gary Vee's Content Framework: One Video, 30+ Content Pieces](https://biteable.com/blog/gary-vees-content-framework-one-video-30-content-pieces/)
- [GaryVee Content Model Explained in 60 Seconds](https://www.contentfries.com/blog/gary-vee-content-model-explained)
- [AI for Marketing Automation: Small Business Playbook](https://www.theslidefactory.com/post/ai-for-marketing-automation-how-small-teams-multiply-their-output)
- [Content Atomization: Maximize ROI](https://martech.org/content-atomization-maximize-roi-by-repurposing-your-best-ideas/)
- [AI Content Repurposing Playbook](https://skywork.ai/blog/ai-agent/ai-content-repurposing-playbook/)
- [The Content Pillar System](https://promptsdaily.substack.com/p/the-content-pillar-system)
- [HeyGen Blog-to-Video](https://www.heygen.com/tool/blog-to-video-ai)
- [How I Solved the Content Repurposing Problem with AI](https://aimaker.substack.com/p/ai-content-repurposing-automation-system-guide-linkedin-twitter-substack-notes)
- [AI Agent to Repurpose Substack to X Posts](https://www.yana-g-y.com/p/ai-agent-to-repurpose-emails-to-x-posts-in-your-voice)
- [IDC: The SMB 2026 Digital Landscape](https://www.idc.com/resource-center/blog/the-smb-2026-digital-landscape-how-ai-is-redefining-growth/)
- [2026 Small Business AI Outlook Report](https://www.business.com/articles/ai-usage-smb-workplace-study/)
- [Small Business AI Automation: 2026 Growth Guide](https://cornelldesigngroup.com/small-business-ai-automation/)
