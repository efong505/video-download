# Deploy Email Confirmation & Enhanced Prayer Wall

## Files Created
1. `email_templates.py` - Professional branded email templates
2. `confirm-email.html` - Email confirmation success page
3. `prayer-wall-enhanced.html` - Enhanced prayer wall design
4. `docs/EMAIL_CONFIRMATION_SYSTEM.md` - System documentation
5. `update_newsletter_confirmation.py` - Update instructions

## Deployment Steps

### 1. Update Newsletter API Lambda

```powershell
# Copy email_templates.py to newsletter_api folder
cp email_templates.py newsletter_api/

# Update newsletter_api/index.py with confirmation code
# (See update_newsletter_confirmation.py for code to add)

# Deploy
cd newsletter_api
zip -r function.zip index.py email_templates.py
aws lambda update-function-code --function-name newsletter_api --zip-file fileb://function.zip
cd ..
```

### 2. Update DynamoDB Table

```powershell
# Add confirmation_token attribute (no schema change needed - DynamoDB is schemaless)
# Just update the code - new items will have the field
```

### 3. Upload Frontend Files

```powershell
# Upload new pages
aws s3 cp confirm-email.html s3://my-video-downloads-bucket/
aws s3 cp prayer-wall-enhanced.html s3://my-video-downloads-bucket/

# Update existing subscribe.html message
# Change success message to: "Please check your email to confirm your subscription"
```

### 4. Update subscribe.html

Change the success message in subscribe.html:
```javascript
$('#message').html('<div class="alert alert-success">✓ Please check your email to confirm your subscription!</div>');
```

### 5. Test the Flow

1. Go to subscribe.html
2. Enter email and submit
3. Check email for confirmation link
4. Click link → redirects to confirm-email.html
5. Should see success message
6. Check email for welcome message

## Email Template Customization

Edit `email_templates.py` to customize:
- Logo URL (currently: techcrosslogo.jpg)
- Colors (PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR)
- Email content and messaging
- Links and CTAs

## Prayer Wall Deployment

```powershell
# Option 1: Replace existing prayer-wall.html
aws s3 cp prayer-wall-enhanced.html s3://my-video-downloads-bucket/prayer-wall.html

# Option 2: Keep both (test first)
aws s3 cp prayer-wall-enhanced.html s3://my-video-downloads-bucket/
# Then update navbar links to point to prayer-wall-enhanced.html
```

## Verification Checklist

- [ ] Confirmation email sends with logo and branding
- [ ] Confirmation link works and activates subscriber
- [ ] Welcome email sends after confirmation
- [ ] Subscriber status changes from 'pending' to 'active'
- [ ] Prayer wall displays with new professional design
- [ ] Prayer wall stats update correctly
- [ ] Prayer submission form works
- [ ] "I Prayed" button increments count

## Rollback Plan

If issues occur:
1. Revert newsletter_api Lambda to previous version
2. Change subscribe.html message back to original
3. Subscribers will be added as 'active' immediately (old behavior)

## Next Steps

After confirmation system is working:
1. Add email notifications for prayer requests
2. Add event reminder emails
3. Add comment reply notifications
4. Build analytics dashboard for email engagement
