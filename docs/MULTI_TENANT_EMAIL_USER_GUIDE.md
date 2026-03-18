# Multi-Tenant Email Marketing - User Guide

## Getting Started

### What is Multi-Tenant Email Marketing?
Each user on Christian Conservatives Today can now manage their own email subscriber lists and send campaigns to their congregation or audience - all from within the platform.

### Why Use This Feature?
- **Save Money**: Mailchimp charges $100-300/month. Our PRO plan is $49.99/month with video hosting included
- **All-in-One**: Manage videos, articles, and email campaigns in one place
- **No Technical Skills**: Easy-to-use interface, no coding required
- **Track Results**: See who opens your emails and clicks your links

---

## Pricing & Quotas

### FREE Plan - $0/month
- ❌ No email marketing feature

### PREMIUM Plan - $19.99/month
- ✅ 500 email subscribers
- ✅ 1,000 emails per month
- ✅ 25GB video storage
- ✅ 500 videos

### PRO Plan - $49.99/month ⭐ BEST VALUE
- ✅ 5,000 email subscribers
- ✅ 10,000 emails per month
- ✅ 100GB video storage
- ✅ 2,000 videos

### ENTERPRISE Plan - $149.99/month
- ✅ Unlimited email subscribers
- ✅ 50,000 emails per month
- ✅ Unlimited video storage
- ✅ Unlimited videos

---

## Step-by-Step Guide

### Step 1: Access Email Dashboard
1. Login to your account
2. Navigate to: https://christianconservativestoday.com/user-email-dashboard.html
3. You'll see your quota usage and recent campaigns

### Step 2: Add Subscribers
1. Click "Manage Subscribers"
2. Click "➕ Add Subscriber"
3. Fill in:
   - Email (required)
   - First Name (required)
   - Last Name (optional)
   - Phone (optional)
4. Click "Add"

**Tip**: You can add subscribers one at a time. CSV import coming in future update.

### Step 3: Create Your First Campaign
1. From dashboard, click "📝 Create Campaign"
2. Enter campaign details:
   - **Campaign Title**: Internal name (e.g., "Weekly Newsletter #1")
   - **Email Subject**: What subscribers see (e.g., "This Week's Updates")
   - **Email Content**: Use the rich text editor to format your message

### Step 4: Personalize with Mail Merge
Add these special tags to personalize emails:
- `{{first_name}}` - Subscriber's first name
- `{{last_name}}` - Subscriber's last name
- `{{email}}` - Subscriber's email address
- `{{unsubscribe_link}}` - Required unsubscribe link

**Example**:
```
Hello {{first_name}},

Thank you for subscribing to our newsletter!

Best regards,
Pastor John

Unsubscribe: {{unsubscribe_link}}
```

**Result**:
```
Hello Sarah,

Thank you for subscribing to our newsletter!

Best regards,
Pastor John

Unsubscribe: [link]
```

### Step 5: Send Your Campaign
1. Click "💾 Save Draft" to save without sending
2. Click "📧 Send Now" to send immediately
3. Confirm you want to send to all active subscribers
4. Campaign will be queued and sent within minutes

---

## Best Practices

### Email Content Tips
1. **Keep it Short**: 200-500 words is ideal
2. **Clear Subject**: Tell them what's inside
3. **Call to Action**: What do you want them to do?
4. **Mobile-Friendly**: Most people read on phones
5. **Always Include Unsubscribe**: Required by law

### Sending Frequency
- **Weekly**: Good for newsletters
- **Monthly**: Good for updates
- **Special Events**: Announcements, holidays
- **Don't Spam**: More than 2x/week = unsubscribes

### Growing Your List
1. **Website Signup Form**: Add to your church website
2. **Sunday Announcements**: "Text your email to..."
3. **Events**: Collect emails at church events
4. **Social Media**: Promote your newsletter
5. **Word of Mouth**: Ask members to share

---

## Understanding Your Quota

