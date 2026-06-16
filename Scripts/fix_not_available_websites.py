import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

# Scan all candidates
response = candidates_table.scan()
candidates = response['Items']

invalid_values = ['Not available', 'not available', 'N/A', 'n/a', 'None', 'none', 'TBD', 'tbd', 'Coming soon', 'coming soon', 'Unknown', 'unknown']

fixed_count = 0
for candidate in candidates:
    website = candidate.get('website', '')
    if website in invalid_values:
        print(f"Fixing: {candidate['name']} ({candidate['state']}) - '{website}' -> ''")
        candidates_table.update_item(
            Key={'candidate_id': candidate['candidate_id']},
            UpdateExpression='SET website = :empty, updated_at = :updated',
            ExpressionAttributeValues={
                ':empty': '',
                ':updated': datetime.now().isoformat()
            }
        )
        fixed_count += 1

print(f"\n[SUCCESS] Fixed {fixed_count} candidates with invalid website values")
