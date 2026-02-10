import json
import boto3
import time
from datetime import datetime
import uuid
import re
from decimal import Decimal
import base64
from enum import Enum

dynamodb = boto3.resource('dynamodb')
articles_table = dynamodb.Table('articles')
users_table = dynamodb.Table('users')

# Bible API configuration
BIBLE_API_BASE = 'https://bible-api.com'

# Circuit Breaker Implementation
class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=30, expected_exception=Exception):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func, *args, **kwargs):
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitBreakerOpenError(f"Service unavailable. Retry in {self._time_until_retry()}s")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except self.expected_exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _should_attempt_reset(self):
        return time.time() - self.last_failure_time >= self.timeout
    
    def _time_until_retry(self):
        if not self.last_failure_time:
            return 0
        elapsed = time.time() - self.last_failure_time
        return max(0, int(self.timeout - elapsed))

class CircuitBreakerOpenError(Exception):
    pass

# Initialize circuit breaker
dynamodb_breaker = CircuitBreaker(failure_threshold=5, timeout=30, expected_exception=Exception)

# Rate Limiter Implementation
class RateLimiter:
    def __init__(self, dynamodb_resource):
        self.table = dynamodb_resource.Table('rate-limits')
        self.limits = {'free': {'requests': 100, 'window': 3600}, 'paid': {'requests': 1000, 'window': 3600}, 'admin': {'requests': 10000, 'window': 3600}, 'anonymous': {'requests': 20, 'window': 3600}}
    def check_rate_limit(self, identifier, tier='free'):
        if tier == 'admin':
            return {'allowed': True, 'remaining': 9999}
        limit_config = self.limits.get(tier, self.limits['free'])
        current_time = int(time.time())
        window_start = current_time - limit_config['window']
        key = f"{tier}:{identifier}"
        try:
            response = self.table.get_item(Key={'rate_key': key})
            item = response.get('Item', {})
            requests = [r for r in item.get('requests', []) if r > window_start]
            if len(requests) >= limit_config['requests']:
                oldest = min(requests)
                reset_time = oldest + limit_config['window']
                return {'allowed': False, 'remaining': 0, 'reset_at': reset_time, 'retry_after': reset_time - current_time}
            requests.append(current_time)
            self.table.put_item(Item={'rate_key': key, 'requests': requests, 'ttl': current_time + limit_config['window'] + 3600})
            return {'allowed': True, 'remaining': limit_config['requests'] - len(requests)}
        except Exception as e:
            print(f"Rate limit check failed: {e}")
            return {'allowed': True, 'remaining': 999}
    def get_identifier(self, event):
        user_id = self._extract_user_id(event)
        if user_id:
            return user_id
        ip = self._extract_ip(event)
        import hashlib
        return hashlib.md5(ip.encode()).hexdigest()[:16]
    def get_tier(self, event):
        user_info = self._extract_user_from_token(event)
        if not user_info:
            return 'anonymous'
        role = user_info.get('role', 'user')
        if role in ['admin', 'super_user']:
            return 'admin'
        subscription = user_info.get('subscription_status', 'free')
        return 'paid' if subscription == 'active' else 'free'
    def _extract_user_id(self, event):
        user_info = self._extract_user_from_token(event)
        return user_info.get('user_id') if user_info else None
    def _extract_ip(self, event):
        headers = event.get('headers', {})
        return (headers.get('X-Forwarded-For', '') or headers.get('x-forwarded-for', '') or event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'unknown'))
    def _extract_user_from_token(self, event):
        try:
            headers = event.get('headers', {})
            auth_header = headers.get('Authorization') or headers.get('authorization', '')
            if not auth_header or not auth_header.startswith('Bearer '):
                return None
            token = auth_header.split(' ')[1]
            parts = token.split('.')
            if len(parts) != 3:
                return None
            payload_data = parts[1]
            payload_data += '=' * (4 - len(payload_data) % 4)
            payload = json.loads(base64.urlsafe_b64decode(payload_data))
            return {'user_id': payload.get('user_id'), 'email': payload.get('email'), 'role': payload.get('role'), 'subscription_status': payload.get('subscription_status', 'free')}
        except Exception:
            return None

class RateLimitExceededError(Exception):
    pass

