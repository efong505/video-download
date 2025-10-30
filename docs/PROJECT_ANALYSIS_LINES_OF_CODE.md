# AWS Christian Conservative Platform - Project Analysis

## 📊 Lines of Code Summary

**Total Lines of Code: ~44,176 lines**

### Breakdown by Language

#### Backend (Python): 18,459 lines
- **Lambda Functions (15 APIs): 7,250 lines**
  - admin_api: 549 lines
  - articles_api: 864 lines (Bible verse integration)
  - auth_api: 312 lines (JWT authentication)
  - comments_api: 440 lines
  - contributors_api: 640 lines (election correspondents)
  - downloader: 323 lines (yt-dlp integration)
  - news_api: 451 lines
  - paypal_billing_api: 892 lines
  - resources_api: 140 lines
  - router: 250 lines (quota management)
  - tag_api: 411 lines
  - thumbnail_generator: 179 lines (FFmpeg)
  - url_analysis_api: 169 lines
  - video_list_api: 56 lines
  - s3_thumbnail_trigger: 77 lines

- **Utility Scripts: 11,209 lines**
  - Election data upload scripts (50 states)
  - Thumbnail generation tools
  - Data migration scripts
  - Database audit tools

#### Frontend (HTML/JavaScript): 24,171 lines
- **59 HTML files** including:
  - Admin dashboard (admin.html)
  - Video gallery & player (videos.html, video-player.html)
  - Article CMS with rich text editor (create-article.html, edit-article.html)
  - Election map (election-map.html) - Interactive SVG
  - News management (news.html, create-news.html)
  - User authentication & profiles (login.html, profile.html)
  - Resource library (resources.html)
  - Draft management (draft-manager.html)

#### DevOps (PowerShell): 1,546 lines
- **49 deployment and automation scripts**
  - Lambda deployment automation
  - S3 sync scripts
  - Log monitoring tools
  - Cost calculators
  - Diagnostic utilities

---

## 🏗️ System Architecture

### How It Works

#### 1. Video Download System
```
User Request → API Gateway → Router Lambda (quota check)
                                    ↓
                            Downloader Lambda (yt-dlp)
                                    ↓
                            FFmpeg Processing
                                    ↓
                            S3 Upload (videos)
                                    ↓
                            S3 Event Trigger
                                    ↓
                            Thumbnail Generator
                                    ↓
                            DynamoDB Metadata
```

**Flow Details:**
1. User submits video URL through web interface
2. Router Lambda validates request and checks quota limits
3. Downloader Lambda uses yt-dlp to download from YouTube/Rumble
4. FFmpeg processes and compresses video
5. Video uploaded to S3 bucket
6. S3 event triggers thumbnail generation Lambda
7. Thumbnail Generator creates preview image
8. Metadata stored in DynamoDB Videos table

#### 2. Content Management System
```
Admin Interface → Admin API → DynamoDB (Articles/News)
                           ↓
                    S3 (images/media)
                           ↓
Public Site ← Articles API ← DynamoDB
            ← Video List API
```

**Flow Details:**
1. Admin creates content using rich text or markdown editor
2. Admin API validates and stores in DynamoDB
3. Images uploaded to S3
4. Public site retrieves content via Articles API
5. Bible verses fetched from integrated API (KJV, ASV, YLT)

#### 3. Election Tracking System
```
CSV Data → Python Upload Scripts → DynamoDB (Races/Candidates/Summaries)
                                         ↓
                            Contributors API
                                         ↓
                            Interactive Map (election-map.html)
                                         ↓
                            PDF/TXT Export
```

**Flow Details:**
1. Election data prepared in CSV format (50 states)
2. Python scripts upload to DynamoDB tables
3. Contributors API serves data to frontend
4. Interactive SVG map displays state-by-state information
5. Users can export voter guides as PDF/TXT

#### 4. Authentication Flow
```
User Login → Auth API → JWT Token Generation
                     ↓
            Protected Routes → JWT Validation
                     ↓
            Role-Based Access (admin/contributor/user)
```

**Flow Details:**
1. User submits credentials
2. Auth API validates against DynamoDB Users table
3. JWT token generated with user role
4. Token stored in localStorage
5. Protected routes validate token on each request
6. Role-based permissions enforced

---

