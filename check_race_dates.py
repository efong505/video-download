import boto3

db = boto3.resource('dynamodb')
races = db.Table('races').scan()['Items']

for state in ['Virginia','Texas','Georgia','Nebraska','California','Hawaii']:
    state_races = [r for r in races if r.get('state') == state]
    dates = sorted(set(r.get('election_date','') for r in state_races))
    print(f'{state}: {len(state_races)} races')
    for date in dates:
        count = len([r for r in state_races if r.get('election_date') == date])
        print(f'  {date}: {count} races')
