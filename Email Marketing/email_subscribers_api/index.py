import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')
table = dynamodb.Table('EmailSubscribers')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        action = body.get('action')
        
        if action == 'subscribe':
            return subscribe(body)
        elif action == 'confirm':
            return confirm_subscription(body)
        elif action == 'unsubscribe':
            return unsubscribe(body)
        elif action == 'list':
            return list_subscribers(body)
        elif action == 'get':
            return get_subscriber(body)
        elif action == 'update':
            return update_subscriber(body)
        elif action == 'import':
            return import_subscribers(body)
        elif action == 'export':
            return export_subscribers()
        else:
            return response(400, {'error': 'Invalid action'})
            
    except Exception as e:
        return response(500, {'error': str(e)})

def subscribe(body):
    email = body.get('email', '').lower().strip()
    first_name = body.get('first_name', '')
    last_name = body.get('last_name', '')
    interests = body.get('interests', [])
    source = body.get('source', 'website')
    
    if not email or '@' not in email:
        return response(400, {'error': 'Invalid email'})
    
    # Check if already subscribed
    try:
        existing = table.get_item(Key={'email': email})
        if 'Item' in existing:
            if existing['Item']['status'] == 'active':
                return response(200, {'message': 'Already subscribed', 'email': email})
    except:
        pass
    
    # Generate confirmation token
    confirmation_token = str(uuid.uuid4())
    
    # Save subscriber with pending status
    subscriber = {
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'interests': interests,
        'status': 'pending',
        'subscribed_at': datetime.utcnow().isoformat(),
        'source': source,
        'confirmation_token': confirmation_token,
        'tags': [],
        'custom_fields': {}
    }
    
    table.put_item(Item=subscriber)
    
    # Send confirmation email
    send_confirmation_email(email, first_name, confirmation_token)
    
    return response(200, {
        'message': 'Confirmation email sent',
        'email': email
    })

def confirm_subscription(body):
    token = body.get('token')
    
    if not token:
        return response(400, {'error': 'Token required'})
    
    # Find subscriber by token
    scan_response = table.scan(
        FilterExpression='confirmation_token = :token',
        ExpressionAttributeValues={':token': token}
    )
    
    if not scan_response.get('Items'):
        return response(404, {'error': 'Invalid token'})
    
    subscriber = scan_response['Items'][0]
    email = subscriber['email']
    
    # Update status to active
    table.update_item(
        Key={'email': email},
        UpdateExpression='SET #status = :status, confirmed_at = :confirmed_at REMOVE confirmation_token',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={
            ':status': 'active',
            ':confirmed_at': datetime.utcnow().isoformat()
        }
    )
    
    # Send welcome email
    send_welcome_email(email, subscriber.get('first_name', ''))
    
    return response(200, {
        'message': 'Subscription confirmed',
        'email': email
    })

def unsubscribe(body):
    email = body.get('email', '').lower().strip()
    
    if not email:
        return response(400, {'error': 'Email required'})
    
    try:
        table.update_item(
            Key={'email': email},
            UpdateExpression='SET #status = :status, unsubscribed_at = :unsubscribed_at',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'unsubscribed',
                ':unsubscribed_at': datetime.utcnow().isoformat()
            }
        )
        
        return response(200, {
            'message': 'Successfully unsubscribed',
            'email': email
        })
    except Exception as e:
        return response(500, {'error': str(e)})

def list_subscribers(body):
    status_filter = body.get('status', 'active')
    limit = body.get('limit', 100)
    
    try:
        if status_filter:
            scan_response = table.query(
                IndexName='StatusIndex',
                KeyConditionExpression='#status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': status_filter},
                Limit=limit
            )
        else:
            scan_response = table.scan(Limit=limit)
        
        items = scan_response.get('Items', [])
        
        return response(200, {
            'subscribers': items,
            'count': len(items)
        })
    except Exception as e:
        return response(500, {'error': str(e)})

def get_subscriber(body):
    email = body.get('email', '').lower().strip()
    
    if not email:
        return response(400, {'error': 'Email required'})
    
    try:
        result = table.get_item(Key={'email': email})
        
        if 'Item' not in result:
            return response(404, {'error': 'Subscriber not found'})
        
        return response(200, {'subscriber': result['Item']})
    except Exception as e:
        return response(500, {'error': str(e)})