## ☁️ AWS Infrastructure

### Services Used

**Compute:**
- **AWS Lambda**: 15 serverless functions (Python 3.12)
- **Memory**: 512MB - 3008MB per function
- **Timeout**: 15 seconds - 15 minutes
- **Concurrency**: Reserved for router (10)

**Storage:**
- **Amazon S3**: 
  - Video storage bucket (techcross-videos)
  - Static website hosting
  - CloudFront CDN distribution
  - Lifecycle policies for cost optimization

**Database:**
- **Amazon DynamoDB**: 8+ tables
  - Videos
  - Articles
  - News
  - Users
  - Comments
  - Tags
  - Resources
  - Contributors
  - Analytics
  - Races
  - Candidates
  - Summaries
- **Billing Mode**: On-demand
- **Indexes**: Global secondary indexes for queries

**API & Networking:**
- **API Gateway**: RESTful endpoints for all Lambda functions
- **CloudFront**: CDN for content delivery
- **CORS**: Enabled for cross-origin requests

**Monitoring:**
- **CloudWatch**: Logs and metrics for all Lambda functions
- **Custom Metrics**: Download tracking, quota monitoring

---

## 🎯 Key Features

### Video Management
- Multi-platform video downloading (YouTube, Rumble, etc.)
- Automatic thumbnail generation with S3 triggers
- FFmpeg video processing and compression
- Quota management and download status tracking
- S3-based video storage and CloudFront delivery
- Video gallery with categorization and tagging
- External video URL embedding

### Content Management
- Rich text article editor with markdown support
- Bible verse lookup and integration (KJV, ASV, YLT translations)
- News article creation and management
- Draft management system
- Category and tag organization
- Author profiles and contributor management
- Comment system for user engagement
- Article analytics and tracking
- Related articles suggestions

### Election Tracking
- Interactive SVG US map with state-specific data
- Complete database of 2025-2026 races (all 50 states)
- Candidate profiles with faith statements and positions
- Dual-mode editor (Markdown/Rich Text) for state summaries
- Comprehensive voter guides (20-30 pages per state)
- CSV import for bulk candidate/race data
- PDF and TXT export capabilities
- Church mobilization strategies
- State correspondent system

### Authentication & Billing
- JWT-based authentication system
- Role-based access control (admin, contributor, user)
- PayPal subscription billing integration
- User profiles and permissions
- Subscription tier management (Free, Premium, Pro, Enterprise)

---

## 📈 Data Scale

### Election Data Coverage
- **50 US States**: Complete coverage
- **Election Cycles**: 2025-2026
- **Races**: Thousands tracked (Governor, Senate, House, State Legislature)
- **Candidates**: Comprehensive profiles with faith statements
- **Voter Guides**: 20-30 pages per state

### Content Scale
- Videos: Unlimited storage capacity
- Articles: Full CMS with versioning
- News: Real-time publishing
- Comments: User engagement tracking
- Tags: Hierarchical categorization

---

## 🔧 Development Workflow

### Standard Development Process
1. **Code** → Write Lambda function or HTML page
2. **Test Locally** → Use test-*.html files
3. **Deploy** → Run PowerShell script (deploy-*.ps1)
4. **Verify** → Check AWS Console
5. **Monitor** → CloudWatch logs (live-logs.ps1)
6. **Iterate** → Fix issues, redeploy

### Deployment Commands
```powershell
# Deploy all Lambda functions
.\deploy-all.ps1

# Deploy specific function
.\deploy-router.ps1
.\deploy-articles-api.ps1

# Deploy election system
.\deploy-election-system.ps1

# Push static files to S3
.\s3-push.ps1

# Monitor logs in real-time
.\live-logs.ps1

# Check Lambda status
.\check-lambda-status.ps1
```

### Testing Strategy
- Unit tests for Lambda functions
- Integration tests with test HTML files
- Manual testing through admin interface
- CloudWatch monitoring for production issues

---

## 💰 Cost Optimization

### Serverless Architecture Benefits
- **Pay-per-use pricing**: Only charged for actual usage
- **Automatic scaling**: Handles traffic spikes without manual intervention
- **No server management**: AWS manages infrastructure
- **Cost-effective**: Minimal costs during low usage periods

