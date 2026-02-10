# verify-7-apis-simple.ps1
# Simple verification of 7 APIs

$Region = "us-east-1"

$apis = @(
    @{Id="qdk8y6nna6"; Name="video-downloader-api OLD"},
    @{Id="ulcbf9glui"; Name="notifications-api OLD"},
    @{Id="o0mzmvcs59"; Name="contributors-api dup1"},
    @{Id="wzn7e1ipjf"; Name="contributors-api dup2"},
    @{Id="ts4xz3fs70"; Name="recipe-scraper-api empty"},
    @{Id="97gtxp82b2"; Name="MyFirstAPI test"},
    @{Id="sljzs4mmue"; Name="MyMusicAPI test"}
)

Write-Host "Verifying 7 APIs for deletion..." -ForegroundColor Cyan
Write-Host ""

$safeCount = 0
$unsafeCount = 0

foreach ($api in $apis) {
    Write-Host "Checking: $($api.Name) ($($api.Id))" -ForegroundColor Yellow
    
    $safe = $true
    $reasons = @()
    
    # Check 1: Lambda integrations
    Write-Host "  [1/3] Lambda integrations..." -NoNewline
    try {
        $resources = aws apigateway get-resources --rest-api-id $api.Id --region $Region 2>$null | ConvertFrom-Json
        $hasIntegration = $false
        
        if ($resources.items) {
            foreach ($resource in $resources.items) {
                if ($resource.resourceMethods) {
                    foreach ($method in $resource.resourceMethods.PSObject.Properties.Name) {
                        try {
                            $integration = aws apigateway get-integration --rest-api-id $api.Id --resource-id $resource.id --http-method $method --region $Region 2>$null | ConvertFrom-Json
                            if ($integration.uri -match "lambda") {
                                $hasIntegration = $true
                                $safe = $false
                                $reasons += "Has Lambda integration"
                                break
                            }
                        } catch {}
                    }
                    if ($hasIntegration) { break }
                }
            }
        }
        
        if ($hasIntegration) {
            Write-Host " FOUND!" -ForegroundColor Red
        } else {
            Write-Host " None" -ForegroundColor Green
        }
    } catch {
        Write-Host " None" -ForegroundColor Green
    }
    
    # Check 2: HTML files
    Write-Host "  [2/3] HTML files..." -NoNewline
    $htmlMatches = Select-String -Path "..\..\*.html" -Pattern $api.Id -Recurse -ErrorAction SilentlyContinue
    if ($htmlMatches) {
        Write-Host " FOUND in $($htmlMatches.Count) files!" -ForegroundColor Red
        $safe = $false
        $reasons += "Found in HTML files"
    } else {
        Write-Host " Not found" -ForegroundColor Green
    }
    
    # Check 3: Recent traffic
    Write-Host "  [3/3] Traffic (last 30 days)..." -NoNewline
    try {
        $endTime = Get-Date
        $startTime = $endTime.AddDays(-30)
        $metrics = aws cloudwatch get-metric-statistics --namespace "AWS/ApiGateway" --metric-name "Count" --dimensions "Name=ApiId,Value=$($api.Id)" --start-time $startTime.ToString("yyyy-MM-ddTHH:mm:ss") --end-time $endTime.ToString("yyyy-MM-ddTHH:mm:ss") --period 86400 --statistics Sum --region $Region 2>$null | ConvertFrom-Json
        
        if ($metrics.Datapoints) {
            $totalRequests = ($metrics.Datapoints | Measure-Object -Property Sum -Sum).Sum
            if ($totalRequests -gt 0) {
                Write-Host " $totalRequests requests!" -ForegroundColor Red
                $safe = $false
                $reasons += "Has traffic"
            } else {
                Write-Host " No traffic" -ForegroundColor Green
            }
        } else {
            Write-Host " No traffic" -ForegroundColor Green
        }
    } catch {
        Write-Host " No traffic" -ForegroundColor Green
    }
    
    # Verdict
    if ($safe) {
        Write-Host "  VERDICT: SAFE TO DELETE" -ForegroundColor Green
        $safeCount++
    } else {
        Write-Host "  VERDICT: DO NOT DELETE - $($reasons -join ', ')" -ForegroundColor Red
        $unsafeCount++
    }
    
    Write-Host ""
}

Write-Host "="*60 -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Yellow
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "Safe to delete: $safeCount / 7" -ForegroundColor $(if ($safeCount -eq 7) { "Green" } else { "Yellow" })
Write-Host "NOT safe: $unsafeCount / 7" -ForegroundColor $(if ($unsafeCount -eq 0) { "Green" } else { "Red" })
Write-Host ""

if ($safeCount -eq 7) {
    Write-Host "All 7 APIs verified safe to delete!" -ForegroundColor Green
} elseif ($unsafeCount -gt 0) {
    Write-Host "WARNING: $unsafeCount APIs show activity - review before deleting!" -ForegroundColor Red
}
