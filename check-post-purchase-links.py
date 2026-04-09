import boto3
import os
import json

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

print('\n=== POST-PURCHASE CAMPAIGNS ===\n')
for c in campaigns:
    print(f"Email #{c['sequence_number']}: {c.get('campaign_name', c.get('subject', 'No name'))}")
    print(f"Subject: {c.get('subject', 'N/A')}")
    print(f"Campaign ID: {c['campaign_id']}")
    
    # Check for book-resources links
    html = c.get('html_content', '')
    if 'book-resources' in html:
        print("⚠️  CONTAINS book-resources.html link")
        # Find the link
        import re
        links = re.findall(r'href="([^"]*book-resources[^"]*)"', html)
        for link in links:
            print(f"   Link: {link}")
    print()
