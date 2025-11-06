import boto3
import re

dynamodb = boto3.resource('dynamodb')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# States with discrepancies from audit
STATES_TO_FIX = ['California', 'Florida', 'Georgia', 'Ohio', 'Texas', 'Virginia']

def get_actual_counts(state):
    """Get actual race and candidate counts from DynamoDB"""
    # Get races
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
    
    # Get candidates
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

def fix_summary_counts(state, actual_races, actual_candidates):
    """Update summary in DynamoDB with correct counts"""
    try:
        # Get existing summary
        response = summaries_table.get_item(Key={'state': state})
        if 'Item' not in response:
            print(f"  [SKIP] No summary found in DynamoDB for {state}")
            return False
        
        summary = response['Item']
        content = summary['content']
        
        # Pattern 1: "Total Races Documented: X races"
        content = re.sub(
            r'(\*\*Total Races Documented:\*\*\s+)\d+(\s+races?)',
            f'\\g<1>{actual_races}\\g<2>',
            content,
            flags=re.IGNORECASE
        )
        
        # Pattern 2: "Total Races: X"
        content = re.sub(
            r'(\*\*Total Races:\*\*\s+)\d+',
            f'\\g<1>{actual_races}',
            content,
            flags=re.IGNORECASE
        )
        
        # Pattern 3: "- **Total Races**: X"
        content = re.sub(
            r'(-\s+\*\*Total Races\*\*:\s+)\d+',
            f'\\g<1>{actual_races}',
            content,
            flags=re.IGNORECASE
        )
        
        # Pattern 4: "Total Candidates Profiled: X candidates"
        content = re.sub(
            r'(\*\*Total Candidates Profiled:\*\*\s+)\d+(\s+(?:major\s+)?candidates?)',
            f'\\g<1>{actual_candidates}\\g<2>',
            content,
            flags=re.IGNORECASE
        )
        
        # Pattern 5: "Total Candidates: X"
        content = re.sub(
            r'(\*\*Total Candidates:\*\*\s+)\d+',
            f'\\g<1>{actual_candidates}',
            content,
            flags=re.IGNORECASE
        )
        
        # Pattern 6: Handle "50+ races" or "8+ candidates" style
        content = re.sub(
            r'(\*\*Total Races Documented:\*\*\s+)\d+\+(\s+races?)',
            f'\\g<1>{actual_races}\\g<2>',
            content,
            flags=re.IGNORECASE
        )
        
        content = re.sub(
            r'(\*\*Total Candidates Profiled:\*\*\s+)\d+\+(\s+(?:major\s+)?candidates?)',
            f'\\g<1>{actual_candidates}\\g<2>',
            content,
            flags=re.IGNORECASE
        )
        
        # Update summary in DynamoDB
        summary['content'] = content
        summaries_table.put_item(Item=summary)
        
        print(f"  [OK] Updated {state}: {actual_races} races, {actual_candidates} candidates")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed to update {state}: {str(e)}")
        return False

def main():
    print("\n" + "="*80)
    print("FIX DYNAMODB SUMMARY COUNTS")
    print("="*80)
    print("\nThis will update state-summaries table in DynamoDB with correct counts")
    print("States to fix:", ", ".join(STATES_TO_FIX))
    print()
    
    confirm = input("Type 'FIX SUMMARIES' to proceed: ")
    
    if confirm != "FIX SUMMARIES":
        print("\n[CANCELLED] Operation cancelled")
        return
    
    print("\n" + "="*80)
    print("PROCESSING STATES")
    print("="*80 + "\n")
    
    updated = 0
    skipped = 0
    
    for state in STATES_TO_FIX:
        print(f"\n{state}:")
        actual_races, actual_candidates = get_actual_counts(state)
        print(f"  Actual counts: {actual_races} races, {actual_candidates} candidates")
        
        if fix_summary_counts(state, actual_races, actual_candidates):
            updated += 1
        else:
            skipped += 1
    
    print("\n" + "="*80)
    print("UPDATE COMPLETE")
    print("="*80)
    print(f"\nStates updated: {updated}")
    print(f"States skipped: {skipped}")
    print("\nThe website will now show correct counts!")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
