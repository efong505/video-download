# API Gateway Consolidation & CI/CD Implementation

## Executive Summary

**Current State**: 25 active API Gateways (22 REST + 3 HTTP), manual PowerShell deployments

**Target State**: 1 unified REST API with custom domain `api.christianconservativestoday.com`, automated GitHub Actions CI/CD

**Benefits**:
- ⏱️ **Time savings**: 4-6 hours/week in management and deployment
- 🚀 **Automated deployments**: Git push → automatic deployment
- 🔒 **Centralized security**: Single auth layer, unified CORS
- 📊 **Better monitoring**: Consolidated CloudWatch metrics
- 🎯 **Professional URLs**: Custom domain vs random AWS URLs

**Timeline**: 2 weeks (16 hours)
**Risk**: Low (phased migration, zero downtime)

**Status**: ✅ 3 unused APIs deleted (ulcbf9glui, ts4xz3fs70, 97gtxp82b2)

---

## Current Architecture Problems

### Problem 1: 25 Separate APIs
```
admin-api:        https://k2avuckm38.execute-api.us-east-1.amazonaws.com
auth-api:         https://r6l0z3605f.execute-api.us-east-1.amazonaws.com
articles-api:     https://fr3hh94h4a.execute-api.us-east-1.amazonaws.com
comments-api:     https://l10alau5g3.execute-api.us-east-1.amazonaws.com
contributors-api: https://hzursivfuk.execute-api.us-east-1.amazonaws.com
news-api:         https://xr1xcc83bj.execute-api.us-east-1.amazonaws.com
resources-api:    https://ckbtfz4vbl.execute-api.us-east-1.amazonaws.com
video-api:        https://wfeds5lejb.execute-api.us-east-1.amazonaws.com
... and 17 more
```

**Issues**:
- Hard to remember URLs
- CORS configuration on 25 APIs
- 25 separate CloudWatch log groups
- No unified rate limiting
- Difficult to manage API keys

### Problem 2: Manual Deployments
```powershell
.\deploy-admin-api.ps1
.\deploy-auth-api.ps1
.\deploy-articles-api.ps1
.\deploy-news-api.ps1
... 18+ scripts
```

**Issues**:
- Human error prone
- No deployment history
- No rollback capability
- No testing before production
- Time consuming (5-10 min per deployment)

### Problem 3: No Custom Domain
**Current**: `https://fr3hh94h4a.execute-api.us-east-1.amazonaws.com/prod/articles`
**Desired**: `https://api.christianconservativestoday.com/articles`

---

## Target Architecture

### Unified API Structure
```
api.christianconservativestoday.com/
├── /admin/*              → admin_api Lambda
├── /auth/*               → auth_api Lambda
├── /articles/*           → articles_api Lambda
├── /videos/*             → video_api Lambda
├── /news/*               → news_api Lambda
├── /resources/*          → resources_api Lambda
├── /contributors/*       → contributors_api Lambda
├── /comments/*           → comments_api Lambda
├── /tags/*               → tag_api Lambda
├── /prayer/*             → prayer_api Lambda
├── /events/*             → events_api Lambda
├── /email/*              → email_subscription_api Lambda
├── /ministry/*           → ministry_tools_api Lambda
├── /notifications/*      → notifications_api Lambda
├── /url-analysis/*       → url_analysis_api Lambda
├── /paypal/*             → paypal_billing_api Lambda
└── /download/*           → downloader Lambda
```

### GitHub Actions CI/CD Pipeline
```
Git Push → GitHub Actions → Run Tests → Deploy to AWS → Verify → Notify
```

---

## Value Analysis

### API Gateway Pricing (Corrected)
```
You ONLY pay for API requests, NOT for API existence:
- REST APIs: $3.50 per million requests
- HTTP APIs: $1.00 per million requests
- Unused APIs with 0 traffic = $0 cost
- Free Tier: First 1 million requests/month FREE
```

### Real Value
```
Cost optimization: Minimal ($5-10/month from better caching)
Time savings: 4-6 hours/week (PRIMARY VALUE)
Operational: Cleaner architecture, easier management
Professional: Custom domain, better credibility
```

---

## Implementation Plan

### Week 1: API Gateway Consolidation (8 hours)

#### Day 1-2: Create Unified API (4 hours)
- [ ] Create new REST API: `unified-api`
- [ ] Configure custom domain: `api.christianconservativestoday.com`
- [ ] Set up ACM certificate
- [ ] Configure Route 53 DNS

#### Day 3-4: Migrate Routes (4 hours)
- [ ] Create base paths for all 19 services
- [ ] Configure Lambda integrations
- [ ] Set up CORS (unified config)
- [ ] Test each endpoint

### Week 2: GitHub Actions CI/CD (8 hours)

#### Day 1-2: GitHub Setup (3 hours)
- [ ] Create GitHub repository (if not exists)
- [ ] Configure AWS credentials as secrets
- [ ] Create `.github/workflows/` structure
- [ ] Set up branch protection rules

#### Day 3-4: CI/CD Workflows (5 hours)
- [ ] Create deployment workflows (19 services)
- [ ] Add automated testing
- [ ] Configure deployment notifications
- [ ] Test full pipeline

---

## Migration Strategy (Zero Downtime)

### Phase 1: Parallel Deployment
1. Create new unified API alongside existing APIs
2. Deploy all Lambda functions to new API
3. Test thoroughly with new URLs
4. Keep old APIs running

### Phase 2: DNS Cutover
1. Update frontend to use new API domain
2. Monitor traffic on both old and new APIs
3. Verify all endpoints working
4. Keep old APIs as backup (1 week)

### Phase 3: Cleanup
1. Redirect old API URLs to new API (301)
2. Monitor for 1 week
3. Delete old APIs
4. Celebrate cost savings 🎉

---

## Files in This Folder

- `README.md` - This file (overview)
- `IMPLEMENTATION_GUIDE.md` - Step-by-step instructions
- `API_MAPPING.md` - Current → New URL mappings
- `GITHUB_ACTIONS_SETUP.md` - CI/CD configuration guide
- `.github/workflows/` - GitHub Actions workflow files
- `scripts/` - Migration and deployment scripts

---

**Ready to proceed?** Start with `IMPLEMENTATION_GUIDE.md` for detailed step-by-step instructions.
