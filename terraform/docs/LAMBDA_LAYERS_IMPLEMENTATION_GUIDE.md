# Lambda Layers Implementation Guide

## Overview

This guide documents the implementation of Lambda Layers in Terraform for the Christian Conservative Platform. Lambda layers provide shared code and dependencies that can be used across multiple Lambda functions.

**Implementation Date**: February 11, 2026  
**Status**: ✅ COMPLETE  
**Duration**: 1 day  
**Complexity**: Low

---

## Architecture

### Layer Strategy

**Design Decision**: Separate infrastructure management from layer code updates
- **Terraform manages**: Layer configuration, runtimes, function associations
- **Manual/CI-CD manages**: Layer code (ZIP files)
- **Pattern**: Same as Lambda functions (ignore_changes on filename)

### Layers Managed (3)

1. **yt-dlp-layer-v2** - Video download library
2. **ffmpeg-layer** - Video processing binaries
3. **requests-layer** - Python HTTP library

---

## Module Structure

### Lambda Layer Module

**Location**: `terraform/modules/lambda-layer/`

**Files**:
```
lambda-layer/
├── main.tf         # Layer resource with ignore_changes
├── variables.tf    # Layer configuration variables
└── outputs.tf      # Layer ARN and version
```

### Module Code

**main.tf**:
```hcl
resource "aws_lambda_layer_version" "this" {
  layer_name          = var.layer_name
  description         = var.description
  compatible_runtimes = var.compatible_runtimes
  filename            = var.filename

  lifecycle {
    ignore_changes = [filename]
  }
}
```

**Key Feature**: `ignore_changes = [filename]` prevents Terraform from recreating layers when ZIP files change.

---

## Implementation Steps

### Step 1: Identify Existing Layers

```bash
# List all Lambda layers
aws lambda list-layers --region us-east-1

# Output showed 6 layers (3 active, 3 unused)
```

**Active Layers**:
- yt-dlp-layer-v2:1 (~2.9 MB)
- ffmpeg-layer:1 (~58 MB)
- requests-layer:1

**Unused Layers** (not imported):
- chrome-aws-lambda-layer:2
- ffmpeg:2 (old version)
- yt-dlp-layer:3 (old version)

### Step 2: Check Layer Usage

```bash
# Check which functions use layers
aws lambda get-function --function-name video-downloader
aws lambda get-function --function-name thumbnail-generator
aws lambda get-function --function-name url-analysis-api
```

**Layer Usage**:
- video-downloader: yt-dlp-layer-v2:1, ffmpeg-layer:1
- thumbnail-generator: ffmpeg-layer:1
- url-analysis-api: requests-layer:1

### Step 3: Create Lambda Layer Module

Created module with 3 files (main.tf, variables.tf, outputs.tf).

### Step 4: Add Layer Modules to main.tf

```hcl
# yt-dlp Layer
module "layer_yt_dlp" {
  source = "../../modules/lambda-layer"

  layer_name          = "yt-dlp-layer-v2"
  description         = "yt-dlp binary for Lambda"
  compatible_runtimes = ["python3.11"]
}

# FFmpeg Layer
module "layer_ffmpeg" {
  source = "../../modules/lambda-layer"

  layer_name          = "ffmpeg-layer"
  description         = "FFmpeg binaries for video conversion"
  compatible_runtimes = ["python3.11"]
}

# Requests Layer
module "layer_requests" {
  source = "../../modules/lambda-layer"

  layer_name          = "requests-layer"
  compatible_runtimes = ["python3.9", "python3.10", "python3.11", "python3.12"]
}
```

**Note**: requests-layer has no description to prevent unnecessary recreation.

### Step 5: Initialize Terraform

```bash
cd terraform/environments/prod
terraform init
```

### Step 6: Import Existing Layers

```bash
# Import yt-dlp layer
terraform import module.layer_yt_dlp.aws_lambda_layer_version.this arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer-v2:1

# Import ffmpeg layer
terraform import module.layer_ffmpeg.aws_lambda_layer_version.this arn:aws:lambda:us-east-1:371751795928:layer:ffmpeg-layer:1

# Import requests layer
terraform import module.layer_requests.aws_lambda_layer_version.this arn:aws:lambda:us-east-1:371751795928:layer:requests-layer:1
```

