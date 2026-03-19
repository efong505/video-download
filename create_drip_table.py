"""
Create user-email-drip-enrollments DynamoDB table
Run: python create_drip_table.py
"""
import boto3

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.client('dynamodb', region_name='us-east-1')

table_name = 'user-email-drip-enrollments'

print(f"Creating table: {table_name}...")

try:
    response = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'user_id', 'KeyType': 'HASH'},  # Partition key
            {'AttributeName': 'enrollment_id', 'KeyType': 'RANGE'}  # Sort key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'enrollment_id', 'AttributeType': 'S'},
            {'AttributeName': 'subscriber_email', 'AttributeType': 'S'},
            {'AttributeName': 'status', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'email-index',
                'KeySchema': [
                    {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'subscriber_email', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            },
            {
                'IndexName': 'status-index',
                'KeySchema': [
                    {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'status', 'KeyType': 'RANGE'}
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
    
    print(f"[OK] Table created: {table_name}")
    print("Waiting for table to become active...")
    
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName=table_name)
    
    print("[SUCCESS] Table is active!")
    
except dynamodb.exceptions.ResourceInUseException:
    print(f"[INFO] Table {table_name} already exists")
except Exception as e:
    print(f"[ERROR] {str(e)}")
