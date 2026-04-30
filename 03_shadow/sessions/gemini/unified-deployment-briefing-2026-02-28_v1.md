---
title: "Unified Deployment Briefing"
exported: 2026-03-10 20:20:00.335
created: 2026-02-28 13:44:26.000
url: https://gemini.google.com/app/6e6f004db3f3bbd1
messages: 2
---

## You

CLAUDE CODE — DEPLOY BRIEFING
Date: 28 February 2026
Source: Kimi K2.5 + Perplexity morning session

READ THIS FIRST. Your job:
1. Create every file exactly as written below
2. No changes. No improvements. No renaming.
3. Commit with the message at the bottom.
4. Run the post-deployment checklist.
Confirm you have read this, then proceed.

─────────────────────────────────────
REPO STRUCTURE TO CREATE:
─────────────────────────────────────

amplified-unified/
├── railway.json
├── docker-compose.yml
├── shared/
│   ├── isolation.js
│   └── qdrant.js
├── services/
│   ├── personal/
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── src/
│   │       ├── index.js
│   │       ├── routes/
│   │       │   ├── dashboard.js
│   │       │   ├── voice.js
│   │       │   └── council.js
│   │       ├── services/
│   │       │   ├── plaud.js
│   │       │   ├── morningBrief.js
│   │       │   └── rubrikEngine.js
│   │       └── views/
│   │           └── dashboard.ejs
│   └── business/
│       ├── Dockerfile
│       ├── package.json
│       └── src/
│           ├── index.js
│           ├── routes/
│           │   ├── client.js
│           │   ├── reddit.js
│           │   └── support.js
│           ├── services/
│           │   ├── redditNinja.js
│           │   ├── avatarFactory.js
│           │   └── supportTrainer.js
│           └── views/
│               └── client-dashboard.ejs
├── rubriks/
│   ├── WOW-ZIGLAR-LUND-01.json
│   ├── WOW-KENNEDY-GODIN-02.json
│   ├── OPS-DALIO-GERBER-03.json
│   ├── OFFER-HORMOZI-LUND-04.json
│   ├── MKTG-CIALDINI-GARYVEE-05.json
│   ├── TRUST-IMMUTABLE-RUBRIK-11.json
│   └── DANGER-SPIRAL-EXIT-12.json
├── SOUL.md
├── VOICE_MIRROR.md
└── .env.example

─────────────────────────────────────
FILE: railway.json
─────────────────────────────────────
{
  "$schema": "https://railway.app/railway.schema.json",
  "services": {
    "personal-command-center": {
      "build": { "dockerfile": "services/personal/Dockerfile" },
      "deploy": {
        "startCommand": "node src/index.js",
        "healthcheckPath": "/health",
        "healthcheckTimeout": 30,
        "restartPolicyType": "ON_FAILURE"
      },
      "envs": { "PORT": "3000", "SERVICE_TYPE": "personal" }
    },
    "business-swarm": {
      "build": { "dockerfile": "services/business/Dockerfile" },
      "deploy": {
        "startCommand": "node src/index.js",
        "healthcheckPath": "/health",
        "healthcheckTimeout": 30,
        "restartPolicyType": "ON_FAILURE"
      },
      "envs": { "PORT": "3001", "SERVICE_TYPE": "business" }
    }
  }
}

─────────────────────────────────────
FILE: .env.example
─────────────────────────────────────
# === SHARED ===
OPENAI_API_KEY=sk-...
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=optional

# === PERSONAL SERVICE (Port 3000) ===
PERSONAL_PORT=3000
PLAUD_API_KEY=plaud_...
PLAUD_WEBHOOK_SECRET=generate_random_string
USER_NAME=ewan
MORNING_BRIEF_TIME=07:00
RUBRIK_CONFIDENCE_THRESHOLD=0.98
DATA_SOVEREIGNTY_MODE=strict

# === BUSINESS SERVICE (Port 3001) ===
BUSINESS_PORT=3001
ELEVENLABS_API_KEY=el_...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USER_AGENT="AmplifiedPartners/1.0"
DATA_ISOLATION_MODE=strict

