import json
import boto3
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
import hashlib

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
newsletters_table = dynamodb.Table('newsletters')
subscribers_table = dynamodb.Table('email_subscribers')
book_subscribers_table = dynamodb.Table('book-subscribers')
templates_table = dynamodb.Table('newsletter_templates')
analytics_table = dynamodb.Table('newsletter_analytics')
ses = boto3.client('ses', region_name='us-east-1')

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    http_method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method')
    
    if http_method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        params = event.get('queryStringParameters') or {}
        action = params.get('action')
        
        if not action and http_method == 'POST':
            body = json.loads(event.get('body', '{}'))
            action = body.get('action', 'list')
        
        if not action:
            action = 'list'
        
        if action == 'create_newsletter':
            return create_newsletter(event, headers)
        elif action == 'list_newsletters':
            return list_newsletters(event, headers)
        elif action == 'get_newsletter':
            return get_newsletter(event, headers)
        elif action == 'update_newsletter':
            return update_newsletter(event, headers)
        elif action == 'delete_newsletter':
            return delete_newsletter(event, headers)
        elif action == 'send_newsletter':
            return send_newsletter(event, headers)
        elif action == 'subscribe':
            return subscribe(event, headers)
        elif action == 'confirm_email':
            return confirm_email(event, headers)
        elif action == 'unsubscribe':
            return unsubscribe(event, headers)
        elif action == 'list_subscribers':
            return list_subscribers(event, headers)
        elif action == 'list_book_subscribers':
            return list_book_subscribers(event, headers)
        elif action == 'create_template':
            return create_template(event, headers)
        elif action == 'list_templates':
            return list_templates(event, headers)
        elif action == 'get_template':
            return get_template(event, headers)
        elif action == 'delete_template':
            return delete_template(event, headers)
        elif action == 'track_open':
            return track_open(event, headers)
        elif action == 'track_click':
            return track_click(event, headers)
        elif action == 'get_analytics':
            return get_analytics(event, headers)
        elif action == 'get_subscriber':
            return get_subscriber(event, headers)
        elif action == 'update_subscriber':
            return update_subscriber(event, headers)
        elif action == 'delete_subscriber':
            return delete_subscriber(event, headers)
        elif action == 'get_newsletter_analytics':
            return get_newsletter_analytics(event, headers)
        elif action == 'add_subscriber':
            return add_subscriber(event, headers)
        elif action == 'bulk_import':
            return bulk_import(event, headers)
        elif action == 'create_campaign':
            return create_campaign(event, headers)
        elif action == 'list_campaigns':
            return list_campaigns(event, headers)
        elif action == 'update_campaign':
            return update_campaign(event, headers)
        elif action == 'delete_campaign':
            return delete_campaign(event, headers)
        else:
            return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Invalid action'})}
    
    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}

def create_newsletter(event, headers):
    body = json.loads(event['body'])
    
    newsletter = {
        'newsletter_id': str(uuid.uuid4()),
        'title': body['title'],
        'subject': body['subject'],
        'content': body['content'],
        'template_id': body.get('template_id', ''),
        'status': body.get('status', 'draft'),
        'scheduled_send': body.get('scheduled_send', ''),
        'created_by': body.get('created_by', ''),
        'created_at': datetime.utcnow().isoformat(),
        'sent_at': '',
        'recipient_count': 0,
        'open_count': 0,
        'click_count': 0
    }
    
    newsletters_table.put_item(Item=newsletter)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Newsletter created', 'newsletter_id': newsletter['newsletter_id']})}

def list_newsletters(event, headers):
    params = event.get('queryStringParameters') or {}
    response = newsletters_table.scan()
    newsletters = response.get('Items', [])
    
    if params.get('status'):
        newsletters = [n for n in newsletters if n.get('status') == params['status']]
    
    newsletters.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'newsletters': newsletters}, cls=DecimalEncoder)}

def get_newsletter(event, headers):
    params = event.get('queryStringParameters') or {}
    newsletter_id = params.get('newsletter_id')
    
    if not newsletter_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'newsletter_id required'})}
    
    response = newsletters_table.get_item(Key={'newsletter_id': newsletter_id})
    newsletter = response.get('Item')
    
    if not newsletter:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Newsletter not found'})}
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'newsletter': newsletter}, cls=DecimalEncoder)}

