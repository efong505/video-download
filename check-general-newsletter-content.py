import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Get all campaigns
response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
)

campaigns = response['Items']

# Find general-newsletter-sequence campaigns
general_campaigns = [c for c in campaigns if c.get('campaign_group') == 'general-newsletter-sequence']

# Sort by step_number
general_campaigns.sort(key=lambda x: int(x.get('step_number', 0)))

print(f"Found {len(general_campaigns)} general-newsletter-sequence campaigns\n")

# Show each campaign
for i, campaign in enumerate(general_campaigns, 1):
    print("=" * 80)
    print(f"CAMPAIGN #{i} - {campaign.get('campaign_name')}")
    print("=" * 80)
    print(f"Campaign ID: {campaign.get('campaign_id')}")
    print(f"Step: {campaign.get('step_number')}/{len(general_campaigns)}")
    print(f"Subject: {campaign.get('subject')}")
    print(f"Delay: {campaign.get('delay_days')} days")
    
    # Check for content
    html_content = campaign.get('html_content', '')
    content = campaign.get('content', '')
    
    print(f"\nHTML Content Length: {len(html_content)} characters")
    print(f"Content Length: {len(content)} characters")
    
    if html_content:
        print("\n" + "-" * 80)
        print("HTML CONTENT (first 500 chars):")
        print("-" * 80)
        print(html_content[:500])
        print("...")
    elif content:
        print("\n" + "-" * 80)
        print("CONTENT (first 500 chars):")
        print("-" * 80)
        print(content[:500])
        print("...")
    else:
        print("\n⚠️ WARNING: NO CONTENT FOUND!")
    
    print("\n")
