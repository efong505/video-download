# E-COMMERCE SHOPPING SYSTEM - IMPLEMENTATION PLAN

## Overview
Complete e-commerce solution for Christian Conservatives Today platform with shopping cart, order management, payment processing (PayPal + Stripe), and smart behavioral tracking for marketing automation.

---

## PHASE 1: BASIC SHOPPING SYSTEM (Weeks 1-5)

### Database Schema

#### DynamoDB Table: **Products**
```
Partition Key: product_id (String)
Attributes:
- name (String)
- description (String)
- price (Number) - in cents
- category (String) - Books, Apparel, Resources, Digital, Merchandise, Ministry Tools
- subcategory (String)
- image_url (String)
- images (List) - multiple product images
- sku (String)
- stock_quantity (Number)
- digital_download (Boolean)
- download_url (String) - for digital products
- weight (Number) - for shipping calculation
- dimensions (Map) - length, width, height
- featured (Boolean)
- status (String) - active, inactive, out_of_stock
- tags (List)
- created_at (String)
- updated_at (String)
- created_by (String)
- sales_count (Number)
- rating (Number)
- review_count (Number)

GSI: category-created_at-index (for browsing by category)
GSI: featured-created_at-index (for featured products)
GSI: status-sales_count-index (for best sellers)
```

#### DynamoDB Table: **Orders**
```
Partition Key: order_id (String)
Sort Key: user_id (String)
Attributes:
- order_number (String) - human-readable (e.g., ORD-2025-001234)
- user_email (String)
- items (List of Maps):
  - product_id
  - product_name
  - quantity
  - price_at_purchase
  - subtotal
- subtotal (Number)
- tax (Number)
- shipping (Number)
- discount (Number)
- total (Number)
- payment_method (String) - paypal, stripe
- payment_id (String) - PayPal/Stripe transaction ID
- payment_status (String) - pending, completed, failed, refunded
- shipping_address (Map):
  - name
  - address_line1
  - address_line2
  - city
  - state
  - zip
  - country
- billing_address (Map)
- order_status (String) - pending, processing, shipped, delivered, cancelled
- tracking_number (String)
- order_date (String)
- shipped_date (String)
- delivered_date (String)
- notes (String)
- digital_downloads (List) - URLs for digital products

GSI: user_id-order_date-index (for user order history)
GSI: order_status-order_date-index (for admin order management)
GSI: payment_status-order_date-index (for payment tracking)
```

#### DynamoDB Table: **Cart**
```
Partition Key: user_id (String) - or session_id for anonymous
Attributes:
- items (List of Maps):
  - product_id
  - product_name
  - quantity
  - price
  - image_url
- created_at (String)
- updated_at (String)
- expires_at (String) - 30 days from last update

Note: Cart data expires after 30 days of inactivity
```

#### DynamoDB Table: **Reviews**
```
Partition Key: review_id (String)
Sort Key: product_id (String)
Attributes:
- user_id (String)
- user_name (String)
- rating (Number) - 1-5 stars
- title (String)
- review_text (String)
- verified_purchase (Boolean)
- helpful_count (Number)
- created_at (String)
- updated_at (String)
- status (String) - pending, approved, rejected

GSI: product_id-created_at-index (for product reviews)
GSI: user_id-created_at-index (for user reviews)
```

---

### Lambda Functions

#### 1. **shop_api** (Main Shopping API)
**Endpoints:**
- `GET /products` - List all products (with filters)
- `GET /products/{id}` - Get single product
- `POST /products` - Create product (admin only)
- `PUT /products/{id}` - Update product (admin only)
- `DELETE /products/{id}` - Delete product (admin only)
- `GET /categories` - List all categories
- `GET /featured` - Get featured products
- `GET /bestsellers` - Get best-selling products
- `POST /reviews` - Submit product review
- `GET /reviews/{product_id}` - Get product reviews

**Memory:** 512MB  
**Timeout:** 30 seconds  
**Environment Variables:** JWT_SECRET, DYNAMODB_TABLE_PRODUCTS

#### 2. **cart_api** (Shopping Cart Management)
**Endpoints:**
- `GET /cart` - Get user's cart
- `POST /cart/add` - Add item to cart
- `PUT /cart/update` - Update item quantity
- `DELETE /cart/remove` - Remove item from cart
- `DELETE /cart/clear` - Clear entire cart
- `POST /cart/merge` - Merge anonymous cart with user cart on login