def update_newsletter(event, headers):
    body = json.loads(event['body'])
    newsletter_id = body['newsletter_id']
    
    update_expr = 'SET '
    expr_values = {}
    expr_names = {}
    updates = []
    
    fields = ['title', 'subject', 'content', 'template_id', 'status', 'scheduled_send']
    
    for field in fields:
        if field in body:
            updates.append(f'#{field} = :{field}')
            expr_values[f':{field}'] = body[field]
            expr_names[f'#{field}'] = field
    
    if not updates:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'No fields to update'})}
    
    update_expr += ', '.join(updates)
    
    newsletters_table.update_item(
        Key={'newsletter_id': newsletter_id},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_names,
        ExpressionAttributeValues=expr_values
    )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Newsletter updated'})}

def delete_newsletter(event, headers):
    params = event.get('queryStringParameters') or {}
    newsletter_id = params.get('newsletter_id')
    
    if not newsletter_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'newsletter_id required'})}
    
    newsletters_table.delete_item(Key={'newsletter_id': newsletter_id})
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Newsletter deleted'})}

def send_newsletter(event, headers):
    body = json.loads(event['body'])
    newsletter_id = body['newsletter_id']
    campaign = body.get('campaign', 'general')
    
    # Get newsletter
    response = newsletters_table.get_item(Key={'newsletter_id': newsletter_id})
    newsletter = response.get('Item')
    
    if not newsletter:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Newsletter not found'})}
    
    # Get active subscribers for campaign
    response = subscribers_table.scan()
    all_subscribers = response.get('Items', [])
    subscribers = [s for s in all_subscribers if s.get('status') == 'active' and campaign in s.get('campaigns', ['general'])]
    
    sent_count = 0
    errors = []
    for subscriber in subscribers:
        try:
            tracking_id = str(uuid.uuid4())
            content_with_tracking = str(newsletter.get('content', ''))
            
            # Mail merge replacements
            content_with_tracking = content_with_tracking.replace('{{first_name}}', subscriber.get('first_name', 'Friend'))
            content_with_tracking = content_with_tracking.replace('{{last_name}}', subscriber.get('last_name', ''))
            content_with_tracking = content_with_tracking.replace('{{email}}', subscriber['email'])
            content_with_tracking = content_with_tracking.replace('{{unsubscribe_link}}', f'https://christianconservativestoday.com/unsubscribe.html?email={subscriber["email"]}')
            
            # Add tracking pixel
            content_with_tracking += f'<img src="https://gu6c08ctel.execute-api.us-east-1.amazonaws.com/prod/newsletter?action=track_open&id={tracking_id}" width="1" height="1" />'
            
            ses.send_email(
                Source='noreply@christianconservativestoday.com',
                Destination={'ToAddresses': [subscriber['email']]},
                Message={
                    'Subject': {'Data': str(newsletter.get('subject', 'Newsletter'))},
                    'Body': {'Html': {'Data': content_with_tracking}}
                }
            )
            
            analytics_table.put_item(Item={
                'tracking_id': tracking_id,
                'newsletter_id': newsletter_id,
                'email': subscriber['email'],
                'campaign': campaign,
                'opened': False,
                'open_count': 0,
                'clicked': False,
                'sent_at': datetime.utcnow().isoformat()
            })
            
            sent_count += 1
        except Exception as e:
            error_msg = f'Failed to send to {subscriber["email"]}: {str(e)}'
            print(error_msg)
            errors.append(error_msg)
    
    if sent_count > 0:
        newsletters_table.update_item(
            Key={'newsletter_id': newsletter_id},
            UpdateExpression='SET #status = :status, sent_at = :sent_at, recipient_count = :count',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'sent', ':sent_at': datetime.utcnow().isoformat(), ':count': sent_count}
        )
    
    result = {'message': f'Newsletter sent to {sent_count} subscribers', 'sent_count': sent_count}
    if errors:
        result['errors'] = errors
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(result)}

