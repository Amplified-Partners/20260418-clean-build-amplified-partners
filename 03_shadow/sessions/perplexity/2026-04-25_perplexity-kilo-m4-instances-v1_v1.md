---
title: "How many kilo called? Kilo code Eh Instances Good I run. Effectively. One I've got. Docker. TheInstalled on my Mac. Eh M4 24 gigabyte"
id: "perplexity-kilo-m4-instances-v1"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "perplexity-session"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# How many kilo called? Kilo code Eh Instances Good I run. Effectively. One I've got. Docker. TheInstalled on my Mac. Eh M4 24 gigabyte

Based on my research, I can provide you with comprehensive guidance on running KiloCode instances on your MacBook Air M4 with 24GB RAM and Docker installed.

## Understanding KiloCode Instances

KiloCode instances can be run in multiple ways:[^1][^2][^3]

**Single Extension Mode:** The VS Code extension running interactive sessions
**CLI Mode:** Command-line instances that can run autonomously using the `--parallel` flag[^3][^4]
**Agent Manager Mode:** New feature allowing multiple parallel agents working on different branches[^2]

The number of instances you can effectively run depends primarily on the **local LLM models** you're running via Ollama, not KiloCode itself—KiloCode is lightweight, but the AI models consume the bulk of your resources.

## Memory Architecture: Your M4 Advantage

Your M4 MacBook Air with 24GB has significant advantages for local AI work:[^5]

- **Unified memory architecture:** GPU and CPU share the same RAM pool at 120 GB/s bandwidth[^6]
- **Efficient memory utilization:** macOS manages unified memory more efficiently than discrete GPU setups
- **No separate VRAM limitation:** Unlike discrete GPUs, your entire 24GB pool is available for model loading


## Model Memory Requirements

Here are the practical memory requirements for common models via Ollama:[^7][^8][^9]


| Model Size | Quantization | Memory Required | Performance on 24GB M4 |
| :-- | :-- | :-- | :-- |
| 3-7B | Q4_K_M | 4-6 GB | Excellent (77+ tokens/s)[^10] |
| 8B | Q4_K_M | 5-7 GB | Very Good (17-20 tokens/s)[^10] |
| 14B | Q4_K_M | 8-10 GB | Adequate (9-12 tokens/s)[^10] |
| 32B | Q4_K_M | 18-20 GB | Functional but slow[^11] |

## Docker Overhead Considerations

Docker Desktop on Mac adds significant overhead:[^12][^13][^14]

- **Base overhead:** 2-4 GB for Docker Desktop itself
- **Per-container overhead:** 200-500 MB depending on services
- **Important note:** Docker on Mac **does NOT support GPU acceleration** for Ollama—you should run Ollama **natively** on macOS, not in Docker[^15]


### Critical Recommendation

Run Ollama **natively** on your Mac, not inside Docker. Docker containers cannot access Apple Silicon GPU acceleration, which will severely degrade performance. Use Docker only for other services (databases, web servers, etc.).[^15]

## Practical Instance Limits for 24GB M4

### Scenario 1: Single Model, Multiple KiloCode Sessions (Recommended)

**Configuration:**

- 1 Ollama instance running natively
- 1 model loaded (7B or 8B Q4_K_M)
- Multiple KiloCode CLI sessions using the same model
- Docker running supporting services

**Memory Breakdown:**

- macOS system: 4-5 GB
- Ollama + 8B model: 6-7 GB
- Docker overhead: 2-3 GB
- Working headroom: 8-10 GB

**Practical limit:** **3-5 concurrent KiloCode sessions** sharing the same model[^16][^17]

This is enabled by Ollama's concurrent request handling. Configure:

```bash
export OLLAMA_NUM_PARALLEL=4
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_KEEP_ALIVE=-1  # Keep model in memory
```


### Scenario 2: Multiple Models, Sequential Usage

**Configuration:**

- Different models for different KiloCode modes
- Models loaded/unloaded dynamically
- Optimized for workflow flexibility

**Example Setup:**[^18]

- **Orchestrator mode:** DeepSeek-R1 7B (6 GB)
- **Code mode:** Qwen2.5-Coder 8B (6 GB)
- **Ask mode:** Gemma 2 3B (4 GB)

**Memory Breakdown:**

- macOS system: 4-5 GB
- Active model: 4-7 GB (swapped as needed)
- Docker: 2-3 GB
- Working headroom: 10-13 GB

