$functionName = "orders-api"
$zipFile = "orders-api.zip"

Write-Host "Deploying orders-api Lambda..." -ForegroundColor Cyan

Set-Location ../orders_api

if (Test-Path $zipFile) { Remove-Item $zipFile }
Compress-Archive -Path index.py -DestinationPath $zipFile

$exists = aws lambda get-function --function-name $functionName 2>$null
if ($LASTEXITCODE -eq 0) {
    aws lambda update-function-code --function-name $functionName --zip-file fileb://$zipFile
} else {
    aws lambda create-function --function-name $functionName --runtime python3.12 --role arn:aws:iam::371751795928:role/lambda-execution-role --handler index.lambda_handler --zip-file fileb://$zipFile --timeout 30
}

Remove-Item $zipFile
Set-Location ../scripts

Write-Host "Deployment complete!" -ForegroundColor Green
