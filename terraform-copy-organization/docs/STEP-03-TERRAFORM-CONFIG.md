# STEP 03: Terraform Configuration

**Goal**: Configure Terraform for multi-account deployment

**Time**: 15-20 minutes

---

## Overview

You'll create:
1. Provider configuration for both accounts
2. Variables for account IDs and configuration
3. Backend configuration for state management
4. Verify Terraform can authenticate to both accounts

---

## Step 3.1: Create Terraform Directory Structure

```powershell
# Navigate to terraform directory
cd C:\Users\Ed\Documents\Programming\AWS\terraform-copy-organization\terraform

# Verify you're in the right place
pwd
# Expected: C:\Users\Ed\Documents\Programming\AWS\terraform-copy-organization\terraform
```

---

## Step 3.2: Create providers.tf

**This file configures Terraform to work with both accounts.**

```powershell
# Create providers.tf
@'
# Terraform version and required providers
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Production account provider (default)
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "Infrastructure-Copy-Tutorial"
      ManagedBy   = "Terraform"
      Environment = "Production"
    }
  }
}

# Child account provider (using assume role)
provider "aws" {
  alias  = "child"
  region = var.aws_region
  
  assume_role {
    role_arn     = var.child_account_role_arn
    session_name = "terraform-copy-tutorial"
    external_id  = var.external_id
  }
  
  default_tags {
    tags = {
      Project     = "Infrastructure-Copy-Tutorial"
      ManagedBy   = "Terraform"
      Environment = "Child-Account"
      CopiedFrom  = "Production"
    }
  }
}
'@ | Out-File -FilePath providers.tf -Encoding utf8

Write-Host "✅ Created providers.tf"
```

**Key Points**:
- Two providers: default (production) and `child` (child account)
- Child provider uses `assume_role` to access child account
- Default tags applied to all resources
- Region is configurable via variable

---

## Step 3.3: Create variables.tf

**This file defines all input variables.**

```powershell
# Create variables.tf
@'
# AWS Region
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}

# Production Account ID
variable "production_account_id" {
  description = "Production AWS account ID"
  type        = string
  default     = "371751795928"
}

# Child Account ID
variable "child_account_id" {
  description = "Child AWS account ID (ed@ekewaka)"
  type        = string
  # No default - must be provided
}

# Cross-Account Role ARN
variable "child_account_role_arn" {
  description = "ARN of the cross-account role in child account"
  type        = string
  # Will be constructed from child_account_id
}

# External ID for AssumeRole
variable "external_id" {
  description = "External ID for cross-account role assumption"
  type        = string
  default     = "terraform-copy-tutorial"
  sensitive   = true
}

# Project Name
variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "infra-copy-tutorial"
}

# Environment
variable "environment" {
  description = "Environment name"
  type        = string
  default     = "tutorial"
}

# S3 Bucket Name
variable "s3_bucket_name" {
  description = "Name for S3 bucket (must be globally unique)"
  type        = string
  # Will be constructed with account ID for uniqueness
}

# Lambda Function Name
variable "lambda_function_name" {
  description = "Name for Lambda function"
  type        = string
  default     = "sample-function-tutorial"
}

# DynamoDB Table Name
variable "dynamodb_table_name" {
  description = "Name for DynamoDB table"
  type        = string
  default     = "sample-table-tutorial"
}

# SNS Topic Name
variable "sns_topic_name" {
  description = "Name for SNS topic"
  type        = string
  default     = "tutorial-alerts"
}

# API Gateway Name
variable "api_gateway_name" {
  description = "Name for API Gateway"
  type        = string
  default     = "sample-api-tutorial"
}
'@ | Out-File -FilePath variables.tf -Encoding utf8

Write-Host "✅ Created variables.tf"
```

---

## Step 3.4: Create terraform.tfvars

**This file provides values for variables.**