**Practical limit:** **2 models loaded simultaneously** or **1-2 concurrent KiloCode instances** with automatic model switching[^17][^16]

Configure:

```bash
export OLLAMA_MAX_LOADED_MODELS=2
export OLLAMA_NUM_PARALLEL=2
```


### Scenario 3: Maximum Concurrency (Aggressive)

**Configuration:**

- Multiple small models loaded simultaneously
- Parallel CLI agents on separate branches
- Minimal Docker usage

**Models:**

- 2x Qwen2.5-Coder 7B Q4 (5 GB each) = 10 GB
- OR: 3x smaller 3B models (4 GB each) = 12 GB

**Memory Breakdown:**

- macOS system: 4 GB (optimized)
- Models: 10-12 GB
- Docker (minimal): 1-2 GB
- Working headroom: 6-9 GB

**Practical limit:** **2-3 concurrent agents** with independent models[^19][^20]

## Recommended Configuration for Your Setup

Based on your profile as an advanced user building AI-powered solutions, here's my recommended configuration:

### Optimal Setup

```bash
# Add to ~/.zshrc or ~/.bash_profile

# Ollama Configuration
export OLLAMA_NUM_PARALLEL=3           # 3 concurrent requests per model
export OLLAMA_MAX_LOADED_MODELS=2      # 2 models in memory max
export OLLAMA_KEEP_ALIVE="5m"          # Keep models for 5 min after use
export OLLAMA_MAX_QUEUE=10             # Queue up to 10 requests
```


### Model Strategy

**Primary workflow model:** Qwen2.5-Coder 8B Q4_K_M (excellent coding performance, 6GB)[^11]
**Quick tasks:** Gemma 2 3B Q4 (fast, lightweight, 4GB)
**Reasoning/planning:** DeepSeek-R1 7B or Qwen2.5 14B (when you need deeper analysis)

### KiloCode Mode Configuration

Set up "sticky models" for each mode:[^21]

- **Orchestrator:** DeepSeek-R1 7B (reasoning)
- **Architect:** Qwen2.5-Coder 8B (planning)
- **Code:** Qwen2.5-Coder 8B (implementation)
- **Debug:** Qwen2.5-Coder 8B (fixing)
- **Ask:** Gemma 2 3B (quick queries)


## Practical Workflow Recommendations

### Parallel Development Pattern

Use KiloCode CLI's parallel mode for independent features:[^4][^3]

```bash
# Terminal 1: Feature A
kilocode --parallel --auto "Build user authentication"

# Terminal 2: Feature B  
kilocode --parallel --auto "Create dashboard UI"

# Terminal 3: Feature C
kilocode --parallel --auto "Set up email notifications"
```

Each runs in a separate git branch. With 3 agents sharing one 8B model, this works smoothly within 24GB.[^20][^22]

### Memory Bank Strategy

Use KiloCode's Memory Bank feature to reduce context window consumption:[^23]

- Front-load project context once
- Reduce repetitive explanations
- Enable efficient multi-session continuity
- Save 30-50% of context tokens


### Docker Optimization

Since Docker can't accelerate Ollama, use it only for supporting services:[^24]

- **PostgreSQL:** 512 MB-1 GB
- **Redis:** 256-512 MB
- **Web services:** 512 MB-1 GB each

Limit Docker Desktop to **4-6 GB total** in Settings > Resources.[^25][^14]

## Performance Expectations

Based on benchmarks for M4 with 24GB:[^10][^11]


| Configuration | Response Time | Throughput | User Experience |
| :-- | :-- | :-- | :-- |
| 1x 7B model, 3 sessions | 1.2s first token | 77 tokens/s | Excellent |
| 1x 8B model, 2 sessions | 1.5-2s first token | 40-50 tokens/s | Very Good |
| 1x 14B model, 1 session | 3-5s first token | 15-20 tokens/s | Adequate |
| 2x 7B models, 2 sessions | 2-3s first token | 30-40 tokens/s | Good |
| 1x 32B model | 13-15s first token | 9-10 tokens/s | Slow but usable[^11] |

## System Monitoring

Monitor resource usage to optimize your configuration:

```bash
# Check Ollama memory usage
ollama ps

# Monitor system memory
vm_stat | grep "Pages free"

# Check Docker memory  
docker stats

# Activity Monitor
# View "Real Memory" column (right-click header to enable)[^57]
```


## Limitations and Trade-offs

**Maximum realistic concurrent instances:** **3-4 KiloCode CLI agents** using shared models[^26][^16]

