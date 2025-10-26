import boto3
import re

dynamodb = boto3.resource('dynamodb')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

def get_all_states_with_summaries():
    """Get all states that have summaries in DynamoDB"""
    response = summaries_table.scan()
    states = [item['state'] for item in response['Items']]
    while 'LastEvaluatedKey' in response:
        response = summaries_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        states.extend([item['state'] for item in response['Items']])
    return sorted(states)

def get_actual_counts(state):
    """Get actual race and candidate counts"""
    races_response = races_table.scan(
        FilterExpression='#s = :state',
        ExpressionAttributeNames={'#s': 'state'},
        ExpressionAttributeValues={':state': state}
    )
    races = races_response['Items']
    while 'LastEvaluatedKey' in races_response:
        races_response = races_table.scan(
            FilterExpression='#s = :state',
            ExpressionAttributeNames={'#s': 'state'},
            ExpressionAttributeValues={':state': state},
            ExclusiveStartKey=races_response['LastEvaluatedKey']
        )
        races.extend(races_response['Items'])
    
    candidates_response = candidates_table.scan(
        FilterExpression='#s = :state',
        ExpressionAttributeNames={'#s': 'state'},
        ExpressionAttributeValues={':state': state}
    )
    candidates = candidates_response['Items']
    while 'LastEvaluatedKey' in candidates_response:
        candidates_response = candidates_table.scan(
            FilterExpression='#s = :state',
            ExpressionAttributeNames={'#s': 'state'},
            ExpressionAttributeValues={':state': state},
            ExclusiveStartKey=candidates_response['LastEvaluatedKey']
        )
        candidates.extend(candidates_response['Items'])
    
    return len(races), len(candidates)

def fix_summary(state, actual_races, actual_candidates):
    """Update summary with correct counts"""
    try:
        response = summaries_table.get_item(Key={'state': state})
        if 'Item' not in response:
            return False, "No summary found"
        
        summary = response['Item']
        content = summary['content']
        original_content = content
        
        # Multiple patterns to catch all variations (including without asterisks)
        patterns = [
            (r'(\*\*Total Races Documented:\*\*\s+)\d+\+?', f'\\g<1>{actual_races}'),
            (r'(Total Races Documented:\s+)\d+\+?', f'\\g<1>{actual_races}'),
            (r'(\*\*Total Races:\*\*\s+)\d+\+?', f'\\g<1>{actual_races}'),
            (r'(-\s+\*\*Total Races\*\*:\s+)\d+\+?', f'\\g<1>{actual_races}'),
            (r'(\*\*Total Candidates Profiled:\*\*\s+)\d+\+?', f'\\g<1>{actual_candidates}'),
            (r'(Total Candidates Profiled:\s+)\d+\+?', f'\\g<1>{actual_candidates}'),
            (r'(\*\*Total Candidates:\*\*\s+)\d+\+?', f'\\g<1>{actual_candidates}'),
        ]
        
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        if content == original_content:
            return False, "No changes needed"
        
        summary['content'] = content
        summaries_table.put_item(Item=summary)
        return True, "Updated"
        
    except Exception as e:
        return False, str(e)

print("\n" + "="*80)
print("FIXING ALL STATE SUMMARIES IN DYNAMODB")
print("="*80 + "\n")

states = get_all_states_with_summaries()
print(f"Found {len(states)} states with summaries\n")

updated = 0
skipped = 0

for state in states:
    actual_races, actual_candidates = get_actual_counts(state)
    success, message = fix_summary(state, actual_races, actual_candidates)
    
    if success:
        print(f"[OK] {state}: {actual_races} races, {actual_candidates} candidates - {message}")
        updated += 1
    else:
        print(f"  {state}: {actual_races} races, {actual_candidates} candidates - {message}")
        skipped += 1

print(f"\n{'='*80}")
print(f"Updated: {updated} states")
print(f"Skipped: {skipped} states")
print(f"{'='*80}\n")
