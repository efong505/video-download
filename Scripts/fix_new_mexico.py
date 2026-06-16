import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')

response = table.get_item(Key={'state': 'New Mexico'})
item = response['Item']

if 'summary' in item:
    table.update_item(
        Key={'state': 'New Mexico'},
        UpdateExpression='SET #content = :content, #updated = :updated REMOVE summary, last_updated',
        ExpressionAttributeNames={'#content': 'content', '#updated': 'updated_at'},
        ExpressionAttributeValues={':content': item['summary'], ':updated': item.get('last_updated', '2025-01-01')}
    )
    print(f"Fixed New Mexico: {len(item['summary'])} chars")
else:
    print("Already fixed")
