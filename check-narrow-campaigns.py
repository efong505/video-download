"""
Check campaigns in election-map-transition-sequence and general-newsletter-sequence
"""

import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('user-email-campaigns')

response = table.scan()
campaigns = response.get('Items', [])

# Filter the problematic groups
problem_groups = ['election-map-transition-sequence', 'general-newsletter-sequence']

for group in problem_groups:
    group_campaigns = [c for c in campaigns if c.get('campaign_group') == group]
    print(f"\n{'='*80}")
    print(f"Group: {group}")
    print(f"Count: {len(group_campaigns)}")
    print(f"{'='*80}\n")
    
    for c in sorted(group_campaigns, key=lambda x: x.get('sequence_number', 0)):
        name = c.get('campaign_name', 'Untitled')
        seq = c.get('sequence_number', '?')
        subject = c.get('subject', 'No subject')
        
        content_len = len(c.get('content', ''))
        html_len = len(c.get('html_content', ''))
        total_len = content_len + html_len
        
        print(f"#{seq} - {name}")
        print(f"  Subject: {subject}")
        print(f"  Content length: {content_len}")
        print(f"  HTML length: {html_len}")
        print(f"  Total: {total_len}")
        print()