**Memory:** 256MB  
**Timeout:** 15 seconds

#### 3. **order_api** (Order Management)
**Endpoints:**
- `POST /orders/create` - Create new order
- `GET /orders` - List user's orders
- `GET /orders/{id}` - Get order details
- `PUT /orders/{id}/status` - Update order status (admin)
- `POST /orders/{id}/cancel` - Cancel order
- `GET /orders/admin/list` - List all orders (admin)
- `POST /orders/{id}/refund` - Process refund (admin)
- `PUT /orders/{id}/tracking` - Add tracking number (admin)

**Memory:** 512MB  
**Timeout:** 30 seconds

#### 4. **payment_api** (Payment Processing)
**Endpoints:**
- `POST /payment/paypal/create` - Create PayPal order
- `POST /payment/paypal/capture` - Capture PayPal payment
- `POST /payment/stripe/intent` - Create Stripe payment intent
- `POST /payment/stripe/confirm` - Confirm Stripe payment
- `POST /payment/webhook/paypal` - PayPal webhook handler
- `POST /payment/webhook/stripe` - Stripe webhook handler

**Memory:** 512MB  
**Timeout:** 30 seconds  
**Environment Variables:** 
- PAYPAL_CLIENT_ID
- PAYPAL_CLIENT_SECRET
- STRIPE_SECRET_KEY
- STRIPE_WEBHOOK_SECRET

---

### Frontend Pages

#### 1. **shop.html** (Product Catalog)
**Features:**
- Grid/list view toggle
- Category filtering
- Price range filter
- Search functionality
- Sort by: price, popularity, newest, rating
- Pagination
- "Add to Cart" buttons
- Quick view modal
- Featured products section
- Best sellers section

**Design:** Bootstrap 5 cards, responsive grid

#### 2. **product.html** (Product Detail Page)
**Features:**
- Image gallery with zoom
- Product description
- Price and availability
- Quantity selector
- "Add to Cart" button
- Product specifications
- Customer reviews and ratings
- Related products
- Social sharing buttons
- Breadcrumb navigation

**Design:** Professional e-commerce layout

#### 3. **cart.html** (Shopping Cart)
**Features:**
- Cart items list with thumbnails
- Quantity adjustment (+/-)
- Remove item button
- Subtotal calculation
- Tax estimation
- Shipping estimation
- Discount code input
- "Continue Shopping" button
- "Proceed to Checkout" button
- Empty cart message
- Save for later option

**Design:** Clean, easy-to-scan layout

#### 4. **checkout.html** (Checkout Process)
**Features:**
- Multi-step checkout:
  1. Shipping information
  2. Payment method selection
  3. Order review
- Guest checkout option
- Saved addresses (for logged-in users)
- Payment method selection (PayPal vs Stripe)
- PayPal button integration
- Stripe card element integration
- Order summary sidebar
- Terms and conditions checkbox
- SSL security badge
- Order confirmation

**Design:** Trust-building, secure appearance

#### 5. **orders.html** (Order History)
**Features:**
- List of user's orders
- Order status badges
- Order details modal
- Reorder button
- Track shipment button
- Download invoice (PDF)
- Download digital products
- Cancel order option
- Leave review button
- Filter by status
- Search orders

**Design:** Clean table/card layout

#### 6. **admin-shop.html** (Admin Product Management)
**Features:**
- Product list with search/filter
- Add new product form
- Edit product modal
- Delete product confirmation
- Bulk actions (activate, deactivate, delete)
- Image upload (S3)
- Category management
- Inventory tracking
- Sales analytics
- Order management section
- Pending orders alert
- Quick status updates
- Export orders to CSV

**Design:** Admin dashboard style

---

### Payment Integration

#### PayPal Integration
**SDK:** PayPal JavaScript SDK v2
**Flow:**
1. User clicks "Pay with PayPal"
2. PayPal button opens popup
3. User logs into PayPal
4. User approves payment
5. payment_api captures payment
6. Order created in DynamoDB
7. Confirmation email sent

**Fees:** 3.49% + $0.49 per transaction

