# Christian Conservatives Today - Complete Project Continuation Prompt (v3.0)

I'm working on **Christian Conservatives Today**, a comprehensive AWS serverless platform combining video hosting, article publishing, nationwide election tracking (ALL 50 STATES COMPLETE), email marketing, and community engagement for Christian conservative ministry.

## **Project Location**
`c:\Users\Ed\Documents\Programming\AWS\Downloader\`

## **Platform URL**
https://christianconservativestoday.com

---

## **PLATFORM OVERVIEW**

### **Mission**
Platform for the 5-fold ministry (apostles, prophets, evangelists, pastors, teachers), Christian believers, and conservative voices to share sermons, publish articles with Bible integration, track elections across all 50 US states, and engage communities without censorship.

### **Key Statistics**
- **Architecture**: 100% Serverless (AWS Lambda, S3, DynamoDB, CloudFront)
- **Lambda Functions**: 17+ microservices
- **Database Tables**: 15+ DynamoDB tables
- **Election Coverage**: ALL 50 US STATES COMPLETE (290+ races, 197+ candidates, 50 comprehensive voter guides)
- **User Roles**: 4-tier system (Super User > Admin > Editor > User)
- **Domain**: christianconservativestoday.com (migrated from videos.mytestimony.click)

---

## **PART 1: VIDEO MANAGEMENT SYSTEM**

### **Video Download & Processing**
- **Platforms**: YouTube, Rumble, Facebook
- **Engine**: yt-dlp + FFmpeg layers
- **Routing**: Lambda (< 15 min) or Fargate (> 15 min)
- **Thumbnails**: Auto-generate 3 thumbnails (10%, 50%, 90% of duration)
- **Storage**: S3 with CloudFront CDN delivery
- **Quota**: Enforced by subscription tier

**Key Files**:
- `router/index.py` - Quota management and job routing
- `downloader/index.py` - Video download with yt-dlp + FFmpeg
- `thumbnail_generator/index.py` - Auto-generate thumbnails
- `video-downloader.html` - Frontend interface
- `videos.html` - Gallery with Netflix-style horizontal scrolling

**Features**:
- External video embedding (YouTube, Rumble, Facebook)
- Platform auto-detection
- S3 presigned URLs for direct uploads
- Public/private visibility controls
- Video ownership tracking
- Share functionality with copy-to-clipboard
- Category ordering system (admin-configurable)
- Bulk video editing (multi-select, delete, visibility, tags)
- Video sorting (6 options: newest/oldest, title A-Z/Z-A, largest/smallest)

---

## **PART 2: ARTICLE & BLOG SYSTEM**

### **Rich Text Editor**
- **Editor**: Quill.js with custom toolbar
- **Bible Integration**: KJV, ASV, YLT translations via bible-api.com
- **Markdown Support**: Dual-mode editing (WYSIWYG ↔ Markdown)
- **Templates**: Sermon, Political Commentary, Service Notes, Bible Study

**Key Files**:
- `create-article.html` - Article creation with Bible lookup
- `edit-article.html` - Article editing
- `articles.html` - Listing with search and horizontal scrolling
- `article.html` - Individual article view
- `articles_api/index.py` - Backend with Bible integration

**Features**:
- Bible verse search and insertion (multiple translations)
- Scripture reference extraction
- Reading time calculation (200 words/min)
- View tracking and analytics
- Featured images with Open Graph integration
- Social sharing (Facebook, Twitter, LinkedIn)
- Public article access (no auth required for public articles)
- Full-text search with relevance scoring
- Related articles suggestions (algorithm-based)
- Comment system with moderation (nested replies, bulk actions)
- Markdown/HTML entity decoding
- Quill editor list preservation fix

**Categories**: Sermons, Politics, Devotionals, Apologetics, Ministry, Bible Study, General

---

## **PART 3: AUTHENTICATION & USER MANAGEMENT**

### **Four-Tier Role System**
```
Super User → Admin → Editor → User
```

- **Super User**: Full access, create all roles, unlimited storage
- **Admin**: User management (except super users), unlimited storage
- **Editor**: Create/edit content for assigned states, approval workflow
- **User**: Upload videos (quota-limited), create articles, manage own content

### **JWT Authentication**
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: 24 hours
- **Storage**: localStorage (auth_token, user_data)

**Key Files**:
- `auth_api/index.py` - JWT generation and validation
- `login.html` - Login interface
- `profile.html` - User profile with subscription management

**localStorage Keys (Standardized)**:
- `auth_token` - JWT token
- `user_data` - JSON object {email, first_name, last_name, role}

---

## **PART 4: SUBSCRIPTION & BILLING SYSTEM**

### **Subscription Tiers**
- **FREE**: 2GB, 50 videos, $0/month
- **PREMIUM**: 25GB, 500 videos, $9.99/month
- **PRO**: 100GB, 2000 videos, $24.99/month
- **ENTERPRISE**: Unlimited, $99.99/month

### **PayPal Integration**
- **Status**: LIVE PRODUCTION MODE
- **Features**: Subscription creation/cancellation, webhook events, quota enforcement, automatic downgrades, grace period
- **Files**: `paypal_billing_api/index.py`, `profile.html`

---

## **PART 5: ELECTION TRACKING SYSTEM - ALL 50 STATES COMPLETE ✅**

### **Interactive Election Map**
**File**: `election-map.html`

**Features**:
- Clickable SVG US map (mobile-responsive with viewBox)
- State summaries with markdown rendering
- Expand button (🔍) for full-screen viewing
- Download: PDF (html2canvas) and TXT formats
- Party badges (R-red, D-blue, third parties-gray)

### **Admin Interface**
**File**: `admin-contributors.html`

**Features**:
- **Dual-mode editor** for state summaries:
  - Markdown mode (📝): Textarea
  - Rich Text mode (🎨): Quill.js WYSIWYG
  - Separate storage: `markdownContent` and `htmlContent`
  - Content detection: Checks if starts with '<' for HTML vs markdown
- Race management (CSV bulk import with auto-matching)
- Candidate management (party dropdown, faith statements, positions)
- Contributor management (first_name, last_name, phone_number)
- Editor role system with approval workflow
- Bypass approval toggle for trusted editors
- Pending changes queue with admin review

### **Voter Guides - ALL 50 STATES COMPLETE**
**Location**: `Voter Guides_Summaries/` folder

**Coverage**: 50/50 states (100% complete)
- Comprehensive 15,000-30,000 character guides per state
- 2025 state races + 2026 federal races
- Christian conservative perspective
- Political landscape analysis
- Priority races and candidate profiles
- Key issues breakdown (8 focus areas)
- Church mobilization strategies
- Prayer points with scripture verses

**Template System**:
- Master template generation system (950 files across 50 states)
- State-size-based scaling (Large/Medium/Small)
- Flexible candidate counts ("UP TO X" prevents fake generation)
- Based on New Jersey's detailed structure

**CSV Format**:
- races.csv: state, office, election_date, race_type, description
- candidates.csv: name, state, office, party, bio, website, faith_statement, positions, endorsements

**Scripts**:
- `scan_election_data.py` - Scan DynamoDB
- `upload_[state]_data.py` - State-specific uploads
- `update_candidate.py` - Update candidate fields
- `validate_election_data.py` - Data quality checker

**Coverage Statistics**:
- **States**: 50/50 (100%)
- **Races**: 290+
- **Candidates**: 197+
- **Voter Guides**: 50 comprehensive (12,000-30,000 chars each)

---

## **PART 6: EMAIL SUBSCRIPTION & TRACKING**

### **AWS SES Integration**
**Email**: contact@christianconservativestoday.com
**Lambda**: email-subscription-handler (Python 3.12)

**Features**:
- Email subscription form on election-map.html
- Welcome email with tracking
- Open tracking (1x1 pixel)
- Click tracking (redirect URLs)
- Newsletter campaigns
- Analytics dashboard
- 95% cheaper than Mailchimp ($1 per 10,000 emails)

**Database Tables**:
- `email-subscribers` - Subscriber management
- `email-events` - Open/click tracking

**API Endpoint**: https://niexv1rw75.execute-api.us-east-1.amazonaws.com

---

## **PART 7: NEWSLETTER SYSTEM**

### **Professional Email Templates**
**File**: `admin-newsletters.html`

**Features**:
- 5 professional templates (Modern Gradient, Classic, Patriotic, Minimalist, Bold Impact)
- Dual editor (Visual contenteditable + HTML textarea)
- Campaign/segment management (4 default campaigns)
- Mail merge personalization ({{first_name}}, {{last_name}}, {{email}}, {{unsubscribe_link}})
- Open tracking & analytics
- Enhanced subscriber management (email, first_name required, last_name/phone optional)
- Auto-digest newsletter (weekly automated generation)
- Newsletter archive (public page with search and share)

**Why contenteditable instead of Quill?**
- Quill strips inline styles and complex HTML
- Email templates require inline CSS
- contenteditable preserves all HTML/CSS

---

## **PART 8: ADVANCED MINISTRY TOOLS**

### **Prayer Request System**
**Files**: `prayer-wall.html`, `admin-prayers.html`, `prayer_api`

**Features**:
- Public prayer wall with submit form
- "I Prayed" tracking
- Admin moderation workflow
- Category filtering (personal, election, ministry, nation, state)
- Testimony system for answered prayers
- State-specific prayer filtering

### **Event Calendar Integration**
**Features**:
- FullCalendar.js integration
- Event CRUD operations
- CSV bulk import
- Election date sync
- Registration tracking
- State/category filtering
- ICS export

### **Email Notification System**
**Features**:
- 4 integrated notification types (comment reply, prayer update, article publication, admin alert)
- User preference management (notification-settings.html)
- Professional branded email templates
- Real-time notification count badge in navbar
- Respects user opt-in/opt-out preferences

---

## **PART 9: NEWS MANAGEMENT SYSTEM**

### **News Features**
**Files**: `news.html`, `news_api/index.py`

**Features**:
- Breaking news banners
- Scheduled publishing with auto-status logic
- State-specific election coverage
- External link support
- Topic categorization (politics, culture, religious freedom, family, pro-life)
- Horizontal scrolling UI
- Author name display (fixed from email addresses)

---

## **PART 10: RESOURCE MANAGEMENT**

### **Resource Features**
**Files**: `resources.html`, `resources_api/index.py`, `admin-resources.html`

**Features**:
- Emoji icons for 47 category keywords
- Edit functionality (complete CRUD)
- Category bulk rename
- Auto-summary with AWS Bedrock AI
- Empty category cleanup
- Multiple categories per resource (array support with backward compatibility)

---

## **PART 11: UI/UX ENHANCEMENTS**

### **Unified Navigation System**
**Files**: `navbar.html`, `navbar.js`

**Features**:
- Reusable navbar component
- Role-based access control
- Dual icon support (emoji and Font Awesome)
- Mobile responsive with hamburger menu
- Fixed positioning with proper page padding

**Pages with Unified Navbar** (10 total):
- index.html, videos.html, articles.html, news.html, resources.html
- election-map.html, profile.html, user-page.html, article.html, news-article.html

### **Horizontal Scrolling UI**
**Implementation**: Netflix-style content browsing

**Pages**:
- videos.html (300px cards, 320px scroll)
- resources.html (400px cards, 420px scroll)
- articles.html (450px cards, 470px scroll)
- news.html (400px cards, 420px scroll)

**Features**:
- Arrow navigation (desktop only, hidden on mobile)
- Touch-friendly mobile scrolling
- Category-based grouping
- Smooth scrolling with visual feedback

### **CSS Consolidation**
**Shared Stylesheets**:
- `assets/css/common-styles.css` - Navigation and dashboard styles (2.5 KiB)
- `assets/css/card-styles.css` - Card components
- `assets/css/form-styles.css` - Form elements

**Benefits**:
- 75+ duplicate CSS rules removed (23.6% reduction)
- Single source of truth
- Improved maintainability
- Better performance (cached assets)

### **Mobile Optimization**
**Responsive Breakpoints**:
- Desktop: Default styles
- Tablet (768px): Reduced font sizes and padding
- Mobile (576px): Further reduced spacing
- Android (422px): Special padding adjustments

**Features**:
- Progressive mobile breakpoints
- Touch-friendly button sizes
- Proper navigation wrapping
- Consistent user experience across devices

### **PWA (Progressive Web App)**
**Files**: `manifest.json`, `service-worker.js`, `pwa-install.js`

**Features**:
- Install as native-like app on mobile and desktop
- Offline caching and background sync
- Auto-install prompt after 30 seconds
- Push notification support (ready for future)
- 8 icon sizes (72x72 to 512x512)
- Standalone display mode

---

## **TECHNICAL STACK**

### **Frontend**
- HTML5, CSS3, JavaScript (ES6+)
- Bootstrap 5
- jQuery
- Quill.js (rich text editor)
- marked.js (markdown rendering)
- html2canvas (PDF generation)
- FullCalendar.js (event calendar)

### **Backend**
- AWS Lambda (Python 3.9-3.12)
- AWS S3 (storage)
- AWS DynamoDB (NoSQL database)
- AWS API Gateway (REST APIs)
- yt-dlp (video downloading)
- FFmpeg (video processing)
- AWS Bedrock (AI summarization)
- AWS SES (email delivery)

### **Authentication**
- JWT tokens (PyJWT library)
- localStorage (auth_token, user_data)
- Role-based access control

---

## **AWS LAMBDA FUNCTIONS (17+ Total)**

1. **auth-api** - User authentication and JWT management
2. **admin-api** - Administrative operations and user management
3. **tag-api** - Video metadata and tag management
4. **router** - Job routing and quota enforcement
5. **downloader** - Video download and processing (yt-dlp + FFmpeg)
6. **articles-api** - Blog/article management with Bible integration
7. **paypal-billing-api** - Subscription management and quota enforcement
8. **thumbnail-generator** - Generate thumbnails for uploaded videos
9. **s3-thumbnail-trigger** - S3 event trigger for thumbnail generation
10. **url-analysis-api** - URL content extraction and AI summarization
11. **news-api** - News article management with scheduled publishing
12. **resources-api** - Resource library management
13. **contributors-api** - State election coverage and contributor management
14. **email-subscription-handler** - Email subscription and tracking
15. **video-list-api** - Video listing and filtering
16. **article-analysis-api** - Article analytics and view tracking
17. **comments-api** - Comment management
18. **newsletter-api** - Newsletter system with campaigns
19. **prayer-api** - Prayer request system

---

## **DYNAMODB TABLES (15+ Total)**

1. **users** - User accounts, roles, subscription data
2. **video-metadata** - Video metadata, tags, ownership
3. **articles** - Article content, authors, categories
4. **download-jobs** - Video download job tracking
5. **comments** - User comments on articles
6. **news** - News articles with topics and states
7. **resources** - Resource library with categories (array support)
8. **contributors** - State correspondents with contact info
9. **races** - Election races (290+ across 50 states)
10. **candidates** - Candidate profiles (197+ with faith statements)
11. **state-summaries** - Comprehensive voter guides (50 states)
12. **pending-changes** - Editor approval workflow
13. **email-subscribers** - Email subscription management
14. **email-events** - Open/click tracking events
15. **templates** - Article templates
16. **prayer-requests** - Prayer request system
17. **events** - Event calendar
18. **newsletters** - Newsletter campaigns

---

## **DEPLOYMENT & SCRIPTS**

### **PowerShell Deployment Scripts**
- `deploy-all.ps1` - Deploy all Lambda functions
- `deploy-router.ps1` - Deploy router Lambda
- `deploy-election-system.ps1` - Deploy election system
- `deploy-news-api.ps1` - Deploy news API
- `deploy-articles-api.ps1` - Deploy articles API
- `deploy-resources-api.ps1` - Deploy resources API
- `s3-push.ps1` - Push static files to S3
- `aws-download.ps1` - Download files from S3

### **Monitoring Scripts**
- `live-logs.ps1` - Real-time Lambda logs
- `check-lambda-status.ps1` - Check Lambda function status
- `diagnose-stuck.ps1` - Diagnose stuck downloads
- `timeout-monitor.ps1` - Monitor Lambda timeouts

### **Utility Scripts**
- `git-commit.ps1` - Quick git commit
- `quick-commit.ps1` - Fast commit with message
- `cost-calculator.ps1` - AWS cost estimation

---

## **DOCUMENTATION**

### **Key Documentation Files** (in `docs/` folder)
- `PROGRESS.md` - Overall project progress (comprehensive history)
- `TECHNICAL_DOCUMENTATION.md` - Technical specs and architecture
- `TECHNICAL_DOCUMENTATION_v2.md` - Updated v2.0 architecture
- `SALES_FLYER_v2.md` - Updated sales materials with v2.0 features
- `README_v2.md` - Comprehensive documentation index
- `DEPLOYMENT_SUMMARY.md` - Deployment guide
- `NEWS_MANAGEMENT_SYSTEM.md` - News system docs
- `ARTICLE_ANALYTICS.md` - Analytics implementation
- `USER_UPLOAD_FIXES.md` - User upload troubleshooting
- `aws-commands-guide.md` - AWS CLI reference
- `DYNAMODB_QUERY_GUIDE.md` - DynamoDB query patterns

### **Election System Documentation**
- `Election Data and Files/ELECTION_DATA_WORKFLOW.md` - Annual election cycle workflow
- `Election Data and Files/Templates/FORMATTING_RULES.md` - Voter guide standards
- `Election Data and Files/Templates/state_summary_template.md` - Blank template
- `Election Data and Files/Templates/AI_PROMPT_TEMPLATE.md` - AI-assisted content creation

### **Email System Documentation**
- `Election Data and Files/Email and Tracking/README.md` - System overview
- `Election Data and Files/Email and Tracking/QUICK_START.md` - 30-minute setup guide
- `Election Data and Files/Email and Tracking/setup_instructions.md` - Detailed setup

### **Newsletter System Documentation**
- `docs/NEWSLETTER_ENHANCEMENTS.md` - Complete feature documentation
- `docs/NEWSLETTER_SYSTEM_GUIDE.md` - User guide
- `docs/AUTO_DIGEST_GUIDE.md` - Auto-digest system guide

---

## **CURRENT STATE**

### **Video/Content System**
- ✅ Video download and processing pipeline
- ✅ Article/news creation and management
- ✅ User authentication and authorization
- ✅ Comment system with moderation
- ✅ Tag/category system
- ✅ Thumbnail generation
- ✅ Bible verse integration (KJV, ASV, YLT)
- ✅ PayPal billing integration (LIVE PRODUCTION MODE)
- ✅ Analytics tracking
- ✅ Dual-mode content editor (WYSIWYG/Markdown)
- ✅ Video sorting (6 options)
- ✅ Bulk video editing

### **Election System**
- ✅ ALL 50 US STATES with comprehensive coverage (100% complete)
- ✅ 290+ races, 197+ candidates
- ✅ Interactive US map with clickable states (mobile-responsive)
- ✅ State summary modals with markdown rendering
- ✅ Expand modal for full-screen viewing
- ✅ Download functionality (PDF with emoji support, TXT)
- ✅ Dual-mode editor (markdown/rich text) for summaries
- ✅ Race and candidate management interface
- ✅ CSV import with auto-matching
- ✅ Comprehensive voter guides (50 states, 15,000-30,000 chars each)
- ✅ Editor role system with approval workflow
- ✅ Complete template system (950 files across 50 states)
- ✅ Party badges with color coding

### **Email & Newsletter System**
- ✅ AWS SES integration with tracking
- ✅ Open tracking (1x1 pixel)
- ✅ Click tracking (redirect URLs)
- ✅ Newsletter campaigns with 5 professional templates
- ✅ Dual editor (Visual + HTML)
- ✅ Mail merge personalization
- ✅ Auto-digest generator
- ✅ Newsletter archive
- ✅ Analytics dashboard
- ✅ 95% cheaper than Mailchimp

### **Advanced Ministry Tools**
- ✅ Prayer request system with moderation
- ✅ Event calendar integration
- ✅ Email notification system (4 types)

### **UI/UX**
- ✅ Unified navigation system (navbar.html/navbar.js)
- ✅ Horizontal scrolling UI (Netflix-style)
- ✅ CSS consolidation (23.6% reduction, 75+ rules removed)
- ✅ Mobile optimization (progressive breakpoints)
- ✅ Authentication standardization (auth_token, user_data)
- ✅ PWA implementation (install as native app)
- ✅ Domain migration (christianconservativestoday.com)

---

## **KEY TECHNICAL PATTERNS**

### **Dual-Mode Editor**
```javascript
// Separate content storage prevents data corruption
let markdownContent = '';
let htmlContent = '';

