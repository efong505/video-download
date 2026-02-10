import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Count races
races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Mexico'}
)['Items']
print(f"Database Races: {len(races)}")

# Count candidates
candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Mexico'}
)['Items']
print(f"Database Candidates: {len(candidates)}")

# Get summary
summary = summaries_table.get_item(Key={'state': 'New Mexico'})['Item']
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
        print("\n✓ COUNTS MATCH - Summary is correct!")
    else:
        print(f"\n✗ MISMATCH - Summary needs update")
        print(f"  Database: {len(races)} races, {len(candidates)} candidates")
        print(f"  Summary: {summary_races} races, {summary_candidates} candidates")
else:
    print("\n✗ Could not find counts in summary")
