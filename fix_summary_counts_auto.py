import boto3
import re

dynamodb = boto3.resource('dynamodb')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

STATES_TO_FIX = ['California', 'Florida', 'Georgia', 'Ohio', 'Texas', 'Virginia']

def get_actual_counts(state):
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

def fix_summary_counts(state, actual_races, actual_candidates):
    try:
        response = summaries_table.get_item(Key={'state': state})
        if 'Item' not in response:
            print(f"  [SKIP] No summary in DynamoDB for {state}")
            return False
        
        summary = response['Item']
        content = summary['content']
        
        content = re.sub(r'(\*\*Total Races Documented:\*\*\s+)\d+(\s+races?)', f'\\g<1>{actual_races}\\g<2>', content, flags=re.IGNORECASE)
        content = re.sub(r'(\*\*Total Races:\*\*\s+)\d+', f'\\g<1>{actual_races}', content, flags=re.IGNORECASE)
        content = re.sub(r'(-\s+\*\*Total Races\*\*:\s+)\d+', f'\\g<1>{actual_races}', content, flags=re.IGNORECASE)
        content = re.sub(r'(\*\*Total Candidates Profiled:\*\*\s+)\d+(\s+(?:major\s+)?candidates?)', f'\\g<1>{actual_candidates}\\g<2>', content, flags=re.IGNORECASE)
        content = re.sub(r'(\*\*Total Candidates:\*\*\s+)\d+', f'\\g<1>{actual_candidates}', content, flags=re.IGNORECASE)
        content = re.sub(r'(\*\*Total Races Documented:\*\*\s+)\d+\+(\s+races?)', f'\\g<1>{actual_races}\\g<2>', content, flags=re.IGNORECASE)
        content = re.sub(r'(\*\*Total Candidates Profiled:\*\*\s+)\d+\+(\s+(?:major\s+)?candidates?)', f'\\g<1>{actual_candidates}\\g<2>', content, flags=re.IGNORECASE)
        
        summary['content'] = content
        summaries_table.put_item(Item=summary)
        
        print(f"  [OK] {state}: {actual_races} races, {actual_candidates} candidates")
        return True
        
    except Exception as e:
        print(f"  [ERROR] {state}: {str(e)}")
        return False

print("\n" + "="*80)
print("FIXING DYNAMODB SUMMARY COUNTS")
print("="*80 + "\n")

updated = 0
for state in STATES_TO_FIX:
    print(f"{state}:")
    actual_races, actual_candidates = get_actual_counts(state)
    if fix_summary_counts(state, actual_races, actual_candidates):
        updated += 1

print(f"\n[SUCCESS] Updated {updated} states")
print("="*80 + "\n")
