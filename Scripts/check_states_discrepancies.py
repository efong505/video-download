import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
summaries_table = dynamodb.Table('state-summaries')

states_to_check = ['California', 'New Mexico', 'Nevada', 'North Carolina']

for state in states_to_check:
    print(f"\n{'='*60}")
    print(f"=== {state.upper()} ===")
    print('='*60)
    
    # Check races
    races_response = races_table.scan(FilterExpression=Attr('state').eq(state))
    races = races_response['Items']
    
    # Check for Senate races
    senate_races = [r for r in races if 'Senate' in r.get('office', '')]
    
    # Check for Governor races
    gov_races = [r for r in races if 'Governor' in r.get('office', '')]
    
    # Check summary
    summary_response = summaries_table.scan(FilterExpression=Attr('state').eq(state))
    summary_length = len(summary_response['Items'][0].get('summary', '')) if summary_response['Items'] else 0
    
    print(f"\nRACES: {len(races)} total")
    print(f"  Senate races: {len(senate_races)}")
    for sr in senate_races:
        print(f"    - {sr.get('race_id')}: {sr.get('office')} on {sr.get('election_date', 'NO DATE')}")
    
    print(f"  Governor races: {len(gov_races)}")
    for gr in gov_races:
        print(f"    - {gr.get('race_id')}: {gr.get('office')} on {gr.get('election_date', 'NO DATE')}")
    
    print(f"\nSUMMARY: {summary_length:,} characters")
    
    # State-specific checks
    if state == 'California':
        print("\n  EXPECTED: NO Senate race in 2026 (Padilla-2028, Schiff-2030)")
        print("  EXPECTED: Governor race 2026 (Newsom term-limited)")
    
    elif state == 'New Mexico':
        print("\n  EXPECTED: NO Senate race in 2026 (Lujan-2028, Heinrich-2030)")
        print("  EXPECTED: Governor race 2026")
        print("  EXPECTED: Albuquerque municipal election Nov 4, 2025")
    
    elif state == 'Nevada':
        print("\n  EXPECTED: NO Senate race in 2026 (Rosen-2028, Cortez Masto-2030)")
        print("  EXPECTED: Governor race 2026 (Lombardo)")
        print("  ISSUE: Guide mentions Sam Brown vs Jacky Rosen - INCORRECT")
    
    elif state == 'North Carolina':
        print("\n  EXPECTED: NO Senate race in 2026 (Tillis-2028, Budd-2030)")
        print("  EXPECTED: Governor race 2026")
        print("  EXPECTED: General election Nov 3, 2026 (NOT Nov 4)")