#### Stripe Integration
**SDK:** Stripe.js v3
**Flow:**
1. User enters card details
2. Stripe creates payment intent
3. User confirms payment
4. Stripe processes payment
5. payment_api receives webhook
6. Order created in DynamoDB
7. Confirmation email sent

**Fees:** 2.9% + $0.30 per transaction

**Security:**
- PCI compliance handled by Stripe
- No card data touches your server
- 3D Secure authentication
- Fraud detection built-in

---

### Product Categories

1. **Books**
   - Christian living
   - Political commentary
   - Bible studies
   - Devotionals
   - Children's books

2. **Apparel**
   - T-shirts
   - Hats
   - Hoodies
   - Accessories

3. **Resources**
   - Voter guides (printed)
   - Study guides
   - Curriculum
   - Workbooks

4. **Digital Downloads**
   - E-books
   - PDF guides
   - Video courses
   - Audio sermons

5. **Merchandise**
   - Mugs
   - Stickers
   - Posters
   - Banners

6. **Ministry Tools**
   - Sermon outlines
   - Bulletin inserts
   - Graphics packages
   - Social media templates

---

### Implementation Timeline (Phase 1)

**Week 1: Database & Backend**
- Create DynamoDB tables
- Implement shop_api Lambda
- Implement cart_api Lambda
- Test CRUD operations

**Week 2: Payment Integration**
- Implement payment_api Lambda
- PayPal SDK integration
- Stripe SDK integration
- Test payment flows

**Week 3: Frontend - Shopping**
- Create shop.html
- Create product.html
- Create cart.html
- Implement cart functionality

**Week 4: Frontend - Checkout**
- Create checkout.html
- Create orders.html
- Implement order tracking
- Email notifications

**Week 5: Admin & Testing**
- Create admin-shop.html
- Bulk product import
- End-to-end testing
- Security audit

---

## PHASE 2: SMART SHOPPING & MARKETING AUTOMATION (Weeks 6-7)

### Overview
Behavioral tracking and automated marketing to recover abandoned carts, re-engage browsers, and increase conversions by 10-30%.

---

### Additional Database Tables

#### DynamoDB Table: **ProductViews**
```
Partition Key: view_id (String)
Sort Key: timestamp (String)
Attributes:
- user_id (String) - if logged in
- session_id (String) - if anonymous
- product_id (String)
- product_name (String)
- product_price (Number)
- view_duration (Number) - seconds on page
- added_to_cart (Boolean)
- purchased (Boolean)
- referrer (String)
- device_type (String) - desktop, mobile, tablet
- created_at (String)

GSI: user_id-timestamp-index (for user behavior analysis)
GSI: session_id-timestamp-index (for anonymous tracking)
GSI: product_id-timestamp-index (for product popularity)
```

#### DynamoDB Table: **MarketingQueue**
```
Partition Key: queue_id (String)
Attributes:
- user_id (String)
- user_email (String)
- trigger_type (String) - abandoned_cart, browse_abandonment, price_drop, back_in_stock
- product_ids (List)
- product_names (List)
- cart_total (Number) - for abandoned cart
- discount_code (String) - optional incentive
- scheduled_send_time (String)
- sent (Boolean)
- sent_at (String)
- opened (Boolean)
- clicked (Boolean)
- converted (Boolean)
- created_at (String)

GSI: sent-scheduled_send_time-index (for processing queue)
GSI: user_email-trigger_type-index (prevent duplicate emails)
```

#### DynamoDB Table: **EmailPreferences**
```
Partition Key: user_id (String)
Attributes:
- email (String)
- marketing_emails (Boolean) - opt-in for marketing
- abandoned_cart_emails (Boolean)
- price_drop_alerts (Boolean)
- back_in_stock_alerts (Boolean)
- product_recommendations (Boolean)
- newsletter (Boolean)
- unsubscribed (Boolean)
- unsubscribe_token (String)
- created_at (String)
- updated_at (String)
```

#### DynamoDB Table: **WatchList**
```
Partition Key: user_id (String)
Sort Key: product_id (String)
Attributes:
- product_name (String)
- current_price (Number)
- target_price (Number) - alert when price drops below this
- in_stock (Boolean)
- notify_on_price_drop (Boolean)
- notify_on_restock (Boolean)
- created_at (String)
```

