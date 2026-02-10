import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table(
    TableName='video-playlists',
    KeySchema=[
        {'AttributeName': 'playlist_id', 'KeyType': 'HASH'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'playlist_id', 'AttributeType': 'S'}
    ],
    BillingMode='PAY_PER_REQUEST'
)

print('Creating video-playlists table...')
table.wait_until_exists()
print('Video playlists table created successfully!')
