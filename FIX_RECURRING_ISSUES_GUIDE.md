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

**Symptom**: Sharing articles/news on Facebook/Twitter shows no image or title, or shows generic logo instead of featured image

**Root Cause**: 
1. Base64 data URLs in og:image tags (social crawlers can't access)
2. Missing static preview HTML files for crawlers
3. Preview generation in edit forms causes script tag syntax errors

**SOLUTION**: Use Python script to generate previews manually

### Why Manual Script Works:
1. Avoids script tag syntax errors in HTML
2. Uses article's featured_image (HTTPS URL) instead of base64 or generic logo
3. Generates clean HTML without JavaScript complications
4. Can be run anytime to regenerate previews

### Script: generate_news_preview.py

Created at root of Downloader folder. Uses article's featured_image if available, otherwise falls back to logo.

**Usage**:
```powershell
python generate_news_preview.py <news_id>
```

**Example**:
```powershell
python generate_news_preview.py 12310e90-31c1-4b33-aaa5-43911ce8504d
```

**Output**:
- Creates `/previews/news-{id}.html` in S3
- Prints shareable URL
- Use that URL for Facebook/Twitter sharing

**Verification**:
1. Run script with news_id
2. Copy the preview URL from output
3. Test in Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/
4. Should show article title, excerpt, and featured image
5. Share the preview URL (not the regular article URL) on social media

**Key Points**:
- Preview URL redirects to actual article
- Social crawlers read meta tags before redirect
- Must use preview URL for sharing, not regular article URL
- Regenerate preview anytime article is updated

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

## Issue 11: Facebook Share Image Not Displaying

**Symptom**: When sharing articles on Facebook, title and text appear but featured image is missing

**Root Causes**: 
1. Articles had base64-encoded images stored in DynamoDB (Facebook can't access data: URLs)
2. Wrong CloudFront domain in preview generation code
3. Images uploaded to S3 but not publicly accessible via correct CloudFront URL

**Solution**: Convert base64 images to S3 and use correct CloudFront domain

### Step 1: Convert base64 images to S3

```powershell
python convert_base64_to_s3.py
```

This script:
- Scans all articles for base64 featured images
- Uploads them to S3 at `article-images/{article_id}.jpg`
- Updates articles table with CloudFront HTTPS URLs

### Step 2: Fix CloudFront domain

Correct CloudFront domain for `my-video-downloads-bucket`: `d271vky579caz9.cloudfront.net`

Update in:
- `convert_base64_to_s3.py`
- `regenerate_all_article_previews.py`
- `edit-article.html`
- `create-article.html`

### Step 3: Update existing articles

```powershell
python fix_cloudfront_urls.py
```

Replaces old CloudFront domain with correct one in all articles.

### Step 4: Regenerate all previews

```powershell
python regenerate_all_article_previews.py
```

Generates preview HTML files with correct image URLs.

### Step 5: Deploy updated HTML files

```powershell
aws s3 cp edit-article.html s3://my-video-downloads-bucket/
aws s3 cp create-article.html s3://my-video-downloads-bucket/
```

**Verification**:
1. Edit an article (don't change featured image)
2. Check preview file in S3: `previews/article-{id}.html`
3. Verify og:image has correct CloudFront URL
4. Test in Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/
5. Should show article image, not logo

**Key Points**:
- Featured images must be HTTPS URLs, not base64
- CloudFront domain: `d271vky579caz9.cloudfront.net`
- Images stored at: `article-images/{article_id}.jpg`
- Preview generation automatically skips base64 and uses logo as fallback
- When editing articles, preview regenerates with current featured_image from database

---

## Issue 12: Share Buttons Using Article URL Instead of Preview URL

**Symptom**: Clicking Facebook/Twitter share buttons shares article URL instead of preview URL

**Root Cause**: Share button functions were using `window.location.href` instead of preview URL
2. Preview generation missing from create-article.html and edit-article.html
3. Base64 images in featured_image field (Facebook can't access base64 data URLs)

**Fix**: Update share functions to use preview URL

### For news-article.html:

In `setupSharing()` function:
```javascript
function setupSharing(news) {
    var previewUrl = 'https://christianconservativestoday.com/previews/news-' + currentNewsId + '.html';
    // Use previewUrl in all share buttons instead of currentUrl
}
```

In `copyLink()` function:
```javascript
function copyLink() {
    var previewUrl = 'https://christianconservativestoday.com/previews/news-' + currentNewsId + '.html';
    navigator.clipboard.writeText(previewUrl).then(function() {
        alert('Link copied to clipboard!');
    }).catch(function() {
        var textArea = document.createElement('textarea');
        textArea.value = previewUrl;
        // ... rest of fallback code
    });
}
```

In `copyLinkForInstagram()` function:
```javascript
function copyLinkForInstagram() {
    var previewUrl = 'https://christianconservativestoday.com/previews/news-' + currentNewsId + '.html';
    navigator.clipboard.writeText(previewUrl).then(function() {
        // ... rest of code
    });
}
```

### For article.html:

In `displayArticle()` function:
```javascript
const previewUrl = 'https://christianconservativestoday.com/previews/article-' + article.article_id + '.html';
// Use previewUrl in share buttons and input field
```

Update `window.currentArticle` object:
```javascript
window.currentArticle = {
    title: article.title,
    excerpt: excerpt,
    url: previewUrl,  // Changed from currentUrl
    author: article.author
};
```

**Deployment**:
```powershell
aws s3 cp news-article.html s3://my-video-downloads-bucket/news-article.html --content-type "text/html"
aws s3 cp article.html s3://my-video-downloads-bucket/article.html --content-type "text/html"
```

**Verification**:
1. Open any news article or article page
2. Click copy link button - should copy preview URL (contains `/previews/`)
3. Click Facebook share - should share preview URL
4. Test preview URL in Facebook Sharing Debugger - should show featured image
5. Preview URL should redirect to actual article after meta tags are read

**Complete Solution**:

### 1. Fix Share Buttons (article.html, news-article.html, articles.html)
Replace all share functions to use preview URLs instead of article URLs.

### 2. Add Automatic Preview Generation

**create-article.html**: Add after article creation success:
```javascript
if (data.article_id) {
    generateAndUploadPreview(data.article_id, title, content, featuredImage).then(function() {
        alert('Article published successfully!');
        window.location.href = 'articles.html';
    });
}
```

**edit-article.html**: Add after article update success:
```javascript
if (response.ok) {
    await generateAndUploadPreview(updateData);
    alert('Article updated successfully!');
    window.location.href = 'articles.html';
}
```

**create-news.html & edit-news.html**: Same pattern as articles.

### 3. Fix Base64 Image Handling

Update preview generation scripts to skip base64 images:

**generate_article_preview.py**:
```python
if featured_image and not featured_image.startswith('data:'):
    image_url = featured_image
else:
    image_url = 'https://d3oo5w3ywcz1uh.cloudfront.net/techcrosslogo.jpg'
```

**generate_news_preview.py**: Same fix.

**JavaScript preview generation**: Check `!featuredImage.startsWith('data:')` before using.

**Deployment**:
```powershell
aws s3 cp create-article.html s3://my-video-downloads-bucket/
aws s3 cp edit-article.html s3://my-video-downloads-bucket/
aws s3 cp article.html s3://my-video-downloads-bucket/
aws s3 cp news-article.html s3://my-video-downloads-bucket/
aws s3 cp articles.html s3://my-video-downloads-bucket/
```

**Why This Matters**:
- Social media crawlers need preview URLs to read proper meta tags
- Facebook/Twitter can't access base64 data URLs - need real HTTPS image URLs
- Preview URLs have article-specific images and descriptions
- Preview URLs redirect users to actual article after crawlers read meta tags
- Automatic generation ensures previews always exist and are up-to-date

---

## Issue 13: New Lambda API Returns 403 CORS Error

**Symptom**: New Lambda API returns 403 Forbidden with CORS error, even though Lambda has CORS headers

**Root Causes**:
1. API Gateway missing GET method (only POST configured)
2. Lambda execution role lacks DynamoDB permissions
3. CORS headers in Lambda not sufficient without API Gateway methods

**Fix**:

### Step 1: Add GET method to API Gateway
```powershell
aws apigateway put-method --rest-api-id <api-id> --resource-id <resource-id> --http-method GET --authorization-type NONE
```

### Step 2: Integrate GET method with Lambda
```powershell
aws apigateway put-integration --rest-api-id <api-id> --resource-id <resource-id> --http-method GET --type AWS_PROXY --integration-http-method POST --uri "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:<account-id>:function:<function-name>/invocations"
```

### Step 3: Add DynamoDB permissions to Lambda role
```powershell
aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
```

### Step 4: Deploy API Gateway changes
```powershell
aws apigateway create-deployment --rest-api-id <api-id> --stage-name prod
```

**Verification**:
1. Test GET request in browser or Postman
2. Should return 200 with proper CORS headers
3. No 403 errors

**Key Points**:
- Lambda CORS headers alone aren't enough - API Gateway needs proper methods configured
- GET requests need separate method configuration from POST
- Lambda role needs explicit DynamoDB permissions
- Always deploy API Gateway after configuration changes

---

## Quick Reference Commands

```powershell
# Fix scripture lookup
.\deploy-articles-api-with-deps.ps1

# Fix article author names
python update_article_author_names.py

# Fix news author names
python update_news_author_names.py

# Generate social media preview for news
python generate_news_preview.py <news_id>

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
