# BEHAVIORAL TRACKING & MARKETING AUTOMATION - TECHNICAL SPECIFICATIONS

## Overview
Technical implementation details for smart shopping features including product view tracking, abandoned cart recovery, browse abandonment detection, and automated email marketing.

---

## ARCHITECTURE

### System Components
1. **Frontend Tracking** - JavaScript tracking on product/cart pages
2. **tracking_api Lambda** - Collect and store behavioral data
3. **marketing_automation_api Lambda** - Process data and queue emails
4. **AWS SES** - Email delivery service
5. **CloudWatch Events** - Scheduled job triggers
6. **DynamoDB** - Data storage

### Data Flow
```
User Action → Frontend JS → tracking_api → DynamoDB (ProductViews/Cart)
                                                ↓
                                    CloudWatch Event (daily 10 AM)
                                                ↓
                                    marketing_automation_api
                                                ↓
                                    Scan for triggers → MarketingQueue
                                                ↓
                                    Send emails via SES
                                                ↓
                                    Track opens/clicks
```

---

## DATABASE SCHEMAS (DETAILED)

### ProductViews Table

**Purpose:** Track every product page view for behavioral analysis

**Schema:**
```python
{
    "view_id": "view_20250115_abc123",  # PK
    "timestamp": "2025-01-15T14:30:00Z",  # SK
    "user_id": "user_123",  # or null if anonymous
    "session_id": "sess_xyz789",  # browser session
    "product_id": "prod_001",
    "product_name": "Christian Voter Guide 2026",
    "product_price": 1999,  # in cents
    "product_category": "Books",
    "view_duration": 45,  # seconds on page
    "added_to_cart": false,
    "purchased": false,
    "referrer": "https://google.com",
    "device_type": "desktop",  # desktop, mobile, tablet
    "browser": "Chrome",
    "ip_address": "192.168.1.1",  # for analytics only
    "created_at": "2025-01-15T14:30:00Z"
}
```

**Indexes:**
- GSI: `user_id-timestamp-index` - Query user's view history
- GSI: `session_id-timestamp-index` - Query anonymous session
- GSI: `product_id-timestamp-index` - Query product popularity

**TTL:** 90 days (auto-delete old data)

---

### MarketingQueue Table

**Purpose:** Queue automated marketing emails for sending

**Schema:**
```python
{
    "queue_id": "queue_20250115_abc123",  # PK
    "user_id": "user_123",
    "user_email": "customer@example.com",
    "user_name": "John Smith",
    "trigger_type": "abandoned_cart",  # abandoned_cart, browse_abandonment, price_drop, back_in_stock
    "trigger_data": {
        "cart_items": [
            {
                "product_id": "prod_001",
                "product_name": "Christian Voter Guide",
                "quantity": 1,
                "price": 1999,
                "image_url": "https://..."
            }
        ],
        "cart_total": 1999,
        "cart_abandoned_at": "2025-01-14T10:00:00Z"
    },
    "discount_code": "CART10",  # optional incentive
    "discount_amount": 10,  # percentage
    "scheduled_send_time": "2025-01-15T10:00:00Z",
    "sent": false,
    "sent_at": null,
    "email_subject": "You left items in your cart!",
    "email_template": "abandoned_cart_v1",
    "opened": false,
    "opened_at": null,
    "clicked": false,
    "clicked_at": null,
    "converted": false,
    "converted_at": null,
    "conversion_order_id": null,
    "created_at": "2025-01-15T09:00:00Z"
}
```

**Indexes:**
- GSI: `sent-scheduled_send_time-index` - Query pending emails
- GSI: `user_email-trigger_type-index` - Prevent duplicate emails

**TTL:** 30 days after sent

---

### EmailPreferences Table

**Purpose:** Store user email preferences and opt-in status

