import boto3
import re

db = boto3.resource('dynamodb', region_name='us-east-1')
table = db.Table('state-summaries')

def convert_nc_to_markdown(content):
    # Add proper markdown structure
    lines = content.split('\n')
    formatted = []
    
    for i, line in enumerate(lines):
        # Main section headers
        if line.strip() in ['State-Specific Context', 'Key Races and Candidate Profiles', "What's At Stake", 'Church Mobilization', 'Extended Prayer Points (with Scriptures)', 'Detailed Resources']:
            formatted.append(f'\n## 🔴 {line.strip()}\n')
        # Subsection headers
        elif line.strip().startswith('U.S. Senate') or line.strip().startswith('Governor') or line.strip().startswith('AG (') or line.strip().startswith('Sec State') or line.strip().startswith('Supreme Court') or line.strip().startswith('U.S. House') or line.strip().startswith('Charlotte Mayor'):
            formatted.append(f'\n### {line.strip()}\n')
        # Candidate names
        elif line.strip() in ['Roy Cooper', 'Michael Whatley (Leading)', 'Democratic Candidates:', 'Republican Candidates (7 Declared):']:
            formatted.append(f'\n**{line.strip()}**\n')
        # Field labels
        elif line.strip().startswith('Faith:') or line.strip().startswith('Bio:') or line.strip().startswith('Voting Record:') or line.strip().startswith('Endorsements:') or line.strip().startswith('Positions:') or line.strip().startswith('Christian Conservative Analysis:'):
            formatted.append(f'\n**{line.strip()}**\n')
        # Prayer points
        elif line.strip().startswith('For ') or line.strip().startswith('Pro-Life:') or line.strip().startswith('School Choice:'):
            formatted.append(f'- **{line.strip()}**')
        else:
            formatted.append(line)
    
    return '\n'.join(formatted)

# Get NC summary
response = table.get_item(Key={'state': 'North Carolina'})
nc_content = response['Item']['content']

# Convert to markdown
nc_markdown = convert_nc_to_markdown(nc_content)

# Upload
table.put_item(Item={
    'state': 'North Carolina',
    'title': 'North Carolina 2026 Voter Guide',
    'content': nc_markdown,
    'updated_at': '2025-01-22'
})

print(f"NC converted: {len(nc_markdown):,} chars")
