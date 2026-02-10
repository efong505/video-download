// Professional Email Templates for Campaigns

var EMAIL_TEMPLATES = {
    // Template 1: Election Update (Purple Gradient)
    election_update: {
        name: "Election Update",
        theme: "Purple Gradient",
        html: `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center;">
                            <h1 style="color: white; margin: 0; font-size: 28px;">🗳️ Election Update</h1>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h2 style="color: #333; margin-top: 0;">{{TITLE}}</h2>
                            <p style="color: #555; font-size: 16px; line-height: 1.6;">{{CONTENT}}</p>
                            
                            <!-- CTA Button -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                <tr>
                                    <td align="center">
                                        <a href="{{CTA_LINK}}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">{{CTA_TEXT}}</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background: #f8f9fa; padding: 20px 30px; text-align: center; border-top: 1px solid #eee;">
                            <p style="color: #999; font-size: 12px; margin: 0;">Christian Conservatives Today</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>`
    },

    // Template 2: Urgent Alert (Red Theme)
    urgent_alert: {
        name: "Urgent Alert",
        theme: "Red Alert",
        html: `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border: 3px solid #dc3545;">
                    <!-- Header -->
                    <tr>
                        <td style="background: #dc3545; padding: 30px; text-align: center;">
                            <h1 style="color: white; margin: 0; font-size: 24px;">⚠️ URGENT: {{TITLE}}</h1>
                        </td>
                    </tr>
                    <!-- Alert Box -->
                    <tr>
                        <td style="padding: 30px;">
                            <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin-bottom: 20px;">
                                <p style="margin: 0; color: #856404; font-weight: bold;">Time-Sensitive Action Required</p>
                            </div>
                            <p style="color: #333; font-size: 16px; line-height: 1.6; margin-top: 0;">{{CONTENT}}</p>
                            
                            <!-- CTA Button -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin: 25px 0;">
                                <tr>
                                    <td align="center">
                                        <a href="{{CTA_LINK}}" style="display: inline-block; background: #dc3545; color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">{{CTA_TEXT}}</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background: #f8f9fa; padding: 20px 30px; text-align: center; border-top: 1px solid #eee;">
                            <p style="color: #999; font-size: 12px; margin: 0;">Christian Conservatives Today</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>`
    },

    // Template 3: Newsletter (Clean & Professional)
    newsletter: {
        name: "Newsletter",
        theme: "Clean Professional",
        html: `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: Georgia, serif; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: #2c3e50; padding: 30px; text-align: center;">
                            <h1 style="color: white; margin: 0; font-size: 32px; font-weight: normal; letter-spacing: 2px;">CCT NEWSLETTER</h1>
                            <p style="color: #ecf0f1; margin: 10px 0 0 0; font-size: 14px;">{{DATE}}</p>
                        </td>
                    </tr>
                    <!-- Featured Image -->
                    <tr>
                        <td style="padding: 0;">
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); height: 200px; display: flex; align-items: center; justify-content: center;">
                                <h2 style="color: white; font-size: 28px; margin: 0; padding: 40px; text-align: center;">{{TITLE}}</h2>
                            </div>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <p style="color: #555; font-size: 16px; line-height: 1.8; margin-top: 0;">{{CONTENT}}</p>
                            
                            <!-- CTA Button -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                <tr>
                                    <td align="center">
                                        <a href="{{CTA_LINK}}" style="display: inline-block; background: #2c3e50; color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">{{CTA_TEXT}}</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background: #34495e; padding: 30px; text-align: center; color: white;">
                            <p style="margin: 0 0 10px 0; font-size: 14px;">Christian Conservatives Today</p>
                            <p style="margin: 0; font-size: 12px; color: #95a5a6;">Equipping believers to vote biblically</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>`
    },

    // Template 4: Prayer & Action (Spiritual Theme)
    prayer_action: {
        name: "Prayer & Action",
        theme: "Spiritual",
        html: `<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; font-family: 'Palatino Linotype', serif; background-color: #f5f5f5;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px;">
        <tr>
            <td align="center">
                <table width="600" cellpadding="0" cellspacing="0" style="background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #8e44ad 0%, #3498db 100%); padding: 40px 30px; text-align: center;">
                            <h1 style="color: white; margin: 0; font-size: 28px;">🙏 Prayer & Action</h1>
                            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-style: italic;">"If my people... will humble themselves and pray"</p>
                        </td>
                    </tr>
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h2 style="color: #8e44ad; margin-top: 0; text-align: center;">{{TITLE}}</h2>
                            
                            <!-- Prayer Box -->
                            <div style="background: #f8f9fa; border-left: 4px solid #8e44ad; padding: 20px; margin: 20px 0;">
                                <p style="margin: 0; color: #555; font-size: 15px; line-height: 1.7; font-style: italic;">{{PRAYER}}</p>
                            </div>
                            
                            <p style="color: #555; font-size: 16px; line-height: 1.8;">{{CONTENT}}</p>
                            
                            <!-- Action Steps -->
                            <div style="background: #e8f4f8; padding: 20px; border-radius: 5px; margin: 25px 0;">
                                <h3 style="color: #3498db; margin-top: 0; font-size: 18px;">Action Steps:</h3>
                                <p style="color: #555; margin: 0; line-height: 1.7;">{{ACTION_STEPS}}</p>
                            </div>
                            
                            <!-- CTA Button -->
                            <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                                <tr>
                                    <td align="center">
                                        <a href="{{CTA_LINK}}" style="display: inline-block; background: linear-gradient(135deg, #8e44ad 0%, #3498db 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">{{CTA_TEXT}}</a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background: #f8f9fa; padding: 20px 30px; text-align: center; border-top: 1px solid #eee;">
                            <p style="color: #999; font-size: 12px; margin: 0;">Christian Conservatives Today</p>
                            <p style="color: #bbb; font-size: 11px; margin: 5px 0 0 0; font-style: italic;">"For such a time as this" - Esther 4:14</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>`
    }
};

if (typeof window !== 'undefined') {
    window.EMAIL_TEMPLATES = EMAIL_TEMPLATES;
}
