# Christian Conservatives Today - Technical Documentation v2.0

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [New Features in v2.0](#new-features-in-v20)
3. [System Architecture v2.0](#system-architecture-v20)
4. [Core Features](#core-features)
5. [AWS Services Integration](#aws-services-integration)
6. [Data Flow Diagrams](#data-flow-diagrams)
7. [Database Schema](#database-schema)
8. [API Endpoints v2.0](#api-endpoints-v20)
9. [Security Architecture](#security-architecture)
10. [Performance Optimizations v2.0](#performance-optimizations-v20)
11. [Deployment Architecture v2.0](#deployment-architecture-v20)
12. [Future Enhancements](#future-enhancements)
13. [Conclusion](#conclusion)

---

## Executive Summary

**Christian Conservatives Today v2.0** is a fully serverless platform built on AWS, designed for the 5-fold ministry (apostles, prophets, evangelists, pastors, teachers), Christian believers, and conservative voices. The platform enables video hosting, article publishing with Bible integration, election tracking for all 50 US states, community engagement, and advanced analytics. Updated January 2025 with significant UI/UX improvements and feature additions.

### Key Metrics v2.0
- **Architecture**: 100% Serverless (AWS Lambda, S3, DynamoDB, CloudFront)
- **Lambda Functions**: 15+ microservices (up from 9)
- **Database Tables**: 12+ DynamoDB tables (up from 4)
- **Storage**: S3 with CloudFront CDN
- **Authentication**: JWT-based with 24-hour expiration
- **User Roles**: 3-tier system (Super User > Admin > User) + Editor role
- **Election Coverage**: All 50 US states with comprehensive voter guides

### Technology Stack
- **Backend**: Python 3.12 (AWS Lambda)
- **Frontend**: HTML5, JavaScript ES6+, Bootstrap 5, Quill.js, marked.js
- **Database**: DynamoDB (NoSQL)
- **Storage**: S3 + CloudFront CDN
- **APIs**: API Gateway (REST + HTTP API v2)
- **Video Processing**: yt-dlp, FFmpeg
- **Notifications**: SNS, AWS SES
- **AI**: AWS Bedrock (Claude) for content summarization

---

## New Features in v2.0

### 1. CSS/JS Consolidation Project ✅
**Status**: Phase 1 Complete
- Created `assets/css/common-styles.css` with shared navigation and dashboard styles
- Removed 75 duplicate CSS rules across 9 pages (23.6% reduction)
- Fixed header spacing issues and mobile hamburger menu
- Deployed to S3 with CloudFront invalidation
- Git commit: 0b45ae4

**Benefits**:
- Single source of truth for navigation styles
- Improved maintainability
- Faster page load times (cached shared CSS)
- Consistent responsive behavior

### 2. Unified Navigation System ✅
**Components**:
- `navbar.html` - Reusable HTML template
- `navbar.js` - Smart authentication logic with role-based access
- Dual icon support (emoji and Font Awesome)
- Mobile responsive with hamburger menu
- Fixed positioning with proper page padding

**Pages Updated**: 10+ pages including index.html, videos.html, articles.html, news.html, resources.html, election-map.html, profile.html, user-page.html, article.html, news-article.html

### 3. Authentication Standardization ✅
**Migration**:
- Old keys (deprecated): `token`, `userRole`, `userEmail`, `userName`
- New standardized keys: `auth_token`, `user_data` (JSON object)
- Fixed authentication issues across admin-contributors.html, news pages, election-map.html
- Resolved "admin access required" errors for super_user role

### 4. Election Tracking System ✅
**Coverage**: ALL 50 US STATES COMPLETE
- **Total Races**: 290+ races across 10 states (more being added)
- **Total Candidates**: 197+ candidates with detailed profiles
- **Voter Guides**: 20-30 page comprehensive guides per state (15,000-30,000+ characters)
- **Interactive Map**: Click-to-view state details with color coding
- **State Correspondents**: Verified contributors with contact info
- **CSV Bulk Import**: Easy data management
- **Dual-Mode Editor**: Markdown and rich text for state summaries

**Key Features**:
- Candidate profiles with faith statements and policy positions
- Race management (federal, statewide, state legislature, municipal)
- Election overview dashboard with visual stats
- Email subscription system with AWS SES
- Open/click tracking for newsletters
- Apply to be correspondent functionality

### 5. Advanced Analytics System ✅
**Article Analytics**:
- View count tracking
- Top articles dashboard
- Category performance stats
- Analytics API endpoint
- Engagement metrics display

**Search Functionality**:
- Full-text search across title, content, author, tags
- Relevance scoring
- Multi-field filtering
- Debounced search (300ms) for optimal performance

### 6. Social Sharing & Public Access ✅
**Features**:
- Facebook, Twitter, LinkedIn integration
- Open Graph meta tags for rich previews
- Copy link functionality with visual feedback
- Public article access for non-authenticated users
- Featured image system with compression

### 7. Horizontal Scrolling UI ✅
**Implementation**:
- Netflix/YouTube-style horizontal scrolling
- Arrow navigation (desktop only, hidden on mobile)
- Category grouping with scroll per section
- Responsive design with touch scrolling on mobile
- Applied to videos, resources, articles, news pages

### 8. Resource Management Enhancements ✅
**Features**:
- Emoji icons for 47 category keywords
- Edit functionality for resources
- Category bulk rename
- Empty category cleanup
- Auto-summary with AWS Bedrock Claude
- URL analysis API integration

### 9. News Management System ✅
**Features**:
- Topic-based news with breaking news banners
- Scheduled publishing with auto-status logic
- State-specific election coverage
- External link support
- Christian/political news categories
- Horizontal scrolling UI
- Admin creation/editing with comprehensive filtering

### 10. Comment System ✅
**Features**:
- User comments on articles
- Moderation tools (approve/delete/restore)
- Discussion threads
- Nested replies
- Edit/delete functionality
- Bulk actions for admins

### 11. Markdown Support ✅
**Implementation**:
- Toggle between WYSIWYG and Markdown modes
- Bidirectional conversion (HTML ↔ Markdown)
- HTML entity decoding for proper character handling
- Separate content storage for each mode
- Preview functionality in both modes
- Applied to create-article.html and edit-article.html

### 12. Mobile Optimization ✅
**Improvements**:
- Footer text visibility fix (text-white on dark background)
- Articles page mobile optimization with responsive grid
- Navigation button sizing fixes at medium widths (992-1199px)
- Progressive mobile breakpoints (768px, 576px, 422px)
- Touch-friendly elements and proper spacing

### 13. Email Subscription System ✅
**Components**:
- AWS SES integration (contact@christianconservativestoday.com)
- DynamoDB storage (email-subscribers, email-events tables)
- Lambda function (email-subscription-handler)
- API Gateway HTTP API v2
- Open tracking (1x1 pixel)
- Click tracking (redirect URLs)
- Analytics dashboard
- Newsletter sending system

**Cost**: ~$1 per 10,000 emails (95% cheaper than Mailchimp)

### 14. Editor Role & Approval Workflow ✅
**System**:
- 3-tier role hierarchy: Super User / Admin > Editor > Regular User
- Approval workflow for editor submissions
- Bypass approval toggle for trusted editors
- Pending count badge in navbar (real-time updates)
- Admin review interface (admin-pending-changes.html)
- Auto-role assignment when contributor created
- User selection dropdown from users table

---

## System Architecture v2.0

### Lambda Functions (15+ Total)

#### Core Functions (Original 9)
1. **auth-api** - User authentication and JWT management
2. **admin-api** - Administrative operations and user management
3. **tag-api** - Video metadata and tag management
4. **router** - Job routing and quota enforcement
5. **downloader** - Video download and processing
6. **articles-api** - Blog/article management with Bible integration
7. **paypal-billing-api** - Subscription management
8. **thumbnail-generator** - Generate thumbnails for uploaded videos
9. **url-analysis-api** - URL content extraction and AI summarization

#### New Functions (v2.0)
10. **contributors-api** - Election system contributor management
11. **comments-api** - Comment system management
12. **news-api** - News article operations
13. **resources-api** - Resource management
14. **article-analysis-api** - Article analytics
15. **email-subscription-handler** - Email subscription and tracking

### DynamoDB Tables (12+ Total)

#### Core Tables (Original 4)
1. **users** - User accounts and subscriptions
2. **video-metadata** - Video information and tags
3. **articles** - Blog articles with scripture references
4. **download-jobs** - Video download job tracking

#### New Tables (v2.0)
5. **comments** - Article comments
6. **news** - News articles
7. **resources** - Resource library
8. **contributors** - Election system contributors
9. **races** - Election races
10. **candidates** - Candidate profiles
11. **state-summaries** - State voter guides
12. **email-subscribers** - Email subscription list
13. **email-events** - Email tracking events
14. **pending-changes** - Editor submission approval queue

### API Endpoints v2.0

**Base URLs**:
- Auth API: https://r6l0z3605f.execute-api.us-east-1.amazonaws.com/prod/auth
- Admin API: https://k2avuckm38.execute-api.us-east-1.amazonaws.com/prod/admin
- TAG API: https://h4hoegi26b.execute-api.us-east-1.amazonaws.com/prod/tags
- Articles API: https://fr3hh94h4a.execute-api.us-east-1.amazonaws.com/prod/articles
- Contributors API: https://yvqx5yjqo3.execute-api.us-east-1.amazonaws.com/prod/contributors
- Comments API: https://[api-id].execute-api.us-east-1.amazonaws.com/prod/comments
- News API: https://[api-id].execute-api.us-east-1.amazonaws.com/prod/news
- Resources API: https://fr3hh94h4a.execute-api.us-east-1.amazonaws.com/prod/resources
- Email Subscription API: https://niexv1rw75.execute-api.us-east-1.amazonaws.com

---

## Performance Optimizations v2.0

### Frontend Optimizations
- **CSS Consolidation**: Shared stylesheets reduce page size by 23.6%
- **Unified Navigation**: Cached navbar component across pages
- **Horizontal Scrolling**: Smooth content browsing with arrow navigation
- **Lazy Loading**: Images and videos load on scroll
- **CDN Delivery**: All static assets via CloudFront
- **Pagination**: 24 videos per page, infinite scroll for articles
- **Debounced Search**: 300ms delay for optimal performance

### Backend Optimizations
- **DynamoDB Indexes**: email-index for fast user lookups
- **S3 Presigned URLs**: Direct upload/download without Lambda proxy
- **Lambda Concurrency**: Automatic scaling with reserved concurrency
- **API Gateway Caching**: Enabled for frequently accessed endpoints
- **Thumbnail Pre-generation**: 3 thumbnails created during upload
- **Batch Operations**: Bulk reads/writes where possible

### Database Optimizations
- **Query Patterns**: Optimized for common access patterns
- **Projection**: Only required attributes returned
- **Decimal Conversion**: Automatic conversion for JSON serialization
- **GSI Usage**: Global secondary indexes for efficient queries

---

## Security Enhancements v2.0

### Authentication & Authorization
- **JWT Token System**: HS256 algorithm, 24-hour expiration
- **Standardized Keys**: `auth_token` and `user_data` in localStorage
- **Role-Based Access Control**: Super User > Admin > Editor > User
- **Permission Checks**: verify_admin_token(), verify_editor_token(), is_editor_for_state()
- **Approval Workflow**: Editor submissions require admin approval (unless bypassed)

### Data Security
- **Password Hashing**: SHA-256 with secure storage
- **HTTPS Only**: All API calls require HTTPS
- **Token Validation**: Every protected endpoint validates JWT
- **Rate Limiting**: API Gateway throttling enabled
- **Input Validation**: All user inputs sanitized
- **CORS Configuration**: Proper cross-origin resource sharing

### Privacy Controls
- **Video Visibility**: Public/private with ownership tracking
- **Article Visibility**: Public articles accessible without authentication
- **User Data**: Email addresses converted to display names
- **Content Moderation**: Admin/super user oversight

---

## Deployment Architecture v2.0

### Infrastructure as Code
```yaml
Lambda Functions: 15+
Runtime: Python 3.12
Memory: 256 MB - 3008 MB (varies by function)
Timeout: 15 seconds - 15 minutes
Concurrency: Reserved for critical functions

DynamoDB Tables: 12+
BillingMode: PAY_PER_REQUEST
Indexes: email-index, category-index, state-index

S3 Buckets:
  - my-video-downloads-bucket (videos, thumbnails, static files)
  - CloudFront Distribution: https://christianconservativestoday.com

API Gateway:
  - REST APIs: 8+ endpoints
  - HTTP API v2: Email subscription endpoint
  - CORS: Enabled on all endpoints
```

### Monitoring & Logging
- **CloudWatch Metrics**: Lambda invocations, API Gateway requests, DynamoDB capacity
- **CloudWatch Logs**: All Lambda function logs with error tracking
- **SNS Notifications**: Video download events, subscription events
- **AWS SES**: Email delivery tracking with open/click analytics

### Cost Optimization
**Estimated Monthly Costs (100 active users)**:
```
Lambda Executions: $10-15
DynamoDB (PAY_PER_REQUEST): $10-20
S3 Storage (500GB): $11.50
CloudFront Data Transfer (1TB): $85
API Gateway: $5
AWS SES: $1 (10,000 emails)
Total: ~$125-140/month
```

---

## Future Enhancements

### Planned Features
- **Phase 2 CSS Consolidation**: Card styles and form styles (50%+ additional reduction)
- **JavaScript Consolidation**: Shared utility functions and API constants
- **Discussion Forums**: Q2 2025 - Chat forums for community engagement
- **Resource Center Expansion**: Q3 2025 - Enhanced educational materials
- **Course Platform**: Q4 2025 - Structured learning and certification
- **Mobile Apps**: Q1 2026 - iOS and Android applications
- **Live Streaming**: Real-time video broadcasting
- **AI Sermon Outlines**: AWS Bedrock integration for content generation
- **Prayer Request System**: Community prayer tracking
- **Event Calendar**: Ministry event management
- **Donation Integration**: PayPal/Stripe donation processing

### Technical Roadmap
- **Angular Conversion**: Phase 4 - Modern frontend framework
- **GraphQL API**: Efficient data fetching
- **WebSocket Support**: Real-time updates
- **Progressive Web App**: Offline functionality
- **Advanced Caching**: Redis/ElastiCache integration
- **Multi-Region Deployment**: Global content delivery
- **Automated Testing**: Unit and integration tests
- **CI/CD Pipeline**: Automated deployment workflow

---

## Conclusion

Christian Conservatives Today v2.0 represents a significant evolution from the original platform, with 15+ Lambda functions, 12+ DynamoDB tables, comprehensive election tracking for all 50 US states, advanced analytics, social sharing, email subscription system, and modern UI/UX improvements. The platform now serves as a complete digital ministry solution with enterprise-grade features and scalability.

### Key Achievements v2.0
- ✅ 100% serverless architecture
- ✅ 15+ microservices (Lambda functions)
- ✅ 3-tier role-based access control + Editor role
- ✅ PayPal subscription integration
- ✅ Bible verse integration with multiple translations
- ✅ Automatic thumbnail generation
- ✅ External video embedding
- ✅ Full-text article search
- ✅ Public article access for ministry outreach
- ✅ Election tracking for all 50 US states
- ✅ Email subscription system with tracking
- ✅ Advanced analytics dashboard
- ✅ Social sharing integration
- ✅ Comment system with moderation
- ✅ Horizontal scrolling UI
- ✅ Markdown support
- ✅ Mobile optimization
- ✅ CSS consolidation (23.6% reduction)
- ✅ Unified navigation system
- ✅ Authentication standardization

---

**Platform URL**: https://christianconservativestoday.com  
**Documentation Version**: 2.0  
**Last Updated**: January 2025
