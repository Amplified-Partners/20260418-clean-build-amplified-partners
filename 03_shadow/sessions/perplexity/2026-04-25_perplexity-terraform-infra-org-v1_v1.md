---
title: "I've completed the infrastructure organization with the following files:"
id: "perplexity-terraform-infra-org-v1"
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

# I've completed the infrastructure organization with the following files:

1. providers.tf - Contains AWS provider configuration and required
   providers
       2. locals.tf - Contains common tags and resource naming conventions
       3. variables.tf - Consolidated input variables for all resources
       4. outputs.tf - Consolidated outputs for network, security groups, and
   IAM roles
       5. main.tf - Simplified to only contain backend configuration
       6. iam.tf - Contains Lambda IAM role and policy
       7. network.tf - Contains existing VPC and networking components

The infrastructure is now better organized with clear separation of concerns
    and consistent naming conventions. Each file has a specific purpose, making
    the codebase more maintainable and easier to understand.

╭─────────────────────────────────

This is a solid intermediate state: the **file organisation is now good**, but the **actual resources still need to match your spec**.

Right now you have:

- `providers.tf` – AWS provider (check region = `eu-west-2`).
- `locals.tf` – tags/naming (good).
- `variables.tf` – inputs (good).
- `outputs.tf` – outputs (good).
- `main.tf` – backend only.
- `iam.tf` – Lambda IAM role.
- `network.tf` – VPC + networking.[^1][^2]

What to do next:

1. **Verify critical pieces:**
    - In Terminal, from `infra/terraform`:

```bash
cat providers.tf
cat network.tf
```

    - Check:
        - Provider region is `eu-west-2`.
        - AZs in `network.tf` are `eu-west-2a`, `eu-west-2b` (no `us-east-1`).[^3][^1]
2. **Ask Claude (in Kilo) explicitly for the missing resources:**

Send this:

> Infra structure looks good now.
> Please add two new files:
> 1. `rds.tf` – PostgreSQL 16 `db.t4g.small` RDS instance in the private subnets from `network.tf`, not publicly accessible, DB name/user/password as variables.
> 2. `lambda_api.tf` – a simple Python hello‑world Lambda with an HTTP API Gateway exposing `/health`.
> Make sure everything is in region `eu-west-2` and uses the locals/variables you already defined.
3. **Then run Terraform (after review):**

```bash
cd infra/terraform
terraform init
terraform plan
```

Review the plan carefully before `terraform apply`.[^1][^3]

So: organisation = right direction; now you just need `rds.tf` + `lambda_api.tf` added on top of this clean structure.
<span style="display:none">[^4][^5]</span>

<div align="center">⁂</div>

[^1]: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-manage

[^2]: https://spacelift.io/blog/terraform-infrastructure-as-code

[^3]: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-create

[^4]: Screenshot-2026-01-18-at-04.48.49.jpg

[^5]: Screenshot-2026-01-18-at-05.03.54.jpg

