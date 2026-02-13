# API Gateway Staging + Custom Domains + Blue/Green Implementation Guide

## Overview

This guide provides step-by-step instructions for implementing staging environments, custom API domains, and blue/green Lambda deployments for the Christian Conservative Platform.

**Status**: 🔜 PLANNED  
**Estimated Duration**: 6-9 hours  
**Risk Level**: Medium  
**Prerequisites**: Phases 1-8 complete

---

## Architecture

### Current State
```
API Gateway (diz6ceeb22)
└── /prod stage
    ├── https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/auth
    ├── https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod/articles
    └── ... (14 endpoints)
    
Lambda Functions (18)
└── Direct invocation (no versioning, no aliases)
```

### Target State
```
API Gateway (diz6ceeb22)
├── /prod stage → api.christianconservativestoday.com
│   └── All 14 endpoints
└── /staging stage → api-staging.christianconservativestoday.com
    └── All 14 endpoints (same Lambda functions)

Lambda Functions (18)
├── Versioning enabled (publish = true)
├── "live" alias → current stable version
└── Blue/Green: Deploy v2 → Test → Update alias → Instant cutover
```

---

## Part 1: Staging Stage + Custom Domains

### Step 1: Create ACM Certificate Module (15 minutes)

**1.1 Create Module Directory**
```bash
mkdir -p terraform/modules/acm-certificate
cd terraform/modules/acm-certificate
```

**1.2 Create main.tf**
```hcl
resource "aws_acm_certificate" "this" {
  domain_name       = var.domain_name
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = var.tags
}

resource "aws_acm_certificate_validation" "this" {
  certificate_arn         = aws_acm_certificate.this.arn
  validation_record_fqdns = [for record in aws_route53_record.validation : record.fqdn]
}

resource "aws_route53_record" "validation" {
  for_each = {
    for dvo in aws_acm_certificate.this.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = var.hosted_zone_id
}
```

**1.3 Create variables.tf**
```hcl
variable "domain_name" {
  type        = string
  description = "Domain name for ACM certificate"
}

variable "hosted_zone_id" {
  type        = string
  description = "Route53 hosted zone ID for DNS validation"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags to apply to certificate"
}
```

**1.4 Create outputs.tf**
```hcl
output "certificate_arn" {
  value       = aws_acm_certificate_validation.this.certificate_arn
  description = "ARN of validated ACM certificate"
}

output "domain_name" {
  value       = aws_acm_certificate.this.domain_name
  description = "Domain name of certificate"
}
```

---

### Step 2: Request ACM Certificates (15 minutes)

**2.1 Add Route53 Data Source to main.tf**
```hcl
# Get Route53 hosted zone
data "aws_route53_zone" "main" {
  name         = "christianconservativestoday.com."
  private_zone = false
}
```

**2.2 Add Certificate Modules**
```hcl
# Production API certificate
module "acm_api_prod" {
  source = "../../modules/acm-certificate"

  domain_name    = "api.christianconservativestoday.com"
  hosted_zone_id = data.aws_route53_zone.main.zone_id

  tags = {
    Environment = "production"
    Purpose     = "API Gateway Custom Domain"
  }
}

# Staging API certificate
module "acm_api_staging" {
  source = "../../modules/acm-certificate"

  domain_name    = "api-staging.christianconservativestoday.com"
  hosted_zone_id = data.aws_route53_zone.main.zone_id

  tags = {
    Environment = "staging"
    Purpose     = "API Gateway Custom Domain"
  }
}
```

**2.3 Apply Certificates**
```bash
cd terraform/environments/prod
terraform init
terraform plan
terraform apply -target=module.acm_api_prod -target=module.acm_api_staging
```

**2.4 Wait for Validation (5-10 minutes)**
```bash
# Monitor certificate status
aws acm describe-certificate \
  --certificate-arn $(terraform output -raw acm_api_prod_arn) \
  --query 'Certificate.Status'

# Should show: "ISSUED"
```

---

### Step 3: Add Staging Stage (10 minutes)

**3.1 Update API Gateway Module**

