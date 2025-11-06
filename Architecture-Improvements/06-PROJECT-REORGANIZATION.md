# Project Reorganization & Management Strategy

## Current State Analysis

Your project has grown significantly and shows signs of **technical debt accumulation**:

### 🚨 Critical Issues Identified

1. **Root Directory Pollution** (200+ files in root)
2. **Duplicate/Backup Files** (50+ .backup, .zip files)
3. **Mixed Concerns** (Lambda code, HTML, scripts, docs all mixed)
4. **No Clear Module Boundaries**
5. **Inconsistent Naming** (snake_case, kebab-case, camelCase mixed)
6. **Large Lambda Functions** (router, admin_api growing too large)

---

## Recommended Project Structure

```
AWS/Downloader/
│
├── src/                          # All source code
│   ├── frontend/                 # Frontend files
│   │   ├── public/              # Static assets
│   │   │   ├── index.html
│   │   │   ├── videos.html
│   │   │   ├── articles.html
│   │   │   ├── news.html
│   │   │   ├── election-map.html
│   │   │   └── ...
│   │   ├── admin/               # Admin pages
│   │   │   ├── admin.html
│   │   │   ├── admin-contributors.html
│   │   │   ├── admin-newsletters.html
│   │   │   └── ...
│   │   ├── components/          # Reusable components
│   │   │   ├── navbar.html
│   │   │   └── navbar.js
│   │   ├── assets/              # CSS, JS, images
│   │   │   ├── css/
│   │   │   │   ├── common-styles.css
│   │   │   │   ├── card-styles.css
│   │   │   │   └── form-styles.css
│   │   │   ├── js/
│   │   │   │   ├── common-utils.js
│   │   │   │   └── token-validator.js
│   │   │   └── images/
│   │   │       ├── logos/
│   │   │       ├── icons/
│   │   │       └── plans/
│   │   └── pwa/                 # PWA files
│   │       ├── manifest.json
│   │       ├── service-worker.js
│   │       └── pwa-install.js
│   │
│   ├── backend/                 # Lambda functions
│   │   ├── shared/              # Shared modules
│   │   │   ├── auth/
│   │   │   │   ├── jwt_validator.py
│   │   │   │   └── permissions.py
│   │   │   ├── database/
│   │   │   │   ├── dynamodb_client.py
│   │   │   │   └── queries.py
│   │   │   ├── cache/
│   │   │   │   └── redis_client.py
│   │   │   ├── utils/
│   │   │   │   ├── response_builder.py
│   │   │   │   ├── validators.py
│   │   │   │   └── error_handler.py
│   │   │   └── models/
│   │   │       ├── user.py
│   │   │       ├── article.py
│   │   │       └── video.py
│   │   │
│   │   ├── api/                 # API Lambda functions
│   │   │   ├── auth/
│   │   │   │   ├── handler.py
│   │   │   │   └── requirements.txt
│   │   │   ├── articles/
│   │   │   │   ├── handler.py
│   │   │   │   ├── bible_integration.py
│   │   │   │   └── requirements.txt
│   │   │   ├── videos/
│   │   │   │   ├── handler.py
│   │   │   │   └── requirements.txt
│   │   │   ├── news/
│   │   │   │   ├── handler.py
│   │   │   │   └── requirements.txt
│   │   │   ├── election/
│   │   │   │   ├── handler.py
│   │   │   │   └── requirements.txt
│   │   │   ├── admin/
│   │   │   │   ├── handler.py
│   │   │   │   └── requirements.txt
│   │   │   └── ...
│   │   │
│   │   ├── workers/             # Background workers
│   │   │   ├── video_processor/
│   │   │   │   ├── handler.py
│   │   │   │   └── requirements.txt
│   │   │   ├── thumbnail_generator/
│   │   │   │   ├── handler.py
│   │   │   │   └── requirements.txt
│   │   │   ├── email_sender/
│   │   │   │   ├── handler.py
│   │   │   │   └── requirements.txt
│   │   │   └── analytics_processor/
│   │   │       ├── handler.py
│   │   │       └── requirements.txt
│   │   │
│   │   └── layers/              # Lambda layers
│   │       ├── yt-dlp/
│   │       ├── ffmpeg/
│   │       ├── redis/
│   │       └── shared-utils/
│   │
│   └── infrastructure/          # IaC (future)
│       ├── terraform/
│       └── cloudformation/
│
├── scripts/                     # Deployment & utility scripts
│   ├── deployment/
│   │   ├── deploy-all.ps1
│   │   ├── deploy-lambda.ps1
│   │   ├── deploy-frontend.ps1
│   │   └── rollback.ps1
│   ├── database/
│   │   ├── migrations/
│   │   ├── seed-data/
│   │   └── backup/
│   ├── election/
│   │   ├── upload-state-data.py
│   │   ├── validate-data.py
│   │   └── generate-guides.py
│   ├── maintenance/
│   │   ├── cleanup-backups.ps1
│   │   ├── optimize-images.py
│   │   └── audit-costs.ps1
│   └── monitoring/
│       ├── live-logs.ps1
│       ├── check-status.ps1
│       └── alert-setup.ps1
│
├── docs/                        # Documentation
│   ├── architecture/
│   │   ├── SYSTEM_DESIGN.md
│   │   ├── API_DOCUMENTATION.md
│   │   └── DATABASE_SCHEMA.md
│   ├── deployment/
│   │   ├── DEPLOYMENT_GUIDE.md
│   │   └── ROLLBACK_PROCEDURES.md
│   ├── features/
│   │   ├── VIDEO_SYSTEM.md
│   │   ├── ARTICLE_SYSTEM.md
│   │   ├── ELECTION_SYSTEM.md
│   │   └── EMAIL_SYSTEM.md
│   ├── operations/
│   │   ├── MONITORING.md
│   │   ├── TROUBLESHOOTING.md
│   │   └── RUNBOOKS.md
│   └── development/
│       ├── CODING_STANDARDS.md
│       ├── TESTING_GUIDE.md
│       └── CONTRIBUTION_GUIDE.md
│
├── data/                        # Data files
│   ├── election/
│   │   ├── csv/
│   │   ├── voter-guides/
│   │   └── templates/
│   ├── email/
│   │   └── templates/
│   └── test/
│       └── fixtures/
│
├── tests/                       # Test files
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── build/                       # Build artifacts (gitignored)
│   ├── lambda-packages/
│   └── frontend-dist/
│
├── .github/                     # GitHub workflows
│   └── workflows/
│       ├── deploy.yml
│       └── test.yml
│
├── .gitignore
├── README.md
└── package.json
```

