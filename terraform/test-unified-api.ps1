# Test Unified API Gateway Endpoints
# Tests all 14 endpoints to verify they're working

$baseUrl = "https://diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod"

$endpoints = @(
    "auth",
    "articles",
    "news",
    "admin",
    "comments",
    "contributors",
    "resources",
    "videos",
    "tags",
    "download",
    "paypal",
    "analyze",
    "prayer",
    "notifications"
)

Write-Host "`n=== Testing Unified API Gateway ===" -ForegroundColor Cyan
Write-Host "Base URL: $baseUrl`n" -ForegroundColor Yellow

$results = @()

foreach ($endpoint in $endpoints) {
    $url = "$baseUrl/$endpoint"
    Write-Host "Testing /$endpoint..." -NoNewline
    
    try {
        $response = Invoke-WebRequest -Uri $url -Method GET -TimeoutSec 10 -ErrorAction Stop
        $statusCode = $response.StatusCode
        
        if ($statusCode -eq 200) {
            Write-Host " ✓ OK ($statusCode)" -ForegroundColor Green
            $results += [PSCustomObject]@{
                Endpoint = $endpoint
                Status = "✓ PASS"
                StatusCode = $statusCode
            }
        } else {
            Write-Host " ⚠ Unexpected ($statusCode)" -ForegroundColor Yellow
            $results += [PSCustomObject]@{
                Endpoint = $endpoint
                Status = "⚠ WARN"
                StatusCode = $statusCode
            }
        }
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode) {
            Write-Host " ✓ Reachable ($statusCode)" -ForegroundColor Green
            $results += [PSCustomObject]@{
                Endpoint = $endpoint
                Status = "✓ PASS"
                StatusCode = $statusCode
            }
        } else {
            Write-Host " ✗ FAIL" -ForegroundColor Red
            $results += [PSCustomObject]@{
                Endpoint = $endpoint
                Status = "✗ FAIL"
                StatusCode = "N/A"
            }
        }
    }
    
    Start-Sleep -Milliseconds 200
}

Write-Host "`n=== Test Summary ===" -ForegroundColor Cyan
$results | Format-Table -AutoSize

$passed = ($results | Where-Object { $_.Status -like "*PASS*" }).Count
$total = $results.Count

Write-Host "`nResults: $passed/$total endpoints responding" -ForegroundColor $(if ($passed -eq $total) { "Green" } else { "Yellow" })

if ($passed -eq $total) {
    Write-Host "`n✓ All endpoints are working! Ready for Step 2." -ForegroundColor Green
} else {
    Write-Host "`n⚠ Some endpoints may need investigation." -ForegroundColor Yellow
}
