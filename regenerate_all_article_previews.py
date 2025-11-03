import boto3
import re

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
articles_table = dynamodb.Table('articles')

# Get all articles
response = articles_table.scan()
articles = response['Items']

print(f"Found {len(articles)} articles. Regenerating previews...\n")

for article in articles:
    article_id = article.get('article_id')
    title = article.get('title', '')
    content = article.get('content', '')
    featured_image = article.get('featured_image', '')
    
    # Extract plain text
    plain_text = re.sub('<[^<]+?>', '', content)
    excerpt = plain_text[:160]
    
    # Skip base64, use logo
    if featured_image and not featured_image.startswith('data:'):
        image_url = featured_image
    else:
        image_url = 'https://d271vky579caz9.cloudfront.net/techcrosslogo.jpg'
    
    preview_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Christian Conservatives Today">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:url" content="https://christianconservativestoday.com/previews/article-{article_id}.html">
<meta property="og:image" content="{image_url}">
<meta property="og:image:secure_url" content="{image_url}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{excerpt}">
<meta name="twitter:image" content="{image_url}">
<meta http-equiv="refresh" content="0;url=/article.html?id={article_id}">
<title>{title} - Christian Conservatives Today</title>
</head>
<body>
<script>window.location.href="/article.html?id={article_id}";</script>
<p>Redirecting to article...</p>
</body>
</html>'''
    
    # Upload to S3
    s3.put_object(
        Bucket='my-video-downloads-bucket',
        Key=f'previews/article-{article_id}.html',
        Body=preview_html.encode('utf-8'),
        ContentType='text/html',
        CacheControl='no-cache'
    )
    
    print(f"Regenerated preview for: {title[:50]}")

print(f"\nDone! Regenerated {len(articles)} article previews")
print("All previews now use HTTPS image URLs")
