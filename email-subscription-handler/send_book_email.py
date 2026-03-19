"""
Add this function to lambda_function.py to send book signup email with PDFs
The PDFs need to be included in the Lambda deployment package
"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os

def send_book_signup_email_with_pdfs(email, first_name):
    """Send book signup confirmation with 3 PDF attachments"""
    greeting = f"Hi {first_name}!" if first_name else "Hello!"
    
    # Create multipart message
    msg = MIMEMultipart('mixed')
    msg['Subject'] = '🎁 Your Free Christian AI Survival Kit is Here!'
    msg['From'] = FROM_EMAIL
    msg['To'] = email
    
    # HTML body
    html_body = f"""
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f5f5f5;">
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <div style="background: linear-gradient(135deg, #16a34a 0%, #15803d 100%); padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 30px;">
                <h2 style="color: white; margin: 0;">🎁 Your Free Christian AI Survival Kit</h2>
            </div>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                {greeting}
            </p>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                Thank you for downloading the <strong>Christian AI Survival Kit</strong>!
            </p>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                You now have access to <strong>$71 worth of resources</strong> to help you master AI without losing your soul:
            </p>
            
            <div style="background: #f0fdf4; padding: 20px; border-radius: 8px; border-left: 4px solid #16a34a; margin: 20px 0;">
                <h3 style="color: #16a34a; margin-top: 0;">📦 What's Included (Attached):</h3>
                <ul style="font-size: 15px; line-height: 1.8; color: #555;">
                    <li><strong>Christian AI Survival Guide</strong> — 7 safeguards for using AI without losing your soul</li>
                    <li><strong>Church Discussion Guide</strong> — 10-session study for small groups</li>
                    <li><strong>AI Parent Guide</strong> — How to protect your children in an AI-driven world</li>
                </ul>
            </div>
            
            <p style="font-size: 16px; line-height: 1.6; color: #333;">
                <strong>Plus:</strong> You can now read the <strong>30-page book preview</strong> online at:
            </p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{DOMAIN}/the-necessary-evil-book.html#preview" 
                   style="display: inline-block; background: linear-gradient(135deg, #16a34a 0%, #15803d 100%); 
                          color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; 
                          font-weight: bold; font-size: 16px;">
                    📖 Read the Book Preview
                </a>
            </div>
            
            <div style="background: #fffbeb; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #d4af37;">
                <p style="margin: 0; font-size: 14px; color: #666;">
                    <strong>💡 Next Step:</strong> Check out the full book <em>The Necessary Evil</em> — 
                    available on Amazon (Kindle, Hardcover & Paperback) and as a signed copy direct from the author.
                </p>
            </div>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="{DOMAIN}/the-necessary-evil-book.html#purchase" 
                   style="display: inline-block; background: #2c5aa0; 
                          color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; 
                          font-weight: bold; font-size: 14px;">
                    📚 Get the Full Book
                </a>
            </div>
            
            <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
            
            <p style="font-size: 12px; color: #999; line-height: 1.6;">
                You're receiving this email because you signed up for the Christian AI Survival Kit at christianconservativestoday.com<br>
                <a href="{DOMAIN}" style="color: #16a34a;">Visit Website</a>
            </p>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    text_body = f"""{greeting}

Thank you for downloading the Christian AI Survival Kit!

You now have access to $71 worth of resources to help you master AI without losing your soul:

WHAT'S INCLUDED (Attached):
• Christian AI Survival Guide — 7 safeguards for using AI without losing your soul
• Church Discussion Guide — 10-session study for small groups  
• AI Parent Guide — How to protect your children in an AI-driven world

PLUS: You can now read the 30-page book preview online at:
{DOMAIN}/the-necessary-evil-book.html#preview

NEXT STEP: Check out the full book "The Necessary Evil" — available on Amazon and as a signed copy direct from the author.
{DOMAIN}/the-necessary-evil-book.html#purchase

---
You're receiving this because you signed up at christianconservativestoday.com
"""
    
    # Attach text and HTML parts
    msg_body = MIMEMultipart('alternative')
    msg_body.attach(MIMEText(text_body, 'plain', 'utf-8'))
    msg_body.attach(MIMEText(html_body, 'html', 'utf-8'))
    msg.attach(msg_body)
    
    # Attach PDFs (they need to be in the Lambda deployment package)
    pdf_files = [
        'christian-ai-survival-guide.pdf',
        'church-discussion-guide.pdf',
        'ai-parent-guide.pdf'
    ]
    
    for pdf_file in pdf_files:
        try:
            # PDFs should be in /tmp or in the Lambda package root
            pdf_path = f'/tmp/{pdf_file}'
            if not os.path.exists(pdf_path):
                pdf_path = pdf_file  # Try current directory
            
            with open(pdf_path, 'rb') as f:
                pdf_data = f.read()
                pdf_part = MIMEApplication(pdf_data, _subtype='pdf')
                pdf_part.add_header('Content-Disposition', 'attachment', filename=pdf_file)
                msg.attach(pdf_part)
        except Exception as e:
            print(f"Error attaching {pdf_file}: {str(e)}")
    
    # Send via SES
    try:
        ses.send_raw_email(
            Source=FROM_EMAIL,
            Destinations=[email],
            RawMessage={'Data': msg.as_string()}
        )
        print(f'Book signup email with PDFs sent to: {email}')
    except Exception as e:
        print(f'Error sending book signup email: {str(e)}')
        raise
