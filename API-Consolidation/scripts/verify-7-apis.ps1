# verify-7-apis.ps1
# Comprehensive verification of the 7 APIs marked for deletion

param([string]$Region = "us-east-1")

$apisToVerify = @{
    "qdk8y6nna6" = "video-downloader-api (OLD duplicate)"
    "ulcbf9glui" = "notifications-api (OLD duplicate)"
    "o0mzmvcs59" = "contributors-api (duplicate 1)"
    "wzn7e1ipjf" = "contributors-api (duplicate 2)"
    "ts4xz3fs70" = "recipe-scraper-api (empty version)"
    "97gtxp82b2" = "MyFirstAPI (test)"
    "sljzs4mmue" = "MyMusicAPI (test)"
}

Write-Host "="*80 -ForegroundColor Cyan
Write-Host "🔍 COMPREHENSIVE VERIFICATION OF 7 APIs" -ForegroundColor Yellow
Write-Host "="*80 -ForegroundColor Cyan
Write-Host ""

$results = @()

foreach ($api in $apisToVerify.GetEnumerator()) {
    $apiId = $api.Key
    $apiName = $api.Value
    
    Write-Host "`n" + "="*80 -ForegroundColor Yellow
    Write-Host "API: $apiName" -ForegroundColor Cyan
    Write-Host "ID: $apiId" -ForegroundColor Gray
    Write-Host "="*80 -ForegroundColor Yellow
    
    $result = @{
        Id = $apiId
        Name = $apiName
        Exists = $false
        HasResources = $false
        HasMethods = 0
        HasIntegrations = $false
        InHTMLFiles = $false
        HasTraffic = $false
        HasLogs = $false
        SafeToDelete = $true
        Reason = @()
    }
    
    # CHECK 1: Does API exist?
    Write-Host "`n[1/5] Checking if API exists..." -NoNewline
    try {
        $apiDetails = aws apigateway get-rest-api --rest-api-id $apiId --region $Region 2>$null | ConvertFrom-Json
        if ($apiDetails) {
            $result.Exists = $true
            Write-Host " ✅ EXISTS" -ForegroundColor Green
            Write-Host "      Name: $($apiDetails.name)" -ForegroundColor Gray
            Write-Host "      Created: $($apiDetails.createdDate)" -ForegroundColor Gray
        }
    } catch {
        Write-Host " ❌ NOT FOUND" -ForegroundColor Red
        $result.Reason += 'API does not exist (already deleted?)'
        $results += $result
        continue
    }
    
    # CHECK 2: Resources and Methods
    Write-Host "`n[2/5] Checking resources and methods..." -NoNewline
    try {
        $resources = aws apigateway get-resources --rest-api-id $apiId --region $Region 2>$null | ConvertFrom-Json
        
        if ($resources.items) {
            $result.HasResources = $true
            $methodCount = 0
            $integrationCount = 0
            
            foreach ($resource in $resources.items) {
                if ($resource.resourceMethods) {
                    $methodCount += $resource.resourceMethods.PSObject.Properties.Count
                    
                    # Check each method for integrations
                    foreach ($method in $resource.resourceMethods.PSObject.Properties.Name) {
                        try {
                            $integration = aws apigateway get-integration `
                                --rest-api-id $apiId `
                                --resource-id $resource.id `
                                --http-method $method `
                                --region $Region 2>$null | ConvertFrom-Json
                            
                            if ($integration.uri) {
                                $integrationCount++
                                if ($integration.uri -match "lambda") {
                                    $result.HasIntegrations = $true
                                    Write-Host " ⚠️  HAS LAMBDA INTEGRATION!" -ForegroundColor Red
                                    Write-Host "      Resource: $($resource.path)" -ForegroundColor Yellow
                                    Write-Host "      Method: $method" -ForegroundColor Yellow
                                    Write-Host "      Lambda: $($integration.uri)" -ForegroundColor Yellow
                                    $result.SafeToDelete = $false
                                    $result.Reason += "Has Lambda integration: $($integration.uri)"
                                }
                            }
                        } catch {}
                    }
                }
            }
            
            $result.HasMethods = $methodCount
            
            if (-not $result.HasIntegrations) {
                Write-Host " ✅ NO INTEGRATIONS" -ForegroundColor Green
                Write-Host "      Resources: $($resources.items.Count)" -ForegroundColor Gray
                Write-Host "      Methods: $methodCount" -ForegroundColor Gray
            }
        } else {
            Write-Host " ✅ NO RESOURCES" -ForegroundColor Green
        }
    } catch {
        Write-Host " ✅ NO RESOURCES" -ForegroundColor Green
    }
    
    # CHECK 3: HTML Files
    Write-Host "`n[3/5] Searching HTML files..." -NoNewline
    $htmlMatches = Select-String -Path "..\..\*.html" -Pattern $apiId -Recurse -ErrorAction SilentlyContinue
    if ($htmlMatches) {
        $result.InHTMLFiles = $true
        $result.SafeToDelete = $false
        Write-Host " ⚠️  FOUND IN HTML!" -ForegroundColor Red
        foreach ($match in $htmlMatches | Select-Object -First 3) {
            Write-Host "      $($match.Path):$($match.LineNumber)" -ForegroundColor Yellow
        }
        $result.Reason += "Found in $($htmlMatches.Count) HTML file(s)"
    } else {
        Write-Host " ✅ NOT IN HTML" -ForegroundColor Green
    }
    
    # CHECK 4: CloudWatch Metrics (Last 30 days)
    Write-Host "`n[4/5] Checking CloudWatch metrics (last 30 days)..." -NoNewline
    try {
        $endTime = Get-Date
        $startTime = $endTime.AddDays(-30)
        
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
            if ($totalRequests -gt 0) {
                $result.HasTraffic = $true
                $result.SafeToDelete = $false
                Write-Host " ⚠️  HAS TRAFFIC!" -ForegroundColor Red
                Write-Host "      Total requests: $totalRequests" -ForegroundColor Yellow
                $result.Reason += "Has traffic: $totalRequests requests in last 30 days"
            } else {
                Write-Host " ✅ NO TRAFFIC" -ForegroundColor Green
            }
        } else {
            Write-Host " ✅ NO TRAFFIC" -ForegroundColor Green
        }
    } catch {
        Write-Host " ✅ NO METRICS" -ForegroundColor Green
    }
    
    # CHECK 5: CloudWatch Logs
    Write-Host "`n[5/5] Checking CloudWatch logs..." -NoNewline
    try {
        $logGroupName = "/aws/apigateway/$apiId"
        $logGroups = aws logs describe-log-groups `
            --log-group-name-prefix $logGroupName `
            --region $Region 2>$null | ConvertFrom-Json
        
        if ($logGroups.logGroups -and $logGroups.logGroups.Count -gt 0) {
            $logStreams = aws logs describe-log-streams `
                --log-group-name $logGroups.logGroups[0].logGroupName `
                --order-by LastEventTime `
                --descending `
                --max-items 1 `
                --region $Region 2>$null | ConvertFrom-Json
            
            if ($logStreams.logStreams -and $logStreams.logStreams.Count -gt 0) {
                $lastEventTime = [DateTimeOffset]::FromUnixTimeMilliseconds($logStreams.logStreams[0].lastEventTimestamp).DateTime
                $daysSince = ($endTime - $lastEventTime).Days
                
                if ($daysSince -le 30) {
                    $result.HasLogs = $true
                    $result.SafeToDelete = $false
                    Write-Host " ⚠️  HAS RECENT LOGS!" -ForegroundColor Red
                    Write-Host "      Last log: $lastEventTime ($daysSince days ago)" -ForegroundColor Yellow
                    $result.Reason += "Has logs from $daysSince days ago"
                } else {
                    Write-Host " ✅ NO RECENT LOGS" -ForegroundColor Green
                    Write-Host "      Last log: $daysSince days ago" -ForegroundColor Gray
                }
            } else {
                Write-Host " ✅ NO LOG STREAMS" -ForegroundColor Green
            }
        } else {
            Write-Host " ✅ NO LOG GROUP" -ForegroundColor Green
        }
    } catch {
        Write-Host " ✅ NO LOGS" -ForegroundColor Green
    }
    
    # VERDICT
    Write-Host "`n📊 VERDICT: " -NoNewline
    if ($result.SafeToDelete) {
        Write-Host "✅ SAFE TO DELETE" -ForegroundColor Green
        Write-Host "   No activity, integrations, or references found" -ForegroundColor Gray
    } else {
        Write-Host "⚠️  DO NOT DELETE!" -ForegroundColor Red
        Write-Host "   Reasons:" -ForegroundColor Yellow
        foreach ($reason in $result.Reason) {
            Write-Host "   - $reason" -ForegroundColor Yellow
        }
    }
    
    $results += $result
}

# FINAL SUMMARY
Write-Host "`n`n" + "="*80 -ForegroundColor Cyan
Write-Host "📊 FINAL VERIFICATION SUMMARY" -ForegroundColor Yellow
Write-Host "="*80 -ForegroundColor Cyan

$safeToDelete = $results | Where-Object { $_.SafeToDelete -eq $true }
$notSafe = $results | Where-Object { $_.SafeToDelete -eq $false }

Write-Host "`n✅ SAFE TO DELETE ($($safeToDelete.Count) APIs):" -ForegroundColor Green
if ($safeToDelete.Count -eq 0) {
    Write-Host "   None - all APIs show activity or usage" -ForegroundColor Yellow
} else {
    foreach ($api in $safeToDelete) {
        Write-Host "   ✓ $($api.Name)" -ForegroundColor Green
        Write-Host "     ID: $($api.Id)" -ForegroundColor Gray
    }
}

Write-Host "`n⚠️  DO NOT DELETE ($($notSafe.Count) APIs):" -ForegroundColor Red
if ($notSafe.Count -eq 0) {
    Write-Host "   None - all APIs are safe to delete" -ForegroundColor Green
} else {
    foreach ($api in $notSafe) {
        Write-Host "   ✗ $($api.Name)" -ForegroundColor Red
        Write-Host "     ID: $($api.Id)" -ForegroundColor Gray
        Write-Host "     Reasons:" -ForegroundColor Yellow
        foreach ($reason in $api.Reason) {
            Write-Host "       - $reason" -ForegroundColor Yellow
        }
    }
}

# Save detailed report
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$reportFile = "verification-report-7-apis-$timestamp.json"
$results | ConvertTo-Json -Depth 10 | Out-File $reportFile

Write-Host "`n📄 Detailed report saved to: $reportFile" -ForegroundColor Cyan

# RECOMMENDATION
Write-Host "`n🎯 RECOMMENDATION:" -ForegroundColor Cyan
if ($safeToDelete.Count -eq 7) {
    Write-Host "   All 7 APIs are confirmed safe to delete!" -ForegroundColor Green
    Write-Host "   Run: .\delete-7-apis.ps1" -ForegroundColor White
} elseif ($safeToDelete.Count -gt 0) {
    Write-Host "   $($safeToDelete.Count) APIs are safe to delete" -ForegroundColor Yellow
    Write-Host "   $($notSafe.Count) APIs should NOT be deleted" -ForegroundColor Red
    Write-Host "   Review the reasons above before proceeding" -ForegroundColor White
} else {
    Write-Host "   ⚠️  STOP! None of the 7 APIs are safe to delete!" -ForegroundColor Red
    Write-Host "   All show signs of usage - do NOT proceed with deletion" -ForegroundColor Red
}

Write-Host "`n" + "="*80 -ForegroundColor Cyan
