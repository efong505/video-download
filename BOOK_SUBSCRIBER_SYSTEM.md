# Book Subscriber System - Setup Complete

## What Was Created

### 1. DynamoDB Table
- **Table Name**: `book-subscribers`
- **Primary Key**: `email` (String)
- **Attributes**: email, first_name, subscribed_at, source
- **Billing**: Pay-per-request (no fixed costs)

### 2. Updated Lambda Function
- **Function**: `email-subscription-handler`
- **New Feature**: Handles both election and book subscribers
- **Parameter**: `list_type: "book"` or `list_type: "election"`
- **Book Subscribers**: No confirmation email needed (instant subscribe)
- **Admin Notification**: Sends email to contact@christianconservativestoday.com

### 3. Updated Frontend Files
- **book.html**: Newsletter form now submits to subscription API with `list_type: "book"`
- **admin-book-subscribers.html**: New admin page to view/export book subscribers

## How It Works

### User Subscribes (book.html)
1. User enters email in "Join Our Mailing List" form
2. Form submits to: `https://niexv1rw75.execute-api.us-east-1.amazonaws.com/subscribe`
3. Payload includes: `{email, list_type: "book", source: "book_landing_page"}`
4. Lambda stores in `book-subscribers` table
5. Lambda sends notification email to you
6. User sees success message

### Admin Views Subscribers (admin-book-subscribers.html)
1. Page loads from: `https://niexv1rw75.execute-api.us-east-1.amazonaws.com/list_book_subscribers`
2. Displays table with: Email, Name, Subscribed Date, Source
3. **Export CSV**: Downloads all subscribers as CSV file
4. **Copy Emails**: Copies all email addresses to clipboard (for BCC)

## Key Differences from Election Newsletter

| Feature | Election List | Book List |
|---------|--------------|-----------|
| **Confirmation** | Required (double opt-in) | Not required (instant) |
| **Welcome Email** | Automatic | None |
| **DynamoDB Table** | `email-subscribers` | `book-subscribers` |
| **Admin Notification** | No | Yes (on each signup) |
| **Status Field** | pending/active/unsubscribed | N/A (all active) |

## How to Send Book Updates

### Option 1: Manual Email (Current Setup)
1. Go to `admin-book-subscribers.html`
2. Click "Copy All Emails"
3. Open your email client (Gmail, Outlook, etc.)
4. Paste emails in BCC field
5. Compose and send your update

### Option 2: Export to Mailchimp
1. Go to `admin-book-subscribers.html`
2. Click "Export CSV"
3. Import CSV to Mailchimp
4. Create campaign and send

### Option 3: Use Newsletter System (Future)
- Can integrate with existing newsletter system
- Would need to add "book" campaign type
- Would enable tracking (opens, clicks)

## Files Modified/Created

### Created
- `C:\Users\Ed\Documents\Programming\AWS\Downloader\admin-book-subscribers.html`
- `C:\Users\Ed\Documents\Programming\AWS\Downloader\BOOK_SUBSCRIBER_SYSTEM.md` (this file)

### Modified
- `C:\Users\Ed\Documents\Programming\AWS\Downloader\book.html`
- `C:\Users\Ed\Documents\Programming\AWS\Downloader\email-subscription-handler\lambda_function.py`

## API Endpoints

### Subscribe to Book List
```
POST https://niexv1rw75.execute-api.us-east-1.amazonaws.com/subscribe
Content-Type: application/json

{
  "email": "user@example.com",
  "first_name": "John",
  "list_type": "book",
  "source": "book_landing_page"
}
```

### List Book Subscribers (Admin Only)
```
GET https://niexv1rw75.execute-api.us-east-1.amazonaws.com/list_book_subscribers
```

## Testing

### Test Subscription
1. Go to your book.html page
2. Enter test email in "Join Our Mailing List" form
3. Click "Join the List"
4. Check your contact@christianconservativestoday.com inbox for notification
5. Go to admin-book-subscribers.html to see the subscriber

### Test Admin Page
1. Open `admin-book-subscribers.html`
2. Should see list of subscribers
3. Click "Export CSV" - should download file
4. Click "Copy All Emails" - should copy to clipboard

## Costs

- **DynamoDB**: ~$0.25 per million reads, $1.25 per million writes
- **Lambda**: First 1M requests free per month
- **SES**: $0.10 per 1,000 emails sent
- **Estimated**: <$1/month for first 1,000 subscribers

## Next Steps

1. **Push files to S3**: Upload book.html and admin-book-subscribers.html
2. **Test the flow**: Subscribe with test email
3. **Verify admin page**: Check that subscribers appear
4. **Send first update**: When book launches, use admin page to export/send

## Support

If you need to:
- Add more fields (phone, address, etc.)
- Enable confirmation emails for book list
- Integrate with newsletter system for tracking
- Set up automated welcome emails

Just let me know!