function switchToMarkdown() {
    htmlContent = quill.root.innerHTML;
    // Display markdownContent in textarea
}

function switchToRichText() {
    markdownContent = textarea.value;
    quill.root.innerHTML = marked.parse(markdownContent);
}
```

### **Content Detection**
```javascript
const content = summary.content || '';
if (content.startsWith('<')) {
    htmlContent = content;  // HTML
    markdownContent = '';
} else {
    markdownContent = content;  // Markdown
    htmlContent = '';
}
```

### **PDF Generation with Emojis**
```javascript
// Uses html2canvas (NOT jsPDF's html() method)
html2canvas(element, { scale: 2 }).then(canvas => {
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF();
    pdf.addImage(imgData, 'PNG', 0, 0, width, height);
    pdf.save('document.pdf');
});
```

### **JWT Token Validation**
```python
def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
```

### **Quota Enforcement**
```python
def check_storage_quota(user_email):
    user = get_user(user_email)
    if user['video_count'] >= user['video_limit']:
        return False, "Video limit reached"
    if user['storage_used'] >= user['storage_limit'] * 0.9:
        return False, "Storage limit reached"
    return True, "Quota available"
```

---

## **IMPORTANT NOTES**

### **Token Budget**
- Amazon Q has 200,000 tokens per conversation (~150,000 words)
- This is per conversation, NOT monthly
- Resets when you start a new conversation

### **localStorage Keys (Standardized)**
- `auth_token` - JWT authentication token
- `user_data` - JSON object {email, first_name, last_name, role}
- **Old keys removed**: token, userRole, userEmail, userName

### **API Gateway Compatibility**
- HTTP API v2 uses `rawPath` instead of `path`
- Lambda must check both `rawPath` and `path` for compatibility
- Method in `requestContext.http.method` instead of `httpMethod`

### **CSS Best Practices**
- Use shared stylesheets (common-styles.css, card-styles.css, form-styles.css)
- Avoid inline styles with `!important` flags
- Fix external stylesheet conflicts at the source
- Test with production asset URLs (not just local)

### **Database Design Patterns**
- Users table uses user_id as primary key (not email)
- Always scan by email for name lookups (not get_item)
- DynamoDB Decimal objects require explicit conversion before JSON serialization
- Resources support both string and array for categories (backward compatible)

### **Best Practices Established**
- **NEVER** use `document.write()` with user-generated content
- **ALWAYS** use DOM methods (createElement, appendChild, textContent, innerHTML)
- **AVOID** string concatenation when content may contain line breaks
- Use Quill's clipboard.convert() and setContents() for loading HTML content
- Use contenteditable instead of Quill for email templates (preserves inline CSS)

---

## **WHAT I NEED HELP WITH**
[Describe your specific task here - e.g., "Add new Lambda function", "Fix bug in election map", "Create voter guide for new state", "Optimize database queries", "Deploy new feature to production", "Add new ministry tool", etc.]

---

**Copy this entire prompt into your new chat, then add your specific request at the "What I Need Help With" section!** state)
- Testimony system for answered prayers
- State-specific prayer filtering

### **Event Calendar Integration**
**Features**:
- FullCalendar.js integration
- Event CRUD operations
- CSV bulk import
- Election date sync
- Registration tracking
- State/category filtering
- ICS export

### **Email Notification System**
**Features**:
- 4 integrated notification types (comment reply, prayer update, article publication, admin alert)
- User preference management (notification-settings.html)
- Professional branded email templates
- Real-time notification count badge in navbar
- Respects user opt-in/opt-out preferences

---

## **PART 9: NEWS MANAGEMENT SYSTEM**

### **News Features**
**Files**: `news.html`, `news_api/index.py`

**Features**:
- Breaking news banners
- Scheduled publishing with auto-status logic
- State-specific election coverage
- External link support
- Topic categorization (politics, culture, religious freedom, family, pro-life)
- Horizontal scrolling UI
- Author name display (fixed from email addresses)

---

## **PART 10: RESOURCE MANAGEMENT**

### **Resource Features**
**Files**: `resources.html`, `resources_api/index.py`, `admin-resources.html`

**Features**:
- Emoji icons for 47 category keywords
- Edit functionality (complete CRUD)
- Category bulk rename
- Auto-summary with AWS Bedrock AI
- Empty category cleanup
- Multiple categories per resource (array support with backward compatibility)

---

## **PART 11: UI/UX ENHANCEMENTS**

### **Unified Navigation System**
**Files**: `navbar.html`, `navbar.js`

**Features**:
- Reusable navbar component
- Role-based access control
- Dual icon support (emoji and Font Awesome)
- Mobile responsive with hamburger menu
- Fixed positioning with proper page padding

**Pages with Unified Navbar** (10 total):
- index.html, videos.html, articles.html, news.html, resources.html
- election-map.html, profile.html, user-page.html, article.html, news-article.html

### **Horizontal Scrolling UI**
**Implementation**: Netflix-style content browsing

**Pages**:
- videos.html (300px cards, 320px scroll)
- resources.html (400px cards, 420px scroll)
- articles.html (450px cards, 470px scroll)
- news.html (400px cards, 420px scroll)

**Features**:
- Arrow navigation (desktop only, hidden on mobile)
- Touch-friendly mobile scrolling
- Category-based grouping
- Smooth scrolling with visual feedback

### **CSS Consolidation**
**Shared Stylesheets**:
- `assets/css/common-styles.css` - Navigation and dashboard styles (2.5 KiB)
- `assets/css/card-styles.css` - Card components
- `assets/css/form-styles.css` - Form elements

**Benefits**:
- 75+ duplicate CSS rules removed (23.6% reduction)
- Single source of truth
- Improved maintainability
- Better performance (cached assets)

### **Mobile Optimization**
**Responsive Breakpoints**:
- Desktop: Default styles
- Tablet (768px): Reduced font sizes and padding
- Mobile (576px): Further reduced spacing
- Android (422px): Special padding adjustments

**Features**:
- Progressive mobile breakpoints
- Touch-friendly button sizes
- Proper navigation wrapping
- Consistent user experience across devices

### **PWA (Progressive Web App)**
**Files**: `manifest.json`, `service-worker.js`, `pwa-install.js`

**Features**:
- Install as native-like app on mobile and desktop
- Offline caching and background sync
- Auto-install prompt after 30 seconds
- Push notification support (ready for future)
- 8 icon sizes (72x72 to 512x512)
- Standalone display mode

---

## **TECHNICAL STACK**

### **Frontend**
- HTML5, CSS3, JavaScript (ES6+)
- Bootstrap 5
- jQuery
- Quill.js (rich text editor)
- marked.js (markdown rendering)
- html2canvas (PDF generation)
- FullCalendar.js (event calendar)

### **Backend**
- AWS Lambda (Python 3.9-3.12)
- AWS S3 (storage)
- AWS DynamoDB (NoSQL database)
- AWS API Gateway (REST APIs)
- yt-dlp (video downloading)
- FFmpeg (video processing)
- AWS Bedrock (AI summarization)
- AWS SES (email delivery)

### **Authentication**
- JWT tokens (PyJWT library)
- localStorage (auth_token, user_data)
- Role-based access control

---

## **AWS LAMBDA FUNCTIONS (17+ Total)**

1. **auth-api** - User authentication and JWT management
2. **admin-api** - Administrative operations and user management
3. **tag-api** - Video metadata and tag management
4. **router** - Job routing and quota enforcement
5. **downloader** - Video download and processing (yt-dlp + FFmpeg)
6. **articles-api** - Blog/article management with Bible integration
7. **paypal-billing-api** - Subscription management and quota enforcement
8. **thumbnail-generator** - Generate thumbnails for uploaded videos
9. **s3-thumbnail-trigger** - S3 event trigger for thumbnail generation
10. **url-analysis-api** - URL content extraction and AI summarization
11. **news-api** - News article management with scheduled publishing
12. **resources-api** - Resource library management
13. **contributors-api** - State election coverage and contributor management
14. **email-subscription-handler** - Email subscription and tracking
15. **video-list-api** - Video listing and filtering
16. **article-analysis-api** - Article analytics and view tracking
17. **comments-api** - Comment management
18. **newsletter-api** - Newsletter system with campaigns
19. **prayer-api** - Prayer request system

---

## **DYNAMODB TABLES (15+ Total)**

1. **users** - User accounts, roles, subscription data
2. **video-metadata** - Video metadata, tags, ownership
3. **articles** - Article content, authors, categories
4. **download-jobs** - Video download job tracking
5. **comments** - User comments on articles
6. **news** - News articles with topics and states
7. **resources** - Resource library with categories (array support)
8. **contributors** - State correspondents with contact info
9. **races** - Election races (290+ across 50 states)
10. **candidates** - Candidate profiles (197+ with faith statements)
11. **state-summaries** - Comprehensive voter guides (50 states)
12. **pending-changes** - Editor approval workflow
13. **email-subscribers** - Email subscription management
14. **email-events** - Open/click tracking events
15. **templates** - Article templates
16. **prayer-requests** - Prayer request system
17. **events** - Event calendar
18. **newsletters** - Newsletter campaigns

---

## **DEPLOYMENT & SCRIPTS**

### **PowerShell Deployment Scripts**
- `deploy-all.ps1` - Deploy all Lambda functions
- `deploy-router.ps1` - Deploy router Lambda
- `deploy-election-system.ps1` - Deploy election system
- `deploy-news-api.ps1` - Deploy news API
- `deploy-articles-api.ps1` - Deploy articles API
- `deploy-resources-api.ps1` - Deploy resources API
- `s3-push.ps1` - Push static files to S3
- `aws-download.ps1` - Download files from S3

### **Monitoring Scripts**
- `live-logs.ps1` - Real-time Lambda logs
- `check-lambda-status.ps1` - Check Lambda function status
- `diagnose-stuck.ps1` - Diagnose stuck downloads
- `timeout-monitor.ps1` - Monitor Lambda timeouts

### **Utility Scripts**
- `git-commit.ps1` - Quick git commit
- `quick-commit.ps1` - Fast commit with message
- `cost-calculator.ps1` - AWS cost estimation

---

## **DOCUMENTATION**

### **Key Documentation Files** (in `docs/` folder)
- `PROGRESS.md` - Overall project progress (comprehensive history)
- `TECHNICAL_DOCUMENTATION.md` - Technical specs and architecture
- `TECHNICAL_DOCUMENTATION_v2.md` - Updated v2.0 architecture
- `SALES_FLYER_v2.md` - Updated sales materials with v2.0 features
- `README_v2.md` - Comprehensive documentation index
- `DEPLOYMENT_SUMMARY.md` - Deployment guide
- `NEWS_MANAGEMENT_SYSTEM.md` - News system docs
- `ARTICLE_ANALYTICS.md` - Analytics implementation
- `USER_UPLOAD_FIXES.md` - User upload troubleshooting
- `aws-commands-guide.md` - AWS CLI commands
- `DYNAMODB_QUERY_GUIDE.md` - DynamoDB query patterns

### **Election System Documentation**
- `Election Data and Files/ELECTION_DATA_WORKFLOW.md` - Annual election cycle workflow
- `Election Data and Files/Templates/FORMATTING_RULES.md` - Voter guide standards
- `Election Data and Files/Templates/state_summary_template.md` - Blank template
- `Election Data and Files/Templates/AI_PROMPT_TEMPLATE.md` - AI-assisted content creation

### **Email System Documentation**
- `Election Data and Files/Email and Tracking/README.md` - System overview
- `Election Data and Files/Email and Tracking/QUICK_START.md` - 30-minute setup guide
- `Election Data and Files/Email and Tracking/setup_instructions.md` - Detailed setup

### **Newsletter System Documentation**
- `docs/NEWSLETTER_ENHANCEMENTS.md` - Complete feature documentation
- `docs/NEWSLETTER_SYSTEM_GUIDE.md` - User guide
- `docs/AUTO_DIGEST_GUIDE.md` - Auto-digest system guide

---

## **CURRENT STATE**

### **Video/Content System**
- ✅ Video download and processing pipeline
- ✅ Article/news creation and management
- ✅ User authentication and authorization
- ✅ Comment system with moderation
- ✅ Tag/category system
- ✅ Thumbnail generation
- ✅ Bible verse integration (KJV, ASV, YLT)
- ✅ PayPal billing integration (LIVE PRODUCTION MODE)
- ✅ Analytics tracking
- ✅ Dual-mode content editor (WYSIWYG/Markdown)
- ✅ Video sorting (6 options)
- ✅ Bulk video editing

### **Election System**
- ✅ ALL 50 US STATES with comprehensive coverage (100% complete)
- ✅ 290+ races, 197+ candidates
- ✅ Interactive US map with clickable states (mobile-responsive)
- ✅ State summary modals with markdown rendering
- ✅ Expand modal for full-screen viewing
- ✅ Download functionality (PDF with emoji support, TXT)
- ✅ Dual-mode editor (markdown/rich text) for summaries
- ✅ Race and candidate management interface
- ✅ CSV import with auto-matching
- ✅ Comprehensive voter guides (50 states, 15,000-30,000 chars each)
- ✅ Editor role system with approval workflow
- ✅ Complete template system (950 files across 50 states)
- ✅ Party badges with color coding

### **Email & Newsletter System**
- ✅ AWS SES integration with tracking
- ✅ Open tracking (1x1 pixel)
- ✅ Click tracking (redirect URLs)
- ✅ Newsletter campaigns with 5 professional templates
- ✅ Dual editor (Visual + HTML)
- ✅ Mail merge personalization
- ✅ Auto-digest generator
- ✅ Newsletter archive
- ✅ Analytics dashboard
- ✅ 95% cheaper than Mailchimp

### **Advanced Ministry Tools**
- ✅ Prayer request system with moderation
- ✅ Event calendar integration
- ✅ Email notification system (4 types)

### **UI/UX**
- ✅ Unified navigation system (navbar.html/navbar.js)
- ✅ Horizontal scrolling UI (Netflix-style)
- ✅ CSS consolidation (23.6% reduction, 75+ rules removed)
- ✅ Mobile optimization (progressive breakpoints)
- ✅ Authentication standardization (auth_token, user_data)
- ✅ PWA implementation (install as native app)
- ✅ Domain migration (christianconservativestoday.com)

---

## **KEY TECHNICAL PATTERNS**

### **Dual-Mode Editor**
```javascript
// Separate content storage prevents data corruption
let markdownContent = '';
let htmlContent = '';

