import boto3, uuid
from datetime import datetime

db = boto3.resource('dynamodb')
table = db.Table('state-summaries')

with open('Voter Guides_Summaries/california_summary_guide.md', encoding='utf-8') as f:
    content = f.read()

table.put_item(Item={
    'summary_id': str(uuid.uuid4()),
    'state': 'California',
    'content': content,
    'created_at': datetime.utcnow().isoformat(),
    'updated_at': datetime.utcnow().isoformat(),
    'created_by': 'super@admin.com',
    'status': 'published'
})

print(f"OK: California summary ({len(content)} chars)")
