"""
Rate Limiter Implementation
Zero-cost API rate limiting using DynamoDB
"""
import time
import hashlib
from datetime import datetime

class RateLimiter:
    def __init__(self, dynamodb_table):
        self.table = dynamodb_table
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
                return {
                    'allowed': False,
                    'remaining': 0,
                    'reset_at': reset_time,
                    'retry_after': reset_time - current_time
                }
            
            requests.append(current_time)
            self.table.put_item(Item={
                'rate_key': key,
                'requests': requests,
                'ttl': current_time + limit_config['window'] + 3600
            })
            
            return {'allowed': True, 'remaining': limit_config['requests'] - len(requests)}
        except Exception as e:
            print(f"Rate limit check failed: {e}")
            return {'allowed': True, 'remaining': 999}
    
    def get_identifier(self, event):
        user_id = self._extract_user_id(event)
        if user_id:
            return user_id
        ip = self._extract_ip(event)
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
        return (headers.get('X-Forwarded-For', '') or 
                headers.get('x-forwarded-for', '') or 
                event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'unknown'))
    
    def _extract_user_from_token(self, event):
        try:
            import json
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
            return {
                'user_id': payload.get('user_id'),
                'email': payload.get('email'),
                'role': payload.get('role'),
                'subscription_status': payload.get('subscription_status', 'free')
            }
        except Exception:
            return None

class RateLimitExceededError(Exception):
    pass