**Result**: All 3 layers imported successfully.

### Step 7: Fix Schema Mismatches

**Issue**: email-events table had range_key "timestamp" not in Terraform config.

**Fix**:
```hcl
module "dynamodb_email_events" {
  source = "../../modules/dynamodb"

  table_name   = "email-events"
  hash_key     = "event_id"
  range_key    = "timestamp"  # Added
  billing_mode = "PAY_PER_REQUEST"

  attributes = [
    { name = "event_id", type = "S" },
    { name = "timestamp", type = "N" }  # Added
  ]
}
```

### Step 8: Apply Changes

```bash
terraform apply -auto-approve
```

**Result**:
- 1 added (new API Gateway deployment)
- 3 changed (email-events table, API Gateway stage, gateway response)
- 1 destroyed (old API Gateway deployment)
- **No layer recreations** ✅

---

## Layer Details

### yt-dlp-layer-v2

**Purpose**: Video download library for YouTube and other platforms

**Configuration**:
- **Name**: yt-dlp-layer-v2
- **Version**: 1
- **Size**: ~2.9 MB
- **Runtime**: python3.11
- **ARN**: arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer-v2:1

**Used By**:
- video-downloader

**Contents**:
- yt-dlp binary
- Python dependencies

### ffmpeg-layer

**Purpose**: Video processing and thumbnail generation

**Configuration**:
- **Name**: ffmpeg-layer
- **Version**: 1
- **Size**: ~58 MB
- **Runtime**: python3.11
- **ARN**: arn:aws:lambda:us-east-1:371751795928:layer:ffmpeg-layer:1

**Used By**:
- video-downloader
- thumbnail-generator

**Contents**:
- FFmpeg 7.0.2 binaries
- Video codec libraries

### requests-layer

**Purpose**: Python HTTP library for API calls

**Configuration**:
- **Name**: requests-layer
- **Version**: 1
- **Size**: Small
- **Runtimes**: python3.9, python3.10, python3.11, python3.12
- **ARN**: arn:aws:lambda:us-east-1:371751795928:layer:requests-layer:1

**Used By**:
- url-analysis-api

**Contents**:
- requests library
- urllib3, certifi dependencies

---

## Key Design Decisions

### 1. ignore_changes on filename

**Rationale**: Separate infrastructure from code updates
- Terraform manages layer configuration
- Manual/CI-CD manages layer code
- Prevents forced recreation on every ZIP change

### 2. No Description for requests-layer

**Issue**: Adding description would force layer recreation (version 1 → 2)

**Solution**: Removed description from module configuration

**Trade-off**: Less documentation in AWS Console, but no unnecessary version bump

### 3. Import Only Active Layers

**Decision**: Import only 3 active layers, skip 3 unused layers

**Rationale**:
- Unused layers add no value
- Reduces Terraform state complexity
- Can import later if needed

### 4. Version Pinning in Lambda Functions

**Current State**: Lambda functions reference layers by ARN with version
```hcl
layers = [
  "arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer-v2:1",
  "arn:aws:lambda:us-east-1:371751795928:layer:ffmpeg-layer:1"
]
```

**Future Enhancement**: Use Terraform outputs for dynamic references
```hcl
layers = [
  module.layer_yt_dlp.layer_arn,
  module.layer_ffmpeg.layer_arn
]
```

---

## Layer Update Process

### Manual Update (Current)

1. Build new layer ZIP locally
2. Upload to AWS Lambda manually
3. Update Lambda function layer version
4. Test function
5. Rollback if needed

### Future CI/CD Enhancement

**Potential Workflow**:
```yaml
name: Deploy Lambda Layer
on:
  push:
    paths:
      - 'layers/**'
jobs:
  deploy:
    - Build layer ZIP
    - Upload to Lambda
    - Update Terraform with new version
    - Run tests
    - Update functions to use new version
```

