# Terraform Quick Reference Cheat Sheet

## Essential Commands

### Initialization & Setup
```powershell
terraform init              # Initialize working directory
terraform init -upgrade     # Upgrade providers
terraform validate          # Validate configuration syntax
terraform fmt              # Format code
terraform fmt -recursive   # Format all files in subdirectories
```

### Planning & Applying
```powershell
terraform plan                    # Preview changes
terraform plan -out=plan.tfplan  # Save plan to file
terraform apply                   # Apply changes
terraform apply plan.tfplan      # Apply saved plan
terraform apply -auto-approve    # Skip confirmation
terraform destroy                # Destroy all resources
terraform destroy -auto-approve  # Skip confirmation
```

### State Management
```powershell
terraform state list                              # List all resources
terraform state show <resource>                   # Show resource details
terraform state rm <resource>                     # Remove from state
terraform import <resource> <id>                  # Import existing resource
terraform state mv <source> <destination>         # Rename resource
terraform state pull                              # Download remote state
terraform state push                              # Upload state
```

### Workspace Management
```powershell
terraform workspace list        # List workspaces
terraform workspace new <name>  # Create workspace
terraform workspace select <name>  # Switch workspace
terraform workspace delete <name>  # Delete workspace
```

### Output & Variables
```powershell
terraform output                # Show all outputs
terraform output <name>         # Show specific output
terraform console               # Interactive console
```

### Troubleshooting
```powershell
terraform refresh               # Update state from AWS
terraform force-unlock <id>     # Unlock state
terraform taint <resource>      # Mark for recreation
terraform untaint <resource>    # Remove taint
```

---

## File Structure

### Module Structure (3-File Pattern)
```
modules/my-module/
├── variables.tf    # Input variables
├── main.tf         # Resources
└── outputs.tf      # Output values
```

### Environment Structure
```
environments/practice/
├── main.tf           # Main configuration
├── variables.tf      # Variable definitions
├── outputs.tf        # Output definitions
├── terraform.tfvars  # Variable values
└── .terraform/       # Provider plugins (auto-generated)
```

---

## Syntax Quick Reference

### Resource
```hcl
resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-unique-name"
  
  tags = {
    Name = "MyBucket"
  }
}
```

### Module
```hcl
module "s3" {
  source = "../../modules/s3"
  
  bucket_name = "my-bucket"
}
```

### Variable
```hcl
variable "bucket_name" {
  description = "Name of the bucket"
  type        = string
  default     = "default-name"  # Optional
}
```

### Output
```hcl
output "bucket_arn" {
  description = "ARN of the bucket"
  value       = aws_s3_bucket.my_bucket.arn
}
```

### Provider
```hcl
provider "aws" {
  region = "us-east-1"
}
```

### Data Source
```hcl
data "aws_caller_identity" "current" {}

output "account_id" {
  value = data.aws_caller_identity.current.account_id
}
```

---

## Variable Types

```hcl
variable "string_var" {
  type = string
  default = "hello"
}

variable "number_var" {
  type = number
  default = 123
}

variable "bool_var" {
  type = bool
  default = true
}

variable "list_var" {
  type = list(string)
  default = ["a", "b", "c"]
}

variable "map_var" {
  type = map(string)
  default = {
    key1 = "value1"
    key2 = "value2"
  }
}

variable "object_var" {
  type = object({
    name = string
    age  = number
  })
  default = {
    name = "John"
    age  = 30
  }
}
```

---

## Lifecycle Blocks

### Ignore Changes
```hcl
lifecycle {
  ignore_changes = [filename, source_code_hash]
}
```

### Create Before Destroy
```hcl
lifecycle {
  create_before_destroy = true
}
```

### Prevent Destroy
```hcl
lifecycle {
  prevent_destroy = true
}
```

---

## Common Patterns

### Random Suffix
```hcl
resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "this" {
  bucket = "my-bucket-${random_id.suffix.hex}"
}
```

### Conditional Resource
```hcl
resource "aws_cloudwatch_alarm" "this" {
  count = var.create_alarm ? 1 : 0
  # ...
}
```

### Dynamic Block
```hcl
dynamic "tag" {
  for_each = var.tags
  content {
    key   = tag.key
    value = tag.value
  }
}
```

### For Each
```hcl
resource "aws_s3_bucket" "buckets" {
  for_each = toset(var.bucket_names)
  bucket   = each.value
}
```

---

## Import Workflow

