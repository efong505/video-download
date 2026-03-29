import boto3
from datetime import datetime
import json

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('user-email-events')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

response = table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

events = response['Items']

# Handle pagination
while 'LastEvaluatedKey' in response:
    response = table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID},
        ExclusiveStartKey=response['LastEvaluatedKey']
    )
    events.extend(response['Items'])

# Sort by timestamp descending
events.sort(key=lambda x: int(x.get('timestamp', 0)), reverse=True)

print(f"Found {len(events)} events\n")
print("Top 10 events with all fields:")
print("-" * 120)

for i, event in enumerate(events[:10], 1):
    print(f"\n{i}. Event fields:")
    for key, value in sorted(event.items()):
        if key == 'timestamp':
            ts = int(value)
            dt = datetime.fromtimestamp(ts)
            print(f"   {key}: {value} ({dt.strftime('%m/%d/%Y %I:%M:%S %p')})")
        else:
            print(f"   {key}: {value}")
