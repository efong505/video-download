"""
AWS Lambda Function for Email Subscription with Open/Click Tracking
Handles: subscriptions, email sending, open tracking, click tracking
"""

import json
import boto3
import uuid
import base64
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

# Initialize AWS services
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='us-east-1')
sns = boto3.client('sns', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
subscribers_table = dynamodb.Table('email-subscribers')
book_subscribers_table = dynamodb.Table('book-subscribers')
events_table = dynamodb.Table('email-events')

# Multi-tenant email marketing bridge
mt_subscribers_table = dynamodb.Table('user-email-subscribers')
mt_users_table = dynamodb.Table('users')
mt_drip_enrollments_table = dynamodb.Table('user-email-drip-enrollments')
mt_campaigns_table = dynamodb.Table('user-email-campaigns')
mt_campaign_stats_table = dynamodb.Table('email-campaign-stats')
mt_subscriber_stats_table = dynamodb.Table('email-subscriber-stats')
PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'
BOOK_DRIP_SEQUENCE_NAME = 'book-welcome-sequence'

SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:371751795928:platform-critical-alerts'

# Configuration
DOMAIN = 'https://christianconservativestoday.com'
API_GATEWAY = 'https://niexv1rw75.execute-api.us-east-1.amazonaws.com'
FROM_EMAIL = 'Christian Conservatives Today <contact@christianconservativestoday.com>'
PDF_BUCKET = 'my-video-downloads-bucket'
PDF_PREFIX = 'book-pdfs/'

def lambda_handler(event, context):
    """Main Lambda handler - routes requests to appropriate function"""
    # API Gateway v2 uses rawPath, v1 uses path
    path = event.get('rawPath', event.get('path', ''))
    # API Gateway v2 uses requestContext.http.method, v1 uses httpMethod
    method = event.get('httpMethod', '')
    if not method and 'requestContext' in event:
        method = event.get('requestContext', {}).get('http', {}).get('method', '')
    
    # Handle CORS preflight
    if method == 'OPTIONS':
        return cors_response(200, {'message': 'OK'})
    
    # Route to appropriate handler
    if path == '/subscribe':
        params = event.get('queryStringParameters') or {}
        if params.get('action') == 'list_book_subscribers':
            return list_book_subscribers()
        elif params.get('action') == 'list_drip_enrollments':
            return list_drip_enrollments()
        elif params.get('action') == 'list_campaigns':
            return list_campaigns()
        elif params.get('action') == 'get_campaign':
            return get_campaign(params.get('campaign_id', ''))
        elif params.get('action') == 'get_analytics_overview':
            return get_analytics_overview()
        elif params.get('action') == 'get_campaign_analytics':
            return get_campaign_analytics()
        elif params.get('action') == 'get_subscriber_analytics':
            return get_subscriber_analytics()
        elif params.get('action') == 'get_recent_events':
            return get_recent_events(params.get('limit', '100'))
        elif params.get('action') == 'list_campaign_groups':
            return list_campaign_groups()
        elif params.get('action') == 'check_subscriber':
            return check_subscriber_status(params.get('email', ''))
        elif params.get('action') == 'resend_book_email':
            return handle_resend_book_email(event)
        elif method == 'POST':
            body = json.loads(event.get('body', '{}'))
            action = body.get('action')
            if action == 'update_preferences':
                return handle_update_preferences(body)
            elif action == 'unsubscribe_all':
                return handle_unsubscribe_all(body)
            elif action == 'create_campaign':
                return create_campaign(body)
            elif action == 'update_campaign':
                return update_campaign(body)
            elif action == 'delete_campaign':
                return delete_campaign(body)
            elif action == 'enroll_post_purchase':
                return enroll_post_purchase(body)
            elif action == 'trigger_drip_now':
                return trigger_drip_now(body)
            else:
                return handle_subscription(event)
        else:
            return cors_response(400, {'error': 'Invalid request'})
    elif path == '/list_book_subscribers':
        return list_book_subscribers()
    elif path == '/confirm':
        return handle_confirmation(event)
    elif path == '/unsubscribe':
        return handle_unsubscribe(event)
    elif path.startswith('/track/open/'):
        return handle_open_tracking(event)
    elif path.startswith('/track/click/'):
        return handle_click_tracking(event)
    else:
        return cors_response(404, {'error': 'Not found'})

def handle_unsubscribe(event):
    """Handle email unsubscribe"""
    try:
        # Get email from query string or body
        email = None
        if 'queryStringParameters' in event and event['queryStringParameters']:
            email = event['queryStringParameters'].get('email', '').strip().lower()
        if not email and event.get('body'):
            body = json.loads(event.get('body', '{}'))
            email = body.get('email', '').strip().lower()
        
        if not email:
            return cors_response(400, {'error': 'Email required'})
        
        # Update subscriber status
        subscribers_table.update_item(
            Key={'email': email},
            UpdateExpression='SET #status = :status, unsubscribed_at = :date',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'unsubscribed',
                ':date': datetime.now().isoformat()
            }
        )
        
        # Log unsubscribe event
        log_event(email, 'unsubscribed', 'user-action')
        
        # Send notification email
        try:
            ses.send_email(
                Source=FROM_EMAIL,
                Destination={'ToAddresses': ['contact@christianconservativestoday.com']},
                Message={
                    'Subject': {'Data': f'Unsubscribe: {email}'},
                    'Body': {'Text': {'Data': f'{email} unsubscribed on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'}}}
            )
        except:
            pass
        
        return cors_response(200, {'message': 'Successfully unsubscribed', 'email': email})
        
    except Exception as e:
        print(f"Unsubscribe error: {str(e)}")
        return cors_response(500, {'error': 'Unsubscribe failed'})

