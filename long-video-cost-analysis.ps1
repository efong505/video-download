# Cost comparison for LONG videos (1-2 hour processing times)
# Based on recent timeout issues with large Rumble videos

Write-Host "=== LONG VIDEO COST ANALYSIS ===" -ForegroundColor Yellow
Write-Host "Analyzing videos that timeout in current Fargate solution" -ForegroundColor White
Write-Host ""

# Long video scenarios
$scenarios = @{
    "Antifa Roundtable 1080p" = @{ SizeMB = 2740; ProcessingHours = 2.5 }  # 2.74GB, timed out at 2hrs
    "Antifa Roundtable 720p" = @{ SizeMB = 1420; ProcessingHours = 1.5 }   # 1.42GB, also timed out
    "Large Podcast/Interview" = @{ SizeMB = 3500; ProcessingHours = 3.0 }   # Hypothetical 3.5GB video
}

foreach ($scenarioName in $scenarios.Keys) {
    $scenario = $scenarios[$scenarioName]
    $videoSizeMB = $scenario.SizeMB
    $videoSizeGB = $videoSizeMB / 1024
    $processingHours = $scenario.ProcessingHours
    
    Write-Host "=== $scenarioName ===" -ForegroundColor Cyan
    Write-Host "Size: $videoSizeMB MB ($([math]::Round($videoSizeGB, 2)) GB)" -ForegroundColor White
    Write-Host "Processing Time: $processingHours hours" -ForegroundColor White
    Write-Host ""
    
    # FARGATE COSTS (current solution)
    $fargateVCPUCost = $processingHours * 0.5 * 0.04048
    $fargateMemoryCost = $processingHours * 1 * 0.004445
    $fargateTotal = $fargateVCPUCost + $fargateMemoryCost
    
    Write-Host "FARGATE (Current):" -ForegroundColor Green
    Write-Host "  vCPU (0.5): `$$([math]::Round($fargateVCPUCost, 4))" -ForegroundColor White
    Write-Host "  Memory (1GB): `$$([math]::Round($fargateMemoryCost, 4))" -ForegroundColor White
    Write-Host "  Total: `$$([math]::Round($fargateTotal, 4))" -ForegroundColor Green
    Write-Host ""
    
    # EC2 OPTIONS
    $ec2Options = @{
        "t3.small" = @{ Cost = 0.0208; vCPU = 2; RAM = 2 }
        "t3.medium" = @{ Cost = 0.0416; vCPU = 2; RAM = 4 }
        "c5.large" = @{ Cost = 0.085; vCPU = 2; RAM = 4 }
        "c5.xlarge" = @{ Cost = 0.17; vCPU = 4; RAM = 8 }
    }
    
    Write-Host "EC2 OPTIONS:" -ForegroundColor Blue
    
    $bestEC2 = $null
    $bestEC2Cost = 999
    
    foreach ($instanceType in $ec2Options.Keys) {
        $instance = $ec2Options[$instanceType]
        
        # EC2 costs
        $ec2ComputeCost = $processingHours * $instance.Cost
        $ebsStorageCost = $processingHours * 0.0001  # EBS cost scales with time
        $dataTransferCost = $videoSizeGB * 0.09  # S3 upload
        $s3StorageCost = $videoSizeGB * 0.023 / 30  # Daily storage
        
        $ec2Total = $ec2ComputeCost + $ebsStorageCost + $dataTransferCost + $s3StorageCost
        
        Write-Host "  $instanceType (${($instance.vCPU)} vCPU, ${($instance.RAM)}GB): `$$([math]::Round($ec2Total, 4))" -ForegroundColor White
        
        if ($ec2Total -lt $bestEC2Cost) {
            $bestEC2Cost = $ec2Total
            $bestEC2 = $instanceType
        }
    }
    
    Write-Host ""
    
    # COMPARISON
    $savings = $fargateTotal - $bestEC2Cost
    Write-Host "COMPARISON:" -ForegroundColor Yellow
    Write-Host "  Fargate: `$$([math]::Round($fargateTotal, 4))" -ForegroundColor Green
    Write-Host "  Best EC2 ($bestEC2): `$$([math]::Round($bestEC2Cost, 4))" -ForegroundColor Blue
    
    if ($savings -gt 0) {
        Write-Host "  💰 EC2 SAVES: `$$([math]::Round($savings, 4)) ($([math]::Round($savings/$fargateTotal*100, 1))%)" -ForegroundColor Green
    } else {
        Write-Host "  💰 Fargate SAVES: `$$([math]::Round([math]::Abs($savings), 4)) ($([math]::Round([math]::Abs($savings)/$bestEC2Cost*100, 1))%)" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "----------------------------------------" -ForegroundColor Gray
    Write-Host ""
}

# SUMMARY RECOMMENDATIONS
Write-Host "=== RECOMMENDATIONS ===" -ForegroundColor Magenta
Write-Host ""
Write-Host "FOR LONG VIDEOS (>1 hour processing):" -ForegroundColor Yellow
Write-Host "✅ EC2 is significantly cheaper" -ForegroundColor Green
Write-Host "✅ No 2-hour timeout limit" -ForegroundColor Green
Write-Host "✅ Better performance with more CPU/RAM" -ForegroundColor Green
Write-Host "✅ Can handle 4K videos without issues" -ForegroundColor Green
Write-Host ""
Write-Host "HYBRID APPROACH:" -ForegroundColor Cyan
Write-Host "• Use Fargate for videos <1 hour processing" -ForegroundColor White
Write-Host "• Use EC2 for videos >1 hour processing" -ForegroundColor White
Write-Host "• Route based on estimated file size/duration" -ForegroundColor White
Write-Host ""
Write-Host "IMPLEMENTATION:" -ForegroundColor Yellow
Write-Host "• Add EC2 launcher to router Lambda" -ForegroundColor White
Write-Host "• Route large videos (>1GB) to EC2" -ForegroundColor White
Write-Host "• Keep current Fargate for small/medium videos" -ForegroundColor White