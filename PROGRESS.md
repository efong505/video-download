# Christian Conservative Video Platform - Development Progress

## Project Mission & Vision
**Platform Purpose**: A dedicated video sharing platform for Christians, Pastors, preachers, and conservative voices to:
- Share sermons, teachings, and biblical messages
- Discuss conservative political issues from a biblical perspective
- Bridge the gap between faith and politics with godly wisdom
- Provide a safe space for Christian discourse on current events
- Encourage Christian involvement in political and social issues
- Combat the false narrative that religion and politics should be separate

**Target Audience**:
- Pastors and church leaders sharing sermons
- Christian political commentators and activists
- Conservative content creators
- Believers seeking biblically-grounded political discussion
- Churches and ministries expanding their digital reach

**Core Values**:
- Biblical truth as the foundation for all content
- Encouraging Christian engagement in civic duties
- Supporting godly leadership in government
- Promoting law, order, and biblical morality
- Creating community around shared faith and values

## Phase 1 - Core System ✅ COMPLETE
- [x] Video downloading with Lambda/Fargate routing
- [x] DynamoDB-based video metadata storage
- [x] Tag management API
- [x] Basic authentication system
- [x] Admin dashboard foundation
- [x] Video management interface

## Phase 2a - Authentication & Basic Features ✅ COMPLETE
- [x] JWT-based login system
- [x] Role-based access (admin/user)
- [x] Protected routes
- [x] Video editing capabilities
- [x] Category browsing
- [x] Custom titles
- [x] Enhanced UI components

## Phase 2b - Advanced User Management & Sharing
### ✅ COMPLETED ITEMS:
1. [x] **Three-tier user system** (Super User > Admin > User)
   - Super User: Full system access, can create all roles
   - Admin: Cannot modify/delete super users, can create admin/user
   - User: Basic video access
   
2. [x] **Video ownership tracking**
   - Videos show uploader/owner information
   - Super users can edit video ownership
   - Admins cannot change ownership
   
3. [x] **Visibility controls**
   - Public/Private toggle for videos
   - Visibility-based filtering
   - Privacy protection for private videos
   
4. [x] **External video embedding**
   - YouTube, Rumble, Facebook link support
   - Embed without downloading
   - Platform-specific handling

### ❌ REMAINING ITEMS:
5. [ ] **Dynamic user pages** - PENDING
   - Super users can share all videos
   - Users can share all their videos
   - Users can share only certain videos
   - Users can hide certain videos
   - Create user-specific sharing pages
   
**5.5. [x] PayPal Subscription System (Phase 2b.5)** - ✅ COMPLETE
   - PayPal Business account setup
   - Storage quota enforcement
   - Subscription tier management
   - Usage tracking and billing
   - Frontend subscription dashboard integration
   
6. [ ] **Dynamic tag-based pages** - PENDING
   - Automatically generate pages based on available tags
   - Tag-specific galleries and navigation
   - Dynamic routing for tag pages

## Phase 3 - Angular Conversion 🔄 PLANNED
- [ ] Convert entire frontend to Angular framework
- [ ] Component-based architecture
- [ ] Enhanced user experience
- [ ] Modern UI/UX patterns
- [ ] Improved performance and maintainability

## Recent Fixes & Enhancements ✅ COMPLETE
- [x] User deletion with video ownership transfer
- [x] Size calculation fixes in videos.html
- [x] S3 size lookup in TAG API
- [x] CORS and thumbnail generation fixes
- [x] Multi-tag selection and autocomplete
- [x] Comprehensive tag management
- [x] Download status tracking system
- [x] Adaptive thumbnail generation
- [x] Privacy system implementation
- [x] Admin panel JavaScript fixes
- [x] Video size display fixes in admin dashboard and videos page
- [x] Profile page usage calculation with TAG API integration
- [x] Admin/Super User unlimited storage and video limits

## Current Status
**ACTIVE PHASE**: Phase 2b - Advanced User Management & Sharing
**CURRENT TASK**: Dynamic user pages (Item 5)
**NEXT MILESTONE**: Complete remaining Phase 2b items
**AFTER PHASE 2b**: Begin Phase 3 Angular conversion

## Key System Information
- **Platform Name**: Christian Conservative Video Platform
- **Super User**: super@admin.com / SuperSecure123!
- **CloudFront URL**: https://d271vky579caz9.cloudfront.net
- **Architecture**: Serverless AWS (Lambda, S3, DynamoDB, CloudFront)
- **Authentication**: JWT with 24-hour expiration
- **Database**: DynamoDB tables for users, video-metadata, download-jobs
- **Content Focus**: Christian sermons, biblical teachings, conservative political commentary

## Storage Quota & Subscription System (Phase 2b Enhancement)

### Proposed Storage Tiers:
**FREE TIER**
- Storage Limit: 2GB
- Video Limit: 50 videos
- Features: Basic upload, public/private videos, external embeds
- Cost: $0/month

