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
2. Lambda missing invoke permissions from API Gateway
3. Lambda execution role lacks DynamoDB permissions
4. CORS headers in Lambda not sufficient without API Gateway methods

**Complete Fix Checklist**:

### Step 1: Add GET method to API Gateway
```powershell
# Get API and resource IDs first
aws apigatewayv2 get-apis
aws apigatewayv2 get-routes --api-id <api-id>

# Add GET method
aws apigatewayv2 create-route --api-id <api-id> --route-key "GET /prayer" --target "integrations/<integration-id>"
```

### Step 2: Grant Lambda invoke permission from API Gateway
```powershell
# CRITICAL: Lambda needs permission for API Gateway to invoke it
aws lambda add-permission `
  --function-name prayer_api `
  --statement-id apigateway-get-invoke `
  --action lambda:InvokeFunction `
  --principal apigateway.amazonaws.com `
  --source-arn "arn:aws:execute-api:us-east-1:<account-id>:<api-id>/*/*/prayer"
```

### Step 3: Add DynamoDB permissions to Lambda role
```powershell
# Find Lambda role name
aws lambda get-function --function-name prayer_api --query 'Configuration.Role'

# Attach DynamoDB policy
aws iam attach-role-policy --role-name <lambda-role-name> --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess
```

### Step 4: Verify Lambda CORS headers
Ensure Lambda function has proper CORS headers in ALL responses:
```python
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
}

# Handle OPTIONS preflight
if event.get('httpMethod') == 'OPTIONS':
    return {'statusCode': 200, 'headers': headers, 'body': ''}
```

### Step 5: Deploy API Gateway changes
```powershell
# For API Gateway v2 (HTTP API)
aws apigatewayv2 create-deployment --api-id <api-id> --stage-name prod

# For API Gateway v1 (REST API)
aws apigateway create-deployment --rest-api-id <api-id> --stage-name prod
```

**Verification**:
1. Test GET request in browser console:
```javascript
fetch('https://<api-id>.execute-api.us-east-1.amazonaws.com/prod/prayer?action=list')
  .then(r => r.json())
  .then(console.log)
```
2. Should return 200 with proper CORS headers
3. No 403 errors
4. Check CloudWatch logs for any errors

**Common Mistakes**:
- ❌ Only adding POST method, forgetting GET
- ❌ Forgetting Lambda invoke permission (causes 403 even with CORS headers)
- ❌ Not deploying API Gateway after changes
- ❌ Lambda role missing DynamoDB permissions
- ❌ CORS headers only in some responses, not all

**Key Points**:
- Lambda CORS headers alone aren't enough - API Gateway needs proper methods configured
- GET requests need separate method configuration from POST
- Lambda needs explicit invoke permission from API Gateway (most common cause of 403)
- Lambda role needs explicit DynamoDB permissions
- Always deploy API Gateway after configuration changes
- Test both GET and POST methods separately

**Real Example (Prayer API)**:
```powershell
# 1. Added GET route
aws apigatewayv2 create-route --api-id cayl9dmtaf --route-key "GET /prayer" --target "integrations/kcmhqxd"

# 2. Added invoke permission (THIS WAS THE KEY FIX)
aws lambda add-permission `
  --function-name prayer_api `
  --statement-id apigateway-get-invoke `
  --action lambda:InvokeFunction `
  --principal apigateway.amazonaws.com `
  --source-arn "arn:aws:execute-api:us-east-1:371751795928:cayl9dmtaf/*/*/prayer"

# 3. Added DynamoDB permissions
aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

# 4. Deployed API
aws apigatewayv2 create-deployment --api-id cayl9dmtaf --stage-name prod
```

---

## Issue 14: DynamoDB Reserved Keyword Error on Update

**Symptom**: Lambda UpdateItem operation fails with error: "Attribute name is a reserved keyword; reserved keyword: location" (or status, state, name, etc.)

**Root Cause**: DynamoDB has reserved keywords that cannot be used directly in UpdateExpression without ExpressionAttributeNames

**Common Reserved Keywords**: location, status, state, name, timestamp, date, year, month, day, comment, data, value, key, type, order, group, user, role, path, size, format, version, connection

