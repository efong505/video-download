"""
Send Newsletter to All Subscribers
Use this script to send email campaigns to your subscriber list
"""

import boto3
import base64
import argparse
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='us-east-1')
subscribers_table = dynamodb.Table('email-subscribers')

DOMAIN = 'https://christianconservativestoday.com'
FROM_EMAIL = 'Christian Conservatives Today <contact@christianconservativestoday.com>'

def get_active_subscribers():
    """Get all active subscribers"""
    response = subscribers_table.scan(
        FilterExpression='#status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'active'}
    )
    return [item['email'] for item in response['Items']]

def create_tracked_link(email, campaign_id, destination_url):
    """Create tracked link for click tracking"""
    data = f"{email}|{campaign_id}|{destination_url}"
    tracking_id = base64.urlsafe_b64encode(data.encode()).decode()
    return f"{DOMAIN}/track/click/{tracking_id}"

def encode_tracking_id(email, campaign_id):
    """Encode email and campaign into tracking ID"""
    data = f"{email}|{campaign_id}"
    return base64.urlsafe_b64encode(data.encode()).decode()

def send_newsletter(subject, html_content, campaign_id, test_mode=False):
    """
    Send newsletter to all subscribers
    
    Args:
        subject: Email subject line
        html_content: HTML email body (use {election_map_link} and {pixel_url} placeholders)
        campaign_id: Unique campaign identifier
        test_mode: If True, only send to first 5 subscribers
    """
    subscribers = get_active_subscribers()
    
    if test_mode:
        subscribers = subscribers[:5]
        print(f"TEST MODE: Sending to {len(subscribers)} subscribers only")
    else:
        print(f"Sending to {len(subscribers)} subscribers...")
    
    sent_count = 0
    failed_count = 0
    
    for email in subscribers:
        try:
            # Generate tracking pixel
            tracking_id = encode_tracking_id(email, campaign_id)
            pixel_url = f"{DOMAIN}/track/open/{tracking_id}"
            
            # Generate tracked links
            election_map_link = create_tracked_link(email, campaign_id, f"{DOMAIN}/election-map.html")
            unsubscribe_link = f"{DOMAIN}/unsubscribe?email={email}"
            
            # Replace placeholders in HTML
            personalized_html = html_content.format(
                email=email,
                election_map_link=election_map_link,
                unsubscribe_link=unsubscribe_link,
                pixel_url=pixel_url,
                domain=DOMAIN
            )
            
            # Add footer if not present
            if 'unsubscribe' not in personalized_html.lower():
                personalized_html += f"""
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 12px; color: #999;">
                    <a href="{unsubscribe_link}">Unsubscribe</a> | 
                    <a href="{DOMAIN}">Visit Website</a>
                </p>
                """
            
            # Add tracking pixel if not present
            if pixel_url not in personalized_html:
                personalized_html += f'<img src="{pixel_url}" width="1" height="1" style="display:none;" alt="">'
            
            # Send email
            ses.send_email(
                Source=FROM_EMAIL,
                Destination={'ToAddresses': [email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Html': {'Data': personalized_html}}
                }
            )
            
            sent_count += 1
            print(f"✓ Sent to {email}")
            
        except Exception as e:
            failed_count += 1
            print(f"✗ Failed to send to {email}: {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"Campaign: {campaign_id}")
    print(f"Successfully sent: {sent_count}")
    print(f"Failed: {failed_count}")
    print(f"{'='*60}")

# Example newsletter templates
EXAMPLE_ELECTION_UPDATE = """
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: white; padding: 30px; border-radius: 10px;">
        <h2 style="color: #667eea;">🗳️ Election Update: January 2025</h2>
        
        <p>Dear Christian Conservative Voter,</p>
        
        <p>We have important updates on upcoming elections in your state:</p>
        
        <h3 style="color: #667eea;">📍 New Candidates Added</h3>
        <ul>
            <li>Pro-life candidates in 15 new races</li>
            <li>Updated faith statements from key candidates</li>
            <li>New voter guides for 5 states</li>
        </ul>
        
        <h3 style="color: #667eea;">📅 Important Dates</h3>
        <ul>
            <li><strong>Feb 1:</strong> Voter registration deadline (TX, FL)</li>
            <li><strong>Feb 15:</strong> Early voting begins (GA, NC)</li>
            <li><strong>Mar 5:</strong> Primary elections (10 states)</li>
        </ul>
        
        <div style="text-align: center; margin: 30px 0;">
            <a href="{election_map_link}" 
               style="display: inline-block; background: #667eea; color: white; 
                      padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                View Updated Election Map
            </a>
        </div>
        
        <p>Stay informed and vote your values!</p>
        
        <p>God bless,<br>Christian Conservatives Today Team</p>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send newsletter to subscribers')
    parser.add_argument('--subject', required=True, help='Email subject line')
    parser.add_argument('--campaign', required=True, help='Campaign ID (e.g., jan-2025-update)')
    parser.add_argument('--test', action='store_true', help='Test mode (send to 5 subscribers only)')
    parser.add_argument('--template', choices=['election-update'], help='Use predefined template')
    
    args = parser.parse_args()
    
    # Use template or custom HTML
    if args.template == 'election-update':
        html_content = EXAMPLE_ELECTION_UPDATE
    else:
        print("No template specified. Using example template.")
        print("To customize, edit this script or provide HTML content.")
        html_content = EXAMPLE_ELECTION_UPDATE
    
    # Confirm before sending
    if not args.test:
        confirm = input(f"\nSend '{args.subject}' to ALL subscribers? (yes/no): ")
        if confirm.lower() != 'yes':
            print("Cancelled.")
            exit()
    
    # Send newsletter
    send_newsletter(args.subject, html_content, args.campaign, args.test)