def subscribe(event, headers):
    body = json.loads(event['body'])
    email = body['email']
    first_name = body.get('first_name', 'Friend')
    list_type = body.get('list_type', 'election')  # 'election' or 'book'
    
    # Choose table based on list type
    table = book_subscribers_table if list_type == 'book' else subscribers_table
    
    # Check if email already exists
    try:
        response = table.get_item(Key={'email': email})
        if 'Item' in response:
            return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'already_subscribed'})}
    except Exception as e:
        print(f'Error checking existing subscriber: {e}')
    
    # For book list, no confirmation needed - direct subscribe
    if list_type == 'book':
        subscriber = {
            'email': email,
            'first_name': first_name,
            'subscribed_at': datetime.utcnow().isoformat(),
            'source': body.get('source', 'book_landing_page')
        }
        table.put_item(Item=subscriber)
        
        # Notify admin
        try:
            ses.send_email(
                Source='noreply@christianconservativestoday.com',
                Destination={'ToAddresses': ['contact@christianconservativestoday.com']},
                Message={
                    'Subject': {'Data': 'New Book Mailing List Subscriber'},
                    'Body': {'Text': {'Data': f'New book subscriber:\n\nEmail: {email}\nName: {first_name}\nSource: {subscriber["source"]}\nSubscribed: {subscriber["subscribed_at"]}'}}
                }
            )
        except Exception as e:
            print(f'Failed to send admin notification: {e}')
        
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Subscription successful'})}
    
    # Election list - use confirmation flow
    token = hashlib.sha256(f"{email}{datetime.utcnow().isoformat()}{uuid.uuid4()}".encode()).hexdigest()
    expires_at = (datetime.utcnow() + timedelta(hours=24)).isoformat()
    
    subscriber = {
        'email': email,
        'first_name': first_name,
        'last_name': body.get('last_name', ''),
        'phone': body.get('phone', ''),
        'campaigns': body.get('campaigns', ['general']),
        'status': 'pending',
        'confirmation_token': token,
        'token_expires_at': expires_at,
        'subscribed_at': datetime.utcnow().isoformat(),
        'source': body.get('source', 'website')
    }
    
    table.put_item(Item=subscriber)
    
    # Send confirmation email
    from email_templates import get_confirmation_email
    confirmation_link = f"https://christianconservativestoday.com/confirm-email.html?token={token}"
    html_content = get_confirmation_email(first_name, confirmation_link)
    
    try:
        ses.send_email(
            Source='noreply@christianconservativestoday.com',
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': 'Confirm Your Subscription - Christian Conservatives Today'},
                'Body': {'Html': {'Data': html_content}}
            }
        )
    except Exception as e:
        print(f'Failed to send confirmation email: {e}')
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Confirmation email sent'})}

def confirm_email(event, headers):
    params = event.get('queryStringParameters') or {}
    token = params.get('token')
    
    if not token:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Token required'})}
    
    # Find subscriber by token
    response = subscribers_table.scan(
        FilterExpression='confirmation_token = :token',
        ExpressionAttributeValues={':token': token}
    )
    
    items = response.get('Items', [])
    if not items:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Invalid token'})}
    
    subscriber = items[0]
    
    # Check if token expired
    if datetime.fromisoformat(subscriber['token_expires_at']) < datetime.utcnow():
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Token expired'})}
    
    # Activate subscriber
    subscribers_table.update_item(
        Key={'email': subscriber['email']},
        UpdateExpression='SET #status = :status, confirmed_at = :time REMOVE confirmation_token, token_expires_at',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'active', ':time': datetime.utcnow().isoformat()}
    )
    
    # Send welcome email
    from email_templates import get_welcome_email
    html_content = get_welcome_email(subscriber.get('first_name', 'Friend'))
    
    try:
        ses.send_email(
            Source='noreply@christianconservativestoday.com',
            Destination={'ToAddresses': [subscriber['email']]},
            Message={
                'Subject': {'Data': 'Welcome to Christian Conservatives Today!'},
                'Body': {'Html': {'Data': html_content}}
            }
        )
    except Exception as e:
        print(f'Failed to send welcome email: {e}')
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Email confirmed successfully'})}

def unsubscribe(event, headers):
    params = event.get('queryStringParameters') or {}
    email = params.get('email')
    
    if not email:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'email required'})}
    
    subscribers_table.update_item(
        Key={'email': email},
        UpdateExpression='SET #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'unsubscribed'}
    )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Unsubscribed successfully'})}

