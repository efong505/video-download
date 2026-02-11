
# CI/CD Pipeline Test - This comment will trigger deployment
import json
import boto3
import os
import uuid
import time
from datetime import datetime
from decimal import Decimal
from enum import Enum

sns_client = boto3.client('sns')
dynamodb = boto3.resource('dynamodb')
jobs_table = dynamodb.Table('download-jobs')
SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:371751795928:video-download-notifications'

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

# Initialize circuit breakers
dynamodb_breaker = CircuitBreaker(failure_threshold=5, timeout=30, expected_exception=Exception)
lambda_breaker = CircuitBreaker(failure_threshold=3, timeout=60, expected_exception=Exception)

# Rate Limiter Implementation
class RateLimiter:
    def __init__(self, dynamodb_resource):
        self.table = dynamodb_resource.Table('rate-limits')
        self.limits = {
            'free': {'requests': 100, 'window': 3600},
            'paid': {'requests': 1000, 'window': 3600},
            'admin': {'requests': 10000, 'window': 3600},
            'anonymous': {'requests': 20, 'window': 3600}
        }
    
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
            import base64
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

# Initialize rate limiter
try:
    rate_limiter = RateLimiter(dynamodb)
except Exception as e:
    print(f"Rate limiter init failed: {e}")
    rate_limiter = None

def lambda_handler(event, context):
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
                        'headers': {
                            'Access-Control-Allow-Origin': '*',
                            'X-RateLimit-Limit': str(rate_limiter.limits[tier]['requests']),
                            'X-RateLimit-Remaining': '0',
                            'X-RateLimit-Reset': str(rate_check['reset_at']),
                            'Retry-After': str(rate_check['retry_after'])
                        },
                        'body': json.dumps({'error': f"Rate limit exceeded. Retry in {rate_check['retry_after']}s"})
                    }
            except Exception as e:
                print(f"Rate limit check error: {e}")
        
        # Handle CORS preflight
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
                    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
                },
                'body': ''
            }
        
        # Handle status requests (GET)
        if event.get('httpMethod') == 'GET':
            query_params = event.get('queryStringParameters') or {}
            if query_params.get('action') == 'status':
                return get_job_status()
        
        
        # Parse request body (POST)
        body = json.loads(event.get('body', '{}'))
        url = body.get('url')
        owner_email = body.get('owner', 'system')
        user_role = body.get('role', '')
        
        if not url:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing url parameter'})
            }
        
        # Check storage quota for non-system users (skip for admins and super_users)
        if owner_email != 'system' and user_role not in ['admin', 'super_user']:
            quota_check = check_storage_quota(owner_email)
            if not quota_check['allowed']:
                # Convert Decimal values in usage dict
                usage = {k: (int(v) if isinstance(v, Decimal) and v % 1 == 0 else float(v) if isinstance(v, Decimal) else v) 
                        for k, v in quota_check.get('usage', {}).items()}
                return {
                    'statusCode': 403,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({
                        'error': 'Storage quota exceeded',
                        'message': quota_check['message'],
                        'current_usage': usage
                    })
                }
        
        # Create job entry
        job_id = str(uuid.uuid4())
        output_name = body.get('output_name', 'video.mp4')
        
        try:
            dynamodb_breaker.call(
                jobs_table.put_item,
                Item={
                    'job_id': job_id,
                    'url': url,
                    'filename': output_name,
                    'title': body.get('title', ''),
                    'tags': body.get('tags', []),
                    'status': 'pending',
                    'started_at': datetime.now().isoformat(),
                    'progress': 0
                }
            )
        except CircuitBreakerOpenError as e:
            return {
                'statusCode': 503,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': str(e)})
            }
        except Exception as e:
            print(f"Failed to create job entry: {e}")
        
        # Send initiation notification
        try:
            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="🚀 Video Download Started",
                Message=f"A new video download has been initiated.\n\n"
                       f"Job ID: {job_id}\n"
                       f"URL: {url}\n"
                       f"Output: {output_name}\n"
                       f"Title: {body.get('title', 'Not specified')}\n"
                       f"Tags: {', '.join(body.get('tags', [])) or 'None'}\n"
                       f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}"
            )
        except Exception as e:
            print(f"Failed to send initiation notification: {e}")
        
        # Convert any Decimal values to int/float for JSON serialization
        def decimal_default(obj):
            if isinstance(obj, Decimal):
                return int(obj) if obj % 1 == 0 else float(obj)
            raise TypeError
        
        # Invoke the downloader Lambda with circuit breaker
        lambda_client = boto3.client('lambda')
        try:
            lambda_breaker.call(
                lambda_client.invoke,
                FunctionName='video-downloader',
                InvocationType='Event',
                Payload=json.dumps({
                    'job_id': job_id,
                    'url': url,
                    'format': 'best',
                    'output_name': output_name,
                    'title': body.get('title', ''),
                    'tags': body.get('tags', []),
                    'owner': body.get('owner', 'system'),
                    'visibility': body.get('visibility', 'public')
                }, default=decimal_default)
            )
        except CircuitBreakerOpenError as e:
            return {
                'statusCode': 503,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': str(e)})
            }
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': 'Download started',
                'job_id': job_id
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def check_storage_quota(owner_email):
    """Check if user has available storage quota"""
    try:
        users_table = dynamodb.Table('users')
        
        # Get user by email with circuit breaker
        response = dynamodb_breaker.call(
            users_table.query,
            IndexName='email-index',
            KeyConditionExpression='email = :email',
            ExpressionAttributeValues={':email': owner_email}
        )
        
        if not response['Items']:
            return {'allowed': False, 'message': 'User not found', 'usage': {}}
        
        user = response['Items'][0]
        storage_used = user.get('storage_used', 0)
        storage_limit = user.get('storage_limit', 1073741824)  # 1GB default for free tier
        video_count = user.get('video_count', 0)
        video_limit = user.get('video_limit', 25)  # 25 videos default for free tier
        
        # Check video count limit
        if video_limit > 0 and video_count >= video_limit:
            return {
                'allowed': False,
                'message': f'Video limit reached ({video_count}/{video_limit}). Upgrade your plan to upload more videos.',
                'usage': {
                    'storage_used': storage_used,
                    'storage_limit': storage_limit,
                    'video_count': video_count,
                    'video_limit': video_limit
                }
            }
        
        # Check storage limit (allow some buffer for video processing)
        storage_buffer = 0.9  # Use 90% of limit as threshold
        if storage_limit > 0 and storage_used >= (storage_limit * storage_buffer):
            return {
                'allowed': False,
                'message': f'Storage limit nearly reached ({storage_used / (1024**3):.1f}GB / {storage_limit / (1024**3):.1f}GB). Upgrade your plan for more storage.',
                'usage': {
                    'storage_used': storage_used,
                    'storage_limit': storage_limit,
                    'video_count': video_count,
                    'video_limit': video_limit
                }
            }
        
        return {
            'allowed': True,
            'message': 'Quota available',
            'usage': {
                'storage_used': storage_used,
                'storage_limit': storage_limit,
                'video_count': video_count,
                'video_limit': video_limit
            }
        }
        
    except Exception as e:
        print(f"Error checking quota: {e}")
        return {'allowed': True, 'message': 'Quota check failed, allowing download', 'usage': {}}

