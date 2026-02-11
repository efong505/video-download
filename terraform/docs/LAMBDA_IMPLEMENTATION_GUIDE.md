# Lambda Functions - Detailed Implementation Guide

## Overview
Step-by-step guide for creating the Lambda module and importing 18 existing Lambda functions into Terraform.

---

## Step 1: Gather Existing Lambda Function Information

### Commands to List All Lambda Functions

```bash
# List all Lambda functions
aws lambda list-functions --query 'Functions[*].[FunctionName,Runtime,Handler,MemorySize,Timeout]' --output table

# Get detailed info for specific function
aws lambda get-function --function-name router

# Get function configuration
aws lambda get-function-configuration --function-name router

# Get function code location
aws lambda get-function --function-name router --query 'Code.Location'

# List function layers
aws lambda get-function-configuration --function-name router --query 'Layers[*].Arn'

# Get environment variables
aws lambda get-function-configuration --function-name router --query 'Environment.Variables'

# Get IAM role
aws lambda get-function-configuration --function-name router --query 'Role'
```

### Data Collected for Each Function

**Example: router function**

```json
{
    "FunctionName": "router",
    "FunctionArn": "arn:aws:lambda:us-east-1:371751795928:function:router",
    "Runtime": "python3.12",
    "Role": "arn:aws:iam::371751795928:role/lambda-execution-role",
    "Handler": "index.lambda_handler",
    "CodeSize": 45678901,
    "Description": "Video download router with quota management",
    "Timeout": 900,
    "MemorySize": 3008,
    "LastModified": "2026-02-09T10:30:00.000+0000",
    "Environment": {
        "Variables": {
            "SNS_TOPIC_ARN": "arn:aws:sns:us-east-1:371751795928:video-download-notifications"
        }
    },
    "Layers": [
        {
            "Arn": "arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer:1"
        }
    ]
}
```

### All 18 Lambda Functions Discovered

| Function Name | Runtime | Memory | Timeout | Layers |
|--------------|---------|--------|---------|--------|
| router | python3.12 | 3008 MB | 900s | yt-dlp-layer |
| downloader | python3.12 | 3008 MB | 900s | yt-dlp-layer, ffmpeg-layer |
| admin_api | python3.12 | 512 MB | 30s | - |
| articles_api | python3.12 | 512 MB | 30s | - |
| auth_api | python3.12 | 512 MB | 30s | - |
| comments_api | python3.12 | 512 MB | 30s | - |
| contributors_api | python3.12 | 512 MB | 30s | - |
| news_api | python3.12 | 512 MB | 30s | - |
| resources_api | python3.12 | 512 MB | 30s | - |
| tag_api | python3.12 | 512 MB | 30s | - |
| thumbnail_generator | python3.12 | 1024 MB | 60s | ffmpeg-layer |
| s3_thumbnail_trigger | python3.12 | 256 MB | 15s | - |
| url_analysis_api | python3.12 | 512 MB | 30s | - |
| article_analysis_api | python3.12 | 512 MB | 30s | - |
| video_list_api | python3.12 | 512 MB | 30s | - |
| paypal_billing_api | python3.12 | 512 MB | 30s | - |
| prayer_api | python3.12 | 512 MB | 30s | - |
| notifications_api | python3.12 | 512 MB | 30s | - |

---

## Step 2: Design Lambda Module Strategy

### Key Decision: Separation of Concerns

**Problem**: Terraform wants to manage Lambda code, but we want CI/CD to handle deployments.

**Solution**: Use placeholder.zip with `ignore_changes` lifecycle rule.

**How it works**:
1. Terraform creates Lambda with placeholder.zip (empty file)
2. Terraform ignores future code changes (`ignore_changes = [filename, source_code_hash]`)
3. CI/CD deploys actual code via `aws lambda update-function-code`
4. Terraform only manages configuration (memory, timeout, IAM role, environment variables)

### Create Placeholder ZIP

```bash
# Create empty placeholder
mkdir -p terraform/modules/lambda
cd terraform/modules/lambda

# Create empty index.py
echo "def lambda_handler(event, context): return {'statusCode': 200}" > index.py

# Create ZIP
zip placeholder.zip index.py

# Remove index.py (only need ZIP)
rm index.py
```

---

## Step 3: Create Lambda Module

### Directory Setup
```bash
mkdir -p terraform/modules/lambda
cd terraform/modules/lambda
```

### Create main.tf

**File**: `terraform/modules/lambda/main.tf`

```hcl
# Lambda Function
resource "aws_lambda_function" "this" {
  function_name = var.function_name
  role          = var.role_arn
  handler       = var.handler
  runtime       = var.runtime
  
  filename         = "${path.module}/placeholder.zip"
  source_code_hash = filebase64sha256("${path.module}/placeholder.zip")
  
  memory_size = var.memory_size
  timeout     = var.timeout
  
  layers = var.layers
  
  dynamic "environment" {
    for_each = length(var.environment_variables) > 0 ? [1] : []
    content {
      variables = var.environment_variables
    }
  }
  
  tags = var.tags
  
  lifecycle {
    ignore_changes = [
      filename,
      source_code_hash,
      last_modified
    ]
  }
}
```

