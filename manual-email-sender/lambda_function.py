"""
Manual Email Sender Lambda
Handles sending specific drip emails and custom emails to subscribers
"""
import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='us-east-1')

enrollments_table = dynamodb.Table('user-email-drip-enrollments')
campaigns_table = dynamodb.Table('user-email-campaigns')
subscribers_table = dynamodb.Table('user-email-subscribers')

def lambda_handler(event, context):
    """
    Handle manual email sending requests
    """
    print(f"Event: {json.dumps(event)}")
    
    # Parse request
    if 'body' in event:
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    else:
        body = event
    
    action = event.get('queryStringParameters', {}).get('action') if 'queryStringParameters' in event else body.get('action')
    
    if action == 'send_specific_drip':
        return send_specific_drip_email(body)
    elif action == 'send_custom_email':
        return send_custom_email(body)
    else:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'Invalid action'})
        }

def send_specific_drip_email(body):
    """
    Send a specific drip email to a subscriber
    """
    try:
        email = body.get('email')
        sequence_number = int(body.get('sequence_number', 1))
        
        if not email:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Email is required'})
            }
        
        # Find enrollment
        response = enrollments_table.scan(
            FilterExpression='subscriber_email = :email',
            ExpressionAttributeValues={':email': email}
        )
        
        if not response['Items']:
            return {
                'statusCode': 404,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Enrollment not found'})
            }
        
        enrollment = response['Items'][0]
        user_id = enrollment['user_id']
        filter_tags = enrollment.get('filter_tags', [])
        
        # Get the specific campaign email
        campaigns_response = campaigns_table.query(
            KeyConditionExpression='user_id = :uid',
            FilterExpression='sequence_number = :seq',
            ExpressionAttributeValues={
                ':uid': user_id,
                ':seq': sequence_number
            }
        )
        
        if not campaigns_response['Items']:
            return {
                'statusCode': 404,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': f'Email {sequence_number} not found'})
            }
        
        # Filter by tags
        campaign = None
        for camp in campaigns_response['Items']:
            camp_tags = camp.get('filter_tags', [])
            if filter_tags and set(filter_tags).intersection(set(camp_tags)):
                campaign = camp
                break
            elif not filter_tags:
                campaign = camp
                break
        
        if not campaign:
            return {
                'statusCode': 404,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'No matching campaign found'})
            }
        
        # Get subscriber info
        sub_response = subscribers_table.get_item(
            Key={'user_id': user_id, 'subscriber_email': email}
        )
        
        if 'Item' not in sub_response:
            return {
                'statusCode': 404,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Subscriber not found'})
            }
        
        subscriber = sub_response['Item']
        
        # Send email via SES
        send_email_via_ses(
            recipient=email,
            subject=campaign['subject'],
            body_html=campaign['body_html'],
            body_text=campaign.get('body_text', ''),
            subscriber=subscriber
        )
        
        # Update enrollment
        enrollments_table.update_item(
            Key={'user_id': user_id, 'enrollment_id': enrollment['enrollment_id']},
            UpdateExpression='SET current_sequence_number = :seq, last_sent_at = :ts',
            ExpressionAttributeValues={
                ':seq': sequence_number,
                ':ts': datetime.now().isoformat()
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': f'Email {sequence_number} sent to {email}',
                'campaign_id': campaign['campaign_id']
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def send_custom_email(body):
    """
    Send a custom email to one or more recipients
    """
    try:
        recipients = body.get('recipients', [])
        subject = body.get('subject')
        message = body.get('message')
        
        if not recipients or not subject or not message:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Recipients, subject, and message are required'})
            }
        
        # Send to each recipient
        sent_count = 0
        for recipient in recipients:
            try:
                ses.send_email(
                    Source='Christian Conservatives Today <noreply@christianconservativestoday.com>',
                    Destination={'ToAddresses': [recipient]},
                    Message={
                        'Subject': {'Data': subject},
                        'Body': {
                            'Html': {'Data': message},
                            'Text': {'Data': message}
                        }
                    }
                )
                sent_count += 1
            except Exception as e:
                print(f"Failed to send to {recipient}: {str(e)}")
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({
                'message': f'Custom email sent to {sent_count} recipient(s)',
                'sent_count': sent_count,
                'total_recipients': len(recipients)
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }

def send_email_via_ses(recipient, subject, body_html, body_text, subscriber):
    """
    Send email via AWS SES
    """
    first_name = subscriber.get('first_name', 'Friend')
    
    body_html = body_html.replace('{{first_name}}', first_name)
    body_text = body_text.replace('{{first_name}}', first_name)
    
    ses.send_email(
        Source='Christian Conservatives Today <noreply@christianconservativestoday.com>',
        Destination={'ToAddresses': [recipient]},
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Html': {'Data': body_html},
                'Text': {'Data': body_text}
            }
        }
    )