---

## Validation

### Verify Layer Import

```bash
# Check Terraform state
terraform state list | grep layer

# Output:
# module.layer_ffmpeg.aws_lambda_layer_version.this
# module.layer_requests.aws_lambda_layer_version.this
# module.layer_yt_dlp.aws_lambda_layer_version.this
```

### Verify Layer ARNs

```bash
# Show layer details
terraform state show module.layer_yt_dlp.aws_lambda_layer_version.this
```

### Verify No Drift

```bash
terraform plan
# Should show: No changes. Your infrastructure matches the configuration.
```

---

## Troubleshooting

### Issue: Layer Wants to Recreate

**Symptom**: Terraform plan shows layer replacement

**Cause**: Description or runtime change

**Solution**: 
1. Check if change is intentional
2. If not, remove description or revert runtime change
3. If intentional, allow recreation (creates new version)

### Issue: Import Failed

**Symptom**: Error during terraform import

**Cause**: Incorrect ARN format

**Solution**: Use full ARN with version
```bash
# Correct format
arn:aws:lambda:us-east-1:371751795928:layer:layer-name:version

# Incorrect format (missing version)
arn:aws:lambda:us-east-1:371751795928:layer:layer-name
```

### Issue: Lambda Function Can't Find Layer

**Symptom**: Function fails with "cannot import module"

**Cause**: Layer not attached to function

**Solution**: Add layer ARN to Lambda function configuration
```hcl
module "lambda_function" {
  layers = ["arn:aws:lambda:us-east-1:371751795928:layer:layer-name:1"]
}
```

---

## Cost Analysis

### Lambda Layers Pricing

**Storage**: $0.03 per GB-month
- yt-dlp-layer-v2: ~2.9 MB = $0.00009/month
- ffmpeg-layer: ~58 MB = $0.0017/month
- requests-layer: ~5 MB = $0.00015/month

**Total**: ~$0.002/month (negligible)

**Invocations**: Included in Lambda pricing (no additional cost)

---

## Benefits Achieved

✅ **Infrastructure as Code**: All layers managed by Terraform  
✅ **Version Control**: Layer versions tracked in Terraform state  
✅ **Easy Rollback**: Pin to specific layer version  
✅ **Consistency**: Same layer versions across all functions  
✅ **Documentation**: Layer configuration documented in code  
✅ **No Downtime**: Zero-downtime import and management  

---

## Future Enhancements

### 1. Dynamic Layer References

Replace hardcoded ARNs with Terraform outputs:
```hcl
layers = [module.layer_yt_dlp.layer_arn]
```

### 2. Layer Build Automation

Create scripts to build layers locally:
```bash
./build-yt-dlp-layer.sh
./build-ffmpeg-layer.sh
```

### 3. CI/CD for Layers

Automate layer deployment on code changes.

### 4. Layer Versioning Strategy

Implement semantic versioning for layers.

### 5. Multi-Region Layers

Deploy layers to multiple regions for disaster recovery.

---

## Maintenance

### Regular Tasks

**Monthly**:
- Check for yt-dlp updates
- Check for FFmpeg updates
- Review layer usage across functions

**Quarterly**:
- Audit unused layers
- Review layer sizes
- Optimize layer contents

**Annually**:
- Major version updates
- Security patches
- Runtime updates

### Layer Update Checklist

- [ ] Build new layer ZIP
- [ ] Test layer locally
- [ ] Upload to Lambda
- [ ] Create new version
- [ ] Update one function (canary)
- [ ] Test canary function
- [ ] Update remaining functions
- [ ] Monitor for errors
- [ ] Update Terraform if needed

---

## Conclusion

Lambda Layers implementation completed successfully in 1 day. All 3 active layers now managed by Terraform with proper separation between infrastructure and code updates.

**Key Takeaway**: The ignore_changes pattern allows Terraform to manage layer infrastructure while keeping layer code updates flexible and independent.

---

**Implementation Date**: February 11, 2026  
**Status**: ✅ COMPLETE  
**Next Phase**: Final Polish (Week 12)