---

### Enhanced Lambda Functions

#### 5. **tracking_api** (Behavioral Tracking)
**Endpoints:**
- `POST /track/view` - Log product view
- `POST /track/cart-add` - Log add to cart
- `POST /track/cart-remove` - Log remove from cart
- `POST /track/purchase` - Log completed purchase
- `GET /track/recommendations/{user_id}` - Get personalized recommendations
- `GET /track/popular` - Get trending products
- `POST /track/watchlist/add` - Add product to watchlist
- `DELETE /track/watchlist/remove` - Remove from watchlist

**Memory:** 256MB  
**Timeout:** 15 seconds

#### 6. **marketing_automation_api** (Automated Marketing)
**Endpoints:**
- `POST /marketing/scan-abandoned-carts` - Scheduled job (daily)
- `POST /marketing/scan-browse-abandonment` - Scheduled job (daily)
- `POST /marketing/scan-price-drops` - Scheduled job (daily)
- `POST /marketing/scan-restock` - Scheduled job (daily)
- `POST /marketing/send-email` - Send queued email
- `POST /marketing/track-open` - Track email open
- `POST /marketing/track-click` - Track email click
- `GET /marketing/analytics` - Marketing performance metrics

**Memory:** 512MB  
**Timeout:** 5 minutes (for batch processing)  
**Trigger:** CloudWatch Events (scheduled daily at 10 AM)

**Environment Variables:**
- SES_FROM_EMAIL
- SES_REGION
- DISCOUNT_CODE_PREFIX

---

### Smart Shopping Features

#### 1. **Abandoned Cart Recovery**
**Trigger:** Cart has items, no purchase within 24 hours

**Email Template:**
```
Subject: You left items in your cart! 🛒

Hi [Name],

You left these items in your cart:

[Product 1 Image] [Product Name] - $[Price]
[Product 2 Image] [Product Name] - $[Price]

Total: $[Cart Total]

Complete your purchase now and get 10% OFF with code: CART10

[Complete Purchase Button]

Questions? Reply to this email!

Blessings,
Christian Conservatives Today Team

[Unsubscribe Link]
```

**Conversion Rate:** Typically 10-15% of abandoned carts convert

#### 2. **Browse Abandonment**
**Trigger:** Viewed product 3+ times, never added to cart, 48 hours since last view

**Email Template:**
```
Subject: Still interested in [Product Name]? 🤔

Hi [Name],

We noticed you've been looking at:

[Product Image]
[Product Name]
$[Price]

Here's 5% OFF to help you decide: BROWSE5

[Shop Now Button]

What others are saying:
⭐⭐⭐⭐⭐ "[Review excerpt]"

[Unsubscribe Link]
```

**Conversion Rate:** Typically 5-8%

#### 3. **Price Drop Alert**
**Trigger:** Product on watchlist drops below target price

**Email Template:**
```
Subject: 🎉 Price Drop Alert: [Product Name]

Hi [Name],

Great news! The price dropped on a product you're watching:

[Product Image]
[Product Name]

Was: $[Old Price]
NOW: $[New Price]
YOU SAVE: $[Savings]

[Buy Now Button]

Limited time offer - grab it before it's gone!

[Unsubscribe Link]
```

**Conversion Rate:** Typically 20-30% (high intent)

#### 4. **Back in Stock Alert**
**Trigger:** Product on watchlist comes back in stock

**Email Template:**
```
Subject: ✅ Back in Stock: [Product Name]

Hi [Name],

Good news! A product you wanted is back in stock:

[Product Image]
[Product Name]
$[Price]

[Add to Cart Button]

Hurry - limited quantity available!

[Unsubscribe Link]
```

**Conversion Rate:** Typically 15-25%

#### 5. **Personalized Recommendations**
**Trigger:** Weekly email based on browsing history

**Email Template:**
```
Subject: Products you might love ❤️

Hi [Name],

Based on your interests, we think you'll love these:

[Product 1] [Product 2] [Product 3]

[Shop Recommendations Button]

New arrivals in [Category]:
[Product 4] [Product 5] [Product 6]

[Unsubscribe Link]
```

**Conversion Rate:** Typically 3-5%

---

