import boto3
from datetime import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

# Check the old newsletter subscribers table
subscribers_table = dynamodb.Table('email_subscribers')

try:
    response = subscribers_table.get_item(Key={'email': 'ekewaka@gmail.com'})
    
    if 'Item' in response:
        print("✅ Found subscription in email_subscribers table:")
        print("-" * 80)
        subscriber = response['Item']
        for key, value in sorted(subscriber.items()):
            print(f"   {key}: {value}")
    else:
        print("❌ No subscription found for ekewaka@gmail.com in email_subscribers table")
        
        # Show recent subscribers
        print("\n📋 Showing last 10 subscribers from email_subscribers table:")
        scan_response = subscribers_table.scan()
        all_subs = scan_response.get('Items', [])
        
        # Sort by subscribed_at if available
        try:
            sorted_subs = sorted(all_subs, key=lambda x: x.get('subscribed_at', ''), reverse=True)
        except:
            sorted_subs = all_subs
        
        for sub in sorted_subs[:10]:
            email = sub.get('email', 'N/A')
            status = sub.get('status', 'N/A')
            subscribed_at = sub.get('subscribed_at', 'N/A')
            print(f"   - {email} | Status: {status} | Subscribed: {subscribed_at}")

except Exception as e:
    print(f"❌ Error: {e}")
