# Fix Guide for 7 Recurring Issues

## Issue 1: Scripture Lookup Not Working

**Symptom**: Bible verse lookup returns "Bible verse lookup not available - requests module missing"

**Root Cause**: Lambda function deployed without requests library

**Fix**:
```powershell
# Run the deployment script with dependencies
.\deploy-articles-api-with-deps.ps1
```

**Verification**:
1. Go to create-article.html
2. Enter "John 3:16" in Bible Verse Lookup
3. Click "Search Verse"
4. Should return verse text successfully

---

## Issue 2: JWT Token Expiration (False "Logged In" State)

**Symptom**: User appears logged in but API calls fail with 401/403 errors saying "must be admin"

**Root Cause**: JWT tokens expire after 24 hours but localStorage retains expired token

**Fix**: Add token validator to all protected pages

### Step 1: Token validator already created at `assets/js/token-validator.js`

### Step 2: Add to protected pages

Add this line to the `<head>` section of these files:
- admin.html
- create-article.html
- edit-article.html
- create-news.html
- edit-news.html
- admin-contributors.html
- admin-resources.html
- admin-templates.html
- profile.html
- user-page.html

```html
<script src="assets/js/token-validator.js"></script>
```

**Verification**:
1. Log in to the site
2. Manually edit localStorage token to have expired timestamp
3. Refresh page
4. Should automatically log out with "session expired" message

---

## Issue 3: Article/News Authors Showing Emails Instead of Names

**Symptom**: Articles and news show "super@admin.com" instead of "Edward Fong"

**Root Cause**: 
1. Lambda create functions not calling get_user_name() to populate author_name field
2. Existing records lack author_name field

**Fix for Articles**:

### Step 1: Verify articles_api Lambda has get_user_name() function

Check `articles_api/index.py` has this function (already present):
```python
def get_user_name(email):
    """Get user's display name from users table"""
    try:
        response = users_table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        users = response.get('Items', [])
        if users:
            user = users[0]
            first_name = user.get('first_name', '')
            last_name = user.get('last_name', '')
            if first_name and last_name:
                return f"{first_name} {last_name}"
            elif first_name:
                return first_name
            elif last_name:
                return last_name
        return email
    except Exception:
        return email
```

### Step 2: Verify create_article() calls get_user_name()

In `articles_api/index.py`, the create_article function should have:
```python
if '@' in author_input:
    author_email = author_input
    author_name = get_user_name(author_email)
else:
    author_name = author_input
    author_email = author_input
```

### Step 3: Deploy Lambda
```powershell
.\deploy-articles-api-with-deps.ps1
```

### Step 4: Run migration script to backfill existing articles
```powershell
python update_article_author_names.py
```

**Fix for News**:

### Step 1: Verify news_api Lambda has get_user_name() function (already present)

### Step 2: Run migration script to backfill existing news
```powershell
python update_news_author_names.py
```

Results: 6 news articles updated from email addresses to "Edward Fong"

**Verification**:
1. Go to articles.html or news.html
2. All articles should show author names (e.g., "Edward Fong") not emails
3. Create new article - should automatically use author name

---

## Issue 4: Old Menu Still Showing on Some Pages

**Symptom**: Some pages still have old hardcoded menu instead of unified navbar

**Root Cause**: Pages not updated to use navbar.html and navbar.js

**Fix**: Replace old menu with unified navbar

### Update page to use unified navbar:

```html
<!-- Replace old menu with this -->
<div id="navbar-container" data-page="page-name"></div>
<script src="navbar.js"></script>
<script>
    fetch('navbar.html')
        .then(r => r.text())
        .then(html => {
            document.getElementById('navbar-container').innerHTML = html;
            initNavbar();
        })
        .catch(err => console.error('Failed to load navbar:', err));
</script>
```

**Verification**:
1. Check page has unified navbar with all menu items
2. Admin link appears for admin/super_user roles
3. Logout works correctly

---

---

## Issue 5: Duplicate Candidates in Election Data

**Symptom**: Same candidate appears multiple times in election map

