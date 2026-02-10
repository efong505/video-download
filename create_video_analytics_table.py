import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table(
    TableName='video-analytics',
    KeySchema=[
        {'AttributeName': 'video_id', 'KeyType': 'HASH'},
        {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'video_id', 'AttributeType': 'S'},
        {'AttributeName': 'timestamp', 'AttributeType': 'N'}
    ],
    BillingMode='PAY_PER_REQUEST'
)

print('Creating video-analytics table...')
table.wait_until_exists()
print('Video analytics table created successfully!')
