import boto3
import uuid
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

print("🚀 Book 2 Campaign Upload - Part 2 (Emails 4-7)")
print("="*70)

# AWS Configuration
session = boto3.Session(profile_name='ekewaka')
ddb = session.resource('dynamodb', region_name='us-east-1')
table = ddb.Table('user-email-campaigns')

OWNER_ID = "effa3242-cf64-4021-b2b0-c8a5a9dfd6d2"
CAMPAIGN_GROUP = "book2-launch-sequence"
TIMESTAMP = datetime.utcnow().isoformat() + "Z"

# Email 4
email4 = {
    "user_id": OWNER_ID,
    "campaign_id": str(uuid.uuid4()),
    "campaign_name": "Book 2 Email 4: The Free AI Direction Workbook Is Live",
    "campaign_group": CAMPAIGN_GROUP,
    "sequence_number": 4,
    "subject_line": "The free AI Direction Workbook is live",
    "delay_hours": 48,
    "created_at": TIMESTAMP,
    "status": "active",
    "html_content": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The free AI Direction Workbook is live</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0; background-color: #f4f4f4;">
    <div style="max-width: 680px; margin: 0 auto; background: #ffffff; padding: 28px;">
        <p style="font-size: 16px;">Hello {{FIRST_NAME}},</p>
        <h1 style="font-size: 25px; line-height: 1.25; color: #111827;">The free AI Direction Workbook is live.</h1>
        <p>Book 2 now has a free companion workbook available for readers.</p>
        <p>The workbook is designed to help you practice the AI Direction Framework from <em>The Necessary Evil: AI Prompting for Everyday People</em>:</p>
        <div style="background: #f8fafc; padding: 16px; border-radius: 6px; margin: 22px 0;">
            <p style="font-size: 18px; font-weight: bold; margin: 0;">Aim. Inform. Direct. Shape. Refine. Verify. Apply.</p>
        </div>
        <p>The book teaches the framework. The workbook helps you practice it.</p>
        <p>It includes printable exercises to help readers move from vague AI use toward clearer direction, better context, refinement, and verification.</p>
        <p>No signup is required.</p>
        <div style="text-align: center; margin: 28px 0;">
            <a href="https://necessaryevilbooks.com/go/book2-workbook" style="display: inline-block; background: #1a73e8; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                Get the Free Workbook
            </a>
        </div>
        <p>If you have not seen the book yet, you can view it here:</p>
        <p>
            <a href="https://necessaryevilbooks.com/books/ai-prompting/" style="color: #1a73e8; font-weight: bold;">Book 2 page</a>
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

# Email 5
email5 = {
    "user_id": OWNER_ID,
    "campaign_id": str(uuid.uuid4()),
    "campaign_name": "Book 2 Email 5: Polished Does Not Mean True",
    "campaign_group": CAMPAIGN_GROUP,
    "sequence_number": 5,
    "subject_line": "Polished does not mean true",
    "delay_hours": 72,
    "created_at": TIMESTAMP,
    "status": "active",
    "html_content": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Polished does not mean true</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0; background-color: #f4f4f4;">
    <div style="max-width: 680px; margin: 0 auto; background: #ffffff; padding: 28px;">
        <p style="font-size: 16px;">Hello {{FIRST_NAME}},</p>
        <h1 style="font-size: 25px; line-height: 1.25; color: #111827;">Polished does not mean true.</h1>
        <p>AI can produce answers that sound complete, confident, and professional.</p>
        <p>But a polished answer can still be wrong.</p>
        <p>That is why verification is not optional.</p>
        <p>Before using AI output, we should ask:</p>
        <ul>
            <li>Is this accurate?</li>
            <li>What assumptions are being made?</li>
            <li>What needs to be checked?</li>
            <li>What source would confirm this?</li>
            <li>What risk would there be if this is wrong?</li>
        </ul>
        <p>This is one reason I wrote <em>The Necessary Evil: AI Prompting for Everyday People</em>. The goal is not simply to get AI to produce more words. The goal is to use AI with better direction and stronger human review.</p>
        <div style="background: #fef2f2; border-left: 4px solid #dc2626; padding: 16px; margin: 22px 0;">
            <p style="margin: 0; font-weight: bold;">AI can assist the work. It should not own the decision.</p>
        </div>
        <div style="text-align: center; margin: 28px 0;">
            <a href="https://necessaryevilbooks.com/books/ai-prompting/" style="display: inline-block; background: #1a73e8; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                View the Book
            </a>
        </div>
        <p>Available now on Amazon and Lulu:</p>
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

# Email 6
email6 = {
    "user_id": OWNER_ID,
    "campaign_id": str(uuid.uuid4()),
    "campaign_name": "Book 2 Email 6: From Warning to Practical Response",
    "campaign_group": CAMPAIGN_GROUP,
    "sequence_number": 6,
    "subject_line": "From warning to practical response",
    "delay_hours": 48,
    "created_at": TIMESTAMP,
    "status": "active",
    "html_content": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>From warning to practical response</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0; background-color: #f4f4f4;">
    <div style="max-width: 680px; margin: 0 auto; background: #ffffff; padding: 28px;">
        <p style="font-size: 16px;">Hello {{FIRST_NAME}},</p>
        <h1 style="font-size: 25px; line-height: 1.25; color: #111827;">From warning to practical response.</h1>
        <p>Book 1 in <em>The Necessary Evil</em> series focused on AI, dehumanization, transhumanism, and the fight for human dignity.</p>
        <p>That warning still matters.</p>
        <p>But warnings are not enough by themselves.</p>
        <p>Everyday people also need to know how to respond practically. How should we use these tools? How do we avoid being passive? How do we keep human judgment in charge?</p>
        <p>That is where Book 2 comes in.</p>
        <div style="background: #f8fafc; border-left: 4px solid #1a73e8; padding: 16px; margin: 22px 0;">
            <p style="margin: 0; font-size: 18px; font-weight: bold;">The Necessary Evil: AI Prompting for Everyday People</p>
            <p style="margin: 8px 0 0 0;">A practical guide to using AI with clarity, confidence, and control.</p>
        </div>
        <p>It is for readers who understand that AI is not neutral magic and not harmless entertainment, but still need practical guidance for ordinary work, learning, writing, planning, and creativity.</p>
        <div style="text-align: center; margin: 28px 0;">
            <a href="https://www.amazon.com/dp/B0H56WFJ94" style="display: inline-block; background: #1a73e8; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                Buy Book 2 on Amazon
            </a>
        </div>
        <p>Or buy through Lulu:</p>
        <p>
            <a href="https://www.lulu.com/shop/edward-fong/the-necessary-evil-ai-prompting-for-everyday-people/paperback/product-84dv9qe.html" style="color: #1a73e8; font-weight: bold;">Buy on Lulu</a>
        </p>
        <p>The free companion workbook is also available here:</p>
        <p>
            <a href="https://necessaryevilbooks.com/go/book2-workbook" style="color: #1a73e8; font-weight: bold;">Get the free workbook</a>
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

# Email 7
email7 = {
    "user_id": OWNER_ID,
    "campaign_id": str(uuid.uuid4()),
    "campaign_name": "Book 2 Email 7: Final Reminder — Book and Workbook Available",
    "campaign_group": CAMPAIGN_GROUP,
    "sequence_number": 7,
    "subject_line": "Final reminder: Book 2 and the free workbook are available",
    "delay_hours": 72,
    "created_at": TIMESTAMP,
    "status": "active",
    "html_content": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Final reminder: Book 2 and the free workbook are available</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333333; margin: 0; padding: 0; background-color: #f4f4f4;">
    <div style="max-width: 680px; margin: 0 auto; background: #ffffff; padding: 28px;">
        <p style="font-size: 16px;">Hello {{FIRST_NAME}},</p>
        <h1 style="font-size: 25px; line-height: 1.25; color: #111827;">Final reminder: Book 2 and the free workbook are available.</h1>
        <p>I wanted to send one final reminder in this sequence.</p>
        <p><em>The Necessary Evil: AI Prompting for Everyday People</em> is now available, and the free companion workbook is live.</p>
        <p>This book was written for everyday readers who want to use AI with clarity, confidence, and control while keeping human judgment and responsibility in charge.</p>
        <p>If you want a practical framework for using AI more wisely, Book 2 walks through:</p>
        <ul>
            <li>how to aim the task,</li>
            <li>how to give useful context,</li>
            <li>how to direct the output,</li>
            <li>how to shape the answer,</li>
            <li>how to refine weak results,</li>
            <li>how to verify before trusting,</li>
            <li>and how to apply AI output responsibly.</li>
        </ul>
        <div style="text-align: center; margin: 28px 0;">
            <a href="https://necessaryevilbooks.com/books/ai-prompting/" style="display: inline-block; background: #1a73e8; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                View Book 2
            </a>
        </div>
        <p><strong>Buy on Amazon:</strong><br>
        <a href="https://www.amazon.com/dp/B0H56WFJ94" style="color: #1a73e8; font-weight: bold;">https://www.amazon.com/dp/B0H56WFJ94</a></p>
        <p><strong>Buy on Lulu:</strong><br>
        <a href="https://www.lulu.com/shop/edward-fong/the-necessary-evil-ai-prompting-for-everyday-people/paperback/product-84dv9qe.html" style="color: #1a73e8; font-weight: bold;">Buy through Lulu</a></p>
        <p><strong>Free companion workbook:</strong><br>
        <a href="https://necessaryevilbooks.com/go/book2-workbook" style="color: #1a73e8; font-weight: bold;">https://necessaryevilbooks.com/go/book2-workbook</a></p>
        <p>If you read the book and find it helpful, I would also be grateful for an honest review. Reviews help independent authors reach readers who would never otherwise know the book exists.</p>
        <p>Please only leave a review if you have actually read enough of the book to give an honest opinion.</p>
        <p>Thank you for your support.</p>
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

campaigns_part2 = [email4, email5, email6, email7]

print(f"\n📧 Uploading {len(campaigns_part2)} campaigns to DynamoDB...")
print(f"Campaign Group: {CAMPAIGN_GROUP}")
print(f"Owner ID: {OWNER_ID}\n")

for campaign in campaigns_part2:
    try:
        table.put_item(Item=campaign)
        print(f"✅ {campaign['campaign_name']}")
        print(f"   UUID: {campaign['campaign_id']}")
        print(f"   Sequence: {campaign['sequence_number']}")
        print(f"   Delay: {campaign['delay_hours']} hours\n")
    except Exception as e:
        print(f"❌ ERROR uploading {campaign['campaign_name']}: {e}\n")

print("="*70)
print("✅ Part 2 Complete - Emails 4-7 uploaded")
print("\n🎉 ALL 7 EMAILS UPLOADED!")
print("\nNext steps:")
print("1. Verify campaigns in DynamoDB")
print("2. Test enrollment with your email")
print("3. Review campaign-manager.html")
