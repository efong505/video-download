import boto3
import sys
import re

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

for campaign in campaigns:
    seq = campaign.get('sequence_number', 0)
    if seq in [4, 5]:
        name = campaign.get('campaign_name', 'N/A')
        html_content = campaign.get('html_content', '')
        
        print(f"\n{'='*60}")
        print(f"Campaign #{seq}: {name}")
        print('='*60)
        
        # Extract text content (remove HTML tags for readability)
        text = re.sub(r'<[^>]+>', ' ', html_content)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Find sentences with "book" or "AI"
        sentences = text.split('.')
        for sentence in sentences:
            if 'book' in sentence.lower() or 'ai' in sentence.lower():
                print(sentence.strip() + '.')
