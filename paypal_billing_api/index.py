import json
import boto3
import requests
import base64
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('users')

# PayPal Configuration - Use environment variables for security
import os
PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID', 'your-paypal-client-id')
PAYPAL_CLIENT_SECRET = os.environ.get('PAYPAL_CLIENT_SECRET', 'your-paypal-client-secret')
PAYPAL_BASE_URL = os.environ.get('PAYPAL_BASE_URL', 'https://api-m.sandbox.paypal.com')

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
        elif method == 'GET' and action == 'test':
            return test_paypal_connection()
        elif method == 'POST' and action == 'activate_subscription':
            return activate_subscription(event)
        elif method == 'POST' and action == 'process_expired_subscriptions':
            return process_expired_subscriptions(event)
        elif method == 'POST' and action == 'reset_user_subscription':
            return reset_user_subscription(event)
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

def create_subscription_plan(tier, access_token):
    """Create PayPal subscription plan"""
    tier_config = SUBSCRIPTION_TIERS[tier]
    
    # Create product first
    product_data = {
        'name': f'Video Platform {tier.title()}',
        'description': f'{tier.title()} video hosting plan',
        'type': 'SERVICE',
        'category': 'SOFTWARE'
    }
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Create product
    product_response = requests.post(
        f'{PAYPAL_BASE_URL}/v1/catalogs/products',
        headers=headers,
        json=product_data
    )
    
    if product_response.status_code != 201:
        return None
    
    product_id = product_response.json()['id']
    
    # Create plan
    plan_data = {
        'product_id': product_id,
        'name': f'{tier.title()} Plan',
        'description': f'Monthly {tier} subscription',
        'billing_cycles': [{
            'frequency': {
                'interval_unit': 'MONTH',
                'interval_count': 1
            },
            'tenure_type': 'REGULAR',
            'sequence': 1,
            'total_cycles': 0,
            'pricing_scheme': {
                'fixed_price': {
                    'value': str(tier_config['price']),
                    'currency_code': 'USD'
                }
            }
        }],
        'payment_preferences': {
            'auto_bill_outstanding': True,
            'setup_fee_failure_action': 'CONTINUE',
            'payment_failure_threshold': 3
        }
    }
    
    plan_response = requests.post(
        f'{PAYPAL_BASE_URL}/v1/billing/plans',
        headers=headers,
        json=plan_data
    )
    
    if plan_response.status_code == 201:
        return plan_response.json()['id']
    
    return None

