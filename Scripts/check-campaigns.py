import boto3
import json

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

response = table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

campaigns = response['Items']
transition_campaigns = [c for c in campaigns if 'election-map-transition' in c.get('campaign_group', '')]

print(f"Found {len(transition_campaigns)} transition campaigns\n")

for c in sorted(transition_campaigns, key=lambda x: x.get('sequence_number', 0)):
    print(f"Campaign: {c.get('campaign_name', 'NO NAME')}")
    print(f"  Campaign ID: {c.get('campaign_id', 'NO ID')}")
    print(f"  Group: {c.get('campaign_group', 'NO GROUP')}")
    print(f"  Sequence: {c.get('sequence_number', 'NO SEQ')}")
    print(f"  Subject: {c.get('subject', 'NO SUBJECT')}")
    print(f"  HTML Content Length: {len(c.get('html_content', ''))}")
    print(f"  Has HTML: {'YES' if c.get('html_content') else 'NO'}")
    print()
