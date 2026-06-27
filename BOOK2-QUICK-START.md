# Book 2 Campaign - Quick Start

## 🚀 Run These Commands in Order

### 1. Upload Campaigns (2 minutes)
```bash
cd c:\Users\Ed\Documents\Programming\AWS\Downloader

python upload-book2-campaign-part1.py
python upload-book2-campaign-part2.py
```

**Expected output**: "✅ Part 1 Complete" then "✅ Part 2 Complete"

---

### 2. Verify Upload (30 seconds)
```bash
python verify-book2-campaign.py
```

**Expected output**: "🎉 ALL 7 EMAILS ARE UPLOADED!"

---

### 3. Edit Test Script (1 minute)
```bash
notepad test-book2-enrollment.py
```

**Change line 11 to YOUR email:**
```python
TEST_EMAIL = "youremail@gmail.com"  # Change this!
```

Save and close.

---

### 4. Create Test Enrollment (30 seconds)
```bash
python test-book2-enrollment.py
```

**Expected output**: "✅ TEST ENROLLMENT CREATED!"

---

### 5. Send Test Email (1 minute)
```bash
python trigger-book2-test-email.py
```

**Expected output**: "✅ Email sent successfully!"

---

### 6. Check Your Inbox (2 minutes)

Look for:
- **From**: Christian Conservatives Today
- **Subject**: "AI is here — but who is directing it?"

**Test:**
- Click Amazon link → should go to book
- Click Lulu link → should go to book
- Click "View the Book" → should go to necessaryevilbooks.com
- Unsubscribe link → should work

---

## ✅ You're Done!

**Campaign is live and tested.**

### Next Steps:
1. Monitor in `advanced-email-analytics.html`
2. Enroll real subscribers when ready
3. Watch performance metrics

---

## 📊 Where to Monitor

**Campaign Manager**: `campaign-manager.html`
- Enrollments tab → see who's enrolled
- Send Next Now → manual trigger
- View analytics per campaign

**Advanced Analytics**: `advanced-email-analytics.html`
- Recent Events → see opens, clicks
- Campaigns → performance by email
- Subscribers → engagement by person

---

## 🆘 If Something Goes Wrong

**No emails found?**
```bash
python verify-book2-campaign.py
# Shows what's uploaded
```

**Test email didn't arrive?**
1. Check spam folder
2. Run: `python trigger-book2-test-email.py` again
3. Check CloudWatch: /aws/lambda/email-sender

**Wrong content?**
- Delete campaign from DynamoDB
- Re-run upload script

---

## 📝 Full Documentation

See `BOOK2-CAMPAIGN-IMPLEMENTATION.md` for complete guide.

---

**That's it! You're ready to launch Book 2! 🚀📚**
