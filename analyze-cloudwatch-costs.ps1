# Analyze CloudWatch Costs
# Identifies what's costing $0.08-0.12/day

Write-Host "Analyzing CloudWatch Costs..." -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Cyan

# 1. Count Alarms (First 10 free, then $0.10/month each)
Write-Host "`n1. ALARMS" -ForegroundColor Cyan
$alarmCount = (aws cloudwatch describe-alarms --query "length(MetricAlarms)" --output text)
$freeAlarms = [Math]::Min($alarmCount, 10)
$paidAlarms = [Math]::Max(0, $alarmCount - 10)
$alarmCost = $paidAlarms * 0.10

Write-Host "   Total Alarms: $alarmCount" -ForegroundColor White
Write-Host "   Free Alarms: $freeAlarms" -ForegroundColor Green
Write-Host "   Paid Alarms: $paidAlarms @ `$0.10/month each" -ForegroundColor Yellow
Write-Host "   Monthly Cost: `$$alarmCost" -ForegroundColor Red

# 2. Check Log Groups and Storage
Write-Host "`n2. LOG GROUPS" -ForegroundColor Cyan
$logGroups = aws logs describe-log-groups --query "logGroups[*].[logGroupName,storedBytes,retentionInDays]" --output json | ConvertFrom-Json

$totalBytes = 0
foreach ($group in $logGroups) {
    $totalBytes += $group[1]
}

$totalGB = [Math]::Round($totalBytes / 1GB, 2)
$freeGB = 5
$paidGB = [Math]::Max(0, $totalGB - $freeGB)
$storageCost = $paidGB * 0.03

Write-Host "   Total Log Groups: $($logGroups.Count)" -ForegroundColor White
Write-Host "   Total Storage: $totalGB GB" -ForegroundColor White
Write-Host "   Free Storage: $freeGB GB" -ForegroundColor Green
Write-Host "   Paid Storage: $paidGB GB @ `$0.03/GB/month" -ForegroundColor Yellow
Write-Host "   Monthly Cost: `$$([Math]::Round($storageCost, 2))" -ForegroundColor Red

# 3. Check for Custom Metrics
Write-Host "`n3. CUSTOM METRICS" -ForegroundColor Cyan
Write-Host "   Checking for custom metrics..." -ForegroundColor White

# Get all namespaces
$namespaces = aws cloudwatch list-metrics --query "Metrics[*].Namespace" --output json | ConvertFrom-Json | Select-Object -Unique

$customNamespaces = $namespaces | Where-Object { $_ -notlike "AWS/*" }

if ($customNamespaces) {
    Write-Host "   Custom Namespaces Found:" -ForegroundColor Yellow
    foreach ($ns in $customNamespaces) {
        $metricCount = (aws cloudwatch list-metrics --namespace $ns --query "length(Metrics)" --output text)
        Write-Host "     - $ns : $metricCount metrics" -ForegroundColor White
    }
    
    $totalCustomMetrics = ($customNamespaces | ForEach-Object {
        aws cloudwatch list-metrics --namespace $_ --query "length(Metrics)" --output text
    } | Measure-Object -Sum).Sum
    
    $freeMetrics = [Math]::Min($totalCustomMetrics, 10)
    $paidMetrics = [Math]::Max(0, $totalCustomMetrics - 10)
    $metricCost = $paidMetrics * 0.30
    
    Write-Host "   Total Custom Metrics: $totalCustomMetrics" -ForegroundColor White
    Write-Host "   Free Metrics: $freeMetrics" -ForegroundColor Green
    Write-Host "   Paid Metrics: $paidMetrics @ `$0.30/month each" -ForegroundColor Yellow
    Write-Host "   Monthly Cost: `$$([Math]::Round($metricCost, 2))" -ForegroundColor Red
} else {
    Write-Host "   No custom metrics found (only AWS metrics)" -ForegroundColor Green
    $metricCost = 0
}

# 4. Check API Requests (First 1M free)
Write-Host "`n4. API REQUESTS" -ForegroundColor Cyan
Write-Host "   First 1,000,000 requests/month: FREE" -ForegroundColor Green
Write-Host "   (Unlikely to exceed free tier)" -ForegroundColor White

# 5. Check Dashboards
Write-Host "`n5. DASHBOARDS" -ForegroundColor Cyan
$dashboards = aws cloudwatch list-dashboards --query "DashboardEntries" --output json | ConvertFrom-Json
$dashboardCount = if ($dashboards) { $dashboards.Count } else { 0 }
$freeDashboards = [Math]::Min($dashboardCount, 3)
$paidDashboards = [Math]::Max(0, $dashboardCount - 3)
$dashboardCost = $paidDashboards * 3.00

Write-Host "   Total Dashboards: $dashboardCount" -ForegroundColor White
Write-Host "   Free Dashboards: $freeDashboards" -ForegroundColor Green
Write-Host "   Paid Dashboards: $paidDashboards @ `$3.00/month each" -ForegroundColor Yellow
Write-Host "   Monthly Cost: `$$([Math]::Round($dashboardCost, 2))" -ForegroundColor Red

# TOTAL COST SUMMARY
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "ESTIMATED MONTHLY COST BREAKDOWN" -ForegroundColor Yellow
Write-Host ("=" * 60) -ForegroundColor Cyan

$totalMonthlyCost = $alarmCost + $storageCost + $metricCost + $dashboardCost

Write-Host "Alarms:          `$$([Math]::Round($alarmCost, 2))" -ForegroundColor White
Write-Host "Log Storage:     `$$([Math]::Round($storageCost, 2))" -ForegroundColor White
Write-Host "Custom Metrics:  `$$([Math]::Round($metricCost, 2))" -ForegroundColor White
Write-Host "Dashboards:      `$$([Math]::Round($dashboardCost, 2))" -ForegroundColor White
Write-Host ("-" * 60) -ForegroundColor Cyan
Write-Host "TOTAL:           `$$([Math]::Round($totalMonthlyCost, 2))/month" -ForegroundColor Red
Write-Host "Daily Average:   `$$([Math]::Round($totalMonthlyCost / 30, 2))/day" -ForegroundColor Red

Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "COST REDUCTION RECOMMENDATIONS" -ForegroundColor Yellow
Write-Host ("=" * 60) -ForegroundColor Cyan

if ($paidAlarms -gt 0) {
    Write-Host "✓ Disable $paidAlarms alarms: Save `$$([Math]::Round($alarmCost, 2))/month" -ForegroundColor Green
}

if ($paidGB -gt 0) {
    Write-Host "✓ Reduce log retention to 1 day: Save ~`$$([Math]::Round($storageCost * 0.5, 2))/month" -ForegroundColor Green
}

if ($paidMetrics -gt 0) {
    Write-Host "✓ Remove custom metrics: Save `$$([Math]::Round($metricCost, 2))/month" -ForegroundColor Green
}

Write-Host "`nRun './disable-cloudwatch-alarms.ps1' to disable alarms temporarily" -ForegroundColor Cyan