def handle_subscription(event):
    """Handle new email subscription"""
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email', '').strip().lower()
        first_name = body.get('first_name', '').strip()
        last_name = body.get('last_name', '').strip()
        list_type = body.get('list_type', 'election')  # 'election' or 'book'
        
        # Validate email
        if not email or '@' not in email or '.' not in email:
            return cors_response(400, {'error': 'Invalid email address'})
        
        # Handle book subscriptions (no confirmation needed)
        if list_type == 'book':
            try:
                response = book_subscribers_table.get_item(Key={'email': email})
                if 'Item' in response:
                    return cors_response(200, {'message': 'already_subscribed', 'email': email})
            except:
                pass
            
            book_subscribers_table.put_item(Item={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'subscribed_at': datetime.now().isoformat(),
                'source': body.get('source', 'book_landing_page')
            })
            
            # Send customer confirmation email with PDFs
            try:
                send_book_signup_email_with_pdfs(email, first_name)
                print(f'Book signup email with PDFs sent to: {email}')
            except Exception as email_error:
                print(f'Book signup email error: {email_error}')
                import traceback
                traceback.print_exc()
            
            # Send SNS notification
            try:
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject=f'New Book Subscriber - {email}',
                    Message=f"""NEW BOOK MAILING LIST SUBSCRIBER

Email: {email}
Name: {first_name} {last_name}
Source: {body.get('source', 'book_landing_page')}
Subscribed: {datetime.now().isoformat()}
"""
                )
            except Exception as sns_error:
                print(f'SNS notification error: {sns_error}')
            
            # Send direct email notification to admin
            try:
                admin_email = 'hawaiianintucson@gmail.com'
                ses.send_email(
                    Source=FROM_EMAIL,
                    Destination={'ToAddresses': [admin_email]},
                    Message={
                        'Subject': {'Data': f'🎉 New Book Subscriber: {email}'},
                        'Body': {
                            'Text': {'Data': f"""NEW BOOK SUBSCRIBER

Email: {email}
First Name: {first_name}
Last Name: {last_name}
Source: {body.get('source', 'book_landing_page')}
Subscribed: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}

Total book subscribers: Check DynamoDB for count
"""}
                        }
                    }
                )
                print(f'Admin notification sent for: {email}')
            except Exception as admin_error:
                print(f'Admin email error: {admin_error}')
            
            # Bridge: also write to multi-tenant email marketing system
            bridge_to_email_marketing(email, first_name, last_name, body.get('source', 'book_landing_page'))
            
            return cors_response(200, {'message': 'Subscription successful', 'email': email})
        
        # Election list - existing confirmation flow
        
        # Check if already subscribed
        try:
            response = subscribers_table.get_item(Key={'email': email})
            if 'Item' in response:
                existing = response['Item']
                if existing.get('status') == 'active':
                    return cors_response(200, {
                        'message': 'already_subscribed',
                        'email': email
                    })
                elif existing.get('status') == 'pending':
                    # Resend confirmation email
                    send_confirmation_email(email, first_name)
                    return cors_response(200, {
                        'message': 'confirmation_resent',
                        'email': email
                    })
                elif existing.get('status') == 'unsubscribed':
                    # Reactivate unsubscribed user
                    update_expr = 'SET #status = :status, last_activity = :now'
                    expr_values = {':status': 'pending', ':now': datetime.now().isoformat()}
                    if first_name:
                        update_expr += ', first_name = :fname'
                        expr_values[':fname'] = first_name
                    if last_name:
                        update_expr += ', last_name = :lname'
                        expr_values[':lname'] = last_name
                    
                    subscribers_table.update_item(
                        Key={'email': email},
                        UpdateExpression=update_expr,
                        ExpressionAttributeNames={'#status': 'status'},
                        ExpressionAttributeValues=expr_values
                    )
                    send_confirmation_email(email, first_name)
                    log_event(email, 'resubscribed', 'confirmation-email')
                    return cors_response(200, {
                        'message': 'Subscription successful',
                        'email': email
                    })
        except Exception as e:
            print(f"Check existing subscriber error: {str(e)}")
        
        # Store new subscriber with pending status
        item = {
            'email': email,
            'status': 'pending',
            'subscribed_at': datetime.now().isoformat(),
            'source': 'election-map',
            'total_opens': 0,
            'total_clicks': 0,
            'last_activity': datetime.now().isoformat()
        }
        if first_name:
            item['first_name'] = first_name
        if last_name:
            item['last_name'] = last_name
        
        subscribers_table.put_item(Item=item)
        
        # Send confirmation email
        send_confirmation_email(email, first_name)
        
        # Log subscription event
        log_event(email, 'pending', 'confirmation-email')
        
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
        path = event.get('rawPath', event.get('path', ''))
        tracking_id = path.split('/')[-1]
        
        # Decode tracking ID (handles both formats)
        email, campaign_id = decode_tracking_id(tracking_id)
        
        print(f"Open tracked: email={email}, campaign={campaign_id}")
        
        # Log event
        log_event_mt(email, 'opened', campaign_id)
        
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
        path = event.get('rawPath', event.get('path', ''))
        tracking_id = path.split('/')[-1]
        
        print(f"Click tracking - Path: {path}, Tracking ID: {tracking_id}")
        
        # Decode to get email, campaign, and destination URL
        try:
            email, campaign_id, destination_url = decode_click_tracking_id(tracking_id)
        except Exception as decode_error:
            print(f"Decode error: {str(decode_error)}")
            # Try to decode and show what's in the tracking ID
            try:
                import base64
                decoded = base64.urlsafe_b64decode(tracking_id.encode()).decode()
                print(f"Raw decoded data: {decoded}")
            except:
                pass
            # Redirect to homepage on decode failure
            return {
                'statusCode': 302,
                'headers': {'Location': DOMAIN},
                'body': ''
            }
        
        print(f"Click tracked: email={email}, campaign={campaign_id}, url={destination_url}")
        
        # Log event
        log_event_mt(email, 'clicked', campaign_id, {'url': destination_url})
        
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
        import traceback
        traceback.print_exc()
        # Redirect to homepage on error
        return {
            'statusCode': 302,
            'headers': {'Location': DOMAIN},
            'body': ''
        }

def handle_confirmation(event):
    """Handle email confirmation"""
    try:
        # Get email from query string
        email = None
        if 'queryStringParameters' in event and event['queryStringParameters']:
            email = event['queryStringParameters'].get('email', '').strip().lower()
        
        if not email:
            return cors_response(400, {'error': 'Email required'})
        
        # Update subscriber status to active
        subscribers_table.update_item(
            Key={'email': email},
            UpdateExpression='SET #status = :status, confirmed_at = :date',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'active',
                ':date': datetime.now().isoformat()
            }
        )
        
        # Send welcome email
        send_welcome_email(email)
        
        # Log confirmation event
        log_event(email, 'confirmed', 'welcome-email')
        
        return cors_response(200, {'message': 'Email confirmed', 'email': email})
        
    except Exception as e:
        print(f"Confirmation error: {str(e)}")
        return cors_response(500, {'error': 'Confirmation failed'})

