# Christian Conservative Video Platform

## 📖 Executive Summary

**Transform Your Ministry's Digital Presence**

A revolutionary serverless platform designed specifically for Christians, pastors, and conservative voices to share videos, write biblically-grounded articles, and build thriving online communities. Combining cutting-edge AWS technology with ministry-focused tools, this platform bridges the gap between faith and digital engagement.

**Perfect For:**
- ⛪ Churches expanding their digital reach
- 🎤 Pastors sharing sermons and teachings
- 📰 Christian political commentators
- 📚 Bible study groups and ministries
- 🎆 Conservative content creators
- 👥 Faith-based communities

## ⚡ Key Features at a Glance

### 🎥 **Advanced Video Management**
- Download and host videos from YouTube, Rumble, Facebook
- Smart Lambda/Fargate processing for any video length
- Automatic thumbnail generation and optimization
- Public/private visibility controls
- External video embedding without storage usage

### ✍️ **Christian Blog & Article System**
- Rich text editor with integrated Bible verse lookup
- Multiple Bible translations (KJV, ASV, YLT) with fallback support
- Ministry-focused templates (Sermons, Political Commentary, Bible Study)
- Automatic scripture reference tracking and extraction
- Role-based article management and deletion

### 🔐 **Enterprise-Grade Security**
- Three-tier role system (Super User > Admin > User)
- JWT-based authentication with 24-hour expiration
- Granular permission controls
- Secure API endpoints with CORS protection

### 💳 **Flexible Subscription System**
- PayPal-integrated billing with automated quota enforcement
- Four tiers: Free (2GB) to Enterprise (Unlimited)
- Real-time usage tracking and upgrade prompts
- Admin/Super User unlimited access

## 🏢 Technical Excellence
**Serverless Architecture**: AWS Lambda, S3, DynamoDB, CloudFront, API Gateway
**Modern Frontend**: HTML5, Bootstrap 5, Quill.js rich text editor
**Integrated APIs**: Bible verse lookup, PayPal billing, intelligent video processing
**Performance**: CDN-optimized delivery, pagination, smart caching

## 🚀 Live Demo
**Platform URL**: https://videos.mytestimony.click
**Demo Credentials**: admin@test.com / AdminPass123!
**Super User Access**: super@admin.com / SuperSecure123!

---

## 🎯 Detailed Platform Overview

A complete serverless video management system built on AWS with intelligent Lambda/Fargate routing, authentication, admin dashboard, and comprehensive video management capabilities.

## 📋 Core Features

### Phase 1 - Foundation System ✅ COMPLETE
- **Video Download**: Download videos from YouTube, Rumble, and other platforms
- **Video Upload**: Direct upload to S3 with automatic thumbnail generation
- **External Video Support**: Add YouTube, Rumble, and Facebook videos without downloading
- **Intelligent Routing**: Automatic Lambda/Fargate selection based on video length
- **Thumbnail Generation**: Automatic thumbnail creation for uploaded/downloaded videos
- **Performance Optimization**: Pagination with category filtering for improved loading

### Phase 2a - Authentication & Basic Features ✅ COMPLETE
- **JWT-based Authentication**: 24-hour token expiration
- **Three-tier Role System**: Super User > Admin > User hierarchy
- **Role-based Permissions**: Granular access control
- **User Management**: Create, edit, delete users with role restrictions
- **Video Management**: Ownership system with transfer capabilities
- **Visibility Controls**: Public/Private video settings

### Phase 2b - Advanced User Management & Sharing ✅ COMPLETE
- **Dynamic User Pages**: User-specific video sharing pages with statistics
- **Tag-Based Pages**: Tag-specific video galleries with related content
- **PayPal Subscription System**: Automated billing and quota enforcement
- **Storage Quota Management**: Real-time tracking and upgrade prompts
- **External Video Integration**: Platform detection and embedded playback

