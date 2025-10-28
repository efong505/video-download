# Setup /tags API Gateway endpoint - Simple version
$API_ID = "wfeds5lejb"
$LAMBDA_ARN = "arn:aws:lambda:us-east-1:371751795928:function:video-tag-api"
$REGION = "us-east-1"

Write-Host "Setting up /tags API endpoint..." -ForegroundColor Yellow

# Get root resource ID
$ROOT_ID = (aws apigateway get-resources --rest-api-id $API_ID --query "items[?path=='/'].id" --output text)
Write-Host "Root ID: $ROOT_ID" -ForegroundColor Gray

# Create /tags resource
Write-Host "Creating /tags resource..." -ForegroundColor Cyan
$result = aws apigateway create-resource --rest-api-id $API_ID --parent-id $ROOT_ID --path-part "tags"
$TAGS_ID = ($result | ConvertFrom-Json).id
Write-Host "Tags resource ID: $TAGS_ID" -ForegroundColor Gray

# Create POST method with Lambda proxy integration
Write-Host "Creating POST method..." -ForegroundColor Cyan
aws apigateway put-method --rest-api-id $API_ID --resource-id $TAGS_ID --http-method POST --authorization-type NONE --no-api-key-required
aws apigateway put-integration --rest-api-id $API_ID --resource-id $TAGS_ID --http-method POST --type AWS_PROXY --integration-http-method POST --uri "arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/${LAMBDA_ARN}/invocations"

# Create GET method with Lambda proxy integration
Write-Host "Creating GET method..." -ForegroundColor Cyan
aws apigateway put-method --rest-api-id $API_ID --resource-id $TAGS_ID --http-method GET --authorization-type NONE --no-api-key-required
aws apigateway put-integration --rest-api-id $API_ID --resource-id $TAGS_ID --http-method GET --type AWS_PROXY --integration-http-method POST --uri "arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/${LAMBDA_ARN}/invocations"

# Create PUT method with Lambda proxy integration
Write-Host "Creating PUT method..." -ForegroundColor Cyan
aws apigateway put-method --rest-api-id $API_ID --resource-id $TAGS_ID --http-method PUT --authorization-type NONE --no-api-key-required
aws apigateway put-integration --rest-api-id $API_ID --resource-id $TAGS_ID --http-method PUT --type AWS_PROXY --integration-http-method POST --uri "arn:aws:apigateway:${REGION}:lambda:path/2015-03-31/functions/${LAMBDA_ARN}/invocations"

# Create OPTIONS method for CORS
Write-Host "Creating OPTIONS method for CORS..." -ForegroundColor Cyan
aws apigateway put-method --rest-api-id $API_ID --resource-id $TAGS_ID --http-method OPTIONS --authorization-type NONE --no-api-key-required
aws apigateway put-integration --rest-api-id $API_ID --resource-id $TAGS_ID --http-method OPTIONS --type MOCK --request-templates "{\`"application/json\`":\`"{\\\`"statusCode\\\`": 200}\`"}"
aws apigateway put-method-response --rest-api-id $API_ID --resource-id $TAGS_ID --http-method OPTIONS --status-code 200 --response-parameters "method.response.header.Access-Control-Allow-Headers=false,method.response.header.Access-Control-Allow-Methods=false,method.response.header.Access-Control-Allow-Origin=false"
aws apigateway put-integration-response --rest-api-id $API_ID --resource-id $TAGS_ID --http-method OPTIONS --status-code 200 --response-parameters "method.response.header.Access-Control-Allow-Headers='Content-Type,Authorization',method.response.header.Access-Control-Allow-Methods='GET,POST,PUT,OPTIONS',method.response.header.Access-Control-Allow-Origin='*'"

# Grant API Gateway permission to invoke Lambda
Write-Host "Granting API Gateway permissions..." -ForegroundColor Cyan
try {
    aws lambda add-permission --function-name video-tag-api --statement-id apigateway-tags-invoke --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:${REGION}:371751795928:${API_ID}/*/*/tags" 2>$null
} catch {
    Write-Host "Permission may already exist" -ForegroundColor Gray
}

# Deploy to prod stage
Write-Host "Deploying to prod stage..." -ForegroundColor Cyan
aws apigateway create-deployment --rest-api-id $API_ID --stage-name prod --description "Added /tags endpoint"

Write-Host "`n✅ /tags endpoint configured!" -ForegroundColor Green
Write-Host "Endpoint: https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/tags" -ForegroundColor White
