import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('newsletter_campaigns')

campaigns = [
    {'campaign_id': 'general', 'name': 'General', 'description': 'All subscribers', 'created_at': datetime.utcnow().isoformat()},
    {'campaign_id': 'election', 'name': 'Election Updates', 'description': 'Election news', 'created_at': datetime.utcnow().isoformat()},
    {'campaign_id': 'prayer', 'name': 'Prayer Requests', 'description': 'Prayer updates', 'created_at': datetime.utcnow().isoformat()},
    {'campaign_id': 'events', 'name': 'Events & Rallies', 'description': 'Event notifications', 'created_at': datetime.utcnow().isoformat()}
]

for campaign in campaigns:
    table.put_item(Item=campaign)
    print(f"Added: {campaign['name']}")

print("Done!")
