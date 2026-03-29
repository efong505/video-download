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

# Find election-map-transition-sequence campaigns
election_campaigns = [c for c in campaigns if c.get('campaign_group') == 'election-map-transition-sequence']

# Sort by step_number
election_campaigns.sort(key=lambda x: int(x.get('step_number', 0)))

print(f"Found {len(election_campaigns)} election-map-transition-sequence campaigns\n")

# Show campaign #1
if election_campaigns:
    campaign1 = election_campaigns[0]
    print("=" * 80)
    print("CAMPAIGN #1 - Transition #1 - Welcome Back")
    print("=" * 80)
    print(f"Campaign ID: {campaign1.get('campaign_id')}")
    print(f"Step: {campaign1.get('step_number')}/7")
    print(f"Subject: {campaign1.get('subject')}")
    print(f"\nHTML Content Length: {len(campaign1.get('html_content', ''))} characters")
    print("\n" + "-" * 80)
    print("HTML CONTENT:")
    print("-" * 80)
    print(campaign1.get('html_content', ''))
