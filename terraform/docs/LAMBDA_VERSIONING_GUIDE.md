# Lambda Versioning + Blue/Green Deployments - Implementation Guide

## Overview
Implementation guide for Phase 9 Part 2: Lambda versioning with aliases for zero-downtime blue/green deployments.

**Status**: 🔄 IN PROGRESS  
**Started**: January 2025  
**Estimated Duration**: 2-3 hours

---

## What is Lambda Versioning?

### Versions
- **Immutable snapshots** of Lambda function code + configuration
- Each publish creates a new version number (1, 2, 3, etc.)
- $LATEST always points to unpublished changes
- Cannot modify or delete published versions

### Aliases
- **Mutable pointers** to specific Lambda versions
- Example: "live" alias → version 5
- Can update alias to point to different version instantly
- Supports weighted routing (10% v6, 90% v5)

### Blue/Green Deployment Flow
```
1. Deploy new code → creates version 6
2. Test version 6 directly
3. Update "live" alias: v5 → v6 (instant cutover)
4. If issues: Update "live" alias: v6 → v5 (instant rollback)
```

---

## Implementation Steps

### Step 1: Update Lambda Module ✅

Added to `terraform/modules/lambda/main.tf`:
- `publish = true` - Creates new version on each deployment
- `aws_lambda_alias` resource - Creates "live" alias
- `ignore_changes = [function_version]` - Prevents Terraform from managing version updates

### Step 2: Test with Single Function ✅

Updated `auth-api` Lambda:
```hcl
module "lambda_auth_api" {
  publish      = true
  create_alias = true
  alias_name   = "live"
}
```

### Step 3: Deploy Real Code FIRST ⚠️

**CRITICAL**: Before running terraform apply, deploy actual Lambda code:

```bash
cd Downloader/auth_api
zip -r function.zip index.py
aws lambda update-function-code \
  --function-name auth-api \
  --zip-file fileb://function.zip
```

**Why?** Terraform uses placeholder.zip with ignore_changes. When you enable publish=true, it will publish whatever code is currently in the Lambda. If you skip this step, version 1 will be empty placeholder code.

### Step 4: Apply Terraform Changes

```bash
cd terraform/environments/prod
terraform init
terraform plan
terraform apply
```

**Expected Output**:
- Lambda function updated with `publish = true`
- New alias "live" created pointing to current version
- No downtime (existing function continues working)

### Step 5: Verify Alias

```bash
# Check alias
aws lambda get-alias --function-name auth-api --name live

# Expected output:
{
    "AliasArn": "arn:aws:lambda:us-east-1:371751795928:function:auth-api:live",
    "Name": "live",
    "FunctionVersion": "1",
    "Description": ""
}
```

### Step 6: Test Blue/Green Deployment

**Deploy new code**:
```bash
cd Downloader/auth_api
zip -r function.zip index.py
aws lambda update-function-code \
  --function-name auth-api \
  --zip-file fileb://function.zip \
  --publish
```

**Output**: Creates version 2

**Update alias to new version**:
```bash
aws lambda update-alias \
  --function-name auth-api \
  --name live \
  --function-version 2
```

**Instant cutover** - all traffic now uses version 2

**Rollback if needed**:
```bash
aws lambda update-alias \
  --function-name auth-api \
  --name live \
  --function-version 1
```

**Instant rollback** - all traffic back to version 1

### Step 7: Update API Gateway Integration (Optional)

To use alias in API Gateway:

```hcl
# In api-gateway-lambda-integration module
lambda_function_arn = "${module.lambda_auth_api.function_arn}:live"
```

**Note**: Current implementation works without this change. API Gateway invokes $LATEST by default, which is fine for now.

### Step 8: Roll Out to All Functions

Once tested with auth-api, add to all 18 Lambda functions:

```hcl
publish      = true
create_alias = true
alias_name   = "live"
```

---

## Benefits

### Zero-Downtime Deployments
- No API Gateway changes needed
- Instant cutover (< 1 second)
- No cold starts (versions are pre-warmed)

### Instant Rollback
- Single CLI command
- No redeployment needed
- Back to previous version in seconds

### Canary Deployments (Optional)
```bash
# Route 10% traffic to v2, 90% to v1
aws lambda update-alias \
  --function-name auth-api \
  --name live \
  --function-version 2 \
  --routing-config AdditionalVersionWeights={1=0.9}
```

### Version History
- Keep last 5-10 versions for rollback
- Audit trail of all deployments
- Easy to compare versions

---

## Deployment Workflow

### Current Workflow (Without Versioning)
```
1. Update code
2. Deploy to Lambda
3. Hope it works
4. If broken: Redeploy old code (5-10 minutes)
```

### New Workflow (With Versioning)
```
1. Update code
2. Deploy to Lambda (creates version N)
3. Test version N directly
4. Update alias to version N (instant)
5. If broken: Update alias back to N-1 (instant)
```

---

## Testing Checklist

