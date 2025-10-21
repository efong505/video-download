# Deploy contributors API Lambda function
Write-Host "Deploying contributors API Lambda function..." -ForegroundColor Green

# Create zip file
Compress-Archive -Path index.py -DestinationPath function.zip -Force

# Update Lambda function
aws lambda update-function-code --function-name contributors-api --zip-file fileb://function.zip

Write-Host "Deployment complete!" -ForegroundColor Green