**Schema:**
```python
{
    "user_id": "user_123",  # PK
    "email": "customer@example.com",
    "marketing_emails": true,  # master opt-in
    "abandoned_cart_emails": true,
    "browse_abandonment_emails": true,
    "price_drop_alerts": true,
    "back_in_stock_alerts": true,
    "product_recommendations": true,
    "newsletter": true,
    "promotional_emails": true,
    "unsubscribed": false,
    "unsubscribe_token": "token_abc123",  # for one-click unsubscribe
    "unsubscribed_at": null,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z"
}
```

**Default Values:** All true except unsubscribed (false)

---

### WatchList Table

**Purpose:** Track products users want to monitor for price drops or restocks

**Schema:**
```python
{
    "user_id": "user_123",  # PK
    "product_id": "prod_001",  # SK
    "product_name": "Christian Voter Guide",
    "current_price": 1999,
    "original_price": 1999,
    "target_price": 1500,  # alert when price drops below this
    "in_stock": true,
    "notify_on_price_drop": true,
    "notify_on_restock": true,
    "notified_price_drop": false,
    "notified_restock": false,
    "created_at": "2025-01-15T10:00:00Z"
}
```

---

## LAMBDA FUNCTION: tracking_api

### Function Configuration
```python
Runtime: Python 3.12
Memory: 256 MB
Timeout: 15 seconds
Environment Variables:
  - DYNAMODB_TABLE_VIEWS: ProductViews
  - DYNAMODB_TABLE_WATCHLIST: WatchList
  - JWT_SECRET: <secret>
```

### Endpoints

#### 1. POST /track/view
**Purpose:** Log product page view

**Request:**
```json
{
  "product_id": "prod_001",
  "product_name": "Christian Voter Guide",
  "product_price": 1999,
  "product_category": "Books",
  "referrer": "https://google.com",
  "device_type": "desktop"
}
```

**Response:**
```json
{
  "success": true,
  "view_id": "view_20250115_abc123"
}
```

**Logic:**
```python
def track_view(event):
    # Extract user_id from JWT or generate session_id
    user_id = get_user_id_from_token(event)
    session_id = get_or_create_session_id(event)
    
    # Create view record
    view = {
        "view_id": generate_id(),
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "session_id": session_id,
        "product_id": event["product_id"],
        "product_name": event["product_name"],
        "product_price": event["product_price"],
        "product_category": event["product_category"],
        "added_to_cart": False,
        "purchased": False,
        "referrer": event.get("referrer"),
        "device_type": event.get("device_type", "unknown"),
        "created_at": datetime.now().isoformat()
    }
    
    # Save to DynamoDB
    dynamodb.put_item(TableName="ProductViews", Item=view)
    
    return {"success": True, "view_id": view["view_id"]}
```

---

#### 2. POST /track/cart-add
**Purpose:** Update view record when product added to cart

**Request:**
```json
{
  "product_id": "prod_001"
}
```

**Logic:**
```python
def track_cart_add(event):
    user_id = get_user_id_from_token(event)
    product_id = event["product_id"]
    
    # Update recent views for this product
    dynamodb.update_item(
        TableName="ProductViews",
        Key={"user_id": user_id, "product_id": product_id},
        UpdateExpression="SET added_to_cart = :true",
        ExpressionAttributeValues={":true": True}
    )
```

---

#### 3. GET /track/recommendations/{user_id}
**Purpose:** Get personalized product recommendations

**Logic:**
```python
def get_recommendations(user_id):
    # Get user's view history
    views = dynamodb.query(
        TableName="ProductViews",
        IndexName="user_id-timestamp-index",
        KeyConditionExpression="user_id = :uid",
        ExpressionAttributeValues={":uid": user_id},
        Limit=50
    )
    
    # Extract viewed categories
    categories = [v["product_category"] for v in views]
    top_category = most_common(categories)
    
    # Get popular products in that category
    products = dynamodb.query(
        TableName="Products",
        IndexName="category-sales_count-index",
        KeyConditionExpression="category = :cat",
        ExpressionAttributeValues={":cat": top_category},
        ScanIndexForward=False,  # descending order
        Limit=6
    )
    
    return products
```

