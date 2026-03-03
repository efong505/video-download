# Disable CloudWatch Alarms Temporarily
# Saves ~$1.70/month by disabling alarm actions

Write-Host "Disabling CloudWatch alarm actions..." -ForegroundColor Yellow

# Get all alarm names
$alarms = aws cloudwatch describe-alarms --query "MetricAlarms[*].AlarmName" --output text

if ($alarms) {
    # Split by whitespace and disable each
    $alarmArray = $alarms -split '\s+'
    
    foreach ($alarm in $alarmArray) {
        if ($alarm) {
            aws cloudwatch disable-alarm-actions --alarm-names $alarm
            Write-Host "✓ Disabled: $alarm" -ForegroundColor Green
        }
    }
    
    Write-Host "`n✅ All alarms disabled. Alarms still exist but won't send notifications." -ForegroundColor Green
    Write-Host "💰 Estimated savings: ~$1.70/month" -ForegroundColor Cyan
} else {
    Write-Host "No alarms found." -ForegroundColor Red
}
