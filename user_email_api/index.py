import json
import boto3
import os
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
subscribers_table = dynamodb.Table('user-email-subscribers')
campaigns_table = dynamodb.Table('user-email-campaigns')
events_table = dynamodb.Table('user-email-events')
users_table = dynamodb.Table('users')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': json.dumps(body, default=decimal_default)
    }

def extract_user_id(event):
    auth_header = event.get('headers', {}).get('Authorization') or event.get('headers', {}).get('authorization')
    if not auth_header:
        return None

    import jwt
    token = auth_header.replace('Bearer ', '')
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload.get('user_id')
    except:
        return None

def check_subscriber_quota(user_id):
    response = users_table.get_item(Key={'user_id': user_id})
    user = response.get('Item', {})

    limit = int(user.get('email_subscriber_limit', 0))
    count = int(user.get('email_subscribers_count', 0))

    if count >= limit:
        return False, f"Subscriber limit reached ({count}/{limit})"
    return True, "Quota available"

def check_send_quota(user_id, recipient_count):
    response = users_table.get_item(Key={'user_id': user_id})
    user = response.get('Item', {})

    limit = int(user.get('email_monthly_limit', 0))
    sent = int(user.get('email_sent_this_month', 0))

    if sent + recipient_count > limit:
        return False, f"Monthly email limit reached ({sent + recipient_count}/{limit})"
    return True, "Quota available"

def add_subscriber(user_id, data):
    subscriber_email = data.get('email', '').lower().strip()
    if not subscriber_email:
        return cors_response(400, {'error': 'Email required'})

    # Check for duplicate before quota check
    existing = subscribers_table.get_item(
        Key={'user_id': user_id, 'subscriber_email': subscriber_email}
    )
    if 'Item' in existing:
        return cors_response(409, {'error': 'Subscriber already exists'})

    allowed, message = check_subscriber_quota(user_id)
    if not allowed:
        return cors_response(403, {'error': message, 'upgrade_url': '/pricing'})

    item = {
        'user_id': user_id,
        'subscriber_email': subscriber_email,
        'first_name': data.get('first_name', ''),
        'last_name': data.get('last_name', ''),
        'phone': data.get('phone', ''),
        'status': 'active',
        'subscribed_at': datetime.now().isoformat(),
        'source': data.get('source', 'manual'),
        'tags': data.get('tags', [])
    }

    subscribers_table.put_item(Item=item)

    users_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET email_subscribers_count = email_subscribers_count + :inc',
        ExpressionAttributeValues={':inc': 1}
    )

    return cors_response(200, {'message': 'Subscriber added', 'subscriber': item})

def list_subscribers(user_id, params):
    status = params.get('status', 'active')
    tags = params.get('tags', '')
    limit = int(params.get('limit', 100))
    last_key = params.get('last_key')

    query_params = {
        'IndexName': 'status-index',
        'KeyConditionExpression': 'user_id = :uid AND #status = :status',
        'ExpressionAttributeNames': {'#status': 'status'},
        'ExpressionAttributeValues': {':uid': user_id, ':status': status},
        'Limit': limit
    }

    if last_key:
        query_params['ExclusiveStartKey'] = json.loads(last_key)

    response = subscribers_table.query(**query_params)
    subscribers = response['Items']

    # Tag filtering (kept from live version's approach)
    if tags:
        tag_list = [t.strip() for t in tags.split(',')]
        subscribers = [s for s in subscribers if any(tag in s.get('tags', []) for tag in tag_list)]

    result = {'subscribers': subscribers}
    if 'LastEvaluatedKey' in response:
        result['last_key'] = json.dumps(response['LastEvaluatedKey'], default=decimal_default)

    return cors_response(200, result)

def update_subscriber(user_id, data):
    subscriber_email = data.get('email', '').lower().strip()
    if not subscriber_email:
        return cors_response(400, {'error': 'Email required'})

    updates = {}
    for field in ['first_name', 'last_name', 'phone', 'tags']:
        if field in data:
            updates[field] = data[field]

    if not updates:
        return cors_response(400, {'error': 'No fields to update'})

    update_expr = 'SET ' + ', '.join(f'#{k} = :{k}' for k in updates)
    expr_names = {f'#{k}': k for k in updates}
    expr_values = {f':{k}': v for k, v in updates.items()}

    subscribers_table.update_item(
        Key={'user_id': user_id, 'subscriber_email': subscriber_email},
        UpdateExpression=update_expr,
        ExpressionAttributeNames=expr_names,
        ExpressionAttributeValues=expr_values
    )

    return cors_response(200, {'message': 'Subscriber updated'})

