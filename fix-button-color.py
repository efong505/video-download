import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

campaigns_table = dynamodb.Table('user-email-campaigns')

# Get campaign #1
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
campaign_id = campaign['campaign_id']
html_content = campaign.get('html_content', '')

# Replace button with inline styles
old_button = '<a href="https://christianconservativestoday.com" class="button">Explore the Platform</a>'
new_button = '<a href="https://christianconservativestoday.com" style="display: inline-block; background: #2c5aa0; color: #ffffff !important; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold;">Explore the Platform</a>'

updated_html = html_content.replace(old_button, new_button)

if updated_html == html_content:
    print("❌ Button not found or already updated")
else:
    # Update campaign
    campaigns_table.update_item(
        Key={'user_id': PLATFORM_OWNER_ID, 'campaign_id': campaign_id},
        UpdateExpression='SET html_content = :html',
        ExpressionAttributeValues={':html': updated_html}
    )
    print(f"✅ Updated campaign #{campaign.get('sequence_number')}: {campaign.get('campaign_name')}")
    print(f"   Button now has inline styles with color: #ffffff !important")
