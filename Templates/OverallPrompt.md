# AWS Video Downloader & Content Management System + Election Database - Project Continuation Prompt

I'm working on a comprehensive **AWS-based video downloader, content management system, and Christian conservative election tracking platform**. Here's the complete project context:

## **Project Location**
`c:\Users\Ed\Documents\Programming\AWS\Downloader\`

---

## **PART 1: VIDEO DOWNLOADER & CONTENT MANAGEMENT SYSTEM**

### **1. Video Download System**
- **Technology**: AWS Lambda + yt-dlp + FFmpeg layers
- **Supported Platforms**: YouTube, Rumble, other video platforms
- **Process**: User submits URL → Lambda downloads → FFmpeg processes → S3 storage
- **Key Files**:
  - `router/index.py` - Main Lambda router with quota management
  - `downloader/index.py` - Video download Lambda function
  - `video-downloader.html` - Frontend interface
  - `download-status.html` - Real-time download status tracking

### **2. Content Management System**

**Admin Interfaces:**
- `admin.html` - Main admin dashboard for video/article management
- `admin-contributors.html` - Contributor management with dual-mode editor
- `admin-resources.html` - Resource management
- `admin-templates.html` - Template management

**Public Interfaces:**
- `index.html` - Homepage
- `videos.html` - Video gallery
- `articles.html` - Article listing
- `article.html` - Individual article view
- `news.html` - News section
- `resources.html` - Resources page

### **3. Article & News System**

**Features:**
- Rich text editor for article creation
- Bible verse integration (multiple translations: KJV, ASV, YLT)
- Category/tag system
- Author profiles
- Comment system
- Draft management
- Article analytics

**Key Files:**
- `create-article.html` - Article creation interface
- `edit-article.html` - Article editing
- `create-news.html` - News creation
- `article-preview.html` - Preview before publishing
- `draft-manager.html` - Manage draft articles

### **4. AWS Lambda APIs**

**Deployed Lambda Functions:**
- `admin_api/index.py` - Admin operations (CRUD for videos/articles)
- `articles_api/index.py` - Article retrieval, Bible verse lookup
- `auth_api/index.py` - JWT authentication
- `comments_api/index.py` - Comment management
- `contributors_api/index.py` - Contributor data
- `news_api/index.py` - News article operations
- `resources_api/index.py` - Resource management
- `tag_api/index.py` - Tag/category operations
- `thumbnail_generator/index.py` - Auto-generate video thumbnails
- `s3_thumbnail_trigger/index.py` - S3 trigger for thumbnail generation
- `url_analysis_api/index.py` - URL metadata extraction
- `article_analysis_api/index.py` - Article analytics
- `video_list_api/index.py` - Video listing
- `paypal_billing_api/index.py` - PayPal subscription billing

### **5. Database Structure (DynamoDB)**

**Tables:**
- `Videos` - Video metadata, URLs, thumbnails, tags
- `Articles` - Article content, authors, categories
- `News` - News articles
- `Users` - User accounts, roles, authentication
- `Comments` - User comments on articles/videos
- `Tags` - Category/tag system
- `Resources` - Downloadable resources
- `Contributors` - Contributor profiles
- `Analytics` - Article/video analytics

---

## **PART 2: ELECTION DATABASE & TRACKING SYSTEM**

### **1. Interactive Election Map**

**File**: `election-map.html`

**Features:**
- Clickable SVG US map with state-specific election data
- Modal displays state summaries with markdown rendering (marked.js)
- Expand button (🔍) opens full-screen modal for better readability
- Download dropdown: PDF and TXT formats
- Bootstrap 5, jQuery, AWS SDK integration
- Loads data from: `races.csv`, `candidates.csv`, state summaries from S3

**PDF Generation:**
- Uses html2canvas (NOT jsPDF's html() method - DOMPurify dependency issues)
- Converts HTML to high-quality image (2x scale) for emoji rendering
- Embeds image in PDF with proper sizing

### **2. Admin Interface for Election Data**

**File**: `admin-contributors.html`

**Features:**
- **Dual-mode editor** for state summaries:
  - **Markdown mode (📝)**: Textarea for markdown editing
  - **Rich Text mode (🎨)**: Quill.js WYSIWYG editor
  - **Separate storage**: `markdownContent` and `htmlContent` variables
  - **Mode switching preserves both formats** without data loss
  - **Content detection**: Checks if content starts with '<' to identify HTML vs markdown

**Mode Switching Logic:**
```javascript
// Separate content storage
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

