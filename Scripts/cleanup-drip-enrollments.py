"""Clean up orphaned drip enrollments and malformed test data."""
import boto3

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
ddb = session.resource('dynamodb')
enrollments_table = ddb.Table('user-email-drip-enrollments')
subscribers_table = ddb.Table('book-subscribers')

# Get all valid subscriber emails
resp = subscribers_table.scan()
valid_emails = {s['email'] for s in resp['Items']}
print(f"Valid subscribers: {len(valid_emails)}")
print(f"  {', '.join(sorted(valid_emails))}")

# Get all enrollments
resp = enrollments_table.scan()
enrollments = resp['Items']
print(f"\nTotal enrollments: {len(enrollments)}")

deleted = 0
for e in enrollments:
    enrollment_id = e['enrollment_id']
    user_id = e['user_id']
    
    # Extract email from enrollment_id (format: email#campaign or email_campaign)
    email = enrollment_id.split('#')[0].split('_')[0]
    
    # Delete if:
    # 1. Email not in valid subscribers
    # 2. Email contains template syntax ({{ or $()
    # 3. Email is a test email that should be removed
    should_delete = False
    reason = ""
    
    if '{{' in email or '$(get-date' in email:
        should_delete = True
        reason = "malformed template syntax"
    elif email not in valid_emails and email.startswith('test-'):
        should_delete = True
        reason = "test email not in subscribers"
    
    if should_delete:
        print(f"  DELETE: {email} ({reason})")
        enrollments_table.delete_item(Key={'user_id': user_id, 'enrollment_id': enrollment_id})
        deleted += 1

print(f"\nDeleted {deleted} orphaned/malformed enrollments")
