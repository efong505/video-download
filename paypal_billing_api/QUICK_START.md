# PayPal Live Setup - Quick Start

## 1. Get Live Credentials

Go to https://developer.paypal.com/dashboard/
- Switch to **Live** mode (toggle top right)
- Go to **My Apps & Credentials**
- Create new app or use existing
- Copy **Client ID** and **Secret**

## 2. Deploy Updated Lambda

```powershell
.\deploy-paypal.ps1
```

## 3. Update Environment Variables

```powershell
.\update-paypal-env.ps1 -ClientId "YOUR_LIVE_CLIENT_ID" -ClientSecret "YOUR_LIVE_SECRET"
```

Or manually via AWS CLI:

```powershell
aws lambda update-function-configuration `
  --function-name paypal_billing_api `
  --environment "Variables={PAYPAL_CLIENT_ID=YOUR_ID,PAYPAL_CLIENT_SECRET=YOUR_SECRET,PAYPAL_BASE_URL=https://api-m.paypal.com}"
```

## 4. Test Connection

```powershell
# Get your API Gateway URL
aws lambda get-function --function-name paypal_billing_api --query 'Configuration.FunctionArn'

# Test endpoint
curl "https://YOUR_API_GATEWAY_URL/paypal?action=test"
```

Expected response:
```json
{
  "status": "success",
  "message": "PayPal API connection successful (LIVE)",
  "environment": "LIVE",
  "base_url": "https://api-m.paypal.com",
  "credentials_configured": true
}
```

## 5. Verify in AWS Console

1. Go to AWS Lambda Console
2. Open `paypal_billing_api` function
3. Click **Configuration** → **Environment variables**
4. Verify:
   - `PAYPAL_CLIENT_ID` = Your live Client ID
   - `PAYPAL_CLIENT_SECRET` = Your live Secret
   - `PAYPAL_BASE_URL` = `https://api-m.paypal.com`

## Environment Variables

| Variable | Value |
|----------|-------|
| `PAYPAL_CLIENT_ID` | Your live PayPal Client ID |
| `PAYPAL_CLIENT_SECRET` | Your live PayPal Secret |
| `PAYPAL_BASE_URL` | `https://api-m.paypal.com` (live) or `https://api-m.sandbox.paypal.com` (sandbox) |

## Troubleshooting

### "PayPal credentials not configured"
- Environment variables not set
- Run `update-paypal-env.ps1` script

### "Failed to get PayPal access token"
- Invalid credentials
- Check Client ID and Secret are correct
- Verify you're using **Live** credentials, not Sandbox

### "SANDBOX" showing instead of "LIVE"
- `PAYPAL_BASE_URL` still set to sandbox
- Update to `https://api-m.paypal.com`

## Rollback to Sandbox

```powershell
aws lambda update-function-configuration `
  --function-name paypal_billing_api `
  --environment "Variables={PAYPAL_CLIENT_ID=SANDBOX_ID,PAYPAL_CLIENT_SECRET=SANDBOX_SECRET,PAYPAL_BASE_URL=https://api-m.sandbox.paypal.com}"
```
