"""
AWS Lambda Function for Email Subscription with Open/Click Tracking
Handles: subscriptions, email sending, open tracking, click tracking
"""

import json
import boto3
import uuid
import base64
from datetime import datetime

# Initialize AWS services
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='us-east-1')
subscribers_table = dynamodb.Table('email-subscribers')
events_table = dynamodb.Table('email-events')

# Configuration
DOMAIN = 'https://christianconservativestoday.com'
FROM_EMAIL = 'Christian Conservatives Today <contact@christianconservativestoday.com>'

def lambda_handler(event, context):
    """Main Lambda handler - routes requests to appropriate function"""
    path = event.get('path', '')
    method = event.get('httpMethod', '')
    
    # Handle CORS preflight
    if method == 'OPTIONS':
        return cors_response(200, {'message': 'OK'})
    
    # Route to appropriate handler
    if path == '/subscribe' or (method == 'POST' and not path.startswith('/track')):
        return handle_subscription(event)
    elif path.startswith('/track/open/'):
        return handle_open_tracking(event)
    elif path.startswith('/track/click/'):
        return handle_click_tracking(event)
    else:
        return cors_response(404, {'error': 'Not found'})

def handle_subscription(event):
    """Handle new email subscription"""
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email', '').strip().lower()
        
        # Validate email
        if not email or '@' not in email or '.' not in email:
            return cors_response(400, {'error': 'Invalid email address'})
        
        # Check if already subscribed
        try:
            response = subscribers_table.get_item(Key={'email': email})
            if 'Item' in response and response['Item'].get('status') == 'active':
                return cors_response(200, {'message': 'Already subscribed', 'email': email})
        except:
            pass
        
        # Store subscriber in DynamoDB
        subscribers_table.put_item(Item={
            'email': email,
            'status': 'active',
            'subscribed_at': datetime.now().isoformat(),
            'source': 'election-map',
            'total_opens': 0,
            'total_clicks': 0,
            'last_activity': datetime.now().isoformat()
        })
        
        # Send welcome email with tracking
        send_welcome_email(email)
        
        # Log subscription event
        log_event(email, 'subscribed', 'welcome-email')
        
        return cors_response(200, {
            'message': 'Subscription successful',
            'email': email
        })
        
    except Exception as e:
        print(f"Subscription error: {str(e)}")
        return cors_response(500, {'error': 'Subscription failed. Please try again.'})

def handle_open_tracking(event):
    """Track email opens via 1x1 pixel"""
    try:
        # Extract tracking ID from URL path
        tracking_id = event['path'].split('/')[-1]
        
        # Decode to get email and campaign
        email, campaign_id = decode_tracking_id(tracking_id)
        
        # Log open event
        log_event(email, 'opened', campaign_id)
        
        # Update subscriber stats
        try:
            subscribers_table.update_item(
                Key={'email': email},
                UpdateExpression='SET total_opens = total_opens + :inc, last_activity = :now',
                ExpressionAttributeValues={
                    ':inc': 1,
                    ':now': datetime.now().isoformat()
                }
            )
        except:
            pass
        
        # Return 1x1 transparent PNG pixel
        pixel_data = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'image/png',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            },
            'body': pixel_data,
            'isBase64Encoded': True
        }
        
    except Exception as e:
        print(f"Open tracking error: {str(e)}")
        # Return pixel anyway to avoid broken images
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'image/png'},
            'body': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==',
            'isBase64Encoded': True
        }

def handle_click_tracking(event):
    """Track link clicks and redirect to destination"""
    try:
        # Extract tracking ID from URL path
        tracking_id = event['path'].split('/')[-1]
        
        # Decode to get email, campaign, and destination URL
        email, campaign_id, destination_url = decode_click_tracking_id(tracking_id)
        
        # Log click event
        log_event(email, 'clicked', campaign_id, {'url': destination_url})
        
        # Update subscriber stats
        try:
            subscribers_table.update_item(
                Key={'email': email},
                UpdateExpression='SET total_clicks = total_clicks + :inc, last_activity = :now',
                ExpressionAttributeValues={
                    ':inc': 1,
                    ':now': datetime.now().isoformat()
                }
            )
        except:
            pass
        
        # Redirect to destination URL
        return {
            'statusCode': 302,
            'headers': {
                'Location': destination_url,
                'Cache-Control': 'no-cache'
            },
            'body': ''
        }
        
    except Exception as e:
        print(f"Click tracking error: {str(e)}")
        # Redirect to homepage on error
        return {
            'statusCode': 302,
            'headers': {'Location': DOMAIN},
            'body': ''
        }