def create_subscription(event):
    """Create PayPal subscription for user"""
    try:
        print(f"Received event: {json.dumps(event)}")
        body = json.loads(event['body'])
        user_id = body['user_id']
        tier = body['tier']
        print(f"Creating subscription for user {user_id}, tier {tier}")
    except Exception as e:
        print(f"Error parsing request body: {str(e)}")
        return {
            'statusCode': 400,
            'headers': cors_headers(),
            'body': json.dumps({'error': f'Invalid request body: {str(e)}'})
        }
    
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
        
        # Create subscription plan dynamically
        plan_id = create_subscription_plan(tier, access_token)
        if not plan_id:
            return {
                'statusCode': 400,
                'headers': cors_headers(),
                'body': json.dumps({'error': f'Failed to create subscription plan for {tier}'})
            }
        
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
                'return_url': body.get('return_url', 'https://christianconservativestoday.com/profile.html'),
                'cancel_url': body.get('cancel_url', 'https://christianconservativestoday.com/profile.html')
            }
        }
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        print(f"Creating subscription with data: {json.dumps(subscription_data)}")
        response = requests.post(
            f'{PAYPAL_BASE_URL}/v1/billing/subscriptions',
            headers=headers,
            json=subscription_data
        )
        
        print(f"PayPal response status: {response.status_code}")
        print(f"PayPal response: {response.text}")
        
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
        
        # Convert Decimal values to int for JSON serialization
        storage_used = int(user.get('storage_used', 0)) if user.get('storage_used') else 0
        storage_limit = int(user.get('storage_limit', 2147483648)) if user.get('storage_limit') else 2147483648
        video_count = int(user.get('video_count', 0)) if user.get('video_count') else 0
        video_limit = int(user.get('video_limit', 50)) if user.get('video_limit') else 50
        
        # Check if cancelled subscription should still show premium benefits
        subscription_status = user.get('subscription_status', 'active')
        subscription_tier = user.get('subscription_tier', 'free')
        next_billing_date = user.get('next_billing_date')
        
        # If cancelled but billing date is in future, show as active with benefits
        if subscription_status == 'cancelled' and next_billing_date and subscription_tier != 'free':
            try:
                billing_date = datetime.fromisoformat(next_billing_date.replace('Z', '+00:00'))
                if billing_date > datetime.utcnow():
                    # Keep showing as active until billing period ends
                    subscription_status = 'active'
            except Exception as date_error:
                print(f'Date parsing error: {str(date_error)}')
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'subscription_tier': subscription_tier,
                'storage_used': storage_used,
                'storage_limit': storage_limit,
                'video_count': video_count,
                'video_limit': video_limit,
                'subscription_status': subscription_status,
                'next_billing_date': next_billing_date,
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
        print(f'Getting usage stats for user: {user_id}')
        # Get user info
        print('Getting user from database...')
        user_response = users_table.get_item(Key={'user_id': user_id})
        if 'Item' not in user_response:
            print('User not found in database')
            return {
                'statusCode': 404,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'User not found'})
            }
        
        user = user_response['Item']
        print(f'User found: {user.get("email")}')
        
        # Calculate actual usage from video metadata
        print('Accessing video-metadata table...')
        video_table = dynamodb.Table('video-metadata')
        print('Scanning for user videos...')
        videos_response = video_table.scan(
            FilterExpression='#owner = :owner',
            ExpressionAttributeNames={'#owner': 'owner'},
            ExpressionAttributeValues={':owner': user['email']}
        )
        print(f'Found {len(videos_response["Items"])} videos')
        
        total_size = 0
        video_count = 0
        
        for video in videos_response['Items']:
            if video.get('video_type', 'local') == 'local':
                # Get actual file size from S3
                try:
                    s3_client = boto3.client('s3')
                    filename = video.get('filename', '')
                    if filename:
                        try:
                            s3_response = s3_client.head_object(
                                Bucket='my-video-downloads-bucket',
                                Key=f"videos/{filename}"
                            )
                            total_size += s3_response['ContentLength']
                        except s3_client.exceptions.NoSuchKey:
                            # File doesn't exist in S3, use estimated size or skip
                            estimated_size = video.get('file_size', 0)
                            if estimated_size:
                                total_size += int(estimated_size)
                        except Exception as s3_error:
                            print(f'S3 error for {filename}: {str(s3_error)}')
                            # Use estimated size if available
                            estimated_size = video.get('file_size', 0)
                            if estimated_size:
                                total_size += int(estimated_size)
                    video_count += 1
                except Exception as general_error:
                    print(f'General error processing video: {str(general_error)}')
                    video_count += 1
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
        
        # Convert Decimal values to int for JSON serialization
        storage_limit = int(user.get('storage_limit', 2147483648)) if user.get('storage_limit') else 2147483648
        video_limit = int(user.get('video_limit', 50)) if user.get('video_limit') else 50
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'storage_used': total_size,
                'storage_limit': storage_limit,
                'video_count': video_count,
                'video_limit': video_limit,
                'storage_percentage': (total_size / storage_limit) * 100 if storage_limit > 0 else 0,
                'video_percentage': (video_count / video_limit) * 100 if video_limit > 0 else 0
            })
        }
        
    except Exception as e:
        print(f'Error in get_usage_stats: {str(e)}')
        import traceback
        print(f'Traceback: {traceback.format_exc()}')
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
        current_tier = user.get('subscription_tier', 'free')
        
        # If user is already on free tier, just update status
        if current_tier == 'free':
            users_table.update_item(
                Key={'user_id': user_id},
                UpdateExpression='SET subscription_status = :status, subscription_id = :sub_id, updated_at = :updated',
                ExpressionAttributeValues={
                    ':status': 'cancelled',
                    ':sub_id': None,
                    ':updated': datetime.utcnow().isoformat()
                }
            )
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({'message': 'User subscription cancelled (was already on free tier)'})
            }
        
        # Try to cancel with PayPal if subscription ID exists
        paypal_cancelled = False
        if subscription_id:
            try:
                access_token = get_paypal_access_token()
                
                headers = {
                    'Authorization': f'Bearer {access_token}',
                    'Content-Type': 'application/json'
                }
                
                cancel_data = {
                    'reason': 'User requested cancellation'
                }
                
                paypal_response = requests.post(
                    f'{PAYPAL_BASE_URL}/v1/billing/subscriptions/{subscription_id}/cancel',
                    headers=headers,
                    json=cancel_data
                )
                
                if paypal_response.status_code == 204:
                    paypal_cancelled = True
                elif paypal_response.status_code == 404:
                    # Subscription doesn't exist in PayPal (common in sandbox), proceed with local cancellation
                    print(f'PayPal subscription {subscription_id} not found, proceeding with local cancellation')
                    paypal_cancelled = True
                else:
                    # Other PayPal errors
                    error_data = paypal_response.json() if paypal_response.text else {}
                    if error_data.get('name') == 'RESOURCE_NOT_FOUND':
                        # Subscription doesn't exist, proceed with local cancellation
                        print(f'PayPal subscription {subscription_id} resource not found, proceeding with local cancellation')
                        paypal_cancelled = True
                    else:
                        return {
                            'statusCode': 400,
                            'headers': cors_headers(),
                            'body': json.dumps({'error': f'PayPal cancellation failed: {paypal_response.text}'})
                        }
            except Exception as paypal_error:
                print(f'PayPal cancellation error: {str(paypal_error)}')
                # If PayPal fails, still proceed with local cancellation
                paypal_cancelled = True
        else:
            # No subscription ID, proceed with local cancellation
            paypal_cancelled = True
        
        # Update user subscription status locally
        if paypal_cancelled:
            next_billing_date = user.get('next_billing_date')
            current_time = datetime.utcnow()
            
            # Check if billing date is in the future
            if next_billing_date:
                try:
                    billing_date = datetime.fromisoformat(next_billing_date.replace('Z', '+00:00'))
                    if billing_date > current_time:
                        # Keep current tier until billing period ends
                        users_table.update_item(
                            Key={'user_id': user_id},
                            UpdateExpression='SET subscription_status = :status, subscription_id = :sub_id, updated_at = :updated',
                            ExpressionAttributeValues={
                                ':status': 'cancelled',
                                ':sub_id': None,
                                ':updated': current_time.isoformat()
                            }
                        )
                        
                        days_remaining = (billing_date - current_time).days
                        return {
                            'statusCode': 200,
                            'headers': cors_headers(),
                            'body': json.dumps({
                                'message': f'Subscription cancelled successfully. You will retain {user.get("subscription_tier", "premium")} benefits until {billing_date.strftime("%B %d, %Y")} ({days_remaining} days remaining).'
                            })
                        }
                except Exception as date_error:
                    print(f'Date parsing error: {str(date_error)}')
            
            # If no valid billing date or date has passed, downgrade immediately
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
                    ':updated': current_time.isoformat()
                }
            )
            
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({'message': 'Subscription cancelled successfully'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def test_paypal_connection():
    """Test PayPal API connection"""
    try:
        access_token = get_paypal_access_token()
        
        # Check recent subscription status
        subscription_id = 'I-J6R67NVLMNF1'  # Most recent subscription
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'{PAYPAL_BASE_URL}/v1/billing/subscriptions/{subscription_id}',
            headers=headers
        )
        
        if response.status_code == 200:
            subscription = response.json()
            status = subscription['status']
            
            # If active, update user record
            if status == 'ACTIVE':
                users_table.update_item(
                    Key={'user_id': '051f56aa-3bc5-4328-8252-2f78e756b011'},
                    UpdateExpression='SET subscription_tier = :tier, subscription_status = :status, storage_limit = :storage, video_limit = :videos, updated_at = :updated',
                    ExpressionAttributeValues={
                        ':tier': 'premium',
                        ':status': 'active',
                        ':storage': 26843545600,  # 25GB
                        ':videos': 500,
                        ':updated': datetime.utcnow().isoformat()
                    }
                )
            
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({
                    'status': 'success',
                    'message': 'PayPal API connection successful',
                    'subscription_status': status,
                    'subscription_id': subscription_id
                })
            }
        else:
            return {
                'statusCode': 200,
                'headers': cors_headers(),
                'body': json.dumps({
                    'status': 'success',
                    'message': 'PayPal API connection successful',
                    'subscription_error': response.text
                })
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({
                'status': 'error',
                'message': f'PayPal API connection failed: {str(e)}'
            })
        }

