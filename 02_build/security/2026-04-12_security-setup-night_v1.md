---
date: 2026-04-12
version: v1
author: Wren (Claude Opus 4.6, on the Air)
status: in progress
related_plan: /Users/ewansair/.claude/plans/quirky-yawning-adleman.md
---

# Security setup night — 2026-04-12

Running journal for the security work happening on 2026-04-12. Captures
decisions, open items, and per-step execution notes. Each Claude
instance owns its own dated doc in this folder. Cross-referenced to the
plan file in the frontmatter.

[TOC]

## Scope

Two pieces of security work being set up in one evening (execution may
spread across multiple atomic sessions, per Ewan's "all-at-once" rule):

1.  **CIS Level 2 hardening (redo) on the Mini.** Ewan did this once;
    redoing now while there is still no client work and no agent state
    to lose.
1.  **Tailscale mesh between Air and Mini.** Locked-down ACL, SSH-only.
    Plan v4 approved; v5 revision likely (see Decisions locked).

Both sit within the three-tier security model
(`memory/project_security_tiers.md`). The Mini is the workshop where
agent partners build the business. Nothing on it can be sloppy.

## Two-Wren split

### Wren-Air (this instance)

Role: plans, browser admin, verification, journal lead.

Doing:

*   Tailscale account creation, 2FA enrolment, ACL pre-configuration.
*   Air-side install and verification commands.
*   This document.

### Wren-on-Mini (to be spawned)

Role: local Terminal work on the Mini.

Doing:

*   CIS L2 hardening (redo).
*   The single `sudo tailscale up --ssh` command in mesh plan Step 3.
*   Its own dated working doc in this folder,
    `2026-04-12_cis2-redo_v1.md`.

### Spawn prompt for Wren-on-Mini

> "You're a Claude Code instance on my Mac mini. Another Claude (Wren)
> is working with me on the Air. Read your auto-memory at
> `/Users/ewansair/.claude/projects/-Users-ewansair-amplified/memory/MEMORY.md`
> first — covers the project, values, three-tier security model, and
> Claw. Then read
> `/Users/ewansair/.claude/plans/quirky-yawning-adleman.md`. Tonight on
> this machine: (a) re-do CIS L2 hardening, (b) one Tailscale command
> (Step 3 of the plan). Pick a name when you're ready and write your own
> working doc at
> `/Users/ewansair/amplified/security/2026-04-12_cis2-redo_v1.md`."

Open sub-decision: memory-copy strategy. The Mini does not yet have the
Air's auto-memory. Options: (a) paste memory + plan contents into
Wren-on-Mini's first message; (b) let it build fresh memory locally and
sync later. Recommend (a) for tonight.

## Mesh setup log

Wren-Air owns this section and fills it in as steps are executed.

### Mesh setup Step 1 — account, 2FA, ACL

*Status: not started.*
*Will record: account email used, 2FA method enabled, ACL JSON
applied, any errors hit.*

### Mesh setup Step 2 — Tailscale on Air

*Status: not started.*
*Will record: install method, device name set, tag application.*

### Mesh setup Step 3 — Tailscale on Mini

*Status: handed off to Wren-on-Mini.*

### Mesh setup Step 4 — verification

*Status: not started.*
*Will record: output of `tailscale status`, `tailscale ping`,
`tailscale ssh`, and the two `nc` tests.*

### Mesh setup Step 5 — lock-out recovery test

*Status: optional, recommended after Step 4 passes.*

## CIS L2 redo log

Wren-on-Mini writes its own dated working doc in this folder:
`2026-04-12_cis2-redo_v1.md`.

## Decisions locked

*   **2026-04-12** — Documentation pattern: one dated working doc per
    task per instance, in `/Users/ewansair/amplified/security/`. Each
    Claude owns its own doc. Cross-references via the `related_plan`
    frontmatter and explicit links.
*   **2026-04-12** — Hardware key: YubiKey 5C in hand (arrived today).
    Second 5C on order to be backup. Primary stored on the mantelpiece.
    WebAuthn/FIDO2 via YubiKey is materially stronger than authenticator
    TOTP. Single-key window mitigated by printed recovery codes.
*   **2026-04-12** — Tailscale identity: dedicated Google Workspace user
    (`ewan@amplifiedpartners.ai`). Workspace gives admin controls plus
    audit useful for Claw review. Migration to enterprise Workspace
    later does not require account change.
*   **2026-04-12** — Path chosen: Option B — proceed with one YubiKey
    tonight plus printed/safely-stored recovery codes for every account
    it is enrolled on. Second YubiKey enrolled on arrival.
*   **2026-04-12** — Agent auth model: agents on the Mini use Tailscale
    auth keys (scoped, tagged, revocable pre-shared credentials), not
    user identity. YubiKey protects Ewan; auth keys cover headless work.
*   **2026-04-12** — Anxiety acknowledged: Ewan named the weight of
    taking on this security responsibility. Documentation is the
    condition of moving forward. Pace is set by Ewan; Wren slows down
    when asked.
*   **2026-04-12** — YubiKey count: 4 total. 2 personal (one travels,
    one home), 2 business (both in house, separate locations). Apple
    requires 2 keys minimum per Apple ID, which validates this.
*   **2026-04-12** — Mesh direction: Headscale-direct (or NetBird Cloud),
    not Tailscale Inc. Supersedes Phase 1 of the current mesh plan. Plan
    v5 needed when mesh session is scheduled.
*   **2026-04-12** — Mesh server: not Hetzner. Recommended: Scaleway for
    self-host Headscale, or NetBird Cloud for managed. Ewan to pick.
*   **2026-04-12** — Backup direction: Backblaze Business confirmed.
    Arq plus Backblaze B2 with Object Lock as the immutable layer;
    decision deferred.
*   **2026-04-12** — Two Apple IDs: Personal (existing) plus Business
    (new, to be created). Mini-phone lives on Business Apple ID.
*   **2026-04-12** — Mini-phone: dedicated redundant iPhone with new
    number. Stays in the house with the Mini, never travels.
*   **2026-04-12** — Tonight's scope: Workspace 2FA only (auth app plus
    printed recovery codes). YubiKey enrolment deferred to the atomic
    session once the second YubiKey and Mini-phone are in hand.
