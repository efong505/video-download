# CloudFront Distribution - Detailed Implementation Guide

## Overview
Step-by-step guide for creating CloudFront modules and importing existing distribution with Origin Access Control (OAC).

---

## Step 1: Gather Existing CloudFront Information

### Commands to List Distributions

```bash
# List all CloudFront distributions
aws cloudfront list-distributions --query 'DistributionList.Items[*].[Id,DomainName,Status]' --output table

# Get detailed distribution config
aws cloudfront get-distribution --id E3N00R2D2NE9C5

# Get distribution config only (for updates)
aws cloudfront get-distribution-config --id E3N00R2D2NE9C5

# Check deployment status
aws cloudfront get-distribution --id E3N00R2D2NE9C5 --query "Distribution.Status"

# List Origin Access Controls
aws cloudfront list-origin-access-controls

# Get OAC details
aws cloudfront get-origin-access-control --id E3B3KMNHQ684US
```

### Data Collected

**Distribution ID**: E3N00R2D2NE9C5

**Domain Name**: d271vky579caz9.cloudfront.net

**Status**: Deployed

**Custom Domains (Aliases)**:
- videos.mytestimony.click
- christianconservativestoday.com

**SSL Certificate**: arn:aws:acm:us-east-1:371751795928:certificate/d29ff60a-9c7e-4b6a-920b-e9b6db5202b4

**Origin**: my-video-downloads-bucket.s3.us-east-1.amazonaws.com

**Origin Access Control ID**: E3B3KMNHQ684US

**Cache Policy**: 658327ea-f89d-4fab-a63d-7e88639e58f6 (AWS Managed CachingOptimized)

**Viewer Protocol Policy**: redirect-to-https

**Compression**: Enabled

---

## Step 2: Understand Origin Access Control (OAC)

### What is OAC?

**Origin Access Control** is the modern replacement for Origin Access Identity (OAI). It provides:
- Better security with AWS Signature Version 4 (SigV4)
- Support for all S3 features (SSE-KMS, SSE-C, DSSE-KMS)
- Improved logging and monitoring

### Get OAC Configuration

```bash
aws cloudfront get-origin-access-control --id E3B3KMNHQ684US
```

**Output**:
```json
{
    "OriginAccessControl": {
        "Id": "E3B3KMNHQ684US",
        "OriginAccessControlConfig": {
            "Name": "my-video-downloads-oac",
            "Description": "OAC for my-video-downloads-bucket",
            "SigningProtocol": "sigv4",
            "SigningBehavior": "always",
            "OriginAccessControlOriginType": "s3"
        }
    }
}
```

---

## Step 3: Create CloudFront OAC Module

### Directory Setup
```bash
mkdir -p terraform/modules/cloudfront-oac
cd terraform/modules/cloudfront-oac
```

### Create main.tf

**File**: `terraform/modules/cloudfront-oac/main.tf`

```hcl
# CloudFront Origin Access Control
resource "aws_cloudfront_origin_access_control" "this" {
  name                              = var.name
  description                       = var.description
  origin_access_control_origin_type = var.origin_type
  signing_behavior                  = var.signing_behavior
  signing_protocol                  = var.signing_protocol

  lifecycle {
    prevent_destroy = true
  }
}
```

**Data Source**: OAC configuration from `aws cloudfront get-origin-access-control`

### Create variables.tf

**File**: `terraform/modules/cloudfront-oac/variables.tf`

```hcl
variable "name" {
  description = "Name of the Origin Access Control"
  type        = string
}

variable "description" {
  description = "Description of the OAC"
  type        = string
  default     = ""
}

variable "origin_type" {
  description = "Type of origin (s3, mediastore, lambda)"
  type        = string
  default     = "s3"
}

variable "signing_behavior" {
  description = "Signing behavior (always, never, no-override)"
  type        = string
  default     = "always"
}

variable "signing_protocol" {
  description = "Signing protocol (sigv4)"
  type        = string
  default     = "sigv4"
}
```

### Create outputs.tf

**File**: `terraform/modules/cloudfront-oac/outputs.tf`

