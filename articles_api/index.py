import json
import boto3
from datetime import datetime
import uuid
import re
from decimal import Decimal
import base64

dynamodb = boto3.resource('dynamodb')
articles_table = dynamodb.Table('articles')
users_table = dynamodb.Table('users')

# Bible API configuration (using free Bible API)
BIBLE_API_BASE = 'https://bible-api.com'

def lambda_handler(event, context):
    # Always add CORS headers
    headers = cors_headers()
    
    try:
        method = event.get('httpMethod', 'GET')
        
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
        elif method == 'GET' and action == 'search':
            return search_articles(event)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Endpoint not found'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def create_article_test(event):
    """Minimal test version of create article"""
    headers = cors_headers()
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps({
            'message': 'Test article creation - CORS working',
            'article_id': 'test-123'
        })
    }

def create_article(event):
    """Create a new article"""
    headers = cors_headers()
    
    try:
        body = json.loads(event['body'])
        
        article_id = str(uuid.uuid4())
        title = body['title']
        content = body['content']
        author_input = body['author']
        category = body.get('category', 'general')
        template_used = body.get('template_used', 'custom')
        tags = body.get('tags', [])
        visibility = body.get('visibility', 'public')
        featured_image = body.get('featured_image', '')
        
        # Handle author field - if it contains @, it's an email, otherwise it's a name
        if '@' in author_input:
            # It's an email, look up the display name
            author_email = author_input
            author_name = get_user_name(author_email)
        else:
            # It's already a display name, use it directly
            author_name = author_input
            author_email = author_input  # Store the name as email for now
        
        # Auto-set study notes to private
        if category == 'study_notes':
            visibility = 'private'
        
        # Extract scripture references from content
        scripture_references = extract_scripture_references(content)
        
        # Calculate reading time (average 200 words per minute)
        word_count = len(content.split())
        reading_time = max(1, round(word_count / 200))
        
        article = {
            'article_id': article_id,
            'title': title,
            'content': content,
            'author': author_name,
            'author_email': author_email,
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
            'headers': headers,
            'body': json.dumps({
                'message': 'Article created successfully',
                'article_id': article_id,
                'scripture_references': scripture_references
            })
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Failed to create article: ' + str(e)})
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
        # Import requests here to handle missing module gracefully
        try:
            import requests
        except ImportError:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': 'Bible verse lookup not available - requests module missing'})
            }
        
        # Format reference for API (e.g., "john3:16")
        # Remove spaces and convert to lowercase
        formatted_ref = reference.lower().replace(' ', '')
        
        # bible-api.com supports KJV, ASV (1901), and YLT (NT only)
        supported_translations = ['kjv', 'asv', 'ylt']
        
        if translation.lower() in supported_translations:
            # Use the requested translation - all need explicit translation parameter
            url = BIBLE_API_BASE + '/' + formatted_ref + '?translation=' + translation.lower()
        else:
            # Fallback to KJV for unsupported translations
            url = BIBLE_API_BASE + '/' + formatted_ref + '?translation=kjv'
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Clean the text to remove line breaks and extra whitespace
            verse_text = data.get('text', '').replace('\n', ' ').replace('\r', ' ').strip()
            # Remove multiple spaces and normalize
            verse_text = ' '.join(verse_text.split())
            
            # Determine actual translation returned
            actual_translation = data.get('translation_name', translation.upper())
            translation_note = ''
            
            # Add fallback note for unsupported translations
            if translation.lower() not in supported_translations:
                translation_note = f' (Note: {translation.upper()} not available, showing KJV)'
                actual_translation = 'KJV'
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'reference': data.get('reference', reference),
                    'text': verse_text,
                    'translation': actual_translation + translation_note
                })
            }
        else:
            # If the specific translation failed, try KJV as fallback
            if translation.lower() != 'kjv':
                fallback_url = BIBLE_API_BASE + '/' + formatted_ref + '?translation=kjv'
                fallback_response = requests.get(fallback_url, timeout=10)
                
                if fallback_response.status_code == 200:
                    data = fallback_response.json()
                    verse_text = data.get('text', '').replace('\n', ' ').replace('\r', ' ').strip()
                    verse_text = ' '.join(verse_text.split())
                    
                    return {
                        'statusCode': 200,
                        'headers': headers,
                        'body': json.dumps({
                            'reference': data.get('reference', reference),
                            'text': verse_text,
                            'translation': f'KJV (Note: {translation.upper()} not found for this verse, showing KJV)'
                        })
                    }
            
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Verse not found. Please check the reference format (e.g., "John 3:16")'})
            }
            
    except ImportError:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': 'Bible verse lookup not available'})
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
        },
        'service_notes': {
            'name': 'Service Notes Template',
            'description': 'Notes and observations from church services',
            'content': '''<h2>📅 Service Information</h2>
<p><strong>Date:</strong> [Insert date]</p>
<p><strong>Speaker:</strong> [Pastor/Speaker name]</p>
<p><strong>Topic:</strong> [Service topic/theme]</p>

<h2>📖 Scripture Focus</h2>
<p>[Main scripture passages covered]</p>

<h2>💡 Key Points</h2>
<ul>
<li>Point 1: [Your notes]</li>
<li>Point 2: [Your notes]</li>
<li>Point 3: [Your notes]</li>
</ul>

<h2>🎯 Personal Application</h2>
<p>How does this apply to my life?</p>

<h2>🙏 Prayer Requests</h2>
<p>[Any prayer requests mentioned or personal prayers]</p>

<h2>📝 Additional Notes</h2>
<p>[Other observations, quotes, or thoughts]</p>'''
        },
        'bible_study': {
            'name': 'Bible Study & Devotional Notes',
            'description': 'Personal Bible study and devotional reflections',
            'content': '''<h2>📖 Scripture Passage</h2>
<p><em>Insert the Bible passage you are studying...</em></p>

<h2>🔍 Observation</h2>
<p>What do I notice about this passage? Key words, themes, context...</p>

<h2>💭 Interpretation</h2>
<p>What does this passage mean? What was the author trying to communicate?</p>

<h2>❤️ Personal Reflection</h2>
<p>How does this speak to my heart? What is God showing me?</p>

<h2>🎯 Application</h2>
<p>How will I apply this truth to my life today?</p>

<h2>🙏 Prayer Response</h2>
<p>Lord, thank You for this truth. Help me to...</p>

<h2>📝 Additional Thoughts</h2>
<p>Cross-references, questions for further study, insights...</p>'''
        }
    }
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({'templates': templates})
    }

