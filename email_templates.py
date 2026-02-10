# Professional Email Templates with Branding

LOGO_URL = "https://christianconservativestoday.com/techcrosslogo.jpg"
PRIMARY_COLOR = "#2c5aa0"
SECONDARY_COLOR = "#8b4513"
ACCENT_COLOR = "#d4af37"

def get_confirmation_email(first_name, confirmation_link):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <!-- Header with gradient -->
                    <tr>
                        <td style="background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%); padding: 40px 20px; text-align: center;">
                            <img src="{LOGO_URL}" alt="Christian Conservatives Today" style="max-width: 150px; height: auto; margin-bottom: 20px;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px;">Confirm Your Subscription</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <p style="font-size: 16px; color: #333333; line-height: 1.6; margin: 0 0 20px 0;">
                                Hi {first_name},
                            </p>
                            <p style="font-size: 16px; color: #333333; line-height: 1.6; margin: 0 0 20px 0;">
                                Thank you for subscribing to <strong>Christian Conservatives Today</strong>! We're excited to have you join our community of believers and truth-seekers.
                            </p>
                            <p style="font-size: 16px; color: #333333; line-height: 1.6; margin: 0 0 30px 0;">
                                Please confirm your email address by clicking the button below:
                            </p>
                            
                            <!-- CTA Button -->
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td align="center" style="padding: 20px 0;">
                                        <a href="{confirmation_link}" style="background-color: {PRIMARY_COLOR}; color: #ffffff; text-decoration: none; padding: 15px 40px; border-radius: 25px; font-size: 18px; font-weight: bold; display: inline-block;">
                                            Confirm My Subscription
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="font-size: 14px; color: #666666; line-height: 1.6; margin: 30px 0 0 0;">
                                Or copy and paste this link into your browser:<br>
                                <a href="{confirmation_link}" style="color: {PRIMARY_COLOR}; word-break: break-all;">{confirmation_link}</a>
                            </p>
                            
                            <p style="font-size: 14px; color: #999999; line-height: 1.6; margin: 30px 0 0 0; padding-top: 20px; border-top: 1px solid #eeeeee;">
                                This link will expire in 24 hours. If you didn't subscribe to our newsletter, please ignore this email.
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px; text-align: center;">
                            <p style="font-size: 14px; color: #666666; margin: 0 0 10px 0;">
                                <strong>Christian Conservatives Today</strong><br>
                                Where Truth Meets Action
                            </p>
                            <p style="font-size: 12px; color: #999999; margin: 0;">
                                © {datetime.now().year} Christian Conservatives Today. All rights reserved.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

def get_welcome_email(first_name):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px 0;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%); padding: 40px 20px; text-align: center;">
                            <img src="{LOGO_URL}" alt="Christian Conservatives Today" style="max-width: 150px; height: auto; margin-bottom: 20px;">
                            <h1 style="color: #ffffff; margin: 0; font-size: 28px;">Welcome to Our Community!</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <p style="font-size: 16px; color: #333333; line-height: 1.6; margin: 0 0 20px 0;">
                                Hi {first_name},
                            </p>
                            <p style="font-size: 16px; color: #333333; line-height: 1.6; margin: 0 0 20px 0;">
                                Welcome to <strong>Christian Conservatives Today</strong>! Your subscription is now active, and you'll receive our latest updates, articles, and news.
                            </p>
                            
                            <h2 style="color: {PRIMARY_COLOR}; font-size: 22px; margin: 30px 0 20px 0;">What You'll Receive:</h2>
                            <ul style="font-size: 16px; color: #333333; line-height: 1.8; margin: 0 0 30px 0; padding-left: 20px;">
                                <li>Weekly newsletter with top articles and news</li>
                                <li>Election updates and voter guides for all 50 states</li>
                                <li>Prayer requests and ministry updates</li>
                                <li>Event announcements and community news</li>
                            </ul>
                            
                            <h2 style="color: {PRIMARY_COLOR}; font-size: 22px; margin: 30px 0 20px 0;">Get Started:</h2>
                            
                            <!-- Feature Boxes -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px;">
                                <tr>
                                    <td style="padding: 20px; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid {ACCENT_COLOR};">
                                        <h3 style="color: {PRIMARY_COLOR}; font-size: 18px; margin: 0 0 10px 0;">📖 Explore Articles</h3>
                                        <p style="font-size: 14px; color: #666666; margin: 0 0 10px 0;">Read faith-based articles with integrated Bible verses</p>
                                        <a href="https://christianconservativestoday.com/articles.html" style="color: {PRIMARY_COLOR}; text-decoration: none; font-weight: bold;">Browse Articles →</a>
                                    </td>
                                </tr>
                            </table>
                            
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px;">
                                <tr>
                                    <td style="padding: 20px; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid {ACCENT_COLOR};">
                                        <h3 style="color: {PRIMARY_COLOR}; font-size: 18px; margin: 0 0 10px 0;">🎥 Watch Videos</h3>
                                        <p style="font-size: 14px; color: #666666; margin: 0 0 10px 0;">Sermons, teachings, and conservative commentary</p>
                                        <a href="https://christianconservativestoday.com/videos.html" style="color: {PRIMARY_COLOR}; text-decoration: none; font-weight: bold;">Watch Now →</a>
                                    </td>
                                </tr>
                            </table>
                            
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom: 20px;">
                                <tr>
                                    <td style="padding: 20px; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid {ACCENT_COLOR};">
                                        <h3 style="color: {PRIMARY_COLOR}; font-size: 18px; margin: 0 0 10px 0;">🗳️ Election Tracking</h3>
                                        <p style="font-size: 14px; color: #666666; margin: 0 0 10px 0;">Voter guides for all 50 states with candidate profiles</p>
                                        <a href="https://christianconservativestoday.com/election-map.html" style="color: {PRIMARY_COLOR}; text-decoration: none; font-weight: bold;">View Map →</a>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="font-size: 16px; color: #333333; line-height: 1.6; margin: 30px 0 0 0;">
                                God bless you,<br>
                                <strong>The Christian Conservatives Today Team</strong>
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px; text-align: center;">
                            <p style="font-size: 14px; color: #666666; margin: 0 0 10px 0;">
                                <strong>Christian Conservatives Today</strong><br>
                                Where Truth Meets Action
                            </p>
                            <p style="font-size: 12px; color: #999999; margin: 0 0 10px 0;">
                                You're receiving this because you subscribed to our newsletter.
                            </p>
                            <p style="font-size: 12px; color: #999999; margin: 0;">
                                <a href="https://christianconservativestoday.com/unsubscribe.html?email={{{{email}}}}" style="color: #999999;">Unsubscribe</a>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

from datetime import datetime