```hcl
output "id" {
  description = "ID of the Origin Access Control"
  value       = aws_cloudfront_origin_access_control.this.id
}

output "etag" {
  description = "ETag of the Origin Access Control"
  value       = aws_cloudfront_origin_access_control.this.etag
}
```

---

## Step 4: Create CloudFront Distribution Module

### Directory Setup
```bash
mkdir -p terraform/modules/cloudfront
cd terraform/modules/cloudfront
```

### Create main.tf

**File**: `terraform/modules/cloudfront/main.tf`

```hcl
# CloudFront Distribution
resource "aws_cloudfront_distribution" "this" {
  enabled             = var.enabled
  is_ipv6_enabled     = var.ipv6_enabled
  comment             = var.comment
  default_root_object = var.default_root_object
  aliases             = var.aliases

  # S3 Origin with OAC
  origin {
    domain_name              = var.origin_domain_name
    origin_id                = var.origin_id
    origin_access_control_id = var.origin_access_control_id
  }

  # Default Cache Behavior
  default_cache_behavior {
    allowed_methods        = var.allowed_methods
    cached_methods         = var.cached_methods
    target_origin_id       = var.origin_id
    viewer_protocol_policy = var.viewer_protocol_policy
    compress               = var.compress

    # Use AWS Managed Cache Policy
    cache_policy_id = var.cache_policy_id
  }

  # SSL Certificate
  viewer_certificate {
    acm_certificate_arn      = var.acm_certificate_arn
    ssl_support_method       = "sni-only"
    minimum_protocol_version = var.minimum_protocol_version
  }

  # Restrictions
  restrictions {
    geo_restriction {
      restriction_type = var.geo_restriction_type
      locations        = var.geo_restriction_locations
    }
  }

  tags = var.tags

  lifecycle {
    prevent_destroy = true
  }
}
```

**Data Source**: Distribution configuration from `aws cloudfront get-distribution`

### Create variables.tf

**File**: `terraform/modules/cloudfront/variables.tf`

```hcl
variable "enabled" {
  description = "Whether the distribution is enabled"
  type        = bool
  default     = true
}

variable "ipv6_enabled" {
  description = "Whether IPv6 is enabled"
  type        = bool
  default     = true
}

variable "comment" {
  description = "Comment for the distribution"
  type        = string
  default     = ""
}

variable "default_root_object" {
  description = "Default root object"
  type        = string
  default     = "index.html"
}

variable "aliases" {
  description = "List of custom domain names (CNAMEs)"
  type        = list(string)
  default     = []
}

variable "origin_domain_name" {
  description = "Domain name of the origin"
  type        = string
}

variable "origin_id" {
  description = "Unique identifier for the origin"
  type        = string
  default     = "S3Origin"
}

variable "origin_access_control_id" {
  description = "ID of the Origin Access Control"
  type        = string
}

variable "allowed_methods" {
  description = "HTTP methods allowed"
  type        = list(string)
  default     = ["GET", "HEAD", "OPTIONS"]
}

variable "cached_methods" {
  description = "HTTP methods to cache"
  type        = list(string)
  default     = ["GET", "HEAD"]
}

variable "viewer_protocol_policy" {
  description = "Viewer protocol policy"
  type        = string
  default     = "redirect-to-https"
}

variable "compress" {
  description = "Enable compression"
  type        = bool
  default     = true
}

variable "cache_policy_id" {
  description = "ID of the cache policy"
  type        = string
}

variable "acm_certificate_arn" {
  description = "ARN of the ACM certificate"
  type        = string
}

variable "minimum_protocol_version" {
  description = "Minimum SSL/TLS protocol version"
  type        = string
  default     = "TLSv1.2_2021"
}

variable "geo_restriction_type" {
  description = "Type of geo restriction (none, whitelist, blacklist)"
  type        = string
  default     = "none"
}

variable "geo_restriction_locations" {
  description = "List of country codes for geo restriction"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Tags to apply to the distribution"
  type        = map(string)
  default     = {}
}
```

### Create outputs.tf

**File**: `terraform/modules/cloudfront/outputs.tf`