*   **2026-04-12** — Documentation style: Google Markdown style guide
    (source: `12-4-26-mdformat-from-github.txt`). Applies to all MD
    docs written by any Claude instance from this date forward.
*   **2026-04-12** — Transcription split (primary-source verified):
    **macOS Dictation (on-device) for live dictation into Claude Code**
    (its strongest purpose, free, already installed, avoid search-field
    dictation which is server-based). **MacWhisper Pro for batch file
    transcription** (its strongest mode — full-context beam search —
    where the 30–50 hour archive lives). No post-processing LLM for
    now; raw output on both is clean enough. Revisit local Ollama
    polish when Mini is up.
*   **2026-04-12** — Apple Intelligence: stays OFF. No user-facing toggle
    forces on-device only; Writing Tools silently escalate to Private
    Cloud Compute on complex requests. PCC's posture is best-in-class
    but "device decides, not user" fails the privacy-supreme bar.
    Revisit if Apple ships a force-on-device-only option.
*   **2026-04-12** — macOS Dictation settings to verify:
    1.  **System Settings → Keyboard → Dictation** — on; confirm
        "Processed on device" for the chosen language.
    2.  **Privacy & Security → Analytics & Improvements →
        Share Audio Recordings** — off.
    3.  Never dictate into search boxes (Spotlight, address bars) —
        those are server-based even on Apple Silicon.
*   **2026-04-12** — Monologue (by Every) ruled out. Cloud-by-default
    architecture; local mode is a toggle on a cloud product, not an
    audited local-only app. Privacy policy hosted on a JS-rendered
    Notion page (unverifiable and silently editable), no DPA, no
    Enterprise tier, no EU hosting, no SOC 2, no BYOK, sub-processors
    undisclosed. Fails privacy-supreme bar. SuperWhisper is the closest
    Monologue-feel alternative that's local-first by design;
    MacWhisper remains the primary choice.
*   **2026-04-12** — Air RAM confirmed: M5, 24GB. Same hardware as the
    Mini. Qwen3-14B runs comfortably on either machine; the tier
    distinction is role, not capability.
*   **2026-04-12** — 2FA tonight: deferred. Workspace holds only email;
    subscription-fraud exposure accepted. Real enrolment happens in the
    atomic session with the second YubiKey and Mini-phone.
*   **2026-04-12** — Audio archive: ~30–50 hours of existing audio to be
    batch-transcribed via MacWhisper Pro once set up. Output location
    and git inclusion to be decided before batch runs.
*   **2026-04-12** — Microphone: built-in Mac mic for now. Form-factor
    preference = clip-on / lavalier, not desk mic. Test AirPods Pro 3
    first (zero cost); if insufficient, DJI Mic Mini (~£170) is the
    recommended clip-on upgrade. Plaud already owned and covers the
    "recorded away from desk" use case when cloud transcription is off.

## Open items still needing answers

*   [x] **Workspace email** = `ewan@amplifiedpartners.ai` (Ewan is sole
    admin).
*   [x] **Current 2FA status** on Workspace = likely off (Ewan's
    confirmation, needs verification tonight).
