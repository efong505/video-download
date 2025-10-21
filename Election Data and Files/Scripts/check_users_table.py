import boto3
import json

db = boto3.resource('dynamodb', region_name='us-east-1')
users_table = db.Table('users')

response = users_table.scan(Limit=5)
users = response.get('Items', [])

print(f"Found {len(users)} users (showing first 5)")
print("\nUser fields:")
for user in users:
    print(json.dumps(user, indent=2, default=str))
    print("-" * 50)