```powershell
# 1. Write Terraform config
module "existing_resource" {
  source = "../../modules/my-module"
  # ... configuration
}

# 2. Import existing resource
terraform import module.existing_resource.aws_s3_bucket.this my-bucket-name

# 3. Verify (should show no changes)
terraform plan
```

---

## Common Import Addresses

```powershell
# S3 Bucket
terraform import aws_s3_bucket.this bucket-name

# DynamoDB Table
terraform import aws_dynamodb_table.this table-name

# Lambda Function
terraform import aws_lambda_function.this function-name

# SNS Topic
terraform import aws_sns_topic.this arn:aws:sns:region:account:topic-name

# CloudWatch Log Group
terraform import aws_cloudwatch_log_group.this /aws/lambda/function-name

# Module Resource
terraform import module.my_module.aws_s3_bucket.this bucket-name
```

---

## Debugging

### Enable Detailed Logging
```powershell
$env:TF_LOG="DEBUG"
terraform plan

# Disable
$env:TF_LOG=""
```

### Show Resource Graph
```powershell
terraform graph | Out-File graph.dot
```

### Validate JSON
```powershell
terraform show -json | ConvertFrom-Json
```

---

## Best Practices Checklist

- ✅ Use modules for reusability
- ✅ Use variables for flexibility
- ✅ Use outputs to expose data
- ✅ Tag all resources
- ✅ Use `terraform fmt` before committing
- ✅ Run `terraform validate` before applying
- ✅ Review `terraform plan` carefully
- ✅ Use remote state for teams
- ✅ Never edit state file manually
- ✅ Use `.gitignore` for sensitive files

---

## .gitignore for Terraform

```gitignore
# Terraform files
.terraform/
*.tfstate
*.tfstate.*
*.tfvars
.terraform.lock.hcl

# Crash logs
crash.log

# Ignore override files
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# Ignore CLI configuration
.terraformrc
terraform.rc
```

---

## Useful AWS CLI Commands

```powershell
# List S3 buckets
aws s3 ls

# Describe DynamoDB table
aws dynamodb describe-table --table-name TableName

# List Lambda functions
aws lambda list-functions

# Get Lambda function
aws lambda get-function --function-name FunctionName

# List SNS topics
aws sns list-topics

# Describe CloudWatch log group
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/
```

---

## Practice Workflow

```powershell
# 1. Initialize
cd terraform/environments/practice
terraform init

# 2. Validate
terraform validate

# 3. Format
terraform fmt -recursive

# 4. Plan
terraform plan

# 5. Apply
terraform apply

# 6. Verify
terraform output
aws s3 ls | findstr practice

# 7. Destroy
terraform destroy
```

---

## Common Errors & Solutions

### Error: "Bucket already exists"
**Solution**: Change bucket name (must be globally unique)

### Error: "Resource not found"
**Solution**: Check resource ID in import command

### Error: "State locked"
**Solution**: `terraform force-unlock <lock-id>`

### Error: "Provider not found"
**Solution**: `terraform init`

### Error: "Invalid configuration"
**Solution**: `terraform validate` to see details

---

## Keyboard Shortcuts (VS Code)

- `Ctrl + Space`: Auto-complete
- `Ctrl + Click`: Go to definition
- `F2`: Rename symbol
- `Ctrl + /`: Comment/uncomment
- `Shift + Alt + F`: Format document

---

## Quick Tips

1. **Always run `terraform plan` before `apply`**
2. **Use modules to avoid repetition**
3. **Tag everything for easy identification**
4. **Use `terraform.tfvars` for environment-specific values**
5. **Never commit `.tfstate` files to Git**
6. **Use `ignore_changes` for externally managed attributes**
7. **Import existing resources instead of recreating**
8. **Use `terraform destroy` to clean up practice resources**
9. **Read error messages carefully - they're usually helpful**
10. **Practice in a safe environment first**

---

## Resource Naming Convention

```
<project>-<environment>-<resource-type>-<description>

Examples:
- practice-dev-s3-videos
- myapp-prod-lambda-api
- platform-staging-dynamodb-users
```

---

## Module Versioning

```hcl
module "s3" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "3.0.0"  # Pin to specific version
  
  # ...
}
```

---

## Remote State (S3 Backend)

```hcl
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "practice/terraform.tfstate"
    region = "us-east-1"
  }
}
```

---

## This Cheat Sheet Covers:
- ✅ Essential commands
- ✅ File structure
- ✅ Syntax examples
- ✅ Common patterns
- ✅ Import workflow
- ✅ Debugging tips
- ✅ Best practices
- ✅ Common errors

**Print this and keep it handy while practicing!**
