# IAM Roles - Detailed Implementation Guide

## Overview
Step-by-step guide for creating the IAM role module and importing the Lambda execution role with 9 managed policies.

---

## Step 1: Gather Existing IAM Role Information

### Commands to List IAM Roles

```bash
# List all IAM roles
aws iam list-roles --query 'Roles[*].[RoleName,Arn]' --output table

# Get specific role details
aws iam get-role --role-name lambda-execution-role

# List attached managed policies
aws iam list-attached-role-policies --role-name lambda-execution-role

# Get role trust policy (assume role policy)
aws iam get-role --role-name lambda-execution-role --query 'Role.AssumeRolePolicyDocument'

# List inline policies (if any)
aws iam list-role-policies --role-name lambda-execution-role
```

### Data Collected

**Role Name**: lambda-execution-role

**Role ARN**: arn:aws:iam::371751795928:role/lambda-execution-role

**Trust Policy** (Assume Role Policy):
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

**Attached Managed Policies** (9 total):
```
1. arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
2. arn:aws:iam::aws:policy/AmazonS3FullAccess
3. arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
4. arn:aws:iam::aws:policy/AmazonSESFullAccess
5. arn:aws:iam::aws:policy/AmazonSNSFullAccess
6. arn:aws:iam::aws:policy/AmazonBedrockFullAccess
7. arn:aws:iam::aws:policy/AWSLambda_FullAccess
8. arn:aws:iam::aws:policy/AmazonSQSFullAccess
9. arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

---

## Step 2: Design IAM Module Strategy

### Key Decision: IAM Users vs IAM Roles

**Question**: Should we add IAM users to Terraform?

**Answer**: NO

**Reason**: Bootstrap problem
- Need AWS credentials to run Terraform
- If IAM user is in Terraform, deleting it breaks Terraform
- Root user serves as emergency access
- IAM users are intentionally excluded

### IAM Role Strategy

**What to manage**:
- Lambda execution role
- Future: EC2 instance roles, ECS task roles

**What NOT to manage**:
- IAM users (bootstrap problem)
- Root account (can't be managed by Terraform)

---

## Step 3: Create IAM Role Module

### Directory Setup
```bash
mkdir -p terraform/modules/iam-role
cd terraform/modules/iam-role
```

### Create main.tf

**File**: `terraform/modules/iam-role/main.tf`

```hcl
# IAM Role
resource "aws_iam_role" "this" {
  name               = var.role_name
  assume_role_policy = var.assume_role_policy
  description        = var.description

  tags = var.tags

  lifecycle {
    prevent_destroy = true
  }
}

# Attach Managed Policies
resource "aws_iam_role_policy_attachment" "managed" {
  for_each = toset(var.managed_policy_arns)

  role       = aws_iam_role.this.name
  policy_arn = each.value
}
```

**Data Source**: 
- Role configuration from `aws iam get-role`
- Managed policies from `aws iam list-attached-role-policies`
- `for_each` pattern for multiple policy attachments

### Create variables.tf

**File**: `terraform/modules/iam-role/variables.tf`

```hcl
variable "role_name" {
  description = "Name of the IAM role"
  type        = string
}

variable "assume_role_policy" {
  description = "Assume role policy (trust policy) JSON"
  type        = string
}

variable "description" {
  description = "Description of the IAM role"
  type        = string
  default     = ""
}

variable "managed_policy_arns" {
  description = "List of managed policy ARNs to attach"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Tags to apply to the role"
  type        = map(string)
  default     = {}
}
```

### Create outputs.tf

**File**: `terraform/modules/iam-role/outputs.tf`

```hcl
output "role_name" {
  description = "Name of the IAM role"
  value       = aws_iam_role.this.name
}

output "role_arn" {
  description = "ARN of the IAM role"
  value       = aws_iam_role.this.arn
}

output "role_id" {
  description = "ID of the IAM role"
  value       = aws_iam_role.this.id
}
```

---

## Step 4: Use Module in Production Environment

### Add to main.tf

**File**: `terraform/environments/prod/main.tf`

```hcl
# Lambda Execution Role
module "iam_lambda_execution" {
  source = "../../modules/iam-role"

