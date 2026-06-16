# Cleanup Script
# Destroys all infrastructure and prepares for next practice run

param(
    [switch]$Force,
    [switch]$KeepState
)

Write-Host "=== Infrastructure Cleanup Script ===" -ForegroundColor Green
Write-Host ""

# Change to terraform directory
Push-Location terraform

# Step 1: Check if resources exist
Write-Host "Step 1: Checking for resources..." -ForegroundColor Yellow
$resources = terraform state list

if ($resources.Count -eq 0) {
    Write-Host "✅ No resources to clean up" -ForegroundColor Green
    Pop-Location
    exit 0
}

Write-Host "Found $($resources.Count) resources to destroy:" -ForegroundColor Cyan
$resources | ForEach-Object { Write-Host "   - $_" -ForegroundColor Cyan }

# Step 2: Confirm destruction
if (-not $Force) {
    Write-Host "`n⚠️  WARNING: This will destroy all infrastructure in the child account!" -ForegroundColor Yellow
    Write-Host "   Type 'yes' to confirm: " -ForegroundColor Yellow -NoNewline
    $confirmation = Read-Host
    
    if ($confirmation -ne "yes") {
        Write-Host "❌ Cleanup cancelled" -ForegroundColor Red
        Pop-Location
        exit 0
    }
}

# Step 3: Get resource details before destruction
Write-Host "`nStep 2: Saving resource details..." -ForegroundColor Yellow
try {
    $outputs = terraform output -json | ConvertFrom-Json
    $s3Bucket = $outputs.s3_bucket_name.value
    $dynamoTable = $outputs.dynamodb_table_name.value
    
    Write-Host "✅ Resource details saved" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Could not get resource details" -ForegroundColor Yellow
    $s3Bucket = $null
    $dynamoTable = $null
}

# Step 4: Empty S3 bucket if it exists
if ($s3Bucket) {
    Write-Host "`nStep 3: Emptying S3 bucket..." -ForegroundColor Yellow
    try {
        $objects = aws s3 ls "s3://$s3Bucket" --profile child-account 2>$null
        if ($objects) {
            aws s3 rm "s3://$s3Bucket" --recursive --profile child-account | Out-Null
            Write-Host "✅ S3 bucket emptied" -ForegroundColor Green
        } else {
            Write-Host "✅ S3 bucket already empty" -ForegroundColor Green
        }
    } catch {
        Write-Host "⚠️  Could not empty S3 bucket (may not exist)" -ForegroundColor Yellow
    }
}

# Step 5: Run terraform destroy
Write-Host "`nStep 4: Destroying infrastructure..." -ForegroundColor Yellow
Write-Host "   This may take 2-3 minutes..." -ForegroundColor Cyan

try {
    if ($Force) {
        terraform destroy -auto-approve
    } else {
        terraform destroy
    }
    
    Write-Host "✅ Infrastructure destroyed" -ForegroundColor Green
} catch {
    Write-Host "❌ Terraform destroy failed" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
    Write-Host "`n   Troubleshooting:" -ForegroundColor Yellow
    Write-Host "   1. Wait 1-2 minutes and try again" -ForegroundColor Yellow
    Write-Host "   2. Check for resources still in use" -ForegroundColor Yellow
    Write-Host "   3. Delete resources manually via AWS Console" -ForegroundColor Yellow
    Pop-Location
    exit 1
}

# Step 6: Verify resources are gone
Write-Host "`nStep 5: Verifying cleanup..." -ForegroundColor Yellow
$remainingResources = terraform state list

if ($remainingResources.Count -eq 0) {
    Write-Host "✅ All resources destroyed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some resources remain:" -ForegroundColor Yellow
    $remainingResources | ForEach-Object { Write-Host "   - $_" -ForegroundColor Yellow }
    Write-Host "   You may need to delete these manually" -ForegroundColor Yellow
}

