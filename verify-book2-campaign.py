import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("🔍 Book 2 Campaign Verification")
print("="*70)

session = boto3.Session(profile_name='ekewaka')
ddb = session.resource('dynamodb', region_name='us-east-1')
table = ddb.Table('user-email-campaigns')

OWNER_ID = "effa3242-cf64-4021-b2b0-c8a5a9dfd6d2"
CAMPAIGN_GROUP = "book2-launch-sequence"

print(f"\n📋 Checking for: {CAMPAIGN_GROUP}")
print(f"Owner: {OWNER_ID}\n")

response = table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='campaign_group = :group',
    ExpressionAttributeValues={
        ':uid': OWNER_ID,
        ':group': CAMPAIGN_GROUP
    }
)

campaigns = sorted(response['Items'], key=lambda x: x['sequence_number'])

if not campaigns:
    print("❌ NO CAMPAIGNS FOUND!")
    print("\nRun the upload scripts:")
    print("  python upload-book2-campaign-part1.py")
    print("  python upload-book2-campaign-part2.py")
else:
    print(f"✅ Found {len(campaigns)} campaigns:\n")
    
    for c in campaigns:
        print(f"{'✓' if c['status'] == 'active' else '✗'} Email {c['sequence_number']}: {c['campaign_name']}")
        print(f"   Subject: {c['subject_line']}")
        print(f"   Delay: {c['delay_hours']} hours")
        print(f"   Status: {c['status']}")
        print(f"   Created: {c.get('created_at', 'N/A')}")
        print()

    print("="*70)
    if len(campaigns) == 7:
        print("🎉 ALL 7 EMAILS ARE UPLOADED!")
        print("\n✅ Campaign is ready for testing")
        print("\nNext: Create test enrollment")
        print("  python test-book2-enrollment.py")
    else:
        print(f"⚠️  Expected 7 emails, found {len(campaigns)}")
        print("Check if all uploads completed successfully")
