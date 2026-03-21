# Feature Flags System - Complete Implementation Guide

## Overview

The Feature Flags system allows you to enable/disable features on your platform without code deployment. This is especially useful for seasonal features like the Election Tracking System that depend on volunteer support and election cycles.

## System Components

### 1. Backend (AWS Lambda)
- **Function**: `feature-flags-api`
- **File**: `feature_flags_api/index.py`
- **Database**: DynamoDB table `feature-flags`
- **API**: REST API with GET, POST, PUT, DELETE operations

### 2. Frontend
- **Admin Interface**: `admin-feature-flags.html`
- **Helper Library**: `feature-flags.js`
- **Integration**: All pages that need feature checking

### 3. Database Schema

```javascript
{
  feature_id: "election_system",           // Primary key
  enabled: true,                           // Feature on/off
  name: "Election Tracking System",        // Display name
  description: "50-state election coverage...",
  admin_only_access: true,                 // Admins can access when disabled
  seasonal: true,                          // Is this a seasonal feature?
  volunteer_dependent: true,               // Requires volunteers?
  min_volunteers_required: 10,             // Minimum volunteers needed
  active_volunteers: 15,                   // Current volunteer count (auto-calculated)
  season_start: "2025-01-01T00:00:00Z",   // Season start date
  season_end: "2026-11-30T23:59:59Z",     // Season end date
  disable_reason: "Between election cycles", // Why disabled (shown to users)
  volunteer_signup_url: "/apply-correspondent.html",
  created_at: "2025-01-15T00:00:00Z",
  updated_at: "2025-01-15T00:00:00Z",
  updated_by: "super@admin.com"
}
```

## Installation Steps

### Step 1: Create DynamoDB Table

```bash
python create_feature_flags_table.py
```

This creates the `feature-flags` table and inserts the default `election_system` flag.

### Step 2: Deploy Lambda Function

```powershell
.\deploy-feature-flags-api.ps1
```

**Before running**, update these values in the script:
- `$Role`: Your Lambda execution role ARN
- Ensure the role has DynamoDB read/write permissions

### Step 3: Create API Gateway

1. Go to AWS API Gateway Console
2. Create HTTP API (not REST API)
3. Add integration to `feature-flags-api` Lambda
4. Create routes:
   - `GET /feature-flags` (list all flags)
   - `POST /feature-flags` (create flag)
   - `PUT /feature-flags` (update flag)
   - `DELETE /feature-flags` (delete flag)
   - `OPTIONS /feature-flags` (CORS preflight)
5. Deploy to `prod` stage
6. Copy the API Gateway URL

### Step 4: Update Frontend Files

**In `feature-flags.js`:**
```javascript
API_URL: 'https://YOUR_API_GATEWAY_URL/prod/feature-flags',
```

**In `admin-feature-flags.html`:**
```javascript
const FEATURE_FLAGS_API = 'https://YOUR_API_GATEWAY_URL/prod/feature-flags';
```

### Step 5: Add to Admin Navigation

**In `admin.html`**, add this link to the admin menu:

```html
<a href="admin-feature-flags.html" class="nav-link">
    <i class="fas fa-flag"></i> Feature Flags
</a>
```

### Step 6: Upload Files to S3

```powershell
aws s3 cp admin-feature-flags.html s3://your-bucket/
aws s3 cp feature-flags.js s3://your-bucket/
```

## Usage Examples

### Example 1: Hide Election Link When Disabled

**In `navbar.html` or `navbar.js`:**

```html
<!-- Include feature flags helper -->
<script src="feature-flags.js"></script>

<script>
// Hide election link if feature is disabled
document.addEventListener('DOMContentLoaded', async () => {
    await FeatureFlags.hideNavLinkIfDisabled('election_system', '#election-nav-link');
});
</script>
```

### Example 2: Protect Election Map Page

**In `election-map.html`:**