  role_name   = "lambda-execution-role"
  description = "Execution role for Lambda functions"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
    "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
    "arn:aws:iam::aws:policy/AmazonSESFullAccess",
    "arn:aws:iam::aws:policy/AmazonSNSFullAccess",
    "arn:aws:iam::aws:policy/AmazonBedrockFullAccess",
    "arn:aws:iam::aws:policy/AWSLambda_FullAccess",
    "arn:aws:iam::aws:policy/AmazonSQSFullAccess",
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  ]

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}
```

**Data Source**: Values from Step 1 AWS CLI output

---

## Step 5: Import IAM Role

### Initialize Terraform
```bash
cd terraform/environments/prod
terraform init
```

### Import IAM Role
```bash
terraform import module.iam_lambda_execution.aws_iam_role.this lambda-execution-role
```

**Output**:
```
module.iam_lambda_execution.aws_iam_role.this: Importing from ID "lambda-execution-role"...
module.iam_lambda_execution.aws_iam_role.this: Import complete!
```

### Import Managed Policy Attachments

Each policy attachment must be imported separately using the format: `role-name/policy-arn`

```bash
# Import DynamoDB policy
terraform import 'module.iam_lambda_execution.aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"]' lambda-execution-role/arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

# Import S3 policy
terraform import 'module.iam_lambda_execution.aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/AmazonS3FullAccess"]' lambda-execution-role/arn:aws:iam::aws:policy/AmazonS3FullAccess

# Import CloudWatch Logs policy
terraform import 'module.iam_lambda_execution.aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"]' lambda-execution-role/arn:aws:iam::aws:policy/CloudWatchLogsFullAccess

# Import SES policy
terraform import 'module.iam_lambda_execution.aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/AmazonSESFullAccess"]' lambda-execution-role/arn:aws:iam::aws:policy/AmazonSESFullAccess

# Import SNS policy
terraform import 'module.iam_lambda_execution.aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/AmazonSNSFullAccess"]' lambda-execution-role/arn:aws:iam::aws:policy/AmazonSNSFullAccess

# Import Bedrock policy
terraform import 'module.iam_lambda_execution.aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/AmazonBedrockFullAccess"]' lambda-execution-role/arn:aws:iam::aws:policy/AmazonBedrockFullAccess

# Import Lambda policy
terraform import 'module.iam_lambda_execution.aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/AWSLambda_FullAccess"]' lambda-execution-role/arn:aws:iam::aws:policy/AWSLambda_FullAccess

# Import SQS policy
terraform import 'module.iam_lambda_execution.aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/AmazonSQSFullAccess"]' lambda-execution-role/arn:aws:iam::aws:policy/AmazonSQSFullAccess

# Import Lambda Basic Execution policy
terraform import 'module.iam_lambda_execution.aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]' lambda-execution-role/arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

**Note**: The quotes and brackets are required for the `for_each` resource addressing.

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

### Issue 1: Missing Policy Attachment
```
# Plan shows:
+ aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/NewPolicy"]

# Solution: Import the missing policy attachment
terraform import 'module.iam_lambda_execution.aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/NewPolicy"]' lambda-execution-role/arn:aws:iam::aws:policy/NewPolicy
```

### Issue 2: Extra Policy in Terraform
```
# Plan shows:
- aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/OldPolicy"]

# Solution: Remove policy from managed_policy_arns list in main.tf
```

### Issue 3: Trust Policy Mismatch
```
# Plan shows:
~ assume_role_policy = jsonencode(...)

# Solution: Get exact trust policy from AWS
aws iam get-role --role-name lambda-execution-role --query 'Role.AssumeRolePolicyDocument'

# Update main.tf to match exactly
```

---

## Step 7: Test Terraform Control

### Add a New Managed Policy
```hcl
managed_policy_arns = [
  "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
  "arn:aws:iam::aws:policy/AmazonS3FullAccess",
  # ... existing policies ...
  "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"  # NEW
]
```

### Apply Change
```bash
terraform apply
```