─────────────────────────────────────
FILE: shared/isolation.js
─────────────────────────────────────
export const IsolationLayer = {
  namespaces: {
    personal: 'ewan_personal_mirror',
    business: (id) => `business_${id}`
  },
  async store(namespace, data) {
    console.log(`[ISOLATION] Storing in ${namespace}:`, data.type || 'unknown');
    return true;
  },
  async query(namespace, vector) {
    console.log(`[ISOLATION] Querying ${namespace}`);
    return [];
  },
  async exportPersonalToBusiness(personalData, businessId, rationale) {
    const exportRecord = {
      timestamp: new Date().toISOString(),
      from: 'personal',
      to: businessId,
      data: personalData,
      rationale,
      approvedBy: 'council',
      auditTrail: true
    };
    console.log('[ISOLATION] Personal → Business export:', exportRecord);
    return exportRecord;
  },
  validateNoCrossContamination(query) {
    if (query.includes('personal') && query.includes('business')) {
      throw new Error('CROSS_CONTAMINATION_DETECTED');
    }
    return true;
  }
};

─────────────────────────────────────
FILE: services/personal/Dockerfile
─────────────────────────────────────
FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm ci --only=production
COPY src ./src
EXPOSE 3000
CMD ["node", "src/index.js"]

─────────────────────────────────────
FILE: services/personal/package.json
─────────────────────────────────────
{
  "name": "personal-command-center",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "start": "node src/index.js",
    "dev": "node --watch src/index.js"
  },
  "dependencies": {
    "fastify": "^4.28.0",
    "@fastify/static": "^7.0.4",
    "@fastify/view": "^9.1.0",
    "ejs": "^3.1.10",
    "openai": "^4.52.0",
    "node-cron": "^3.0.3",
    "@qdrant/js-client-rest": "^1.9.0"
  }
}

─────────────────────────────────────
FILE: services/personal/src/index.js
─────────────────────────────────────
import Fastify from 'fastify';
import fastifyStatic from '@fastify/static';
import fastifyView from '@fastify/view';
import ejs from 'ejs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import cron from 'node-cron';
import dashboardRoutes from './routes/dashboard.js';
import voiceRoutes from './routes/voice.js';
import councilRoutes from './routes/council.js';
import { MorningBrief } from './services/morningBrief.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const fastify = Fastify({ logger: true });

fastify.register(fastifyView, { engine: { ejs }, root: join(__dirname, 'views') });
fastify.register(fastifyStatic, { root: join(__dirname, 'public') });
fastify.register(dashboardRoutes);
fastify.register(voiceRoutes, { prefix: '/webhook' });
fastify.register(councilRoutes, { prefix: '/council' });

const brief = new MorningBrief();
cron.schedule(process.env.MORNING_BRIEF_TIME || '0 7 * * *', async () => {
  console.log('[CRON] Generating morning brief...');
  await brief.generate();
});

fastify.get('/health', async () => ({
  status: 'ok',
  service: 'personal',
  timestamp: new Date().toISOString()
}));

