import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table(
    TableName='events',
    KeySchema=[
        {'AttributeName': 'event_id', 'KeyType': 'HASH'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'event_id', 'AttributeType': 'S'}
    ],
    BillingMode='PAY_PER_REQUEST'
)

print('Creating events table...')
table.wait_until_exists()
print('Events table created successfully!')
