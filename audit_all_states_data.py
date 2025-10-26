import boto3
import re
import os

dynamodb = boto3.resource('dynamodb')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# All 50 states
STATES = [
    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
    'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
    'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
    'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
    'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
    'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
    'Wisconsin', 'Wyoming'
]

def get_dynamodb_counts(state):
    """Get actual counts from DynamoDB"""
    try:
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
    except Exception as e:
        return None, None

def get_summary_guide_counts(state):
    """Extract counts from summary guide markdown file"""
    filename = f"Election Data and Files/Voter Guides_Summaries/{state.lower()}_summary_guide.md"
    
    if not os.path.exists(filename):
        return None, None
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for various patterns
        races_match = re.search(r'Total Races.*?(\d+)', content, re.IGNORECASE)
        candidates_match = re.search(r'Total Candidates.*?(\d+)', content, re.IGNORECASE)
        
        races_count = int(races_match.group(1)) if races_match else None
        candidates_count = int(candidates_match.group(1)) if candidates_match else None
        
        return races_count, candidates_count
    except Exception as e:
        return None, None

def main():
    print("\n" + "="*80)
    print("ELECTION DATA AUDIT - ALL 50 STATES")
    print("="*80)
    print("\nComparing DynamoDB actual data vs Summary Guide documentation\n")
    
    discrepancies = []
    missing_data = []
    perfect_matches = []
    
    for state in STATES:
        db_races, db_candidates = get_dynamodb_counts(state)
        guide_races, guide_candidates = get_summary_guide_counts(state)
        
        # Check for issues
        if db_races is None and db_candidates is None:
            missing_data.append({
                'state': state,
                'issue': 'No DynamoDB data'
            })
        elif guide_races is None and guide_candidates is None:
            missing_data.append({
                'state': state,
                'issue': 'No summary guide'
            })
        elif db_races != guide_races or db_candidates != guide_candidates:
            discrepancies.append({
                'state': state,
                'db_races': db_races,
                'db_candidates': db_candidates,
                'guide_races': guide_races,
                'guide_candidates': guide_candidates
            })
        else:
            perfect_matches.append({
                'state': state,
                'races': db_races,
                'candidates': db_candidates
            })
    
    # Print discrepancies
    if discrepancies:
        print("="*80)
        print("DISCREPANCIES FOUND")
        print("="*80)
        for item in discrepancies:
            print(f"\n{item['state']}:")
            print(f"  DynamoDB:     {item['db_races']} races, {item['db_candidates']} candidates")
            print(f"  Summary Guide: {item['guide_races']} races, {item['guide_candidates']} candidates")
            races_diff = item['db_races'] - (item['guide_races'] or 0)
            cand_diff = item['db_candidates'] - (item['guide_candidates'] or 0)
            print(f"  Difference:    {races_diff:+d} races, {cand_diff:+d} candidates")
    
    # Print missing data
    if missing_data:
        print("\n" + "="*80)
        print("MISSING DATA")
        print("="*80)
        for item in missing_data:
            print(f"  {item['state']}: {item['issue']}")
    
    # Print perfect matches
    if perfect_matches:
        print("\n" + "="*80)
        print(f"PERFECT MATCHES ({len(perfect_matches)} states)")
        print("="*80)
        for item in perfect_matches:
            print(f"  ✓ {item['state']}: {item['races']} races, {item['candidates']} candidates")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"  Perfect Matches: {len(perfect_matches)}")
    print(f"  Discrepancies:   {len(discrepancies)}")
    print(f"  Missing Data:    {len(missing_data)}")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