```hcl
output "distribution_id" {
  description = "ID of the CloudFront distribution"
  value       = aws_cloudfront_distribution.this.id
}

output "distribution_arn" {
  description = "ARN of the CloudFront distribution"
  value       = aws_cloudfront_distribution.this.arn
}

output "distribution_domain_name" {
  description = "Domain name of the CloudFront distribution"
  value       = aws_cloudfront_distribution.this.domain_name
}

output "distribution_hosted_zone_id" {
  description = "Hosted zone ID of the CloudFront distribution"
  value       = aws_cloudfront_distribution.this.hosted_zone_id
}
```

---

## Step 5: Use Modules in Production Environment

### Add to main.tf

**File**: `terraform/environments/prod/main.tf`

```hcl
# CloudFront Origin Access Control
module "cloudfront_oac" {
  source = "../../modules/cloudfront-oac"

  name              = "my-video-downloads-oac"
  description       = "OAC for my-video-downloads-bucket"
  origin_type       = "s3"
  signing_behavior  = "always"
  signing_protocol  = "sigv4"
}

# CloudFront Distribution
module "cloudfront_distribution" {
  source = "../../modules/cloudfront"

  enabled             = true
  ipv6_enabled        = true
  comment             = "CloudFront distribution for ministry platform"
  default_root_object = "index.html"

  aliases = [
    "videos.mytestimony.click",
    "christianconservativestoday.com"
  ]

  origin_domain_name       = module.s3_main.bucket_regional_domain_name
  origin_id                = "S3-my-video-downloads-bucket"
  origin_access_control_id = module.cloudfront_oac.id

  allowed_methods        = ["GET", "HEAD", "OPTIONS"]
  cached_methods         = ["GET", "HEAD"]
  viewer_protocol_policy = "redirect-to-https"
  compress               = true

  # AWS Managed CachingOptimized policy
  cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"

  acm_certificate_arn      = "arn:aws:acm:us-east-1:371751795928:certificate/d29ff60a-9c7e-4b6a-920b-e9b6db5202b4"
  minimum_protocol_version = "TLSv1.2_2021"

  geo_restriction_type = "none"

  tags = {
    Environment = "production"
    ManagedBy   = "terraform"
    Project     = "ministry-platform"
  }
}
```

**Data Source**: Values from Step 1 AWS CLI output

---

## Step 6: Update S3 Module for CloudFront

### Add Output to S3 Module

**File**: `terraform/modules/s3/outputs.tf`

```hcl
output "bucket_regional_domain_name" {
  description = "The bucket region-specific domain name"
  value       = aws_s3_bucket.main.bucket_regional_domain_name
}
```

**Why?** CloudFront needs the regional domain name for the origin configuration.

---

## Step 7: Import CloudFront Resources

### Initialize Terraform
```bash
cd terraform/environments/prod
terraform init
```

### Import OAC
```bash
terraform import module.cloudfront_oac.aws_cloudfront_origin_access_control.this E3B3KMNHQ684US
```

**Output**:
```
module.cloudfront_oac.aws_cloudfront_origin_access_control.this: Importing from ID "E3B3KMNHQ684US"...
module.cloudfront_oac.aws_cloudfront_origin_access_control.this: Import complete!
```

### Import CloudFront Distribution
```bash
terraform import module.cloudfront_distribution.aws_cloudfront_distribution.this E3N00R2D2NE9C5
```

**Output**:
```
module.cloudfront_distribution.aws_cloudfront_distribution.this: Importing from ID "E3N00R2D2NE9C5"...
module.cloudfront_distribution.aws_cloudfront_distribution.this: Import complete!
```

**Note**: This import triggers a CloudFront deployment which takes 2+ hours for global propagation.

---

## Step 8: Monitor CloudFront Deployment

### Check Deployment Status
```bash
# Check status every 5 minutes
while true; do
  STATUS=$(aws cloudfront get-distribution --id E3N00R2D2NE9C5 --query "Distribution.Status" --output text)
  echo "$(date): Status = $STATUS"
  if [ "$STATUS" = "Deployed" ]; then
    echo "Deployment complete!"
    break
  fi
  sleep 300
done
```

### Get Detailed Status
```bash
aws cloudfront get-distribution --id E3N00R2D2NE9C5 --query "Distribution.{Status:Status,LastModified:LastModifiedTime,InProgressInvalidationBatches:InProgressInvalidationBatches,Enabled:DistributionConfig.Enabled}" --output json
```

