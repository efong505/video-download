import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

for state in ['Florida', 'California']:
    response = summaries_table.scan(FilterExpression=Attr('state').eq(state))
    if response['Items']:
        summary = response['Items'][0]
        content = summary.get('summary', '')
        print(f"\n{'='*60}")
        print(f"{state} Summary: {len(content)} characters")
        print('='*60)
        
        # Check for Senate mentions
        if 'Senate' in content or 'Senator' in content:
            print("⚠️ WARNING: Contains Senate references")
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'Senate' in line or 'Senator' in line:
                    print(f"  Line {i}: {line[:100]}")
        else:
            print("✓ No Senate references found")
        
        # Check for key info
        if 'term-limited' in content.lower() or 'open seat' in content.lower():
            print("✓ Mentions term-limited/open seat")
        
        print(f"\nFirst 300 chars:\n{content[:300]}")
    else:
        print(f"\n{state}: NO SUMMARY FOUND")
