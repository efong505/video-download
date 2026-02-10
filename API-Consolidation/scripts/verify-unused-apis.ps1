# verify-unused-apis.ps1
# Comprehensive verification script to check if APIs are truly unused

param(
    [int]$DaysToCheck = 30,
    [string]$Region = "us-east-1"
)

Write-Host "🔍 API Usage Verification Script" -ForegroundColor Cyan
Write-Host "Checking last $DaysToCheck days of activity...`n" -ForegroundColor Gray

# APIs suspected to be unused
$suspectedUnusedApis = @{
    "MyFirstAPI" = "97gtxp82b2"
    "MyMusicAPI" = "sljzs4mmue"
    "MyTestimony API" = "wm234jgiv3"
    "recipe-scraper-api-1" = "1lgppg87fe"
    "recipe-scraper-api-2" = "ts4xz3fs70"
    "NewsScraperAPI" = "xi6azy9cp9"
    "video-downloader-api-dup" = "qdk8y6nna6"
    "notifications-api-dup" = "ulcbf9glui"
    "storage-subscription-api-http" = "fm52xqjuz3"
}

$results = @()
$safeToDelete = @()
$needsReview = @()

# Calculate date range
$endTime = Get-Date
$startTime = $endTime.AddDays(-$DaysToCheck)

Write-Host "="*80 -ForegroundColor Cyan
Write-Host "VERIFICATION METHOD:" -ForegroundColor Yellow
Write-Host "1. Check API Gateway configuration (does it exist?)" -ForegroundColor Gray
Write-Host "2. Check CloudWatch metrics (any requests in last $DaysToCheck days?)" -ForegroundColor Gray
Write-Host "3. Check Lambda integrations (connected to any Lambda?)" -ForegroundColor Gray
Write-Host "4. Check CloudWatch logs (any log entries?)" -ForegroundColor Gray
Write-Host "5. Search HTML files (referenced in frontend?)" -ForegroundColor Gray
Write-Host "="*80 -ForegroundColor Cyan
Write-Host ""

