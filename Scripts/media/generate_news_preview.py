import boto3
import sys

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
news_table = dynamodb.Table('news-table')

if len(sys.argv) < 2:
    print("Usage: python generate_news_preview.py <news_id>")
    sys.exit(1)

news_id = sys.argv[1]

# Get news article
response = news_table.get_item(Key={'news_id': news_id})
if 'Item' not in response:
    print(f"News article {news_id} not found")
    sys.exit(1)

news = response['Item']
title = news.get('title', '')
content = news.get('content', '')
featured_image = news.get('featured_image', '')

# Extract plain text from HTML
import re
plain_text = re.sub('<[^<]+?>', '', content)
excerpt = plain_text[:160]

# Use featured image if available, otherwise use logo
if featured_image:
    image_url = featured_image
else:
    image_url = 'https://d3oo5w3ywcz1uh.cloudfront.net/techcrosslogo.jpg'

preview_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta property="og:type" content="article">
<meta property="og:site_name" content="Christian Conservatives Today">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{excerpt}">
<meta property="og:url" content="https://christianconservativestoday.com/previews/news-{news_id}.html">
<meta property="og:image" content="{image_url}">
<meta property="og:image:secure_url" content="{image_url}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{excerpt}">
<meta name="twitter:image" content="{image_url}">
<meta http-equiv="refresh" content="0;url=/news-article.html?id={news_id}">
<title>{title} - Christian Conservatives Today</title>
</head>
<body>
<script>window.location.href="/news-article.html?id={news_id}";</script>
<p>Redirecting to article...</p>
</body>
</html>'''

# Upload to S3
s3.put_object(
    Bucket='my-video-downloads-bucket',
    Key=f'previews/news-{news_id}.html',
    Body=preview_html.encode('utf-8'),
    ContentType='text/html',
    CacheControl='no-cache'
)

print(f"Preview created: https://christianconservativestoday.com/previews/news-{news_id}.html")
print(f"Share this URL on Facebook")
