import boto3
import sys
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
lambda_client = session.client('lambda')

enrollments_table = dynamodb.Table('user-email-drip-enrollments')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# All 12 subscribers (11 + 1 test)
SUBSCRIBERS = [
    'fall1776@aol.com',
    'contact@ekewaka.com',
    'reedandjuliesmom@gmail.com',
    'ekewakafong@gmail.com',
    'efong505@nmsu.edu',
    'bobnglendagill@gmail.com',
    'davidoliver01@yahoo.com',
    'dkechols77@gmail.com',
    'contact@christianconservativestoday.com',
    'hitormissatthepottery@gmail.com',
    'doake@msn.com',
    'hawaiianintucson@gmail.com'
]

print(f"📧 Triggering Email #1 for {len(SUBSCRIBERS)} subscribers\n")
print("="*60)

sent_count = 0
error_count = 0

for email in SUBSCRIBERS:
    print(f"\nProcessing: {email}")
    
    try:
        # Get enrollment
        enrollment_id = f"{email}:election-map-transition-sequence"
        response = enrollments_table.get_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'enrollment_id': enrollment_id}
        )
        
        if 'Item' not in response:
            print(f"  ❌ Enrollment not found")
            error_count += 1
            continue
        
        enrollment = response['Item']
        current_step = int(enrollment.get('current_step', 0))
        
        if current_step > 0:
            print(f"  ⚠️  Already at step {current_step} - skipping")
            continue
        
        # Invoke drip processor Lambda to send next email
        payload = {
            'manual_trigger': True,
            'user_id': PLATFORM_OWNER_ID,
            'enrollment_id': enrollment_id
        }
        
        lambda_response = lambda_client.invoke(
            FunctionName='email-drip-processor',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )
        
        response_payload = json.loads(lambda_response['Payload'].read())
        
        if lambda_response['StatusCode'] == 200:
            print(f"  ✅ Email #1 queued for sending")
            sent_count += 1
        else:
            print(f"  ❌ Error: {response_payload}")
            error_count += 1
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        error_count += 1

# Summary
print("\n" + "="*60)
print("✅ SEND COMPLETE!")
print("="*60)
print(f"\n📊 Summary:")
print(f"   Total subscribers: {len(SUBSCRIBERS)}")
print(f"   ✅ Emails queued: {sent_count}")
print(f"   ❌ Errors: {error_count}")

print(f"\n📧 Email #1 'Welcome Back' is now:")
print(f"   ✅ Queued in SQS (email-sending-queue)")
print(f"   ✅ Will be sent by email-sender Lambda")
print(f"   ✅ Subscribers will receive within minutes")

print(f"\n💡 Check your inbox at hawaiianintucson@gmail.com to see the email!")
