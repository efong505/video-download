import boto3
import sys

db = boto3.resource('dynamodb', region_name='us-east-1')
users_table = db.Table('users')

def assign_editor_role(email):
    """Assign editor role to a user"""
    try:
        # Find user by email
        response = users_table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        
        if not response['Items']:
            print(f"User {email} not found")
            return
        
        user = response['Items'][0]
        user_id = user['user_id']
        
        # Update using correct key
        users_table.update_item(
            Key={'user_id': user_id},
            UpdateExpression='SET #role = :role',
            ExpressionAttributeNames={'#role': 'role'},
            ExpressionAttributeValues={':role': 'editor'}
        )
        print(f"Editor role assigned to {email}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python assign_editor_role.py <email>")
        print("Example: python assign_editor_role.py editor@example.com")
        sys.exit(1)
    
    assign_editor_role(sys.argv[1])
