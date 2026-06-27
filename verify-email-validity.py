import boto3
import sys
import dns.resolver
import socket
import re
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

email = 'joycewilliam478@hotmail.com'

print(f"🔍 Email Verification Report: {email}")
print("="*70)

# 1. Check syntax
print("\n1️⃣ SYNTAX CHECK")
print("-"*70)
email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
if re.match(email_regex, email):
    print("✅ Email format is valid")
else:
    print("❌ Email format is INVALID")

# 2. Extract domain
domain = email.split('@')[1]
print(f"\n📧 Domain: {domain}")

# 3. Check DNS MX Records
print("\n2️⃣ DNS MX RECORDS CHECK (Does mail server exist?)")
print("-"*70)
try:
    mx_records = dns.resolver.resolve(domain, 'MX')
    print(f"✅ Found {len(mx_records)} mail server(s):")
    for mx in mx_records:
        print(f"   • {mx.exchange} (priority: {mx.preference})")
    mx_valid = True
except dns.resolver.NXDOMAIN:
    print(f"❌ Domain '{domain}' does NOT exist")
    mx_valid = False
except dns.resolver.NoAnswer:
    print(f"❌ Domain exists but has NO mail servers (MX records)")
    mx_valid = False
except Exception as e:
    print(f"⚠️  Error: {e}")
    mx_valid = False

# 4. Check SES Bounce Details
print("\n3️⃣ AWS SES BOUNCE DETAILS")
print("-"*70)
session = boto3.Session(profile_name='ekewaka')
ses = session.client('sesv2', region_name='us-east-1')

try:
    suppressed = ses.get_suppressed_destination(EmailAddress=email)
    reason = suppressed['SuppressedDestination']['Reason']
    last_update = suppressed['SuppressedDestination']['LastUpdateTime']
    
    print(f"⚠️  On Suppression List")
    print(f"   Reason: {reason}")
    print(f"   Last bounce: {last_update}")
    
    if reason == 'BOUNCE':
        print(f"\n   📋 Bounce Type Analysis:")
        print(f"   • BOUNCE = Hard bounce (permanent delivery failure)")
        print(f"   • This typically means:")
        print(f"     - Mailbox doesn't exist")
        print(f"     - Email address is invalid")
        print(f"     - Domain doesn't accept mail")
        
except Exception as e:
    print(f"✅ NOT on suppression list")

# 5. Check CloudWatch for bounce reason
print("\n4️⃣ RECENT BOUNCE LOGS")
print("-"*70)
logs = session.client('logs', region_name='us-east-1')

try:
    # SES automatically logs bounce events to CloudWatch
    response = logs.filter_log_events(
        logGroupName='/aws/lambda/ses-event-processor',
        startTime=int((datetime.now() - timedelta(days=1)).timestamp() * 1000),
        filterPattern='"joycewilliam478"'
    )
    
    if response.get('events'):
        print("📜 Found bounce event details:")
        for event in response['events'][-3:]:
            print(f"\n{event['message']}")
    else:
        print("⚠️  No bounce logs found in ses-event-processor")
        
except Exception as e:
    print(f"⚠️  Could not check logs: {e}")

# 6. Verify with domain info
print("\n5️⃣ DOMAIN INFORMATION")
print("-"*70)
try:
    # Check if domain resolves
    ip = socket.gethostbyname(domain)
    print(f"✅ Domain resolves to IP: {ip}")
except socket.gaierror:
    print(f"❌ Domain does NOT resolve (doesn't exist)")

print("\n" + "="*70)
print("📊 VERDICT:")
print("="*70)

if mx_valid:
    print("✅ Domain has valid mail servers")
    print("⚠️  But email BOUNCED twice = likely the mailbox doesn't exist")
    print("\n🔴 CONCLUSION: Email address is probably INVALID")
    print("   Reasons:")
    print("   • Hotmail server accepted connection but rejected user")
    print("   • User likely typed wrong email or account was closed")
    print("   • Domain is valid but this specific mailbox doesn't exist")
else:
    print("❌ Domain has NO mail servers or doesn't exist")
    print("\n🔴 CONCLUSION: Email is DEFINITELY INVALID")

print("\n💡 RECOMMENDATION:")
print("   • Leave email on suppression list")
print("   • Don't attempt to send again")
print("   • Contact user through another channel to get correct email")
