import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

states_to_check = [
    'Pennsylvania', 'Ohio', 'North Carolina', 'Georgia', 'Virginia',
    'New Hampshire', 'Minnesota', 'Colorado', 'Delaware', 'New Jersey', 'Rhode Island'
]

template_sections = [
    'Database Summary',
    'POLITICAL LANDSCAPE',
    'CHURCH MOBILIZATION',
    'What Pastors Can Do',
    'What Church Members Can Do',
    'BOTTOM LINE',
    'If Conservatives Win',
    'If Progressives Win',
    'PRAYER POINTS'
]

print("STATE SUMMARY TEMPLATE COMPLIANCE CHECK")
print("=" * 80)

for state in states_to_check:
    response = summaries_table.get_item(Key={'state': state})
    if 'Item' in response:
        content = response['Item']['content']
        length = len(content)
        
        print(f"\n{state}: {length:,} chars")
        
        missing = []
        for section in template_sections:
            if section not in content:
                missing.append(section)
        
        if missing:
            print(f"  MISSING: {', '.join(missing)}")
        else:
            print(f"  [OK] All template sections present")
    else:
        print(f"\n{state}: NOT FOUND")

print("\n" + "=" * 80)
print("SUMMARY:")
print("States with FULL template (all sections): Check above")
print("States MISSING sections: Need regeneration")
