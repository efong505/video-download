# Feature Flags System - Deployment Checklist

## Pre-Deployment Checklist

### ✅ Files Created (Verify All Exist)
- [ ] `feature_flags_api/index.py` - Lambda function
- [ ] `create_feature_flags_table.py` - DynamoDB table script
- [ ] `deploy-feature-flags-api.ps1` - Deployment script
- [ ] `admin-feature-flags.html` - Admin interface
- [ ] `feature-flags.js` - Helper library
- [ ] `docs/FEATURE_FLAGS_GUIDE.md` - Complete guide
- [ ] `docs/FEATURE_FLAGS_QUICK_START.md` - Quick examples
- [ ] `docs/FEATURE_FLAGS_VISUAL_GUIDE.md` - Visual guide
- [ ] `FEATURE_FLAGS_README.md` - Summary

## Step 1: Backend Deployment (AWS)

### 1.1 Create DynamoDB Table
- [ ] Run: `python create_feature_flags_table.py`
- [ ] Verify table created in AWS Console
- [ ] Verify default `election_system` flag exists
- [ ] Check table has correct schema (feature_id as primary key)

**Expected Output:**
```
Creating feature-flags table...
✅ Table created successfully!
✅ Default election_system flag created!
```

### 1.2 Update Lambda Deployment Script
- [ ] Open `deploy-feature-flags-api.ps1`
- [ ] Update `$Role` with your Lambda execution role ARN
- [ ] Verify role has DynamoDB permissions (read/write)
- [ ] Verify role has CloudWatch Logs permissions

**Find your role ARN:**
```powershell
aws iam list-roles --query 'Roles[?contains(RoleName, `lambda`)].Arn'
```

### 1.3 Deploy Lambda Function
- [ ] Run: `.\deploy-feature-flags-api.ps1`
- [ ] Verify function created in AWS Console
- [ ] Check function has correct runtime (Python 3.12)
- [ ] Verify PyJWT dependency installed
- [ ] Test function with sample event

**Expected Output:**
```
🚀 Deploying Feature Flags API Lambda Function...
📦 Creating deployment package...
📥 Installing dependencies...
🗜️ Creating zip archive...
✅ Deployment complete!
```

### 1.4 Create API Gateway
- [ ] Go to AWS API Gateway Console
- [ ] Click "Create API" → "HTTP API"
- [ ] Name: `feature-flags-api`
- [ ] Add integration: Lambda → `feature-flags-api`
- [ ] Configure routes:
  - [ ] `GET /feature-flags`
  - [ ] `POST /feature-flags`
  - [ ] `PUT /feature-flags`
  - [ ] `DELETE /feature-flags`
  - [ ] `OPTIONS /feature-flags` (for CORS)
- [ ] Deploy to stage: `prod`
- [ ] Copy API Gateway URL

**API Gateway URL Format:**
```
https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/feature-flags
```

### 1.5 Grant Lambda Permissions
- [ ] Add API Gateway invoke permission to Lambda
- [ ] Run this command (replace with your values):

```powershell
aws lambda add-permission `
  --function-name feature-flags-api `
  --statement-id apigateway-invoke `
  --action lambda:InvokeFunction `
  --principal apigateway.amazonaws.com `
  --source-arn "arn:aws:execute-api:us-east-1:YOUR_ACCOUNT_ID:YOUR_API_ID/*/*/*"
```

### 1.6 Test API Endpoints
- [ ] Test GET (public): `curl https://YOUR_API_URL/feature-flags?action=list`
- [ ] Test GET single: `curl https://YOUR_API_URL/feature-flags?action=get&feature_id=election_system`
- [ ] Verify CORS headers in response
- [ ] Test with admin token (POST/PUT/DELETE)

**Expected Response:**
```json
[
  {
    "feature_id": "election_system",
    "enabled": true,
    "name": "Election Tracking System",
    "seasonal": true,
    "volunteer_dependent": true,
    "active_volunteers": 0,
    "min_volunteers_required": 10
  }
]
```

## Step 2: Frontend Configuration

### 2.1 Update API URLs
- [ ] Open `feature-flags.js`
- [ ] Line 7: Replace `YOUR_API_GATEWAY_URL` with actual URL
- [ ] Save file

- [ ] Open `admin-feature-flags.html`
- [ ] Line 85: Replace `YOUR_API_GATEWAY_URL` with actual URL
- [ ] Save file

**Example:**
```javascript
// Before
API_URL: 'https://YOUR_API_GATEWAY_URL/prod/feature-flags'

// After
API_URL: 'https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/feature-flags'
```

