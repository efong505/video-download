import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.client('dynamodb')

tables_to_delete = [
    'users-restored-20260405',
    'users-restored-20260412',
    'user-email-events-restored',
    'user-email-events-yesterday'
]

print("🗑️  Deleting restored backup tables...\n")

for table_name in tables_to_delete:
    try:
        print(f"Deleting {table_name}...", end=' ')
        dynamodb.delete_table(TableName=table_name)
        print("✅ Deleted")
    except dynamodb.exceptions.ResourceNotFoundException:
        print("⚠️  Already deleted")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n✅ Cleanup complete!")
