# Deploy PayPal IPN Handler Lambda
$functionName = "paypal-ipn-handler"
$zipFile = "paypal-ipn-handler.zip"

Write-Host "Creating deployment package..." -ForegroundColor Cyan
Set-Location ..
Set-Location paypal_ipn_handler
if (Test-Path $zipFile) { Remove-Item $zipFile }
Compress-Archive -Path index.py -DestinationPath $zipFile

Write-Host "Deploying to Lambda..." -ForegroundColor Cyan
aws lambda update-function-code --function-name $functionName --zip-file fileb://$zipFile

Write-Host "Deployment complete!" -ForegroundColor Green
Set-Location ..
Set-Location scripts