**Race Management:**
- Add/edit/delete races
- Fields: state, office, election_date, race_type, description

**Candidate Management:**
- Add/edit/delete candidates
- Fields: name, state, office, party, bio, website, faith_statement, positions, endorsements

**CSV Import:**
- Auto-matches candidates to races using state + office exact match
- Bulk upload capability

**Summaries List Display:**
- Renders markdown to HTML, strips tags
- Shows first 200 chars of clean text instead of raw markdown syntax

### **3. CSV Data Format**

**races.csv:**
```
state,office,election_date,race_type,description
```

**candidates.csv:**
```
name,state,office,party,bio,website,faith_statement,positions,endorsements
```

### **4. Voter Guides**

**Location**: `Voter Guides_Summaries/` folder

**Completed Guides:**
- `virginia_summary_guide.md` - 2025 state races (Governor: Winsome Earle-Sears, 140 legislature seats) + 2026 federal races (Senate: Tim Kaine, 11 House seats)
- `new_jersey_summary_guide.md` - 2025 state races (Governor: Jack Ciattarelli, 120 legislature seats) + 2026 federal races (Senate: Menendez seat, 12 House seats)
- `hawaii_summary_guide.md` - Template guide
- `california_summary_guide.md` - Template guide

**Voter Guide Structure:**
- 20-30 page markdown guides
- Political landscape analysis
- Priority races for Christian conservatives
- Detailed candidate profiles
- Key issues breakdown
- Church mobilization strategies
- Prayer points
- Critical dates and deadlines

