import boto3, sys
sys.stdout.reconfigure(encoding='utf-8')
session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
ddb = session.resource('dynamodb')
table = ddb.Table('user-email-campaigns')

# Fix missing names
fixes = {
    '7ef7b6b6-3f5d-4d2e-97e1-4a41b138add7': 'Pre-Purchase #5 - Final Push',
    '4e26dc60-c8f8-4e5e-8e5e-8e5e8e5e8e5e': 'Pre-Purchase #6 - Last Chance',
    'eb60f56c-d4e9-459d-9f3a-20ed48acf54e': 'Pre-Purchase #0 - Welcome (DELETE THIS)'
}

for campaign_id, name in fixes.items():
    try:
        table.update_item(
            Key={'user_id': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2', 'campaign_id': campaign_id},
            UpdateExpression='SET campaign_name = :name',
            ExpressionAttributeValues={':name': name}
        )
        print(f"Updated {campaign_id[:8]}... → {name}")
    except Exception as e:
        print(f"Error updating {campaign_id}: {e}")
