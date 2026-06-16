# Quick Start Guide

Get up and running in 15 minutes!

---

## Prerequisites

- [ ] AWS CLI installed and configured
- [ ] Terraform installed (v1.0+)
- [ ] PowerShell 7+
- [ ] Access to production account (371751795928)
- [ ] Child account created (ed@ekewaka)

---

## Option 1: Automated Setup (Recommended)

```powershell
# 1. Navigate to tutorial directory
cd C:\Users\Ed\Documents\Programming\AWS\terraform-copy-organization

# 2. Run automated setup
.\scripts\setup-accounts.ps1 -ChildAccountId YOUR_CHILD_ACCOUNT_ID

# 3. Deploy infrastructure
cd terraform
terraform apply

# 4. Verify deployment
cd ..
.\scripts\verify-deployment.ps1

# 5. Clean up when done
.\scripts\cleanup.ps1
```

**Total time**: ~15 minutes

---

## Option 2: Manual Setup (Learning Mode)

### Step 1: Account Setup (20 minutes)
```powershell
# Read the guide
Get-Content docs\STEP-01-ACCOUNT-SETUP.md

# Follow instructions to:
# - Set up AWS Organizations
# - Create cross-account IAM role
# - Test assume-role access
```

### Step 2: IAM Configuration (10 minutes)
```powershell
# Read the guide
Get-Content docs\STEP-02-IAM-ROLES.md

# Understand:
# - Lambda execution role
# - Policy attachments
# - Trust vs permission policies
```

### Step 3: Terraform Config (15 minutes)
```powershell
# Read the guide
Get-Content docs\STEP-03-TERRAFORM-CONFIG.md

# Create Terraform files:
# - providers.tf
# - variables.tf
# - terraform.tfvars
# - backend.tf
# - outputs.tf

# Initialize Terraform
cd terraform
terraform init
terraform validate
```

### Step 4: Deploy (30 minutes)
```powershell
# Read the guide
Get-Content docs\STEP-04-DEPLOY.md

# Create Lambda code
# Create main.tf
# Deploy infrastructure
terraform plan
terraform apply
```

### Step 5: Verify (15 minutes)
```powershell
# Read the guide
Get-Content docs\STEP-05-VERIFY.md

# Test all components:
# - Lambda function
# - API Gateway
# - DynamoDB
# - S3
# - CloudWatch
```

### Step 6: Cleanup (10 minutes)
```powershell
# Read the guide
Get-Content docs\STEP-06-CLEANUP.md

# Destroy infrastructure
terraform destroy

# Verify cleanup
```

**Total time**: ~2 hours (first time)

---

## Practice Runs

After first complete run, subsequent practice runs take ~15-20 minutes:

```powershell
# Quick practice cycle
cd C:\Users\Ed\Documents\Programming\AWS\terraform-copy-organization

# Deploy
cd terraform
terraform apply

# Test
cd ..
.\scripts\verify-deployment.ps1

# Cleanup
.\scripts\cleanup.ps1 -Force
```

---

## Troubleshooting

**Issue?** Check `docs\TROUBLESHOOTING.md`

**Common problems**:
- terraform.tfvars not updated → Edit and replace REPLACE_WITH_YOUR_CHILD_ACCOUNT_ID
- Lambda ZIP not found → Run STEP-04 to create Lambda code
- Can't assume role → Verify cross-account role in child account
- Bucket name exists → Change s3_bucket_name in terraform.tfvars

---

## What You'll Learn

- ✅ Multi-account AWS architecture
- ✅ Cross-account IAM roles
- ✅ Terraform provider configuration
- ✅ Infrastructure as Code patterns
- ✅ Resource dependencies
- ✅ Deployment and verification
- ✅ Cleanup and reset

---

## Resources Created

- 1 IAM role with 4 policies
- 1 S3 bucket (versioned, encrypted)
- 1 DynamoDB table with GSI
- 1 Lambda function
- 1 API Gateway REST API
- 1 SNS topic
- 1 CloudWatch alarm
- 1 CloudWatch log group

**Total**: 20+ resources

---

## Cost

**Per practice run**: ~$0.02/day
**After cleanup**: $0

---

## Next Steps

1. **First time?** → Start with `docs\STEP-01-ACCOUNT-SETUP.md`
2. **Want automation?** → Run `.\scripts\setup-accounts.ps1`
3. **Need help?** → Check `docs\TROUBLESHOOTING.md`
4. **Ready to practice?** → Run the quick practice cycle above

---

## Support

- **Documentation**: See `docs/` directory
- **Scripts**: See `scripts/` directory
- **Issues**: Check `docs\TROUBLESHOOTING.md`

---

**Ready to start?** Choose Option 1 (automated) or Option 2 (manual) above!
