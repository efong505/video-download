# Book Email Campaign Automation Plan

## Overview
Automatically send 7-email sequence to book subscribers using the multi-tenant email marketing system.

## Email Sequence Schedule
- **Day 0**: Welcome + Free Gift + Your Story (ALREADY SENT via signup)
- **Day 1**: Why I Wrote This Book
- **Day 3**: The Two Paths of AI
- **Day 5**: Personal Impact (Family/Church/Career)
- **Day 7**: Testimonials + Buy
- **Day 10**: Objection Handling
- **Day 14**: Urgency + Offer

## Implementation Options

### Option A: Use Existing Multi-Tenant Campaign System ✅ RECOMMENDED
Your `user-email-api` Lambda already has campaign functionality with scheduled sending.

**Steps:**
1. Create campaign in multi-tenant system for Ed's `user_id`
2. Set campaign type to "drip" or "sequence"
3. Add all 7 emails to campaign
4. Set delay intervals (1 day, 2 days, 2 days, 2 days, 3 days, 4 days)
5. Auto-enroll new book subscribers via bridge function

**Pros:**
- Uses existing infrastructure
- Full campaign management UI
- Segmentation by tags (`book`, `survival-kit`)
- Analytics built-in
- SQS-based sending (scalable)

**Cons:**
- Need to add "drip sequence" logic if not already there
- Need to auto-enroll subscribers

---

### Option B: EventBridge Scheduled Lambda ⚠️ MORE COMPLEX
Create scheduled Lambda that checks subscriber dates and sends appropriate email.

**Steps:**
1. EventBridge rule runs daily at 9am
2. Lambda queries `book-subscribers` table
3. Calculates days since `subscribed_at`
4. Sends appropriate email based on day count
5. Tracks which emails have been sent

**Pros:**
- Simple scheduling
- Direct control

**Cons:**
- Need to track email state per subscriber
- More code to maintain
- No campaign UI

---

### Option C: Step Functions State Machine 🔧 OVERKILL
Use AWS Step Functions to orchestrate email sequence with wait states.

**Pros:**
- Visual workflow
- Built-in retry logic

**Cons:**
- Expensive for high volume
- Complex setup
- Overkill for this use case

---

## RECOMMENDED: Option A Implementation

### Phase 1: Enhance Multi-Tenant System for Drip Campaigns

#### 1. Add Campaign Type Field
Update `user-email-campaigns` table to support:
```json
{
  "campaign_type": "one-time" | "drip",
  "drip_config": {
    "emails": [
      {
        "sequence_number": 1,
        "delay_days": 1,
        "subject": "Why I Wrote This Book",
        "body_html": "...",
        "body_text": "..."
      },
      {
        "sequence_number": 2,
        "delay_days": 2,
        "subject": "The Two Paths of AI",
        "body_html": "...",
        "body_text": "..."
      }
      // ... etc
    ]
  }
}
```

#### 2. Add Subscriber Enrollment Tracking
Create new table: `user-email-drip-enrollments`
```json
{
  "user_id": "effa3242-cf64-4021-b2b0-c8a5a9dfd6d2",
  "subscriber_email": "user@example.com",
  "campaign_id": "book-welcome-sequence",
  "enrolled_at": "2026-03-19T12:00:00Z",
  "current_sequence": 2,
  "last_sent_at": "2026-03-20T09:00:00Z",
  "status": "active" | "completed" | "paused"
}
```

#### 3. Create Drip Campaign Processor Lambda
New Lambda: `email-drip-processor`
- Triggered by EventBridge (daily at 9am)
- Queries active drip enrollments
- Calculates which emails to send based on `enrolled_at` + `delay_days`
- Sends via SQS to existing `email-sender` Lambda
- Updates enrollment status

#### 4. Auto-Enroll New Subscribers
Update `email-subscription-handler` bridge function:
```python
def bridge_to_email_marketing(email, first_name, last_name, source):
    # ... existing code ...
    
    # Auto-enroll in book welcome sequence
    try:
        drip_enrollments_table.put_item(Item={
            'user_id': PLATFORM_OWNER_ID,
            'subscriber_email': email,
            'campaign_id': 'book-welcome-sequence',
            'enrolled_at': datetime.now().isoformat(),
            'current_sequence': 0,
            'status': 'active'
        })
    except Exception as e:
        print(f'Drip enrollment error: {str(e)}')
```

---

## SIMPLER ALTERNATIVE: Mailchimp/ConvertKit Integration

If you want to avoid building drip logic, you could:

1. **Export book subscribers to Mailchimp/ConvertKit**
2. **Set up automation there** (they have built-in drip sequences)
3. **Sync new subscribers via webhook**

**Pros:**
- No code needed
- Professional email templates
- Built-in analytics
- A/B testing

**Cons:**
- Monthly cost ($20-50/month)
- External dependency
- Less control

---

## QUICKEST SOLUTION: Manual Campaign Creation

For immediate launch:

1. **Create 7 separate campaigns** in your multi-tenant system
2. **Manually schedule each one** for specific dates
3. **Segment by `subscribed_at` date** using tags
4. **Send to appropriate cohorts**

Example:
- Campaign 1: "Day 1 - Why I Wrote This" → Send to subscribers from yesterday
- Campaign 2: "Day 3 - Two Paths" → Send to subscribers from 3 days ago
- etc.

**Pros:**
- Works with existing system
- No new code
- Can start today

**Cons:**
- Manual work
- Not truly automated
- Requires daily management

---

## My Recommendation

**Start with the QUICKEST SOLUTION** to get revenue flowing, then **build Option A** for long-term automation.

### Immediate (This Week):
1. Create 7 campaigns in multi-tenant system with email content
2. Manually send to appropriate subscriber cohorts
3. Track results

### Long-term (Next 2 weeks):
1. Add drip campaign support to multi-tenant system
2. Create `email-drip-processor` Lambda
3. Auto-enroll new subscribers
4. Migrate existing subscribers to drip sequence

---

## Next Steps

Which approach do you want to take?

**A)** Build full drip automation in multi-tenant system (2-3 days work)
**B)** Use Mailchimp/ConvertKit integration (1 day setup)
**C)** Manual campaign management (start today)

Let me know and I'll implement it!