def delete_subscriber(user_id, data):
    subscriber_email = data.get('email', '').lower().strip()

    # Verify subscriber exists before decrementing count
    existing = subscribers_table.get_item(
        Key={'user_id': user_id, 'subscriber_email': subscriber_email}
    )
    if 'Item' not in existing:
        return cors_response(404, {'error': 'Subscriber not found'})

    subscribers_table.delete_item(
        Key={'user_id': user_id, 'subscriber_email': subscriber_email}
    )

    users_table.update_item(
        Key={'user_id': user_id},
        UpdateExpression='SET email_subscribers_count = email_subscribers_count - :dec',
        ExpressionAttributeValues={':dec': 1}
    )

    return cors_response(200, {'message': 'Subscriber deleted'})

def unsubscribe(user_id, data):
    subscriber_email = data.get('email', '').lower().strip()
    if not subscriber_email:
        return cors_response(400, {'error': 'Email required'})

    subscribers_table.update_item(
        Key={'user_id': user_id, 'subscriber_email': subscriber_email},
        UpdateExpression='SET #status = :status, unsubscribed_at = :ts',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={
            ':status': 'unsubscribed',
            ':ts': datetime.now().isoformat()
        }
    )

    return cors_response(200, {'message': 'Unsubscribed successfully'})

def create_campaign(user_id, data):
    campaign_id = str(uuid.uuid4())

    item = {
        'user_id': user_id,
        'campaign_id': campaign_id,
        'title': data.get('title', ''),
        'subject': data.get('subject', ''),
        'content': data.get('content', ''),
        'template_id': data.get('template_id', ''),
        'filter_tags': data.get('filter_tags', []),
        'status': 'draft',
        'created_at': datetime.now().isoformat(),
        'recipient_count': 0,
        'open_count': 0,
        'click_count': 0
    }

    campaigns_table.put_item(Item=item)

    return cors_response(200, {'message': 'Campaign created', 'campaign_id': campaign_id})

def get_campaign(user_id, params):
    campaign_id = params.get('campaign_id')

    response = campaigns_table.get_item(Key={'user_id': user_id, 'campaign_id': campaign_id})
    campaign = response.get('Item')

    if not campaign:
        return cors_response(404, {'error': 'Campaign not found'})

    return cors_response(200, {'campaign': campaign})

def update_campaign(user_id, data):
    campaign_id = data.get('campaign_id')

    campaigns_table.update_item(
        Key={'user_id': user_id, 'campaign_id': campaign_id},
        UpdateExpression='SET title = :title, subject = :subject, content = :content, filter_tags = :tags',
        ExpressionAttributeValues={
            ':title': data.get('title', ''),
            ':subject': data.get('subject', ''),
            ':content': data.get('content', ''),
            ':tags': data.get('filter_tags', [])
        }
    )

    return cors_response(200, {'message': 'Campaign updated', 'campaign_id': campaign_id})

def list_campaigns(user_id):
    response = campaigns_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id},
        ScanIndexForward=False
    )

    return cors_response(200, {'campaigns': response['Items']})

def send_campaign(user_id, data):
    campaign_id = data.get('campaign_id')

    response = campaigns_table.get_item(Key={'user_id': user_id, 'campaign_id': campaign_id})
    campaign = response.get('Item')

    if not campaign:
        return cors_response(404, {'error': 'Campaign not found'})

    if campaign['user_id'] != user_id:
        return cors_response(403, {'error': 'Not your campaign'})

    filter_tags = campaign.get('filter_tags', [])

    # Get all active subscribers (handle pagination for large lists)
    subs_response = subscribers_table.query(
        IndexName='status-index',
        KeyConditionExpression='user_id = :uid AND #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':uid': user_id, ':status': 'active'}
    )
    subscribers = subs_response['Items']

    while 'LastEvaluatedKey' in subs_response:
        subs_response = subscribers_table.query(
            IndexName='status-index',
            KeyConditionExpression='user_id = :uid AND #status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':uid': user_id, ':status': 'active'},
            ExclusiveStartKey=subs_response['LastEvaluatedKey']
        )
        subscribers.extend(subs_response['Items'])

    # Filter by tags if specified
    if filter_tags:
        subscribers = [s for s in subscribers if any(tag in s.get('tags', []) for tag in filter_tags)]

    recipient_count = len(subscribers)
    if recipient_count == 0:
        return cors_response(400, {'error': 'No matching subscribers found'})

    allowed, message = check_send_quota(user_id, recipient_count)
    if not allowed:
        return cors_response(403, {'error': message, 'upgrade_url': '/pricing'})

    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/371751795928/email-sending-queue'

    # Batch recipients to stay under SQS 256KB message limit
    batch_size = 5000
    recipient_emails = [s['subscriber_email'] for s in subscribers]

    for i in range(0, len(recipient_emails), batch_size):
        batch = recipient_emails[i:i + batch_size]
        sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps({
                'user_id': user_id,
                'campaign_id': campaign_id,
                'recipients': batch
            })
        )

    campaigns_table.update_item(
        Key={'user_id': user_id, 'campaign_id': campaign_id},
        UpdateExpression='SET #status = :status, recipient_count = :count',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'sending', ':count': recipient_count}
    )

    return cors_response(200, {'message': 'Campaign queued for sending', 'recipient_count': recipient_count})

