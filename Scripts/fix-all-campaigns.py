import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Map campaign IDs to their content (from check-campaigns.py output)
campaigns = {
    '40aee2fb-951b-4563-9034-a043da9a9e05': {
        'name': 'Transition #1 - Welcome Back',
        'sequence': 1,
        'delay_days': 0
    },
    '3c2802b2-7306-4480-86a5-fb2a4becfd50': {
        'name': 'Transition #2 - The 7 Mountains',
        'sequence': 2,
        'delay_days': 3
    },
    'd7997cdf-8285-4002-a3b1-8a5c14478502': {
        'name': 'Transition #3 - AI is Changing Everything',
        'sequence': 3,
        'delay_days': 5
    },
    'e2640592-a7ee-43b1-bb51-27b77b41d93e': {
        'name': 'Transition #4 - The Book Reveal',
        'sequence': 4,
        'delay_days': 7
    },
    'ff51b71a-8a1e-4a2c-8a8a-32799695416e': {
        'name': 'Transition #5 - Free AI Survival Kit',
        'sequence': 5,
        'delay_days': 10
    },
    '53c979fb-e9ec-4c39-aefe-934856057b0f': {
        'name': 'Transition #6 - Last Chance',
        'sequence': 6,
        'delay_days': 14
    },
    '8a36b5d4-1f0c-4dfb-9990-1e0c9d042450': {
        'name': 'Transition #7 - Stay Connected',
        'sequence': 7,
        'delay_days': 17
    }
}

# Read HTML content from the original creation scripts
from pathlib import Path

# Get HTML from part1 script
part1_path = Path(__file__).parent / 'create-transition-campaigns-part1.py'
part2_path = Path(__file__).parent / 'create-transition-campaigns-part2.py'
part3_path = Path(__file__).parent / 'create-transition-campaigns-part3.py'

print("Fixing all 7 transition campaigns...\n")

# For each campaign, extract HTML from original scripts and update
for campaign_id, info in campaigns.items():
    try:
        # Read the original script to extract HTML
        if info['sequence'] <= 2:
            script_content = part1_path.read_text(encoding='utf-8')
        elif info['sequence'] <= 4:
            script_content = part2_path.read_text(encoding='utf-8')
        else:
            script_content = part3_path.read_text(encoding='utf-8')
        
        # Extract HTML between 'content': ''' and ''',
        start_marker = f"campaign_{info['sequence']} = {{"
        end_marker = "'status': 'active'"
        
        start_idx = script_content.find(start_marker)
        if start_idx == -1:
            print(f"⚠️  Could not find campaign_{info['sequence']} in script")
            continue
            
        content_start = script_content.find("'content': '''", start_idx)
        if content_start == -1:
            print(f"⚠️  Could not find content for campaign_{info['sequence']}")
            continue
            
        content_start += len("'content': '''")
        content_end = script_content.find("'''", content_start)
        
        html_content = script_content[content_start:content_end].strip()
        
        # Update DynamoDB
        campaigns_table.update_item(
            Key={
                'user_id': PLATFORM_OWNER_ID,
                'campaign_id': campaign_id
            },
            UpdateExpression='SET html_content = :html, sequence_number = :seq, delay_days = :delay',
            ExpressionAttributeValues={
                ':html': html_content,
                ':seq': info['sequence'],
                ':delay': info['delay_days']
            }
        )
        
        print(f"✅ Fixed: {info['name']} (seq #{info['sequence']}, {len(html_content)} chars)")
        
    except Exception as e:
        print(f"❌ Error fixing {campaign_id}: {e}")

print("\n✅ Done! Run check-campaigns.py to verify.")
