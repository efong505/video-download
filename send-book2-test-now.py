import boto3
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

email = "hawaiianintucson@gmail.com"

print(f"📧 Sending Book 2 Email 1 to: {email}")
print("="*70)

session = boto3.Session(profile_name='ekewaka')
lambda_client = session.client('lambda', region_name='us-east-1')

# Manually invoke email sender with first campaign
payload = {
    "action": "send_next_drip",
    "email": email,
    "campaign_group": "book2-launch-sequence"
}

print(f"\n🚀 Invoking email-subscription-handler...")
print(f"Sending Email 1: 'AI is here — but who is directing it?'\n")

try:
    response = lambda_client.invoke(
        FunctionName='email-subscription-handler',
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    
    result = json.loads(response['Payload'].read())
    print("✅ Response:")
    print(json.dumps(result, indent=2))
    
    if result.get('statusCode') == 200:
        print(f"\n✅ EMAIL SENT!")
        print(f"\n📧 Check hawaiianintucson@gmail.com inbox for:")
        print(f"   From: Christian Conservatives Today")
        print(f"   Subject: 'AI is here — but who is directing it?'")
        print(f"\n✅ Test these links:")
        print(f"   • Amazon link")
        print(f"   • Lulu link")
        print(f"   • Book page link")
        print(f"   • Unsubscribe link")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