### Phase 3 - Christian Blog & Article System ✅ COMPLETE
- **Rich Text Editor**: Quill.js editor with Bible verse integration
- **Bible Integration**: Search and insert verses from multiple translations (KJV, ASV, YLT)
- **Article Templates**: Pre-built templates for sermons, political commentary, and Bible study
- **Article Management**: Full CRUD operations with role-based permissions
- **Scripture References**: Automatic extraction and tracking of Bible verses
- **Category System**: Sermons, Politics, Devotionals, Apologetics, Ministry, Bible Study, General
- **Search & Filter**: Find articles by title, content, category, author, or tags
- **Analytics**: Reading time calculation and view count tracking

## 🏗️ Technical Architecture

### AWS Services Used
- **Lambda Functions**: Video processing, APIs, thumbnail generation
- **Fargate**: Heavy video processing tasks
- **S3**: Video and thumbnail storage with CloudFront CDN
- **DynamoDB**: User data, video metadata, articles, job tracking
- **API Gateway**: RESTful API endpoints with CORS support
- **SNS**: Email notifications

### API Endpoints
- **Auth API**: User authentication and JWT management
- **Admin API**: Administrative operations and user management
- **TAG API**: Video metadata and tag management
- **Router API**: Download job routing and management
- **Articles API**: Blog/article management with Bible integration
- **PayPal Billing API**: Subscription management and quota enforcement

## 💾 Database Schema

### Users Table
- `user_id` (Primary Key), `email`, `password_hash`, `role`
- `first_name`, `last_name`, `subscription_tier`, `storage_used`
- `created_at`, `updated_at`, `active`

### Video Metadata Table
- `video_id` (Primary Key), `filename`, `title`, `tags[]`
- `owner`, `visibility`, `video_type`, `external_url`
- `upload_date`, `created_at`

### Articles Table
- `article_id` (Primary Key), `title`, `content`, `author`
- `category`, `tags[]`, `visibility`, `scripture_references[]`
- `reading_time`, `view_count`, `created_at`, `updated_at`

### Download Jobs Table
- `job_id` (Primary Key), `status`, `progress`, `error_message`
- `created_at`, `updated_at`

## 💰 Subscription Plans

### Free Tier
- **Storage**: 2GB
- **Videos**: 50 videos maximum
- **Features**: Basic upload, public/private videos, external embeds
- **Cost**: Free

### Premium Tier ($9.99/month)
- **Storage**: 25GB
- **Videos**: 500 videos maximum
- **Features**: All free features + priority processing, custom branding
- **PayPal**: Automatic billing and management

### Pro Tier ($24.99/month)
- **Storage**: 100GB
- **Videos**: 2000 videos maximum
- **Features**: All premium features + analytics, API access, bulk operations

### Enterprise Tier ($99.99/month)
- **Storage**: Unlimited
- **Videos**: Unlimited
- **Features**: All pro features + white-label, dedicated support

### Admin/Super User Access
- **Unlimited Storage**: No storage restrictions
- **Unlimited Videos**: No video count limits
- **Full Access**: All platform features available

## 🛠️ Installation & Deployment

### Prerequisites
- AWS CLI configured with appropriate permissions
- Python 3.9+ for Lambda functions
- S3 bucket for video storage
- CloudFront distribution for CDN

### Lambda Functions
1. **video-downloader**: Main video processing
2. **video-router**: Job routing logic
3. **video-tag-api**: Metadata management
4. **admin-api**: Administrative operations
5. **auth-api**: Authentication and user management
6. **thumbnail-generator**: Thumbnail creation
7. **articles-api**: Blog/article management with Bible integration
8. **paypal-billing-api**: Subscription and quota management

