"""
Check pre-purchase campaign content
"""

import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('user-email-campaigns')

response = table.scan()
campaigns = response.get('Items', [])

# Filter pre-purchase campaigns
pre_purchase = [c for c in campaigns if c.get('campaign_group') == 'pre-purchase-book-sequence']
pre_purchase.sort(key=lambda x: x.get('sequence_number', 0))

print(f"Found {len(pre_purchase)} pre-purchase campaigns\n")

for c in pre_purchase:
    name = c.get('campaign_name', 'Untitled')
    seq = c.get('sequence_number', '?')
    has_html = 'html_content' in c and c['html_content']
    has_content = 'content' in c and c['content']
    
    print(f"#{seq} - {name}")
    print(f"  Has html_content: {has_html}")
    print(f"  Has content: {has_content}")
    
    if has_html:
        html_len = len(c['html_content'])
        print(f"  html_content length: {html_len} chars")
        if html_len < 100:
            print(f"  html_content: '{c['html_content']}'")
    
    if has_content:
        content_len = len(c['content'])
        print(f"  content length: {content_len} chars")
        if content_len < 100:
            print(f"  content: '{c['content']}'")
    
    if not has_html and not has_content:
        print(f"  ⚠️ NO CONTENT AT ALL!")
    
    print()
