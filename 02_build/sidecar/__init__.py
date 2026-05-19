"""sidecar — ephemeral context for just-in-time assistance.

The sidecar provides session-scoped context that:
  - Has a TTL and is cleaned up deterministically
  - Never becomes a source of record for customer/contact data
  - Emits Vellum deletion receipts when context is destroyed
  - Keeps stable preference context separate from SaaS context

Signals extracted from sessions are candidate-only and permission-scoped.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""
