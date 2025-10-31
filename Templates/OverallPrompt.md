# Christian Conservatives Today - Complete Project Continuation Prompt

I'm working on **Christian Conservatives Today**, a comprehensive AWS-based serverless platform combining video hosting, article publishing, nationwide election tracking, and email marketing for Christian conservative ministry and civic engagement.

## **Project Location**
`c:\Users\Ed\Documents\Programming\AWS\Downloader\`

---

## **PLATFORM OVERVIEW**

### **Mission & Purpose**
A dedicated platform for the 5-fold ministry (apostles, prophets, evangelists, pastors, teachers), Christian believers, and conservative voices to:
- Share sermons, teachings, and biblical messages
- Publish articles with integrated Bible verse lookup
- Track elections across all 50 US states with Christian conservative perspective
- Engage communities through comments, social sharing, and email campaigns
- Provide voter guides and candidate profiles for informed Christian voting

### **Platform URL**
https://christianconservativestoday.com

### **Key Statistics**
- **Architecture**: 100% Serverless (AWS Lambda, S3, DynamoDB, CloudFront)
- **Lambda Functions**: 15+ microservices
- **Database Tables**: 15+ DynamoDB tables
- **Election Coverage**: ALL 50 US STATES (290+ races, 197+ candidates)
- **User Roles**: 4-tier system (Super User > Admin > Editor > User)
- **Email System**: AWS SES with open/click tracking

---

## **PART 1: VIDEO MANAGEMENT SYSTEM**

### **Video Download & Processing**
**Supported Platforms**: YouTube, Rumble, Facebook
**Processing Engine**: yt-dlp + FFmpeg layers
**Smart Routing**: Lambda (< 15 min) or Fargate (> 15 min)

**Key Files**:
- `router/index.py` - Main Lambda router with quota management
- `downloader/index.py` - Video download Lambda (yt-dlp + FFmpeg)
- `thumbnail_generator/index.py` - Auto-generate 3 thumbnails
- `s3_thumbnail_trigger/index.py` - S3 event trigger
- `video-downloader.html` - Frontend interface
- `download-status.html` - Real-time status tracking

**Features**:
- Automatic thumbnail generation (10%, 50%, 90% of duration)
- Quota enforcement (storage and video count limits)
- External video embedding (YouTube, Rumble, Facebook)
- Platform auto-detection
- S3 presigned URLs for direct uploads
- CloudFront CDN delivery

### **Video Display & Management**
**Key Files**:
- `videos.html` - Video gallery with horizontal scrolling UI
- `admin.html` - Admin dashboard for video management
- `user-page.html` - User-specific video pages
- `embed.html` - Video embedding page

**Features**:
- Netflix-style horizontal scrolling
- Category filtering (sermons, politics, teaching)
- Public/private visibility controls
- Video ownership tracking
- Share functionality with copy-to-clipboard
- Pagination (24 videos per page)

---

## **PART 2: ARTICLE & BLOG SYSTEM**

### **Rich Text Editor**
**Editor**: Quill.js with custom toolbar
**Bible Integration**: Multiple translations (KJV, ASV, YLT)
**Markdown Support**: Dual-mode editing (WYSIWYG ↔ Markdown)

**Key Files**:
- `create-article.html` - Article creation with Bible lookup
- `edit-article.html` - Article editing interface
- `articles.html` - Article listing with search
- `article.html` - Individual article view
- `articles_api/index.py` - Backend API with Bible integration

**Article Templates**:
1. **Sermon Template**: Scripture → Prayer → Main Points → Application
2. **Political Commentary**: Biblical Foundation → Current Issue → Response
3. **Service Notes**: Date, Speaker, Key Points, Application
4. **Bible Study**: Observation → Interpretation → Application → Prayer

**Features**:
- Bible verse search and insertion (KJV, ASV, YLT)
- Scripture reference extraction
- Reading time calculation (200 words/min)
- View tracking and analytics
- Featured images with Open Graph integration
- Social sharing (Facebook, Twitter, LinkedIn)
- Public article access (no auth required for public articles)
- Full-text search with relevance scoring
- Related articles suggestions
- Comment system with moderation

**Categories**: Sermons, Politics, Devotionals, Apologetics, Ministry, Bible Study, General

---

## **PART 3: AUTHENTICATION & USER MANAGEMENT**

### **Four-Tier Role System**
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

Editor (Content Contributor)
├── Create/edit content for assigned states
├── Submissions require approval (unless bypass enabled)
├── State-specific permissions
└── Cannot access admin functions

User (Standard Access)
├── Upload videos (quota-limited)
├── Create articles
├── Manage own content
└── Subject to subscription limits
```

