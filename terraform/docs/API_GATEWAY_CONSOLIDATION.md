# API Gateway Consolidation Plan

## Current State
- **25 API Gateways** (22 REST + 3 HTTP)
- **12 APIs** for Christian Conservative Platform
- **Duplicate APIs**: 3x contributors-api, 2x video-downloader-api
- **Cost**: $0/month (no traffic), but messy architecture

## Target State
- **1 Unified REST API**: `ministry-platform-api`
- **14 Lambda integrations** with proper routing
- **Clean architecture**: /v1/{resource} pattern
- **CORS enabled**: All endpoints support cross-origin requests

## Unified API Structure

```
ministry-platform-api
├── /v1/auth              → auth-api Lambda
├── /v1/admin             → admin-api Lambda
├── /v1/articles          → articles-api Lambda
├── /v1/news              → news-api Lambda
├── /v1/comments          → comments-api Lambda
├── /v1/contributors      → contributors-api Lambda
├── /v1/resources         → resources-api Lambda
├── /v1/videos            → video-list-api Lambda
├── /v1/tags              → video-tag-api Lambda
├── /v1/download          → video-download-router Lambda
├── /v1/paypal            → paypal-billing-api Lambda
├── /v1/analyze           → url-analysis-api Lambda
├── /v1/prayer            → prayer_api Lambda
└── /v1/notifications     → notifications_api Lambda
```

## Terraform Modules Created

### 1. API Gateway Module (`modules/api-gateway/`)
Creates the base REST API with:
- Regional endpoint
- Deployment and stage
- CORS gateway responses
- Outputs: api_id, root_resource_id, invoke_url

### 2. API Gateway Lambda Integration Module (`modules/api-gateway-lambda-integration/`)
Creates Lambda integration with:
- Resource and method
- Lambda proxy integration
- Lambda invoke permissions
- CORS OPTIONS method (automatic)
- Outputs: resource_id, resource_path

## Implementation Steps

### Phase 1: Create Unified API (Session 1 - Today)
✅ Analyzed existing APIs
✅ Designed unified structure
✅ Created Terraform modules
⏳ Add unified API to main.tf
⏳ Deploy with 2-3 endpoints for testing

### Phase 2: Migrate All Endpoints (Session 2)
- Add all 14 Lambda integrations
- Test each endpoint
- Verify CORS works
- Document new API URLs

### Phase 3: Update Frontend & Cleanup (Session 3)
- Update frontend to use new API URLs
- Test end-to-end
- Delete old 12 API Gateways
- Celebrate clean architecture!

## Benefits

### Operational
- **Single API to manage**: Easier monitoring, logging, security
- **No duplicates**: Clear which API is "production"
- **Versioned endpoints**: /v1/ prefix allows future v2 without breaking changes
- **Consistent CORS**: All endpoints have same CORS config

### Learning
- **API Gateway patterns**: Resource, method, integration
- **Lambda permissions**: How API Gateway invokes Lambda
- **Terraform modules**: Reusable infrastructure components
- **AWS best practices**: Unified API architecture

### Resume Value
- "Consolidated 12 API Gateways into unified REST API"
- "Designed and implemented API Gateway Terraform modules"
- "Reduced API Gateway complexity by 92%"

## Next Session Preview

We'll add the unified API to your main.tf and deploy it with 2-3 endpoints to verify everything works. Then you'll see your first unified API in action!
