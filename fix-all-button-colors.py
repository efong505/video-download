import boto3
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

campaigns_table = dynamodb.Table('user-email-campaigns')

# Get all campaigns in general-newsletter-sequence
response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='campaign_group = :cg',
    ExpressionAttributeValues={
        ':uid': PLATFORM_OWNER_ID,
        ':cg': 'general-newsletter-sequence'
    }
)

campaigns = sorted(response['Items'], key=lambda x: x.get('sequence_number', 0))

print(f"\n=== Fixing buttons in {len(campaigns)} campaigns ===\n")

for campaign in campaigns:
    campaign_id = campaign['campaign_id']
    seq = campaign.get('sequence_number', 0)
    name = campaign.get('campaign_name', 'N/A')
    html_content = campaign.get('html_content', '')
    
    # Find all buttons with class="button"
    pattern = r'<a href="([^"]+)" class="button">([^<]+)</a>'
    matches = re.findall(pattern, html_content)
    
    if matches:
        updated_html = html_content
        for url, text in matches:
            old = f'<a href="{url}" class="button">{text}</a>'
            new = f'<a href="{url}" style="display: inline-block; background: #2c5aa0; color: #ffffff !important; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold;">{text}</a>'
            updated_html = updated_html.replace(old, new)
        
        if updated_html != html_content:
            campaigns_table.update_item(
                Key={'user_id': PLATFORM_OWNER_ID, 'campaign_id': campaign_id},
                UpdateExpression='SET html_content = :html',
                ExpressionAttributeValues={':html': updated_html}
            )
            print(f"✅ Campaign #{seq}: {name}")
            print(f"   Fixed {len(matches)} button(s)")
        else:
            print(f"⚠️  Campaign #{seq}: {name} - No changes needed")
    else:
        print(f"ℹ️  Campaign #{seq}: {name} - No buttons found")

print("\n✅ All campaigns checked and updated")
