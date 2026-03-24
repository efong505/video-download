# Check for the scheduled article in DynamoDB
Write-Host "Checking for 'test-scheduled again number 23' article..." -ForegroundColor Cyan

# Query DynamoDB for articles with title containing "test-scheduled"
Write-Host "Scanning DynamoDB articles table..." -ForegroundColor Yellow
$allArticles = aws dynamodb scan --table-name articles --profile ekewaka --region us-east-1 --output json | ConvertFrom-Json

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error scanning DynamoDB" -ForegroundColor Red
    exit 1
}

Write-Host "Total articles in database: $($allArticles.Items.Count)" -ForegroundColor Cyan

$filtered = $allArticles.Items | Where-Object { $_.title.S -like "*test-scheduled*" }

if ($filtered.Count -gt 0) {
    Write-Host "`nFound $($filtered.Count) article(s) with 'test-scheduled' in title" -ForegroundColor Green
    foreach ($item in $filtered) {
        Write-Host "`n=== Article Found ===" -ForegroundColor Green
        Write-Host "Title: $($item.title.S)"
        Write-Host "Article ID: $($item.article_id.S)"
        Write-Host "Status: $($item.status.S)"
        Write-Host "Visibility: $($item.visibility.S)"
        Write-Host "Category: $($item.category.S)"
        Write-Host "Created: $($item.created_at.S)"
        if ($item.scheduled_publish) {
            Write-Host "Scheduled Publish: $($item.scheduled_publish.S)" -ForegroundColor Magenta
        }
    }
} else {
    Write-Host "`nNo articles found with 'test-scheduled' in the title" -ForegroundColor Red
    Write-Host "The article may have been deleted or never saved to the database." -ForegroundColor Yellow
}
