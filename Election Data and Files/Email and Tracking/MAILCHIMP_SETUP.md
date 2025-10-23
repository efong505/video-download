# Mailchimp Integration Setup Guide

## Step 1: Create Mailchimp Account
1. Go to https://mailchimp.com/
2. Sign up for free account (up to 500 subscribers free)
3. Verify your email

## Step 2: Create Audience (Mailing List)
1. In Mailchimp dashboard, go to **Audience** → **All contacts**
2. Click **Create Audience** (or use default audience)
3. Name it: "Election Map Subscribers"
4. Fill in required fields (your email, organization name, etc.)

## Step 3: Get Your Mailchimp Form Action URL

### Method A: Embedded Form (Easiest)
1. Go to **Audience** → **Signup forms**
2. Click **Embedded forms**
3. Select **Classic** form
4. Look for the form code that looks like:
   ```html
   <form action="https://YOURDOMAIN.us1.list-manage.com/subscribe/post?u=XXXXX&amp;id=YYYYY" method="post">
   ```
5. Copy the entire URL from `action="..."` (this is your FORM_ACTION_URL)

### Method B: API Integration (More Control)
1. Go to **Account** → **Settings** → **Extras** → **API keys**
2. Click **Create A Key**
3. Copy your API key
4. Get your Audience ID:
   - Go to **Audience** → **Settings** → **Audience name and defaults**
   - Look for **Audience ID** (looks like: a1b2c3d4e5)

## Step 4: Update election-map.html

Replace the `subscribeEmail()` function with the code below.

### For Embedded Form (No API Key Needed):
```javascript
async function subscribeEmail() {
    const emailInput = document.getElementById('email-input');
    const email = emailInput.value.trim();

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        alert('Please enter a valid email address.');
        return;
    }

    // Replace with YOUR Mailchimp form action URL
    const MAILCHIMP_URL = 'https://YOURDOMAIN.us1.list-manage.com/subscribe/post-json?u=XXXXX&id=YYYYY';
    
    try {
        const url = MAILCHIMP_URL + '&EMAIL=' + encodeURIComponent(email) + '&c=?';
        
        await fetch(url, {
            method: 'GET',
            mode: 'no-cors'
        });

        const banner = document.getElementById('email-capture-banner');
        banner.innerHTML = '<div class="text-center py-3">' +
            '<h5 class="text-success mb-2">✓ Thank You for Subscribing!</h5>' +
            '<p class="mb-0">You\'ll receive election updates at <strong>' + email + '</strong></p>' +
            '<small class="text-muted">Check your inbox for a confirmation email.</small>' +
            '</div>';
    } catch (error) {
        console.error('Subscription error:', error);
        alert('There was an error subscribing. Please try again.');
    }
}
```

### For API Integration (More Reliable):
You'll need a backend Lambda function. Let me know if you want this approach.

## Step 5: Test Your Integration
1. Upload updated election-map.html to your server
2. Visit the page and enter a test email
3. Check Mailchimp dashboard → **Audience** → **All contacts**
4. Verify the email appears in your list
5. Check your email for Mailchimp's confirmation message

## Step 6: Customize Confirmation Email (Optional)
1. Go to **Audience** → **Signup forms** → **Form builder**
2. Click **Settings** → **Confirmation email**
3. Customize the message subscribers receive
4. Add your branding and welcome message

## Important Notes:
- Mailchimp requires **double opt-in** by default (subscribers must confirm via email)
- Free plan: 500 subscribers, 1,000 emails/month
- Subscribers won't receive emails until they click confirmation link
- You can disable double opt-in in Audience Settings (not recommended for compliance)

## Troubleshooting:
- **No emails appearing**: Check spam folder, verify form URL is correct
- **CORS errors**: Use the `post-json` endpoint with `mode: 'no-cors'`
- **"Already subscribed" error**: This is normal, Mailchimp prevents duplicates
- **Rate limiting**: Mailchimp may block rapid test submissions

## Next Steps After Setup:
1. Create welcome email campaign in Mailchimp
2. Set up automated emails for new subscribers
3. Create segments (by state, interests, etc.)
4. Design email templates for election updates
