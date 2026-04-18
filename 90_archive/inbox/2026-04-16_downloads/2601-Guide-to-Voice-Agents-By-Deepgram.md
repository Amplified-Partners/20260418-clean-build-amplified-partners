**EBOOK**

The Definitive Guide to Voice AI Agents 

Table of Contents Chapter 0  
2 

Chapter 1 Chapter 2 Chapter 3 Chapter 4 

**Introduction** 

**Setting the Stage** 

Why Voice Agents Now **5** About This Guide **5** Scope and Structure **6**   
**Foundations:** 

**How Voice Agents Work** 

Anatomy of a Voice Agent **8** Voice Agent Stack **11** 

Production-Ready **14** Stack: Operational Layer 

Architectural Approaches **16** to Building Voice Agents 

Overview of Build **17** Approaches 

Comparing the **19** Approaches 

Guidance on Choosing **20** an Approach   
**System Design** 

**and Architecture** 

Voice UX Design **22** Principles 

Reasoning and **29** Orchestration Layer 

Telephony Runtime **33** Architecture 

Multilingual Strategies **38** and Localization   
**Deployment**  

**and Runtime** 

Deployment and Runtime **43** Architecture 

Hosting Models and **43** Regional Placement 

Scaling and Concurrency **44** 

Resilience and Graceful **44** Degradation 

Observability and Runtime **45** Visibility 

Edge and Offline **45** Deployments 

Security as a Runtime **46** Baseline 

Summary **46**   
**Operational** 

**Excellence** 

Reliability, Testing, **48** and Evaluation 

Observability and **51** Monitoring   
3 

Table of Contents 

Chapter 5 Chapter 6 Chapter 7 Chapter 8 Chapter 9

**Compliance  and Governance**   
**Applied** 

**Architectures**   
**The Future Getting Started Appendices of Voice AI** 

Compliance and Data **55** Control 

Regional Deployment and **55** Data Residency 

Secure Transmission **56** and Authentication 

Data Retention, Redaction, **57** and Minimization 

User Authentication, **57** Consent, and Disclosure 

Logging, Auditability, **58** and Governance 

Putting Compliance **58** into Practice 

Content Safety **59** and Guardrails 

Safety Governance and **63** Continuous Improvement 

Operational Realities: Pitfalls **63** and Success Factors 

Reference Architectures **67** (Topologies)  

Tier 1 – Single-Agent  **67** Foundations 

Tier 2 – Specialized and **70** Localized Agents 

Tier 3 – Integrated and **73** Distributed Systems 

Tier 4 – Low-Level and **77** Edge Implementations 

Synthesis: The Architecture **79** Continuum 

Ecosystem Patterns **80** (Integrations)  

The Next Architectural **88** Shift 

Neuroplex Architecture **89** Overview 

Implications for Builders **91**   
Recap: A Practical **94** Framework for Voice Agents 

Choosing Your Build Path **95** Your Open Build Path **95** Take the First Steps **96** 

Glossary of Key Terms **98** 

Quick Reference: Deepgram **101** APIs and SDKs 

Common Failure Modes **103** in Real-Time Voice Agents   
CHAPTER 0

Introduction Setting the Stage   
CHAPTER 0: INTRODUCTION \- SETTING THE STAGE 5

Why Voice Agents Now 

Voice is no longer a novelty in human–computer interaction. It has become a  foundational interface. This shift is driven by advances in real-time AI, growing  production adoption, and the inherent complexity of spoken interaction. 

Recent breakthroughs across the stack have made high-quality voice agents  viable at scale. Large language models now support low-latency, multi turn reasoning. Synthetic speech has become natural and expressive. Most  importantly, new approaches to conversational speech recognition have solved  one of voice UX's longest-standing challenges: accurately determining when  a speaker has finished talking. This shift, driven by infrastructure-level  research, has fundamentally changed how voice agents manage turn-taking,  timing, and responsiveness. 

At the same time, market adoption has accelerated. Organizations with high  volumes of inbound and outbound conversations are deploying voice agents  to extend availability, reduce staffing pressure, and improve responsiveness.  

Falling costs for real-time AI models, combined with more composable  infrastructure, have lowered the barrier to entry. What once required  significant in-house engineering effort can now be built with modern APIs  and specialized platforms. 

The result is a clear inflection point: the technology is mature, demand is real,  and the systems involved are complex enough to require serious engineering.  Voice agents are now production-grade, real-time software systems.   
About This Guide  

This guide is Deepgram's definitive, opinionated playbook for designing,  deploying, and operating real-time voice agents. We wrote this as practitioners,  for practitioners. It reflects our perspective on how voice agents should be  architected and run in production. 

While many resources explain how to call a speech API or connect to  a telephony provider, far less guidance exists on how to design voice agents  as end-to-end systems. Voice agents are distributed, low-latency systems  that must coordinate perception, reasoning, timing, and response under  real-world constraints. This guide focuses on that system-level view. 

This guide is for developers and engineers building voice agents, architects  evaluating design and deployment trade-offs, and technical product  leaders responsible for reliability, scalability, and user experience. If you are  implementing or evaluating a voice agent in a real production environment,  this guide is for you.   
CHAPTER 0: INTRODUCTION \- SETTING THE STAGE 6

Scope and Structure 

The guide is organized into modular sections that can be read linearly  or used as a reference: 

• **Foundations** explains how voice agents work, their core components,  and why real-time voice systems are uniquely challenging. 

• **System Design and Architecture** covers agent behavior, real-time UX,  reasoning logic, telephony integration, and multilingual considerations. 

• **Operational Excellence and Governance** focuses on reliability, testing,  metrics, monitoring, compliance, and guardrails. 

• **Applied Architectures and Patterns** presents reference architectures and  real-world integration patterns. 

• **The Future of Voice AI** explores emerging directions, including Deepgram's  Neuroplex research on speech-to-speech systems. 

• **Getting Started** outlines practical next steps and resources for  different personas. 

• **Appendices** provide reference material such as glossaries, event flows,  and troubleshooting guidance. 

Throughout the guide, we emphasize how the pieces fit together at a system  level. You will not find exhaustive API syntax here. Product documentation  already serves that purpose. Instead, this guide helps you build a clear mental  model of real-time voice agents: how they work, how to design them well, how  to operate them in production, and where the technology is headed. 

With that foundation in place, we begin by examining how voice agents are  constructed and how they behave in practice.   
CHAPTER 1 

Foundations 

How Voice Agents Work  
CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 8

Anatomy of a Voice Agent 

Understanding voice agents begins with examining their fundamental structure  and behavior. This section breaks down what voice agents are, how they  operate, and why building them presents unique challenges. 

**What Is a Voice Agent?** 

A voice agent is an autonomous, real-time conversational system that listens,  reasons, and responds using natural spoken language. Users interact with it  through speech, typically over a phone call, device microphone, or embedded  application, and receive spoken responses in return. 

Voice agents differ from traditional IVR systems, which rely on prerecorded  prompts and rigid menus. They also differ from text-based chatbots, which  operate without real-time audio constraints. Unlike those systems, voice  agents must handle continuous audio streams, ambiguous turn boundaries,  and strict latency requirements while maintaining a natural conversational flow. 

A voice agent is a real-time system designed for spoken interaction under  real-world conditions. 

**The Conversational Loop** 

At a behavioral level, every voice agent follows a continuous conversational  loop that mirrors human dialogue: 

**Listen → Understand → Reason → Respond → Speak** 

These stages map to distinct system functions: 

• **Listen:** Capture incoming audio from the user in real time. 

• **Understand:** Extract meaning and detect conversational signals such  as pauses and end-of-turn. 

• **Reason:** Interpret intent and decide on a response or action. • **Respond:** Generate spoken output. 

• **Speak:** Stream audio back to the user and resume listening.   
CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 9

**Listen** 

Capture audio input  from the user 

**Understand** Extract meaning from audio 

**Reason** 

Process context and  generate response 

**Respond** 

Formulate appropriate  reply content 

**Speak** 

Deliver audio  response to user 

**Figure 1.1: The Conversational Loop Flow** 

The five core stages of voice agent interaction form a continuous cycle,  with each stage feeding into the next.   
In production systems, this loop does not operate as a strict, turn-by-turn  pipeline. The stages overlap and run concurrently. An agent may begin  reasoning before a user has finished speaking, or start speaking while the  remainder of a response is still being generated. This **streaming, event-driven  behavior** is what gives voice interactions a natural rhythm. 

This loop describes how a voice agent behaves. Implementing it reliably under  real-world conditions is where complexity arises.   
CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 10

**Why This Is Hard** 

Building a voice agent that feels truly conversational is difficult because real world interaction is not a controlled environment. People interrupt each other,  audio quality varies, latency introduces awkward pauses, and individual AI  components do not inherently share timing or state. What appears simple  quickly becomes a real-time systems problem. 

The core challenges are: 

**• Real-time orchestration of multiple systems** 

A voice agent consists of multiple independently operating components  such as speech recognition, reasoning, synthesis, and audio I/O, each  producing asynchronous events. Without strong orchestration, timing  mismatches cause premature cutoffs, delayed responses, or the agent  speaking at the wrong moment. 

**• Latency compounding across stages** 

Small delays at each stage of the conversational loop accumulate into  perceptible pauses. To improve responsiveness, overlap work, react to  partial signals, and minimize handoff overhead. In voice interaction, every  100 milliseconds matters. 

**• Interrupt-driven interaction and turn-taking** 

Users interrupt responses, correct themselves mid-utterance, and  change intent while the system is speaking. A production agent must  detect these events instantly, stop or adjust output, and resume listening  without losing context. 

**• Synchronizing speech and reasoning for natural rhythm** When reasoning takes time, the agent must manage perceptible states  such as listening, thinking, and speaking. Without awareness of its  own timing, systems produce awkward pauses, self-interruptions, or  repetitive filler. 

Together, these constraints make it insufficient to treat voice agents as  sequential pipelines. Human-like interaction requires an **event-driven,  interrupt-aware architecture** that treats **timing and partial signals as first class inputs**. 

The next section examines the systems that make this behavior possible,  starting with the core technologies in the voice agent stack.   
CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 11 

Voice Agent Stack 

We can now examine what a voice agent is actually built from. While  implementations vary, modern voice agents share a common set of  architectural building blocks. These components exist to support the  conversational loop described earlier and to operate reliably under  real-time conditions. 

The architecture described in this section represents cascade-based voice  agents: systems that convert speech to text, process that text through a  reasoning layer, then synthesize responses back to speech. While the industry  is actively developing streaming speech-to-speech (S2S) architectures that operate on continuous audio representations without text intermediaries,  cascade systems remain the dominant production pattern. They offer  mature tooling, interpretable debugging boundaries, and proven operational  characteristics. 

For a detailed exploration of S2S architectures and Deepgram’s Neuroplex research, see Chapter 7: The Future of Voice AI. 

**The Stack Concept** 

At a high level, a voice agent stack can be divided into two layers. 

The **core conversational layer** contains the components required to carry  out a real-time spoken interaction at all. This layer is responsible for listening,  reasoning, and speaking, and for coordinating those functions continuously.  Without it, there is no conversational agent. 

The **operational layer** sits above the core and becomes essential as systems  move toward production. This layer handles concerns such as scalability,  reliability, observability, integration with external systems, and compliance.  These components do not change how the agent converses, but they  determine whether it can function dependably in real-world deployments. 

Put another way, the core layer answers the question: **Can the agent hold  a conversation?** 

The operational layer answers: **Can that conversation run at scale, under  load, and within real-world constraints?**  
CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 12

The sections that follow break down these layers in more detail, starting  

with the minimal set of components required for a functioning voice agent,  

and then expanding to the additional capabilities needed for production-grade  systems. Where relevant, we reference how Deepgram provides infrastructure  across both layers. 

**Operational Layer**   
**Figure 1.2: Voice Agent Stack Architecture** 

The two-layer architecture separates production concerns  (Operational Layer) from real-time interaction capabilities (Core Conversational Layer). 

**Memory  & Context**   
**Observability & Telemetry** 

Enables 

**Core Conversational Layer**   
**Integration  Layer**   
**Compliance  & Security** 

**Audio I/O & Transport**   
**Speech-to-Text & CSR**   
**Language Model / Reasoning**   
**Text-to-Speech Orchestration Runtime**   
CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 13

**MVP Stack: Functional Core** 

