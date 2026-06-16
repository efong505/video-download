import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.client('dynamodb', region_name='us-east-1')

table_name = 'prayer-responses'

try:
    # Check if table exists
    dynamodb.describe_table(TableName=table_name)
    print(f"✅ Table '{table_name}' already exists")
except dynamodb.exceptions.ResourceNotFoundException:
    # Create table
    print(f"Creating table '{table_name}'...")
    
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'response_id', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'response_id', 'AttributeType': 'S'},
            {'AttributeName': 'request_id', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'request-index',
                'KeySchema': [
                    {'AttributeName': 'request_id', 'KeyType': 'HASH'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    
    print(f"✅ Table '{table_name}' created successfully")
    print("⏳ Waiting for table to become active...")
    
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName=table_name)
    
    print(f"✅ Table '{table_name}' is now active")
