# Create payload with proper encoding
@'
{"test": true}
'@ | Out-File -FilePath payload.json -Encoding ASCII -NoNewline

# Invoke Lambda
aws lambda invoke `
  --function-name router `
  --profile child-account `
  --region us-east-1 `
  --payload file://payload.json `
  response.json

# Show response
Write-Host "`nLambda Response:" -ForegroundColor Green
Get-Content response.json

# Clean up
Remove-Item payload.json -ErrorAction SilentlyContinue
