"""
Subscriber List Management
View, export, and manage email subscribers
"""

import boto3
import csv
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
subscribers_table = dynamodb.Table('email-subscribers')

def list_subscribers(status='active'):
    """List all subscribers with given status"""
    response = subscribers_table.scan()
    subscribers = response['Items']
    
    # Filter by status if specified
    if status:
        subscribers = [s for s in subscribers if s.get('status') == status]
    
    # Sort by subscription date
    subscribers.sort(key=lambda x: x.get('subscribed_at', ''), reverse=True)
    
    print(f"\n{'='*80}")
    print(f"SUBSCRIBERS ({status.upper()}): {len(subscribers)}")
    print(f"{'='*80}\n")
    
    for i, sub in enumerate(subscribers, 1):
        print(f"{i}. {sub['email']}")
        print(f"   Subscribed: {sub.get('subscribed_at', 'Unknown')}")
        print(f"   Opens: {sub.get('total_opens', 0)} | Clicks: {sub.get('total_clicks', 0)}")
        print(f"   Last Activity: {sub.get('last_activity', 'None')}")
        print()
    
    return subscribers

def export_subscribers(filename='subscribers.csv', status='active'):
    """Export subscribers to CSV"""
    response = subscribers_table.scan()
    subscribers = response['Items']
    
    if status:
        subscribers = [s for s in subscribers if s.get('status') == status]
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Email', 'Status', 'Subscribed Date', 'Source', 'Total Opens', 'Total Clicks', 'Last Activity'])
        
        for sub in subscribers:
            writer.writerow([
                sub['email'],
                sub.get('status', 'active'),
                sub.get('subscribed_at', ''),
                sub.get('source', ''),
                sub.get('total_opens', 0),
                sub.get('total_clicks', 0),
                sub.get('last_activity', '')
            ])
    
    print(f"\n✓ Exported {len(subscribers)} subscribers to {filename}")

def unsubscribe_email(email):
    """Unsubscribe an email address"""
    try:
        subscribers_table.update_item(
            Key={'email': email},
            UpdateExpression='SET #status = :status, unsubscribed_at = :date',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'unsubscribed',
                ':date': datetime.now().isoformat()
            }
        )
        print(f"✓ Unsubscribed: {email}")
    except Exception as e:
        print(f"✗ Error: {e}")

def resubscribe_email(email):
    """Resubscribe an email address"""
    try:
        subscribers_table.update_item(
            Key={'email': email},
            UpdateExpression='SET #status = :status REMOVE unsubscribed_at',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'active'}
        )
        print(f"✓ Resubscribed: {email}")
    except Exception as e:
        print(f"✗ Error: {e}")

