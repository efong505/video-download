# PayPal Live Production Setup Guide

## Step 1: Get Live PayPal Credentials

1. Log in to [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/)
2. Click **"Switch to Live"** toggle in the top right
3. Go to **My Apps & Credentials**
4. Under **Live** section, click **"Create App"**
5. Name your app (e.g., "Video Platform Billing")
6. Copy the **Client ID** and **Secret**

## Step 2: Update Lambda Environment Variables

Run this AWS CLI command to update the Lambda function:

```powershell
aws lambda update-function-configuration `
  --function-name paypal_billing_api `
  --environment "Variables={
    PAYPAL_CLIENT_ID=YOUR_LIVE_CLIENT_ID,
    PAYPAL_CLIENT_SECRET=YOUR_LIVE_CLIENT_SECRET,
    PAYPAL_BASE_URL=https://api-m.paypal.com
  }"
```

**Replace:**
- `YOUR_LIVE_CLIENT_ID` with your live Client ID
- `YOUR_LIVE_CLIENT_SECRET` with your live Secret

## Step 3: Create Live Subscription Plans

The Lambda function creates plans dynamically, but you can pre-create them:

### Premium Plan ($9.99/month)
```bash
# Get access token first
curl -v https://api-m.paypal.com/v1/oauth2/token \
  -H "Accept: application/json" \
  -H "Accept-Language: en_US" \
  -u "CLIENT_ID:SECRET" \
  -d "grant_type=client_credentials"

# Create product
curl -v -X POST https://api-m.paypal.com/v1/catalogs/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -d '{
    "name": "Video Platform Premium",
    "description": "Premium video hosting plan",
    "type": "SERVICE",
    "category": "SOFTWARE"
  }'

# Create plan (use product_id from above)
curl -v -X POST https://api-m.paypal.com/v1/billing/plans \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -d '{
    "product_id": "PRODUCT_ID",
    "name": "Premium Plan",
    "billing_cycles": [{
      "frequency": {"interval_unit": "MONTH", "interval_count": 1},
      "tenure_type": "REGULAR",
      "sequence": 1,
      "total_cycles": 0,
      "pricing_scheme": {
        "fixed_price": {"value": "9.99", "currency_code": "USD"}
      }
    }],
    "payment_preferences": {
      "auto_bill_outstanding": true,
      "setup_fee_failure_action": "CONTINUE",
      "payment_failure_threshold": 3
    }
  }'
```

### Pro Plan ($24.99/month)
Same process, change price to "24.99"

### Enterprise Plan ($99.99/month)
Same process, change price to "99.99"

## Step 4: Configure Webhooks (Optional but Recommended)

1. In PayPal Developer Dashboard → **Webhooks**
2. Click **"Add Webhook"**
3. Enter your webhook URL: `https://your-api-gateway-url/paypal?action=webhook`
4. Select events:
   - `BILLING.SUBSCRIPTION.ACTIVATED`
   - `BILLING.SUBSCRIPTION.CANCELLED`
   - `BILLING.SUBSCRIPTION.SUSPENDED`
   - `BILLING.SUBSCRIPTION.UPDATED`
   - `PAYMENT.SALE.COMPLETED`

## Step 5: Test the Connection

```powershell
# Test PayPal API connection
curl "https://your-api-gateway-url/paypal?action=test"
```

## Step 6: Update Frontend URLs

If you have hardcoded return/cancel URLs in your frontend, update them to production URLs:

```javascript
return_url: 'https://christianconservativestoday.com/profile.html'
cancel_url: 'https://christianconservativestoday.com/profile.html'
```

## Environment Variables Summary

| Variable | Sandbox Value | Live Value |
|----------|--------------|------------|
| `PAYPAL_CLIENT_ID` | Sandbox Client ID | Live Client ID |
| `PAYPAL_CLIENT_SECRET` | Sandbox Secret | Live Secret |
| `PAYPAL_BASE_URL` | `https://api-m.sandbox.paypal.com` | `https://api-m.paypal.com` |

## Verification Checklist

- [ ] Live PayPal credentials obtained
- [ ] Lambda environment variables updated
- [ ] Test connection successful
- [ ] Subscription plans created (or dynamic creation working)
- [ ] Webhooks configured
- [ ] Frontend URLs updated
- [ ] Test subscription flow end-to-end

## Rollback Plan

If issues occur, revert to sandbox:

```powershell
aws lambda update-function-configuration `
  --function-name paypal_billing_api `
  --environment "Variables={
    PAYPAL_CLIENT_ID=SANDBOX_CLIENT_ID,
    PAYPAL_CLIENT_SECRET=SANDBOX_CLIENT_SECRET,
    PAYPAL_BASE_URL=https://api-m.sandbox.paypal.com
  }"
```