**Guide Format:**
```markdown
# State 2025 Elections - Complete Christian Conservative Guide

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

### **5. Election Data Scripts**

**Python Scripts:**
- `scan_election_data.py` - Scan DynamoDB for election data
- `get_hawaii_races.py` - Retrieve Hawaii race data
- `upload_hawaii_candidates.py` - Upload Hawaii candidates to DynamoDB
- `upload_virginia_candidates.py` - Upload Virginia candidates to DynamoDB

**CSV Files:**
- `hawaii_races_2025-2026.csv`
- `hawaii_candidates_2025-2026.csv`
- `virginia_candidates_2025.csv`
- `sample_races_2024.csv`
- `sample_candidates_2024.csv`

---

## **KEY TECHNICAL IMPLEMENTATIONS**

### **Dual-Mode Content Editor**
- Prevents data corruption during mode switching
- Markdown stays as markdown, HTML stays as HTML
- Content detection on load determines which mode to display
- Used in both contributor management and election summaries

### **Bible Verse Integration**
- Multiple translations: KJV, ASV, YLT
- API endpoint: `articles_api/index.py`
- Automatic verse lookup and formatting
- Used in article creation/editing

### **Thumbnail Generation**
- Automatic thumbnail generation from videos
- S3 trigger: `s3_thumbnail_trigger/index.py`
- Generator: `thumbnail_generator/index.py`
- Manual scripts: `generate_thumbnails.py`, `fix_thumbnail.py`

### **Authentication System**
- JWT-based authentication
- User roles: admin, contributor, user
- Protected admin routes
- PayPal subscription integration

### **Video Processing Pipeline**
1. User submits video URL
2. Router Lambda validates and queues
3. Downloader Lambda uses yt-dlp to download
4. FFmpeg processes video (compression, format conversion)
5. Upload to S3
6. Trigger thumbnail generation
7. Update DynamoDB with metadata

---

## **DEPLOYMENT & SCRIPTS**

**PowerShell Deployment Scripts:**
- `deploy-all.ps1` - Deploy all Lambda functions
- `deploy-router.ps1` - Deploy router Lambda
- `deploy-election-system.ps1` - Deploy election system
- `s3-push.ps1` - Push static files to S3
- `aws-download.ps1` - Download files from S3

**Monitoring Scripts:**
- `live-logs.ps1` - Real-time Lambda logs
- `check-lambda-status.ps1` - Check Lambda function status
- `diagnose-stuck.ps1` - Diagnose stuck downloads
- `timeout-monitor.ps1` - Monitor Lambda timeouts

**Utility Scripts:**
- `git-commit.ps1` - Quick git commit
- `quick-commit.ps1` - Fast commit with message
- `cost-calculator.ps1` - AWS cost estimation
- `cost-comparison.ps1` - Compare AWS service costs

---

## **TECHNICAL STACK**

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Bootstrap 5
- jQuery
- Quill.js (rich text editor)
- marked.js (markdown rendering)
- html2canvas (PDF generation)

**Backend:**
- AWS Lambda (Python 3.11)
- AWS S3 (video/image/file storage)
- AWS DynamoDB (database)
- AWS API Gateway (REST APIs)
- yt-dlp (video downloading)
- FFmpeg (video processing)

**Authentication:**
- JWT tokens (PyJWT library)
- AWS Cognito (optional)
- PayPal OAuth (billing)

**External APIs:**
- Bible API (verse lookup)
- PayPal API (subscriptions)
- URL metadata extraction

---

## **DOCUMENTATION**

Key documentation files in `docs/` folder:
- `PROGRESS.md` - Overall project progress
- `TECHNICAL_DOCUMENTATION.md` - Technical specs
- `DEPLOYMENT_SUMMARY.md` - Deployment guide
- `DEPLOYMENT_ELECTION_SYSTEM.md` - Election system deployment
- `NEWS_MANAGEMENT_SYSTEM.md` - News system docs
- `ARTICLE_ANALYTICS.md` - Analytics implementation
- `USER_UPLOAD_FIXES.md` - User upload troubleshooting
- `aws-commands-guide.md` - AWS CLI commands
- `DYNAMODB_QUERY_GUIDE.md` - DynamoDB query patterns

---

## **CURRENT STATE**

**Video/Content System:**
- ✅ Video download and processing pipeline
- ✅ Article/news creation and management
- ✅ User authentication and authorization
- ✅ Comment system
- ✅ Tag/category system
- ✅ Thumbnail generation
- ✅ Bible verse integration
- ✅ PayPal billing integration
- ✅ Analytics tracking

**Election System:**
- ✅ Interactive US election map with clickable states
- ✅ State summary modals with markdown rendering
- ✅ Expand modal for full-screen viewing
- ✅ Download functionality (PDF with emoji support, TXT)
- ✅ Dual-mode editor (markdown/rich text) for summaries
- ✅ Race and candidate management interface
- ✅ CSV import with auto-matching
- ✅ Comprehensive voter guides (Virginia, New Jersey, Hawaii, California)
- ✅ DynamoDB integration for election data storage

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

### **Election Data Creation**
- Use comprehensive voter guides as templates
- Include political landscape, priority races, candidate profiles
- Focus on Christian conservative perspective
- Cover state races (2025) and federal races (2026)
- 20-30 pages per state guide

### **Dual-Mode Editor Best Practices**
- Always save current mode content before switching
- Use content detection (starts with '<') to identify format
- Keep markdownContent and htmlContent separate
- Never mix or overwrite the two formats

---

## **WHAT I NEED HELP WITH**
[Describe your specific task here - e.g., "Create voter guide for Nebraska", "Add new feature to election map", "Fix bug in dual-mode editor", "Optimize Lambda function", "Add new state to election database", "Deploy new Lambda API", etc.]

---

**Copy this entire prompt into your new chat, then add your specific request at the "What I Need Help With" section!**