Edit `terraform/modules/api-gateway/main.tf`:
```hcl
# Add staging stage resource
resource "aws_api_gateway_stage" "staging" {
  count = var.create_staging_stage ? 1 : 0

  deployment_id = aws_api_gateway_deployment.this.id
  rest_api_id   = aws_api_gateway_rest_api.this.id
  stage_name    = "staging"

  tags = merge(
    var.tags,
    {
      Stage = "staging"
    }
  )
}
```

Edit `terraform/modules/api-gateway/variables.tf`:
```hcl
variable "create_staging_stage" {
  type        = bool
  default     = false
  description = "Create staging stage in addition to prod"
}
```

Edit `terraform/modules/api-gateway/outputs.tf`:
```hcl
output "staging_invoke_url" {
  value       = var.create_staging_stage ? "https://${aws_api_gateway_rest_api.this.id}.execute-api.${data.aws_region.current.name}.amazonaws.com/staging" : null
  description = "Staging stage invoke URL"
}
```

**3.2 Enable Staging in main.tf**
```hcl
module "unified_api" {
  source = "../../modules/api-gateway"

  api_name              = "ministry-platform-api"
  api_description       = "Unified API for Christian Conservative Platform"
  stage_name            = "prod"
  create_staging_stage  = true  # Add this line
}
```

**3.3 Apply Staging Stage**
```bash
terraform plan -target=module.unified_api
terraform apply -target=module.unified_api
```

**3.4 Test Staging**
```bash
curl https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/staging/auth
# Should return same response as prod
```

---

### Step 4: Create Custom Domain Module (15 minutes)

**4.1 Create Module Directory**
```bash
mkdir -p terraform/modules/api-gateway-domain
cd terraform/modules/api-gateway-domain
```

**4.2 Create main.tf**
```hcl
data "aws_region" "current" {}

resource "aws_api_gateway_domain_name" "this" {
  domain_name              = var.domain_name
  regional_certificate_arn = var.certificate_arn

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = var.tags
}

resource "aws_api_gateway_base_path_mapping" "this" {
  api_id      = var.api_id
  stage_name  = var.stage_name
  domain_name = aws_api_gateway_domain_name.this.domain_name
}

resource "aws_route53_record" "this" {
  zone_id = var.hosted_zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_api_gateway_domain_name.this.regional_domain_name
    zone_id                = aws_api_gateway_domain_name.this.regional_zone_id
    evaluate_target_health = false
  }
}
```

**4.3 Create variables.tf**
```hcl
variable "domain_name" {
  type        = string
  description = "Custom domain name"
}

variable "certificate_arn" {
  type        = string
  description = "ACM certificate ARN"
}

variable "api_id" {
  type        = string
  description = "API Gateway REST API ID"
}

variable "stage_name" {
  type        = string
  description = "API Gateway stage name"
}

variable "hosted_zone_id" {
  type        = string
  description = "Route53 hosted zone ID"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Tags to apply"
}
```

**4.4 Create outputs.tf**
```hcl
output "domain_name" {
  value       = aws_api_gateway_domain_name.this.domain_name
  description = "Custom domain name"
}

output "regional_domain_name" {
  value       = aws_api_gateway_domain_name.this.regional_domain_name
  description = "Regional domain name for Route53 alias"
}

output "cloudfront_domain_name" {
  value       = aws_api_gateway_domain_name.this.cloudfront_domain_name
  description = "CloudFront domain name"
}
```

---

### Step 5: Create Custom Domains (15 minutes)

**5.1 Add Custom Domain Modules to main.tf**
```hcl
# Production custom domain
module "api_domain_prod" {
  source = "../../modules/api-gateway-domain"

  domain_name     = "api.christianconservativestoday.com"
  certificate_arn = module.acm_api_prod.certificate_arn
  api_id          = module.unified_api.api_id
  stage_name      = "prod"
  hosted_zone_id  = data.aws_route53_zone.main.zone_id

  tags = {
    Environment = "production"
  }
}

# Staging custom domain
module "api_domain_staging" {
  source = "../../modules/api-gateway-domain"

  domain_name     = "api-staging.christianconservativestoday.com"
  certificate_arn = module.acm_api_staging.certificate_arn
  api_id          = module.unified_api.api_id
  stage_name      = "staging"
  hosted_zone_id  = data.aws_route53_zone.main.zone_id

  tags = {
    Environment = "staging"
  }
}
```

