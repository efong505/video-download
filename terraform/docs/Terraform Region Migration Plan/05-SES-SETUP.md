# Phase 5: SES Setup in New Region

## Objective

Amazon SES (Simple Email Service) identities, sending limits, and configuration are region-specific. When migrating to a new region, you must re-verify your sending domain, request production access, and configure event notifications — all before the cutover.

## Risk Level: LOW

SES setup in a new region doesn't affect the existing region. The only risk is the 24-48 hour wait for production access approval.

## Estimated Time: 1 hour of work + 24-48 hours waiting for AWS approval

## Prerequisites

- Target region decided
- AWS CLI configured with `ekewaka` profile
- Access to DNS management (Route53)

---

## Current SES Configuration (us-east-1)

Before migrating, document what exists:

```bash
# List verified identities
aws ses list-identities --profile ekewaka --region us-east-1

# Check sending quota
aws ses get-send-quota --profile ekewaka --region us-east-1

# Check account sending status (sandbox vs production)
aws sesv2 get-account --profile ekewaka --region us-east-1 \
  --query "{ProductionAccess:ProductionAccessEnabled,SendingEnabled:SendingEnabled}"
```

### Expected Current State

| Setting | Value |
|---------|-------|
| Verified Domain | `christianconservativestoday.com` |
| Verified Emails | `hawaiianintucson@gmail.com` (and possibly others) |
| Sending Mode | Production (not sandbox) |
| Daily Sending Limit | Check with `get-send-quota` |
| DKIM | Enabled for domain |
| SNS Notifications | Bounces → `ses-bounces` topic, Events → `ses-email-events` topic |

---

## Step 1: Request Production Access in New Region (DO THIS FIRST)

**This is the longest wait — start it immediately.**

SES starts in sandbox mode in every new region. In sandbox mode, you can only send to verified email addresses (not real users). You must request production access.

### Via AWS Console:
1. Go to SES console in the target region (e.g., `us-west-2`)
2. Click "Request production access"
3. Fill out the form:
   - **Mail type:** Transactional + Marketing
   - **Website URL:** `https://christianconservativestoday.com`
   - **Use case description:** "Migrating existing production email sending from us-east-1. We send transactional emails (account notifications, drip campaigns) and marketing emails (newsletters) to opted-in subscribers. Current sending volume: [check your quota]. We have proper unsubscribe mechanisms and handle bounces/complaints via SNS notifications."
   - **Expected daily volume:** Match your current quota
   - **Bounce/complaint handling:** "We process bounces and complaints via SNS → Lambda pipeline. Bounced addresses are automatically suppressed."

### Via CLI:
```bash
aws sesv2 put-account-details \
  --mail-type TRANSACTIONAL \
  --website-url "https://christianconservativestoday.com" \
  --use-case-description "Migrating production email from us-east-1. Transactional and marketing emails to opted-in subscribers with bounce/complaint handling via SNS." \
  --additional-contact-email-addresses "hawaiianintucson@gmail.com" \
  --production-access-enabled \
  --profile ekewaka --region us-west-2
```

**Expected wait time:** 24-48 hours. AWS reviews the request manually.

---

## Step 2: Verify Domain in New Region

Domain verification is per-region. You need to verify `christianconservativestoday.com` in the target region.

```bash
# Create domain identity in new region
aws sesv2 create-email-identity \
  --email-identity christianconservativestoday.com \
  --profile ekewaka --region us-west-2
```

This returns DKIM tokens. Since you're using Route53, you can use the same DKIM CNAME records — but check if the tokens are different from us-east-1:

```bash
# Get DKIM tokens for new region
aws sesv2 get-email-identity \
  --email-identity christianconservativestoday.com \
  --profile ekewaka --region us-west-2 \
  --query "DkimAttributes.Tokens"
```

### If tokens are different from us-east-1:

You'll need to add new CNAME records in Route53. The old ones stay (for us-east-1) and new ones are added (for the target region). They don't conflict because the CNAME names include region-specific tokens.