### Email Delivery (AWS SES)

**Setup:**
1. Verify domain in AWS SES
2. Move out of SES sandbox (request production access)
3. Set up DKIM and SPF records
4. Create email templates in SES

**Features:**
- HTML email templates
- Inline CSS for compatibility
- Responsive design
- Tracking pixels for opens
- UTM parameters for clicks
- Unsubscribe link in every email

**Cost:** $0.10 per 1,000 emails (very cheap!)

**Deliverability:**
- Maintain sender reputation
- Monitor bounce rates
- Handle unsubscribes promptly
- Avoid spam triggers

---

### Privacy & Compliance

#### GDPR/CCPA Compliance
- **Opt-in Required:** Checkbox during account creation
- **Granular Preferences:** Users control email types
- **Easy Unsubscribe:** One-click unsubscribe link
- **Data Deletion:** Users can request data deletion
- **Privacy Policy:** Clear explanation of tracking

#### Email Preference Center
**Features:**
- Toggle each email type on/off
- Update email address
- Unsubscribe from all
- Re-subscribe option
- Export my data
- Delete my data

**Page:** preferences.html

#### Tracking Disclosure
**Privacy Policy Addition:**
```
We track your browsing behavior to provide personalized 
recommendations and send relevant marketing emails. This includes:
- Products you view
- Items you add to cart
- Time spent on pages
- Purchase history

You can opt out of marketing emails at any time.
```

---

### Analytics Dashboard (admin-marketing.html)

**Metrics:**
- Abandoned cart rate
- Cart recovery rate
- Email open rates
- Email click rates
- Conversion rates by email type
- Revenue from marketing emails
- Most viewed products
- Most abandoned products
- Best performing email campaigns

**Charts:**
- Daily abandoned carts
- Recovery funnel
- Email performance over time
- Revenue attribution

---

### Implementation Timeline (Phase 2)

**Week 6: Tracking System**
- Create ProductViews table
- Create MarketingQueue table
- Create EmailPreferences table
- Create WatchList table
- Implement tracking_api Lambda
- Add tracking to frontend pages
- Test tracking functionality

**Week 7: Marketing Automation**
- Implement marketing_automation_api Lambda
- Set up AWS SES
- Create email templates
- Configure CloudWatch Events
- Implement preference center
- Test email flows
- Create admin analytics dashboard

---

## Cost Estimates

### AWS Costs (Monthly)

**DynamoDB:**
- Products table: ~$1
- Orders table: ~$2
- Cart table: ~$0.50
- Reviews table: ~$0.50
- ProductViews table: ~$1
- MarketingQueue table: ~$0.50
- EmailPreferences table: ~$0.25
- WatchList table: ~$0.25
**Subtotal: ~$6/month**

**Lambda:**
- shop_api: ~$1
- cart_api: ~$0.50
- order_api: ~$1
- payment_api: ~$1
- tracking_api: ~$0.50
- marketing_automation_api: ~$0.50
**Subtotal: ~$4.50/month**

**S3 (Product Images):**
- Storage: ~$0.50
- Requests: ~$0.25
**Subtotal: ~$0.75/month**

**SES (Email):**
- 10,000 emails/month: ~$1
**Subtotal: ~$1/month**

**Total AWS: ~$12.25/month**

### Payment Processing Fees

**PayPal:** 3.49% + $0.49 per transaction  
**Stripe:** 2.9% + $0.30 per transaction

**Example (100 orders @ $50 average):**
- PayPal: $223.50 in fees
- Stripe: $175 in fees
- **Savings with Stripe: $48.50/month**

**Recommendation:** Offer both, but incentivize Stripe (lower fees)

---

## Security Considerations

### Payment Security
- ✅ PCI compliance via PayPal/Stripe
- ✅ No card data stored on server
- ✅ HTTPS only
- ✅ Webhook signature verification
- ✅ Idempotency keys for payments

### Data Security
- ✅ JWT authentication for API calls
- ✅ Input validation and sanitization
- ✅ SQL injection prevention (NoSQL)
- ✅ XSS prevention (DOMPurify)
- ✅ CORS configuration
- ✅ Rate limiting on APIs

