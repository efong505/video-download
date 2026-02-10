import boto3
import json

db = boto3.resource('dynamodb')
table = db.Table('state-summaries')

summaries = table.scan()['Items']
print(f"Found {len(summaries)} summaries\n")

for s in summaries:
    print(f"State: {s.get('state')}")
    print(f"  title: {s.get('title', 'MISSING')}")
    print(f"  election_year: {s.get('election_year', 'MISSING')}")
    print(f"  content length: {len(s.get('content', ''))} chars")
    print()
