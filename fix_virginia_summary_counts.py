import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

state = 'Virginia'

print(f"Updating {state} summary counts...")

# Get current summary
summary = summaries_table.get_item(Key={'state': state})['Item']
content = summary['content']

# Update counts
content = content.replace('Total Races Documented:** 24', 'Total Races Documented:** 25')
content = content.replace('Total Candidates Profiled:** 20', 'Total Candidates Profiled:** 22')

# Save updated summary
summary['content'] = content
summaries_table.put_item(Item=summary)

print(f"[SUCCESS] Updated {state} summary:")
print(f"  Races: 24 -> 25")
print(f"  Candidates: 20 -> 22")
