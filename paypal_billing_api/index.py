import json
import boto3
import requests
import base64
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('users')

# PayPal Configuration (use environment variables in production)
PAYPAL_CLIENT_ID = 'your-paypal-client-id'  # Set in Lambda environment
PAYPAL_CLIENT_SECRET = 'your-paypal-client-secret'  # Set in Lambda environment
PAYPAL_BASE_URL = 'https://api-m.sandbox.paypal.com'  # Use https://api-m.paypal.com for production

# Subscription tier configurations
SUBSCRIPTION_TIERS = {
    'free': {
        'storage_limit': 2147483648,  # 2GB
        'video_limit': 50,
        'price': 0
    },
    'premium': {
        'storage_limit': 26843545600,  # 25GB
        'video_limit': 500,
        'price': 9.99
    },
    'pro': {
        'storage_limit': 107374182400,  # 100GB
        'video_limit': 2000,
        'price': 24.99
    },
    'enterprise': {
        'storage_limit': -1,  # Unlimited
        'video_limit': -1,  # Unlimited
        'price': 99.99
    }
}

def lambda_handler(event, context):
    try:
        method = event.get('httpMethod', 'POST')
        
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': ''
            }
        
        query_params = event.get('queryStringParameters') or {}
        action = query_params.get('action')
        
        if method == 'POST' and action == 'create_subscription':
            return create_subscription(event)
        elif method == 'POST' and action == 'webhook':
            return handle_webhook(event)
        elif method == 'GET' and action == 'subscription_status':
            return get_subscription_status(event)
        elif method == 'POST' and action == 'cancel_subscription':
            return cancel_subscription(event)
        elif method == 'GET' and action == 'usage':
            return get_usage_stats(event)
        else:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Endpoint not found'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def get_paypal_access_token():
    """Get PayPal access token for API calls"""
    auth_string = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    
    headers = {
        'Authorization': f'Basic {auth_b64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    data = 'grant_type=client_credentials'
    
    response = requests.post(f'{PAYPAL_BASE_URL}/v1/oauth2/token', headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f'Failed to get PayPal access token: {response.text}')

def create_subscription(event):
    """Create PayPal subscription for user"""
    body = json.loads(event['body'])
    user_id = body['user_id']
    tier = body['tier']
    
    if tier not in SUBSCRIPTION_TIERS:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Invalid subscription tier'})
        }
    
    if tier == 'free':
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'Cannot create subscription for free tier'})
        }
    
    try:
        access_token = get_paypal_access_token()
        
        # Create subscription plan if not exists (in production, create these once)
        plan_id = f'video-downloader-{tier}'
        
        # Create subscription
        subscription_data = {
            'plan_id': plan_id,
            'subscriber': {
                'email_address': body.get('email', ''),
                'name': {
                    'given_name': body.get('first_name', 'User'),
                    'surname': body.get('last_name', 'Name')
                }
            },
            'application_context': {
                'brand_name': 'Video Downloader',
                'user_action': 'SUBSCRIBE_NOW',
                'return_url': body.get('return_url', 'https://d271vky579caz9.cloudfront.net/profile.html'),
                'cancel_url': body.get('cancel_url', 'https://d271vky579caz9.cloudfront.net/profile.html')
            }
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(
            f'{PAYPAL_BASE_URL}/v1/billing/subscriptions',
            headers=headers,
            json=subscription_data
        )
        
        if response.status_code == 201:
            subscription = response.json()
            
            # Update user with subscription info
            users_table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET subscription_tier = :tier, subscription_id = :sub_id, payment_provider = :provider, subscription_status = :status, updated_at = :updated',
                ExpressionAttributeValues={
                    ':tier': tier,
                    ':sub_id': subscription['id'],
                    ':provider': 'paypal',
                    ':status': 'pending',
                    ':updated': datetime.utcnow().isoformat()
                }
            )
            
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({
                    'subscription_id': subscription['id'],
                    'approval_url': next(link['href'] for link in subscription['links'] if link['rel'] == 'approve')
                })
            }
        else:
            return {
                'statusCode': 400,
                'headers': cors_headers(),
                'body': json.dumps({'error': f'PayPal error: {response.text}'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def handle_webhook(event):
    """Handle PayPal webhook events"""
    body = json.loads(event['body'])
    event_type = body.get('event_type')
    
    if event_type == 'BILLING.SUBSCRIPTION.ACTIVATED':
        subscription_id = body['resource']['id']
        
        # Find user by subscription ID and activate
        response = users_table.scan(
            FilterExpression='subscription_id = :sub_id',
            ExpressionAttributeValues={':sub_id': subscription_id}
        )
        
        if response['Items']:
            user = response['Items'][0]
            tier = user['subscription_tier']
            tier_config = SUBSCRIPTION_TIERS[tier]
            
            users_table.update_item(
                Key={'user_id': user['user_id']},
                UpdateExpression='SET subscription_status = :status, storage_limit = :storage, video_limit = :videos, next_billing_date = :billing, updated_at = :updated',
                ExpressionAttributeValues={
                    ':status': 'active',
                    ':storage': tier_config['storage_limit'],
                    ':videos': tier_config['video_limit'],
                    ':billing': (datetime.utcnow() + timedelta(days=30)).isoformat(),
                    ':updated': datetime.utcnow().isoformat()
                }
            )
    
    elif event_type == 'BILLING.SUBSCRIPTION.CANCELLED':
        subscription_id = body['resource']['id']
        
        # Downgrade user to free tier
        response = users_table.scan(
            FilterExpression='subscription_id = :sub_id',
            ExpressionAttributeValues={':sub_id': subscription_id}
        )
        
        if response['Items']:
            user = response['Items'][0]
            free_config = SUBSCRIPTION_TIERS['free']
            
            users_table.update_item(
                Key={'user_id': user['user_id']},
                UpdateExpression='SET subscription_tier = :tier, subscription_status = :status, storage_limit = :storage, video_limit = :videos, subscription_id = :sub_id, updated_at = :updated',
                ExpressionAttributeValues={
                    ':tier': 'free',
                    ':status': 'cancelled',
                    ':storage': free_config['storage_limit'],
                    ':videos': free_config['video_limit'],
                    ':sub_id': None,
                    ':updated': datetime.utcnow().isoformat()
                }
            )
    
    return {
        'statusCode': 200,
        'headers': cors_headers(),
        'body': json.dumps({'status': 'processed'})
    }

def get_subscription_status(event):
    """Get user's subscription status and usage"""
    query_params = event.get('queryStringParameters') or {}
    user_id = query_params.get('user_id')
    
    if not user_id:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'user_id required'})
        }
    
    try:
        response = users_table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'User not found'})
            }
        
        user = response['Item']
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'subscription_tier': user.get('subscription_tier', 'free'),
                'storage_used': user.get('storage_used', 0),
                'storage_limit': user.get('storage_limit', 2147483648),
                'video_count': user.get('video_count', 0),
                'video_limit': user.get('video_limit', 50),
                'subscription_status': user.get('subscription_status', 'active'),
                'next_billing_date': user.get('next_billing_date'),
                'payment_provider': user.get('payment_provider')
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def get_usage_stats(event):
    """Calculate and return current usage statistics"""
    query_params = event.get('queryStringParameters') or {}
    user_id = query_params.get('user_id')
    
    if not user_id:
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': 'user_id required'})
        }
    
    try:
        # Get user info
        user_response = users_table.get_item(Key={'user_id': user_id})
        if 'Item' not in user_response:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'User not found'})
            }
        
        user = user_response['Item']
        
        # Calculate actual usage from video metadata
        video_table = dynamodb.Table('video-metadata')
        videos_response = video_table.scan(
            FilterExpression='owner = :owner',
            ExpressionAttributeValues={':owner': user['email']}
        )
        
        total_size = 0
        video_count = 0
        
        for video in videos_response['Items']:
            if video.get('video_type', 'local') == 'local':
                # Get actual file size from S3
                try:
                    import boto3
                    s3_client = boto3.client('s3')
                    s3_response = s3_client.head_object(
                        Bucket='my-video-downloads-bucket',
                        Key=f"videos/{video.get('filename', '')}"
                    )
                    total_size += s3_response['ContentLength']
                    video_count += 1
                except:
                    pass
            else:
                video_count += 1
        
        # Update user's actual usage
        users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression='SET storage_used = :storage, video_count = :count, updated_at = :updated',
            ExpressionAttributeValues={
                ':storage': total_size,
                ':count': video_count,
                ':updated': datetime.utcnow().isoformat()
            }
        )
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'storage_used': total_size,
                'storage_limit': user.get('storage_limit', 2147483648),
                'video_count': video_count,
                'video_limit': user.get('video_limit', 50),
                'storage_percentage': (total_size / user.get('storage_limit', 2147483648)) * 100 if user.get('storage_limit', 2147483648) > 0 else 0,
                'video_percentage': (video_count / user.get('video_limit', 50)) * 100 if user.get('video_limit', 50) > 0 else 0
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def cancel_subscription(event):
    """Cancel user's PayPal subscription"""
    body = json.loads(event['body'])
    user_id = body['user_id']
    
    try:
        # Get user's subscription info
        response = users_table.get_item(Key={'user_id': user_id})
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'User not found'})
            }
        
        user = response['Item']
        subscription_id = user.get('subscription_id')
        
        if not subscription_id:
            return {
                'statusCode': 400,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'No active subscription found'})
            }
        
        # Cancel subscription with PayPal
        access_token = get_paypal_access_token()
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        cancel_data = {
            'reason': 'User requested cancellation'
        }
        
        response = requests.post(
            f'{PAYPAL_BASE_URL}/v1/billing/subscriptions/{subscription_id}/cancel',
            headers=headers,
            json=cancel_data
        )
        
        if response.status_code == 204:
            # Update user to free tier
            free_config = SUBSCRIPTION_TIERS['free']
            
            users_table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET subscription_tier = :tier, subscription_status = :status, storage_limit = :storage, video_limit = :videos, subscription_id = :sub_id, updated_at = :updated',
                ExpressionAttributeValues={
                    ':tier': 'free',
                    ':status': 'cancelled',
                    ':storage': free_config['storage_limit'],
                    ':videos': free_config['video_limit'],
                    ':sub_id': None,
                    ':updated': datetime.utcnow().isoformat()
                }
            )
            
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({'message': 'Subscription cancelled successfully'})
            }
        else:
            return {
                'statusCode': 400,
                'headers': cors_headers(),
                'body': json.dumps({'error': f'PayPal cancellation failed: {response.text}'})
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
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Date, X-Api-Key, X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Max-Age': '86400'
    }