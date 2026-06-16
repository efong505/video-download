import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

states = ['Kansas', 'Iowa', 'Maine', 'Kentucky']

for state in states:
    print(f"\n{'='*60}")
    print(f"=== {state.upper()} ===")
    print('='*60)
    
    # Check races
    races_response = races_table.scan(FilterExpression=Attr('state').eq(state))
    races = races_response['Items']
    
    # Check candidates
    candidates_response = candidates_table.scan(FilterExpression=Attr('state').eq(state))
    candidates = candidates_response['Items']
    
    # Check summary
    summary_response = summaries_table.scan(FilterExpression=Attr('state').eq(state))
    summary_length = len(summary_response['Items'][0].get('summary', '')) if summary_response['Items'] else 0
    summary_content = summary_response['Items'][0].get('summary', '')[:500] if summary_response['Items'] else ''
    
    print(f"\nRACES: {len(races)} total")
    
    # Governor races
    gov_races = [r for r in races if 'Governor' in r.get('office', '')]
    print(f"  Governor races: {len(gov_races)}")
    for gr in gov_races:
        print(f"    - {gr.get('office')}: {gr.get('status', 'NO STATUS')}")
    
    # Senate races
    senate_races = [r for r in races if 'Senate' in r.get('office', '')]
    print(f"  Senate races: {len(senate_races)}")
    for sr in senate_races:
        print(f"    - {sr.get('office')}: {sr.get('status', 'NO STATUS')}")
    
    print(f"\nCANDIDATES: {len(candidates)} total")
    for c in sorted(candidates, key=lambda x: x.get('name', ''))[:10]:
        print(f"  - {c.get('name')} ({c.get('party')}) - {c.get('office')}")
    
    print(f"\nSUMMARY: {summary_length:,} characters")
    if summary_content:
        print(f"  Preview: {summary_content[:200]}...")
    
    # State-specific checks
    if state == 'Kansas':
        print("\n  ISSUE: Guide says 'defeat Laura Kelly' but she's TERM-LIMITED (OPEN SEAT)")
        print("  MISSING: Jeff Colyer (R), Ty Masterson (R), Ethan Corson (D), Cindy Holscher (D)")
    
    elif state == 'Iowa':
        print("\n  ISSUE: Guide says Reynolds 'term-limited' but Iowa has NO term limits")
        print("  CORRECT: Reynolds voluntarily not seeking re-election (OPEN SEAT)")
        print("  MISSING: Rob Sand (D), Julie Stauch (D)")
    
    elif state == 'Maine':
        print("\n  ISSUE: Missing Governor Janet Mills (D) as major Senate challenger")
        print("  UPDATE: Race moved from 'Leans R' to 'Toss-up' after Mills entered")
    
    elif state == 'Kentucky':
        print("\n  ISSUE: Guide mentions Amy McGrath but she's NOT declared")
        print("  MISSING: Logan Forsythe (D), Pamela Stevenson (D), Joel Willett (D)")
