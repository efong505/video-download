# Test Book Signup
# Simulates a user signing up for the book email list

param(
    [Parameter(Mandatory=$false)]
    [string]$Email = "test-$(Get-Date -Format 'yyyyMMdd-HHmmss')@example.com",
    
    [Parameter(Mandatory=$false)]
    [string]$Name = "Test User"
)

$apiUrl = "https://niexv1rw75.execute-api.us-east-1.amazonaws.com/subscribe"

$body = @{
    email = $Email
    name = $Name
    list_type = "book"
} | ConvertTo-Json

Write-Host "Testing book signup..." -ForegroundColor Cyan
Write-Host "Email: $Email" -ForegroundColor Yellow
Write-Host "Name: $Name" -ForegroundColor Yellow
Write-Host ""

try {
    $response = Invoke-RestMethod -Uri $apiUrl -Method POST -Body $body -ContentType "application/json"
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
    Write-Host ""
    Write-Host "Check your email (or admin email) for:" -ForegroundColor Cyan
    Write-Host "  1. Welcome email with 4 PDFs" -ForegroundColor White
    Write-Host "  2. Admin notification" -ForegroundColor White
    Write-Host "  3. Drip enrollment created" -ForegroundColor White
} catch {
    Write-Host "ERROR!" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Write-Host $_.ErrorDetails.Message
}