At the foundation of every voice agent is a real-time conversational core. These components are non-negotiable.  

Without all of them working together, a system may demonstrate basic functionality but will not behave like a true  

conversational agent. 

| Component  | Role in the System  | Deepgram Example |
| :---- | :---- | :---- |
| **Audio I/O and Transport**  | Streams audio into and out of the system with low  latency. | Real-time, bidirectional audio streaming via **SDKs** and APIs for web, mobile, and  telephony environments. |
| **Speech-to-Text and Conversational   Speech Recognition** | Transcribes speech and detects conversational  boundaries such as end-of-turn. | **Flux** unifies transcription and turn detection in a single conversational model optimized  for real-time agents. |
| **Language Model or Reasoning Engine**  | Interprets intent and determines the agent’s response or action. | Model-agnostic LLM integration optimized for streaming input and incremental output. |
| **Text-to-Speech**  | Converts responses into spoken audio and  streams output to the user. | **Aura-2** provides low-latency, streaming speech synthesis for real-time interaction. |
| **Orchestration Runtime**  | Coordinates timing, state, and interaction across  all components. | **Voice Agent API** manages real-time orchestration, interruption handling, and stream  control within a single session. |

CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 14Together, these components form the minimum viable voice agent. Early **Production-Ready Operational Components**   
implementations often stitched these pieces together manually using multiple  APIs, which worked for demos but introduced unnecessary latency and  coordination issues. Modern platforms increasingly integrate parts of this core  to reduce handoffs and enable streaming, event-driven behavior by default. 

Production-Ready Stack:  

Operational Layer 

While the functional core enables conversation, production deployments  introduce additional requirements. Voice agents must operate reliably at  scale, integrate with business systems, and meet regulatory and security  

expectations. These concerns are addressed by the operational layer  of the stack. 

| Component  | Role  | When Needed  | Deepgram Example |
| :---- | ----- | ----- | :---- |
| **Memory   and Context  Management** | Maintains   conversational  state across   turns or   sessions. | Required for   multi-turn or   personalized  agents. | Session-level context, designed   to integrate with external stores you  manage for long-term memory. |
| **Observability  and Telemetry** | Measures   latency,   quality, and   system health. | Required for   any production  deployment. | Real-time event streams that plug into  your monitoring stack to support quality  tracking and external observability. |
| **Integration   Layer** | Executes   actions in   external   systems. | Required for   task-oriented  agents. | **Structured function calls** that integrate  external logic into the conversational flow. |
| **Compliance   and Security  Controls** | Enforces   privacy,   access control,  and regulatory  requirements | Required for   enterprise   and regulated  environments. | **Regional deployment options**, isolated  infrastructure, **short-lived credentials**,  and redaction support. |

CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 15

These components do not change how an agent speaks or listens, but they  determine whether the system can be trusted in real-world environments. Most  successful deployments begin with the functional core and progressively add  operational capabilities as they scale. 

With the components of the voice agent stack defined, the remaining question  is how these pieces should be assembled into real systems. There is no single  correct approach. Different teams make different architectural trade-offs  depending on their requirements, constraints, and appetite for control. 

**Deepgram’s Opinionated View** 

Deepgram’s perspective is that real-time voice agents perform best when built on an integrated, streaming-first speech infrastructure rather than a  loosely chained set of APIs. Speech recognition, speech synthesis, and audio  transport should operate as a unified layer, coordinated by a purpose-built  orchestration runtime. 

Optimizing the speech loop as a whole reduces latency, minimizes handoffs,  and enables faster transitions between listening, reasoning, and responding.  This produces more responsive and natural interactions than optimizing  individual components in isolation.   
At the same time, Deepgram does not advocate for a monolithic stack. Teams  should remain free to choose their own language models, tools, and business  logic. While reasoning layers may vary by use case, the speech layer must  be unified and streaming-first to support interruption handling, precise timing,  and low-latency response. 

Deepgram supports different abstraction levels by offering flexible  APIs that allow teams to decide how much of the system they want to  manage themselves. 

The next section examines how teams assemble these components in  practice. There are multiple valid approaches, each with trade-offs in  control, complexity, and abstraction.   
CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 16

Architectural Approaches  

to Building Voice Agents 

While all voice agents rely on the same core components, teams differ 

in how they assemble those components. The primary differences come  

down to **where orchestration logic lives** and **how much abstraction**  

**versus control** a team prefers. 

At one end of the spectrum, teams assemble everything themselves  

using low-level APIs. At the other, teams adopt fully managed platforms  

where voice is one feature in a broader system. Most real-world  

implementations fall somewhere in between. 

Rather than rigid categories, these approaches represent  

**common architectural patterns**. Teams often move between  

them as requirements evolve.   
CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 17

Overview of Build Approaches 

We can broadly group voice agent architectures into four patterns,  

ordered from maximum control to maximum convenience. 

**The Four Build Approaches** 

| Build Approach  | Description  | Examples  | Deepgram Role |
| :---- | :---- | :---- | :---- |
| **DIY Frameworks (Custom Stack)**  | Teams assemble their own pipeline using  separate STT, LLM, and TTS components and  implement orchestration themselves or via open source frameworks. | LiveKit, Pipecat, custom pipelines  | Provides foundational STT and TTS APIs  and SDKs used directly within custom   orchestration code. |
| **Unified APIs (End-to-End Runtime)**  | A single real-time API integrates speech,  orchestration, and LLM interaction while still  allowing configuration and custom logic. | Deepgram Voice Agent API,   OpenAI Realtime API | Provides both speech infrastructure and  real-time orchestration in a single runtime,  with model choice and function calling. |
| **Managed Voice Agent Platforms**  | Hosted platforms offering visual builders,  telephony integration, and preconfigured  orchestration for common use cases. | Vapi, Retell  | Often used as the underlying speech layer  powering platform-managed agents. |
| **Enterprise Conversational Suites**  | Large CX platforms where voice is one channel  within a broader, multimodal system. | Cognigy, Kore.ai, Decagon  | Serves as the embedded speech infrastructure,  typically consumed indirectly by end customers. |

CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 18

These approaches trade off control, abstraction, and operational responsibility. None is inherently better than the  

others. The right choice depends on team capability, use case complexity, and long-term ownership preferences. 

More  

Control & Flexibility 

**DIY**   
**Frameworks (Custom Stack)** 

Maximum Control Custom Orchestration 

More  

Abstraction 

**Unified**    
**APIs** 

**(End-to-end Runtime)** 

Balanced 

Managed Runtime 

More  

Abstraction 

**Managed**   
**Platforms** 

**(Voice Agent Platforms)** 

Simplified 

Visual Builders 

More  

Abstraction 

**Enterprise**   
**Suites** 

**(CX Platforms)** 

Maximum Convenience Integrated Solution   
More  

Convenience & Integration 

**Figure 1.3: Build Approaches Comparison** 

The four architectural approaches form a spectrum from maximum control and  flexibility (DIY Frameworks) to maximum convenience and integration (Enterprise Suites).   
CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 19

Comparing the Approaches 

Rather than evaluating each approach in isolation, it is more useful  to compare them along a few consistent dimensions: 

• **Abstraction level** 

DIY approaches offer the lowest abstraction and highest responsibility.  Unified APIs strike a balance by abstracting orchestration while preserving  code-level control. Managed platforms and enterprise suites offer higher  abstraction, often at the cost of flexibility. 

• **Customization and control** 

DIY provides full control over every component. Unified APIs  allow meaningful customization within a managed runtime. Managed  platforms limit customization to supported workflows. Enterprise suites  offer the least direct control over AI behavior but maximize integration. 

• **Latency and performance** 

In theory, DIY can be optimized for specific scenarios. In practice, purpose built unified APIs often achieve better real-time performance due to  integrated streaming and optimized internals. Higher-level platforms may  introduce additional latency depending on telephony and routing layers. 

• **Integration complexity** 

DIY places the full integration burden on the team. Unified APIs reduce  complexity by collapsing the conversational loop into a single integration.  Managed platforms simplify agent construction but may still require  integration with downstream systems. Enterprise suites aim to minimize  integration by providing a comprehensive solution. 

• **Compliance and governance** 

DIY offers maximum flexibility but shifts compliance responsibility to  the team. Unified APIs can provide strong governance options when  deployed in controlled environments. Managed platforms are typically  SaaS-first. Enterprise suites usually offer the most comprehensive  compliance posture.   
CHAPTER 1: FOUNDATIONS \- HOW VOICE AGENTS WORK 20

Guidance on Choosing an Approach 

The right architectural approach depends on priorities and constraints: 

• **Choose DIY** if you require maximum control, need to self-host components,  

or must integrate proprietary models. This approach demands strong  

engineering resources and careful real-time systems design. 

• **Choose a unified API** if you want a balance of speed, flexibility, and  

performance. This is often the best fit for teams building production  

voice agents who want to avoid implementing streaming orchestration  

themselves while retaining control over models and logic. 

• **Choose a managed platform or enterprise suite** if speed to deployment,  

minimal coding, or enterprise procurement requirements dominate. These  

approaches work well for standardized use cases or organizations that  

prefer integrated vendor solutions. 

Many teams mix approaches over time. Some prototype with managed  

platforms and later transition to unified APIs or DIY stacks. Others embed  

unified APIs within larger platforms or enterprise workflows. Deepgram is  

designed to support this spectrum, allowing teams to adopt the abstraction  

level that best matches their needs.   
CHAPTER 2 

System Design and Architecture  
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 22

Voice UX Design Principles 

Voice user experience design sits at the intersection of linguistics, cognition,  and real-time systems engineering. A voice agent does not merely transcribe  speech and return answers. It must manage timing, tone, and conversational  expectations so that interaction feels cooperative rather than transactional. 

Across academic research and production deployments, one conclusion is  consistent: **the quality of a voice agent is determined less by what it says  than by *when* and *how* it says it**. Micro-timing, interruption handling, and  perceptual cues shape whether users trust the system or abandon it. 

Deepgram’s approach to voice UX reflects this reality. We view voice interaction as a real-time control problem, not a text interface with audio  attached. From that perspective, effective voice UX emerges from three  interdependent design layers: **reactive**, **predictive**, and **adaptive** behavior.  These layers govern how an agent responds in the moment, anticipates intent,  and adjusts tone over time. 

**Reactive Design: Establishing Conversational Rhythm** 

Human conversation follows a surprisingly strict rhythm. Turn gaps that are too  short feel interruptive; gaps that are too long feel inattentive. Reactive design  focuses on reproducing this rhythm in software. 

The foundation is **accurate turn-taking**. A voice agent must reliably determine  when a user has finished speaking while tolerating natural pauses and  hesitations. In production systems, this requires conversational speech  recognition that models timing and intent, not just words. 

Deepgram’s conversational speech models are designed around this principle. Rather than treating end-of-speech as a fixed silence threshold, they infer  turn completion from conversational context, allowing the system to respond  quickly without cutting users off. This precision enables agents to maintain  human-like pacing even under noisy or ambiguous conditions. 

When downstream reasoning or data access introduces delay, reactive  design calls for **explicit acknowledgment**. Short, low-commitment cues signal  attentiveness without breaking conversational flow.   
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 23 

Conceptually, the behavior looks like this: 

`if user_turn_complete:` 

`prepare_to_respond()` 

`if response_is_delayed:` 

`acknowledge_progress()` 

`if user_resumes_speaking:` 

`immediately_yield_control()` 

The goal is reassurance through restraint. Silence creates uncertainty, while  brief acknowledgment maintains trust. 

Reactive design establishes the baseline rhythm of interaction. Without it,  predictive and adaptive behaviors cannot compensate for broken pacing. 

**Predictive Design: Reducing Perceived Latency** 

Once basic rhythm is stable, voice agents can move beyond reaction to  **anticipation**. Predictive design allows the system to infer intent before a user  finishes speaking and begin preparing a response in parallel. 

**Research on incremental dialogue processing** shows that overlapping  listening and reasoning can dramatically reduce perceived latency.  Deepgram’s streaming-first architecture enables this behavior by emitting early conversational signals that allow downstream systems to act speculatively.   
The core pattern is speculative preparation with safe cancellation: 

`if early_intent_inferred:` 

`begin_drafting_response()` 

`if user_continues_or_changes_direction:` 

`discard_draft()` 

`if turn_is_confirmed_complete:` 

`finalize_and_speak()` 

