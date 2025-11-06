import boto3

db = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = db.Table('state-summaries')

# Get current summary
response = summaries_table.get_item(Key={'state': 'New Mexico'})
summary = response['Item']

# Update the counts in the content
content = summary['content']
content = content.replace('**Total Races Documented:** 20', '**Total Races Documented:** 30')
content = content.replace('**Total Candidates Profiled:** 26', '**Total Candidates Profiled:** 38')

# Save updated summary
summary['content'] = content
summaries_table.put_item(Item=summary)

print("Updated New Mexico summary:")
print("   Total Races: 20 -> 30")
print("   Total Candidates: 26 -> 38")
