# CloudVault - Storage Subscription Service

A complete cloud storage subscription platform built on AWS serverless architecture with Stripe payment integration.

## Features

### User Features
- **Free Tier**: 1GB storage for all users
- **Paid Tiers**: Basic (10GB), Pro (100GB), Business (1TB)
- **File Management**: Upload, download, delete files with drag-and-drop
- **Secure Storage**: Files encrypted in S3 with presigned URLs
- **Real-time Updates**: Live storage usage tracking
- **Responsive Design**: Works on desktop, tablet, and mobile

### Admin Features
- **Dashboard**: Real-time statistics and analytics
- **User Management**: View, edit, and delete users
- **Revenue Tracking**: Monthly revenue calculations
- **Storage Analytics**: Total storage usage across all users
- **Subscription Distribution**: Visual charts of tier breakdown

### Technical Features
- **Serverless Architecture**: AWS Lambda, API Gateway, DynamoDB, S3
- **JWT Authentication**: Secure token-based authentication
- **Stripe Integration**: Subscription billing and payment processing
- **CORS Enabled**: Cross-origin resource sharing configured
- **Scalable**: Automatic scaling with AWS services

## Architecture

```
Frontend (S3 + CloudFront)
    ↓
API Gateway
    ↓
Lambda Functions
    ├── auth_api (Registration, Login, JWT)
    ├── storage_api (Upload, Download, Delete)
    ├── subscription_api (Stripe Checkout, Webhooks)
    └── admin_api (User Management, Statistics)
    ↓
DynamoDB (StorageUsers, StorageFiles)
S3 (File Storage)
```

## Project Structure

```
Storage Subscription Service/
├── lambda/                  # Lambda function code
│   ├── auth_api/           # Authentication
│   ├── storage_api/        # File operations
│   ├── subscription_api/   # Stripe integration
│   └── admin_api/          # Admin operations
├── frontend/               # HTML/CSS/JS files
│   ├── index.html         # Landing page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # User dashboard
│   ├── files.html         # File management
│   ├── upgrade.html       # Subscription upgrade
│   ├── admin.html         # Admin dashboard
│   ├── config.js          # API configuration
│   ├── auth.js            # Auth helpers
│   └── styles.css         # Custom styles
├── scripts/               # Deployment scripts
│   ├── create-infrastructure.ps1
│   ├── deploy-all.ps1
│   └── deploy-frontend.ps1
└── docs/                  # Documentation
    ├── README.md
    ├── DEPLOYMENT.md
    └── API.md
```

## Prerequisites

- AWS Account with CLI configured
- Python 3.12
- PowerShell 7+
- Stripe Account (for payments)
- Node.js (optional, for local testing)

## Quick Start

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed setup instructions.

### 1. Create Infrastructure

```powershell
cd scripts
.\create-infrastructure.ps1
```

This creates:
- S3 bucket for file storage
- DynamoDB tables (StorageUsers, StorageFiles)
- Lambda functions (auth_api, storage_api, subscription_api, admin_api)
- API Gateway with routes
- IAM roles and permissions

### 2. Configure Stripe

1. Create a Stripe account at https://stripe.com
2. Get your API keys from the Stripe Dashboard
3. Create products and prices in Stripe:
   - Basic: $5/month (price_basic)
   - Pro: $15/month (price_pro)
   - Business: $50/month (price_business)
4. Update Lambda environment variables with Stripe keys

### 3. Update Configuration

Edit `frontend/config.js`:
```javascript
const API_URL = 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod';
const STRIPE_PUBLIC_KEY = 'pk_test_YOUR_KEY';
```

### 4. Deploy Frontend

```powershell
.\deploy-frontend.ps1
```

### 5. Access Your Application

Visit the S3 website URL provided after deployment.

## Usage

### For Users

1. **Sign Up**: Create a free account (1GB storage)
2. **Upload Files**: Drag and drop or click to upload
3. **Manage Files**: Download or delete files
4. **Upgrade**: Choose a paid plan for more storage

### For Admins

1. **Login**: Use admin email configured in Lambda
2. **View Dashboard**: See statistics and analytics
3. **Manage Users**: View, edit, or delete users
4. **Track Revenue**: Monitor subscription revenue

## API Endpoints

### Authentication
- `POST /auth` - Register, login, verify token

### Storage
- `GET /storage` - List files
- `POST /storage` - Upload file
- `DELETE /storage?fileName=X` - Delete file

### Subscription
- `POST /subscription` - Create checkout, cancel subscription
- `GET /subscription?action=get_status` - Get subscription status

### Admin
- `GET /admin/users` - List all users
- `DELETE /admin/users?email=X` - Delete user
- `PUT /admin/users` - Update user
- `GET /admin/stats` - Get statistics

See [API.md](API.md) for detailed API documentation.

## Cost Estimation

### Free Tier (AWS)
- Lambda: 1M requests/month free
- DynamoDB: 25GB storage free
- S3: 5GB storage free
- API Gateway: 1M requests/month free

### Estimated Monthly Costs (after free tier)
- **10 users**: ~$2-5/month
- **100 users**: ~$20-40/month
- **1000 users**: ~$150-300/month

Costs vary based on:
- Storage usage
- API requests
- Data transfer
- Lambda execution time

## Security

- **JWT Tokens**: Secure authentication with 30-day expiration
- **Password Hashing**: SHA-256 hashing (upgrade to bcrypt recommended)
- **CORS**: Configured for cross-origin requests
- **IAM Roles**: Least privilege access for Lambda functions
- **Presigned URLs**: Temporary access to S3 objects
- **Stripe**: PCI-DSS compliant payment processing

## Monitoring

- **CloudWatch Logs**: Lambda function logs
- **CloudWatch Metrics**: API Gateway and Lambda metrics
- **DynamoDB Metrics**: Read/write capacity usage
- **S3 Metrics**: Storage and request metrics

## Troubleshooting

See [DEPLOYMENT.md](DEPLOYMENT.md) for common issues and solutions.

## Future Enhancements

- [ ] File sharing with public links
- [ ] Folder organization
- [ ] File versioning
- [ ] Team collaboration features
- [ ] Mobile app
- [ ] File preview (images, PDFs)
- [ ] Search functionality
- [ ] Activity logs
- [ ] Two-factor authentication
- [ ] Email notifications

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [Your Repo URL]
- Email: support@yourdomain.com
- Documentation: [Your Docs URL]

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

## Acknowledgments

- AWS for serverless infrastructure
- Stripe for payment processing
- Bootstrap for UI components
- Chart.js for analytics visualization
