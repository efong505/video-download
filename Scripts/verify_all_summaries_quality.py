import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')

# Scan all summaries
response = table.scan()
summaries = response['Items']

# Required markers for comprehensive summaries
required_markers = [
    'Database Summary',
    'POLITICAL LANDSCAPE',
    'Faith Statement:',
    'Christian Conservative Analysis:',
    'KEY ISSUES',
    'CHURCH MOBILIZATION',
    'BOTTOM LINE',
    'PRAYER',
    'Proverbs 14:34',
    'Proverbs 29:2',
    '2 Chronicles 7:14'
]

print('=' * 80)
print('VERIFYING ALL 50 STATE SUMMARIES FOR COMPREHENSIVE FORMAT')
print('=' * 80)

comprehensive_states = []
incomplete_states = []

for summary in sorted(summaries, key=lambda x: x['state']):
    state = summary['state']
    content = summary.get('content', '')
    char_count = len(content)
    
    # Check for required markers
    missing_markers = []
    for marker in required_markers:
        if marker not in content:
            missing_markers.append(marker)
    
    # Determine if comprehensive
    is_comprehensive = len(missing_markers) == 0 and char_count >= 12000
    
    if is_comprehensive:
        comprehensive_states.append(state)
        print(f'[OK] {state:20} - {char_count:,} chars - COMPREHENSIVE')
    else:
        incomplete_states.append({
            'state': state,
            'chars': char_count,
            'missing': missing_markers
        })
        print(f'[!!] {state:20} - {char_count:,} chars - NEEDS WORK')

print('\n' + '=' * 80)
print(f'SUMMARY: {len(comprehensive_states)}/50 states have comprehensive summaries')
print('=' * 80)

if incomplete_states:
    print(f'\n{len(incomplete_states)} STATES NEED ATTENTION:\n')
    for item in incomplete_states:
        print(f"\n{item['state']} ({item['chars']:,} chars):")
        if item['chars'] < 12000:
            print(f"  - Too short (need 12,000+ chars)")
        if item['missing']:
            print(f"  - Missing {len(item['missing'])} required sections:")
            for marker in item['missing'][:5]:  # Show first 5
                print(f"    - {marker.replace('📊', '[DB]').replace('🔴', '[RED]').replace('🎯', '[TARGET]').replace('🗳️', '[VOTE]').replace('🔥', '[FIRE]').replace('🙏', '[PRAY]')}")
            if len(item['missing']) > 5:
                print(f"    ... and {len(item['missing']) - 5} more")
else:
    print('\n*** ALL 50 STATES HAVE COMPREHENSIVE SUMMARIES! ***')

print('\n' + '=' * 80)
