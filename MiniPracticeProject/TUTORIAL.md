# Mini Terraform Practice Project - Complete Tutorial

## Table of Contents
1. [Setup](#setup)
2. [Phase 1: Create S3 Module](#phase-1-create-s3-module)
3. [Phase 2: Create DynamoDB Module](#phase-2-create-dynamodb-module)
4. [Phase 3: Create Lambda Module](#phase-3-create-lambda-module)
5. [Phase 4: Create CloudWatch Module](#phase-4-create-cloudwatch-module)
6. [Phase 5: Create SNS Module](#phase-5-create-sns-module)
7. [Phase 6: Main Configuration](#phase-6-main-configuration)
8. [Phase 7: Deploy Everything](#phase-7-deploy-everything)
9. [Phase 8: Practice Import](#phase-8-practice-import)
10. [Phase 9: Teardown](#phase-9-teardown)

---

## Setup

### Step 1: Verify Prerequisites
```powershell
# Check AWS CLI
aws --version

# Check Terraform
terraform --version

# Verify AWS credentials
aws sts get-caller-identity
```

### Step 2: Navigate to Project
```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\MiniPracticeProject
```

---

## Phase 1: Create S3 Module

### What You'll Learn
- Module structure (variables.tf, main.tf, outputs.tf)
- S3 bucket configuration
- Random suffix generation

### Step 1.1: Create Module Directory
```powershell
mkdir terraform\modules\s3-practice
cd terraform\modules\s3-practice
```

### Step 1.2: Create variables.tf
**File**: `terraform/modules/s3-practice/variables.tf`

```hcl
variable "bucket_prefix" {
  description = "Prefix for S3 bucket name"
  type        = string
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "practice"
}
```

**Explanation**:
- `bucket_prefix`: Required input (no default)
- `environment`: Optional input (has default)

### Step 1.3: Create main.tf
**File**: `terraform/modules/s3-practice/main.tf`

```hcl
# Generate random suffix for unique bucket name
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# Create S3 bucket
resource "aws_s3_bucket" "this" {
  bucket = "${var.bucket_prefix}-${random_id.bucket_suffix.hex}"

  tags = {
    Name        = "${var.bucket_prefix}-${random_id.bucket_suffix.hex}"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# Enable versioning
resource "aws_s3_bucket_versioning" "this" {
  bucket = aws_s3_bucket.this.id

  versioning_configuration {
    status = "Enabled"
  }
}
```

**Explanation**:
- `random_id`: Creates unique suffix (prevents naming conflicts)
- `aws_s3_bucket`: Main bucket resource
- `aws_s3_bucket_versioning`: Separate resource for versioning (AWS best practice)

### Step 1.4: Create outputs.tf
**File**: `terraform/modules/s3-practice/outputs.tf`

```hcl
output "bucket_name" {
  description = "Name of the S3 bucket"
  value       = aws_s3_bucket.this.bucket
}

output "bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.this.arn
}

output "bucket_id" {
  description = "ID of the S3 bucket"
  value       = aws_s3_bucket.this.id
}
```

**Explanation**:
- Outputs expose module data to parent configuration
- Think of them as "return values" from a function

---

## Phase 2: Create DynamoDB Module

### What You'll Learn
- DynamoDB table configuration
- Attribute definitions
- On-demand billing mode

### Step 2.1: Create Module Directory
```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\MiniPracticeProject
mkdir terraform\modules\dynamodb-practice
cd terraform\modules\dynamodb-practice
```

### Step 2.2: Create variables.tf
**File**: `terraform/modules/dynamodb-practice/variables.tf`

```hcl
variable "table_name" {
  description = "Name of the DynamoDB table"
  type        = string
}

variable "hash_key" {
  description = "Hash key (partition key) for the table"
  type        = string
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "practice"
}
```

### Step 2.3: Create main.tf
**File**: `terraform/modules/dynamodb-practice/main.tf`

```hcl
resource "aws_dynamodb_table" "this" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"  # On-demand (no cost when empty)
  hash_key     = var.hash_key

  attribute {
    name = var.hash_key
    type = "S"  # String type
  }

  tags = {
    Name        = var.table_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

**Explanation**:
- `PAY_PER_REQUEST`: Only pay for actual reads/writes (free when empty)
- `hash_key`: Partition key for data distribution
- `attribute`: Only define keys used in indexes

### Step 2.4: Create outputs.tf
**File**: `terraform/modules/dynamodb-practice/outputs.tf`

```hcl
output "table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.this.name
}

output "table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.this.arn
}

output "table_id" {
  description = "ID of the DynamoDB table"
  value       = aws_dynamodb_table.this.id
}
```

---

## Phase 3: Create Lambda Module

### What You'll Learn
- Lambda function configuration
- Placeholder.zip pattern
- ignore_changes lifecycle

### Step 3.1: Create Module Directory
```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\MiniPracticeProject
mkdir terraform\modules\lambda-practice
cd terraform\modules\lambda-practice
```

### Step 3.2: Create Placeholder ZIP
```powershell
# Create empty placeholder
echo "placeholder" > placeholder.txt
Compress-Archive -Path placeholder.txt -DestinationPath placeholder.zip
Remove-Item placeholder.txt
```

### Step 3.3: Create variables.tf
**File**: `terraform/modules/lambda-practice/variables.tf`

```hcl
variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.12"
}

variable "handler" {
  description = "Lambda handler"
  type        = string
  default     = "index.lambda_handler"
}

variable "memory_size" {
  description = "Memory allocation in MB"
  type        = number
  default     = 128
}

variable "timeout" {
  description = "Timeout in seconds"
  type        = number
  default     = 30
}

variable "role_arn" {
  description = "IAM role ARN for Lambda execution"
  type        = string
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "practice"
}
```

### Step 3.4: Create main.tf
**File**: `terraform/modules/lambda-practice/main.tf`

```hcl
resource "aws_lambda_function" "this" {
  function_name = var.function_name
  role          = var.role_arn
  handler       = var.handler
  runtime       = var.runtime
  memory_size   = var.memory_size
  timeout       = var.timeout
  filename      = "${path.module}/placeholder.zip"

  tags = {
    Name        = var.function_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }

  lifecycle {
    # Don't update when code changes (managed separately)
    ignore_changes = [filename, source_code_hash]
  }
}
```

**Explanation**:
- `filename`: Uses placeholder.zip initially
- `lifecycle.ignore_changes`: Terraform won't update when you deploy real code
- This pattern separates infrastructure (Terraform) from code (deployment scripts)

### Step 3.5: Create outputs.tf
**File**: `terraform/modules/lambda-practice/outputs.tf`

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
  description = "Invoke ARN for API Gateway integration"
  value       = aws_lambda_function.this.invoke_arn
}
```

---

## Phase 4: Create CloudWatch Module

### What You'll Learn
- CloudWatch log group configuration
- Retention policies

### Step 4.1: Create Module Directory
```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\MiniPracticeProject
mkdir terraform\modules\cloudwatch-practice
cd terraform\modules\cloudwatch-practice
```

### Step 4.2: Create variables.tf
**File**: `terraform/modules/cloudwatch-practice/variables.tf`

```hcl
variable "log_group_name" {
  description = "Name of the CloudWatch log group"
  type        = string
}

variable "retention_days" {
  description = "Log retention in days"
  type        = number
  default     = 7
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "practice"
}
```

### Step 4.3: Create main.tf
**File**: `terraform/modules/cloudwatch-practice/main.tf`

```hcl
resource "aws_cloudwatch_log_group" "this" {
  name              = var.log_group_name
  retention_in_days = var.retention_days

  tags = {
    Name        = var.log_group_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

### Step 4.4: Create outputs.tf
**File**: `terraform/modules/cloudwatch-practice/outputs.tf`

```hcl
output "log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.this.name
}

output "log_group_arn" {
  description = "ARN of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.this.arn
}
```

---

## Phase 5: Create SNS Module

### What You'll Learn
- SNS topic configuration
- Email subscriptions

### Step 5.1: Create Module Directory
```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\MiniPracticeProject
mkdir terraform\modules\sns-practice
cd terraform\modules\sns-practice
```

### Step 5.2: Create variables.tf
**File**: `terraform/modules/sns-practice/variables.tf`

```hcl
variable "topic_name" {
  description = "Name of the SNS topic"
  type        = string
}

variable "environment" {
  description = "Environment tag"
  type        = string
  default     = "practice"
}
```

### Step 5.3: Create main.tf
**File**: `terraform/modules/sns-practice/main.tf`

```hcl
resource "aws_sns_topic" "this" {
  name = var.topic_name

  tags = {
    Name        = var.topic_name
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

### Step 5.4: Create outputs.tf
**File**: `terraform/modules/sns-practice/outputs.tf`

```hcl
output "topic_arn" {
  description = "ARN of the SNS topic"
  value       = aws_sns_topic.this.arn
}

output "topic_name" {
  description = "Name of the SNS topic"
  value       = aws_sns_topic.this.name
}
```

---

## Phase 6: Main Configuration

### What You'll Learn
- Calling modules
- Passing variables between modules
- Output aggregation

### Step 6.1: Create Environment Directory
```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\MiniPracticeProject
mkdir terraform\environments\practice
cd terraform\environments\practice
```

### Step 6.2: Create main.tf
**File**: `terraform/environments/practice/main.tf`

```hcl
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "MiniPracticeProject"
      Environment = "practice"
      ManagedBy   = "Terraform"
    }
  }
}

# S3 Bucket Module
module "s3_practice" {
  source = "../../modules/s3-practice"
  
  bucket_prefix = var.bucket_prefix
  environment   = "practice"
}

# DynamoDB Table Module
module "dynamodb_practice" {
  source = "../../modules/dynamodb-practice"
  
  table_name  = var.dynamodb_table_name
  hash_key    = "id"
  environment = "practice"
}

# Lambda Function Module
module "lambda_practice" {
  source = "../../modules/lambda-practice"
  
  function_name = var.lambda_function_name
  runtime       = "python3.12"
  handler       = "index.lambda_handler"
  memory_size   = 128
  timeout       = 30
  role_arn      = var.lambda_role_arn
  environment   = "practice"
}

# CloudWatch Log Group Module
module "cloudwatch_practice" {
  source = "../../modules/cloudwatch-practice"
  
  log_group_name = "/aws/lambda/${var.lambda_function_name}"
  retention_days = 7
  environment    = "practice"
}

# SNS Topic Module
module "sns_practice" {
  source = "../../modules/sns-practice"
  
  topic_name  = var.sns_topic_name
  environment = "practice"
}
```

### Step 6.3: Create variables.tf
**File**: `terraform/environments/practice/variables.tf`

```hcl
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "bucket_prefix" {
  description = "Prefix for S3 bucket name"
  type        = string
  default     = "practice-terraform-learning"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  type        = string
  default     = "PracticeTable"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "hello-world-practice"
}

variable "lambda_role_arn" {
  description = "IAM role ARN for Lambda (use existing role)"
  type        = string
}

variable "sns_topic_name" {
  description = "Name of the SNS topic"
  type        = string
  default     = "practice-alerts"
}
```

### Step 6.4: Create outputs.tf
**File**: `terraform/environments/practice/outputs.tf`

```hcl
output "s3_bucket_name" {
  description = "Name of the S3 bucket"
  value       = module.s3_practice.bucket_name
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = module.dynamodb_practice.table_name
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = module.lambda_practice.function_name
}

output "cloudwatch_log_group" {
  description = "Name of the CloudWatch log group"
  value       = module.cloudwatch_practice.log_group_name
}

output "sns_topic_arn" {
  description = "ARN of the SNS topic"
  value       = module.sns_practice.topic_arn
}
```

### Step 6.5: Create terraform.tfvars
**File**: `terraform/environments/practice/terraform.tfvars`

```hcl
aws_region            = "us-east-1"
bucket_prefix         = "practice-terraform-learning"
dynamodb_table_name   = "PracticeTable"
lambda_function_name  = "hello-world-practice"
lambda_role_arn       = "arn:aws:iam::371751795928:role/lambda-execution-role"  # Use your existing role
sns_topic_name        = "practice-alerts"
```

**Note**: Replace the `lambda_role_arn` with your actual IAM role ARN.

---

## Phase 7: Deploy Everything

### Step 7.1: Initialize Terraform
```powershell
cd C:\Users\Ed\Documents\Programming\AWS\Downloader\MiniPracticeProject\terraform\environments\practice

terraform init
```

**What happens**:
- Downloads AWS provider
- Downloads random provider
- Initializes modules
- Creates `.terraform` directory

### Step 7.2: Validate Configuration
```powershell
terraform validate
```

**Expected output**: `Success! The configuration is valid.`

### Step 7.3: Format Code
```powershell
terraform fmt -recursive
```

**What happens**: Auto-formats all `.tf` files

### Step 7.4: Preview Changes
```powershell
terraform plan
```

**What to look for**:
- `Plan: 7 to add, 0 to change, 0 to destroy`
- Review each resource being created
- Check for any errors

### Step 7.5: Apply Configuration
```powershell
terraform apply
```

**Steps**:
1. Review the plan
2. Type `yes` when prompted
3. Wait 30-60 seconds for creation
4. Review outputs

**Expected output**:
```
Apply complete! Resources: 7 added, 0 changed, 0 destroyed.

Outputs:

cloudwatch_log_group = "/aws/lambda/hello-world-practice"
dynamodb_table_name = "PracticeTable"
lambda_function_name = "hello-world-practice"
s3_bucket_name = "practice-terraform-learning-a1b2c3d4"
sns_topic_arn = "arn:aws:sns:us-east-1:371751795928:practice-alerts"
```

### Step 7.6: Verify in AWS Console
```powershell
# List S3 buckets
aws s3 ls | findstr practice

# Check DynamoDB table
aws dynamodb describe-table --table-name PracticeTable --query "Table.TableStatus"

# Check Lambda function
aws lambda get-function --function-name hello-world-practice --query "Configuration.FunctionName"

# Check CloudWatch log group
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/hello-world-practice"

# Check SNS topic
aws sns list-topics | findstr practice
```

---

## Phase 8: Practice Import

### What You'll Learn
- Importing existing resources
- State management
- Removing resources from state

### Step 8.1: Remove Lambda from State
```powershell
terraform state rm module.lambda_practice.aws_lambda_function.this
```

**What happens**: Terraform "forgets" about the Lambda function (but it still exists in AWS)

### Step 8.2: Verify State
```powershell
terraform state list
```

**Expected**: Lambda function NOT in list

### Step 8.3: Run Plan (Shows Drift)
```powershell
terraform plan
```

**Expected**: Terraform wants to CREATE the Lambda function (because it's not in state)

### Step 8.4: Import Lambda Back
```powershell
terraform import module.lambda_practice.aws_lambda_function.this hello-world-practice
```

**What happens**: Terraform adds the existing Lambda back to state

### Step 8.5: Verify Import
```powershell
terraform plan
```

**Expected**: `No changes. Your infrastructure matches the configuration.`

### Step 8.6: Practice with Other Resources
```powershell
# Remove DynamoDB from state
terraform state rm module.dynamodb_practice.aws_dynamodb_table.this

# Import it back
terraform import module.dynamodb_practice.aws_dynamodb_table.this PracticeTable

# Verify
terraform plan
```

---

## Phase 9: Teardown

### Step 9.1: Preview Destruction
```powershell
terraform plan -destroy
```

**What to look for**: `Plan: 0 to add, 0 to change, 7 to destroy`

### Step 9.2: Destroy All Resources
```powershell
terraform destroy
```

**Steps**:
1. Review destruction plan
2. Type `yes` when prompted
3. Wait 30-60 seconds
4. Verify all resources deleted

### Step 9.3: Verify Cleanup
```powershell
# Check S3 (should be empty)
aws s3 ls | findstr practice

# Check DynamoDB (should not exist)
aws dynamodb describe-table --table-name PracticeTable 2>$null

# Check Lambda (should not exist)
aws lambda get-function --function-name hello-world-practice 2>$null
```

**Expected**: All commands return empty or "not found"

### Step 9.4: Clean Local Files (Optional)
```powershell
# Remove Terraform state files
Remove-Item terraform.tfstate*
Remove-Item .terraform -Recurse -Force
Remove-Item .terraform.lock.hcl
```

---

## Practice Exercises

### Exercise 1: Full Cycle (Repeat 3 times)
1. `terraform init`
2. `terraform plan`
3. `terraform apply`
4. Verify in AWS Console
5. `terraform destroy`

**Goal**: Build muscle memory for the workflow

### Exercise 2: Modify Resources
1. Change `retention_days` in CloudWatch module to 14
2. Run `terraform plan` (see the change)
3. Run `terraform apply`
4. Verify in AWS Console

**Goal**: Understand update operations

### Exercise 3: Add New Module
1. Create a new module (e.g., `sqs-practice`)
2. Add it to `main.tf`
3. Run `terraform init` (initialize new module)
4. Run `terraform apply`

**Goal**: Practice module creation

### Exercise 4: Import Practice
1. Create a resource manually in AWS Console (e.g., S3 bucket)
2. Write Terraform config for it
3. Import it: `terraform import module.name.resource.this <resource-id>`
4. Run `terraform plan` (should show no changes)

**Goal**: Master import workflow

---

## Troubleshooting

### Error: "Bucket already exists"
**Solution**: S3 bucket names are globally unique. Change `bucket_prefix` in `terraform.tfvars`

### Error: "Role does not exist"
**Solution**: Update `lambda_role_arn` in `terraform.tfvars` with your actual IAM role ARN

### Error: "Region not found"
**Solution**: Verify `aws_region` in `terraform.tfvars` matches your AWS CLI configuration

### State File Locked
**Solution**: 
```powershell
# Force unlock (use with caution)
terraform force-unlock <lock-id>
```

### Resources Not Destroyed
**Solution**:
```powershell
# Manually delete in AWS Console, then remove from state
terraform state rm <resource-address>
```

---

## Next Steps

After mastering this mini project:

1. **Add Complexity**: Add API Gateway, CloudFront modules
2. **Practice Imports**: Import your Shopping system resources
3. **Create Custom Modules**: Build modules for your specific needs
4. **Apply to Production**: Use learnings on main platform

## Estimated Time
- **First run**: 60-90 minutes (reading + implementation)
- **Subsequent runs**: 15-20 minutes
- **Teardown**: 2-3 minutes

## Cost
**$0.00** - All resources within AWS free tier, destroyed immediately after practice