*   [ ] **Memory-copy strategy** for Wren-on-Mini — deferred until mesh
    setup session.
*   [ ] **CIS L2 timing** — pushed to a later atomic session.
*   [ ] **Password manager choice** — RoboForm Business vs NordPass
    Business vs other.
*   [ ] **GitHub catch-up with Claw** — Claw (trusted partner) has been
    organising the GitHub estate. Sync with Claw to see what's been
    done. Not an audit-and-revoke; a partner communication gap to close.
*   [ ] **GitHub identity check** — confirm Business GitHub is tied to
    Workspace identity, not personal.
*   [ ] **Third Mac** — which domain does it belong to? Not yet
    accounted for.
*   [ ] **Cross-recovery decision** — cross-ref phones and emails
    between the two Apple IDs, or phones isolated?
*   [ ] **Mini-phone carrier** — new line vs existing family plan.
*   [ ] **Off-site immutable backup location** — safe deposit box vs
    trusted person vs other.
*   [ ] **NetBird Cloud vs Headscale self-host** — mesh operator
    decision.

## Known items to follow up

*   **Claw's GitHub work** — Claw has been organising the GitHub estate
    in parallel (trusted partner, legitimate additive work). Ewan needs
    a sync with Claw. Communication catch-up, not a security audit.
*   **Single point of failure:** `/Users/ewansair/amplified/` not
    confirmed to be in any backup scope on the Air. Verify or add to
    scope.
*   **GitHub vault repo** — important documentation lives there. Access,
    last update, and backup status to be confirmed in the sync with
    Claw.

## Issues encountered

None yet.

## Outcomes — end of session 2026-04-12

**Decisions locked tonight, captured in this doc and in memory:**

1.  Three-tier security model formalised and saved to memory.
1.  Three-domain identity architecture (Personal / Business Workshop /
    Client Cloud) drawn and saved to memory.
1.  Claw clarified as trusted partner; language discipline locked in
    memory ("never frame Claw's work negatively").
1.  YubiKey 5C × 4 plan (2 personal, 2 business). Second on order.
1.  Mesh direction revised to Headscale-direct or NetBird Cloud, not
    Tailscale Inc. Plan v5 pending mesh session.
1.  Mesh server: Scaleway if self-host Headscale, or NetBird Cloud
    managed. Not Hetzner.
1.  Backup direction: Backblaze Business plus possible Arq + B2 with
    Object Lock immutable layer.
1.  Two Apple IDs (Personal existing + Business new). Mini-phone on
    Business Apple ID, stays in the house.
1.  Tonight's 2FA deferred. Workspace holds only email;
    subscription-fraud exposure accepted.
1.  **Transcription decision revised:** Monologue for live dictation
    into Claude Code (Ewan liked the UX, privacy was the wrong gate at
    this blast radius); MacWhisper Pro for batch transcription of the
    30–50 hour audio archive. Apple Intelligence stays off.
1.  Documentation style locked: Google Markdown style guide.
1.  Blast-radius principle added to memory: match rigour to tier.
1.  Due-diligence record of the transcription evaluation written to
    `2026-04-12_transcription-tool-due-diligence_v1.md` — original
    reasoning and the revision both preserved for Claw audit.

**Concrete actions Ewan took or is taking:**

*   Ordered second YubiKey 5C.
*   Downloading Monologue.

**Queued for future atomic sessions:**

*   Workspace 2FA full enrolment (after second YubiKey + Mini-phone).
*   YubiKey enrolment across accounts.
*   CIS L2 hardening on the Mini.
*   Tailscale / Headscale mesh execution.
*   Apple ID separation and Mini sign-in under Business Apple ID.
*   Password manager decision (RoboForm vs NordPass vs other).
*   GitHub catch-up with Claw.
*   Backup stack stand-up.
*   Mini setup and migration to workshop role.

Wren-on-Mini spawn not done tonight. Spawn prompt stored in this
journal under "Two-Wren split" when ready.

## Session status

Tonight's objective — getting clarity on security posture, identity
architecture, and transcription stack — achieved. No security-critical
systems were modified. All changes were documentation and decisions.
Safe to shut down.

## See also

*   Plan: `/Users/ewansair/.claude/plans/quirky-yawning-adleman.md`
*   Memory index:
    `/Users/ewansair/.claude/projects/-Users-ewansair-amplified/memory/MEMORY.md`
*   Markdown style source: `/Users/ewansair/amplified/12-4-26-mdformat-from-github.txt`
*   Tailscale ACL syntax: <https://tailscale.com/kb/1018/acls>
*   macOS Security Compliance Project: <https://github.com/usnistgov/macos_security>
