import boto3
import uuid
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

campaigns = [
    {
        'step': 1,
        'delay_days': 0,
        'subject': 'Welcome to Christian Conservatives Today! 🙏',
        'campaign_name': 'Welcome - Introduction',
        'html_content': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #2c5aa0 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .highlight { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
        .button { display: inline-block; background: #2c5aa0; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Welcome! 🙏</h1>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>Thank you for subscribing to Christian Conservatives Today!</p>
        
        <p>I'm excited to have you join our community of believers who are committed to living out their faith in every area of life - not just on Sunday mornings.</p>
        
        <h3>What is Christian Conservatives Today?</h3>
        
        <p>We're a platform dedicated to helping Christians engage with culture through the lens of the <strong>7 Mountains of Influence</strong>:</p>
        
        <ul>
            <li>Family</li>
            <li>Religion</li>
            <li>Education</li>
            <li>Media</li>
            <li>Arts & Entertainment</li>
            <li>Business & Economics</li>
            <li>Government</li>
        </ul>
        
        <div class="highlight">
            <p><strong>Our mission:</strong> To equip Christians to be salt and light in their spheres of influence - whether that's in the classroom, the boardroom, the voting booth, or the living room.</p>
        </div>
        
        <h3>What to expect from these emails:</h3>
        
        <p>Over the next few days, I'll send you a series of emails to help you:</p>
        
        <ul>
            <li>Understand the 7 Mountains strategy</li>
            <li>Discover which "mountain" you're called to influence</li>
            <li>Get practical resources for living out your faith</li>
            <li>Stay informed on issues that matter to Christian conservatives</li>
        </ul>
        
        <p>In the meantime, feel free to explore the platform:</p>
        
        <p style="text-align: center;">
            <a href="https://christianconservativestoday.com" class="button">Explore the Platform</a>
        </p>
        
        <p>Looking forward to this journey together!</p>
        
        <p>Blessings,<br>
        Christian Conservatives Today</p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
        <p><a href="{{unsubscribe_link}}">Unsubscribe</a></p>
    </div>
</body>
</html>'''
    },
    {
        'step': 2,
        'delay_days': 2,
        'subject': 'The 7 Mountains that shape our world (and why it matters)',
        'campaign_name': 'The 7 Mountains Explained',
        'html_content': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #2c5aa0 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .mountain-box { background: #f8f9fa; border-left: 4px solid #d4af37; padding: 15px; margin: 10px 0; }
        .mountain-box h4 { margin: 0 0 5px 0; color: #2c5aa0; }
        .highlight { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
        .button { display: inline-block; background: #2c5aa0; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>The 7 Mountains 🏔️</h1>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>Yesterday I welcomed you to Christian Conservatives Today. Today, I want to explain the core concept that drives everything we do: <strong>The 7 Mountains of Influence.</strong></p>
        
        <h3>Culture is shaped by 7 key areas:</h3>
        
        <div class="mountain-box">
            <h4>1. Family</h4>
            <p>The foundation of civilization - where values are first taught and lived</p>
        </div>
        
        <div class="mountain-box">
            <h4>2. Religion</h4>
            <p>Spiritual and moral guidance for individuals and communities</p>
        </div>
        
        <div class="mountain-box">
            <h4>3. Education</h4>
            <p>What we teach the next generation shapes the future</p>
        </div>
        
        <div class="mountain-box">
            <h4>4. Media</h4>
            <p>Who controls the narrative controls the culture</p>
        </div>
        
        <div class="mountain-box">
            <h4>5. Arts & Entertainment</h4>
            <p>What captures our imagination shapes our values</p>
        </div>
        
        <div class="mountain-box">
            <h4>6. Business & Economics</h4>
            <p>Where resources flow determines what gets built</p>
        </div>
        
        <div class="mountain-box">
            <h4>7. Government</h4>
            <p>Laws and policies that affect every area of life</p>
        </div>
        
        <div class="highlight">
            <h3>Here's the problem:</h3>
            <p>For decades, Christians have retreated from these mountains. We've focused on personal piety while secular forces have taken over education, media, entertainment, business, and government.</p>
            <p><strong>The result?</strong> A culture increasingly hostile to Christian values.</p>
        </div>
        
        <h3>The 7 Mountains strategy says:</h3>
        
        <p>Christians need to be present, active, and influential in ALL these areas - not just church on Sunday.</p>
        
        <p>We're not called to retreat. We're called to be <strong>salt and light</strong> (Matthew 5:13-16).</p>
        
        <p>Tomorrow, I'll help you discover which mountain YOU are called to influence.</p>
        
        <p>Blessings,<br>
        Christian Conservatives Today</p>
        
        <p><em>P.S. - Want to explore each mountain on the platform? <a href="https://christianconservativestoday.com">Visit our homepage</a></em></p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
        <p><a href="{{unsubscribe_link}}">Unsubscribe</a></p>
    </div>
</body>
</html>'''
    },
    {
        'step': 3,
        'delay_days': 2,
        'subject': 'Which mountain are YOU called to? 🤔',
        'campaign_name': 'Discover Your Mountain',
        'html_content': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #2c5aa0 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .question-box { background: #e3f2fd; border-left: 4px solid #2c5aa0; padding: 15px; margin: 15px 0; }
        .highlight { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
        .button { display: inline-block; background: #2c5aa0; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Your Calling 🤔</h1>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>Now that you understand the 7 Mountains, here's the most important question:</p>
        
        <h2 style="text-align: center; color: #2c5aa0;">Which mountain are YOU called to influence?</h2>
        
        <p>The answer might be more obvious than you think. Consider:</p>
        
        <div class="question-box">
            <p><strong>Are you a parent or grandparent?</strong><br>
            You're influencing the <strong>Family</strong> mountain.</p>
        </div>
        
        <div class="question-box">
            <p><strong>Do you work in education or homeschool your kids?</strong><br>
            You're on the <strong>Education</strong> mountain.</p>
        </div>
        
        <div class="question-box">
            <p><strong>Do you own a business or work in corporate America?</strong><br>
            You're climbing the <strong>Business & Economics</strong> mountain.</p>
        </div>
        
        <div class="question-box">
            <p><strong>Are you involved in local politics or community organizing?</strong><br>
            You're on the <strong>Government</strong> mountain.</p>
        </div>
        
        <div class="question-box">
            <p><strong>Do you create content, write, or work in communications?</strong><br>
            You're influencing the <strong>Media</strong> mountain.</p>
        </div>
        
        <div class="question-box">
            <p><strong>Are you an artist, musician, or work in entertainment?</strong><br>
            You're on the <strong>Arts & Entertainment</strong> mountain.</p>
        </div>
        
        <div class="question-box">
            <p><strong>Are you a pastor, ministry leader, or active in your church?</strong><br>
            You're on the <strong>Religion</strong> mountain.</p>
        </div>
        
        <div class="highlight">
            <h3>Here's the truth:</h3>
            <p>God hasn't placed you where you are by accident. Your job, your family, your community - these are your mission field.</p>
            <p><strong>You don't need to quit your job to serve God. You need to serve God IN your job.</strong></p>
        </div>
        
        <h3>Explore your mountain:</h3>
        
        <p>On our platform, each mountain has its own hub with:</p>
        <ul>
            <li>Articles and resources specific to your sphere</li>
            <li>Stories of Christians making a difference</li>
            <li>Practical ways to live out your faith</li>
            <li>A community of like-minded believers</li>
        </ul>
        
        <p style="text-align: center;">
            <a href="https://christianconservativestoday.com" class="button">Explore Your Mountain</a>
        </p>
        
        <p>Tomorrow, I'll share some practical ways to start making an impact right where you are.</p>
        
        <p>Blessings,<br>
        Christian Conservatives Today</p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
        <p><a href="{{unsubscribe_link}}">Unsubscribe</a></p>
    </div>
</body>
</html>'''
    },
    {
        'step': 4,
        'delay_days': 2,
        'subject': '3 ways to start making an impact TODAY',
        'campaign_name': 'Practical Action Steps',
        'html_content': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #2c5aa0 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .action-box { background: #e8f5e9; border-left: 4px solid #4caf50; padding: 20px; margin: 15px 0; }
        .action-box h3 { margin: 0 0 10px 0; color: #2c5aa0; }
        .highlight { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
        .button { display: inline-block; background: #2c5aa0; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Take Action 💪</h1>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>Over the past few days, we've talked about the 7 Mountains and discovering your calling. Today, let's get practical.</p>
        
        <h2>Here are 3 ways you can start making an impact TODAY:</h2>
        
        <div class="action-box">
            <h3>1. Pray with Purpose</h3>
            <p>Start praying specifically for your sphere of influence. Pray for:</p>
            <ul>
                <li>Your coworkers, clients, or customers</li>
                <li>Leaders in your industry or community</li>
                <li>Opportunities to be salt and light</li>
                <li>Wisdom to navigate difficult conversations</li>
            </ul>
            <p><strong>Action:</strong> Set a daily reminder to pray for your "mountain" for just 5 minutes.</p>
        </div>
        
        <div class="action-box">
            <h3>2. Be Intentionally Present</h3>
            <p>Excellence and character speak louder than words. Show up with:</p>
            <ul>
                <li>Integrity in your work</li>
                <li>Kindness in your interactions</li>
                <li>Excellence in your craft</li>
                <li>Peace in stressful situations</li>
            </ul>
            <p><strong>Action:</strong> This week, look for one opportunity to go above and beyond in serving someone.</p>
        </div>
        
        <div class="action-box">
            <h3>3. Stay Informed and Engaged</h3>
            <p>You can't influence what you don't understand. Stay informed about:</p>
            <ul>
                <li>Issues affecting your industry or community</li>
                <li>Cultural trends shaping your mountain</li>
                <li>Biblical principles that apply to your work</li>
                <li>Stories of Christians making a difference</li>
            </ul>
            <p><strong>Action:</strong> Bookmark our platform and check in weekly for articles relevant to your mountain.</p>
        </div>
        
        <div class="highlight">
            <h3>Remember:</h3>
            <p>You don't need a platform, a title, or a big audience to make a difference. You just need to be faithful where God has placed you.</p>
            <p><strong>"Whatever you do, work at it with all your heart, as working for the Lord, not for human masters." - Colossians 3:23</strong></p>
        </div>
        
        <h3>Resources to help you:</h3>
        
        <p>On our platform, you'll find:</p>
        <ul>
            <li>Mountain-specific articles and videos</li>
            <li>A forum to connect with other believers in your sphere</li>
            <li>Prayer requests and community support</li>
            <li>Tools and resources for your journey</li>
        </ul>
        
        <p style="text-align: center;">
            <a href="https://christianconservativestoday.com" class="button">Explore Resources</a>
        </p>
        
        <p>Tomorrow, I'll share one final thought about why this matters more than ever right now.</p>
        
        <p>Blessings,<br>
        Christian Conservatives Today</p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
        <p><a href="{{unsubscribe_link}}">Unsubscribe</a></p>
    </div>
</body>
</html>'''
    },
    {
        'step': 5,
        'delay_days': 2,
        'subject': 'The urgency of NOW (and what comes next)',
        'campaign_name': 'Final - The Urgency',
        'html_content': '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #2c5aa0 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .highlight { background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }
        .urgent-box { background: #ffebee; border-left: 4px solid #f44336; padding: 20px; margin: 20px 0; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
        .button { display: inline-block; background: #2c5aa0; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Why NOW Matters ⏰</h1>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>Over the past week, we've covered a lot:</p>
        <ul>
            <li>The 7 Mountains of Influence</li>
            <li>Discovering your calling</li>
            <li>Practical ways to make an impact</li>
        </ul>
        
        <p>Today, I want to share why this matters more urgently than ever.</p>
        
        <div class="urgent-box">
            <h3>We're at a cultural crossroads</h3>
            <p>The next few years will determine the direction of our culture for generations to come. Issues like:</p>
            <ul>
                <li>Religious freedom</li>
                <li>Parental rights in education</li>
                <li>The definition of family</li>
                <li>Free speech and censorship</li>
                <li>Economic freedom</li>
                <li>The role of faith in public life</li>
            </ul>
            <p>These aren't just political issues - they're battles for the soul of our nation.</p>
        </div>
        
        <h3>The good news?</h3>
        
        <p>Christians are waking up. We're realizing that:</p>
        <ul>
            <li>Silence is not an option</li>
            <li>Retreat is not a strategy</li>
            <li>We have a responsibility to engage</li>
            <li>God has placed us here "for such a time as this" (Esther 4:14)</li>
        </ul>
        
        <div class="highlight">
            <h3>What comes next?</h3>
            <p>This is the end of our welcome series, but it's just the beginning of your journey with Christian Conservatives Today.</p>
            <p><strong>Here's what you can expect going forward:</strong></p>
            <ul>
                <li>Weekly updates on issues that matter</li>
                <li>New articles and resources for your mountain</li>
                <li>Election coverage and voter guides</li>
                <li>Community discussions and prayer requests</li>
                <li>Opportunities to get involved</li>
            </ul>
        </div>
        
        <h3>Stay connected:</h3>
        
        <p>Make sure to:</p>
        <ul>
            <li>Bookmark <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></li>
            <li>Follow us on social media (links on the site)</li>
            <li>Join the conversation in our forums</li>
            <li>Share articles that resonate with you</li>
        </ul>
        
        <p style="text-align: center;">
            <a href="https://christianconservativestoday.com" class="button">Visit the Platform</a>
        </p>
        
        <div class="highlight">
            <h3>One more thing...</h3>
            <p>If you've found value in these emails, would you consider sharing Christian Conservatives Today with a friend? Forward this email or share the link.</p>
            <p>The more Christians we can equip and mobilize, the greater impact we can make together.</p>
        </div>
        
        <h3>Thank you</h3>
        
        <p>Thank you for taking this journey with me. Thank you for your commitment to being salt and light in your sphere of influence.</p>
        
        <p>The world needs Christians who are willing to engage, not retreat. Who are willing to speak truth in love. Who are willing to climb their mountain for the glory of God.</p>
        
        <p><strong>You are one of those Christians.</strong></p>
        
        <p>Let's do this together.</p>
        
        <p>Blessings,<br>
        Christian Conservatives Today</p>
        
        <p><em>P.S. - Have questions or feedback? Hit reply - I read every email.</em></p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
        <p><a href="{{unsubscribe_link}}">Unsubscribe</a></p>
    </div>
</body>
</html>'''
    }
]

print("Creating general-newsletter-sequence campaigns...\n")

for campaign in campaigns:
    campaign_id = str(uuid.uuid4())
    
    item = {
        'user_id': PLATFORM_OWNER_ID,
        'campaign_id': campaign_id,
        'campaign_name': campaign['campaign_name'],
        'campaign_group': 'general-newsletter-sequence',
        'subject': campaign['subject'],
        'html_content': campaign['html_content'],
        'status': 'active',
        'step_number': campaign['step'],
        'delay_days': campaign['delay_days'],
        'sequence_number': campaign['step']
    }
    
    campaigns_table.put_item(Item=item)
    print(f"✅ Created Email #{campaign['step']}: {campaign['campaign_name']}")
    print(f"   Campaign ID: {campaign_id}")
    print(f"   Subject: {campaign['subject']}")
    print(f"   Delay: {campaign['delay_days']} days\n")

print("=" * 80)
print("✅ All 5 general-newsletter-sequence campaigns created successfully!")
print("\nNew subscribers from subscribe.html will now be auto-enrolled in this sequence.")
