import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')

response = table.scan()
items = response['Items']

# Criteria for comprehensive summary
comprehensive = []
needs_work = []

for item in items:
    state = item['state']
    content = item.get('content', '')
    length = len(content)
    
    # Check for comprehensive markers
    has_database = '## 📊 Database Summary' in content
    has_landscape = '## 🔴' in content and 'POLITICAL LANDSCAPE' in content
    has_detailed_candidates = 'Faith Statement:' in content and 'Christian Conservative Analysis:' in content
    has_key_issues = '## 🎯 KEY ISSUES' in content
    has_church_mobilization = '## 🗳️ CHURCH MOBILIZATION' in content
    has_bottom_line = '## 🔥 BOTTOM LINE' in content
    has_prayer = '## 🙏 PRAYER' in content
    
    # Comprehensive if has all sections and good length
    is_comprehensive = (has_database and has_landscape and has_detailed_candidates and 
                       has_key_issues and has_church_mobilization and has_bottom_line and 
                       has_prayer and length > 12000)
    
    if is_comprehensive:
        comprehensive.append((state, length))
    else:
        needs_work.append((state, length, {
            'database': has_database,
            'landscape': has_landscape,
            'candidates': has_detailed_candidates,
            'issues': has_key_issues,
            'mobilization': has_church_mobilization,
            'bottom_line': has_bottom_line,
            'prayer': has_prayer
        }))

print("=" * 80)
print("COMPREHENSIVE SUMMARIES (Nebraska-style - GOOD):")
print("=" * 80)
for state, length in sorted(comprehensive, key=lambda x: x[1], reverse=True):
    print(f"[OK] {state:20} {length:>7,} chars")

print(f"\n{'=' * 80}")
print(f"STATES NEEDING COMPREHENSIVE REWRITES ({len(needs_work)} states):")
print("=" * 80)

for state, length, markers in sorted(needs_work, key=lambda x: x[1], reverse=True):
    missing = [k for k, v in markers.items() if not v]
    status = "SHORT" if length < 8000 else "MISSING SECTIONS"
    print(f"[REDO] {state:20} {length:>7,} chars - {status}")
    if missing and length > 8000:
        print(f"       Missing: {', '.join(missing)}")

print(f"\n{'=' * 80}")
print("SUMMARY:")
print("=" * 80)
print(f"Comprehensive (ready): {len(comprehensive)} states")
print(f"Need work: {len(needs_work)} states")
print(f"\nPriority: Focus on states with races/candidates in database first")
