# 7 Mountains Phase 4 - Quick Start Script
# Run this to set up everything automatically

Write-Host "🏔️  7 Mountains Phase 4 - Backend Integration Setup" -ForegroundColor Cyan
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create DynamoDB Tables
Write-Host "Step 1: Creating DynamoDB Tables..." -ForegroundColor Yellow
Write-Host "This will create 3 tables: mountain-pledges, mountain-badges, mountain-contributions" -ForegroundColor White
Write-Host ""
$createTables = Read-Host "Create tables now? (y/n)"

if ($createTables -eq 'y') {
    python create_mountains_tables.py
    Write-Host ""
    Write-Host "✅ Tables created!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "⏭️  Skipping table creation" -ForegroundColor Yellow
    Write-Host ""
}

# Step 2: Deploy Lambda Function
Write-Host "Step 2: Deploying Lambda Function..." -ForegroundColor Yellow
Write-Host "This will package and deploy the mountains-api Lambda function" -ForegroundColor White
Write-Host ""
$deployLambda = Read-Host "Deploy Lambda now? (y/n)"

if ($deployLambda -eq 'y') {
    .\deploy-mountains-api.ps1
    Write-Host ""
    Write-Host "✅ Lambda deployed!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "⏭️  Skipping Lambda deployment" -ForegroundColor Yellow
    Write-Host ""
}

# Step 3: API Gateway Setup Instructions
Write-Host "Step 3: API Gateway Setup" -ForegroundColor Yellow
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next, you need to create an API Gateway endpoint:" -ForegroundColor White
Write-Host ""
Write-Host "1. Go to: https://console.aws.amazon.com/apigateway" -ForegroundColor Cyan
Write-Host "2. Create REST API named 'mountains-api'" -ForegroundColor White
Write-Host "3. Create resource '/mountains'" -ForegroundColor White
Write-Host "4. Add POST and GET methods" -ForegroundColor White
Write-Host "5. Link to 'mountains-api' Lambda function" -ForegroundColor White
Write-Host "6. Enable CORS" -ForegroundColor White
Write-Host "7. Deploy to 'prod' stage" -ForegroundColor White
Write-Host ""
Write-Host "📖 Full instructions: 7-MOUNTAINS-PHASE4-SETUP.md" -ForegroundColor Cyan
Write-Host ""

$openGuide = Read-Host "Open setup guide now? (y/n)"
if ($openGuide -eq 'y') {
    Start-Process "7-MOUNTAINS-PHASE4-SETUP.md"
}

Write-Host ""
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host "✅ Phase 4 Setup Script Complete!" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 What was done:" -ForegroundColor Yellow
Write-Host "   ✅ DynamoDB tables created (if selected)" -ForegroundColor White
Write-Host "   ✅ Lambda function deployed (if selected)" -ForegroundColor White
Write-Host "   📝 API Gateway setup instructions provided" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation created:" -ForegroundColor Yellow
Write-Host "   📖 7-MOUNTAINS-PHASE4-SETUP.md - Complete setup guide" -ForegroundColor White
Write-Host "   📖 7-MOUNTAINS-API-REFERENCE.md - Quick reference card" -ForegroundColor White
Write-Host "   📖 7-MOUNTAINS-PHASE4-SUMMARY.md - Phase 4 summary" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Next steps:" -ForegroundColor Yellow
Write-Host "   1. Complete API Gateway setup (15 minutes)" -ForegroundColor White
Write-Host "   2. Test all 6 endpoints" -ForegroundColor White
Write-Host "   3. Note your API URL" -ForegroundColor White
Write-Host "   4. Update frontend with API calls" -ForegroundColor White
Write-Host "   5. Proceed to Phase 5 (Templates)" -ForegroundColor White
Write-Host ""
Write-Host "💡 Need help? Check the documentation files above!" -ForegroundColor Cyan
Write-Host ""