---

#### 4. POST /track/watchlist/add
**Purpose:** Add product to user's watchlist

**Request:**
```json
{
  "product_id": "prod_001",
  "target_price": 1500,
  "notify_on_price_drop": true,
  "notify_on_restock": true
}
```

---

## LAMBDA FUNCTION: marketing_automation_api

### Function Configuration
```python
Runtime: Python 3.12
Memory: 512 MB
Timeout: 5 minutes (for batch processing)
Environment Variables:
  - DYNAMODB_TABLE_QUEUE: MarketingQueue
  - DYNAMODB_TABLE_CART: Cart
  - DYNAMODB_TABLE_VIEWS: ProductViews
  - DYNAMODB_TABLE_PREFERENCES: EmailPreferences
  - SES_FROM_EMAIL: noreply@christianconservatives.today
  - SES_REGION: us-east-1
  - DISCOUNT_CODE_ABANDONED_CART: CART10
  - DISCOUNT_CODE_BROWSE: BROWSE5
```

### CloudWatch Event Trigger
```json
{
  "schedule": "cron(0 10 * * ? *)",
  "description": "Run marketing automation daily at 10 AM EST"
}
```

---

### Job 1: Scan Abandoned Carts

**Trigger:** Daily at 10 AM

**Logic:**
```python
def scan_abandoned_carts():
    # Get all carts updated 24-48 hours ago
    cutoff_time = datetime.now() - timedelta(hours=24)
    cutoff_end = datetime.now() - timedelta(hours=48)
    
    carts = dynamodb.scan(
        TableName="Cart",
        FilterExpression="updated_at BETWEEN :start AND :end AND size(items) > :zero",
        ExpressionAttributeValues={
            ":start": cutoff_end.isoformat(),
            ":end": cutoff_time.isoformat(),
            ":zero": 0
        }
    )
    
    for cart in carts:
        user_id = cart["user_id"]
        
        # Check if user has email preferences
        prefs = get_email_preferences(user_id)
        if not prefs.get("abandoned_cart_emails", True):
            continue
        
        # Check if already sent abandoned cart email recently
        existing = dynamodb.query(
            TableName="MarketingQueue",
            IndexName="user_email-trigger_type-index",
            KeyConditionExpression="user_email = :email AND trigger_type = :type",
            FilterExpression="created_at > :recent",
            ExpressionAttributeValues={
                ":email": prefs["email"],
                ":type": "abandoned_cart",
                ":recent": (datetime.now() - timedelta(days=7)).isoformat()
            }
        )
        
        if existing["Count"] > 0:
            continue  # Already sent recently
        
        # Queue abandoned cart email
        queue_item = {
            "queue_id": generate_id(),
            "user_id": user_id,
            "user_email": prefs["email"],
            "user_name": get_user_name(user_id),
            "trigger_type": "abandoned_cart",
            "trigger_data": {
                "cart_items": cart["items"],
                "cart_total": calculate_total(cart["items"]),
                "cart_abandoned_at": cart["updated_at"]
            },
            "discount_code": "CART10",
            "discount_amount": 10,
            "scheduled_send_time": datetime.now().isoformat(),
            "sent": False,
            "email_subject": "You left items in your cart! 🛒",
            "email_template": "abandoned_cart_v1",
            "created_at": datetime.now().isoformat()
        }
        
        dynamodb.put_item(TableName="MarketingQueue", Item=queue_item)
        
    # Send queued emails
    send_queued_emails()
```

---

### Job 2: Scan Browse Abandonment

**Trigger:** Daily at 10 AM

