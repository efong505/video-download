# API URL Mapping: Old → New

## Overview

This document maps all current API endpoints to the new unified API structure.

**Old Pattern**: `https://{random-id}.execute-api.us-east-1.amazonaws.com/prod/{path}`
**New Pattern**: `https://api.christianconservativestoday.com/{service}/{path}`

---

## Service Mappings

### 1. Admin API
**Lambda**: `admin_api`
**Old URL**: `https://k2avuckm38.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/admin/`

**Endpoints**:
- GET `/admin/users` → `/admin/users`
- POST `/admin/videos` → `/admin/videos`
- PUT `/admin/articles/{id}` → `/admin/articles/{id}`
- DELETE `/admin/comments/{id}` → `/admin/comments/{id}`

---

### 2. Auth API
**Lambda**: `auth_api`
**Old URL**: `https://r6l0z3605f.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/auth/`

**Endpoints**:
- POST `/auth/login` → `/auth/login`
- POST `/auth/register` → `/auth/register`
- POST `/auth/refresh` → `/auth/refresh`
- GET `/auth/verify` → `/auth/verify`

---

### 3. Articles API
**Lambda**: `articles_api`
**Old URL**: `https://fr3hh94h4a.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/articles/`

**Endpoints**:
- GET `/articles` → `/articles`
- GET `/articles/{id}` → `/articles/{id}`
- POST `/articles` → `/articles`
- PUT `/articles/{id}` → `/articles/{id}`
- GET `/articles/search?q={query}` → `/articles/search?q={query}`
- GET `/articles/bible-verse?book={book}&chapter={ch}&verse={v}` → `/articles/bible-verse?book={book}&chapter={ch}&verse={v}`

---

### 4. Videos API
**Lambda**: `video_list_api`
**Old URL**: `https://wfeds5lejb.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/videos/`

**Endpoints**:
- GET `/videos` → `/videos`
- GET `/videos/{id}` → `/videos/{id}`
- POST `/videos` → `/videos`
- PUT `/videos/{id}` → `/videos/{id}`
- DELETE `/videos/{id}` → `/videos/{id}`

---

### 5. News API
**Lambda**: `news_api`
**Old URL**: `https://xr1xcc83bj.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/news/`

**Endpoints**:
- GET `/news` → `/news`
- GET `/news/{id}` → `/news/{id}`
- POST `/news` → `/news`
- PUT `/news/{id}` → `/news/{id}`
- GET `/news/breaking` → `/news/breaking`

---

### 6. Resources API
**Lambda**: `resources_api`
**Old URL**: `https://ckbtfz4vbl.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/resources/`

**Endpoints**:
- GET `/resources` → `/resources`
- GET `/resources/{id}` → `/resources/{id}`
- POST `/resources` → `/resources`
- PUT `/resources/{id}` → `/resources/{id}`
- GET `/resources/categories` → `/resources/categories`

---

### 7. Contributors API
**Lambda**: `contributors_api`
**Old URL**: `https://hzursivfuk.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/contributors/`

**Endpoints**:
- GET `/contributors` → `/contributors`
- GET `/contributors/{id}` → `/contributors/{id}`
- POST `/contributors` → `/contributors`
- PUT `/contributors/{id}` → `/contributors/{id}`
- GET `/contributors/races` → `/contributors/races`
- GET `/contributors/candidates` → `/contributors/candidates`
- GET `/contributors/summaries/{state}` → `/contributors/summaries/{state}`

---

### 8. Comments API
**Lambda**: `comments_api`
**Old URL**: `https://l10alau5g3.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/comments/`

**Endpoints**:
- GET `/comments?articleId={id}` → `/comments?articleId={id}`
- POST `/comments` → `/comments`
- PUT `/comments/{id}` → `/comments/{id}`
- DELETE `/comments/{id}` → `/comments/{id}`
- POST `/comments/{id}/approve` → `/comments/{id}/approve`

---

### 9. Tags API
**Lambda**: `tag_api`
**Old URL**: `https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/tags/`

**Endpoints**:
- GET `/tags` → `/tags`
- POST `/tags` → `/tags`
- GET `/tags/{id}/articles` → `/tags/{id}/articles`

---

### 10. Prayer API
**Lambda**: `prayer_api`
**Old URL**: `https://cayl9dmtaf.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/prayer/`

**Endpoints**:
- GET `/prayer/requests` → `/prayer/requests`
- POST `/prayer/requests` → `/prayer/requests`
- PUT `/prayer/requests/{id}` → `/prayer/requests/{id}`
- POST `/prayer/requests/{id}/pray` → `/prayer/requests/{id}/pray`

---

### 11. Events API
**Lambda**: `events_api`
**Old URL**: `https://{id}.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/events/`

**Endpoints**:
- GET `/events` → `/events`
- POST `/events` → `/events`
- PUT `/events/{id}` → `/events/{id}`
- DELETE `/events/{id}` → `/events/{id}`

---

### 12. Email Subscription API
**Lambda**: `email_subscription_api`
**Old URL**: `https://niexv1rw75.execute-api.us-east-1.amazonaws.com/`
**New URL**: `https://api.christianconservativestoday.com/email/`

