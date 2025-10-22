$states = aws dynamodb scan --table-name states --region us-east-1 --query "Items[?summary_guide_url!=null].state_name" --output json | ConvertFrom-Json

Write-Host "`nStates with Summary Guides:" -ForegroundColor Green
Write-Host "============================`n" -ForegroundColor Green
$states | Sort-Object | ForEach-Object { Write-Host "  - $_" }
Write-Host "`nTotal: $($states.Count) states`n" -ForegroundColor Cyan
