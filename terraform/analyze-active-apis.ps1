# Analyze which API Gateway IDs are actually used in production code
Write-Host "=== API Gateway Usage Analysis ===" -ForegroundColor Cyan

# Get all API Gateway IDs from AWS
Write-Host "`nFetching API Gateways from AWS..." -ForegroundColor Yellow
$apis = aws apigateway get-rest-apis --query 'items[*].[id,name]' --output json | ConvertFrom-Json

# Search all HTML and JS files for API Gateway URLs
$searchPath = "c:\Users\Ed\Documents\Programming\AWS\Downloader"
$files = Get-ChildItem -Path $searchPath -Include *.html,*.js -Recurse -File | 
    Where-Object { $_.FullName -notmatch '\\node_modules\\|\\\.git\\|\\Downloader_backup' }

Write-Host "`nScanning $($files.Count) files for API Gateway usage..." -ForegroundColor Yellow

# Track API usage
$apiUsage = @{}
foreach ($api in $apis) {
    $apiId = $api[0]
    $apiName = $api[1]
    $apiUsage[$apiId] = @{
        Name = $apiName
        Files = @()
        Count = 0
    }
}

# Scan files
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if ($content) {
        foreach ($apiId in $apiUsage.Keys) {
            if ($content -match $apiId) {
                $apiUsage[$apiId].Files += $file.Name
                $apiUsage[$apiId].Count++
            }
        }
    }
}

# Display results
Write-Host "`n=== ACTIVE APIs (Used in Code) ===" -ForegroundColor Green
$activeApis = $apiUsage.GetEnumerator() | Where-Object { $_.Value.Count -gt 0 } | Sort-Object { $_.Value.Count } -Descending
foreach ($api in $activeApis) {
    Write-Host "`n$($api.Value.Name) ($($api.Key))" -ForegroundColor Cyan
    Write-Host "  Used in $($api.Value.Count) files" -ForegroundColor White
    Write-Host "  Files: $($api.Value.Files -join ', ')" -ForegroundColor Gray
}

Write-Host "`n=== UNUSED APIs (Not Found in Code) ===" -ForegroundColor Red
$unusedApis = $apiUsage.GetEnumerator() | Where-Object { $_.Value.Count -eq 0 } | Sort-Object { $_.Value.Name }
foreach ($api in $unusedApis) {
    Write-Host "  $($api.Value.Name) ($($api.Key))" -ForegroundColor Yellow
}

# Check CloudWatch metrics for actual traffic
Write-Host "`n=== Checking CloudWatch Metrics (Last 7 Days) ===" -ForegroundColor Cyan
$endTime = Get-Date
$startTime = $endTime.AddDays(-7)

foreach ($api in $unusedApis) {
    $apiId = $api.Key
    $apiName = $api.Value.Name
    
    try {
        $metrics = aws cloudwatch get-metric-statistics `
            --namespace AWS/ApiGateway `
            --metric-name Count `
            --dimensions Name=ApiName,Value=$apiName `
            --start-time $startTime.ToString("yyyy-MM-ddTHH:mm:ss") `
            --end-time $endTime.ToString("yyyy-MM-ddTHH:mm:ss") `
            --period 604800 `
            --statistics Sum `
            --output json 2>$null | ConvertFrom-Json
        
        if ($metrics.Datapoints -and $metrics.Datapoints.Count -gt 0) {
            $sum = ($metrics.Datapoints | Measure-Object -Property Sum -Sum).Sum
            if ($sum -gt 0) {
                Write-Host "  $apiName ($apiId): $sum requests" -ForegroundColor Yellow
            }
        }
    } catch {
        # Ignore errors
    }
}

Write-Host "`n=== DUPLICATE APIs ===" -ForegroundColor Magenta
$duplicates = $apiUsage.GetEnumerator() | Group-Object { $_.Value.Name } | Where-Object { $_.Count -gt 1 }
foreach ($group in $duplicates) {
    Write-Host "`n$($group.Name):" -ForegroundColor Cyan
    foreach ($api in $group.Group) {
        $status = if ($api.Value.Count -gt 0) { "ACTIVE ($($api.Value.Count) files)" } else { "UNUSED" }
        Write-Host "  $($api.Key) - $status" -ForegroundColor $(if ($api.Value.Count -gt 0) { "Green" } else { "Red" })
    }
}

Write-Host "`n=== SUMMARY ===" -ForegroundColor Cyan
Write-Host "Total APIs: $($apis.Count)" -ForegroundColor White
Write-Host "Active (used in code): $($activeApis.Count)" -ForegroundColor Green
Write-Host "Unused (not in code): $($unusedApis.Count)" -ForegroundColor Red
Write-Host "Duplicates: $($duplicates.Count)" -ForegroundColor Magenta

Write-Host "`n=== RECOMMENDATION ===" -ForegroundColor Yellow
Write-Host "1. Delete UNUSED APIs with no CloudWatch traffic" -ForegroundColor White
Write-Host "2. For DUPLICATES, keep the ACTIVE one, delete others" -ForegroundColor White
Write-Host "3. Consolidate remaining ACTIVE APIs into unified gateway" -ForegroundColor White
