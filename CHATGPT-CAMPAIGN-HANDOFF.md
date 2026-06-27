# Email Campaign System Handoff - Book 2 Promotion

## Purpose
This document explains our email drip campaign infrastructure so an AI agent can design campaign content that fits our exact technical requirements.

---

## 🏗️ System Architecture Overview

### Campaign Storage
- **Platform**: AWS DynamoDB table `user-email-campaigns`
- **Primary Key**: `user_id` (UUID - owner ID)
- **Sort Key**: `campaign_id` (UUID - unique campaign identifier)

### Campaign Groups (Sequences)
We organize campaigns into "groups" that form complete email sequences:

**Existing Campaign Groups:**
1. `pre-purchase-book-sequence` - 7 emails for Book 1 survival kit signups
2. `post-purchase-sequence` - 7 emails for Book 1 purchasers

**New Campaign Group Needed:**
3. `book2-launch-sequence` - X emails for Book 2 promotion (you decide count)

### Enrollment System
- Table: `user-email-drip-enrollments`
- Tracks each subscriber's progress through a campaign group
- Auto-increments through steps (1 → 2 → 3, etc.)
- Sends next email based on `delay_hours` setting

---

## 📋 Campaign Record Structure

Each email in a sequence is ONE record in DynamoDB with this exact schema:

```json
{
  "user_id": "effa3242-cf64-4021-b2b0-c8a5a9dfd6d2",  // ALWAYS use this (platform owner)
  "campaign_id": "<GENERATE_NEW_UUID>",               // Unique ID per email
  "campaign_name": "Book 2 Email 1: Hook Title",      // Descriptive name
  "campaign_group": "book2-launch-sequence",          // Group name (same for all emails in sequence)
  "sequence_number": 1,                                // Step number (1, 2, 3...)
  "subject_line": "Your subject here",
  "html_content": "<full HTML email content>",
  "delay_hours": 0,                                    // Hours to wait AFTER PREVIOUS email
  "created_at": "2026-06-27T12:00:00Z",
  "status": "active"
}
```

---

## ⏱️ Timing Logic (CRITICAL)

### delay_hours Explained:
- **Email 1**: `delay_hours: 0` (sends immediately upon enrollment)
- **Email 2**: `delay_hours: 24` (sends 24 hours AFTER Email 1)
- **Email 3**: `delay_hours: 48` (sends 48 hours AFTER Email 2)
- And so on...

**Common Patterns:**
- Daily emails: 24 hours between each
- Every 2 days: 48 hours between each
- Every 3 days: 72 hours between each

**Example 7-email sequence:**
```
Email 1: delay_hours = 0   (immediate)
Email 2: delay_hours = 24  (1 day later)
Email 3: delay_hours = 48  (2 days after Email 2)
Email 4: delay_hours = 72  (3 days after Email 3)
Email 5: delay_hours = 48  (2 days after Email 4)
Email 6: delay_hours = 24  (1 day after Email 5)
Email 7: delay_hours = 24  (1 day after Email 6)
```

---

## 📧 HTML Email Content Requirements

### Must Include:
1. **Unsubscribe link** - REQUIRED by law
   ```html
   <a href="https://christianconservativestoday.com/unsubscribe.html?email={{EMAIL}}">Unsubscribe</a>
   ```

2. **Proper HTML structure**
   ```html
   <!DOCTYPE html>
   <html>
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
   </head>
   <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
       <!-- Content here -->
   </body>
   </html>
   ```

3. **Inline CSS** - Email clients strip `<style>` tags
   ```html
   <div style="background: #f4f4f4; padding: 20px;">
   ```

4. **CTA Buttons** - Use this style
   ```html
   <a href="LINK" style="display: inline-block; background: #1a73e8; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">
       Button Text
   </a>
   ```

5. **From Address** - All emails send from:
   ```
   From: Christian Conservatives Today <contact@christianconservativestoday.com>
   ```

### Variable Substitution
The system automatically replaces:
- `{{EMAIL}}` → subscriber's email address
- `{{FIRST_NAME}}` → subscriber's first name (if captured)

---

## 🎯 Campaign Goals & Context

### Book 1 Campaign Strategy (for reference):
**Pre-Purchase (Survival Kit):**
- Email 1: Immediate PDF delivery + welcome
- Email 2-6: Value-building, urgency, social proof
- Email 7: Final pitch to buy full book

**Post-Purchase:**
- Email 1: Thank you + access to resources
- Email 2-6: Deep dives, community building, next steps
- Email 7: Invitation to live event / next product

### Book 2 Details (YOU PROVIDE TO CHATGPT):
- Book title:
- Book topic/theme:
- Target audience:
- Main value proposition:
- Call-to-action (buy link, landing page, etc.):
- Tone/voice (professional, casual, urgent, etc.):

---

## 🤖 Automation System

### How Emails Send:
1. **Enrollment**: User gets added to `user-email-drip-enrollments` with `campaign_group`
2. **Lambda Processor**: Runs daily via EventBridge (checks all active enrollments)
3. **Step Check**: Sees if `delay_hours` has passed since last email
4. **Send**: Triggers SES to send next email in sequence
5. **Increment**: Moves user to next `sequence_number`
6. **Repeat**: Until all emails in group are sent

