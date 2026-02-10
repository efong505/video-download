# Import Remaining Lambda Functions to Terraform
# This script automates: fetch config → generate Terraform code → import → verify

$ErrorActionPreference = "Stop"

# Remaining Lambda functions to import
$functions = @(
    "video-download-router",
    "prayer_api",
    "events_api",
    "notifications_api"
)

$mainTfPath = "..\environments\prod\main.tf"
$roleArn = "arn:aws:iam::371751795928:role/lambda-execution-role"

Write-Host "`n=== Terraform Lambda Import Automation ===" -ForegroundColor Cyan
Write-Host "This script will import $($functions.Count) Lambda functions`n" -ForegroundColor Cyan

# Step 1: Fetch configurations from AWS
Write-Host "[Step 1/5] Fetching Lambda configurations from AWS..." -ForegroundColor Yellow
$configs = @{}

foreach ($funcName in $functions) {
    Write-Host "  Fetching: $funcName" -ForegroundColor Gray
    
    $config = aws lambda get-function --function-name $funcName --query 'Configuration' --output json | ConvertFrom-Json
    
    $configs[$funcName] = @{
        Runtime = $config.Runtime
        Handler = $config.Handler
        MemorySize = $config.MemorySize
        Timeout = $config.Timeout
        Layers = $config.Layers.Arn
    }
    
    Write-Host "    Runtime: $($config.Runtime), Memory: $($config.MemorySize)MB, Timeout: $($config.Timeout)s" -ForegroundColor DarkGray
    if ($config.Layers) {
        Write-Host "    Layers: $($config.Layers.Count) layer(s)" -ForegroundColor DarkGray
    }
}

# Step 2: Generate Terraform module blocks
Write-Host "`n[Step 2/5] Generating Terraform module blocks..." -ForegroundColor Yellow
$terraformCode = "`n"

foreach ($funcName in $functions) {
    $config = $configs[$funcName]
    $moduleName = $funcName -replace '-', '_'
    
    $terraformCode += @"

module "lambda_$moduleName" {
  source = "../../modules/lambda"

  function_name = "$funcName"
  runtime       = "$($config.Runtime)"
  handler       = "$($config.Handler)"
  memory_size   = $($config.MemorySize)
  timeout       = $($config.Timeout)
  role_arn      = "$roleArn"
"@

    if ($config.Layers -and $config.Layers.Count -gt 0) {
        $layersJson = ($config.Layers | ForEach-Object { "`"$_`"" }) -join ",`n        "
        $terraformCode += @"

  layers        = [
        $layersJson
  ]
"@
    }

    $terraformCode += @"

  
  environment_variables = {}
}

"@
}

Write-Host "  Generated $($functions.Count) module blocks" -ForegroundColor Green

# Step 3: Append to main.tf
Write-Host "`n[Step 3/5] Appending to main.tf..." -ForegroundColor Yellow
Add-Content -Path $mainTfPath -Value $terraformCode
Write-Host "  Updated: $mainTfPath" -ForegroundColor Green

# Step 4: Run terraform init
Write-Host "`n[Step 4/5] Running terraform init..." -ForegroundColor Yellow
Set-Location "..\environments\prod"
terraform init -upgrade | Out-Null
Write-Host "  Terraform initialized" -ForegroundColor Green

# Step 5: Import each Lambda function
Write-Host "`n[Step 5/5] Importing Lambda functions..." -ForegroundColor Yellow

foreach ($funcName in $functions) {
    $moduleName = $funcName -replace '-', '_'
    Write-Host "  Importing: $funcName" -ForegroundColor Gray
    
    terraform import "module.lambda_$moduleName.aws_lambda_function.this" $funcName 2>&1 | Out-Null
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "    ✓ Imported successfully" -ForegroundColor Green
    } else {
        Write-Host "    ✗ Import failed" -ForegroundColor Red
    }
}

# Final verification
Write-Host "`n=== Import Complete ===" -ForegroundColor Cyan
Write-Host "`nRunning terraform plan to verify..." -ForegroundColor Yellow
Write-Host "(Should show only tag additions)`n" -ForegroundColor DarkGray

terraform plan

Write-Host "`n=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Review the plan above" -ForegroundColor White
Write-Host "2. If it looks good, run: terraform apply" -ForegroundColor White
Write-Host "3. Commit changes: git add terraform/ && git commit -m 'Imported remaining 4 Lambda functions'" -ForegroundColor White