def send_confirmation_email(email, first_name=''):
    """Send confirmation email with verify link"""
    confirm_link = f"{DOMAIN}/confirm.html?email={email}"
    greeting = f"Hi {first_name}!" if first_name else "Hello!"
    
    html_body = f"""
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #667eea; margin-top: 0;">Confirm Your Subscription 📧</h2>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                {greeting}
            </p>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                Thank you for subscribing to Christian Conservatives Today!
            </p>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                Please confirm your email address to start receiving election updates and voter guides.
            </p>
            
            <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                <tr>
                    <td align="center">
                        <a href="{confirm_link}" 
                           style="display: inline-block; padding: 15px 40px; background-color: #667eea; 
                                  color: #ffffff !important; text-decoration: none; font-weight: bold; 
                                  font-size: 16px; border-radius: 5px; mso-padding-alt: 0; 
                                  font-family: Arial, sans-serif;">
                            <span style="color: #ffffff !important;">✓ Confirm Subscription</span>
                        </a>
                    </td>
                </tr>
            </table>
            
            <p style="font-size: 14px; color: #666; line-height: 1.6;">
                If you didn't sign up for this, you can safely ignore this email.
            </p>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            
            <p style="font-size: 12px; color: #999;">
                Christian Conservatives Today<br>
                <a href="{DOMAIN}" style="color: #667eea;">Visit Website</a>
            </p>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""
    Confirm Your Subscription
    
    Thank you for subscribing to Christian Conservatives Today!
    
    Please confirm your email address by clicking this link:
    {confirm_link}
    
    If you didn't sign up for this, you can safely ignore this email.
    
    Christian Conservatives Today
    {DOMAIN}
    """
    
    ses.send_email(
        Source=FROM_EMAIL,
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': '✓ Confirm Your Subscription - Christian Conservatives Today'},
            'Body': {
                'Text': {'Data': text_body},
                'Html': {'Data': html_body}
            }
        }
    )

def send_welcome_email(email):
    """Send welcome email with tracking pixels and links"""
    campaign_id = 'welcome-email'
    
    # Generate tracking pixel URL
    tracking_id = encode_tracking_id(email, campaign_id)
    pixel_url = f"{API_GATEWAY}/track/open/{tracking_id}"
    
    # Direct links (no click tracking)
    election_map_link = f"{DOMAIN}/election-map.html"
    unsubscribe_link = f"{DOMAIN}/unsubscribe.html?email={email}"
    
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
    """Decode tracking ID to email and campaign (handles both formats)"""
    data = base64.urlsafe_b64decode(tracking_id.encode()).decode()
    if '|' in data:
        # Format from subscription_handler: email|campaign_id
        email, campaign_id = data.split('|')
    elif ':' in data:
        # Format from email_sender: user_id:campaign_id:email
        parts = data.split(':')
        if len(parts) >= 3:
            email = parts[-1]
            campaign_id = parts[-2]
        else:
            email, campaign_id = parts[0], parts[1]
    else:
        raise ValueError(f"Unknown tracking format: {data}")
    return email, campaign_id

def create_tracked_link(email, campaign_id, destination_url):
    """Create tracked link for click tracking"""
    data = f"{email}|{campaign_id}|{destination_url}"
    tracking_id = base64.urlsafe_b64encode(data.encode()).decode()
    return f"{DOMAIN}/track/click/{tracking_id}"

def decode_click_tracking_id(tracking_id):
    """Decode click tracking ID to email, campaign, and URL (handles both formats)"""
    data = base64.urlsafe_b64decode(tracking_id.encode()).decode()
    if '|' in data:
        # Format from subscription_handler: email|campaign_id|url
        parts = data.split('|', 2)
        return parts[0], parts[1], parts[2]
    elif ':' in data:
        # Format from email_sender: user_id:campaign_id:email:https://...
        # URLs contain colons, so split carefully
        parts = data.split(':')
        if len(parts) >= 4:
            campaign_id = parts[1]
            email = parts[2]
            url = ':'.join(parts[3:])  # Rejoin URL parts
            return email, campaign_id, url
        else:
            raise ValueError(f"Unknown click tracking format: {data}")
    else:
        raise ValueError(f"Unknown click tracking format: {data}")

def log_event(email, event_type, campaign_id, metadata=None):
    """Log email event to email-events table"""
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

def log_event_mt(email, event_type, campaign_id, metadata=None):
    """Log email event to user-email-events table (for analytics)"""
    try:
        mt_events_table = dynamodb.Table('user-email-events')
        event_id = f"{campaign_id}_{email}_{event_type}_{int(datetime.now().timestamp())}"
        item = {
            'user_id': PLATFORM_OWNER_ID,
            'event_id': event_id,
            'campaign_id': campaign_id,
            'subscriber_email': email,
            'event_type': event_type,
            'timestamp': int(datetime.now().timestamp()),
            'date': datetime.now().isoformat()
        }
        if metadata:
            item['metadata'] = json.dumps(metadata)
        mt_events_table.put_item(Item=item)
    except Exception as e:
        print(f"Error logging MT event: {str(e)}")

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

def bridge_to_email_marketing(email, first_name, last_name, source):
    """Dual-write book subscriber to multi-tenant email marketing system"""
    try:
        existing = mt_subscribers_table.get_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'subscriber_email': email}
        )
        if 'Item' in existing:
            current_tags = existing['Item'].get('tags', [])
            needed_tags = {'book', 'survival-kit'}
            if not needed_tags.issubset(set(current_tags)):
                merged = list(set(current_tags) | needed_tags)
                mt_subscribers_table.update_item(
                    Key={'user_id': PLATFORM_OWNER_ID, 'subscriber_email': email},
                    UpdateExpression='SET tags = :tags',
                    ExpressionAttributeValues={':tags': merged}
                )
            return

        mt_subscribers_table.put_item(Item={
            'user_id': PLATFORM_OWNER_ID,
            'subscriber_email': email,
            'first_name': first_name or '',
            'last_name': last_name or '',
            'phone': '',
            'status': 'active',
            'subscribed_at': datetime.now().isoformat(),
            'source': source,
            'tags': ['book', 'survival-kit']
        })

        mt_users_table.update_item(
            Key={'user_id': PLATFORM_OWNER_ID},
            UpdateExpression='SET email_subscribers_count = email_subscribers_count + :inc',
            ExpressionAttributeValues={':inc': 1}
        )
        print(f'Bridge: {email} added to email marketing system')
        
        # Auto-enroll in book drip sequence
        try:
            enrollment_id = f"{email}#{BOOK_DRIP_SEQUENCE_NAME}"
            mt_drip_enrollments_table.put_item(Item={
                'user_id': PLATFORM_OWNER_ID,
                'enrollment_id': enrollment_id,
                'subscriber_email': email,
                'sequence_name': BOOK_DRIP_SEQUENCE_NAME,
                'filter_tags': ['book', 'survival-kit'],
                'enrolled_at': datetime.now().isoformat(),
                'current_sequence_number': 0,
                'status': 'active'
            })
            print(f'Bridge: {email} enrolled in drip sequence')
        except Exception as drip_error:
            print(f'Drip enrollment error (non-fatal): {str(drip_error)}')
    except Exception as e:
        print(f'Bridge error (non-fatal): {str(e)}')

