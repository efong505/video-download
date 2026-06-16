import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

campaigns_table = dynamodb.Table('user-email-campaigns')
response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='campaign_group = :cg',
    ExpressionAttributeValues={
        ':uid': PLATFORM_OWNER_ID,
        ':cg': 'general-newsletter-sequence'
    }
)

campaigns = sorted(response['Items'], key=lambda x: x.get('sequence_number', 0))

print(f"\n=== Checking content in {len(campaigns)} campaigns ===\n")

for c in campaigns:
    seq = c.get('sequence_number', 0)
    name = c.get('campaign_name', 'N/A')
    
    content = c.get('content', '')
    html_content = c.get('html_content', '')
    
    print(f"Campaign #{seq}: {name}")
    print(f"  content field: {len(content)} chars")
    print(f"  html_content field: {len(html_content)} chars")
    
    if not content and not html_content:
        print(f"  ❌ NO CONTENT IN EITHER FIELD!")
    elif html_content:
        print(f"  ✅ Has html_content")
    elif content:
        print(f"  ✅ Has content")
    print()