### Privacy
- ✅ Encrypted data at rest (DynamoDB)
- ✅ Encrypted data in transit (HTTPS)
- ✅ User consent for tracking
- ✅ Easy opt-out mechanism
- ✅ Data deletion on request

---

## Testing Plan

### Unit Tests
- Lambda function logic
- Payment processing
- Cart calculations
- Email template rendering

### Integration Tests
- End-to-end checkout flow
- PayPal payment flow
- Stripe payment flow
- Email delivery
- Webhook handling

### User Acceptance Tests
- Browse products
- Add to cart
- Complete purchase
- View order history
- Receive marketing emails
- Unsubscribe from emails

### Load Tests
- 100 concurrent users
- 1000 products in catalog
- Payment processing under load

---

## Launch Checklist

### Pre-Launch
- [ ] All Lambda functions deployed
- [ ] DynamoDB tables created
- [ ] S3 bucket configured
- [ ] PayPal account verified
- [ ] Stripe account verified
- [ ] SES domain verified
- [ ] Email templates created
- [ ] Test products added
- [ ] Test orders completed
- [ ] Privacy policy updated
- [ ] Terms of service updated

### Launch Day
- [ ] Enable payment processing
- [ ] Monitor error logs
- [ ] Test live payments
- [ ] Verify email delivery
- [ ] Check order creation
- [ ] Monitor performance

### Post-Launch (Week 1)
- [ ] Review analytics
- [ ] Check abandoned cart rate
- [ ] Monitor email open rates
- [ ] Gather user feedback
- [ ] Fix any bugs
- [ ] Optimize performance

---

## Future Enhancements (Phase 3+)

### Advanced Features
- Product bundles and packages
- Subscription products (monthly boxes)
- Gift cards and vouchers
- Affiliate program
- Wholesale pricing for churches
- Bulk order discounts
- Pre-orders for upcoming products
- Product variants (sizes, colors)
- Inventory management alerts
- Automatic reordering
- Multi-currency support
- International shipping
- Tax calculation by state
- Shipping carrier integration (UPS, FedEx)
- Print-on-demand integration

### Marketing Features
- Referral program
- Loyalty points system
- Birthday discounts
- VIP customer tiers
- Flash sales and limited offers
- Countdown timers
- Exit-intent popups
- Product comparison tool
- Wish list sharing
- Gift registry

### Analytics
- Customer lifetime value
- Cohort analysis
- Product performance reports
- Marketing attribution
- A/B testing framework
- Heatmaps and session recordings

---

## Success Metrics

### Key Performance Indicators (KPIs)

**Revenue Metrics:**
- Monthly revenue
- Average order value
- Revenue per customer
- Conversion rate

**Customer Metrics:**
- New customers
- Repeat customers
- Customer retention rate
- Customer lifetime value

**Marketing Metrics:**
- Cart abandonment rate (target: <70%)
- Cart recovery rate (target: >10%)
- Email open rate (target: >20%)
- Email click rate (target: >3%)
- Email conversion rate (target: >2%)

**Product Metrics:**
- Best-selling products
- Most viewed products
- Most abandoned products
- Average products per order

---

## Support & Maintenance

### Ongoing Tasks
- Monitor order fulfillment
- Respond to customer inquiries
- Process refunds
- Update product inventory
- Add new products
- Review and approve customer reviews
- Monitor email deliverability
- Optimize email campaigns
- Analyze sales data
- Update pricing

### Monthly Reviews
- Sales performance
- Marketing effectiveness
- Customer feedback
- Technical issues
- Cost analysis
- Feature requests

---

## Conclusion

This comprehensive e-commerce system will:
- ✅ Generate new revenue stream
- ✅ Provide valuable resources to customers
- ✅ Increase platform engagement
- ✅ Build customer loyalty
- ✅ Support ministry mission
- ✅ Recover lost sales with smart marketing
- ✅ Maximize conversions with dual payment options

**Estimated Development Time:** 7 weeks  
**Estimated Monthly Cost:** ~$12 AWS + payment processing fees  
**Estimated ROI:** Positive within 3-6 months

**Next Steps:**
1. Review and approve plan
2. Set up PayPal and Stripe accounts
3. Begin Phase 1 implementation
4. Add initial product catalog
5. Launch beta testing
6. Implement Phase 2 smart features
7. Full public launch