def send_book_signup_email_with_pdfs(email, first_name):
    """Send book signup confirmation with 3 PDF attachments from S3"""
    greeting = f"Hi {first_name}!" if first_name else "Hello!"
    
    msg = MIMEMultipart('mixed')
    msg['Subject'] = '🎁 Your Free Christian AI Survival Kit is Here!'
    msg['From'] = FROM_EMAIL
    msg['To'] = email
    
    html_body = f"""
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <div style="background: linear-gradient(135deg, #16a34a 0%, #15803d 100%); padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 30px;">
                <h2 style="color: white; margin: 0;">🎁 Your Free Christian AI Survival Kit</h2>
            </div>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">{greeting}</p>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                Thank you for downloading the <strong>Christian AI Survival Kit</strong>!
            </p>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                You now have access to <strong>$71 worth of resources</strong> to help you master AI without losing your soul:
            </p>
            
            <div style="background: #f0fdf4; padding: 20px; border-radius: 8px; border-left: 4px solid #16a34a; margin: 20px 0;">
                <h3 style="color: #16a34a; margin-top: 0;">📦 What's Included (Attached):</h3>
                <ul style="font-size: 15px; line-height: 1.8; color: #555;">
                    <li><strong>30-Page Book Preview</strong> — Introduction + the most powerful chapters</li>
                    <li><strong>Christian AI Survival Guide</strong> — 7 safeguards for using AI without losing your soul</li>
                    <li><strong>Church Discussion Guide</strong> — 10-session study for small groups</li>
                    <li><strong>AI Parent Guide</strong> — How to protect your children in an AI-driven world</li>
                </ul>
            </div>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                <strong>Plus:</strong> You can now read the <strong>30-page book preview</strong> online at:
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{DOMAIN}/the-necessary-evil-book.html#preview" 
                   style="display: inline-block; background: linear-gradient(135deg, #16a34a 0%, #15803d 100%); 
                          color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; 
                          font-weight: bold; font-size: 16px;">
                    📖 Read the Book Preview
                </a>
            </div>
            
            <div style="background: #f0f9ff; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #2c5aa0;">
                <p style="margin: 0; font-size: 14px; color: #666;">
                    <strong>📥 Need to re-download?</strong> Access your PDFs anytime at:<br>
                    <a href="{DOMAIN}/book-resources.html?email={email}" style="color: #2c5aa0; font-weight: bold;">{DOMAIN}/book-resources.html</a>
                </p>
            </div>
            
            <div style="background: #fffbeb; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #d4af37;">
                <p style="margin: 0; font-size: 14px; color: #666;">
                    <strong>💡 Next Step:</strong> Check out the full book <em>The Necessary Evil</em> — 
                    available on Amazon (Kindle, Hardcover & Paperback) and as a signed copy direct from the author.
                </p>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{DOMAIN}/the-necessary-evil-book.html#purchase" 
                   style="display: inline-block; background: #2c5aa0; 
                          color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; 
                          font-weight: bold; font-size: 14px;">
                    📚 Get the Full Book
                </a>
            </div>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            
            <p style="font-size: 12px; color: #999; line-height: 1.6; text-align: center;">
                You're receiving this email because you signed up for the Christian AI Survival Kit at christianconservativestoday.com<br>
                <a href="{DOMAIN}/manage-email-preferences.html?email={email}" style="color: #16a34a;">Manage Email Preferences</a> | 
                <a href="{DOMAIN}" style="color: #16a34a;">Visit Website</a>
            </p>
        </div>
    </body>
    </html>
    """
    
    text_body = f"""{greeting}

Thank you for downloading the Christian AI Survival Kit!

You now have access to $71 worth of resources to help you master AI without losing your soul:

WHAT'S INCLUDED (Attached):
* 30-Page Book Preview - Introduction + the most powerful chapters
* Christian AI Survival Guide - 7 safeguards for using AI without losing your soul
* Church Discussion Guide - 10-session study for small groups  
* AI Parent Guide - How to protect your children in an AI-driven world

PLUS: You can now read the 30-page book preview online at:
{DOMAIN}/the-necessary-evil-book.html#preview

Need to re-download? Access your PDFs anytime at:
{DOMAIN}/book-resources.html?email={email}

NEXT STEP: Check out the full book "The Necessary Evil" - available on Amazon and as a signed copy direct from the author.
{DOMAIN}/the-necessary-evil-book.html#purchase

---
You're receiving this because you signed up at christianconservativestoday.com
"""
    
    msg_body = MIMEMultipart('alternative')
    msg_body.attach(MIMEText(text_body, 'plain', 'utf-8'))
    msg_body.attach(MIMEText(html_body, 'html', 'utf-8'))
    msg.attach(msg_body)
    
    pdf_files = [
        'christian-ai-survival-guide.pdf',
        'church-discussion-guide.pdf',
        'ai-parent-guide.pdf',
        'book-teaser.pdf'
    ]
    
    for pdf_file in pdf_files:
        try:
            s3_key = f"{PDF_PREFIX}{pdf_file}"
            response = s3.get_object(Bucket=PDF_BUCKET, Key=s3_key)
            pdf_data = response['Body'].read()
            
            pdf_part = MIMEApplication(pdf_data, _subtype='pdf')
            pdf_part.add_header('Content-Disposition', 'attachment', filename=pdf_file)
            msg.attach(pdf_part)
            print(f"Attached {pdf_file}")
        except Exception as e:
            print(f"Error attaching {pdf_file}: {str(e)}")
    
    ses.send_raw_email(
        Source=FROM_EMAIL,
        Destinations=[email],
        RawMessage={'Data': msg.as_string()}
    )

