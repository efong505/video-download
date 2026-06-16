import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

response = summaries_table.get_item(Key={'state': 'Pennsylvania'})
if 'Item' in response:
    content = response['Item']['content']
    print(f"Pennsylvania Summary Length: {len(content)} chars")
    print(f"\nTemplate Compliance Check:")
    print(f"  Has 'Database Summary': {'Database Summary' in content or '📊 Database Summary' in content}")
    print(f"  Has 'POLITICAL LANDSCAPE': {'POLITICAL LANDSCAPE' in content}")
    print(f"  Has 'CHURCH MOBILIZATION': {'CHURCH MOBILIZATION' in content}")
    print(f"  Has 'BOTTOM LINE': {'BOTTOM LINE' in content}")
    print(f"  Has 'PRAYER POINTS': {'PRAYER POINTS' in content}")
    print(f"  Has 'What Pastors Can Do': {'What Pastors Can Do' in content}")
    print(f"  Has 'If Conservatives Win': {'If Conservatives Win' in content}")
    print(f"  Has 'If Progressives Win': {'If Progressives Win' in content}")
    
    # Show first 500 chars
    print(f"\nFirst 500 characters:")
    print(content[:500])
else:
    print("Pennsylvania summary not found")
