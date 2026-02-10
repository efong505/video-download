import boto3
import json

lambda_client = boto3.client('lambda')
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('users')

def notify_admins(alert_type, message, link=''):
    """Send notification to all admins"""
    try:
        # Get all admin users
        response = users_table.scan()
        users = response.get('Items', [])
        admins = [u for u in users if u.get('role') in ['admin', 'super_user']]
        
        subject_map = {
            'new_comment': 'New Comment Submitted',
            'new_prayer': 'New Prayer Request',
            'new_video': 'New Video Uploaded',
            'reported_content': 'Content Reported'
        }
        
        subject = subject_map.get(alert_type, 'Admin Alert')
        
        for admin in admins:
            try:
                lambda_client.invoke(
                    FunctionName='notifications_api',
                    InvocationType='Event',
                    Payload=json.dumps({
                        'body': json.dumps({
                            'action': 'send_notification',
                            'type': 'admin_alert',
                            'recipient_email': admin['email'],
                            'subject': subject,
                            'message': message,
                            'link': link
                        })
                    })
                )
            except Exception as e:
                print(f'Failed to notify admin {admin["email"]}: {e}')
    except Exception as e:
        print(f'Error sending admin notifications: {e}')
