# Terraform Concepts Explained

## Table of Contents
1. [What is Terraform?](#what-is-terraform)
2. [Core Concepts](#core-concepts)
3. [Module Pattern](#module-pattern)
4. [State Management](#state-management)
5. [Lifecycle Management](#lifecycle-management)
6. [Best Practices](#best-practices)

---

## What is Terraform?

**Terraform** is Infrastructure as Code (IaC) - you write code to define your AWS resources, and Terraform creates/updates/destroys them automatically.

### Why Use Terraform?

**Without Terraform** (Manual AWS Console):
- ❌ Click through 50+ screens to create resources
- ❌ Forget what you created
- ❌ Can't recreate if deleted
- ❌ No version control
- ❌ Takes 12 hours to rebuild

**With Terraform**:
- ✅ Write code once, deploy anywhere
- ✅ Version control with Git
- ✅ Recreate in 15 minutes
- ✅ Document infrastructure
- ✅ Prevent configuration drift

---

## Core Concepts

### 1. Resources
**What**: Individual AWS components (S3 bucket, Lambda function, etc.)

**Example**:
```hcl
resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-unique-bucket-name"
}
```

**Breakdown**:
- `resource`: Terraform keyword
- `"aws_s3_bucket"`: Resource type (from AWS provider)
- `"my_bucket"`: Local name (how you reference it)
- `bucket = "..."`: Configuration

### 2. Modules
**What**: Reusable groups of resources (like functions in programming)

**Why**: Don't repeat yourself (DRY principle)

**Example**:
```hcl
# Instead of copying S3 config 10 times...
module "s3_videos" {
  source = "../../modules/s3"
  bucket_name = "videos"
}

module "s3_images" {
  source = "../../modules/s3"
  bucket_name = "images"
}
```

### 3. Variables
**What**: Inputs to modules (like function parameters)

**Example**:
```hcl
variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "my-bucket"  # Optional
}
```

**Types**:
- `string`: Text ("hello")
- `number`: Integer (123)
- `bool`: True/false
- `list`: Array (["a", "b", "c"])
- `map`: Key-value pairs ({key = "value"})

### 4. Outputs
**What**: Return values from modules (like function return values)

**Example**:
```hcl
output "bucket_name" {
  value = aws_s3_bucket.this.bucket
}
```

**Usage**: Access in parent with `module.s3_practice.bucket_name`

### 5. Providers
**What**: Plugins that talk to AWS/Azure/GCP

**Example**:
```hcl
provider "aws" {
  region = "us-east-1"
}
```

### 6. State
**What**: Terraform's memory of what exists in AWS

**File**: `terraform.tfstate` (JSON file)

**Critical**: Never edit manually, never delete

---

## Module Pattern

### The 3-File Pattern

Every module has 3 files:

#### 1. variables.tf (Inputs)
```hcl
variable "bucket_name" {
  description = "Name of bucket"
  type        = string
}
```
**Think**: Function parameters

#### 2. main.tf (Logic)
```hcl
resource "aws_s3_bucket" "this" {
  bucket = var.bucket_name
}
```
**Think**: Function body

#### 3. outputs.tf (Return Values)
```hcl
output "bucket_arn" {
  value = aws_s3_bucket.this.arn
}
```
**Think**: Function return statement

### Module Structure
```
modules/
└── s3-practice/
    ├── variables.tf   # Inputs
    ├── main.tf        # Resources
    └── outputs.tf     # Outputs
```

### Calling a Module
```hcl
module "my_s3" {
  source = "../../modules/s3-practice"
  
  # Pass variables
  bucket_name = "my-bucket"
}

# Access outputs
output "bucket" {
  value = module.my_s3.bucket_arn
}
```

---

## State Management

### What is State?

Terraform tracks what exists in AWS using a **state file** (`terraform.tfstate`).

**State File Contains**:
- Resource IDs
- Resource attributes
- Dependencies between resources
- Metadata

### State Commands

#### View State
```powershell
# List all resources
terraform state list

# Show specific resource
terraform state show module.s3_practice.aws_s3_bucket.this
```

#### Remove from State
```powershell
# Terraform "forgets" resource (but it still exists in AWS)
terraform state rm module.s3_practice.aws_s3_bucket.this
```

#### Import into State
```powershell
# Terraform "remembers" existing AWS resource
terraform import module.s3_practice.aws_s3_bucket.this my-bucket-name
```

### State Workflow

```
1. terraform plan
   ↓
   Compares: Code vs State vs AWS
   ↓
2. terraform apply
   ↓
   Updates: AWS + State file
   ↓
3. State file now matches AWS
```

### State Best Practices

✅ **DO**:
- Commit `.tf` files to Git
- Use remote state (S3 backend) for teams
- Use `terraform state` commands carefully

❌ **DON'T**:
- Edit `terraform.tfstate` manually
- Delete state file
- Commit state file to Git (contains secrets)

---

## Lifecycle Management

### The Terraform Workflow

```
terraform init     # Download providers, initialize modules
    ↓
terraform validate # Check syntax
    ↓
terraform plan     # Preview changes
    ↓
terraform apply    # Create/update resources
    ↓
terraform destroy  # Delete everything
```

### Lifecycle Hooks

Control how Terraform manages resources:

#### ignore_changes
**Use**: When you manage something outside Terraform

```hcl
resource "aws_lambda_function" "this" {
  filename = "placeholder.zip"
  
  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}
```

**Why**: Lambda code deployed separately (not via Terraform)

#### create_before_destroy
**Use**: Zero-downtime updates

```hcl
resource "aws_instance" "web" {
  ami = "ami-12345"
  
  lifecycle {
    create_before_destroy = true
  }
}
```

**Why**: Creates new instance before destroying old one

#### prevent_destroy
**Use**: Protect critical resources

```hcl
resource "aws_s3_bucket" "important" {
  bucket = "critical-data"
  
  lifecycle {
    prevent_destroy = true
  }
}
```

**Why**: Terraform will error if you try to destroy

---

## Best Practices

### 1. Module Organization

```
terraform/
├── modules/           # Reusable components
│   ├── s3/
│   ├── lambda/
│   └── dynamodb/
└── environments/      # Deployments
    ├── prod/
    ├── staging/
    └── dev/
```

### 2. Naming Conventions

**Resources**: Use `this` for single-resource modules
```hcl
resource "aws_s3_bucket" "this" {
  # ...
}
```

**Modules**: Descriptive names
```hcl
module "s3_videos" {
  # ...
}
```

**Variables**: Descriptive, snake_case
```hcl
variable "bucket_name" {
  # ...
}
```

### 3. Variable Defaults

**Required variables**: No default
```hcl
variable "bucket_name" {
  type = string
  # No default = required
}
```

**Optional variables**: Provide default
```hcl
variable "environment" {
  type    = string
  default = "dev"
}
```

### 4. Tagging Strategy

**Always tag resources**:
```hcl
tags = {
  Name        = "my-resource"
  Environment = "production"
  ManagedBy   = "Terraform"
  Project     = "MyProject"
}
```

**Use default_tags** (applies to all resources):
```hcl
provider "aws" {
  default_tags {
    tags = {
      ManagedBy = "Terraform"
      Project   = "MyProject"
    }
  }
}
```

### 5. Placeholder Pattern (Lambda)

**Problem**: Terraform needs a ZIP file, but code is deployed separately

**Solution**: Use placeholder.zip + ignore_changes

```hcl
resource "aws_lambda_function" "this" {
  filename = "${path.module}/placeholder.zip"
  
  lifecycle {
    ignore_changes = [filename, source_code_hash]
  }
}
```

**Workflow**:
1. Terraform creates Lambda with placeholder
2. Deployment script updates Lambda code
3. Terraform ignores code changes

### 6. Import Existing Resources

**When**: You created resources manually, now want Terraform to manage them

**Steps**:
1. Write Terraform config matching existing resource
2. Import: `terraform import <address> <id>`
3. Verify: `terraform plan` (should show no changes)

**Example**:
```powershell
# 1. Write config
module "existing_bucket" {
  source = "../../modules/s3"
  bucket_name = "my-existing-bucket"
}

# 2. Import
terraform import module.existing_bucket.aws_s3_bucket.this my-existing-bucket

# 3. Verify
terraform plan  # Should show: No changes
```

### 7. Separate Infrastructure from Code

**Infrastructure** (Terraform):
- S3 buckets
- DynamoDB tables
- Lambda functions (shell)
- API Gateway

**Code** (Deployment scripts):
- Lambda function code
- Static website files
- Application logic

**Why**: Infrastructure changes rarely, code changes frequently

---

## Common Patterns

### Pattern 1: Random Suffix for Unique Names

**Problem**: S3 bucket names must be globally unique

**Solution**: Use random_id
```hcl
resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_s3_bucket" "this" {
  bucket = "my-bucket-${random_id.suffix.hex}"
}
```

### Pattern 2: Conditional Resources

**Problem**: Only create resource in production

**Solution**: Use count
```hcl
resource "aws_cloudwatch_alarm" "this" {
  count = var.environment == "prod" ? 1 : 0
  # ...
}
```

### Pattern 3: Dynamic Blocks

**Problem**: Variable number of sub-resources

**Solution**: Use dynamic blocks
```hcl
resource "aws_dynamodb_table" "this" {
  # ...
  
  dynamic "global_secondary_index" {
    for_each = var.global_secondary_indexes
    content {
      name            = global_secondary_index.value.name
      hash_key        = global_secondary_index.value.hash_key
      projection_type = global_secondary_index.value.projection_type
    }
  }
}
```

---

## Terraform vs AWS Console

| Task | AWS Console | Terraform |
|------|-------------|-----------|
| Create S3 bucket | 5 minutes, 10 clicks | 3 lines of code |
| Recreate if deleted | 5 minutes, 10 clicks | `terraform apply` (30 seconds) |
| Document setup | Screenshots? | Code is documentation |
| Version control | ❌ | ✅ Git |
| Disaster recovery | 12 hours | 15 minutes |
| Team collaboration | Hard | Easy (code review) |

---

## Key Takeaways

1. **Terraform = Infrastructure as Code**: Write code, not click buttons
2. **Modules = Reusable Components**: Write once, use many times
3. **State = Terraform's Memory**: Never edit manually
4. **Import = Adopt Existing Resources**: Bring manual resources under Terraform
5. **Lifecycle = Control Updates**: ignore_changes, create_before_destroy, etc.
6. **Separate Infrastructure from Code**: Terraform for structure, scripts for content

---

## Learning Path

1. ✅ Understand concepts (this document)
2. ✅ Follow tutorial (TUTORIAL.md)
3. ✅ Practice full cycle 3-5 times
4. ✅ Experiment with modifications
5. ✅ Apply to real projects

---

## Additional Resources

- [Terraform Documentation](https://www.terraform.io/docs)
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