```html
<script src="feature-flags.js"></script>
<script>
// Require feature to be enabled or user to be admin
document.addEventListener('DOMContentLoaded', async () => {
    await FeatureFlags.requireFeature('election_system', 'index.html');
});
</script>
```

### Example 3: Show Feature Status Banner

**On homepage or feature page:**

```html
<div id="election-status"></div>

<script src="feature-flags.js"></script>
<script>
document.addEventListener('DOMContentLoaded', async () => {
    await FeatureFlags.showStatusBanner('election_system', 'election-status');
});
</script>
```

### Example 4: Conditional Feature Display

**In any page:**

```javascript
// Check if feature is enabled
const electionEnabled = await FeatureFlags.isEnabled('election_system');

if (electionEnabled) {
    // Show election features
    document.getElementById('election-section').style.display = 'block';
} else {
    // Show "coming soon" message
    document.getElementById('election-section').innerHTML = `
        <div class="alert alert-info">
            📅 Election coverage returns during active election cycles.
            <a href="/volunteer">Volunteer to help maintain this feature</a>
        </div>
    `;
}
```

## Admin Workflow

### Disabling the Election Feature

1. Go to `admin-feature-flags.html`
2. Find "Election Tracking System"
3. Click "Disable" button
4. Optionally update "Disable Reason": "Between election cycles - Returns 2027"
5. Feature is now hidden from public users
6. Admins can still access via direct URL with "Admin Preview" banner

### Re-enabling the Election Feature

1. Go to `admin-feature-flags.html`
2. Find "Election Tracking System"
3. Click "Enable" button
4. Feature is now visible to all users
5. Update season dates if needed

### Editing Feature Settings

1. Click "Edit" button on any feature
2. Update fields:
   - **Enabled**: Toggle on/off
   - **Seasonal**: Check if feature is seasonal
   - **Season Start/End**: Set active dates
   - **Volunteer Dependent**: Check if requires volunteers
   - **Min Volunteers**: Set minimum required (e.g., 10)
   - **Disable Reason**: Message shown to users when disabled
   - **Volunteer Signup URL**: Link to volunteer application
3. Click "Save"

## Public User Experience

### When Feature is ENABLED:

**Homepage:**
```
✅ Election Coverage is active (15 volunteers)
Track races in all 50 states with our volunteer correspondents!
[View Election Map]
```

**Navigation:**
- "🗳️ Election Map" link visible in navbar

**Election Map Page:**
- Full access to all features
- No banners or warnings

### When Feature is DISABLED:

**Homepage:**
```
⚠️ Election Coverage is currently inactive: Between election cycles
Our election tracking returns during active election cycles with volunteer support.
Next activation: 2027 election cycle
[Volunteer to Help Maintain This Feature]
```

**Navigation:**
- "🗳️ Election Map" link hidden from navbar

**Election Map Page (direct URL):**
- Redirects to homepage with message: "This feature is currently unavailable."

### Admin Experience (When Disabled):

**Navigation:**
- "🗳️ Election Map" link visible with badge: "Admin Preview"

**Election Map Page:**
- Full access to all features
- Yellow banner at top:
  ```
  ⚠️ Admin Preview Mode
  This feature is currently disabled for public users. 
  You're viewing it as an administrator.
  [Manage Feature Flags]
  ```

## API Endpoints

### Public Endpoints (No Auth Required)

**GET /feature-flags?action=list**
- Returns all flags with public info only
- Response: `[{feature_id, enabled, name, seasonal, volunteer_dependent, ...}]`

**GET /feature-flags?action=get&feature_id=election_system**
- Returns single flag with public info
- Response: `{feature_id, enabled, name, ...}`

### Admin Endpoints (Auth Required)

**POST /feature-flags?action=create**
- Create new feature flag
- Body: `{feature_id, name, description, enabled, ...}`
- Requires: Admin JWT token in Authorization header