### 2.2 Upload Files to S3
- [ ] Upload `admin-feature-flags.html` to S3
- [ ] Upload `feature-flags.js` to S3
- [ ] Set public read permissions (if needed)
- [ ] Verify files accessible via CloudFront

```powershell
aws s3 cp admin-feature-flags.html s3://your-bucket/
aws s3 cp feature-flags.js s3://your-bucket/
```

### 2.3 Invalidate CloudFront Cache
- [ ] Invalidate `/admin-feature-flags.html`
- [ ] Invalidate `/feature-flags.js`

```powershell
aws cloudfront create-invalidation `
  --distribution-id YOUR_DISTRIBUTION_ID `
  --paths "/admin-feature-flags.html" "/feature-flags.js"
```

## Step 3: Integration into Existing Pages

### 3.1 Update navbar.js
- [ ] Add feature check code (see FEATURE_FLAGS_QUICK_START.md)
- [ ] Test election link visibility
- [ ] Upload to S3
- [ ] Invalidate CloudFront cache

**Code to Add:**
```javascript
const FEATURE_FLAGS_API = 'https://YOUR_API_URL/prod/feature-flags';

async function checkElectionFeature() {
    // See FEATURE_FLAGS_QUICK_START.md for full code
}

document.addEventListener('DOMContentLoaded', checkElectionFeature);
```

### 3.2 Update election-map.html
- [ ] Add access protection code (see FEATURE_FLAGS_QUICK_START.md)
- [ ] Test redirect for non-admins when disabled
- [ ] Test admin preview banner
- [ ] Upload to S3
- [ ] Invalidate CloudFront cache

**Code to Add:**
```javascript
const FEATURE_FLAGS_API = 'https://YOUR_API_URL/prod/feature-flags';

async function checkFeatureAccess() {
    // See FEATURE_FLAGS_QUICK_START.md for full code
}

checkFeatureAccess().then(() => loadData());
```

### 3.3 Update index.html
- [ ] Add feature status display (see FEATURE_FLAGS_QUICK_START.md)
- [ ] Test status card rendering
- [ ] Upload to S3
- [ ] Invalidate CloudFront cache

**Code to Add:**
```html
<div id="election-feature-status"></div>
<script>
async function showElectionStatus() {
    // See FEATURE_FLAGS_QUICK_START.md for full code
}
document.addEventListener('DOMContentLoaded', showElectionStatus);
</script>
```

### 3.4 Update admin.html
- [ ] Add "Feature Flags" link to navigation
- [ ] Test link accessibility
- [ ] Upload to S3
- [ ] Invalidate CloudFront cache

**Code to Add:**
```html
<a href="admin-feature-flags.html" class="nav-link">
    <i class="fas fa-flag"></i> Feature Flags
</a>
```

## Step 4: Testing

### 4.1 Test Feature ENABLED
- [ ] Go to `admin-feature-flags.html`
- [ ] Verify "Election Tracking System" shows as enabled
- [ ] Visit homepage
  - [ ] Should see green "Active" status card
  - [ ] Should show volunteer count
- [ ] Check navbar
  - [ ] "Election Map" link should be visible
  - [ ] No "Preview" badge
- [ ] Visit `election-map.html`
  - [ ] Should have full access
  - [ ] No warning banners

### 4.2 Test Feature DISABLED (Admin User)
- [ ] Go to `admin-feature-flags.html`
- [ ] Click "Disable" on "Election Tracking System"
- [ ] Update "Disable Reason": "Between election cycles"
- [ ] Visit homepage
  - [ ] Should see yellow "Seasonal - Inactive" card
  - [ ] Should show volunteer recruitment link
- [ ] Check navbar
  - [ ] "Election Map" link should be visible
  - [ ] Should have "Preview" badge
- [ ] Visit `election-map.html`
  - [ ] Should have full access
  - [ ] Should see yellow "Admin Preview" banner at top

### 4.3 Test Feature DISABLED (Public User)
- [ ] Logout or use incognito window
- [ ] Visit homepage
  - [ ] Should see yellow "Seasonal - Inactive" card
  - [ ] Should show volunteer recruitment link
  - [ ] Should show next activation date
- [ ] Check navbar
  - [ ] "Election Map" link should be HIDDEN
- [ ] Try to visit `election-map.html` directly
  - [ ] Should show alert: "This feature is currently unavailable"
  - [ ] Should redirect to homepage

### 4.4 Test Volunteer Count
- [ ] Verify volunteer count updates automatically
- [ ] Check progress bar color:
  - [ ] Red if < 50% of minimum
  - [ ] Yellow if 50-99% of minimum
  - [ ] Green if >= 100% of minimum
