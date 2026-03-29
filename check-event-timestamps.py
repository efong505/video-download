import boto3
from datetime import datetime

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
print("Top 30 events sorted by timestamp:")
print("-" * 120)

for i, event in enumerate(events[:30], 1):
    ts = int(event.get('timestamp', 0))
    dt = datetime.fromtimestamp(ts)
    email = event.get('email', 'N/A')
    event_type = event.get('event_type', 'N/A')
    campaign_name = event.get('campaign_name', 'N/A')
    
    print(f"{i:2}. {dt.strftime('%m/%d/%Y %I:%M:%S %p')} | TS: {ts} | {email:35} | {event_type:8} | {campaign_name}")
