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

print(f"\n=== Checking {len(campaigns)} campaigns for book mentions ===\n")

book_keywords = ['book', 'ai', 'artificial intelligence', 'survival kit', 'necessary evil']

for campaign in campaigns:
    seq = campaign.get('sequence_number', 0)
    name = campaign.get('campaign_name', 'N/A')
    subject = campaign.get('subject', 'N/A')
    html_content = campaign.get('html_content', '').lower()
    
    mentions = [kw for kw in book_keywords if kw in html_content]
    
    print(f"Campaign #{seq}: {name}")
    print(f"  Subject: {subject}")
    if mentions:
        print(f"  ✅ Mentions: {', '.join(mentions)}")
    else:
        print(f"  ❌ No book mentions")
    print()
