import boto3
import re

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

# Get current summary
response = summaries_table.get_item(Key={'state': 'New Jersey'})
summary = response['Item']

content = summary['content']

# Fix the counts in the summary text
content = re.sub(r'\b41\s+races?\b', '151 races', content, flags=re.IGNORECASE)
content = re.sub(r'\b102\s+candidates?\b', '150 candidates', content, flags=re.IGNORECASE)

# Update the summary
summary['content'] = content
summaries_table.put_item(Item=summary)

print("Fixed summary counts:")
print("  41 races -> 151 races")
print("  102 candidates -> 150 candidates")
print("\nSummary updated successfully!")
