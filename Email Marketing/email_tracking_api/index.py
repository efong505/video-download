import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
analytics_table = dynamodb.Table('EmailAnalytics')
campaigns_table = dynamodb.Table('EmailCampaigns')

def lambda_handler(event, context):
    try:
        # Handle both API Gateway and direct invocation
        if 'body' in event:
            body = json.loads(event.get('body', '{}'))
        else:
            body = event
        
        action = body.get('action')
        
        if action == 'track_open':
            return track_open(body)
        elif action == 'track_click':
            return track_click(body)
        elif action == 'get_stats':
            return get_campaign_stats(body)
        elif action == 'get_events':
            return get_campaign_events(body)
        else:
            return response(400, {'error': 'Invalid action'})
            
    except Exception as e:
        return response(500, {'error': str(e)})

def track_open(body):
    campaign_id = body.get('campaign_id')
    email = body.get('email')
    
    if not campaign_id or not email:
        return response(400, {'error': 'campaign_id and email required'})
    
    # Log open event
    event_id = str(uuid.uuid4())
    event = {
        'event_id': event_id,
        'campaign_id': campaign_id,
        'email': email,
        'event_type': 'opened',
        'timestamp': datetime.utcnow().isoformat(),
        'metadata': {
            'user_agent': body.get('user_agent', ''),
            'ip_address': body.get('ip_address', '')
        }
    }
    
    analytics_table.put_item(Item=event)
    
    # Update campaign open count
    try:
        campaigns_table.update_item(
            Key={'campaign_id': campaign_id},
            UpdateExpression='SET open_count = open_count + :inc',
            ExpressionAttributeValues={':inc': 1}
        )
    except:
        pass
    
    # Return 1x1 transparent pixel
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'image/gif',
            'Cache-Control': 'no-cache, no-store, must-revalidate'
        },
        'body': 'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7',
        'isBase64Encoded': True
    }

def track_click(body):
    campaign_id = body.get('campaign_id')
    email = body.get('email')
    link_url = body.get('link_url')
    
    if not campaign_id or not email or not link_url:
        return response(400, {'error': 'campaign_id, email, and link_url required'})
    
    # Log click event
    event_id = str(uuid.uuid4())
    event = {
        'event_id': event_id,
        'campaign_id': campaign_id,
        'email': email,
        'event_type': 'clicked',
        'timestamp': datetime.utcnow().isoformat(),
        'metadata': {
            'link_url': link_url,
            'user_agent': body.get('user_agent', ''),
            'ip_address': body.get('ip_address', '')
        }
    }
    
    analytics_table.put_item(Item=event)
    
    # Update campaign click count
    try:
        campaigns_table.update_item(
            Key={'campaign_id': campaign_id},
            UpdateExpression='SET click_count = click_count + :inc',
            ExpressionAttributeValues={':inc': 1}
        )
    except:
        pass
    
    # Redirect to actual URL
    return {
        'statusCode': 302,
        'headers': {
            'Location': link_url
        },
        'body': ''
    }

def get_campaign_stats(body):
    campaign_id = body.get('campaign_id')
    
    if not campaign_id:
        return response(400, {'error': 'campaign_id required'})
    
    try:
        # Get campaign
        result = campaigns_table.get_item(Key={'campaign_id': campaign_id})
        if 'Item' not in result:
            return response(404, {'error': 'Campaign not found'})
        
        campaign = result['Item']
        
        # Calculate rates
        recipient_count = campaign.get('recipient_count', 0)
        open_count = campaign.get('open_count', 0)
        click_count = campaign.get('click_count', 0)
        unsubscribe_count = campaign.get('unsubscribe_count', 0)
        bounce_count = campaign.get('bounce_count', 0)
        
        stats = {
            'campaign_id': campaign_id,
            'title': campaign.get('title'),
            'status': campaign.get('status'),
            'sent_at': campaign.get('sent_at'),
            'recipient_count': recipient_count,
            'open_count': open_count,
            'click_count': click_count,
            'unsubscribe_count': unsubscribe_count,
            'bounce_count': bounce_count,
            'open_rate': round((open_count / recipient_count * 100), 2) if recipient_count > 0 else 0,
            'click_rate': round((click_count / recipient_count * 100), 2) if recipient_count > 0 else 0,
            'unsubscribe_rate': round((unsubscribe_count / recipient_count * 100), 2) if recipient_count > 0 else 0,
            'bounce_rate': round((bounce_count / recipient_count * 100), 2) if recipient_count > 0 else 0
        }
        
        return response(200, {'stats': stats})
        
    except Exception as e:
        return response(500, {'error': str(e)})

def get_campaign_events(body):
    campaign_id = body.get('campaign_id')
    event_type = body.get('event_type')
    limit = body.get('limit', 100)
    
    if not campaign_id:
        return response(400, {'error': 'campaign_id required'})
    
    try:
        # Query events by campaign
        query_params = {
            'IndexName': 'CampaignIndex',
            'KeyConditionExpression': 'campaign_id = :campaign_id',
            'ExpressionAttributeValues': {':campaign_id': campaign_id},
            'Limit': limit,
            'ScanIndexForward': False
        }
        
        # Filter by event type if specified
        if event_type:
            query_params['FilterExpression'] = 'event_type = :event_type'
            query_params['ExpressionAttributeValues'][':event_type'] = event_type
        
        result = analytics_table.query(**query_params)
        events = result.get('Items', [])
        
        return response(200, {
            'events': events,
            'count': len(events)
        })
        
    except Exception as e:
        return response(500, {'error': str(e)})

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
