import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

response = candidates_table.scan(
    FilterExpression=Attr('state').eq('Georgia')
)

print(f"\n=== GEORGIA CANDIDATES ({len(response['Items'])} total) ===\n")

for candidate in sorted(response['Items'], key=lambda x: x.get('name', '')):
    print(f"ID: {candidate['candidate_id']}")
    print(f"Name: {candidate.get('name', 'N/A')}")
    print(f"Office: {candidate.get('office', 'N/A')}")
    print(f"Party: {candidate.get('party', 'N/A')}")
    print(f"Race ID: {candidate.get('race_id', 'N/A')}")
    print("-" * 60)
