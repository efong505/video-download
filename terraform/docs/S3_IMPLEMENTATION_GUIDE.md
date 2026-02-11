# S3 Module - Detailed Implementation Guide

## Overview
Step-by-step guide for creating the S3 module and importing the existing `my-video-downloads-bucket` into Terraform.

---

## Step 1: Gather Existing S3 Bucket Information

### Commands to Inspect Current Bucket

```bash
# List all S3 buckets
aws s3 ls

# Get bucket location
aws s3api get-bucket-location --bucket my-video-downloads-bucket

# Get bucket versioning status
aws s3api get-bucket-versioning --bucket my-video-downloads-bucket

# Get bucket encryption
aws s3api get-bucket-encryption --bucket my-video-downloads-bucket

# Get bucket CORS configuration
aws s3api get-bucket-cors --bucket my-video-downloads-bucket

# Get bucket policy
aws s3api get-bucket-policy --bucket my-video-downloads-bucket

# Get bucket ACL
aws s3api get-bucket-acl --bucket my-video-downloads-bucket
```

### Data Collected

**Bucket Name**: `my-video-downloads-bucket`

**Region**: `us-east-1`

**Versioning**:
```json
{
    "Status": "Enabled"
}
```

**Encryption**:
```json
{
    "ServerSideEncryptionConfiguration": {
        "Rules": [
            {
                "ApplyServerSideEncryptionByDefault": {
                    "SSEAlgorithm": "AES256"
                },
                "BucketKeyEnabled": false
            }
        ]
    }
}
```

**CORS Configuration**:
```json
{
    "CORSRules": [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "PUT", "POST", "DELETE", "HEAD"],
            "AllowedOrigins": ["*"],
            "ExposeHeaders": ["ETag"],
            "MaxAgeSeconds": 3000
        }
    ]
}
```

