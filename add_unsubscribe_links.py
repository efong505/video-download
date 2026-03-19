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
print(f"Found {len(campaigns)} drip campaigns")

unsubscribe_footer = """
<hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

<p style="font-size: 12px; color: #999; line-height: 1.6; text-align: center;">
    You're receiving this email because you signed up for the Christian AI Survival Kit.<br>
    <a href="https://christianconservativestoday.com/manage-email-preferences.html?email={{subscriber_email}}" style="color: #667eea;">Manage Preferences</a> | 
    <a href="https://christianconservativestoday.com/manage-email-preferences.html?email={{subscriber_email}}" style="color: #667eea;">Unsubscribe</a>
</p>
"""

for campaign in campaigns:
    campaign_id = campaign['campaign_id']
    html_content = campaign.get('html_content', '')
    
    # Check if unsubscribe link already exists
    if 'manage-email-preferences' in html_content:
        print(f"Campaign {campaign_id[:8]}... already has unsubscribe link")
        continue
    
    # Add unsubscribe footer before closing body tag
    if '</body>' in html_content:
        updated_html = html_content.replace('</body>', f'{unsubscribe_footer}</body>')
    else:
        updated_html = html_content + unsubscribe_footer
    
    # Update campaign
    campaigns_table.update_item(
        Key={'user_id': user_id, 'campaign_id': campaign_id},
        UpdateExpression='SET html_content = :html',
        ExpressionAttributeValues={':html': updated_html}
    )
    
    print(f"Updated campaign {campaign_id[:8]}... (Sequence {campaign.get('sequence_number')})")

print("\nAll campaigns updated with unsubscribe links!")
