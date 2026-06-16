import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Use default account (wrong account)
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

tables = [
    'media-bias-tracker',
    'fake-news-reports',
    'corporate-wokeness-tracker',
    'political-corruption-tracker'
]

print("Deleting tables from wrong account (372110294325)...\n")

for table_name in tables:
    try:
        dynamodb.delete_table(TableName=table_name)
        print(f"✓ Deleted table: {table_name}")
    except dynamodb.exceptions.ResourceNotFoundException:
        print(f"⚠ Table {table_name} not found (already deleted or doesn't exist)")
    except Exception as e:
        print(f"✗ Error deleting {table_name}: {e}")

print("\n✅ Cleanup complete")
