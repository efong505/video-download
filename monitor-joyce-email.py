import boto3
import sys
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

email = 'joycewilliam478@hotmail.com'
session = boto3.Session(profile_name='ekewaka')

print(f"📊 Monitoring email delivery for: {email}\n")
print("="*70)

# 1. Check CloudWatch Logs for recent sends
print("\n1️⃣ CHECKING SES SEND LOGS (last 10 minutes)...")
print("-"*70)
logs_client = session.client('logs', region_name='us-east-1')

try:
    # Check email-sender Lambda logs
    log_groups = [
        '/aws/lambda/email-sender',
        '/aws/lambda/email-drip-processor',
        '/aws/lambda/email-subscription-handler'
    ]
    
    start_time = int((datetime.now() - timedelta(minutes=10)).timestamp() * 1000)
    
    for log_group in log_groups:
        try:
            response = logs_client.filter_log_events(
                logGroupName=log_group,
                startTime=start_time,
                filterPattern=email
            )
            
            if response['events']:
                print(f"\n✅ Found in {log_group}:")
                for event in response['events'][-5:]:  # Last 5 events
                    timestamp = datetime.fromtimestamp(event['timestamp']/1000).strftime('%Y-%m-%d %H:%M:%S')
                    message = event['message'].strip()[:200]
                    print(f"   [{timestamp}] {message}")
            
        except Exception as e:
            if 'ResourceNotFoundException' not in str(e):
                print(f"   ⚠️  Error checking {log_group}: {e}")
    
except Exception as e:
    print(f"❌ Error checking logs: {e}")

# 2. Check DynamoDB user-email-events
print("\n\n2️⃣ CHECKING EMAIL EVENTS TABLE...")
print("-"*70)
ddb = session.resource('dynamodb', region_name='us-east-1')
events_table = ddb.Table('user-email-events')

try:
    # Query by user_id
    response = events_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': email},
        ScanIndexForward=False,
        Limit=10
    )
    
    if response['Items']:
        print(f"✅ Found {len(response['Items'])} recent events:\n")
        for item in response['Items']:
            timestamp = item.get('timestamp', 'N/A')
            event_type = item.get('event_type', 'unknown')
            campaign = item.get('campaign_id', 'N/A')
            print(f"   • [{timestamp}] {event_type} - Campaign: {campaign}")
    else:
        print(f"⚠️  No events found yet (events may take a few minutes to appear)")
        
except Exception as e:
    print(f"❌ Error: {e}")

# 3. Check SES sending statistics
print("\n\n3️⃣ CHECKING SES SEND STATISTICS...")
print("-"*70)
ses_client = session.client('ses', region_name='us-east-1')

try:
    stats = ses_client.get_send_statistics()
    
    if stats['SendDataPoints']:
        # Get most recent data point
        recent = sorted(stats['SendDataPoints'], key=lambda x: x['Timestamp'], reverse=True)[0]
        print(f"✅ Last 15 minutes stats:")
        print(f"   • Sent: {int(recent['DeliveryAttempts'])}")
        print(f"   • Bounces: {int(recent['Bounces'])}")
        print(f"   • Complaints: {int(recent['Complaints'])}")
        print(f"   • Rejects: {int(recent['Rejects'])}")
    
except Exception as e:
    print(f"❌ Error: {e}")

# 4. Check suppression list
print("\n\n4️⃣ CHECKING SES SUPPRESSION LIST...")
print("-"*70)
try:
    suppressed = ses_client.get_suppressed_destination(
        EmailAddress=email
    )
    print(f"❌ STILL ON SUPPRESSION LIST!")
    print(f"   Reason: {suppressed['SuppressedDestination']['Reason']}")
    print(f"   Since: {suppressed['SuppressedDestination']['LastUpdateTime']}")
    print(f"\n⚠️  Email will NOT be delivered until removed from suppression list!")
    
except ses_client.exceptions.NotFoundException:
    print(f"✅ NOT on suppression list - emails can be delivered")
    
except Exception as e:
    print(f"⚠️  Error checking: {e}")

# 5. Check enrollments
print("\n\n5️⃣ CHECKING ENROLLMENT STATUS...")
print("-"*70)
enrollments_table = ddb.Table('user-email-drip-enrollments')

try:
    response = enrollments_table.scan()
    matching = [item for item in response['Items'] if email in item.get('enrollment_id', '')]
    
    if matching:
        print(f"✅ Found {len(matching)} enrollments:\n")
        for item in matching:
            print(f"   Campaign: {item.get('campaign_group')}")
            print(f"   Step: {item.get('current_step')} / {item.get('total_steps', 'N/A')}")
            print(f"   Status: {item.get('status')}")
            print(f"   Last sent: {item.get('last_sent_date', 'Never')}")
            print(f"   Next send: {item.get('next_send_date', 'N/A')}")
            print()
    else:
        print(f"⚠️  No active enrollments found")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*70)
print("💡 HOW TO CONTINUE MONITORING:")
print("="*70)
print("1. Open advanced-email-analytics.html in browser")
print("2. Click 'Recent Events' tab")
print(f"3. Filter by: {email}")
print("4. Look for 'sent', 'delivered', 'opened', or 'bounced' events")
print("\nOR")
print("\nCheck CloudWatch Logs manually:")
print("• https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups")
print("• Filter log group: /aws/lambda/email-sender")
print(f"• Search for: {email}")