- [ ] Apply Terraform changes for auth-api
- [ ] Verify alias created
- [ ] Deploy new code with --publish
- [ ] Verify new version created
- [ ] Update alias to new version
- [ ] Test API endpoint works
- [ ] Rollback alias to previous version
- [ ] Verify rollback works
- [ ] Document process

---

## Rollback Procedures

### Immediate Rollback (< 1 minute)
```bash
# List recent versions
aws lambda list-versions-by-function --function-name auth-api

# Update alias to previous version
aws lambda update-alias \
  --function-name auth-api \
  --name live \
  --function-version <PREVIOUS_VERSION>
```

### Emergency Rollback (If alias broken)
```bash
# Update API Gateway to use specific version
aws apigateway update-integration \
  --rest-api-id diz6ceeb22 \
  --resource-id <RESOURCE_ID> \
  --http-method ANY \
  --patch-operations op=replace,path=/uri,value=arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:371751795928:function:auth-api:1/invocations
```

---

## Security: JWT Secret Management

### Issue: Hardcoded JWT Secret in Public GitHub Repo

If your repo is public and contains hardcoded secrets like:
```python
JWT_SECRET = 'your-jwt-secret-key'
```

Anyone can forge authentication tokens and access your system as any user (including admin).

### Solution: Use Environment Variables

**Step 1: Generate Strong Secret**
```powershell
# Generate 64-character random secret
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})
```

Copy the output (e.g., `aB3xK9mP7qR2sT5vW8yZ1cD4eF6gH9jK...`)

**Step 2: Add to Lambda Environment Variables**
```bash
# Set for all functions that use JWT
aws lambda update-function-configuration \
  --function-name auth-api \
  --environment Variables={JWT_SECRET=<YOUR_SECRET>}

aws lambda update-function-configuration \
  --function-name news-api \
  --environment Variables={JWT_SECRET=<YOUR_SECRET>}

aws lambda update-function-configuration \
  --function-name admin-api \
  --environment Variables={JWT_SECRET=<YOUR_SECRET>}
```

**Step 3: Update Code (Safe for GitHub)**

Change in `auth_api/index.py`, `news_api/index.py`, `admin_api/index.py`:

```python
# Before (INSECURE - hardcoded)
JWT_SECRET = 'your-jwt-secret-key'

# After (SECURE - reads from environment)
import os
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-jwt-secret-key')
```

**Step 4: Deploy Updated Code**
```bash
# For each function:
cd Downloader/auth_api
zip -r function.zip index.py
aws lambda update-function-code \
  --function-name auth-api \
  --zip-file fileb://function.zip \
  --publish

# Update alias to new version
aws lambda update-alias \
  --function-name auth-api \
  --name live \
  --function-version <NEW_VERSION>

# Repeat for news-api and admin-api
```

**Step 5: Commit to GitHub**
```bash
git add auth_api/index.py news_api/index.py admin_api/index.py
git commit -m "Secure JWT secret using environment variables"
git push
```

**Why This is Safe:**
- GitHub only sees: `os.environ.get('JWT_SECRET', ...)`
- Actual secret stored in AWS Lambda (not in code)
- Secret never appears in git history
- Can rotate secret without code changes

**Note:** This will invalidate all existing tokens. Users must re-login.

---

## Troubleshooting

### Issue: CORS Error After Enabling Versioning

**Symptoms**: 502 Bad Gateway + missing Access-Control-Allow-Origin header

**Root Cause**: Alias pointing to version with placeholder.zip (empty code)

**Fix**:
```bash
# 1. Deploy real code with --publish
cd Downloader/auth_api
zip -r function.zip index.py
aws lambda update-function-code \
  --function-name auth-api \
  --zip-file fileb://function.zip \
  --publish

# Note the version number (e.g., 6)

# 2. Update alias to new version
aws lambda update-alias \
  --function-name auth-api \
  --name live \
  --function-version 6
```

**Prevention**: Always deploy real code BEFORE enabling versioning in Terraform.

### Issue: Alias Not Found

**Symptoms**: API Gateway returns error about missing alias

**Fix**:
```bash
# Create alias manually
aws lambda create-alias \
  --function-name auth-api \
  --name live \
  --function-version 1
```

### Issue: Version Mismatch

**Symptoms**: Alias points to old version

**Fix**:
```bash
# Check current alias
aws lambda get-alias --function-name auth-api --name live

# Update to latest version
aws lambda update-alias \
  --function-name auth-api \
  --name live \
  --function-version $LATEST
```

---

## Cost Impact

**Lambda Versioning**: $0/month
- Versions stored as code (negligible storage)
- No additional invocation costs
- Aliases are free

**Total Additional Cost**: $0/month

---

## Next Steps

1. ✅ Update Lambda module
2. ✅ Test with auth-api
3. ⏳ Apply Terraform changes
4. ⏳ Verify alias creation
5. ⏳ Test blue/green deployment
6. ⏳ Document rollback procedures
7. ⏳ Roll out to remaining 17 functions

---

**Status**: Ready for testing  
**Last Updated**: January 2025
