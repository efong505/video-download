import json
import boto3
from datetime import datetime
import uuid
import re
import requests

dynamodb = boto3.resource('dynamodb')
articles_table = dynamodb.Table('articles')

# Bible API configuration (using free Bible API)
BIBLE_API_BASE = 'https://bible-api.com'

def lambda_handler(event, context):
    try:
        method = event.get('httpMethod', 'GET')
        
        # Always add CORS headers
        headers = cors_headers()
        
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        query_params = event.get('queryStringParameters') or {}
        action = query_params.get('action')
        
        if method == 'POST' and action == 'create':
            return create_article(event)
        elif method == 'GET' and action == 'list':
            return list_articles(event)
        elif method == 'GET' and action == 'get':
            return get_article(event)
        elif method == 'PUT' and action == 'update':
            return update_article(event)
        elif method == 'DELETE' and action == 'delete':
            return delete_article(event)
        elif method == 'GET' and action == 'bible_verse':
            return get_bible_verse(event)
        elif method == 'GET' and action == 'templates':
            return get_article_templates(event)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Endpoint not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def create_article(event):
    """Create a new article"""
    body = json.loads(event['body'])
    
    article_id = str(uuid.uuid4())
    title = body['title']
    content = body['content']
    author = body['author']
    category = body.get('category', 'general')
    template_used = body.get('template_used', 'custom')
    tags = body.get('tags', [])
    visibility = body.get('visibility', 'public')
    featured_image = body.get('featured_image', '')
    
    # Extract scripture references from content
    scripture_references = extract_scripture_references(content)
    
    # Calculate reading time (average 200 words per minute)
    word_count = len(content.split())
    reading_time = max(1, round(word_count / 200))
    
    article = {
        'article_id': article_id,
        'title': title,
        'content': content,
        'author': author,
        'category': category,
        'template_used': template_used,
        'scripture_references': scripture_references,
        'tags': tags,
        'visibility': visibility,
        'featured_image': featured_image,
        'reading_time': reading_time,
        'view_count': 0,
        'likes_count': 0,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    articles_table.put_item(Item=article)
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({
            'message': 'Article created successfully',
            'article_id': article_id,
            'scripture_references': scripture_references
        })
    }

def get_bible_verse(event):
    """Get Bible verse from API"""
    headers = cors_headers()
    
    query_params = event.get('queryStringParameters') or {}
    reference = query_params.get('reference')
    translation = query_params.get('translation', 'kjv')
    
    if not reference:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': 'reference required'})
        }
    
    try:
        # Format reference for API (e.g., "john 3:16")
        formatted_ref = reference.lower().replace(' ', '')
        url = BIBLE_API_BASE + '/' + formatted_ref + '?translation=' + translation
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Clean the text to remove line breaks and extra whitespace
            verse_text = data.get('text', '').replace('\n', ' ').replace('\r', ' ').strip()
            # Remove multiple spaces and normalize
            verse_text = ' '.join(verse_text.split())
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'reference': data.get('reference', reference),
                    'text': verse_text,
                    'translation': data.get('translation_name', translation.upper())
                })
            }
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Verse not found'})
            }
            
    except ImportError:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'requests module not available'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Bible API error: ' + str(e)})
        }

def get_article_templates(event):
    """Get available article templates"""
    templates = {
        'sermon': {
            'name': 'Sermon Template',
            'description': 'Traditional sermon structure with biblical foundation',
            'content': '''<h2>📖 Scripture Reading</h2>
<p><em>Insert your main scripture passage here...</em></p>

<h2>🙏 Opening Prayer</h2>
<p>Heavenly Father, we thank You for Your Word...</p>

<h2>💡 Main Points</h2>
<h3>1. First Point</h3>
<p>Your first main point with supporting scripture...</p>

<h3>2. Second Point</h3>
<p>Your second main point with supporting scripture...</p>

<h2>🎯 Application</h2>
<p>How does this apply to our daily lives?</p>

<h2>🙏 Closing Prayer</h2>
<p>Lord, help us to apply these truths...</p>'''
        },
        'political': {
            'name': 'Christian Political Commentary',
            'description': 'Biblical perspective on political and social issues',
            'content': '''<h2>📖 Biblical Foundation</h2>
<p>What does Scripture say about this issue?</p>

<h2>🏛️ Current Issue</h2>
<p>Analysis of the current political/social situation...</p>

<h2>✝️ Christian Response</h2>
<p>How should Christians respond biblically?</p>

<h2>📢 Call to Action</h2>
<p>Practical steps for Christian engagement...</p>

<h2>🙏 Prayer for Leaders</h2>
<p>Let us pray for our leaders and nation...</p>'''
        }
    }
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({'templates': templates})
    }

def list_articles(event):
    """List articles with optional filtering"""
    query_params = event.get('queryStringParameters') or {}
    visibility = query_params.get('visibility', 'public')
    category = query_params.get('category')
    author = query_params.get('author')
    
    try:
        # Scan articles table
        scan_kwargs = {}
        
        if visibility == 'public':
            scan_kwargs['FilterExpression'] = 'visibility = :vis'
            scan_kwargs['ExpressionAttributeValues'] = {':vis': 'public'}
        
        response = articles_table.scan(**scan_kwargs)
        articles = response.get('Items', [])
        
        # Sort by created_at descending
        articles.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'articles': articles,
                'count': len(articles)
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def get_article(event):
    """Get a single article by ID"""
    query_params = event.get('queryStringParameters') or {}
    article_id = query_params.get('article_id')
    
    if not article_id:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'article_id required'})
        }
    
    try:
        response = articles_table.get_item(Key={'article_id': article_id})
        article = response.get('Item')
        
        if not article:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Article not found'})
            }
        
        # Increment view count
        articles_table.update_item(
            Key={'article_id': article_id},
            UpdateExpression='SET view_count = view_count + :inc',
            ExpressionAttributeValues={':inc': 1}
        )
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'article': article})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def update_article(event):
    """Update an existing article"""
    body = json.loads(event['body'])
    article_id = body.get('article_id')
    
    if not article_id:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'article_id required'})
        }
    
    try:
        # Update article
        update_expression = 'SET updated_at = :updated'
        expression_values = {':updated': datetime.utcnow().isoformat()}
        
        if 'title' in body:
            update_expression += ', title = :title'
            expression_values[':title'] = body['title']
        
        if 'content' in body:
            update_expression += ', content = :content'
            expression_values[':content'] = body['content']
            # Re-extract scripture references
            scripture_refs = extract_scripture_references(body['content'])
            update_expression += ', scripture_references = :refs'
            expression_values[':refs'] = scripture_refs
        
        if 'visibility' in body:
            update_expression += ', visibility = :vis'
            expression_values[':vis'] = body['visibility']
        
        articles_table.update_item(
            Key={'article_id': article_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values
        )
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'message': 'Article updated successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def delete_article(event):
    """Delete an article"""
    query_params = event.get('queryStringParameters') or {}
    article_id = query_params.get('article_id')
    
    if not article_id:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'article_id required'})
        }
    
    try:
        articles_table.delete_item(Key={'article_id': article_id})
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'message': 'Article deleted successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def extract_scripture_references(content):
    """Extract Bible verse references from content"""
    pattern = r'\b(?:\d\s)?[A-Za-z]+\s\d+:\d+(?:-\d+)?\b'
    references = re.findall(pattern, content)
    return list(set(references))

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Max-Age': '86400'
    }