### **JWT Authentication**
**Algorithm**: HS256 (HMAC with SHA-256)
**Expiration**: 24 hours
**Storage**: localStorage (auth_token, user_data)

**Key Files**:
- `auth_api/index.py` - JWT generation and validation
- `login.html` - Login interface
- `profile.html` - User profile with subscription management

**localStorage Keys**:
- `auth_token` - JWT token
- `user_data` - JSON object {email, first_name, last_name, role}

---

## **PART 4: SUBSCRIPTION & BILLING SYSTEM**

### **Subscription Tiers**
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

### **PayPal Integration**
**Payment Processor**: PayPal Subscriptions API
**Key Files**:
- `paypal_billing_api/index.py` - Subscription management
- `profile.html` - Subscription dashboard

**Features**:
- Subscription creation and cancellation
- Webhook event handling
- Quota enforcement (pre-upload checks)
- Automatic downgrades (CloudWatch Events)
- Grace period (benefits retained until billing period ends)

**Webhook Events**:
- BILLING.SUBSCRIPTION.CREATED
- BILLING.SUBSCRIPTION.ACTIVATED
- BILLING.SUBSCRIPTION.CANCELLED
- BILLING.SUBSCRIPTION.EXPIRED

---

## **PART 5: ELECTION TRACKING SYSTEM - ALL 50 STATES COMPLETE ✅**

### **Interactive Election Map**
**File**: `election-map.html`

**Features**:
- Clickable SVG US map with state-specific data
- Modal displays state summaries with markdown rendering
- Expand button (🔍) for full-screen viewing
- Download dropdown: PDF (html2canvas) and TXT formats
- Bootstrap 5, jQuery, AWS SDK integration
- Mobile-responsive design

### **Admin Interface for Election Data**
**File**: `admin-contributors.html`

**Features**:
- **Dual-mode editor** for state summaries:
  - Markdown mode (📝): Textarea for markdown editing
  - Rich Text mode (🎨): Quill.js WYSIWYG editor
  - Separate storage: `markdownContent` and `htmlContent` variables
  - Mode switching preserves both formats without data loss
  - Content detection: Checks if content starts with '<' to identify HTML vs markdown

**Race Management**:
- Add/edit/delete races
- Fields: state, office, election_date, race_type, description
- CSV bulk import with auto-matching

**Candidate Management**:
- Add/edit/delete candidates
- Fields: name, state, office, party, bio, website, faith_statement, positions, endorsements
- Party badges with color coding (R-red, D-blue, third parties-gray)
- Auto-matching to races by state + office

**Contributor Management**:
- State correspondents with verification badges
- Contact info: first_name, last_name, phone_number
- Bio and email display
- Role-based access control

**Editor Role System**:
- Approval workflow for editor submissions
- Bypass approval toggle for trusted editors
- Pending changes queue with admin review
- Auto-role assignment when contributor created

### **Voter Guides**
**Location**: `Voter Guides_Summaries/` folder

**Completed Guides** (ALL 50 STATES):
- Comprehensive 15,000-30,000 character guides per state
- 2025 state races + 2026 federal races
- Christian conservative perspective
- Political landscape analysis
- Priority races and candidate profiles
- Key issues breakdown
- Church mobilization strategies
- Prayer points with scripture verses

**Guide Format**:
```markdown
# State 2025-2026 Elections - Complete Christian Conservative Guide

## 📊 Database Summary
## 🔴 STATE POLITICAL LANDSCAPE
## 🔴 TOP PRIORITY RACES FOR CHRISTIAN CONSERVATIVES
## 🏛️ STATE LEGISLATURE
## 💡 CHRISTIAN CONSERVATIVE VOTER STRATEGY
## 🎯 KEY ISSUES FOR CHRISTIAN CONSERVATIVES
## 📅 CRITICAL DATES
## 🙏 PRAYER POINTS
## 📞 GET INVOLVED
```

