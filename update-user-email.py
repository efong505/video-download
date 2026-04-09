import boto3
import os

os.environ['AWS_PROFILE'] = 'ekewaka'

db = boto3.resource('dynamodb', region_name='us-east-1')
table = db.Table('users')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Update email to your actual email
NEW_EMAIL = 'contact@christianconservativestoday.com'

table.update_item(
    Key={'user_id': PLATFORM_OWNER_ID},
    UpdateExpression='SET email = :email',
    ExpressionAttributeValues={':email': NEW_EMAIL}
)

print(f"Updated user email to: {NEW_EMAIL}")
print("This will now be used as the Reply-To address for all campaign emails")
