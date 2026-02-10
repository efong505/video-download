import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
summaries_table = dynamodb.Table('state-summaries')

summaries = [
    {
        'state': 'Virginia',
        'file': 'Voter Guides_Summaries/virginia_summary_guide.md'
    },
    {
        'state': 'Texas',
        'file': 'Voter Guides_Summaries/texas_summary_guide.md'
    }
]

for summary in summaries:
    with open(summary['file'], 'r', encoding='utf-8') as f:
        content = f.read()
    
    item = {
        'summary_id': str(uuid.uuid4()),
        'state': summary['state'],
        'content': content,
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'created_by': 'super@admin.com',
        'status': 'published'
    }
    
    try:
        summaries_table.put_item(Item=item)
        print(f"OK: Uploaded {summary['state']} summary ({len(content)} chars)")
    except Exception as e:
        print(f"FAIL: {summary['state']} - {str(e)}")

print("\nUpload complete!")