def get_analytics(user_id, params):
    campaign_id = params.get('campaign_id')
    if not campaign_id:
        return cors_response(400, {'error': 'campaign_id required'})

    # Verify ownership
    camp_response = campaigns_table.get_item(Key={'user_id': user_id, 'campaign_id': campaign_id})
    campaign = camp_response.get('Item')
    if not campaign:
        return cors_response(404, {'error': 'Campaign not found'})

    # Get events for this campaign
    events_response = events_table.query(
        IndexName='campaign-index',
        KeyConditionExpression='campaign_id = :cid',
        ExpressionAttributeValues={':cid': campaign_id}
    )

    events = events_response['Items']
    opens = sum(1 for e in events if e.get('event_type') == 'opened')
    clicks = sum(1 for e in events if e.get('event_type') == 'clicked')
    sent = sum(1 for e in events if e.get('event_type') == 'sent')

    recipient_count = int(campaign.get('recipient_count', 0))

    return cors_response(200, {
        'analytics': {
            'campaign_id': campaign_id,
            'title': campaign.get('title'),
            'status': campaign.get('status'),
            'recipient_count': recipient_count,
            'sent_count': sent,
            'open_count': opens,
            'click_count': clicks,
            'open_rate': round((opens / recipient_count * 100), 2) if recipient_count > 0 else 0,
            'click_rate': round((clicks / recipient_count * 100), 2) if recipient_count > 0 else 0
        }
    })

def get_analytics_overview(user_id):
    # Get all campaigns for user
    campaigns_response = campaigns_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id}
    )
    campaigns = campaigns_response['Items']

    # Get all events for user (query by partition key)
    events_response = events_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id}
    )
    events = events_response['Items']

    # Handle pagination if there are many events
    while 'LastEvaluatedKey' in events_response:
        events_response = events_table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': user_id},
            ExclusiveStartKey=events_response['LastEvaluatedKey']
        )
        events.extend(events_response['Items'])

    # Aggregate stats
    total_sent = sum(1 for e in events if e.get('event_type') == 'sent')
    total_delivered = sum(1 for e in events if e.get('event_type') == 'delivered')
    total_opens = sum(1 for e in events if e.get('event_type') == 'opened')
    total_clicks = sum(1 for e in events if e.get('event_type') == 'clicked')
    total_bounces = sum(1 for e in events if e.get('event_type') == 'bounced')
    total_complaints = sum(1 for e in events if e.get('event_type') == 'complaint')

    return cors_response(200, {
        'stats': {
            'total_sent': total_sent,
            'total_delivered': total_delivered,
            'total_opens': total_opens,
            'total_clicks': total_clicks,
            'total_bounces': total_bounces,
            'total_complaints': total_complaints
        }
    })

def get_recent_events_public(params):
    """Public endpoint for platform owner analytics"""
    PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'
    limit = int(params.get('limit', 50))
    
    # Get ALL events to sort by timestamp
    events = []
    response = events_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
    )
    events.extend(response['Items'])
    
    # Handle pagination
    while 'LastEvaluatedKey' in response:
        response = events_table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID},
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        events.extend(response['Items'])
    
    # Sort by timestamp descending (newest first)
    events.sort(key=lambda x: int(x.get('timestamp', 0)), reverse=True)
    
    # Take only requested limit
    events = events[:limit]
    
    return cors_response(200, {'events': events})