# Step 7: Check for orphaned resources
Write-Host "`nStep 6: Checking for orphaned resources..." -ForegroundColor Yellow

# Check CloudWatch log groups
try {
    $logGroups = aws logs describe-log-groups `
        --log-group-name-prefix "/aws/lambda/sample-function-tutorial" `
        --profile child-account 2>$null | ConvertFrom-Json
    
    if ($logGroups.logGroups.Count -gt 0) {
        Write-Host "⚠️  Found orphaned CloudWatch log group" -ForegroundColor Yellow
        Write-Host "   Deleting..." -ForegroundColor Yellow
        aws logs delete-log-group `
            --log-group-name $logGroups.logGroups[0].logGroupName `
            --profile child-account
        Write-Host "✅ Log group deleted" -ForegroundColor Green
    } else {
        Write-Host "✅ No orphaned log groups" -ForegroundColor Green
    }
} catch {
    Write-Host "✅ No orphaned log groups" -ForegroundColor Green
}

# Check SNS subscriptions
try {
    $subscriptions = aws sns list-subscriptions --profile child-account 2>$null | ConvertFrom-Json
    $tutorialSubs = $subscriptions.Subscriptions | Where-Object { $_.TopicArn -like "*tutorial-alerts*" }
    
    if ($tutorialSubs) {
        Write-Host "⚠️  Found orphaned SNS subscriptions" -ForegroundColor Yellow
        foreach ($sub in $tutorialSubs) {
            Write-Host "   Deleting subscription: $($sub.SubscriptionArn)" -ForegroundColor Yellow
            aws sns unsubscribe --subscription-arn $sub.SubscriptionArn --profile child-account
        }
        Write-Host "✅ SNS subscriptions deleted" -ForegroundColor Green
    } else {
        Write-Host "✅ No orphaned SNS subscriptions" -ForegroundColor Green
    }
} catch {
    Write-Host "✅ No orphaned SNS subscriptions" -ForegroundColor Green
}

# Step 8: Clean local files
Write-Host "`nStep 7: Cleaning local files..." -ForegroundColor Yellow

# Remove response files
Remove-Item response.json -ErrorAction SilentlyContinue
Remove-Item deployment-outputs.json -ErrorAction SilentlyContinue

# Optionally remove state files
if (-not $KeepState) {
    Write-Host "   Removing Terraform state files..." -ForegroundColor Cyan
    Remove-Item terraform.tfstate -ErrorAction SilentlyContinue
    Remove-Item terraform.tfstate.backup -ErrorAction SilentlyContinue
    Write-Host "✅ State files removed" -ForegroundColor Green
} else {
    Write-Host "✅ State files kept (use -KeepState:$false to remove)" -ForegroundColor Green
}

Write-Host "✅ Local files cleaned" -ForegroundColor Green

Pop-Location

# Step 9: Verify Terraform is ready for next run
Write-Host "`nStep 8: Verifying Terraform is ready..." -ForegroundColor Yellow
Push-Location terraform

try {
    terraform validate | Out-Null
    Write-Host "✅ Terraform configuration is valid" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Terraform validation failed" -ForegroundColor Yellow
    Write-Host "   Run 'terraform init' before next deployment" -ForegroundColor Yellow
}

Pop-Location

# Final summary
Write-Host "`n=== Cleanup Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "✅ All infrastructure destroyed" -ForegroundColor Green
Write-Host "✅ Orphaned resources cleaned" -ForegroundColor Green
Write-Host "✅ Local files cleaned" -ForegroundColor Green
Write-Host "✅ Ready for next practice run" -ForegroundColor Green
Write-Host ""
Write-Host "To deploy again:" -ForegroundColor Cyan
Write-Host "  cd terraform" -ForegroundColor Yellow
Write-Host "  terraform apply" -ForegroundColor Yellow
Write-Host ""
Write-Host "Estimated cost savings: ~$0.02/day" -ForegroundColor Green
Write-Host ""