**Expected Output** (after 2+ hours):
```json
{
    "Status": "Deployed",
    "LastModified": "2026-02-10T23:37:11.655000+00:00",
    "InProgressInvalidationBatches": 0,
    "Enabled": true
}
```

---

## Step 9: Verify CloudFront Configuration

### Test Distribution Domain
```bash
curl -I https://d271vky579caz9.cloudfront.net
```

**Expected Headers**:
```
HTTP/2 200
x-cache: Hit from cloudfront
x-amz-cf-pop: IAD89-C1
x-amz-cf-id: ...
```

### Test Custom Domains
```bash
curl -I https://videos.mytestimony.click
curl -I https://christianconservativestoday.com
```

### Test HTTPS Redirect
```bash
curl -I http://videos.mytestimony.click
```

**Expected**: 301 redirect to https://

---

## Step 10: Verify S3 Bucket Policy

### Check Bucket Policy Includes CloudFront OAC

```bash
aws s3api get-bucket-policy --bucket my-video-downloads-bucket --query Policy --output text | jq .
```

**Expected Statement**:
```json
{
  "Sid": "AllowCloudFrontOAC",
  "Effect": "Allow",
  "Principal": {
    "Service": "cloudfront.amazonaws.com"
  },
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::my-video-downloads-bucket/*",
  "Condition": {
    "StringEquals": {
      "AWS:SourceArn": "arn:aws:cloudfront::371751795928:distribution/E3N00R2D2NE9C5"
    }
  }
}
```

**If missing**, add to S3 bucket policy in Terraform.

---

## Key Learnings

### CloudFront Deployment Time
- **Initial deployment**: 15-20 minutes
- **Updates with Terraform import**: 2+ hours
- **Reason**: Global propagation to 400+ edge locations
- **Impact**: Zero downtime - old config serves traffic during deployment

### Origin Access Control vs Origin Access Identity
- **OAC**: Modern, supports all S3 features, uses SigV4
- **OAI**: Legacy, limited S3 feature support, uses SigV2
- **Migration**: Can't directly migrate, must create new OAC

### Cache Policies
- **AWS Managed**: Pre-configured, best practices, free
- **Custom**: Full control, more complex
- **CachingOptimized**: Good default for static content

### SSL Certificates
- **Must be in us-east-1**: CloudFront requirement
- **ACM certificates**: Free, auto-renewal
- **Custom certificates**: Supported but not recommended

---

## Common Pitfalls

**Pitfall 1: Wrong origin domain name**
- **Problem**: Using bucket website endpoint instead of regional domain
- **Solution**: Use `bucket_regional_domain_name` output from S3 module

**Pitfall 2: Missing OAC in bucket policy**
- **Problem**: CloudFront can't access S3 objects
- **Solution**: Add CloudFront service principal to bucket policy

**Pitfall 3: Certificate in wrong region**
- **Problem**: ACM certificate not in us-east-1
- **Solution**: Create certificate in us-east-1 for CloudFront

**Pitfall 4: Impatient during deployment**
- **Problem**: Thinking deployment is stuck
- **Solution**: Wait 2+ hours, check status periodically

---

## Troubleshooting

### Issue: 403 Forbidden from CloudFront
**Cause**: OAC not configured in S3 bucket policy  
**Solution**: Add CloudFront service principal with SourceArn condition

### Issue: Certificate error
**Cause**: ACM certificate not in us-east-1  
**Solution**: Create new certificate in us-east-1

### Issue: Custom domain not working
**Cause**: DNS not pointing to CloudFront  
**Solution**: Create CNAME record pointing to CloudFront domain

### Issue: Deployment stuck "In Progress"
**Cause**: Normal - global propagation takes time  
**Solution**: Wait 2+ hours, check status with AWS CLI

---

## Related Files
- [CloudFront Module](../../modules/cloudfront/main.tf)
- [CloudFront OAC Module](../../modules/cloudfront-oac/main.tf)
- [S3 Module](../../modules/s3/main.tf)
- [Production Environment](../prod/main.tf)
- [Terraform Documentation](../TERRAFORM_DOCUMENTATION.md)

---

**Created**: February 10, 2026  
**Last Updated**: February 10, 2026