def activate_subscription(event):
    """Activate subscription after PayPal approval"""
    try:
        query_params = event.get('queryStringParameters') or {}
        subscription_id = query_params.get('subscription_id')
        user_id = query_params.get('user_id')
        
        if not subscription_id or not user_id:
            return {
                'statusCode': 400,
                'headers': cors_headers(),
                'body': json.dumps({'error': 'Missing subscription_id or user_id'})
            }
        
        # Get subscription details from PayPal
        access_token = get_paypal_access_token()
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(
            f'{PAYPAL_BASE_URL}/v1/billing/subscriptions/{subscription_id}',
            headers=headers
        )
        
        if response.status_code == 200:
            subscription = response.json()
            status = subscription['status']
            
            if status == 'ACTIVE':
                # Get user's tier and update with active status
                user_response = users_table.get_item(Key={'user_id': user_id})
                if 'Item' in user_response:
                    user = user_response['Item']
                    tier = user.get('subscription_tier', 'free')
                    tier_config = SUBSCRIPTION_TIERS[tier]
                    
                    users_table.update_item(
                        Key={'user_id': user_id},
                        UpdateExpression='SET subscription_status = :status, storage_limit = :storage, video_limit = :videos, updated_at = :updated',
                        ExpressionAttributeValues={
                            ':status': 'active',
                            ':storage': tier_config['storage_limit'],
                            ':videos': tier_config['video_limit'],
                            ':updated': datetime.utcnow().isoformat()
                        }
                    )
                
                return {
                    'statusCode': 200,
                    'headers': cors_headers(),
                    'body': json.dumps({'status': 'activated', 'subscription_status': status})
                }
            else:
                return {
                    'statusCode': 200,
                    'headers': cors_headers(),
                    'body': json.dumps({'status': 'pending', 'subscription_status': status})
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

def reset_user_subscription(event):
    """Reset user subscription to clean free tier state"""
    try:
        body = json.loads(event['body'])
        user_id = body['user_id']
        
        # Reset user to clean free tier state
        free_config = SUBSCRIPTION_TIERS['free']
        current_time = datetime.utcnow()
        
        users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression='SET subscription_tier = :tier, subscription_status = :status, storage_limit = :storage, video_limit = :videos, subscription_id = :sub_id, payment_provider = :provider, next_billing_date = :billing, updated_at = :updated',
            ExpressionAttributeValues={
                ':tier': 'free',
                ':status': 'active',
                ':storage': free_config['storage_limit'],
                ':videos': free_config['video_limit'],
                ':sub_id': None,
                ':provider': None,
                ':billing': None,
                ':updated': current_time.isoformat()
            }
        )
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({'message': 'User subscription reset to free tier successfully'})
        }
        
    except Exception as e:
        print(f'Error resetting user subscription: {str(e)}')
        return {
            'statusCode': 500,
            'headers': cors_headers(),
            'body': json.dumps({'error': str(e)})
        }

