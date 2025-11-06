import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

state = 'New Jersey'

# Count races
races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': state}
)['Items']
print(f"Database Races: {len(races)}")

# Count candidates
candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': state}
)['Items']
print(f"Database Candidates: {len(candidates)}")

# Get summary
try:
    summary = summaries_table.get_item(Key={'state': state})['Item']
    content = summary['content']
    
    # Extract counts from summary
    import re
    race_match = re.search(r'Total Races Documented:\*\* (\d+)', content)
    candidate_match = re.search(r'Total Candidates Profiled:\*\* (\d+)', content)
    
    if race_match and candidate_match:
        summary_races = int(race_match.group(1))
        summary_candidates = int(candidate_match.group(1))
        print(f"\nSummary Races: {summary_races}")
        print(f"Summary Candidates: {summary_candidates}")
        
        if len(races) == summary_races and len(candidates) == summary_candidates:
            print("\nCOUNTS MATCH!")
        else:
            print(f"\nMISMATCH:")
            print(f"  Database has: {len(races)} races, {len(candidates)} candidates")
            print(f"  Summary says: {summary_races} races, {summary_candidates} candidates")
            print(f"  Difference: {len(races) - summary_races} races, {len(candidates) - summary_candidates} candidates")
    else:
        print("\nCould not find counts in summary")
except Exception as e:
    print(f"\nError: {e}")
