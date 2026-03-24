"""
Create DynamoDB tables for 7 Mountains tracking system
Run this script once to set up the database infrastructure
"""

import boto3
from botocore.exceptions import ClientError

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.client('dynamodb')

def create_mountain_pledges_table():
    """Create table to track user pledges per mountain"""
    try:
        response = dynamodb.create_table(
            TableName='mountain-pledges',
            KeySchema=[
                {'AttributeName': 'user_id', 'KeyType': 'HASH'},  # Partition key
                {'AttributeName': 'mountain', 'KeyType': 'RANGE'}  # Sort key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'mountain', 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST',  # On-demand pricing
            Tags=[
                {'Key': 'Project', 'Value': '7Mountains'},
                {'Key': 'Environment', 'Value': 'Production'}
            ]
        )
        print("✅ Created mountain-pledges table")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("⚠️  mountain-pledges table already exists")
        else:
            print(f"❌ Error creating mountain-pledges: {e}")
            raise

def create_mountain_badges_table():
    """Create table to track user badges per mountain"""
    try:
        response = dynamodb.create_table(
            TableName='mountain-badges',
            KeySchema=[
                {'AttributeName': 'badge_id', 'KeyType': 'HASH'}  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'badge_id', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'mountain', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user-index',
                    'KeySchema': [
                        {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'mountain', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            BillingMode='PAY_PER_REQUEST',
            Tags=[
                {'Key': 'Project', 'Value': '7Mountains'},
                {'Key': 'Environment', 'Value': 'Production'}
            ]
        )
        print("✅ Created mountain-badges table")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("⚠️  mountain-badges table already exists")
        else:
            print(f"❌ Error creating mountain-badges: {e}")
            raise

def create_mountain_contributions_table():
    """Create table to track user contributions per mountain"""
    try:
        response = dynamodb.create_table(
            TableName='mountain-contributions',
            KeySchema=[
                {'AttributeName': 'contribution_id', 'KeyType': 'HASH'}  # Partition key
            ],
            AttributeDefinitions=[
                {'AttributeName': 'contribution_id', 'AttributeType': 'S'},
                {'AttributeName': 'user_id', 'AttributeType': 'S'},
                {'AttributeName': 'mountain', 'AttributeType': 'S'},
                {'AttributeName': 'contribution_date', 'AttributeType': 'S'}
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'user-index',
                    'KeySchema': [
                        {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                        {'AttributeName': 'contribution_date', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                },
                {
                    'IndexName': 'mountain-index',
                    'KeySchema': [
                        {'AttributeName': 'mountain', 'KeyType': 'HASH'},
                        {'AttributeName': 'contribution_date', 'KeyType': 'RANGE'}
                    ],
                    'Projection': {'ProjectionType': 'ALL'}
                }
            ],
            BillingMode='PAY_PER_REQUEST',
            Tags=[
                {'Key': 'Project', 'Value': '7Mountains'},
                {'Key': 'Environment', 'Value': 'Production'}
            ]
        )
        print("✅ Created mountain-contributions table")
        return response
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print("⚠️  mountain-contributions table already exists")
        else:
            print(f"❌ Error creating mountain-contributions: {e}")
            raise

def verify_tables():
    """Verify all tables were created successfully"""
    tables = ['mountain-pledges', 'mountain-badges', 'mountain-contributions']
    
    print("\n📊 Verifying tables...")
    for table_name in tables:
        try:
            response = dynamodb.describe_table(TableName=table_name)
            status = response['Table']['TableStatus']
            print(f"✅ {table_name}: {status}")
        except ClientError as e:
            print(f"❌ {table_name}: NOT FOUND")

if __name__ == '__main__':
    print("🏔️  Creating 7 Mountains DynamoDB Tables...\n")
    
    create_mountain_pledges_table()
    create_mountain_badges_table()
    create_mountain_contributions_table()
    
    print("\n⏳ Waiting for tables to become active...")
    print("This may take 30-60 seconds...\n")
    
    # Wait for tables to be active
    waiter = dynamodb.get_waiter('table_exists')
    for table in ['mountain-pledges', 'mountain-badges', 'mountain-contributions']:
        try:
            waiter.wait(TableName=table)
        except:
            pass
    
    verify_tables()
    
    print("\n✅ 7 Mountains database setup complete!")
    print("\nNext steps:")
    print("1. Deploy mountains_api Lambda function")
    print("2. Create API Gateway endpoints")
    print("3. Update frontend to call new APIs")
