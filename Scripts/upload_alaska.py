import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')

with open(r'c:\Users\Ed\Documents\Programming\AWS\Downloader\Election Data and Files\Voter Guides_Summaries\UpdatedGuides\alaska.md', 'r', encoding='utf-8') as f:
    content = f.read()

table.update_item(
    Key={'state': 'Alaska'},
    UpdateExpression='SET #content = :content, #updated = :updated, #title = :title',
    ExpressionAttributeNames={'#content': 'content', '#updated': 'updated_at', '#title': 'title'},
    ExpressionAttributeValues={
        ':content': content,
        ':updated': datetime.now().isoformat(),
        ':title': 'Alaska 2025-2026 Elections - Complete Christian Conservatives Today Guide'
    }
)

print(f"Alaska uploaded: {len(content):,} chars")
