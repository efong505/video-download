"""
Find campaigns with missing content
"""

import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('user-email-campaigns')

response = table.scan()
campaigns = response.get('Items', [])

print(f"Checking {len(campaigns)} campaigns for missing content...\n")

missing = []
for c in campaigns:
    name = c.get('campaign_name', 'Untitled')
    has_html = 'html_content' in c and c['html_content']
    has_content = 'content' in c and c['content']
    
    if not has_html and not has_content:
        missing.append(c)
        print(f"❌ NO CONTENT: {name}")
        print(f"   Campaign ID: {c.get('campaign_id')}")
        print(f"   Group: {c.get('campaign_group', 'N/A')}")
        print()

print(f"\nTotal campaigns with missing content: {len(missing)}")