**Fix**: Use ExpressionAttributeNames to map placeholder names to actual field names

### Before (Causes Error):
```python
def update_event(event, headers):
    body = json.loads(event['body'])
    event_id = body['event_id']
    
    update_expr = 'SET '
    expr_values = {}
    updates = []
    
    fields = ['title', 'location', 'status']  # location and status are reserved
    
    for field in fields:
        if field in body:
            updates.append(f'{field} = :{field}')  # ❌ Direct use of reserved keyword
            expr_values[f':{field}'] = body[field]
    
    update_expr += ', '.join(updates)
    
    events_table.update_item(
        Key={'event_id': event_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values  # ❌ Missing ExpressionAttributeNames
    )
```

### After (Fixed):
```python
def update_event(event, headers):
    body = json.loads(event['body'])
    event_id = body['event_id']
    
    update_expr = 'SET '
    expr_values = {}
    expr_names = {}  # ✅ Add expression attribute names
    updates = []
    
    fields = ['title', 'location', 'status']
    
    for field in fields:
        if field in body:
            updates.append(f'#{field} = :{field}')  # ✅ Use placeholder with #
            expr_values[f':{field}'] = body[field]
            expr_names[f'#{field}'] = field  # ✅ Map placeholder to actual field
    
    update_expr += ', '.join(updates)
    
    events_table.update_item(
        Key={'event_id': event_id},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_names,  # ✅ Include attribute names
        ExpressionAttributeValues=expr_values
    )
```

**Key Changes**:
1. Add `expr_names = {}` dictionary
2. Use `#{field}` instead of `{field}` in UpdateExpression
3. Map each field: `expr_names[f'#{field}'] = field`
4. Include `ExpressionAttributeNames=expr_names` in update_item()

**Best Practice**: Always use ExpressionAttributeNames for ALL fields in UpdateExpression, not just reserved keywords. This prevents future issues if DynamoDB adds new reserved keywords.

**Deployment**:
```powershell
# Package and deploy Lambda
cd events_api
powershell -Command "Compress-Archive -Path index.py,requirements.txt -DestinationPath ../events_api.zip -Force"
cd ..
aws lambda update-function-code --function-name events_api --zip-file fileb://events_api.zip
```

**Verification**:
1. Try updating an item with reserved keyword field (e.g., location, status)
2. Should succeed without ValidationException
3. Check CloudWatch logs for successful update

**Real Example (Events API)**:
Fixed events_api update_event() function to use ExpressionAttributeNames for all fields including 'location' and 'status' reserved keywords.

---

## Issue 15: Quill Editor Stripping Email Template Styling

**Symptom**: Professional email templates with inline CSS lose all styling when loaded into Quill rich text editor

**Root Cause**: Quill.js sanitizes and strips inline styles, complex HTML structures, and email-specific CSS for security. This is by design - Quill is meant for simple rich text, not preserving complex HTML like email templates.

