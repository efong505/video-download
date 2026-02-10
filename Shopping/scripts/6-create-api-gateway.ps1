Write-Host "Creating API Gateway for products-api..." -ForegroundColor Cyan

# Create REST API
Write-Host "Creating REST API..."
$apiResult = aws apigateway create-rest-api --name "shopping-api" --region us-east-1 | ConvertFrom-Json
$apiId = $apiResult.id
Write-Host "API ID: $apiId"

# Get root resource
$resources = aws apigateway get-resources --rest-api-id $apiId --region us-east-1 | ConvertFrom-Json
$rootId = $resources.items[0].id

# Create /products resource
Write-Host "Creating /products resource..."
$productsResource = aws apigateway create-resource --rest-api-id $apiId --parent-id $rootId --path-part "products" --region us-east-1 | ConvertFrom-Json
$productsId = $productsResource.id

# Create GET method
Write-Host "Creating GET method..."
aws apigateway put-method --rest-api-id $apiId --resource-id $productsId --http-method GET --authorization-type NONE --region us-east-1

# Set up Lambda integration
Write-Host "Setting up Lambda integration..."
$lambdaArn = "arn:aws:lambda:us-east-1:371751795928:function:products-api"
$uri = "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/$lambdaArn/invocations"

aws apigateway put-integration --rest-api-id $apiId --resource-id $productsId --http-method GET --type AWS_PROXY --integration-http-method POST --uri $uri --region us-east-1

# Add Lambda permission
Write-Host "Adding Lambda permission..."
aws lambda add-permission --function-name products-api --statement-id apigateway-products --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:us-east-1:371751795928:$apiId/*/*" --region us-east-1

# Create OPTIONS method for CORS
Write-Host "Creating OPTIONS method for CORS..."
aws apigateway put-method --rest-api-id $apiId --resource-id $productsId --http-method OPTIONS --authorization-type NONE --region us-east-1

aws apigateway put-integration --rest-api-id $apiId --resource-id $productsId --http-method OPTIONS --type MOCK --request-templates '{"application/json":"{\"statusCode\":200}"}' --region us-east-1

aws apigateway put-method-response --rest-api-id $apiId --resource-id $productsId --http-method OPTIONS --status-code 200 --response-parameters "method.response.header.Access-Control-Allow-Headers=false,method.response.header.Access-Control-Allow-Methods=false,method.response.header.Access-Control-Allow-Origin=false" --region us-east-1

aws apigateway put-integration-response --rest-api-id $apiId --resource-id $productsId --http-method OPTIONS --status-code 200 --response-parameters '{\"method.response.header.Access-Control-Allow-Headers\":\"'"'"'Content-Type,Authorization'"'"'\",\"method.response.header.Access-Control-Allow-Methods\":\"'"'"'GET,OPTIONS'"'"'\",\"method.response.header.Access-Control-Allow-Origin\":\"'"'"'*'"'"'\"}' --region us-east-1

# Deploy API
Write-Host "Deploying API..."
aws apigateway create-deployment --rest-api-id $apiId --stage-name prod --region us-east-1

$endpoint = "https://$apiId.execute-api.us-east-1.amazonaws.com/prod/products"
Write-Host "`n✅ API Gateway created successfully!" -ForegroundColor Green
Write-Host "Endpoint: $endpoint"
Write-Host "`nTest with: curl `"$endpoint?action=list`""
