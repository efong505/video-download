# Feature Flags - Quick Implementation Examples

## 1. Update navbar.js (Hide Election Link When Disabled)

Add this code to your `navbar.js` file after the navbar is loaded:

```javascript
// At the top of navbar.js, after other constants
const FEATURE_FLAGS_API = 'https://YOUR_API_GATEWAY_URL/prod/feature-flags';

// Add this function
async function checkElectionFeature() {
    try {
        const response = await fetch(`${FEATURE_FLAGS_API}?action=get&feature_id=election_system`);
        if (!response.ok) return;
        
        const flag = await response.json();
        const electionLink = document.querySelector('a[href="election-map.html"]');
        
        if (!electionLink) return;
        
        // Check if user is admin
        const userData = localStorage.getItem('user_data');
        const isAdmin = userData && (JSON.parse(userData).role === 'admin' || JSON.parse(userData).role === 'super_user');
        
        if (!flag.enabled && !isAdmin) {
            // Hide link for non-admins
            electionLink.style.display = 'none';
        } else if (!flag.enabled && isAdmin) {
            // Show admin preview badge
            electionLink.innerHTML += ' <span class="badge bg-warning text-dark ms-1">Preview</span>';
        }
    } catch (error) {
        console.error('Error checking election feature:', error);
    }
}

// Call this after navbar loads
document.addEventListener('DOMContentLoaded', () => {
    checkElectionFeature();
});
```

## 2. Update election-map.html (Protect Page Access)

Add this at the top of the `<script>` section in `election-map.html`:

```javascript
// Add at the very top of your script section
const FEATURE_FLAGS_API = 'https://YOUR_API_GATEWAY_URL/prod/feature-flags';

async function checkFeatureAccess() {
    try {
        const response = await fetch(`${FEATURE_FLAGS_API}?action=get&feature_id=election_system`);
        if (!response.ok) {
            window.location.href = 'index.html';
            return;
        }
        
        const flag = await response.json();
        
        if (flag.enabled) {
            // Feature is enabled, allow access
            return;
        }
        
        // Feature is disabled, check if admin
        const userData = localStorage.getItem('user_data');
        if (!userData) {
            alert('This feature is currently unavailable.');
            window.location.href = 'index.html';
            return;
        }
        
        const user = JSON.parse(userData);
        if (user.role === 'admin' || user.role === 'super_user') {
            // Show admin preview banner
            showAdminBanner();
        } else {
            alert('This feature is currently unavailable.');
            window.location.href = 'index.html';
        }
    } catch (error) {
        console.error('Error checking feature access:', error);
    }
}

function showAdminBanner() {
    const banner = document.createElement('div');
    banner.className = 'alert alert-warning position-fixed top-0 start-50 translate-middle-x mt-3';
    banner.style.zIndex = '9999';
    banner.style.maxWidth = '600px';
    banner.innerHTML = `
        <strong>⚠️ Admin Preview Mode</strong><br>
        This feature is currently disabled for public users. You're viewing it as an administrator.
        <a href="admin-feature-flags.html" class="alert-link ms-2">Manage Feature Flags</a>
    `;
    document.body.insertBefore(banner, document.body.firstChild);
}

// Call this before loading data
checkFeatureAccess().then(() => {
    // Your existing loadData() call
    loadData();
});
```

## 3. Update index.html (Show Feature Status)

Add this section where you want to show the election feature status:

```html
<!-- Add this div where you want the status to appear -->
<div class="container mt-4">
    <div id="election-feature-status"></div>
</div>

<!-- Add this script at the bottom before </body> -->
<script>
const FEATURE_FLAGS_API = 'https://YOUR_API_GATEWAY_URL/prod/feature-flags';

async function showElectionStatus() {
    try {
        const response = await fetch(`${FEATURE_FLAGS_API}?action=get&feature_id=election_system`);
        if (!response.ok) return;
        
        const flag = await response.json();
        const container = document.getElementById('election-feature-status');
        
        if (!container) return;
        
        if (flag.enabled) {
            // Feature is enabled
            container.innerHTML = `
                <div class="card" style="border: 2px solid #28a745; border-radius: 12px;">
                    <div class="card-body">
                        <h5 class="card-title">
                            <span class="badge bg-success">Active</span>
                            🗳️ ${flag.name}
                        </h5>
                        <p class="card-text">
                            Tracking races in all 50 states thanks to our ${flag.active_volunteers} volunteer correspondents!
                        </p>
                        <a href="election-map.html" class="btn btn-primary">View Election Map</a>
                    </div>
                </div>
            `;
        } else {
            // Feature is disabled
            let message = flag.disable_reason || 'Currently inactive';
            let nextSeason = '';
            
            if (flag.season_start) {
                const start = new Date(flag.season_start);
                if (start > new Date()) {
                    nextSeason = `<small class="text-muted d-block mt-2">Next activation: ${start.toLocaleDateString()}</small>`;
                }
            }
            
            container.innerHTML = `
                <div class="card" style="border: 2px solid #ffc107; border-radius: 12px;">
                    <div class="card-body">
                        <h5 class="card-title">
                            <span class="badge bg-warning text-dark">Seasonal</span>
                            🗳️ ${flag.name}
                        </h5>
                        <p class="card-text">
                            ⚠️ ${message}
                        </p>
                        <p class="card-text">
                            Our election tracking returns during active election cycles with volunteer support.
                            ${nextSeason}
                        </p>
                        ${flag.volunteer_signup_url ? 
                            `<a href="${flag.volunteer_signup_url}" class="btn btn-outline-primary">Volunteer to Help Maintain This Feature</a>` : 
                            ''}
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error showing election status:', error);
    }
}

