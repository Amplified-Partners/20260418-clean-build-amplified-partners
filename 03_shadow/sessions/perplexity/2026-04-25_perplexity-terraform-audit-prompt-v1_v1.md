---
title: "can you right the perfect prompt to audit what we have should have terraform now. and once you see that audit we will know where to go"
id: "perplexity-terraform-audit-prompt-v1"
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

# can you right the perfect prompt to audit what we have should have terraform now. and once you see that audit we will know where to go

To audit what you have now, you want Claude to:

- Look only at the actual `.tf` files.
- Summarise structure and resources.
- Compare against the target spec.
- Propose minimal, concrete fixes.

Here’s a prompt you can paste directly into Claude (in Kilo) as a **one-shot “audit” prompt**.

***

### Terraform audit prompt

> You are my Terraform infrastructure auditor.
> Your ONLY job in this conversation is to:
> 1) Inspect the current Terraform files under `infra/terraform/`,
> 2) Summarise what they actually do, and
> 3) Compare that against a target spec I will give you, then
> 4) Tell me exactly what is missing or misconfigured and how to fix it.
>
> You must not invent resources that are not really in the files; base your conclusions ONLY on the code I paste in.
>
> ---
>
> \#\# Target spec (what the Terraform SHOULD represent)
>
> For my `VoiceAI_SMB_Platform` project, the Terraform should model:
>
> 1. **Provider**
>    - AWS provider pinned to region `eu-west-2` (London).
>
> 2. **Networking**
>    - VPC with CIDR `10.0.0.0/16`.
>    - At least:
>      - 2 public subnets (e.g. `10.0.1.0/24`, `10.0.2.0/24`).
>      - 2 private subnets (e.g. `10.0.101.0/24`, `10.0.102.0/24`).
>    - Availability zones must be in `eu-west-2` only (e.g. `eu-west-2a`, `eu-west-2b`).
>    - NAT gateway so private subnets can reach the internet.
>    - Security groups:
>      - One suitable for web/Lambda traffic.
>      - One for RDS allowing ingress only from app/Lambda SG, no public DB access.
>
> 3. **RDS PostgreSQL**
>    - PostgreSQL 16 RDS instance.
>    - Dev size: `db.t4g.small`, GP3 50–100 GB.
>    - In private subnets from the VPC.
>    - NOT publicly accessible.
>    - DB name, username, password provided as variables (no hard‑coded credentials).
>
> 4. **Lambda + HTTP API**
>    - A simple Lambda function (Python is fine) that can serve as a health check.
>    - HTTP API Gateway exposing at least a `/health` endpoint mapped to that Lambda.
>
> 5. **Variables / outputs / locals**
>    - Centralised `variables` and `locals` for:
>      - `project_name`, `env`, region (default `eu-west-2`).
>      - DB credentials.
>      - Common tags.
>    - Outputs for:
>      - VPC ID.
>      - Public and private subnet IDs.
>      - RDS endpoint.
>      - API Gateway URL.
>
> 6. **Non‑goals for now**
>    - No S3/CloudFront static website unless it’s clearly marked as optional.
>    - No other AWS regions (no `us-east-1` anywhere).
>
> ---
>
> \#\# How to perform the audit
>
> 1. Ask me to paste the **contents of all Terraform files** under `infra/terraform/`:
>    - `providers.tf`
>    - `locals.tf`
>    - `variables.tf`
>    - `outputs.tf`
>    - `main.tf`
>    - `network.tf`
>    - `iam.tf`
>    - Any others that exist (e.g. `rds.tf`, `lambda_api.tf`, etc.).
>
> 2. For each pasted file, read it carefully and build an internal picture of:
>    - Which resources exist.
>    - Which region/AZs they use.
>    - How they are wired together.
>
> 3. Then produce a **structured audit report** with these sections:
>
>    **A. Current files and purpose**
>    - Briefly list each `.tf` file and what it defines in practice.
>
>    **B. Requirements coverage**
>    - For each target spec item 1–5 above, say:
>      - ✅ Fully met
>      - ⚠️ Partially met
>      - ❌ Missing
>    - Include short evidence (e.g. “provider region is eu-west-2”, or “no RDS resource present”).
>
>    **C. Problems / drift**
>    - Explicitly list:
>      - Any use of non‑`eu-west-2` regions or AZs.
>      - Any public RDS or missing security.
>      - Any extra stacks (e.g. S3/CloudFront) that are not in the target spec.
>
>    **D. Concrete change plan**
>    - For each gap, propose **specific edits or new files**, for example:
>      - “Create `rds.tf` with an `aws_db_instance` …”
>      - “In `network.tf`, change AZs from `us-east-1a/b` to `eu-west-2a/b`.”
>      - “Remove or comment out S3/CloudFront resources in `static-hosting.tf`.”
>    - Refer to filenames and resource names explicitly so I can implement changes easily.
>
> 4. Do NOT output full new Terraform files yet; just the structured audit and a precise change plan. We will generate or edit files in a follow‑up step.
>
> Start by asking me to paste the contents of all `.tf` files under `infra/terraform/`, and then wait for my paste before you begin the audit.
<span style="display:none">[^1][^2]</span>

<div align="center">⁂</div>

[^1]: Screenshot-2026-01-18-at-04.48.49.jpg

[^2]: Screenshot-2026-01-18-at-05.03.54.jpg