This overlap shortens response time without increasing error rates, provided  the system can cancel cleanly when predictions are wrong. 

Predictive design also shapes how speed is perceived. Users judge  responsiveness not by absolute latency, but by feedback continuity. Subtle  backchannel cues, brief affirmations, or tonal acknowledgment during  processing can make identical systems feel significantly faster.  

Deepgram’s opinion is clear here: latency is as much a UX problem as an infrastructure problem. Optimizing models alone is insufficient if orchestration  does not allow early signals to flow through the system. 

**Adaptive Design: Tone, Persona, and Context Awareness** 

Static voice personas break down quickly in real-world interaction. Effective  agents adjust tone, pacing, and phrasing based on context while maintaining  a consistent identity.  
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 24 

Adaptive design draws on two signal classes: 

1\.  Input-side context, such as hesitation, interruptions, repeated questions,  or unstable recognition 

2\.  Output-side expressiveness, including prosody, pacing, and emphasis 

Deepgram’s speech models expose timing and stability signals that can be used to infer conversational friction. For example, rapidly changing partial  transcripts or delayed stabilization often correlate with user uncertainty or  frustration. These signals can guide downstream response shaping without  

explicit sentiment classification. 

On the output side, modern expressive synthesis allows tone modulation  without brittle markup. Deepgram’s **Aura-2** voices are designed to produce  consistent, professional speech while adapting pacing and emphasis  naturally from text and conversational context. Developers influence tone  primarily through response construction and persona choice, rather than  micromanaging synthesis parameters. 

**Vida**’s healthcare voice agents process tens of thousands of calls daily for appointment scheduling and medication adherence, where empathetic  tone directly correlates with task completion. Their architecture prioritizes  alphanumeric accuracy for dates and medication names without SSML  markup, demonstrating that entity rendering precision is a UX requirement,  not a feature.   
The guiding principle is **contextual sensitivity, not emotional mimicry**.  The agent should sound calm when users are rushed, reassuring when  they hesitate, and concise when confidence is high. 

**Conversational Framing and Meta-Communication** 

Humans constantly talk **about** the conversation itself. These meta communicative cues manage expectations and keep dialogue cooperative. 

In voice UX, meta-communication reframes latency or uncertainty as progress  rather than failure. Compare silence to a phrase like “I’m checking that now.” The latter maintains engagement by explaining what the system is doing. 

Meta-communication operates across layers: 

| Layer  | Responsibility  | Example  |
| :---- | :---- | :---- |
| **Policy**  | Decide when to acknowledge delay  | “Acknowledge if reasoning exceeds  one second” |
| **Orchestration**  | Detect slow operations  | Trigger acknowledgment |
| **Timing**  | Ensure cues respect turn ownership  | Never interrupt user speech |
| **Synthesis**  | Convey reflective tone  | Slight pause, measured delivery |

The intent of meta-communication is transparency. When done well, it builds  trust by making the system’s internal state legible to the user.  
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 25

**Repair and Recovery** 

No voice agent avoids errors. Reliability depends on how gracefully  the system recovers. 

Effective repair follows a consistent pattern: 

• Acknowledge uncertainty 

• Narrow ambiguity 

• Confirm resolution 

Conceptually: 

`if confidence_is_low:` 

`ask_for_clarification()` 

`if user_corrects_agent:` 

`prioritize_user_input()` 

`confirm_updated_understanding()` 

Interruptions during agent speech are especially important signals.  A system that immediately yields control reinforces that the user remains  the primary speaker. 

Deepgram’s event-driven speech infrastructure is designed to support this behavior, allowing playback cancellation and rapid listening resumption without  losing conversational state. 

When recovery is transparent and cooperative, users perceive the agent  as attentive rather than flawed. 

**Multimodal Reinforcement and Cognitive Load** 

Voice interaction often coexists with visual or tactile feedback. Coordinating  these channels reduces cognitive load by reinforcing system state through  multiple signals. 

Auditory acknowledgments can be paired with visual indicators such as  progress animations or status lights, all synchronized to conversational timing.  The critical requirement is **temporal alignment**. When cues drift out of sync,  trust erodes. 

As multimodal interfaces mature, the best experiences will feel unified  rather than layered, with users perceiving responsiveness rather than  individual channels.   
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 26 

**Perspective and Path Forward** 

Voice UX is shifting from scripted interaction toward real-time collaboration.  Anticipatory processing, adaptive prosody, and event-driven orchestration  are redefining how agents listen and respond. 

Deepgram’s position is that voice UX quality emerges from optimizing the entire conversational loop, not isolated components. Low-latency speech  models, expressive synthesis, and fine-grained timing signals enable agents  that feel cooperative rather than mechanical. 

As these systems evolve, tone and timing will adapt fluidly to live context  rather than fixed personas. Measuring and improving these behaviors in  production is the next challenge, which we address in the following section. 

**Interaction and UX Architecture** 

If voice UX principles define **how an agent should feel**, interaction architecture  defines **how that feeling is produced in real time**. This section focuses on the  systems beneath the conversation: audio pipelines, event flow, interruption  handling, and state signaling. A well-architected voice agent does not  guess what is happening. It reacts deterministically to real-time signals  and coordinates perception, reasoning, and output under latency and  concurrency constraints.   
**Real-Time Audio Pipeline** 

Every voice interaction begins with audio capture, and architectural choices  here directly affect responsiveness. Audio should be streamed in small,  consistent frames rather than buffered in large chunks. 

Frame sizes in the 20–50 millisecond range strike a balance between reactivity and network efficiency. Smaller frames increase responsiveness but raise  overhead; larger frames reduce overhead but introduce audible lag. 

Encoding formats should match the environment. Telephony typically uses  8 kHz mono µ-law or A-law PCM, while browsers and mobile devices  commonly support 16 or 48 kHz PCM. On the output side, synthesized  speech should be streamed incrementally and buffered just enough to prevent  playback gaps. A short jitter buffer around 100 milliseconds is usually sufficient  to smooth minor network variation without adding perceptible delay. 

Deepgram’s **SDKs** handle audio chunking, format negotiation, and stream  continuity automatically, allowing developers to focus on interaction logic  rather than transport mechanics. This abstraction matters because timing  errors at the audio layer propagate upward into turn-taking and UX failures  
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 27 

**Event-Driven Turn Management** 

Turn-taking is the backbone of conversational UX. Humans rely on implicit  

timing cues; systems require explicit events. A production voice agent should  never poll for state. It should react to a stream of conversational events. 

Key transitions such as speech start, speech end, interruption, and resume  must be handled as asynchronous signals. These events drive both backend  behavior and user-facing feedback. For example, detecting speech start  should immediately cancel any active playback, while detecting turn  completion should trigger reasoning or acknowledgment. 

**Flux** simplifies this layer by collapsing traditional ASR and VAD stacks  into a single conversational model that emits deterministic turn events: 

• **StartOfTurn**: user begins speaking, cancel playback 

• **EagerEndOfTurn**: medium confidence turn ending, begin  speculative reasoning 

• **TurnResumed**: user continues, cancel speculative work 

• **EndOfTurn**: high confidence completion, finalize response 

Thresholds such as eager\_eot\_threshold and eot\_threshold allow teams  to tune the speed–stability trade-off, and Flux is designed to keep transcripts  highly consistent between eager and final turn boundaries. Speculative  reasoning rarely diverges from the final text. 

Start 

OfTurn   
**Initial** 

**Ready**   
**TurnOngoing** 

**Speaking** 

End 

OfTurn 

Eager 

EndOfTurn 

Turn 

Resumed   
**AwaitingEnd Processing** 

**Figure 2.1: Flux Turn Management State Machine** 

Flux emits deterministic turn events, enabling the orchestration layer  to react to speech boundaries without polling or redundant VAD.  
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 28

When integrating Flux into frameworks like LiveKit, Pipecat, or Vapi,  downstream VAD and turn logic should be disabled. Redundant  detection introduces desynchronization, leading to premature responses  or mid-utterance replies. Flux should be the single source of truth for  conversational boundaries. 

Deepgram’s Voice Agent API builds on these primitives by exposing higher-level lifecycle events such as UserStartedSpeaking, AgentThinking,  AgentStartedSpeaking, and AgentAudioDone. The underlying turn logic  remains Flux-driven, but orchestration complexity is abstracted away, allowing  teams to work at the interaction level rather than the signal-processing level. 

**Interruption and Playback Control** 

Interruption handling, or barge-in, must be supported at both the audio and  orchestration layers. Users expect to interrupt naturally, and systems that fail  here feel rigid and uncooperative. 

Input and output pipelines must run concurrently. When new speech is  detected during playback, output should stop immediately and state should  transition back to listening. Playback cancellation must be explicit so buffers  and downstream components reset cleanly. 

In Deepgram’s Voice Agent API, barge-in is handled automatically. User speech immediately cancels synthesis and playback, and the system re-enters a  listening state. For custom implementations, inbound audio energy or speech  detection flags should directly trigger playback termination. Confirmation    
events such as AgentAudioDone provide a clean boundary for recovery  and next actions. 

The core principle is control. TTS must be interruptible, cancellable, and  replaceable at any moment. Voice agents that cannot stop themselves on  demand will never feel conversational. 

**State Signaling and UX Feedback** 

Conversational UX depends on shared understanding of system state.  Rather than inferring state from timing heuristics, production systems  should emit explicit lifecycle signals. 

Deepgram’s Voice Agent API exposes structured events representing conversation state directly. These signals allow interfaces, analytics, and  monitoring systems to remain synchronized without duplicating logic. 

Treating state signaling as part of orchestration rather than presentation  produces a single source of truth across devices, simplifying debugging  and ensuring feedback aligns with actual system behavior. 

**Multi-Modal and Multi-Device Adaptation** 

Voice agents increasingly operate across browsers, mobile apps, contact center consoles, kiosks, and embedded devices. Conversation logic should  remain platform-agnostic while presentation adapts locally. 

The orchestration layer should emit structured state and content, while  clients decide how to render it. A display-equipped device may visualize    
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 29 

AgentThinking, while a voice-only interface inserts a brief acknowledgment  triggered by the same event. 

This separation allows consistent behavior across environments even  as interfaces evolve. 

**Reliability, Failover, and Session Recovery** 

Voice interactions are long-lived and streaming-based, making transient  failures unavoidable. Reliability architecture ensures that conversations  degrade gracefully rather than collapse. 

Streaming connections should implement reconnection logic with exponential  backoff. When reconnection is possible, prior conversational context should be  restored through injected state rather than restarting cold. When recovery fails,  the system should communicate clearly rather than leaving silence. 

Backend components should monitor audio flow and message cadence.  If input or output stalls, the system should treat it as a failure and initiate  recovery. Where possible, fallback responses or alternate synthesis paths  should preserve conversational continuity. 

The goal is not perfect uptime but resilient interaction. Even under failure,  the agent should remain state-aware, transparent, and responsive. 

**Synthesis: Building Resilient Interaction** 

Interaction architecture is where voice UX becomes real. A production agent   
treats speech boundaries, interruptions, and reasoning delays as first-class  events rather than edge cases. 

By combining event-driven architecture with the UX principles described  earlier, teams can build voice agents that remain fluid under real-world  conditions. The result is steadier rhythm, better recovery, and interactions that  feel attentive because the system never loses track of the conversation. 

Reasoning and Orchestration Layer 

Real-time voice agents succeed or fail in the layer that sits between perception  and speech: the reasoning and orchestration layer. This is where transcripts  become decisions, decisions become actions, and actions return to the  conversation as coherent, timely responses. Unlike text-based systems, this  layer must operate under tight latency constraints, tolerate interruption, and  maintain conversational continuity across asynchronous events. 

In a production voice agent, reasoning coordinates thought, action, and  response within a continuous conversational loop. 

**From Conversation to Decision** 

Effective voice agents deliberately separate **interpretation** from **execution**. 

The model’s role is to understand intent and decide **what should happen**.  Deterministic systems handle **how it happens**. Business rules, validation,  permissions, and side effects belong in code. Open-ended interpretation,  ambiguity resolution, and language generation belong in the model.  
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 30

Most modern architectures therefore follow a **Think → Act** pattern: 

• **Think:** Interpret the user’s intent and decide whether a response requires action. 

• **Act:** Execute that action deterministically and return results to  the conversation. 

