# Christian Conservatives Today - Technical Documentation

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Core Features](#core-features)
4. [AWS Services Integration](#aws-services-integration)
5. [Data Flow Diagrams](#data-flow-diagrams)
6. [Database Schema](#database-schema)
7. [API Endpoints](#api-endpoints)
8. [Security Architecture](#security-architecture)
9. [Deployment Architecture](#deployment-architecture)

---

## Executive Summary

**Christian Conservatives Today** is a serverless video and article platform built on AWS, designed for the 5-fold ministry (apostles, prophets, evangelists, pastors, teachers), Christian believers, and conservative voices. The platform enables video hosting, article publishing with Bible integration, and community engagement through a fully serverless architecture.

### Key Metrics
- **Architecture**: 100% Serverless (AWS Lambda, S3, DynamoDB, CloudFront)
- **Lambda Functions**: 15+ microservices
- **Database Tables**: 15+ DynamoDB tables
- **Storage**: S3 with CloudFront CDN
- **Authentication**: JWT-based with 24-hour expiration
- **User Roles**: 4-tier system (Super User > Admin > Editor > User)
- **Election Coverage**: ALL 50 US STATES (290+ races, 197+ candidates)
- **Email System**: AWS SES with open/click tracking

### Technology Stack
- **Backend**: Python 3.9+ (AWS Lambda)
- **Frontend**: HTML5, JavaScript, Bootstrap 5, Quill.js
- **Database**: DynamoDB (NoSQL)
- **Storage**: S3 + CloudFront CDN
- **APIs**: API Gateway (REST)
- **Video Processing**: yt-dlp, FFmpeg
- **Notifications**: SNS (Simple Notification Service)

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  (CloudFront CDN: https://christianconservativestoday.com)      │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ index.   │  │ videos.  │  │ articles.│  │ admin.   │      │
│  │ html     │  │ html     │  │ html     │  │ html     │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY (REST)                         │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Auth API │  │ Admin API│  │ TAG API  │  │ Router   │      │
│  │ /auth    │  │ /admin   │  │ /tags    │  │ /download│      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                     │
│  │ Articles │  │ PayPal   │  │ URL      │                     │
│  │ /articles│  │ /paypal  │  │ Analysis │                     │
│  └──────────┘  └──────────┘  └──────────┘                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AWS LAMBDA FUNCTIONS                        │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ auth-api     │  │ admin-api    │  │ tag-api      │         │
│  │ (Auth &      │  │ (User Mgmt)  │  │ (Video Meta) │         │
│  │  JWT)        │  │              │  │              │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ router       │  │ downloader   │  │ articles-api │         │
│  │ (Job Route)  │  │ (yt-dlp)     │  │ (Blog/Bible) │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ paypal-api   │  │ thumbnail    │                            │
│  │ (Billing)    │  │ (FFmpeg)     │                            │
│  └──────────────┘  └──────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DATA & STORAGE LAYER                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────┐          │
│  │              DynamoDB Tables                      │          │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │          │
│  │  │ users    │  │ video-   │  │ articles │      │          │
│  │  │          │  │ metadata │  │          │      │          │
│  │  └──────────┘  └──────────┘  └──────────┘      │          │
│  │  ┌──────────┐                                    │          │
│  │  │ download │                                    │          │
│  │  │ -jobs    │                                    │          │
│  │  └──────────┘                                    │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                  │
│  ┌──────────────────────────────────────────────────┐          │
│  │         S3 Bucket (my-video-downloads-bucket)    │          │
│  │  ┌──────────┐  ┌──────────┐                     │          │
│  │  │ videos/  │  │thumbnails│                     │          │
│  │  │          │  │    /     │                     │          │
│  │  └──────────┘  └──────────┘                     │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ SNS      │  │ Bible API│  │ PayPal   │  │ AWS      │      │
│  │ (Notify) │  │ (Verses) │  │ (Billing)│  │ Bedrock  │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Features

### 1. Video Management System

#### Video Download & Processing
- **Supported Platforms**: YouTube, Rumble, Facebook
- **Processing Engine**: yt-dlp with FFmpeg
- **Smart Routing**: Lambda (< 15 min) or Fargate (> 15 min)
- **Format Selection**: Automatic best quality selection up to 1080p
- **Thumbnail Generation**: 3 thumbnails at 10%, 50%, 90% of duration

#### Video Upload
- **Direct Upload**: S3 presigned URLs for secure uploads
- **File Size Limits**: 500MB for regular users
- **Supported Formats**: MP4, WebM, MOV, AVI
- **Quota Enforcement**: Real-time storage and video count checks

#### External Video Embedding
- **YouTube Integration**: Automatic thumbnail extraction
- **Rumble Support**: Video ID extraction and embedding
- **Facebook Videos**: Basic embed support
- **Platform Detection**: Automatic video type identification

### 2. Article & Blog System

#### Rich Text Editor
- **Editor**: Quill.js with custom toolbar
- **Bible Integration**: Search and insert verses from multiple translations
- **Supported Translations**: KJV, ASV (1901), YLT (NT only)
- **Markdown Support**: Toggle between WYSIWYG and Markdown modes
- **Image Upload**: Featured images with compression

#### Article Templates
1. **Sermon Template**: Scripture → Prayer → Main Points → Application
2. **Political Commentary**: Biblical Foundation → Current Issue → Response
3. **Service Notes**: Date, Speaker, Key Points, Application
4. **Bible Study**: Observation → Interpretation → Application → Prayer

#### Article Features
- **Categories**: Sermons, Politics, Devotionals, Apologetics, Ministry, Bible Study
- **Scripture Tracking**: Automatic extraction of Bible references
- **Reading Time**: Calculated based on word count (200 words/min)
- **View Tracking**: Increment view count on each access
- **Search**: Full-text search across title, content, author, tags
- **Social Sharing**: Facebook, Twitter, LinkedIn integration
- **Public Access**: Non-authenticated users can view public articles

### 3. Authentication & Authorization

#### Three-Tier Role System
```
Super User (Highest Authority)
    ├── Full system access
    ├── Create/delete all roles
    ├── Unlimited storage & videos
    └── Cannot be modified by admins

Admin (Middle Authority)
    ├── User management (except super users)
    ├── Content moderation
    ├── Unlimited storage & videos
    └── Cannot create super users

User (Standard Access)
    ├── Upload videos (quota-limited)
    ├── Create articles
    ├── Manage own content
    └── Subject to subscription limits
```

#### JWT Token System
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: 24 hours
- **Payload**: user_id, email, role, exp
- **Storage**: localStorage (client-side)
- **Validation**: Every API request

### 4. Subscription & Billing System

#### Subscription Tiers
```
FREE TIER
├── Storage: 2GB
├── Videos: 50 maximum
├── Cost: $0/month
└── Features: Basic upload, public/private videos

PREMIUM TIER
├── Storage: 25GB
├── Videos: 500 maximum
├── Cost: $9.99/month
└── Features: Priority processing, custom branding

PRO TIER
├── Storage: 100GB
├── Videos: 2000 maximum
├── Cost: $24.99/month
└── Features: Analytics, API access, bulk operations

ENTERPRISE TIER
├── Storage: Unlimited
├── Videos: Unlimited
├── Cost: $99.99/month
└── Features: White-label, dedicated support
```

#### PayPal Integration
- **Payment Processor**: PayPal Subscriptions API
- **Webhook Events**: Subscription created, cancelled, expired
- **Quota Enforcement**: Pre-upload storage checks
- **Automatic Downgrades**: Daily CloudWatch Events rule
- **Grace Period**: Benefits retained until billing period ends

---

## AWS Services Integration

### Lambda Functions (15+ Total)

#### 1. auth-api
**Purpose**: User authentication and JWT management
**Trigger**: API Gateway (POST /auth)
**Runtime**: Python 3.9
**Memory**: 256 MB
**Timeout**: 30 seconds

**Key Functions**:
- `register_user()`: Create new user accounts
- `login_user()`: Authenticate and generate JWT
- `verify_token()`: Validate JWT tokens
- `change_password()`: Update user passwords

**DynamoDB Access**: users table (read/write)

#### 2. admin-api
**Purpose**: Administrative operations and user management
**Trigger**: API Gateway (GET/POST/PUT/DELETE /admin)
**Runtime**: Python 3.9
**Memory**: 512 MB
**Timeout**: 60 seconds

**Key Functions**:
- `get_all_users()`: List all users with subscription data
- `update_user_role()`: Modify user roles and names
- `delete_user()`: Remove users (with role restrictions)
- `get_all_videos()`: List videos with metadata
- `delete_video()`: Remove videos and thumbnails
- `get_upload_url()`: Generate S3 presigned URLs
- `update_user_subscription()`: Manual subscription adjustments

**AWS Access**: DynamoDB (users, video-metadata), S3 (videos, thumbnails)

#### 3. tag-api
**Purpose**: Video metadata and tag management
**Trigger**: API Gateway (GET/POST/PUT /tags)
**Runtime**: Python 3.9
**Memory**: 512 MB
**Timeout**: 60 seconds

**Key Functions**:
- `add_video_metadata()`: Create video metadata entries
- `get_videos_by_tag()`: Filter videos by tags
- `get_all_tags()`: List unique tags
- `list_all_videos()`: Paginated video listing with category filtering
- `update_video_metadata()`: Modify video details

**Features**:
- Pagination support (24 videos per page)
- Category filtering (sermons, politics, teaching)
- S3 size lookup for local videos
- Visibility-based filtering
- Platform auto-detection for external videos

**AWS Access**: DynamoDB (video-metadata), S3 (head_object for sizes)

#### 4. router
**Purpose**: Job routing and quota enforcement
**Trigger**: API Gateway (POST /download)
**Runtime**: Python 3.9
**Memory**: 256 MB
**Timeout**: 30 seconds

**Key Functions**:
- `lambda_handler()`: Route download requests
- `check_storage_quota()`: Validate user limits
- `get_job_status()`: Track active and recent jobs

**Workflow**:
1. Receive download request
2. Check user storage quota
3. Create job entry in DynamoDB
4. Invoke video-downloader Lambda
5. Send SNS notification

**AWS Access**: DynamoDB (download-jobs, users), Lambda (invoke), SNS (publish)

#### 5. downloader
**Purpose**: Video download and processing
**Trigger**: Lambda invocation from router
**Runtime**: Python 3.9
**Memory**: 3008 MB (maximum)
**Timeout**: 900 seconds (15 minutes)
**Layers**: yt-dlp-layer, ffmpeg-layer

**Key Functions**:
- `lambda_handler()`: Main download orchestration
- `get_best_format()`: Select optimal video format
- `generate_thumbnails()`: Create 3 thumbnails with FFmpeg
- `update_job_status()`: Track progress in DynamoDB

**Processing Steps**:
1. Download video to /tmp using yt-dlp
2. Upload video to S3 (videos/)
3. Generate 3 thumbnails with FFmpeg
4. Upload thumbnails to S3 (thumbnails/)
5. Save metadata to DynamoDB
6. Send completion notification via SNS

**AWS Access**: S3 (upload), DynamoDB (video-metadata, download-jobs), SNS (notify)

#### 6. articles-api
**Purpose**: Blog/article management with Bible integration
**Trigger**: API Gateway (GET/POST/PUT/DELETE /articles)
**Runtime**: Python 3.9
**Memory**: 512 MB
**Timeout**: 60 seconds

**Key Functions**:
- `create_article()`: Create new articles with scripture extraction
- `list_articles()`: List articles with filtering
- `get_article()`: Retrieve single article (public access for public articles)
- `update_article()`: Modify existing articles
- `delete_article()`: Remove articles (role-based permissions)
- `get_bible_verse()`: Fetch verses from Bible API
- `get_article_templates()`: Return pre-built templates
- `search_articles()`: Full-text search with relevance scoring

**Bible API Integration**:
- **Endpoint**: https://bible-api.com
- **Translations**: KJV, ASV, YLT
- **Format**: john3:16 (lowercase, no spaces)
- **Fallback**: KJV for unsupported translations

**AWS Access**: DynamoDB (articles, users for name lookup)

#### 7. paypal-billing-api
**Purpose**: Subscription management and quota enforcement
**Trigger**: API Gateway (POST /paypal)
**Runtime**: Python 3.9
**Memory**: 256 MB
**Timeout**: 30 seconds

**Key Functions**:
- `create_subscription()`: Initialize PayPal subscriptions
- `cancel_subscription()`: Handle cancellations with grace period
- `webhook_handler()`: Process PayPal webhook events
- `get_subscription_status()`: Retrieve user subscription details
- `process_expired_subscriptions()`: Automatic downgrades

**PayPal Events Handled**:
- BILLING.SUBSCRIPTION.CREATED
- BILLING.SUBSCRIPTION.ACTIVATED
- BILLING.SUBSCRIPTION.CANCELLED
- BILLING.SUBSCRIPTION.EXPIRED

**AWS Access**: DynamoDB (users), CloudWatch Events (scheduled downgrades)

#### 8. thumbnail-generator
**Purpose**: Generate thumbnails for uploaded videos
**Trigger**: S3 event (video upload) or manual invocation
**Runtime**: Python 3.9
**Memory**: 1024 MB
**Timeout**: 300 seconds (5 minutes)
**Layers**: ffmpeg-layer

**Key Functions**:
- `lambda_handler()`: Main thumbnail generation
- Extract frames at 10%, 50%, 90% of video duration
- Upload 3 thumbnails to S3 (thumbnails/)

**Processing**:
1. Download video from S3 to /tmp
2. Get video duration with ffprobe
3. Extract 3 frames with ffmpeg
4. Upload thumbnails to S3
5. Clean up /tmp directory

**AWS Access**: S3 (read videos, write thumbnails)

#### 9. url-analysis-api
**Purpose**: URL content extraction and AI summarization
**Trigger**: API Gateway (POST /url-analysis)
**Runtime**: Python 3.9
**Memory**: 512 MB
**Timeout**: 30 seconds

**Key Functions**:
- `analyze_url()`: Extract meta tags and generate AI summary
- `extract_text_content()`: Parse HTML for main content
- `generate_ai_summary()`: AWS Bedrock Claude integration

**Features**:
- **Meta Tag Extraction**: Title, description, Open Graph image (always active)
- **AI Summarization**: Optional AWS Bedrock integration (toggle via environment variable)
- **Christian Perspective**: Summaries highlight biblical relevance
- **Cost Control**: Enable/disable AI via USE_AI_SUMMARY environment variable

**AWS Access**: AWS Bedrock (Claude Instant model)

#### 10. news-api
**Purpose**: News article management with scheduled publishing
**Trigger**: API Gateway (GET/POST/PUT/DELETE /news)
**Runtime**: Python 3.9
**Memory**: 512 MB
**Timeout**: 60 seconds

**Key Functions**:
- `create_news()`: Create news articles with scheduled publishing
- `list_news()`: List news with filtering by topic, state, status
- `get_news()`: Retrieve single news article
- `update_news()`: Modify existing news articles
- `delete_news()`: Remove news articles (role-based permissions)

**Features**:
- Breaking news banners
- Scheduled publishing with auto-status logic
- State-specific election coverage
- External link support
- Topic-based categorization

**AWS Access**: DynamoDB (news table)

#### 11. resources-api
**Purpose**: Resource library management with categories
**Trigger**: API Gateway (GET/POST/PUT/DELETE /resources)
**Runtime**: Python 3.9
**Memory**: 512 MB
**Timeout**: 60 seconds

**Key Functions**:
- `create_resource()`: Add new resources to library
- `list_resources()`: List resources with category filtering
- `update_resource()`: Edit resource details
- `delete_resource()`: Remove resources

**Features**:
- Emoji icons for 47 category keywords
- Category bulk rename
- Auto-summary with AWS Bedrock
- Empty category cleanup

**AWS Access**: DynamoDB (resources table)

#### 12. contributors-api
**Purpose**: State election coverage and contributor management
**Trigger**: API Gateway (GET/POST/PUT/DELETE /contributors)
**Runtime**: Python 3.9
**Memory**: 512 MB
**Timeout**: 60 seconds

**Key Functions**:
- Manage contributors (state correspondents)
- Manage races (290+ across all 50 states)
- Manage candidates (197+ with comprehensive profiles)
- Manage state summaries (comprehensive voter guides)
- Manage pending changes (editor approval workflow)

**Features**:
- ALL 50 US STATES coverage
- CSV bulk import for races and candidates
- Editor role system with approval workflow
- Bypass approval toggle for trusted editors
- Auto-role assignment

**AWS Access**: DynamoDB (contributors, races, candidates, state-summaries, pending-changes tables)

#### 13. email-subscription-handler
**Purpose**: Email subscription and tracking system
**Trigger**: API Gateway HTTP API (POST /subscribe, GET /track/open, GET /track/click)
**Runtime**: Python 3.12
**Memory**: 256 MB
**Timeout**: 30 seconds

**Key Functions**:
- `handle_subscription()`: Process email subscriptions
- `track_open()`: Log email open events via 1x1 pixel
- `track_click()`: Log click events via redirect URLs
- `send_welcome_email()`: Automated welcome email with tracking

**Features**:
- AWS SES integration
- Open tracking (1x1 pixel)
- Click tracking (redirect URLs)
- Newsletter campaigns
- Analytics dashboard
- 95% cheaper than Mailchimp

**AWS Access**: DynamoDB (email-subscribers, email-events tables), AWS SES

#### 14. video-list-api
**Purpose**: Video listing and filtering
**Trigger**: API Gateway (GET /video-list)
**Runtime**: Python 3.9
**Memory**: 512 MB
**Timeout**: 60 seconds

**Key Functions**:
- `list_videos()`: Paginated video listing
- Filter by category, tags, visibility
- Sort by date, title, views

**AWS Access**: DynamoDB (video-metadata table)

#### 15. article-analysis-api
**Purpose**: Article analytics and view tracking
**Trigger**: API Gateway (POST /article-analysis)
**Runtime**: Python 3.9
**Memory**: 256 MB
**Timeout**: 30 seconds

**Key Functions**:
- `track_view()`: Increment article view count
- `get_analytics()`: Retrieve article statistics
- `get_top_articles()`: Most viewed articles
- `get_category_stats()`: Performance by category

**AWS Access**: DynamoDB (articles table)

#### 16. article-meta-tags-edge (Lambda@Edge)
**Purpose**: Dynamic Open Graph meta tags for social media crawlers
**Trigger**: CloudFront Viewer Request
**Runtime**: Python 3.12
**Memory**: 128 MB
**Timeout**: 5 seconds
**Region**: us-east-1 (Lambda@Edge requirement)

**Key Functions**:
- `lambda_handler()`: Intercept crawler requests
- `is_crawler()`: Detect social media bots by user-agent
- `get_article()`: Fetch article data from DynamoDB
- `generate_response()`: Return HTML with article-specific meta tags

**Supported Crawlers**:
- Facebook (facebookexternalhit)
- Twitter (twitterbot)
- LinkedIn (linkedinbot)
- Slack (slackbot)
- WhatsApp (whatsapp)

**Features**:
- Article-specific og:image, og:title, og:description
- Kill switch via ENABLE_DYNAMIC_META environment variable
- Cost: ~$0.0001 for 50 shares/month (free tier)
- Instant disable capability

**AWS Access**: DynamoDB (articles, news tables), CloudFront (edge locations)

**Purpose**: URL content extraction and AI summarization
**Trigger**: API Gateway (POST /url-analysis)
**Runtime**: Python 3.9
**Memory**: 512 MB
**Timeout**: 30 seconds

**Key Functions**:
- `analyze_url()`: Extract meta tags and generate AI summary
- `extract_text_content()`: Parse HTML for main content
- `generate_ai_summary()`: AWS Bedrock Claude integration

**Features**:
- **Meta Tag Extraction**: Title, description, Open Graph image (always active)
- **AI Summarization**: Optional AWS Bedrock integration (toggle via environment variable)
- **Christian Perspective**: Summaries highlight biblical relevance
- **Cost Control**: Enable/disable AI via USE_AI_SUMMARY environment variable

**AWS Access**: AWS Bedrock (Claude Instant model)


### DynamoDB Tables

#### 1. users Table
**Primary Key**: user_id (String)
**Global Secondary Index**: email-index (email)

**Schema**:
```json
{
  "user_id": "uuid",
  "email": "user@example.com",
  "password_hash": "sha256_hash",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user|admin|super_user",
  "active": true,
  "subscription_tier": "free|premium|pro|enterprise",
  "subscription_status": "active|pending|cancelled|expired",
  "subscription_id": "paypal_subscription_id",
  "payment_provider": "paypal",
  "billing_cycle": "monthly",
  "next_billing_date": "2025-01-15T00:00:00Z",
  "storage_used": 1073741824,
  "storage_limit": 2147483648,
  "video_count": 25,
  "video_limit": 50,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-12-01T00:00:00Z"
}
```

#### 2. video-metadata Table
**Primary Key**: video_id (String)

**Schema**:
```json
{
  "video_id": "filename.mp4",
  "filename": "filename.mp4",
  "title": "Video Title",
  "tags": ["sermon", "politics", "teaching"],
  "owner": "user@example.com",
  "visibility": "public|private",
  "video_type": "local|youtube|rumble|facebook|external",
  "external_url": "https://youtube.com/watch?v=...",
  "s3_key": "videos/filename.mp4",
  "url": "original_source_url",
  "upload_date": "2024-01-01T00:00:00Z",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-12-01T00:00:00Z"
}
```

#### 3. articles Table
**Primary Key**: article_id (String)

**Schema**:
```json
{
  "article_id": "uuid",
  "title": "Article Title",
  "content": "<p>Rich text content with HTML...</p>",
  "author": "John Doe",
  "author_email": "user@example.com",
  "category": "sermon|politics|devotional|apologetics|ministry|bible_study|general",
  "template_used": "sermon|political|service_notes|bible_study|custom",
  "scripture_references": ["John 3:16", "Romans 8:28"],
  "tags": ["faith", "politics", "bible"],
  "visibility": "public|private",
  "featured_image": "https://cdn.example.com/image.jpg",
  "reading_time": 5,
  "view_count": 150,
  "likes_count": 25,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-12-01T00:00:00Z"
}
```

#### 4. download-jobs Table
**Primary Key**: job_id (String)

**Schema**:
```json
{
  "job_id": "uuid",
  "url": "https://youtube.com/watch?v=...",
  "filename": "output.mp4",
  "title": "Video Title",
  "tags": ["tag1", "tag2"],
  "status": "pending|processing|downloading|completed|failed",
  "progress": 75,
  "error_message": "Error details if failed",
  "started_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:05:00Z",
  "completed_at": "2024-01-01T00:10:00Z"
}
```

#### 5. comments Table
**Primary Key**: comment_id (String)

**Schema**:
```json
{
  "comment_id": "uuid",
  "article_id": "uuid",
  "user_email": "user@example.com",
  "user_name": "John Doe",
  "content": "Comment text",
  "parent_comment_id": "uuid (for nested replies)",
  "status": "approved|pending|rejected",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 6. news Table
**Primary Key**: news_id (String)

**Schema**:
```json
{
  "news_id": "uuid",
  "title": "News Title",
  "content": "News content",
  "topic": "politics|culture|religious_freedom|family|pro_life",
  "state": "State name (optional)",
  "external_url": "https://...",
  "is_breaking": true,
  "status": "published|scheduled|draft",
  "publish_date": "2024-01-01T00:00:00Z",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 7. resources Table
**Primary Key**: resource_id (String)

**Schema**:
```json
{
  "resource_id": "uuid",
  "name": "Resource Name",
  "category": "Category Name",
  "url": "https://...",
  "description": "Resource description",
  "created_at": "2024-01-01T00:00:00Z"
}
```

#### 8. contributors Table
**Primary Key**: contributor_id (String)

**Schema**:
```json
{
  "contributor_id": "uuid",
  "user_email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+1234567890",
  "state": "State Name",
  "bio": "Contributor bio",
  "verified": true,
  "status": "active|inactive",
  "bypass_approval": false
}
```

#### 9. races Table
**Primary Key**: race_id (String)

**Schema**:
```json
{
  "race_id": "uuid",
  "state": "State Name",
  "office": "U.S. Senate|Governor|etc.",
  "election_date": "2025-11-04",
  "race_type": "primary|general|special|runoff",
  "description": "Race description"
}
```

#### 10. candidates Table
**Primary Key**: candidate_id (String)

**Schema**:
```json
{
  "candidate_id": "uuid",
  "race_id": "uuid",
  "name": "Candidate Name",
  "state": "State Name",
  "office": "U.S. Senate",
  "party": "Republican|Democrat|Independent|etc.",
  "bio": "Candidate biography",
  "faith_statement": "Faith statement text",
  "positions": {
    "abortion": "pro-life",
    "guns": "strong-support",
    "immigration": "border-security"
  },
  "endorsements": ["NRA", "Right to Life"],
  "website": "https://...",
  "voting_record_url": "https://..."
}
```

#### 11. state-summaries Table
**Primary Key**: state (String)

**Schema**:
```json
{
  "state": "State Name",
  "title": "State 2025-2026 Elections Guide",
  "election_year": "2025-2026",
  "content": "Comprehensive voter guide (15,000-30,000 chars)",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

#### 12. pending-changes Table
**Primary Key**: change_id (String)

**Schema**:
```json
{
  "change_id": "uuid",
  "change_type": "candidate|race|event|summary",
  "data": {},
  "submitted_by": "user@example.com",
  "submitted_at": "2024-01-01T00:00:00Z",
  "status": "pending|approved|denied",
  "state": "State Name",
  "reviewed_by": "admin@example.com",
  "reviewed_at": "2024-01-01T00:00:00Z"
}
```

#### 13. email-subscribers Table
**Primary Key**: email (String)

**Schema**:
```json
{
  "email": "user@example.com",
  "status": "active|unsubscribed",
  "subscribed_at": "2024-01-01T00:00:00Z",
  "source": "election-map",
  "total_opens": 5,
  "total_clicks": 3,
  "last_activity": "2024-01-01T00:00:00Z"
}
```

#### 14. email-events Table
**Primary Key**: event_id (String)
**Sort Key**: timestamp (Number)

**Schema**:
```json
{
  "event_id": "uuid",
  "timestamp": 1704153600,
  "email": "user@example.com",
  "event_type": "subscribed|opened|clicked",
  "campaign_id": "campaign-uuid",
  "date": "2024-01-01",
  "metadata": "{}"
}
```

#### 15. templates Table
**Primary Key**: template_id (String)

**Schema**:
```json
{
  "template_id": "uuid",
  "name": "Template Name",
  "content": "Template HTML content",
  "created_at": "2024-01-01T00:00:00Z"
}
```
**Primary Key**: job_id (String)

**Schema**:
```json
{
  "job_id": "uuid",
  "url": "https://youtube.com/watch?v=...",
  "filename": "output.mp4",
  "title": "Video Title",
  "tags": ["tag1", "tag2"],
  "status": "pending|processing|downloading|completed|failed",
  "progress": 75,
  "error_message": "Error details if failed",
  "started_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:05:00Z",
  "completed_at": "2024-01-01T00:10:00Z"
}
```

### S3 Bucket Structure

**Bucket Name**: my-video-downloads-bucket

```
my-video-downloads-bucket/
├── videos/
│   ├── video1.mp4
│   ├── video2.mp4
│   └── sermon-2024.mp4
│
└── thumbnails/
    ├── video1_thumb_1.jpg (10% timestamp)
    ├── video1_thumb_2.jpg (50% timestamp)
    ├── video1_thumb_3.jpg (90% timestamp)
    ├── video2_thumb_1.jpg
    ├── video2_thumb_2.jpg
    └── video2_thumb_3.jpg
```

**CloudFront Distribution**: https://christianconservativestoday.com
- **Origin**: S3 bucket
- **Caching**: Enabled for videos and thumbnails
- **HTTPS**: Required
- **Compression**: Enabled

---

## Data Flow Diagrams

### 1. Video Download Flow

```
┌─────────────┐
│   User      │
│  Interface  │
└──────┬──────┘
       │ 1. Submit URL
       ▼
┌─────────────────────────────────────────────┐
│         Router Lambda                       │
│  ┌────────────────────────────────────┐    │
│  │ 1. Validate request                │    │
│  │ 2. Check storage quota             │    │
│  │ 3. Create job entry (DynamoDB)     │    │
│  │ 4. Send SNS notification           │    │
│  └────────────────────────────────────┘    │
└──────────────┬──────────────────────────────┘
               │ 2. Invoke
               ▼
┌─────────────────────────────────────────────┐
│      Downloader Lambda                      │
│  ┌────────────────────────────────────┐    │
│  │ 1. Update status: processing       │    │
│  │ 2. Download video (yt-dlp)         │    │
│  │ 3. Upload to S3 (videos/)          │    │
│  │ 4. Generate thumbnails (FFmpeg)    │    │
│  │ 5. Upload thumbnails (thumbnails/) │    │
│  │ 6. Save metadata (DynamoDB)        │    │
│  │ 7. Update status: completed        │    │
│  │ 8. Send success notification       │    │
│  └────────────────────────────────────┘    │
└──────────────┬──────────────────────────────┘
               │ 3. Store
               ▼
┌─────────────────────────────────────────────┐
│           S3 + DynamoDB                     │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ videos/      │  │ video-       │        │
│  │ file.mp4     │  │ metadata     │        │
│  └──────────────┘  └──────────────┘        │
│  ┌──────────────┐  ┌──────────────┐        │
│  │ thumbnails/  │  │ download-    │        │
│  │ file_thumb_*.│  │ jobs         │        │
│  └──────────────┘  └──────────────┘        │
└──────────────┬──────────────────────────────┘
               │ 4. Deliver via CDN
               ▼
┌─────────────────────────────────────────────┐
│         CloudFront CDN                      │
│  (Cached video and thumbnail delivery)     │
└──────────────┬──────────────────────────────┘
               │ 5. Display
               ▼
┌─────────────────────────────────────────────┐
│         User Interface                      │
│  (Video player with thumbnails)            │
└─────────────────────────────────────────────┘
```

### 2. User Authentication Flow

```
┌─────────────┐
│   User      │
│  (Login)    │
└──────┬──────┘
       │ 1. POST /auth?action=login
       │    {email, password}
       ▼
┌─────────────────────────────────────────────┐
│         Auth API Lambda                     │
│  ┌────────────────────────────────────┐    │
│  │ 1. Query users table by email      │    │
│  │ 2. Verify password hash (SHA-256)  │    │
│  │ 3. Generate JWT token              │    │
│  │    - Header: {alg: HS256}          │    │
│  │    - Payload: {user_id, email,     │    │
│  │               role, exp: 24h}      │    │
│  │    - Signature: HMAC-SHA256        │    │
│  │ 4. Return token + user info        │    │
│  └────────────────────────────────────┘    │
└──────────────┬──────────────────────────────┘
               │ 2. Query
               ▼
┌─────────────────────────────────────────────┐
│         DynamoDB (users table)              │
│  email-index: user@example.com              │
└──────────────┬──────────────────────────────┘
               │ 3. Return JWT
               ▼
┌─────────────────────────────────────────────┐
│         User Interface                      │
│  ┌────────────────────────────────────┐    │
│  │ 1. Store token in localStorage     │    │
│  │ 2. Include in Authorization header │    │
│  │    Bearer <token>                  │    │
│  │ 3. Redirect to videos/articles     │    │
│  └────────────────────────────────────┘    │
└─────────────────────────────────────────────┘

Subsequent API Requests:
┌─────────────┐
│   User      │
│  Request    │
└──────┬──────┘
       │ Authorization: Bearer <token>
       ▼
┌─────────────────────────────────────────────┐
│         Any API Lambda                      │
│  ┌────────────────────────────────────┐    │
│  │ 1. Extract token from header       │    │
│  │ 2. Decode JWT payload              │    │
│  │ 3. Verify signature                │    │
│  │ 4. Check expiration                │    │
│  │ 5. Validate role permissions       │    │
│  │ 6. Process request                 │    │
│  └────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```

### 3. Article Creation with Bible Integration Flow

```
┌─────────────┐
│   User      │
│  (Editor)   │
└──────┬──────┘
       │ 1. Search Bible verse
       │    GET /articles?action=bible_verse
       │    &reference=John 3:16&translation=kjv
       ▼
┌─────────────────────────────────────────────┐
│      Articles API Lambda                    │
│  ┌────────────────────────────────────┐    │
│  │ 1. Format reference (john3:16)     │    │
│  │ 2. Call Bible API                  │    │
│  │ 3. Clean verse text (remove \n)    │    │
│  │ 4. Return formatted verse          │    │
│  └────────────────────────────────────┘    │
└──────────────┬──────────────────────────────┘
               │ 2. HTTP GET
               ▼
┌─────────────────────────────────────────────┐
│      Bible API (bible-api.com)              │
│  Translations: KJV, ASV, YLT                │
└──────────────┬──────────────────────────────┘
               │ 3. Return verse
               ▼
┌─────────────────────────────────────────────┐
│         User Interface (Quill.js)           │
│  ┌────────────────────────────────────┐    │
│  │ 1. Display verse in modal          │    │
│  │ 2. User clicks "Insert"            │    │
│  │ 3. Insert as blockquote in editor  │    │
│  └────────────────────────────────────┘    │
└──────────────┬──────────────────────────────┘
               │ 4. Save article
               │    POST /articles?action=create
               ▼
┌─────────────────────────────────────────────┐
│      Articles API Lambda                    │
│  ┌────────────────────────────────────┐    │
│  │ 1. Extract scripture references    │    │
│  │    (regex: Book \d+:\d+)           │    │
│  │ 2. Calculate reading time          │    │
│  │    (word_count / 200 words/min)    │    │
│  │ 3. Get author name from users      │    │
│  │ 4. Save to DynamoDB                │    │
│  └────────────────────────────────────┘    │
└──────────────┬──────────────────────────────┘
               │ 5. Store
               ▼
┌─────────────────────────────────────────────┐
│      DynamoDB (articles table)              │
│  {article_id, title, content,               │
│   scripture_references: ["John 3:16"]}      │
└─────────────────────────────────────────────┘
```

### 4. Subscription & Quota Enforcement Flow

```
┌─────────────┐
│   User      │
│  (Upload)   │
└──────┬──────┘
       │ 1. Initiate video upload
       ▼
┌─────────────────────────────────────────────┐
│         Router Lambda                       │
│  ┌────────────────────────────────────┐    │
│  │ check_storage_quota(user_email)    │    │
│  │  ├─ Query users table              │    │
│  │  ├─ Get storage_used, video_count  │    │
│  │  ├─ Compare to limits              │    │
│  │  └─ Return allowed/denied          │    │
│  └────────────────────────────────────┘    │
└──────────────┬──────────────────────────────┘
               │ 2. Query user data
               ▼
┌─────────────────────────────────────────────┐
│      DynamoDB (users table)                 │
│  {subscription_tier: "free",                │
│   storage_used: 1.8GB,                      │
│   storage_limit: 2GB,                       │
│   video_count: 48,                          │
│   video_limit: 50}                          │
└──────────────┬──────────────────────────────┘
               │ 3. Check limits
               ▼
┌─────────────────────────────────────────────┐
│         Quota Decision                      │
│  ┌────────────────────────────────────┐    │
│  │ IF video_count >= video_limit:     │    │
│  │    DENY (403 Forbidden)            │    │
│  │ IF storage_used >= 90% of limit:   │    │
│  │    DENY (403 Forbidden)            │    │
│  │ ELSE:                              │    │
│  │    ALLOW (proceed with upload)     │    │
│  └────────────────────────────────────┘    │
└──────────────┬──────────────────────────────┘
               │ 4. Response
               ▼
┌─────────────────────────────────────────────┐
│         User Interface                      │
│  ┌────────────────────────────────────┐    │
│  │ IF DENIED:                         │    │
│  │   Show upgrade prompt              │    │
│  │   Display current usage            │    │
│  │   Link to PayPal subscription      │    │
│  │ IF ALLOWED:                        │    │
│  │   Proceed with upload              │    │
│  └────────────────────────────────────┘    │
└─────────────────────────────────────────────┘

PayPal Subscription Flow:
┌─────────────┐
│   User      │
│  (Upgrade)  │
└──────┬──────┘
       │ 1. Select plan (Premium/Pro/Enterprise)
       ▼
┌─────────────────────────────────────────────┐
│      PayPal Billing API Lambda              │
│  ┌────────────────────────────────────┐    │
│  │ 1. Create PayPal subscription      │    │
│  │ 2. Update user record              │    │
│  │    - subscription_tier             │    │
│  │    - subscription_id               │    │
│  │    - storage_limit (increased)     │    │
│  │    - video_limit (increased)       │    │
│  │ 3. Return approval URL             │    │
│  └────────────────────────────────────┘    │
└──────────────┬──────────────────────────────┘
               │ 2. API call
               ▼
┌─────────────────────────────────────────────┐
│      PayPal API (Subscriptions)             │
│  Create subscription plan                   │
└──────────────┬──────────────────────────────┘
               │ 3. Redirect to PayPal
               ▼
┌─────────────────────────────────────────────┐
│      PayPal Payment Page                    │
│  User completes payment                     │
└──────────────┬──────────────────────────────┘
               │ 4. Webhook notification
               ▼
┌─────────────────────────────────────────────┐
│      PayPal Billing API (Webhook)           │
│  ┌────────────────────────────────────┐    │
│  │ Event: SUBSCRIPTION.ACTIVATED      │    │
│  │ 1. Update subscription_status      │    │
│  │ 2. Set next_billing_date           │    │
│  │ 3. Activate new limits             │    │
│  └────────────────────────────────────┘    │
└─────────────────────────────────────────────┘
```


---

## API Endpoints

### Base URLs
- **Auth API**: https://r6l0z3605f.execute-api.us-east-1.amazonaws.com/prod/auth
- **Admin API**: https://k2avuckm38.execute-api.us-east-1.amazonaws.com/prod/admin
- **TAG API**: https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/tags
- **Router API**: https://j3w8kgqlvi.execute-api.us-east-1.amazonaws.com/prod/download
- **Articles API**: https://fr3hh94h4a.execute-api.us-east-1.amazonaws.com/prod/articles
- **PayPal API**: https://j3w8kgqlvi.execute-api.us-east-1.amazonaws.com/prod/paypal
- **URL Analysis API**: https://[api-id].execute-api.us-east-1.amazonaws.com/prod/url-analysis

### Authentication Endpoints

#### POST /auth?action=register
**Purpose**: Create new user account
**Authentication**: None
**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "role": "user"
}
```
**Response**:
```json
{
  "message": "User registered successfully",
  "user_id": "uuid"
}
```

#### POST /auth?action=login
**Purpose**: Authenticate user and generate JWT
**Authentication**: None
**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```
**Response**:
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "name": "John Doe",
    "role": "user"
  }
}
```

#### GET /auth?action=verify
**Purpose**: Verify JWT token validity
**Authentication**: Bearer token
**Headers**: `Authorization: Bearer <token>`
**Response**:
```json
{
  "valid": true,
  "user": {
    "user_id": "uuid",
    "email": "user@example.com",
    "role": "user"
  }
}
```

### Video Management Endpoints

#### POST /download
**Purpose**: Initiate video download
**Authentication**: Bearer token
**Request Body**:
```json
{
  "url": "https://youtube.com/watch?v=...",
  "output_name": "video.mp4",
  "title": "Video Title",
  "tags": ["sermon", "teaching"],
  "owner": "user@example.com",
  "visibility": "public"
}
```
**Response**:
```json
{
  "message": "Download started",
  "job_id": "uuid"
}
```

#### GET /download?action=status
**Purpose**: Get download job status
**Authentication**: None
**Response**:
```json
{
  "active": [
    {
      "job_id": "uuid",
      "status": "downloading",
      "progress": 75,
      "started_at": "2024-01-01T00:00:00Z"
    }
  ],
  "recent": [
    {
      "job_id": "uuid",
      "status": "completed",
      "filename": "video.mp4",
      "completed_at": "2024-01-01T00:10:00Z"
    }
  ]
}
```

#### GET /tags?action=list
**Purpose**: List all videos with pagination
**Authentication**: Optional (affects visibility filtering)
**Query Parameters**:
- `user`: User email (for filtering)
- `role`: User role (admin/super_user see all)
- `page`: Page number (default: 1)
- `limit`: Videos per page (default: 24)
- `category`: Filter by category (all/sermons/politics/teaching)

**Response**:
```json
{
  "videos": [
    {
      "filename": "video.mp4",
      "title": "Video Title",
      "tags": ["sermon"],
      "owner": "user@example.com",
      "visibility": "public",
      "video_type": "local",
      "size": 52428800,
      "upload_date": "2024-01-01T00:00:00Z"
    }
  ],
  "count": 24,
  "total_count": 150,
  "page": 1,
  "limit": 24,
  "total_pages": 7,
  "has_more": true
}
```

#### POST /tags?action=add_video
**Purpose**: Add video metadata
**Authentication**: Bearer token
**Request Body**:
```json
{
  "filename": "video.mp4",
  "title": "Video Title",
  "tags": ["sermon", "teaching"],
  "owner": "user@example.com",
  "visibility": "public",
  "video_type": "local"
}
```

#### POST /tags?action=add_video (External Video)
**Purpose**: Add external video without downloading
**Authentication**: Bearer token
**Request Body**:
```json
{
  "filename": "youtube-video-id",
  "title": "YouTube Video Title",
  "tags": ["sermon"],
  "owner": "user@example.com",
  "visibility": "public",
  "video_type": "external",
  "external_url": "https://youtube.com/watch?v=..."
}
```

### Article Management Endpoints

#### POST /articles?action=create
**Purpose**: Create new article
**Authentication**: Bearer token
**Request Body**:
```json
{
  "title": "Article Title",
  "content": "<p>Rich text content...</p>",
  "author": "user@example.com",
  "category": "sermon",
  "template_used": "sermon",
  "tags": ["faith", "bible"],
  "visibility": "public",
  "featured_image": "https://cdn.example.com/image.jpg"
}
```
**Response**:
```json
{
  "message": "Article created successfully",
  "article_id": "uuid",
  "scripture_references": ["John 3:16", "Romans 8:28"]
}
```

#### GET /articles?action=list
**Purpose**: List articles
**Authentication**: Optional (public articles accessible without auth)
**Query Parameters**:
- `visibility`: public/private (default: public)
- `category`: Filter by category
- `author`: Filter by author

**Response**:
```json
{
  "articles": [
    {
      "article_id": "uuid",
      "title": "Article Title",
      "author": "John Doe",
      "category": "sermon",
      "tags": ["faith"],
      "visibility": "public",
      "featured_image": "https://...",
      "reading_time": 5,
      "view_count": 150,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "count": 25
}
```

#### GET /articles?action=get&article_id=uuid
**Purpose**: Get single article
**Authentication**: Optional (required for private articles)
**Response**:
```json
{
  "article": {
    "article_id": "uuid",
    "title": "Article Title",
    "content": "<p>Full content...</p>",
    "author": "John Doe",
    "author_email": "user@example.com",
    "category": "sermon",
    "scripture_references": ["John 3:16"],
    "tags": ["faith"],
    "visibility": "public",
    "reading_time": 5,
    "view_count": 151,
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

#### GET /articles?action=search&q=keyword
**Purpose**: Search articles
**Authentication**: Optional
**Query Parameters**:
- `q`: Search query
- `category`: Filter by category
- `author`: Filter by author
- `visibility`: public/private

**Response**:
```json
{
  "articles": [...],
  "count": 10,
  "search_query": "keyword",
  "filters": {
    "category": "sermon",
    "author": null,
    "visibility": "public"
  }
}
```

#### GET /articles?action=bible_verse&reference=John 3:16&translation=kjv
**Purpose**: Fetch Bible verse
**Authentication**: None
**Response**:
```json
{
  "reference": "John 3:16",
  "text": "For God so loved the world...",
  "translation": "KJV"
}
```

#### DELETE /articles?action=delete&article_id=uuid
**Purpose**: Delete article
**Authentication**: Bearer token (role-based permissions)
**Permissions**:
- Super users and admins: Can delete any article
- Regular users: Can only delete their own articles

### Admin Endpoints

#### GET /admin?action=users
**Purpose**: List all users
**Authentication**: Bearer token (admin/super_user only)
**Response**:
```json
{
  "users": [
    {
      "user_id": "uuid",
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "user",
      "subscription_tier": "premium",
      "subscription_status": "active",
      "storage_used": 5368709120,
      "storage_limit": 26843545600,
      "video_count": 125,
      "video_limit": 500,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "count": 50
}
```

#### PUT /admin?action=user_role
**Purpose**: Update user role and details
**Authentication**: Bearer token (admin/super_user only)
**Restrictions**:
- Admins cannot modify super users
- Admins cannot create super users

**Request Body**:
```json
{
  "user_id": "uuid",
  "role": "admin",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### PUT /admin?action=user_subscription
**Purpose**: Manually adjust user subscription
**Authentication**: Bearer token (admin/super_user only)
**Request Body**:
```json
{
  "user_id": "uuid",
  "subscription_tier": "pro",
  "subscription_status": "active",
  "storage_limit": 107374182400,
  "video_limit": 2000,
  "next_billing_date": "2025-02-01T00:00:00Z"
}
```

#### DELETE /admin?action=user&user_id=uuid
**Purpose**: Delete user
**Authentication**: Bearer token (admin/super_user only)
**Restrictions**: Admins cannot delete super users

#### DELETE /admin?action=video&filename=video.mp4
**Purpose**: Delete video and thumbnails
**Authentication**: Bearer token (admin/super_user only)

#### POST /admin?action=upload_url
**Purpose**: Generate S3 presigned upload URL
**Authentication**: Bearer token (any authenticated user)
**Request Body**:
```json
{
  "filename": "video.mp4"
}
```
**Response**:
```json
{
  "upload_url": "https://s3.amazonaws.com/...",
  "filename": "video.mp4"
}
```

### PayPal Subscription Endpoints

#### POST /paypal?action=create_subscription
**Purpose**: Create PayPal subscription
**Authentication**: Bearer token
**Request Body**:
```json
{
  "plan": "premium",
  "user_email": "user@example.com"
}
```
**Response**:
```json
{
  "subscription_id": "paypal_sub_id",
  "approval_url": "https://paypal.com/...",
  "status": "pending"
}
```

#### POST /paypal?action=cancel_subscription
**Purpose**: Cancel subscription (retains benefits until billing period ends)
**Authentication**: Bearer token
**Request Body**:
```json
{
  "user_email": "user@example.com"
}
```

#### GET /paypal?action=get_subscription_status
**Purpose**: Get user subscription details
**Authentication**: Bearer token
**Query Parameters**: `user_email`
**Response**:
```json
{
  "subscription_tier": "premium",
  "subscription_status": "active",
  "storage_used": 5368709120,
  "storage_limit": 26843545600,
  "video_count": 125,
  "video_limit": 500,
  "next_billing_date": "2025-02-01T00:00:00Z"
}
```

#### POST /paypal?action=webhook
**Purpose**: Handle PayPal webhook events
**Authentication**: PayPal signature verification
**Events Handled**:
- BILLING.SUBSCRIPTION.CREATED
- BILLING.SUBSCRIPTION.ACTIVATED
- BILLING.SUBSCRIPTION.CANCELLED
- BILLING.SUBSCRIPTION.EXPIRED

### URL Analysis Endpoint

#### POST /url-analysis
**Purpose**: Extract meta tags and generate AI summary
**Authentication**: None
**Request Body**:
```json
{
  "url": "https://example.com/article"
}
```
**Response**:
```json
{
  "url": "https://example.com/article",
  "title": "Article Title",
  "description": "Article description from meta tags",
  "image": "https://example.com/og-image.jpg",
  "ai_enabled": true,
  "ai_summary": "2-3 sentence summary from Christian perspective..."
}
```

---

## Security Architecture

### Authentication & Authorization

#### JWT Token Structure
```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "user_id": "uuid",
  "email": "user@example.com",
  "role": "user|admin|super_user",
  "exp": 1704153600  // Unix timestamp (24 hours)
}

Signature:
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

#### Role-Based Access Control (RBAC)

**Super User Permissions**:
- ✅ All admin capabilities
- ✅ Create/delete super users
- ✅ Modify any user (including admins)
- ✅ Unlimited storage and videos
- ✅ System-wide configuration

**Admin Permissions**:
- ✅ User management (except super users)
- ✅ Content moderation (all videos/articles)
- ✅ Subscription management
- ✅ Unlimited storage and videos
- ❌ Cannot modify super users
- ❌ Cannot create super users

**User Permissions**:
- ✅ Upload videos (quota-limited)
- ✅ Create/edit own articles
- ✅ Manage own content
- ✅ View public content
- ❌ Cannot access admin functions
- ❌ Subject to subscription limits

### Data Security

#### Password Security
- **Hashing Algorithm**: SHA-256
- **Storage**: Only hashed passwords stored in DynamoDB
- **Transmission**: HTTPS only
- **Password Reset**: Admin-initiated with new hash generation

#### API Security
- **CORS**: Configured on all API endpoints
- **HTTPS**: Required for all API calls
- **Token Validation**: Every protected endpoint validates JWT
- **Rate Limiting**: API Gateway throttling enabled
- **Input Validation**: All user inputs sanitized

#### S3 Security
- **Bucket Policy**: Private by default
- **CloudFront**: Public access via CDN only
- **Presigned URLs**: Time-limited (1 hour for uploads, 24 hours for playback)
- **Content-Type**: Enforced on uploads
- **Encryption**: Server-side encryption enabled

### Privacy Controls

#### Video Visibility
- **Public**: Accessible to all users (authenticated and anonymous)
- **Private**: Only visible to owner, admins, and super users
- **Ownership**: Videos tied to user email
- **Transfer**: Ownership can be changed by admins/super users

#### Article Visibility
- **Public**: Accessible without authentication
- **Private**: Requires authentication and ownership/admin access
- **Author Privacy**: Email addresses converted to display names
- **Study Notes**: Automatically set to private

---

## Deployment Architecture

### Infrastructure as Code

#### Lambda Function Configuration
```yaml
Runtime: python3.9
Architecture: x86_64
Memory: 
  - auth-api: 256 MB
  - admin-api: 512 MB
  - tag-api: 512 MB
  - router: 256 MB
  - downloader: 3008 MB (max)
  - articles-api: 512 MB
  - paypal-billing-api: 256 MB
  - thumbnail-generator: 1024 MB
  - url-analysis-api: 512 MB

Timeout:
  - auth-api: 30 seconds
  - admin-api: 60 seconds
  - tag-api: 60 seconds
  - router: 30 seconds
  - downloader: 900 seconds (15 min)
  - articles-api: 60 seconds
  - paypal-billing-api: 30 seconds
  - thumbnail-generator: 300 seconds (5 min)
  - url-analysis-api: 30 seconds

Environment Variables:
  - S3_BUCKET: my-video-downloads-bucket
  - JWT_SECRET: (stored securely)
  - PAYPAL_CLIENT_ID: (environment variable)
  - PAYPAL_CLIENT_SECRET: (environment variable)
  - USE_AI_SUMMARY: true/false
```

#### Lambda Layers
```
yt-dlp-layer:
  - yt-dlp binary
  - Python dependencies
  - Size: ~50 MB

ffmpeg-layer:
  - ffmpeg binary
  - ffprobe binary
  - Size: ~100 MB
```

#### DynamoDB Configuration
```yaml
users:
  BillingMode: PAY_PER_REQUEST
  GlobalSecondaryIndexes:
    - IndexName: email-index
      KeySchema: email (HASH)
      Projection: ALL

video-metadata:
  BillingMode: PAY_PER_REQUEST
  KeySchema: video_id (HASH)

articles:
  BillingMode: PAY_PER_REQUEST
  KeySchema: article_id (HASH)

download-jobs:
  BillingMode: PAY_PER_REQUEST
  KeySchema: job_id (HASH)
```

#### S3 Bucket Configuration
```yaml
Bucket: my-video-downloads-bucket
Region: us-east-1
Versioning: Disabled
Encryption: AES-256 (SSE-S3)
Lifecycle Rules:
  - Delete incomplete multipart uploads after 7 days
Public Access: Blocked (access via CloudFront only)
CORS:
  - AllowedOrigins: ['*']
  - AllowedMethods: [GET, PUT, POST]
  - AllowedHeaders: ['*']
```

#### CloudFront Distribution
```yaml
Origin: my-video-downloads-bucket.s3.amazonaws.com
PriceClass: PriceClass_100 (US, Canada, Europe)
ViewerProtocolPolicy: redirect-to-https
Compress: true
CacheBehaviors:
  - PathPattern: videos/*
    TTL: 86400 (24 hours)
  - PathPattern: thumbnails/*
    TTL: 604800 (7 days)
```

### Monitoring & Logging

#### CloudWatch Metrics
- Lambda invocations and errors
- API Gateway request count and latency
- DynamoDB read/write capacity
- S3 storage and requests

#### CloudWatch Logs
- Lambda function logs (all functions)
- API Gateway access logs
- Error tracking and debugging

#### SNS Notifications
- Video download started
- Video download completed
- Video download failed
- Subscription events

### Cost Optimization

#### Estimated Monthly Costs (100 active users)
```
Lambda Executions: $5-10
DynamoDB (PAY_PER_REQUEST): $5-15
S3 Storage (500GB): $11.50
CloudFront Data Transfer (1TB): $85
API Gateway: $3.50
Total: ~$120-135/month
```

#### Cost Reduction Strategies
- Pagination to reduce DynamoDB scans
- CloudFront caching to reduce S3 requests
- Lambda memory optimization
- S3 lifecycle policies for old content
- Thumbnail generation on-demand vs. automatic

---

## Performance Optimization

### Frontend Optimization
- **Pagination**: 24 videos per page
- **Lazy Loading**: Images and videos load on scroll
- **CDN Delivery**: All static assets via CloudFront
- **Caching**: Browser caching for static resources
- **Minification**: CSS and JavaScript minified

### Backend Optimization
- **DynamoDB Indexes**: email-index for fast user lookups
- **S3 Presigned URLs**: Direct upload/download without Lambda proxy
- **Lambda Concurrency**: Automatic scaling
- **API Gateway Caching**: Enabled for frequently accessed endpoints
- **Thumbnail Pre-generation**: 3 thumbnails created during upload

### Database Optimization
- **Query Patterns**: Optimized for common access patterns
- **Projection**: Only required attributes returned
- **Batch Operations**: Bulk reads/writes where possible
- **Decimal Conversion**: Automatic conversion for JSON serialization

---

## Recent Major Enhancements (2024-2025)

### Election Tracking System - ALL 50 STATES COMPLETE ✅
**Comprehensive nationwide election coverage**:
- **290+ Races**: Federal, statewide, state legislature, municipal across all 50 states
- **197+ Candidates**: Detailed profiles with faith statements, policy positions, endorsements
- **50 State Voter Guides**: 15,000-30,000 character comprehensive guides with Christian conservative perspective
- **Interactive US Map**: Click-to-view state-specific election data
- **Editor Role System**: Distributed content management with approval workflow
- **CSV Bulk Import**: Automated race and candidate data uploads
- **Dual-Mode Editor**: Markdown and rich text editing for voter guides

### Email Subscription & Tracking System ✅
**Professional email marketing with analytics**:
- **AWS SES Integration**: contact@christianconservativestoday.com
- **Open Tracking**: 1x1 pixel tracking for email opens
- **Click Tracking**: Redirect URLs with engagement analytics
- **Newsletter System**: Bulk email campaigns to subscribers
- **Analytics Dashboard**: Open rates, click rates, engagement metrics
- **Cost Efficiency**: 95% cheaper than Mailchimp ($1 per 10,000 emails)

### Advanced Content Features ✅
**Enhanced user engagement and content management**:
- **Comment System**: User comments with moderation tools, nested replies, bulk actions
- **Article Analytics**: View tracking, top articles dashboard, category performance stats
- **Social Sharing**: Facebook, Twitter, LinkedIn integration with Open Graph meta tags
- **Markdown Support**: Dual-mode editing (WYSIWYG/Markdown) with bidirectional conversion
- **Featured Images**: Open Graph integration for rich social media previews
- **Related Articles**: Algorithm-based recommendations using category, tags, author matching
- **Public Article Access**: Non-authenticated viewing for ministry outreach

### UI/UX Enhancements ✅
**Modern, responsive design improvements**:
- **Horizontal Scrolling UI**: Netflix-style content browsing on videos, articles, news, resources
- **Unified Navigation**: navbar.html/navbar.js components with role-based access control
- **Mobile Optimization**: Responsive design with progressive breakpoints (768px, 576px, 422px)
- **CSS Consolidation**: 75+ duplicate rules removed (23.6% reduction) into shared stylesheets
- **Authentication Standardization**: Consistent localStorage keys (auth_token, user_data)

### Resource Management System ✅
**Enhanced organization and automation**:
- **Emoji Icons**: 47 category keywords with automatic emoji selection
- **Edit Functionality**: Complete CRUD operations for resources
- **Category Bulk Rename**: Organizational flexibility
- **Auto-Summary**: AWS Bedrock AI-powered descriptions from URLs
- **Empty Category Cleanup**: Automatic maintenance

### News Management System ✅
**Comprehensive news coverage**:
- **Breaking News Banners**: Priority content highlighting
- **Scheduled Publishing**: Auto-status logic for future publication dates
- **State-Specific Coverage**: Election and local news by state
- **External Link Support**: Aggregation from trusted sources
- **Topic Categorization**: Politics, culture, religious freedom, family, pro-life

## Conclusion

Christian Conservatives Today has evolved into a comprehensive, enterprise-grade serverless platform built on AWS that combines video hosting, article publishing, nationwide election tracking, and community engagement. The architecture leverages AWS Lambda for compute, DynamoDB for data storage, S3 for media storage, and CloudFront for content delivery, resulting in a cost-effective, high-performance solution.

### Key Achievements
- ✅ 100% serverless architecture
- ✅ 15+ microservices (Lambda functions)
- ✅ 15+ DynamoDB tables
- ✅ 4-tier role-based access control (Super User > Admin > Editor > User)
- ✅ PayPal subscription integration
- ✅ Bible verse integration with multiple translations
- ✅ Automatic thumbnail generation
- ✅ External video embedding
- ✅ Full-text article search
- ✅ Public article access for ministry outreach
- ✅ ALL 50 US STATES election coverage (290+ races, 197+ candidates)
- ✅ Email subscription system with open/click tracking
- ✅ Comment system with moderation
- ✅ Article analytics and view tracking
- ✅ Social sharing integration
- ✅ Markdown support with dual-mode editing
- ✅ Horizontal scrolling UI (Netflix-style)
- ✅ CSS consolidation (23.6% reduction)
- ✅ Unified navigation system
- ✅ Mobile optimization

### Future Enhancements
- Angular frontend conversion (Phase 4)
- Mobile applications (iOS/Android)
- Live streaming integration
- Advanced analytics dashboard
- Community forums and discussion boards
- AI-powered sermon outline generator
- Newsletter and email marketing tools

---

**Platform URL**: https://christianconservativestoday.com  
**Documentation Version**: 1.0  
**Last Updated**: January 2025