def get_job_status():
    try:
        # Get all jobs with circuit breaker
        response = dynamodb_breaker.call(jobs_table.scan)
        jobs = response.get('Items', [])
        
        # Filter jobs from last 24 hours in Python
        from datetime import timedelta
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        recent_jobs_filtered = []
        for job in jobs:
            try:
                job_time = datetime.fromisoformat(job.get('started_at', ''))
                if job_time > cutoff_time:
                    recent_jobs_filtered.append(job)
            except:
                # Include jobs with invalid timestamps
                recent_jobs_filtered.append(job)
        
        # Separate active and completed jobs
        active_jobs = [job for job in recent_jobs_filtered if job.get('status') in ['pending', 'processing', 'downloading']]
        recent_jobs = [job for job in recent_jobs_filtered if job.get('status') in ['completed', 'failed']]
        
        # Sort by started_at (most recent first)
        active_jobs.sort(key=lambda x: x.get('started_at', ''), reverse=True)
        recent_jobs.sort(key=lambda x: x.get('started_at', ''), reverse=True)
        
        # Convert Decimal objects to int/float for JSON serialization
        def convert_decimals(obj):
            if isinstance(obj, list):
                return [convert_decimals(item) for item in obj]
            elif isinstance(obj, dict):
                return {key: convert_decimals(value) for key, value in obj.items()}
            elif isinstance(obj, Decimal):
                return int(obj) if obj % 1 == 0 else float(obj)
            return obj
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'active': convert_decimals(active_jobs[:10]),
                'recent': convert_decimals(recent_jobs[:20])
            })
        }
    except CircuitBreakerOpenError as e:
        return {
            'statusCode': 503,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e), 'active': [], 'recent': []})
        }
    except Exception as e:
        print(f"Error getting job status: {e}")
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'active': [], 'recent': []})
        }