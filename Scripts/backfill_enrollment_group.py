"""Backfill existing drip enrollments with campaign_group field"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import boto3

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('user-email-drip-enrollments')

USER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

response = table.scan()
items = response['Items']

for item in items:
    table.update_item(
        Key={'user_id': item['user_id'], 'enrollment_id': item['enrollment_id']},
        UpdateExpression='SET campaign_group = :cg',
        ExpressionAttributeValues={':cg': 'pre-purchase-book-sequence'}
    )
    print(f"Updated enrollment: {item['enrollment_id']}")

print(f'Backfill complete - {len(items)} enrollments updated')