```bash
# Format: {token}._domainkey.christianconservativestoday.com → {token}.dkim.amazonses.com
# Add via Route53 console or CLI
```

### If tokens are the same:

No DNS changes needed — the existing CNAME records work for both regions.

### Verify DKIM status:

```bash
# Check verification status (may take a few minutes)
aws sesv2 get-email-identity \
  --email-identity christianconservativestoday.com \
  --profile ekewaka --region us-west-2 \
  --query "DkimAttributes.{Status:DkimStatus,SigningEnabled:SigningEnabled}"
```

Wait until `DkimStatus` is `SUCCESS`.

---

## Step 3: Verify Individual Email Addresses (If Needed)

If you send FROM specific email addresses (not just the domain), verify them too:

```bash
# Verify a specific email address
aws sesv2 create-email-identity \
  --email-identity "noreply@christianconservativestoday.com" \
  --profile ekewaka --region us-west-2
```

If you only send from `@christianconservativestoday.com` addresses and the domain is verified, individual email verification is not needed.

---

## Step 4: Configure SNS Notifications for Bounces/Complaints

Your current setup routes SES events through SNS topics. Recreate this in the new region.

### Terraform handles the SNS topics:

The `ses-bounces` and `ses-email-events` SNS topics are already in your Terraform config. When you deploy to the new region, Terraform creates them automatically.

### Wire SES to SNS (after Terraform deploy):

```bash
# Set bounce notifications
aws sesv2 create-configuration-set-event-destination \
  --configuration-set-name default \
  --event-destination-name bounces \
  --event-destination '{
    "Enabled": true,
    "MatchingEventTypes": ["BOUNCE", "COMPLAINT"],
    "SnsDestination": {
      "TopicArn": "arn:aws:sns:us-west-2:371751795928:ses-bounces"
    }
  }' \
  --profile ekewaka --region us-west-2
```

**Note:** You may need to create a configuration set first if one doesn't exist:

```bash
aws sesv2 create-configuration-set \
  --configuration-set-name default \
  --profile ekewaka --region us-west-2
```

### Add to Terraform (Optional but Recommended)

To make SES configuration fully managed by Terraform, add these resources:

```hcl
resource "aws_ses_domain_identity" "main" {
  domain = "christianconservativestoday.com"
}

resource "aws_ses_domain_dkim" "main" {
  domain = aws_ses_domain_identity.main.domain
}

resource "aws_ses_domain_identity_verification" "main" {
  domain     = aws_ses_domain_identity.main.id
  depends_on = [aws_route53_record.ses_verification]
}

# DKIM DNS records
resource "aws_route53_record" "ses_dkim" {
  count   = 3
  zone_id = data.aws_route53_zone.main.zone_id
  name    = "${aws_ses_domain_dkim.main.dkim_tokens[count.index]}._domainkey"
  type    = "CNAME"
  ttl     = 600
  records = ["${aws_ses_domain_dkim.main.dkim_tokens[count.index]}.dkim.amazonses.com"]
}
```

This ensures SES is set up automatically in any region you deploy to.

---

## Step 5: Update Lambda Environment Variables

Some Lambda functions may have SES-related environment variables or hardcoded region references for email sending. Check:

```bash
# Check which Lambdas reference SES or email
aws lambda list-functions --profile ekewaka --region us-east-1 \
  --query "Functions[].{Name:FunctionName,Env:Environment.Variables}" \
  --output json | findstr -i "ses\|email\|region"
```

Common patterns to look for:
- `SES_REGION` environment variable
- Hardcoded `region_name='us-east-1'` in boto3 SES client calls
- `AWS_REGION` references in email-sending code

