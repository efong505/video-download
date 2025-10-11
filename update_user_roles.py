import boto3

# Update users table to support super_user role
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('users')

try:
    # Scan all users to update role field if needed
    response = users_table.scan()
    users = response.get('Items', [])
    
    print(f"Found {len(users)} users")
    
    # Check if any user needs role field update
    for user in users:
        if 'role' not in user:
            # Add default role for existing users
            users_table.update_item(
                Key={'user_id': user['user_id']},
                UpdateExpression='SET #role = :role',
                ExpressionAttributeNames={'#role': 'role'},
                ExpressionAttributeValues={':role': 'user'}
            )
            print(f"Updated user {user['email']} with default role")
    
    print("User role update complete")
    
except Exception as e:
    print(f"Error: {e}")