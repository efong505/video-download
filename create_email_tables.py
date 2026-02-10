import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Table 1: user-email-subscribers
print("Creating user-email-subscribers table...")
try:
    table = dynamodb.create_table(
        TableName='user-email-subscribers',
        KeySchema=[
            {'AttributeName': 'user_id', 'KeyType': 'HASH'},
            {'AttributeName': 'subscriber_email', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'subscriber_email', 'AttributeType': 'S'},
            {'AttributeName': 'status', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'status-index',
                'KeySchema': [
                    {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'status', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'}
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    table.wait_until_exists()
    print("[OK] user-email-subscribers created")
except Exception as e:
    print(f"[ERROR] {e}")

# Table 2: user-email-campaigns
print("\nCreating user-email-campaigns table...")
try:
    table = dynamodb.create_table(
        TableName='user-email-campaigns',
        KeySchema=[
            {'AttributeName': 'user_id', 'KeyType': 'HASH'},
            {'AttributeName': 'campaign_id', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'campaign_id', 'AttributeType': 'S'},
            {'AttributeName': 'status', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'status-index',
                'KeySchema': [
                    {'AttributeName': 'user_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'status', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'}
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    table.wait_until_exists()
    print("[OK] user-email-campaigns created")
except Exception as e:
    print(f"[ERROR] {e}")

# Table 3: user-email-events
print("\nCreating user-email-events table...")
try:
    table = dynamodb.create_table(
        TableName='user-email-events',
        KeySchema=[
            {'AttributeName': 'user_id', 'KeyType': 'HASH'},
            {'AttributeName': 'event_id', 'KeyType': 'RANGE'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'user_id', 'AttributeType': 'S'},
            {'AttributeName': 'event_id', 'AttributeType': 'S'},
            {'AttributeName': 'campaign_id', 'AttributeType': 'S'},
            {'AttributeName': 'timestamp', 'AttributeType': 'N'},
            {'AttributeName': 'subscriber_email', 'AttributeType': 'S'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'campaign-index',
                'KeySchema': [
                    {'AttributeName': 'campaign_id', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'}
            },
            {
                'IndexName': 'email-index',
                'KeySchema': [
                    {'AttributeName': 'subscriber_email', 'KeyType': 'HASH'},
                    {'AttributeName': 'timestamp', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'}
            }
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    table.wait_until_exists()
    print("[OK] user-email-events created")
except Exception as e:
    print(f"[ERROR] {e}")

print("\n[OK] All tables created successfully!")
