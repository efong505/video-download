"""
Check campaign content in database
"""

import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('user-email-campaigns')

response = table.scan()
campaigns = response.get('Items', [])

print(f"Found {len(campaigns)} campaigns\n")

for c in campaigns:
    name = c.get('campaign_name', 'Untitled')
    group = c.get('campaign_group', 'N/A')
    has_html = 'html_content' in c and c['html_content']
    has_content = 'content' in c and c['content']
    
    print(f"Campaign: {name}")
    print(f"  Group: {group}")
    print(f"  Has html_content: {has_html}")
    print(f"  Has content: {has_content}")
    
    if has_html:
        print(f"  html_content length: {len(c['html_content'])} chars")
        print(f"  Preview: {c['html_content'][:100]}...")
    elif has_content:
        print(f"  content length: {len(c['content'])} chars")
        print(f"  Preview: {c['content'][:100]}...")
    else:
        print(f"  ⚠️ NO CONTENT!")
    print()