**PUT /feature-flags?action=update**
- Update existing flag
- Body: `{feature_id, enabled, name, ...}`
- Requires: Admin JWT token

**DELETE /feature-flags?action=delete&feature_id=X**
- Delete feature flag
- Requires: Admin JWT token

## Volunteer Count Tracking

The system automatically tracks active volunteers for the election system:

1. Queries `contributors` table for `status = 'active'`
2. Updates `active_volunteers` field in real-time
3. Displays progress bar in admin interface
4. Shows volunteer count in public status messages

**Example:**
- Min Required: 10 volunteers
- Active: 15 volunteers
- Progress: 150% (Green bar)
- Status: "✅ Election Coverage is active (15 volunteers)"

## Seasonal Activation Logic

Features can be automatically enabled/disabled based on season dates:

```javascript
// In Lambda function
function check_seasonal_status(flag) {
    const now = new Date();
    const start = new Date(flag.season_start);
    const end = new Date(flag.season_end);
    
    return start <= now && now <= end;
}
```

**Recommendation**: Set up CloudWatch Events to run daily check:
1. Check all seasonal features
2. Auto-enable if within season and volunteers >= minimum
3. Auto-disable if outside season or volunteers < minimum
4. Send email notification to admins on status changes

## Best Practices

### 1. Feature Naming
- Use lowercase with underscores: `election_system`, `newsletter_system`
- Keep IDs short and descriptive
- Use clear display names: "Election Tracking System"

### 2. Disable Reasons
- Be specific: "Between election cycles - Returns January 2027"
- Include next activation date if known
- Mention volunteer needs: "Seeking 5 more volunteers to reactivate"

### 3. Admin Access
- Always set `admin_only_access: true` for features in development
- Allows testing without public visibility
- Admins see "Admin Preview" badge

### 4. Seasonal Features
- Set realistic season dates
- Update dates annually
- Consider buffer time before/after elections

### 5. Volunteer Thresholds
- Set achievable minimums (10-15 volunteers)
- Monitor volunteer count regularly
- Send recruitment emails when below threshold

## Troubleshooting

### Issue: Feature flag not loading
**Solution**: Check browser console for API errors. Verify API Gateway URL is correct in `feature-flags.js`.

### Issue: Admin can't update flags
**Solution**: Verify JWT token is valid and user role is `admin` or `super_user`.

### Issue: Volunteer count not updating
**Solution**: Check that `contributors` table has `status` field. Lambda function queries this field.

### Issue: CORS errors
**Solution**: Ensure Lambda function returns CORS headers in all responses. Add OPTIONS route to API Gateway.

### Issue: Feature still visible when disabled
**Solution**: Clear browser cache. Check that page is calling `FeatureFlags.isEnabled()` correctly.

## Future Enhancements

### Planned Features:
- [ ] Scheduled activation/deactivation
- [ ] Email notifications on status changes
- [ ] Feature usage analytics
- [ ] A/B testing support
- [ ] Feature dependencies (Feature B requires Feature A)
- [ ] Rollout percentage (enable for 10% of users)
- [ ] Geographic restrictions (enable only in certain states)

### CloudWatch Integration:
- [ ] Daily cron job to check seasonal status
- [ ] Auto-enable/disable based on volunteer count
- [ ] Alert admins when volunteers drop below threshold
- [ ] Log all feature flag changes for audit trail

## Support

For issues or questions:
1. Check CloudWatch Logs for Lambda function errors
2. Verify DynamoDB table has correct schema
3. Test API endpoints with Postman or curl
4. Review browser console for JavaScript errors

## Summary

The Feature Flags system provides:
✅ Easy enable/disable without code deployment
✅ Seasonal feature management
✅ Volunteer dependency tracking
✅ Admin-only preview mode
✅ Public status messaging
✅ Audit trail of changes

This allows you to maintain the election feature privately while it's disabled publicly, and easily re-enable it when ready for the next election cycle.
