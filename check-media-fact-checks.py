"""
Check media category fact-checks
"""

import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('fact-checks')

response = table.scan()
items = response.get('Items', [])

# Filter media category
media_items = [item for item in items if item.get('category', '').lower() == 'media']

print(f"Found {len(media_items)} fact-checks in Media category\n")

for item in media_items:
    print(f"Claim: {item.get('claim', 'N/A')}")
    print(f"Verdict: {item.get('verdict', 'N/A')}")
    print(f"Category: {item.get('category', 'N/A')}")
    print(f"Created: {item.get('created_at', 'N/A')}")
    print()
