"""
Flask API for Email Dashboard
Provides REST API for subscriber management without exposing AWS credentials
Run: python dashboard_api.py
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from datetime import datetime

app = Flask(__name__)
CORS(app)

dynamodb = boto3.resource('dynamodb')
subscribers_table = dynamodb.Table('email-subscribers')
events_table = dynamodb.Table('email-events')

@app.route('/api/subscribers', methods=['GET'])
def get_subscribers():
    """Get all subscribers"""
    response = subscribers_table.scan()
    return jsonify(response['Items'])

@app.route('/api/subscribers/<email>', methods=['GET'])
def get_subscriber(email):
    """Get specific subscriber"""
    response = subscribers_table.get_item(Key={'email': email})
    if 'Item' in response:
        return jsonify(response['Item'])
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/subscribers/<email>/unsubscribe', methods=['POST'])
def unsubscribe(email):
    """Unsubscribe a user"""
    subscribers_table.update_item(
        Key={'email': email},
        UpdateExpression='SET #status = :status, unsubscribed_at = :date',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={
            ':status': 'unsubscribed',
            ':date': datetime.now().isoformat()
        }
    )
    return jsonify({'message': 'Unsubscribed'})

@app.route('/api/subscribers/<email>/resubscribe', methods=['POST'])
def resubscribe(email):
    """Resubscribe a user"""
    subscribers_table.update_item(
        Key={'email': email},
        UpdateExpression='SET #status = :status REMOVE unsubscribed_at',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'active'}
    )
    return jsonify({'message': 'Resubscribed'})

@app.route('/api/subscribers/<email>/resend', methods=['POST'])
def resend_welcome(email):
    """Resend welcome email"""
    import base64
    ses = boto3.client('ses', region_name='us-east-1')
    DOMAIN = 'https://christianconservativestoday.com'
    API_GATEWAY = 'https://niexv1rw75.execute-api.us-east-1.amazonaws.com'
    FROM_EMAIL = 'Christian Conservatives Today <contact@christianconservativestoday.com>'
    
    try:
        response = subscribers_table.get_item(Key={'email': email})
        if 'Item' not in response:
            return jsonify({'error': 'Not found'}), 404
        
        campaign_id = 'welcome-email-resend'
        tracking_id = base64.urlsafe_b64encode(f"{email}|{campaign_id}".encode()).decode()
        pixel_url = f"{API_GATEWAY}/track/open/{tracking_id}"
        election_map_data = f"{email}|{campaign_id}|{DOMAIN}/election-map.html"
        election_map_link = f"{API_GATEWAY}/track/click/{base64.urlsafe_b64encode(election_map_data.encode()).decode()}"
        unsubscribe_link = f"{DOMAIN}/unsubscribe.html?email={email}"
        
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
            <div style="background: white; padding: 30px; border-radius: 10px;">
                <h2 style="color: #667eea;">Welcome to Christian Conservatives Today!</h2>
                <p>Thank you for subscribing to our election updates and voter guides!</p>
                <ul>
                    <li>Election updates and critical dates</li>
                    <li>State-specific voter guides for all 50 states</li>
                    <li>Pro-life, pro-family candidate information</li>
                </ul>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{election_map_link}" style="display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px;">View Interactive Election Map</a>
                </div>
                <hr style="margin: 30px 0;">
                <p style="font-size: 12px; color: #999;"><a href="{unsubscribe_link}">Unsubscribe</a></p>
            </div>
            <img src="{pixel_url}" width="1" height="1" style="display:none;">
        </body>
        </html>
        """
        
        ses.send_email(
            Source=FROM_EMAIL,
            Destination={'ToAddresses': [email]},
            Message={
                'Subject': {'Data': 'Welcome to Christian Conservatives Today!'},
                'Body': {'Html': {'Data': html_body}}
            }
        )
        return jsonify({'message': 'Email sent'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events"""
    response = events_table.scan()
    return jsonify(response['Items'])

@app.route('/api/events/<email>', methods=['GET'])
def get_subscriber_events(email):
    """Get events for specific subscriber"""
    response = events_table.scan(
        FilterExpression='email = :email',
        ExpressionAttributeValues={':email': email}
    )
    return jsonify(response['Items'])

@app.route('/api/campaigns/send', methods=['POST'])
def send_campaign():
    """Send email campaign to all active subscribers"""
    import base64
    from datetime import datetime
    
    data = request.json
    subject = data.get('subject', '')
    html_content = data.get('html_content', '')
    campaign_id = data.get('campaign_id', f"campaign-{int(datetime.now().timestamp())}")
    
    if not subject or not html_content:
        return jsonify({'error': 'Subject and content required'}), 400
    
    ses = boto3.client('ses', region_name='us-east-1')
    DOMAIN = 'https://christianconservativestoday.com'
    FROM_EMAIL = 'Christian Conservatives Today <contact@christianconservativestoday.com>'
    
    # Get all active subscribers
    subs = subscribers_table.scan(
        FilterExpression='#status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'active'}
    )['Items']
    
    sent_count = 0
    failed = []
    
    for sub in subs:
        email = sub['email']
        try:
            # Add tracking pixel
            tracking_id = base64.urlsafe_b64encode(f"{email}|{campaign_id}".encode()).decode()
            API_GATEWAY = 'https://niexv1rw75.execute-api.us-east-1.amazonaws.com'
            pixel_url = f"{API_GATEWAY}/track/open/{tracking_id}"
            unsubscribe_link = f"{DOMAIN}/unsubscribe.html?email={email}"
            
            # Add click tracking to all links
            import re
            tracked_html = html_content
            
            # Find all href links
            def replace_link(match):
                original_url = match.group(1)
                # Skip if already a tracking link or unsubscribe link
                if 'track/click' in original_url or 'unsubscribe' in original_url:
                    return match.group(0)
                # Create tracked link
                link_data = f"{email}|{campaign_id}|{original_url}"
                tracked_id = base64.urlsafe_b64encode(link_data.encode()).decode()
                tracked_url = f"{API_GATEWAY}/track/click/{tracked_id}"
                return f'href="{tracked_url}"'
            
            tracked_html = re.sub(r'href="([^"]+)"', replace_link, tracked_html)
            
            # Inject tracking pixel and unsubscribe
            tracked_html = tracked_html.replace('</body>', f'<img src="{pixel_url}" width="1" height="1" style="display:none;"><p style="font-size:11px;color:#999;margin-top:20px;"><a href="{unsubscribe_link}">Unsubscribe</a></p></body>')
            
            ses.send_email(
                Source=FROM_EMAIL,
                Destination={'ToAddresses': [email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {'Html': {'Data': tracked_html}}
                }
            )
            sent_count += 1
        except Exception as e:
            failed.append({'email': email, 'error': str(e)})
    
    return jsonify({
        'message': f'Campaign sent to {sent_count} subscribers',
        'sent': sent_count,
        'failed': len(failed),
        'failures': failed
    })

@app.route('/api/subscribers', methods=['POST'])
def add_subscriber():
    """Manually add a subscriber"""
    data = request.json
    email = data.get('email', '').strip().lower()
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    # Check if exists
    response = subscribers_table.get_item(Key={'email': email})
    if 'Item' in response:
        return jsonify({'error': 'Email already exists'}), 400
    
    item = {
        'email': email,
        'status': 'active',
        'subscribed_at': datetime.now().isoformat(),
        'source': 'manual-dashboard',
        'total_opens': 0,
        'total_clicks': 0,
        'last_activity': datetime.now().isoformat()
    }
    if first_name:
        item['first_name'] = first_name
    if last_name:
        item['last_name'] = last_name
    
    subscribers_table.put_item(Item=item)
    return jsonify({'message': 'Subscriber added', 'email': email})

@app.route('/api/subscribers/<email>', methods=['PUT'])
def update_subscriber(email):
    """Update subscriber details"""
    data = request.json
    first_name = data.get('first_name', '').strip()
    last_name = data.get('last_name', '').strip()
    
    update_expr = 'SET '
    expr_values = {}
    expr_names = {}
    
    if first_name:
        update_expr += 'first_name = :fname, '
        expr_values[':fname'] = first_name
    if last_name:
        update_expr += 'last_name = :lname, '
        expr_values[':lname'] = last_name
    
    update_expr = update_expr.rstrip(', ')
    
    if not expr_values:
        return jsonify({'error': 'No fields to update'}), 400
    
    subscribers_table.update_item(
        Key={'email': email},
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_values
    )
    return jsonify({'message': 'Subscriber updated'})

@app.route('/api/subscribers/<email>', methods=['DELETE'])
def delete_subscriber(email):
    """Delete a subscriber"""
    subscribers_table.delete_item(Key={'email': email})
    return jsonify({'message': 'Subscriber deleted'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    subs = subscribers_table.scan()['Items']
    events = events_table.scan()['Items']
    
    active = len([s for s in subs if s.get('status') == 'active'])
    total_opens = sum(s.get('total_opens', 0) for s in subs)
    total_clicks = sum(s.get('total_clicks', 0) for s in subs)
    
    campaigns = {}
    for e in events:
        cid = e.get('campaign_id', 'unknown')
        if cid not in campaigns:
            campaigns[cid] = {'opens': 0, 'clicks': 0, 'subscribes': 0}
        if e['event_type'] == 'opened':
            campaigns[cid]['opens'] += 1
        elif e['event_type'] == 'clicked':
            campaigns[cid]['clicks'] += 1
        elif e['event_type'] == 'subscribed':
            campaigns[cid]['subscribes'] += 1
    
    return jsonify({
        'total': len(subs),
        'active': active,
        'unsubscribed': len(subs) - active,
        'total_opens': total_opens,
        'total_clicks': total_clicks,
        'campaigns': campaigns
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Email Dashboard API Server")
    print("="*60)
    print("\nStarting server on http://localhost:5000")
    print("\nAvailable endpoints:")
    print("  GET  /api/subscribers")
    print("  GET  /api/subscribers/<email>")
    print("  POST /api/subscribers (add new)")
    print("  PUT  /api/subscribers/<email> (edit)")
    print("  DELETE /api/subscribers/<email>")
    print("  POST /api/subscribers/<email>/unsubscribe")
    print("  POST /api/subscribers/<email>/resubscribe")
    print("  POST /api/subscribers/<email>/resend")
    print("  GET  /api/events")
    print("  GET  /api/events/<email>")
    print("  GET  /api/stats")
    print("  POST /api/campaigns/send")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, port=5000)