```powershell
# Create terraform.tfvars
@'
# AWS Configuration
aws_region             = "us-east-1"
production_account_id  = "371751795928"

# IMPORTANT: Replace with your actual child account ID
child_account_id = "628478946937"

# Cross-Account Role (constructed from child account ID)
child_account_role_arn = "arn:aws:iam::628478946937:role/TerraformCrossAccountRole"

# External ID (matches what you set in Step 1)
external_id = "terraform-copy-tutorial"

# Resource Names (will be unique per account)
project_name           = "infra-copy-tutorial"
environment            = "tutorial"
s3_bucket_name         = "infra-copy-tutorial-628478946937"
lambda_function_name   = "sample-function-tutorial"
dynamodb_table_name    = "sample-table-tutorial"
sns_topic_name         = "tutorial-alerts"
api_gateway_name       = "sample-api-tutorial"
'@ | Out-File -FilePath terraform.tfvars -Encoding utf8

Write-Host "✅ Created terraform.tfvars"
Write-Host "⚠️  IMPORTANT: Edit terraform.tfvars and replace REPLACE_WITH_YOUR_CHILD_ACCOUNT_ID with your actual child account ID"
```

**Action Required**: Edit `terraform.tfvars` and replace placeholders with your child account ID.

---

## Step 3.5: Create backend.tf

**This file configures where Terraform stores state.**

```powershell
# Create backend.tf
@'
# Local backend for tutorial
# In production, you would use S3 backend with state locking

terraform {
  backend "local" {
    path = "terraform.tfstate"
  }
}

# For production, use S3 backend:
# terraform {
#   backend "s3" {
#     bucket         = "my-terraform-state-bucket"
#     key            = "infra-copy/terraform.tfstate"
#     region         = "us-east-1"
#     encrypt        = true
#     dynamodb_table = "terraform-state-lock"
#   }
# }
'@ | Out-File -FilePath backend.tf -Encoding utf8

Write-Host "✅ Created backend.tf"
```

**Note**: Using local backend for tutorial simplicity. Production should use S3 backend with DynamoDB locking.

---

## Step 3.6: Create outputs.tf

**This file defines outputs to verify deployment.**

```powershell
# Create outputs.tf
@'
# Account Information
output "production_account_id" {
  description = "Production AWS account ID"
  value       = var.production_account_id
}

output "child_account_id" {
  description = "Child AWS account ID"
  value       = var.child_account_id
}

# IAM Role
output "lambda_execution_role_arn" {
  description = "ARN of Lambda execution role"
  value       = aws_iam_role.lambda_execution.arn
}

# S3 Bucket
output "s3_bucket_name" {
  description = "Name of S3 bucket"
  value       = aws_s3_bucket.main.id
}

output "s3_bucket_arn" {
  description = "ARN of S3 bucket"
  value       = aws_s3_bucket.main.arn
}

# DynamoDB Table
output "dynamodb_table_name" {
  description = "Name of DynamoDB table"
  value       = aws_dynamodb_table.main.name
}

output "dynamodb_table_arn" {
  description = "ARN of DynamoDB table"
  value       = aws_dynamodb_table.main.arn
}

# Lambda Function
output "lambda_function_name" {
  description = "Name of Lambda function"
  value       = aws_lambda_function.main.function_name
}

output "lambda_function_arn" {
  description = "ARN of Lambda function"
  value       = aws_lambda_function.main.arn
}

# API Gateway
output "api_gateway_id" {
  description = "ID of API Gateway"
  value       = aws_api_gateway_rest_api.main.id
}

output "api_gateway_endpoint" {
  description = "Invoke URL of API Gateway"
  value       = "${aws_api_gateway_deployment.main.invoke_url}${aws_api_gateway_stage.main.stage_name}"
}

# SNS Topic
output "sns_topic_arn" {
  description = "ARN of SNS topic"
  value       = aws_sns_topic.alerts.arn
}

# CloudWatch Log Group
output "log_group_name" {
  description = "Name of CloudWatch log group"
  value       = aws_cloudwatch_log_group.lambda.name
}

# Summary
output "deployment_summary" {
  description = "Summary of deployed resources"
  value = {
    account     = var.child_account_id
    region      = var.aws_region
    environment = var.environment
    resources = {
      s3_bucket       = aws_s3_bucket.main.id
      dynamodb_table  = aws_dynamodb_table.main.name
      lambda_function = aws_lambda_function.main.function_name
      api_gateway     = aws_api_gateway_rest_api.main.name
      sns_topic       = aws_sns_topic.alerts.name
    }
  }
}
'@ | Out-File -FilePath outputs.tf -Encoding utf8

Write-Host "✅ Created outputs.tf"
```

