# 📧 MULTI-TENANT EMAIL MARKETING SYSTEM - COMPLETE DESIGN

## Executive Summary

**Goal**: Enable each user to manage their own email subscriber lists and send campaigns to their congregation/audience.

**Timeline**: 4-6 weeks implementation
**Billing**: Keep PayPal, update subscription tiers
**Launch**: Q2 2025

---

## 🎯 BUSINESS CASE

### Problem Statement
Current system only allows platform-level email campaigns. Users cannot manage their own subscriber lists or send emails to their congregation.

### Solution
Multi-tenant email system where each user has isolated subscriber lists, campaign management, and analytics.

### Value Proposition
**For Churches with 2,000 subscribers**:
- Mailchimp: $100/month
- Our PRO Plan: $49.99/month
  - Video hosting ($75 value)
  - Email marketing ($100 value)
  - Election tracking ($100 value)
  - **Total value**: $275/month

**Savings**: $50/month vs Mailchimp, $225/month vs separate tools

---

## 💰 UPDATED PRICING STRATEGY

### Current Pricing (Inadequate)
- FREE: $0/month - 2GB, 50 videos
- PREMIUM: $9.99/month - 25GB, 500 videos
- PRO: $24.99/month - 100GB, 2,000 videos
- ENTERPRISE: $99.99/month - Unlimited

### New Pricing (With Email)
**FREE** - $0/month
- 2GB storage, 50 videos
- NO email campaigns

**PREMIUM** - $19.99/month (+$10)
- 25GB storage, 500 videos
- **500 email subscribers**
- **1,000 emails/month**

**PRO** - $49.99/month (+$25) ⭐ BEST VALUE
- 100GB storage, 2,000 videos
- **5,000 email subscribers**
- **10,000 emails/month**

**ENTERPRISE** - $149.99/month (+$50)
- Unlimited storage, videos
- **Unlimited email subscribers**
- **50,000 emails/month**

### Pricing Justification
**Why Higher Prices?**
- Email marketing is expensive (Mailchimp charges $100-300/month)
- AWS SES costs $1 per 10,000 emails (98% profit margin)
- Users get video + email + election tracking for less than Mailchimp alone
- Competitive advantage: all-in-one platform

---

## 🏗️ TECHNICAL ARCHITECTURE

### Database Schema (DynamoDB)

#### 1. user-email-subscribers
**Purpose**: Store each user's subscriber list

```
Primary Key: user_id (String)
Sort Key: subscriber_email (String)

Attributes:
- user_id: String (user's unique ID)
- subscriber_email: String (subscriber's email)
- first_name: String (required)
- last_name: String (optional)
- phone: String (optional)
- status: String ("active", "unsubscribed")
- subscribed_at: String (ISO timestamp)
- source: String ("manual", "import", "form")
- tags: List<String> (optional categorization)
- custom_fields: Map (optional additional data)
- unsubscribed_at: String (ISO timestamp, if unsubscribed)
```

**Indexes**:
- GSI: status-index (user_id, status) - Query active subscribers
- GSI: email-index (subscriber_email) - Check duplicates across users

---

#### 2. user-email-campaigns
**Purpose**: Store each user's email campaigns

```
Primary Key: user_id (String)
Sort Key: campaign_id (String)

Attributes:
- user_id: String
- campaign_id: String (UUID)
- title: String
- subject: String
- content: String (HTML)
- template_id: String (which template used)
- status: String ("draft", "scheduled", "sending", "sent", "failed")
- created_at: String (ISO timestamp)
- scheduled_send: String (ISO timestamp, optional)
- sent_at: String (ISO timestamp, when sent)
- recipient_count: Number
- open_count: Number
- click_count: Number
- bounce_count: Number
- unsubscribe_count: Number
- filter_tags: List<String> (send to specific tags)
```

**Indexes**:
- GSI: status-index (user_id, status) - Query campaigns by status

---

#### 3. user-email-events
**Purpose**: Track opens, clicks, bounces per user

```
Primary Key: user_id (String)
Sort Key: event_id (String)

Attributes:
- user_id: String
- event_id: String (UUID)
- campaign_id: String
- subscriber_email: String
- event_type: String ("opened", "clicked", "bounced", "unsubscribed")
- event_data: Map (URL for clicks, bounce reason, etc.)
- timestamp: Number (Unix timestamp for sorting)
- date: String (YYYY-MM-DD for daily aggregation)
```

