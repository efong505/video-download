# Cost comparison: EC2 vs Fargate for video downloads
# Using the Trish video example (35MB, ~20 min processing)

Write-Host "=== EC2 vs FARGATE COST COMPARISON ===" -ForegroundColor Yellow
Write-Host ""

# Example video specs
$videoSizeMB = 35.32
$processingTimeMinutes = 20
$processingTimeHours = $processingTimeMinutes / 60

Write-Host "Example Video: Trish.mp4 ($videoSizeMB MB, $processingTimeMinutes min processing)" -ForegroundColor Cyan
Write-Host ""

# CURRENT FARGATE SOLUTION
Write-Host "=== CURRENT FARGATE SOLUTION ===" -ForegroundColor Green
$fargateVCPU = 0.5
$fargateMemoryGB = 1
$fargateVCPUCost = $processingTimeHours * $fargateVCPU * 0.04048
$fargateMemoryCost = $processingTimeHours * $fargateMemoryGB * 0.004445
$fargateTotal = $fargateVCPUCost + $fargateMemoryCost

Write-Host "vCPU Cost (0.5 vCPU): `$$([math]::Round($fargateVCPUCost, 6))" -ForegroundColor White
Write-Host "Memory Cost (1GB): `$$([math]::Round($fargateMemoryCost, 6))" -ForegroundColor White
Write-Host "Total Fargate: `$$([math]::Round($fargateTotal, 6))" -ForegroundColor Green
Write-Host ""

# EC2 SOLUTION
Write-Host "=== EC2 SOLUTION ===" -ForegroundColor Blue

# EC2 instance types and costs (per hour)
$ec2Options = @{
    "t3.micro" = @{ vCPU = 2; RAM = 1; Cost = 0.0104 }
    "t3.small" = @{ vCPU = 2; RAM = 2; Cost = 0.0208 }
    "t3.medium" = @{ vCPU = 2; RAM = 4; Cost = 0.0416 }
    "c5.large" = @{ vCPU = 2; RAM = 4; Cost = 0.085 }
}

foreach ($instanceType in $ec2Options.Keys) {
    $instance = $ec2Options[$instanceType]
    
    # EC2 compute cost
    $ec2ComputeCost = $processingTimeHours * $instance.Cost
    
    # Additional costs
    $ebsStorageCost = 0.0001  # ~8GB EBS for 20 min = $0.0001
    $dataTransferCost = ($videoSizeMB / 1024) * 0.09  # S3 upload
    $s3StorageCost = ($videoSizeMB / 1024) * 0.023 / 30  # Daily storage
    
    $ec2Total = $ec2ComputeCost + $ebsStorageCost + $dataTransferCost + $s3StorageCost
    
    Write-Host "$instanceType (${($instance.vCPU)} vCPU, ${($instance.RAM)}GB):" -ForegroundColor Cyan
    Write-Host "  Compute: `$$([math]::Round($ec2ComputeCost, 6))" -ForegroundColor White
    Write-Host "  EBS: `$$([math]::Round($ebsStorageCost, 6))" -ForegroundColor White
    Write-Host "  Data Transfer: `$$([math]::Round($dataTransferCost, 6))" -ForegroundColor White
    Write-Host "  S3 Storage: `$$([math]::Round($s3StorageCost, 6))" -ForegroundColor White
    Write-Host "  Total: `$$([math]::Round($ec2Total, 6))" -ForegroundColor Blue
    
    $savings = $fargateTotal - $ec2Total
    if ($savings -gt 0) {
        Write-Host "  Savings vs Fargate: `$$([math]::Round($savings, 6))" -ForegroundColor Green
    } else {
        Write-Host "  Extra cost vs Fargate: `$$([math]::Round([math]::Abs($savings), 6))" -ForegroundColor Red
    }
    Write-Host ""
}

# OVERHEAD COSTS
Write-Host "=== ADDITIONAL EC2 OVERHEAD ===" -ForegroundColor Magenta
Write-Host "• Instance startup time: ~60-90 seconds (vs 30s Fargate)" -ForegroundColor White
Write-Host "• Minimum billing: 1 minute (vs per-second Fargate)" -ForegroundColor White
Write-Host "• Management complexity: Higher" -ForegroundColor White
Write-Host "• Security updates: Manual (vs automatic Fargate)" -ForegroundColor White
Write-Host "• Scaling: Manual (vs automatic Fargate)" -ForegroundColor White
Write-Host ""

# BREAK-EVEN ANALYSIS
Write-Host "=== BREAK-EVEN ANALYSIS ===" -ForegroundColor Yellow
$cheapestEC2 = $ec2Options["t3.micro"].Cost * $processingTimeHours + 0.0001 + $dataTransferCost + $s3StorageCost
$breakEvenTime = $cheapestEC2 / ($fargateVCPUCost + $fargateMemoryCost) * $processingTimeMinutes

Write-Host "Fargate becomes cheaper for videos requiring:" -ForegroundColor White
Write-Host "• Less than $([math]::Round($breakEvenTime, 1)) minutes processing time" -ForegroundColor Green
Write-Host "• Or frequent small downloads (due to per-second billing)" -ForegroundColor Green
Write-Host ""

Write-Host "EC2 becomes cheaper for:" -ForegroundColor White
Write-Host "• Videos requiring >$([math]::Round($breakEvenTime, 1)) minutes processing" -ForegroundColor Blue
Write-Host "• Batch processing multiple videos" -ForegroundColor Blue
Write-Host "• When you can optimize instance utilization" -ForegroundColor Blue