#!/bin/bash
# Emergency Revert Script - Revert all Lambda functions back to Node.js 18.x

echo "🚨 REVERTING ALL LAMBDA FUNCTIONS TO NODE.JS 18.x"

# Revert all functions to nodejs18.x
aws lambda update-function-configuration --function-name testimony-auth --runtime nodejs18.x
aws lambda update-function-configuration --function-name testimony-email-sharing --runtime nodejs18.x  
aws lambda update-function-configuration --function-name testimony-admin --runtime nodejs18.x
aws lambda update-function-configuration --function-name testimony-email-ses --runtime nodejs18.x
aws lambda update-function-configuration --function-name testimony-crud --runtime nodejs18.x

echo "✅ All functions reverted to Node.js 18.x"
echo "🔍 Verifying runtime versions..."

# Verify all functions are back to nodejs18.x
aws lambda list-functions --region us-east-1 --query "Functions[?contains(FunctionName, 'testimony')].{Name:FunctionName,Runtime:Runtime}" --output table