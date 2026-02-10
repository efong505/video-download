import json
import boto3
import base64
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')
subscribers_table = dynamodb.Table('user-email-subscribers')
campaigns_table = dynamodb.Table('user-email-campaigns')
events_table = dynamodb.Table('user-email-events')
users_table = dynamodb.Table('users')

def lambda_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['body'])
        user_id = message['user_id']
        campaign_id = message['campaign_id']
        recipients = message['recipients']
        
        # Get campaign
        campaign = campaigns_table.get_item(Key={'user_id': user_id, 'campaign_id': campaign_id})['Item']
        
        # Get user info
        user = users_table.get_item(Key={'user_id': user_id})['Item']
        user_email = user.get('email', 'contact@christianconservativestoday.com')
        
        sent_count = 0
        
        for recipient_email in recipients:
            # Get subscriber details
            subscriber = subscribers_table.get_item(
                Key={'user_id': user_id, 'subscriber_email': recipient_email}
            ).get('Item', {})
            
            # Apply mail merge
            content = apply_mail_merge(campaign['content'], subscriber, user_id, campaign_id, recipient_email)
            
            # Add tracking pixel
            tracking_id = generate_tracking_id(user_id, campaign_id, recipient_email)
            content = add_tracking_pixel(content, tracking_id)
            
            # Send email
            try:
                ses.send_email(
                    Source=f"Christian Conservatives Today <contact@christianconservativestoday.com>",
                    Destination={'ToAddresses': [recipient_email]},
                    ReplyToAddresses=[user_email],
                    Message={
                        'Subject': {'Data': campaign['subject']},
                        'Body': {'Html': {'Data': content}}
                    }
                )
                sent_count += 1
                
                # Log event
                events_table.put_item(Item={
                    'user_id': user_id,
                    'event_id': f"{campaign_id}_{recipient_email}_{int(datetime.now().timestamp())}",
                    'campaign_id': campaign_id,
                    'subscriber_email': recipient_email,
                    'event_type': 'sent',
                    'timestamp': int(datetime.now().timestamp()),
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
            except Exception as e:
                print(f"Failed to send to {recipient_email}: {e}")
        
        # Update campaign
        campaigns_table.update_item(
            Key={'user_id': user_id, 'campaign_id': campaign_id},
            UpdateExpression='SET #status = :status, sent_at = :sent_at',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'sent',
                ':sent_at': datetime.now().isoformat()
            }
        )
        
        # Update user quota
        users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression='SET email_sent_this_month = email_sent_this_month + :count',
            ExpressionAttributeValues={':count': sent_count}
        )
    
    return {'statusCode': 200, 'body': 'Emails sent'}

def apply_mail_merge(content, subscriber, user_id, campaign_id, recipient_email):
    content = content.replace('{{first_name}}', subscriber.get('first_name', ''))
    content = content.replace('{{last_name}}', subscriber.get('last_name', ''))
    content = content.replace('{{email}}', recipient_email)
    
    # Unsubscribe link
    unsubscribe_token = base64.urlsafe_b64encode(
        f"{user_id}:{recipient_email}".encode()
    ).decode()
    unsubscribe_url = f"https://christianconservativestoday.com/unsubscribe?token={unsubscribe_token}"
    content = content.replace('{{unsubscribe_link}}', unsubscribe_url)
    
    return content

def generate_tracking_id(user_id, campaign_id, recipient_email):
    data = f"{user_id}:{campaign_id}:{recipient_email}"
    return base64.urlsafe_b64encode(data.encode()).decode()

def add_tracking_pixel(content, tracking_id):
    pixel_url = f"https://christianconservativestoday.com/track/open/{tracking_id}"
    pixel_html = f'<img src="{pixel_url}" width="1" height="1" style="display:none;" />'
    
    if '</body>' in content:
        content = content.replace('</body>', f'{pixel_html}</body>')
    else:
        content += pixel_html
    
    return content
