import json
import boto3
import re
from urllib.parse import parse_qs

dynamodb = boto3.resource('dynamodb')
articles_table = dynamodb.Table('Articles')
news_table = dynamodb.Table('news-table')

def lambda_handler(event, context):
    request = event['Records'][0]['cf']['request']
    uri = request['uri']
    
    headers = request.get('headers', {})
    user_agent = headers.get('user-agent', [{}])[0].get('value', '').lower()
    
    # Only process crawlers on article pages
    if not is_crawler(user_agent):
        return request
    
    if not (uri.endswith('article.html') or uri.endswith('news-article.html')):
        return request
    
    query_string = request.get('querystring', '')
    params = parse_qs(query_string)
    article_id = params.get('id', [None])[0]
    
    if not article_id:
        return request
    
    try:
        if 'news-article' in uri:
            article = get_news_article(article_id)
        else:
            article = get_article(article_id)
        
        if article:
            return generate_response(article, uri, query_string)
    except Exception as e:
        print(f"Error fetching article {article_id}: {e}")
    
    return request

def is_crawler(user_agent):
    crawlers = ['facebookexternalhit', 'twitterbot', 'linkedinbot', 'slackbot', 'whatsapp']
    return any(crawler in user_agent for crawler in crawlers)

def get_article(article_id):
    response = articles_table.get_item(Key={'article_id': article_id})
    return response.get('Item')

def get_news_article(news_id):
    response = news_table.get_item(Key={'news_id': news_id})
    return response.get('Item')

def generate_response(article, uri, query_string):
    title = article.get('title', 'Christian Conservative Article')
    content = article.get('content', '')
    featured_image = article.get('featured_image', 'https://christianconservativestoday.com/techcrosslogo.jpg')
    
    plain_text = re.sub('<[^<]+?>', '', content)
    excerpt = plain_text[:160] if plain_text else 'Read Christian conservative articles with biblical perspective.'
    
    full_url = f"https://christianconservativestoday.com{uri}?{query_string}"
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="Christian Conservatives Today">
    <meta property="og:title" content="{escape_html(title)}">
    <meta property="og:description" content="{escape_html(excerpt)}">
    <meta property="og:url" content="{full_url}">
    <meta property="og:image" content="{featured_image}">
    <meta property="og:image:secure_url" content="{featured_image}">
    <meta property="og:image:type" content="image/jpeg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape_html(title)}">
    <meta name="twitter:description" content="{escape_html(excerpt)}">
    <meta name="twitter:image" content="{featured_image}">
    <title>{escape_html(title)} - Christian Conservatives Today</title>
</head>
<body>
    <h1>{escape_html(title)}</h1>
    <p>{escape_html(excerpt)}</p>
    <p><a href="{full_url}">Read full article</a></p>
</body>
</html>'''
    
    return {
        'status': '200',
        'statusDescription': 'OK',
        'headers': {
            'content-type': [{'key': 'Content-Type', 'value': 'text/html; charset=utf-8'}],
            'cache-control': [{'key': 'Cache-Control', 'value': 'public, max-age=3600'}]
        },
        'body': html
    }

def escape_html(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')
