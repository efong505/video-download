import json
import boto3
from datetime import datetime
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
notifications_table = dynamodb.Table('notifications')
users_table = dynamodb.Table('users')
ses = boto3.client('ses', region_name='us-east-1')

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        params = event.get('queryStringParameters') or {}
        body = json.loads(event.get('body', '{}')) if event.get('body') else {}
        action = params.get('action') or body.get('action')
        
        if action == 'send_notification':
            return send_notification(body, headers)
        elif action == 'get_user_notifications':
            return get_user_notifications(params, headers)
        elif action == 'mark_read':
            return mark_read(body, headers)
        elif action == 'get_preferences':
            return get_preferences(params, headers)
        elif action == 'update_preferences':
            return update_preferences(body, headers)
        else:
            return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Invalid action'})}
    
    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}

def send_notification(body, headers):
    notification_type = body['type']
    recipient_email = body['recipient_email']
    subject = body['subject']
    message = body['message']
    link = body.get('link', '')
    
    # Check user preferences
    try:
        user_response = users_table.get_item(Key={'email': recipient_email})
        user = user_response.get('Item', {})
        prefs = user.get('notification_preferences', {})
        
        if not prefs.get(f'{notification_type}_email', True):
            return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'User opted out'})}
    except:
        pass
    
    # Store notification
    notification_id = f"{recipient_email}#{datetime.utcnow().isoformat()}"
    notifications_table.put_item(Item={
        'notification_id': notification_id,
        'recipient_email': recipient_email,
        'type': notification_type,
        'subject': subject,
        'message': message,
        'link': link,
        'read': False,
        'created_at': datetime.utcnow().isoformat()
    })
    
    # Send email
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
            <h1 style="color: white; margin: 0;">Christian Conservatives Today</h1>
        </div>
        <div style="padding: 30px; background: #f9f9f9;">
            <h2 style="color: #333;">{subject}</h2>
            <p style="color: #666; line-height: 1.6;">{message}</p>
            {f'<p><a href="{link}" style="display: inline-block; background: #667eea; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin-top: 20px;">View Details</a></p>' if link else ''}
        </div>
        <div style="padding: 20px; text-align: center; color: #999; font-size: 12px;">
            <p>Christian Conservatives Today | <a href="https://christianconservativestoday.com">Visit Website</a></p>
        </div>
    </body>
    </html>
    """
    
    try:
        ses.send_email(
            Source='noreply@christianconservativestoday.com',
            Destination={'ToAddresses': [recipient_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Html': {'Data': html_body}}
            }
        )
    except Exception as e:
        print(f'Email send error: {e}')
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Notification sent'})}

def get_user_notifications(params, headers):
    email = params.get('email')
    
    response = notifications_table.scan(
        FilterExpression='recipient_email = :email',
        ExpressionAttributeValues={':email': email}
    )
    
    notifications = response.get('Items', [])
    notifications.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'notifications': notifications}, cls=DecimalEncoder)}

def mark_read(body, headers):
    notification_id = body['notification_id']
    
    notifications_table.update_item(
        Key={'notification_id': notification_id},
        UpdateExpression='SET #read = :val',
        ExpressionAttributeNames={'#read': 'read'},
        ExpressionAttributeValues={':val': True}
    )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Marked as read'})}

def get_preferences(params, headers):
    email = params.get('email')
    
    response = users_table.get_item(Key={'email': email})
    user = response.get('Item', {})
    prefs = user.get('notification_preferences', {
        'comment_reply_email': True,
        'article_published_email': True,
        'prayer_update_email': True,
        'event_reminder_email': True,
        'admin_alert_email': True
    })
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'preferences': prefs})}

def update_preferences(body, headers):
    email = body['email']
    prefs = body['preferences']
    
    users_table.update_item(
        Key={'email': email},
        UpdateExpression='SET notification_preferences = :prefs',
        ExpressionAttributeValues={':prefs': prefs}
    )
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Preferences updated'})}
