# CloudVault - Storage Subscription Service

> A complete, production-ready cloud storage subscription platform built on AWS serverless architecture with Stripe payment integration.

![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20S3%20%7C%20DynamoDB-orange)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Stripe](https://img.shields.io/badge/Stripe-Payments-blueviolet)
![License](https://img.shields.io/badge/License-MIT-green)

## 🚀 Features

### For End Users
- ✅ **Free Tier** - 1GB storage for all users
- 💳 **Paid Plans** - Basic (10GB), Pro (100GB), Business (1TB)
- 📁 **File Management** - Upload, download, delete with drag-and-drop
- 🔒 **Secure Storage** - Files encrypted in S3
- 📊 **Real-time Dashboard** - Live storage usage tracking
- 📱 **Responsive Design** - Works on all devices

### For Administrators
- 📈 **Analytics Dashboard** - Real-time statistics
- 👥 **User Management** - View, edit, delete users
- 💰 **Revenue Tracking** - Monthly revenue calculations
- 📊 **Visual Charts** - Subscription distribution graphs
- 🔍 **Storage Analytics** - Total usage across platform

### Technical Features
- ⚡ **Serverless** - AWS Lambda, API Gateway, DynamoDB, S3
- 🔐 **JWT Authentication** - Secure token-based auth
- 💳 **Stripe Integration** - Subscription billing
- 🌐 **CORS Enabled** - Cross-origin support
- 📈 **Auto-scaling** - Handles any load
- 💰 **Cost-effective** - Pay only for what you use

## 📋 Quick Start

Get up and running in 15 minutes! See [QUICKSTART.md](docs/QUICKSTART.md)

```powershell
# 1. Deploy infrastructure
cd scripts
.\create-infrastructure.ps1

# 2. Configure frontend
# Edit frontend/config.js with your API URL

# 3. Deploy frontend
.\deploy-frontend.ps1

# Done! 🎉
```

## 📁 Project Structure

```
Storage Subscription Service/
├── lambda/                     # Backend Lambda functions
│   ├── auth_api/              # User authentication & JWT
│   ├── storage_api/           # File upload/download/delete
│   ├── subscription_api/      # Stripe payment integration
│   └── admin_api/             # Admin dashboard & analytics
│
├── frontend/                   # Professional web interface
│   ├── index.html             # Landing page
│   ├── dashboard.html         # User dashboard
│   ├── files.html             # File management
│   ├── admin.html             # Admin dashboard
│   └── [6 more pages]
│
├── scripts/                    # Deployment automation
│   ├── create-infrastructure.ps1  # One-click AWS setup
│   ├── deploy-all.ps1            # Deploy Lambda functions
│   └── deploy-frontend.ps1       # Deploy website
│
└── docs/                       # Complete documentation
    ├── README.md              # Full documentation
    ├── QUICKSTART.md          # 15-minute setup guide
    ├── DEPLOYMENT.md          # Detailed deployment
    └── API.md                 # API reference
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (S3 + CloudFront)               │
│  Landing • Login • Dashboard • Files • Admin • Upgrade      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway (REST)                      │
│  /auth • /storage • /subscription • /admin/*                │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┬──────────────┐
         ▼               ▼               ▼              ▼
    ┌────────┐     ┌──────────┐    ┌──────────┐  ┌──────────┐
    │ Auth   │     │ Storage  │    │Subscription│ │  Admin   │
    │ Lambda │     │  Lambda  │    │  Lambda   │  │  Lambda  │
    └────┬───┘     └─────┬────┘    └─────┬─────┘  └─────┬────┘
         │               │               │              │
         └───────────────┼───────────────┼──────────────┘
                         ▼               ▼
              ┌──────────────┐    ┌──────────┐
              │  DynamoDB    │    │    S3    │
              │ Users/Files  │    │  Storage │
              └──────────────┘    └──────────┘
                                        │
                                        ▼
                                  ┌──────────┐
                                  │  Stripe  │
                                  │ Payments │
                                  └──────────┘
```

## 💻 Technology Stack

### Backend
- **AWS Lambda** - Serverless compute (Python 3.12)
- **API Gateway** - RESTful API endpoints
- **DynamoDB** - NoSQL database
- **S3** - File storage
- **IAM** - Security & permissions

### Frontend
- **HTML5/CSS3/JavaScript** - No framework dependencies
- **Bootstrap 5** - Responsive UI
- **Chart.js** - Analytics visualization
- **Stripe.js** - Payment processing

### DevOps
- **PowerShell** - Deployment automation
- **AWS CLI** - Infrastructure management
- **CloudWatch** - Monitoring & logging

## 📊 Pricing Tiers

| Tier | Storage | Price | Features |
|------|---------|-------|----------|
| **Free** | 1 GB | $0/mo | Basic file management |
| **Basic** | 10 GB | $5/mo | Priority support |
| **Pro** | 100 GB | $15/mo | Team collaboration |
| **Business** | 1 TB | $50/mo | Advanced security |

## 💰 Cost Analysis

### AWS Costs (Monthly)

**Development/Testing**
- Free Tier: $0 (first 12 months)
- After Free Tier: ~$2-5

**Production (100 users)**
- Lambda: ~$5
- DynamoDB: ~$5
- S3: ~$10
- API Gateway: ~$5
- **Total: ~$25/month**

**Revenue Example (100 users)**
- 70 free, 20 basic, 8 pro, 2 business
- Revenue: $320/month
- **Profit: ~$295/month**

## 🚀 Deployment

### Prerequisites
- AWS Account with CLI configured
- Python 3.12
- PowerShell 7+
- Stripe Account

### One-Command Deploy

```powershell
cd scripts
.\create-infrastructure.ps1
```

This creates:
- ✅ S3 bucket for file storage
- ✅ DynamoDB tables (Users, Files)
- ✅ 4 Lambda functions
- ✅ API Gateway with routes
- ✅ IAM roles & permissions

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## 📖 Documentation

- **[QUICKSTART.md](docs/QUICKSTART.md)** - Get started in 15 minutes
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Complete deployment guide
- **[API.md](docs/API.md)** - Full API reference
- **[README.md](docs/README.md)** - Detailed documentation

## 🧪 Testing

### Test API Endpoints

```powershell
cd scripts
.\test-api.ps1
```

### Manual Testing

1. **Register**: Create account at `/register.html`
2. **Upload**: Upload file at `/files.html`
3. **Subscribe**: Upgrade at `/upgrade.html`
4. **Admin**: View dashboard at `/admin.html`

## 🔒 Security

- ✅ JWT token authentication (30-day expiration)
- ✅ Password hashing (SHA-256)
- ✅ CORS configuration
- ✅ IAM least privilege access
- ✅ S3 presigned URLs (1-hour expiration)
- ✅ Stripe PCI-DSS compliance

**Production Recommendations:**
- Upgrade to bcrypt for passwords
- Enable CloudFront with SSL
- Add rate limiting
- Implement 2FA
- Enable CloudTrail auditing

## 📈 Monitoring

### CloudWatch Logs

```powershell
# View Lambda logs
aws logs tail /aws/lambda/auth_api --follow

# View API Gateway logs
aws logs tail /aws/apigateway/storage-subscription-api --follow
```

### Metrics
- Lambda invocations & errors
- API Gateway requests & latency
- DynamoDB read/write capacity
- S3 storage & requests

## 🛠️ Customization

### Branding
- Edit `frontend/styles.css` for colors
- Update logo in navigation
- Change company name

### Features
- Add file sharing
- Implement folders
- Add file preview
- Enable versioning
- Add team features

### Scaling
- Enable DynamoDB auto-scaling
- Add Lambda reserved concurrency
- Implement CloudFront caching
- Use multi-region deployment

## 🐛 Troubleshooting

### Common Issues

**CORS Error**
```powershell
# Verify API Gateway CORS
aws apigatewayv2 get-api --api-id YOUR_API_ID
```

**Lambda Timeout**
```powershell
# Increase timeout
aws lambda update-function-configuration --function-name auth_api --timeout 30
```

**Stripe Webhook Failed**
```powershell
# Check webhook logs in Stripe Dashboard
# Verify webhook secret in Lambda environment
```

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for more solutions.

## 🗺️ Roadmap

- [ ] File sharing with public links
- [ ] Folder organization
- [ ] File versioning
- [ ] Team collaboration
- [ ] Mobile app (React Native)
- [ ] File preview (images, PDFs)
- [ ] Search functionality
- [ ] Activity logs
- [ ] Two-factor authentication
- [ ] Email notifications
- [ ] API rate limiting
- [ ] Multi-region support

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## 💬 Support

- **Documentation**: See `/docs` folder
- **Issues**: Open GitHub issue
- **Email**: support@yourdomain.com

## 🙏 Acknowledgments

- **AWS** - Serverless infrastructure
- **Stripe** - Payment processing
- **Bootstrap** - UI framework
- **Chart.js** - Data visualization

## ⭐ Show Your Support

If this project helped you, please give it a ⭐!

---

**Built with ❤️ using AWS Serverless**

Ready to launch your own cloud storage business? Get started now! 🚀