**Root Cause**: AI generated duplicate candidates across multiple chunk files

**Fix**:
```powershell
cd "Election Chunks/COMPLETE_STATE_TEMPLATES/Pennsylvania"
python clean_slate_upload.py
```

**Prevention**: Use deduplication script before upload

---

## Issue 6: Candidates in "Other Candidates" Section

**Symptom**: Candidates show under "Other Candidates" instead of their race

**Root Cause**: Candidates missing `race_id` field

**Fix**:
```powershell
cd "Election Chunks/COMPLETE_STATE_TEMPLATES/Pennsylvania"
python fix_candidate_race_ids.py
```

**Prevention**: Always include `race_id` when adding candidates

---

## Issue 7: Summary Guide Shows Wrong Candidate Count

**Symptom**: Summary shows 119 candidates but database has 12

**Root Cause**: Summary text has hardcoded counts that don't auto-update

**CRITICAL**: Check actual text pattern first!
```powershell
cd "Election Chunks/COMPLETE_STATE_TEMPLATES/Pennsylvania"
python check_summary.py
```

Then update the replace patterns in `update_summary_counts.py` to match actual text (e.g., "Total Candidates Profiled:" not "Total Candidates:").

**Fix**:
```powershell
python update_summary_counts.py
```

**Prevention**: Run after every data upload/change

---

## Issue 8: Edit News Page Shows Blank Fields

**Symptom**: When editing a news article, all form fields appear blank

**Root Cause**: API returns news object directly, not wrapped in `{news: {...}}`

**Fix**: In edit-news.html, change:
```javascript
.then(function(news) {
```
To:
```javascript
.then(function(data) {
    var news = data.news || data;
```

**Deployment**:
```powershell
aws s3 cp edit-news.html s3://my-video-downloads-bucket/
```

**Verification**:
1. Go to news.html
2. Click edit on any news article
3. All fields should populate correctly

---

## Issue 9: Social Media Previews Not Working

**Symptom**: Sharing articles/news on Facebook/Twitter shows no image or title

