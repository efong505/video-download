import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')

ne = table.get_item(Key={'state': 'Nebraska'})['Item']

with open('nebraska_full.md', 'w', encoding='utf-8') as f:
    f.write(ne['content'])

print(f"Nebraska exported: {len(ne['content'])} chars")