### Tracking:
- Opens: 1x1 tracking pixel in email
- Clicks: All links rewritten to `/track/click/` endpoint
- Events logged to: `user-email-events` table

---

## 📊 What ChatGPT Should Create

Please provide:

### 1. Campaign Overview
```
Campaign Group Name: book2-launch-sequence
Total Emails: [number]
Target Audience: [who is this for]
Primary Goal: [what action do you want]
Tone: [professional/casual/urgent/friendly]
```

### 2. Sequence Timing
```
Email 1: Immediate (delay_hours: 0)
Email 2: [X hours] after Email 1 (delay_hours: [X])
Email 3: [X hours] after Email 2 (delay_hours: [X])
...
```

### 3. For Each Email, Provide:
```
campaign_name: "Book 2 Email [N]: [Descriptive Title]"
sequence_number: [N]
subject_line: "[Subject]"
delay_hours: [number]

html_content:
[Full HTML email with:
 - Inline CSS styling
 - Clear CTA button
 - Unsubscribe link
 - Mobile-responsive design
 - Variable placeholders {{EMAIL}}, {{FIRST_NAME}}
]

Strategy Note: [Brief explanation of this email's purpose in the sequence]
```

---

## 🛠️ Implementation Steps (YOU DO AFTER CHATGPT RESPONDS)

Once ChatGPT provides the campaign content:

### Step 1: Create Python Script
```python
import boto3
import uuid
from datetime import datetime

campaigns = [
    {
        "user_id": "effa3242-cf64-4021-b2b0-c8a5a9dfd6d2",
        "campaign_id": str(uuid.uuid4()),
        "campaign_name": "[FROM CHATGPT]",
        "campaign_group": "book2-launch-sequence",
        "sequence_number": 1,
        "subject_line": "[FROM CHATGPT]",
        "html_content": """[FROM CHATGPT]""",
        "delay_hours": 0,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "status": "active"
    },
    # ... repeat for each email
]

ddb = boto3.Session(profile_name='ekewaka').resource('dynamodb', region_name='us-east-1')
table = ddb.Table('user-email-campaigns')

for campaign in campaigns:
    table.put_item(Item=campaign)
    print(f"✅ Created: {campaign['campaign_name']}")
```

### Step 2: Test Enrollment
```python
# Enroll test user
enrollments_table = ddb.Table('user-email-drip-enrollments')
enrollments_table.put_item(Item={
    "user_id": "effa3242-cf64-4021-b2b0-c8a5a9dfd6d2",
    "enrollment_id": f"YOUR_EMAIL|{str(uuid.uuid4())}",
    "campaign_group": "book2-launch-sequence",
    "current_step": 1,
    "total_steps": [TOTAL_EMAILS],
    "status": "active",
    "enrolled_at": datetime.utcnow().isoformat() + "Z",
    "last_sent_date": None,
    "next_send_date": datetime.utcnow().isoformat() + "Z"
})
```

### Step 3: Trigger Test
```bash
python trigger-payload.py  # Or use campaign manager "Send Next Now" button
```

### Step 4: Monitor
- Open `advanced-email-analytics.html`
- Check Recent Events tab
- Verify email sends, opens, clicks

---

## 📁 Reference Files in Your Repo

Look at these for examples:
- `Scripts/create-transition-campaigns-part1.py` - Campaign creation script
- `check-campaign-content.py` - View existing campaigns
- `email-subscription-handler/lambda_function.py` - Enrollment logic
- `email-drip-processor/lambda_function.py` - Email sending logic

---

## ✅ Checklist for ChatGPT Response

Make sure ChatGPT provides:
- [ ] Campaign group name
- [ ] Total number of emails
- [ ] Complete timing sequence (delay_hours for each)
- [ ] Full HTML for EACH email
- [ ] Subject lines for each
- [ ] Unsubscribe links in each email
- [ ] Mobile-responsive design
- [ ] Clear CTAs with proper button styling
- [ ] Strategy notes explaining the flow

---

## 🎯 Example Prompt for ChatGPT

"I need you to design a 5-email drip campaign to promote my new book titled '[BOOK TITLE]'. 

The book is about [TOPIC] and targets [AUDIENCE].

Based on the technical specifications in the attached handoff document, please create:

1. A campaign overview with timing strategy
2. 5 complete HTML emails with:
   - Engaging subject lines
   - Full HTML content with inline CSS
   - Clear CTA buttons linking to [YOUR_LINK]
   - Unsubscribe links
   - Mobile-responsive design
3. Recommended delay_hours between each email

Use a [TONE] tone and focus on [KEY BENEFIT].

The sequence should: [YOUR GOALS - build trust, create urgency, etc.]"

---

## 🔄 Return Here With ChatGPT Output

Once you have the campaign content from ChatGPT, come back and say:

"I have the Book 2 campaign content from ChatGPT. Here's what it provided: [paste output]"

I'll help you:
1. Create the Python script to upload campaigns
2. Test the sequence
3. Set up enrollment automation
4. Monitor performance

---

**Current Date for Campaign Creation**: 2026-06-27
**Platform Owner ID**: effa3242-cf64-4021-b2b0-c8a5a9dfd6d2
**AWS Region**: us-east-1
**AWS Profile**: ekewaka
