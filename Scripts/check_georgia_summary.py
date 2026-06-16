import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

response = summaries_table.scan(FilterExpression=Attr('state').eq('Georgia'))

if response['Items']:
    summary = response['Items'][0]
    content = summary.get('summary', '')
    print(f"Georgia Summary Length: {len(content)} characters")
    print(f"\nFirst 500 characters:\n{content[:500]}")
    print(f"\n...\n\nLast 500 characters:\n{content[-500:]}")
else:
    print("No Georgia summary found")