def list_book_subscribers():
    """List all book subscribers"""
    try:
        response = book_subscribers_table.scan()
        subscribers = response.get('Items', [])
        subscribers.sort(key=lambda x: x.get('subscribed_at', ''), reverse=True)
        return cors_response(200, {'subscribers': subscribers})
    except Exception as e:
        print(f"List book subscribers error: {str(e)}")
        return cors_response(500, {'error': 'Failed to list subscribers'})

def list_drip_enrollments():
    """List all drip enrollments for analytics"""
    try:
        from boto3.dynamodb.types import TypeDeserializer
        from decimal import Decimal
        
        response = mt_drip_enrollments_table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
        )
        enrollments = response.get('Items', [])
        
        # Convert Decimal to int/float for JSON serialization
        def convert_decimals(obj):
            if isinstance(obj, list):
                return [convert_decimals(i) for i in obj]
            elif isinstance(obj, dict):
                return {k: convert_decimals(v) for k, v in obj.items()}
            elif isinstance(obj, Decimal):
                return int(obj) if obj % 1 == 0 else float(obj)
            else:
                return obj
        
        enrollments = convert_decimals(enrollments)
        enrollments.sort(key=lambda x: x.get('enrolled_at', ''), reverse=True)
        
        print(f"Successfully retrieved {len(enrollments)} enrollments")
        return cors_response(200, {'enrollments': enrollments})
    except Exception as e:
        print(f"List enrollments error: {str(e)}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': f'Failed to list enrollments: {str(e)}'})

def check_subscriber_status(email):
    """Check if email is a book subscriber"""
    try:
        if not email:
            return cors_response(400, {'error': 'Email required'})
        
        email = email.strip().lower()
        response = book_subscribers_table.get_item(Key={'email': email})
        
        if 'Item' in response:
            return cors_response(200, {'is_subscriber': True, 'email': email})
        else:
            return cors_response(200, {'is_subscriber': False, 'email': email})
    except Exception as e:
        print(f"Check subscriber error: {str(e)}")
        return cors_response(500, {'error': 'Failed to check status'})

def handle_resend_book_email(event):
    """Resend book signup email with PDFs"""
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email', '').strip().lower()
        first_name = body.get('first_name', '').strip()
        
        if not email:
            return cors_response(400, {'error': 'Email required'})
        
        # Verify subscriber exists
        response = book_subscribers_table.get_item(Key={'email': email})
        if 'Item' not in response:
            return cors_response(404, {'error': 'Subscriber not found'})
        
        # Get first name from DB if not provided
        if not first_name:
            first_name = response['Item'].get('first_name', '')
        
        # Resend email
        send_book_signup_email_with_pdfs(email, first_name)
        print(f'Resent book email to: {email}')
        
        return cors_response(200, {'message': 'success', 'email': email})
    except Exception as e:
        print(f"Resend email error: {str(e)}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': 'Failed to resend email'})

def handle_update_preferences(body):
    """Update user email preferences"""
    try:
        email = body.get('email', '').strip().lower()
        drip_enabled = body.get('drip_enabled', True)
        
        if not email:
            return cors_response(400, {'error': 'Email required'})
        
        # Update drip enrollment status
        enrollment_id = f"{email}#{BOOK_DRIP_SEQUENCE_NAME}"
        
        try:
            if drip_enabled:
                # Reactivate enrollment
                mt_drip_enrollments_table.update_item(
                    Key={'user_id': PLATFORM_OWNER_ID, 'enrollment_id': enrollment_id},
                    UpdateExpression='SET #status = :status',
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={':status': 'active'}
                )
            else:
                # Pause enrollment
                mt_drip_enrollments_table.update_item(
                    Key={'user_id': PLATFORM_OWNER_ID, 'enrollment_id': enrollment_id},
                    UpdateExpression='SET #status = :status',
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={':status': 'paused'}
                )
        except Exception as e:
            print(f"Error updating enrollment: {str(e)}")
        
        return cors_response(200, {'message': 'Preferences updated', 'email': email})
        
    except Exception as e:
        print(f"Update preferences error: {str(e)}")
        return cors_response(500, {'error': 'Failed to update preferences'})

def handle_unsubscribe_all(body):
    """Unsubscribe user from all emails"""
    try:
        email = body.get('email', '').strip().lower()
        
        if not email:
            return cors_response(400, {'error': 'Email required'})
        
        # Pause drip enrollment
        enrollment_id = f"{email}#{BOOK_DRIP_SEQUENCE_NAME}"
        try:
            mt_drip_enrollments_table.update_item(
                Key={'user_id': PLATFORM_OWNER_ID, 'enrollment_id': enrollment_id},
                UpdateExpression='SET #status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': 'paused'}
            )
        except Exception as e:
            print(f"Error pausing enrollment: {str(e)}")
        
        # Update subscriber status
        try:
            mt_subscribers_table.update_item(
                Key={'user_id': PLATFORM_OWNER_ID, 'subscriber_email': email},
                UpdateExpression='SET #status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': 'unsubscribed'}
            )
        except Exception as e:
            print(f"Error updating subscriber: {str(e)}")
        
        return cors_response(200, {'message': 'Unsubscribed from all emails', 'email': email})
        
    except Exception as e:
        print(f"Unsubscribe all error: {str(e)}")
        return cors_response(500, {'error': 'Failed to unsubscribe'})

def list_campaigns():
    """List all email campaigns"""
    try:
        from decimal import Decimal
        
        response = mt_campaigns_table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
        )
        campaigns = response.get('Items', [])
        
        # Convert Decimal to int/float for JSON
        def convert_decimals(obj):
            if isinstance(obj, list):
                return [convert_decimals(i) for i in obj]
            elif isinstance(obj, dict):
                return {k: convert_decimals(v) for k, v in obj.items()}
            elif isinstance(obj, Decimal):
                return int(obj) if obj % 1 == 0 else float(obj)
            else:
                return obj
        
        campaigns = convert_decimals(campaigns)
        return cors_response(200, {'campaigns': campaigns})
    except Exception as e:
        print(f"List campaigns error: {str(e)}")
        return cors_response(500, {'error': 'Failed to list campaigns'})