def send_welcome_email(email):
    """Send welcome email with tracking pixels and links"""
    campaign_id = 'welcome-email'
    
    # Generate tracking pixel URL
    tracking_id = encode_tracking_id(email, campaign_id)
    pixel_url = f"{DOMAIN}/track/open/{tracking_id}"
    
    # Generate tracked links
    election_map_link = create_tracked_link(email, campaign_id, f"{DOMAIN}/election-map.html")
    unsubscribe_link = f"{DOMAIN}/unsubscribe?email={email}"
    
    # HTML email body
    html_body = f"""
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #667eea; margin-top: 0;">Welcome to Christian Conservatives Today! 🙏</h2>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                Thank you for subscribing to our election updates and voter guides!
            </p>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                You'll now receive:
            </p>
            
            <ul style="font-size: 15px; line-height: 1.8; color: #555;">
                <li>🗳️ <strong>Election updates</strong> and critical dates</li>
                <li>📖 <strong>State-specific voter guides</strong> for all 50 states</li>
                <li>🎯 <strong>Pro-life, pro-family candidate</strong> information</li>
                <li>⛪ <strong>Church mobilization</strong> resources and strategies</li>
                <li>📊 <strong>Biblical voting guidance</strong> on key issues</li>
            </ul>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{election_map_link}" 
                   style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; 
                          font-weight: bold; font-size: 16px;">
                    📍 View Interactive Election Map
                </a>
            </div>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p style="margin: 0; font-size: 14px; color: #666;">
                    <strong>💡 Quick Tip:</strong> Bookmark the election map and check back regularly for updates 
                    as we add new candidates and races!
                </p>
            </div>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            
            <p style="font-size: 12px; color: #999; line-height: 1.6;">
                You're receiving this email because you subscribed at christianconservativestoday.com<br>
                <a href="{unsubscribe_link}" style="color: #667eea;">Unsubscribe</a> | 
                <a href="{DOMAIN}" style="color: #667eea;">Visit Website</a>
            </p>
        </div>
        
        <!-- Tracking pixel -->
        <img src="{pixel_url}" width="1" height="1" style="display:none;" alt="">
    </body>
    </html>
    """
    
    # Plain text version
    text_body = f"""
    Welcome to Christian Conservatives Today!
    
    Thank you for subscribing to our election updates and voter guides!
    
    You'll now receive:
    - Election updates and critical dates
    - State-specific voter guides for all 50 states
    - Pro-life, pro-family candidate information
    - Church mobilization resources and strategies
    - Biblical voting guidance on key issues
    
    View the interactive election map: {DOMAIN}/election-map.html
    
    ---
    You're receiving this because you subscribed at christianconservativestoday.com
    Unsubscribe: {unsubscribe_link}
    """
    
    # Send email via SES
    ses.send_email(
        Source=FROM_EMAIL,
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': '🗳️ Welcome to Christian Conservatives Today!'},
            'Body': {
                'Text': {'Data': text_body},
                'Html': {'Data': html_body}
            }
        }
    )

def encode_tracking_id(email, campaign_id):
    """Encode email and campaign into tracking ID"""
    data = f"{email}|{campaign_id}"
    return base64.urlsafe_b64encode(data.encode()).decode()

def decode_tracking_id(tracking_id):
    """Decode tracking ID to email and campaign"""
    data = base64.urlsafe_b64decode(tracking_id.encode()).decode()
    email, campaign_id = data.split('|')
    return email, campaign_id

def create_tracked_link(email, campaign_id, destination_url):
    """Create tracked link for click tracking"""
    data = f"{email}|{campaign_id}|{destination_url}"
    tracking_id = base64.urlsafe_b64encode(data.encode()).decode()
    return f"{DOMAIN}/track/click/{tracking_id}"

def decode_click_tracking_id(tracking_id):
    """Decode click tracking ID to email, campaign, and URL"""
    data = base64.urlsafe_b64decode(tracking_id.encode()).decode()
    parts = data.split('|', 2)  # Split into max 3 parts
    return parts[0], parts[1], parts[2]

def log_event(email, event_type, campaign_id, metadata=None):
    """Log email event to DynamoDB"""
    event_id = str(uuid.uuid4())
    timestamp = int(datetime.now().timestamp())
    
    item = {
        'event_id': event_id,
        'timestamp': timestamp,
        'email': email,
        'event_type': event_type,
        'campaign_id': campaign_id,
        'date': datetime.now().isoformat()
    }
    
    if metadata:
        item['metadata'] = json.dumps(metadata)
    
    try:
        events_table.put_item(Item=item)
    except Exception as e:
        print(f"Error logging event: {str(e)}")

def cors_response(status_code, body):
    """Return response with CORS headers"""
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }
