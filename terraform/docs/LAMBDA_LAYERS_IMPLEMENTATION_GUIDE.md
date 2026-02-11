# Lambda Layers - Implementation Guide (Week 11-12)

## Status: 🔜 NOT YET IMPLEMENTED

This guide outlines the planned implementation for Week 11-12.

---

## Overview
Add Lambda Layers to Terraform for yt-dlp and FFmpeg, enabling version control and automated deployment of shared dependencies.

---

## Goals

### Week 11: yt-dlp Layer
- Create Lambda Layer module
- Import existing yt-dlp layer
- Version control layer updates
- Automate layer deployment

### Week 12: FFmpeg Layer & Polish
- Import FFmpeg layer
- Update Lambda functions to use Terraform-managed layers
- Documentation updates
- Final testing and validation

---

## Step 1: Gather Current Layer Information

### Commands to Inspect Existing Layers

```bash
# List all Lambda layers
aws lambda list-layers

# Get layer versions
aws lambda list-layer-versions --layer-name yt-dlp-layer
aws lambda list-layer-versions --layer-name ffmpeg-layer

# Get specific layer version details
aws lambda get-layer-version --layer-name yt-dlp-layer --version-number 1

# Get layer version ARN
aws lambda get-layer-version --layer-name yt-dlp-layer --version-number 1 --query 'LayerVersionArn'

# Check which functions use the layer
aws lambda list-functions --query 'Functions[?Layers[?contains(Arn, `yt-dlp-layer`)]].[FunctionName]' --output table
```

### Expected Current State

**yt-dlp Layer**:
```
Layer Name: yt-dlp-layer
Version: 1
ARN: arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer:1
Size: ~50 MB
Compatible Runtimes: python3.12
Used by: router, downloader
```

**FFmpeg Layer**:
```
Layer Name: ffmpeg-layer
Version: 1
ARN: arn:aws:lambda:us-east-1:371751795928:layer:ffmpeg-layer:1
Size: ~120 MB
Compatible Runtimes: python3.12
Used by: downloader, thumbnail_generator
```

---

## Step 2: Design Layer Management Strategy

### Current State
- Layers created manually
- No version control
- Manual updates required
- No automated deployment

### Target State
- Layers managed by Terraform
- Version controlled in Git
- Automated deployment via CI/CD
- Easy rollback to previous versions

### Layer Update Strategy

**Option 1: Immutable Layers** (Recommended)
- Create new layer version for each update
- Update Lambda functions to use new version
- Keep old versions for rollback

**Option 2: Mutable Layers**
- Update existing layer version
- Lambda functions automatically use new version
- No rollback capability

**Decision**: Use Option 1 (Immutable Layers) for safety

---

## Step 3: Create Lambda Layer Module

### Module Structure

**File**: `terraform/modules/lambda-layer/main.tf`

```hcl
resource "aws_lambda_layer_version" "this" {
  layer_name          = var.layer_name
  description         = var.description
  filename            = var.filename
  source_code_hash    = filebase64sha256(var.filename)
  compatible_runtimes = var.compatible_runtimes

  lifecycle {
    create_before_destroy = true
  }
}
```

**File**: `terraform/modules/lambda-layer/variables.tf`

```hcl
variable "layer_name" {
  description = "Name of the Lambda layer"
  type        = string
}

variable "description" {
  description = "Description of the layer"
  type        = string
  default     = ""
}

variable "filename" {
  description = "Path to the layer ZIP file"
  type        = string
}

variable "compatible_runtimes" {
  description = "List of compatible runtimes"
  type        = list(string)
  default     = ["python3.12"]
}
```

**File**: `terraform/modules/lambda-layer/outputs.tf`

```hcl
output "layer_arn" {
  description = "ARN of the Lambda layer version"
  value       = aws_lambda_layer_version.this.arn
}

output "layer_version" {
  description = "Version number of the layer"
  value       = aws_lambda_layer_version.this.version
}
```

---

## Step 4: Prepare Layer ZIP Files

### yt-dlp Layer Structure

```
yt-dlp-layer/
├── python/
│   └── lib/
│       └── python3.12/
│           └── site-packages/
│               └── yt_dlp/
│                   └── ... (yt-dlp files)
└── yt-dlp-layer.zip
```

