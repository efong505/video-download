"""
Create 7-email book welcome sequence campaigns
Run: python create_book_campaigns.py
"""
import boto3
import uuid
from datetime import datetime

# Use ekewaka profile
session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
campaigns_table = dynamodb.Table('user-email-campaigns')

# Ed's user_id
USER_ID = 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'

# Email campaigns from email-campaign.md
campaigns = [
    {
        'sequence_number': 1,
        'delay_days': 1,
        'title': 'Day 1 - Why I Wrote This Book',
        'subject': 'Why I wrote The Necessary Evil',
        'content_html': '''<p>Hey,</p>

<p>I didn't set out to write a book about AI.</p>

<p>I set out to build something.</p>

<p>And AI helped me do it faster than I thought possible.</p>

<p>But the deeper I went…</p>

<p>…the more I saw something most people are missing.</p>

<p>AI isn't just changing:</p>

<ul>
<li>jobs</li>
<li>productivity</li>
<li>technology</li>
</ul>

<p>It's changing how we:</p>

<ul>
<li>think</li>
<li>reason</li>
<li>relate</li>
<li>understand truth</li>
</ul>

<p>And here's the part that concerned me most:</p>

<p><strong>Most Christians aren't prepared.</strong></p>

<p>Not because they're not intelligent…</p>

<p>…but because no one is explaining this from a biblical perspective.</p>

<p>So I wrote the book I wish existed:</p>

<p>👉 <a href="https://christianconservativestoday.com/the-necessary-evil-book.html">The Necessary Evil</a></p>

<p>A guide for Christians to understand:</p>

<ul>
<li>the power of AI</li>
<li>the risks of AI</li>
<li>and how to navigate both without compromise</li>
</ul>

<p>This isn't fear-based.</p>

<p>It's clarity-based.</p>

<p>Because ignoring AI isn't an option anymore.</p>

<p>Talk soon,<br>
Edward</p>''',
        'content_text': '''Hey,

I didn't set out to write a book about AI.

I set out to build something.

And AI helped me do it faster than I thought possible.

But the deeper I went…

…the more I saw something most people are missing.

AI isn't just changing:

• jobs
• productivity
• technology

It's changing how we:

• think
• reason
• relate
• understand truth

And here's the part that concerned me most:

Most Christians aren't prepared.

Not because they're not intelligent…

…but because no one is explaining this from a biblical perspective.

So I wrote the book I wish existed:

👉 The Necessary Evil
https://christianconservativestoday.com/the-necessary-evil-book.html

A guide for Christians to understand:

• the power of AI
• the risks of AI
• and how to navigate both without compromise

This isn't fear-based.

It's clarity-based.

Because ignoring AI isn't an option anymore.

Talk soon,
Edward'''
    },
    {
        'sequence_number': 2,
        'delay_days': 2,
        'title': 'Day 3 - The Two Paths of AI',
        'subject': 'The two paths of AI (and which one we are on)',
        'content_html': '''<p>Hey,</p>

<p>We are standing at a crossroads.</p>

<p>And there are only two paths forward with AI.</p>

<hr>

<h3>Path 1: AI as a TOOL</h3>

<p>AI helps us:</p>

<ul>
<li>work faster</li>
<li>create more</li>
<li>focus on what matters</li>
<li>serve others better</li>
</ul>

<p>This is AI under <strong>human and spiritual authority</strong>.</p>

<hr>

<h3>Path 2: AI as a REPLACEMENT</h3>

<p>AI begins to:</p>

<ul>
<li>think for us</li>
<li>decide for us</li>
<li>speak for us</li>
<li>replace human roles entirely</li>
</ul>

<p>This is where things get dangerous.</p>

<hr>

<p>The question is not:</p>

<p><strong>"Will AI change everything?"</strong></p>

<p>It will.</p>

<p>The real question is:</p>

<p>👉 <strong>Who is in control?</strong></p>

<p>That's the central message of <em>The Necessary Evil</em>.</p>

<p>Not fear.</p>

<p>Not hype.</p>

<p>But a clear warning:</p>

<p><strong>We must master AI—or be mastered by it.</strong></p>

<p>If you haven't yet, you can explore the book here:</p>

<p>👉 <a href="https://christianconservativestoday.com/the-necessary-evil-book.html">View the book</a></p>

<p>Talk soon,<br>
Edward</p>''',
        'content_text': '''Hey,

We are standing at a crossroads.

And there are only two paths forward with AI.

---

Path 1: AI as a TOOL

AI helps us:

• work faster
• create more
• focus on what matters
• serve others better

This is AI under human and spiritual authority.

---

Path 2: AI as a REPLACEMENT

AI begins to:

• think for us
• decide for us
• speak for us
• replace human roles entirely

This is where things get dangerous.

---

The question is not:

"Will AI change everything?"

It will.

The real question is:

👉 Who is in control?

That's the central message of The Necessary Evil.

Not fear.

Not hype.

But a clear warning:

We must master AI—or be mastered by it.

If you haven't yet, you can explore the book here:

👉 https://christianconservativestoday.com/the-necessary-evil-book.html

Talk soon,
Edward'''
    },
    {
        'sequence_number': 3,
        'delay_days': 2,
        'title': 'Day 5 - Personal Impact (Family/Church/Career)',
        'subject': 'How AI is already affecting your family',
        'content_html': '''<p>Hey,</p>

<p>Let's bring this closer to home.</p>

<p>Because AI isn't just a "future issue."</p>

<p>It's already impacting:</p>

<hr>

<h3>Your Career</h3>

<p>Jobs are shifting.</p>

<p>Skills are changing.</p>

<p>Those who use AI effectively will accelerate.</p>

<p>Those who don't… risk falling behind.</p>

<hr>

<h3>Your Family</h3>

<p>Children are growing up with:</p>

<ul>
<li>AI companions</li>
<li>AI-generated content</li>
<li>AI-influenced thinking</li>
</ul>

<p>And most parents aren't prepared.</p>

<hr>

<h3>Your Church</h3>

<p>Many churches are:</p>

<ul>
<li>silent</li>
<li>unaware</li>
<li>unprepared</li>
</ul>

<p>Meanwhile, culture is being shaped rapidly.</p>

<hr>

<p>This is not about panic.</p>

<p>It's about <strong>preparation</strong>.</p>

<p>That's why this book doesn't just explain AI—</p>

<p>It gives <strong>practical strategies</strong> for:</p>

<ul>
<li>individuals</li>
<li>families</li>
<li>churches</li>
</ul>

<p>👉 <a href="https://christianconservativestoday.com/the-necessary-evil-book.html">Explore the book here</a></p>

<p>Talk soon,<br>
Edward</p>''',
        'content_text': '''Hey,

Let's bring this closer to home.

Because AI isn't just a "future issue."

It's already impacting:

---

Your Career

Jobs are shifting.

Skills are changing.

Those who use AI effectively will accelerate.

Those who don't… risk falling behind.

---

Your Family

Children are growing up with:

• AI companions
• AI-generated content
• AI-influenced thinking

And most parents aren't prepared.

---

Your Church

Many churches are:

• silent
• unaware
• unprepared

Meanwhile, culture is being shaped rapidly.

---

This is not about panic.

It's about preparation.

That's why this book doesn't just explain AI—

It gives practical strategies for:

• individuals
• families
• churches

👉 https://christianconservativestoday.com/the-necessary-evil-book.html

Talk soon,
Edward'''
    },
    {
        'sequence_number': 4,
        'delay_days': 2,
        'title': 'Day 7 - Testimonials + Buy',
        'subject': 'What readers are saying about The Necessary Evil',
        'content_html': '''<p>Hey,</p>

<p>I wanted to share something with you.</p>

<p>Here's what someone said after reading <em>The Necessary Evil</em>:</p>

<hr>

<blockquote>
<p>"This completely changed how I think about AI—not just as a tool, but as something that could reshape how we live, think, and believe."</p>
</blockquote>

<hr>

<p>That's exactly why I wrote it.</p>

<p>Because most people are only seeing:</p>

<p>👉 the convenience</p>

<p>But not:</p>

<p>👉 the consequences</p>

<p>This book connects the dots between:</p>

<ul>
<li>technology</li>
<li>culture</li>
<li>faith</li>
<li>and human identity</li>
</ul>

<p>If you've been thinking about it, this is a great time to grab your copy:</p>

<p>👉 <a href="https://christianconservativestoday.com/the-necessary-evil-book.html#purchase">Get the book</a></p>

<p>Talk soon,<br>
Edward</p>''',
        'content_text': '''Hey,

I wanted to share something with you.

Here's what someone said after reading The Necessary Evil:

---

"This completely changed how I think about AI—not just as a tool, but as something that could reshape how we live, think, and believe."

---

That's exactly why I wrote it.

Because most people are only seeing:

👉 the convenience

But not:

👉 the consequences

This book connects the dots between:

• technology
• culture
• faith
• and human identity

If you've been thinking about it, this is a great time to grab your copy:

👉 https://christianconservativestoday.com/the-necessary-evil-book.html#purchase

Talk soon,
Edward'''
    },
    {
        'sequence_number': 5,
        'delay_days': 3,
        'title': 'Day 10 - Objection Handling',
        'subject': 'Is this book anti-AI?',
        'content_html': '''<p>Hey,</p>

<p>Let me answer a question I get a lot:</p>

<p><strong>"Is this book anti-AI?"</strong></p>

<p>Short answer:</p>

<p>👉 No.</p>

<p>This isn't about rejecting technology.</p>

<p>In fact—</p>

<p>I actively use AI.</p>

<p>It helped me build faster than ever before.</p>

<hr>

<p>But here's the difference:</p>

<p>I don't trust it blindly.</p>

<p>And I don't let it replace:</p>

<ul>
<li>thinking</li>
<li>discernment</li>
<li>faith</li>
</ul>

<hr>

<p>This book is about balance:</p>

<p>✔ Using AI wisely<br>
✔ Understanding its risks<br>
✔ Staying grounded in truth</p>

<p>Because the real danger isn't AI itself.</p>

<p>It's <strong>unquestioned reliance on it.</strong></p>

<p>If that resonates with you, you'll get a lot out of this:</p>

<p>👉 <a href="https://christianconservativestoday.com/the-necessary-evil-book.html">View the book</a></p>

<p>Talk soon,<br>
Edward</p>''',
        'content_text': '''Hey,

Let me answer a question I get a lot:

"Is this book anti-AI?"

Short answer:

👉 No.

This isn't about rejecting technology.

In fact—

I actively use AI.

It helped me build faster than ever before.

---

But here's the difference:

I don't trust it blindly.

And I don't let it replace:

• thinking
• discernment
• faith

---

This book is about balance:

✔ Using AI wisely
✔ Understanding its risks
✔ Staying grounded in truth

Because the real danger isn't AI itself.

It's unquestioned reliance on it.

If that resonates with you, you'll get a lot out of this:

👉 https://christianconservativestoday.com/the-necessary-evil-book.html

Talk soon,
Edward'''
    },
    {
        'sequence_number': 6,
        'delay_days': 4,
        'title': 'Day 14 - Urgency + Offer',
        'subject': 'Limited time: Signed copies + bonus webinar',
        'content_html': '''<p>Hey,</p>

<p>I wanted to give you a quick heads up.</p>

<p>For a limited time, I'm offering:</p>

<p>🎁 Signed copies of <em>The Necessary Evil</em><br>
🎁 Bonus access to an upcoming live Q&A<br>
🎁 Additional study resources</p>

<p>But this won't be available much longer.</p>

<hr>

<p>If you've been on the fence…</p>

<p>This is the best time to get it.</p>

<p>👉 <a href="https://christianconservativestoday.com/the-necessary-evil-book.html#purchase">Get your copy here</a></p>

<hr>

<p>We are entering a time where:</p>

<p>AI will shape culture.</p>

<p>The question is:</p>

<p>👉 Will we shape it back?</p>

<p>Appreciate you being here,<br>
Edward</p>''',
        'content_text': '''Hey,

I wanted to give you a quick heads up.

For a limited time, I'm offering:

🎁 Signed copies of The Necessary Evil
🎁 Bonus access to an upcoming live Q&A
🎁 Additional study resources

But this won't be available much longer.

---

If you've been on the fence…

This is the best time to get it.

👉 https://christianconservativestoday.com/the-necessary-evil-book.html#purchase

---

We are entering a time where:

AI will shape culture.

The question is:

👉 Will we shape it back?

Appreciate you being here,
Edward'''
    }
]