try:
    rate_limiter = RateLimiter(dynamodb)
except Exception as e:
    print(f"Rate limiter init failed: {e}")
    rate_limiter = None

def lambda_handler(event, context):
    headers = cors_headers()
    
    try:
        # Check rate limit
        if rate_limiter:
            try:
                identifier = rate_limiter.get_identifier(event)
                tier = rate_limiter.get_tier(event)
                rate_check = rate_limiter.check_rate_limit(identifier, tier)
                if not rate_check['allowed']:
                    return {
                        'statusCode': 429,
                        'headers': {**headers, 'X-RateLimit-Limit': str(rate_limiter.limits[tier]['requests']), 'X-RateLimit-Remaining': '0', 'X-RateLimit-Reset': str(rate_check['reset_at']), 'Retry-After': str(rate_check['retry_after'])},
                        'body': json.dumps({'error': f"Rate limit exceeded. Retry in {rate_check['retry_after']}s"})
                    }
            except Exception as e:
                print(f"Rate limit check error: {e}")
        
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
        elif method == 'GET' and action == 'analytics':
            return get_analytics(event)
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
        
        dynamodb_breaker.call(articles_table.put_item, Item=article)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Article created successfully',
                'article_id': article_id,
                'scripture_references': scripture_references
            })
        }
    except CircuitBreakerOpenError as e:
        return {
            'statusCode': 503,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
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
        
        response = dynamodb_breaker.call(articles_table.scan, **scan_kwargs)
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
    except CircuitBreakerOpenError as e:
        return {
            'statusCode': 503,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
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
        
        response = dynamodb_breaker.call(articles_table.scan, **scan_kwargs)
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
    except CircuitBreakerOpenError as e:
        return {
            'statusCode': 503,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def get_article(event):
    """Get a single article by ID - supports public access for public articles"""
    query_params = event.get('queryStringParameters') or {}
    article_id = query_params.get('article_id')
    
    if not article_id:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'article_id required'})
        }
    
    try:
        response = dynamodb_breaker.call(articles_table.get_item, Key={'article_id': article_id})
        article = response.get('Item')
        
        if not article:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Article not found'})
            }
        
        # Check if article is private and user is not authenticated
        if article.get('visibility') == 'private':
            user_info = extract_user_from_token(event)
            if not user_info:
                return {
                    'statusCode': 401,
                    'headers': cors_headers(),
                    'body': json.dumps({'error': 'Authentication required for private articles'})
                }
            
            # Check if user can access this private article (author or admin)
            user_email = user_info['email']
            user_role = user_info['role']
            article_author_email = article.get('author_email', '')
            article_author = article.get('author', '')
            
            # DEBUG LOGGING
            print(f"DEBUG: user_email={user_email}, user_role={user_role}")
            print(f"DEBUG: article_author_email={article_author_email}, article_author={article_author}")
            
            # Allow access if: admin/super_user/editor, or email matches author_email, or email matches author field
            is_admin = user_role in ['super_user', 'admin', 'editor']
            is_author = user_email == article_author_email or user_email == article_author
            
            print(f"DEBUG: is_admin={is_admin}, is_author={is_author}")
            
            if not (is_admin or is_author):
                return {
                    'statusCode': 403,
                    'headers': cors_headers(),
                    'body': json.dumps({'error': 'Access denied to private article'})
                }
        
        # Fix author name if it's an email
        author_field = article.get('author', '')
        if '@' in author_field:
            proper_name = get_user_name(author_field)
            article['author'] = proper_name
        
        # Increment view count
        dynamodb_breaker.call(
            articles_table.update_item,
            Key={'article_id': article_id},
            UpdateExpression='SET view_count = if_not_exists(view_count, :zero) + :inc',
            ExpressionAttributeValues={':inc': 1, ':zero': 0}
        )
        article['view_count'] = article.get('view_count', 0) + 1
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'article': convert_decimals(article)})
        }
    except CircuitBreakerOpenError as e:
        return {
            'statusCode': 503,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
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
        
        if 'category' in body:
            update_expression += ', category = :cat'
            expression_values[':cat'] = body['category']
        
        if 'tags' in body:
            update_expression += ', tags = :tags'
            expression_values[':tags'] = body['tags']
        
        if 'visibility' in body:
            update_expression += ', visibility = :vis'
            expression_values[':vis'] = body['visibility']
        
        if 'featured_image' in body:
            update_expression += ', featured_image = :img'
            expression_values[':img'] = body['featured_image']
        
        if 'author_email' in body:
            # Get new author's name
            new_author_name = get_user_name(body['author_email'])
            update_expression += ', author = :author, author_email = :author_email'
            expression_values[':author'] = new_author_name
            expression_values[':author_email'] = body['author_email']
        
        dynamodb_breaker.call(
            articles_table.update_item,
            Key={'article_id': article_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values
        )
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'message': 'Article updated successfully'})
        }
    except CircuitBreakerOpenError as e:
        return {
            'statusCode': 503,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
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
        response = dynamodb_breaker.call(articles_table.get_item, Key={'article_id': article_id})
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
        dynamodb_breaker.call(articles_table.delete_item, Key={'article_id': article_id})
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Article deleted successfully'})
        }
    except CircuitBreakerOpenError as e:
        return {
            'statusCode': 503,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
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
        headers = event.get('headers', {})
        # API Gateway may normalize headers to lowercase
        auth_header = headers.get('Authorization') or headers.get('authorization', '')
        
        print(f"DEBUG: auth_header={auth_header[:50] if auth_header else 'None'}...")  # Log first 50 chars
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Decode payload
        payload_data = parts[1]
        payload_data += '=' * (4 - len(payload_data) % 4)
        payload = json.loads(base64.urlsafe_b64decode(payload_data))
        
        print(f"DEBUG: Decoded token - email={payload.get('email')}, role={payload.get('role')}")
        
        return {
            'user_id': payload.get('user_id'),
            'email': payload.get('email'),
            'role': payload.get('role')
        }
    except Exception as e:
        print(f"DEBUG: Token extraction error: {str(e)}")
        return None

def get_user_name(email):
    """Get user's display name from users table"""
    try:
        # Scan users table
        response = dynamodb_breaker.call(
            users_table.scan,
            FilterExpression='email = :email',
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

def get_analytics(event):
    """Get article analytics"""
    query_params = event.get('queryStringParameters') or {}
    article_id = query_params.get('article_id')
    
    try:
        if article_id:
            # Get analytics for specific article
            response = dynamodb_breaker.call(articles_table.get_item, Key={'article_id': article_id})
            article = response.get('Item')
            
            if not article:
                return {
                    'statusCode': 404,
                    'headers': cors_headers(),
                    'body': json.dumps({'error': 'Article not found'})
                }
            
            analytics = {
                'article_id': article_id,
                'title': article.get('title'),
                'view_count': article.get('view_count', 0),
                'likes_count': article.get('likes_count', 0),
                'created_at': article.get('created_at'),
                'author': article.get('author'),
                'category': article.get('category'),
                'tags': article.get('tags', [])
            }
            
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({'analytics': convert_decimals(analytics)})
            }
        else:
            # Get overall analytics
            response = dynamodb_breaker.call(articles_table.scan)
            articles = response.get('Items', [])
            
            total_views = sum(article.get('view_count', 0) for article in articles)
            total_articles = len(articles)
            
            # Top 10 most viewed articles
            top_articles = sorted(articles, key=lambda x: x.get('view_count', 0), reverse=True)[:10]
            
            # Category breakdown
            category_stats = {}
            for article in articles:
                cat = article.get('category', 'general')
                if cat not in category_stats:
                    category_stats[cat] = {'count': 0, 'views': 0}
                category_stats[cat]['count'] += 1
                category_stats[cat]['views'] += article.get('view_count', 0)
            
            analytics = {
                'total_articles': total_articles,
                'total_views': total_views,
                'average_views': round(total_views / total_articles, 1) if total_articles > 0 else 0,
                'top_articles': [{
                    'article_id': a.get('article_id'),
                    'title': a.get('title'),
                    'view_count': a.get('view_count', 0),
                    'author': a.get('author'),
                    'category': a.get('category')
                } for a in top_articles],
                'category_stats': category_stats
            }
            
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({'analytics': convert_decimals(analytics)})
            }
    except CircuitBreakerOpenError as e:
        return {
            'statusCode': 503,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
    }