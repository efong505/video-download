"""
Backfill Subscriber Stats from Email Events
This script scans all email events and ensures every subscriber has an entry in email-subscriber-stats
"""
import boto3
from datetime import datetime
from collections import defaultdict

# Use ekewaka profile
session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
events_table = dynamodb.Table('email-events')
subscriber_stats_table = dynamodb.Table('email-subscriber-stats')

def scan_all_events():
    """Scan all events from email-events table"""
    print("Scanning all email events...")
    
    events = []
    last_key = None
    
    while True:
        if last_key:
            response = events_table.scan(ExclusiveStartKey=last_key)
        else:
            response = events_table.scan()
        
        events.extend(response.get('Items', []))
        
        last_key = response.get('LastEvaluatedKey')
        if not last_key:
            break
    
    print(f"Found {len(events)} total events")
    return events

def aggregate_subscriber_stats(events):
    """Aggregate stats by subscriber email"""
    print("Aggregating stats by subscriber...")
    
    stats = defaultdict(lambda: {
        'emails_sent': 0,
        'emails_delivered': 0,
        'opens': 0,
        'clicks': 0,
        'bounces': 0,
        'complaints': 0,
        'last_activity': None
    })
    
    for event in events:
        email = event.get('email', '')
        event_type = event.get('event_type', '')
        date = event.get('date', '')
        
        if not email or email == 'unknown':
            continue
        
        # Update last activity
        if not stats[email]['last_activity'] or date > stats[email]['last_activity']:
            stats[email]['last_activity'] = date
        
        # Count events
        if event_type in ['sent', 'subscribed']:
            stats[email]['emails_sent'] += 1
        elif event_type == 'delivered':
            stats[email]['emails_delivered'] += 1
        elif event_type in ['opened', 'confirmed']:  # Count confirmed as activity
            stats[email]['opens'] += 1
        elif event_type == 'clicked':
            stats[email]['clicks'] += 1
        elif event_type == 'bounced':
            stats[email]['bounces'] += 1
        elif event_type == 'complaint':
            stats[email]['complaints'] += 1
    
    print(f"Aggregated stats for {len(stats)} unique subscribers")
    return stats

def update_subscriber_stats_table(stats):
    """Update or create subscriber stats in DynamoDB"""
    print("Updating subscriber stats table...")
    
    updated = 0
    created = 0
    
    for email, subscriber_stats in stats.items():
        try:
            # Try to get existing record
            response = subscriber_stats_table.get_item(Key={'subscriber_email': email})
            
            if 'Item' in response:
                # Update existing
                subscriber_stats_table.update_item(
                    Key={'subscriber_email': email},
                    UpdateExpression='''
                        SET emails_sent = :sent,
                            emails_delivered = :delivered,
                            opens = :opens,
                            clicks = :clicks,
                            bounces = :bounces,
                            complaints = :complaints,
                            last_activity = :activity
                    ''',
                    ExpressionAttributeValues={
                        ':sent': subscriber_stats['emails_sent'],
                        ':delivered': subscriber_stats['emails_delivered'],
                        ':opens': subscriber_stats['opens'],
                        ':clicks': subscriber_stats['clicks'],
                        ':bounces': subscriber_stats['bounces'],
                        ':complaints': subscriber_stats['complaints'],
                        ':activity': subscriber_stats['last_activity']
                    }
                )
                updated += 1
            else:
                # Create new
                subscriber_stats_table.put_item(Item={
                    'subscriber_email': email,
                    'emails_sent': subscriber_stats['emails_sent'],
                    'emails_delivered': subscriber_stats['emails_delivered'],
                    'opens': subscriber_stats['opens'],
                    'clicks': subscriber_stats['clicks'],
                    'bounces': subscriber_stats['bounces'],
                    'complaints': subscriber_stats['complaints'],
                    'last_activity': subscriber_stats['last_activity']
                })
                created += 1
            
            if (updated + created) % 10 == 0:
                print(f"Progress: {updated} updated, {created} created")
                
        except Exception as e:
            print(f"Error updating {email}: {str(e)}")
            continue
    
    print(f"\nCompleted: {updated} updated, {created} created")
    return updated, created

def main():
    print("=" * 60)
    print("Backfilling Subscriber Stats")
    print("=" * 60)
    
    # Scan all events
    events = scan_all_events()
    
    # Aggregate by subscriber
    stats = aggregate_subscriber_stats(events)
    
    # Update DynamoDB
    updated, created = update_subscriber_stats_table(stats)
    
    print("\n" + "=" * 60)
    print("Backfill Complete!")
    print(f"Total subscribers: {len(stats)}")
    print(f"Updated: {updated}")
    print(f"Created: {created}")
    print("=" * 60)

if __name__ == '__main__':
    main()
