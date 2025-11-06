import boto3, uuid
from datetime import datetime

db = boto3.resource('dynamodb')
table = db.Table('state-summaries')

with open('Election Data and Files/Voter Guides_Summaries/new_mexico_summary_guide.md', encoding='utf-8') as f:
    content = f.read()

table.put_item(Item={
    'state': 'New Mexico',
    'title': 'New Mexico 2025-2026 Elections - Complete Christian Conservatives Today Guide',
    'election_year': '2025-2026',
    'content': content,
    'created_at': datetime.utcnow().isoformat(),
    'updated_at': datetime.utcnow().isoformat(),
    'created_by': 'super@admin.com',
    'status': 'published'
})

print(f"OK: New Mexico summary uploaded ({len(content)} chars)")
