import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

campaigns_table = dynamodb.Table('user-email-campaigns')
response = campaigns_table.get_item(
    Key={'user_id': PLATFORM_OWNER_ID, 'campaign_id': '68264b18-8e5a-4c6e-9f3a-2e1d4c5b6a7f'}
)

if 'Item' not in response:
    # Try querying for sequence #1
    response = campaigns_table.query(
        KeyConditionExpression='user_id = :uid',
        FilterExpression='campaign_group = :cg AND sequence_number = :seq',
        ExpressionAttributeValues={
            ':uid': PLATFORM_OWNER_ID,
            ':cg': 'general-newsletter-sequence',
            ':seq': 1
        }
    )
    if response['Items']:
        campaign = response['Items'][0]
    else:
        print("Campaign not found")
        sys.exit(1)
else:
    campaign = response['Item']

html_content = campaign.get('html_content', '')

# Find button HTML
import re
button_matches = re.findall(r'<a[^>]*style="[^"]*"[^>]*>.*?</a>', html_content, re.DOTALL)

print(f"\n=== Campaign: {campaign.get('campaign_name')} ===")
print(f"\nFound {len(button_matches)} button/link elements\n")

for i, match in enumerate(button_matches, 1):
    if 'padding' in match or 'background' in match:  # Likely a button
        print(f"Button {i}:")
        print(match[:500])
        print("\n")
