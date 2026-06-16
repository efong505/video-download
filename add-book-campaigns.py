import boto3
import sys
import uuid
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'
campaigns_table = dynamodb.Table('user-email-campaigns')

# Campaign #6 - AI & Faith Introduction
campaign6_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #16a34a 0%, #15803d 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .highlight { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 The AI Revolution & Your Faith</h1>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>We've talked about the 7 Mountains and how Christians are called to influence culture. But there's one force that's reshaping ALL seven mountains faster than anything in history:</p>
        
        <p style="text-align: center; font-size: 20px; font-weight: bold; color: #16a34a;">Artificial Intelligence</p>
        
        <h3>AI is already transforming:</h3>
        
        <ul>
            <li><strong>Education</strong> - AI tutors, personalized learning, and automated grading</li>
            <li><strong>Business</strong> - Customer service, hiring decisions, and market predictions</li>
            <li><strong>Media</strong> - Content creation, news curation, and deepfakes</li>
            <li><strong>Government</strong> - Surveillance, law enforcement, and policy analysis</li>
            <li><strong>Family</strong> - Parenting apps, relationship advice, and home automation</li>
            <li><strong>Arts</strong> - AI-generated music, art, and entertainment</li>
            <li><strong>Religion</strong> - AI sermon writers, prayer apps, and "digital disciples"</li>
        </ul>
        
        <div class="highlight">
            <p><strong>The question isn't whether AI will impact your mountain.</strong></p>
            <p><strong>The question is: Will you be prepared to navigate it with biblical wisdom?</strong></p>
        </div>
        
        <h3>Here's the challenge:</h3>
        
        <p>Most Christians are either:</p>
        <ul>
            <li>❌ Completely ignoring AI (hoping it goes away)</li>
            <li>❌ Embracing it uncritically (without considering the spiritual implications)</li>
            <li>❌ Paralyzed by fear (seeing only the dangers)</li>
        </ul>
        
        <p><strong>But there's a better way.</strong></p>
        
        <p>What if you could harness AI's power for Kingdom purposes while protecting yourself from its dangers?</p>
        
        <p>That's exactly why I wrote <em><strong>The Necessary Evil: A Christian's Guide to Navigating AI Without Losing Your Soul</strong></em>.</p>
        
        <h3>📖 What you'll discover:</h3>
        
        <ul>
            <li>The 7 spiritual dangers of AI (and how to guard against them)</li>
            <li>How to use AI tools ethically as a Christian</li>
            <li>Practical safeguards for your family in an AI-driven world</li>
            <li>Biblical principles for discerning truth in the age of deepfakes</li>
            <li>How AI is being used to target Christians and erode religious freedom</li>
        </ul>
        
        <div class="highlight">
            <p><strong>🎁 FREE Christian AI Survival Kit ($71 value)</strong></p>
            <p>When you sign up, you'll get instant access to:</p>
            <ul>
                <li>30-page book preview</li>
                <li>Christian AI Survival Guide</li>
                <li>Church Discussion Guide (10 sessions)</li>
                <li>AI Parent Guide</li>
            </ul>
        </div>
        
        <p style="text-align: center;">
            <a href="https://christianconservativestoday.com/the-necessary-evil-book.html" style="display: inline-block; background: #16a34a; color: #ffffff !important; padding: 15px 35px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; font-size: 16px;">📥 Get Your FREE Survival Kit</a>
        </p>
        
        <p>Tomorrow, I'll share a specific example of how AI is already being used to target Christian values - and what you can do about it.</p>
        
        <p>In Christ,<br>
        Christian Conservatives Today</p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
        <p><a href="{{unsubscribe_link}}">Unsubscribe</a></p>
    </div>