If any Lambda code has hardcoded `us-east-1` for SES calls, update it to use `os.environ['AWS_REGION']` (which Lambda sets automatically to the function's region).

---

## Step 6: Suppression List Migration

SES maintains a suppression list (bounced/complained addresses) per region. You should migrate this to prevent sending to known-bad addresses in the new region.

```bash
# Export suppression list from source region
aws sesv2 list-suppressed-destinations \
  --profile ekewaka --region us-east-1 \
  --query "SuppressedDestinationSummaries[].{Email:EmailAddress,Reason:Reason}" \
  --output json > ses-suppression-list.json

# Import each address into target region
# (Script needed — no bulk import API)
```

```python
import boto3
import json

session = boto3.Session(profile_name='ekewaka')
client = session.client('sesv2', region_name='us-west-2')

with open('ses-suppression-list.json') as f:
    addresses = json.load(f)

for addr in addresses:
    client.put_suppressed_destination(
        EmailAddress=addr['Email'],
        Reason=addr['Reason']
    )
    print(f"Suppressed: {addr['Email']} ({addr['Reason']})")
```

---

## Testing

### Test 1: Verify Domain Status

```bash
aws sesv2 get-email-identity \
  --email-identity christianconservativestoday.com \
  --profile ekewaka --region us-west-2 \
  --query "{Verified:VerifiedForSendingStatus,DKIM:DkimAttributes.DkimStatus}"
```

Expected: `Verified: true, DKIM: SUCCESS`

### Test 2: Send Test Email (Sandbox Mode)

While still in sandbox, you can only send to verified addresses:

```bash
aws sesv2 send-email \
  --from-email-address "noreply@christianconservativestoday.com" \
  --destination '{"ToAddresses":["hawaiianintucson@gmail.com"]}' \
  --content '{"Simple":{"Subject":{"Data":"SES Migration Test"},"Body":{"Text":{"Data":"This is a test email from the new region."}}}}' \
  --profile ekewaka --region us-west-2
```

### Test 3: Verify Production Access

```bash
aws sesv2 get-account \
  --profile ekewaka --region us-west-2 \
  --query "{ProductionAccess:ProductionAccessEnabled,SendingEnabled:SendingEnabled,Quota:SendQuota}"
```

Expected after approval: `ProductionAccess: true`

### Test 4: End-to-End Email Flow

After production access is granted:
1. Trigger a drip email via the `email-drip-processor` Lambda in the new region
2. Verify the email arrives
3. Click a tracked link — verify the click is logged in `user-email-events`
4. Check the open pixel loads — verify the open is logged

### Test 5: Bounce Handling

```bash
# SES provides a simulator for testing bounces
aws sesv2 send-email \
  --from-email-address "noreply@christianconservativestoday.com" \
  --destination '{"ToAddresses":["bounce@simulator.amazonses.com"]}' \
  --content '{"Simple":{"Subject":{"Data":"Bounce Test"},"Body":{"Text":{"Data":"Testing bounce handling."}}}}' \
  --profile ekewaka --region us-west-2

# Check that the bounce notification arrived via SNS → Lambda
```

---

## Timeline

| Day | Action |
|-----|--------|
| Day 1 | Request production access + verify domain |
| Day 1 | Add DKIM DNS records if needed |
| Day 1-2 | Wait for DKIM verification (usually minutes) |
| Day 1-3 | Wait for production access approval (24-48 hours) |
| Day 3 | Send test emails, verify bounce handling |
| Day 3 | Migrate suppression list |

**Start this phase early** — the production access wait is the bottleneck.

---

## Checklist

- [ ] Production access requested in target region
- [ ] Domain identity created in target region
- [ ] DKIM tokens added to Route53 (if different from source)
- [ ] DKIM status is SUCCESS
- [ ] Production access approved
- [ ] Test email sent successfully
- [ ] SNS bounce/complaint notifications configured
- [ ] Suppression list migrated
- [ ] Lambda email-sending code uses dynamic region (not hardcoded)
- [ ] SES resources added to Terraform (optional)
- [ ] End-to-end email flow tested (send → receive → track open → track click)
- [ ] Git commit: "Phase 5: SES configuration for region migration"