**Endpoints**:
- POST `/email/subscribe` → `/email/subscribe`
- POST `/email/unsubscribe` → `/email/unsubscribe`
- GET `/email/verify?token={token}` → `/email/verify?token={token}`
- POST `/email/send-newsletter` → `/email/send-newsletter`

---

### 13. Ministry Tools API
**Lambda**: `ministry_tools_api`
**Old URL**: `https://gu6c08ctel.execute-api.us-east-1.amazonaws.com/`
**New URL**: `https://api.christianconservativestoday.com/ministry/`

**Endpoints**:
- GET `/ministry/tools` → `/ministry/tools`
- POST `/ministry/tools` → `/ministry/tools`

---

### 14. Notifications API
**Lambda**: `notifications_api`
**Old URL**: `https://lc7w6ebg4m.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/notifications/`

**Endpoints**:
- GET `/notifications` → `/notifications`
- POST `/notifications` → `/notifications`
- PUT `/notifications/{id}/read` → `/notifications/{id}/read`

---

### 15. URL Analysis API
**Lambda**: `url_analysis_api`
**Old URL**: `https://q65k3dbpd7.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/url-analysis/`

**Endpoints**:
- POST `/url-analysis/analyze` → `/url-analysis/analyze`

---

### 16. PayPal Billing API
**Lambda**: `paypal_billing_api`
**Old URL**: `https://{id}.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/paypal/`

**Endpoints**:
- POST `/paypal/create-subscription` → `/paypal/create-subscription`
- POST `/paypal/webhook` → `/paypal/webhook`
- GET `/paypal/subscription/{id}` → `/paypal/subscription/{id}`

---

### 17. Video Downloader API
**Lambda**: `downloader`
**Old URL**: `https://j3w8kgqlvi.execute-api.us-east-1.amazonaws.com/prod/`
**New URL**: `https://api.christianconservativestoday.com/download/`

**Endpoints**:
- POST `/download` → `/download`
- GET `/download/status/{id}` → `/download/status/{id}`

---

## Frontend Update Checklist

Update these files to use new API URLs:

### JavaScript Files
- [ ] `admin.html` - Update admin API calls
- [ ] `articles.html` - Update articles API calls
- [ ] `article.html` - Update article detail API calls
- [ ] `videos.html` - Update videos API calls
- [ ] `news.html` - Update news API calls
- [ ] `resources.html` - Update resources API calls
- [ ] `election-map.html` - Update contributors API calls
- [ ] `create-article.html` - Update article creation API
- [ ] `edit-article.html` - Update article editing API
- [ ] `video-downloader.html` - Update download API
- [ ] `download-status.html` - Update status API

### Configuration Files
- [ ] Update any hardcoded API URLs in config.js (if exists)
- [ ] Update environment variables
- [ ] Update API documentation

---

## Search & Replace Commands

### PowerShell
```powershell
# Replace admin API
Get-ChildItem -Path . -Filter *.html -Recurse | ForEach-Object {
    (Get-Content $_.FullName) -replace 'https://k2avuckm38.execute-api.us-east-1.amazonaws.com/prod/', 'https://api.christianconservativestoday.com/admin/' | Set-Content $_.FullName
}

# Replace auth API
Get-ChildItem -Path . -Filter *.html -Recurse | ForEach-Object {
    (Get-Content $_.FullName) -replace 'https://r6l0z3605f.execute-api.us-east-1.amazonaws.com/prod/', 'https://api.christianconservativestoday.com/auth/' | Set-Content $_.FullName
}

# Repeat for all APIs...
```

### Bash
```bash
# Replace admin API
find . -name "*.html" -type f -exec sed -i 's|https://k2avuckm38.execute-api.us-east-1.amazonaws.com/prod/|https://api.christianconservativestoday.com/admin/|g' {} +

# Replace auth API
find . -name "*.html" -type f -exec sed -i 's|https://r6l0z3605f.execute-api.us-east-1.amazonaws.com/prod/|https://api.christianconservativestoday.com/auth/|g' {} +

# Repeat for all APIs...
```

---

## Testing Checklist

After migration, test each endpoint:

- [ ] Admin: Login, user management, content moderation
- [ ] Auth: Login, register, token refresh
- [ ] Articles: List, view, create, edit, search, Bible verses
- [ ] Videos: List, view, upload, edit, delete
- [ ] News: List, view, create, breaking news
- [ ] Resources: List, view, categories
- [ ] Contributors: Election data, races, candidates, summaries
- [ ] Comments: List, create, approve, delete
- [ ] Tags: List, create, filter articles
- [ ] Prayer: List requests, create, pray
- [ ] Events: List, create, edit, delete
- [ ] Email: Subscribe, unsubscribe, verify, send newsletter
- [ ] Ministry: Tools list, create
- [ ] Notifications: List, create, mark read
- [ ] URL Analysis: Analyze URL
- [ ] PayPal: Create subscription, webhook, get subscription
- [ ] Download: Start download, check status

---

## Monitoring

After migration, monitor these metrics:

- API Gateway 4XX errors (should be <1%)
- API Gateway 5XX errors (should be <0.1%)
- Lambda errors (should be <0.1%)
- API latency (should be <500ms p99)
- CORS errors (should be 0)

---

**Next**: See `GITHUB_ACTIONS_SETUP.md` for CI/CD automation.
