import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

response = summaries_table.scan()
summaries = response['Items']

print(f"\n=== ALL STATE SUMMARIES ({len(summaries)} total) ===\n")

for summary in sorted(summaries, key=lambda x: x.get('state', '')):
    state = summary.get('state', 'Unknown')
    length = len(summary.get('summary', ''))
    print(f"{state}: {length:,} characters")

print(f"\nTotal states with summaries: {len(summaries)}")
