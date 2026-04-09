import boto3
import os

os.environ['AWS_PROFILE'] = 'ekewaka'

db = boto3.resource('dynamodb', region_name='us-east-1')
table = db.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'
CAMPAIGN_ID = '2b8d8840-25c7-4de1-b9d3-3aca442241da'

# Correct HTML content with purchaser-resources link
html_content = """<div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
<p>Hey {{first_name}},</p>

<p>Quick tip as you start reading:</p>

<p><strong>Don't rush it.</strong></p>

<p>This book is designed to make you think.</p>

<p>You might find it helpful to:</p>
<ul>
<li>take notes</li>
<li>discuss with others</li>
<li>revisit key sections</li>
</ul>

<p>There's also a discussion guide you can use if you want to go deeper.</p>

<p>👉 <a href="https://christianconservativestoday.com/purchaser-resources.html?email={{email}}">Download Guide</a></p>

<p>This is not just information — it's meant to be applied.</p>

<p>— Ed</p>
</div>"""

# Update the campaign
table.update_item(
    Key={
        'user_id': PLATFORM_OWNER_ID,
        'campaign_id': CAMPAIGN_ID
    },
    UpdateExpression='SET html_content = :html',
    ExpressionAttributeValues={
        ':html': html_content
    }
)

print("Updated Post-Purchase Email #2")
print("  Changed: book-resources.html -> purchaser-resources.html")
