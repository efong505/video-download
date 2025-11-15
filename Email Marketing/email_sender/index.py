import json
import boto3
import time
from datetime import datetime

ses = boto3.client('ses')
dynamodb = boto3.resource('dynamodb')
campaigns_table = dynamodb.Table('EmailCampaigns')
analytics_table = dynamodb.Table('EmailAnalytics')

# Throttle settings
BATCH_SIZE = 10  # Send 10 emails per batch
DELAY_BETWEEN_BATCHES = 1  # 1 second delay

def lambda_handler(event, context):
    try:
        campaign_id = event.get('campaign_id')
        recipients = event.get('recipients', [])
        is_test = event.get('is_test', False)
        
        if not campaign_id:
            return {'error': 'campaign_id required'}
        
        # Get campaign details
        result = campaigns_table.get_item(Key={'campaign_id': campaign_id})
        if 'Item' not in result:
            return {'error': 'Campaign not found'}
        
        campaign = result['Item']
        
        # Send emails in batches
        sent_count = 0
        failed_count = 0
        
        for i in range(0, len(recipients), BATCH_SIZE):
            batch = recipients[i:i + BATCH_SIZE]
            
            for email in batch:
                try:
                    send_email(campaign, email, campaign_id)
                    sent_count += 1
                    
                    # Log sent event
                    log_event(campaign_id, email, 'sent')
                    
                except Exception as e:
                    print(f"Failed to send to {email}: {e}")
                    failed_count += 1
            
            # Delay between batches to avoid throttling
            if i + BATCH_SIZE < len(recipients):
                time.sleep(DELAY_BETWEEN_BATCHES)
        
        # Update campaign status
        if not is_test:
            campaigns_table.update_item(
                Key={'campaign_id': campaign_id},
                UpdateExpression='SET #status = :status, sent_count = :sent_count',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={
                    ':status': 'sent',
                    ':sent_count': sent_count
                }
            )
        
        return {
            'message': 'Campaign sent',
            'campaign_id': campaign_id,
            'sent_count': sent_count,
            'failed_count': failed_count
        }
        
    except Exception as e:
        print(f"Error in email_sender: {e}")
        return {'error': str(e)}

def send_email(campaign, recipient_email, campaign_id):
    subject = campaign.get('subject', 'Newsletter')
    from_name = campaign.get('from_name', 'Christian Conservatives Today')
    from_email = campaign.get('from_email', 'newsletter@christianconservativestoday.com')
    reply_to = campaign.get('reply_to', 'contact@christianconservativestoday.com')
    
    # Get content
    html_content = campaign.get('content_html', '')
    text_content = campaign.get('content_text', '')
    
    # Add tracking pixel for opens
    tracking_pixel = f'<img src="https://christianconservativestoday.com/track-open?campaign_id={campaign_id}&email={recipient_email}" width="1" height="1" />'
    html_content += tracking_pixel
    
    # Add unsubscribe link
    unsubscribe_link = f'https://christianconservativestoday.com/email-unsubscribe.html?email={recipient_email}'
    html_content += f'<hr><p style="font-size: 12px; color: #666;"><a href="{unsubscribe_link}">Unsubscribe</a></p>'
    
    # Replace merge tags
    html_content = replace_merge_tags(html_content, recipient_email)
    text_content = replace_merge_tags(text_content, recipient_email)
    
    # Send email
    ses.send_email(
        Source=f'{from_name} <{from_email}>',
        Destination={'ToAddresses': [recipient_email]},
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': text_content},
                'Html': {'Data': html_content}
            }
        },
        ReplyToAddresses=[reply_to]
    )

def replace_merge_tags(content, email):
    # Get subscriber data
    subscribers_table = dynamodb.Table('EmailSubscribers')
    
    try:
        result = subscribers_table.get_item(Key={'email': email})
        if 'Item' in result:
            subscriber = result['Item']
            content = content.replace('{{first_name}}', subscriber.get('first_name', ''))
            content = content.replace('{{last_name}}', subscriber.get('last_name', ''))
            content = content.replace('{{email}}', email)
    except:
        pass
    
    return content

def log_event(campaign_id, email, event_type, metadata=None):
    import uuid
    
    event = {
        'event_id': str(uuid.uuid4()),
        'campaign_id': campaign_id,
        'email': email,
        'event_type': event_type,
        'timestamp': datetime.utcnow().isoformat(),
        'metadata': metadata or {}
    }
    
    try:
        analytics_table.put_item(Item=event)
    except Exception as e:
        print(f"Error logging event: {e}")
