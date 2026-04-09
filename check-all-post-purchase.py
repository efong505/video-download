import boto3
import os
import html

os.environ['AWS_PROFILE'] = 'ekewaka'

db = boto3.resource('dynamodb', region_name='us-east-1')
table = db.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

resp = table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='campaign_group = :cg',
    ExpressionAttributeValues={
        ':uid': PLATFORM_OWNER_ID,
        ':cg': 'post-purchase-sequence'
    }
)

campaigns = sorted(resp['Items'], key=lambda x: int(x.get('sequence_number', 0)))

print('\n=== Checking for book-resources.html links ===\n')
for c in campaigns:
    seq = c['sequence_number']
    name = c.get('campaign_name', 'No name')
    html_content = c.get('html_content', '')
    
    # Decode HTML entities if present
    decoded = html.unescape(html_content)
    
    if 'book-resources' in decoded or 'book-resources' in html_content:
        print(f"Email #{seq}: {name}")
        print(f"  Campaign ID: {c['campaign_id']}")
        print(f"  HAS book-resources.html link")
        print()
