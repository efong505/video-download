import boto3
import os

os.environ['AWS_PROFILE'] = 'ekewaka'

db = boto3.resource('dynamodb', region_name='us-east-1')
table = db.Table('users')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

resp = table.get_item(Key={'user_id': PLATFORM_OWNER_ID})

if 'Item' in resp:
    user = resp['Item']
    print(f"User ID: {user['user_id']}")
    print(f"Email: {user.get('email', 'NOT SET')}")
    print(f"Username: {user.get('username', 'NOT SET')}")
else:
    print("User not found")