**5.2 Apply Custom Domains**
```bash
terraform plan
terraform apply
```

**5.3 Wait for DNS Propagation (5-10 minutes)**
```bash
# Check DNS resolution
dig api.christianconservativestoday.com
dig api-staging.christianconservativestoday.com
```

**5.4 Test Custom Domains**
```bash
# Test staging
curl https://api-staging.christianconservativestoday.com/auth

# Test production
curl https://api.christianconservativestoday.com/auth
```

---

### Step 6: Update Frontend (30 minutes)

**6.1 Gradual Migration Strategy**

Update frontend API base URL with feature flag:
```javascript
// config.js or similar
const USE_CUSTOM_DOMAIN = false; // Start with false

const API_BASE_URL = USE_CUSTOM_DOMAIN
  ? 'https://api.christianconservativestoday.com'
  : 'https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod';

export { API_BASE_URL };
```

**6.2 Test with Feature Flag**
1. Enable flag for yourself only
2. Test all functionality
3. Enable for 10% of users
4. Monitor for errors
5. Enable for 100%

**6.3 Final Cutover**
```javascript
// Remove feature flag
const API_BASE_URL = 'https://api.christianconservativestoday.com';
```

---

## Part 2: Lambda Versioning + Blue/Green

### Step 7: Enable Lambda Versioning (30 minutes)

**7.1 Update Lambda Module**

Edit `terraform/modules/lambda/main.tf`:
```hcl
resource "aws_lambda_function" "this" {
  function_name = var.function_name
  runtime       = var.runtime
  handler       = var.handler
  role          = var.role_arn
  memory_size   = var.memory_size
  timeout       = var.timeout
  filename      = var.filename
  layers        = var.layers
  
  publish = var.enable_versioning  # Add this line

  environment {
    variables = var.environment_variables
  }

  lifecycle {
    ignore_changes = [filename, last_modified]
  }
}

# Add alias resource
resource "aws_lambda_alias" "live" {
  count = var.enable_versioning ? 1 : 0

  name             = "live"
  function_name    = aws_lambda_function.this.function_name
  function_version = var.alias_version != "" ? var.alias_version : aws_lambda_function.this.version
}
```

Edit `terraform/modules/lambda/variables.tf`:
```hcl
variable "enable_versioning" {
  type        = bool
  default     = false
  description = "Enable Lambda versioning and create live alias"
}

variable "alias_version" {
  type        = string
  default     = ""
  description = "Specific version for alias (empty = latest published version)"
}
```

Edit `terraform/modules/lambda/outputs.tf`:
```hcl
output "alias_arn" {
  value       = var.enable_versioning ? aws_lambda_alias.live[0].arn : null
  description = "ARN of live alias"
}

output "alias_name" {
  value       = var.enable_versioning ? aws_lambda_alias.live[0].name : null
  description = "Name of live alias"
}

output "version" {
  value       = aws_lambda_function.this.version
  description = "Published version number"
}
```

**7.2 Enable Versioning for Test Function**

Update one function in main.tf (start with auth-api):
```hcl
module "lambda_auth_api" {
  source = "../../modules/lambda"

  function_name      = "auth-api"
  runtime            = "python3.12"
  handler            = "index.lambda_handler"
  memory_size        = 128
  timeout            = 30
  role_arn           = "arn:aws:iam::371751795928:role/lambda-execution-role"
  enable_versioning  = true  # Add this line

  environment_variables = {}
}
```

**7.3 Apply Versioning**
```bash
terraform plan -target=module.lambda_auth_api
terraform apply -target=module.lambda_auth_api
```

**7.4 Verify Alias**
```bash
aws lambda get-alias --function-name auth-api --name live
# Should show version 1
```

---

### Step 8: Update API Gateway Integrations (45 minutes)

**8.1 Update Integration Module**