- [ ] Verify count matches `contributors` table

### 4.5 Test Admin Interface
- [ ] Create new feature flag
- [ ] Edit existing flag
- [ ] Toggle feature on/off
- [ ] Delete test flag
- [ ] Verify audit trail (updated_by, updated_at)

## Step 5: Documentation

### 5.1 Update PROGRESS.md
- [ ] Add "Feature Flags System" section
- [ ] Document API Gateway URL
- [ ] Note deployment date
- [ ] List integrated pages

**Add to PROGRESS.md:**
```markdown
## Feature Flags System ✅ COMPLETE (January 2025)

**Status**: Fully operational
**API**: https://YOUR_API_URL/prod/feature-flags
**Admin Interface**: admin-feature-flags.html
**Helper Library**: feature-flags.js

**Features Implemented**:
- Seasonal feature support (election cycles)
- Volunteer dependency tracking
- Admin preview mode
- Public status messaging
- Easy toggle without code deployment

**Integrated Pages**:
- navbar.js - Hide election link when disabled
- election-map.html - Access protection
- index.html - Feature status display
- admin.html - Feature Flags link

**Documentation**:
- docs/FEATURE_FLAGS_GUIDE.md - Complete guide
- docs/FEATURE_FLAGS_QUICK_START.md - Quick examples
- docs/FEATURE_FLAGS_VISUAL_GUIDE.md - Visual guide
- FEATURE_FLAGS_README.md - Summary
```

### 5.2 Create Backup
- [ ] Backup all modified files
- [ ] Document original state
- [ ] Save API Gateway configuration
- [ ] Export DynamoDB table schema

## Step 6: Post-Deployment

### 6.1 Monitor CloudWatch Logs
- [ ] Check Lambda function logs
- [ ] Verify no errors
- [ ] Monitor API Gateway metrics
- [ ] Check DynamoDB read/write units

### 6.2 Test Edge Cases
- [ ] Test with expired JWT token
- [ ] Test with invalid feature_id
- [ ] Test with missing permissions
- [ ] Test CORS from different origins

### 6.3 Performance Check
- [ ] Verify API response time < 500ms
- [ ] Check DynamoDB query performance
- [ ] Monitor Lambda cold starts
- [ ] Test with multiple concurrent requests

### 6.4 Security Review
- [ ] Verify admin-only endpoints require auth
- [ ] Check JWT token validation
- [ ] Ensure public endpoints don't leak sensitive data
- [ ] Review CORS configuration

## Rollback Plan (If Needed)

### If Something Goes Wrong:
1. [ ] Restore original navbar.js from backup
2. [ ] Restore original election-map.html from backup
3. [ ] Restore original index.html from backup
4. [ ] Remove Feature Flags link from admin.html
5. [ ] Delete Lambda function (optional)
6. [ ] Delete API Gateway (optional)
7. [ ] Delete DynamoDB table (optional)

### Quick Rollback Commands:
```powershell
# Restore files from backup
aws s3 cp s3://your-bucket/backups/navbar.js s3://your-bucket/navbar.js
aws s3 cp s3://your-bucket/backups/election-map.html s3://your-bucket/election-map.html
aws s3 cp s3://your-bucket/backups/index.html s3://your-bucket/index.html

# Invalidate cache
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

## Success Criteria

### ✅ Deployment is Successful When:
- [ ] DynamoDB table exists with default flag
- [ ] Lambda function deploys without errors
- [ ] API Gateway returns valid responses
- [ ] Admin interface loads and functions
- [ ] Feature can be toggled on/off
- [ ] Public users see correct status
- [ ] Admins can preview disabled features
- [ ] Volunteer count updates automatically
- [ ] All three test scenarios pass
- [ ] No errors in CloudWatch Logs

## Estimated Time

- **Backend Deployment**: 15 minutes
- **Frontend Configuration**: 10 minutes
- **Integration**: 15 minutes
- **Testing**: 20 minutes
- **Documentation**: 10 minutes

**Total**: ~70 minutes (1 hour 10 minutes)

## Support

If you encounter issues:
1. Check CloudWatch Logs for Lambda errors
2. Verify API Gateway URL is correct
3. Test API endpoints with curl/Postman
4. Review browser console for JavaScript errors
5. Refer to docs/FEATURE_FLAGS_GUIDE.md

## Final Checklist

- [ ] All backend components deployed
- [ ] All frontend files updated and uploaded
- [ ] All three test scenarios pass
- [ ] Documentation updated
- [ ] Backup created
- [ ] Team notified of new feature

---

**Deployment Date**: _______________
**Deployed By**: _______________
**API Gateway URL**: _______________
**Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Complete
