import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Check races
races_response = races_table.scan(FilterExpression=Attr('state').eq('Arizona'))
print(f"\n=== ARIZONA RACES ({len(races_response['Items'])} total) ===\n")
for race in sorted(races_response['Items'], key=lambda x: x.get('race_id', '')):
    print(f"{race.get('race_id', 'N/A')}: {race.get('office', 'N/A')}")

# Check candidates
candidates_response = candidates_table.scan(FilterExpression=Attr('state').eq('Arizona'))
print(f"\n=== ARIZONA CANDIDATES ({len(candidates_response['Items'])} total) ===\n")
for candidate in sorted(candidates_response['Items'], key=lambda x: x.get('name', '')):
    print(f"{candidate.get('name', 'N/A')} ({candidate.get('party', 'N/A')}) - {candidate.get('office', 'N/A')} - {candidate.get('race_id', 'N/A')}")