**Data Source**: 
- Lambda configurations from `aws lambda get-function-configuration`
- Placeholder.zip created in Step 2
- `ignore_changes` prevents Terraform from managing code

### Create variables.tf

**File**: `terraform/modules/lambda/variables.tf`

```hcl
variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "role_arn" {
  description = "ARN of the IAM role for Lambda execution"
  type        = string
}

variable "handler" {
  description = "Function entrypoint (e.g., index.lambda_handler)"
  type        = string
  default     = "index.lambda_handler"
}

variable "runtime" {
  description = "Lambda runtime (e.g., python3.12)"
  type        = string
  default     = "python3.12"
}

variable "memory_size" {
  description = "Amount of memory in MB"
  type        = number
  default     = 512
}

variable "timeout" {
  description = "Function timeout in seconds"
  type        = number
  default     = 30
}

variable "layers" {
  description = "List of Lambda layer ARNs"
  type        = list(string)
  default     = []
}

variable "environment_variables" {
  description = "Environment variables for the function"
  type        = map(string)
  default     = {}
}

variable "tags" {
  description = "Tags to apply to the function"
  type        = map(string)
  default     = {}
}
```

**Data Source**: Derived from AWS Lambda configuration structure

### Create outputs.tf

**File**: `terraform/modules/lambda/outputs.tf`

```hcl
output "function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.this.function_name
}

output "function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.this.arn
}

output "invoke_arn" {
  description = "Invoke ARN of the Lambda function"
  value       = aws_lambda_function.this.invoke_arn
}

output "qualified_arn" {
  description = "Qualified ARN of the Lambda function"
  value       = aws_lambda_function.this.qualified_arn
}
```

---

## Step 4: Use Module in Production Environment

### Add to main.tf

**File**: `terraform/environments/prod/main.tf`

```hcl
# Router Lambda (high memory, long timeout, with layers)
module "lambda_router" {
  source = "../../modules/lambda"

  function_name = "router"
  role_arn      = module.iam_lambda_execution.role_arn
  handler       = "index.lambda_handler"
  runtime       = "python3.12"
  memory_size   = 3008
  timeout       = 900

  layers = [
    "arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer:1"
  ]

  environment_variables = {
    SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:371751795928:video-download-notifications"
  }

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}

# Admin API Lambda (standard config)
module "lambda_admin_api" {
  source = "../../modules/lambda"

  function_name = "admin_api"
  role_arn      = module.iam_lambda_execution.role_arn
  handler       = "index.lambda_handler"
  runtime       = "python3.12"
  memory_size   = 512
  timeout       = 30

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}

# Repeat for all 18 functions...
```

**Data Source**: Values from Step 1 AWS CLI output

---

## Step 5: Import Existing Lambda Functions

### Initialize Terraform
```bash
cd terraform/environments/prod
terraform init
```

### Import Router Function
```bash
terraform import module.lambda_router.aws_lambda_function.this router
```

**Output**:
```
module.lambda_router.aws_lambda_function.this: Importing from ID "router"...
module.lambda_router.aws_lambda_function.this: Import prepared!
module.lambda_router.aws_lambda_function.this: Import complete!
```

### Import All 18 Functions

```bash
# Script to import all functions
FUNCTIONS=(
  "router"
  "downloader"
  "admin_api"
  "articles_api"
  "auth_api"
  "comments_api"
  "contributors_api"
  "news_api"
  "resources_api"
  "tag_api"
  "thumbnail_generator"
  "s3_thumbnail_trigger"
  "url_analysis_api"
  "article_analysis_api"
  "video_list_api"
  "paypal_billing_api"
  "prayer_api"
  "notifications_api"
)

for func in "${FUNCTIONS[@]}"; do
  echo "Importing $func..."
  terraform import "module.lambda_${func}.aws_lambda_function.this" "$func"
done
```

---

## Step 6: Verify Import

### Run Terraform Plan
```bash
terraform plan
```

**Expected Output**:
```
No changes. Your infrastructure matches the configuration.
```

**If there are changes**, common issues:

### Issue 1: Memory Size Mismatch
```
# Plan shows:
~ memory_size = 1024 -> 512

# Solution: Update main.tf to match AWS
memory_size = 1024
```

### Issue 2: Environment Variables Mismatch
```
# Plan shows:
~ environment {
    ~ variables = {
        + NEW_VAR = "value"
      }
  }

# Solution: Add missing variables to main.tf
environment_variables = {
  SNS_TOPIC_ARN = "..."
  NEW_VAR       = "value"
}
```

### Issue 3: Layers Mismatch
```
# Plan shows:
~ layers = [
    - "arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer:2"
    + "arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer:1"
  ]

# Solution: Update layer version in main.tf
layers = [
  "arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer:2"
]
```