Deepgram’s Voice Agent API formalizes this separation by combining streaming transcription, contextual history, and structured function  calling inside a real-time orchestration loop. The result is a system  where language models express intent, but execution remains controlled,  auditable, and interruptible. 

**Function Calling as the Action Interface** 

Function calling is the primary mechanism that allows a voice agent to act in  the real world. Rather than generating free-form text instructions, the model  emits structured requests that the orchestrator executes against external  systems such as databases, APIs, or device controls. 

This design turns the voice agent into an interactive system rather than a  conversational endpoint. The model decides **which** action to take and **with  what parameters**. The orchestrator decides **when**, **whether**, and **how** that  action is executed.   
At a conceptual level, the flow looks like this: 

`# Pseudocode illustrating Think → Act orchestration` 

`on_user_end_of_turn(transcript):` 

`decision = llm.think(` 

`input=transcript,` 

`context=conversation_state` 

`)` 

`if decision.type == “function_call”:` 

`emit_state(“AgentThinking”)` 

`result = execute_function(` 

`name=decision.name,` 

`args=decision.arguments` 

`)` 

`update_context(decision, result)` 

`speak(` 

`llm.respond(` 

`context=conversation_state` 

`)` 

`)` 

`else:` 

`speak(decision.text)`   
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 31

This pattern highlights several opinionated principles: 

• **The model never executes side effects directly** 

• Every action has a clear request and response boundary • Results are reintegrated into conversational context before speech • The system remains explainable and auditable 

**Interruption-Aware Reasoning** 

Voice agents must remain responsive even while actions are in flight.  If a user interrupts mid-task, the system should immediately prioritize  listening over completion. 

Architecturally, this means treating user speech as a higher-priority signal  than pending actions: 

`on_user_started_speaking():` 

`cancel_active_action()` 

`stop_tts_playback()` 

`emit_state(“Listening”)`   
This interruption-first design prevents stale responses, reinforces user control,  and preserves conversational trust. Long-running or asynchronous actions  should always be cancelable or safely ignored if they become irrelevant. 

**Managing Latency and Perceived Responsiveness** 

Tool invocation introduces unavoidable delay. Each function call requires at  least two reasoning steps: one to request the action and one to incorporate  the result. In voice interaction, unmanaged silence during this gap quickly  degrades user trust. 

The orchestration layer should therefore manage perception as actively  as execution: 

• If reasoning or execution exceeds a short threshold, inject a brief  acknowledgment. 

• Treat progress cues as part of conversational flow, not error handling. • Resume normal speech immediately when results arrive. 

Because function calls are discrete messages, they are not inherently  streamable. Execution should occur atomically, while the conversational layer  maintains responsiveness through short, well-timed cues.   
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 32

**Reliability Under Real-Time Conditions** 

Voice agents stress reasoning systems more than text benchmarks suggest.  Long sessions, overlapping turns, noisy input, and repeated tool use increase  prompt complexity and error risk over time. 

Production systems should explicitly evaluate: 

• Correctness of function selection and arguments 

• Stability under interruption and cancellation 

• Time to first spoken response after user turn completion 

• Consistency across long, multi-turn conversations 

Determinism matters more in voice than in chat. Lower decoding temperature  for transactional flows. Track state explicitly in code rather than relying on  probabilistic memory. Log every decision boundary to support debugging,  replay, and audit. 

**Memory and Context Management** 

Conversational coherence depends on disciplined context management. Short-term memory should retain recent turns and relevant function results.  As sessions grow, older content should be summarized or pruned to preserve  context limits without losing intent. Function call history can be retained  explicitly, allowing the agent to reference prior outcomes naturally. Long-term memory requires external storage. Persist only what is necessary,  such as preferences or identifiers, and re-inject selectively at session start.  

Voice agents should remember **what matters**, not everything that was said. 

**Retrieval and Grounded Reasoning** 

For knowledge-intensive domains, retrieval-augmented reasoning grounds  responses in verified data. In voice systems, retrieval belongs in the  orchestration layer, not embedded directly in model prompts. When retrieval is needed: 

• Fetch small, high-relevance snippets 

• Keep retrieval latency low 

• Cache frequent queries 

• Inject results into the next reasoning step 

Deepgram’s Voice Agent API integrates cleanly with external retrieval systems through structured function calls, allowing agents to reason over live enterprise  data without sacrificing real-time responsiveness. 

**Building a Coherent Reasoning Loop** 

The reasoning and orchestration layer defines how a voice agent thinks and  acts in real time. It governs how intent becomes execution, how actions remain  interruptible, and how conversational state stays coherent under latency and  uncertainty. When this layer is well designed, the agent feels responsive,  deliberate, and in control.   
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 33

However, all of this reasoning ultimately operates within a delivery environment  that imposes its own constraints. For many production deployments, that  environment is telephony. 

Phone networks introduce additional complexity: constrained audio formats,  strict timing expectations, call setup and teardown semantics, regional routing,  and reliability requirements that differ fundamentally from browser or device based voice interactions. These constraints shape how audio is streamed, how  interruptions are detected, and how orchestration must behave at the edges  of the system. 

In the next section, we examine telephony architecture for voice agents.  We explore how real-time voice systems integrate with PSTN and SIP  infrastructure, how call state and media streams interact with conversational  loops, and what architectural patterns are required to deliver natural, low latency voice agents over the phone at scale. 

Telephony Runtime Architecture 

Telephony remains one of the most demanding environments for real time voice agents. Inbound customer support, outbound automation,  and compliance-sensitive workflows still rely heavily on PSTN and SIP  infrastructure. Unlike browser or device-based voice, telephony introduces  strict constraints around audio format, latency, session control, and call  lifecycle management.   
Building a production-grade phone agent requires more than connecting  speech models to a phone number. It requires a runtime that can bridge  legacy telephony systems with modern, event-driven voice orchestration  while preserving natural conversational flow.   
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 34 

**Bridging PSTN to Real-Time Voice Systems** 

A typical telephony flow begins when a caller dials a number managed by a  provider such as Twilio. The provider terminates the PSTN call and establishes  a bidirectional media stream, commonly via WebSocket, between the live call  and a voice-agent runtime. 

**Caller** 

PSTN/SIP 

Bidirectional Audio 

**Telephony Gateway** 

E.g. Twilio 

WebSocket 

Bidirectional Stream 

**Voice Agent Runtime** 

STT \+ Reasoning \+ TTS 

From that point forward, the call behaves as a continuous streaming session: 

The telephony provider acts as a media bridge, converting PSTN audio  into packetized frames and routing synthesized speech back into the call.  Each session is identified by a unique call or stream identifier, which  must be preserved on all inbound and outbound media to avoid  cross-call contamination. 

Deepgram’s Voice Agent API is designed to sit directly behind this gateway, receiving and emitting audio streams while coordinating transcription,  reasoning, and synthesis as a single real-time loop. 

**Audio Format and Latency Constraints** 

Telephony audio operates at 8 kHz, mono, using μ-law or A-law PCM. This limited bandwidth places a hard ceiling on acoustic fidelity and slightly  increases recognition difficulty compared to broadband sources. 

The most important optimization is **format alignment**. Avoid transcoding  wherever possible. Deepgram’s speech models accept μ-law PCM natively, and its TTS can emit μ-law audio directly consumable by telephony gateways. Eliminating format conversion removes unnecessary latency and reduces  failure modes. 

Even with optimal alignment, PSTN interactions typically add  100–200 milliseconds of round-trip delay. The best mitigation strategy is **regional proximity**:  
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 35 

• Match telephony media regions with speech infrastructure regions • Co-locate orchestration middleware with both 

• Minimize inter-region hops between gateway, agent runtime, and LLM 

Telephony UX lives or dies on perceived responsiveness. Every avoidable  millisecond matters. 

**Asynchronous Streaming and Event Coordination** 

Phone-based agents must send and receive audio concurrently. Blocking  pipelines introduce dead air, clipped speech, or missed interruptions. 

A robust telephony runtime uses non-blocking, event-driven loops for media  ingress and egress: 

`async def receive_media(ws, inbound_queue):` 

`async for frame in ws:` 

`await inbound_queue.put(frame)` 

`async def send_media(ws, outbound_queue):` 

`while True:` 

`frame = await outbound_queue.get()` 

`await ws.send(frame)`

Recognition, reasoning, and synthesis operate independently but are  synchronized through events. Signals such as “user stopped speaking,” “agent started speaking,” and “audio playback completed” anchor conversational timing and allow orchestration logic to manage fillers, interruptions, and state transitions. 

Deepgram’s Voice Agent API surfaces these lifecycle signals explicitly, allowing telephony runtimes to remain reactive rather than polling-based. 

**Barge-In, Interruption, and Playback Control** 

Telephony users interrupt frequently. A phone agent that cannot stop speaking  immediately when the caller interjects feels broken. 

Barge-in must be enforced at two levels: 

• **Media:** Stop or mute outbound audio the moment inbound speech resumes • **Logic:** Cancel or invalidate any pending reasoning or tool execution 

In integrated runtimes, interruption is automatic. In custom telephony stacks,  inbound audio energy or speech detection should immediately preempt  playback and return the system to a listening state. Playback confirmation  events are essential to ensure buffers are reset cleanly before the next  response begins.   
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 36 

**DTMF and Call Control** 

Although speech-first interaction is preferred, telephony environments still  produce keypad input. DTMF tones should be detected explicitly and handled  outside the speech pipeline so they do not pollute transcripts. 

Use DTMF sparingly and deterministically. Numeric shortcuts such as “Press  0 for an operator” should route cleanly into call-control logic while preserving conversational continuity for speech interactions. 

Call termination, transfer, and escalation must also be handled explicitly. When  a call ends or is redirected, the associated media stream should be closed  immediately. During transfers, inform the caller verbally, mute audio during the  transition, and avoid overlapping speech that can cause clipping or echo. 

**Voximplant**’s native connector eliminates custom media infrastructure requirements for production voice agents across PSTN, SIP, and WebRTC  channels. This architecture validates that abstracting telephony complexity at  the platform layer accelerates deployment without sacrificing real-time control. 

**Escalation and Multi-Party Scenarios** 

In enterprise settings, AI agents frequently hand off to humans. The  simplest pattern is a clean transfer: stop the AI stream and redirect the call  to a new endpoint. 

More advanced scenarios keep the AI present as an assistant while a human  joins. These require strict separation of inbound and outbound streams to  prevent cross-talk. The AI should never inject speech into the caller’s channel unless explicitly authorized. 

Agent-assist architectures benefit from the same real-time transcription and  orchestration capabilities, but the conversational contract changes. The AI  listens continuously and advises silently rather than speaking. 

**Scaling and Concurrency** 

Telephony workloads scale horizontally. Each call maps to an independent,  long-lived streaming session. 

Scaling challenges typically arise in: 

• WebSocket concurrency limits 

• Orchestrator throughput 

• Downstream LLM rate limits 

Use async runtimes and load balancers that support connection persistence.  Implement graceful connection draining and backpressure during traffic  spikes. For critical flows, define fallback behaviors when upstream services  degrade so callers never experience unexplained silence.  
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 37

**Monitoring and Quality Measurement** 

Telephony UX is judged almost entirely by timing and clarity. Measure: 

• End-of-turn to first audio response latency 

• Barge-in success rate 

• Frequency of clipped or interrupted responses 

• Call abandonment during silence 

Event-level instrumentation provides the most actionable insight. Tracking  

user stop, agent start, and audio completion events across large call volumes  

reveals where conversational rhythm breaks down and where optimization  

yields the highest return. 

**Bringing It All Together** 

Telephony architecture is where legacy voice infrastructure meets modern  

real-time AI systems. Success depends on disciplined media handling, explicit  

event coordination, and interruption-first design. 

When engineered correctly, the underlying complexity disappears. The caller  

experiences not a stitched-together system, but a responsive, conversational  

agent that behaves naturally despite the constraints of PSTN. That illusion is  

the benchmark of a production-ready telephony voice agent.   
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 38

Multilingual Strategies and Localization 

As voice agents expand globally, multilingual support becomes a system-level  concern rather than a feature add-on. Language choice affects every layer of  the stack, including speech recognition, reasoning, synthesis, orchestration,  and UX. Successful multilingual agents balance accuracy, latency, cultural  alignment, and operational simplicity. 

The core challenge is preserving conversational continuity and persona while  adapting to linguistic and regional variation in real time. 

