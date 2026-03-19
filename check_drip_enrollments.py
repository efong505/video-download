import boto3
import sys
from datetime import datetime

profile = 'ekewaka'
region = 'us-east-1'
table_name = 'user-email-drip-enrollments'

session = boto3.Session(profile_name=profile, region_name=region)
dynamodb = session.resource('dynamodb')
table = dynamodb.Table(table_name)

email = sys.argv[1] if len(sys.argv) > 1 else None

print("Checking drip enrollments...\n")

if email:
    print(f"Searching for: {email}")
    response = table.scan(
        FilterExpression='subscriber_email = :email',
        ExpressionAttributeValues={':email': email}
    )
else:
    print("Scanning all active enrollments...")
    response = table.scan(
        FilterExpression='#status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'active'}
    )

items = response.get('Items', [])

if not items:
    print("No enrollments found")
else:
    print(f"Found {len(items)} enrollment(s):\n")
    for item in items:
        print(f"Email: {item['subscriber_email']}")
        print(f"  User ID: {item['user_id']}")
        print(f"  Sequence Name: {item.get('sequence_name', item.get('campaign_id', 'N/A'))}")
        print(f"  Filter Tags: {item.get('filter_tags', [])}")
        print(f"  Status: {item['status']}")
        print(f"  Current Sequence: {item.get('current_sequence_number', 0)}")
        print(f"  Enrolled: {item['enrolled_at']}")
        if 'last_sent_at' in item:
            print(f"  Last Sent: {item['last_sent_at']}")
        print()
