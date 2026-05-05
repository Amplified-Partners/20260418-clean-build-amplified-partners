---
title: "Variables and Outputs Documentation"
id: "variables-outputs"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Variables and Outputs Documentation

## Variables

### Project Variables (`main.tf`)

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| `project_name` | string | Name of the project | "static-web-app" |
| `environment` | string | Environment (e.g., prod, dev, staging) | "prod" |

## Outputs

### Network Outputs (`network.tf`)

| Output | Description | Source |
|--------|-------------|--------|
| `vpc_id` | ID of the created VPC | `module.vpc.vpc_id` |
| `public_subnet_ids` | List of public subnet IDs | `module.vpc.public_subnets` |
| `private_subnet_ids` | List of private subnet IDs | `module.vpc.private_subnets` |

### Static Hosting Outputs (`static-hosting.tf`)

| Output | Description | Source |
|--------|-------------|--------|
| `website_bucket_name` | Name of the S3 bucket hosting the website | `aws_s3_bucket.website.id` |
| `cloudfront_distribution_id` | ID of the CloudFront distribution | `aws_cloudfront_distribution.website.id` |
| `cloudfront_domain_name` | Domain name of the CloudFront distribution | `aws_cloudfront_distribution.website.domain_name` |

## Local Variables

### Common Tags (`main.tf`)

```hcl
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

These tags are applied to all resources created by this Terraform configuration.