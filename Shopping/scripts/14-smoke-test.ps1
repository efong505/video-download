# Week 9: Smoke Test All Shopping APIs
$base = "https://ydq9xzya5d.execute-api.us-east-1.amazonaws.com/prod"
$pass = 0; $fail = 0

function Test-Endpoint($name, $url, $method="GET", $body=$null) {
    try {
        $params = @{Uri=$url; Method=$method; UseBasicParsing=$true; TimeoutSec=10}
        if ($body) { $params['ContentType']='application/json'; $params['Body']=$body }
        $r = Invoke-WebRequest @params
        $preview = ($r.Content | ConvertFrom-Json | ConvertTo-Json -Compress).Substring(0, [Math]::Min(80, ($r.Content | ConvertFrom-Json | ConvertTo-Json -Compress).Length))
        Write-Host "  PASS  $name ($($r.StatusCode)) - $preview" -ForegroundColor Green
        $script:pass++
    } catch {
        $code = $_.Exception.Response.StatusCode.value__
        $msg = $_.ErrorDetails.Message
        Write-Host "  FAIL  $name ($code) - $msg" -ForegroundColor Red
        $script:fail++
    }
}

Write-Host "`n=== SHOPPING SYSTEM SMOKE TEST ===" -ForegroundColor Cyan
Write-Host "Base: $base`n"

Write-Host "--- Products API ---" -ForegroundColor Yellow
Test-Endpoint "List Products" "$base/products?action=list&limit=3"
Test-Endpoint "Search Products" "$base/products?action=search&q=book"
Test-Endpoint "Get Product" "$base/products?action=get&product_id=book-paperback-001"

Write-Host "`n--- Reviews API ---" -ForegroundColor Yellow
Test-Endpoint "List Reviews" "$base/reviews?action=list&product_id=book-paperback-001"

Write-Host "`n--- Orders API ---" -ForegroundColor Yellow
Test-Endpoint "List Orders" "$base/orders?action=list&user_id=guest"

Write-Host "`n--- Tracking API ---" -ForegroundColor Yellow
Test-Endpoint "Popular Products" "$base/tracking?action=popular"
Test-Endpoint "Recommendations" "$base/tracking?action=recommendations&session_id=smoke-test"
Test-Endpoint "Watchlist" "$base/tracking?action=watchlist&user_id=smoke-test"
Test-Endpoint "Track View" "$base/tracking?action=track-view" "POST" '{"product_id":"smoke-test","product_name":"Smoke Test","product_price":9.99,"product_category":"test","session_id":"smoke-test"}'
Test-Endpoint "Track Cart Add" "$base/tracking?action=track-cart-add" "POST" '{"product_id":"smoke-test","session_id":"smoke-test"}'

Write-Host "`n--- Marketing API ---" -ForegroundColor Yellow
Test-Endpoint "Stats" "$base/marketing?action=stats"
Test-Endpoint "Get Preferences" "$base/marketing?action=preferences-get&user_id=smoke-test"
Test-Endpoint "Run Scans" "$base/marketing?action=run-scans" "POST"

Write-Host "`n=== RESULTS ===" -ForegroundColor Cyan
$total = $pass + $fail
Write-Host "  $pass/$total passed" -ForegroundColor $(if($fail -eq 0){"Green"}else{"Yellow"})
if ($fail -gt 0) { Write-Host "  $fail FAILED" -ForegroundColor Red }
else { Write-Host "  All endpoints healthy!" -ForegroundColor Green }

# Clean up smoke test data
Write-Host "`nCleaning up smoke test data..." -ForegroundColor Gray
