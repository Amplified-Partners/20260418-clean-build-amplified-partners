# Dedup Statistics Report

Generated: 2026-04-27 03:04 UTC
Signed-by: Devon (Devin) | 2026-04-27 | session 7cd95caf339c46a2896fbf6ffbda02be

---

## Summary

| Metric | Value |
|--------|-------|
| Total files scanned | 5,505 |
| Unique files (SHA-256) | 5,445 |
| Exact duplicate sets | 51 |
| Duplicate files (would be removed) | 60 |
| Bytes that would be saved | 980.6 KB |
| Near-duplicate pairs (ssdeep >90) | 1,459 |
| Possible near-duplicates (60-90) | 37,085 |

---

## Files by Directory

| Directory | Files |
|-----------|-------|
| corpus-raw/vault/transcripts | 2,214 |
| corpus-raw/vault/_inbox-voice | 888 |
| corpus-raw/vault/_staging | 624 |
| clean-build/90_archive | 404 |
| corpus-raw/vault/_inbox | 359 |
| clean-build/01_truth | 236 |
| corpus-raw/vault/research | 169 |
| clean-build/02_build | 134 |
| corpus-raw/vault/imported-business-docs | 122 |
| clean-build/03_shadow | 101 |
| corpus-raw/vault/work | 96 |
| corpus-raw/vault/work-covered-ai | 79 |
| corpus-raw/vault/infra-ai-stack | 17 |
| corpus-raw/vault/knowledge-qdrant | 14 |
| corpus-raw/vault/projects | 13 |
| corpus-raw/vault/scripts | 11 |
| corpus-raw/vault/_inbox-uncategorised | 7 |
| corpus-raw/vault/therapy-suite | 5 |
| corpus-raw/vault/_system | 4 |
| corpus-raw/vault/(root) | 2 |
| corpus-raw/vault/_inbox-work | 2 |
| corpus-raw/vault/.github | 2 |
| corpus-raw/vault/the-room | 1 |
| corpus-raw/vault/eli | 1 |

## Files by Extension

| Extension | Files |
|-----------|-------|
| .md | 5,253 |
| .py | 160 |
| .json | 13 |
| .sh | 11 |
| .tsx | 10 |
| .xlsx | 9 |
| .ts | 9 |
| (no ext) | 7 |
| .pdf | 6 |
| .txt | 5 |
| .yml | 5 |
| .csv | 3 |
| .sql | 3 |
| .ps1 | 1 |
| .example | 1 |
| .worker | 1 |
| .nightscout-mcp | 1 |
| .nightscout | 1 |
| .html | 1 |
| .db-shm | 1 |
| .db-wal | 1 |
| .voice | 1 |
| .db | 1 |
| .css | 1 |

---

## Tier 1: Exact Duplicates (SHA-256)

- **51** duplicate sets containing **111** files
- **60** redundant copies that could be removed
- **980.6 KB** would be reclaimed

### Top 20 Most-Duplicated Files