### Build Script

**File**: `terraform/layers/build-yt-dlp-layer.sh`

```bash
#!/bin/bash

# Create layer directory structure
mkdir -p yt-dlp-layer/python/lib/python3.12/site-packages

# Install yt-dlp
pip install yt-dlp==2025.9.26 -t yt-dlp-layer/python/lib/python3.12/site-packages

# Create ZIP
cd yt-dlp-layer
zip -r ../yt-dlp-layer.zip .
cd ..

# Cleanup
rm -rf yt-dlp-layer

echo "yt-dlp layer created: yt-dlp-layer.zip"
```

### FFmpeg Layer Structure

```
ffmpeg-layer/
├── bin/
│   ├── ffmpeg
│   └── ffprobe
└── ffmpeg-layer.zip
```

### Build Script

**File**: `terraform/layers/build-ffmpeg-layer.sh`

```bash
#!/bin/bash

# Download FFmpeg static build
wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz

# Extract
tar -xf ffmpeg-release-amd64-static.tar.xz

# Create layer structure
mkdir -p ffmpeg-layer/bin
cp ffmpeg-*-amd64-static/ffmpeg ffmpeg-layer/bin/
cp ffmpeg-*-amd64-static/ffprobe ffmpeg-layer/bin/

# Create ZIP
cd ffmpeg-layer
zip -r ../ffmpeg-layer.zip .
cd ..

# Cleanup
rm -rf ffmpeg-*-amd64-static*
rm -rf ffmpeg-layer

echo "FFmpeg layer created: ffmpeg-layer.zip"
```

---

## Step 5: Use Module in Production Environment

### Add to main.tf

**File**: `terraform/environments/prod/main.tf`

```hcl
# yt-dlp Lambda Layer
module "lambda_layer_yt_dlp" {
  source = "../../modules/lambda-layer"

  layer_name          = "yt-dlp-layer"
  description         = "yt-dlp library for video downloading"
  filename            = "${path.module}/../../layers/yt-dlp-layer.zip"
  compatible_runtimes = ["python3.12"]
}

# FFmpeg Lambda Layer
module "lambda_layer_ffmpeg" {
  source = "../../modules/lambda-layer"

  layer_name          = "ffmpeg-layer"
  description         = "FFmpeg binaries for video processing"
  filename            = "${path.module}/../../layers/ffmpeg-layer.zip"
  compatible_runtimes = ["python3.12"]
}

# Update Lambda functions to use Terraform-managed layers
module "lambda_router" {
  source = "../../modules/lambda"

  function_name = "router"
  # ... other config ...

  layers = [
    module.lambda_layer_yt_dlp.layer_arn  # Use Terraform-managed layer
  ]
}

module "lambda_downloader" {
  source = "../../modules/lambda"

  function_name = "downloader"
  # ... other config ...

  layers = [
    module.lambda_layer_yt_dlp.layer_arn,
    module.lambda_layer_ffmpeg.layer_arn
  ]
}
```

---

## Step 6: Import Existing Layers

### Import Layer Versions

```bash
# Import yt-dlp layer version 1
terraform import module.lambda_layer_yt_dlp.aws_lambda_layer_version.this arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer:1

# Import FFmpeg layer version 1
terraform import module.lambda_layer_ffmpeg.aws_lambda_layer_version.this arn:aws:lambda:us-east-1:371751795928:layer:ffmpeg-layer:1
```

### Verify Import

```bash
terraform plan
```

**Expected**: No changes (layers match Terraform config)

---

## Step 7: Automate Layer Deployment with CI/CD

### GitHub Actions Workflow

**File**: `.github/workflows/deploy-layers.yml`

```yaml
name: Deploy Lambda Layers

on:
  push:
    branches:
      - main
    paths:
      - 'terraform/layers/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Build yt-dlp layer
        run: |
          cd terraform/layers
          bash build-yt-dlp-layer.sh
      
      - name: Build FFmpeg layer
        run: |
          cd terraform/layers
          bash build-ffmpeg-layer.sh
      
      - name: Deploy layers with Terraform
        run: |
          cd terraform/environments/prod
          terraform init
          terraform apply -auto-approve -target=module.lambda_layer_yt_dlp -target=module.lambda_layer_ffmpeg
```