**Indexes**:
- GSI: campaign-index (campaign_id, timestamp) - Query events by campaign
- GSI: email-index (subscriber_email, timestamp) - Query events by subscriber

---

#### 4. users (Enhanced)
**Purpose**: Add email quota fields to existing users table

```
New Fields:
- email_subscriber_limit: Number (500, 5000, unlimited)
- email_monthly_limit: Number (1000, 10000, 50000)
- email_subscribers_count: Number (current count)
- email_sent_this_month: Number (resets monthly)
- email_quota_reset_date: String (ISO timestamp)
```

---

### Lambda Functions

#### 1. user-email-api (NEW)
**Purpose**: Handle all user-level email operations

**Actions**:
- `add_subscriber` - Add subscriber to user's list
- `import_subscribers` - Bulk CSV import
- `list_subscribers` - Get user's subscribers (paginated)
- `update_subscriber` - Update subscriber info
- `delete_subscriber` - Remove subscriber
- `unsubscribe` - Handle unsubscribe requests
- `create_campaign` - Create new campaign
- `update_campaign` - Edit campaign
- `send_campaign` - Send campaign to subscribers
- `schedule_campaign` - Schedule future send
- `get_campaign` - Get campaign details
- `list_campaigns` - Get user's campaigns
- `get_analytics` - Get campaign analytics
- `track_open` - Log email open event
- `track_click` - Log email click event

**Quota Enforcement**:
```python
def check_subscriber_quota(user_id):
    user = get_user(user_id)
    if user['email_subscribers_count'] >= user['email_subscriber_limit']:
        return False, "Subscriber limit reached"
    return True, "Quota available"

def check_send_quota(user_id, recipient_count):
    user = get_user(user_id)
    if user['email_sent_this_month'] + recipient_count > user['email_monthly_limit']:
        return False, "Monthly email limit reached"
    return True, "Quota available"
```

**Data Isolation**:
```python
def list_subscribers(user_id):
    # CRITICAL: Always filter by user_id
    response = subscribers_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id}
    )
    return response['Items']
```

---

#### 2. email-sender (NEW)
**Purpose**: Background Lambda for sending emails via AWS SES

**Trigger**: SQS queue (decouples sending from API)

**Process**:
1. Receive campaign_id from SQS
2. Get campaign details
3. Get all active subscribers for user
4. For each subscriber:
   - Replace mail merge tokens ({{first_name}}, etc.)
   - Generate tracking pixel URL
   - Wrap links with click tracking
   - Send via AWS SES
   - Log send event
5. Update campaign stats
6. Handle bounces and errors

**Mail Merge**:
```python
def apply_mail_merge(content, subscriber):
    content = content.replace('{{first_name}}', subscriber.get('first_name', ''))
    content = content.replace('{{last_name}}', subscriber.get('last_name', ''))
    content = content.replace('{{email}}', subscriber['subscriber_email'])
    
    # Generate unsubscribe link
    unsubscribe_token = generate_token(user_id, subscriber_email)
    unsubscribe_url = f"https://christianconservativestoday.com/unsubscribe?token={unsubscribe_token}"
    content = content.replace('{{unsubscribe_link}}', unsubscribe_url)
    
    return content
```

**Tracking Pixel**:
```python
def add_tracking_pixel(content, tracking_id):
    pixel_url = f"https://christianconservativestoday.com/track/open/{tracking_id}"
    pixel_html = f'<img src="{pixel_url}" width="1" height="1" style="display:none;" />'
    content = content.replace('</body>', f'{pixel_html}</body>')
    return content
```

---

### Frontend Pages

#### 1. user-email-dashboard.html (NEW)
**Purpose**: Main email marketing dashboard for users

**Features**:
- Campaign list with stats (sent, opens, clicks)
- Quick actions (create campaign, import subscribers)
- Quota usage display (subscribers, emails sent this month)
- Recent activity feed
- Analytics overview

