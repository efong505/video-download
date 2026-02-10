# Implementation Guide: API Gateway Consolidation

## Prerequisites

- AWS CLI configured with admin credentials
- Domain: `christianconservativestoday.com` in Route 53
- PowerShell 7+ or Bash
- Git installed

---

## WEEK 1: API GATEWAY CONSOLIDATION

### Step 1: Request ACM Certificate (5 minutes)

```bash
# Request SSL certificate for api subdomain
aws acm request-certificate \
  --domain-name api.christianconservativestoday.com \
  --validation-method DNS \
  --region us-east-1

# Note the CertificateArn from output
# Example: arn:aws:acm:us-east-1:123456789012:certificate/abc123...
```

**Action Required**: Add DNS validation records in Route 53 (AWS Console will show these)

Wait 5-10 minutes for certificate validation.

---

### Step 2: Create Unified REST API (10 minutes)

```bash
# Create the unified API
aws apigateway create-rest-api \
  --name "unified-api" \
  --description "Consolidated API for Christian Conservatives Today" \
  --endpoint-configuration types=REGIONAL \
  --region us-east-1

# Note the API ID from output
# Example: abc123xyz
```

**Save this API ID** - you'll use it throughout the migration.

---

### Step 3: Get Root Resource ID (2 minutes)

```bash
# Replace YOUR_API_ID with the ID from Step 2
export API_ID=YOUR_API_ID

# Get root resource ID
aws apigateway get-resources \
  --rest-api-id $API_ID \
  --region us-east-1

# Note the root resource ID (usually looks like: a1b2c3d4e5)
export ROOT_ID=YOUR_ROOT_ID
```

---

### Step 4: Create Base Path Resources (30 minutes)

Run this script to create all base paths:

```bash
#!/bin/bash
# create-resources.sh

API_ID="YOUR_API_ID"
ROOT_ID="YOUR_ROOT_ID"

# Array of all service paths
PATHS=(
  "admin"
  "auth"
  "articles"
  "videos"
  "news"
  "resources"
  "contributors"
  "comments"
  "tags"
  "prayer"
  "events"
  "email"
  "ministry"
  "notifications"
  "url-analysis"
  "paypal"
  "download"
)

# Create each resource
for path in "${PATHS[@]}"; do
  echo "Creating resource: /$path"
  aws apigateway create-resource \
    --rest-api-id $API_ID \
    --parent-id $ROOT_ID \
    --path-part $path \
    --region us-east-1
done

echo "All resources created!"
```

**PowerShell version**:
```powershell
# create-resources.ps1
$API_ID = "YOUR_API_ID"
$ROOT_ID = "YOUR_ROOT_ID"

$paths = @(
  "admin", "auth", "articles", "videos", "news", "resources",
  "contributors", "comments", "tags", "prayer", "events",
  "email", "ministry", "notifications", "url-analysis", "paypal", "download"
)

foreach ($path in $paths) {
  Write-Host "Creating resource: /$path"
  aws apigateway create-resource `
    --rest-api-id $API_ID `
    --parent-id $ROOT_ID `
    --path-part $path `
    --region us-east-1
}

Write-Host "All resources created!"
```

---

### Step 5: Create Proxy Resources (20 minutes)

Each base path needs a `{proxy+}` resource to catch all sub-paths:

```bash
#!/bin/bash
# create-proxy-resources.sh

API_ID="YOUR_API_ID"

# Get all resource IDs
RESOURCES=$(aws apigateway get-resources --rest-api-id $API_ID --region us-east-1)

# For each base path, create {proxy+}
for path in admin auth articles videos news resources contributors comments tags prayer events email ministry notifications url-analysis paypal download; do
  # Get resource ID for this path
  RESOURCE_ID=$(echo $RESOURCES | jq -r ".items[] | select(.path == \"/$path\") | .id")
  
  echo "Creating proxy for /$path (ID: $RESOURCE_ID)"
  
  aws apigateway create-resource \
    --rest-api-id $API_ID \
    --parent-id $RESOURCE_ID \
    --path-part "{proxy+}" \
    --region us-east-1
done
```

