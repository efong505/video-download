# Phase 2: CloudFront ACM Certificate — Multi-Provider Setup

## Objective

CloudFront distributions require their ACM (SSL/TLS) certificates to be in `us-east-1`, regardless of where your other resources live. This phase sets up a secondary AWS provider pinned to `us-east-1` specifically for CloudFront's certificate, so the rest of your infrastructure can deploy to any region.

## Risk Level: ZERO

No infrastructure changes. This is a Terraform configuration refactor only.

## Estimated Time: 30 minutes

## Prerequisites

- Phase 1 complete (all hardcoded values parameterized)
- `terraform plan` shows 0 changes

---

## Background: Why CloudFront Needs us-east-1

CloudFront is a global service — it runs at AWS edge locations worldwide. AWS requires that any ACM certificate used with CloudFront be created in `us-east-1`. This is a hard requirement that cannot be changed.

When your resources are in `us-east-1`, this isn't an issue — everything is in the same region. But when you migrate to `us-west-2` (or any other region), you need:

- **Default provider** → `us-west-2` (for Lambdas, DynamoDB, API Gateway, etc.)
- **Secondary provider** → `us-east-1` (for CloudFront's ACM certificate only)

Terraform supports this via [provider aliases](https://developer.hashicorp.com/terraform/language/providers/configuration#alias-multiple-provider-configurations).

---

## Step 1: Add Secondary Provider

In `main.tf`, add a second provider block after the existing one:

```hcl
# Default provider — deploys to target region
provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = var.project_name
    }
  }
}

# Secondary provider — us-east-1 only, for CloudFront ACM certificates
provider "aws" {
  alias   = "us_east_1"
  region  = "us-east-1"
  profile = var.aws_profile

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "Terraform"
      Project     = var.project_name
    }
  }
}
```

### Key Points:
- The `alias = "us_east_1"` makes this a named provider
- Resources use the default provider unless explicitly told otherwise
- Only the CloudFront ACM certificate module will use this aliased provider

---

## Step 2: Create a CloudFront-Specific ACM Module (or Modify Existing)

You have two options:

### Option A: Pass provider to existing ACM module

Terraform modules can accept providers via the `providers` argument:

```hcl
# CloudFront ACM certificate — MUST be in us-east-1
module "acm_cloudfront" {
  source = "../../modules/acm-certificate"

  providers = {
    aws = aws.us_east_1    # Forces this module to use us-east-1
  }

  domain_name    = "christianconservativestoday.com"
  hosted_zone_id = data.aws_route53_zone.main.zone_id

  subject_alternative_names = [
    "*.christianconservativestoday.com"
  ]

  tags = {
    Purpose = "CloudFront SSL Certificate"
  }
}
```

Then reference it in CloudFront:
```hcl
module "cloudfront_distribution" {
  source = "../../modules/cloudfront"

  acm_certificate_arn = module.acm_cloudfront.certificate_arn
  ...
}
```

### Option B: Inline resource (simpler, no module changes)

```hcl
# CloudFront ACM certificate — MUST be in us-east-1
resource "aws_acm_certificate" "cloudfront" {
  provider          = aws.us_east_1
  domain_name       = "christianconservativestoday.com"
  validation_method = "DNS"

  subject_alternative_names = [
    "*.christianconservativestoday.com"
  ]

  lifecycle {
    create_before_destroy = true
  }

  tags = {
    Purpose = "CloudFront SSL Certificate"
  }
}

resource "aws_acm_certificate_validation" "cloudfront" {
  provider        = aws.us_east_1
  certificate_arn = aws_acm_certificate.cloudfront.arn
}
```

**Recommendation:** Option A is cleaner if your ACM module already supports the `providers` argument. Option B is simpler and avoids module changes.

---

## Step 3: Update CloudFront Distribution Reference

### Before (hardcoded ARN):
```hcl
module "cloudfront_distribution" {
  source = "../../modules/cloudfront"

  acm_certificate_arn = "arn:aws:acm:us-east-1:371751795928:certificate/d29ff60a-9c7e-4b6a-920b-e9b6db5202b4"
  ...
}
```

### After (module reference):
```hcl
module "cloudfront_distribution" {
  source = "../../modules/cloudfront"

  acm_certificate_arn = module.acm_cloudfront.certificate_arn
  ...
}
```

---

## Step 4: Handle the API Gateway ACM Certificates

Your existing API Gateway custom domain certificates are also ACM certs, but these are different from CloudFront:

- **API Gateway (Regional)** — ACM cert must be in the **same region** as the API Gateway
- **CloudFront (Global)** — ACM cert must be in `us-east-1`

Your current API certs (`acm_api_prod` and `acm_api_staging`) use the default provider, which is correct — they'll automatically be created in whatever region you deploy to.

```hcl
# These are fine — they use the default provider (target region)
module "acm_api_prod" {
  source         = "../../modules/acm-certificate"
  domain_name    = "api.christianconservativestoday.com"
  hosted_zone_id = data.aws_route53_zone.main.zone_id
}

module "acm_api_staging" {
  source         = "../../modules/acm-certificate"
  domain_name    = "api-staging.christianconservativestoday.com"
  hosted_zone_id = data.aws_route53_zone.main.zone_id
}
```

No changes needed for these.

---

## Step 5: Route53 Considerations

Route53 is a global service — it doesn't live in any specific region. The `data "aws_route53_zone"` and any Route53 records work the same regardless of which provider region you use.

However, when you migrate regions, the API Gateway custom domain will have a **new regional endpoint**. Terraform handles this automatically — the Route53 ALIAS record points to the API Gateway domain name output, which changes when the API Gateway is in a new region.

No manual changes needed, but be aware that DNS propagation takes time (typically 60 seconds with low TTL, up to 48 hours in worst case).

---

## Step 6: Import Existing CloudFront Certificate

If you go with Option A or B above, you need to import the existing certificate so Terraform doesn't try to create a new one:

```bash
# Find the existing certificate ARN
aws acm list-certificates --profile ekewaka --region us-east-1 \
  --query "CertificateSummaryList[?DomainName=='christianconservativestoday.com'].CertificateArn" \
  --output text

# Import it (adjust resource address based on Option A vs B)
# Option A:
terraform import "module.acm_cloudfront.aws_acm_certificate.this" "arn:aws:acm:us-east-1:371751795928:certificate/d29ff60a-..."

# Option B:
terraform import "aws_acm_certificate.cloudfront" "arn:aws:acm:us-east-1:371751795928:certificate/d29ff60a-..."
```

---

## Step 7: Validate

### 7a. Terraform plan

```bash
terraform plan
```

**Expected: 0 to add, 0 to change, 0 to destroy.**

The certificate ARN resolves to the same value as the hardcoded string it replaced.

### 7b. Verify provider configuration

```bash
terraform providers
```

Should show two AWS providers:
```
├── provider[registry.terraform.io/hashicorp/aws]
├── provider[registry.terraform.io/hashicorp/aws].us_east_1
```

### 7c. Functional test

- Verify `https://christianconservativestoday.com` loads (CloudFront + cert working)
- Verify `https://api.christianconservativestoday.com/articles` responds (API Gateway + cert working)

---

## What This Enables

After this phase, your Terraform config supports:

```hcl
# Deploy everything to us-west-2
variable "aws_region" {
  default = "us-west-2"
}
```

Terraform will:
- Create all Lambdas, DynamoDB, API Gateway, SQS, SNS in `us-west-2`
- Keep the CloudFront ACM certificate in `us-east-1` (via aliased provider)
- Create new API Gateway ACM certificates in `us-west-2`
- Update Route53 to point to the new regional endpoints

---

## Checklist

- [ ] Secondary provider `aws.us_east_1` added with alias
- [ ] CloudFront ACM certificate uses `aws.us_east_1` provider
- [ ] CloudFront distribution references module output (not hardcoded ARN)
- [ ] API Gateway ACM certs still use default provider (no changes needed)
- [ ] Existing certificate imported into state
- [ ] `terraform plan` shows 0 changes
- [ ] CloudFront site loads with valid SSL
- [ ] API Gateway endpoints respond with valid SSL
- [ ] Git commit: "Phase 2: Multi-provider setup for CloudFront ACM certificate"
