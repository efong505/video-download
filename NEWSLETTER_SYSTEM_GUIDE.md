# Newsletter System - User Guide

## Overview

The Newsletter System allows you to build, send, and manage email newsletters to your subscribers. It includes a drag-and-drop editor, subscriber management, templates, and analytics tracking.

## Features

- **Rich Text Editor**: Create beautiful newsletters with formatting, images, and links
- **Subscriber Management**: Track active and unsubscribed users
- **Email Templates**: Save and reuse newsletter layouts
- **Send & Schedule**: Send immediately or schedule for later
- **Analytics**: Track open rates and click rates
- **Unsubscribe Links**: Automatic unsubscribe handling

---

## For Subscribers

### How to Subscribe

1. Go to **https://christianconservativestoday.com/subscribe.html**
2. Enter your name (optional) and email address
3. Click "Subscribe"
4. You'll receive newsletters when admins send them

### How to Unsubscribe

1. Click the unsubscribe link at the bottom of any newsletter email
2. Click "Unsubscribe" button on the page
3. You'll be removed from the mailing list immediately

---

## For Admins

### Accessing Newsletter Management

1. Log in as admin
2. Go to **Admin Dashboard** → **Newsletters** (in secondary menu)
3. You'll see three tabs: Newsletters, Subscribers, Templates

---

## Creating a Newsletter

### Step 1: Open Newsletter Editor

1. Click **"Create Newsletter"** button
2. Modal opens with newsletter form

### Step 2: Fill in Details

