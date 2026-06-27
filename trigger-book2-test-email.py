import boto3
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("⚡ Triggering Email Drip Processor for Book 2 Test")
print("="*70)

session = boto3.Session(profile_name='ekewaka')
lambda_client = session.client('lambda', region_name='us-east-1')

print("\n🚀 Invoking email-drip-processor Lambda...")
print("This will process all active enrollments and send next emails\n")

try:
    response = lambda_client.invoke(
        FunctionName='email-drip-processor',
        InvocationType='RequestResponse',
        Payload=json.dumps({})
    )
    
    result = json.loads(response['Payload'].read())
    
    print("✅ Lambda Response:")
    print(json.dumps(result, indent=2))
    
    if result.get('statusCode') == 200:
        body = json.loads(result.get('body', '{}'))
        print(f"\n📊 Results:")
        print(f"   Enrollments processed: {body.get('enrollments_processed', 0)}")
        print(f"   Emails sent: {body.get('emails_sent', 0)}")
        
        if body.get('emails_sent', 0) > 0:
            print("\n✅ Email sent successfully!")
            print("\n📧 Check your inbox for:")
            print("   Subject: 'AI is here — but who is directing it?'")
            print("   From: Christian Conservatives Today")
        else:
            print("\n⚠️  No emails sent")
            print("   This might mean:")
            print("   • No active enrollments found")
            print("   • delay_hours not yet passed")
            print("   • Check enrollment status")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