**Output**:
```
Terraform will perform the following actions:

  # module.iam_lambda_execution.aws_iam_role_policy_attachment.managed["arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"] will be created
  + resource "aws_iam_role_policy_attachment" "managed" {
      + policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
      + role       = "lambda-execution-role"
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```

### Verify in AWS
```bash
aws iam list-attached-role-policies --role-name lambda-execution-role
```

**Output**: Should include AmazonEC2ReadOnlyAccess

### Remove Test Policy
```hcl
# Remove AmazonEC2ReadOnlyAccess from list
```

```bash
terraform apply
```

---

## Step 8: Understand IAM Best Practices

### Least Privilege Principle

**Current State**: Using AWS managed "FullAccess" policies

**Why?**: 
- Rapid development phase
- Multiple services accessed by Lambda functions
- Easier to manage during prototyping

**Future Improvement**:
- Create custom policies with minimal permissions
- Use IAM Access Analyzer to identify unused permissions
- Implement least privilege access

### Example: Custom Policy (Future)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:371751795928:table/articles"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::my-video-downloads-bucket/*"
    }
  ]
}
```

---

## Key Learnings

### IAM Role vs IAM User
- **Role**: Assumed by services (Lambda, EC2), temporary credentials
- **User**: Long-term credentials, used by people or applications
- **Best Practice**: Use roles for AWS services, users for people

### Managed Policies vs Inline Policies
- **Managed**: Reusable, versioned, can attach to multiple roles
- **Inline**: Embedded in role, deleted with role
- **Best Practice**: Use managed policies for reusability

### Trust Policy (Assume Role Policy)
- **Purpose**: Defines who can assume the role
- **Lambda**: Service principal is `lambda.amazonaws.com`
- **Cross-Account**: Can allow other AWS accounts to assume role

### for_each Pattern
- **Purpose**: Create multiple similar resources
- **Benefit**: Each resource has unique address in state
- **Import**: Must import each resource individually

---

## Common Pitfalls

**Pitfall 1: Forgetting to import policy attachments**
- **Problem**: Terraform wants to create attachments that already exist
- **Solution**: Import each policy attachment separately

**Pitfall 2: Wrong import format for for_each**
- **Problem**: Import fails with "resource not found"
- **Solution**: Use quotes and brackets: `'resource["key"]'`

**Pitfall 3: Trust policy formatting**
- **Problem**: Terraform shows policy change even though it matches
- **Solution**: Use `jsonencode()` for consistent formatting

**Pitfall 4: Adding IAM users to Terraform**
- **Problem**: Bootstrap problem - can't run Terraform without credentials
- **Solution**: Don't manage IAM users in Terraform

---

## Troubleshooting

### Issue: Import fails with "role not found"
**Solution**: Verify role name with `aws iam get-role --role-name lambda-execution-role`

### Issue: Policy attachment import fails
**Solution**: Check format: `role-name/policy-arn` with quotes and brackets

### Issue: Plan shows trust policy change
**Solution**: Use `jsonencode()` and ensure exact JSON structure match

### Issue: Can't delete role
**Solution**: Remove `prevent_destroy` lifecycle rule first (intentional protection)

---

## Disaster Recovery Consideration

### Why IAM Users Aren't in Terraform

**Scenario**: Complete AWS account disaster

**Recovery Process**:
1. Use root user to create new IAM user
2. Configure AWS CLI with new credentials
3. Run `terraform apply` to recreate infrastructure
4. Infrastructure restored in 15-20 minutes

**If IAM user was in Terraform**:
1. Use root user to create new IAM user
2. Configure AWS CLI with new credentials
3. Run `terraform apply`
4. Terraform tries to create IAM user that already exists
5. Manual intervention required to import or delete user
6. Adds complexity to disaster recovery

**Conclusion**: Root user serves as bootstrap mechanism for disaster recovery.

---

## Related Files
- [IAM Role Module](../../modules/iam-role/main.tf)
- [Production Environment](../prod/main.tf)
- [Terraform Documentation](../TERRAFORM_DOCUMENTATION.md)

---

**Created**: February 10, 2026  
**Last Updated**: February 10, 2026