---

## Step 8: Layer Update Process

### Update yt-dlp Version

1. **Update build script**:
```bash
# Change version in build-yt-dlp-layer.sh
pip install yt-dlp==2025.10.15 -t yt-dlp-layer/python/lib/python3.12/site-packages
```

2. **Build new layer**:
```bash
cd terraform/layers
bash build-yt-dlp-layer.sh
```

3. **Apply Terraform**:
```bash
cd terraform/environments/prod
terraform apply
```

4. **Terraform creates new layer version** (version 2)

5. **Update Lambda functions** to use new version:
```hcl
layers = [
  module.lambda_layer_yt_dlp.layer_arn  # Automatically uses latest version
]
```

6. **Apply Lambda updates**:
```bash
terraform apply
```

---

## Step 9: Rollback Process

### Rollback to Previous Layer Version

1. **Identify previous version ARN**:
```bash
aws lambda list-layer-versions --layer-name yt-dlp-layer
```

2. **Update Lambda function** to use previous version:
```hcl
layers = [
  "arn:aws:lambda:us-east-1:371751795928:layer:yt-dlp-layer:1"  # Hardcode previous version
]
```

3. **Apply change**:
```bash
terraform apply
```

4. **Verify rollback**:
```bash
aws lambda get-function-configuration --function-name router --query 'Layers[*].Arn'
```

---

## Expected Benefits

### Version Control
- **Before**: No history of layer changes
- **After**: Git tracks all layer updates

### Automated Deployment
- **Before**: Manual ZIP creation and upload
- **After**: CI/CD builds and deploys automatically

### Rollback Capability
- **Before**: No easy way to revert layer changes
- **After**: Simple rollback to previous version

### Consistency
- **Before**: Different layer versions across environments
- **After**: Terraform ensures consistent versions

---

## Estimated Costs

### Lambda Layers
- **Storage**: $0.00 (included in Lambda pricing)
- **Requests**: $0.00 (no additional charge)

**Total Estimated Cost**: $0/month

---

## Implementation Timeline

### Week 11 (Days 1-3)
- Create Lambda Layer module
- Create build scripts for yt-dlp layer
- Import existing yt-dlp layer
- Test layer deployment

### Week 11 (Days 4-5)
- Create build script for FFmpeg layer
- Import existing FFmpeg layer
- Update Lambda functions to use Terraform-managed layers
- Test layer updates

### Week 12 (Days 1-3)
- Create CI/CD workflow for layer deployment
- Test automated layer deployment
- Document layer update process
- Create rollback procedures

### Week 12 (Days 4-5)
- Final testing and validation
- Update all documentation
- Create maintenance runbooks
- Project completion celebration! 🎉

---

## Success Criteria

✅ yt-dlp layer managed by Terraform  
✅ FFmpeg layer managed by Terraform  
✅ Lambda functions use Terraform-managed layers  
✅ CI/CD workflow deploys layers automatically  
✅ Rollback process documented and tested  
✅ All documentation updated  

---

## Key Learnings (To Be Documented)

### Layer Size Limits
- **Unzipped**: 250 MB max
- **Zipped**: 50 MB max (direct upload), 250 MB max (S3)
- **Total (function + layers)**: 250 MB unzipped

### Layer Path Structure
- **Python**: `/opt/python/lib/python3.12/site-packages`
- **Binaries**: `/opt/bin`
- **Lambda adds `/opt` to PATH automatically**

### Layer Versioning
- **Immutable**: Each version is permanent
- **Can't update**: Must create new version
- **Can delete**: Old versions can be deleted if not in use

---

## Related Files
- [Lambda Implementation Guide](./LAMBDA_IMPLEMENTATION_GUIDE.md)
- [Terraform Documentation](../TERRAFORM_DOCUMENTATION.md)
- [CI/CD Documentation](../../.github/CI_CD_DOCUMENTATION.md)

---

**Status**: Planning Phase  
**Planned Start**: Week 11  
**Estimated Duration**: 2 weeks  
**Created**: February 10, 2026
