import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')

# Map filenames to state names
file_to_state = {
    'alaska.md': 'Alaska',
    'florida.md': 'Florida',
    'georgia.md': 'Georgia',
    'hawaii.md': 'Hawaii',
    'nebraska.md': 'Nebraska',
    'newhampshire.md': 'New Hampshire',
    'northcarolina.md': 'North Carolina',
    'pennsylvania.md': 'Pennsylvania',
    'Southcarolina.md': 'South Carolina',
    'texas.md': 'Texas',
    'virginia.md': 'Virginia',
    'west virginia.md': 'West Virginia'
}

guides_dir = r'c:\Users\Ed\Documents\Programming\AWS\Downloader\Election Data and Files\Voter Guides_Summaries\UpdatedGuides'

uploaded = []
errors = []

for filename, state in file_to_state.items():
    filepath = os.path.join(guides_dir, filename)
    
    if not os.path.exists(filepath):
        errors.append(f"{state}: File not found")
        continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title from first line
        first_line = content.split('\n')[0].strip('# ')
        title = first_line if first_line else f"{state} 2025-2026 Elections - Complete Christian Conservatives Today Guide"
        
        table.update_item(
            Key={'state': state},
            UpdateExpression='SET #content = :content, #updated = :updated, #title = :title',
            ExpressionAttributeNames={'#content': 'content', '#updated': 'updated_at', '#title': 'title'},
            ExpressionAttributeValues={
                ':content': content,
                ':updated': datetime.now().isoformat(),
                ':title': title
            }
        )
        
        uploaded.append(f"{state}: {len(content):,} chars")
    except Exception as e:
        errors.append(f"{state}: {str(e)}")

print("UPLOADED:")
for item in uploaded:
    print(f"  {item}")

if errors:
    print("\nERRORS:")
    for error in errors:
        print(f"  {error}")

print(f"\nTotal: {len(uploaded)} uploaded, {len(errors)} errors")
