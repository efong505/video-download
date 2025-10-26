import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

def delete_hawaii_races():
    print("\n" + "="*60)
    print("DELETING HAWAII RACES")
    print("="*60 + "\n")
    
    # Scan for all Hawaii races
    response = races_table.scan(
        FilterExpression=Key('state').eq('Hawaii')
    )
    
    races = response['Items']
    
    # Handle pagination if more than 1MB of data
    while 'LastEvaluatedKey' in response:
        response = races_table.scan(
            FilterExpression=Key('state').eq('Hawaii'),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        races.extend(response['Items'])
    
    print(f"Found {len(races)} Hawaii races to delete\n")
    
    deleted = 0
    for race in races:
        try:
            races_table.delete_item(Key={'race_id': race['race_id']})
            print(f"✓ Deleted race: {race['office']}")
            deleted += 1
        except Exception as e:
            print(f"✗ Failed to delete race {race['office']}: {str(e)}")
    
    print(f"\n[OK] Deleted {deleted} races")
    return deleted

def delete_hawaii_candidates():
    print("\n" + "="*60)
    print("DELETING HAWAII CANDIDATES")
    print("="*60 + "\n")
    
    # Scan for all Hawaii candidates
    response = candidates_table.scan(
        FilterExpression=Key('state').eq('Hawaii')
    )
    
    candidates = response['Items']
    
    # Handle pagination
    while 'LastEvaluatedKey' in response:
        response = candidates_table.scan(
            FilterExpression=Key('state').eq('Hawaii'),
            ExclusiveStartKey=response['LastEvaluatedKey']
        )
        candidates.extend(response['Items'])
    
    print(f"Found {len(candidates)} Hawaii candidates to delete\n")
    
    deleted = 0
    for candidate in candidates:
        try:
            candidates_table.delete_item(Key={'candidate_id': candidate['candidate_id']})
            print(f"✓ Deleted candidate: {candidate['name']} - {candidate['office']}")
            deleted += 1
        except Exception as e:
            print(f"✗ Failed to delete candidate {candidate['name']}: {str(e)}")
    
    print(f"\n[OK] Deleted {deleted} candidates")
    return deleted

def main():
    print("\n" + "="*60)
    print("HAWAII DATA DELETION SCRIPT")
    print("="*60)
    print("\nThis will DELETE ALL Hawaii races and candidates from DynamoDB")
    print("This action CANNOT be undone!\n")
    
    confirm = input("Type 'DELETE HAWAII' to confirm: ")
    
    if confirm != "DELETE HAWAII":
        print("\n[CANCELLED] Deletion cancelled")
        return
    
    # Delete candidates first (they reference races)
    candidates_deleted = delete_hawaii_candidates()
    
    # Then delete races
    races_deleted = delete_hawaii_races()
    
    print("\n" + "="*60)
    print("DELETION COMPLETE")
    print("="*60)
    print(f"\nTotal races deleted: {races_deleted}")
    print(f"Total candidates deleted: {candidates_deleted}")
    print("\nYou can now run your new upload script to add fresh Hawaii data.")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
