# Deploy auto-cache-monitor Lambda with EventBridge trigger
# Cost: $0 (Lambda free tier covers this)

$ErrorActionPreference = "Stop"

Write-Host "=== Deploying Auto Cache Monitor ===" -ForegroundColor Cyan

# Create deployment package
Write-Host "`nCreating deployment package..." -ForegroundColor Yellow
cd auto-cache-monitor
Compress-Archive -Path index.py -DestinationPath function.zip -Force
cd ..

# Create/update Lambda function
Write-Host "Deploying Lambda function..." -ForegroundColor Yellow
try {
    aws lambda get-function --function-name auto-cache-monitor --region us-east-1 2>$null
    $exists = $true
} catch {
    $exists = $false
}

if ($exists) {
    aws lambda update-function-code `
        --function-name auto-cache-monitor `
        --zip-file fileb://auto-cache-monitor/function.zip `
        --region us-east-1
    Write-Host "Lambda function updated" -ForegroundColor Green
} else {
    aws lambda create-function `
        --function-name auto-cache-monitor `
        --runtime python3.12 `
        --role arn:aws:iam::371751795928:role/lambda-execution-role `
        --handler index.lambda_handler `
        --zip-file fileb://auto-cache-monitor/function.zip `
        --timeout 60 `
        --memory-size 256 `
        --region us-east-1
    Write-Host "Lambda function created" -ForegroundColor Green
}

# Add CloudWatch, ElastiCache, and API Gateway permissions to Lambda role
Write-Host "`nAdding IAM permissions..." -ForegroundColor Yellow

@'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:GetMetricStatistics",
        "elasticache:DescribeCacheClusters",
        "elasticache:CreateCacheCluster",
        "apigateway:GET",
        "apigateway:PATCH"
      ],
      "Resource": "*"
    }
  ]
}
'@ | Out-File -FilePath auto-cache-policy.json -Encoding utf8

aws iam put-role-policy `
    --role-name lambda-execution-role `
    --policy-name AutoCacheMonitorPolicy `
    --policy-document file://auto-cache-policy.json
Remove-Item auto-cache-policy.json
Write-Host "IAM permissions added" -ForegroundColor Green

# Create EventBridge rule (runs daily at 2 AM UTC)
Write-Host "`nCreating EventBridge rule..." -ForegroundColor Yellow
aws events put-rule `
    --name auto-cache-monitor-daily `
    --schedule-expression "cron(0 2 * * ? *)" `
    --state ENABLED `
    --region us-east-1

# Add Lambda permission for EventBridge
aws lambda add-permission `
    --function-name auto-cache-monitor `
    --statement-id EventBridgeInvoke `
    --action lambda:InvokeFunction `
    --principal events.amazonaws.com `
    --source-arn arn:aws:events:us-east-1:371751795928:rule/auto-cache-monitor-daily `
    --region us-east-1 2>$null

# Add Lambda as target
aws events put-targets `
    --rule auto-cache-monitor-daily `
    --targets '[{"Id":"1","Arn":"arn:aws:lambda:us-east-1:371751795928:function:auto-cache-monitor"}]' `
    --region us-east-1

Write-Host "`n=== Deployment Complete ===" -ForegroundColor Green
Write-Host "`nAuto-monitoring enabled:" -ForegroundColor Cyan
Write-Host "  - Runs daily at 2 AM UTC" -ForegroundColor White
Write-Host "  - Checks DynamoDB reads and API requests" -ForegroundColor White
Write-Host "  - Auto-enables ElastiCache at 2M reads/day" -ForegroundColor White
Write-Host "  - Auto-enables API cache at 500K requests/day" -ForegroundColor White
Write-Host "  - Cost: `$0 (Lambda free tier)" -ForegroundColor Green

Write-Host "`nTest now:" -ForegroundColor Yellow
Write-Host "  aws lambda invoke --function-name auto-cache-monitor response.json --region us-east-1" -ForegroundColor White
Write-Host "  cat response.json" -ForegroundColor White

Write-Host "`nView logs:" -ForegroundColor Yellow
Write-Host "  aws logs tail /aws/lambda/auto-cache-monitor --follow --region us-east-1" -ForegroundColor White
