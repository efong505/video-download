import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

state = 'New Jersey'

print(f"Fixing {state} summary counts to match database...")

# Get current summary
summary = summaries_table.get_item(Key={'state': state})['Item']
content = summary['content']

# Update counts to match actual database (80 races, 6 candidates)
import re
content = re.sub(r'Total Races Documented:\*\* \d+', 'Total Races Documented:** 80', content)
content = re.sub(r'Total Candidates Profiled:\*\* \d+', 'Total Candidates Profiled:** 6', content)

# Save updated summary
summary['content'] = content
summaries_table.put_item(Item=summary)

print(f"[SUCCESS] Updated {state} summary:")
print(f"  Races: 78 -> 80")
print(f"  Candidates: 186 -> 6")
print(f"\nWARNING: Only 6 candidates for 80 races is inadequate!")
print(f"You need to regenerate with 160+ candidates (2 per race minimum)")