**Logic:**
```python
def scan_browse_abandonment():
    # Get users who viewed products 3+ times but never added to cart
    cutoff_time = datetime.now() - timedelta(hours=48)
    
    # Query ProductViews for frequent viewers
    views = dynamodb.scan(
        TableName="ProductViews",
        FilterExpression="view_count >= :three AND added_to_cart = :false AND timestamp < :cutoff",
        ExpressionAttributeValues={
            ":three": 3,
            ":false": False,
            ":cutoff": cutoff_time.isoformat()
        }
    )
    
    # Group by user and product
    user_products = {}
    for view in views:
        user_id = view["user_id"]
        product_id = view["product_id"]
        
        if user_id not in user_products:
            user_products[user_id] = []
        user_products[user_id].append(view)
    
    # Queue browse abandonment emails
    for user_id, products in user_products.items():
        prefs = get_email_preferences(user_id)
        if not prefs.get("browse_abandonment_emails", True):
            continue
        
        # Pick most viewed product
        top_product = max(products, key=lambda p: p["view_count"])
        
        queue_item = {
            "queue_id": generate_id(),
            "user_id": user_id,
            "user_email": prefs["email"],
            "trigger_type": "browse_abandonment",
            "trigger_data": {
                "product": top_product
            },
            "discount_code": "BROWSE5",
            "discount_amount": 5,
            "scheduled_send_time": datetime.now().isoformat(),
            "sent": False,
            "email_subject": f"Still interested in {top_product['product_name']}? 🤔",
            "email_template": "browse_abandonment_v1",
            "created_at": datetime.now().isoformat()
        }
        
        dynamodb.put_item(TableName="MarketingQueue", Item=queue_item)
    
    send_queued_emails()
```

---

### Job 3: Scan Price Drops

**Logic:**
```python
def scan_price_drops():
    # Get all watchlist items
    watchlist = dynamodb.scan(TableName="WatchList")
    
    for item in watchlist:
        if not item["notify_on_price_drop"]:
            continue
        
        # Get current product price
        product = dynamodb.get_item(
            TableName="Products",
            Key={"product_id": item["product_id"]}
        )
        
        current_price = product["price"]
        
        # Check if price dropped below target
        if current_price < item["target_price"] and not item["notified_price_drop"]:
            # Queue price drop email
            prefs = get_email_preferences(item["user_id"])
            
            queue_item = {
                "queue_id": generate_id(),
                "user_id": item["user_id"],
                "user_email": prefs["email"],
                "trigger_type": "price_drop",
                "trigger_data": {
                    "product": product,
                    "old_price": item["current_price"],
                    "new_price": current_price,
                    "savings": item["current_price"] - current_price
                },
                "scheduled_send_time": datetime.now().isoformat(),
                "sent": False,
                "email_subject": f"🎉 Price Drop Alert: {product['name']}",
                "email_template": "price_drop_v1",
                "created_at": datetime.now().isoformat()
            }
            
            dynamodb.put_item(TableName="MarketingQueue", Item=queue_item)
            
            # Mark as notified
            dynamodb.update_item(
                TableName="WatchList",
                Key={"user_id": item["user_id"], "product_id": item["product_id"]},
                UpdateExpression="SET notified_price_drop = :true, current_price = :price",
                ExpressionAttributeValues={
                    ":true": True,
                    ":price": current_price
                }
            )
    
    send_queued_emails()
```

---

### Email Sending Function

```python
def send_queued_emails():
    # Get pending emails
    pending = dynamodb.query(
        TableName="MarketingQueue",
        IndexName="sent-scheduled_send_time-index",
        KeyConditionExpression="sent = :false AND scheduled_send_time <= :now",
        ExpressionAttributeValues={
            ":false": False,
            ":now": datetime.now().isoformat()
        },
        Limit=100  # Process 100 at a time
    )
    
    ses = boto3.client('ses', region_name=os.environ['SES_REGION'])
    
    for email in pending["Items"]:
        try:
            # Render email template
            html_body = render_template(
                email["email_template"],
                email["trigger_data"]
            )
            
            # Send via SES
            response = ses.send_email(
                Source=os.environ['SES_FROM_EMAIL'],
                Destination={'ToAddresses': [email["user_email"]]},
                Message={
                    'Subject': {'Data': email["email_subject"]},
                    'Body': {
                        'Html': {'Data': html_body}
                    }
                },
                ConfigurationSetName='marketing-emails'  # for tracking
            )
            
            # Mark as sent
            dynamodb.update_item(
                TableName="MarketingQueue",
                Key={"queue_id": email["queue_id"]},
                UpdateExpression="SET sent = :true, sent_at = :now",
                ExpressionAttributeValues={
                    ":true": True,
                    ":now": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            print(f"Error sending email: {e}")
            continue
```