def get_campaign(campaign_id):
    """Get a single campaign by ID"""
    try:
        from decimal import Decimal
        
        if not campaign_id:
            return cors_response(400, {'error': 'Campaign ID required'})
        
        response = mt_campaigns_table.get_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'campaign_id': campaign_id}
        )
        
        if 'Item' not in response:
            return cors_response(404, {'error': 'Campaign not found'})
        
        campaign = response['Item']
        
        # Convert Decimal to int/float
        def convert_decimals(obj):
            if isinstance(obj, list):
                return [convert_decimals(i) for i in obj]
            elif isinstance(obj, dict):
                return {k: convert_decimals(v) for k, v in obj.items()}
            elif isinstance(obj, Decimal):
                return int(obj) if obj % 1 == 0 else float(obj)
            else:
                return obj
        
        campaign = convert_decimals(campaign)
        return cors_response(200, {'campaign': campaign})
    except Exception as e:
        print(f"Get campaign error: {str(e)}")
        return cors_response(500, {'error': 'Failed to get campaign'})

def list_campaign_groups():
    """List distinct campaign groups"""
    try:
        response = mt_campaigns_table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID},
            ProjectionExpression='campaign_group'
        )
        groups = set()
        for item in response.get('Items', []):
            g = item.get('campaign_group', '')
            if g:
                groups.add(g)
        return cors_response(200, {'groups': sorted(list(groups))})
    except Exception as e:
        print(f"List campaign groups error: {str(e)}")
        return cors_response(500, {'error': 'Failed to list groups'})

def create_campaign(body):
    """Create a new email campaign"""
    try:
        campaign_id = str(uuid.uuid4())
        campaign_name = body.get('campaign_name', '').strip()
        sequence_number = int(body.get('sequence_number', 1))
        delay_days = int(body.get('delay_days', 1))
        subject = body.get('subject', '').strip()
        content = body.get('content', '').strip()
        filter_tags = body.get('filter_tags', [])
        campaign_group = body.get('campaign_group', '').strip()
        
        if not campaign_name or not subject or not content:
            return cors_response(400, {'error': 'Campaign name, subject, and content required'})
        
        item = {
            'user_id': PLATFORM_OWNER_ID,
            'campaign_id': campaign_id,
            'campaign_name': campaign_name,
            'sequence_number': sequence_number,
            'delay_days': delay_days,
            'delay_hours': 0,
            'subject': subject,
            'content': content,
            'filter_tags': filter_tags,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        if campaign_group:
            item['campaign_group'] = campaign_group
        
        mt_campaigns_table.put_item(Item=item)
        
        return cors_response(200, {'message': 'Campaign created', 'campaign_id': campaign_id})
    except Exception as e:
        print(f"Create campaign error: {str(e)}")
        return cors_response(500, {'error': 'Failed to create campaign'})

def update_campaign(body):
    """Update an existing campaign"""
    try:
        campaign_id = body.get('campaign_id', '').strip()
        
        if not campaign_id:
            return cors_response(400, {'error': 'Campaign ID required'})
        
        # Build update expression dynamically
        update_parts = []
        expr_values = {':updated': datetime.now().isoformat()}
        
        if 'campaign_name' in body:
            update_parts.append('campaign_name = :name')
            expr_values[':name'] = body['campaign_name'].strip()
        
        if 'sequence_number' in body:
            update_parts.append('sequence_number = :seq')
            expr_values[':seq'] = int(body['sequence_number'])
        
        if 'delay_days' in body:
            update_parts.append('delay_days = :delay')
            expr_values[':delay'] = int(body['delay_days'])
        
        if 'subject' in body:
            update_parts.append('subject = :subj')
            expr_values[':subj'] = body['subject'].strip()
        
        if 'content' in body:
            update_parts.append('content = :cont')
            expr_values[':cont'] = body['content'].strip()
        
        if 'filter_tags' in body:
            update_parts.append('filter_tags = :tags')
            expr_values[':tags'] = body['filter_tags']
        
        if 'campaign_group' in body:
            update_parts.append('campaign_group = :cg')
            expr_values[':cg'] = body['campaign_group'].strip()
        
        if not update_parts:
            return cors_response(400, {'error': 'No fields to update'})
        
        update_parts.append('updated_at = :updated')
        update_expr = 'SET ' + ', '.join(update_parts)
        
        mt_campaigns_table.update_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'campaign_id': campaign_id},
            UpdateExpression=update_expr,
            ExpressionAttributeValues=expr_values
        )
        
        return cors_response(200, {'message': 'Campaign updated', 'campaign_id': campaign_id})
    except Exception as e:
        print(f"Update campaign error: {str(e)}")
        return cors_response(500, {'error': 'Failed to update campaign'})

def delete_campaign(body):
    """Delete a campaign"""
    try:
        campaign_id = body.get('campaign_id', '').strip()
        
        if not campaign_id:
            return cors_response(400, {'error': 'Campaign ID required'})
        
        mt_campaigns_table.delete_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'campaign_id': campaign_id}
        )
        
        return cors_response(200, {'message': 'Campaign deleted', 'campaign_id': campaign_id})
    except Exception as e:
        print(f"Delete campaign error: {str(e)}")
        return cors_response(500, {'error': 'Failed to delete campaign'})

