import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

response = candidates_table.scan()
candidates = response['Items']

print(f"Total candidates: {len(candidates)}\n")

for candidate in candidates:
    print(f"Name: {candidate.get('name', 'N/A')}")
    print(f"  Party: {candidate.get('party', 'NOT SET')}")
    print(f"  State: {candidate.get('state', 'N/A')}")
    print(f"  Office: {candidate.get('office', 'N/A')}")
    print()