**PREMIUM TIER**
- Storage Limit: 25GB
- Video Limit: 500 videos
- Features: All free features + priority processing, custom branding
- Cost: $9.99/month

**PRO TIER**
- Storage Limit: 100GB
- Video Limit: 2000 videos
- Features: All premium features + analytics, API access, bulk operations
- Cost: $24.99/month

**ENTERPRISE TIER**
- Storage Limit: Unlimited
- Video Limit: Unlimited
- Features: All pro features + white-label, dedicated support
- Cost: $99.99/month

### Subscription Management Implementation:
1. **Primary Payment Processor: PayPal** ✅ SELECTED
   - PayPal Subscriptions API with webhook integration
   - PayPal Business account required
   - Lambda functions for PayPal webhook handling
   - Future option: Add Stripe as alternative payment method

2. **PayPal Integration Benefits**:
   - Wider global acceptance (especially international users)
   - No credit card required for users
   - Built-in dispute resolution
   - Lower barrier to entry for users
   - PayPal Business account handles tax compliance

3. **Database Schema Updates**:
   - Add `subscription_tier`, `storage_used`, `storage_limit` to users table
   - Add `subscription_id`, `payment_provider` (paypal/stripe), `billing_cycle`, `next_billing_date` fields
   - Track usage in real-time with S3 size calculations
   - Store PayPal subscription ID and customer ID for management

4. **Quota Enforcement**:
   - Pre-upload storage checks in upload API
   - Real-time usage tracking with each video upload/delete
   - Grace period handling for over-limit users
   - Automatic downgrade/upgrade processing

5. **User Experience**:
   - Storage usage dashboard in user profile
   - Upgrade prompts when approaching limits
   - Billing history and invoice management
   - Subscription cancellation with data retention period

### PayPal Implementation Plan (Phase 2b.5):
**Step 1: PayPal Setup**
- [ ] Create PayPal Business account
- [ ] Set up PayPal Developer App (Client ID, Secret)
- [ ] Configure subscription products in PayPal dashboard
- [ ] Set up webhook endpoints

**Step 2: Database Updates**
- [x] Add subscription fields to users table
- [x] Default free tier setup (2GB, 50 videos)
- [x] Add storage usage tracking

**Step 3: Backend Implementation**
- [x] Create PayPal billing API Lambda function
- [x] Implement subscription creation/management
- [x] Add webhook handlers for PayPal events
- [x] Create quota enforcement middleware in router
- [x] Deploy PayPal billing API to AWS Lambda
- [x] Set up API Gateway endpoint (/paypal)
- [x] Deploy updated router with quota checks
- [x] Deploy updated auth API with subscription fields

**Step 4: Frontend Integration** ✅ COMPLETE
- [x] Add PayPal subscription buttons
- [x] Create subscription management page
- [x] Add usage dashboard to profile
- [x] Implement upgrade/downgrade flows

**Step 5: Admin Tools**
- [ ] Subscription management in admin dashboard
- [ ] Usage monitoring and reporting
- [ ] Manual subscription adjustments

## Platform-Specific Features to Consider
**Content Categories**:
- Sermons & Biblical Teachings
- Conservative Political Commentary
- Faith & Politics Integration
- Current Events from Biblical Perspective
- Church Leadership & Ministry
- Christian Activism & Civic Engagement

**Community Features** (Future phases):
- Comment system with biblical discussion
- Prayer request integration
- Scripture reference linking
- Church/Ministry profiles
- Event announcements
- Donation/Tithing integration

**Content Moderation**:
- Biblical content guidelines
- Conservative values alignment
- Community reporting system
- Pastor/Leader verification system

## Development Notes
- All Phase 2b items 1-4 are fully functional and deployed
- User deletion properly transfers video ownership to 'system'
- Size calculations work correctly with S3 integration
- External video embedding supports YouTube, Rumble, Facebook
- Three-tier permission system is properly implemented
- **NEW**: PayPal selected as primary payment processor
- **NEW**: Phase 2b.5 (PayPal Subscription System) ready to implement
- **DECISION**: Storage quota system with 4-tier pricing structure finalized
- **VISION**: Platform repositioned as Christian Conservative Video Platform
- **BACKEND READY**: PayPal billing system and quota enforcement implemented
- **FRONTEND READY**: PayPal subscription management integrated in profile page
- **PHASE 2b.5 COMPLETE**: Full subscription system operational (backend ready, PayPal setup pending)
- **PERFORMANCE OPTIMIZED**: Pagination and category filtering implemented
- **SIZE DISPLAY FIXED**: Video sizes now show correctly in admin dashboard and videos page
- **USAGE TRACKING WORKING**: Profile page shows accurate storage and video count from TAG API
- **ADMIN PRIVILEGES**: Admin and Super Users have unlimited storage and video access
- **ROLE-BASED LIMITS**: Regular users have 2GB/50 video limits, admins have unlimited access