def process_expired_subscriptions(event):
    """Process expired subscriptions and downgrade users to free tier"""
    try:
        current_time = datetime.utcnow()
        print(f'Processing expired subscriptions at {current_time.isoformat()}')
        
        # Scan for cancelled subscriptions with past billing dates
        response = users_table.scan(
            FilterExpression='subscription_status = :status AND next_billing_date < :current_time',
            ExpressionAttributeValues={
                ':status': 'cancelled',
                ':current_time': current_time.isoformat()
            }
        )
        
        processed_count = 0
        for user in response['Items']:
            if user.get('subscription_tier') != 'free':
                # Downgrade to free tier
                free_config = SUBSCRIPTION_TIERS['free']
                
                users_table.update_item(
                    Key={'user_id': user['user_id']},
                    UpdateExpression='SET subscription_tier = :tier, storage_limit = :storage, video_limit = :videos, updated_at = :updated',
                    ExpressionAttributeValues={
                        ':tier': 'free',
                        ':storage': free_config['storage_limit'],
                        ':videos': free_config['video_limit'],
                        ':updated': current_time.isoformat()
                    }
                )
                
                processed_count += 1
                print(f'Downgraded user {user["user_id"]} from {user.get("subscription_tier")} to free')
        
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': json.dumps({
                'message': f'Processed {processed_count} expired subscriptions',
                'processed_count': processed_count
            })
        }
        
    except Exception as e:
        print(f'Error processing expired subscriptions: {str(e)}')
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