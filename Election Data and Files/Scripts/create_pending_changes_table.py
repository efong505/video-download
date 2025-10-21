import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

# Create pending-changes table for editor submissions
table = dynamodb.create_table(
    TableName='pending-changes',
    KeySchema=[
        {'AttributeName': 'change_id', 'KeyType': 'HASH'}
    ],
    AttributeDefinitions=[
        {'AttributeName': 'change_id', 'AttributeType': 'S'}
    ],
    BillingMode='PAY_PER_REQUEST'
)

print("Creating pending-changes table...")
table.wait_until_exists()
print("Table created successfully!")
