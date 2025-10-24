# Email Subscription System - Quick Start

Get up and running in 5 minutes!

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Web Dashboard

**Option A: Web Dashboard (Recommended)**
```bash
# Terminal 1: Start API server
python dashboard_api.py

# Terminal 2: Open dashboard in browser
start dashboard_simple.html
```

**Option B: Command Line**
```bash
# View all subscribers
python manage_subscribers.py list

# Export to CSV
python manage_subscribers.py export subscribers.csv

# View stats
python manage_subscribers.py stats
```

---

## 📊 Web Dashboard Features

Once you open `dashboard_simple.html`, you can:

### Overview Tab
- See total subscribers, active count, opens, and clicks
- View recent subscribers
- See most engaged users

### Subscribers Tab
- View all subscribers in a table
- Search by email
- Unsubscribe/resubscribe users
- Click any row to see detailed activity
- Export to CSV

### Campaigns Tab
- View all email campaigns
- See opens, clicks, and subscribes per campaign
- Track campaign performance

---

## 🎯 Common Tasks

### View Your Subscriber List
```bash
python manage_subscribers.py list
```

### Export Emails to CSV
```bash
python manage_subscribers.py export my_list.csv
```

### Search for Someone
```bash
python manage_subscribers.py search user@example.com
```

### View Statistics
```bash
python manage_subscribers.py stats
```

### Send a Newsletter
```bash
python send_newsletter.py
```

### View Email Analytics
```bash
python analytics_queries.py
```

---

## 🌐 API Endpoints

Your system has these endpoints:

- **Subscribe**: `POST /subscribe`
- **Unsubscribe**: `GET /unsubscribe?email=...`
- **Track Opens**: `GET /track/open/{id}`
- **Track Clicks**: `GET /track/click/{id}`

API Base URL: `https://niexv1rw75.execute-api.us-east-1.amazonaws.com`

---

## 📁 File Overview

| File | Purpose |
|------|---------|
| `dashboard_simple.html` | Web dashboard UI |
| `dashboard_api.py` | Flask API server for dashboard |
| `manage_subscribers.py` | Command-line subscriber management |
| `send_newsletter.py` | Send email campaigns |
| `analytics_queries.py` | View email statistics |
| `lambda_function.py` | AWS Lambda function (deployed) |
| `unsubscribe.html` | Public unsubscribe page |

---

## 🔧 Troubleshooting

### Dashboard shows "Error loading data"
- Make sure `dashboard_api.py` is running
- Check AWS credentials are configured: `aws sts get-caller-identity`

### Command-line tools not working
- Verify AWS credentials: `aws configure list`
- Check DynamoDB tables exist: `aws dynamodb list-tables`

### Subscribers not receiving emails
- Check spam folder
- Verify SES is out of sandbox mode
- Check Lambda logs: `aws logs tail /aws/lambda/email-subscription-handler --since 1h`

---

## 📚 Full Documentation

- **USAGE_GUIDE.md** - Complete usage instructions
- **setup_instructions.md** - Initial setup guide
- **troubleshooting.md** - Common issues and solutions
- **README.md** - System overview

---

## 💡 Tips

1. **Backup your list regularly**: `python manage_subscribers.py export backup.csv`
2. **Monitor engagement**: Check analytics after each campaign
3. **Clean inactive subscribers**: Remove users with 0 opens after 6 months
4. **Test before sending**: Always send test emails first
5. **Use the web dashboard**: It's faster than command-line for most tasks

---

## 🎉 You're Ready!

Your email subscription system is now ready to use. Start by:

1. Opening the web dashboard to see your current subscribers
2. Sending a test newsletter with `send_newsletter.py`
3. Monitoring opens and clicks in the dashboard

For detailed instructions, see **USAGE_GUIDE.md**
