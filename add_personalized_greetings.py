import boto3

profile = 'ekewaka'
region = 'us-east-1'
user_id = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

session = boto3.Session(profile_name=profile, region_name=region)
dynamodb = session.resource('dynamodb')
campaigns_table = dynamodb.Table('user-email-campaigns')

# Get all drip campaigns
response = campaigns_table.query(
    KeyConditionExpression='user_id = :uid',
    FilterExpression='attribute_exists(sequence_number)',
    ExpressionAttributeValues={':uid': user_id}
)

campaigns = response['Items']
print(f"Found {len(campaigns)} drip campaigns\n")

for campaign in campaigns:
    campaign_id = campaign['campaign_id']
    
    # Get content field (the main email content)
    content = campaign.get('content', '')
    
    if not content:
        print(f"Skipping {campaign_id[:8]}... - no content field")
        continue
    
    # Replace "Hey," with "Hey {{first_name}},"
    if '<p>Hey,</p>' in content:
        updated_content = content.replace('<p>Hey,</p>', '<p>Hey {{first_name}},</p>', 1)
    elif content.startswith('Hey,'):
        updated_content = content.replace('Hey,', 'Hey {{first_name}},', 1)
    else:
        print(f"Skipping {campaign_id[:8]}... - doesn't contain 'Hey,'")
        continue
    
    # Update the campaign
    campaigns_table.update_item(
        Key={'user_id': user_id, 'campaign_id': campaign_id},
        UpdateExpression='SET content = :content',
        ExpressionAttributeValues={':content': updated_content}
    )
    
    print(f"Updated campaign {campaign_id[:8]}... (Sequence {campaign.get('sequence_number')})")
    print(f"  Changed: 'Hey,' -> 'Hey {{{{first_name}}}},'")

print("\nAll campaigns updated with personalized greetings!")
