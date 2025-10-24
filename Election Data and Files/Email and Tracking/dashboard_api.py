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
    print("  POST /api/subscribers/<email>/unsubscribe")
    print("  POST /api/subscribers/<email>/resubscribe")
    print("  GET  /api/events")
    print("  GET  /api/events/<email>")
    print("  GET  /api/stats")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, port=5000)
