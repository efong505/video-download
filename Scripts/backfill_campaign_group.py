"""Backfill existing campaigns with campaign_group field"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import boto3

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('user-email-campaigns')

USER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

campaign_ids = [
    '0ad371ae-7065-442f-831f-545a70d5c415',
    '3a3df4d2-119e-4905-84fc-cf73e597b670',
    '4e26dc60-d6e5-46b7-ac4d-96e904b2642a',
    '7ef7b6b6-3f5d-4d2e-97e1-4a41b138add7',
    'b4cdaae5-e33d-4dbf-b8bd-24d9afe910b7',
    'b514b0f5-7d31-4c56-9df6-261548fe4c65',
    'eb60f56c-d4e9-459d-9f3a-20ed48acf54e',
]

for cid in campaign_ids:
    table.update_item(
        Key={'user_id': USER_ID, 'campaign_id': cid},
        UpdateExpression='SET campaign_group = :cg',
        ExpressionAttributeValues={':cg': 'pre-purchase-book-sequence'}
    )
    print(f'Updated {cid}')

print('Backfill complete')
