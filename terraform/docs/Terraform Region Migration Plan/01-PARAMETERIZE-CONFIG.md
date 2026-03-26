# Phase 1: Parameterize the Terraform Configuration

## Objective

Replace all hardcoded region references, account IDs, and ARNs with Terraform variables and module references. After this phase, the entire config is region-agnostic — you can deploy to any region by changing a single variable.

## Risk Level: ZERO

This phase makes no infrastructure changes. You are only refactoring HCL code. The values resolve to the exact same strings as before.

## Estimated Time: 2-3 hours

---

## Step 1: Create variables.tf

Create `terraform/environments/prod/variables.tf`:

```hcl
variable "aws_region" {
  description = "AWS region to deploy all resources"
  type        = string
  default     = "us-east-1"
}

variable "account_id" {
  description = "AWS account ID"
  type        = string
  default     = "371751795928"
}

variable "environment" {
  description = "Environment name (prod, staging, dev)"
  type        = string
  default     = "prod"
}

variable "project_name" {
  description = "Project name used in tags and resource naming"
  type        = string
  default     = "ChristianConservativePlatform"
}

variable "aws_profile" {
  description = "AWS CLI profile to use"
  type        = string
  default     = "ekewaka"
}
```

### Why These Variables?

- `aws_region` — Used in provider block, module calls, and anywhere `us-east-1` appears
- `account_id` — Used in all IAM role ARNs (48 Lambda functions reference this)
- `environment` — Used in tags and stage names
- `project_name` — Used in default tags
- `aws_profile` — Used in provider block (backend block cannot use variables)

---

## Step 2: Update Provider Block

### Before:
```hcl
provider "aws" {
  region  = "us-east-1"
  profile = "ekewaka"

  default_tags {
    tags = {
      Environment = "production"
      ManagedBy   = "Terraform"
      Project     = "ChristianConservativePlatform"
    }
  }
}
```

### After:
```hcl
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
```

### Backend Block — CANNOT Use Variables

```hcl
# NOTE: Terraform backend blocks do not support variables.
# The region here must stay hardcoded OR be overridden via CLI:
#   terraform init -backend-config="region=us-west-2"
backend "s3" {
  bucket       = "techcross-terraform-state"
  key          = "prod/terraform.tfstate"
  region       = "us-east-1"          # Keep as-is — state stays in us-east-1
  encrypt      = true
  use_lockfile = true
  profile      = "ekewaka"
}
```

**Important:** The state backend does NOT need to be in the same region as your resources. It's fine to keep state in `us-east-1` even if resources move to `us-west-2`. This is actually recommended — single source of truth.

---

## Step 3: Add Data Source for Account ID

Instead of hardcoding `371751795928` everywhere, use a data source. Add to main.tf near the top:

```hcl
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
```

Now you can reference:
- `data.aws_caller_identity.current.account_id` → `"371751795928"`
- `data.aws_region.current.name` → `"us-east-1"`

---

## Step 4: Replace Hardcoded Role ARNs in Lambda Modules

This is the biggest change — 48 Lambda function modules have hardcoded role ARNs.

### Before (repeated 40+ times):
```hcl
role_arn = "arn:aws:iam::371751795928:role/lambda-execution-role"
```

### After:
```hcl
role_arn = module.lambda_execution_role.role_arn
```

### For functions using other roles:

| Role | Functions | New Reference |
|------|-----------|---------------|
| `lambda-execution-role` | 40+ functions | `module.lambda_execution_role.role_arn` |
| `testimony-lambda-role` | testimony-auth, testimony-crud, testimony-admin, testimony-email-sharing, testimony-email-ses, feature-flags-api | Need to import this role into Terraform first (see below) |
| `tracking-api-role` | tracking-api | Need to import this role into Terraform first |
| `NewsScraperLambdaRole` | NewsScraperLambda | Need to import this role into Terraform first |
| `service-role/email-subscription-handler-role-s3uqsrwg` | email-subscription-handler | Need to import this role into Terraform first |

### Importing Additional IAM Roles

For the roles not yet in Terraform, you have two options:

