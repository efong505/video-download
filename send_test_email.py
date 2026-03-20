import boto3
import json

# Send test email via SES directly
ses = boto3.client('ses', region_name='us-east-1')

html_body = """
<html>
<body>
<h2>Test Email - Day 1 Drip Campaign</h2>
<p>Hey Edward,</p>
<p>This is a test of the drip email system with the footer included.</p>
<p>If you're seeing this, the email system is working!</p>

<hr style="margin-top: 30px; border: none; border-top: 1px solid #ddd;">
<p style="font-size: 12px; color: #666;">
You're receiving this because you signed up for the Christian AI Survival Kit.<br>
<a href="https://christianconservativestoday.com/manage-email-preferences.html?email=hawaiianintucson@gmail.com">Manage Email Preferences</a> | 
<a href="https://christianconservativestoday.com/unsubscribe?email=hawaiianintucson@gmail.com">Unsubscribe</a>
</p>
</body>
</html>
"""

try:
    response = ses.send_email(
        Source='contact@christianconservativestoday.com',
        Destination={'ToAddresses': ['hawaiianintucson@gmail.com']},
        Message={
            'Subject': {'Data': 'Test: Day 1 - Your First Step with AI'},
            'Body': {'Html': {'Data': html_body}}
        }
    )
    print(f"Email sent! Message ID: {response['MessageId']}")
except Exception as e:
    print(f"Error sending email: {e}")