**Bucket Policy**:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowCloudFrontOAC",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::my-video-downloads-bucket/*",
            "Condition": {
                "StringEquals": {
                    "AWS:SourceArn": "arn:aws:cloudfront::371751795928:distribution/E3N00R2D2NE9C5"
                }
            }
        },
        {
            "Sid": "AllowCrossAccountAccess",
            "Effect": "Allow",
            "Principal": {
                "AWS": [
                    "arn:aws:iam::846247542066:root",
                    "arn:aws:iam::628478946937:root"
                ]
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::my-video-downloads-bucket/*"
        }
    ]
}
```

---

## Step 2: Create S3 Module Structure

### Directory Setup
```bash
mkdir -p terraform/modules/s3
cd terraform/modules/s3
```

### Create main.tf

**File**: `terraform/modules/s3/main.tf`

```hcl
# S3 Bucket
resource "aws_s3_bucket" "main" {
  bucket = var.bucket_name

  tags = var.tags

  lifecycle {
    prevent_destroy = true
  }
}

# Bucket Versioning
resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id

  versioning_configuration {
    status = var.versioning_enabled ? "Enabled" : "Suspended"
  }
}

# Server-Side Encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "main" {
  bucket = aws_s3_bucket.main.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = var.sse_algorithm
    }
    bucket_key_enabled = var.bucket_key_enabled
  }
}

# CORS Configuration
resource "aws_s3_bucket_cors_configuration" "main" {
  count  = length(var.cors_rules) > 0 ? 1 : 0
  bucket = aws_s3_bucket.main.id

  dynamic "cors_rule" {
    for_each = var.cors_rules
    content {
      allowed_headers = cors_rule.value.allowed_headers
      allowed_methods = cors_rule.value.allowed_methods
      allowed_origins = cors_rule.value.allowed_origins
      expose_headers  = cors_rule.value.expose_headers
      max_age_seconds = cors_rule.value.max_age_seconds
    }
  }
}

# Bucket Policy
resource "aws_s3_bucket_policy" "main" {
  count  = var.bucket_policy != null ? 1 : 0
  bucket = aws_s3_bucket.main.id
  policy = var.bucket_policy
}
```

**Data Source**: AWS CLI commands above provided the configuration values

---

### Create variables.tf

**File**: `terraform/modules/s3/variables.tf`

```hcl
variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "versioning_enabled" {
  description = "Enable versioning for the bucket"
  type        = bool
  default     = true
}

variable "sse_algorithm" {
  description = "Server-side encryption algorithm (AES256 or aws:kms)"
  type        = string
  default     = "AES256"
}

variable "bucket_key_enabled" {
  description = "Enable S3 Bucket Key for SSE-KMS"
  type        = bool
  default     = false
}

variable "cors_rules" {
  description = "List of CORS rules"
  type = list(object({
    allowed_headers = list(string)
    allowed_methods = list(string)
    allowed_origins = list(string)
    expose_headers  = list(string)
    max_age_seconds = number
  }))
  default = []
}

variable "bucket_policy" {
  description = "Bucket policy JSON"
  type        = string
  default     = null
}

variable "tags" {
  description = "Tags to apply to the bucket"
  type        = map(string)
  default     = {}
}
```

**Data Source**: Derived from AWS CLI output structure

---

### Create outputs.tf

**File**: `terraform/modules/s3/outputs.tf`

```hcl
output "bucket_id" {
  description = "The name of the bucket"
  value       = aws_s3_bucket.main.id
}

output "bucket_arn" {
  description = "The ARN of the bucket"
  value       = aws_s3_bucket.main.arn
}

output "bucket_regional_domain_name" {
  description = "The bucket region-specific domain name"
  value       = aws_s3_bucket.main.bucket_regional_domain_name
}
```

**Data Source**: Terraform AWS provider documentation for available attributes

---

## Step 3: Use Module in Production Environment

### Add to main.tf

**File**: `terraform/environments/prod/main.tf`

```hcl
module "s3_main" {
  source = "../../modules/s3"

  bucket_name        = "my-video-downloads-bucket"
  versioning_enabled = true
  sse_algorithm      = "AES256"
  bucket_key_enabled = false

  cors_rules = [
    {
      allowed_headers = ["*"]
      allowed_methods = ["GET", "PUT", "POST", "DELETE", "HEAD"]
      allowed_origins = ["*"]
      expose_headers  = ["ETag"]
      max_age_seconds = 3000
    }
  ]

  bucket_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowCloudFrontOAC"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "arn:aws:s3:::my-video-downloads-bucket/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = "arn:aws:cloudfront::371751795928:distribution/E3N00R2D2NE9C5"
          }
        }
      },
      {
        Sid    = "AllowCrossAccountAccess"
        Effect = "Allow"
        Principal = {
          AWS = [
            "arn:aws:iam::846247542066:root",
            "arn:aws:iam::628478946937:root"
          ]
        }
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "arn:aws:s3:::my-video-downloads-bucket/*"
      }
    ]
  })

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}
```

**Data Source**: Values copied from AWS CLI output in Step 1

---

## Step 4: Import Existing Resources

### Initialize Terraform
```bash
cd terraform/environments/prod
terraform init
```

### Import S3 Bucket
```bash
terraform import module.s3_main.aws_s3_bucket.main my-video-downloads-bucket
```

**Output**:
```
module.s3_main.aws_s3_bucket.main: Importing from ID "my-video-downloads-bucket"...
module.s3_main.aws_s3_bucket.main: Import prepared!
module.s3_main.aws_s3_bucket.main: Import complete!
```

### Import Versioning Configuration
```bash
terraform import module.s3_main.aws_s3_bucket_versioning.main my-video-downloads-bucket
```

### Import Encryption Configuration
```bash
terraform import module.s3_main.aws_s3_bucket_server_side_encryption_configuration.main my-video-downloads-bucket
```

### Import CORS Configuration
```bash
terraform import 'module.s3_main.aws_s3_bucket_cors_configuration.main[0]' my-video-downloads-bucket
```

**Note**: The `[0]` is needed because CORS uses `count` in the module

### Import Bucket Policy
```bash
terraform import 'module.s3_main.aws_s3_bucket_policy.main[0]' my-video-downloads-bucket
```

---

## Step 5: Verify Import

### Run Terraform Plan
```bash
terraform plan
```

**Expected Output**:
```
No changes. Your infrastructure matches the configuration.
```

**If there are changes**, it means the Terraform config doesn't match AWS. Common issues:

1. **Bucket policy formatting**: Use `jsonencode()` for proper formatting
2. **CORS rule order**: Ensure rules match AWS exactly
3. **Tags**: Add any missing tags from AWS

### Fix Discrepancies

**Example Issue**: Plan shows bucket policy change

**Solution**: Copy exact policy from AWS CLI and format with `jsonencode()`

```bash
# Get current policy
aws s3api get-bucket-policy --bucket my-video-downloads-bucket --query Policy --output text | jq .

# Copy output and paste into main.tf with jsonencode()
```

### Re-run Plan
```bash
terraform plan
```

Repeat until output shows "No changes"

---

## Step 6: Test Changes

### Make a Small Change
```hcl
# Add a new tag
tags = {
  Environment = "production"
  ManagedBy   = "terraform"
  Project     = "ministry-platform"
  TestTag     = "test-value"  # NEW
}
```

### Apply Change
```bash
terraform apply
```

### Verify in AWS
```bash
aws s3api get-bucket-tagging --bucket my-video-downloads-bucket
```

**Output**:
```json
{
    "TagSet": [
        {"Key": "Environment", "Value": "production"},
        {"Key": "ManagedBy", "Value": "terraform"},
        {"Key": "Project", "Value": "ministry-platform"},
        {"Key": "TestTag", "Value": "test-value"}
    ]
}
```

### Remove Test Tag
```hcl
# Remove TestTag from main.tf
```

```bash
terraform apply
```

---

## Key Learnings

### Import Process
1. **Gather data first**: Use AWS CLI to inspect existing resources
2. **Create module**: Build Terraform config matching AWS state
3. **Import resources**: Use `terraform import` for each resource
4. **Verify**: Run `terraform plan` until no changes
5. **Test**: Make small change to verify Terraform control

### Common Pitfalls

**Pitfall 1: Bucket policy formatting**
- **Problem**: Terraform shows policy change even though it matches
- **Solution**: Use `jsonencode()` for consistent formatting

**Pitfall 2: CORS rule order**
- **Problem**: Terraform wants to recreate CORS rules
- **Solution**: Ensure rule order matches AWS exactly

**Pitfall 3: Missing sub-resources**
- **Problem**: Forgot to import versioning, encryption, etc.
- **Solution**: Import all sub-resources separately

### Terraform State

After import, Terraform state contains:
```json
{
  "resources": [
    {
      "module": "module.s3_main",
      "type": "aws_s3_bucket",
      "name": "main",
      "instances": [
        {
          "attributes": {
            "bucket": "my-video-downloads-bucket",
            "region": "us-east-1",
            "arn": "arn:aws:s3:::my-video-downloads-bucket"
          }
        }
      ]
    }
  ]
}
```

**Note**: State stores metadata, not actual S3 objects/data

---

## Troubleshooting

### Issue: Import fails with "resource already exists"
**Solution**: Resource already in state. Check with `terraform state list`

### Issue: Plan shows changes after import
**Solution**: Config doesn't match AWS. Update Terraform config to match AWS exactly

### Issue: Can't import CORS configuration
**Solution**: Use `[0]` index: `module.s3_main.aws_s3_bucket_cors_configuration.main[0]`

### Issue: Bucket policy shows as different
**Solution**: Use `jsonencode()` and ensure exact JSON structure match

---

## Related Files
- [S3 Module](../../modules/s3/main.tf)
- [Production Environment](../prod/main.tf)
- [Terraform Documentation](../TERRAFORM_DOCUMENTATION.md)

---

**Created**: February 10, 2026  
**Last Updated**: February 10, 2026