def list_subscribers(event, headers):
    params = event.get('queryStringParameters') or {}
    response = subscribers_table.scan()
    subscribers = response.get('Items', [])
    
    if params.get('status'):
        subscribers = [s for s in subscribers if s.get('status') == params['status']]
    
    subscribers.sort(key=lambda x: x.get('subscribed_at', ''), reverse=True)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'subscribers': subscribers}, cls=DecimalEncoder)}

def list_book_subscribers(event, headers):
    response = book_subscribers_table.scan()
    subscribers = response.get('Items', [])
    subscribers.sort(key=lambda x: x.get('subscribed_at', ''), reverse=True)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'subscribers': subscribers}, cls=DecimalEncoder)}

def create_template(event, headers):
    body = json.loads(event['body'])
    
    template = {
        'template_id': str(uuid.uuid4()),
        'name': body['name'],
        'description': body.get('description', ''),
        'html': body['html'],
        'thumbnail': body.get('thumbnail', ''),
        'created_at': datetime.utcnow().isoformat()
    }
    
    templates_table.put_item(Item=template)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Template created', 'template_id': template['template_id']})}

def list_templates(event, headers):
    response = templates_table.scan()
    templates = response.get('Items', [])
    templates.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'templates': templates}, cls=DecimalEncoder)}

def get_template(event, headers):
    params = event.get('queryStringParameters') or {}
    template_id = params.get('template_id')
    
    if not template_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'template_id required'})}
    
    response = templates_table.get_item(Key={'template_id': template_id})
    template = response.get('Item')
    
    if not template:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Template not found'})}
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'template': template}, cls=DecimalEncoder)}

def delete_template(event, headers):
    params = event.get('queryStringParameters') or {}
    template_id = params.get('template_id')
    
    if not template_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'template_id required'})}
    
    templates_table.delete_item(Key={'template_id': template_id})
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Template deleted'})}

def track_open(event, headers):
    params = event.get('queryStringParameters') or {}
    tracking_id = params.get('id')
    
    if tracking_id:
        try:
            # Get current open_count
            response = analytics_table.get_item(Key={'tracking_id': tracking_id})
            item = response.get('Item', {})
            current_count = int(item.get('open_count', 0))
            
            # Increment open count
            analytics_table.update_item(
                Key={'tracking_id': tracking_id},
                UpdateExpression='SET opened = :opened, open_count = :count, last_opened_at = :time',
                ExpressionAttributeValues={
                    ':opened': True,
                    ':count': current_count + 1,
                    ':time': datetime.utcnow().isoformat()
                }
            )
        except Exception as e:
            print(f'Track open error: {e}')
    
    # Return 1x1 transparent GIF
    return {
        'statusCode': 200,
        'headers': {
            **headers,
            'Content-Type': 'image/gif'
        },
        'body': 'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
        'isBase64Encoded': True
    }

def track_click(event, headers):
    params = event.get('queryStringParameters') or {}
    tracking_id = params.get('id')
    
    if tracking_id:
        analytics_table.update_item(
            Key={'tracking_id': tracking_id},
            UpdateExpression='SET clicked = :val',
            ExpressionAttributeValues={':val': True}
        )
    
    return {'statusCode': 200, 'headers': headers, 'body': ''}

def get_analytics(event, headers):
    response = analytics_table.scan()
    analytics = response.get('Items', [])
    analytics.sort(key=lambda x: x.get('sent_at', ''), reverse=True)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'analytics': analytics}, cls=DecimalEncoder)}

def get_subscriber(event, headers):
    params = event.get('queryStringParameters') or {}
    email = params.get('email')
    
    if not email:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'email required'})}
    
    response = subscribers_table.get_item(Key={'email': email})
    subscriber = response.get('Item')
    
    if not subscriber:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Subscriber not found'})}
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'subscriber': subscriber}, cls=DecimalEncoder)}

def update_subscriber(event, headers):
    body = json.loads(event['body'])
    email = body['email']
    
    update_expr = 'SET '
    expr_values = {}
    expr_names = {}
    updates = []
    
    fields = ['first_name', 'last_name', 'phone', 'campaigns']
    
    for field in fields:
        if field in body:
            updates.append(f'#{field} = :{field}')
            expr_values[f':{field}'] = body[field]
            expr_names[f'#{field}'] = field
    
    if updates:
        update_expr += ', '.join(updates)
        subscribers_table.update_item(
            Key={'email': email},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values
        )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Subscriber updated'})}