def update_subscriber(body):
    email = body.get('email', '').lower().strip()
    updates = body.get('updates', {})
    
    if not email:
        return response(400, {'error': 'Email required'})
    
    # Build update expression
    update_expr = 'SET '
    expr_values = {}
    expr_names = {}
    
    for key, value in updates.items():
        if key != 'email':  # Can't update primary key
            update_expr += f'#{key} = :{key}, '
            expr_names[f'#{key}'] = key
            expr_values[f':{key}'] = value
    
    update_expr = update_expr.rstrip(', ')
    
    try:
        table.update_item(
            Key={'email': email},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values
        )
        
        return response(200, {'message': 'Subscriber updated', 'email': email})
    except Exception as e:
        return response(500, {'error': str(e)})

def import_subscribers(body):
    subscribers = body.get('subscribers', [])
    
    if not subscribers:
        return response(400, {'error': 'No subscribers provided'})
    
    imported = 0
    errors = []
    
    for sub in subscribers:
        try:
            email = sub.get('email', '').lower().strip()
            if not email or '@' not in email:
                errors.append(f"Invalid email: {email}")
                continue
            
            subscriber = {
                'email': email,
                'first_name': sub.get('first_name', ''),
                'last_name': sub.get('last_name', ''),
                'interests': sub.get('interests', []),
                'status': 'active',  # Skip confirmation for imports
                'subscribed_at': datetime.utcnow().isoformat(),
                'source': 'import',
                'tags': sub.get('tags', []),
                'custom_fields': sub.get('custom_fields', {})
            }
            
            table.put_item(Item=subscriber)
            imported += 1
        except Exception as e:
            errors.append(f"Error importing {email}: {str(e)}")
    
    return response(200, {
        'message': f'Imported {imported} subscribers',
        'imported': imported,
        'errors': errors
    })

def export_subscribers():
    try:
        scan_response = table.scan()
        items = scan_response.get('Items', [])
        
        # Convert to CSV-friendly format
        subscribers = []
        for item in items:
            subscribers.append({
                'email': item.get('email'),
                'first_name': item.get('first_name', ''),
                'last_name': item.get('last_name', ''),
                'status': item.get('status'),
                'subscribed_at': item.get('subscribed_at', ''),
                'interests': ','.join(item.get('interests', []))
            })
        
        return response(200, {
            'subscribers': subscribers,
            'count': len(subscribers)
        })
    except Exception as e:
        return response(500, {'error': str(e)})

def send_confirmation_email(email, first_name, token):
    confirmation_url = f"https://christianconservativestoday.com/email-confirm.html?token={token}"
    
    subject = "Confirm Your Subscription - Christian Conservatives Today"
    
    html_body = f"""
    <html>
    <body>
        <h2>Welcome to Christian Conservatives Today!</h2>
        <p>Hi {first_name or 'there'},</p>
        <p>Thank you for subscribing to our newsletter. Please confirm your subscription by clicking the button below:</p>
        <p><a href="{confirmation_url}" style="background-color: #0066cc; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">Confirm Subscription</a></p>
        <p>Or copy and paste this link into your browser:</p>
        <p>{confirmation_url}</p>
        <p>If you didn't request this subscription, you can safely ignore this email.</p>
        <p>God bless,<br>Christian Conservatives Today Team</p>
    </body>
    </html>
    """
    
    text_body = f"""
    Welcome to Christian Conservatives Today!
    
    Hi {first_name or 'there'},
    
    Thank you for subscribing to our newsletter. Please confirm your subscription by visiting:
    {confirmation_url}
    
    If you didn't request this subscription, you can safely ignore this email.
    
    God bless,
    Christian Conservatives Today Team
    """
    
    try:
        ses.send_email(
            Source='newsletter@christianconservativestoday.com',
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {
                    'Text': {'Data': text_body},
                    'Html': {'Data': html_body}
                }
            }
        )
    except Exception as e:
        print(f"Error sending confirmation email: {e}")

def send_welcome_email(email, first_name):
    subject = "Welcome to Christian Conservatives Today!"
    
    html_body = f"""
    <html>
    <body>
        <h2>Welcome to Our Community!</h2>
        <p>Hi {first_name or 'there'},</p>
        <p>Your subscription is now confirmed! You'll receive:</p>
        <ul>
            <li>Weekly newsletter with top articles and videos</li>
            <li>Election updates and voter guides</li>
            <li>Prayer requests and ministry updates</li>
        </ul>
        <p><a href="https://christianconservativestoday.com">Visit our website</a></p>
        <p>God bless,<br>Christian Conservatives Today Team</p>
        <hr>
        <p style="font-size: 12px; color: #666;">
            <a href="https://christianconservativestoday.com/email-unsubscribe.html?email={email}">Unsubscribe</a>
        </p>
    </body>
    </html>
    """
    
    try:
        ses.send_email(
            Source='newsletter@christianconservativestoday.com',
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Html': {'Data': html_body}}
            }
        )
    except Exception as e:
        print(f"Error sending welcome email: {e}")

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(body, default=str)
    }