**Layout**:
```
+----------------------------------+
| Email Marketing Dashboard        |
+----------------------------------+
| Quota: 1,234 / 5,000 subscribers |
| Sent: 3,456 / 10,000 this month  |
+----------------------------------+
| [Create Campaign] [Import CSV]   |
+----------------------------------+
| Recent Campaigns:                |
| - Newsletter #5 (sent, 45% open) |
| - Event Invite (scheduled)       |
| - Welcome Series (draft)         |
+----------------------------------+
```

---

#### 2. user-email-subscribers.html (NEW)
**Purpose**: Manage subscriber list

**Features**:
- Subscriber table (email, name, status, subscribed date)
- Add subscriber form
- CSV import
- Bulk actions (delete, tag, export)
- Search and filter
- Pagination

**Actions**:
- Add subscriber manually
- Import from CSV
- Edit subscriber details
- Delete subscriber
- View subscriber activity

---

#### 3. user-email-campaign-create.html (NEW)
**Purpose**: Create/edit email campaigns

**Features**:
- Template selector (5 professional templates)
- Dual editor (Visual + HTML)
- Subject line editor
- Preview function
- Mail merge token insertion
- Recipient selection (all, tags, specific)
- Send now or schedule

**Workflow**:
1. Choose template
2. Edit content (visual or HTML)
3. Set subject line
4. Select recipients
5. Preview
6. Send or schedule

---

#### 4. user-email-analytics.html (NEW)
**Purpose**: Campaign analytics and reporting

**Features**:
- Campaign performance table
- Open rate, click rate, bounce rate
- Subscriber engagement metrics
- Top performing campaigns
- Date range filtering
- Export reports

**Metrics**:
- Total campaigns sent
- Average open rate
- Average click rate
- Most engaged subscribers
- Best performing subject lines

---

### AWS SES Configuration

#### Sending Identity
**Current**: contact@christianconservativestoday.com (platform)
**New**: Users send from contact@christianconservativestoday.com with Reply-To set to user's email

**Why Not User's Domain?**
- Requires DNS verification per user (complex)
- Users may not have technical skills
- Deliverability issues with unverified domains
- Simpler to manage one verified domain

**Email Headers**:
```
From: Christian Conservatives Today <contact@christianconservativestoday.com>
Reply-To: Pastor John <pastor@churchexample.com>
Subject: Weekly Newsletter
```

#### Bounce Handling
**SNS Topic**: ses-bounces
**Lambda**: bounce-handler
**Process**:
1. SES sends bounce notification to SNS
2. Lambda receives notification
3. Update subscriber status to "bounced"
4. Increment campaign bounce_count
5. Log event in user-email-events

---

## 🔐 SECURITY & DATA ISOLATION

### Critical Security Patterns

#### 1. Always Filter by user_id
```python
# CORRECT - User can only see their data
def list_subscribers(user_id):
    return subscribers_table.query(
        KeyConditionExpression='user_id = :uid',
        ExpressionAttributeValues={':uid': user_id}
    )

# WRONG - User could see all subscribers
def list_subscribers():
    return subscribers_table.scan()  # DON'T DO THIS!
```

#### 2. Validate Ownership
```python
def send_campaign(user_id, campaign_id):
    campaign = get_campaign(campaign_id)
    
    # CRITICAL: Verify user owns this campaign
    if campaign['user_id'] != user_id:
        raise PermissionError("Not your campaign")
    
    # Proceed with sending
    send_emails(campaign)
```

#### 3. Quota Enforcement
```python
def add_subscriber(user_id, email):
    # Check quota BEFORE adding
    allowed, message = check_subscriber_quota(user_id)
    if not allowed:
        return {'error': message, 'upgrade_url': '/pricing'}
    
    # Add subscriber
    subscribers_table.put_item(Item={...})
```

---

## 📊 QUOTA MANAGEMENT

### Subscriber Limits
**FREE**: 0 subscribers (no email feature)
**PREMIUM**: 500 subscribers
**PRO**: 5,000 subscribers
**ENTERPRISE**: Unlimited

### Monthly Send Limits
**FREE**: 0 emails
**PREMIUM**: 1,000 emails/month
**PRO**: 10,000 emails/month
**ENTERPRISE**: 50,000 emails/month

