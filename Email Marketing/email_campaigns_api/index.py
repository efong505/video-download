import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
campaigns_table = dynamodb.Table('EmailCampaigns')
subscribers_table = dynamodb.Table('EmailSubscribers')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        action = body.get('action')
        
        if action == 'create':
            return create_campaign(body)
        elif action == 'list':
            return list_campaigns(body)
        elif action == 'get':
            return get_campaign(body)
        elif action == 'update':
            return update_campaign(body)
        elif action == 'delete':
            return delete_campaign(body)
        elif action == 'send':
            return send_campaign(body)
        elif action == 'schedule':
            return schedule_campaign(body)
        else:
            return response(400, {'error': 'Invalid action'})
            
    except Exception as e:
        return response(500, {'error': str(e)})

def create_campaign(body):
    campaign_id = str(uuid.uuid4())
    
    campaign = {
        'campaign_id': campaign_id,
        'title': body.get('title', 'Untitled Campaign'),
        'subject': body.get('subject', ''),
        'from_name': body.get('from_name', 'Christian Conservatives Today'),
        'from_email': body.get('from_email', 'newsletter@christianconservativestoday.com'),
        'reply_to': body.get('reply_to', 'contact@christianconservativestoday.com'),
        'content_html': body.get('content_html', ''),
        'content_text': body.get('content_text', ''),
        'template_id': body.get('template_id', ''),
        'segment': body.get('segment', 'all'),
        'tags': body.get('tags', []),
        'status': 'draft',
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'recipient_count': 0,
        'open_count': 0,
        'click_count': 0,
        'unsubscribe_count': 0,
        'bounce_count': 0
    }
    
    campaigns_table.put_item(Item=campaign)
    
    return response(200, {
        'message': 'Campaign created',
        'campaign_id': campaign_id,
        'campaign': campaign
    })

def list_campaigns(body):
    status_filter = body.get('status')
    limit = body.get('limit', 50)
    
    try:
        if status_filter:
            scan_response = campaigns_table.query(
                IndexName='StatusIndex',
                KeyConditionExpression='#status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': status_filter},
                Limit=limit,
                ScanIndexForward=False
            )
        else:
            scan_response = campaigns_table.scan(Limit=limit)
        
        items = scan_response.get('Items', [])
        
        # Sort by created_at descending
        items.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return response(200, {
            'campaigns': items,
            'count': len(items)
        })
    except Exception as e:
        return response(500, {'error': str(e)})

def get_campaign(body):
    campaign_id = body.get('campaign_id')
    
    if not campaign_id:
        return response(400, {'error': 'campaign_id required'})
    
    try:
        result = campaigns_table.get_item(Key={'campaign_id': campaign_id})
        
        if 'Item' not in result:
            return response(404, {'error': 'Campaign not found'})
        
        return response(200, {'campaign': result['Item']})
    except Exception as e:
        return response(500, {'error': str(e)})