</body>
</html>"""

# Campaign #7 - AI Threats & Book Offer
campaign7_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .highlight { background: #fee2e2; border-left: 4px solid #dc2626; padding: 15px; margin: 20px 0; }
        .success { background: #d1fae5; border-left: 4px solid #16a34a; padding: 15px; margin: 20px 0; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>⚠️ How AI is Targeting Christians</h1>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>Yesterday I introduced you to the AI revolution. Today, I need to share something urgent.</p>
        
        <h3>AI is already being weaponized against Christian values:</h3>
        
        <div class="highlight">
            <p><strong>🎯 Content Censorship</strong></p>
            <p>AI algorithms on social media platforms are trained to flag "controversial" content - which often includes biblical teachings on marriage, gender, and morality.</p>
        </div>
        
        <div class="highlight">
            <p><strong>🎯 Hiring Discrimination</strong></p>
            <p>AI hiring tools can be programmed to filter out candidates from Christian colleges or with "religious bias" in their social media history.</p>
        </div>
        
        <div class="highlight">
            <p><strong>🎯 Worldview Manipulation</strong></p>
            <p>AI chatbots like ChatGPT are trained on datasets that often present secular worldviews as "neutral" while framing Christian perspectives as "extreme."</p>
        </div>
        
        <div class="highlight">
            <p><strong>🎯 Deepfake Deception</strong></p>
            <p>AI can now create fake videos of pastors saying things they never said, or fabricate "evidence" to discredit Christian leaders.</p>
        </div>
        
        <h3>But here's the good news:</h3>
        
        <p>You don't have to be a victim of AI. You can learn to:</p>
        
        <ul>
            <li>✅ Spot AI-generated deception</li>
            <li>✅ Use AI tools without compromising your values</li>
            <li>✅ Protect your family from AI manipulation</li>
            <li>✅ Advocate for AI policies that protect religious freedom</li>
        </ul>
        
        <div class="success">
            <p style="font-size: 18px; font-weight: bold; margin-top: 0;">📖 The Necessary Evil: Your Complete Guide</p>
            <p>This isn't just a book about AI - it's a survival manual for Christians living in an AI-dominated world.</p>
            <p><strong>Written specifically for believers who want to:</strong></p>
            <ul>
                <li>Understand AI without needing a tech degree</li>
                <li>Apply biblical wisdom to cutting-edge technology</li>
                <li>Protect their families from AI's spiritual dangers</li>
                <li>Use AI as a tool for Kingdom impact</li>
            </ul>
        </div>
        
        <h3>🎁 Start with the FREE Survival Kit</h3>
        
        <p>Not ready to buy the book? No problem!</p>
        
        <p>Get instant access to <strong>$71 worth of free resources</strong>:</p>
        
        <ul>
            <li>📖 <strong>30-Page Book Preview</strong> - Read the introduction + most powerful chapters</li>
            <li>🛡️ <strong>Christian AI Survival Guide</strong> - 7 safeguards for using AI without losing your soul</li>
            <li>⛪ <strong>Church Discussion Guide</strong> - 10-session study for small groups</li>
            <li>👨‍👩‍👧 <strong>AI Parent Guide</strong> - Protect your children in an AI-driven world</li>
        </ul>
        
        <p style="text-align: center;">
            <a href="https://christianconservativestoday.com/the-necessary-evil-book.html" style="display: inline-block; background: #16a34a; color: #ffffff !important; padding: 15px 35px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; font-size: 16px;">📥 Get Your FREE Survival Kit Now</a>
        </p>
        
        <p style="text-align: center; font-size: 14px; color: #666;">
            <em>Plus: Read the 30-page preview online instantly</em>
        </p>
        
        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
        
        <h3>📚 Want the full book?</h3>
        
        <p>Available now on:</p>
        <ul>
            <li>Amazon Kindle (instant download)</li>
            <li>Amazon Paperback & Hardcover</li>
            <li>Signed copies direct from the author</li>
        </ul>
        
        <p style="text-align: center;">
            <a href="https://christianconservativestoday.com/the-necessary-evil-book.html#purchase" style="display: inline-block; background: #2c5aa0; color: #ffffff !important; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 10px 0; font-weight: bold;">📚 Get the Full Book</a>
        </p>
        
        <p>Don't let AI catch you unprepared. Equip yourself with biblical wisdom for the AI age.</p>
        
        <p>In Christ,<br>
        Christian Conservatives Today</p>
        
        <p style="font-size: 12px; color: #999; margin-top: 30px;">
            <em>P.S. - Even if you just grab the free survival kit, you'll be better equipped than 99% of Christians to navigate the AI revolution with your faith intact.</em>
        </p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
        <p><a href="{{unsubscribe_link}}">Unsubscribe</a></p>
    </div>
</body>
</html>"""

# Create campaign #6
campaign6_id = str(uuid.uuid4())
campaigns_table.put_item(Item={
    'user_id': PLATFORM_OWNER_ID,
    'campaign_id': campaign6_id,
    'campaign_name': 'AI & Faith - Book Introduction',
    'campaign_group': 'general-newsletter-sequence',
    'sequence_number': 6,
    'delay_days': 2,
    'delay_hours': 0,
    'subject': '🤖 AI is reshaping your mountain (are you ready?)',
    'html_content': campaign6_html,
    'created_at': datetime.now().isoformat(),
    'updated_at': datetime.now().isoformat()
})
print(f"✅ Created Campaign #6: AI & Faith - Book Introduction")
print(f"   Subject: 🤖 AI is reshaping your mountain (are you ready?)")
print(f"   Delay: 2 days after campaign #5")

# Create campaign #7
campaign7_id = str(uuid.uuid4())
campaigns_table.put_item(Item={
    'user_id': PLATFORM_OWNER_ID,
    'campaign_id': campaign7_id,
    'campaign_name': 'AI Threats & Book Offer',
    'campaign_group': 'general-newsletter-sequence',
    'sequence_number': 7,
    'delay_days': 1,
    'delay_hours': 0,
    'subject': '⚠️ How AI is targeting Christians (and what you can do)',
    'html_content': campaign7_html,
    'created_at': datetime.now().isoformat(),
    'updated_at': datetime.now().isoformat()
})
print(f"\n✅ Created Campaign #7: AI Threats & Book Offer")
print(f"   Subject: ⚠️ How AI is targeting Christians (and what you can do)")
print(f"   Delay: 1 day after campaign #6")

print(f"\n✅ General newsletter sequence now has 7 emails total")
print(f"   Timeline: Day 0, +2, +2, +2, +2, +2, +1 = 11 days total")
