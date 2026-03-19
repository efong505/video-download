import boto3
from datetime import datetime
import uuid

profile = 'ekewaka'
region = 'us-east-1'
user_id = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'  # Ed's user ID
campaign_id = 'book-drip-campaign'

session = boto3.Session(profile_name=profile, region_name=region)
dynamodb = session.resource('dynamodb')
enrollments_table = dynamodb.Table('user-email-drip-enrollments')
subscribers_table = dynamodb.Table('user-email-subscribers')

# Get all book subscribers
print("Fetching book subscribers...")
response = subscribers_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': user_id}
)

subscribers = response.get('Items', [])
print(f"Found {len(subscribers)} subscribers\n")

enrolled_count = 0
for sub in subscribers:
    email = sub['subscriber_email']
    tags = sub.get('tags', [])
    
    # Only enroll if they have 'book' or 'survival-kit' tag
    if 'book' not in tags and 'survival-kit' not in tags:
        print(f"Skipping {email} - no book/survival-kit tag")
        continue
    
    # Check if already enrolled
    check = enrollments_table.get_item(
        Key={
            'user_id': user_id,
            'enrollment_id': f"{email}#{campaign_id}"
        }
    )
    
    if 'Item' in check:
        print(f"Already enrolled: {email}")
        continue
    
    # Enroll in drip campaign
    enrollment_item = {
        'user_id': user_id,
        'enrollment_id': f"{email}#{campaign_id}",
        'subscriber_email': email,
        'campaign_id': campaign_id,
        'status': 'active',
        'current_sequence_number': 0,
        'enrolled_at': datetime.utcnow().isoformat() + 'Z'
    }
    
    enrollments_table.put_item(Item=enrollment_item)
    print(f"Enrolled: {email}")
    enrolled_count += 1

print(f"\nEnrolled {enrolled_count} new subscriber(s) in drip campaign")