def get_campaign_analytics_public(params):
    """Public endpoint for platform owner campaign analytics"""
    PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'
    
    campaigns_response = campaigns_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
    )
    
    campaigns = []
    for campaign in campaigns_response['Items']:
        events_response = events_table.query(
            IndexName='campaign-index',
            KeyConditionExpression='campaign_id = :cid',
            ExpressionAttributeValues={':cid': campaign['campaign_id']}
        )
        events = events_response['Items']
        
        opens = sum(1 for e in events if e.get('event_type') == 'opened')
        clicks = sum(1 for e in events if e.get('event_type') == 'clicked')
        sent = sum(1 for e in events if e.get('event_type') == 'sent')
        bounces = sum(1 for e in events if e.get('event_type') == 'bounced')
        complaints = sum(1 for e in events if e.get('event_type') == 'complaint')
        
        campaigns.append({
            'campaign_id': campaign['campaign_id'],
            'campaign_name': campaign.get('campaign_name', campaign.get('title', '')),
            'title': campaign.get('campaign_name', campaign.get('title', '')),
            'campaign_group': campaign.get('campaign_group', ''),
            'sent_count': sent,
            'open_count': opens,
            'click_count': clicks,
            'bounce_count': bounces,
            'complaint_count': complaints,
            'open_rate': round((opens / sent * 100), 2) if sent > 0 else 0,
            'click_rate': round((clicks / sent * 100), 2) if sent > 0 else 0
        })
    
    return cors_response(200, {'campaigns': campaigns})

def get_analytics_overview_public():
    """Public endpoint for platform owner overview"""
    PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'
    return get_analytics_overview(PLATFORM_OWNER_ID)

def get_subscriber_analytics_public():
    """Public endpoint for platform owner subscriber analytics"""
    PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'
    
    # Get all subscribers
    subs_response = subscribers_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
    )
    subscribers = subs_response['Items']
    
    # Get all events
    events_response = events_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
    )
    events = events_response['Items']
    
    # Aggregate stats per subscriber
    subscriber_stats = {}
    for event in events:
        email = event.get('subscriber_email') or event.get('email')
        if not email:
            continue
            
        if email not in subscriber_stats:
            subscriber_stats[email] = {
                'subscriber_email': email,
                'sent_count': 0,
                'open_count': 0,
                'click_count': 0,
                'bounce_count': 0,
                'complaint_count': 0,
                'last_activity': None
            }
        
        event_type = event.get('event_type')
        if event_type == 'sent':
            subscriber_stats[email]['sent_count'] += 1
        elif event_type == 'opened':
            subscriber_stats[email]['open_count'] += 1
        elif event_type == 'clicked':
            subscriber_stats[email]['click_count'] += 1
        elif event_type == 'bounced':
            subscriber_stats[email]['bounce_count'] += 1
        elif event_type == 'complaint':
            subscriber_stats[email]['complaint_count'] += 1
        
        # Update last activity
        event_date = event.get('date') or (datetime.fromtimestamp(event.get('timestamp', 0)).isoformat() if event.get('timestamp') else None)
        if event_date and (not subscriber_stats[email]['last_activity'] or event_date > subscriber_stats[email]['last_activity']):
            subscriber_stats[email]['last_activity'] = event_date
    
    return cors_response(200, {'subscribers': list(subscriber_stats.values())})

def lambda_handler(event, context):
    if event.get('httpMethod') == 'OPTIONS':
        return cors_response(200, {})

    params = event.get('queryStringParameters') or {}
    action = params.get('action')

    try:
        body = json.loads(event.get('body', '{}'))
    except:
        body = {}
    
    user_id = extract_user_id(event)

    # Public actions (no auth required) for platform owner analytics
    public_actions = {
        'get_recent_events': lambda: get_recent_events_public(params),
        'get_campaign_analytics': lambda: get_campaign_analytics_public(params),
        'get_analytics_overview': lambda: get_analytics_overview_public(),
        'get_subscriber_analytics': lambda: get_subscriber_analytics_public(),
    }
    
    # Check if it's a public action first
    if action in public_actions:
        return public_actions[action]()
    
    # For authenticated actions, require user_id
    if not user_id:
        return cors_response(401, {'error': 'Unauthorized'})
    
    actions = {
        'add_subscriber': lambda: add_subscriber(user_id, body),
        'list_subscribers': lambda: list_subscribers(user_id, params),
        'update_subscriber': lambda: update_subscriber(user_id, body),
        'delete_subscriber': lambda: delete_subscriber(user_id, body),
        'unsubscribe': lambda: unsubscribe(user_id, body),
        'create_campaign': lambda: create_campaign(user_id, body),
        'get_campaign': lambda: get_campaign(user_id, params),
        'update_campaign': lambda: update_campaign(user_id, body),
        'list_campaigns': lambda: list_campaigns(user_id),
        'send_campaign': lambda: send_campaign(user_id, body),
        'get_analytics': lambda: get_analytics(user_id, params),
        'get_analytics_overview': lambda: get_analytics_overview(user_id),
    }

    handler = actions.get(action)
    if handler:
        return handler()

    return cors_response(400, {'error': f'Invalid action: {action}'})