### Quota Reset
**When**: 1st of each month at midnight UTC
**Process**:
```python
def reset_monthly_quotas():
    # Run via CloudWatch Events (cron: 0 0 1 * ? *)
    users = scan_all_users()
    for user in users:
        users_table.update_item(
            Key={'user_id': user['user_id']},
            UpdateExpression='SET email_sent_this_month = :zero, email_quota_reset_date = :now',
            ExpressionAttributeValues={
                ':zero': 0,
                ':now': datetime.now().isoformat()
            }
        )
```

### Upgrade Prompts
**When to Show**:
- 90% of subscriber limit reached
- 90% of monthly send limit reached
- User tries to exceed limit

**Message**:
```
⚠️ You've reached 90% of your subscriber limit (450/500).
Upgrade to PRO for 5,000 subscribers!
[Upgrade Now]
```

---

## 💳 BILLING INTEGRATION

### PayPal Subscription Updates

#### Step 1: Create New Plans in PayPal
```
PREMIUM Plan:
- Name: "Premium Ministry"
- Price: $19.99/month
- Description: "25GB storage, 500 videos, 500 email subscribers, 1,000 emails/month"

PRO Plan:
- Name: "PRO Church"
- Price: $49.99/month
- Description: "100GB storage, 2,000 videos, 5,000 email subscribers, 10,000 emails/month"

ENTERPRISE Plan:
- Name: "Enterprise Network"
- Price: $149.99/month
- Description: "Unlimited storage, videos, email subscribers, 50,000 emails/month"
```

#### Step 2: Update paypal_billing_api Lambda
```python
# Add new plan IDs
PLAN_IDS = {
    'premium': 'P-NEW-PREMIUM-PLAN-ID',
    'pro': 'P-NEW-PRO-PLAN-ID',
    'enterprise': 'P-NEW-ENTERPRISE-PLAN-ID'
}

# Add email quota fields
TIER_LIMITS = {
    'free': {
        'storage_limit': 2 * 1024 * 1024 * 1024,
        'video_limit': 50,
        'email_subscriber_limit': 0,
        'email_monthly_limit': 0
    },
    'premium': {
        'storage_limit': 25 * 1024 * 1024 * 1024,
        'video_limit': 500,
        'email_subscriber_limit': 500,
        'email_monthly_limit': 1000
    },
    'pro': {
        'storage_limit': 100 * 1024 * 1024 * 1024,
        'video_limit': 2000,
        'email_subscriber_limit': 5000,
        'email_monthly_limit': 10000
    },
    'enterprise': {
        'storage_limit': float('inf'),
        'video_limit': float('inf'),
        'email_subscriber_limit': float('inf'),
        'email_monthly_limit': 50000
    }
}
```

#### Step 3: Migrate Existing Users
```python
def migrate_existing_users():
    # Users on old pricing keep their current tier
    # New signups get new pricing
    # Existing users see upgrade prompt with new features
    
    users = scan_all_users()
    for user in users:
        tier = user.get('subscription_tier', 'free')
        limits = TIER_LIMITS[tier]
        
        users_table.update_item(
            Key={'user_id': user['user_id']},
            UpdateExpression='SET email_subscriber_limit = :sub_limit, email_monthly_limit = :send_limit, email_subscribers_count = :zero, email_sent_this_month = :zero',
            ExpressionAttributeValues={
                ':sub_limit': limits['email_subscriber_limit'],
                ':send_limit': limits['email_monthly_limit'],
                ':zero': 0
            }
        )
```

---

## 🚀 IMPLEMENTATION PLAN

### Phase 1: Backend (Weeks 1-2)

**Week 1: Database & Core API**
- [ ] Create user-email-subscribers table
- [ ] Create user-email-campaigns table
- [ ] Create user-email-events table
- [ ] Update users table schema
- [ ] Create user-email-api Lambda
- [ ] Implement subscriber CRUD operations
- [ ] Implement quota enforcement
- [ ] Add data isolation checks

**Week 2: Campaign & Sending**
- [ ] Implement campaign CRUD operations
- [ ] Create email-sender Lambda
- [ ] Set up SQS queue for sending
- [ ] Implement mail merge logic
- [ ] Add tracking pixel generation
- [ ] Add click tracking wrapper
- [ ] Configure AWS SES sending
- [ ] Set up bounce handling

### Phase 2: Frontend (Weeks 3-4)