---

### Step 6: Map Lambda Functions (1 hour)

For each service, create the integration:

```bash
#!/bin/bash
# map-lambda-functions.sh

API_ID="YOUR_API_ID"
REGION="us-east-1"
ACCOUNT_ID="YOUR_ACCOUNT_ID"

# Get account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# Array of path -> Lambda function mappings
declare -A MAPPINGS=(
  ["admin"]="admin_api"
  ["auth"]="auth_api"
  ["articles"]="articles_api"
  ["videos"]="video_list_api"
  ["news"]="news_api"
  ["resources"]="resources_api"
  ["contributors"]="contributors_api"
  ["comments"]="comments_api"
  ["tags"]="tag_api"
  ["prayer"]="prayer_api"
  ["events"]="events_api"
  ["email"]="email_subscription_api"
  ["ministry"]="ministry_tools_api"
  ["notifications"]="notifications_api"
  ["url-analysis"]="url_analysis_api"
  ["paypal"]="paypal_billing_api"
  ["download"]="downloader"
)

# Get all resources
RESOURCES=$(aws apigateway get-resources --rest-api-id $API_ID --region $REGION)

for path in "${!MAPPINGS[@]}"; do
  LAMBDA_NAME="${MAPPINGS[$path]}"
  
  # Get proxy resource ID
  PROXY_ID=$(echo $RESOURCES | jq -r ".items[] | select(.path == \"/$path/{proxy+}\") | .id")
  
  echo "Mapping /$path/{proxy+} to Lambda: $LAMBDA_NAME"
  
  # Create ANY method
  aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $PROXY_ID \
    --http-method ANY \
    --authorization-type NONE \
    --region $REGION
  
  # Create Lambda integration
  aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $PROXY_ID \
    --http-method ANY \
    --type AWS_PROXY \
    --integration-http-method POST \
    --uri "arn:aws:apigateway:$REGION:lambda:path/2015-03-31/functions/arn:aws:lambda:$REGION:$ACCOUNT_ID:function:$LAMBDA_NAME/invocations" \
    --region $REGION
  
  # Grant API Gateway permission to invoke Lambda
  aws lambda add-permission \
    --function-name $LAMBDA_NAME \
    --statement-id "apigateway-unified-$path" \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:$REGION:$ACCOUNT_ID:$API_ID/*/*" \
    --region $REGION
done

echo "All Lambda functions mapped!"
```

---

### Step 7: Enable CORS (15 minutes)

```bash
#!/bin/bash
# enable-cors.sh

API_ID="YOUR_API_ID"
REGION="us-east-1"

# Get all proxy resources
RESOURCES=$(aws apigateway get-resources --rest-api-id $API_ID --region $REGION)
PROXY_IDS=$(echo $RESOURCES | jq -r '.items[] | select(.path | contains("{proxy+}")) | .id')

for PROXY_ID in $PROXY_IDS; do
  echo "Enabling CORS for resource: $PROXY_ID"
  
  # Create OPTIONS method
  aws apigateway put-method \
    --rest-api-id $API_ID \
    --resource-id $PROXY_ID \
    --http-method OPTIONS \
    --authorization-type NONE \
    --region $REGION
  
  # Create mock integration
  aws apigateway put-integration \
    --rest-api-id $API_ID \
    --resource-id $PROXY_ID \
    --http-method OPTIONS \
    --type MOCK \
    --request-templates '{"application/json": "{\"statusCode\": 200}"}' \
    --region $REGION
  
  # Create method response
  aws apigateway put-method-response \
    --rest-api-id $API_ID \
    --resource-id $PROXY_ID \
    --http-method OPTIONS \
    --status-code 200 \
    --response-parameters '{"method.response.header.Access-Control-Allow-Headers": true, "method.response.header.Access-Control-Allow-Methods": true, "method.response.header.Access-Control-Allow-Origin": true}' \
    --region $REGION
  
  # Create integration response
  aws apigateway put-integration-response \
    --rest-api-id $API_ID \
    --resource-id $PROXY_ID \
    --http-method OPTIONS \
    --status-code 200 \
    --response-parameters '{"method.response.header.Access-Control-Allow-Headers": "\"Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token\"", "method.response.header.Access-Control-Allow-Methods": "\"GET,POST,PUT,DELETE,OPTIONS\"", "method.response.header.Access-Control-Allow-Origin": "\"*\""}' \
    --region $REGION
done

echo "CORS enabled for all resources!"
```