foreach ($api in $suspectedUnusedApis.GetEnumerator()) {
    $apiName = $api.Key
    $apiId = $api.Value
    
    Write-Host "`n" + "="*80 -ForegroundColor Yellow
    Write-Host "Checking: $apiName ($apiId)" -ForegroundColor Cyan
    Write-Host "="*80 -ForegroundColor Yellow
    
    $apiInfo = @{
        Name = $apiName
        Id = $apiId
        Exists = $false
        HasTraffic = $false
        HasLambdaIntegration = $false
        HasLogs = $false
        InHTMLFiles = $false
        RequestCount = 0
        LastActivity = "Never"
        Recommendation = ""
    }
    
    # CHECK 1: Does API exist?
    Write-Host "`n[1/5] Checking if API exists..." -NoNewline
    try {
        if ($apiId -eq "fm52xqjuz3") {
            # HTTP API
            $apiDetails = aws apigatewayv2 get-api --api-id $apiId --region $Region 2>$null | ConvertFrom-Json
        } else {
            # REST API
            $apiDetails = aws apigateway get-rest-api --rest-api-id $apiId --region $Region 2>$null | ConvertFrom-Json
        }
        
        if ($apiDetails) {
            $apiInfo.Exists = $true
            Write-Host " ✅ EXISTS" -ForegroundColor Green
            Write-Host "   Name: $($apiDetails.name)" -ForegroundColor Gray
            Write-Host "   Created: $($apiDetails.createdDate)" -ForegroundColor Gray
        }
    } catch {
        Write-Host " ❌ NOT FOUND (already deleted?)" -ForegroundColor Red
        $apiInfo.Recommendation = "Already deleted or doesn't exist"
        $results += $apiInfo
        continue
    }
    
    # CHECK 2: CloudWatch Metrics - Any traffic?
    Write-Host "`n[2/5] Checking CloudWatch metrics (last $DaysToCheck days)..." -NoNewline
    try {
        $metrics = aws cloudwatch get-metric-statistics `
            --namespace "AWS/ApiGateway" `
            --metric-name "Count" `
            --dimensions "Name=ApiId,Value=$apiId" `
            --start-time $startTime.ToString("yyyy-MM-ddTHH:mm:ss") `
            --end-time $endTime.ToString("yyyy-MM-ddTHH:mm:ss") `
            --period 86400 `
            --statistics Sum `
            --region $Region 2>$null | ConvertFrom-Json
        
        if ($metrics.Datapoints -and $metrics.Datapoints.Count -gt 0) {
            $totalRequests = ($metrics.Datapoints | Measure-Object -Property Sum -Sum).Sum
            $apiInfo.RequestCount = $totalRequests
            $apiInfo.HasTraffic = $true
            $lastDatapoint = $metrics.Datapoints | Sort-Object Timestamp -Descending | Select-Object -First 1
            $apiInfo.LastActivity = $lastDatapoint.Timestamp
            Write-Host " ⚠️  HAS TRAFFIC" -ForegroundColor Yellow
            Write-Host "   Total requests: $totalRequests" -ForegroundColor Yellow
            Write-Host "   Last activity: $($apiInfo.LastActivity)" -ForegroundColor Yellow
        } else {
            Write-Host " ✅ NO TRAFFIC" -ForegroundColor Green
        }
    } catch {
        Write-Host " ✅ NO METRICS FOUND" -ForegroundColor Green
    }
    
    # CHECK 3: Lambda Integrations
    Write-Host "`n[3/5] Checking Lambda integrations..." -NoNewline
    try {
        if ($apiId -eq "fm52xqjuz3") {
            # HTTP API
            $integrations = aws apigatewayv2 get-integrations --api-id $apiId --region $Region 2>$null | ConvertFrom-Json
            if ($integrations.Items -and $integrations.Items.Count -gt 0) {
                $apiInfo.HasLambdaIntegration = $true
                Write-Host " ⚠️  HAS INTEGRATIONS" -ForegroundColor Yellow
                foreach ($integration in $integrations.Items) {
                    Write-Host "   - $($integration.IntegrationUri)" -ForegroundColor Yellow
                }
            } else {
                Write-Host " ✅ NO INTEGRATIONS" -ForegroundColor Green
            }
        } else {
            # REST API
            $resources = aws apigateway get-resources --rest-api-id $apiId --region $Region 2>$null | ConvertFrom-Json
            $hasIntegration = $false
            
            if ($resources.items) {
                foreach ($resource in $resources.items) {
                    if ($resource.resourceMethods) {
                        foreach ($method in $resource.resourceMethods.PSObject.Properties.Name) {
                            try {
                                $integration = aws apigateway get-integration `
                                    --rest-api-id $apiId `
                                    --resource-id $resource.id `
                                    --http-method $method `
                                    --region $Region 2>$null | ConvertFrom-Json
                                
                                if ($integration.uri -match "lambda") {
                                    $hasIntegration = $true
                                    $apiInfo.HasLambdaIntegration = $true
                                    Write-Host " ⚠️  HAS LAMBDA INTEGRATION" -ForegroundColor Yellow
                                    Write-Host "   - $($integration.uri)" -ForegroundColor Yellow
                                    break
                                }
                            } catch {}
                        }
                        if ($hasIntegration) { break }
                    }
                }
            }
            
            if (-not $hasIntegration) {
                Write-Host " ✅ NO LAMBDA INTEGRATIONS" -ForegroundColor Green
            }
        }
    } catch {
        Write-Host " ✅ NO INTEGRATIONS FOUND" -ForegroundColor Green
    }
    
    # CHECK 4: CloudWatch Logs
    Write-Host "`n[4/5] Checking CloudWatch logs..." -NoNewline
    try {
        $logGroupName = "/aws/apigateway/$apiId"
        $logGroups = aws logs describe-log-groups `
            --log-group-name-prefix $logGroupName `
            --region $Region 2>$null | ConvertFrom-Json
        
        if ($logGroups.logGroups -and $logGroups.logGroups.Count -gt 0) {
            $logGroup = $logGroups.logGroups[0]
            
            # Check for recent log streams
            $logStreams = aws logs describe-log-streams `
                --log-group-name $logGroup.logGroupName `
                --order-by LastEventTime `
                --descending `
                --max-items 1 `
                --region $Region 2>$null | ConvertFrom-Json
            
            if ($logStreams.logStreams -and $logStreams.logStreams.Count -gt 0) {
                $lastEventTime = [DateTimeOffset]::FromUnixTimeMilliseconds($logStreams.logStreams[0].lastEventTimestamp).DateTime
                $daysSinceLastLog = ($endTime - $lastEventTime).Days
                
                if ($daysSinceLastLog -le $DaysToCheck) {
                    $apiInfo.HasLogs = $true
                    Write-Host " ⚠️  HAS RECENT LOGS" -ForegroundColor Yellow
                    Write-Host "   Last log: $lastEventTime ($daysSinceLastLog days ago)" -ForegroundColor Yellow
                } else {
                    Write-Host " ✅ NO RECENT LOGS" -ForegroundColor Green
                    Write-Host "   Last log: $lastEventTime ($daysSinceLastLog days ago)" -ForegroundColor Gray
                }
            } else {
                Write-Host " ✅ NO LOG STREAMS" -ForegroundColor Green
            }
        } else {
            Write-Host " ✅ NO LOG GROUP" -ForegroundColor Green
        }
    } catch {
        Write-Host " ✅ NO LOGS FOUND" -ForegroundColor Green
    }
    
    # CHECK 5: HTML Files
    Write-Host "`n[5/5] Checking HTML files..." -NoNewline
    $htmlSearch = Select-String -Path "*.html" -Pattern $apiId -Recurse -ErrorAction SilentlyContinue
    if ($htmlSearch) {
        $apiInfo.InHTMLFiles = $true
        Write-Host " ⚠️  FOUND IN HTML FILES" -ForegroundColor Yellow
        foreach ($match in $htmlSearch | Select-Object -First 3) {
            Write-Host "   - $($match.Path):$($match.LineNumber)" -ForegroundColor Yellow
        }
        if ($htmlSearch.Count -gt 3) {
            Write-Host "   ... and $($htmlSearch.Count - 3) more" -ForegroundColor Yellow
        }
    } else {
        Write-Host " ✅ NOT IN HTML FILES" -ForegroundColor Green
    }
    
    # RECOMMENDATION
    Write-Host "`n📊 ANALYSIS:" -ForegroundColor Cyan
    if ($apiInfo.HasTraffic -or $apiInfo.HasLogs -or $apiInfo.InHTMLFiles) {
        $apiInfo.Recommendation = "⚠️  NEEDS REVIEW - Has activity or references"
        Write-Host "   Status: " -NoNewline
        Write-Host "NEEDS REVIEW" -ForegroundColor Yellow
        Write-Host "   Reason: " -NoNewline
        if ($apiInfo.HasTraffic) { Write-Host "Has traffic ($($apiInfo.RequestCount) requests)" -ForegroundColor Yellow }
        if ($apiInfo.HasLogs) { Write-Host "Has recent logs" -ForegroundColor Yellow }
        if ($apiInfo.InHTMLFiles) { Write-Host "Referenced in HTML files" -ForegroundColor Yellow }
        $needsReview += $apiInfo
    } else {
        $apiInfo.Recommendation = "✅ SAFE TO DELETE - No activity detected"
        Write-Host "   Status: " -NoNewline
        Write-Host "SAFE TO DELETE" -ForegroundColor Green
        Write-Host "   Reason: No traffic, no logs, no HTML references, no recent activity" -ForegroundColor Green
        $safeToDelete += $apiInfo
    }
    
    $results += $apiInfo
}

# SUMMARY REPORT
Write-Host "`n`n" + "="*80 -ForegroundColor Cyan
Write-Host "📊 VERIFICATION SUMMARY" -ForegroundColor Yellow
Write-Host "="*80 -ForegroundColor Cyan

Write-Host "`n✅ SAFE TO DELETE ($($safeToDelete.Count) APIs):" -ForegroundColor Green
if ($safeToDelete.Count -eq 0) {
    Write-Host "   None - all APIs show some activity" -ForegroundColor Gray
} else {
    foreach ($api in $safeToDelete) {
        Write-Host "   - $($api.Name) ($($api.Id))" -ForegroundColor Green
    }
}

Write-Host "`n⚠️  NEEDS REVIEW ($($needsReview.Count) APIs):" -ForegroundColor Yellow
if ($needsReview.Count -eq 0) {
    Write-Host "   None - all APIs are clearly unused" -ForegroundColor Gray
} else {
    foreach ($api in $needsReview) {
        Write-Host "   - $($api.Name) ($($api.Id))" -ForegroundColor Yellow
        Write-Host "     Requests: $($api.RequestCount) | Logs: $($api.HasLogs) | In HTML: $($api.InHTMLFiles)" -ForegroundColor Gray
    }
}

# COST SAVINGS
$monthlySavings = $safeToDelete.Count * 3.50
$annualSavings = $monthlySavings * 12

Write-Host "`n💰 POTENTIAL SAVINGS:" -ForegroundColor Cyan
Write-Host "   APIs to delete: $($safeToDelete.Count)" -ForegroundColor White
Write-Host "   Monthly savings: `$$monthlySavings" -ForegroundColor Green
Write-Host "   Annual savings: `$$annualSavings" -ForegroundColor Green

# EXPORT RESULTS
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$reportFile = "api-verification-report-$timestamp.json"
$results | ConvertTo-Json -Depth 10 | Out-File $reportFile

Write-Host "`n📄 DETAILED REPORT:" -ForegroundColor Cyan
Write-Host "   Saved to: $reportFile" -ForegroundColor White

# NEXT STEPS
Write-Host "`n🎯 NEXT STEPS:" -ForegroundColor Cyan
if ($safeToDelete.Count -gt 0) {
    Write-Host "   1. Review the report above" -ForegroundColor White
    Write-Host "   2. Run: .\delete-unused-apis.ps1 (to delete safe APIs)" -ForegroundColor White
    Write-Host "   3. Manually review APIs that need attention" -ForegroundColor White
} else {
    Write-Host "   All APIs show some activity - manual review recommended" -ForegroundColor Yellow
}

Write-Host "`n" + "="*80 -ForegroundColor Cyan
