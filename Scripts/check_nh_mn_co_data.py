import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

states = ['New Hampshire', 'Minnesota', 'Colorado']

for state in states:
    print(f"\n{'='*60}")
    print(f"{state.upper()}")
    print('='*60)
    
    # Check races
    races_response = races_table.scan(FilterExpression=Key('state').eq(state))
    races = races_response['Items']
    print(f"\nRACES ({len(races)}):")
    for race in sorted(races, key=lambda x: x.get('office', '')):
        print(f"  - {race.get('office', 'N/A')} | {race.get('race_type', 'N/A')} | {race.get('incumbent_party', 'N/A')} | ID: {race.get('race_id', 'N/A')}")
    
    # Check candidates
    candidates_response = candidates_table.scan(FilterExpression=Key('state').eq(state))
    candidates = candidates_response['Items']
    print(f"\nCANDIDATES ({len(candidates)}):")
    for candidate in sorted(candidates, key=lambda x: (x.get('office', ''), x.get('party', ''), x.get('name', ''))):
        print(f"  - {candidate.get('name', 'N/A')} ({candidate.get('party', 'N/A')}) - {candidate.get('office', 'N/A')}")
    
    # Check summary
    summary_response = summaries_table.get_item(Key={'state': state})
    summary = summary_response.get('Item', {})
    summary_text = summary.get('summary', '')
    print(f"\nSUMMARY: {len(summary_text)} characters")
    if len(summary_text) == 0:
        print("  WARNING: NO SUMMARY EXISTS")

print("\n" + "="*60)
