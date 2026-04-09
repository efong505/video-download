import boto3
import os

os.environ['AWS_PROFILE'] = 'ekewaka'

db = boto3.resource('dynamodb', region_name='us-east-1')
table = db.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Get email #2
resp = table.get_item(
    Key={
        'user_id': PLATFORM_OWNER_ID,
        'campaign_id': '2b8d8840-25c7-4de1-b9d3-3aca442241da'
    }
)

campaign = resp['Item']
print(f"Email #2: {campaign.get('campaign_name')}")
print(f"Subject: {campaign.get('subject')}")
print("\n=== HTML CONTENT ===\n")
print(campaign.get('html_content', 'No content'))