def update_campaign(body):
    campaign_id = body.get('campaign_id')
    updates = body.get('updates', {})
    
    if not campaign_id:
        return response(400, {'error': 'campaign_id required'})
    
    # Build update expression
    update_expr = 'SET updated_at = :updated_at'
    expr_values = {':updated_at': datetime.utcnow().isoformat()}
    expr_names = {}
    
    for key, value in updates.items():
        if key != 'campaign_id':
            update_expr += f', #{key} = :{key}'
            expr_names[f'#{key}'] = key
            expr_values[f':{key}'] = value
    
    try:
        campaigns_table.update_item(
            Key={'campaign_id': campaign_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names if expr_names else None,
            ExpressionAttributeValues=expr_values
        )
        
        return response(200, {'message': 'Campaign updated', 'campaign_id': campaign_id})
    except Exception as e:
        return response(500, {'error': str(e)})

def delete_campaign(body):
    campaign_id = body.get('campaign_id')
    
    if not campaign_id:
        return response(400, {'error': 'campaign_id required'})
    
    try:
        campaigns_table.delete_item(Key={'campaign_id': campaign_id})
        
        return response(200, {'message': 'Campaign deleted', 'campaign_id': campaign_id})
    except Exception as e:
        return response(500, {'error': str(e)})

def send_campaign(body):
    campaign_id = body.get('campaign_id')
    test_email = body.get('test_email')
    
    if not campaign_id:
        return response(400, {'error': 'campaign_id required'})
    
    try:
        # Get campaign
        result = campaigns_table.get_item(Key={'campaign_id': campaign_id})
        if 'Item' not in result:
            return response(404, {'error': 'Campaign not found'})
        
        campaign = result['Item']
        
        # If test email, send only to that address
        if test_email:
            lambda_client = boto3.client('lambda')
            payload = {
                'campaign_id': campaign_id,
                'recipients': [test_email],
                'is_test': True
            }
            
            lambda_client.invoke(
                FunctionName='email_sender',
                InvocationType='Event',
                Payload=json.dumps(payload)
            )
            
            return response(200, {
                'message': 'Test email queued',
                'campaign_id': campaign_id,
                'test_email': test_email
            })
        
        # Get recipients based on segment
        recipients = get_recipients(campaign.get('segment', 'all'), campaign.get('tags', []))
        
        if not recipients:
            return response(400, {'error': 'No recipients found'})
        
        # Update campaign status
        campaigns_table.update_item(
            Key={'campaign_id': campaign_id},
            UpdateExpression='SET #status = :status, recipient_count = :count, sent_at = :sent_at',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'sending',
                ':count': len(recipients),
                ':sent_at': datetime.utcnow().isoformat()
            }
        )
        
        # Invoke email_sender Lambda asynchronously
        lambda_client = boto3.client('lambda')
        payload = {
            'campaign_id': campaign_id,
            'recipients': recipients
        }
        
        lambda_client.invoke(
            FunctionName='email_sender',
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        
        return response(200, {
            'message': 'Campaign queued for sending',
            'campaign_id': campaign_id,
            'recipient_count': len(recipients)
        })
        
    except Exception as e:
        return response(500, {'error': str(e)})

def schedule_campaign(body):
    campaign_id = body.get('campaign_id')
    scheduled_time = body.get('scheduled_time')
    
    if not campaign_id or not scheduled_time:
        return response(400, {'error': 'campaign_id and scheduled_time required'})
    
    try:
        campaigns_table.update_item(
            Key={'campaign_id': campaign_id},
            UpdateExpression='SET #status = :status, scheduled_send_time = :scheduled_time',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'scheduled',
                ':scheduled_time': scheduled_time
            }
        )
        
        # Create EventBridge rule to trigger at scheduled time
        events_client = boto3.client('events')
        rule_name = f'email-campaign-{campaign_id}'
        
        # Convert ISO time to cron expression
        dt = datetime.fromisoformat(scheduled_time.replace('Z', '+00:00'))
        cron_expr = f'cron({dt.minute} {dt.hour} {dt.day} {dt.month} ? {dt.year})'
        
        events_client.put_rule(
            Name=rule_name,
            ScheduleExpression=cron_expr,
            State='ENABLED',
            Description=f'Send email campaign {campaign_id}'
        )
        
        # Add Lambda target
        events_client.put_targets(
            Rule=rule_name,
            Targets=[{
                'Id': '1',
                'Arn': 'arn:aws:lambda:us-east-1:YOUR-ACCOUNT-ID:function:email_campaigns_api',
                'Input': json.dumps({'body': json.dumps({'action': 'send', 'campaign_id': campaign_id})})
            }]
        )
        
        return response(200, {
            'message': 'Campaign scheduled',
            'campaign_id': campaign_id,
            'scheduled_time': scheduled_time
        })
        
    except Exception as e:
        return response(500, {'error': str(e)})

def get_recipients(segment, tags):
    recipients = []
    
    try:
        if segment == 'all':
            # Get all active subscribers
            scan_response = subscribers_table.query(
                IndexName='StatusIndex',
                KeyConditionExpression='#status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': 'active'}
            )
            recipients = [item['email'] for item in scan_response.get('Items', [])]
            
        elif segment == 'tagged':
            # Get subscribers with specific tags
            scan_response = subscribers_table.scan()
            for item in scan_response.get('Items', []):
                if item.get('status') == 'active':
                    subscriber_tags = item.get('tags', [])
                    if any(tag in subscriber_tags for tag in tags):
                        recipients.append(item['email'])
        
        return recipients
        
    except Exception as e:
        print(f"Error getting recipients: {e}")
        return []

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