**Why This Happens**:
- Quill removes inline styles (style="color: red;")
- Quill strips div containers and complex layouts
- Quill converts HTML to its own Delta format, losing original structure
- Email templates need inline CSS (external stylesheets don't work in emails)
- Quill's clipboard.dangerouslyPasteHTML() still sanitizes content

**Failed Attempts**:
1. ❌ Using quill.root.innerHTML = template - Quill immediately sanitizes on next render
2. ❌ Using quill.clipboard.dangerouslyPasteHTML() - Still strips styles
3. ❌ Using quill.clipboard.convert() with setContents() - Converts to Delta, loses HTML
4. ❌ Delaying with setTimeout() - Quill sanitizes regardless of timing
5. ❌ Using 'silent' parameter - Only prevents events, doesn't prevent sanitization

**Solution**: Replace Quill with contenteditable div + formatting toolbar

### Implementation:

**Step 1: Remove Quill initialization**
```javascript
// OLD - Remove this
quill = new Quill('#editor', {
    theme: 'snow',
    modules: { toolbar: [...] }
});

// NEW - Use contenteditable
$('#editor').attr('contenteditable', 'true').css('background', 'white');
```

**Step 2: Add formatting toolbar**
```html
<div class="p-2 border-bottom bg-light">
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="formatDoc('bold')"><b>B</b></button>
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="formatDoc('italic')"><i>I</i></button>
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="formatDoc('underline')"><u>U</u></button>
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="formatDoc('insertUnorderedList')">• List</button>
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="formatDoc('insertOrderedList')">1. List</button>
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="formatDoc('justifyLeft')">Left</button>
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="formatDoc('justifyCenter')">Center</button>
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="formatDoc('justifyRight')">Right</button>
    <select class="form-select form-select-sm d-inline-block" style="width: auto;" onchange="formatDoc('fontSize', this.value); this.value=''">
        <option value="">Font Size</option>
        <option value="1">Small</option>
        <option value="3">Normal</option>
        <option value="5">Large</option>
        <option value="7">Huge</option>
    </select>
    <input type="color" class="form-control form-control-sm d-inline-block" style="width: 50px;" onchange="formatDoc('foreColor', this.value)" title="Text Color">
    <button type="button" class="btn btn-sm btn-outline-secondary" onclick="insertLink()">🔗 Link</button>
</div>
<div id="editor" style="min-height: 300px; padding: 15px; overflow-y: auto;"></div>
```

**Step 3: Add formatting functions**
```javascript
function formatDoc(cmd, value = null) {
    document.execCommand(cmd, false, value);
    $('#editor').focus();
}

function insertLink() {
    const url = prompt('Enter URL:');
    if (url) {
        document.execCommand('createLink', false, url);
    }
}
```

**Step 4: Add dual-tab editor (Visual + HTML)**
```html
<ul class="nav nav-tabs" role="tablist">
    <li class="nav-item"><a class="nav-link active" data-bs-toggle="tab" href="#visualEditor">Visual Editor</a></li>
    <li class="nav-item"><a class="nav-link" data-bs-toggle="tab" href="#htmlEditor">HTML Editor</a></li>
</ul>
<div class="tab-content border border-top-0">
    <div id="visualEditor" class="tab-pane fade show active">
        <!-- Toolbar and contenteditable div here -->
    </div>
    <div id="htmlEditor" class="tab-pane fade">
        <textarea id="htmlContent" class="form-control" rows="15" style="font-family: monospace;"></textarea>
    </div>
</div>
```

**Step 5: Sync editors on tab switch**
```javascript
$('a[data-bs-toggle="tab"]').on('shown.bs.tab', function(e) {
    const target = $(e.target).attr('href');
    if (target === '#htmlEditor') {
        $('#htmlContent').val($('#editor').html());
    } else if (target === '#visualEditor') {
        $('#editor').html($('#htmlContent').val());
    }
});
```

**Step 6: Update save function**
```javascript
function saveNewsletter() {
    const activeTab = $('.tab-pane.active').attr('id');
    const content = activeTab === 'htmlEditor' ? $('#htmlContent').val() : $('#editor').html();
    // Use content for saving
}
```

**Benefits of This Solution**:
- ✅ Preserves ALL HTML and inline CSS
- ✅ Works with complex email templates
- ✅ Visual editing with formatting toolbar
- ✅ HTML tab for direct code editing
- ✅ Both tabs stay in sync
- ✅ No sanitization or style stripping
- ✅ Uses native browser contenteditable (same as Mailchimp, SendGrid)

**Why contenteditable Works**:
- Browser's native contenteditable doesn't sanitize like Quill
- document.execCommand() applies formatting without stripping existing styles
- Direct HTML manipulation via .html() preserves everything
- Professional email builders (Mailchimp, SendGrid) use contenteditable, not Quill

**Deployment**:
```powershell
aws s3 cp admin-newsletters.html s3://my-video-downloads-bucket/
```

**Verification**:
1. Click "Use Template" on any professional template
2. Switch to Visual Editor tab - should see styled content
3. Switch to HTML Editor tab - should see full HTML with inline styles
4. Edit in Visual tab, switch to HTML - changes preserved
5. Edit in HTML tab, switch to Visual - changes rendered
6. Save newsletter - all styling preserved in database
7. Send newsletter - recipients see full professional design

**Key Takeaway**: Quill is great for simple rich text (blog posts, comments) but NOT for email templates. Use contenteditable + document.execCommand() for email editing.

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

## Issue 16: Video Delete Returns Success But Video Still Exists

**Symptom**: Clicking delete on a video shows "Video deleted successfully" but video still appears in admin dashboard after refresh

**Root Cause**: DynamoDB video-metadata table uses `video_id` as primary key, but older videos have UUID video_ids that don't match their filenames. The delete function was trying to delete using `filename` as the key, which silently failed.

**Example**:
- Filename: `test-video.mp4`
- video_id: `57d3e0ff-0a87-44f0-8178-e559a00547d6` (UUID)
- Delete tried: `Key={'video_id': 'test-video.mp4'}` ❌
- Should be: `Key={'video_id': '57d3e0ff-0a87-44f0-8178-e559a00547d6'}` ✅

**Why It Happened**:
- Old videos created before standardization used UUIDs as video_id
- New videos use filename as video_id
- Delete function assumed video_id always equals filename
- DynamoDB delete_item() doesn't throw error if key doesn't exist - just returns success

**Fix**: Update admin_api delete_video() to scan for filename first, then delete using correct video_id

### Before (Broken):
```python
def delete_video(event):
    filename = query_params.get('filename')
    
    # Assumes video_id equals filename
    metadata_response = metadata_table.get_item(Key={'video_id': filename})
    metadata = metadata_response.get('Item', {})
    
    # Delete using filename as key (fails for old videos with UUID video_ids)
    metadata_table.delete_item(Key={'video_id': filename})
```

### After (Fixed):
```python
def delete_video(event):
    filename = query_params.get('filename')
    
    # Scan to find video by filename (handles both UUID and filename video_ids)
    scan_response = metadata_table.scan(
        FilterExpression='filename = :fn',
        ExpressionAttributeValues={':fn': filename}
    )
    
    if not scan_response.get('Items'):
        return {'statusCode': 404, 'error': 'Video not found'}
    
    metadata = scan_response['Items'][0]
    video_id = metadata['video_id']  # Get actual video_id (might be UUID)
    
    # Delete using correct video_id primary key
    metadata_table.delete_item(Key={'video_id': video_id})
```

**Deployment**:
```powershell
cd admin_api
powershell -Command "Compress-Archive -Path index.py -DestinationPath function.zip -Force"
aws lambda update-function-code --function-name admin-api --zip-file fileb://function.zip
```

**Verification**:
1. Find a video with UUID video_id: `aws dynamodb scan --table-name video-metadata --filter-expression "attribute_exists(video_id) AND video_id <> filename"`
2. Try deleting it from admin dashboard
3. Should delete successfully
4. Verify it's gone: `aws dynamodb get-item --table-name video-metadata --key "{\"video_id\": {\"S\": \"<uuid>\"}}"`
5. Should return empty response

**Manual Fix for Stuck Videos**:
```powershell
# Find the video's actual video_id
aws dynamodb scan --table-name video-metadata --filter-expression "filename = :fn" --expression-attribute-values "{\":fn\":{\"S\":\"test-video.mp4\"}}"

# Delete using correct video_id
aws dynamodb delete-item --table-name video-metadata --key "{\"video_id\": {\"S\": \"57d3e0ff-0a87-44f0-8178-e559a00547d6\"}}"
```

**Prevention**:
1. Always use scan with FilterExpression when looking up by non-primary-key fields
2. Never assume video_id equals filename
3. Test delete function with both old (UUID) and new (filename) videos
4. Add logging to show which video_id is being deleted

**Key Takeaway**: DynamoDB delete_item() with wrong key silently succeeds without deleting anything. Always verify the primary key value before deleting.

---


## Issue 17: Videos Moving/Reordering After Editing in Admin Dashboard

**Symptom**: When editing videos in the admin dashboard (especially those in the "Load More" section), videos appear to move to different positions or categories after saving.

**Root Cause**: 
- The `updateVideo()` function in admin.html was calling `TAG_API?action=add_video`
- The `add_video` action uses DynamoDB's `put_item()` which **OVERWRITES** the entire item
- This caused the `upload_date` to be reset to the current timestamp
- Since videos.html sorts by `upload_date` (newest first), edited videos jumped to the top
- This changed pagination boundaries, making videos appear in different positions

**The Fix**:
1. Changed `updateVideo()` to use `TAG_API?action=update_video` instead of `add_video`
2. Changed HTTP method to POST (API Gateway accepts POST, not PUT)
3. Updated TAG API's `update_video_tags()` function to:
   - Handle title updates
   - Use ExpressionAttributeNames for reserved keyword "owner"
   - Only update specified fields with `update_item()`
4. Now preserves original `upload_date`, `size`, and other metadata

**Files Modified**:
- `admin.html`: Changed updateVideo() to use update_video action with POST
- `tag_api/index.py`: Fixed update_video_tags() to handle reserved keywords and title updates

**Key Learning**: 
- DynamoDB reserved keywords (like "owner") must use ExpressionAttributeNames
- Always use `update_item()` for partial updates, never `put_item()`

## Issue 18: Load More Button Removed - Horizontal Scrolling Sufficient

**Symptom**: "Load More Videos" button was confusing users - they expected it to load more videos within categories, but it actually loaded more categories.

**Root Cause**:
- Pagination was designed for vertical scrolling
- With horizontal scrolling per category, pagination became redundant
- Users couldn't tell if videos were hidden or just in other categories

**The Solution**:
1. Removed "Load More" button and pagination logic from videos.html
2. Updated TAG API to return ALL videos when no page/limit parameters provided
3. All categories now load on initial page load
4. Each category uses horizontal scrolling to show all videos
5. Thumbnails use `loading="lazy"` for efficient bandwidth usage

**Benefits**:
- ✅ Simpler UX - no hidden content
- ✅ All categories visible at once
- ✅ Efficient loading - thumbnails lazy load as you scroll
- ✅ Fast initial load - only visible thumbnails download
- ✅ No confusing pagination

**Files Modified**:
- `videos.html`: Removed pagination variables, loadMoreVideos(), Load More button HTML
- `tag_api/index.py`: Modified list_all_videos() to return all videos when no pagination params

**Performance**: Page loads ALL video metadata but only downloads thumbnail images as they scroll into view (lazy loading).


---

## Issue 19: Featured Image Upload and Social Media Sharing

**Symptom**: 
1. Image uploads corrupted/failed when using multipart FormData
2. Facebook/X sharing shows no featured image or wrong image
3. X/Twitter icon displays as black and misaligned

**Root Causes**:
1. API Gateway configured multipart as binary media type, causing base64 encoding issues
2. Preview HTML files missing proper Twitter/X meta tags
3. Font Awesome X icon not rendering properly in Font Awesome 6.0.0

**Complete Solution**:

### Part 1: Fix Image Upload (admin_api/index.py)

Changed from multipart FormData to JSON with base64 encoding:

```python
def upload_image(event):
    """Handle image upload to S3 from base64 JSON data"""
    import uuid
    import re
    
    try:
        body_str = event.get('body', '{}')
        is_base64 = event.get('isBase64Encoded', False)
        
        # Try JSON format first (new format)
        try:
            body = json.loads(body_str)
            file_data_base64 = body.get('file_data')
            file_ext = body.get('file_ext', 'jpg')
            
            if file_data_base64:
                file_data = base64.b64decode(file_data_base64)
            else:
                raise ValueError("No file_data in JSON")
        except (json.JSONDecodeError, ValueError):
            # Fallback to multipart format for backward compatibility
            # ... multipart parsing code ...
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        s3_key = f'article-images/{unique_id}.{file_ext}'
        
        # Upload to S3
        s3_client.put_object(
            Bucket='my-video-downloads-bucket',
            Key=s3_key,
            Body=file_data,
            ContentType=f'image/{file_ext}'
        )
        
        # Return CloudFront URL (not S3 URL)
        cloudfront_url = f'https://d271vky579caz9.cloudfront.net/{s3_key}'
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'url': cloudfront_url})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }
```

### Part 2: Update Frontend Upload (edit-article.html, create-article.html)

```javascript
function uploadImageToS3(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        const base64Data = e.target.result.split(',')[1];
        const fileExt = file.name.split('.').pop().toLowerCase();
        
        fetch(ADMIN_API + '?action=upload_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + authToken
            },
            body: JSON.stringify({
                file_data: base64Data,
                file_ext: fileExt
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.url) {
                document.getElementById('featured-image-url').value = data.url;
                alert('Image uploaded successfully!');
            }
        });
    };
    reader.readAsDataURL(file);
}
```

### Part 3: Fix Twitter/X Meta Tags in Preview Generation

Updated both create-article.html and edit-article.html:

```javascript
function generateAndUploadPreview(articleData) {
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = articleData.content;
    const plainText = tempDiv.textContent || tempDiv.innerText || '';
    const excerpt = plainText.substring(0, 160);
    
    let imageUrl = 'https://d271vky579caz9.cloudfront.net/techcrosslogo.jpg';
    if (articleData.featured_image && !articleData.featured_image.startsWith('data:')) {
        imageUrl = articleData.featured_image;
    }
    
    const previewHtml = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Christian Conservatives Today">
<meta property="og:title" content="${escapeHtml(articleData.title)}">
<meta property="og:description" content="${escapeHtml(excerpt)}">
<meta property="og:url" content="https://christianconservativestoday.com/previews/article-${articleData.article_id}.html">
<meta property="og:image" content="${imageUrl}">
<meta property="og:image:secure_url" content="${imageUrl}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@ArizonaAloha">
<meta name="twitter:creator" content="@ArizonaAloha">
<meta name="twitter:title" content="${escapeHtml(articleData.title)}">
<meta name="twitter:description" content="${escapeHtml(excerpt)}">
<meta name="twitter:image" content="${imageUrl}">
<meta name="twitter:image:alt" content="${escapeHtml(articleData.title)}">
<title>${escapeHtml(articleData.title)} - Christian Conservatives Today</title>
<script>window.location.href="/article.html?id=${articleData.article_id}";</script>
</head>
<body>
<p>Redirecting to article...</p>
</body>
</html>`;
    
    await uploadPreviewToS3(articleData.article_id, previewHtml);
}

