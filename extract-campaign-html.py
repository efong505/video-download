import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

campaigns_table = dynamodb.Table('user-email-campaigns')
response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='campaign_group = :cg AND sequence_number = :seq',
    ExpressionAttributeValues={
        ':uid': PLATFORM_OWNER_ID,
        ':cg': 'general-newsletter-sequence',
        ':seq': 1
    }
)

campaign = response['Items'][0]
html_content = campaign.get('html_content', '')

# Save to file
with open('campaign1-html.txt', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Saved HTML content to campaign1-html.txt ({len(html_content)} chars)")

# Find button sections
import re
button_sections = re.findall(r'<a[^>]+href[^>]*>.*?</a>', html_content, re.DOTALL | re.IGNORECASE)
print(f"\nFound {len(button_sections)} <a> tags")

for i, section in enumerate(button_sections, 1):
    if len(section) < 200:  # Short links are likely buttons
        print(f"\nLink {i}:")
        print(section)