def delete_subscriber(event, headers):
    params = event.get('queryStringParameters') or {}
    email = params.get('email')
    
    if not email:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'email required'})}
    
    subscribers_table.delete_item(Key={'email': email})
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Subscriber deleted'})}

def get_newsletter_analytics(event, headers):
    params = event.get('queryStringParameters') or {}
    newsletter_id = params.get('newsletter_id')
    
    if not newsletter_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'newsletter_id required'})}
    
    response = analytics_table.scan(
        FilterExpression='newsletter_id = :nid',
        ExpressionAttributeValues={':nid': newsletter_id}
    )
    analytics = response.get('Items', [])
    analytics.sort(key=lambda x: x.get('open_count', 0), reverse=True)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'analytics': analytics}, cls=DecimalEncoder)}

def add_subscriber(event, headers):
    body = json.loads(event['body'])
    email = body['email']
    
    # Check if already exists
    try:
        response = subscribers_table.get_item(Key={'email': email})
        if 'Item' in response:
            return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Email already exists'})}
    except Exception as e:
        print(f'Error checking email: {e}')
    
    subscriber = {
        'email': email,
        'first_name': body.get('first_name', ''),
        'last_name': body.get('last_name', ''),
        'phone': body.get('phone', ''),
        'campaigns': body.get('campaigns', ['general']),
        'status': 'active',
        'subscribed_at': datetime.utcnow().isoformat(),
        'confirmed_at': datetime.utcnow().isoformat(),
        'source': 'admin'
    }
    
    subscribers_table.put_item(Item=subscriber)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Subscriber added'})}

def bulk_import(event, headers):
    body = json.loads(event['body'])
    subscribers_data = body.get('subscribers', [])
    
    added = 0
    skipped = 0
    errors = []
    
    for sub in subscribers_data:
        email = sub.get('email', '').strip().lower()
        if not email:
            skipped += 1
            continue
        
        try:
            response = subscribers_table.get_item(Key={'email': email})
            if 'Item' in response:
                skipped += 1
                continue
            
            subscriber = {
                'email': email,
                'first_name': sub.get('first_name', '').strip(),
                'last_name': sub.get('last_name', '').strip(),
                'phone': sub.get('phone', '').strip(),
                'campaigns': sub.get('campaigns', ['general']),
                'status': 'active',
                'subscribed_at': datetime.utcnow().isoformat(),
                'confirmed_at': datetime.utcnow().isoformat(),
                'source': 'bulk_import'
            }
            
            subscribers_table.put_item(Item=subscriber)
            added += 1
        except Exception as e:
            errors.append(f'{email}: {str(e)}')
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({
        'message': f'Import complete: {added} added, {skipped} skipped',
        'added': added,
        'skipped': skipped,
        'errors': errors
    })}

def create_campaign(event, headers):
    body = json.loads(event['body'])
    campaigns_table = dynamodb.Table('newsletter_campaigns')
    
    campaign = {
        'campaign_id': body.get('campaign_id', body['name'].lower().replace(' ', '_')),
        'name': body['name'],
        'description': body.get('description', ''),
        'created_at': datetime.utcnow().isoformat()
    }
    
    campaigns_table.put_item(Item=campaign)
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Campaign created'})}

def list_campaigns(event, headers):
    campaigns_table = dynamodb.Table('newsletter_campaigns')
    response = campaigns_table.scan()
    campaigns = response.get('Items', [])
    campaigns.sort(key=lambda x: x.get('created_at', ''))
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'campaigns': campaigns}, cls=DecimalEncoder)}

def update_campaign(event, headers):
    body = json.loads(event['body'])
    campaigns_table = dynamodb.Table('newsletter_campaigns')
    
    campaigns_table.update_item(
        Key={'campaign_id': body['campaign_id']},
        UpdateExpression='SET #name = :name, description = :desc',
        ExpressionAttributeNames={'#name': 'name'},
        ExpressionAttributeValues={':name': body['name'], ':desc': body.get('description', '')}
    )
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Campaign updated'})}

def delete_campaign(event, headers):
    params = event.get('queryStringParameters') or {}
    campaign_id = params.get('campaign_id')
    campaigns_table = dynamodb.Table('newsletter_campaigns')
    campaigns_table.delete_item(Key={'campaign_id': campaign_id})
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Campaign deleted'})}
