# Email Subscribers Breakdown

## Total: 21 Unique Email Addresses

### Source Analysis:

## 1. BOOK SUBSCRIBERS (user-email-subscribers table)
**Purpose**: People who signed up for FREE book "Christian Survival Kit"
**Source**: book_landing_page
**Enrolled in**: 6-email drip campaign (Days 1, 3, 5, 7, 10, 14)

**Real Book Subscribers (3)**:
1. ✅ hawaiianintucson@gmail.com - Edward Fong (you)
2. ✅ juliahinojos@protonmail.com - Julia Fong (real subscriber)
3. ✅ waianaeboy702@aol.com - Edward Fong (your AOL email)

**Test Entries (4)**:
- test-drip-$(get-date...)@example.com
- test-drip-20260319144031@example.com
- test-drip-20260319144326@example.com
- test-final-20260319144845@example.com

---

## 2. EMAIL ANALYTICS SUBSCRIBERS (email-subscriber-stats table)
**Purpose**: Tracks ALL email activity across ALL campaigns
**Source**: ANY email sent through SES
**Includes**: Welcome emails, confirmation emails, book emails, test emails

### Breakdown by Source:

#### A. WEBSITE EMAIL SUBSCRIPTIONS (subscribed via website forms)
These people subscribed through your website email signup forms:

1. ✅ **hawaiiantucson@gmail.com** - Subscribed 10/24/2025 (typo variant of your email)
2. ✅ **hawaiiainintucson@gmail.com** - Subscribed 10/24/2025 (typo variant)
3. ✅ **contact@ekewaka.com** - Subscribed 10/24/2025 (your business email)
4. ✅ **efong505@nmsu.edu** - Subscribed 10/24/2025 (your NMSU email)
5. ✅ **test@example.com** - Subscribed 10/23/2025 (test)
6. ✅ **hawaiianintucson@gmail.com** - Subscribed 10/24/2025 (your main test email)

**Campaign**: welcome-email (sent after subscribing to general email list)

#### B. EMAIL CONFIRMATIONS (confirmed their email subscription)
These people clicked the confirmation link in their email:

7. ✅ **edward.fong@teksynap.com** - Confirmed 10/27/2025 (your work email)
8. ✅ **dkechols77@gmail.com** - Confirmed 3/16/2026 ⭐ REAL SUBSCRIBER
9. ✅ **davidoliver01@yahoo.com** - Confirmed 3/6/2026 ⭐ REAL SUBSCRIBER
10. ✅ **efong505@protonmail.com** - Confirmed 1/20/2026 (your ProtonMail)
11. ✅ **bobnglendagill@gmail.com** - Confirmed 3/3/2026 ⭐ REAL SUBSCRIBER
12. ✅ **contact@christianconservativestoday.com** - Confirmed 1/20/2026 (your site email)
13. ✅ **hitormissatthepottery@gmail.com** - Confirmed 3/3/2026 ⭐ REAL SUBSCRIBER
14. ✅ **ekewakafong@gmail.com** - Confirmed 10/24/2025 (your personal email)
15. ✅ **edward.fong@tekysnap.com** - Confirmed 10/27/2025 (typo of teksynap)

**Campaign**: confirmation-email → welcome-email (double opt-in flow)

#### C. PENDING CONFIRMATIONS (haven't confirmed yet)
These people subscribed but haven't clicked the confirmation link:

16. ⏳ **fall1776@aol.com** - Pending since 3/17/2026 ⭐ REAL SUBSCRIBER
17. ⏳ **reedandjuliesmom@gmail.com** - Pending since 2/15/2026 ⭐ REAL SUBSCRIBER
18. ⏳ **waianaeboy702@aol.com** - Pending since 1/18/2026 (your AOL - also in book list)

#### D. EMAIL ENGAGEMENT (opened/clicked emails)
These people engaged with emails but may not be in subscriber lists:

19. ✅ **hawaiianintuscon@gmail.com** - Opened emails (typo variant)
20. ✅ **hawaiiantintucson@gmail.com** - Opened emails (typo variant)
21. ✅ **doake@msn.com** - Email activity ⭐ REAL SUBSCRIBER

---

## SUMMARY:

### Real Subscribers (Non-You): 7-10 people
1. juliahinojos@protonmail.com (book subscriber)
2. dkechols77@gmail.com (confirmed)
3. davidoliver01@yahoo.com (confirmed)
4. bobnglendagill@gmail.com (confirmed)
5. hitormissatthepottery@gmail.com (confirmed)
6. fall1776@aol.com (pending)
7. reedandjuliesmom@gmail.com (pending)
8. doake@msn.com (engaged)
9. waianaeboy702@aol.com (could be you or real person)

### Your Test Emails: 10-12 variants
- hawaiianintucson@gmail.com (main)
- edward.fong@teksynap.com
- efong505@protonmail.com
- efong505@nmsu.edu
- ekewakafong@gmail.com
- contact@ekewaka.com
- contact@christianconservativestoday.com
- Plus typo variants (hawaiiantucson, hawaiiainintucson, etc.)

### Test Entries: 5
- test@example.com
- test-drip-* entries

---

## WHERE THEY SUBSCRIBED FROM:

### 1. Book Landing Page (book_landing_page)
- Signup form on your book download page
- Gets enrolled in 6-email drip campaign
- Tagged with: ["book", "survival-kit"]
- **Subscribers**: 3 real + 4 test = 7 total

### 2. Website Email Signup Forms (general subscription)
- Signup forms on your main website
- Gets welcome email
- NOT enrolled in book drip campaign
- **Subscribers**: 6 subscribed, 15 confirmed

### 3. Manual Entry (manual)
- You manually added them
- **Subscribers**: 1 (hawaiianintucson@gmail.com)

---

## KEY DIFFERENCES:

| Feature | Book Subscribers | Email Analytics |
|---------|-----------------|-----------------|
| **Table** | user-email-subscribers | email-subscriber-stats |
| **Purpose** | Book drip campaign | Track all email activity |
| **Count** | 7 (3 real + 4 test) | 21 (all email recipients) |
| **Source** | book_landing_page only | ALL sources |
| **Campaigns** | Drip sequence only | ALL campaigns |
| **Includes** | Active book readers | Everyone who got ANY email |

---

## RECOMMENDATION:

You have **TWO separate email lists**:

1. **Book List** (7 people) - Gets drip campaign
2. **General List** (14+ people) - Gets welcome/confirmation emails only

Consider:
- Merging the lists?
- Creating separate campaigns for general subscribers?
- Adding general subscribers to book drip campaign?
- Building a unified subscriber management page?
