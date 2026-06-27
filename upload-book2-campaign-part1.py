import boto3
import uuid
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Book 2 Campaign Upload - Part 1 (Emails 1-3)")
print("="*70)

# AWS Configuration
session = boto3.Session(profile_name='ekewaka')
ddb = session.resource('dynamodb', region_name='us-east-1')
table = ddb.Table('user-email-campaigns')

OWNER_ID = "effa3242-cf64-4021-b2b0-c8a5a9dfd6d2"
CAMPAIGN_GROUP = "book2-launch-sequence"
TIMESTAMP = datetime.utcnow().isoformat() + "Z"

# Email 1
email1 = {
    "user_id": OWNER_ID,
    "campaign_id": str(uuid.uuid4()),
    "campaign_name": "Book 2 Email 1: AI Is Here — But Who Is Directing It?",
    "campaign_group": CAMPAIGN_GROUP,
    "sequence_number": 1,
    "subject_line": "AI is here — but who is directing it?",
    "delay_hours": 0,
    "created_at": TIMESTAMP,
    "status": "active",
    "html_content": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI is here — but who is directing it?</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0; background-color: #f4f4f4;">
    <div style="max-width: 680px; margin: 0 auto; background: #ffffff; padding: 28px;">
        <p style="font-size: 16px;">Hello {{FIRST_NAME}},</p>
        <h1 style="font-size: 26px; line-height: 1.25; color: #111827; margin-bottom: 16px;">AI is here — but who is directing it?</h1>
        <p>Artificial intelligence is moving into work, writing, learning, creativity, research, planning, and everyday decision-making.</p>
        <p>But most people were never taught how to use it wisely.</p>
        <p>That is why I wrote my new book:</p>
        <div style="background: #f8fafc; border-left: 4px solid #1a73e8; padding: 16px; margin: 20px 0;">
            <p style="margin: 0; font-size: 18px; font-weight: bold;">The Necessary Evil: AI Prompting for Everyday People</p>
            <p style="margin: 8px 0 0 0;">Breaking Down Prompt Engineering So Anyone Can Use AI in Real Life, Work, Learning, and Creativity with Clarity, Confidence, and Control</p>
        </div>
        <p>This is Book 2 in <em>The Necessary Evil</em> series. Book 1 dealt with AI, dehumanization, transhumanism, and the fight for human dignity. Book 2 moves into the practical question:</p>
        <p style="font-size: 18px; font-weight: bold; color: #111827;">How do everyday people use AI without handing over human judgment?</p>
        <p>The core message is simple:</p>
        <p style="font-size: 18px; font-weight: bold; color: #1f2937;">AI should be assistance, not authority.</p>
        <p>The book teaches the AI Direction Framework:</p>
        <p style="font-weight: bold;">Aim. Inform. Direct. Shape. Refine. Verify. Apply.</p>
        <p>If AI has felt confusing, overhyped, risky, or hard to use well, this book was written to help make the process clearer and more responsible.</p>
        <div style="text-align: center; margin: 28px 0;">
            <a href="https://necessaryevilbooks.com/books/ai-prompting/" style="display: inline-block; background: #1a73e8; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                View the Book
            </a>
        </div>
        <p>You can also buy it directly here:</p>
        <p>
            <a href="https://www.amazon.com/dp/B0H56WFJ94" style="color: #1a73e8; font-weight: bold;">Buy on Amazon</a><br>
            <a href="https://www.lulu.com/shop/edward-fong/the-necessary-evil-ai-prompting-for-everyday-people/paperback/product-84dv9qe.html" style="color: #1a73e8; font-weight: bold;">Buy on Lulu</a>
        </p>
        <p>Thank you for reading and for supporting this work.</p>
        <p>Edward Fong<br>
        Christian Conservatives Today</p>
        <hr style="border: none; border-top: 1px solid #dddddd; margin: 28px 0;">
        <p style="font-size: 12px; color: #666666;">
            You are receiving this email because you subscribed to Christian Conservatives Today or requested related resources.
            <br>
            <a href="https://christianconservativestoday.com/unsubscribe.html?email={{EMAIL}}" style="color: #666666;">Unsubscribe</a>
        </p>
    </div>
</body>
</html>"""
}

# Email 2
email2 = {
    "user_id": OWNER_ID,
    "campaign_id": str(uuid.uuid4()),
    "campaign_name": "Book 2 Email 2: Prompting Is Not Magic Wording",
    "campaign_group": CAMPAIGN_GROUP,
    "sequence_number": 2,
    "subject_line": "Prompting is not magic wording",
    "delay_hours": 24,
    "created_at": TIMESTAMP,
    "status": "active",
    "html_content": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prompting is not magic wording</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0; background-color: #f4f4f4;">
    <div style="max-width: 680px; margin: 0 auto; background: #ffffff; padding: 28px;">
        <p style="font-size: 16px;">Hello {{FIRST_NAME}},</p>
        <h1 style="font-size: 25px; line-height: 1.25; color: #111827;">Prompting is not magic wording.</h1>
        <p>One of the biggest misunderstandings about AI is that "prompt engineering" is about finding secret phrases or clever tricks.</p>
        <p>That is not the heart of it.</p>
        <p style="font-size: 18px; font-weight: bold; color: #111827;">Prompting is direction.</p>
        <p>A better prompt is a clearer explanation of:</p>
        <ul>
            <li>what you are trying to do,</li>
            <li>what context matters,</li>
            <li>what kind of help you want,</li>
            <li>what the output should look like,</li>
            <li>what boundaries should be respected,</li>
            <li>and how the answer should be checked.</li>
        </ul>
        <p>That is why <em>The Necessary Evil: AI Prompting for Everyday People</em> teaches a practical framework instead of a list of gimmicks.</p>
        <div style="background: #f8fafc; padding: 16px; border-radius: 6px; margin: 22px 0;">
            <p style="margin-top: 0; font-weight: bold;">The AI Direction Framework:</p>
            <p style="font-size: 18px; margin-bottom: 0;">Aim. Inform. Direct. Shape. Refine. Verify. Apply.</p>
        </div>
        <p>This is a book for everyday readers who want to use AI better without surrendering judgment, responsibility, or discernment.</p>
        <div style="text-align: center; margin: 28px 0;">
            <a href="https://necessaryevilbooks.com/books/ai-prompting/" style="display: inline-block; background: #1a73e8; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                Learn About Book 2
            </a>
        </div>
        <p>Available now:</p>
        <p>
            <a href="https://www.amazon.com/dp/B0H56WFJ94" style="color: #1a73e8; font-weight: bold;">Amazon</a><br>
            <a href="https://www.lulu.com/shop/edward-fong/the-necessary-evil-ai-prompting-for-everyday-people/paperback/product-84dv9qe.html" style="color: #1a73e8; font-weight: bold;">Lulu</a>
        </p>
        <p>Edward Fong</p>
        <hr style="border: none; border-top: 1px solid #dddddd; margin: 28px 0;">
        <p style="font-size: 12px; color: #666666;">
            You are receiving this email because you subscribed to Christian Conservatives Today or requested related resources.
            <br>
            <a href="https://christianconservativestoday.com/unsubscribe.html?email={{EMAIL}}" style="color: #666666;">Unsubscribe</a>
        </p>
    </div>
</body>
</html>"""
}