Edit `terraform/modules/api-gateway-lambda-integration/main.tf`:
```hcl
data "aws_region" "current" {}

resource "aws_lambda_permission" "this" {
  statement_id  = "AllowAPIGatewayInvoke-${var.path_part}-${var.http_method}"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
  
  # Add qualifier for alias
  qualifier = var.lambda_alias_name != "" ? var.lambda_alias_name : null
}

resource "aws_api_gateway_integration" "this" {
  rest_api_id             = var.api_id
  resource_id             = aws_api_gateway_resource.this.id
  http_method             = aws_api_gateway_method.this.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  
  # Use alias-qualified ARN if provided
  uri = var.lambda_alias_name != "" ? 
    "arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/${var.lambda_function_arn}:${var.lambda_alias_name}/invocations" :
    "arn:aws:apigateway:${data.aws_region.current.name}:lambda:path/2015-03-31/functions/${var.lambda_function_arn}/invocations"
}
```

Edit `terraform/modules/api-gateway-lambda-integration/variables.tf`:
```hcl
variable "lambda_alias_name" {
  type        = string
  default     = ""
  description = "Lambda alias name (empty = no alias)"
}
```

**8.2 Update Test Integration**

Update auth endpoint in main.tf:
```hcl
module "api_auth" {
  source = "../../modules/api-gateway-lambda-integration"

  api_id               = module.unified_api.api_id
  root_resource_id     = module.unified_api.root_resource_id
  path_part            = "auth"
  http_method          = "ANY"
  lambda_function_name = module.lambda_auth_api.function_name
  lambda_function_arn  = module.lambda_auth_api.function_arn
  lambda_alias_name    = module.lambda_auth_api.alias_name  # Add this line
  enable_cors          = true
}
```

**8.3 Apply Integration Update**
```bash
terraform plan -target=module.api_auth
terraform apply -target=module.api_auth
```

**8.4 Test Alias Integration**
```bash
curl https://api.christianconservativestoday.com/auth
# Should work via alias
```

**8.5 Roll Out to All Functions**

Once auth-api works, enable for all 18 functions:
1. Add `enable_versioning = true` to all Lambda modules
2. Add `lambda_alias_name = module.lambda_*.alias_name` to all integrations
3. Apply changes

---

### Step 9: Blue/Green Deployment Process

**9.1 Deploy New Version**
```bash
cd Downloader/auth_api
zip -r function.zip index.py

aws lambda update-function-code \
  --function-name auth-api \
  --zip-file fileb://function.zip \
  --publish
```

**9.2 Test New Version**
```bash
# Get new version number
NEW_VERSION=$(aws lambda list-versions-by-function \
  --function-name auth-api \
  --query 'Versions[-1].Version' \
  --output text)

# Test new version directly
aws lambda invoke \
  --function-name auth-api:$NEW_VERSION \
  --payload '{"test": "data"}' \
  response.json
```

**9.3 Promote to Live (Blue → Green)**
```bash
aws lambda update-alias \
  --function-name auth-api \
  --name live \
  --function-version $NEW_VERSION
```

**9.4 Rollback if Needed (Green → Blue)**
```bash
# Get previous version
OLD_VERSION=$((NEW_VERSION - 1))

aws lambda update-alias \
  --function-name auth-api \
  --name live \
  --function-version $OLD_VERSION
```

---

## Rollback Procedures

### DNS Rollback (5 minutes)
```bash
# Delete Route53 records
terraform destroy -target=module.api_domain_prod.aws_route53_record.this
terraform destroy -target=module.api_domain_staging.aws_route53_record.this

# Frontend falls back to execute-api endpoint
```

### Lambda Rollback (Instant)
```bash
# Revert alias to previous version
aws lambda update-alias \
  --function-name FUNCTION_NAME \
  --name live \
  --function-version PREVIOUS_VERSION
```

---

## Validation Checklist

- [ ] ACM certificates issued
- [ ] Staging stage accessible
- [ ] Custom domains resolve
- [ ] All 14 endpoints work on api.christianconservativestoday.com
- [ ] All 14 endpoints work on api-staging.christianconservativestoday.com
- [ ] Lambda versioning enabled
- [ ] Aliases created
- [ ] API Gateway uses alias-qualified ARNs
- [ ] Blue/green deployment tested
- [ ] Rollback tested
- [ ] Frontend migrated
- [ ] Zero downtime achieved

---

**Status**: 🔜 PLANNED  
**Next Steps**: Execute Part 1, validate, then execute Part 2  
**Estimated Completion**: Week 13
