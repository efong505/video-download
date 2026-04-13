# Create payload with proper event structure
@'
{
  "httpMethod": "POST",
  "body": "{\"url\": \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\", \"output_name\": \"test-video.mp4\", \"title\": \"Test Video\", \"owner\": \"system\"}",
  "headers": {
    "Content-Type": "application/json"
  }
}
'@ | Out-File -FilePath payload.json -Encoding ASCII -NoNewline

# Invoke Lambda
Write-Host "Testing router with YouTube URL..." -ForegroundColor Green
aws lambda invoke `
  --function-name router `
  --profile child-account `
  --region us-east-1 `
  --payload file://payload.json `
  response.json

# Show response
Write-Host "`nLambda Response:" -ForegroundColor Green
Get-Content response.json | ConvertFrom-Json | ConvertTo-Json -Depth 10

# Clean up
Remove-Item payload.json -ErrorAction SilentlyContinue
