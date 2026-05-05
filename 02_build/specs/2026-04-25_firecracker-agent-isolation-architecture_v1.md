---
title: "Firecracker MicroVM Agent Isolation — Architecture Brief"
id: firecracker-agent-isolation-arch-v1
version: 1
created: 2026-04-25
type: architecture-brief
topic_type: infrastructure
audience: Ewan, build agents
layer: 02_build
status: draft
confidence: 82
signed_by: "Signed-by: Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Firecracker MicroVM Agent Isolation — Architecture Brief

## Decision

Run all agent execution workloads inside Firecracker microVMs on the Beast (Hetzner AX-146-R, AMD EPYC, 128GB RAM). Beast remains the single infrastructure node for inference, data, and agent compute. No cloud VMs required.

## Status

DRAFT — requires Ewan's approval before promotion to `00_authority/DECISION_LOG.md`. This is an irreversible architecture choice (95% confidence floor per OPINION_CONFIDENCE rules). Current confidence: **82%** — research validates feasibility but no hands-on proof-of-concept yet. Recommend a bounded spike (2–4 hours) to validate before committing.

## Context

The Cognition team (Devin's builders) published findings from 2+ years of cloud agent infrastructure: containerised agents share a kernel (security risk), cannot snapshot/resume across async gaps, and lack the isolation needed for multi-tenant workloads. Their solution: VM-level isolation with Firecracker microVMs plus hypervisor-level state snapshotting.

Amplified Partners' architecture already specifies:
- Local LLMs on Beast for inference (Llama 3.3 70B via vLLM)
- QDRANT vector DB on Beast for retrieval
- Cove-orchestrator + Temporal for agent orchestration
- Cloud models (Claude, GPT-4) for reasoning via LiteLLM

The missing piece: **where do the agents that execute tasks actually run?** This brief answers: on Beast, inside Firecracker microVMs, orchestrated by Temporal.

## Why Firecracker

| Property | Firecracker | Containers | Cloud VMs |
|----------|-------------|------------|-----------|
| Kernel isolation | Full (each VM = own kernel) | Shared kernel | Full |
| Boot time | <125ms (8ms CPU time on bare metal) | <1s | 30–60s |
| Memory overhead | ~5MB per VM | ~1MB | ~256MB+ |
| Snapshot/resume | <28ms restore | Not reliable | Provider-dependent |
| Cost | €0 (own hardware) | €0 | €4–40/month per VM |
| Attack surface | Minimal (no device emulation beyond virtio-net/block) | Large (shared kernel, cgroups escape) | Provider-managed |

Firecracker is what AWS Lambda and Cognition/Devin both use. It is production-proven at massive scale.

## AMD EPYC Compatibility

Firecracker on AMD EPYC is verified in production:
- Hetzner dedicated AMD EPYC servers show near-native performance: 8.7s host vs 10.4s in Firecracker (19% overhead on compute-intensive builds)
- KVM support via AMD-V is required — must be enabled in BIOS (should already be on AX-146-R)
- No known EPYC-specific gotchas beyond ensuring `kvm_amd` module is loaded

**Prerequisite check (run on Beast):**
```bash
lsmod | grep kvm_amd
# Should show kvm_amd loaded
# If not: sudo modprobe kvm_amd
```

## Capacity Estimate

With 128GB RAM on the AX-146-R:

| Per-VM allocation | Max concurrent VMs | Use case |
|-------------------|-------------------|----------|
| 256MB (minimal) | ~450 | Lightweight script execution |
| 512MB (typical) | ~220 | Standard agent workload |
| 1GB (generous) | ~110 | Agent + local tools + build |
| 2GB (heavy) | ~55 | Agent + full dev environment |

Reserve 16GB for host (OS, QDRANT, LLM inference, Temporal). Realistic sweet spot: **50–100 concurrent agent VMs at 1GB each**, with headroom for inference workloads.

CPU: AMD EPYC supports 1–128 vCPU per guest. With 16+ cores available, allocating 1–2 vCPU per agent VM allows 8–16 concurrent CPU-active agents without oversubscription.

## Networking Isolation

Each microVM gets a dedicated TAP device for L2 isolation:

```
Host (Beast)
├── eth0 (public interface)
├── tap0 → microVM-0 (10.200.0.2/24)
├── tap1 → microVM-1 (10.200.1.2/24)
├── tap2 → microVM-2 (10.200.2.2/24)
└── firecracker0 (bridge, optional VM-VM comms)
```

Per-VM setup (automated by orchestrator):
1. Create TAP device: `ip tuntap add dev tapN mode tap`
2. Assign host-side IP: `ip addr add 10.200.N.1/24 dev tapN`
3. Enable forwarding + NAT masquerade via iptables/nftables
4. Register TAP with Firecracker via REST API
5. Guest configures eth0 with 10.200.N.2/24, default route via host IP

Client data isolation: each microVM only accesses its assigned client's data. No shared filesystem between VMs.

## Snapshot/Resume for Async Agent Work

This is the critical capability for agent orchestration:

1. Agent starts task (e.g., "write PR for client X")
2. Agent opens PR, needs to wait for CI → **snapshot VM state**
3. VM memory + disk written to NVMe storage, compute released
4. CI completes → **restore VM from snapshot in <28ms**
5. Agent continues exactly where it left off

Firecracker exposes this via REST API:
- `PUT /snapshot/create` — captures full VM state (memory + device state)
- `PUT /snapshot/load` — restores from snapshot file
- Snapshots stored on Beast's NVMe — fast I/O, no network latency

## Temporal Integration Pattern

```
Temporal Server (on Beast)
│
├── Workflow: AgentTaskWorkflow
│   ├── Activity: ProvisionFirecrackerVM(client_id, task_spec)
│   │   └── Creates TAP, boots microVM, injects task
│   ├── Activity: MonitorExecution(vm_id)
│   │   └── Polls agent progress, handles heartbeats
│   ├── Activity: SnapshotVM(vm_id) — on async gap
│   │   └── Calls Firecracker snapshot API, stores to NVMe
│   ├── Signal: ExternalEvent (CI result, review comment)
│   │   └── Triggers RestoreVM activity
│   ├── Activity: RestoreVM(vm_id, snapshot_path)
│   │   └── Loads snapshot, resumes execution
│   └── Activity: DestroyVM(vm_id)
│       └── Cleanup: delete TAP, release memory, archive logs
│
├── Worker Pool: 4–8 Temporal workers on Beast
└── Task Queue: agent-tasks
```

**SDK choice:** `firecracker-go-sdk` (Go) or Python REST client for Temporal activities. The Go SDK is more mature for Firecracker lifecycle management; Python works if Temporal workers are Python-based (matching Cove-orchestrator).

## Risks and Open Questions

| Risk | Severity | Mitigation |
|------|----------|------------|
| Single point of failure (Beast goes down = all agents down) | Medium | Scheduled backups, monitoring, Hetzner cloud as failover |
| Snapshot storage fills NVMe | Low | TTL on snapshots (delete after 24h), monitor disk usage |
| AMD-V not enabled in BIOS | Low | Check with `lsmod`; Hetzner support can enable |
| Firecracker version compatibility | Low | Pin to stable release, test upgrades in shadow |
| No existing Temporal-Firecracker integration | Medium | Build custom activities (~2 days estimated) |
| Unknown: actual agent memory footprint | Medium | Spike required to measure realistic per-VM allocation |

## Recommended Next Steps

1. **Spike (2–4 hours):** Boot a Firecracker microVM on Beast, run a simple agent task, measure memory/CPU, test snapshot/restore
2. **If spike succeeds:** Build Temporal activities for VM lifecycle (provision, snapshot, restore, destroy) — ~2 days
3. **Promote to DECISION_LOG.md** with 95%+ confidence after spike validates
4. **Build the networking automation** — script to create/destroy TAP devices per VM — ~0.5 days
5. **Integration test:** Full Temporal workflow → Firecracker VM → agent executes → snapshot → restore → complete

## References

- Cognition (Devin): "What We Learned Building Cloud Agents" — 2026
- Firecracker NSDI'20 paper: <125ms boot, <28ms restore
- Hetzner AMD EPYC benchmarks: near-native performance in Firecracker
- firecracker-go-sdk: `github.com/firecracker-microvm/firecracker-go-sdk`
- firecracker-containerd: `github.com/firecracker-microvm/firecracker-containerd`

Signed-by: Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd
