import boto3
import re

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
news_table = dynamodb.Table('news-table')
articles_table = dynamodb.Table('articles')

def generate_news_preview(news_id, news):
    title = news.get('title', '')
    content = news.get('content', '')
    featured_image = news.get('featured_image', '')
    
    plain_text = re.sub('<[^<]+?>', '', content)
    excerpt = plain_text[:160]
    
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
    
    s3.put_object(
        Bucket='my-video-downloads-bucket',
        Key=f'previews/news-{news_id}.html',
        Body=preview_html.encode('utf-8'),
        ContentType='text/html',
        CacheControl='no-cache'
    )
    print(f"News: {title[:50]}")

def generate_article_preview(article_id, article):
    title = article.get('title', '')
    content = article.get('content', '')
    featured_image = article.get('featured_image', '')
    
    plain_text = re.sub('<[^<]+?>', '', content)
    excerpt = plain_text[:160]
    
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
    
    s3.put_object(
        Bucket='my-video-downloads-bucket',
        Key=f'previews/article-{article_id}.html',
        Body=preview_html.encode('utf-8'),
        ContentType='text/html',
        CacheControl='no-cache'
    )
    print(f"Article: {title[:50]}")

# Generate all news previews
print("Generating news previews...")
response = news_table.scan()
news_items = response.get('Items', [])
for news in news_items:
    generate_news_preview(news['news_id'], news)

print(f"\n{len(news_items)} news previews created")

# Generate all article previews
print("\nGenerating article previews...")
response = articles_table.scan()
articles = response.get('Items', [])
for article in articles:
    generate_article_preview(article['article_id'], article)

print(f"\n{len(articles)} article previews created")
print("\nAll previews generated successfully!")
