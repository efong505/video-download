import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Get actual counts from database
races_response = races_table.scan(
    FilterExpression='#st = :state',
    ExpressionAttributeNames={'#st': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)
actual_races = len(races_response['Items'])

candidates_response = candidates_table.scan(
    FilterExpression='#st = :state',
    ExpressionAttributeNames={'#st': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)
actual_candidates = len(candidates_response['Items'])

print(f"Actual database counts:")
print(f"  Races: {actual_races}")
print(f"  Candidates: {actual_candidates}")

# Get current summary
summary_response = summaries_table.get_item(Key={'state': 'Pennsylvania'})
if 'Item' not in summary_response:
    print("ERROR: Pennsylvania summary not found!")
    exit(1)

current_summary = summary_response['Item']['content']

# Replace incorrect counts in summary text
updated_summary = current_summary.replace('**Total Races**: 341', f'**Total Races**: {actual_races}')
updated_summary = updated_summary.replace('**Total Candidates**: 119', f'**Total Candidates**: {actual_candidates}')
updated_summary = updated_summary.replace('**Total Candidates Profiled:** 119', f'**Total Candidates Profiled:** {actual_candidates}')

# Update summary in database
print(f"\nUpdating summary with correct counts...")
summaries_table.update_item(
    Key={'state': 'Pennsylvania'},
    UpdateExpression='SET content = :summary',
    ExpressionAttributeValues={':summary': updated_summary}
)

print("Summary updated successfully!")
print(f"  Races: 341 -> {actual_races}")
print(f"  Candidates: 119 -> {actual_candidates}")