| Copies | Size | Keeper | Other locations |
|--------|------|--------|-----------------|
| 6 | 0.0 B | `clean-build/02_build/cove-orchestrator/mcp-servers/email-mcp/__init__.py` | corpus-raw/vault/_inbox/2026-02-08.md; clean-build/02_build/cove-orchestrator/temporal/activities/__init__.py; clean-build/02_build/cove-orchestrator/temporal/workers/__init__.py; clean-build/02_build/cove-orchestrator/temporal/workflows/__init__.py; clean-build/02_build/command-centre/backend/searches.db-wal |
| 4 | 6.9 KB | `corpus-raw/vault/research/2026-02-24-session-notes-2026-02-11.md` | corpus-raw/vault/research/2026-02-24-session-notes-2026-02-11-e723b0.md; corpus-raw/vault/_inbox/session-notes-2026-02-11-v2.md; corpus-raw/vault/_inbox/session-notes-2026-02-11.md |
| 3 | 7.9 KB | `corpus-raw/vault/research/2026-02-24-technical-decision-self-hosted-only.md` | corpus-raw/vault/research/2026-02-24-TECHNICAL-DECISION-SELF-HOSTED-ONLY-e8ced0.md; corpus-raw/vault/_inbox/TECHNICAL-DECISION-SELF-HOSTED-ONLY.md |
| 3 | 5.2 KB | `corpus-raw/vault/work/sessions/gates/COMMITMENT-SYSTEM-REVIEW.md` | corpus-raw/vault/imported-business-docs/openclaw-workspace/COMMITMENT-SYSTEM-REVIEW.md; corpus-raw/vault/imported-business-docs/openclaw-workspace/REVIEW.md |
| 3 | 27.1 KB | `corpus-raw/vault/imported-business-docs/openclaw-workspace/PERSONA-TECH-STACKS.md` | corpus-raw/vault/projects/PERSONA-TECH-STACKS.md; corpus-raw/vault/projects/personas/PERSONA-TECH-STACKS.md |
| 2 | 5.4 KB | `corpus-raw/vault/research/2026-02-25-staged-sprouting-sifakis.md` | corpus-raw/vault/_inbox/2026-02-25-staged-sprouting-sifakis.md |
| 2 | 6.9 KB | `clean-build/03_shadow/sessions/2026-02-24_publishing-sequence_v1.md` | corpus-raw/vault/research/2026-02-24-PUBLISHING-SEQUENCE.md |
| 2 | 4.5 KB | `corpus-raw/vault/research/2026-02-25-cuddly-munching-popcorn.md` | corpus-raw/vault/_inbox/2026-02-25-cuddly-munching-popcorn.md |
| 2 | 1.7 KB | `corpus-raw/vault/research/2026-02-24-content-draft-001-linkedin-first-post.md` | corpus-raw/vault/_inbox/content/content-draft-001-linkedin-first-post.md |
| 2 | 8.0 KB | `clean-build/03_shadow/sessions/2026-02-24_dave-workflow-spec_v1.md` | corpus-raw/vault/research/2026-02-24-DAVE-WORKFLOW-SPEC-V1-68138e.md |
| 2 | 4.5 KB | `corpus-raw/vault/research/2026-02-25-jaunty-kindling-shore-8251ac.md` | corpus-raw/vault/_inbox/2026-02-25-jaunty-kindling-shore-8251ac.md |
| 2 | 3.3 KB | `corpus-raw/vault/research/2026-02-25-logical-percolating-swan.md` | corpus-raw/vault/_inbox/2026-02-25-logical-percolating-swan.md |
| 2 | 4.9 KB | `corpus-raw/vault/research/2026-02-25-jaunty-kindling-shore.md` | corpus-raw/vault/_inbox/2026-02-25-jaunty-kindling-shore.md |
| 2 | 2.2 KB | `corpus-raw/vault/research/2026-02-25-abundant-growing-emerson.md` | corpus-raw/vault/_inbox/2026-02-25-abundant-growing-emerson.md |
| 2 | 4.4 KB | `corpus-raw/vault/research/2026-02-24-FILESYSTEM-SWEEP-COMPLETE.md` | corpus-raw/vault/_inbox/FILESYSTEM-SWEEP-COMPLETE.md |
| 2 | 1.7 KB | `corpus-raw/vault/work/sessions/gates/content-draft-001-linkedin-first-post.md` | corpus-raw/vault/imported-business-docs/openclaw-workspace/content-draft-001-linkedin-first-post.md |
| 2 | 194.0 B | `corpus-raw/vault/work/sessions/gates/IDENTITY.md` | corpus-raw/vault/imported-business-docs/openclaw-workspace/IDENTITY.md |
| 2 | 3.2 KB | `corpus-raw/vault/work/sessions/gates/TELEGRAM-BOT-SETUP.md` | corpus-raw/vault/imported-business-docs/amplified-crm-docs/TELEGRAM-BOT-SETUP.md |
| 2 | 1.5 KB | `corpus-raw/vault/work/sessions/gates/content-draft-002-linkedin-immutable-accountability.md` | corpus-raw/vault/imported-business-docs/openclaw-workspace/content-draft-002-linkedin-immutable-accountability.md |
| 2 | 1.3 KB | `corpus-raw/vault/work/sessions/gates/content-draft-001-linkedin-ai-what-is-it.md` | corpus-raw/vault/imported-business-docs/openclaw-workspace/content-draft-001-linkedin-ai-what-is-it.md |

### Vault Subdirectory Duplication

| Vault subdirectory | Files in duplicate sets |
|--------------------|------------------------|
| imported-business-docs | 35 |
| research | 14 |
| work | 14 |
| _inbox | 12 |
| work-covered-ai | 8 |
| projects | 5 |
| _inbox-voice | 1 |
| transcripts | 1 |

---

## Tier 2: Fuzzy Near-Duplicates (ssdeep)

| Score band | Pairs |
|------------|-------|
| 90+ (auto-flag) | 1,459 |
| 80-90 | 4,215 |
| 70-80 | 14,563 |
| 60-70 | 18,307 |

---

## Known Problem Areas

| Area | Duplicate sets |
|------|---------------|
| `vault/_inbox/` vs `vault/research/` overlap | 10 |
| `vault/_inbox-voice/` timestamp pairs | 1 |
| `vault/transcripts/monologue/` vs `monologue-full/` | 0 |
| `corpus-raw/vault/` vs `clean-build/` cross-repo | 5 |

---

*This is a read-only analysis. No files were deleted or moved.*
