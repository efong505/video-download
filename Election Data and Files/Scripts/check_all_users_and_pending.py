import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
users_table = dynamodb.Table('users')
contributors_table = dynamodb.Table('contributors')
pending_changes_table = dynamodb.Table('pending-changes')

print("=== ALL USERS ===")
response = users_table.scan()
for user in response['Items']:
    print(f"\nEmail: {user['email']}")
    print(f"  User ID: {user['user_id']}")
    print(f"  Role: {user.get('role', 'NOT SET')}")

print("\n\n=== ALL CONTRIBUTORS ===")
response = contributors_table.scan()
for contrib in response['Items']:
    print(f"\nEmail: {contrib['user_email']}")
    print(f"  State: {contrib['state']}")
    print(f"  Status: {contrib['status']}")
    print(f"  Bypass Approval: {contrib.get('bypass_approval', False)}")

print("\n\n=== ALL PENDING CHANGES ===")
response = pending_changes_table.scan()
print(f"Total changes in table: {len(response['Items'])}")
for change in response['Items']:
    print(f"\nChange ID: {change['change_id']}")
    print(f"  Type: {change['change_type']}")
    print(f"  Status: {change['status']}")
    print(f"  Submitted by: {change['submitted_by']}")
    print(f"  State: {change.get('state', 'N/A')}")
    print(f"  Submitted at: {change['submitted_at']}")
    if change['status'] == 'pending':
        print("  *** NEEDS REVIEW ***")