### **CSV Data Format**
**races.csv**:
```
state,office,election_date,race_type,description
```

**candidates.csv**:
```
name,state,office,party,bio,website,faith_statement,positions,endorsements
```

### **Election Data Scripts**
**Python Scripts**:
- `scan_election_data.py` - Scan DynamoDB for election data
- `upload_[state]_data.py` - State-specific upload scripts
- `update_candidate.py` - Update existing candidate fields
- `validate_election_data.py` - Data quality checker

**Coverage Statistics**:
- **States**: 50/50 (100% complete)
- **Races**: 290+ across all states
- **Candidates**: 197+ with comprehensive profiles
- **Voter Guides**: 50 comprehensive guides (12,000-30,000 chars each)

---

## **PART 6: EMAIL SUBSCRIPTION & TRACKING SYSTEM**

### **AWS SES Integration**
**Email**: contact@christianconservativestoday.com
**Lambda Function**: email-subscription-handler (Python 3.12)

**Features**:
- Email subscription form on election-map.html
- Welcome email with tracking
- Open tracking (1x1 pixel)
- Click tracking (redirect URLs)
- Newsletter campaigns
- Analytics dashboard

**Database Tables**:
- `email-subscribers` - Subscriber management
- `email-events` - Open/click tracking

**Cost Efficiency**: 95% cheaper than Mailchimp ($1 per 10,000 emails)

**Key Files**:
- `Election Data and Files/Email and Tracking/lambda_function.py`
- `Election Data and Files/Email and Tracking/analytics_queries.py`
- `Election Data and Files/Email and Tracking/send_newsletter.py`

---

## **PART 7: NEWS MANAGEMENT SYSTEM**

### **News Features**
**File**: `news.html`, `news_api/index.py`

**Features**:
- Breaking news banners
- Scheduled publishing with auto-status logic
- State-specific election coverage
- External link support
- Topic categorization (politics, culture, religious freedom, family, pro-life)
- Horizontal scrolling UI

**Key Files**:
- `create-news.html` - News creation interface
- `edit-news.html` - News editing
- `news-article.html` - Individual news article view

---

## **PART 8: RESOURCE MANAGEMENT SYSTEM**

### **Resource Features**
**File**: `resources.html`, `resources_api/index.py`

**Features**:
- Emoji icons for 47 category keywords
- Edit functionality (complete CRUD)
- Category bulk rename
- Auto-summary with AWS Bedrock AI
- Empty category cleanup
- Multiple categories per resource

**Key Files**:
- `admin-resources.html` - Admin resource management

---

## **PART 9: COMMENT SYSTEM**

### **Comment Features**
**Database Table**: `comments`

**Features**:
- User comments on articles
- Moderation tools (approve/reject/delete)
- Nested replies (parent_comment_id)
- Bulk actions for admins
- Status tracking (approved, pending, rejected)

---

## **PART 10: UI/UX ENHANCEMENTS**

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
- Arrow navigation (desktop only)
- Touch-friendly mobile scrolling
- Category-based grouping
- Smooth scrolling with visual feedback

### **CSS Consolidation**
**Shared Stylesheets**:
- `assets/css/common-styles.css` - Navigation and dashboard styles
- `assets/css/card-styles.css` - Card components
- `assets/css/form-styles.css` - Form elements

**Benefits**:
- 75+ duplicate CSS rules removed (23.6% reduction)
- Single source of truth for shared styles
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

---

## **TECHNICAL STACK**

### **Frontend**
- HTML5, CSS3, JavaScript (ES6+)
- Bootstrap 5
- jQuery
- Quill.js (rich text editor)
- marked.js (markdown rendering)
- html2canvas (PDF generation)

### **Backend**
- AWS Lambda (Python 3.9-3.12)
- AWS S3 (video/image/file storage)
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

### **External APIs**
- Bible API (verse lookup)
- PayPal API (subscriptions)
- URL metadata extraction

