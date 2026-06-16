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

campaigns = response['Items']

print(f"\n=== Updating {len(campaigns)} campaigns ===")
for c in campaigns:
    campaign_id = c['campaign_id']
    seq = c.get('sequence_number', 0)
    
    # Set delay_hours = 0 for all campaigns
    campaigns_table.update_item(
        Key={'user_id': PLATFORM_OWNER_ID, 'campaign_id': campaign_id},
        UpdateExpression='SET delay_hours = :hours',
        ExpressionAttributeValues={':hours': 0}
    )
    print(f"✅ Updated campaign #{seq}: {c.get('campaign_name', 'N/A')} - set delay_hours=0")

print("\n✅ All campaigns updated")