---

## Migration Plan

### Phase 1: Create New Structure (2 hours)

```powershell
# Create new directory structure
mkdir src\frontend\public
mkdir src\frontend\admin
mkdir src\frontend\components
mkdir src\frontend\assets\css
mkdir src\frontend\assets\js
mkdir src\frontend\assets\images
mkdir src\backend\shared\auth
mkdir src\backend\shared\database
mkdir src\backend\shared\utils
mkdir src\backend\api
mkdir src\backend\workers
mkdir scripts\deployment
mkdir scripts\database
mkdir scripts\election
mkdir scripts\maintenance
mkdir docs\architecture
mkdir docs\features
mkdir data\election
mkdir tests\unit
mkdir build
```

### Phase 2: Move Frontend Files (3 hours)

```powershell
# Move public HTML files
Move-Item *.html src\frontend\public\

# Move admin files
Move-Item admin*.html src\frontend\admin\

# Move components
Move-Item navbar.* src\frontend\components\

# Move assets
Move-Item assets\* src\frontend\assets\

# Move PWA files
Move-Item manifest.json src\frontend\pwa\
Move-Item service-worker.js src\frontend\pwa\
Move-Item pwa-install.js src\frontend\pwa\
```

### Phase 3: Reorganize Lambda Functions (4 hours)

```powershell
# Move Lambda functions to new structure
Move-Item auth_api\index.py src\backend\api\auth\handler.py
Move-Item articles_api\index.py src\backend\api\articles\handler.py
Move-Item admin_api\index.py src\backend\api\admin\handler.py
# ... repeat for all Lambda functions
```

### Phase 4: Consolidate Scripts (2 hours)