**Root Cause**: 
1. Base64 data URLs in og:image tags (social crawlers can't access)
2. Missing static preview HTML files for crawlers

**Fix**: Generate static preview HTML with proper meta tags

### Files Modified:
- create-article.html - Added generateAndUploadPreview() function
- edit-article.html - Added preview generation on update
- create-news.html - Added preview generation
- edit-news.html - Added preview generation

### Key Changes:
1. Use CloudFront URL for og:image: `https://d3oo5w3ywcz1uh.cloudfront.net/techcrosslogo.jpg`
2. Generate minimal HTML at `/previews/article-{id}.html` or `/previews/news-{id}.html`
3. Split script tags in strings: `'<scr'+'ipt>'` to avoid syntax errors

**Deployment**:
```powershell
aws s3 cp create-article.html s3://my-video-downloads-bucket/
aws s3 cp edit-article.html s3://my-video-downloads-bucket/
aws s3 cp create-news.html s3://my-video-downloads-bucket/
aws s3 cp edit-news.html s3://my-video-downloads-bucket/
```

**Verification**:
1. Create/edit article or news
2. Check S3 for `/previews/article-{id}.html` or `/previews/news-{id}.html`
3. Test URL in Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/
4. Should show proper title, description, and image

---

## Issue 10: News Articles Showing Email Instead of Author Name (PERMANENT FIX)

**Symptom**: News articles display author email (e.g., "super@admin.com") instead of name, and issue keeps recurring

**Root Causes**: 
1. news_api Lambda get_user_name() using get_item() instead of scan()
2. No author field in create/edit forms - author was auto-set from JWT token
3. Existing records lack author_name field

**Permanent Solution**: Add editable author field to forms

### Step 1: Fix news_api Lambda get_user_name()

Update `news_api/index.py`:
```python
def get_user_name(email):
    """Get user's display name from users table"""
    try:
        response = users_table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        users = response.get('Items', [])
        if users:
            user = users[0]
            first_name = user.get('first_name', '')
            last_name = user.get('last_name', '')
            if first_name and last_name:
                return f"{first_name} {last_name}"
            elif first_name:
                return first_name
            elif last_name:
                return last_name
        return email
    except Exception:
        return email
```

### Step 2: Update create_news() to accept author_name from frontend

In `news_api/index.py` create_news():
```python
# Get author_name from request or derive from email
author_name = body.get('author_name', '')
if not author_name:
    author_name = get_user_name(user_info['email'])

news_item = {
    'news_id': news_id,
    'title': body['title'],
    ...
    'author': user_info['email'],
    'author_name': author_name,
    ...
}
```

### Step 3: Update update_news() to accept author_name

Add 'author_name' to fields list:
```python
fields = ['title', 'content', 'summary', 'category', 'tags', 'state', 'visibility', 
         'is_breaking', 'external_url', 'featured_image', 'scheduled_publish', 'status', 'author_name']
```

### Step 4: Add author field to create-news.html

After title field:
```html
<div class="row">
    <div class="col-md-12">
        <div class="mb-3">
            <label for="author" class="form-label">Author *</label>
            <input type="text" class="form-control" id="author" required placeholder="Enter author name">
        </div>
    </div>
</div>
```

In DOMContentLoaded, pre-fill with current user:
```javascript
if (userData) {
    var user = JSON.parse(userData);
    var authorName = (user.first_name && user.last_name) ? user.first_name + ' ' + user.last_name : user.email;
    document.getElementById('author').value = authorName;
}
```

In createNews(), add to newsData:
```javascript
author_name: document.getElementById('author').value,
```

### Step 5: Add author field to edit-news.html

Same as create-news.html, plus in loadNews():
```javascript
document.getElementById('author').value = news.author_name || news.author || '';
```

In updateNews(), add to newsData:
```javascript
author_name: document.getElementById('author').value,
```

**Deployment**:
```powershell
# Deploy Lambda
cd news_api
powershell -Command "Compress-Archive -Path * -DestinationPath ..\news_api.zip -Force"
cd ..
aws lambda update-function-code --function-name news-api --zip-file fileb://news_api.zip

# Push HTML files
aws s3 cp create-news.html s3://my-video-downloads-bucket/
aws s3 cp edit-news.html s3://my-video-downloads-bucket/

# Backfill existing records
python update_news_author_names.py
```

**Why This is Permanent**:
1. Author field is now editable in UI - admins can fix it anytime
2. Field auto-fills with current user's name on create
3. Lambda accepts author_name directly from frontend
4. No dependency on automatic email-to-name conversion
5. Migration script available for bulk fixes

**Verification**:
1. Create new news article - author field should show your name
2. Edit existing news - author field should be editable
3. Change author name and save - should persist
4. Check news.html - should display author names not emails

---

## Quick Reference Commands

```powershell
# Fix scripture lookup
.\deploy-articles-api-with-deps.ps1

# Fix article author names
python update_article_author_names.py

# Fix news author names
python update_news_author_names.py

# Fix duplicate candidates
cd "Election Chunks/COMPLETE_STATE_TEMPLATES/Pennsylvania"
python clean_slate_upload.py

# Fix candidates in "Other Candidates"
python fix_candidate_race_ids.py

# Fix summary counts
python check_summary.py  # Check text pattern first!
python update_summary_counts.py

# Check if token validator is loaded (in browser console)
typeof checkTokenExpiration
# Should return "function"
```

## Prevention

To prevent these issues from recurring:

1. **Scripture Lookup**: Always deploy articles-api with `deploy-articles-api-with-deps.ps1` (not the basic deploy script)

2. **JWT Expiration**: Token validator is now in `assets/js/token-validator.js` and should be included in all protected pages

3. **Author Names**: 
   - Always use get_user_name() when creating articles/news
   - Store both author_name and author_email fields
   - Run migration scripts after any bulk data imports

## Files Modified/Created

- `deploy-articles-api-with-deps.ps1` - Deployment with dependencies
- `assets/js/token-validator.js` - JWT expiration checker
- `update_article_author_names.py` - Article migration script
- `update_news_author_names.py` - News migration script (already exists)