---

## Step 3.7: Initialize Terraform

```powershell
# Initialize Terraform
terraform init

# Expected output:
# Initializing the backend...
# Initializing provider plugins...
# - Finding hashicorp/aws versions matching "~> 5.0"...
# - Installing hashicorp/aws v5.x.x...
# Terraform has been successfully initialized!
```

**If successful**: You'll see "Terraform has been successfully initialized!"

**If error**: Check that:
- You're in the terraform directory
- providers.tf exists
- Internet connection is working

---

## Step 3.8: Validate Configuration

```powershell
# Validate Terraform configuration
terraform validate

# Expected output:
# Success! The configuration is valid.
```

**If error**: Check syntax in .tf files

---

## Step 3.9: Format Configuration

```powershell
# Format all Terraform files
terraform fmt

# This will auto-format all .tf files
```

---

## Step 3.10: Verification Checklist

Before proceeding, verify:

- [ ] All .tf files created (providers, variables, backend, outputs)
- [ ] terraform.tfvars created and edited with child account ID
- [ ] `terraform init` completed successfully
- [ ] `terraform validate` shows success
- [ ] `terraform fmt` ran without errors
- [ ] You understand provider aliases (default vs child)
- [ ] You understand assume_role configuration

---

## Understanding Multi-Account Providers

### Default Provider (Production Account)

```hcl
provider "aws" {
  region = "us-east-1"
  # Uses default AWS credentials
}

# Resources use this provider by default
resource "aws_s3_bucket" "prod" {
  bucket = "my-prod-bucket"
  # Created in production account
}
```

### Child Provider (Child Account)

```hcl
provider "aws" {
  alias  = "child"
  region = "us-east-1"
  
  assume_role {
    role_arn = "arn:aws:iam::CHILD_ID:role/TerraformCrossAccountRole"
  }
}

# Resources must specify provider explicitly
resource "aws_s3_bucket" "child" {
  provider = aws.child
  bucket   = "my-child-bucket"
  # Created in child account
}
```

**Key Difference**: Must specify `provider = aws.child` for child account resources.

---

## Troubleshooting

### Error: "No valid credential sources found"

**Cause**: AWS credentials not configured

**Fix**:
```powershell
aws configure
# Enter your access key, secret key, region
```

### Error: "Error assuming role"

**Cause**: Cross-account role not accessible

**Fix**: Verify in Step 1 that assume-role works:
```powershell
aws sts assume-role `
    --role-arn "arn:aws:iam::CHILD_ID:role/TerraformCrossAccountRole" `
    --role-session-name "test" `
    --external-id "terraform-copy-tutorial"
```

### Error: "Invalid provider configuration"

**Cause**: Syntax error in providers.tf

**Fix**: Run `terraform validate` to see specific error

---

## Quick Reference

**Files Created**:
- `providers.tf` - Provider configuration
- `variables.tf` - Variable definitions
- `terraform.tfvars` - Variable values
- `backend.tf` - State configuration
- `outputs.tf` - Output definitions

**Commands Used**:
- `terraform init` - Initialize Terraform
- `terraform validate` - Validate configuration
- `terraform fmt` - Format files

---

## Next Step

✅ **Terraform configuration complete!**

→ Continue to `STEP-04-DEPLOY.md` to create the main infrastructure and deploy to child account.

---

## Practice Tips

**For subsequent practice runs**:
1. Files already exist - just review
2. Run `terraform init` (quick if providers cached)
3. Verify `terraform validate` passes
4. Update terraform.tfvars if needed
5. Takes ~3 minutes