// Call on page load
document.addEventListener('DOMContentLoaded', showElectionStatus);
</script>
```

## 4. Update admin.html (Add Feature Flags Link)

Find the admin navigation menu and add this link:

```html
<!-- In your admin navigation menu -->
<li class="nav-item">
    <a class="nav-link" href="admin-feature-flags.html">
        <i class="fas fa-flag"></i> Feature Flags
    </a>
</li>
```

Or if you have a secondary menu:

```html
<a href="admin-feature-flags.html" class="btn btn-outline-primary">
    <i class="fas fa-flag"></i> Feature Flags
</a>
```

## 5. Simple Feature Check (Any Page)

For a simple check on any page:

```javascript
// Simple inline check
fetch('https://YOUR_API_GATEWAY_URL/prod/feature-flags?action=get&feature_id=election_system')
    .then(r => r.json())
    .then(flag => {
        if (flag.enabled) {
            // Show feature
            document.getElementById('election-section').style.display = 'block';
        } else {
            // Hide feature
            document.getElementById('election-section').style.display = 'none';
        }
    })
    .catch(err => console.error('Feature check failed:', err));
```

## 6. Using the Helper Library (Recommended)

If you include `feature-flags.js` on your page:

```html
<script src="feature-flags.js"></script>
<script>
// Simple check
const enabled = await FeatureFlags.isEnabled('election_system');

// Get full flag details
const flag = await FeatureFlags.getFlag('election_system');

// Show status banner
await FeatureFlags.showStatusBanner('election_system', 'status-container');

// Hide nav link if disabled
await FeatureFlags.hideNavLinkIfDisabled('election_system', '#election-link');

// Require feature (redirect if disabled and not admin)
await FeatureFlags.requireFeature('election_system', 'index.html');
</script>
```

## 7. Testing the Implementation

### Test 1: Feature Enabled
1. Go to `admin-feature-flags.html`
2. Ensure "Election Tracking System" is enabled
3. Visit homepage - should see green "Active" card
4. Check navbar - "Election Map" link visible
5. Visit `election-map.html` - full access, no banner

### Test 2: Feature Disabled (Admin)
1. Go to `admin-feature-flags.html`
2. Disable "Election Tracking System"
3. Visit homepage - should see yellow "Seasonal" card
4. Check navbar - "Election Map" link visible with "Preview" badge
5. Visit `election-map.html` - full access with yellow "Admin Preview" banner

### Test 3: Feature Disabled (Public User)
1. Logout or use incognito window
2. Visit homepage - should see yellow "Seasonal" card with volunteer link
3. Check navbar - "Election Map" link hidden
4. Try to visit `election-map.html` directly - redirects to homepage with alert

## 8. Deployment Checklist

- [ ] Create DynamoDB table: `python create_feature_flags_table.py`
- [ ] Deploy Lambda function: `.\deploy-feature-flags-api.ps1`
- [ ] Create API Gateway and get URL
- [ ] Update `feature-flags.js` with API URL
- [ ] Update `admin-feature-flags.html` with API URL
- [ ] Update `navbar.js` with feature check code
- [ ] Update `election-map.html` with access protection
- [ ] Update `index.html` with status display
- [ ] Update `admin.html` with Feature Flags link
- [ ] Upload all files to S3
- [ ] Test all three scenarios (enabled, disabled-admin, disabled-public)
- [ ] Document API Gateway URL in PROGRESS.md

## Quick Reference: API URLs to Update

Replace `YOUR_API_GATEWAY_URL` in these files:
1. `feature-flags.js` - Line 7
2. `admin-feature-flags.html` - Line 85
3. `navbar.js` - Add constant at top
4. `election-map.html` - Add constant at top
5. `index.html` - Add constant in script section

Example URL format:
```
https://abc123xyz.execute-api.us-east-1.amazonaws.com/prod/feature-flags
```

## Summary

This implementation gives you:
✅ Public users see feature status and volunteer recruitment
✅ Admins can access disabled features with preview banner
✅ Easy toggle in admin interface
✅ Automatic volunteer count tracking
✅ Seasonal activation messaging
✅ No code deployment needed to enable/disable

The election feature can now be maintained privately while disabled, and easily re-enabled for the next election cycle!