**Key constraints:**

1. **Context size impact:** Larger context windows multiply memory requirements[^27][^28]
2. **Model swapping latency:** Loading/unloading models takes 2-5 seconds[^19]
3. **System stability:** Leave 4-6 GB free for macOS to prevent swapping[^9]
4. **Docker conflict:** Running Ollama in Docker loses GPU acceleration entirely[^15]

## Advanced Optimization: Headless Mode

For maximum efficiency, consider running your M4 in optimized server mode:[^24]

- Disable unnecessary services
- Reduce system memory from 11GB → 3GB baseline
- Configure Ollama autostart
- Use SSH for remote access
- Run Docker via Colima for container autostart

This can free up **8GB additional RAM** for models.

## Conclusion: Your Practical Limits

**Conservative (Reliable):**

- **2-3 concurrent KiloCode instances**
- 1-2 models loaded (7-8B)
- Full Docker stack running
- Smooth, responsive experience

**Optimal (Recommended):**

- **3-4 concurrent KiloCode instances**
- 1 primary model (8B) + 1 lightweight (3B)
- Selective Docker services
- Excellent balance of capability and performance

**Aggressive (Maximum):**

- **4-5 concurrent KiloCode sessions**
- 2 models loaded (2x 7B or 1x 8B + 1x 3B)
- Minimal Docker overhead
- May experience occasional slowdowns

Your 24GB M4 is well-suited for parallel AI development work. The unified memory architecture gives you an advantage over discrete GPU setups for multi-model scenarios. The key is running Ollama natively (not in Docker) and choosing appropriately sized models for your workflow.

For your SMB AI automation agency work, I'd recommend the **Optimal configuration** with 3 concurrent agents using Qwen2.5-Coder 8B—this provides excellent coding quality while maintaining responsive performance for iterative development.[^29][^30][^5]
<span style="display:none">[^31][^32][^33][^34][^35][^36][^37][^38][^39][^40][^41][^42][^43][^44][^45][^46][^47][^48][^49][^50][^51][^52][^53][^54][^55][^56][^58][^59][^60][^61][^62][^63][^64][^65][^66][^67][^68][^69]</span>

<div align="center">⁂</div>

[^1]: https://www.npmjs.com/package/@kilocode/cli

[^2]: https://www.youtube.com/watch?v=5kQivY2oBg8

[^3]: https://www.youtube.com/watch?v=z1xzOAQ-MME

[^4]: https://www.youtube.com/watch?v=WYjxN8QUJi8

[^5]: https://johnwlittle.com/ollama-on-mac-silicon-local-ai-for-m-series-macs/

[^6]: https://discussions.apple.com/thread/255888747

[^7]: https://localllm.in/blog/ollama-vram-requirements-for-local-llms

[^8]: https://github.com/ollama/ollama

[^9]: https://localaimaster.com/blog/mac-local-ai-setup

[^10]: https://malcolmlow.net/2025/11/13/mac-studio-vs-mac-mini-m4-local-ai-performance-benchmarks/

[^11]: https://www.youtube.com/watch?v=RrXLXNr0BFM

[^12]: https://github.com/docker/for-mac/issues/7111

[^13]: https://github.com/docker/for-mac/issues/6120

[^14]: https://www.reddit.com/r/docker/comments/1lea1rh/mac_docker_using_a_lot_of_memory/

[^15]: https://chariotsolutions.com/blog/post/apple-silicon-gpus-docker-and-ollama-pick-two/

[^16]: https://www.reddit.com/r/LocalLLaMA/comments/1go86pm/does_ollama_work_as_a_server_to_server_multiple/

[^17]: https://docs.ollama.com/faq

[^18]: https://www.reddit.com/r/kilocode/comments/1nz0qk1/which_model_do_you_use_for_each_mode_architect/

[^19]: https://github.com/ollama/ollama/issues/4855

[^20]: https://www.youtube.com/watch?v=HmDliV9KMxA

[^21]: https://kilo.ai/docs/agent-behavior/custom-modes

[^22]: https://zsiegel.com/training-myself-to-work-with-ai-in-parallel/

[^23]: https://kilo.ai/docs/advanced-usage/memory-bank

[^24]: https://www.reddit.com/r/ollama/comments/1j0cwah/mac_studio_server_guide_run_ollama_with_optimized/

[^25]: https://stackoverflow.com/questions/44533319/how-to-assign-more-memory-to-docker-container

