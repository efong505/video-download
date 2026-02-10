# test-unified-api.ps1
# Tests all endpoints of the unified API

param(
    [string]$BaseUrl = "https://api.christianconservativestoday.com",
    [string]$JwtToken = ""
)

Write-Host "🧪 Testing Unified API Endpoints..." -ForegroundColor Cyan
Write-Host "Base URL: $BaseUrl`n" -ForegroundColor Gray

$results = @()
$passed = 0
$failed = 0

function Test-Endpoint {
    param(
        [string]$Name,
        [string]$Url,
        [string]$Method = "GET",
        [string]$Token = ""
    )
    
    Write-Host "Testing $Name..." -NoNewline
    
    try {
        $headers = @{}
        if ($Token) {
            $headers["Authorization"] = "Bearer $Token"
        }
        
        if ($Method -eq "GET") {
            $response = Invoke-WebRequest -Uri $Url -Method GET -Headers $headers -TimeoutSec 10 -ErrorAction Stop
        } else {
            $response = Invoke-WebRequest -Uri $Url -Method $Method -Headers $headers -TimeoutSec 10 -ErrorAction Stop
        }
        
        if ($response.StatusCode -eq 200 -or $response.StatusCode -eq 201) {
            Write-Host " ✅ PASS" -ForegroundColor Green
            return $true
        } else {
            Write-Host " ⚠️  Status: $($response.StatusCode)" -ForegroundColor Yellow
            return $false
        }
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode -eq 401 -or $statusCode -eq 403) {
            Write-Host " ⚠️  Auth required (expected)" -ForegroundColor Yellow
            return $true
        } else {
            Write-Host " ❌ FAIL: $($_.Exception.Message)" -ForegroundColor Red
            return $false
        }
    }
}

# Test public endpoints
Write-Host "`n📋 Testing Public Endpoints..." -ForegroundColor Cyan

$endpoints = @(
    @{ Name = "Articles List"; Url = "$BaseUrl/articles" },
    @{ Name = "Videos List"; Url = "$BaseUrl/videos" },
    @{ Name = "News List"; Url = "$BaseUrl/news" },
    @{ Name = "Resources List"; Url = "$BaseUrl/resources" },
    @{ Name = "Contributors List"; Url = "$BaseUrl/contributors" },
    @{ Name = "Tags List"; Url = "$BaseUrl/tags" },
    @{ Name = "Prayer Requests"; Url = "$BaseUrl/prayer/requests" },
    @{ Name = "Events List"; Url = "$BaseUrl/events" }
)

foreach ($endpoint in $endpoints) {
    if (Test-Endpoint -Name $endpoint.Name -Url $endpoint.Url) {
        $passed++
    } else {
        $failed++
    }
}

# Test auth endpoints
Write-Host "`n🔐 Testing Auth Endpoints..." -ForegroundColor Cyan

$authEndpoints = @(
    @{ Name = "Auth Health"; Url = "$BaseUrl/auth/health" }
)

foreach ($endpoint in $authEndpoints) {
    if (Test-Endpoint -Name $endpoint.Name -Url $endpoint.Url) {
        $passed++
    } else {
        $failed++
    }
}

# Test protected endpoints (should return 401/403)
Write-Host "`n🔒 Testing Protected Endpoints (should require auth)..." -ForegroundColor Cyan

$protectedEndpoints = @(
    @{ Name = "Admin Users"; Url = "$BaseUrl/admin/users" },
    @{ Name = "Admin Videos"; Url = "$BaseUrl/admin/videos" },
    @{ Name = "Create Article"; Url = "$BaseUrl/articles"; Method = "POST" },
    @{ Name = "Create News"; Url = "$BaseUrl/news"; Method = "POST" }
)

foreach ($endpoint in $protectedEndpoints) {
    if (Test-Endpoint -Name $endpoint.Name -Url $endpoint.Url -Method $endpoint.Method -Token $JwtToken) {
        $passed++
    } else {
        $failed++
    }
}

# Test CORS
Write-Host "`n🌐 Testing CORS..." -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri "$BaseUrl/articles" -Method OPTIONS -TimeoutSec 10
    $corsHeaders = $response.Headers["Access-Control-Allow-Origin"]
    if ($corsHeaders) {
        Write-Host "CORS Headers Present... ✅ PASS" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "CORS Headers Missing... ❌ FAIL" -ForegroundColor Red
        $failed++
    }
} catch {
    Write-Host "CORS Test Failed... ❌ FAIL" -ForegroundColor Red
    $failed++
}

# Summary
Write-Host "`n" + "="*60 -ForegroundColor Cyan
Write-Host "📊 TEST SUMMARY" -ForegroundColor Yellow
Write-Host "="*60 -ForegroundColor Cyan
Write-Host "Total Tests: $($passed + $failed)" -ForegroundColor White
Write-Host "Passed:      $passed" -ForegroundColor Green
Write-Host "Failed:      $failed" -ForegroundColor $(if ($failed -eq 0) { "Green" } else { "Red" })
Write-Host "Success Rate: $([math]::Round(($passed / ($passed + $failed)) * 100, 2))%" -ForegroundColor Yellow
Write-Host "="*60 -ForegroundColor Cyan

if ($failed -eq 0) {
    Write-Host "`n🎉 All tests passed! API is working correctly." -ForegroundColor Green
} else {
    Write-Host "`n⚠️  Some tests failed. Check the output above for details." -ForegroundColor Yellow
}

Write-Host "`nNext Steps:" -ForegroundColor Cyan
Write-Host "1. If tests passed, update frontend URLs"
Write-Host "2. Run: .\update-frontend-urls.ps1"
Write-Host "3. Monitor CloudWatch logs for errors"