### Get Current Configuration
```bash
# If plan shows changes, get exact AWS config
aws lambda get-function-configuration --function-name router > router-config.json

# Compare with Terraform config
cat router-config.json
```

---

## Step 7: Test Terraform Control

### Make a Small Change
```hcl
# Increase memory for router
memory_size = 3072  # Changed from 3008
```

### Apply Change
```bash
terraform apply
```

**Output**:
```
Terraform will perform the following actions:

  # module.lambda_router.aws_lambda_function.this will be updated in-place
  ~ resource "aws_lambda_function" "this" {
      ~ memory_size = 3008 -> 3072
    }

Plan: 0 to add, 1 to change, 0 to destroy.

Apply complete! Resources: 0 added, 1 changed, 0 destroyed.
```

### Verify in AWS
```bash
aws lambda get-function-configuration --function-name router --query 'MemorySize'
```

**Output**: `3072`

### Revert Change
```hcl
memory_size = 3008  # Back to original
```

```bash
terraform apply
```

---

## Step 8: Verify Code Deployment Separation

### Deploy Code via CI/CD (Not Terraform)

```bash
# Navigate to function directory
cd router

# Create deployment package
zip -r function.zip . -x "*.zip" "*.pyc" "__pycache__/*"

# Deploy via AWS CLI (simulating CI/CD)
aws lambda update-function-code \
  --function-name router \
  --zip-file fileb://function.zip
```

### Run Terraform Plan
```bash
cd terraform/environments/prod
terraform plan
```

**Expected Output**:
```
No changes. Your infrastructure matches the configuration.
```

**Why?** The `ignore_changes` lifecycle rule tells Terraform to ignore code changes.

---

## Step 9: Document Lambda Layer Strategy

### Current Layers

```bash
# List all layers
aws lambda list-layers

# Get layer versions
aws lambda list-layer-versions --layer-name yt-dlp-layer
aws lambda list-layer-versions --layer-name ffmpeg-layer
```

**Layers Found**:
- `yt-dlp-layer:1` - Video download library (used by router, downloader)
- `ffmpeg-layer:1` - Video processing (used by downloader, thumbnail_generator)

### Layer Management Decision

**Current State**: Layers managed manually, not in Terraform

**Reason**: Layers are large (100+ MB) and rarely change

**Future Plan**: Add to Terraform in Week 11-12

---

## Key Learnings

### Placeholder.zip Pattern
- **Purpose**: Satisfy Terraform's requirement for Lambda code
- **Benefit**: Separates infrastructure (Terraform) from code (CI/CD)
- **Implementation**: Use `ignore_changes` to prevent Terraform from managing code

### Import Process
1. Gather exact configuration from AWS
2. Create Terraform config matching AWS
3. Import resource into state
4. Verify with `terraform plan` (should show no changes)
5. Test by making small change

### Common Pitfalls

**Pitfall 1: Forgetting ignore_changes**
- **Problem**: Terraform tries to update code on every apply
- **Solution**: Add `ignore_changes = [filename, source_code_hash]`

**Pitfall 2: Layer version mismatch**
- **Problem**: Terraform uses layer:1 but AWS has layer:2
- **Solution**: Check current layer version with `aws lambda get-function-configuration`

**Pitfall 3: Environment variables**
- **Problem**: Missing or extra environment variables
- **Solution**: Use `dynamic "environment"` block to handle optional variables

---

## Terraform State

After import, state contains:

```json
{
  "resources": [
    {
      "module": "module.lambda_router",
      "type": "aws_lambda_function",
      "name": "this",
      "instances": [
        {
          "attributes": {
            "function_name": "router",
            "arn": "arn:aws:lambda:us-east-1:371751795928:function:router",
            "role": "arn:aws:iam::371751795928:role/lambda-execution-role",
            "runtime": "python3.12",
            "handler": "index.lambda_handler",
            "memory_size": 3008,
            "timeout": 900
          }
        }
      ]
    }
  ]
}
```

**Note**: State stores configuration, not actual Lambda code

---

## Troubleshooting

### Issue: Import fails with "resource already exists"
**Solution**: Resource already in state. Check with `terraform state list`

### Issue: Plan shows code changes after import
**Solution**: Add `ignore_changes` lifecycle rule for filename and source_code_hash

### Issue: Environment variables keep changing
**Solution**: Use `dynamic "environment"` block with conditional logic

### Issue: Layer ARN format incorrect
**Solution**: Use full ARN including version: `arn:aws:lambda:region:account:layer:name:version`

---

## Related Files
- [Lambda Module](../../modules/lambda/main.tf)
- [Production Environment](../prod/main.tf)
- [Terraform Documentation](../TERRAFORM_DOCUMENTATION.md)
- [CI/CD Documentation](../../.github/CI_CD_DOCUMENTATION.md)

---

**Created**: February 10, 2026  
**Last Updated**: February 10, 2026