def enroll_post_purchase(body):
    """Enroll a buyer in the post-purchase drip sequence"""
    try:
        email = body.get('email', '').strip().lower()
        first_name = body.get('first_name', '').strip()
        last_name = body.get('last_name', '').strip()
        source = body.get('source', 'book_purchase')
        
        if not email or '@' not in email:
            return cors_response(400, {'error': 'Valid email required'})
        
        # Ensure subscriber exists in multi-tenant system
        try:
            existing = mt_subscribers_table.get_item(
                Key={'user_id': PLATFORM_OWNER_ID, 'subscriber_email': email}
            )
            if 'Item' in existing:
                current_tags = existing['Item'].get('tags', [])
                if 'purchaser' not in current_tags:
                    mt_subscribers_table.update_item(
                        Key={'user_id': PLATFORM_OWNER_ID, 'subscriber_email': email},
                        UpdateExpression='SET tags = list_append(tags, :t)',
                        ExpressionAttributeValues={':t': ['purchaser']}
                    )
            else:
                mt_subscribers_table.put_item(Item={
                    'user_id': PLATFORM_OWNER_ID,
                    'subscriber_email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                    'phone': '',
                    'status': 'active',
                    'subscribed_at': datetime.now().isoformat(),
                    'source': source,
                    'tags': ['purchaser']
                })
        except Exception as sub_err:
            print(f"Subscriber upsert error: {sub_err}")
        
        # Create drip enrollment for post-purchase sequence
        group = body.get('campaign_group', 'post-purchase-sequence').strip() or 'post-purchase-sequence'
        enrollment_id = f"{email}#{group}"
        
        # Check if already enrolled
        try:
            existing_enrollment = mt_drip_enrollments_table.get_item(
                Key={'user_id': PLATFORM_OWNER_ID, 'enrollment_id': enrollment_id}
            )
            if 'Item' in existing_enrollment:
                return cors_response(200, {'message': 'Already enrolled in post-purchase sequence', 'email': email})
        except:
            pass
        
        mt_drip_enrollments_table.put_item(Item={
            'user_id': PLATFORM_OWNER_ID,
            'enrollment_id': enrollment_id,
            'subscriber_email': email,
            'sequence_name': group,
            'campaign_group': group,
            'filter_tags': ['purchaser'],
            'enrolled_at': datetime.now().isoformat(),
            'current_sequence_number': 0,
            'status': 'active'
        })
        
        print(f"Post-purchase enrollment: {email} enrolled in {group}")
        
        # Send SNS notification
        try:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=f'New Book Purchase Confirmed - {email}',
                Message=f"""BOOK PURCHASE CONFIRMED

Email: {email}
Name: {first_name} {last_name}
Source: {source}
Enrolled in: {group}
Time: {datetime.now().isoformat()}
"""
            )
        except:
            pass
        
        return cors_response(200, {'message': 'Enrolled in post-purchase sequence', 'email': email})
    except Exception as e:
        print(f"Post-purchase enrollment error: {str(e)}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': 'Enrollment failed'})

def trigger_drip_now(body):
    """Manually trigger the next drip email for an enrollment (bypasses delay)"""
    try:
        enrollment_id = body.get('enrollment_id', '').strip()
        if not enrollment_id:
            return cors_response(400, {'error': 'enrollment_id required'})

        # Get enrollment
        enrollment = mt_drip_enrollments_table.get_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'enrollment_id': enrollment_id}
        ).get('Item')
        if not enrollment:
            return cors_response(404, {'error': 'Enrollment not found'})

        if enrollment.get('status') != 'active':
            return cors_response(400, {'error': f"Enrollment status is '{enrollment.get('status')}', must be active"})

        subscriber_email = enrollment['subscriber_email']
        campaign_group = enrollment.get('campaign_group', '')
        current_seq = int(enrollment.get('current_sequence_number', 0))

        # Get campaigns in this group
        from decimal import Decimal
        all_camps = mt_campaigns_table.query(
            KeyConditionExpression='user_id = :uid',
            FilterExpression='attribute_exists(sequence_number)',
            ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
        ).get('Items', [])

        drip_campaigns = sorted(
            [c for c in all_camps if c.get('campaign_group') == campaign_group],
            key=lambda x: int(x.get('sequence_number', 0))
        )

        # Find next email
        next_email = None
        for c in drip_campaigns:
            if int(c.get('sequence_number', 0)) == current_seq + 1:
                next_email = c
                break

        if not next_email:
            return cors_response(400, {'error': f'No next email — sequence complete (at {current_seq}/{len(drip_campaigns)})'})

        # Verify subscriber is active
        sub = mt_subscribers_table.get_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'subscriber_email': subscriber_email}
        ).get('Item')
        if not sub or sub.get('status') != 'active':
            return cors_response(400, {'error': f'Subscriber {subscriber_email} is not active'})

        # Send via SQS
        sqs = boto3.client('sqs', region_name='us-east-1')
        sqs.send_message(
            QueueUrl='https://sqs.us-east-1.amazonaws.com/371751795928/email-sending-queue',
            MessageBody=json.dumps({
                'user_id': PLATFORM_OWNER_ID,
                'campaign_id': next_email['campaign_id'],
                'recipients': [subscriber_email],
                'drip_sequence': True
            })
        )

        # Update enrollment
        mt_drip_enrollments_table.update_item(
            Key={'user_id': PLATFORM_OWNER_ID, 'enrollment_id': enrollment_id},
            UpdateExpression='SET current_sequence_number = :seq, last_sent_at = :ts',
            ExpressionAttributeValues={
                ':seq': next_email['sequence_number'],
                ':ts': datetime.now().isoformat()
            }
        )

        return cors_response(200, {
            'message': f"Email #{next_email['sequence_number']} queued for {subscriber_email}",
            'campaign_name': next_email.get('campaign_name', ''),
            'subject': next_email.get('subject', '')
        })
    except Exception as e:
        print(f"Trigger drip now error: {str(e)}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': f'Failed to trigger: {str(e)}'})

def get_analytics_overview():
    """Get overview analytics stats from user-email-events (where email_sender logs)"""
    try:
        from decimal import Decimal
        
        # Read from user-email-events table (the one email_sender actually writes to)
        mt_events_table = dynamodb.Table('user-email-events')
        
        events = []
        response = mt_events_table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
        )
        events.extend(response.get('Items', []))
        while 'LastEvaluatedKey' in response:
            response = mt_events_table.query(
                KeyConditionExpression='user_id = :uid',
                ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID},
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            events.extend(response.get('Items', []))
        
        # Also pull from legacy email-events table
        legacy_events = []
        legacy_response = events_table.scan()
        legacy_events.extend(legacy_response.get('Items', []))
        while 'LastEvaluatedKey' in legacy_response:
            legacy_response = events_table.scan(ExclusiveStartKey=legacy_response['LastEvaluatedKey'])
            legacy_events.extend(legacy_response.get('Items', []))
        
        all_events = events + legacy_events
        
        stats = {
            'total_sent': sum(1 for e in all_events if e.get('event_type') == 'sent'),
            'total_delivered': sum(1 for e in all_events if e.get('event_type') in ('sent', 'delivered')),
            'total_opens': sum(1 for e in all_events if e.get('event_type') == 'opened'),
            'total_clicks': sum(1 for e in all_events if e.get('event_type') == 'clicked'),
            'total_bounces': sum(1 for e in all_events if e.get('event_type') == 'bounced'),
            'total_complaints': sum(1 for e in all_events if e.get('event_type') == 'complaint')
        }
        
        return cors_response(200, {'stats': stats})
    except Exception as e:
        print(f"Get analytics overview error: {str(e)}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': 'Failed to get analytics'})

def get_campaign_analytics():
    """Get per-campaign analytics from user-email-events"""
    try:
        from decimal import Decimal
        
        # Get all campaigns
        campaigns_response = mt_campaigns_table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
        )
        campaigns = campaigns_response.get('Items', [])
        
        # Get all events from user-email-events
        mt_events_table = dynamodb.Table('user-email-events')
        events = []
        response = mt_events_table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
        )
        events.extend(response.get('Items', []))
        while 'LastEvaluatedKey' in response:
            response = mt_events_table.query(
                KeyConditionExpression='user_id = :uid',
                ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID},
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            events.extend(response.get('Items', []))
        
        # Group events by campaign_id
        events_by_campaign = {}
        for e in events:
            cid = e.get('campaign_id', '')
            if cid not in events_by_campaign:
                events_by_campaign[cid] = []
            events_by_campaign[cid].append(e)
        
        campaign_analytics = []
        for campaign in campaigns:
            campaign_id = campaign['campaign_id']
            camp_events = events_by_campaign.get(campaign_id, [])
            
            sent = sum(1 for e in camp_events if e.get('event_type') == 'sent')
            opens = sum(1 for e in camp_events if e.get('event_type') == 'opened')
            clicks = sum(1 for e in camp_events if e.get('event_type') == 'clicked')
            bounces = sum(1 for e in camp_events if e.get('event_type') == 'bounced')
            complaints = sum(1 for e in camp_events if e.get('event_type') == 'complaint')
            
            campaign_analytics.append({
                'campaign_id': campaign_id,
                'campaign_name': campaign.get('campaign_name', ''),
                'campaign_group': campaign.get('campaign_group', ''),
                'sequence_number': int(campaign.get('sequence_number', 0)),
                'sent_count': sent,
                'delivered_count': sent,
                'open_count': opens,
                'click_count': clicks,
                'bounce_count': bounces,
                'complaint_count': complaints
            })
        
        return cors_response(200, {'campaigns': campaign_analytics})
    except Exception as e:
        print(f"Get campaign analytics error: {str(e)}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': 'Failed to get campaign analytics'})

def get_subscriber_analytics():
    """Get per-subscriber analytics from both event tables"""
    try:
        from decimal import Decimal
        
        # Get events from user-email-events
        mt_events_table = dynamodb.Table('user-email-events')
        events = []
        response = mt_events_table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID}
        )
        events.extend(response.get('Items', []))
        while 'LastEvaluatedKey' in response:
            response = mt_events_table.query(
                KeyConditionExpression='user_id = :uid',
                ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID},
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            events.extend(response.get('Items', []))
        
        # Also get from legacy email-events table
        legacy_response = events_table.scan()
        legacy_events = legacy_response.get('Items', [])
        while 'LastEvaluatedKey' in legacy_response:
            legacy_response = events_table.scan(ExclusiveStartKey=legacy_response['LastEvaluatedKey'])
            legacy_events.extend(legacy_response.get('Items', []))
        for le in legacy_events:
            if 'email' in le and 'subscriber_email' not in le:
                le['subscriber_email'] = le['email']
        
        all_events = events + legacy_events
        
        # Group by subscriber email
        by_subscriber = {}
        for e in all_events:
            email = e.get('subscriber_email', e.get('email', ''))
            if not email:
                continue
            if email not in by_subscriber:
                by_subscriber[email] = {'sent': 0, 'opened': 0, 'clicked': 0, 'bounced': 0, 'complaint': 0, 'last_activity': ''}
            et = e.get('event_type', '')
            if et in by_subscriber[email]:
                by_subscriber[email][et] += 1
            ts = e.get('date', e.get('timestamp', ''))
            if str(ts) > by_subscriber[email]['last_activity']:
                by_subscriber[email]['last_activity'] = str(ts)
        
        subscribers = []
        for email, stats in by_subscriber.items():
            subscribers.append({
                'subscriber_email': email,
                'sent_count': stats['sent'],
                'open_count': stats['opened'],
                'click_count': stats['clicked'],
                'bounce_count': stats['bounced'],
                'complaint_count': stats['complaint'],
                'last_activity': stats['last_activity']
            })
        
        subscribers.sort(key=lambda x: x.get('last_activity', ''), reverse=True)
        return cors_response(200, {'subscribers': subscribers})
    except Exception as e:
        print(f"Get subscriber analytics error: {str(e)}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': 'Failed to get subscriber analytics'})

def get_recent_events(limit='100'):
    """Get recent email events from both tables"""
    try:
        from decimal import Decimal
        
        limit_int = int(limit)
        
        # Get from user-email-events (where email_sender logs)
        mt_events_table = dynamodb.Table('user-email-events')
        response = mt_events_table.query(
            KeyConditionExpression='user_id = :uid',
            ExpressionAttributeValues={':uid': PLATFORM_OWNER_ID},
            ScanIndexForward=False,
            Limit=limit_int
        )
        events = response.get('Items', [])
        
        # Also get from legacy email-events table
        legacy_response = events_table.scan(Limit=limit_int)
        legacy_events = legacy_response.get('Items', [])
        # Normalize legacy events to have subscriber_email field
        for le in legacy_events:
            if 'email' in le and 'subscriber_email' not in le:
                le['subscriber_email'] = le['email']
        
        all_events = events + legacy_events
        all_events.sort(key=lambda x: int(x.get('timestamp', 0)), reverse=True)
        all_events = all_events[:limit_int]
        
        # Convert Decimal to int/float
        def convert_decimals(obj):
            if isinstance(obj, list):
                return [convert_decimals(i) for i in obj]
            elif isinstance(obj, dict):
                return {k: convert_decimals(v) for k, v in obj.items()}
            elif isinstance(obj, Decimal):
                return int(obj) if obj % 1 == 0 else float(obj)
            else:
                return obj
        
        all_events = convert_decimals(all_events)
        
        return cors_response(200, {'events': all_events})
    except Exception as e:
        print(f"Get recent events error: {str(e)}")
        import traceback
        traceback.print_exc()
        return cors_response(500, {'error': 'Failed to get events'})
