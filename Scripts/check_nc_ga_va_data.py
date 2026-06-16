import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

states = ['North Carolina', 'Georgia', 'Virginia']

for state in states:
    print(f"\n{'='*60}")
    print(f"{state.upper()}")
    print('='*60)
    
    races_response = races_table.scan(FilterExpression=Key('state').eq(state))
    races = races_response['Items']
    print(f"\nRACES ({len(races)}):")
    for race in sorted(races, key=lambda x: x.get('office', ''))[:10]:
        print(f"  - {race.get('office', 'N/A')} | {race.get('incumbent', 'N/A')} ({race.get('incumbent_party', 'N/A')}) | Date: {race.get('election_date', 'N/A')}")
    if len(races) > 10:
        print(f"  ... and {len(races) - 10} more races")
    
    candidates_response = candidates_table.scan(FilterExpression=Key('state').eq(state))
    candidates = candidates_response['Items']
    print(f"\nCANDIDATES ({len(candidates)}):")
    for candidate in sorted(candidates, key=lambda x: (x.get('office', ''), x.get('name', '')))[:10]:
        print(f"  - {candidate.get('name', 'N/A')} ({candidate.get('party', 'N/A')}) - {candidate.get('office', 'N/A')}")
    if len(candidates) > 10:
        print(f"  ... and {len(candidates) - 10} more candidates")
    
    summary_response = summaries_table.get_item(Key={'state': state})
    summary = summary_response.get('Item', {})
    summary_text = summary.get('summary', '')
    print(f"\nSUMMARY: {len(summary_text)} characters")
    if len(summary_text) == 0:
        print("  WARNING: NO SUMMARY EXISTS")
    elif len(summary_text) < 15000:
        print(f"  WARNING: Summary too short (need 15,000-25,000 chars)")

print("\n" + "="*60)