---

## EMAIL TEMPLATES

### Template: abandoned_cart_v1

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #003366; color: white; padding: 20px; text-align: center; }
        .product { border: 1px solid #ddd; padding: 15px; margin: 10px 0; }
        .product img { max-width: 100px; float: left; margin-right: 15px; }
        .button { background: #28a745; color: white; padding: 15px 30px; text-decoration: none; display: inline-block; margin: 20px 0; }
        .footer { text-align: center; color: #666; font-size: 12px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>You Left Items in Your Cart! 🛒</h1>
        </div>
        
        <p>Hi {{user_name}},</p>
        
        <p>You left these items in your cart:</p>
        
        {{#each cart_items}}
        <div class="product">
            <img src="{{image_url}}" alt="{{product_name}}">
            <h3>{{product_name}}</h3>
            <p>Quantity: {{quantity}}</p>
            <p><strong>${{price_formatted}}</strong></p>
        </div>
        {{/each}}
        
        <p><strong>Total: ${{cart_total_formatted}}</strong></p>
        
        <p>Complete your purchase now and get <strong>10% OFF</strong> with code: <strong>{{discount_code}}</strong></p>
        
        <a href="{{checkout_url}}" class="button">Complete Purchase</a>
        
        <p>Questions? Reply to this email!</p>
        
        <p>Blessings,<br>Christian Conservatives Today Team</p>
        
        <div class="footer">
            <p><a href="{{unsubscribe_url}}">Unsubscribe</a> | <a href="{{preferences_url}}">Email Preferences</a></p>
            <img src="{{tracking_pixel_url}}" width="1" height="1" alt="">
        </div>
    </div>
</body>
</html>
```

---

## FRONTEND TRACKING CODE

### Product Page (product.html)

```javascript
// Track product view on page load
document.addEventListener('DOMContentLoaded', function() {
    const productId = getProductIdFromURL();
    const productData = getProductData();
    
    // Track view
    fetch('https://api.christianconservatives.today/track/view', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getJWTToken()
        },
        body: JSON.stringify({
            product_id: productId,
            product_name: productData.name,
            product_price: productData.price,
            product_category: productData.category,
            referrer: document.referrer,
            device_type: getDeviceType()
        })
    });
    
    // Track time on page
    let startTime = Date.now();
    window.addEventListener('beforeunload', function() {
        let duration = Math.floor((Date.now() - startTime) / 1000);
        navigator.sendBeacon(
            'https://api.christianconservatives.today/track/duration',
            JSON.stringify({ product_id: productId, duration: duration })
        );
    });
});

// Track add to cart
document.getElementById('add-to-cart-btn').addEventListener('click', function() {
    const productId = getProductIdFromURL();
    
    // Track cart add
    fetch('https://api.christianconservatives.today/track/cart-add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getJWTToken()
        },
        body: JSON.stringify({ product_id: productId })
    });
});
```

---

## TRACKING & ANALYTICS

### Email Open Tracking
- Embed 1x1 transparent pixel in email
- URL: `https://api.christianconservatives.today/track/email-open?queue_id=xxx`
- Update MarketingQueue: `opened = true, opened_at = now()`

### Email Click Tracking
- Wrap all links with tracking URL
- URL: `https://api.christianconservatives.today/track/email-click?queue_id=xxx&redirect=xxx`
- Update MarketingQueue: `clicked = true, clicked_at = now()`
- Redirect to actual URL

### Conversion Tracking
- When order completed, check if from marketing email
- URL parameter: `?ref=email_queue_xxx`
- Update MarketingQueue: `converted = true, converted_at = now(), conversion_order_id = xxx`

---

## PRIVACY & COMPLIANCE

### Opt-In Flow
```html
<!-- During account creation -->
<label>
    <input type="checkbox" name="marketing_emails" checked>
    Send me product recommendations and special offers
</label>
```

### Unsubscribe Flow
```
1. User clicks unsubscribe link in email
2. Redirect to: /unsubscribe?token=xxx
3. One-click unsubscribe (no login required)
4. Update EmailPreferences: unsubscribed = true
5. Show confirmation message
```

### Preference Center (/preferences.html)
```html
<h2>Email Preferences</h2>
<form>
    <label><input type="checkbox" name="abandoned_cart_emails"> Abandoned cart reminders</label>
    <label><input type="checkbox" name="price_drop_alerts"> Price drop alerts</label>
    <label><input type="checkbox" name="back_in_stock_alerts"> Back in stock notifications</label>
    <label><input type="checkbox" name="product_recommendations"> Product recommendations</label>
    <label><input type="checkbox" name="newsletter"> Newsletter</label>
    <button type="submit">Save Preferences</button>
</form>
```

---

## TESTING PLAN

### Unit Tests
- Track view function
- Abandoned cart detection
- Email template rendering
- Discount code generation

### Integration Tests
- End-to-end tracking flow
- Email sending via SES
- Unsubscribe flow
- Preference updates

### Load Tests
- 1000 concurrent product views
- 100 emails sent simultaneously
- Database query performance

---

## MONITORING & ALERTS

### CloudWatch Metrics
- Emails sent per day
- Email open rate
- Email click rate
- Conversion rate
- Failed email sends
- Lambda errors

### Alerts
- Email send failures > 5%
- Lambda timeout errors
- DynamoDB throttling
- SES bounce rate > 5%

---

## COST ANALYSIS

### DynamoDB
- ProductViews: 10,000 writes/day × $1.25/million = $0.38/month
- MarketingQueue: 500 writes/day × $1.25/million = $0.02/month
- Reads: Minimal cost

### Lambda
- tracking_api: 10,000 invocations/day × $0.20/million = $0.60/month
- marketing_automation_api: 1 invocation/day × 5 min = $0.01/month

### SES
- 10,000 emails/month × $0.10/1000 = $1.00/month

**Total: ~$2/month for smart shopping features**

---

## SUCCESS METRICS

### Target KPIs
- Cart abandonment rate: <70%
- Cart recovery rate: >10%
- Email open rate: >20%
- Email click rate: >3%
- Email conversion rate: >2%
- Revenue from marketing emails: >$500/month

### ROI Calculation
```
Monthly Cost: $2
Monthly Revenue from Recovered Carts: $500
ROI: 25,000%
```

---

## DEPLOYMENT CHECKLIST

- [ ] Create DynamoDB tables
- [ ] Deploy tracking_api Lambda
- [ ] Deploy marketing_automation_api Lambda
- [ ] Set up CloudWatch Event trigger
- [ ] Configure AWS SES
- [ ] Verify domain in SES
- [ ] Create email templates
- [ ] Add tracking code to frontend
- [ ] Test email sending
- [ ] Test unsubscribe flow
- [ ] Monitor for 1 week
- [ ] Optimize based on data

---

## CONCLUSION

This tracking system will:
- ✅ Recover 10-15% of abandoned carts
- ✅ Re-engage interested browsers
- ✅ Increase customer lifetime value
- ✅ Provide valuable behavioral insights
- ✅ Cost only ~$2/month to operate
- ✅ Generate $500+ in recovered revenue

**ROI: 25,000%+**
