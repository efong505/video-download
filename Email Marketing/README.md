# Email Marketing System - Mailchimp-Style Solution

## Overview
Complete email marketing and automation platform integrated into Christian Conservatives Today, providing newsletter campaigns, subscriber management, automation workflows, and analytics.

## Mailchimp vs Tailwind - Why Mailchimp?

### Mailchimp (Email Marketing Platform)
- **Focus**: Pure email marketing and automation
- **Strength**: Campaigns, segmentation, analytics, A/B testing
- **Use Case**: Newsletters, promotional emails, drip campaigns
- **Integration**: Perfect fit for content platform (articles, videos, news)
- **ROI**: Email converts 40x better than social media

### Tailwind (Social Media Scheduler)
- **Focus**: Pinterest/Instagram scheduling + email
- **Strength**: Visual content calendar, hashtag tools
- **Use Case**: E-commerce brands, visual marketers
- **Complexity**: Multi-platform management
- **Fit**: Less relevant for text-heavy ministry content

### Decision: Build Mailchimp-Style Solution
**Reasons**:
1. ✅ You already have content (articles, news, videos, election updates)
2. ✅ Natural fit: Send newsletters about new content
3. ✅ Simpler scope: Email-only vs multi-platform social
4. ✅ Higher ROI: Email converts better for ministry content
5. ✅ Existing user base: Convert website visitors to subscribers
6. ✅ AWS SES integration is straightforward and cost-effective

## Core Features

### 1. Subscriber Management
- **Email List**: Store subscribers in DynamoDB
- **Segmentation**: Tag subscribers by interests (articles, videos, election, prayer)
- **Import/Export**: CSV bulk import/export
- **Opt-in/Opt-out**: Double opt-in confirmation, one-click unsubscribe
- **List Hygiene**: Bounce handling, complaint management
- **Custom Fields**: First name, last name, state, interests

### 2. Campaign Builder
- **Visual Editor**: Drag-and-drop email builder (or reuse Quill.js)
- **Templates**: Pre-built email templates (newsletter, announcement, update)
- **Personalization**: Merge tags ({{first_name}}, {{article_title}})
- **Preview**: Desktop/mobile preview before sending
- **Test Emails**: Send test to yourself before campaign

### 3. Automation Workflows
- **Welcome Series**: Automatic welcome email on signup
- **Drip Campaigns**: Multi-email sequences (e.g., "New Subscriber Series")
- **Triggers**: Send based on actions (new article published, video uploaded)
- **Abandoned Cart**: For future e-commerce integration
- **Re-engagement**: Automatic emails to inactive subscribers

### 4. Email Analytics
- **Open Tracking**: 1x1 pixel tracking
- **Click Tracking**: Redirect URLs to track clicks
- **Conversion Tracking**: Track signups, donations, actions
- **Engagement Metrics**: Open rate, click rate, unsubscribe rate
- **A/B Testing**: Test subject lines, content, send times

### 5. Scheduling & Sending
- **Immediate Send**: Send campaign now
- **Scheduled Send**: Schedule for specific date/time
- **Time Zone Optimization**: Send at optimal time per subscriber
- **Batch Sending**: Throttle sends to avoid spam filters
- **Resend to Non-Openers**: Automatic resend with different subject

## Technical Architecture

### AWS Services
- **Amazon SES**: Email sending (verified domain required)
- **DynamoDB**: Subscriber data, campaign data, analytics
- **Lambda**: Campaign processing, automation triggers
- **EventBridge**: Scheduled sends, automation workflows
- **S3**: Email templates, images, attachments
- **SNS**: Bounce/complaint notifications

### Database Schema

#### Subscribers Table
```
email (PK)
first_name
last_name
state
interests (list: articles, videos, election, prayer)
status (active, unsubscribed, bounced)
subscribed_at
source (website, import, api)
tags (list)
custom_fields (map)
```

#### Campaigns Table
```
campaign_id (PK)
title
subject
from_name
from_email
reply_to
content_html
content_text
template_id
segment (all, tagged, custom)
status (draft, scheduled, sending, sent)
scheduled_send_time
sent_at
recipient_count
open_count
click_count
unsubscribe_count
```

#### Analytics Table
```
event_id (PK)
campaign_id
email
event_type (sent, opened, clicked, bounced, complained, unsubscribed)
timestamp
metadata (link_url, bounce_reason, etc.)
```

#### Automation Table
```
automation_id (PK)
name
trigger_type (signup, article_published, video_uploaded)
status (active, paused)
emails (list of email objects with delay, subject, content)
created_at
```

### Lambda Functions

#### email_campaigns_api
- Actions: create, list, get, update, delete, send
- Handles campaign CRUD operations
- Processes campaign sends

#### email_subscribers_api
- Actions: subscribe, unsubscribe, list, import, export
- Manages subscriber data
- Handles opt-in/opt-out

#### email_tracking_api
- Actions: track_open, track_click
- Logs analytics events
- Updates campaign statistics

#### email_automation_api
- Actions: create, trigger, pause, resume
- Manages automation workflows
- Processes trigger events

#### email_sender
- Batch processes campaign sends
- Handles SES API calls
- Manages send throttling
- Logs send events

## Integration with Existing Platform

### Content Notifications
- **New Article Published**: Automatic email to subscribers
- **New Video Uploaded**: Weekly digest of new videos
- **Election Updates**: Breaking news alerts for election changes
- **Prayer Requests**: Daily prayer digest

### Subscription Forms
- **Footer Signup**: Add email signup to all pages
- **Article Popup**: Exit-intent popup on articles
- **Video Page**: Subscribe for new video notifications
- **Election Map**: Subscribe for state-specific updates