**Week 3: Dashboard & Subscribers**
- [ ] Create user-email-dashboard.html
- [ ] Create user-email-subscribers.html
- [ ] Implement subscriber table with pagination
- [ ] Add subscriber form
- [ ] Implement CSV import
- [ ] Add quota usage display
- [ ] Integrate with user-email-api

**Week 4: Campaign Creation & Analytics**
- [ ] Create user-email-campaign-create.html
- [ ] Implement template selector
- [ ] Add dual editor (Visual + HTML)
- [ ] Implement preview function
- [ ] Add recipient selection
- [ ] Create user-email-analytics.html
- [ ] Implement analytics dashboard
- [ ] Add export functionality

### Phase 3: Testing & Launch (Weeks 5-6)

**Week 5: Beta Testing**
- [ ] Recruit 5 beta churches
- [ ] Provide free PRO accounts
- [ ] Monitor usage and gather feedback
- [ ] Fix bugs and issues
- [ ] Optimize performance
- [ ] Test quota enforcement
- [ ] Verify data isolation

**Week 6: Documentation & Launch**
- [ ] Create user documentation
- [ ] Create video tutorials
- [ ] Update marketing materials
- [ ] Update pricing page
- [ ] Announce to existing users
- [ ] Launch to public
- [ ] Monitor system performance

---

## 📈 SUCCESS METRICS

### Technical Metrics
- **Email Delivery Rate**: >95%
- **API Response Time**: <500ms
- **System Uptime**: >99.9%
- **Data Isolation**: 100% (no cross-user data leaks)

### Business Metrics
- **Conversion Rate**: 20% of free users upgrade for email
- **Revenue Impact**: 2x MRR from higher pricing
- **User Adoption**: 50% of paid users use email feature
- **Churn Reduction**: <5% monthly churn

### User Satisfaction
- **Feature Satisfaction**: >4.5/5 stars
- **Support Tickets**: <10% of users need help
- **Upgrade Rate**: 30% upgrade from Premium to PRO

---

## 🎯 LAUNCH STRATEGY

### Pre-Launch (Week 5)
- [ ] Update sales flyer to v3.2 (remove "Coming Soon")
- [ ] Create launch announcement email
- [ ] Prepare video tutorial
- [ ] Set up support documentation
- [ ] Train support team

### Launch Day (Week 6, Day 1)
- [ ] Deploy all Lambda functions
- [ ] Enable feature for all users
- [ ] Send launch announcement email
- [ ] Post on social media
- [ ] Monitor system closely

### Post-Launch (Week 6, Days 2-7)
- [ ] Gather user feedback
- [ ] Fix any critical bugs
- [ ] Optimize performance
- [ ] Create case studies
- [ ] Plan next features

---

## 💡 FUTURE ENHANCEMENTS

### Phase 2 Features (Q3 2025)
- [ ] A/B testing for subject lines
- [ ] Automated drip campaigns
- [ ] Segmentation by engagement
- [ ] Advanced analytics (heat maps, device tracking)
- [ ] Integration with Zapier
- [ ] Mobile app for campaign management

### Phase 3 Features (Q4 2025)
- [ ] SMS marketing integration
- [ ] Landing page builder
- [ ] Form builder for signups
- [ ] CRM integration
- [ ] Advanced automation workflows
- [ ] White-label email sending (user's domain)

---

## ✅ DECISION CHECKLIST

Before proceeding with implementation:

- [x] Business case validated (95% cheaper than Mailchimp)
- [x] Pricing strategy finalized (Premium $19.99, PRO $49.99, Enterprise $149.99)
- [x] Technical architecture designed (multi-tenant with data isolation)
- [x] Database schema defined (3 new tables, 1 enhanced)
- [x] Lambda functions specified (user-email-api, email-sender)
- [x] Frontend pages planned (4 new pages)
- [x] Security patterns established (always filter by user_id)
- [x] Quota management designed (subscriber and send limits)
- [x] Billing integration planned (PayPal subscription updates)
- [x] Implementation timeline set (4-6 weeks)
- [x] Success metrics defined (technical, business, satisfaction)
- [x] Launch strategy prepared (pre-launch, launch, post-launch)

**Status**: ✅ Design complete, ready for implementation approval

---

**Next Step**: Get approval to proceed with Phase 1 backend implementation (Weeks 1-2)
