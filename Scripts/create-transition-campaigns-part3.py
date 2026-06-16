import boto3
import sys
import uuid

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Email #5 - Free AI Survival Kit
campaign_5 = {
    'user_id': PLATFORM_OWNER_ID,
    'campaign_id': str(uuid.uuid4()),
    'campaign_name': 'Transition #5 - Free AI Survival Kit',
    'campaign_group': 'election-map-transition-sequence',
    'subject': 'FREE: Your AI Survival Kit (before you buy anything)',
    'content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #16a34a 0%, #15803d 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .free-badge { background: #16a34a; color: white; padding: 10px 20px; border-radius: 25px; display: inline-block; font-weight: bold; font-size: 18px; margin: 10px 0; }
        .kit-item { background: #f0fdf4; padding: 15px; margin: 10px 0; border-left: 4px solid #16a34a; }
        .button { display: inline-block; background: #16a34a; color: white; padding: 18px 50px; text-decoration: none; border-radius: 8px; margin: 25px 0; font-weight: bold; font-size: 18px; }
        .button:hover { background: #15803d; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🎁 FREE Resource for You</h1>
        <div class="free-badge">100% FREE - No Credit Card Required</div>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>I know I just told you about my book on AI and Christianity.</p>
        
        <p>But before you decide whether to buy it, I want to give you something for FREE:</p>
        
        <h2 style="text-align: center; color: #16a34a;">The AI Survival Kit for Christian Families</h2>
        
        <p>This is a free resource I put together to help Christians take immediate action - even if you're not ready to dive into the full book yet.</p>
        
        <h3>Here's what's inside:</h3>
        
        <div class="kit-item">
            📄 <strong>Quick-Start Guide:</strong> 5 things every Christian should know about AI (10-minute read)
        </div>
        
        <div class="kit-item">
            🛡️ <strong>Family Protection Checklist:</strong> How to protect your kids from AI's dangers
        </div>
        
        <div class="kit-item">
            🙏 <strong>Prayer Guide:</strong> Scriptures and prayers for the AI age
        </div>
        
        <div class="kit-item">
            💡 <strong>Practical Tips:</strong> How to use AI tools wisely (without compromising your values)
        </div>
        
        <div class="kit-item">
            📚 <strong>Recommended Resources:</strong> Books, articles, and tools to go deeper
        </div>
        
        <h3>Why am I giving this away for free?</h3>
        
        <p>Because I genuinely believe every Christian needs to be informed about AI - whether you buy my book or not. This is too important to gatekeep.</p>
        
        <div style="text-align: center; background: #f0fdf4; padding: 30px; margin: 30px 0; border-radius: 10px;">
            <h3 style="margin-top: 0;">Get Your Free AI Survival Kit</h3>
            <p>Just click below and enter your email. I'll send it to you instantly.</p>
            <a href="https://christianconservativestoday.com/book.html#survival-kit" class="button">GET MY FREE SURVIVAL KIT →</a>
            <p style="font-size: 14px; color: #666; margin-top: 15px;">No credit card required. Instant access.</p>
        </div>
        
        <p>And hey - if you find the Survival Kit helpful and want to go deeper, you can always grab the full book later. No pressure.</p>
        
        <p>My goal isn't to sell you something. It's to equip you for what's coming.</p>
        
        <p>Let's do this together.</p>
        
        <p>In Christ,<br>
        Christian Conservatives Today</p>
        
        <p><em>P.S. - The Survival Kit is 100% free. No strings attached. Just practical wisdom for Christians navigating the AI revolution.</em></p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
    </div>
</body>
</html>
    ''',
    'status': 'active',
    'delay_days': 10
}

# Email #6 - Last Chance
campaign_6 = {
    'user_id': PLATFORM_OWNER_ID,
    'campaign_id': str(uuid.uuid4()),
    'campaign_name': 'Transition #6 - Last Chance',
    'campaign_group': 'election-map-transition-sequence',
    'subject': 'Don\'t let AI catch you unprepared (final reminder)',
    'content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .urgency-box { background: #fef2f2; border: 3px solid #dc2626; padding: 20px; margin: 20px 0; border-radius: 8px; }
        .testimonial { background: #f8f9fa; padding: 20px; margin: 15px 0; border-left: 4px solid #2c5aa0; font-style: italic; }
        .button-primary { display: inline-block; background: #16a34a; color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; margin: 10px 5px; font-weight: bold; }
        .button-secondary { display: inline-block; background: #2c5aa0; color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; margin: 10px 5px; font-weight: bold; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>⏰ Final Reminder</h1>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>I've been sending you emails about AI and how Christians need to respond.</p>
        
        <p>Maybe you've been busy. Maybe you're still on the fence. Maybe you're thinking "I'll get to it later."</p>
        
        <p>I get it. Life is crazy.</p>
        
        <div class="urgency-box">
            <h3 style="margin-top: 0; color: #dc2626;">But here's the thing:</h3>
            <p><strong>AI isn't waiting for you to be ready.</strong></p>
        </div>
        
        <p>While you're deciding whether to pay attention, AI is:</p>
        
        <ul>
            <li>Influencing what your kids see online</li>
            <li>Shaping the news you read</li>
            <li>Making decisions about your job and finances</li>
            <li>Redefining what "truth" means in our culture</li>
        </ul>
        
        <p style="font-size: 20px; text-align: center; color: #dc2626;"><strong>You can't afford to ignore this.</strong></p>
        
        <h3>So here's my final offer:</h3>
        
        <p>If you haven't grabbed the <strong>FREE AI Survival Kit</strong> yet, now's the time. It takes 2 minutes to sign up, and you'll have practical tools to protect your family and engage AI wisely.</p>
        
        <p>And if you're ready to go deeper, the full book <strong>"How Christians Should Respond to AI"</strong> is available now.</p>
        
        <h3>Here's what readers are saying:</h3>
        
        <div class="testimonial">
            "This book opened my eyes to something I didn't even know I needed to understand. Every Christian should read this." <br>
            <strong>- Sarah M.</strong>
        </div>
        
        <div class="testimonial">
            "Finally, a balanced, biblical perspective on AI. Not fear-mongering, not naive - just wisdom." <br>
            <strong>- Pastor John K.</strong>
        </div>
        
        <div class="testimonial">
            "I bought this for myself and ended up buying 5 more copies for my small group." <br>
            <strong>- David R.</strong>
        </div>
        
        <h3 style="text-align: center;">The choice is yours:</h3>
        
        <div style="text-align: center; margin: 30px 0;">
            <p>✅ Stay informed and equipped</p>
            <p>❌ Stay in the dark and hope for the best</p>
        </div>
        
        <div style="text-align: center; background: #f8f9fa; padding: 30px; margin: 30px 0; border-radius: 10px;">
            <a href="https://christianconservativestoday.com/book.html#survival-kit" class="button-primary">GET FREE SURVIVAL KIT</a>
            <br>
            <a href="https://christianconservativestoday.com/book.html" class="button-secondary">BUY THE BOOK</a>
        </div>
        
        <p>I know which one I'd choose.</p>
        
        <p>Let's be ready for what's coming.</p>
        
        <p>Blessings,<br>
        Christian Conservatives Today</p>
        
        <p><em>P.S. - This is my last email specifically about the AI book. After this, I'll still send occasional updates about the platform, but I won't keep bugging you about AI. The ball is in your court.</em></p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
    </div>
</body>
</html>
    ''',
    'status': 'active',
    'delay_days': 14
}

# Email #7 - Stay Connected
campaign_7 = {
    'user_id': PLATFORM_OWNER_ID,
    'campaign_id': str(uuid.uuid4()),
    'campaign_name': 'Transition #7 - Stay Connected',
    'campaign_group': 'election-map-transition-sequence',
    'subject': 'Even if you don\'t buy the book, let\'s stay connected',
    'content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #2c5aa0 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .feature-box { background: #f0f7ff; padding: 20px; margin: 15px 0; border-left: 4px solid #2c5aa0; border-radius: 5px; }
        .feature-box h4 { margin-top: 0; color: #2c5aa0; }
        .button { display: inline-block; background: #2c5aa0; color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Let's Stay Connected 🤝</h1>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>Okay, I promise this is the last email about the AI book. 😊</p>
        
        <p>Whether you grabbed the free Survival Kit, bought the book, or just read my emails and moved on - I'm grateful you gave me your time and attention.</p>
        
        <h3>Here's the thing:</h3>
        
        <p>Even if AI isn't your focus right now, I still want to stay connected.</p>
        
        <p>Because the Christian Conservatives Today platform is about MORE than just AI. It's about equipping believers to live out their faith boldly in every area of life.</p>
        
        <h3>Here's how you can stay plugged in:</h3>
        
        <div class="feature-box">
            <h4>📰 Weekly Newsletter</h4>
            <p>Get the latest articles, videos, and resources delivered to your inbox</p>
        </div>
        
        <div class="feature-box">
            <h4>💬 Community Forums</h4>
            <p>Connect with other believers who are passionate about faith and culture</p>
        </div>
        
        <div class="feature-box">
            <h4>🎥 Video Content</h4>
            <p>Watch interviews, teachings, and discussions on the issues that matter</p>
        </div>
        
        <div class="feature-box">
            <h4>📚 Resource Library</h4>
            <p>Access tools, guides, and materials to help you grow</p>
        </div>
        
        <p><strong>No pressure. No sales pitches. Just a community of Christians trying to make a difference.</strong></p>
        
        <div style="text-align: center; background: #f8f9fa; padding: 30px; margin: 30px 0; border-radius: 10px;">
            <h3 style="margin-top: 0;">Stay Connected</h3>
            <p>Join our community and get weekly updates</p>
            <a href="https://christianconservativestoday.com" class="button">VISIT THE PLATFORM</a>
        </div>
        
        <p>And if you ever change your mind about the AI book or Survival Kit, you know where to find me. 😊</p>
        
        <h3>Thank you for being part of this journey.</h3>
        
        <p>Even if we never interact again, I'm praying for you. I'm praying that God uses you powerfully in whatever "mountain" He's called you to. And I'm praying that the church wakes up to the opportunities and challenges of this moment in history.</p>
        
        <p>Let's keep fighting the good fight.</p>
        
        <p>In Christ,<br>
        Christian Conservatives Today</p>
        
        <p><em>P.S. - If you ever want to reach out, just hit reply. I actually read these emails (or at least I try to!). I'd love to hear your story.</em></p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
        <p style="margin-top: 10px;">
            <a href="{{unsubscribe_url}}" style="color: #666;">Unsubscribe</a>
        </p>
    </div>
</body>
</html>
    ''',
    'status': 'active',
    'delay_days': 17
}

print("Creating campaigns 5, 6, and 7...")

try:
    campaigns_table.put_item(Item=campaign_5)
    print(f"✅ Created: {campaign_5['campaign_name']} (ID: {campaign_5['campaign_id']})")
    
    campaigns_table.put_item(Item=campaign_6)
    print(f"✅ Created: {campaign_6['campaign_name']} (ID: {campaign_6['campaign_id']})")
    
    campaigns_table.put_item(Item=campaign_7)
    print(f"✅ Created: {campaign_7['campaign_name']} (ID: {campaign_7['campaign_id']})")
    
    print("\n✅ Part 3 complete! All 7 transition campaigns created!")
    print("\n📧 Campaign Summary:")
    print("   Email #1 (Day 0): Welcome Back")
    print("   Email #2 (Day 3): The 7 Mountains")
    print("   Email #3 (Day 5): AI is Changing Everything")
    print("   Email #4 (Day 7): The Book Reveal")
    print("   Email #5 (Day 10): Free AI Survival Kit")
    print("   Email #6 (Day 14): Last Chance")
    print("   Email #7 (Day 17): Stay Connected")
    
except Exception as e:
    print(f"❌ Error: {e}")
