# Phase 3: JavaScript Consolidation

## Overview
Consolidate duplicate JavaScript functions across 42 HTML pages into shared `common-utils.js` file.

## Created Files
- `assets/js/common-utils.js` - Shared JavaScript utilities (8.5 KB)

## Functions Consolidated

### Authentication (68 duplicates found)
- `getAuthToken()` - Get JWT token from localStorage
- `getUserData()` - Get parsed user data object
- `getUserRole()` - Get user role (admin/super_user/editor/user)
- `isAuthenticated()` - Check if user is logged in
- `isAdmin()` - Check if user is admin or super_user
- `isSuperUser()` - Check if user is super_user
- `isEditor()` - Check if user is editor/admin/super_user
- `logout()` - Clear auth data and redirect to login
- `requireAuth()` - Redirect if not authenticated
- `requireAdmin()` - Redirect if not admin

### API Endpoints (Centralized)
- `API_ENDPOINTS` object with all API URLs
- `apiRequest()` - Wrapper for fetch with auth headers

### UI Utilities
- `showNotification()` - Display success/error/warning messages
- `handleError()` - Centralized error handling
- `showLoading()` / `hideLoading()` - Loading spinners
- `copyToClipboard()` - Copy text with fallback

### Data Formatting
- `formatDate()` - Format ISO dates to readable format
- `formatFileSize()` - Convert bytes to KB/MB/GB
- `debounce()` - Debounce function calls
- `isValidEmail()` - Email validation regex
- `sanitizeHTML()` - Basic HTML sanitization

### URL Utilities
- `getQueryParam()` - Get URL parameter value
- `setQueryParam()` - Set URL parameter

## Usage Example

### Before (Duplicate Code)
```javascript
// In every HTML file
const AUTH_API = 'https://r6l0z3605f.execute-api.us-east-1.amazonaws.com/prod/auth';
const token = localStorage.getItem('auth_token');
if (!token) {
    window.location.href = 'login.html';
}
```

### After (Shared Utilities)
```html
<script src="assets/js/common-utils.js"></script>
<script>
    requireAuth(); // One line replaces 4 lines
</script>
```

## Implementation Plan

### Step 1: Add Script Tag (All Pages)
Add before closing `</body>` tag:
```html
<script src="assets/js/common-utils.js"></script>
```

### Step 2: Replace Authentication Code
**Find:**
```javascript
const token = localStorage.getItem('auth_token');
if (!token) {
    window.location.href = 'login.html';
    return;
}
```

**Replace with:**
```javascript
requireAuth();
```

### Step 3: Replace API Endpoints
**Find:**
```javascript
const AUTH_API = 'https://r6l0z3605f.execute-api.us-east-1.amazonaws.com/prod/auth';
const ARTICLES_API = 'https://fr3hh94h4a.execute-api.us-east-1.amazonaws.com/prod/articles';
```

**Replace with:**
```javascript
// Use API_ENDPOINTS.AUTH, API_ENDPOINTS.ARTICLES, etc.
```

### Step 4: Replace Notification Code
**Find:**
```javascript
const notification = document.createElement('div');
notification.style.cssText = '...';
notification.textContent = message;
document.body.appendChild(notification);
setTimeout(() => notification.remove(), 3000);
```

**Replace with:**
```javascript
showNotification('Message here', 'success');
```

### Step 5: Replace Logout Functions
**Find:**
```javascript
function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    window.location.href = 'login.html';
}
```

**Replace with:**
```javascript
// Use logout() from common-utils.js
```

## Pages to Update (Priority Order)

### High Priority (Authentication Heavy)
1. admin.html
2. admin-contributors.html
3. admin-resources.html
4. admin-templates.html
5. profile.html
6. create-article.html
7. edit-article.html
8. create-news.html
9. edit-news.html
10. user-upload.html

### Medium Priority (API Heavy)
11. articles.html
12. news.html
13. resources.html
14. videos.html
15. election-map.html
16. article.html
17. news-article.html
18. user-page.html

### Low Priority (Minimal JS)
19. index.html
20. category.html
21. embed.html

## Estimated Savings
- **Lines Removed**: ~500+ duplicate lines
- **File Size Reduction**: ~15 KB per page (cached common-utils.js)
- **Maintenance**: Single source of truth for auth/API logic
- **Consistency**: Uniform error handling and notifications

## Testing Checklist
- [ ] Authentication redirects work
- [ ] Admin checks function correctly
- [ ] API requests include auth headers
- [ ] Notifications display properly
- [ ] Logout clears all data
- [ ] No JavaScript console errors
- [ ] All pages load common-utils.js successfully

## Deployment Steps
1. Upload `assets/js/common-utils.js` to S3
2. Update HTML pages with script tag
3. Test authentication flows
4. Invalidate CloudFront cache
5. Verify production functionality

## Next Phase
After Phase 3 completion, proceed to:
- **Phase 4**: Form styles consolidation
- **Phase 5**: Component styles (modals, tables, utilities)
