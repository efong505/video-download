# Import DynamoDB tables into Terraform state

$tables = @(
    @{module="dynamodb_articles"; name="articles"},
    @{module="dynamodb_users"; name="users"},
    @{module="dynamodb_news"; name="news-table"},
    @{module="dynamodb_comments"; name="comments"},
    @{module="dynamodb_video_metadata"; name="video-metadata"},
    @{module="dynamodb_resources"; name="resources-table"},
    @{module="dynamodb_contributors"; name="contributors"},
    @{module="dynamodb_rate_limits"; name="rate-limits"}
)

Write-Host "=== Importing DynamoDB Tables ===" -ForegroundColor Cyan
Write-Host ""

foreach ($table in $tables) {
    Write-Host "Importing $($table.name)..." -ForegroundColor Yellow
    
    terraform import "module.$($table.module).aws_dynamodb_table.this" $table.name
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Successfully imported $($table.name)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Failed to import $($table.name)" -ForegroundColor Red
    }
    Write-Host ""
}

Write-Host "Import complete!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Run 'terraform plan' to verify the import" -ForegroundColor Yellow
