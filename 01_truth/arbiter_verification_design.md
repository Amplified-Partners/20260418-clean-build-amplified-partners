# Arbiter Cryptographic Verification Design
**Antigravity | 2026-05-05 | Status: Phase 2 Blueprint**

## Overview
Currently, an Arbiter's approval is just a string or a boolean flag (`approved=true`). In a zero-trust, IBAC-governed sovereign fleet, a string is a massive security gap. Any agent can spoof `approved=true`. We need cryptographic signatures to prove that the Arbiter (Alpha or Antigravity) definitively authorized an action.

## Implementation Blueprint

### 1. Key Generation
On container boot, each agent generates a localized Ed25519 keypair. The public keys are registered in the central Postgres `agent_registry` table.

### 2. The Signing Protocol
When an Arbiter approves a deployment or a destructive Git push:
- The Arbiter takes the SHA-256 hash of the proposed payload (e.g., the commit diff or the docker-compose YAML).
- The Arbiter signs the hash using its private Ed25519 key.
- The signature is attached to the payload as an `x-arbiter-signature` header.

### 3. The Verification Gate (Kimmy / Charlie)
Before the Plumber (Charlie) or Orchestrator (Kimmy) executes the payload:
- They intercept the `x-arbiter-signature`.
- They retrieve the Arbiter's public key from Postgres.
- They verify the signature against the payload hash.
- If the signature is invalid or missing, the action is hard-blocked and an alert is fired to the CyberAuditLogger.

## Security Posture
This closes the spoofing gap. A compromised or hallucinating agent cannot trick the fleet into deploying code without a genuine signature from the Arbiter's secure enclave.
