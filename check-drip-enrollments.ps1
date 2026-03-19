# Check Drip Enrollments
# Shows all active drip enrollments and their status

param(
    [Parameter(Mandatory=$false)]
    [string]$Email = ""
)

$profile = "ekewaka"
$region = "us-east-1"
$table = "user-email-drip-enrollments"

Write-Host "Checking drip enrollments..." -ForegroundColor Cyan
Write-Host ""

if ($Email) {
    # Check specific email
    Write-Host "Searching for: $Email" -ForegroundColor Yellow
    $result = aws dynamodb query `
        --table-name $table `
        --index-name email-index `
        --key-condition-expression "subscriber_email = :email" `
        --expression-attribute-values "{\":email\":{\"S\":\"$Email\"}}" `
        --profile $profile `
        --region $region | ConvertFrom-Json
} else {
    # Scan all active enrollments
    Write-Host "Scanning all active enrollments..." -ForegroundColor Yellow
    $result = aws dynamodb scan `
        --table-name $table `
        --filter-expression "#status = :status" `
        --expression-attribute-names "{\"#status\":\"status\"}" `
        --expression-attribute-values "{\":status\":{\"S\":\"active\"}}" `
        --profile $profile `
        --region $region | ConvertFrom-Json
}

if ($result.Count -eq 0) {
    Write-Host "No enrollments found" -ForegroundColor Yellow
} else {
    Write-Host "Found $($result.Count) enrollment(s):" -ForegroundColor Green
    Write-Host ""
    
    foreach ($item in $result.Items) {
        Write-Host "Email: $($item.subscriber_email.S)" -ForegroundColor Cyan
        Write-Host "  User ID: $($item.user_id.S)"
        Write-Host "  Campaign: $($item.campaign_id.S)"
        Write-Host "  Status: $($item.status.S)"
        Write-Host "  Current Sequence: $($item.current_sequence_number.N)"
        Write-Host "  Enrolled: $($item.enrolled_at.S)"
        if ($item.last_sent_at) {
            Write-Host "  Last Sent: $($item.last_sent_at.S)"
        }
        Write-Host ""
    }
}
