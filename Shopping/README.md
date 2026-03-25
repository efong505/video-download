# SHOPPING SYSTEM - PROJECT FOLDER

## Overview
Full e-commerce shopping system with behavioral tracking and marketing automation. Built on AWS serverless (Lambda, DynamoDB, API Gateway, SQS, SES).

**Status:** ✅ 100% Complete (9/9 weeks)

---

## Infrastructure

### API Gateway
- **ID:** `ydq9xzya5d`
- **Base URL:** `https://ydq9xzya5d.execute-api.us-east-1.amazonaws.com/prod/`
- **Resources:** /products, /orders, /reviews, /tracking, /marketing

### DynamoDB Tables (8)
| Table | Purpose |
|-------|---------|
| Products | Product catalog (3 GSIs) |
| Orders | Order history (3 GSIs) |
| Cart | Shopping carts (TTL) |
| Reviews | Product reviews (2 GSIs) |
| ProductViews | Behavioral tracking (3 GSIs, 90-day TTL) |
| WatchList | Price drop alerts |
| MarketingQueue | Email queue (2 GSIs, 30-day TTL) |
| EmailPreferences | User email opt-in/out |

### SQS Queues (8)
- 4 main queues: order-processing, payment-processing, email-notification, inventory-update
- 4 dead letter queues (DLQs) with 3-retry policy

### Lambda Functions (5)
| Lambda | Runtime | Memory | Purpose |
|--------|---------|--------|---------|
| products-api | Python 3.12 | 128MB | Product CRUD, list, search |
| orders-api | Python 3.12 | 128MB | Order create, get, list, status |
| reviews-api | Python 3.12 | 128MB | Review create, list, vote |
| tracking-api | Python 3.12 | 256MB | View/cart tracking, recommendations, watchlist |
| marketing-api | Python 3.12 | 512MB | Abandoned cart scans, email sending, preferences |

### Monitoring
- CloudWatch Dashboard: `Shopping-System` (6 widgets)
- 14 CloudWatch Alarms (4 DLQ + 5 error + 5 latency)
- CloudWatch Events: `marketing-daily-scan` (10 AM EST daily)

---

## Frontend Pages (7)

| Page | Purpose |
|------|---------|
| shop.html | Product catalog with ratings, tracking integration |
| product.html | Product detail with reviews, watchlist, view tracking |
| cart.html | Shopping cart with checkout |
| orders.html | User order history |
| admin-products.html | Admin product CRUD |
| admin-orders.html | Admin order dashboard with status management |
| preferences.html | Email preference center with unsubscribe |

All pages hosted on S3: `s3://my-video-downloads-bucket/Shopping/`

---

## Features

### Core Shopping ✅
- Product catalog with search/filter and star ratings
- Shopping cart (localStorage) with checkout
- Order creation with stock validation
- Order history and status tracking (pending → processing → shipped → delivered)
- Customer reviews with helpful/unhelpful voting
- Admin product management (CRUD)
- Admin order management

### Behavioral Tracking ✅
- Product view tracking (device type, referrer, session)
- Cart-add tracking
- Popular products (last 7 days)
- Personalized recommendations (category-based)
- Watchlist with price drop alerts

### Marketing Automation ✅
- Abandoned cart detection (24-72hr window)
- Browse abandonment detection (3+ views, no cart add)
- Price drop alerts (watchlist target price)
- 3 HTML email templates via SES
- 7-day duplicate prevention cooldown
- Email preference center with one-click unsubscribe
- Daily automated scan via CloudWatch Events

---

## Product Categories
1. Books — Christian living, political commentary, Bible studies
2. Apparel — T-shirts, hats, hoodies
3. Resources — Voter guides, study guides, curriculum
4. Digital Downloads — E-books, PDFs, video courses
5. Merchandise — Mugs, stickers, posters
6. Ministry Tools — Sermon outlines, graphics packages

---

## Post-Launch Items
- ⏸️ Payment processing (Stripe/PayPal) — currently orders are free/test
- ⏸️ User authentication for Shopping APIs
- ⏸️ Shipping integration
- ⏸️ Tighten IAM policies (replace FullAccess with scoped)
- ⏸️ ElastiCache Redis (when traffic justifies ~$15/month)
- ⏸️ API Gateway caching (when traffic justifies ~$10/month)

---

## Cost Estimates

### Current (Monthly)
- DynamoDB: ~$6 (8 tables, on-demand)
- Lambda: ~$4.50 (5 functions)
- SQS: ~$2 (8 queues)
- SES: ~$1
- S3: ~$0.75
- **Total: ~$14.25/month**

### With Caching (When Traffic Justifies)
- Add ElastiCache: +$15/month
- Add API Gateway Cache: +$10/month
- DynamoDB savings: -$3/month
- **Total: ~$36.25/month**

---

## Documentation
- **IMPLEMENTATION_PROGRESS.md** — Week-by-week progress tracker (100% complete)
- **SHOPPING_SYSTEM_PLAN.md** — Original 9-week implementation plan
- **TRACKING_SYSTEM_SPECS.md** — Behavioral tracking + marketing specs
- **ARCHITECTURE_REQUIREMENTS.md** — Architecture patterns and requirements
- **QUICK_START.md** — Setup guide for all deployment scripts
- **scripts/README.md** — Script-by-script documentation

---

## AWS Details
- **Profile:** `ekewaka` (account 371751795928)
- **Region:** `us-east-1`
- **S3 Bucket:** `my-video-downloads-bucket`
- **SES Domain:** `christianconservativestoday.com` (verified, out of sandbox)
- **SNS Topic:** `arn:aws:sns:us-east-1:371751795928:platform-critical-alerts`
