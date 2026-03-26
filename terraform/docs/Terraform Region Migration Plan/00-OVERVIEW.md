# Terraform Region Migration Plan — Overview

## Purpose

This guide provides a complete, step-by-step implementation plan for migrating the Christian Conservative Platform infrastructure from `us-east-1` to any other AWS region using Terraform.

## Current State

- **AWS Account:** 371751795928 (profile: `ekewaka`)
- **Current Region:** `us-east-1`
- **Terraform Version:** 1.14.6
- **AWS Provider:** ~> 5.0
- **State Backend:** S3 (`techcross-terraform-state/prod/terraform.tfstate`)

### Managed Resources (as of latest audit)

| Resource Type | Count | Notes |
|---------------|-------|-------|
| Lambda Functions | 48 | Code managed externally (lifecycle ignore) |
| DynamoDB Tables | 54+ | Mix of PAY_PER_REQUEST and PROVISIONED |
| API Gateway | 1 unified (`diz6ceeb22`) | 17+ route integrations |
| SQS Queues | 5 main + 5 DLQs | Video processing, email, analytics, etc. |
| SNS Topics | 4 | Alerts, notifications, SES events |
| S3 Buckets | 1 | `my-video-downloads-bucket` |
| CloudFront | 1 distribution | `E3N00R2D2NE9C5` |
| Lambda Layers | 3 | yt-dlp, ffmpeg, requests |
| IAM Roles | 4 | lambda-execution-role, testimony-lambda-role, etc. |
| ACM Certificates | 2 | api.christianconservativestoday.com, api-staging |
| Route53 Records | Multiple | Custom domain mappings |
| CloudWatch Dashboard | 1 | Platform monitoring |

### Known Hardcoded Values in Current Config

| What | Where | Count |
|------|-------|-------|
| `us-east-1` | main.tf provider, backend, CloudFront OAC, dashboard | 4 |
| `us-east-1` | Lambda layer ARNs | 4 |
| `us-east-1` | Modules (api-gateway-integration, cloudfront, cloudwatch) | 4 |
| `371751795928` | Lambda role_arn fields | 48 |
| `371751795928` | CloudWatch dashboard account_id | 1 |
| Hardcoded ACM ARN | CloudFront distribution | 1 |

## Phase Summary

| Phase | Document | Effort | Risk | Infra Changes |
|-------|----------|--------|------|---------------|
| 1 | [01-PARAMETERIZE-CONFIG.md](01-PARAMETERIZE-CONFIG.md) | 2-3 hours | Zero | None |
| 2 | [02-CLOUDFRONT-ACM-PROVIDER.md](02-CLOUDFRONT-ACM-PROVIDER.md) | 30 min | Zero | None |
| 3 | [03-LAMBDA-CODE-DEPLOYMENT.md](03-LAMBDA-CODE-DEPLOYMENT.md) | 3-4 hours | Low | None |
| 4 | [04-DATA-MIGRATION-STRATEGY.md](04-DATA-MIGRATION-STRATEGY.md) | 2-3 hours | Medium | Adds replication |
| 5 | [05-SES-SETUP.md](05-SES-SETUP.md) | 1 hour + 48hr wait | Low | New region SES |
| 6 | [06-DRY-RUN-STAGING.md](06-DRY-RUN-STAGING.md) | 4-6 hours | Zero | Isolated test env |
| 7 | [07-PRODUCTION-CUTOVER.md](07-PRODUCTION-CUTOVER.md) | 2-4 hours | Medium | Full migration |

**Total estimated effort:** 2-3 days of work spread over ~1 week (accounting for SES production access approval).

## Prerequisites

Before starting any phase:

1. Terraform state backup exists:
   ```
   terraform state pull > backup-pre-migration.tfstate
   ```
2. Current `terraform plan` is clean (no unexpected changes)
3. Git working tree is clean — all current changes committed
4. AWS CLI configured with `ekewaka` profile
5. Target region decided (e.g., `us-west-2`)

## Architecture Diagram (Current)

```
                    Route53
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     CloudFront    API GW     API GW
     (static)    (prod)     (staging)
          │           │
          ▼           ▼
         S3      48 Lambdas
                      │
              ┌───────┼───────┐
              ▼       ▼       ▼
          DynamoDB   SQS     SES
          (54 tbl)  (5+5)   (email)
                      │
                      ▼
                     SNS
                   (alerts)
```

## Architecture Diagram (Post-Migration)

```
                    Route53
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     CloudFront    API GW     API GW
     (global)   (new region) (staging)
     │    │           │
     ▼    ▼           ▼
    S3   ACM*     48 Lambdas
  (new)  (us-east-1)  │
                ┌──────┼───────┐
                ▼      ▼       ▼
            DynamoDB  SQS     SES
            (new)   (new)   (new, verified)
                      │
                      ▼
                     SNS
                   (new)

* ACM cert for CloudFront MUST remain in us-east-1
```

## Key Decisions to Make Before Starting

1. **Target region** — Where are you migrating to? (e.g., `us-west-2`, `eu-west-1`)
2. **Migration strategy** — Big bang (maintenance window) or gradual (traffic shifting)?
3. **Data migration** — Global Tables (zero downtime) or export/import (cheaper, has downtime)?
4. **Lambda code management** — Keep external deployment or move to Terraform-managed zips?
5. **Rollback window** — How long to keep old region running after cutover? (Recommended: 48 hours)
