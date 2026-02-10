"""
Email Analytics Queries
Run this script to view email campaign statistics and subscriber engagement
"""

import boto3
from collections import defaultdict
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
subscribers_table = dynamodb.Table('email-subscribers')
events_table = dynamodb.Table('email-events')

def get_total_subscribers():
    """Get total number of active subscribers"""
    response = subscribers_table.scan(
        FilterExpression='#status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'active'}
    )
    return len(response['Items'])

def get_campaign_stats(campaign_id):
    """Get detailed stats for a specific campaign"""
    response = events_table.scan(
        FilterExpression='campaign_id = :cid',
        ExpressionAttributeValues={':cid': campaign_id}
    )
    
    events = response['Items']
    
    stats = {
        'total_sent': 0,
        'total_opens': 0,
        'total_clicks': 0,
        'unique_opens': set(),
        'unique_clicks': set()
    }
    
    for event in events:
        email = event['email']
        event_type = event['event_type']
        
        if event_type == 'subscribed':
            stats['total_sent'] += 1
        elif event_type == 'opened':
            stats['total_opens'] += 1
            stats['unique_opens'].add(email)
        elif event_type == 'clicked':
            stats['total_clicks'] += 1
            stats['unique_clicks'].add(email)
    
    unique_opens = len(stats['unique_opens'])
    unique_clicks = len(stats['unique_clicks'])
    total_sent = max(stats['total_sent'], 1)  # Avoid division by zero
    
    return {
        'campaign_id': campaign_id,
        'total_sent': stats['total_sent'],
        'total_opens': stats['total_opens'],
        'unique_opens': unique_opens,
        'total_clicks': stats['total_clicks'],
        'unique_clicks': unique_clicks,
        'open_rate': f"{(unique_opens / total_sent) * 100:.1f}%",
        'click_rate': f"{(unique_clicks / total_sent) * 100:.1f}%",
        'click_to_open_rate': f"{(unique_clicks / max(unique_opens, 1)) * 100:.1f}%"
    }

def get_all_campaigns():
    """Get list of all campaigns"""
    response = events_table.scan()
    campaigns = set()
    
    for item in response['Items']:
        campaigns.add(item.get('campaign_id', 'unknown'))
    
    return sorted(list(campaigns))

def get_most_engaged_subscribers(limit=10):
    """Get subscribers with highest engagement"""
    response = subscribers_table.scan()
    subscribers = response['Items']
    
    # Sort by total engagement (opens + clicks)
    sorted_subscribers = sorted(
        subscribers,
        key=lambda x: x.get('total_opens', 0) + x.get('total_clicks', 0),
        reverse=True
    )
    
    return sorted_subscribers[:limit]

def get_recent_activity(days=7):
    """Get activity from last N days"""
    cutoff_timestamp = int((datetime.now() - timedelta(days=days)).timestamp())
    
    response = events_table.scan(
        FilterExpression='#ts > :cutoff',
        ExpressionAttributeNames={'#ts': 'timestamp'},
        ExpressionAttributeValues={':cutoff': cutoff_timestamp}
    )
    
    events = response['Items']
    
    activity = {
        'subscriptions': 0,
        'opens': 0,
        'clicks': 0
    }
    
    for event in events:
        event_type = event['event_type']
        if event_type == 'subscribed':
            activity['subscriptions'] += 1
        elif event_type == 'opened':
            activity['opens'] += 1
        elif event_type == 'clicked':
            activity['clicks'] += 1
    
    return activity

def print_dashboard():
    """Print complete analytics dashboard"""
    print("=" * 60)
    print("EMAIL ANALYTICS DASHBOARD")
    print("=" * 60)
    print()
    
    # Total subscribers
    total = get_total_subscribers()
    print(f"📊 TOTAL ACTIVE SUBSCRIBERS: {total}")
    print()
    
    # Recent activity
    print("📅 LAST 7 DAYS ACTIVITY:")
    activity = get_recent_activity(7)
    print(f"  New Subscriptions: {activity['subscriptions']}")
    print(f"  Email Opens: {activity['opens']}")
    print(f"  Link Clicks: {activity['clicks']}")
    print()
    
    # Campaign stats
    print("📧 CAMPAIGN PERFORMANCE:")
    campaigns = get_all_campaigns()
    
    for campaign in campaigns:
        stats = get_campaign_stats(campaign)
        print(f"\n  Campaign: {campaign}")
        print(f"    Sent: {stats['total_sent']}")
        print(f"    Opens: {stats['unique_opens']} unique ({stats['open_rate']})")
        print(f"    Clicks: {stats['unique_clicks']} unique ({stats['click_rate']})")
        print(f"    Click-to-Open: {stats['click_to_open_rate']}")
    
    print()
    
    # Most engaged subscribers
    print("🌟 TOP 10 MOST ENGAGED SUBSCRIBERS:")
    engaged = get_most_engaged_subscribers(10)
    
    for i, subscriber in enumerate(engaged, 1):
        email = subscriber['email']
        opens = subscriber.get('total_opens', 0)
        clicks = subscriber.get('total_clicks', 0)
        print(f"  {i}. {email}")
        print(f"     Opens: {opens}, Clicks: {clicks}")
    
    print()
    print("=" * 60)

if __name__ == '__main__':
    print_dashboard()
