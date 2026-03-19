import boto3
from datetime import datetime, timedelta

profile = 'ekewaka'
region = 'us-east-1'
user_id = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

session = boto3.Session(profile_name=profile, region_name=region)
dynamodb = session.resource('dynamodb')
enrollments_table = dynamodb.Table('user-email-drip-enrollments')

# Backdate the most recent enrollment by 2 days
email = 'test-final-20260319144845@example.com'
enrollment_id = f'{email}#book-welcome-sequence'

# Set enrolled_at to 2 days ago
enrolled_at = (datetime.now() - timedelta(days=2)).isoformat()

enrollments_table.update_item(
    Key={'user_id': user_id, 'enrollment_id': enrollment_id},
    UpdateExpression='SET enrolled_at = :ts',
    ExpressionAttributeValues={':ts': enrolled_at}
)

print(f"Backdated {email} to {enrolled_at}")
print("Now run the drip processor to send Day 1 email")