**Language Strategy and Conversational Architecture** 

Multilingual voice agents typically follow one of two **conversation-level  strategies**: 

• **Unified multilingual conversational streams**, where a single real-time  stream supports multiple languages dynamically 

• **Language-specialized conversational streams**, where the system  converges on a dominant language and optimizes for it over time 

**Examples:** 

**Unified multilingual conversational streams:** These are powered by  a multilingual model that can understand and generate replies in many  languages in the same session. For example, a customer support bot  

that responds in Spanish, then seamlessly switches to French if the user  changes languages mid-conversation. 

**Language-specialized conversational streams:** Some helpdesk or customer  support systems require users to choose their language upfront. Once  selected (e.g., Japanese), the voice agent uses a Japanese-specialized model for all understanding and response generation in that session. 

Unified multilingual streams prioritize continuity. They avoid disruptive mid conversation transitions, simplify orchestration, and handle moderate code switching naturally. Language-specialized streams can optimize accuracy or  cost in long-running interactions, but introduce additional complexity around  transition, state management, and UX consistency. 

Deepgram’s platform supports both approaches, allowing teams to choose based on product requirements rather than model constraints. In practice, real time voice agents benefit most from minimizing disruption. Continuity usually  matters more than marginal accuracy gains unless regulatory, domain-specific,  or cost considerations dictate otherwise. 

**Klubi**’s AI voice agents handle 30,000+ monthly interactions in Brazilian Portuguese across noisy mobile environments, maintaining 90%+ end-to end conversation handling. Their deployment validates that domain-specific  terminology accuracy and environmental robustness matter more than raw  WER in production voice-led sales workflows.   
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 39

**Language Awareness and Adaptive Routing** 

Language awareness must emerge early in the interaction, but it should  remain **incremental rather than decisive**. In real-time voice systems, language  detection functions as a probabilistic signal that informs orchestration, not  a hard routing gate that resets conversational state. 

Streaming multilingual recognition allows agents to adapt dynamically as  language stabilizes, without requiring explicit selection or disruptive handoffs.  Early signals can guide response phrasing, acknowledgment style, or  escalation logic while preserving turn-taking and conversational rhythm. 

In more complex deployments, language confidence may still influence  downstream behavior, such as: 

• Restricting inference to a known language set 

• Gradually specializing speech or reasoning behavior 

• Triggering human handoff or fallback workflows 

The key requirement is that language-aware behavior enhances  responsiveness without breaking timing, interruption handling, or  persona continuity. 

**Voice and Persona Consistency Across Languages** 

A multilingual agent should feel like the same character in every language.  Inconsistent tone, pacing, or expressiveness breaks trust faster than minor  recognition errors. 

Persona continuity is best achieved by: 

• Selecting voices with similar tonal characteristics across languages • Maintaining consistent pacing and turn-taking behavior 

• Treating voice selection as a UX and brand decision, not a technical one 

Modern speech synthesis systems increasingly support expressive,  enterprise-grade voices across many languages. Where native voices are  unavailable, composable orchestration allows teams to integrate external  synthesis providers while preserving real-time interruption handling and  session control. 

Language switching mid-conversation should update voice and synthesis  behavior dynamically without resetting context. The user should experience  adaptation, not reconfiguration.   
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 40

**Prompt and Context Localization** 

Localization is not translation. 

Prompts, personas, and system messages should be authored directly in the  target language. Relying on real-time translation introduces tone drift, syntactic  artifacts, and cultural misalignment that compound over long interactions. 

Effective localization requires: 

• Language-native persona definitions 

• Regionally appropriate politeness and formality norms 

• Localized acknowledgments, clarifications, and error handling 

Knowledge grounding must also be localized. If enterprise data exists in one  language and the user speaks another, retrieved content should be translated  and adapted before synthesis to avoid disruptive code-mixing. 

Localization is a UX responsibility. Agents feel fluent when they follow linguistic  norms rather than simply translating vocabulary.   
**Testing, Quality, and Fallback Behavior** 

Multilingual quality cannot be evaluated by transcription accuracy alone.  Native speakers should assess pronunciation, phrasing, pacing, and cultural  appropriateness. Each language may require different tuning for response  length, acknowledgment patterns, or synthesis speed. 

When an unsupported language is encountered, agents should  fail gracefully: 

• A brief explanation in the detected language, when possible • Optional escalation to a human operator 

• Clear acknowledgment rather than silence or confusion 

Graceful degradation preserves trust even when full support  is unavailable.   
CHAPTER 2: SYSTEM DESIGN AND ARCHITECTURE 41

**Summary** 

Multilingual voice agents succeed when language support is designed into  

the architecture rather than layered on later. Effective systems prioritize  

conversational continuity, persona consistency, and localization over rigid  

language pipelines. 

Deepgram’s platform supports this approach through real-time multilingual 

speech recognition, expressive synthesis, and a composable orchestration  

layer that adapts across languages without sacrificing responsiveness.   
CHAPTER 3 

Deployment and Runtime  
CHAPTER 3: DEPLOYMENT AND RUNTIME 43

Deployment and Runtime Architecture  

Designing a high-performing voice agent does not end with model quality  or UX design. Once deployed, success depends on infrastructure: where  the system runs, how it scales under load, and how it behaves when things  go wrong. Real-time voice systems place stricter demands on infrastructure  than typical web services because latency, interruptions, and downtime are  experienced directly through conversation. 

This chapter focuses on **performance, availability, and runtime behavior**.  Regulatory, privacy, and governance considerations are addressed separately  in the Compliance chapter.   
Hosting Models and Regional  

Placement 

Voice agents must run close to users, support different levels of operational  control, and operate reliably across environments. Deepgram supports these  needs through multiple **deployment models**, including a fully managed Cloud  API, single-tenant Dedicated clusters, EU-hosted endpoints for regional data  residency, and **self-hosted deployments** for private cloud, bare-metal, or  restricted environments. 

The Cloud API provides the fastest path to production, with automatic scaling  and global availability managed by Deepgram. Dedicated deployments give  enterprises isolation, custom configuration, and predictable performance. Our  EU-hosted endpoint provides deterministic regional data residency, ensuring  inference and audio processing occur within a defined geographic boundary.  In environments with strict connectivity or security constraints, self-hosted  speech models can run locally while orchestration logic remains under  customer control. 

Endpoint proximity is critical for conversational responsiveness. Routing users  to the nearest available speech endpoint can reduce round-trip latency by  hundreds of milliseconds. Telephony gateways, orchestrators, and speech  infrastructure should be co-located in the same region whenever possible to  minimize inter-service hops and preserve conversational timing.   
CHAPTER 3: DEPLOYMENT AND RUNTIME 44 

Scaling and Concurrency 

Each active voice session maintains long-lived streaming connections for  audio input, transcription, and synthesis. While a single session consumes  modest resources, large deployments must support thousands of concurrent  conversations without degradation. 

Deepgram’s managed speech infrastructure automatically handles concurrency and scaling for transcription and synthesis workloads. Customer managed orchestration and reasoning layers should be designed with similar  elasticity, using asynchronous runtimes and stateless gateways to manage  large numbers of open connections efficiently. 

Production systems commonly distribute sessions across a pool of compute  behind a load balancer, ensuring that no single node becomes a bottleneck.  External reasoning components such as LLM APIs may impose rate limits or  

cost constraints, so many deployments tier model usage, reserving larger  models for complex turns and using lighter models for routine exchanges.   
Resilience and Graceful Degradation 

Real-world reliability is defined not by the absence of failure, but by how  the system behaves when components degrade. Voice agents should never  fail silently. 

If reasoning or retrieval fails, the orchestrator should acknowledge the issue  verbally and recover or escalate. If synthesis fails, a fallback voice or canned  audio response should be used. If transcription confidence drops, the agent  

should prompt for clarification rather than proceeding with uncertain input.  When automated recovery fails, the system should escalate to a human  operator rather than trapping users in conversational dead ends. 

Infrastructure changes should also be non-disruptive. Deploy updates  gradually, drain existing sessions before recycling instances, and allow active  conversations to complete cleanly. These practices preserve trust even during  maintenance or partial outages.  
CHAPTER 3: DEPLOYMENT AND RUNTIME 45

Observability and Runtime Visibility 

Operational insight is essential for both debugging and optimization. Every  session should emit structured events capturing transcript segments, timing,  interruptions, and major system transitions. These signals allow teams to  correlate infrastructure behavior directly with user experience. 

For self-hosted deployments, including those running on AWS SageMaker,  private cloud, or bare-metal infrastructure, Deepgram exposes detailed  event-level telemetry for speech activity, which can be integrated directly  into standard observability stacks such as Datadog or CloudWatch. Tracking  metrics like end-to-end response latency, interruption success rates, and  session stability enables teams to identify regressions and continuously refine  conversational performance. 

These same event streams later serve as inputs to audit and governance  workflows discussed in the Compliance chapter.   
Edge and Offline Deployments 

Some environments cannot rely on persistent cloud connectivity.  Vehicles, kiosks, and industrial systems may require local inference to  guarantee availability. 

Deepgram supports these scenarios through self-hosted speech deployments  that run STT and TTS models locally while preserving the same streaming  interfaces used in cloud environments. These systems often trade model  breadth for predictability, using constrained vocabularies or lighter models to  maintain responsiveness on limited hardware. While less flexible than cloud  deployments, edge architectures ensure continuity when network access is  unreliable or unavailable.   
CHAPTER 3: DEPLOYMENT AND RUNTIME 46

Security as a Runtime Baseline 

All real-time voice systems must operate over secure channels. Encrypted  transport, short-lived authentication tokens, and strict network isolation are  baseline requirements. 

Deepgram enforces these controls across its Cloud, Dedicated, and EU hosted deployments, while customer-managed components must implement  equivalent safeguards. Security establishes the foundation for safe operation.  How these controls extend into retention, access governance, and auditability  is addressed in the next chapter.   
Summary 

Deployment is where voice UX becomes operational reality. The runtime  architecture must balance latency, scale, and resilience without sacrificing  availability or responsiveness. With thoughtful regional placement, elastic  scaling, and graceful recovery strategies, teams can deploy voice agents that  remain trustworthy and performant in production, regardless of scale  or environment.   
CHAPTER 4 

Operational Excellence  
CHAPTER 4: OPERATIONAL EXCELLENCE 48

Reliability, Testing, and Evaluation 

Reliability for voice agents is defined by whether the system behaves naturally  under real-world conversational conditions, not by uptime alone. Voice agents  fail in experiential ways: replies that start too early, pauses that stretch too  long, or responses that technically answer but miss intent. Ensuring reliability  requires validating not just correctness, but conversational behavior. 

Effective testing combines two complementary dimensions. Quantitative  evaluation measures timing, flow, and responsiveness at the event level.  Qualitative evaluation assesses meaning, intent alignment, and task  success. Together, these approaches predict how an agent will feel to  users in production. 

**Deepgram’s Voice Agent API** exposes detailed event telemetry that enables  precise timing analysis. For large-scale simulation and behavioral evaluation,  teams often pair this telemetry with tools from **Coval**, which specializes in  probabilistic testing and multi-turn agent evaluation. 

**From Deterministic QA to Probabilistic Reliability** 

Traditional QA assumes that identical inputs yield identical outputs. Voice  agents violate this assumption by design. Speech recognition, language  models, and real-time orchestration all introduce variability. 

The goal of reliability testing is therefore not to validate a single  correctresponse, but to measure outcome distributions and improve  their consistency. 

Probabilistic evaluation treats conversational behavior statistically. Teams run  many sessions under controlled variation such as accents, noise, or speaking  cadence and measure how often the agent behaves acceptably. This approach  reflects real usage and allows systems to be tuned for conversational  smoothness rather than brittle correctness. 

**VAQI: Measuring Conversational Flow** 

The Voice Agent Quality Index (VAQI) provides a concise way to quantify conversational responsiveness using three timing behaviors: 

• **Interruptions (I)**: how often the agent speaks before the user finishes 

• **Missed responses (M):** how often the agent fails to respond within a  defined window after a turn ends 

• **Latency (L):** elapsed time from UserStoppedSpeaking to  

AgentStartedSpeaking 

These metrics are derived directly from event timestamps, making them well  suited for automated testing. Improvements in VAQI correlate strongly with  perceived experience. For example, teams often see measurable gains after  tuning end-of-turn thresholds or optimizing orchestration latency.   
CHAPTER 4: OPERATIONAL EXCELLENCE 49

