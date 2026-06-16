# STEP 02: IAM Roles and Policies

**Goal**: Create IAM roles and policies that will be used by Lambda and other services

**Time**: 10-15 minutes

---

## Overview

You'll create:
1. Lambda execution role (similar to production)
2. Attach necessary policies
3. Verify role is ready for use

**Note**: This step creates the IAM role that Lambda will use. The cross-account role from Step 1 is what Terraform uses to create resources.

---

## Step 2.1: Understand the Role Structure

**Two different roles**:

1. **TerraformCrossAccountRole** (Step 1)
   - Used BY: Terraform
   - Purpose: Create resources in child account
   - Location: Child account

2. **lambda-execution-role-tutorial** (This step)
   - Used BY: Lambda functions
   - Purpose: Execute Lambda code, access AWS services
   - Location: Child account (created by Terraform)

---

## Step 2.2: Review Lambda Execution Role

**This role will be created by Terraform, but let's understand it first.**

### Trust Policy (Who can use this role)

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

**Meaning**: Only Lambda service can assume this role.

### Permissions (What this role can do)

**Policies to attach**:
1. `AWSLambdaBasicExecutionRole` - CloudWatch Logs
2. `AmazonDynamoDBFullAccess` - DynamoDB operations
3. `AmazonS3FullAccess` - S3 operations
4. `AmazonSNSFullAccess` - SNS notifications

**Note**: In production, you have 9 policies. For tutorial, we'll use 4 essential ones.

---

## Step 2.3: Verify Terraform Will Create Role

**The role will be created automatically by Terraform. Let's preview the configuration.**

**File**: `terraform/main.tf` (we'll create this in Step 3)

```hcl
# Lambda execution role
resource "aws_iam_role" "lambda_execution" {
  provider = aws.child
  name     = "lambda-execution-role-tutorial"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  tags = {
    Environment = "Tutorial"
    ManagedBy   = "Terraform"
  }
}

# Attach policies
resource "aws_iam_role_policy_attachment" "lambda_basic" {
  provider   = aws.child
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb" {
  provider   = aws.child
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_s3" {
  provider   = aws.child
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "lambda_sns" {
  provider   = aws.child
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
}
```

---

## Step 2.4: Compare with Production

**Your production role** (`lambda-execution-role`):
- 9 managed policies
- Used by 18 Lambda functions
- Full access to multiple services

**Tutorial role** (`lambda-execution-role-tutorial`):
- 4 managed policies (essential subset)
- Used by 1 sample Lambda function
- Simplified for learning

**Key Difference**: Tutorial uses fewer policies to keep it simple, but follows same pattern.

---

## Step 2.5: Understanding Policy Attachments

### Why Separate Resources?

```hcl
# ❌ Don't do this (inline policy)
resource "aws_iam_role" "lambda" {
  name = "lambda-role"
  # inline_policy = ... (hard to manage)
}

# ✅ Do this (managed policy attachments)
resource "aws_iam_role" "lambda" {
  name = "lambda-role"
}

resource "aws_iam_role_policy_attachment" "policy1" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/..."
}
```

**Benefits**:
- Easy to add/remove policies
- Clear separation of concerns
- Matches production pattern
- Easier to audit

---

## Step 2.6: Verification Checklist

Before proceeding, understand:

- [ ] Difference between Terraform role and Lambda execution role
- [ ] Lambda execution role will be created by Terraform
- [ ] Role allows Lambda service to assume it
- [ ] Four managed policies will be attached
- [ ] Role follows production pattern (simplified)
- [ ] Role will be created in child account

---

## Step 2.7: Manual Verification (Optional)

**If you want to verify the role after Terraform creates it**:

```powershell
# After running terraform apply (in Step 4), verify role exists
aws iam get-role `
    --role-name lambda-execution-role-tutorial `
    --profile child-account

# List attached policies
aws iam list-attached-role-policies `
    --role-name lambda-execution-role-tutorial `
    --profile child-account

# Expected: 4 policies attached
```

---

## Key Concepts

### 1. Trust Policies vs Permission Policies

**Trust Policy** (Who can use the role):
```json
{
  "Principal": {
    "Service": "lambda.amazonaws.com"
  }
}
```

**Permission Policy** (What the role can do):
```json
{
  "Action": "dynamodb:*",
  "Resource": "*"
}
```

### 2. Managed vs Inline Policies

**Managed Policies**:
- ✅ Reusable across roles
- ✅ AWS-managed or customer-managed
- ✅ Easy to update
- ✅ Used in production

**Inline Policies**:
- ❌ Embedded in role
- ❌ Not reusable
- ❌ Harder to manage
- ❌ Avoid for this tutorial

### 3. Least Privilege Principle

**Production**: Each Lambda should have only the permissions it needs

**Tutorial**: Using full access policies for simplicity, but in production you'd restrict:
```hcl
# Production example (more restrictive)
policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess"

# Tutorial (simpler)
policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
```

---

## Troubleshooting

### Error: "Role already exists"

**Cause**: Role name conflicts with existing role

**Fix**: Use unique name like `lambda-execution-role-tutorial-v2`

### Error: "Cannot attach policy"

**Cause**: Policy ARN is incorrect

**Fix**: Verify policy ARN:
```powershell
aws iam list-policies --scope AWS | Select-String "AWSLambdaBasicExecutionRole"
```

### Error: "Access denied"

**Cause**: Terraform cross-account role doesn't have IAM permissions

**Fix**: Ensure TerraformCrossAccountRole has AdministratorAccess

---

## Quick Reference

**Role Name**: `lambda-execution-role-tutorial`
**Trust Principal**: `lambda.amazonaws.com`
**Policies**: 4 managed policies
**Created By**: Terraform (not manually)
**Location**: Child account

---

## Next Step

✅ **IAM role understanding complete!**

→ Continue to `STEP-03-TERRAFORM-CONFIG.md` to configure Terraform for multi-account deployment.

---

## Practice Tips

**For subsequent practice runs**:
1. This step is mostly conceptual
2. Terraform handles role creation automatically
3. Focus on understanding trust vs permission policies
4. Review production role for comparison
5. Takes ~2 minutes to review