### Optimization Strategies
- On-demand DynamoDB billing (no reserved capacity)
- S3 lifecycle policies (archive old videos)
- Lambda reserved concurrency for critical functions only
- CloudFront caching reduces origin requests
- Efficient Lambda memory allocation per function

### Cost Monitoring
- PowerShell cost calculator scripts
- CloudWatch billing alarms
- Regular cost analysis and optimization

---

## 🎓 Complexity Analysis

### High Complexity Components
- **Video Processing Pipeline**: yt-dlp + FFmpeg integration, S3 triggers
- **Election Data Management**: 50 states × multiple races, CSV imports
- **Bible Verse API Integration**: Multi-translation support
- **PayPal Billing Integration**: Subscription management, webhooks
- **Dual-Mode Editor**: Markdown/Rich Text with content detection

### Medium Complexity Components
- **Authentication & Authorization**: JWT tokens, role-based access
- **Comment System**: Nested comments, moderation
- **Analytics Tracking**: View counts, engagement metrics
- **Resource Management**: File uploads, categorization

### Low Complexity Components
- **Static Content Delivery**: S3 + CloudFront
- **Basic CRUD Operations**: DynamoDB queries
- **Tag Management**: Simple categorization

---

## 🎯 Target Users

### Primary Users
- **Church Leaders**: Access voter guides and election resources
- **Christian Conservatives**: Track candidates aligned with faith values
- **Content Creators**: Publish articles and manage video content
- **Ministry Organizations**: Distribute faith-based content

### User Roles
- **Administrators**: Full system access, content moderation, user management
- **Contributors**: Create and edit articles, manage resources
- **Subscribers**: Access premium content, download voter guides
- **Public Users**: View articles, videos, and basic election information

---

## 🚀 Production Readiness

### Completed Features
✅ All 50 states election data uploaded  
✅ Video download and processing pipeline  
✅ Article CMS with Bible verse integration  
✅ News management system  
✅ User authentication and authorization  
✅ PayPal subscription billing  
✅ Interactive election map  
✅ Voter guide generation  
✅ Comment system  
✅ Analytics tracking  
✅ Resource library  
✅ PWA support with service worker  

### System Status
- **Lambda Functions**: All running Python 3.12 (AWS compliant)
- **Database**: DynamoDB tables optimized
- **Storage**: S3 buckets configured with CloudFront
- **Monitoring**: CloudWatch logs and metrics active
- **Security**: JWT authentication, role-based access control

---

## 📝 Documentation

### Available Documentation
- `README.md` - Main project documentation
- `TECHNICAL_DOCUMENTATION.md` - Architecture details
- `DEPLOYMENT_SUMMARY.md` - Deployment guide
- `PROGRESS.md` - Project status (ALL 50 STATES COMPLETE)
- `NEWS_MANAGEMENT_SYSTEM.md` - News system documentation
- `ARTICLE_ANALYTICS.md` - Analytics features
- `DYNAMODB_QUERY_GUIDE.md` - Database query reference
- `aws-commands-guide.md` - AWS CLI commands

### Code Comments
- Lambda functions include inline documentation
- HTML files have section comments
- PowerShell scripts include usage instructions

---

## 🔐 Security Features

### Authentication
- JWT token-based authentication
- Secure password hashing
- Token expiration and refresh
- Role-based access control

### Data Protection
- HTTPS only (CloudFront SSL)
- DynamoDB encryption at rest
- S3 bucket policies (public read, authenticated write)
- Input validation and sanitization (DOMPurify)

### Monitoring
- CloudWatch logs for all Lambda functions
- Failed login attempt tracking
- API Gateway request logging
- CloudTrail for audit logs

---

## 📊 Summary

This is a **full-stack serverless application** combining:
- Video content management
- Article publishing with Bible integration
- Comprehensive election tracking (50 states)
- User authentication and billing
- Faith-based civic engagement tools

**Total Codebase**: ~44,176 lines  
**Architecture**: AWS Serverless (Lambda, DynamoDB, S3, CloudFront)  
**Target Audience**: Christian conservative organizations and churches  
**Status**: Production-ready with all 50 states complete  
**Compliance**: Python 3.12 (AWS Lambda compliant through 2029)

The platform serves as a complete digital ministry and civic engagement tool for faith-based organizations across the United States.
