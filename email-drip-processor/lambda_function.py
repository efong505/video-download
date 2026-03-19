"""
Email Drip Campaign Processor Lambda
Triggered daily by EventBridge to send scheduled drip emails
"""
import json
import boto3
from datetime import datetime, timedelta
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')
ses = boto3.client('ses', region_name='us-east-1')

enrollments_table = dynamodb.Table('user-email-drip-enrollments')
campaigns_table = dynamodb.Table('user-email-campaigns')
subscribers_table = dynamodb.Table('user-email-subscribers')

SQS_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/371751795928/email-sending-queue'

def lambda_handler(event, context):
    """
    Process active drip enrollments and send due emails
    """
    print("Starting drip processor...")
    
    # Get all active enrollments
    response = enrollments_table.scan(
        FilterExpression='#status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'active'}
    )
    
    enrollments = response['Items']
    print(f"Found {len(enrollments)} active enrollments")
    
    emails_sent = 0
    
    for enrollment in enrollments:
        try:
            result = process_enrollment(enrollment)
            if result:
                emails_sent += 1
        except Exception as e:
            print(f"Error processing enrollment {enrollment.get('enrollment_id')}: {str(e)}")
            continue
    
    print(f"Drip processor complete. Sent {emails_sent} emails.")
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Drip processor complete',
            'enrollments_processed': len(enrollments),
            'emails_sent': emails_sent
        })
    }

def process_enrollment(enrollment):
    """
    Check if enrollment is due for next email and send it
    Returns True if email was sent
    """
    user_id = enrollment['user_id']
    subscriber_email = enrollment['subscriber_email']
    campaign_id = enrollment['campaign_id']
    current_sequence = int(enrollment.get('current_sequence', 0))
    enrolled_at = datetime.fromisoformat(enrollment['enrolled_at'])
    last_sent_at = enrollment.get('last_sent_at')
    
    # Get campaign to find next email in sequence
    camp_response = campaigns_table.get_item(
        Key={'user_id': user_id, 'campaign_id': campaign_id}
    )
    
    if 'Item' not in camp_response:
        print(f"Campaign {campaign_id} not found")
        return False
    
    campaign = camp_response['Item']
    
    # Check if this is a drip campaign
    if campaign.get('campaign_type') != 'drip':
        print(f"Campaign {campaign_id} is not a drip campaign")
        return False
    
    # Get all campaigns for this drip sequence (sorted by sequence_number)
    all_campaigns_response = campaigns_table.query(
        KeyConditionExpression='user_id = :uid',
        FilterExpression='campaign_type = :type AND filter_tags = :tags',
        ExpressionAttributeValues={
            ':uid': user_id,
            ':type': 'drip',
            ':tags': campaign.get('filter_tags', [])
        }
    )
    
    drip_campaigns = sorted(
        all_campaigns_response['Items'],
        key=lambda x: int(x.get('sequence_number', 0))
    )
    
    # Find next email to send
    next_email = None
    for camp in drip_campaigns:
        seq_num = int(camp.get('sequence_number', 0))
        if seq_num == current_sequence + 1:
            next_email = camp
            break
    
    if not next_email:
        # No more emails in sequence - mark as completed
        enrollments_table.update_item(
            Key={'user_id': user_id, 'enrollment_id': enrollment['enrollment_id']},
            UpdateExpression='SET #status = :status, completed_at = :ts',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'completed',
                ':ts': datetime.now().isoformat()
            }
        )
        print(f"Enrollment {enrollment['enrollment_id']} completed")
        return False
    
    # Calculate if email is due
    delay_days = int(next_email.get('delay_days', 1))
    
    if last_sent_at:
        last_sent = datetime.fromisoformat(last_sent_at)
        due_date = last_sent + timedelta(days=delay_days)
    else:
        # First email after enrollment
        due_date = enrolled_at + timedelta(days=delay_days)
    
    now = datetime.now()
    
    if now < due_date:
        # Not due yet
        return False
    
    # Email is due - send it
    print(f"Sending email {next_email['sequence_number']} to {subscriber_email}")
    
    # Verify subscriber is still active
    sub_response = subscribers_table.get_item(
        Key={'user_id': user_id, 'subscriber_email': subscriber_email}
    )
    
    if 'Item' not in sub_response or sub_response['Item'].get('status') != 'active':
        print(f"Subscriber {subscriber_email} is not active - skipping")
        # Pause enrollment
        enrollments_table.update_item(
            Key={'user_id': user_id, 'enrollment_id': enrollment['enrollment_id']},
            UpdateExpression='SET #status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'paused'}
        )
        return False
    
    subscriber = sub_response['Item']
    
    # Send email via SQS (existing email-sender Lambda will process it)
    sqs.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps({
            'user_id': user_id,
            'campaign_id': next_email['campaign_id'],
            'recipients': [subscriber_email],
            'drip_sequence': True
        })
    )
    
    # Update enrollment
    enrollments_table.update_item(
        Key={'user_id': user_id, 'enrollment_id': enrollment['enrollment_id']},
        UpdateExpression='SET current_sequence = :seq, last_sent_at = :ts',
        ExpressionAttributeValues={
            ':seq': next_email['sequence_number'],
            ':ts': now.isoformat()
        }
    )
    
    print(f"Email queued for {subscriber_email}")
    return True