const start = async () => {
  try {
    await fastify.listen({ port: process.env.PORT || 3000, host: '0.0.0.0' });
    console.log(`🧠 Personal Command Center on port ${process.env.PORT || 3000}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};
start();

─────────────────────────────────────
FILE: services/personal/src/routes/voice.js
─────────────────────────────────────
import { PlaudService } from '../services/plaud.js';
const plaud = new PlaudService();

export default async function voiceRoutes(fastify) {
  fastify.post('/plaud', async (request, reply) => {
    const secret = request.headers['x-plaud-secret'];
    if (secret !== process.env.PLAUD_WEBHOOK_SECRET) {
      return reply.code(401).send({ error: 'Unauthorized' });
    }
    try {
      const result = await plaud.processWebhook(request.body);
      return { success: true, processed: result };
    } catch (err) {
      console.error('[PLAUD ERROR]', err);
      return reply.code(500).send({ error: 'Processing failed' });
    }
  });

  fastify.post('/test-voice', async (request, reply) => {
    const testPayload = {
      transcription: request.body.text || 'Test capture',
      timestamp: new Date().toISOString(),
      location: 'test'
    };
    const result = await plaud.processWebhook(testPayload);
    return { success: true, result };
  });
}

─────────────────────────────────────
FILE: services/personal/src/routes/council.js
─────────────────────────────────────
export default async function councilRoutes(fastify) {
  fastify.get('/status', async () => ({
    active: true,
    hats: [
      { name: 'Librarian', color: 'white', status: 'active' },
      { name: 'Critic', color: 'black', status: 'active' },
      { name: 'Operator', color: 'yellow', status: 'active' },
      { name: 'Strategist', color: 'green', status: 'active' },
      { name: 'Judge', color: 'blue', status: 'active' }
    ],
    lastDecision: 'Approve business insight export',
    pendingReviews: 2
  }));

  fastify.post('/review', async (request, reply) => {
    const { item, context } = request.body;
    return {
      item,
      councilDecision: 'approved',
      confidence: 0.94,
      rationale: 'Significant advantage confirmed across all hats'
    };
  });
}

─────────────────────────────────────
FILE: services/personal/src/services/plaud.js
─────────────────────────────────────
import OpenAI from 'openai';
const openai = new OpenAI();

export class PlaudService {
  async processWebhook(payload) {
    const { transcription, timestamp, location } = payload;
    const context = await this.inferContext(transcription);
    const councilReview = await this.routeToCouncil(transcription, context);
    await this.storePersonal({ transcription, context, councilReview, timestamp });
    return { context, councilReview, timestamp };
  }

  async inferContext(text) {
    const patterns = {
      drinking: /\b(drink|pint|wine|beer|whisky|had a few)\b/i,
      idea: /\b(what if|imagine|could we|breakthrough|insight)\b/i,
      task: /\b(need to|must|should|deadline|call|email)\b/i,
      health: /\b(gym|run|walk|weight|sleep|tired)\b/i
    };
    for (const [context, regex] of Object.entries(patterns)) {
      if (regex.test(text)) return context;
    }
    return 'general';
  }

  async routeToCouncil(capture, context) {
    const hats = [
      { name: 'Librarian', prompt: 'What are the facts here? Be objective.' },
      { name: 'Critic', prompt: 'What could go wrong? Be skeptical.' },
      { name: 'Operator', prompt: 'How would we execute? Be practical.' },
      { name: 'Strategist', prompt: 'What are the alternatives? Be creative.' },
      { name: 'Judge', prompt: 'What is the verdict? Be decisive.' }
    ];
    const reviews = await Promise.all(hats.map(async hat => {
      const completion = await openai.chat.completions.create({
        model: 'gpt-4o-mini',
        messages: [
          { role: 'system', content: `You are the ${hat.name} hat. ${hat.prompt}` },
          { role: 'user', content: `Review: "${capture}"` }
        ],
        max_tokens: 100
      });
      return { hat: hat.name, insight: completion.choices[0].message.content };
    }));
    return reviews;
  }

  async storePersonal(data) {
    console.log('[PERSONAL-VAULT] Stored:', data.context);
    return true;
  }
}

─────────────────────────────────────
FILE: services/personal/src/services/morningBrief.js
─────────────────────────────────────
import OpenAI from 'openai';
const openai = new OpenAI();

export class MorningBrief {
  async generate() {
    const script = await this.generateScript();
    return { script, timestamp: new Date().toISOString(), ready: true };
  }

  async generateScript() {
    const completion = await openai.chat.completions.create({
      model: 'gpt-4o',
      messages: [{
        role: 'system',
        content: `Generate a 2-minute morning brief for Ewan.
Tone: Direct, Newcastle-inflected, radically honest, warm. Like a trusted mate who knows everything and judges nothing.
Use: "right then", "here's the thing", "no bullshit".
Structure: Morning acknowledgement → yesterday pattern mirror (no judgment) → 3 tasks today → one shite-volume insight → red line check → "go get em" close.
Never lecture. Never judge. Just the pattern, his data, his call.`
      }],
      temperature: 0.7
    });
    return completion.choices[0].message.content;
  }
}

─────────────────────────────────────
FILE: services/business/Dockerfile
─────────────────────────────────────
FROM node:20-alpine
WORKDIR /app
COPY package.json ./
RUN npm ci --only=production
COPY src ./src
EXPOSE 3001
CMD ["node", "src/index.js"]

─────────────────────────────────────
FILE: services/business/package.json
─────────────────────────────────────
{
  "name": "business-swarm",
  "version": "1.0.0",
  "type": "module",
  "scripts": { "start": "node src/index.js" },
  "dependencies": {
    "fastify": "^4.28.0",
    "@fastify/static": "^7.0.4",
    "@fastify/view": "^9.1.0",
    "ejs": "^3.1.10",
    "openai": "^4.52.0",
    "@qdrant/js-client-rest": "^1.9.0",
    "axios": "^1.7.0"
  }
}

─────────────────────────────────────
FILE: services/business/src/index.js
─────────────────────────────────────
import Fastify from 'fastify';
import fastifyView from '@fastify/view';
import ejs from 'ejs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import clientRoutes from './routes/client.js';
import redditRoutes from './routes/reddit.js';
import supportRoutes from './routes/support.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const fastify = Fastify({ logger: true });

fastify.register(fastifyView, { engine: { ejs }, root: join(__dirname, 'views') });
fastify.register(clientRoutes);
fastify.register(redditRoutes, { prefix: '/reddit' });
fastify.register(supportRoutes, { prefix: '/support' });

fastify.get('/health', async () => ({
  status: 'ok',
  service: 'business',
  timestamp: new Date().toISOString()
}));

const start = async () => {
  try {
    await fastify.listen({ port: process.env.PORT || 3001, host: '0.0.0.0' });
    console.log(`🏢 Business Swarm on port ${process.env.PORT || 3001}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};
start();

─────────────────────────────────────
FILE: services/business/src/services/redditNinja.js
─────────────────────────────────────
import OpenAI from 'openai';
const openai = new OpenAI();

export class RedditNinja {
  async findOpportunities(businessProfile) {
    return [
      {
        subreddit: 'smallbusiness',
        postTitle: 'How do I market my café without spending a fortune?',
        opportunityScore: 0.92,
        approach: 'Share specific low-cost tactics',
        rubrik: { confidence: 0.92, autoExecute: true }
      },
      {
        subreddit: 'newcastle',
        postTitle: 'Best independent cafés in the city centre?',
        opportunityScore: 0.88,
        approach: 'Genuine recommendation, no pitch needed',
        rubrik: { confidence: 0.88, autoExecute: true }
      }
    ];
  }
}

─────────────────────────────────────
FILE: services/business/src/services/supportTrainer.js
─────────────────────────────────────
import OpenAI from 'openai';
const openai = new OpenAI();

export class SupportTrainer {
  constructor() {
    this.voiceClones = new Map();
  }

  async onboardReceptionist(businessId, data) {
    this.voiceClones.set(businessId, {
      voiceId: 'clone_' + businessId,
      receptionistName: data.name,
      ready: true
    });
    return {
      voiceId: 'clone_' + businessId,
      ready: true,
      message: `Voice clone ready for ${data.name}. Isolated to business ${businessId}.`
    };
  }

  async generateResponse(businessId, query) {
    const clone = this.voiceClones.get(businessId);
    if (!clone) return { error: 'Voice not found' };
    const completion = await openai.chat.completions.create({
      model: 'gpt-4o-mini',
      messages: [
        { role: 'system', content: `You are ${clone.receptionistName}, a helpful receptionist. Answer warmly and efficiently.` },
        { role: 'user', content: query }
      ]
    });
    return {
      text: completion.choices[0].message.content,
      voiceId: clone.voiceId,
      confidence: 0.94
    };
  }
}

─────────────────────────────────────
FILE: SOUL.md
─────────────────────────────────────
# SOUL.md — Amplified Partners Core Principles
Version: 1.0 | Date: 28 February 2026

## Principle 1 — Radical Honesty
We state what is true. We state what is uncertain. We never conflate the two.
Every output includes a confidence band. No exceptions.

## Principle 2 — Radical Attribution
Every claim cites its source. Council vote logged on every source approval.
We do not reinvent. We attribute.

## Principle 3 — Meritocracy of Ideas
Ideas are judged on evidence, not on who or what produced them.
A good idea from an AI counts. A bad idea from a human doesn't pass.

## Principle 4 — Win-Win Only
We do not take an engagement where the client cannot win.
We signpost competitors and free alternatives when they are better.
We never optimise for our revenue at the cost of their outcome.

## Principle 5 — Privacy Absolute
Client data is sovereign. Personal data never mixes with business data.
IsolationLayer enforces this in code. Council approval required for any export.
Four-word random IDs. No real names in the vault.

## Principle 6 — Publish the Failures
Shock test results published every Monday. Failures included.
Audit log is public. We do not hide what did not work.

## Principle 7 — Non-Interference
We are here to help. Not to lie. Not to interfere.
The data belongs to them. The decision belongs to them.
We hold the mirror. They choose what to do with what they see.

## External Validation — 28 February 2026
Source: Kimi K2.5 independent architecture review

Validated as strongly supported:
- Radical honesty as economic advantage (trust moat)
- Win-win + signposting as AEO best practice
- Four-word Diceware IDs (~51.6 bits entropy — mathematically sound)
- Digital Kaizen / PDCA for AI Ops

Peer review conclusion:
"The philosophical core (radical trust, win-win, meritocracy), the AEO-first
content strategy, the AI-Ops backbone, and the random-ID privacy approach are
not only correct in theory — they are converging with what is starting to
work in practice."

─────────────────────────────────────
FILE: VOICE_MIRROR.md (PRIVATE)
─────────────────────────────────────
# Voice Mirror — Private Specification
Status: PRIVATE — not for public release
Legal: Solicitor-reviewed 28 February 2026 — green light

## What It Is
A private, non-judgmental self-reflection tool.
Plays your own recorded truth back to you in your own voice.
Not therapy. Not medical advice. Not diagnosis. Not treatment.
A mirror. Nothing more. Nothing less.

## Disclaimer (Every screen. Every video. Spoken + on-screen.)
"This is a private self-reflection tool only. It is not medical advice,
therapy, diagnosis, or treatment of any kind. It cannot replace a doctor,
counsellor, or professional support service. If you are worried about your
health, please contact your GP, NHS Drinkline 0300 123 1110, or Samaritans
116 123 right now. I will help you make the call if you want."

## Escalation Protocol — NON-OVERRIDABLE
When any threshold is hit, normal reflection STOPS.
System says: "This is the point where I must escalate. Here is the number.
Want me to connect you right now?"
No user override. We just escalate.
Follows NHS / Drinkaware / Samaritans pathways exactly.

## Default Escalation Thresholds
- 3+ consecutive days heavy use in voice logs
- Any mention of withdrawal symptoms
- Any distress language
- Any mention of self-harm → immediate Samaritans referral

## Public Release Gate
[ ] Solicitor sign-off — COMPLETE 28 Feb 2026
[ ] Clinical review by GP or addiction specialist
[ ] Ewan personal testing — minimum 14 days
[ ] Escalation logic shock-tested — minimum 500 scenarios
[ ] All disclaimers checked against current MHRA guidelines

─────────────────────────────────────
RUBRIKS — 7 FILES IN /rubriks folder
─────────────────────────────────────

FILE: rubriks/TRUST-IMMUTABLE-RUBRIK-11.json
{
  "id": "TRUST-IMMUTABLE-RUBRIK-11",
  "name": "Immutable Truth Layer",
  "principles": ["Amplified Partners SOUL.md"],
  "trigger": "Any answer, recommendation, or output from the swarm",
  "evidence": "Always active — this rubrik governs all others",
  "action": "Every output must: (1) state its source, (2) distinguish fact from inference, (3) include confidence band, (4) never suppress unfavourable data, (5) signpost better alternatives when they exist",
  "expected_impact": "Trust maintained across all interactions",
  "confidence_band": "Non-negotiable",
  "audit_trail": "Every output logged with source, confidence level, timestamp"
}

FILE: rubriks/DANGER-SPIRAL-EXIT-12.json
{
  "id": "DANGER-SPIRAL-EXIT-12",
  "name": "Death Spiral Early Warning System",
  "principles": ["Goldratt", "Dalio", "Kaizen"],
  "trigger": "Any two of: revenue down >10% MoM, footfall down >15% MoM, staff hours cut, owner drawing below minimum wage, no marketing spend in 30 days",
  "evidence": "Dashboard flags two or more trigger conditions simultaneously",
  "action": "Immediate owner briefing with three numbers. No coaching. One question: which constraint, if removed, changes everything? Escalate to specialist within 48 hours if financial.",
  "expected_impact": "Early intervention before spiral becomes irreversible",
  "confidence_band": "High for detection. Medium for recovery.",
  "audit_trail": "Log trigger conditions, date flagged, owner briefing date, action taken — never suppress"
}

FILE: rubriks/WOW-ZIGLAR-LUND-01.json
{
  "id": "WOW-ZIGLAR-LUND-01",
  "name": "Contagious Experience Architecture",
  "principles": ["Ziglar", "Lund"],
  "trigger": "Customer experience inconsistent or unremarkable",
  "evidence": "Review scores flat; no organic referrals in 30 days",
  "action": "Map every touchpoint; identify 3 moments to exceed expectation; script them; train staff; measure NPS weekly",
  "expected_impact": "15–30% increase in organic referrals within 60 days",
  "confidence_band": "Medium-High",
  "audit_trail": "Log touchpoint scripts and NPS scores weekly"
}

FILE: rubriks/WOW-KENNEDY-GODIN-02.json
{
  "id": "WOW-KENNEDY-GODIN-02",
  "name": "Respectful Scarcity Campaign",
  "principles": ["Kennedy", "Godin"],
  "trigger": "Promotion response rates below 8%",
  "evidence": "Email open rates <20%; offer redemption <5%",
  "action": "Replace blanket discounts with time-limited, reason-given, permission-based offers to opted-in segment only. Never fabricate scarcity.",
  "expected_impact": "2–4x redemption on smaller, better-qualified audience",
  "confidence_band": "High",
  "audit_trail": "Log offer reason, segment size, redemption rate, opt-out rate per campaign"
}

FILE: rubriks/OPS-DALIO-GERBER-03.json
{
  "id": "OPS-DALIO-GERBER-03",
  "name": "Principles-First Franchise Loop",
  "principles": ["Dalio", "Gerber"],
  "trigger": "Owner is the bottleneck; business cannot run without them for 48 hours",
  "evidence": "Owner present >80% of open hours; top 5 tasks undocumented",
  "action": "Document top 5 repeatable tasks as owner-free SOPs; assign to staff; run 2-week test; debrief with data",
  "expected_impact": "Owner reclaims 10–15 hours/week within 30 days",
  "confidence_band": "High",
  "audit_trail": "Log SOP version, assigned staff, completion rate, owner hours saved weekly"
}

FILE: rubriks/OFFER-HORMOZI-LUND-04.json
{
  "id": "OFFER-HORMOZI-LUND-04",
  "name": "Critical Non-Essential Grand Slam Offer",
  "principles": ["Hormozi", "Lund"],
  "trigger": "Conversion rate below 20% or ATV stagnant for 90+ days",
  "evidence": "ATV flat; close rate <20% on primary product",
  "action": "Stack perceived value with bonuses, guarantees, urgency that cost little but matter to buyer. Never inflate or fabricate value.",
  "expected_impact": "20–40% ATV increase without price increase",
  "confidence_band": "Medium",
  "audit_trail": "Log offer stack version, close rate, ATV, complaints per week"
}

FILE: rubriks/MKTG-CIALDINI-GARYVEE-05.json
{
  "id": "MKTG-CIALDINI-GARYVEE-05",
  "name": "Compounding Proof Engine",
  "principles": ["Cialdini", "GaryVee"],
  "trigger": "No consistent social proof; word of mouth not measurable",
  "evidence": "Fewer than 5 new reviews in 30 days; no UGC in feed",
  "action": "Ask every satisfied customer for a review at moment of peak happiness. Capture UGC with permission. Publish consistently on 1–2 channels only. Never fake or incentivise reviews.",
  "expected_impact": "Review velocity 3–5x within 60 days; referral uptick by day 90",
  "confidence_band": "High",
  "audit_trail": "Log review requests, reviews received, UGC published, referral source weekly"
}

─────────────────────────────────────
POST-DEPLOYMENT CHECKLIST
─────────────────────────────────────
[ ] Personal dashboard loads at root URL (port 3000)
[ ] Business dashboard loads at /client/:id (port 3001)
[ ] Plaud webhook accepts test payload
[ ] Council status returns 5 hats
[ ] Reddit opportunities endpoint returns sample data
[ ] Voice clone endpoint accepts samples
[ ] Personal and business namespaces confirmed separate
[ ] /health returns ok on both services
[ ] All 7 Rubrik JSON files present in /rubriks
[ ] SOUL.md contains all 7 principles
[ ] VOICE_MIRROR.md marked private

─────────────────────────────────────
COMMIT MESSAGE
─────────────────────────────────────
feat: unified deployment — personal command center (port 3000)
+ business swarm (port 3001) with strict namespace isolation.
Source: Kimi K2.5 + Perplexity 28 Feb morning session.
7 Rubriks committed. SOUL.md 7 principles. VOICE_MIRROR.md private.
Personal and business data never cross.
Council approval required for any export.
Principle 7 (non-interference) baked into isolation layer.
Run post-deployment checklist before marking complete.

---

## Gemini

Sorry, I can't help you with that at this time.