```powershell
# Move deployment scripts
Move-Item deploy-*.ps1 scripts\deployment\

# Move database scripts
Move-Item upload_*.py scripts\database\
Move-Item check_*.py scripts\database\

# Move election scripts
Move-Item "Election Data and Files\Scripts\*" scripts\election\
```

### Phase 5: Clean Up (2 hours)

```powershell
# Remove backup files
Remove-Item *.backup
Remove-Item *.backup_*

# Remove old ZIP files
Remove-Item *-api.zip
Remove-Item *-deployment.zip

# Remove test files from root
Move-Item test-*.html tests\integration\
```

---

## Decoupling Recommendations

### 1. Extract Shared Logic into Modules

**Current Problem:**
```python
# Duplicated in every Lambda function
def verify_token(token):
    # JWT validation logic
    pass

def get_user(email):
    # DynamoDB query
    pass
```

**Better Approach:**
```python
# src/backend/shared/auth/jwt_validator.py
class JWTValidator:
    def __init__(self, secret):
        self.secret = secret
    
    def verify(self, token):
        # Centralized JWT validation
        pass

# src/backend/shared/database/user_repository.py
class UserRepository:
    def __init__(self, dynamodb_client):
        self.db = dynamodb_client
    
    def get_by_email(self, email):
        # Centralized user queries
        pass

# Usage in Lambda functions
from shared.auth import JWTValidator
from shared.database import UserRepository

validator = JWTValidator(os.environ['JWT_SECRET'])
user_repo = UserRepository(dynamodb)

def handler(event, context):
    token = event['headers']['authorization']
    user = validator.verify(token)
    # ...
```

**Benefits:**
- Single source of truth
- Easier testing
- Consistent behavior
- Reduced code duplication

---

### 2. Create Lambda Layer for Shared Code

**Current:** Each Lambda has duplicate dependencies

**Better:**
```
shared-utils-layer/
├── python/
│   ├── shared/
│   │   ├── auth/
│   │   ├── database/
│   │   ├── cache/
│   │   └── utils/
│   └── requirements.txt
```

**Deploy:**
```powershell
# Package shared layer
cd src\backend\shared
zip -r ../../../build/shared-utils-layer.zip .

# Upload to Lambda
aws lambda publish-layer-version `
    --layer-name shared-utils `
    --zip-file fileb://build/shared-utils-layer.zip `
    --compatible-runtimes python3.12

# Attach to all Lambda functions
$LAYER_ARN = (aws lambda list-layer-versions --layer-name shared-utils --query 'LayerVersions[0].LayerVersionArn' --output text)

aws lambda update-function-configuration `
    --function-name auth-api `
    --layers $LAYER_ARN
```

---

### 3. Split Monolithic Lambda Functions

**Current Problem:** `router/index.py` is 500+ lines

**Better Approach:**
```
src/backend/api/router/
├── handler.py              # Main entry point (50 lines)
├── quota_checker.py        # Quota logic (100 lines)
├── job_dispatcher.py       # Routing logic (100 lines)
├── validators.py           # Input validation (50 lines)
└── requirements.txt
```

**handler.py:**
```python
from quota_checker import QuotaChecker
from job_dispatcher import JobDispatcher
from validators import validate_video_request

quota = QuotaChecker()
dispatcher = JobDispatcher()

def handler(event, context):
    # Parse request
    request = parse_event(event)
    
    # Validate
    if not validate_video_request(request):
        return error_response(400, "Invalid request")
    
    # Check quota
    if not quota.check(request['user_email']):
        return error_response(429, "Quota exceeded")
    
    # Dispatch job
    job_id = dispatcher.dispatch(request)
    
    return success_response({'job_id': job_id})
```

---

### 4. Implement Repository Pattern

**Current:** Direct DynamoDB calls everywhere

**Better:**
```python
# src/backend/shared/database/repositories/article_repository.py
class ArticleRepository:
    def __init__(self, table):
        self.table = table
    
    def get_by_id(self, article_id):
        response = self.table.get_item(Key={'article_id': article_id})
        return response.get('Item')
    
    def list_published(self, limit=20):
        response = self.table.query(
            IndexName='status-index',
            KeyConditionExpression='status = :status',
            ExpressionAttributeValues={':status': 'published'},
            Limit=limit
        )
        return response['Items']
    
    def create(self, article):
        self.table.put_item(Item=article)
        return article
    
    def update(self, article_id, updates):
        # Build update expression
        update_expr = 'SET ' + ', '.join([f'#{k} = :{k}' for k in updates.keys()])
        expr_names = {f'#{k}': k for k in updates.keys()}
        expr_values = {f':{k}': v for k, v in updates.items()}
        
        self.table.update_item(
            Key={'article_id': article_id},
            UpdateExpression=update_expr,
            ExpressionAttributeNames=expr_names,
            ExpressionAttributeValues=expr_values
        )