function uploadPreviewToS3(articleId, htmlContent) {
    return fetch(ADMIN_API + '?action=upload_url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + authToken
        },
        body: JSON.stringify({
            filename: `previews/article-${articleId}.html`,
            content_type: 'text/html'
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.upload_url) {
            return fetch(data.upload_url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'text/html',
                    'Cache-Control': 'no-cache, no-store, must-revalidate'
                },
                body: htmlContent
            }).then(() => {
                console.log('Preview uploaded successfully for article:', articleId);
            });
        }
    });
}
```

### Part 4: Fix X Icon Display

Replace Font Awesome icon with inline SVG in article.html, articles.html, news-article.html:

```html
<!-- OLD (doesn't work in FA 6.0.0) -->
<i class="fab fa-x-twitter"></i>

<!-- NEW (inline SVG) -->
<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="white" viewBox="0 0 16 16">
    <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865l8.875 11.633Z"/>
</svg>
```

Update CSS for X button:

```css
.share-btn-twitter { 
    background: #000000; 
}
.share-btn-twitter i, .share-btn-twitter svg { 
    color: white !important; 
    fill: white !important;
    line-height: 1; 
    display: inline-block; 
}
```

**Deployment**:
```powershell
# Deploy Lambda
cd admin_api
powershell -Command "Compress-Archive -Path index.py -DestinationPath function.zip -Force"
aws lambda update-function-code --function-name admin-api --zip-file fileb://function.zip

# Deploy HTML files
aws s3 cp create-article.html s3://my-video-downloads-bucket/ --content-type "text/html"
aws s3 cp edit-article.html s3://my-video-downloads-bucket/ --content-type "text/html"
aws s3 cp article.html s3://my-video-downloads-bucket/ --content-type "text/html"
aws s3 cp articles.html s3://my-video-downloads-bucket/ --content-type "text/html"
aws s3 cp news-article.html s3://my-video-downloads-bucket/ --content-type "text/html"

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id E3N00R2D2NE9C5 --paths "/*"
```

**Verification**:
1. Upload featured image in create/edit article - should return CloudFront URL
2. Create/edit article - preview HTML should auto-generate
3. Share article on Facebook - should show featured image and title
4. Share article on X/Twitter - should show featured image and title
5. X icon should display white on black background, aligned with other icons

**Key Points**:
- Use JSON with base64 encoding instead of multipart FormData
- Always return CloudFront URLs, not S3 URLs
- Include Twitter-specific meta tags (twitter:site, twitter:creator, twitter:image:alt)
- Preview generation happens automatically on create/edit
- Use inline SVG for X icon (Font Awesome 6.0.0 has rendering issues)
- Set Cache-Control headers on preview uploads
- Featured images must be HTTPS URLs, not base64 data URLs

**Why This Solution Works**:
- JSON avoids API Gateway binary media type complications
- CloudFront URLs are publicly accessible for social media crawlers
- Twitter meta tags ensure proper X/Twitter card display
- Inline SVG bypasses Font Awesome rendering issues
- Automatic preview generation ensures previews always exist and are current
- Cache-Control headers prevent stale previews

---


## Issue 20: Service Worker Chrome Extension Cache Error

**Symptom**: Console errors when using create-article.html or edit-article.html:
```
Uncaught (in promise) TypeError: Failed to execute 'put' on 'Cache': Request scheme 'chrome-extension' is unsupported
```

**Root Cause**: Service worker attempts to cache all fetch requests including chrome-extension:// URLs which cannot be cached.

**Fix**: Add URL scheme check in service-worker.js

```javascript
self.addEventListener('fetch', function(event) {
  // Skip non-http URLs (chrome-extension, etc.)
  if (!event.request.url.startsWith('http')) {
    return;
  }
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // ... rest of code
      })
  );
});
```

**Deployment**:
```powershell
aws s3 cp service-worker.js s3://my-video-downloads-bucket/
aws cloudfront create-invalidation --distribution-id E3N00R2D2NE9C5 --paths "/service-worker.js"
```

**Verification**:
1. Open create-article.html or edit-article.html
2. Check console - no cache errors
3. Service worker still caches http/https requests normally

**Key Point**: Service workers can only cache http/https URLs, not chrome-extension, file, or other schemes.

---


## Issue 21: External YouTube Videos Not Showing Thumbnails

**Symptom**: When adding external YouTube videos via admin dashboard, videos appear without thumbnails and don't play.

**Root Cause**: 
1. Missing `size: 0` field for external videos (they have no file size)
2. Thumbnail generation being called for YouTube videos unnecessarily (YouTube provides direct CDN URLs)
3. `thumbnail_url` not being properly saved to DynamoDB

**Fix**: Update `addExternalVideo()` function in admin.html (around line 3780):

```javascript
const response = await fetch(`${TAG_API}?action=add_video`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        video_id: videoId,
        filename: videoId,
        title: title,
        tags: tags,
        owner: currentUser.email,
        visibility: visibility,
        external_url: url,
        video_type: videoType,
        thumbnail_url: thumbnailUrl,
        size: 0  // External videos have no size - CRITICAL
    })
});

const data = await response.json();

if (response.ok) {
    // For YouTube videos, thumbnail URL is already set
    // For other platforms, attempt thumbnail generation
    if (videoType !== 'youtube' && thumbnailUrl === '') {
        try {
            await fetch(`${ADMIN_API}?action=generate_thumbnail`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${authToken}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: videoId,
                    video_type: videoType,
                    external_url: url
                })
            });
        } catch (error) {
            console.log('Thumbnail generation failed (non-critical):', error);
        }
    }
```

**Key Changes**:
1. Added `size: 0` to video metadata (external videos have no file size)
2. Conditional thumbnail generation - only for non-YouTube videos
3. YouTube thumbnails use direct CDN URL: `https://img.youtube.com/vi/{VIDEO_ID}/maxresdefault.jpg`

**Deployment**:
```powershell
aws s3 cp admin.html s3://my-video-downloads-bucket/ --content-type "text/html"
```

**Verification**:
1. Go to admin dashboard → Videos tab
2. Click "Add External Video"
3. Enter YouTube URL and title
4. Video should appear with thumbnail immediately
5. Clicking video should play in modal

**Prevention**: This issue occurs when the `addExternalVideo()` function is modified without preserving the `size: 0` field and conditional thumbnail generation logic.

---
