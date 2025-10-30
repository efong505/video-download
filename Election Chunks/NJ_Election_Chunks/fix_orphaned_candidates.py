import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

# Fix candidates with wrong office names
fixes = {
    "Gregory P. McGuckin": "General Assembly District 9 Seat 2",
    "Kyler Dineen": "General Assembly District 10 Seat 1",
    "Margaret M. Donlon": "General Assembly District 10 Seat 1",
    "Andrew C. Wardell": "General Assembly District 10 Seat 2",
    "Michael Torrissi Jr.": "General Assembly District 7 Seat 2",
    "John M. Brangan": "General Assembly District 5 Seat 1",
    "Constance Ditzel": "General Assembly District 4 Seat 2",
    "Dione Johnson": "General Assembly District 6 Seat 1",
    "Christopher Cerf": "Newark School Board Seat 1",
    "Paula Jones": "Jersey City School Board Seat 3",
    "Natalia Ioffe": "Jersey City School Board Seat 2",
    "Afaf Muhammad": "Jersey City School Board Seat 1",
    "Emily Morgan": "Plainfield School Board Seat 2",
    "Kenneth Armwood": "Plainfield School Board Seat 1",
    "Armando Virguez": "Perth Amboy School Board Seat 1",
    "Janine Walker": "Perth Amboy School Board Seat 2"
}

candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New Jersey'}
)['Items']

for candidate in candidates:
    name = candidate['name']
    if name in fixes:
        old_office = candidate['office']
        new_office = fixes[name]
        candidate['office'] = new_office
        candidate['race_id'] = ''  # Will be fixed by next script
        candidates_table.put_item(Item=candidate)
        print(f"Fixed: {name}")
        print(f"  {old_office} -> {new_office}")

print("\nDone! Now run smart_fix_race_ids.py again")
