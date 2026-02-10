# Social Media Preview & Author Name Fixes

## Issues Fixed

### 1. Social Media Preview Not Showing Featured Image/Title
**Problem**: When sharing articles/news on social media, the featured image and title were not displaying properly.

**Root Cause**: The `generateAndUploadPreview()` function was using base64 data URLs for the `og:image` meta tag. Social media crawlers (Facebook, Twitter, LinkedIn) cannot access base64 data URLs - they require publicly accessible HTTPS URLs.

**Solution**: Changed the image URL to use the CloudFront CDN URL instead:
```javascript
// OLD (doesn't work for social media):
var imageUrl = featuredImage || 'https://christianconservativestoday.com/techcrosslogo.jpg';

// NEW (works for social media):
var imageUrl = 'https://d3oo5w3ywcz1uh.cloudfront.net/techcrosslogo.jpg';
```

**Files Modified**:
- `create-article.html` - Line 1031
- `edit-article.html` - Line 653
- `create-news.html` - Added preview generation function
- `edit-news.html` - Added preview generation function

### 2. Author Showing Email Instead of Name
**Problem**: Articles and news were displaying author email addresses (e.g., "super@admin.com") instead of display names (e.g., "Edward Fong").

**Root Cause**: The `get_user_name()` function in `articles_api/index.py` was trying to use a DynamoDB index called `email-index` that doesn't exist on the users table, causing it to fail and fall back to the email address.

**Solution**: Changed the `get_user_name()` function to use `scan()` with a FilterExpression instead of `query()` with an index:
```python
# OLD (requires email-index):
response = users_table.query(
    IndexName='email-index',
    KeyConditionExpression='email = :email',
    ExpressionAttributeValues={':email': email}
)

# NEW (works without index):
response = users_table.scan(
    FilterExpression='email = :email',
    ExpressionAttributeValues={':email': email}
)
```

**Files Modified**:
- `articles_api/index.py` - Line 1009-1027

## Deployment Steps

### 1. Deploy Lambda Function Fix
```powershell
cd articles_api
Compress-Archive -Path index.py -DestinationPath articles-api.zip -Force
aws lambda update-function-code --function-name articles-api --zip-file fileb://articles-api.zip --region us-east-1
```

### 2. Upload HTML Files to S3
```powershell
.\s3-push.ps1
```

Or manually:
```powershell
aws s3 cp create-article.html s3://techcross-videos/
aws s3 cp edit-article.html s3://techcross-videos/
aws s3 cp create-news.html s3://techcross-videos/
aws s3 cp edit-news.html s3://techcross-videos/
```

### 3. Clear CloudFront Cache (Optional)
```bash
aws cloudfront create-invalidation --distribution-id E3N00R2D2NE9C5 --paths "/create-article.html" "/edit-article.html" "/create-news.html" "/edit-news.html"
```

## Testing

### Test Social Media Preview
1. Create or edit an article/news
2. Get the preview URL: `https://christianconservativestoday.com/previews/article-{id}.html`
3. Test with Facebook Sharing Debugger: https://developers.facebook.com/tools/debug/
4. Test with Twitter Card Validator: https://cards-dev.twitter.com/validator
5. Test with LinkedIn Post Inspector: https://www.linkedin.com/post-inspector/

### Test Author Name Display
1. Create a new article
2. Check that the author shows as "Edward Fong" (or your name) instead of "super@admin.com"
3. View the article on the public articles page
4. Verify the author name displays correctly

## How Preview Generation Works

### For Articles
1. User creates/edits article in `create-article.html` or `edit-article.html`
2. Article is saved to DynamoDB via `articles_api` Lambda
3. `generateAndUploadPreview()` function creates static HTML file with:
   - Open Graph meta tags (og:title, og:description, og:image, etc.)
   - Twitter Card meta tags
   - Instant redirect to actual article page
4. Preview HTML uploaded to S3 at `/previews/article-{id}.html`
5. When shared on social media, crawlers read the preview page and extract meta tags
6. Users are instantly redirected to the real article page

### For News
Same process but:
- Preview saved to `/previews/news-{id}.html`
- Redirects to `/news-article.html?id={id}`

## Important Notes

### Why CloudFront URL Instead of Data URL?
- **Data URLs** (base64 encoded images) are embedded directly in HTML
- Social media crawlers **cannot access** data URLs
- They need **publicly accessible HTTPS URLs**
- CloudFront CDN provides fast, reliable image delivery

### Why Not Use Featured Image?
Currently, the featured image is stored as a base64 data URL in DynamoDB. To use it for social media:
1. Would need to upload featured image to S3 first
2. Get the S3/CloudFront URL
3. Store that URL in DynamoDB
4. Use that URL in the preview

For now, using the default logo ensures social media previews always work.

### Future Enhancement
To support custom featured images in social media previews:
1. Modify image upload to save to S3 instead of base64
2. Store S3/CloudFront URL in DynamoDB
3. Update `generateAndUploadPreview()` to use that URL

## Verification

After deployment, verify:
- ✅ New articles show author name (not email)
- ✅ Existing articles show author name (Lambda fixes on-the-fly)
- ✅ Social media preview shows title and logo
- ✅ Preview pages redirect instantly to article
- ✅ News articles also generate previews

## Related Documentation
- `STATIC_PREVIEW_PAGES_SOLUTION.md` - Original implementation guide
- `SOCIAL_MEDIA_SHARING_SOLUTION.md` - All solutions evaluated
- `FIX_RECURRING_ISSUES_GUIDE.md` - Author name fix guide