**Option A: Import them as Terraform resources** (recommended for migration)
```hcl
module "testimony_lambda_role" {
  source    = "../../modules/iam-role"
  role_name = "testimony-lambda-role"
  # ... (get config from AWS)
}
```
Then: `terraform import "module.testimony_lambda_role.aws_iam_role.this" "testimony-lambda-role"`

**Option B: Use data sources** (simpler, read-only)
```hcl
data "aws_iam_role" "testimony_lambda" {
  name = "testimony-lambda-role"
}
```
Then reference: `data.aws_iam_role.testimony_lambda.arn`

**For migration, Option A is better** because Terraform will recreate the roles in the new region. With Option B, the roles would need to exist already.

Note: IAM is a global service — roles exist across all regions. But managing them in Terraform ensures they're created as part of the deployment.

### Verification

After replacing all role ARNs, run:
```powershell
Select-String -Path main.tf -Pattern "371751795928"
```
The only remaining matches should be in the `backend` block (which can't use variables).

---

## Step 5: Replace Hardcoded Lambda Layer ARNs

### Before:
```hcl
# In lambda_url_analysis_api:
layers = ["arn:aws:lambda:us-east-1:371751795928:layer:requests-layer:1"]

# In lambda_video_downloader:
layers = [
  "arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer-v2:1",
  "arn:aws:lambda:us-east-1:371751795928:layer:ffmpeg-layer:1"
]

# In lambda_thumbnail_generator:
layers = ["arn:aws:lambda:us-east-1:371751795928:layer:ffmpeg-layer:1"]
```

### After:
```hcl
# In lambda_url_analysis_api:
layers = [module.layer_requests.layer_arn]

# In lambda_video_downloader:
layers = [
  module.layer_yt_dlp.layer_arn,
  module.layer_ffmpeg.layer_arn
]

# In lambda_thumbnail_generator:
layers = [module.layer_ffmpeg.layer_arn]
```

### Required: Add output to lambda-layer module

Check if `terraform/modules/lambda-layer/main.tf` exports `layer_arn`. If not, add:

```hcl
output "layer_arn" {
  value       = aws_lambda_layer_version.this.arn
  description = "ARN of the Lambda layer version"
}
```

### Functions Using Layers

| Function | Layers |
|----------|--------|
| `url-analysis-api` | requests-layer |
| `video-downloader` | yt-dlp-layer-v2, ffmpeg-layer |
| `thumbnail-generator` | ffmpeg-layer |
| `s3-thumbnail-trigger` | (none currently) |

---

## Step 6: Replace Hardcoded Region in CloudFront OAC

### Before:
```hcl
module "cloudfront_oac" {
  source = "../../modules/cloudfront-oac"
  name   = "my-video-downloads-bucket.s3.us-east-1.amazonaws.com"
  ...
}
```

### After:
```hcl
module "cloudfront_oac" {
  source = "../../modules/cloudfront-oac"
  name   = "my-video-downloads-bucket.s3.${var.aws_region}.amazonaws.com"
  ...
}
```

---

## Step 7: Replace Hardcoded Region in CloudWatch Dashboard

### Before:
```hcl
module "platform_dashboard" {
  ...
  region     = "us-east-1"
  account_id = "371751795928"
  ...
}
```

### After:
```hcl
module "platform_dashboard" {
  ...
  region     = var.aws_region
  account_id = data.aws_caller_identity.current.account_id
  ...
}
```

---

## Step 8: Replace Hardcoded ACM Certificate ARN

### Before:
```hcl
module "cloudfront_distribution" {
  ...
  acm_certificate_arn = "arn:aws:acm:us-east-1:371751795928:certificate/d29ff60a-9c7e-4b6a-920b-e9b6db5202b4"
  ...
}
```

### After:
This one is special — CloudFront requires ACM certs in `us-east-1`. This will be handled in Phase 2 with a separate provider. For now, leave it hardcoded with a comment:

```hcl
module "cloudfront_distribution" {
  ...
  # TODO: Phase 2 — Replace with module reference using us-east-1 provider
  # CloudFront requires ACM certificates to be in us-east-1 regardless of resource region
  acm_certificate_arn = "arn:aws:acm:us-east-1:371751795928:certificate/d29ff60a-9c7e-4b6a-920b-e9b6db5202b4"
  ...
}
```

---

## Step 9: Update Module Default Values

### api-gateway-lambda-integration module

File: `terraform/modules/api-gateway-lambda-integration/main.tf`

**Before:**
```hcl
variable "region" {
  type    = string
  default = "us-east-1"
}
```

**After:**
```hcl
variable "region" {
  type        = string
  description = "AWS region for Lambda integration URI"
  # No default — must be passed explicitly
}
```

Then in every `module "api_*"` block in main.tf, add:
```hcl
module "api_articles" {
  source = "../../modules/api-gateway-lambda-integration"
  region = var.aws_region    # ADD THIS LINE
  ...
}
```

This affects all 17 API Gateway integration modules.

### cloudfront module

File: `terraform/modules/cloudfront/main.tf`

**Before:**
```hcl
origin_id = "${var.bucket_name}.s3.us-east-1.amazonaws.com-mgidi2pjodn"
```

**After — add a region variable:**
```hcl
variable "aws_region" {
  type        = string
  description = "AWS region for S3 origin"
}
```

```hcl
origin_id = "${var.bucket_name}.s3.${var.aws_region}.amazonaws.com-mgidi2pjodn"
```

And update both references (origin block and default_cache_behavior target_origin_id).

Then in main.tf:
```hcl
module "cloudfront_distribution" {
  source     = "../../modules/cloudfront"
  aws_region = var.aws_region    # ADD THIS LINE
  ...
}
```

### cloudwatch-dashboard module

File: `terraform/modules/cloudwatch-dashboard/variables.tf`

**Before:**
```hcl
variable "region" {
  default = "us-east-1"
}
```

**After:**
```hcl
variable "region" {
  type        = string
  description = "AWS region for dashboard metrics"
  # No default — must be passed explicitly
}
```

Already passed from main.tf, so no change needed there.

---

## Step 10: Validate

### 10a. Check for remaining hardcoded values

```powershell
# Should return ONLY the backend block line
Select-String -Path main.tf -Pattern "us-east-1"

# Should return ZERO matches
Select-String -Path main.tf -Pattern "371751795928"

# Check modules too
Get-ChildItem -Recurse ..\..\modules -Filter *.tf | Select-String -Pattern "us-east-1"
```

### 10b. Terraform validate

```bash
terraform validate
```

Must pass with no errors.

### 10c. Terraform plan — THE CRITICAL TEST

```bash
terraform plan
```

**Expected result: 0 to add, 0 to change, 0 to destroy.**

If you see ANY changes, something was refactored incorrectly. The variable values are identical to the hardcoded values they replaced, so the plan must be empty.

Common issues:
- Trailing whitespace differences in ARN strings
- Missing `region` parameter on a module call
- Layer ARN version number mismatch (module output includes version, hardcoded string had `:1`)

### 10d. Functional test

After applying (even though plan shows 0 changes), verify:
- Hit `https://api.christianconservativestoday.com/articles` — should return articles
- Hit `https://api.christianconservativestoday.com/auth` — should respond
- Check CloudFront is still serving `https://christianconservativestoday.com`
- Send a test email through the subscription flow

---

## Checklist

- [ ] `variables.tf` created with `aws_region`, `account_id`, `environment`, `project_name`, `aws_profile`
- [ ] `data "aws_caller_identity"` and `data "aws_region"` added
- [ ] Provider block uses `var.aws_region` and `var.aws_profile`
- [ ] All 48 Lambda `role_arn` fields use module references or data sources
- [ ] All Lambda layer ARNs use module output references
- [ ] CloudFront OAC name uses `var.aws_region`
- [ ] CloudWatch dashboard uses `var.aws_region` and data source for account_id
- [ ] API Gateway integration module has no default region
- [ ] All 17 `module "api_*"` blocks pass `region = var.aws_region`
- [ ] CloudFront module parameterized for region
- [ ] `terraform validate` passes
- [ ] `terraform plan` shows 0 changes
- [ ] All API endpoints still functional
- [ ] Git commit: "Phase 1: Parameterize Terraform config for region portability"
