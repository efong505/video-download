# check-specific-apis.ps1
# Quick check for storage-subscription and recipe-scraper APIs

param([string]$Region = "us-east-1")

Write-Host "🔍 Checking Specific APIs" -ForegroundColor Cyan
Write-Host ""

# Check 1: storage-subscription-api
Write-Host "="*80 -ForegroundColor Yellow
Write-Host "1. storage-subscription-api (fm52xqjuz3)" -ForegroundColor Cyan
Write-Host "="*80 -ForegroundColor Yellow

Write-Host "`nChecking HTTP API integrations..." -ForegroundColor Gray
$integrations = aws apigatewayv2 get-integrations --api-id fm52xqjuz3 --region $Region 2>$null | ConvertFrom-Json

if ($integrations.Items -and $integrations.Items.Count -gt 0) {
    Write-Host "✅ Has $($integrations.Items.Count) integration(s):" -ForegroundColor Green
    foreach ($int in $integrations.Items) {
        Write-Host "   - $($int.IntegrationUri)" -ForegroundColor White
    }
} else {
    Write-Host "❌ No integrations found" -ForegroundColor Red
}

Write-Host "`nSearching HTML files for fm52xqjuz3..." -ForegroundColor Gray
$htmlMatches = Select-String -Path "..\..\*.html" -Pattern "fm52xqjuz3" -Recurse -ErrorAction SilentlyContinue
if ($htmlMatches) {
    Write-Host "✅ Found in $($htmlMatches.Count) location(s):" -ForegroundColor Green
    foreach ($match in $htmlMatches | Select-Object -First 5) {
        Write-Host "   - $($match.Path):$($match.LineNumber)" -ForegroundColor White
    }
} else {
    Write-Host "❌ Not found in HTML files" -ForegroundColor Red
}

# Check 2: recipe-scraper-api versions
Write-Host "`n"
Write-Host "="*80 -ForegroundColor Yellow
Write-Host '2. recipe-scraper-api (2 versions)' -ForegroundColor Cyan
Write-Host "="*80 -ForegroundColor Yellow

$recipeApis = @{
    'ts4xz3fs70' = 'Version 1 (16:01:46)'
    '1lgppg87fe' = 'Version 2 (16:03:16)'
}

foreach ($api in $recipeApis.GetEnumerator()) {
    Write-Host "`nChecking $($api.Value) - $($api.Key)..." -ForegroundColor Gray
    
    # Check resources
    $resources = aws apigateway get-resources --rest-api-id $api.Key --region $Region 2>$null | ConvertFrom-Json
    
    if ($resources.items) {
        $methodCount = 0
        foreach ($resource in $resources.items) {
            if ($resource.resourceMethods) {
                $methodCount += $resource.resourceMethods.PSObject.Properties.Count
            }
        }
        
        if ($methodCount -gt 0) {
            Write-Host "   ✅ Has $methodCount method(s) configured" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️  Has resources but no methods" -ForegroundColor Yellow
        }
    } else {
        Write-Host "   ❌ No resources configured" -ForegroundColor Red
    }
    
    # Check HTML usage
    $htmlMatches = Select-String -Path "..\..\*.html" -Pattern $api.Key -Recurse -ErrorAction SilentlyContinue
    if ($htmlMatches) {
        Write-Host "   ✅ Found in HTML files" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Not in HTML files" -ForegroundColor Red
    }
}

# Check 3: Search for subscription patterns
Write-Host "`n"
Write-Host "="*80 -ForegroundColor Yellow
Write-Host "3. Subscription API Usage Pattern" -ForegroundColor Cyan
Write-Host "="*80 -ForegroundColor Yellow

Write-Host "`nSearching for subscription-related API calls..." -ForegroundColor Gray
$subPatterns = Select-String -Path "..\..\*.html" -Pattern "subscription.*execute-api" -Recurse -ErrorAction SilentlyContinue

if ($subPatterns) {
    Write-Host "Found subscription API calls:" -ForegroundColor White
    $uniqueApis = @{}
    foreach ($match in $subPatterns) {
        if ($match.Line -match '([a-z0-9]{10})\.execute-api') {
            $apiId = $matches[1]
            if (-not $uniqueApis.ContainsKey($apiId)) {
                $uniqueApis[$apiId] = @()
            }
            $uniqueApis[$apiId] += $match.Path
        }
    }
    
    foreach ($api in $uniqueApis.GetEnumerator()) {
        Write-Host "`n   API: $($api.Key)" -ForegroundColor Cyan
        Write-Host "   Used in: $($api.Value.Count) file(s)" -ForegroundColor Gray
        $api.Value | Select-Object -Unique | ForEach-Object {
            Write-Host "     - $_" -ForegroundColor White
        }
    }
}

# Summary
Write-Host "`n"
Write-Host "="*80 -ForegroundColor Cyan
Write-Host "📊 SUMMARY & RECOMMENDATIONS" -ForegroundColor Yellow
Write-Host "="*80 -ForegroundColor Cyan

Write-Host "`n1. storage-subscription-api (fm52xqjuz3):"
if ($integrations.Items -or $htmlMatches) {
    Write-Host "   ✅ KEEP - Has integrations or HTML references" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  VERIFY - No obvious usage found" -ForegroundColor Yellow
    Write-Host "   Check if replaced by email-subscription-api (niexv1rw75)" -ForegroundColor Gray
}

Write-Host "`n2. recipe-scraper-api:"
Write-Host "   ⚠️  VERIFY which version is active for news.mytestimony.click" -ForegroundColor Yellow
Write-Host "   Check news.mytestimony.click configuration" -ForegroundColor Gray

Write-Host "`n3. Next Steps:"
Write-Host "   - Check news.mytestimony.click to see which recipe-scraper it uses" -ForegroundColor White
Write-Host "   - Verify storage-subscription-api is not replaced by newer APIs" -ForegroundColor White
Write-Host "   - Run full verification: .\verify-unused-apis.ps1" -ForegroundColor White

Write-Host "`n" + "="*80 -ForegroundColor Cyan
