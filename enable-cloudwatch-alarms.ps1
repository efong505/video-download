# Enable CloudWatch Alarms
# Re-enables alarm actions when you need monitoring again

Write-Host "Enabling CloudWatch alarm actions..." -ForegroundColor Yellow

# Get all alarm names
$alarms = aws cloudwatch describe-alarms --query "MetricAlarms[*].AlarmName" --output text

if ($alarms) {
    # Split by whitespace and enable each
    $alarmArray = $alarms -split '\s+'
    
    foreach ($alarm in $alarmArray) {
        if ($alarm) {
            aws cloudwatch enable-alarm-actions --alarm-names $alarm
            Write-Host "✓ Enabled: $alarm" -ForegroundColor Green
        }
    }
    
    Write-Host "`n✅ All alarms re-enabled and will send notifications." -ForegroundColor Green
} else {
    Write-Host "No alarms found." -ForegroundColor Red
}