# Email 3
email3 = {
    "user_id": OWNER_ID,
    "campaign_id": str(uuid.uuid4()),
    "campaign_name": "Book 2 Email 3: AI Should Be Assistance, Not Authority",
    "campaign_group": CAMPAIGN_GROUP,
    "sequence_number": 3,
    "subject_line": "AI should be assistance, not authority",
    "delay_hours": 48,
    "created_at": TIMESTAMP,
    "status": "active",
    "html_content": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI should be assistance, not authority</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0; background-color: #f4f4f4;">
    <div style="max-width: 680px; margin: 0 auto; background: #ffffff; padding: 28px;">
        <p style="font-size: 16px;">Hello {{FIRST_NAME}},</p>
        <h1 style="font-size: 25px; line-height: 1.25; color: #111827;">AI should be assistance, not authority.</h1>
        <p>That statement is at the center of Book 2.</p>
        <p>AI can help draft, summarize, organize, brainstorm, compare, plan, and explain. But it should not replace human judgment.</p>
        <p>For Christian and conservative readers especially, this matters.</p>
        <p>We should not hand over discernment, responsibility, truth, conscience, wisdom, or moral judgment to a machine.</p>
        <p>That does not mean we reject every tool. It means we learn how to use tools without being ruled by them.</p>
        <div style="background: #fff7ed; border-left: 4px solid #f59e0b; padding: 16px; margin: 22px 0;">
            <p style="margin: 0; font-weight: bold;">The question is not only, "Can AI do this?"</p>
            <p style="margin: 8px 0 0 0;">The better question is, "Should I use AI here, and how do I remain responsible for the result?"</p>
        </div>
        <p><em>The Necessary Evil: AI Prompting for Everyday People</em> teaches readers how to give clearer direction, refine the output, and verify results before trusting them.</p>
        <div style="text-align: center; margin: 28px 0;">
            <a href="https://www.amazon.com/dp/B0H56WFJ94" style="display: inline-block; background: #1a73e8; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                Buy on Amazon
            </a>
        </div>
        <p>If you prefer Lulu, it is available here:</p>
        <p>
            <a href="https://www.lulu.com/shop/edward-fong/the-necessary-evil-ai-prompting-for-everyday-people/paperback/product-84dv9qe.html" style="color: #1a73e8; font-weight: bold;">Buy on Lulu</a>
        </p>
        <p>Edward Fong</p>
        <hr style="border: none; border-top: 1px solid #dddddd; margin: 28px 0;">
        <p style="font-size: 12px; color: #666666;">
            You are receiving this email because you subscribed to Christian Conservatives Today or requested related resources.
            <br>
            <a href="https://christianconservativestoday.com/unsubscribe.html?email={{EMAIL}}" style="color: #666666;">Unsubscribe</a>
        </p>
    </div>
</body>
</html>"""
}

campaigns_part1 = [email1, email2, email3]

print(f"\n📧 Uploading {len(campaigns_part1)} campaigns to DynamoDB...")
print(f"Campaign Group: {CAMPAIGN_GROUP}")
print(f"Owner ID: {OWNER_ID}\n")

for campaign in campaigns_part1:
    try:
        table.put_item(Item=campaign)
        print(f"✅ {campaign['campaign_name']}")
        print(f"   UUID: {campaign['campaign_id']}")
        print(f"   Sequence: {campaign['sequence_number']}")
        print(f"   Delay: {campaign['delay_hours']} hours\n")
    except Exception as e:
        print(f"❌ ERROR uploading {campaign['campaign_name']}: {e}\n")

print("="*70)
print("✅ Part 1 Complete - Emails 1-3 uploaded")
print("\nNext: Run upload-book2-campaign-part2.py for emails 4-7")
