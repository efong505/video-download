# Terraform Multi-Account Infrastructure Copy Tutorial

**Purpose**: Learn to replicate production infrastructure to a child AWS account using Terraform

**What You'll Learn**:
- Multi-account AWS architecture with AWS Organizations
- Terraform provider configuration for multiple accounts
- Cross-account IAM roles and permissions
- Infrastructure replication patterns
- State management across accounts
- Resource naming strategies

**Time Required**: 2-3 hours for first run, 30-45 minutes for practice runs

**Prerequisites**:
- AWS CLI configured with production account credentials (371751795928)
- Terraform installed (v1.0+)
- Access to ed@ekewaka child account
- PowerShell 7+

---

## Tutorial Overview

This tutorial teaches you to copy a simplified version of your production infrastructure to a child account. You'll practice:

1. **Account Setup**: Configure cross-account access
2. **Provider Configuration**: Set up Terraform for multi-account
3. **Infrastructure Copy**: Deploy resources to child account
4. **Verification**: Test the copied infrastructure
5. **Cleanup**: Remove all resources

---

## What Gets Copied

**Simplified Production Stack**:
- ✅ S3 bucket with versioning, encryption, CORS
- ✅ DynamoDB table (1 sample table)
- ✅ Lambda function with layer
- ✅ API Gateway REST API
- ✅ CloudWatch log group and alarm
- ✅ IAM role with policies
- ✅ SNS topic for notifications

**Not Included** (to keep tutorial focused):
- CloudFront (2+ hour deployment)
- Route53/ACM (requires domain ownership)
- 28 DynamoDB tables (1 sample is enough)
- 18 Lambda functions (1 sample is enough)

---

## Directory Structure

```
terraform-copy-organization/
├── README.md                          # This file
├── docs/
│   ├── STEP-01-ACCOUNT-SETUP.md      # AWS Organizations setup
│   ├── STEP-02-IAM-ROLES.md          # Cross-account IAM
│   ├── STEP-03-TERRAFORM-CONFIG.md   # Provider configuration
│   ├── STEP-04-DEPLOY.md             # Deploy infrastructure
│   ├── STEP-05-VERIFY.md             # Test deployment
│   ├── STEP-06-CLEANUP.md            # Destroy resources
│   └── TROUBLESHOOTING.md            # Common issues
├── terraform/
│   ├── main.tf                        # Main infrastructure
│   ├── providers.tf                   # Multi-account providers
│   ├── variables.tf                   # Input variables
│   ├── outputs.tf                     # Verification outputs
│   ├── terraform.tfvars.example       # Example variables
│   └── backend.tf                     # State configuration
├── lambda-code/
│   └── sample-function/
│       └── index.py                   # Sample Lambda
├── scripts/
│   ├── setup-accounts.ps1             # Account setup automation
│   ├── verify-deployment.ps1          # Test deployment
│   ├── cleanup.ps1                    # Cleanup script
│   └── reset-tutorial.ps1             # Reset for practice
└── .gitignore                         # Ignore sensitive files
```

---

## Quick Start

```powershell
# 1. Navigate to tutorial directory
cd C:\Users\Ed\Documents\Programming\AWS\terraform-copy-organization

# 2. Follow step-by-step guides
# Start with: docs\STEP-01-ACCOUNT-SETUP.md

# 3. Or use automated setup
.\scripts\setup-accounts.ps1

# 4. Deploy infrastructure
cd terraform
terraform init
terraform plan
terraform apply

# 5. Verify deployment
cd ..
.\scripts\verify-deployment.ps1

# 6. Cleanup when done
terraform destroy
```

---

## Learning Path

### First Time (2-3 hours)
1. Read all documentation carefully
2. Understand each Terraform resource
3. Manually execute each step
4. Verify outputs at each stage
5. Troubleshoot any issues

### Practice Runs (30-45 minutes)
1. Use automated scripts
2. Focus on Terraform commands
3. Experiment with modifications
4. Practice rollback scenarios
5. Build muscle memory

---

## Key Concepts Covered

### 1. AWS Organizations
- Parent/child account relationships
- Cross-account access patterns
- Consolidated billing
- Service Control Policies (SCPs)

### 2. Terraform Multi-Account
- Multiple provider configurations
- Provider aliases
- Cross-account resource creation
- State management strategies

### 3. IAM Cross-Account Roles
- AssumeRole permissions
- Trust relationships
- External ID for security
- Least privilege principles

### 4. Infrastructure Replication
- Resource naming conventions
- Environment-specific variables
- Configuration management
- Dependency handling

---

## Safety Features

✅ **Isolated Environment**: Child account keeps production safe
✅ **Unique Naming**: Resources won't conflict with production
✅ **Easy Cleanup**: `terraform destroy` removes everything
✅ **No Production Impact**: Completely separate infrastructure
✅ **Cost Control**: Minimal resources, easy to monitor

---

## Cost Estimate

**Per Practice Run**:
- S3: $0.01 (minimal storage)
- DynamoDB: $0.00 (on-demand, no data)
- Lambda: $0.00 (free tier)
- API Gateway: $0.00 (no traffic)
- CloudWatch: $0.01 (logs)

**Total**: ~$0.02 per practice run

---

## Next Steps

1. **Read**: `docs\STEP-01-ACCOUNT-SETUP.md`
2. **Setup**: Configure AWS accounts
3. **Deploy**: Run Terraform apply
4. **Practice**: Repeat multiple times
5. **Experiment**: Modify and learn

---

## Support

**Issues?** Check `docs\TROUBLESHOOTING.md`

**Questions?** Review step-by-step guides in `docs/`

**Reset?** Run `.\scripts\reset-tutorial.ps1`

---

**Ready to start?** → Open `docs\STEP-01-ACCOUNT-SETUP.md`
