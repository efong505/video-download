import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

email = 'joycewilliam478@hotmail.com'
region = 'us-east-1'

ddb = boto3.resource('dynamodb', region_name=region)

# Check book-subscribers table
print(f"🔍 Searching for {email}...\n")

book_table = ddb.Table('book-subscribers')
try:
    response = book_table.scan(
        FilterExpression='contains(email, :email)',
        ExpressionAttributeValues={':email': email}
    )
    if response['Items']:
        print("✅ Found in book-subscribers:")
        for item in response['Items']:
            print(f"   Email: {item.get('email')}")
            print(f"   Subscribed: {item.get('subscribed_at')}")
            print(f"   Source: {item.get('source', 'N/A')}")
            print(f"   Book delivered: {item.get('book_delivered', False)}")
            print()
    else:
        print("❌ NOT found in book-subscribers\n")
except Exception as e:
    print(f"❌ Error checking book-subscribers: {e}\n")

# Check user-email-drip-enrollments
enrollments_table = ddb.Table('user-email-drip-enrollments')
try:
    response = enrollments_table.scan()
    matching = [item for item in response['Items'] if email in item.get('enrollment_id', '')]
    
    if matching:
        print("✅ Found in user-email-drip-enrollments:")
        for item in matching:
            print(f"   Enrollment ID: {item.get('enrollment_id')}")
            print(f"   Campaign Group: {item.get('campaign_group')}")
            print(f"   Current Step: {item.get('current_step')}")
            print(f"   Status: {item.get('status')}")
            print(f"   Next Send: {item.get('next_send_date')}")
            print()
    else:
        print("❌ NOT found in user-email-drip-enrollments\n")
except Exception as e:
    print(f"❌ Error checking enrollments: {e}\n")

# Check email-subscribers (old table)
email_subscribers_table = ddb.Table('email-subscribers')
try:
    response = email_subscribers_table.scan(
        FilterExpression='contains(email, :email)',
        ExpressionAttributeValues={':email': email}
    )
    if response['Items']:
        print("✅ Found in email-subscribers:")
        for item in response['Items']:
            print(f"   Email: {item.get('email')}")
            print(f"   Subscribed: {item.get('subscribed_at')}")
            print()
    else:
        print("❌ NOT found in email-subscribers\n")
except Exception as e:
    print(f"❌ Error checking email-subscribers: {e}\n")

print("\n" + "="*60)
print("To resend the welcome email, I need to know which campaign")
print("group this person should be in:")
print("  1. pre-purchase-book-sequence (for book survival kit signups)")
print("  2. post-purchase-sequence (for book purchasers)")