[^26]: https://www.youtube.com/watch?v=8r_8CZqt5yk

[^27]: https://localaimaster.com/blog/run-llama3-on-mac

[^28]: https://www.reddit.com/r/ollama/comments/1lmjbxj/can_i_combine_2x_m4_pro_macbooks_for_llms_and/

[^29]: https://news.ycombinator.com/item?id=43918581

[^30]: https://kilo.ai/docs/providers/ollama

[^31]: https://www.reddit.com/r/mac/comments/1pvhdzf/macbook_air_m4_for_coding/

[^32]: https://maaz.ihmc.us/rid=1VT6HWC2S-1L5FJ61-JM/2016 - Health informatics meets ehealth Predictive model.pdf

[^33]: https://archive.org/stream/PersonalComputerWorld1981-01/1981-01_djvu.txt

[^34]: https://archive.org/stream/Personal_Computer_World_2008-07_VNU_Business_Publications_GB/Personal_Computer_World_2008-07_VNU_Business_Publications_GB_djvu.txt

[^35]: https://archive.org/stream/PersonalComputerWorldMagazine/PCW 200507 July_djvu.txt

[^36]: https://github.com/Kilo-Org/kilocode/issues/1854

[^37]: https://docs.docker.com/engine/containers/resource_constraints/

[^38]: https://macstadium.com/blog/m4-mac-mini-review

[^39]: https://archive.org/stream/TheDailyTelegraph1971UKEnglish/Jun 25 1971, The Daily Telegraph, %2336120, UK (en)_djvu.txt

[^40]: https://www.reddit.com/r/kilocode/comments/1liatwo/new_on_kilo_code/

[^41]: https://archive.org/stream/PersonalComputerWorldMagazine/PCW 200101 January Created From PCW Cover CD (No Cover)_djvu.txt

[^42]: https://www.youtube.com/watch?v=EjheIfFD7Dc

[^43]: https://blog.ovhcloud.com/use-kilo-code-with-ai-endpoints-and-vscode/

[^44]: https://www.youtube.com/watch?v=T9PnGcLromA\&vl=en

[^45]: https://docs.megallm.io/en/agents/kilocode

[^46]: https://www.youtube.com/watch?v=_UbmP08SxsY

[^47]: https://www.reddit.com/r/kilocode/comments/1nt5rmt/maintaining_memory_across_different_coding_agents/

[^48]: https://github.com/ollama/ollama/issues/6008

[^49]: https://www.databasemart.com/blog/choosing-the-right-gpu-for-popluar-llms-on-ollama

[^50]: https://blog.kilocode.ai/p/how-kilo-codes-orchestrator-mode

[^51]: https://kilo.ai/docs/basic-usage/orchestrator-mode

[^52]: https://www.youtube.com/watch?v=20MmJNeOODo

[^53]: https://apidog.com/blog/kilo-code/

[^54]: https://skywork.ai/blog/kilo-code-ai-review-2025-vs-code-jetbrains/

[^55]: https://github.com/hiyouga/LlamaFactory

[^56]: https://www.datastudios.org/post/kilo-code-the-open-source-agent-that-s-redefining-ai-coding-assistants

[^57]: https://www.linkedin.com/pulse/beyond-threads-rethinking-ai-hardware-unified-memory-neural-shafik-ti96c

[^58]: https://www.reddit.com/r/kilocode/comments/1n0xqmx/gave_kilo_code_an_actual_memory_with_mcp/

[^59]: https://stencel.io/posts/buying-gpu-for-local-models-llm.html

[^60]: https://support.apple.com/en-gb/121553

[^61]: https://stackoverflow.com/questions/58308169/docker-for-mac-memory-usage-in-com-docker-hyperkit

[^62]: https://www.reddit.com/r/docker/comments/14adajy/running_multiple_docker_containers_on_macbook_pro/

[^63]: https://creativecodingtech.com/ai-agents/automation/devops/2026/01/13/day-1-building-autonomous-coding-agent.html

[^64]: https://tech-now.io/en/blogs/kilo-code-the-new-open-source-ai-coding-agent-for-vs-code

[^65]: https://github.com/Kilo-Org/kilocode/discussions/2337

[^66]: https://arxiv.org/pdf/2504.19413.pdf

[^67]: https://kilo.ai/docs/basic-usage/model-selection-guide

[^68]: https://xxchan.me/blog/2025-11-14-concurrent-local-coding-agents/index_en/

[^69]: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

