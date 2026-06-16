import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')

response = table.scan()
items = response['Items']

fixed = []
for item in items:
    if 'summary' in item and 'content' not in item:
        table.update_item(
            Key={'state': item['state']},
            UpdateExpression='SET #content = :content, #updated = :updated REMOVE summary, last_updated',
            ExpressionAttributeNames={'#content': 'content', '#updated': 'updated_at'},
            ExpressionAttributeValues={':content': item['summary'], ':updated': item.get('last_updated', '2025-01-01')}
        )
        fixed.append(item['state'])

print(f"Fixed {len(fixed)} states: {', '.join(fixed)}")