### Frontend Files
- `index.html`: Landing page with platform overview
- `login.html`: Authentication interface
- `videos.html`: Video gallery with pagination and filtering
- `admin.html`: Comprehensive admin dashboard
- `profile.html`: User profile with subscription management
- `articles.html`: Article listing and browsing
- `create-article.html`: Article creation with Bible integration
- `edit-article.html`: Article editing with full CRUD capabilities
- `article.html`: Individual article viewer
- `user-page.html`: Dynamic user-specific pages
- `tag-page.html`: Tag-based video galleries

## 🎯 Usage Guide

### For End Users
1. **Registration**: Create account with email and password
2. **Video Access**: Browse public videos and own private content
3. **Article Reading**: Access articles with Bible verse integration
4. **Subscription Management**: Upgrade plans via PayPal integration

### For Content Creators
1. **Video Upload**: Direct upload or external video linking
2. **Article Creation**: Use rich text editor with Bible verse lookup
3. **Content Management**: Organize with tags and categories
4. **Analytics**: Track views and engagement

### For Administrators
1. **User Management**: Full CRUD operations for user accounts
2. **Content Moderation**: Edit metadata, manage visibility
3. **System Monitoring**: Track usage, subscriptions, and performance
4. **Template Management**: Create and modify article templates

### For Super Users
- All admin capabilities plus system-wide control
- Create other super users and admins
- Unlimited storage and video access

## 🔧 Advanced Features

### Bible Verse Integration
- **Supported Translations**: KJV, ASV (1901), YLT (NT only)
- **Search Format**: "John 3:16", "1 John 1:9", "Romans 8:28"
- **Auto-formatting**: Verses inserted as styled blockquotes
- **Reference Tracking**: Automatic scripture reference extraction

### Article Templates
- **Sermon Template**: Scripture → Prayer → Main Points → Application → Closing Prayer
- **Political Commentary**: Biblical Foundation → Current Issue → Christian Response → Call to Action
- **Bible Study Template**: Observation → Interpretation → Reflection → Application → Prayer
- **Service Notes**: Structured format for church service observations

### External Video Support
- **YouTube**: Full embed support with automatic thumbnail generation
- **Rumble**: Embed support with video ID extraction
- **Facebook**: Basic embed support with platform restrictions

## 🔒 Security & Privacy

### Authentication
- JWT tokens with 24-hour expiration
- Secure password hashing
- Role-based access control

### Data Protection
- Private videos only visible to owners and admins
- Secure API endpoints with CORS protection
- Encrypted data transmission

### Content Moderation
- Role-based content management
- Visibility controls for sensitive content
- Admin oversight capabilities

## 🚨 Troubleshooting

### Common Issues
1. **Video Upload Failures**: Check file size limits and format compatibility
2. **Bible Verse Lookup Errors**: Verify reference format and translation availability
3. **Authentication Problems**: Check JWT token expiration and credentials
4. **Subscription Issues**: Verify PayPal webhook configuration
5. **Performance Issues**: Pagination implemented for large content libraries

### Debug Features
- Console logging in browser developer tools
- Download status tracking page
- Comprehensive error messages in admin dashboard

## 🔮 Future Enhancements (Phase 4)

### Planned Features
- **Angular Conversion**: Modern component-based frontend
- **Mobile App**: Native iOS/Android applications
- **Advanced Ministry Tools**: AI-assisted sermon outlines, prayer request system
- **Community Features**: Discussion forums, Bible study groups
- **Live Streaming**: Integrated live video capabilities
- **Social Integration**: Enhanced sharing and embedding options

## 📞 Support & Documentation

### Default Credentials
- **Super User**: super@admin.com / SuperSecure123!
- **Platform URL**: https://videos.mytestimony.click
- **CloudFront CDN**: https://d271vky579caz9.cloudfront.net

### Development
- Built with serverless-first architecture
- Comprehensive API documentation
- Modular Lambda function design
- Scalable DynamoDB schema

## 📄 License

This project is designed for educational and ministry use, promoting Christian values and conservative political engagement through digital platforms.

---

**Empowering Christian voices in the digital age through cutting-edge technology and biblical integration.**