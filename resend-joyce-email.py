import boto3
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# This will manually invoke the email drip processor to send the next email
# for joycewilliam478@hotmail.com

email = 'joycewilliam478@hotmail.com'

# Invoke the drip processor Lambda to process this subscriber
lambda_client = boto3.Session(profile_name='ekewaka').client('lambda', region_name='us-east-1')

# Create a test event to trigger processing for this specific subscriber
event = {
    "test_mode": True,
    "target_email": email
}

print(f"🚀 Triggering email drip processor for {email}...")
print(f"📧 This will send the next scheduled email in their sequence\n")

try:
    response = lambda_client.invoke(
        FunctionName='email-drip-processor',
        InvocationType='RequestResponse',
        Payload=json.dumps(event)
    )
    
    result = json.loads(response['Payload'].read())
    print("✅ Response:")
    print(json.dumps(result, indent=2))
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n" + "="*60)
    print("ALTERNATIVE: Use the Campaign Manager")
    print("="*60)
    print(f"1. Open: campaign-manager.html")
    print(f"2. Go to 'Enrollments' tab")
    print(f"3. Search for: {email}")
    print(f"4. Click '⚡ Send Next Now' button")
    print(f"\nThis will immediately send the next email in their sequence")
