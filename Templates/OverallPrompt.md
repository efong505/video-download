# Christian Conservatives Today - Complete Project Continuation Prompt (v4.0)

I'm working on **Christian Conservatives Today**, a comprehensive AWS serverless platform combining video hosting, article publishing, nationwide election tracking (ALL 50 STATES COMPLETE), email marketing, community engagement, e-commerce shopping, and enterprise-grade architecture improvements.

## **Project Location**
`c:\Users\Ed\Documents\Programming\AWS\Downloader\`

## **Platform URL**
https://christianconservativestoday.com

---

## **PLATFORM OVERVIEW**

### **Mission**
Platform for the 5-fold ministry (apostles, prophets, evangelists, pastors, teachers), Christian believers, and conservative voices to share sermons, publish articles with Bible integration, track elections across all 50 US states, sell ministry resources, and engage communities without censorship.

### **Key Statistics**
- **Architecture**: 100% Serverless (AWS Lambda, S3, DynamoDB, CloudFront)
- **Lambda Functions**: 19+ microservices (27+ planned with shopping)
- **Database Tables**: 18+ DynamoDB tables (26+ planned with shopping)
- **Election Coverage**: ALL 50 US STATES COMPLETE (290+ races, 197+ candidates, 50 comprehensive voter guides)
- **User Roles**: 4-tier system (Super User > Admin > Editor > User)
- **Domain**: christianconservativestoday.com
- **Next Phase**: E-commerce shopping + Enterprise architecture improvements

---

## **COMPLETED SYSTEMS** (Parts 1-11)

### **PART 1: VIDEO MANAGEMENT** ✅
- Multi-platform downloads (YouTube, Rumble, Facebook)
- Auto-thumbnail generation
- Netflix-style horizontal scrolling
- Bulk editing, sorting (6 options)

### **PART 2: ARTICLE & BLOG** ✅
- Quill.js + Markdown dual-mode editor
- Bible integration (KJV, ASV, YLT)
- Full-text search, analytics
- Comment system with moderation

### **PART 3: AUTHENTICATION** ✅
- 4-tier role system
- JWT tokens (24-hour expiration)
- localStorage standardization

### **PART 4: SUBSCRIPTION & BILLING** ✅
- PayPal LIVE production mode
- 4 tiers (FREE to ENTERPRISE)
- Quota enforcement

### **PART 5: ELECTION TRACKING** ✅
- ALL 50 US STATES complete
- 290+ races, 197+ candidates
- Interactive SVG map
- Dual-mode editor for summaries
- PDF/TXT downloads

### **PART 6: EMAIL SUBSCRIPTION** ✅
- AWS SES integration
- Open/click tracking
- 95% cheaper than Mailchimp

### **PART 7: NEWSLETTER SYSTEM** ✅
- 5 professional templates
- Mail merge personalization
- Auto-digest generator
- Newsletter archive

### **PART 8: MINISTRY TOOLS** ✅
- Prayer request system
- Event calendar
- Email notifications (4 types)

### **PART 9: NEWS MANAGEMENT** ✅
- Breaking news banners
- Scheduled publishing
- State-specific coverage

### **PART 10: RESOURCE MANAGEMENT** ✅
- Emoji icons (47 categories)
- Multiple categories per resource
- AI auto-summary

### **PART 11: UI/UX** ✅
- Unified navigation (navbar.html/navbar.js)
- Horizontal scrolling UI
- CSS consolidation (23.6% reduction)
- Mobile optimization
- PWA implementation

---

## **PHASE 5: E-COMMERCE SHOPPING SYSTEM** 🛒 PLANNED

### Overview
**Timeline**: 9 weeks | **Status**: Planning complete | **Location**: `Shopping/` folder

### Implementation Phases

**Phase 1: Basic Shopping (Weeks 1-6)**
- Week 1: Database + SQS queues
- Week 2: APIs + ElastiCache caching
- Week 3: Payment (PayPal + Stripe) + Circuit breakers + Rate limiting
- Week 4: Frontend + API Gateway caching
- Week 5: Checkout + Order processing
- Week 6: Admin interface

**Phase 2: Smart Shopping (Weeks 7-8)**
- Week 7: Behavioral tracking via SQS
- Week 8: Marketing automation via SQS
- Abandoned cart recovery (10% discount)
- Browse abandonment emails (5% discount)
- Price drop alerts, back in stock notifications

**Phase 3: Testing & Launch (Week 9)**
- Load testing (100 concurrent users)
- Security audit, production launch

### Core Features

**Basic Shopping:**
- Product catalog with search/filter
- Shopping cart with quantity adjustment
- Guest checkout, PayPal + Stripe payments
- Order history, digital downloads
- Customer reviews, inventory tracking

**Smart Shopping:**
- Product view tracking
- Abandoned cart recovery emails
- Personalized recommendations
- Email preference center
- Marketing analytics dashboard

### Database Tables (8 new)
1. **Products** - Catalog with images, pricing, inventory
2. **Orders** - Order history with payment status
3. **Cart** - Shopping carts (cached in Redis)
4. **Reviews** - Product reviews and ratings
5. **ProductViews** - Behavioral tracking (90-day TTL)
6. **MarketingQueue** - Email queue (30-day TTL)
7. **EmailPreferences** - User preferences
8. **WatchList** - Price/stock alerts

### Lambda Functions (10 new)
1. **shop_api** - Product CRUD (with ElastiCache)
2. **cart_api** - Cart management (with ElastiCache)
3. **order_api** - Order processing (with SQS)
4. **payment_api** - PayPal + Stripe (with circuit breakers)
5. **order_processor** - SQS consumer
6. **payment_processor** - SQS consumer
7. **email_sender** - SQS consumer
8. **inventory_updater** - SQS consumer
9. **tracking_api** - Behavioral tracking (via SQS)
10. **marketing_automation_api** - Automated emails (via SQS)

### Product Categories
1. Books - Christian living, political commentary
2. Apparel - T-shirts, hats, hoodies
3. Resources - Voter guides, study guides
4. Digital Downloads - E-books, PDFs, courses
5. Merchandise - Mugs, stickers, posters
6. Ministry Tools - Sermon outlines, graphics

### Cost Estimates (with Architecture)
- DynamoDB: $3/month (50% reduction from caching)
- Lambda: $2.50/month (44% reduction)
- S3: $0.75/month
- SES: $1/month
- SQS: $2/month (4 queues + 4 DLQs)
- ElastiCache: $15/month (cache.t3.micro)
- API Gateway Cache: $10/month (0.5 GB)
- **Total: ~$34.25/month**

### Success Metrics
- Cart recovery rate: >10%
- Email open rate: >20%
- Email conversion rate: >2%
- ROI: 25,000%+ on marketing automation

### Documentation
- Shopping/README.md
- Shopping/SHOPPING_SYSTEM_PLAN.md
- Shopping/TRACKING_SYSTEM_SPECS.md
- Shopping/ARCHITECTURE_REQUIREMENTS.md

---

## **ARCHITECTURE IMPROVEMENTS** 🏗️ READY

### Overview
**Goal**: Transform from 7.5/10 to 9/10 enterprise-grade
**Timeline**: 4 weeks (44 hours) | **Location**: `Architecture-Improvements/` folder

### Expected Results
- ⚡ 20-40x faster (2s → 50ms)
- 💰 40% cost reduction ($1,620/year savings)
- 🛡️ 99.9% uptime (from 99.5%)
- 📈 10x scalability (1K → 10K+ users)

### Implementation Timeline

**Week 1: SQS Message Queues (12 hours)**
- 8 SQS queues for async operations
- Automatic retry logic, DLQs
- **Cost**: +$5/month | **Benefit**: Fault tolerance

**Week 2: ElastiCache Redis (16 hours)**
- Redis caching (cache.t3.micro)
- 90% cache hit rate, 80% DynamoDB reduction
- **Cost**: +$15/month (saves $100/month) | **Benefit**: 40x faster

**Week 3: Fault Tolerance (10 hours)**
- Circuit breakers for external APIs
- Rate limiting by subscription tier
- **Cost**: $0 | **Benefit**: 99.9% uptime

**Week 4: API Gateway Caching (6 hours)**
- Response caching (0.5 GB)
- 80% Lambda reduction, sub-100ms responses
- **Cost**: +$25/month (saves $80/month) | **Benefit**: Instant performance

### Architecture Components (Mandatory)

**1. SQS Message Queues**
- Queues: order-processing, payment-processing, email-notification, inventory-update
- Each with DLQ, 1-5 min visibility timeout
- **Rule**: NO direct Lambda invocations for async operations

**2. ElastiCache Redis**
- Cache product catalog (80% reads, 1hr TTL)
- Cache cart data (90% reduction, 30min TTL)
- Cache sessions (24hr TTL)
- **Expected**: 90% faster, 40% cost reduction

**3. Circuit Breakers**
- Wrap PayPal, Stripe, SES, Bible API
- Failure threshold: 5 in 1 minute
- Timeout: 30s, retry after 60s

**4. Rate Limiting**
- Payment: 10 req/min per user
- Cart: 100 req/min per user
- Admin: 50 req/min per admin
- Public: 1000 req/min total

**5. API Gateway Caching**
- Cache GET /products (5min TTL)
- Cache GET /categories (1hr TTL)
- Cache GET /featured (15min TTL)
- **Config**: 0.5 GB cache size

### Financial Summary
**Investment**: 44 hours, $50/month new services
**Returns**: $185/month savings
**Net**: $135/month savings ($1,620/year)
**ROI**: 2.7x return, immediate payback

### Performance Improvements
- Articles: 2000ms → 100ms (20x)
- Videos: 1800ms → 120ms (15x)
- Election Map: 2200ms → 80ms (27x)
- Resources: 1500ms → 90ms (16x)

### Quick Wins (5 hours, $80/month savings)
1. Enable API Gateway Caching (1 hour)
2. Deploy SQS Queues (2 hours)
3. Add Circuit Breakers (2 hours)

### Documentation (16 files)
- START-HERE.md, README.md, QUICK-START-GUIDE.md
- VISUAL-SUMMARY.md, 00-MASTER-PLAN.md
- IMPLEMENTATION-GAMEPLAN.md
- 01-SQS-IMPLEMENTATION.md through 05-API-GATEWAY-CACHING.md
- scripts/week1-deploy.ps1, week1-deploy.sh

### Rollback Strategy
All changes are additive and reversible:
- SQS: Disable queue, revert to direct calls
- ElastiCache: Remove cache layer
- API Gateway: Disable caching (1 click)
- Zero downtime deployment

---

## **AWS CONFIGURATION** ⚠️ CRITICAL

### S3 Buckets
- **Primary Video Bucket**: `my-video-downloads-bucket` ← ALWAYS USE THIS
- **Video Path**: `videos/` prefix
- **Thumbnail Path**: `thumbnails/` prefix
- **CloudFront Distribution**: Enabled for video delivery

### DynamoDB Tables
- **Region**: us-east-1
- **Billing Mode**: On-demand
- **Primary Tables**: See "DYNAMODB TABLES" section below

### Lambda Configuration
- **Runtime**: Python 3.9-3.12
- **Region**: us-east-1
- **Environment Variables**:
  - `S3_BUCKET=my-video-downloads-bucket`
  - `JWT_SECRET=<secret>`
  - `DYNAMODB_TABLE=<table-name>`

### IMPORTANT: Bucket Name Rules
- ❌ **NEVER** use `techcross-videos` (old/incorrect)
- ✅ **ALWAYS** use `my-video-downloads-bucket` (correct)
- When creating scripts, ALWAYS verify bucket name
- Check existing code for hardcoded bucket names

---

## **TECHNICAL STACK**

### Frontend
- HTML5, CSS3, JavaScript (ES6+), Bootstrap 5, jQuery
- Quill.js, marked.js, html2canvas, FullCalendar.js

### Backend
- AWS Lambda (Python 3.9-3.12), S3, DynamoDB, API Gateway
- yt-dlp, FFmpeg, AWS Bedrock, AWS SES

### Authentication
- JWT tokens (PyJWT), localStorage (auth_token, user_data)

---

## **AWS LAMBDA FUNCTIONS**

**Current (19)**: auth-api, admin-api, tag-api, router, downloader, articles-api, paypal-billing-api, thumbnail-generator, s3-thumbnail-trigger, url-analysis-api, news-api, resources-api, contributors-api, email-subscription-handler, video-list-api, article-analysis-api, comments-api, newsletter-api, prayer-api

**Planned Shopping (10)**: shop_api, cart_api, order_api, payment_api, order_processor, payment_processor, email_sender, inventory_updater, tracking_api, marketing_automation_api

**Total Planned**: 29 Lambda functions

---

## **DYNAMODB TABLES**

**Current (18)**: users, video-metadata, articles, download-jobs, comments, news, resources, contributors, races, candidates, state-summaries, pending-changes, email-subscribers, email-events, templates, prayer-requests, events, newsletters

**Planned Shopping (8)**: Products, Orders, Cart, Reviews, ProductViews, MarketingQueue, EmailPreferences, WatchList

**Total Planned**: 26 DynamoDB tables

---

## **KEY TECHNICAL PATTERNS**

### Dual-Mode Editor
```javascript
let markdownContent = '';
let htmlContent = '';
function switchToMarkdown() { htmlContent = quill.root.innerHTML; }
function switchToRichText() { markdownContent = textarea.value; quill.root.innerHTML = marked.parse(markdownContent); }
```

### Circuit Breaker Pattern
```python
@circuit_breaker(failure_threshold=5, timeout=30, retry_after=60)
def call_external_api():
    # API call here
```

### Cache-Aside Pattern
```python
def get_product(product_id):
    cached = redis.get(f"product:{product_id}")
    if cached: return cached
    product = dynamodb.get_item(Key={'product_id': product_id})
    redis.setex(f"product:{product_id}", 3600, product)
    return product
```

---

## **IMPORTANT NOTES**

### localStorage Keys (Standardized)
- `auth_token` - JWT authentication token
- `user_data` - JSON {email, first_name, last_name, role}

### Best Practices
- **NEVER** use `document.write()` with user-generated content
- **ALWAYS** use DOM methods (createElement, appendChild)
- Use Quill's clipboard.convert() and setContents()
- Use contenteditable for email templates (preserves inline CSS)

### Database Patterns
- Users table uses user_id as primary key (not email)
- Always scan by email for name lookups
- DynamoDB Decimals require explicit conversion before JSON serialization

---

## **WHAT I NEED HELP WITH**
[Describe your specific task here - e.g., "Implement Week 1 SQS queues", "Deploy shopping system Phase 1", "Add new Lambda function", "Fix bug in election map", "Create voter guide for new state", "Optimize database queries", etc.]

---

**Copy this entire prompt into your new chat, then add your specific request at the "What I Need Help With" section!**
