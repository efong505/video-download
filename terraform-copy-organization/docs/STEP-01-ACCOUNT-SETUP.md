# STEP 01: AWS Account Setup

**Goal**: Configure AWS Organizations and create cross-account access

**Time**: 20-30 minutes (first time), 5 minutes (practice runs)

---

## Overview

You'll set up:
1. AWS Organizations structure (if not already done)
2. Child account (ed@ekewaka)
3. Cross-account IAM role for Terraform
4. Verify access from production account

---

## Prerequisites Check

```powershell
# Verify AWS CLI is configured
aws sts get-caller-identity

# Expected output:
# {
#     "UserId": "...",
#     "Account": "371751795928",
#     "Arn": "arn:aws:iam::371751795928:user/..."
# }

# Verify Terraform is installed
terraform version

# Expected: Terraform v1.0 or higher
```

---

## Step 1.1: Verify AWS Organizations

**Check if Organizations is already set up**:

```powershell
# Check organization status
aws organizations describe-organization
```

**If you get an error** (Organizations not set up):

```powershell
# Create organization
aws organizations create-organization --feature-set ALL

# Expected output:
# {
#     "Organization": {
#         "Id": "o-...",
#         "Arn": "arn:aws:organizations::371751795928:organization/o-...",
#         "MasterAccountId": "371751795928",
#         ...
#     }
# }
```

**If successful**: You'll see organization details. Note the Organization ID.

---

## Step 1.2: Get Child Account ID

**Option A: If child account already exists**:

```powershell
# List all accounts in organization
aws organizations list-accounts

# Look for ed@ekewawa account and note the Account ID
```

**Option B: If you need to create child account**:

```powershell
# Create child account
aws organizations create-account `
    --email ed@ekewaka.com `
    --account-name "Ed-Practice-Account"

# Check creation status
aws organizations describe-create-account-status `
    --create-account-request-id car-...

# Wait for "State": "SUCCEEDED"
# Note the AccountId from the output
```

**Save the child account ID**: You'll need it throughout the tutorial.

**Example**: `123456789012` (replace with your actual child account ID)

---

## Step 1.3: Create Cross-Account IAM Role

**This role allows production account to manage resources in child account.**

### Create Trust Policy File

```powershell
# Create trust policy
@"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::371751795928:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "terraform-copy-tutorial"
        }
      }
    }
  ]
}
"@ | Out-File -FilePath trust-policy.json -Encoding utf8
```

### Create the Role in Child Account

**Important**: You need to switch to the child account to create this role.

**Method 1: Using AWS Console** (Easiest for first time):

1. Log into AWS Console with child account credentials
2. Go to IAM → Roles → Create Role
3. Select "Another AWS account"
4. Enter production account ID: `371751795928`
5. Check "Require external ID"
6. Enter external ID: `terraform-copy-tutorial`
7. Attach policy: `AdministratorAccess` (for tutorial simplicity)
8. Name the role: `TerraformCrossAccountRole`
9. Create role
10. Note the Role ARN: `arn:aws:iam::CHILD_ACCOUNT_ID:role/TerraformCrossAccountRole`

**Method 2: Using AWS CLI** (if you have child account credentials configured):

```powershell
# Switch to child account profile (if configured)
$env:AWS_PROFILE = "child-account"

# Create the role
aws iam create-role `
    --role-name TerraformCrossAccountRole `
    --assume-role-policy-document file://trust-policy.json

# Attach administrator policy (for tutorial)
aws iam attach-role-policy `
    --role-name TerraformCrossAccountRole `
    --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Get role ARN
aws iam get-role --role-name TerraformCrossAccountRole

# Switch back to production account
$env:AWS_PROFILE = "default"
```

---

## Step 1.4: Test Cross-Account Access

**Verify you can assume the role from production account**:

```powershell
# Assume role in child account
aws sts assume-role `
    --role-arn "arn:aws:iam::CHILD_ACCOUNT_ID:role/TerraformCrossAccountRole" `
    --role-session-name "terraform-test" `
    --external-id "terraform-copy-tutorial"

# Expected output: Credentials with AccessKeyId, SecretAccessKey, SessionToken
```

**If successful**: You'll see temporary credentials. This confirms cross-account access works!

**If error**: Check that:
- Role ARN is correct
- External ID matches
- Trust policy is correct
- You're using production account credentials

---

## Step 1.5: Save Configuration

**Create a configuration file for easy reference**:

```powershell
@"
# AWS Account Configuration
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

PRODUCTION_ACCOUNT_ID=371751795928
CHILD_ACCOUNT_ID=REPLACE_WITH_YOUR_CHILD_ACCOUNT_ID
CROSS_ACCOUNT_ROLE_ARN=arn:aws:iam::REPLACE_WITH_YOUR_CHILD_ACCOUNT_ID:role/TerraformCrossAccountRole
EXTERNAL_ID=terraform-copy-tutorial
AWS_REGION=us-east-1
"@ | Out-File -FilePath account-config.txt -Encoding utf8

Write-Host "✅ Configuration saved to account-config.txt"
Write-Host "⚠️  IMPORTANT: Replace CHILD_ACCOUNT_ID with your actual child account ID"
```

---

## Step 1.6: Verification Checklist

Before proceeding, verify:

- [ ] AWS Organizations is set up
- [ ] Child account exists and you have the Account ID
- [ ] Cross-account IAM role created in child account
- [ ] Role has AdministratorAccess policy attached
- [ ] Trust policy allows production account to assume role
- [ ] External ID is set to `terraform-copy-tutorial`
- [ ] You can successfully assume the role from production account
- [ ] Configuration saved in `account-config.txt`

---

## Troubleshooting

### Error: "AccessDenied when calling AssumeRole"

**Cause**: Trust policy doesn't allow production account

**Fix**: Verify trust policy in child account role:
```json
{
  "Principal": {
    "AWS": "arn:aws:iam::371751795928:root"
  }
}
```

### Error: "ExternalId mismatch"

**Cause**: External ID doesn't match

**Fix**: Ensure external ID is exactly `terraform-copy-tutorial` in both trust policy and assume-role command

### Error: "Role not found"

**Cause**: Role doesn't exist in child account

**Fix**: Create role in child account (not production account)

---

## Quick Reference

**Production Account**: 371751795928
**Child Account**: [Your child account ID]
**Role Name**: TerraformCrossAccountRole
**External ID**: terraform-copy-tutorial
**Region**: us-east-1

---

## Next Step

✅ **Account setup complete!**

→ Continue to `STEP-02-IAM-ROLES.md` to configure IAM permissions for infrastructure resources.

---

## Practice Tips

**For subsequent practice runs**:
1. Role already exists - skip creation
2. Just verify assume-role works
3. Update `account-config.txt` if needed
4. Takes ~2 minutes instead of 20-30

**To reset**: Delete role in child account and recreate (optional)
