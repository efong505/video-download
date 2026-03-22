# Email Notifications Deployment Instructions

## Status: CODE READY - AWAITING DEPLOYMENT ⏳

The email notification feature for comment replies has been implemented but needs to be deployed to the correct AWS account.

## What Was Done:
✅ Added email notification code to `comments-handler/lambda_function.py`
✅ Integrated with existing `notifications_api` Lambda
✅ Async invocation to avoid slowing down comments
✅ Includes reply preview and direct link
✅ Graceful failure handling
✅ Documentation updated

## Deployment Issue:
The AWS CLI is configured for account `372110294325`, but the Lambda functions are in account `371751795928`.

## To Deploy:

### Option 1: Switch AWS Profile
```bash
# List available profiles
aws configure list-profiles

# Use the correct profile
aws configure --profile [correct-profile-name]

# Or set environment variable
$env:AWS_PROFILE="[correct-profile-name]"

# Then run deployment
.\deploy-comments-handler.ps1
```

### Option 2: Manual Deployment via AWS Console
1. Go to AWS Lambda Console (account 371751795928)
2. Find function: `comments-api`
3. Upload `comments-handler/lambda.zip`
4. Click "Deploy"

### Option 3: Create Deployment Package Manually
```bash
cd comments-handler
zip lambda.zip lambda_function.py

# Then upload via AWS Console or use correct AWS credentials
```

## Verification After Deployment:

1. **Test Comment Reply**:
   - Go to any article/video with comments
   - Reply to someone's comment
   - Check if they receive an email notification

2. **Check CloudWatch Logs**:
   - Go to CloudWatch Logs
   - Find log group: `/aws/lambda/comments-api`
   - Look for: "Notification sent to [email] for reply"

3. **Verify Notification Lambda**:
   - Check CloudWatch Logs for `/aws/lambda/notifications_api`
   - Confirm email was sent via SES

## Email Notification Features:

When deployed, users will receive emails when someone replies to their comment with:
- Subject: "New Reply from [Name]"
- Message: "[Name] replied to your comment: [preview]..."
- Direct link to the comment thread
- No self-notification (won't email if you reply to your own comment)

## Files Modified:
- `comments-handler/lambda_function.py` - Added notification logic
- `COMMENTS_INTEGRATION_GUIDE.md` - Updated documentation
- `deploy-comments-handler.ps1` - Deployment script

## Next Steps:
1. Configure AWS CLI with correct account credentials
2. Run `.\deploy-comments-handler.ps1`
3. Test comment reply notifications
4. Move to Phase 2 features

---

**Note**: The comments system is fully functional without this feature. Email notifications are an enhancement that can be deployed when AWS credentials are properly configured.
