import boto3

all_states = [
    'Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut',
    'Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa',
    'Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan',
    'Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire',
    'New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio',
    'Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota',
    'Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia',
    'Wisconsin','Wyoming'
]

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')
response = table.scan()
db_states = sorted([item['state'] for item in response['Items']])
missing = sorted(set(all_states) - set(db_states))

print('=' * 60)
print('ALL 50 US STATES STATUS')
print('=' * 60)
print(f'\nStates in database: {len(db_states)}/50')
print(f'Missing states: {len(missing)}/50')
print('\n' + '=' * 60)

if missing:
    print('MISSING STATES:')
    print('=' * 60)
    for s in missing:
        print(f'  X {s}')
else:
    print('ALL 50 STATES COMPLETED!')
    print('=' * 60)

print('\nCOMPLETED STATES:')
print('=' * 60)
for s in db_states:
    print(f'  + {s}')