print("Creating 7 book welcome sequence campaigns...")
print(f"User ID: {USER_ID}\n")

for campaign in campaigns:
    campaign_id = str(uuid.uuid4())
    
    item = {
        'user_id': USER_ID,
        'campaign_id': campaign_id,
        'title': campaign['title'],
        'subject': campaign['subject'],
        'content': campaign['content_html'],
        'content_text': campaign['content_text'],
        'template_id': '',
        'filter_tags': ['book', 'survival-kit'],
        'status': 'draft',
        'created_at': datetime.now().isoformat(),
        'recipient_count': 0,
        'open_count': 0,
        'click_count': 0,
        # Drip campaign fields
        'campaign_type': 'drip',
        'sequence_number': campaign['sequence_number'],
        'delay_days': campaign['delay_days']
    }
    
    campaigns_table.put_item(Item=item)
    
    print(f"[OK] Created: {campaign['title']}")
    print(f"  Campaign ID: {campaign_id}")
    print(f"  Sequence: {campaign['sequence_number']} | Delay: {campaign['delay_days']} days")
    print()

print("\n[SUCCESS] All 7 campaigns created successfully!")
print("\nNext steps:")
print("1. Review campaigns in user-email-dashboard.html")
print("2. Deploy drip automation Lambda")
print("3. Test with a subscriber")