### Subscriber Limit
- **What it means**: Total number of people on your list
- **When it resets**: Never (it's a total count)
- **What happens at limit**: Can't add more until you upgrade or delete subscribers

### Monthly Email Limit
- **What it means**: Total emails sent this month
- **When it resets**: 1st of each month at midnight UTC
- **What happens at limit**: Can't send more campaigns until next month or upgrade

**Example**:
- PRO Plan: 5,000 subscribers, 10,000 emails/month
- If you send 1 campaign to all 5,000 subscribers = 5,000 emails used
- You can send 2 campaigns per month to your full list

---

## Tracking & Analytics

### What We Track
1. **Emails Sent**: How many emails delivered
2. **Opens**: How many people opened your email
3. **Clicks**: How many clicked links (coming soon)
4. **Unsubscribes**: Who opted out

### How to View Stats
1. Go to Email Dashboard
2. See campaign list with stats
3. Click campaign for detailed analytics (coming soon)

---

## Troubleshooting

### "Subscriber limit reached"
**Solution**: Upgrade your plan or delete inactive subscribers

### "Monthly email limit reached"
**Solution**: Wait until next month or upgrade your plan

### "Email not delivered"
**Possible Causes**:
1. Invalid email address
2. Subscriber's inbox full
3. Email marked as spam
4. Subscriber unsubscribed

### "Campaign stuck in 'sending' status"
**Solution**: Wait 5-10 minutes. Large lists take time. If still stuck after 30 minutes, contact support.

---

## Frequently Asked Questions

### Can I import subscribers from Mailchimp?
Not yet. CSV import coming in Q3 2025. For now, add manually or use API.

### Can I schedule campaigns for later?
Not yet. Scheduling coming in Q3 2025. For now, send immediately.

### Can I use my own email domain?
Not yet. All emails send from contact@christianconservativestoday.com with your email as Reply-To. Custom domains coming in Q4 2025.

### What happens if I downgrade my plan?
You keep your subscribers but can't send campaigns until you're under the new limit.

### Can I export my subscriber list?
Yes, via API. CSV export coming in Q3 2025.

### Is there a mobile app?
Not yet. Mobile app coming in Q4 2025. For now, use mobile browser.

---

## Compliance & Legal

### CAN-SPAM Act Requirements
We automatically include:
- ✅ Unsubscribe link in every email
- ✅ Physical address in footer (our address)
- ✅ Accurate "From" information

**Your Responsibility**:
- ❌ Don't buy email lists
- ❌ Don't add people without permission
- ❌ Don't use misleading subject lines
- ❌ Don't send after they unsubscribe

### GDPR Compliance (EU subscribers)
- Get explicit consent before adding
- Honor unsubscribe requests immediately
- Provide data export on request
- Delete data when requested

---

## Getting Help

### Support Resources
1. **Documentation**: docs/MULTI_TENANT_EMAIL_SYSTEM_DESIGN.md
2. **Testing Guide**: docs/MULTI_TENANT_EMAIL_TESTING_GUIDE.md
3. **Email**: contact@christianconservativestoday.com
4. **Video Tutorials**: Coming soon

### Common Issues
- Check CloudWatch logs for errors
- Verify your quota hasn't been exceeded
- Ensure subscribers have valid email addresses
- Check spam folder if emails not received

---

## Upgrade Your Plan

### Ready for More Subscribers?
Visit: https://christianconservativestoday.com/pricing

### Compare Plans
| Feature | Premium | PRO | Enterprise |
|---------|---------|-----|------------|
| Price | $19.99/mo | $49.99/mo | $149.99/mo |
| Subscribers | 500 | 5,000 | Unlimited |
| Emails/Month | 1,000 | 10,000 | 50,000 |
| Video Storage | 25GB | 100GB | Unlimited |

---

## What's Coming Next?

### Q3 2025
- CSV subscriber import
- Campaign scheduling
- Advanced analytics dashboard
- Email templates library

### Q4 2025
- A/B testing for subject lines
- Segmentation by tags
- Custom email domains
- Mobile app

---

**Questions?** Email us at contact@christianconservativestoday.com
