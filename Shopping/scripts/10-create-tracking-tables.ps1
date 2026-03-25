# Week 7: Create Behavioral Tracking DynamoDB Tables
# Tables: ProductViews, WatchList

$profile = "ekewaka"
$region = "us-east-1"

Write-Host "`n=== Week 7: Creating Tracking Tables ===" -ForegroundColor Cyan

# --- ProductViews Table ---
Write-Host "`nCreating ProductViews table..." -ForegroundColor Yellow
try {
    aws dynamodb create-table `
        --table-name ProductViews `
        --attribute-definitions `
            AttributeName=view_id,AttributeType=S `
            AttributeName=user_id,AttributeType=S `
            AttributeName=product_id,AttributeType=S `
            AttributeName=timestamp,AttributeType=S `
            AttributeName=session_id,AttributeType=S `
        --key-schema `
            AttributeName=view_id,KeyType=HASH `
            AttributeName=timestamp,KeyType=RANGE `
        --global-secondary-indexes `
            "[{`"IndexName`":`"user_id-timestamp-index`",`"KeySchema`":[{`"AttributeName`":`"user_id`",`"KeyType`":`"HASH`"},{`"AttributeName`":`"timestamp`",`"KeyType`":`"RANGE`"}],`"Projection`":{`"ProjectionType`":`"ALL`"},`"ProvisionedThroughput`":{`"ReadCapacityUnits`":5,`"WriteCapacityUnits`":5}},{`"IndexName`":`"product_id-timestamp-index`",`"KeySchema`":[{`"AttributeName`":`"product_id`",`"KeyType`":`"HASH`"},{`"AttributeName`":`"timestamp`",`"KeyType`":`"RANGE`"}],`"Projection`":{`"ProjectionType`":`"ALL`"},`"ProvisionedThroughput`":{`"ReadCapacityUnits`":5,`"WriteCapacityUnits`":5}},{`"IndexName`":`"session_id-timestamp-index`",`"KeySchema`":[{`"AttributeName`":`"session_id`",`"KeyType`":`"HASH`"},{`"AttributeName`":`"timestamp`",`"KeyType`":`"RANGE`"}],`"Projection`":{`"ProjectionType`":`"ALL`"},`"ProvisionedThroughput`":{`"ReadCapacityUnits`":5,`"WriteCapacityUnits`":5}}]" `
        --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 `
        --region $region --profile $profile --no-cli-pager | Out-Null
    Write-Host "  ProductViews table created" -ForegroundColor Green
} catch {
    if ($_.Exception.Message -match "Table already exists") {
        Write-Host "  ProductViews table already exists - skipping" -ForegroundColor Yellow
    } else { throw }
}

# Enable TTL on ProductViews (90 days auto-delete)
Write-Host "  Enabling TTL on ProductViews..." -ForegroundColor Gray
aws dynamodb update-time-to-live `
    --table-name ProductViews `
    --time-to-live-specification "Enabled=true,AttributeName=expires_at" `
    --region $region --profile $profile --no-cli-pager 2>$null

# --- WatchList Table ---
Write-Host "`nCreating WatchList table..." -ForegroundColor Yellow
try {
    aws dynamodb create-table `
        --table-name WatchList `
        --attribute-definitions `
            AttributeName=user_id,AttributeType=S `
            AttributeName=product_id,AttributeType=S `
        --key-schema `
            AttributeName=user_id,KeyType=HASH `
            AttributeName=product_id,KeyType=RANGE `
        --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 `
        --region $region --profile $profile --no-cli-pager | Out-Null
    Write-Host "  WatchList table created" -ForegroundColor Green
} catch {
    if ($_.Exception.Message -match "Table already exists") {
        Write-Host "  WatchList table already exists - skipping" -ForegroundColor Yellow
    } else { throw }
}

# Wait for tables to become active
Write-Host "`nWaiting for tables to become active..." -ForegroundColor Yellow
aws dynamodb wait table-exists --table-name ProductViews --region $region --profile $profile
aws dynamodb wait table-exists --table-name WatchList --region $region --profile $profile

# Verify
Write-Host "`n=== Verification ===" -ForegroundColor Cyan
$pvStatus = aws dynamodb describe-table --table-name ProductViews --query "Table.TableStatus" --output text --region $region --profile $profile
$wlStatus = aws dynamodb describe-table --table-name WatchList --query "Table.TableStatus" --output text --region $region --profile $profile

Write-Host "  ProductViews: $pvStatus" -ForegroundColor $(if ($pvStatus -eq "ACTIVE") {"Green"} else {"Red"})
Write-Host "  WatchList:    $wlStatus" -ForegroundColor $(if ($wlStatus -eq "ACTIVE") {"Green"} else {"Red"})

if ($pvStatus -eq "ACTIVE" -and $wlStatus -eq "ACTIVE") {
    Write-Host "`n=== All tracking tables created successfully! ===" -ForegroundColor Green
} else {
    Write-Host "`n=== Some tables not active yet - check AWS Console ===" -ForegroundColor Red
}
