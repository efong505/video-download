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
    sequence_name = enrollment.get('sequence_name', enrollment.get('campaign_id', ''))
    filter_tags = enrollment.get('filter_tags', [])
    current_sequence = int(enrollment.get('current_sequence_number', enrollment.get('current_sequence', 0)))
    enrolled_at = datetime.fromisoformat(enrollment['enrolled_at'].replace('Z', ''))
    last_sent_at = enrollment.get('last_sent_at')
    
    # Get all campaigns for this drip sequence (sorted by sequence_number)
    all_campaigns_response = campaigns_table.query(
        KeyConditionExpression='user_id = :uid',
        FilterExpression='attribute_exists(sequence_number)',
        ExpressionAttributeValues={':uid': user_id}
    )
    
    print(f"Found {len(all_campaigns_response['Items'])} campaigns with sequence_number")
    
    # Filter by tags if specified
    drip_campaigns = []
    for camp in all_campaigns_response['Items']:
        camp_tags = camp.get('filter_tags', [])
        print(f"Campaign {camp['campaign_id'][:8]}... has tags: {camp_tags}")
        if filter_tags and set(filter_tags).intersection(set(camp_tags)):
            drip_campaigns.append(camp)
            print(f"  -> Matched filter_tags {filter_tags}")
        elif not filter_tags:
            drip_campaigns.append(camp)
            print(f"  -> No filter_tags, including")
    
    drip_campaigns = sorted(drip_campaigns, key=lambda x: int(x.get('sequence_number', 0)))
    
    if not drip_campaigns:
        print(f"No drip campaigns found for {sequence_name}")
        return False
    
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
        last_sent = datetime.fromisoformat(last_sent_at.replace('Z', ''))
        due_date = last_sent + timedelta(days=delay_days)
    else:
        # First email after enrollment - send immediately (or after 1 hour)
        # Use delay_hours for first email if specified, otherwise send now
        delay_hours = int(next_email.get('delay_hours', 0))
        if delay_hours > 0:
            due_date = enrolled_at + timedelta(hours=delay_hours)
        else:
            due_date = enrolled_at  # Send immediately on next processor run
    
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
        UpdateExpression='SET current_sequence_number = :seq, last_sent_at = :ts',
        ExpressionAttributeValues={
            ':seq': next_email['sequence_number'],
            ':ts': now.isoformat()
        }
    )
    
    print(f"Email queued for {subscriber_email}")
    return True
