import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('users')
contributors_table = dynamodb.Table('contributors')
pending_changes_table = dynamodb.Table('pending-changes')

# Get user email to check
user_email = input("Enter user email to check: ")

# Check user role
print("\n=== USER ROLE ===")
response = users_table.scan(
    FilterExpression=Attr('email').eq(user_email)
)
if response['Items']:
    user = response['Items'][0]
    print(f"User ID: {user['user_id']}")
    print(f"Email: {user['email']}")
    print(f"Role: {user.get('role', 'NOT SET')}")
else:
    print(f"User {user_email} NOT FOUND in users table")

# Check contributor status
print("\n=== CONTRIBUTOR STATUS ===")
response = contributors_table.scan(
    FilterExpression=Attr('user_email').eq(user_email)
)
if response['Items']:
    for contrib in response['Items']:
        print(f"State: {contrib['state']}")
        print(f"Status: {contrib['status']}")
        print(f"Bypass Approval: {contrib.get('bypass_approval', False)}")
else:
    print(f"User {user_email} is NOT a contributor")

# Check pending changes
print("\n=== PENDING CHANGES ===")
response = pending_changes_table.scan(
    FilterExpression=Attr('status').eq('pending')
)
if response['Items']:
    print(f"Total pending changes: {len(response['Items'])}")
    for change in response['Items']:
        print(f"\nChange ID: {change['change_id']}")
        print(f"Type: {change['change_type']}")
        print(f"Submitted by: {change['submitted_by']}")
        print(f"State: {change.get('state', 'N/A')}")
        print(f"Submitted at: {change['submitted_at']}")
else:
    print("No pending changes found")

# Check ALL pending changes (including approved/denied)
print("\n=== ALL CHANGES (including approved/denied) ===")
response = pending_changes_table.scan()
if response['Items']:
    print(f"Total changes: {len(response['Items'])}")
    for change in response['Items']:
        print(f"\nChange ID: {change['change_id']}")
        print(f"Type: {change['change_type']}")
        print(f"Status: {change['status']}")
        print(f"Submitted by: {change['submitted_by']}")
else:
    print("No changes found in table")
