import boto3
import sys

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Get state from command line argument
if len(sys.argv) < 2:
    print("Usage: python auto_fix_summary_counts.py <state_name>")
    print("Example: python auto_fix_summary_counts.py 'New Jersey'")
    sys.exit(1)

state = sys.argv[1]

print(f"Auto-fixing summary counts for {state}...")

# Count actual database records
races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': state}
)['Items']
actual_races = len(races)

candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': state}
)['Items']
actual_candidates = len(candidates)

print(f"Database has: {actual_races} races, {actual_candidates} candidates")

# Get summary and extract current counts
try:
    summary = summaries_table.get_item(Key={'state': state})['Item']
    content = summary['content']
    
    import re
    race_match = re.search(r'Total Races Documented:\*\* (\d+)', content)
    candidate_match = re.search(r'Total Candidates Profiled:\*\* (\d+)', content)
    
    if race_match and candidate_match:
        old_races = int(race_match.group(1))
        old_candidates = int(candidate_match.group(1))
        print(f"Summary says: {old_races} races, {old_candidates} candidates")
        
        if old_races == actual_races and old_candidates == actual_candidates:
            print(f"\nCounts already match - no update needed!")
        else:
            # Update counts
            content = re.sub(r'Total Races Documented:\*\* \d+', f'Total Races Documented:** {actual_races}', content)
            content = re.sub(r'Total Candidates Profiled:\*\* \d+', f'Total Candidates Profiled:** {actual_candidates}', content)
            
            summary['content'] = content
            summaries_table.put_item(Item=summary)
            
            print(f"\n[SUCCESS] Updated summary:")
            print(f"  Races: {old_races} -> {actual_races}")
            print(f"  Candidates: {old_candidates} -> {actual_candidates}")
    else:
        print("\nError: Could not find count fields in summary")
except Exception as e:
    print(f"\nError: {e}")