---

## **AWS LAMBDA FUNCTIONS (15+ Total)**

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

---

## **DYNAMODB TABLES (15+ Total)**

1. **users** - User accounts, roles, subscription data
2. **video-metadata** - Video metadata, tags, ownership
3. **articles** - Article content, authors, categories
4. **download-jobs** - Video download job tracking
5. **comments** - User comments on articles
6. **news** - News articles with topics and states
7. **resources** - Resource library with categories
8. **contributors** - State correspondents with contact info
9. **races** - Election races (290+ across 50 states)
10. **candidates** - Candidate profiles (197+ with faith statements)
11. **state-summaries** - Comprehensive voter guides (50 states)
12. **pending-changes** - Editor approval workflow
13. **email-subscribers** - Email subscription management
14. **email-events** - Open/click tracking events
15. **templates** - Article templates

---

## **DEPLOYMENT & SCRIPTS**

### **PowerShell Deployment Scripts**
- `deploy-all.ps1` - Deploy all Lambda functions
- `deploy-router.ps1` - Deploy router Lambda
- `deploy-election-system.ps1` - Deploy election system
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
- ✅ PayPal billing integration
- ✅ Analytics tracking
- ✅ Dual-mode content editor (WYSIWYG/Markdown)

### **Election System**
- ✅ ALL 50 US STATES with comprehensive coverage
- ✅ 290+ races, 197+ candidates
- ✅ Interactive US map with clickable states
- ✅ State summary modals with markdown rendering
- ✅ Expand modal for full-screen viewing
- ✅ Download functionality (PDF with emoji support, TXT)
- ✅ Dual-mode editor (markdown/rich text) for summaries
- ✅ Race and candidate management interface
- ✅ CSV import with auto-matching
- ✅ Comprehensive voter guides (50 states, 15,000-30,000 chars each)
- ✅ Editor role system with approval workflow
- ✅ DynamoDB integration for election data storage

### **Email System**
- ✅ AWS SES integration with tracking
- ✅ Open tracking (1x1 pixel)
- ✅ Click tracking (redirect URLs)
- ✅ Newsletter campaigns
- ✅ Analytics dashboard
- ✅ 95% cheaper than Mailchimp

### **UI/UX**
- ✅ Unified navigation system (navbar.html/navbar.js)
- ✅ Horizontal scrolling UI (Netflix-style)
- ✅ CSS consolidation (23.6% reduction)
- ✅ Mobile optimization (progressive breakpoints)
- ✅ Authentication standardization (auth_token, user_data)

---

## **KEY TECHNICAL PATTERNS**

### **Dual-Mode Editor Implementation**
```javascript
// Separate content storage prevents data corruption
let markdownContent = '';
let htmlContent = '';

// Switch to Markdown: Save HTML, show markdown textarea
function switchToMarkdown() {
    htmlContent = quill.root.innerHTML;
    // Display markdownContent in textarea
}

// Switch to Rich Text: Save markdown, render to HTML in Quill
function switchToRichText() {
    markdownContent = textarea.value;
    quill.root.innerHTML = marked.parse(markdownContent);
}
```

### **Content Detection on Load**
```javascript
const content = summary.content || '';
if (content.startsWith('<')) {
    htmlContent = content;  // HTML content
    markdownContent = '';
} else {
    markdownContent = content;  // Markdown content
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
- Includes all messages, responses, and file contents

### **File Context**
- When you mention files using `@filename`, the content is automatically included
- No need to ask Q to read files you've already mentioned with @
- Use `@workspace` to include relevant project files automatically

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

### **Election Data Creation**
- Use comprehensive voter guides as templates
- Include political landscape, priority races, candidate profiles
- Focus on Christian conservative perspective
- Cover state races (2025) and federal races (2026)
- 15,000-30,000 characters per state guide

---

## **WHAT I NEED HELP WITH**
[Describe your specific task here - e.g., "Add new Lambda function", "Fix bug in election map", "Create voter guide for new state", "Optimize database queries", "Deploy new feature to production", etc.]

---

**Copy this entire prompt into your new chat, then add your specific request at the "What I Need Help With" section!**
