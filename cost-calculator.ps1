param(
    [double]$Hours,
    [double]$Minutes = 0,
    [double]$vCPU = 0.5,
    [double]$MemoryGB = 1.0
)

if ($Minutes -gt 0 -and $Hours -eq 0) {
    $Hours = $Minutes / 60
}

if ($Hours -eq 0) {
    Write-Host "Usage: .\cost-calculator.ps1 -Hours 0.85"
    Write-Host "   Or: .\cost-calculator.ps1 -Minutes 51"
    exit 1
}

# AWS Fargate Pricing (US East 1)
$vCPU_RATE = 0.04048    # per vCPU hour
$MEMORY_RATE = 0.004445 # per GB hour

$vCpuCost = $Hours * $vCPU * $vCPU_RATE
$memoryCost = $Hours * $MemoryGB * $MEMORY_RATE
$totalCost = $vCpuCost + $memoryCost

Write-Host "💰 AWS Fargate Cost Calculation" -ForegroundColor Cyan
Write-Host ""
Write-Host "Runtime: $([math]::Round($Hours, 2)) hours ($([math]::Round($Hours * 60, 1)) minutes)" -ForegroundColor White
Write-Host "Resources: $vCPU vCPU, $MemoryGB GB RAM" -ForegroundColor White
Write-Host ""
Write-Host "vCPU Cost:    `$$([math]::Round($vCpuCost, 4))" -ForegroundColor Yellow
Write-Host "Memory Cost:  `$$([math]::Round($memoryCost, 4))" -ForegroundColor Yellow
Write-Host "Total Cost:   `$$([math]::Round($totalCost, 4))" -ForegroundColor Green
Write-Host ""
Write-Host "Daily if continuous: `$$([math]::Round($totalCost * 24 / $Hours, 2))" -ForegroundColor Gray
Write-Host "Monthly if continuous: `$$([math]::Round($totalCost * 24 * 30 / $Hours, 2))" -ForegroundColor Gray