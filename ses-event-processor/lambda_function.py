"""
SES Event Processor Lambda
Processes SES events (bounce, complaint, delivery, open, click) from SNS
Stores analytics in DynamoDB for dashboard
"""
import json
import boto3
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
events_table = dynamodb.Table('email-events')
campaign_stats_table = dynamodb.Table('email-campaign-stats')
subscriber_stats_table = dynamodb.Table('email-subscriber-stats')

def lambda_handler(event, context):
    """
    Process SES events from SNS
    """
    print(f"Received event: {json.dumps(event)}")
    
    for record in event.get('Records', []):
        try:
            # Parse SNS message
            message = json.loads(record['Sns']['Message'])
            event_type = message.get('eventType', message.get('notificationType', 'unknown'))
            
            print(f"Processing event type: {event_type}")
            
            # Route to appropriate handler
            if event_type == 'Bounce':
                process_bounce(message)
            elif event_type == 'Complaint':
                process_complaint(message)
            elif event_type == 'Delivery':
                process_delivery(message)
            elif event_type == 'Send':
                process_send(message)
            elif event_type == 'Reject':
                process_reject(message)
            elif event_type == 'Open':
                process_open(message)
            elif event_type == 'Click':
                process_click(message)
            else:
                print(f"Unknown event type: {event_type}")
                
        except Exception as e:
            print(f"Error processing record: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    return {'statusCode': 200, 'body': 'Events processed'}

def process_send(message):
    """Process email send event"""
    mail = message.get('mail', {})
    destination = mail.get('destination', [])
    message_id = mail.get('messageId', '')
    timestamp = mail.get('timestamp', datetime.now().isoformat())
    
    tags = mail.get('tags', {})
    campaign_id = tags.get('campaign_id', ['unknown'])[0] if isinstance(tags.get('campaign_id'), list) else tags.get('campaign_id', 'unknown')
    
    for recipient in destination:
        log_event(recipient, 'sent', campaign_id, {
            'message_id': message_id,
            'timestamp': timestamp
        })
        
        update_campaign_stats(campaign_id, 'sent_count', 1)
        update_subscriber_stats(recipient, 'emails_sent', 1)

def process_delivery(message):
    """Process email delivery event"""
    mail = message.get('mail', {})
    delivery = message.get('delivery', {})
    
    recipients = delivery.get('recipients', [])
    message_id = mail.get('messageId', '')
    timestamp = delivery.get('timestamp', datetime.now().isoformat())
    
    tags = mail.get('tags', {})
    campaign_id = tags.get('campaign_id', ['unknown'])[0] if isinstance(tags.get('campaign_id'), list) else tags.get('campaign_id', 'unknown')
    
    for recipient in recipients:
        log_event(recipient, 'delivered', campaign_id, {
            'message_id': message_id,
            'timestamp': timestamp,
            'processing_time_millis': delivery.get('processingTimeMillis', 0)
        })
        
        update_campaign_stats(campaign_id, 'delivered_count', 1)
        update_subscriber_stats(recipient, 'emails_delivered', 1)

def process_bounce(message):
    """Process bounce event"""
    mail = message.get('mail', {})
    bounce = message.get('bounce', {})
    
    bounced_recipients = bounce.get('bouncedRecipients', [])
    bounce_type = bounce.get('bounceType', 'Unknown')
    bounce_subtype = bounce.get('bounceSubType', 'Unknown')
    timestamp = bounce.get('timestamp', datetime.now().isoformat())
    
    tags = mail.get('tags', {})
    campaign_id = tags.get('campaign_id', ['unknown'])[0] if isinstance(tags.get('campaign_id'), list) else tags.get('campaign_id', 'unknown')
    
    for recipient_info in bounced_recipients:
        recipient = recipient_info.get('emailAddress', '')
        
        log_event(recipient, 'bounced', campaign_id, {
            'bounce_type': bounce_type,
            'bounce_subtype': bounce_subtype,
            'timestamp': timestamp,
            'diagnostic_code': recipient_info.get('diagnosticCode', '')
        })
        
        update_campaign_stats(campaign_id, 'bounce_count', 1)
        update_subscriber_stats(recipient, 'bounces', 1)
        
        # Mark subscriber as bounced if hard bounce
        if bounce_type == 'Permanent':
            mark_subscriber_bounced(recipient)

def process_complaint(message):
    """Process spam complaint event"""
    mail = message.get('mail', {})
    complaint = message.get('complaint', {})
    
    complained_recipients = complaint.get('complainedRecipients', [])
    complaint_type = complaint.get('complaintFeedbackType', 'Unknown')
    timestamp = complaint.get('timestamp', datetime.now().isoformat())
    
    tags = mail.get('tags', {})
    campaign_id = tags.get('campaign_id', ['unknown'])[0] if isinstance(tags.get('campaign_id'), list) else tags.get('campaign_id', 'unknown')
    
    for recipient_info in complained_recipients:
        recipient = recipient_info.get('emailAddress', '')
        
        log_event(recipient, 'complaint', campaign_id, {
            'complaint_type': complaint_type,
            'timestamp': timestamp
        })
        
        update_campaign_stats(campaign_id, 'complaint_count', 1)
        update_subscriber_stats(recipient, 'complaints', 1)
        
        # Mark subscriber as complained
        mark_subscriber_complained(recipient)

def process_reject(message):
    """Process email reject event"""
    mail = message.get('mail', {})
    reject = message.get('reject', {})
    
    destination = mail.get('destination', [])
    reason = reject.get('reason', 'Unknown')
    
    tags = mail.get('tags', {})
    campaign_id = tags.get('campaign_id', ['unknown'])[0] if isinstance(tags.get('campaign_id'), list) else tags.get('campaign_id', 'unknown')
    
    for recipient in destination:
        log_event(recipient, 'rejected', campaign_id, {
            'reason': reason
        })
        
        update_campaign_stats(campaign_id, 'reject_count', 1)

def process_open(message):
    """Process email open event"""
    mail = message.get('mail', {})
    open_event = message.get('open', {})
    
    tags = mail.get('tags', {})
    campaign_id = tags.get('campaign_id', ['unknown'])[0] if isinstance(tags.get('campaign_id'), list) else tags.get('campaign_id', 'unknown')
    recipient = tags.get('recipient', ['unknown'])[0] if isinstance(tags.get('recipient'), list) else tags.get('recipient', 'unknown')
    
    timestamp = open_event.get('timestamp', datetime.now().isoformat())
    user_agent = open_event.get('userAgent', '')
    
    log_event(recipient, 'opened', campaign_id, {
        'timestamp': timestamp,
        'user_agent': user_agent,
        'ip_address': open_event.get('ipAddress', '')
    })
    
    update_campaign_stats(campaign_id, 'open_count', 1)
    update_subscriber_stats(recipient, 'opens', 1)

def process_click(message):
    """Process email click event"""
    mail = message.get('mail', {})
    click_event = message.get('click', {})
    
    tags = mail.get('tags', {})
    campaign_id = tags.get('campaign_id', ['unknown'])[0] if isinstance(tags.get('campaign_id'), list) else tags.get('campaign_id', 'unknown')
    recipient = tags.get('recipient', ['unknown'])[0] if isinstance(tags.get('recipient'), list) else tags.get('recipient', 'unknown')
    
    timestamp = click_event.get('timestamp', datetime.now().isoformat())
    link = click_event.get('link', '')
    user_agent = click_event.get('userAgent', '')
    
    log_event(recipient, 'clicked', campaign_id, {
        'timestamp': timestamp,
        'link': link,
        'user_agent': user_agent,
        'ip_address': click_event.get('ipAddress', '')
    })
    
    update_campaign_stats(campaign_id, 'click_count', 1)
    update_subscriber_stats(recipient, 'clicks', 1)

def log_event(email, event_type, campaign_id, metadata=None):
    """Log event to email-events table"""
    import uuid
    
    event_id = str(uuid.uuid4())
    timestamp = int(datetime.now().timestamp())
    
    item = {
        'event_id': event_id,
        'timestamp': timestamp,
        'email': email,
        'event_type': event_type,
        'campaign_id': campaign_id,
        'date': datetime.now().isoformat()
    }
    
    if metadata:
        item['metadata'] = json.dumps(metadata)
    
    try:
        events_table.put_item(Item=item)
        print(f"Logged {event_type} event for {email}")
    except Exception as e:
        print(f"Error logging event: {str(e)}")

def update_campaign_stats(campaign_id, metric, increment):
    """Update campaign statistics"""
    try:
        campaign_stats_table.update_item(
            Key={'campaign_id': campaign_id},
            UpdateExpression=f'ADD {metric} :inc SET last_updated = :ts',
            ExpressionAttributeValues={
                ':inc': increment,
                ':ts': datetime.now().isoformat()
            }
        )
    except Exception as e:
        # Create if doesn't exist
        try:
            campaign_stats_table.put_item(Item={
                'campaign_id': campaign_id,
                metric: increment,
                'last_updated': datetime.now().isoformat()
            })
        except Exception as e2:
            print(f"Error updating campaign stats: {str(e2)}")

def update_subscriber_stats(email, metric, increment):
    """Update subscriber statistics"""
    try:
        subscriber_stats_table.update_item(
            Key={'subscriber_email': email},
            UpdateExpression=f'ADD {metric} :inc SET last_activity = :ts',
            ExpressionAttributeValues={
                ':inc': increment,
                ':ts': datetime.now().isoformat()
            }
        )
    except Exception as e:
        # Create if doesn't exist
        try:
            subscriber_stats_table.put_item(Item={
                'subscriber_email': email,
                metric: increment,
                'last_activity': datetime.now().isoformat()
            })
        except Exception as e2:
            print(f"Error updating subscriber stats: {str(e2)}")

def mark_subscriber_bounced(email):
    """Mark subscriber as bounced"""
    subscribers_table = dynamodb.Table('user-email-subscribers')
    try:
        subscribers_table.update_item(
            Key={'user_id': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2', 'subscriber_email': email},
            UpdateExpression='SET #status = :status, bounced_at = :ts',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'bounced',
                ':ts': datetime.now().isoformat()
            }
        )
    except Exception as e:
        print(f"Error marking subscriber bounced: {str(e)}")

def mark_subscriber_complained(email):
    """Mark subscriber as complained"""
    subscribers_table = dynamodb.Table('user-email-subscribers')
    try:
        subscribers_table.update_item(
            Key={'user_id': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2', 'subscriber_email': email},
            UpdateExpression='SET #status = :status, complained_at = :ts',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'complained',
                ':ts': datetime.now().isoformat()
            }
        )
    except Exception as e:
        print(f"Error marking subscriber complained: {str(e)}")
