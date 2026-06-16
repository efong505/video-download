import boto3
import sys
import uuid

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
campaigns_table = dynamodb.Table('user-email-campaigns')

PLATFORM_OWNER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Email #3 - AI is Changing Everything
campaign_3 = {
    'user_id': PLATFORM_OWNER_ID,
    'campaign_id': str(uuid.uuid4()),
    'campaign_name': 'Transition #3 - AI is Changing Everything',
    'campaign_group': 'election-map-transition-sequence',
    'subject': 'The one technology reshaping all 7 mountains (most Christians are ignoring it)',
    'content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #2c5aa0 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .warning-box { background: #fff3cd; border: 2px solid #ffc107; padding: 20px; margin: 20px 0; border-radius: 8px; }
        .ai-impact { background: #f0f7ff; padding: 15px; margin: 10px 0; border-left: 4px solid #2c5aa0; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AI is Changing Everything 🤖</h1>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>Quick question: What do you think is the biggest threat to Christian values in the next 10 years?</p>
        
        <p>Most people would say: politics, media bias, moral decline, persecution...</p>
        
        <p>All valid concerns. But there's something bigger coming - something that will reshape EVERY mountain of influence:</p>
        
        <h2 style="text-align: center; color: #2c5aa0;">Artificial Intelligence.</h2>
        
        <p>I know, I know - it sounds like sci-fi. But hear me out:</p>
        
        <h3>AI is already:</h3>
        
        <div class="ai-impact">
            <strong>📰 Media Mountain:</strong> Writing news articles and controlling what information you see
        </div>
        
        <div class="ai-impact">
            <strong>📚 Education Mountain:</strong> Teaching your kids and grading their work
        </div>
        
        <div class="ai-impact">
            <strong>💼 Business Mountain:</strong> Making hiring decisions and determining who gets promoted
        </div>
        
        <div class="ai-impact">
            <strong>🎨 Arts Mountain:</strong> Creating art, music, and entertainment
        </div>
        
        <div class="ai-impact">
            <strong>🗳️ Government Mountain:</strong> Influencing elections and policy decisions
        </div>
        
        <div class="ai-impact">
            <strong>⛪ Religion Mountain:</strong> Even giving "spiritual advice" and answering theological questions
        </div>
        
        <div class="warning-box">
            <h3 style="margin-top: 0;">Here's the scary part:</h3>
            <p><strong>Most Christians have no idea this is happening.</strong></p>
            <p>While we've been focused on traditional culture war battles, AI has quietly become the most powerful force shaping society. And it's being built almost entirely by people who don't share our values.</p>
        </div>
        
        <h3>Think about it:</h3>
        
        <p>If AI controls what information people see, what jobs they get, what art they consume, and even what "truth" looks like... then <strong>whoever controls AI controls culture.</strong></p>
        
        <h3>So what do we do?</h3>
        
        <p>That's exactly what I've been wrestling with. And it's why I wrote a book about it.</p>
        
        <p>But before I tell you about the book, I want to make sure you understand WHY this matters.</p>
        
        <p><strong>AI isn't just another technology.</strong> It's a worldview battle. And Christians need to be equipped to engage it with wisdom, discernment, and biblical truth.</p>
        
        <p>In my next email, I'll share what I've learned about how Christians should respond to AI - and why this might be the most important conversation the church isn't having.</p>
        
        <p>Talk soon,<br>
        Christian Conservatives Today</p>
        
        <p><em>P.S. - If you're thinking "I'm not a tech person, this doesn't apply to me" - I get it. But AI will affect your job, your kids' education, your church, and your community. This is for EVERYONE.</em></p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
    </div>
</body>
</html>
    ''',
    'status': 'active',
    'delay_days': 5
}

# Email #4 - The Book Reveal
campaign_4 = {
    'user_id': PLATFORM_OWNER_ID,
    'campaign_id': str(uuid.uuid4()),
    'campaign_name': 'Transition #4 - The Book Reveal',
    'campaign_group': 'election-map-transition-sequence',
    'subject': 'I wrote a book about AI and Christianity (here\'s why)',
    'content': '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #2c5aa0 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
        .content { padding: 30px; background: #ffffff; }
        .book-box { background: #f8f9fa; border: 3px solid #2c5aa0; padding: 25px; margin: 25px 0; border-radius: 10px; text-align: center; }
        .benefit { background: #f0f7ff; padding: 12px; margin: 8px 0; border-left: 4px solid #2c5aa0; }
        .button { display: inline-block; background: #2c5aa0; color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; margin: 20px 0; font-weight: bold; }
        .footer { background: #f8f9fa; padding: 20px; text-align: center; font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📖 I Wrote a Book</h1>
    </div>
    
    <div class="content">
        <p>Hi {{first_name}},</p>
        
        <p>So... I wrote a book.</p>
        
        <div class="book-box">
            <h2 style="color: #2c5aa0; margin-top: 0;">"How Christians Should Respond to AI"</h2>
            <p style="font-size: 18px; color: #666;">A Biblical Framework for the Digital Age</p>
        </div>
        
        <p>And honestly? I never planned to write it.</p>
        
        <p>But the more I researched AI, the more I realized: <strong>The church is asleep at the wheel.</strong></p>
        
        <p>We're having debates about worship styles and political candidates while AI is quietly rewriting the rules of reality. And when Christians DO talk about AI, it's usually one of two extremes:</p>
        
        <ol>
            <li><strong>"AI is the mark of the beast! Run for the hills!"</strong> (Fear-based, not helpful)</li>
            <li><strong>"AI is just a tool, no big deal."</strong> (Naive, dangerously optimistic)</li>
        </ol>
        
        <p style="font-size: 20px; text-align: center; color: #2c5aa0;"><strong>Neither response is biblical.</strong></p>
        
        <p>So I wrote the book I wish existed - a practical, biblical guide to help Christians navigate the AI revolution with wisdom, courage, and hope.</p>
        
        <h3>Here's what you'll learn:</h3>
        
        <div class="benefit">
            ✅ What AI actually is (and isn't) - no tech jargon, just clear explanations
        </div>
        
        <div class="benefit">
            ✅ The spiritual and ethical issues AI raises for Christians
        </div>
        
        <div class="benefit">
            ✅ How to protect your family from AI's dangers
        </div>
        
        <div class="benefit">
            ✅ How to use AI as a tool for Kingdom work (yes, it can be used for good!)
        </div>
        
        <div class="benefit">
            ✅ A biblical framework for thinking about technology and culture
        </div>
        
        <p><strong>This isn't a "doom and gloom" book.</strong> It's a roadmap for how Christians can engage AI with discernment and purpose.</p>
        
        <h3>Who is this book for?</h3>
        
        <ul>
            <li>Parents who want to protect their kids from AI's influence</li>
            <li>Pastors and church leaders navigating new technology</li>
            <li>Business owners wondering how AI will affect their industry</li>
            <li>Anyone who wants to be informed and equipped (not fearful or naive)</li>
        </ul>
        
        <p><strong>Here's the thing:</strong> I'm not trying to make you afraid of AI. I'm trying to wake you up to the reality that it's already here - and Christians need to be part of the conversation.</p>
        
        <p>In my next email, I'll share a FREE resource to help you get started (even if you're not ready to buy the book yet).</p>
        
        <div style="text-align: center;">
            <a href="https://christianconservativestoday.com/book.html" class="button">Learn More About the Book</a>
        </div>
        
        <p>Blessings,<br>
        Christian Conservatives Today</p>
    </div>
    
    <div class="footer">
        <p>Christian Conservatives Today<br>
        <a href="https://christianconservativestoday.com">christianconservativestoday.com</a></p>
    </div>
</body>
</html>
    ''',
    'status': 'active',
    'delay_days': 7
}

print("Creating campaigns 3 and 4...")

try:
    campaigns_table.put_item(Item=campaign_3)
    print(f"✅ Created: {campaign_3['campaign_name']} (ID: {campaign_3['campaign_id']})")
    
    campaigns_table.put_item(Item=campaign_4)
    print(f"✅ Created: {campaign_4['campaign_name']} (ID: {campaign_4['campaign_id']})")
    
    print("\n✅ Part 2 complete! Campaigns 3-4 created.")
    
except Exception as e:
    print(f"❌ Error: {e}")
