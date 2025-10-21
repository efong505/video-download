import boto3
from datetime import datetime

db = boto3.resource('dynamodb', region_name='us-east-1')
table = db.Table('candidates')

def fix_faith_statements():
    """Update all candidates with 'Not publicly disclosed' to 'No publicly disclosed faith statement'"""
    
    response = table.scan()
    candidates = response['Items']
    
    # Handle pagination
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        candidates.extend(response['Items'])
    
    updated_count = 0
    
    for candidate in candidates:
        faith = candidate.get('faith_statement', '')
        
        if faith == 'Not publicly disclosed':
            table.update_item(
                Key={'candidate_id': candidate['candidate_id']},
                UpdateExpression='SET faith_statement = :faith, updated_at = :time',
                ExpressionAttributeValues={
                    ':faith': 'No publicly disclosed faith statement',
                    ':time': datetime.utcnow().isoformat()
                }
            )
            updated_count += 1
            print(f"Updated: {candidate['name']} ({candidate['state']})")
    
    print(f"\nTotal candidates updated: {updated_count}")

if __name__ == '__main__':
    fix_faith_statements()
