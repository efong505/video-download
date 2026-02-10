# JWT Token Expiration Fix

## Issue
Site was not automatically logging out users when JWT tokens expired after 24 hours. Users appeared logged in but API calls failed with 401/403 errors.

## Root Cause
Pages were missing the `token-validator.js` script that checks JWT expiration on page load.

## Solution
Added `<script src="assets/js/token-validator.js"></script>` to all protected pages.

## Pages Updated
✅ videos.html
✅ articles.html  
✅ news.html
✅ resources.html

## Remaining Pages to Update
- create-article.html
- edit-article.html
- create-news.html
- edit-news.html
- admin.html
- admin-contributors.html
- admin-resources.html
- admin-templates.html
- profile.html
- user-page.html

## How Token Validator Works
1. Runs on page load via `window.addEventListener('load', checkTokenExpiration)`
2. Reads `auth_token` from localStorage
3. Decodes JWT payload and checks `exp` timestamp
4. If expired: Shows alert, clears localStorage, redirects to login.html
5. If invalid: Clears localStorage, redirects to login.html

## Deployment
```powershell
# Upload updated pages
aws s3 cp videos.html s3://my-video-downloads-bucket/
aws s3 cp articles.html s3://my-video-downloads-bucket/
aws s3 cp news.html s3://my-video-downloads-bucket/
aws s3 cp resources.html s3://my-video-downloads-bucket/

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id E3N00R2D2NE9C5 --paths "/*"
```

## Testing
1. Log in to site
2. Manually edit localStorage auth_token to have expired timestamp
3. Refresh page
4. Should see "Your session has expired. Please log in again." alert
5. Should redirect to login.html