function switchToMarkdown() {
    htmlContent = quill.root.innerHTML;
    // Display markdownContent in textarea
}

function switchToRichText() {
    markdownContent = textarea.value;
    quill.root.innerHTML = marked.parse(markdownContent);
}
```

### **Content Detection**
```javascript
const content = summary.content || '';
if (content.startsWith('<')) {
    htmlContent = content;  // HTML
    markdownContent = '';
} else {
    markdownContent = content;  // Markdown
    htmlContent = '';
}
```

### **PDF Generation with Emojis**
```javascript
// Uses html2canvas (NOT jsPDF's html() method)
html2canvas(element, { scale: 2 }).then(canvas => {
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF();
    pdf.addImage(imgData, 'PNG', 0, 0, width, height);
    pdf.save('document.pdf');
});
```

### **JWT Token Validation**
```python
def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
```

### **Quota Enforcement**
```python
def check_storage_quota(user_email):
    user = get_user(user_email)
    if user['video_count'] >= user['video_limit']:
        return False, "Video limit reached"
    if user['storage_used'] >= user['storage_limit'] * 0.9:
        return False, "Storage limit reached"
    return True, "Quota available"
```

---

## **IMPORTANT NOTES**

### **Token Budget**
- Amazon Q has 200,000 tokens per conversation (~150,000 words)
- This is per conversation, NOT monthly
- Resets when you start a new conversation

### **localStorage Keys (Standardized)**
- `auth_token` - JWT authentication token
- `user_data` - JSON object {email, first_name, last_name, role}
- **Old keys removed**: token, userRole, userEmail, userName

### **API Gateway Compatibility**
- HTTP API v2 uses `rawPath` instead of `path`
- Lambda must check both `rawPath` and `path` for compatibility
- Method in `requestContext.http.method` instead of `httpMethod`

### **CSS Best Practices**
- Use shared stylesheets (common-styles.css, card-styles.css, form-styles.css)
- Avoid inline styles with `!important` flags
- Fix external stylesheet conflicts at the source
- Test with production asset URLs (not just local)

### **Database Design Patterns**
- Users table uses user_id as primary key (not email)
- Always scan by email for name lookups (not get_item)
- DynamoDB Decimal objects require explicit conversion before JSON serialization
- Resources support both string and array for categories (backward compatible)

### **Best Practices Established**
- **NEVER** use `document.write()` with user-generated content
- **ALWAYS** use DOM methods (createElement, appendChild, textContent, innerHTML)
- **AVOID** string concatenation when content may contain line breaks
- Use Quill's clipboard.convert() and setContents() for loading HTML content
- Use contenteditable instead of Quill for email templates (preserves inline CSS)

---

## **WHAT I NEED HELP WITH**
[Describe your specific task here - e.g., "Add new Lambda function", "Fix bug in election map", "Create voter guide for new state", "Optimize database queries", "Deploy new feature to production", "Add new ministry tool", etc.]

---

**Copy this entire prompt into your new chat, then add your specific request at the "What I Need Help With" section!**