- **Title**: Internal name for the newsletter (not shown to subscribers)
- **Email Subject**: What subscribers see in their inbox
- **Content**: Use the rich text editor to create your message
- **Status**: 
  - **Draft**: Save for later
  - **Ready to Send**: Mark as ready (doesn't send yet)

### Step 3: Format Content

Use the editor toolbar:
- **Bold, Italic, Underline**: Text formatting
- **Link**: Add clickable links
- **Image**: Insert images
- **Lists**: Ordered or bullet lists
- **Clean**: Remove formatting

### Step 4: Add Unsubscribe Link

**IMPORTANT**: Always include `{{unsubscribe_link}}` in your newsletter content. This will be replaced with the actual unsubscribe URL when sent.

Example:
```
Thank you for reading!

If you no longer wish to receive these emails, click here: {{unsubscribe_link}}
```

### Step 5: Save

- Click **"Save"** to save as draft
- Newsletter appears in the Newsletters tab

---

## Sending a Newsletter

### Option 1: Send Immediately

1. Find your newsletter in the Newsletters tab
2. Click **"Send"** button
3. Confirm: "Send this newsletter to all active subscribers?"
4. Newsletter is sent to all active subscribers immediately

### Option 2: Schedule for Later

1. Edit your newsletter
2. Set **Scheduled Send** date/time (feature in development)
3. Save newsletter
4. It will send automatically at scheduled time

---

## Managing Subscribers

### View Subscribers

1. Go to **Subscribers** tab
2. See list of all subscribers with:
   - Email address
   - Name (if provided)
   - Status (active/unsubscribed)
   - Subscription date
   - Source (website, import, etc.)

### Subscriber Statistics

- **Active Subscribers**: Currently receiving newsletters
- **Unsubscribed**: Opted out of emails

### Manual Unsubscribe

Admins cannot manually unsubscribe users. Users must click the unsubscribe link in emails.

---

## Using Templates

### Create a Template

1. Go to **Templates** tab
2. Click **"Create Template"** button
3. Fill in:
   - **Template Name**: e.g., "Monthly Update"
   - **Description**: What this template is for
   - **HTML Content**: Full HTML code for the template
4. Click **"Save Template"**

### Use a Template

1. When creating a newsletter
2. Click **"Use Template"** on a saved template
3. Template content loads into editor
4. Customize and send

### Template Tips

- Include `{{unsubscribe_link}}` placeholder
- Use inline CSS for styling (email clients don't support external CSS)
- Test templates before sending to full list

---

## Newsletter Analytics

### Tracking Metrics

Each sent newsletter tracks:
- **Recipients**: Number of subscribers who received it
- **Opens**: How many opened the email (tracked via invisible pixel)
- **Clicks**: How many clicked links in the email

### View Analytics

1. Go to **Newsletters** tab
2. Find sent newsletter
3. View metrics in the table:
   - **Recipients**: Total sent
   - **Open Count**: Number of opens
   - **Click Count**: Number of clicks

### How Tracking Works

- **Open Tracking**: Invisible 1x1 pixel image in email
- **Click Tracking**: Special tracking URLs on links
- **Privacy**: Tracking is anonymous, no personal data collected

---

## Best Practices

### Content Guidelines

1. **Keep it concise**: Most people skim emails
2. **Clear subject lines**: Tell them what's inside
3. **Call to action**: Include clear next steps
4. **Mobile-friendly**: Most people read on phones
5. **Unsubscribe link**: Always include it (required by law)

### Sending Guidelines

1. **Test first**: Send to yourself before full list
2. **Consistent schedule**: Weekly, monthly, etc.
3. **Don't spam**: Only send valuable content
4. **Segment later**: Consider different lists for different topics

### Legal Requirements

- **CAN-SPAM Act**: Must include unsubscribe link
- **GDPR**: Get consent before adding to list
- **Honest subject lines**: Don't mislead subscribers

---

## Troubleshooting

### Newsletter Not Sending

**Problem**: Clicked "Send" but subscribers didn't receive it

**Solutions**:
1. Check AWS SES is configured and verified
2. Verify sender email is verified in AWS SES
3. Check CloudWatch logs for errors
4. Ensure subscribers have "active" status

### Unsubscribe Link Not Working

**Problem**: Unsubscribe link shows error

**Solutions**:
1. Verify `{{unsubscribe_link}}` is in newsletter content
2. Check API Gateway is deployed
3. Test unsubscribe URL manually: `https://christianconservativestoday.com/unsubscribe.html?email=test@example.com`

### Images Not Showing

**Problem**: Images in newsletter don't display

**Solutions**:
1. Use full HTTPS URLs for images (not relative paths)
2. Host images on S3 or CloudFront
3. Test image URLs in browser first
4. Some email clients block images by default

### Low Open Rates

**Problem**: Few people opening newsletters

**Solutions**:
1. Improve subject lines (be specific and compelling)
2. Send at optimal times (Tuesday-Thursday, 10am-2pm)
3. Clean your list (remove inactive subscribers)
4. Personalize content
5. A/B test different approaches

---

## API Endpoints

For developers integrating with the newsletter system:

### Base URL
```
https://gu6c08ctel.execute-api.us-east-1.amazonaws.com/prod/newsletter
```

### Available Actions

**Create Newsletter**
```
POST /newsletter?action=create_newsletter
Body: {title, subject, content, status, created_by}
```

**List Newsletters**
```
GET /newsletter?action=list_newsletters&status=draft
```

**Send Newsletter**
```
POST /newsletter?action=send_newsletter
Body: {newsletter_id}
```

**Subscribe**
```
POST /newsletter?action=subscribe
Body: {email, name, source}
```

**Unsubscribe**
```
GET /newsletter?action=unsubscribe&email=user@example.com
```

**List Subscribers**
```
GET /newsletter?action=list_subscribers&status=active
```

---

## AWS SES Setup (For Admins)

### Verify Sender Email

1. Go to AWS SES Console
2. Click "Verified identities"
3. Click "Create identity"
4. Choose "Email address"
5. Enter: `noreply@christianconservativestoday.com`
6. Click verification link in email
7. Status changes to "Verified"

### Move Out of Sandbox

AWS SES starts in "sandbox mode" (can only send to verified emails).

To send to any email:
1. Go to AWS SES Console
2. Click "Account dashboard"
3. Click "Request production access"
4. Fill out form explaining use case
5. Wait for approval (usually 24 hours)

### Set Sending Limits

- **Sandbox**: 200 emails/day, 1 email/second
- **Production**: 50,000 emails/day, 14 emails/second (increases over time)

---

## Database Schema

### newsletters Table
- `newsletter_id` (Primary Key): Unique ID
- `title`: Internal title
- `subject`: Email subject line
- `content`: HTML content
- `template_id`: Associated template
- `status`: draft/ready/sent
- `scheduled_send`: ISO date string
- `created_by`: Admin email
- `created_at`: ISO date string
- `sent_at`: ISO date string
- `recipient_count`: Number sent to
- `open_count`: Number of opens
- `click_count`: Number of clicks

### email_subscribers Table
- `email` (Primary Key): Subscriber email
- `name`: Subscriber name
- `status`: active/unsubscribed
- `subscribed_at`: ISO date string
- `source`: website/import/api

### newsletter_templates Table
- `template_id` (Primary Key): Unique ID
- `name`: Template name
- `description`: Template description
- `html`: HTML content
- `thumbnail`: Preview image URL
- `created_at`: ISO date string

### newsletter_analytics Table
- `tracking_id` (Primary Key): Unique tracking ID
- `newsletter_id`: Associated newsletter
- `email`: Subscriber email
- `opened`: Boolean
- `clicked`: Boolean
- `sent_at`: ISO date string

---

## Support

For issues or questions:
1. Check CloudWatch logs: `/aws/lambda/newsletter_api`
2. Test API directly with Postman or curl
3. Review this guide for common solutions
4. Check AWS SES sending statistics

---

## Quick Reference

| Task | Location | Action |
|------|----------|--------|
| Subscribe | subscribe.html | Enter email, click Subscribe |
| Unsubscribe | Email link | Click unsubscribe link |
| Create Newsletter | Admin → Newsletters | Click "Create Newsletter" |
| Send Newsletter | Admin → Newsletters | Click "Send" on newsletter |
| View Subscribers | Admin → Subscribers | See full list |
| Create Template | Admin → Templates | Click "Create Template" |
| View Analytics | Admin → Newsletters | Check sent newsletters |

---

## Version History

- **v1.0** (2024): Initial release with basic newsletter functionality
- Rich text editor
- Subscriber management
- Template system
- Open/click tracking
