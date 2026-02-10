"""
Update existing candidate in DynamoDB
Usage: python update_candidate.py "Candidate Name" "State" --field status --value withdrawn
"""
import boto3
import sys
from datetime import datetime

db = boto3.resource('dynamodb')
table = db.Table('candidates')

def update_candidate(name, state, field, value):
    response = table.scan(
        FilterExpression='#name = :name AND #state = :state',
        ExpressionAttributeNames={'#name': 'name', '#state': 'state'},
        ExpressionAttributeValues={':name': name, ':state': state}
    )
    
    if not response['Items']:
        print(f"Candidate not found: {name} ({state})")
        return False
    
    candidate = response['Items'][0]
    
    table.update_item(
        Key={'candidate_id': candidate['candidate_id']},
        UpdateExpression=f'SET #{field} = :value, updated_at = :time',
        ExpressionAttributeNames={f'#{field}': field},
        ExpressionAttributeValues={
            ':value': value,
            ':time': datetime.utcnow().isoformat()
        }
    )
    
    print(f"Updated {name}: {field} = {value}")
    return True

if __name__ == '__main__':
    if len(sys.argv) >= 7:
        update_candidate(sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[6])
    else:
        print("Usage: python update_candidate.py 'Name' 'State' --field FIELD --value VALUE")
