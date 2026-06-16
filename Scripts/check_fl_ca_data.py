import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

for state in ['Florida', 'California']:
    print(f"\n{'='*60}")
    print(f"=== {state.upper()} ===")
    print('='*60)
    
    # Check races
    races_response = races_table.scan(FilterExpression=Attr('state').eq(state))
    print(f"\nRACES ({len(races_response['Items'])} total):")
    for race in sorted(races_response['Items'], key=lambda x: x.get('race_id', '')):
        print(f"  {race.get('race_id', 'N/A')}: {race.get('office', 'N/A')}")
    
    # Check candidates
    candidates_response = candidates_table.scan(FilterExpression=Attr('state').eq(state))
    print(f"\nCANDIDATES ({len(candidates_response['Items'])} total):")
    for candidate in sorted(candidates_response['Items'], key=lambda x: x.get('name', '')):
        print(f"  {candidate.get('name', 'N/A')} ({candidate.get('party', 'N/A')}) - {candidate.get('race_id', 'N/A')}")
