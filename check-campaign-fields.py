import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

campaigns_table = dynamodb.Table('user-email-campaigns')

# Get the specific campaign
response = campaigns_table.get_item(
    Key={
        'user_id': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2',
        'campaign_id': '40aee2fb-951b-4563-9034-a043da9a9e05'  # Transition #1
    }
)

if 'Item' in response:
    campaign = response['Item']
    print("Campaign #1 - Transition #1 - Welcome Back")
    print("=" * 80)
    
    for key in sorted(campaign.keys()):
        value = campaign[key]
        if key in ['content', 'html_content']:
            print(f"\n{key}:")
            print(f"  Length: {len(str(value))} characters")
            print(f"  First 200 chars: {str(value)[:200]}...")
        else:
            print(f"{key}: {value}")
else:
    print("Campaign not found")
