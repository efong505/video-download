import boto3
import re
import os
from datetime import datetime

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
        return 0, 0

def update_summary_guide(state, db_races, db_candidates):
    """Update summary guide with correct counts"""
    filename = f"Election Data and Files/Voter Guides_Summaries/{state.lower()}_summary_guide.md"
    
    if not os.path.exists(filename):
        print(f"  [SKIP] No summary guide found for {state}")
        return False
    
    try:
        # Create backup
        backup_filename = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Pattern 1: "Total Races Documented: X races"
        pattern1 = r'(\*\*Total Races Documented:\*\*\s+)\d+(\s+races?)'
        replacement1 = f'\\g<1>{db_races}\\g<2>'
        content = re.sub(pattern1, replacement1, content, flags=re.IGNORECASE)
        
        # Pattern 2: "Total Races: X"
        pattern2 = r'(\*\*Total Races:\*\*\s+)\d+'
        replacement2 = f'\\g<1>{db_races}'
        content = re.sub(pattern2, replacement2, content, flags=re.IGNORECASE)
        
        # Pattern 3: "- **Total Races**: X"
        pattern3 = r'(-\s+\*\*Total Races\*\*:\s+)\d+'
        replacement3 = f'\\g<1>{db_races}'
        content = re.sub(pattern3, replacement3, content, flags=re.IGNORECASE)
        
        # Pattern 4: "Total Candidates Profiled: X candidates"
        pattern4 = r'(\*\*Total Candidates Profiled:\*\*\s+)\d+(\s+candidates?)'
        replacement4 = f'\\g<1>{db_candidates}\\g<2>'
        content = re.sub(pattern4, replacement4, content, flags=re.IGNORECASE)
        
        # Pattern 5: "Total Candidates: X"
        pattern5 = r'(\*\*Total Candidates:\*\*\s+)\d+'
        replacement5 = f'\\g<1>{db_candidates}'
        content = re.sub(pattern5, replacement5, content, flags=re.IGNORECASE)
        
        # Pattern 6: Handle "50+ races" or "8+ major candidates" style
        pattern6 = r'(\*\*Total Races Documented:\*\*\s+)\d+\+(\s+races?)'
        replacement6 = f'\\g<1>{db_races}\\g<2>'
        content = re.sub(pattern6, replacement6, content, flags=re.IGNORECASE)
        
        pattern7 = r'(\*\*Total Candidates Profiled:\*\*\s+)\d+\+(\s+(?:major\s+)?candidates?)'
        replacement7 = f'\\g<1>{db_candidates}\\g<2>'
        content = re.sub(pattern7, replacement7, content, flags=re.IGNORECASE)
        
        # Write updated content
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  [OK] Updated {state}: {db_races} races, {db_candidates} candidates")
        print(f"       Backup: {os.path.basename(backup_filename)}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] Failed to update {state}: {str(e)}")
        return False

def main():
    print("\n" + "="*80)
    print("AUTO-FIX SUMMARY GUIDES - UPDATE ALL COUNTS TO MATCH DYNAMODB")
    print("="*80)
    print("\nThis will update all summary guide files with correct DynamoDB counts")
    print("Backups will be created for each file\n")
    
    confirm = input("Type 'UPDATE ALL' to proceed: ")
    
    if confirm != "UPDATE ALL":
        print("\n[CANCELLED] Operation cancelled")
        return
    
    print("\n" + "="*80)
    print("PROCESSING ALL STATES")
    print("="*80 + "\n")
    
    updated = 0
    skipped = 0
    errors = 0
    
    for state in STATES:
        print(f"\n{state}:")
        db_races, db_candidates = get_dynamodb_counts(state)
        
        if db_races == 0 and db_candidates == 0:
            print(f"  [SKIP] No DynamoDB data for {state}")
            skipped += 1
            continue
        
        if update_summary_guide(state, db_races, db_candidates):
            updated += 1
        else:
            errors += 1
    
    print("\n" + "="*80)
    print("UPDATE COMPLETE")
    print("="*80)
    print(f"\nStates updated: {updated}")
    print(f"States skipped: {skipped}")
    print(f"Errors: {errors}")
    print("\nAll updated files have backups with timestamp")
    print("="*80 + "\n")

if __name__ == '__main__':
    main()
