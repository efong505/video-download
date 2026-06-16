import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')

response = table.scan()
items = response['Items']

# Check for comprehensive vs basic summaries
comprehensive = []
basic = []

for item in items:
    state = item['state']
    content = item.get('content', item.get('summary', ''))
    length = len(content)
    
    # Check for template markers
    has_database = '## 📊 Database Summary' in content or '## Database Summary' in content
    has_landscape = '## 🔴' in content or 'POLITICAL LANDSCAPE' in content
    has_detailed = 'Faith:' in content or 'Voting Record:' in content
    
    if has_database and has_landscape and has_detailed and length > 12000:
        comprehensive.append((state, length))
    else:
        basic.append((state, length))

print("COMPREHENSIVE (Nebraska-style):")
for state, length in sorted(comprehensive, key=lambda x: x[1], reverse=True):
    print(f"  {state}: {length:,} chars")

print(f"\nBASIC (Need comprehensive content):")
for state, length in sorted(basic, key=lambda x: x[1], reverse=True):
    print(f"  {state}: {length:,} chars")