# Usage in Lambda
from shared.database.repositories import ArticleRepository

articles = ArticleRepository(dynamodb.Table('articles'))

def handler(event, context):
    article_id = event['pathParameters']['id']
    article = articles.get_by_id(article_id)
    return success_response(article)
```

---

### 5. Create Service Layer

**Current:** Business logic mixed with API handlers

**Better:**
```python
# src/backend/shared/services/article_service.py
class ArticleService:
    def __init__(self, article_repo, cache, analytics):
        self.articles = article_repo
        self.cache = cache
        self.analytics = analytics
    
    def get_article(self, article_id):
        # Try cache first
        cached = self.cache.get(f'article:{article_id}')
        if cached:
            return cached
        
        # Get from database
        article = self.articles.get_by_id(article_id)
        
        # Cache it
        self.cache.set(f'article:{article_id}', article, ttl=3600)
        
        # Track view
        self.analytics.track_view(article_id)
        
        return article
    
    def publish_article(self, article_id, user):
        # Check permissions
        if not user.can_publish():
            raise PermissionError("User cannot publish articles")
        
        # Update status
        self.articles.update(article_id, {'status': 'published', 'published_at': datetime.now()})
        
        # Invalidate cache
        self.cache.delete(f'article:{article_id}')
        
        # Send notifications
        self.send_publication_notifications(article_id)
        
        return self.articles.get_by_id(article_id)

# Usage in Lambda
from shared.services import ArticleService
from shared.database.repositories import ArticleRepository
from shared.cache import RedisCache
from shared.analytics import AnalyticsTracker

articles_repo = ArticleRepository(dynamodb.Table('articles'))
cache = RedisCache(redis_client)
analytics = AnalyticsTracker(dynamodb.Table('analytics'))

article_service = ArticleService(articles_repo, cache, analytics)

def handler(event, context):
    article_id = event['pathParameters']['id']
    article = article_service.get_article(article_id)
    return success_response(article)
```

---

### 6. Implement Event-Driven Architecture

**Current:** Tight coupling between components

**Better:**
```python
# src/backend/shared/events/event_bus.py
class EventBus:
    def __init__(self, sns_client):
        self.sns = sns_client
        self.topic_arn = os.environ['EVENT_TOPIC_ARN']
    
    def publish(self, event_type, data):
        self.sns.publish(
            TopicArn=self.topic_arn,
            Message=json.dumps(data),
            MessageAttributes={
                'event_type': {'DataType': 'String', 'StringValue': event_type}
            }
        )

# Usage: Publish events
event_bus = EventBus(sns_client)

def publish_article(article):
    # Save article
    articles.create(article)
    
    # Publish event
    event_bus.publish('article.published', {
        'article_id': article['article_id'],
        'title': article['title'],
        'author': article['author']
    })

# Subscribers listen for events
def email_notification_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        event_type = record['Sns']['MessageAttributes']['event_type']['Value']
        
        if event_type == 'article.published':
            send_email_notification(message)

def analytics_handler(event, context):
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        event_type = record['Sns']['MessageAttributes']['event_type']['Value']
        
        if event_type == 'article.published':
            track_publication(message)