---

### Step 8: Deploy API (5 minutes)

```bash
# Create deployment
aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name prod \
  --stage-description "Production stage" \
  --description "Initial deployment of unified API" \
  --region us-east-1

echo "API deployed to: https://$API_ID.execute-api.us-east-1.amazonaws.com/prod"
```

---

### Step 9: Configure Custom Domain (20 minutes)

```bash
# Create custom domain
aws apigateway create-domain-name \
  --domain-name api.christianconservativestoday.com \
  --certificate-arn YOUR_CERTIFICATE_ARN \
  --endpoint-configuration types=REGIONAL \
  --region us-east-1

# Create base path mapping
aws apigateway create-base-path-mapping \
  --domain-name api.christianconservativestoday.com \
  --rest-api-id $API_ID \
  --stage prod \
  --region us-east-1

# Get the target domain name for Route 53
aws apigateway get-domain-name \
  --domain-name api.christianconservativestoday.com \
  --region us-east-1 \
  --query regionalDomainName
```

---

### Step 10: Update Route 53 (10 minutes)

```bash
# Get hosted zone ID
ZONE_ID=$(aws route53 list-hosted-zones-by-name \
  --dns-name christianconservativestoday.com \
  --query "HostedZones[0].Id" \
  --output text | cut -d'/' -f3)

# Get API Gateway domain name
API_DOMAIN=$(aws apigateway get-domain-name \
  --domain-name api.christianconservativestoday.com \
  --region us-east-1 \
  --query regionalDomainName \
  --output text)

# Create Route 53 record
cat > change-batch.json <<EOF
{
  "Changes": [{
    "Action": "CREATE",
    "ResourceRecordSet": {
      "Name": "api.christianconservativestoday.com",
      "Type": "CNAME",
      "TTL": 300,
      "ResourceRecords": [{"Value": "$API_DOMAIN"}]
    }
  }]
}
EOF

aws route53 change-resource-record-sets \
  --hosted-zone-id $ZONE_ID \
  --change-batch file://change-batch.json

echo "DNS record created! Wait 5-10 minutes for propagation."
```

---

### Step 11: Test Unified API (30 minutes)

```bash
# Test each endpoint
curl https://api.christianconservativestoday.com/articles
curl https://api.christianconservativestoday.com/videos
curl https://api.christianconservativestoday.com/news
curl https://api.christianconservativestoday.com/auth/health

# Test with authentication
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  https://api.christianconservativestoday.com/admin/users
```

---

## WEEK 2: GITHUB ACTIONS CI/CD

See `GITHUB_ACTIONS_SETUP.md` for detailed CI/CD implementation.

---

## Rollback Plan

If anything goes wrong:

```bash
# Keep old APIs running
# Update frontend to use old URLs
# Delete new unified API
aws apigateway delete-rest-api --rest-api-id $API_ID --region us-east-1

# Delete custom domain
aws apigateway delete-domain-name \
  --domain-name api.christianconservativestoday.com \
  --region us-east-1

# Delete Route 53 record
# (Use AWS Console or CLI)
```

---

## Next Steps

1. Complete Week 1 steps above
2. Test all endpoints thoroughly
3. Move to Week 2: GitHub Actions setup
4. Update frontend to use new API domain
5. Monitor for 1 week
6. Delete old APIs

---

**Questions?** Check `API_MAPPING.md` for URL mappings or `GITHUB_ACTIONS_SETUP.md` for CI/CD details.
