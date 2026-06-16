import boto3
import json
import jwt
import os
import stripe
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('StorageUsers')

JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-in-production')
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_your_key')

TIER_CONFIG = {
    'free': {'quota': 1073741824, 'price': 0, 'name': 'Free', 'priceId': None},
    'basic': {'quota': 10737418240, 'price': 5, 'name': 'Basic', 'priceId': 'price_basic'},
    'pro': {'quota': 107374182400, 'price': 15, 'name': 'Pro', 'priceId': 'price_pro'},
    'business': {'quota': 1099511627776, 'price': 50, 'name': 'Business', 'priceId': 'price_business'}
}

def lambda_handler(event, context):
    # Handle OPTIONS for CORS preflight
    if event.get('httpMethod') == 'OPTIONS' or event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return response(200, {})
    
    try:
        # Try different header case variations
        headers = event.get('headers', {})
        token = headers.get('Authorization') or headers.get('authorization', '')
        token = token.replace('Bearer ', '').replace('bearer ', '')
        
        if not token:
            return response(401, {'error': 'No token provided'})
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            email = payload['email']
        except:
            return response(401, {'error': 'Invalid token'})
        
        # Get action from query params or body
        params = event.get('queryStringParameters') or {}
        action = params.get('action')
        
        if not action:
            body = json.loads(event.get('body', '{}'))
            action = body.get('action')
        else:
            body = {}
        
        if action == 'create_checkout':
            return create_checkout_session(email, body)
        elif action == 'webhook':
            return handle_webhook(event)
        elif action == 'cancel':
            return cancel_subscription(email)
        elif action == 'get_status':
            return get_subscription_status(email)
        else:
            return response(400, {'error': 'Invalid action'})
    except Exception as e:
        return response(500, {'error': str(e)})

def create_checkout_session(email, body):
    tier = body.get('tier')
    
    if tier not in TIER_CONFIG or tier == 'free':
        return response(400, {'error': 'Invalid tier'})
    
    user = users_table.get_item(Key={'email': email})['Item']
    
    # Create or retrieve Stripe customer
    if not user.get('stripeCustomerId'):
        customer = stripe.Customer.create(email=email, name=user['name'])
        customer_id = customer.id
        users_table.update_item(
            Key={'email': email},
            UpdateExpression='SET stripeCustomerId = :cid',
            ExpressionAttributeValues={':cid': customer_id}
        )
    else:
        customer_id = user['stripeCustomerId']
    
    # Create checkout session
    session = stripe.checkout.Session.create(
        customer=customer_id,
        payment_method_types=['card'],
        line_items=[{
            'price': TIER_CONFIG[tier]['priceId'],
            'quantity': 1
        }],
        mode='subscription',
        success_url=body.get('successUrl', 'https://yourdomain.com/success'),
        cancel_url=body.get('cancelUrl', 'https://yourdomain.com/cancel'),
        metadata={'tier': tier, 'email': email}
    )
    
    return response(200, {'sessionId': session.id, 'url': session.url})

def handle_webhook(event):
    # Stripe webhook handler for subscription events
    payload = event['body']
    sig_header = event['headers'].get('Stripe-Signature')
    
    try:
        event_obj = stripe.Webhook.construct_event(
            payload, sig_header, os.environ.get('STRIPE_WEBHOOK_SECRET')
        )
    except:
        return response(400, {'error': 'Invalid signature'})
    
    if event_obj['type'] == 'checkout.session.completed':
        session = event_obj['data']['object']
        email = session['metadata']['email']
        tier = session['metadata']['tier']
        subscription_id = session['subscription']
        
        users_table.update_item(
            Key={'email': email},
            UpdateExpression='SET subscriptionTier = :tier, storageQuota = :quota, stripeSubscriptionId = :sid, subscriptionStatus = :status',
            ExpressionAttributeValues={
                ':tier': tier,
                ':quota': Decimal(str(TIER_CONFIG[tier]['quota'])),
                ':sid': subscription_id,
                ':status': 'active'
            }
        )
    
    elif event_obj['type'] == 'customer.subscription.deleted':
        subscription = event_obj['data']['object']
        subscription_id = subscription['id']
        
        # Find user by subscription ID
        result = dynamodb.meta.client.scan(
            TableName='StorageUsers',
            FilterExpression='stripeSubscriptionId = :sid',
            ExpressionAttributeValues={':sid': {'S': subscription_id}}
        )
        
        if result['Items']:
            email = result['Items'][0]['email']['S']
            users_table.update_item(
                Key={'email': email},
                UpdateExpression='SET subscriptionTier = :tier, storageQuota = :quota, subscriptionStatus = :status',
                ExpressionAttributeValues={
                    ':tier': 'free',
                    ':quota': Decimal(str(TIER_CONFIG['free']['quota'])),
                    ':status': 'cancelled'
                }
            )
    
    return response(200, {'received': True})

def cancel_subscription(email):
    user = users_table.get_item(Key={'email': email})['Item']
    
    if not user.get('stripeSubscriptionId'):
        return response(400, {'error': 'No active subscription'})
    
    try:
        stripe.Subscription.delete(user['stripeSubscriptionId'])
        
        users_table.update_item(
            Key={'email': email},
            UpdateExpression='SET subscriptionTier = :tier, storageQuota = :quota, subscriptionStatus = :status',
            ExpressionAttributeValues={
                ':tier': 'free',
                ':quota': Decimal(str(TIER_CONFIG['free']['quota'])),
                ':status': 'cancelled'
            }
        )
        
        return response(200, {'message': 'Subscription cancelled successfully'})
    except Exception as e:
        return response(500, {'error': str(e)})

def get_subscription_status(email):
    user = users_table.get_item(Key={'email': email})['Item']
    
    return response(200, {
        'tier': user['subscriptionTier'],
        'status': user.get('subscriptionStatus', 'active'),
        'storageQuota': int(user['storageQuota']),
        'storageUsed': int(user['storageUsed']),
        'storagePercent': round((int(user['storageUsed']) / int(user['storageQuota'])) * 100, 2)
    })

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization,Stripe-Signature',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }
