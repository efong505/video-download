import boto3
import sys

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.client('dynamodb', region_name='us-east-1')

tables = [
    {
        'name': 'media-bias-tracker',
        'pk': 'report_id'
    },
    {
        'name': 'fake-news-reports',
        'pk': 'report_id'
    },
    {
        'name': 'corporate-wokeness-tracker',
        'pk': 'report_id'
    },
    {
        'name': 'political-corruption-tracker',
        'pk': 'report_id'
    }
]

for table_config in tables:
    table_name = table_config['name']
    pk = table_config['pk']
    
    try:
        print(f"Creating table: {table_name}...")
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': pk, 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': pk, 'AttributeType': 'S'}
            ],
            BillingMode='PAY_PER_REQUEST'
        )
        print(f"✓ Table {table_name} created successfully")
    except dynamodb.exceptions.ResourceInUseException:
        print(f"⚠ Table {table_name} already exists")
    except Exception as e:
        print(f"✗ Error creating table {table_name}: {e}")

print("\n✅ All tables processed")