def resend_welcome_email(email):
    """Resend welcome email to a subscriber"""
    import boto3
    import base64
    
    ses = boto3.client('ses', region_name='us-east-1')
    DOMAIN = 'https://christianconservativestoday.com'
    FROM_EMAIL = 'Christian Conservatives Today <contact@christianconservativestoday.com>'
    
    try:
        # Check if subscriber exists
        response = subscribers_table.get_item(Key={'email': email})
        if 'Item' not in response:
            print(f"✗ Email not found: {email}")
            return
        
        campaign_id = 'welcome-email-resend'
        tracking_id = base64.urlsafe_b64encode(f"{email}|{campaign_id}".encode()).decode()
        pixel_url = f"{DOMAIN}/track/open/{tracking_id}"
        
        election_map_data = f"{email}|{campaign_id}|{DOMAIN}/election-map.html"
        election_map_link = f"{DOMAIN}/track/click/{base64.urlsafe_b64encode(election_map_data.encode()).decode()}"
        unsubscribe_link = f"{DOMAIN}/unsubscribe?email={email}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
            <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h2 style="color: #667eea;">Welcome to Christian Conservatives Today! 🙏</h2>
                <p style="font-size: 16px; line-height: 1.6; color: #333;">Thank you for subscribing to our election updates and voter guides!</p>
                <ul style="font-size: 15px; line-height: 1.8; color: #555;">
                    <li>🗳️ <strong>Election updates</strong> and critical dates</li>
                    <li>📖 <strong>State-specific voter guides</strong> for all 50 states</li>
                    <li>🎯 <strong>Pro-life, pro-family candidate</strong> information</li>
                </ul>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{election_map_link}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">📍 View Interactive Election Map</a>
                </div>
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                <p style="font-size: 12px; color: #999;"><a href="{unsubscribe_link}" style="color: #667eea;">Unsubscribe</a></p>
            </div>
            <img src="{pixel_url}" width="1" height="1" style="display:none;" alt="">
        </body>
        </html>
        """
        
        ses.send_email(
            Source=FROM_EMAIL,
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': '🗳️ Welcome to Christian Conservatives Today!'},
                'Body': {'Html': {'Data': html_body}}
            }
        )
        print(f"✓ Welcome email resent to: {email}")
    except Exception as e:
        print(f"✗ Error: {e}")

def search_subscriber(email):
    """Search for a specific subscriber"""
    try:
        response = subscribers_table.get_item(Key={'email': email})
        if 'Item' in response:
            sub = response['Item']
            print(f"\n{'='*60}")
            print(f"SUBSCRIBER: {sub['email']}")
            print(f"{'='*60}")
            print(f"Status: {sub.get('status', 'active')}")
            print(f"Subscribed: {sub.get('subscribed_at', 'Unknown')}")
            print(f"Source: {sub.get('source', 'Unknown')}")
            print(f"Total Opens: {sub.get('total_opens', 0)}")
            print(f"Total Clicks: {sub.get('total_clicks', 0)}")
            print(f"Last Activity: {sub.get('last_activity', 'None')}")
            if sub.get('status') == 'unsubscribed':
                print(f"Unsubscribed: {sub.get('unsubscribed_at', 'Unknown')}")
            print()
        else:
            print(f"✗ Email not found: {email}")
    except Exception as e:
        print(f"✗ Error: {e}")

def get_stats():
    """Get subscriber statistics"""
    response = subscribers_table.scan()
    subscribers = response['Items']
    
    active = len([s for s in subscribers if s.get('status') == 'active'])
    unsubscribed = len([s for s in subscribers if s.get('status') == 'unsubscribed'])
    total_opens = sum(s.get('total_opens', 0) for s in subscribers)
    total_clicks = sum(s.get('total_clicks', 0) for s in subscribers)
    
    print(f"\n{'='*60}")
    print("SUBSCRIBER STATISTICS")
    print(f"{'='*60}")
    print(f"Total Subscribers: {len(subscribers)}")
    print(f"Active: {active}")
    print(f"Unsubscribed: {unsubscribed}")
    print(f"Total Opens: {total_opens}")
    print(f"Total Clicks: {total_clicks}")
    if active > 0:
        print(f"Avg Opens per Subscriber: {total_opens/active:.1f}")
        print(f"Avg Clicks per Subscriber: {total_clicks/active:.1f}")
    print()

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("\nSubscriber Management Tool")
        print("="*60)
        print("\nUsage:")
        print("  python manage_subscribers.py list [status]")
        print("  python manage_subscribers.py export [filename] [status]")
        print("  python manage_subscribers.py search <email>")
        print("  python manage_subscribers.py unsubscribe <email>")
        print("  python manage_subscribers.py resubscribe <email>")
        print("  python manage_subscribers.py resend <email>")
        print("  python manage_subscribers.py stats")
        print("\nExamples:")
        print("  python manage_subscribers.py list")
        print("  python manage_subscribers.py list unsubscribed")
        print("  python manage_subscribers.py export subscribers.csv")
        print("  python manage_subscribers.py search user@example.com")
        print("  python manage_subscribers.py unsubscribe user@example.com")
        print("  python manage_subscribers.py resend user@example.com")
        print("  python manage_subscribers.py stats")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'list':
        status = sys.argv[2] if len(sys.argv) > 2 else 'active'
        list_subscribers(status)
    
    elif command == 'export':
        filename = sys.argv[2] if len(sys.argv) > 2 else 'subscribers.csv'
        status = sys.argv[3] if len(sys.argv) > 3 else 'active'
        export_subscribers(filename, status)
    
    elif command == 'search':
        if len(sys.argv) < 3:
            print("✗ Please provide an email address")
        else:
            search_subscriber(sys.argv[2])
    
    elif command == 'unsubscribe':
        if len(sys.argv) < 3:
            print("✗ Please provide an email address")
        else:
            unsubscribe_email(sys.argv[2])
    
    elif command == 'resubscribe':
        if len(sys.argv) < 3:
            print("✗ Please provide an email address")
        else:
            resubscribe_email(sys.argv[2])
    
    elif command == 'stats':
        get_stats()
    
    elif command == 'resend':
        if len(sys.argv) < 3:
            print("✗ Please provide an email address")
        else:
            resend_welcome_email(sys.argv[2])
    
    else:
        print(f"✗ Unknown command: {command}")
