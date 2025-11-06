import boto3

db = boto3.resource('dynamodb')
races = db.Table('races').scan()['Items']
summaries = set(s['state'] for s in db.Table('state-summaries').scan()['Items'])

# Check major states
states = ['New Mexico','New Jersey','Illinois','Louisiana','Mississippi','Missouri',
          'Oklahoma','Washington','Pennsylvania','Ohio','Michigan','Minnesota',
          'Montana','Iowa','Utah','North Carolina','Massachusetts']

print("States with races but NO summary:\n")
for s in states:
    count = len([r for r in races if r.get('state') == s])
    if count > 0:
        has_summary = 'YES' if s in summaries else 'NO'
        if has_summary == 'NO':
            print(f'{s}: {count} races - Summary: {has_summary}')