**Retell AI** consistently achieves \~800ms response times with interruption handling in production voice agents, demonstrating that sub-second  responsiveness is achievable at scale when perception, reasoning, and  synthesis are tightly orchestrated. This validates VAQI latency metrics as  measurable predictors of conversational quality. 

In **large-scale benchmarks conducted with Cova**l, Deepgram’s conversational speech models demonstrated faster response onset while maintaining  transcription accuracy under production-like conditions, reinforcing the  importance of timing as a first-class reliability metric. 

**Designing Effective Evaluation Programs** 

A comprehensive reliability program blends multiple testing methods, each  revealing different failure modes: 

• Probabilistic regression: Run many sessions under varied conditions and  compare metric distributions across versions to detect drift. 

• Replay testing: Reprocess recorded audio through new builds to isolate  timing regressions while holding input constant. 

• Load and stress testing: Simulate concurrent sessions and track tail latency  rather than averages, since worst-case delays dominate user perception.   
• Fault injection: Introduce controlled failures such as delayed reasoning  or dropped synthesis to confirm graceful recovery. 

• Turn-level diagnostics: Visualize UserStoppedSpeaking to  AgentStartedSpeaking intervals and overlay interruption events to  pinpoint orchestration bottlenecks. 

Well-run teams maintain a fixed library of representative test calls and  enforce tolerance bands, such as maximum acceptable VAQI deltas or  missed-response rates, as part of every release cycle. 

**Qualitative Evaluation and Semantic Accuracy** 

Timing metrics describe how an agent behaves, but not whether it says  the right thing. Qualitative evaluation measures intent alignment, semantic  correctness, and tone. Coval supports this layer through a mix of automated  checks and human-in-the-loop review. 

Common practices include scenario-based simulations, dialogue-level  assertions such as required fields in responses, and human review of tone  or empathy. These methods surface issues that quantitative metrics alone  cannot capture, particularly in regulated or customer-facing domains.   
CHAPTER 4: OPERATIONAL EXCELLENCE 50

**Validating Reliability Before Production** 

Reliability must be proven before exposure to real users. Testing environments  

should mirror production configurations, including telephony codecs,  

streaming pipelines, and orchestration logic. New builds should be validated  

against baseline metrics and exercised under failure conditions such as  

transient network loss or delayed downstream services. 

A release should advance only after key indicators such as VAQI, missed 

response rate, and instruction compliance meet predefined thresholds.  

Once validated, these same metrics can be monitored continuously in  

production to detect drift and guide ongoing optimization. 

Reliability begins with evaluation, but it is sustained through measurement.  

The next section extends these principles into production observability  

and continuous monitoring, ensuring that voice agents remain consistent  

as they scale.   
CHAPTER 4: OPERATIONAL EXCELLENCE 51

Observability and Monitoring 

Reliability testing validates a voice agent before release. Observability ensures  that conversational health holds in production as traffic scales, models  evolve, and real-world conditions vary. In real-time voice systems, latency,  interruptions, and failures are immediately audible to users, which makes early  detection essential. 

Observability is concerned with detection and response. Its purpose is to  surface live degradation quickly so teams can investigate, mitigate, or route  traffic appropriately while conversations are in progress. 

Effective observability turns conversational behavior into operational signals. It  exposes emerging issues before users report them and provides the feedback  loop required to maintain stable performance over time. 

**From Testing Metrics to Live Signals** 

Many of the same event boundaries used during testing continue to matter in  production. These include turn boundaries, reasoning states, and playback  transitions emitted by the Voice Agent API, such as UserStoppedSpeaking,  AgentThinking, and AgentStartedSpeaking. 

In production, these events function as live signals rather than evaluation  artifacts. Tracking the intervals between them allows teams to monitor  conversational timing and flow continuously. Aggregated across sessions,  these measurements reveal shifts in responsiveness or turn handling that  warrant investigation. 

A production observability pipeline typically includes: 

• Event instrumentation that emits timestamps and metadata for every user  and agent turn 

• Metric derivation that computes per-stage latency for speech recognition,  reasoning, and synthesis, as well as end-to-end turn timing 

• Storage and visualization using systems such as Datadog, Grafana, or  CloudWatch 

• Alerting based on sustained deviations, such as rising tail latency or  interruption failures 

When tuned correctly, this pipeline functions as an early warning system for  conversational degradation.   
CHAPTER 4: OPERATIONAL EXCELLENCE 52

**Monitoring Conversational Behavior** 

Infrastructure health alone does not capture the quality of live voice  interactions. Observability must also track how conversations unfold in  practice so teams can detect abnormal patterns as they emerge. 

Key behavioral signals include: 

• Barge-in handling, measured by whether the agent stops speaking  promptly when the user resumes 

• Silence or stall detection, where expected responses fail to arrive within  defined time windows 

• Error distribution across speech recognition, reasoning, and synthesis  components 

• Session dynamics such as unusually long turns, repeated prompts, or  looping behavior 

These signals surface deviations from expected interaction patterns that  may indicate upstream failures, orchestration regressions, or dependency  issues. Correlating them with latency and error metrics helps teams localize  problems quickly.   
**Dashboards, Alerts, and SLOs** 

Dashboards consolidate telemetry into a live operational view.  Common views include active session volume, latency percentiles,  interruption success rates, and error counts. Trend analysis often  reveals issues before users experience widespread impact. 

Service Level Objectives should express acceptable operational  bounds for conversational systems, such as: 

• Response latency remaining below a defined percentile threshold • Interruption handling success staying within tolerance bands • Error rates remaining below predefined limits 

Alerts tied to these objectives exist to trigger operational  response. They signal when investigation, mitigation, or traffic  control actions are required, rather than serving as judgments of  conversational correctness. 

**Logging and Traceability** 

Metrics reveal trends, while logs support incident investigation.  Each conversation should carry a unique session identifier that links  transcripts, events, and errors across systems.   
CHAPTER 4: OPERATIONAL EXCELLENCE 53

Structured logging enables reconstruction of problematic interactions when  diagnosing failures. Logs commonly capture system events such as retries,  timeouts, and function calls, as well as conversational events such as speech  boundaries and interruptions. 

Transcript storage used for debugging must follow strict privacy controls.  Sensitive data should be redacted, logs encrypted at rest, and access  governed by role-based permissions, as described in the Compliance chapter. 

**Synthetic and Real-User Monitoring** 

Production observability benefits from combining synthetic probes with real user telemetry. 

Synthetic monitoring runs scripted sessions on a schedule to validate  baseline system behavior. These probes often reuse representative  scenarios developed during pre-release testing and help catch known  failure modes early. 

Real-user monitoring aggregates signals from live traffic. It captures variability  introduced by user behavior, network conditions, and external dependencies  that synthetic tests cannot fully simulate. 

Together, these approaches provide both predictability and coverage.  Synthetic monitoring confirms expected behavior, while real-user telemetry  surfaces emergent issues.   
**Closing the Loop with Evaluation** 

Observability supplies real-world signals that inform what should be  investigated, mitigated, or prioritized for further testing. It does not replace  evaluation or testing programs. Instead, it provides continuous input that  guides where deeper analysis is required. 

By feeding production signals back into testing workflows, teams can refine  scenarios, adjust thresholds, and focus evaluation efforts on the failure modes  that matter most in practice. 

**Operational Discipline** 

Observability supports resilience only when paired with operational rigor.  Teams should regularly validate alerting pipelines, rehearse incident response,  and evolve dashboards as systems change. Deployments should be versioned  and metrics tracked alongside build identifiers to preserve traceability. 

Testing establishes readiness before launch. Observability maintains  conversational health during live operation.   
CHAPTER 5 

Compliance  and Governance  
CHAPTER 5: COMPLIANCE AND GOVERNANCE 55

Compliance and Data Control 

Operating voice agents responsibly requires protecting user data across  its entire lifecycle, from capture and processing to storage and deletion.  Compliance functions as an architectural property of the system and must be  designed deliberately. 

Many of the mechanisms referenced in this chapter, such as regional isolation,  secure transport, tokenized access, and event logging, appear earlier as  runtime capabilities. In this section, those same mechanisms are treated as  governance controls that define how data is protected, retained, and audited  over time. 

Voice agents process sensitive data including live audio, transcripts, and  user-specific information. Privacy and security therefore must be enforced  deliberately at every layer of the stack. A compliant deployment is defined  by how data flows through the system, how long it persists, and how access is controlled.   
Regional Deployment and  

Data Residency 

The execution environment of a voice agent determines which regulatory  frameworks apply. Jurisdictions such as the EU and UK impose strict  requirements on where audio and transcripts may be processed and stored. 

Regional alignment ensures that audio and transcript data remains subject  to the appropriate jurisdictional controls. Managed speech infrastructure  should support explicit regional routing and avoid cross-region processing. 

**Vida** processes hundreds of millions of TTS characters monthly for  healthcare voice agents while maintaining HIPAA compliance, achieving  50% cost savings through unified STT+TTS from a single provider. This architecture demonstrates that compliance and cost optimization reinforce  each other when vendor consolidation reduces both data exposure and  integration complexity.   
CHAPTER 5: COMPLIANCE AND GOVERNANCE 56

Highly regulated environments often require additional isolation.  Single-tenant or region-specific deployments provide stronger  data segregation, clearer audit boundaries, and more predictable  governance. Deepgram supports this model through Dedicated  clusters and EU-hosted deployments. 

When external services such as language models or downstream APIs  are involved, their residency guarantees must be evaluated as part  of the overall compliance architecture. In environments requiring full  control, self-hosting components within a controlled infrastructure  provides the most deterministic guarantees. 

The core principle remains consistent. Systems should be designed  so data remains within the regions where it is legally or contractually  required to reside.   
Secure Transmission and Authentication 

Protecting data in motion and enforcing strict access controls form the  foundation of compliance. All real-time audio and transcript traffic should  be encrypted using TLS, including secure WebSocket connections. Internal  service-to-service communication should also use encrypted channels. 

Authentication should rely on short-lived credentials rather than static  API keys. Deepgram uses token-based authentication with ephemeral  credentials that expire quickly, limiting exposure if intercepted.  Long-running sessions should refresh tokens automatically without  extending credential validity windows. 

Client applications should avoid embedding long-lived credentials. Backend  services should issue scoped, time-limited tokens following the principle of  least privilege across browser, mobile, and device environments. The specific  implementation of these controls varies by deployment model and is treated as  an operational concern.   
CHAPTER 5: COMPLIANCE AND GOVERNANCE 57

Data Retention, Redaction,  

and Minimization 

Effective compliance places strong emphasis on data minimization. 

Clear data-retention policies should limit storage to what is strictly necessary,  with deletion or anonymization applied once data has served its purpose. Voice  transcripts frequently contain personally identifiable information. Deepgram’s speech-to-text APIs support model-based PII redaction, allowing sensitive  entities to be masked at inference time. 

Many organizations choose to avoid storing audio altogether. Deepgram does  not retain audio by default, and storage is opt-in only for specific programs.  Other deployments maintain short-lived buffers for quality assurance and  delete recordings automatically. These minimization practices are essential for  meeting GDPR, HIPAA, and PCI requirements. 

When transcripts or logs are stored, they should be treated as confidential  assets. Data should be encrypted at rest, protected by role-based  access controls, restricted through IAM policies, and monitored through  comprehensive access auditing. Storage systems should be private by default.   
User Authentication, Consent,  and Disclosure 

When agents handle user-specific data or perform sensitive actions, users  must be authenticated before proceeding. In telephony environments, this  may involve caller ID verification, PINs, or step-up authentication flows. If  authentication fails, the agent should restrict disclosures or escalate to a  human operator. 

Consent and disclosure requirements apply across many jurisdictions. Users  may need to be informed that calls are recorded or that they are interacting  with an AI system. Telephony frameworks can deliver standardized disclosures  automatically, and agents should identify themselves as AI when asked. 

Clear disclosure practices reduce regulatory risk and reinforce user trust.   
CHAPTER 5: COMPLIANCE AND GOVERNANCE 58

Logging, Auditability, and Governance 

Compliance requires verifiable records of sensitive system behavior.  Audit logs should be maintained for actions such as financial transactions,  consent capture, and content filtering. These logs should include timestamps,  session identifiers, and relevant metadata, and should be designed to  prevent tampering. 

