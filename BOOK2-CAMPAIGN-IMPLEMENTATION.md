# Book 2 Campaign Implementation - Complete Guide

## 📚 Campaign Details

**Campaign Group**: `book2-launch-sequence`  
**Total Emails**: 7  
**Duration**: ~12 days  
**Target**: Christian Conservatives Today subscribers

---

## 🚀 Implementation Steps

### Step 1: Upload Campaigns to DynamoDB

```bash
# Upload emails 1-3
python upload-book2-campaign-part1.py

# Upload emails 4-7
python upload-book2-campaign-part2.py
```

**What this does:**
- Creates 7 campaign records in `user-email-campaigns` table
- Each email has unique UUID
- Proper sequence numbers (1-7)
- Correct delay timing

---

### Step 2: Verify Upload

```bash
python verify-book2-campaign.py
```

**Should show:**
- ✅ 7 campaigns found
- All with status: "active"
- Correct sequence numbers
- Proper delay_hours

---

### Step 3: Test Enrollment

**Edit the test script first:**
```bash
# Open in editor
notepad test-book2-enrollment.py

# Change line 11:
TEST_EMAIL = "your-actual-email@gmail.com"
```

**Then run:**
```bash
python test-book2-enrollment.py
```

**What this does:**
- Enrolls your test email in book2-launch-sequence
- Sets current_step = 1
- Sets next_send_date = now (immediate)
- Status = active

---

### Step 4: Send Test Email

```bash
python trigger-book2-test-email.py
```

**Or use Campaign Manager:**
1. Open `campaign-manager.html` in browser
2. Click "Enrollments" tab
3. Search for your test email
4. Click "⚡ Send Next Now"

---

### Step 5: Verify Email Delivery

**Check your inbox for:**
- **From**: Christian Conservatives Today
- **Subject**: "AI is here — but who is directing it?"

**Test these:**
- [ ] Email arrives
- [ ] Layout looks good (desktop)
- [ ] Layout looks good (mobile)
- [ ] Amazon link works
- [ ] Lulu link works
- [ ] Book page link works
- [ ] Unsubscribe link works
- [ ] Images display (if added)

---

### Step 6: Monitor in Analytics

Open `advanced-email-analytics.html`:
- Go to "Recent Events" tab
- Filter by your email
- Should see:
  - `sent` event
  - `delivered` event
  - `opened` event (after you open email)
  - `clicked` event (after you click links)

---

## 📧 Email Sequence Summary

| # | Subject | Delay | Purpose |
|---|---------|-------|---------|
| 1 | AI is here — but who is directing it? | 0 hrs | Announce book, introduce framework |
| 2 | Prompting is not magic wording | 24 hrs | Teach core concept: direction |
| 3 | AI should be assistance, not authority | 48 hrs | Connect to worldview |
| 4 | The free AI Direction Workbook is live | 48 hrs | Offer free resource |
| 5 | Polished does not mean true | 72 hrs | Teach verification |
| 6 | From warning to practical response | 48 hrs | Bridge Book 1 & 2 |
| 7 | Final reminder | 72 hrs | Last CTA + review request |

**Total timeline**: 12 days from enrollment

---

## 🖼️ Optional: Add Images

See `BOOK2-IMAGE-GENERATION-GUIDE.md` for:
- Image generation prompts for ChatGPT/DALL-E
- Where to place images in HTML
- Upload instructions to S3

**4 images needed:**
1. `book2-hero-desk.jpg` - Hero shot of book on desk
2. `book2-framework-mockup.jpg` - Book with framework diagram
3. `book2-reading-corner.jpg` - Cozy reading scene
4. `book2-with-workbook.jpg` - Book with workbook pages

---

## 📊 Launch Checklist

### Pre-Launch
- [ ] All 7 campaigns uploaded
- [ ] Verification script shows 7 active campaigns
- [ ] Test enrollment created
- [ ] Test email sent to yourself
- [ ] Email received and tested
- [ ] All links work
- [ ] Mobile layout tested
- [ ] Desktop layout tested

### Soft Launch (Recommended)
- [ ] Enroll 10-20 engaged subscribers first
- [ ] Monitor for 24-48 hours
- [ ] Check open rates
- [ ] Check click rates
- [ ] Watch for unsubscribes
- [ ] Fix any issues before wider launch

### Full Launch
- [ ] Segment: Book 1 readers
- [ ] Segment: AI/tech interested subscribers
- [ ] Segment: Active engagers
- [ ] Monitor daily for first week
- [ ] Adjust if needed

---

## 🔧 Troubleshooting

### Campaign not found
```bash
python verify-book2-campaign.py
# If shows 0 campaigns, run upload scripts
```

### Test email not sending
```bash
# Check enrollment exists
python test-book2-enrollment.py

# Manually trigger
python trigger-book2-test-email.py
```

### Email sent but not received
1. Check spam folder
2. Check SES suppression list:
   ```bash
   aws sesv2 get-suppressed-destination --email-address YOUR_EMAIL --region us-east-1 --profile ekewaka
   ```
3. Check CloudWatch logs: `/aws/lambda/email-sender`

### Wrong email content
- Update campaign in DynamoDB
- Or delete and re-upload
- New subscribers get updated version

---

## 📈 Success Metrics to Track

**Email Performance:**
- Open rate goal: >20%
- Click rate goal: >5%
- Unsubscribe rate: <0.5%

**Conversion Metrics:**
- Amazon link clicks
- Lulu link clicks
- Workbook downloads
- Book page visits

**Monitor in:**
- `advanced-email-analytics.html`
- `campaign-manager.html` → Enrollments tab
- AWS CloudWatch

---

## 🎯 Post-Launch Actions

**Week 1:**
- Monitor daily sends
- Check for bounces
- Watch click-through rates
- Adjust timing if needed

**Week 2:**
- Analyze completion rates (how many finish all 7 emails)
- Check conversion rates
- Gather feedback
- Plan improvements

**Ongoing:**
- A/B test subject lines
- Test different CTAs
- Optimize images
- Refine copy based on performance

---

## 📝 Files Created

### Upload Scripts
- `upload-book2-campaign-part1.py` - Emails 1-3
- `upload-book2-campaign-part2.py` - Emails 4-7

### Testing Scripts
- `verify-book2-campaign.py` - Check uploads
- `test-book2-enrollment.py` - Create test enrollment
- `trigger-book2-test-email.py` - Send test email

### Documentation
- `CHATGPT-CAMPAIGN-HANDOFF.md` - System architecture
- `BOOK2-IMAGE-GENERATION-GUIDE.md` - Image prompts
- `BOOK2-CAMPAIGN-IMPLEMENTATION.md` - This file

---

## 🚨 Important Notes

1. **Always test first** - Use your own email before enrolling others
2. **Check links** - All 7 emails have Amazon, Lulu, workbook links
3. **Monitor SES reputation** - Keep bounce rate <5%, complaint rate <0.1%
4. **Segment carefully** - Don't blast entire list at once
5. **Respect unsubscribes** - System handles automatically

---

## 🎉 Ready to Launch!

Once testing is complete:

```python
# Create production enrollments
# Manually enroll specific subscribers OR
# Create enrollment automation for new signups
```

Good luck with Book 2 launch! 🚀📚
