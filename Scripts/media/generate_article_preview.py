import boto3
import sys
import re

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
articles_table = dynamodb.Table('articles')

if len(sys.argv) < 2:
    print("Usage: python generate_article_preview.py <article_id>")
    sys.exit(1)

article_id = sys.argv[1]

# Get article
response = articles_table.get_item(Key={'article_id': article_id})
if 'Item' not in response:
    print(f"Article {article_id} not found")
    sys.exit(1)

article = response['Item']
title = article.get('title', '')
content = article.get('content', '')
featured_image = article.get('featured_image', '')

# Extract plain text from HTML
plain_text = re.sub('<[^<]+?>', '', content)
excerpt = plain_text[:160]

# Use featured image if available and not base64, otherwise use logo
if featured_image and not featured_image.startswith('data:'):
    image_url = featured_image
else:
    image_url = 'https://christianconservativestoday.com/techcrosslogo.jpg'

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

print(f"Preview created: https://christianconservativestoday.com/previews/article-{article_id}.html")
print(f"Share this URL on Facebook/Twitter")