Audit logs typically reuse the same event streams captured for operational  observability, with stricter retention, access controls, and immutability  guarantees applied. This alignment ensures consistency between operational  monitoring and compliance reporting. 

Access to audit data should be tightly restricted, encrypted at rest, and stored  using immutable or versioned storage where appropriate. Organizations should  maintain documented incident-response and business-continuity plans and  validate them regularly. 

Security and compliance operate as continuous processes that evolve  alongside the system.   
Putting Compliance into Practice Compliance for voice agents is achieved through layered controls: 

• Keep data within the appropriate region 

• Secure data in transit and at rest 

• Minimize and redact stored information 

• Authenticate users and capture consent 

• Log sensitive actions for accountability 

Deepgram’s platform supports these principles through regional endpoints, tokenized authentication, built-in PII redaction, and deployment options such  as Dedicated and EU-hosted runtimes. These capabilities align with common  enterprise compliance frameworks including SOC 2 Type II, HIPAA, PCI,  GDPR, and CCPA. 

Compliance ultimately reflects a design philosophy. Systems built with  privacy by default, disciplined data handling, and consistent governance  controls can operate at enterprise scale while maintaining trust, safety,  and regulatory alignment.   
CHAPTER 5: COMPLIANCE AND GOVERNANCE 59Content Safety and Guardrails   
Voice agents operate in open-ended, real-time conversations,  

which makes them uniquely exposed to unsafe, sensitive, or out-of 

scope inputs. Unlike traditional software, failures in voice systems  

are immediately perceptible and cannot be silently corrected. Once  

something is spoken, it cannot be taken back. 

Content safety is therefore not an add-on. It is a core systems  

responsibility that protects users, organizations, and operators by  

enforcing clear behavioral boundaries at runtime. 

Effective guardrails operate across three layers: input moderation,  

reasoning control, and output filtering. These technical controls  

are reinforced by governance processes that track, review, and  

continuously refine safety behavior in production.   
CHAPTER 5: COMPLIANCE AND GOVERNANCE 60 

**User Input**   
Flagged 

**Layer 1:** 

Violated Rules 

**Spoken**   
**Policy**   
**Response** 

