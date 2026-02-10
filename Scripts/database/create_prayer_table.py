import boto3

dynamodb = boto3.client('dynamodb', region_name='us-east-1')

table_name = 'prayer-requests'

try:
    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'request_id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'request_id', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    print(f"Table {table_name} created successfully")
except dynamodb.exceptions.ResourceInUseException:
    print(f"Table {table_name} already exists")
