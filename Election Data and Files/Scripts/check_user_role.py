import boto3

db = boto3.resource('dynamodb', region_name='us-east-1')
users_table = db.Table('users')

email = input("Enter email to check: ").strip()

response = users_table.scan(
    FilterExpression='email = :email',
    ExpressionAttributeValues={':email': email}
)

if response['Items']:
    user = response['Items'][0]
    print(f"\nUser: {user.get('first_name', '')} {user.get('last_name', '')}")
    print(f"Email: {user['email']}")
    print(f"Role: {user.get('role', 'NO ROLE SET')}")
else:
    print(f"User {email} not found")
