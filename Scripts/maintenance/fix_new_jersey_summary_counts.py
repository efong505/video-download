import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

state = 'New Jersey'

print(f"Updating {state} summary counts...")

# Get current summary
summary = summaries_table.get_item(Key={'state': state})['Item']
content = summary['content']

# Update counts to match actual database
content = content.replace('Total Races Documented:** 50', 'Total Races Documented:** 56')
content = content.replace('Total Candidates Profiled:** 50', 'Total Candidates Profiled:** 7')

# Save updated summary
summary['content'] = content
summaries_table.put_item(Item=summary)

print(f"[SUCCESS] Updated {state} summary:")
print(f"  Races: 50 -> 56")
print(f"  Candidates: 50 -> 7")
print(f"\nNOTE: Only 7 candidates were generated. You may want to regenerate with more candidates.")