### User Accounts
- **Sync with Users Table**: Link email subscribers to user accounts
- **Preference Center**: Let users manage email preferences
- **Unified Profile**: Show subscription status in user profile

## Implementation Plan

### Phase 1: Foundation (Week 1-2)
- [ ] Set up Amazon SES (verify domain, request production access)
- [ ] Create DynamoDB tables (subscribers, campaigns, analytics)
- [ ] Build email_subscribers_api Lambda
- [ ] Create basic subscription form
- [ ] Implement double opt-in workflow

### Phase 2: Campaign Builder (Week 3-4)
- [ ] Build email_campaigns_api Lambda
- [ ] Create campaign builder UI (admin-campaigns.html)
- [ ] Implement email templates
- [ ] Add merge tag support
- [ ] Build preview functionality

### Phase 3: Sending & Tracking (Week 5-6)
- [ ] Build email_sender Lambda
- [ ] Implement open/click tracking
- [ ] Create email_tracking_api Lambda
- [ ] Build analytics dashboard
- [ ] Add unsubscribe handling

### Phase 4: Automation (Week 7-8)
- [ ] Build email_automation_api Lambda
- [ ] Create automation builder UI
- [ ] Implement welcome series
- [ ] Add trigger system (EventBridge)
- [ ] Build drip campaign workflows

### Phase 5: Advanced Features (Week 9-10)
- [ ] A/B testing functionality
- [ ] Segmentation builder
- [ ] CSV import/export
- [ ] Bounce/complaint handling
- [ ] Re-engagement campaigns

## Cost Analysis

### AWS SES Pricing
- **Sending**: $0.10 per 1,000 emails
- **Receiving**: $0.10 per 1,000 emails (for bounce handling)
- **Attachments**: S3 storage costs

### Example Costs
- **1,000 subscribers, 4 emails/month**: $0.40/month
- **10,000 subscribers, 4 emails/month**: $4.00/month
- **100,000 subscribers, 4 emails/month**: $40.00/month

### Comparison to Mailchimp
- **Mailchimp**: $13-20/month for 500 subscribers
- **AWS SES**: $0.40/month for 1,000 subscribers
- **Savings**: 95%+ cheaper at scale

## Use Cases for Christian Conservatives Today

### Weekly Newsletter
- **Content**: Top 3 articles, latest video, election update
- **Audience**: All subscribers
- **Frequency**: Every Sunday evening
- **Goal**: Drive traffic back to website

### Election Alerts
- **Content**: Breaking election news, candidate updates
- **Audience**: Subscribers interested in election coverage
- **Frequency**: As needed (breaking news)
- **Goal**: Keep users informed on critical races

### New Article Notifications
- **Content**: Article title, excerpt, read more link
- **Audience**: Article subscribers
- **Frequency**: Immediately after publish
- **Goal**: Increase article readership

### Prayer Request Digest
- **Content**: Top 5 prayer requests from prayer wall
- **Audience**: Prayer subscribers
- **Frequency**: Daily at 6am
- **Goal**: Encourage prayer engagement

### Donation Campaigns
- **Content**: Ministry impact, donation appeal
- **Audience**: Engaged subscribers (high open rate)
- **Frequency**: Quarterly
- **Goal**: Raise funds for platform operations

## Success Metrics

### Email Performance
- **Open Rate**: Target 20-30% (industry average 15-25%)
- **Click Rate**: Target 2-5% (industry average 1-3%)
- **Unsubscribe Rate**: Keep below 0.5%
- **Bounce Rate**: Keep below 2%

### Business Impact
- **Website Traffic**: Increase from email by 30%
- **Article Readership**: Increase by 40%
- **User Engagement**: Increase return visits by 50%
- **Donations**: Generate $X per campaign

## Next Steps

1. **Review this documentation** - Confirm approach and features
2. **Set up AWS SES** - Verify domain, request production access
3. **Create database tables** - Set up DynamoDB schema
4. **Build subscriber API** - Start with basic subscription functionality
5. **Create signup forms** - Add to website footer and key pages
6. **Test end-to-end** - Verify subscription and email sending works
7. **Build campaign builder** - Create admin interface for campaigns
8. **Launch first campaign** - Send welcome email to existing users

## Questions to Consider

1. **Domain Verification**: Do you have access to DNS records for christianconservativestoday.com?
2. **From Email**: What email should campaigns come from? (e.g., newsletter@christianconservativestoday.com)
3. **Reply-To**: Should replies go to a monitored inbox?
4. **Unsubscribe**: One-click or preference center?
5. **Frequency**: How often will you send campaigns?
6. **Content Strategy**: Who will write email content?
7. **Design**: Use simple text emails or HTML templates?
8. **Compliance**: Familiar with CAN-SPAM Act requirements?

## Resources

### AWS Documentation
- [Amazon SES Developer Guide](https://docs.aws.amazon.com/ses/)
- [SES Email Sending Best Practices](https://docs.aws.amazon.com/ses/latest/dg/best-practices.html)
- [SES Production Access Request](https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html)

### Email Marketing Best Practices
- Subject lines: 40-50 characters
- Preview text: 85-100 characters
- Mobile-first design
- Clear call-to-action
- Personalization increases opens by 26%
- Segmentation increases revenue by 760%

### Legal Compliance
- **CAN-SPAM Act**: Include physical address, unsubscribe link
- **GDPR**: Get explicit consent for EU subscribers
- **CCPA**: Allow California residents to opt-out