```

---

### 7. Configuration Management

**Current:** Hardcoded values everywhere

**Better:**
```python
# src/backend/shared/config/settings.py
class Settings:
    def __init__(self):
        self.jwt_secret = os.environ['JWT_SECRET']
        self.dynamodb_region = os.environ.get('AWS_REGION', 'us-east-1')
        self.redis_host = os.environ.get('REDIS_HOST')
        self.redis_port = int(os.environ.get('REDIS_PORT', 6379))
        self.s3_bucket = os.environ['S3_BUCKET']
        self.cloudfront_domain = os.environ['CLOUDFRONT_DOMAIN']
        
        # Feature flags
        self.enable_cache = os.environ.get('ENABLE_CACHE', 'true').lower() == 'true'
        self.enable_analytics = os.environ.get('ENABLE_ANALYTICS', 'true').lower() == 'true'
        
        # Rate limits
        self.rate_limit_free = int(os.environ.get('RATE_LIMIT_FREE', 10))
        self.rate_limit_premium = int(os.environ.get('RATE_LIMIT_PREMIUM', 100))

settings = Settings()

# Usage
from shared.config import settings

def handler(event, context):
    if settings.enable_cache:
        # Use cache
        pass
```

---

## File Naming Conventions

### Standardize on kebab-case for files:

```
✅ Good:
- article-service.py
- user-repository.py
- jwt-validator.py
- admin-dashboard.html
- create-article.html

❌ Bad:
- articleService.py
- user_repository.py
- JWTValidator.py
- adminDashboard.html
- create_article.html
```

### Python modules: snake_case
```python
from shared.auth import jwt_validator
from shared.database import user_repository
```

### Classes: PascalCase
```python
class ArticleService:
    pass

class UserRepository:
    pass
```

### Functions/variables: snake_case
```python
def get_article_by_id(article_id):
    pass

user_email = "test@example.com"
```

---

## Cleanup Script

```powershell
# cleanup-project.ps1

Write-Host "Cleaning up project..." -ForegroundColor Cyan

# Remove backup files
Write-Host "Removing backup files..." -ForegroundColor Yellow
Remove-Item *.backup -Force
Remove-Item *.backup_* -Force

# Remove old ZIP files
Write-Host "Removing old deployment packages..." -ForegroundColor Yellow
Remove-Item *-api.zip -Force
Remove-Item *-deployment.zip -Force
Remove-Item function.zip -Force -Recurse

# Remove test payloads from root
Write-Host "Moving test files..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path tests\payloads -Force
Move-Item test-*.json tests\payloads\ -Force
Move-Item *-payload.json tests\payloads\ -Force

# Remove duplicate dependencies
Write-Host "Removing duplicate dependencies..." -ForegroundColor Yellow
Get-ChildItem -Recurse -Directory -Filter "jwt" | Where-Object { $_.Parent.Name -like "*_api" } | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Directory -Filter "PyJWT-*" | Where-Object { $_.Parent.Name -like "*_api" } | Remove-Item -Recurse -Force

# Create build directory
Write-Host "Creating build directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path build -Force

# Move deployment packages to build
Move-Item *.zip build\ -Force

Write-Host "✅ Cleanup complete!" -ForegroundColor Green
```

---

## Benefits of Reorganization

### Immediate Benefits
- ✅ Easier to find files
- ✅ Clearer separation of concerns
- ✅ Reduced duplication
- ✅ Better version control

### Long-term Benefits
- ✅ Easier onboarding for new developers
- ✅ Simpler testing
- ✅ Better code reuse
- ✅ Easier to scale team
- ✅ Reduced maintenance burden

### Cost Benefits
- ✅ Smaller Lambda packages (faster cold starts)
- ✅ Shared layers reduce duplication
- ✅ Easier to optimize performance
- ✅ Reduced debugging time

---

## Implementation Timeline

### Week 1: Planning (4 hours)
- Review current structure
- Plan new structure
- Create migration scripts
- Test on small subset

### Week 2: Backend Reorganization (12 hours)
- Create shared modules
- Extract common logic
- Create Lambda layers
- Update deployment scripts

### Week 3: Frontend Reorganization (8 hours)
- Move HTML files
- Reorganize assets
- Update paths
- Test all pages

### Week 4: Cleanup & Documentation (8 hours)
- Remove duplicates
- Update documentation
- Create runbooks
- Train team

**Total: 32 hours over 4 weeks**

---

## Success Criteria

✅ All files in logical directories
✅ No duplicate code across Lambda functions
✅ Shared logic in Lambda layers
✅ Clear naming conventions
✅ Updated documentation
✅ All tests passing
✅ Deployment scripts working
✅ Team trained on new structure

**Next:** Start with Phase 1 - Create new directory structure