def search_articles(event):
    """Search articles by title, content, category, tags, or author"""
    query_params = event.get('queryStringParameters') or {}
    search_query = query_params.get('q', '').strip().lower()
    category = query_params.get('category')
    author = query_params.get('author')
    visibility = query_params.get('visibility', 'public')
    
    try:
        # Scan articles table
        scan_kwargs = {}
        
        # Base filter for visibility
        if visibility == 'public':
            scan_kwargs['FilterExpression'] = 'visibility = :vis'
            scan_kwargs['ExpressionAttributeValues'] = {':vis': 'public'}
        
        response = articles_table.scan(**scan_kwargs)
        articles = response.get('Items', [])
        
        # Fix author names for existing articles that have email addresses
        for article in articles:
            author_field = article.get('author', '')
            if '@' in author_field:
                proper_name = get_user_name(author_field)
                article['author'] = proper_name
        
        # Apply search filters
        filtered_articles = []
        
        for article in articles:
            match = True
            
            # Text search in title and content
            if search_query:
                title_match = search_query in article.get('title', '').lower()
                content_match = search_query in article.get('content', '').lower()
                author_match = search_query in article.get('author', '').lower()
                tag_match = any(search_query in tag.lower() for tag in article.get('tags', []))
                
                if not (title_match or content_match or author_match or tag_match):
                    match = False
            
            # Category filter
            if category and article.get('category', '') != category:
                match = False
            
            # Author filter
            if author and author.lower() not in article.get('author', '').lower():
                match = False
            
            if match:
                filtered_articles.append(article)
        
        # Sort by relevance (title matches first, then by date)
        if search_query:
            def relevance_score(article):
                score = 0
                title = article.get('title', '').lower()
                content = article.get('content', '').lower()
                
                # Title matches get highest score
                if search_query in title:
                    score += 10
                    if title.startswith(search_query):
                        score += 5
                
                # Content matches get medium score
                if search_query in content:
                    score += 3
                
                # Author matches get low score
                if search_query in article.get('author', '').lower():
                    score += 1
                
                return score
            
            filtered_articles.sort(key=lambda x: (relevance_score(x), x.get('created_at', '')), reverse=True)
        else:
            # Sort by date if no search query
            filtered_articles.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'articles': convert_decimals(filtered_articles),
                'count': len(filtered_articles),
                'search_query': search_query,
                'filters': {
                    'category': category,
                    'author': author,
                    'visibility': visibility
                }
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
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
        
        # Fix author names for existing articles that have email addresses
        for article in articles:
            author_field = article.get('author', '')
            if '@' in author_field:
                # This is an email, look up the proper name
                proper_name = get_user_name(author_field)
                article['author'] = proper_name
        
        # Sort by created_at descending
        articles.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'articles': convert_decimals(articles),
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
            'body': json.dumps({'article': convert_decimals(article)})
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
        
        if 'author_email' in body:
            # Get new author's name
            new_author_name = get_user_name(body['author_email'])
            update_expression += ', author = :author, author_email = :author_email'
            expression_values[':author'] = new_author_name
            expression_values[':author_email'] = body['author_email']
        
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
    """Delete an article with role-based permissions"""
    headers = cors_headers()
    query_params = event.get('queryStringParameters') or {}
    article_id = query_params.get('article_id')
    
    if not article_id:
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({'error': 'article_id required'})
        }
    
    try:
        # Get user info from token
        user_info = extract_user_from_token(event)
        if not user_info:
            return {
                'statusCode': 401,
                'headers': headers,
                'body': json.dumps({'error': 'Authentication required'})
            }
        
        # Get the article to check ownership
        response = articles_table.get_item(Key={'article_id': article_id})
        article = response.get('Item')
        
        if not article:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Article not found'})
            }
        
        user_email = user_info['email']
        user_role = user_info['role']
        article_author_email = article.get('author_email', '')
        
        # Check permissions: super_user and admin can delete any article, users can only delete their own
        if user_role in ['super_user', 'admin']:
            # Super users and admins can delete any article
            pass
        elif user_email == article_author_email:
            # Users can delete their own articles
            pass
        else:
            return {
                'statusCode': 403,
                'headers': headers,
                'body': json.dumps({'error': 'You can only delete your own articles'})
            }
        
        # Delete the article
        articles_table.delete_item(Key={'article_id': article_id})
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Article deleted successfully'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def extract_scripture_references(content):
    """Extract Bible verse references from content"""
    pattern = r'\b(?:\d\s)?[A-Za-z]+\s\d+:\d+(?:-\d+)?\b'
    references = re.findall(pattern, content)
    return list(set(references))

def convert_decimals(obj):
    """Convert Decimal objects to int/float for JSON serialization"""
    if isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_decimals(value) for key, value in obj.items()}
    elif isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    return obj

def extract_user_from_token(event):
    """Extract user information from JWT token"""
    try:
        auth_header = event.get('headers', {}).get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Decode payload
        payload_data = parts[1]
        payload_data += '=' * (4 - len(payload_data) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_data))
        
        return {
            'user_id': payload.get('user_id'),
            'email': payload.get('email'),
            'role': payload.get('role')
        }
    except Exception:
        return None

def get_user_name(email):
    """Get user's display name from users table"""
    try:
        # Query using email index since email is not the primary key
        response = users_table.query(
            IndexName='email-index',
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        
        users = response.get('Items', [])
        if users:
            user = users[0]  # Get first matching user
            first_name = user.get('first_name', '')
            last_name = user.get('last_name', '')
            
            if first_name and last_name:
                return f"{first_name} {last_name}"
            elif first_name:
                return first_name
            elif last_name:
                return last_name
        
        # Fallback to email if no name found
        return email
    except Exception:
        # Fallback to email on any error
        return email

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
    }