**Refusal/**   
**Redirect** 

**Text-to**   
**Audio/ Speech**   
**Input**    
**ModerationLayer 2:**   
**Speech Synthesis**   
**Response** 

Clean   
**Reasoning**   
**ControlLayer 3:**   
Unsafe Content 

**Suppress/ Rewrite** 

Compliant 

**Figure 5.1: Three-Layer Guardrails Architecture — Input moderation,**  reasoning control, and output filtering work together to enforce behavioral boundaries at runtime.   
**Output**   
**Filtering** 

Validated   
CHAPTER 5: COMPLIANCE AND GOVERNANCE 61

**Input Moderation: Controlling What the Model Sees** 

The first line of defense is filtering user input before it reaches the reasoning  layer. Input moderation reduces the likelihood that the model processes  content that is abusive, unsafe, or outside its intended domain. 

Use moderation or classification systems to detect categories such as hate  speech, explicit content, self-harm, or criminal intent. When input is flagged,  route the conversation into a policy-compliant handling path rather than  passing it directly to the language model. 

Common patterns include: 

• Abusive language: respond with a calm boundary, such as “I can help  if we keep the conversation respectful.” 

• Self-harm signals: provide supportive language and escalate to  appropriate resources. 

• Illegal or dangerous requests: refuse clearly and redirect without  elaboration. 

Deepgram’s speech recognition can accurately transcribe profanity or mask it when required, allowing moderation systems to operate reliably on text output.  Teams typically pair this with text-based moderation models or classifiers to  cover policy categories across languages and contexts. 

Guardrails should be validated before deployment. Structured regression tests  that probe adversarial phrasing, edge cases, and tone ensure that unsafe  inputs never propagate into production conversations. 

**Reasoning Control: Constraining Model Behavior** 

Even with moderated input, language models require explicit behavioral  boundaries. These constraints live in system prompts and policy instructions  and should be treated as part of the agent’s safety configuration. 

Effective reasoning controls include: 

• Refusal rules for violent, illegal, or disallowed requests. 

• Tone constraints that enforce calm, respectful responses  

under provocation. 

• Instruction protection rules that prevent disclosure of system  or developer prompts. 

Prompts should be versioned, tested, and reviewed like code. High-risk  applications benefit from approval workflows for prompt changes, ensuring  that updates do not introduce unintended behavior. 

Many production systems now adopt layered guardrail architectures, where  multiple lightweight safety checks evaluate intent, policy compliance, or  hallucination risk in parallel with generation. These supervisory checks  can operate continuously without adding noticeable latency, preserving    
CHAPTER 5: COMPLIANCE AND GOVERNANCE 62

conversational flow while improving control. Frameworks such as **Decagon**’s layered real-time guardrails demonstrate how this approach scales in  production voice environments. 

**Output Filtering: Controlling What Is Spoken** 

The final and most critical safeguard verifies model output before it is  converted to speech. Because spoken responses cannot be retracted, only  validated text should ever reach the synthesis stage. 

Run each response through a post-generation filter to detect disallowed  content, sensitive data, or unauthorized disclosures. If violations are detected,  suppress or rewrite the response before synthesis. 

Typical safeguards include: 

• Redacting numeric patterns that resemble payment or identity data. • Masking explicit or unsafe terms. 

• Blocking responses that reference restricted internal data or system state. 

This final verification step is essential in voice systems. Even a single unsafe  utterance can undermine trust or create regulatory exposure.   
**Voice-Specific Safety Risks** 

Voice introduces safety considerations that do not exist in text-only systems.  Tone, pacing, and delivery shape how users perceive intent and trustworthiness. 

Key voice-specific risks include: 

• Tone and empathy mismatches that escalate frustration or appear  dismissive. 

• Hallucinated confirmations, where the agent implies an action succeeded  before it actually did. 

• Pronunciation errors in TTS that unintentionally resemble offensive language 

Mitigating these risks requires both technical controls and review processes.  Monitoring user interruptions, sentiment shifts, and post-call feedback often  surfaces issues that automated filters miss.   
CHAPTER 5: COMPLIANCE AND GOVERNANCE 63

Safety Governance and  

Continuous Improvement 

Safety does not end at runtime. Governance processes ensure  that guardrails remain effective as models, prompts, and user behavior evolve. 

Reuse existing observability pipelines to capture moderation events, refusals,  and escalations, tagging them by policy category and outcome. This keeps  safety telemetry integrated with operational metrics rather than siloed in  separate systems. 

Maintain audit logs for every safety intervention and review them regularly to  identify recurring triggers or emerging patterns. In regulated environments, this  is often supported by human-in-the-loop review processes. 

Some organizations extend governance further with post-conversation  analysis that evaluates completed interactions for policy compliance, tone, and  escalation accuracy. Continuous QA systems, such as Decagon’s Watchtower style monitoring, help close the loop by feeding insights back into prompt  design, moderation rules, and detection thresholds. 

Guardrails must evolve over time. New forms of prompt injection, indirect  requests, and policy evasion appear regularly. Moderation logic and escalation  criteria should be updated accordingly.  

When sessions exceed defined risk thresholds, such as repeated violations or  distress signals, agents should escalate automatically to human operators. 

In voice systems, safety is about guiding conversations within clear,  responsible boundaries. Well-designed guardrails protect users while  preserving natural dialogue, ensuring agents remain helpful, trustworthy,  and appropriate as conditions change. 

Operational Realities: 

Pitfalls and Success Factors 

Building a voice agent that works is only the starting point. Sustained success  depends on how the system is introduced, adopted, and measured inside an  organization. Teams that succeed treat voice AI as an operational capability  that evolves over time, not a one-time deployment. 

**Start with Focused Wins** 

A common failure mode is overreach. Voice agents perform best when they  begin with a narrow, high-volume workflow that is repetitive and clearly  scoped. Tasks like password resets, order status checks, or appointment  confirmations are ideal starting points. 

**Klubi** started with a single repeatable workflow—outbound qualification calls in  Brazilian Portuguese—before expanding to post-sales support.    
CHAPTER 5: COMPLIANCE AND GOVERNANCE 64

This narrow scope allowed them to tune domain vocabulary and noisy  environment handling while replacing \~40 human SDRs with continuous AI operation handling 90%+ of conversations end-to-end. 

Constrained use cases allow teams to tune vocabulary, behavior, and  integrations without the noise of edge cases. They also deliver visible  ROI quickly, building confidence and momentum. Most successful voice  deployments started with a single domain-specific pilot before expanding into  broader coverage. 

Start small, prove reliability, then widen the scope deliberately. 

**Integrate, Then Iterate** 

Production voice agents sit at the intersection of telephony, authentication,  backend systems, and analytics. Underestimating integration effort is a  common cause of delay. 

Plan for multiple tuning cycles. Prompts will evolve. Turn-taking thresholds  will need adjustment. Domain vocabulary will improve with real data. Treat the  initial rollout as a pilot, not a finished product. Launch to a limited audience,  observe real interactions, and refine continuously before scaling. 

Stability is achieved through iterative refinement based on real usage, rather  than upfront completeness.   
**Align Humans and Manage Change** 

Voice agents change how people work, and adoption depends on trust. 

For employees, position the agent as a tool that removes repetitive work so  humans can focus on complex or high-value interactions. Involve frontline staff  early. Their input improves agent behavior and creates ownership rather than  resistance. Provide simple feedback loops so human agents can flag issues,  suggest improvements, or review transferred calls. 

For customers, transparency matters. Clearly identify the agent as AI and give  it a consistent voice and identity. When users know what they are interacting  with, expectations align and satisfaction improves. 

**Design for Hybrid Operation** 

The most durable deployments combine AI and humans. The agent handles  what it can, and humans take over when needed. 

Handoffs should preserve context. Passing transcripts or summaries prevents  users from repeating themselves and reduces frustration. AI can also support  human agents by summarizing prior interactions or suggesting next steps,  improving efficiency without removing human judgment. 

Hybrid systems work because they acknowledge limits and design for  them explicitly.   
CHAPTER 5: COMPLIANCE AND GOVERNANCE 65

**Measure Incremental ROI** 

Return on investment builds progressively. Measure coverage, such as the  percentage of calls handled end to end, alongside efficiency metrics like  reduced handling time or deflection rate. 

Even partial automation creates value. If an agent completes intake before  transferring to a human, it still reduces workload and improves throughput.  Track improvements over time and use them to guide expansion. 

Progress compounds when each stage is measured and validated. 

**Optimize for Human Outcomes** 

Voice automation succeeds when it improves outcomes for people. Highlight  the impact on employees and customers: fewer repetitive tasks, shorter wait  times, and more consistent experiences. 

For example, automating hundreds of routine calls per day translates  directly into hours returned to human agents for higher-value work. Share  these results internally to reinforce that the goal is service quality and  empowerment, not replacement.   
**Sustain Momentum** 

Most failures are organizational, not technical. Teams that succeed adopt a  crawl, walk, run mindset: start narrow, involve people, measure impact, and  iterate continuously. 

Celebrate incremental wins. Treat improvement as ongoing work, not a final  milestone. Trust in voice AI is earned through consistent, reliable interaction  over time, one practical improvement at a time.   
CHAPTER 6 

Applied    
Architectures  
CHAPTER 6: APPLIED ARCHITECTURES 67

Reference Architectures (Topologies) 

Designing a real-time voice agent is an architectural problem, not a wiring  exercise. How audio, reasoning, and synthesis are composed determines  conversational timing, state coherence, and reliability. **Deepgram’s platform** supports multiple deployment topologies, from fully managed streaming loops  to deeply customized, multi-service runtimes. 

The following reference architectures illustrate proven patterns across that  spectrum. Each reflects a production-grade implementation and highlights  trade-offs between simplicity, extensibility, and operational control. 

**Tier 1 – Single-Agent Foundations** 

This pattern represents the simplest viable architecture for a natural,  real-time voice agent: a single, persistent streaming loop that handles  perception, reasoning, and speech synthesis end to end. 

**Topology** 

**Baseline Voice Agent (End-to-End Streaming Loop) Reference Implementation: GitHub** 

Audio 

**User Browser**   
WebSocket 

Bidirectional Stream   
**Deepgram**   
**Voice Agent** STT \+ LLM \+ TTS   
CHAPTER 6: APPLIED ARCHITECTURES 68

A lightweight browser client captures microphone audio and opens a secure  WebSocket connection to the Deepgram Voice Agent API. Audio is streamed  continuously. The agent runtime performs speech recognition, routes  transcripts to an integrated LLM, and streams synthesized speech back using  Aura-2. Playback begins immediately as audio arrives, creating a full-duplex  conversational loop. 

Because the entire interaction runs over one persistent WebSocket, there is  no separate backend orchestrator. Conversational state, timing, interruption  handling, and turn management are owned by the managed agent runtime.  

The client remains focused on transport, authentication, and playback, using  short-lived JWTs for stateless session control. 

This topology prioritizes architectural compression: fewer moving parts, fewer  failure modes, and minimal latency. All conversational intelligence lives in the  agent runtime, while the client acts as a thin edge.   
**When to use it** 

This pattern is well suited for prototypes, internal tools, and early production  deployments where speed, simplicity, and conversational responsiveness  matter more than deep system integration. 

**Function-Calling / Tool-Use Agent** 

**Reference Implementation: GitHub** 

This pattern extends a real-time voice agent with external actions and data  access through structured function calls.   
CHAPTER 6: APPLIED ARCHITECTURES 69**Topology** 

WebSocket Bidirectional   
**Deepgram** 

Function Calls    
& Results Queries    
Audio   
**User Client Browser/App** 

Stream 

**Voice Agent** 

STT \+ Reasoning \+ TTS   
**Backend**   
**Service** 

Function Handlers 

& Data 

**External APIs/**   
**Datastores**   
CHAPTER 6: APPLIED ARCHITECTURES 70

Deepgram’s Voice Agent API continues to manage the conversational loop, including streaming speech recognition, turn-taking, reasoning, and TTS.  When an interaction requires action, the agent emits a structured function call  rather than free-form text. These events are handled by a backend service  (Flask in this reference implementation), which executes trusted logic and returns results to the agent for immediate verbalization. 

The backend exposes a small, explicit set of functions such as customer  lookup, order status, or scheduling. Each function maps directly to  a deterministic handler. The demo uses mock but realistic datasets  stored as timestamped JSON files to enable repeatable testing without  external dependencies. 

This architecture separates concerns cleanly: 

• The agent runtime owns dialogue, timing, and state. 

• Function definitions constrain what the model is allowed to do. • Backend handlers execute side effects and data access.   
**When to use it** 

This topology is ideal when an agent must interact with live systems or perform  transactions without breaking the voice session. 

**Tier 2 – Specialized and Localized Agents** 

**Domain-Specific Voice Agent (Medical Assistant)** 

**Reference Implementation: GitHub** 

This pattern shows how a general-purpose voice agent can be adapted for  regulated, domain-specific workflows such as clinical documentation. It  extends the baseline Voice Agent API topology with domain-optimized speech  models and structured reasoning to handle specialized vocabulary, privacy  constraints, and downstream data systems.   
CHAPTER 6: APPLIED ARCHITECTURES 71**Topology** 

WebSocket 

**User**   
Audio   
Bidirectional Stream   
**Deepgram Voice Agent API**   
Clinical Notes & Patient Context 

**EMR / Data Store**   
**Clinician/Patient Browser** 

Nova 3 Medical \+ Reasoning \+ TTS (Optional) 

**Clinical Records**   
CHAPTER 6: APPLIED ARCHITECTURES 72 

Audio is streamed directly from the browser into the Voice Agent API, where  Nova-3 Medical provides accurate transcription of clinical terminology and  abbreviations. The resulting text is passed to a reasoning layer that structures  the content into summaries or draft clinical notes suitable for review or export.  Optional TTS can be used for confirmations or summaries, though the primary  output is structured text rather than conversational reply. 

The key architectural characteristic is **domain specialization without  orchestration change**. The real-time speech loop remains intact, while domain  intelligence is introduced through model choice, prompting, and downstream  integrations. The same pattern applies to other regulated domains such as  finance or legal by substituting the speech model and knowledge layer. 

**When to use** 

Healthcare or regulated workflows that require high transcription accuracy and  structured outputs, without rebuilding the real-time speech pipeline. 

**Language Coach (Multilingual and Localization Pattern)** 

**Reference Implementation: GitHub**   
**Topology** 

**User**   
**Language Learner** 

Audio 

**Browser** 

WebSocket 

Real-time Stream 

**Session & API Proxy**    
**Flask \+ SocketIO** 

Voice Agent API 

Connection 

**Deepgram Voice Agent API** 

Nova 3 Multilingual \+ Aura-2 \+ LLM  
CHAPTER 6: APPLIED ARCHITECTURES 73

This pattern demonstrates linguistic specialization: a multilingual, code switching voice agent that supports real-time conversation, pronunciation  feedback, and adaptive responses across languages within a single session.  

A browser client streams audio through a thin backend to the Voice Agent  API. Nova-3 Multilingual handles real-time transcription across languages  within one continuous session, enabling natural code-switching without  reinitialization. Speech output is generated via Aura-2, with voices updated  dynamically as language context changes to maintain persona consistency. 

The reasoning layer focuses on corrective feedback and guided conversation  rather than task execution. Because multilingual STT, dynamic TTS switching,  and localized prompting all operate inside the same streaming loop, the  agent preserves timing and conversational flow even as languages change  mid-session. 

This architecture directly operationalizes the multilingual strategies described  earlier: unified transcription, adaptive synthesis, and language-aware  prompting coordinated in real time. 

**When to use** 

Language learning, global assistants, or cross-market applications that require  seamless multilingual interaction within a single conversation.   
**Tier 3 – Integrated and Distributed Systems** 

**Telephony Voice Agent (PSTN / SIP Frontend)** 

**Reference Implementation: Documentation** and **GitHub** 

This pattern connects Deepgram’s Voice Agent API to traditional phone networks via Twilio Media Streams, enabling real-time, natural conversations  over PSTN or SIP.   
CHAPTER 6: APPLIED ARCHITECTURES 74**Topology** 

WebSocket 

Phone Call 

8kHz µ-law 

**Caller PSTN/SIP Phone Network** 

Telephony 

**Twilio Media  Stream** 

**WebSocket  Bridge**   
Real-time Stream 

**Async**   
**Orchestrator Python/** 

**Coordinator Server**   
Voice Agent API 

STT \+ TTS **Deepgram Voice  Agent API** 

Nova 3 \+ Reasoning 

\+ Aura-2   
CHAPTER 6: APPLIED ARCHITECTURES 75

Twilio bridges 8 kHz μ-law audio from the phone network into a bidirectional WebSocket stream. The Voice Agent API handles  transcription, reasoning, and synthesis, returning Aura-2 audio  that Twilio injects directly back into the live call. A small async  server coordinates inbound audio, outbound playback, and  interruption handling. 

Key capabilities are built into the topology: 

• Low-latency turn-taking with barge-in support 

• DTMF handling for IVR-style interactions 

• Session-level call control and clean teardown 

• Secure, token-based authentication for live streams 

This architecture modernizes legacy IVR and call-center systems  without requiring custom telephony stacks. It preserves PSTN  compatibility while enabling real-time AI interaction and observability  through streamed transcripts.   
**When to use** 

Inbound or outbound phone agents, IVR modernization, customer support  automation, or agent-assist systems that must operate over standard  telephone infrastructure. 

**Multi-Agent Orchestration (Specialized Agents with Context Handoff) Reference Implementation: GitHub** 

This pattern scales a single voice agent into a coordinated system  of specialized sub-agents, each responsible for a distinct phase of a  conversation. A central orchestrator maintains the live audio stream while  rotating agents behind the scenes.   
CHAPTER 6: APPLIED ARCHITECTURES 76**Topology** 

Bidirectional 

Phase 1   
**Qualifier Agent** 

Summarize & Handoff 

Session 

**Twilio Media Stream (Persistent WebSocket)**   
Audio   
**Call Orchestration Manages Phases**   
Phase 2 Session   
**Advisor**   
**Agent** 

Summarize 

& Handoff 

**Deepgram Voice Agent API (Creates session per agent)** 

Phase 3 Session **Closer**   
**Agent**   
CHAPTER 6: APPLIED ARCHITECTURES 77 

A persistent Twilio WebSocket carries audio for the entire call. The  orchestrator keeps this connection open while creating short-lived Voice Agent  sessions for each sub-agent. Each agent runs with a focused prompt, limited  toolset, and clear role, then hands off control when its task is complete. 

Between phases, the orchestrator summarizes the prior exchange and injects  that summary as context for the next agent. This prevents prompt bloat,  isolates failures, and keeps reasoning targeted. Audio streaming continues  uninterrupted across agent transitions, so the caller experiences a single,  continuous conversation. 

This architecture enables: 

• Explicit phase separation and cleaner reasoning 

• Controlled context growth through summarization 

• Easier debugging and evaluation per agent role 

• Flexible composition of complex workflows 

**When to use** 

Multi-step interactions such as sales qualification, onboarding, triage,  or claims processing, where different conversational stages benefit from  distinct prompts, logic, or success criteria. 

**Tier 4 – Low-Level and Edge Implementations** 

**Native SDK / Embedded Voice Agent (Rust)** 

**Reference Implementation: GitHub** 

This pattern demonstrates a fully custom voice agent built directly on  Deepgram’s WebSocket APIs, without the managed Voice Agent runtime. Implemented in Rust, it prioritizes low latency, deterministic control,  and tight integration with local audio hardware.  
CHAPTER 6: APPLIED ARCHITECTURES 78**Topology** 

Rust Agent Application 

**CPAL** 

**WebSocket**  

Synthesized 

**Rodio**   
Playback 

Capture   
Audio Stream (Auto-mute mic) Speech   
**Audio**   
**Client**   
**Audio**   
**Microphone Speaker**   
**Capture**   
**(Async I/O)** 

Bidirectional 

WebSocket   
**Playback** 

**Deepgram WebSocket APIs**   
**Nova-3 (STT) \+ LLM**    
**\+ Aura-2 (TTS)**   
CHAPTER 6: APPLIED ARCHITECTURES 79 

The agent streams microphone audio to Deepgram for real-time transcription  and reasoning, then plays synthesized speech locally with precise timing.  Audio input and output are handled asynchronously, with automatic  microphone muting during playback to prevent feedback and support natural  turn-taking. 

Configuration is explicit and lightweight: 

• **Listen:** Nova-3 (streaming STT) 

• **Think:** compact reasoning model 

• **Speak:** Aura-2 voice 

• **Audio:** linear PCM with device-level control 

This architecture exposes the full speech pipeline while avoiding unnecessary  abstractions. It is well suited to environments where latency budgets are tight,  dependencies must be minimal, or cloud-managed runtimes are not viable. 

**When to use** 

Edge devices, kiosks, embedded systems, IVR gateways, or on-prem  deployments that require maximum control over audio I/O, threading,  and runtime behavior.   
**Synthesis: The Architecture Continuum** 

These reference architectures form a practical continuum: 

| Tier  | Focus  | Example Patterns  | When to Use |
| :---- | :---- | :---- | :---- |
| **1**  | Unified simplicity  | Baseline Agent,   Function Calling | Prototypes and managed  agents |
| **2**  | Specialization  | Medical Assistant,   Language Coach | Domain or multilingual   systems |
| **3**  | Integration  | Telephony, Multi-Agent  Orchestration | Enterprise workflows |
| **4**  | Performance & control  | Native SDK / Edge   Agent | On-prem and embedded  environments |

Most real-world deployments evolve across tiers. Teams often begin with  a managed, end-to-end agent and progressively introduce custom  orchestration, telephony, or edge execution as requirements grow.  Deepgram’s APIs and runtime model support this progression without forcing architectural resets, allowing systems to scale in complexity  while preserving real-time conversational performance.  
CHAPTER 6: APPLIED ARCHITECTURES 80

**Ecosystem Patterns (Integrations)** 

The previous section focused on reference architectures owned end to end by  

the builder. This section shows how those same architectural principles appear  

in **ecosystem integrations**, where Deepgram provides the real-time speech  

layer inside partner-managed orchestration, transport, or enterprise platforms. 

Each pattern below represents a distinct integration topology and clarifies how  

responsibility is divided between Deepgram and the surrounding system. 

**VAPI Orchestrated Agent (Managed Platform Topology)** 

**Reference: Vapi documentation** 