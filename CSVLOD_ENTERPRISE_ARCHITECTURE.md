# CSVLOD Enterprise Architecture Framework

## Christian Conservatives Today Platform

**Document Version**: 1.0  
**Date**: January 2025  
**Framework**: Svyatoslav Kotusev CSVLOD Model  
**Organization**: Christian Conservatives Today  
**Platform URL**: https://christianconservativestoday.com

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Considerations (Strategic EA Artifacts)](#considerations)
3. [Standards (IT Standards & Policies)](#standards)
4. [Visions (Future State Architecture)](#visions)
5. [Landscapes (Current State Architecture)](#landscapes)
6. [Outlines (Solution Architecture)](#outlines)
7. [Designs (Technical Specifications)](#designs)

---

## Executive Summary

### About CSVLOD Framework

The CSVLOD framework, developed by Svyatoslav Kotusev, represents six types of Enterprise Architecture artifacts that organizations actually use in practice:

- **Considerations**: Strategic documents guiding IT investment decisions
- **Standards**: Mandatory rules and policies for technology usage
- **Visions**: High-level future state architecture descriptions
- **Landscapes**: Current state IT environment documentation
- **Outlines**: Solution-level architecture for specific initiatives
- **Designs**: Detailed technical specifications for implementation

### Platform Overview

**Christian Conservatives Today** is a serverless video and article platform serving the 5-fold ministry (apostles, prophets, evangelists, pastors, teachers), Christian believers, and conservative voices. Built entirely on AWS serverless architecture with 9 microservices, 4 DynamoDB tables, and S3/CloudFront content delivery.

**Key Metrics**:

- **Architecture**: 100% Serverless (AWS Lambda, DynamoDB, S3, CloudFront)
- **Microservices**: 9 Lambda functions
- **Users**: 3-tier role system (Super User > Admin > User)
- **Content**: Video hosting, article publishing, Bible integration
- **Billing**: PayPal subscription system (4 tiers)
- **Current Scale**: 100+ users, 500GB storage, 150+ articles

---

## 1. CONSIDERATIONS (Strategic EA Artifacts)

### 1.1 Business Case - Platform Justification

**Document Type**: Strategic Business Case  
**Audience**: Executive Leadership, Board of Directors  
**Purpose**: Justify investment in Christian Conservative digital platform

#### Problem Statement

Christian conservatives face increasing censorship on mainstream platforms (YouTube, Facebook, Twitter). Churches, ministries, and conservative voices need a safe platform to share biblical teachings, sermons, and political commentary without fear of deplatforming.

#### Business Opportunity

**Market Gap**:
- Existing platforms (YouTube, Vimeo) censor conservative Christian content
- No platform combines video hosting + article publishing + Bible integration
- Ministry-focused features (sermon templates, scripture lookup) not available elsewhere
- Conservative political commentary increasingly restricted on mainstream platforms

**Target Market**:
- 5-fold ministry leaders (apostles, prophets, evangelists, pastors, teachers)
- 75 million evangelical Christians in USA
- Conservative political commentators and activists
- Churches seeking digital outreach platforms
- Bible study groups and Christian educators

#### Financial Projections

**Revenue Model**: Subscription-based (PayPal)
```
Tier          | Price/Month | Storage | Videos | Target Users
--------------|-------------|---------|--------|-------------
Free          | $0          | 2GB     | 50     | 10,000
Premium       | $9.99       | 25GB    | 500    | 1,000
Pro           | $24.99      | 100GB   | 2,000  | 200
Enterprise    | $99.99      | Unlimited| Unlimited| 50
```

**Year 1 Projections**:
- Free Users: 10,000 (no revenue)
- Premium: 1,000 × $9.99 = $9,990/month = $119,880/year
- Pro: 200 × $24.99 = $4,998/month = $59,976/year
- Enterprise: 50 × $99.99 = $4,999/month = $59,988/year
- **Total Year 1 Revenue**: $239,844

**Year 1 Costs**:
- AWS Infrastructure: $5,000/month = $60,000/year
- Development: $150,000 (2 engineers)
- Marketing: $30,000
- **Total Year 1 Costs**: $240,000

**Break-even**: Month 12  
**ROI**: 5-year projected ROI of 400%

#### Strategic Alignment

**Mission Alignment**:
- ✅ Advance Christian ministry through digital platforms
- ✅ Provide censorship-free platform for conservative voices
- ✅ Bridge gap between faith and politics with biblical wisdom
- ✅ Support churches and ministries in digital transformation

**Strategic Objectives**:
1. Become #1 Christian conservative video platform by 2027
2. Reach 100,000 users by 2026
3. Host 1 million videos by 2028
4. Generate $2M annual revenue by 2027

### 1.2 Principles - Architectural Guiding Principles

**Document Type**: IT Principles  
**Audience**: IT Leadership, Development Teams  
**Purpose**: Guide all technology decisions

#### Principle 1: Serverless First
**Statement**: All new services must be serverless unless justified otherwise  
**Rationale**: Minimize operational overhead, maximize scalability, reduce costs  
**Implications**: Use Lambda, DynamoDB, S3; avoid EC2, RDS unless necessary

#### Principle 2: AWS Native
**Statement**: Prefer AWS-native services over third-party solutions  
**Rationale**: Deep integration, better support, simplified architecture  
**Implications**: Use AWS Bedrock (not OpenAI), DynamoDB (not MongoDB), S3 (not third-party storage)

#### Principle 3: API-First Design
**Statement**: All services expose RESTful APIs via API Gateway  
**Rationale**: Enable future mobile apps, third-party integrations, microservices communication  
**Implications**: Every Lambda function accessible via API Gateway, versioned APIs

#### Principle 4: Security by Design
**Statement**: Security controls built into every layer from day one  
**Rationale**: Protect user data, prevent breaches, maintain trust  
**Implications**: JWT authentication, role-based access, encryption at rest/transit, WAF protection

#### Principle 5: Cost Optimization
**Statement**: Minimize AWS costs through architectural decisions  
**Rationale**: Maintain profitability, keep subscription prices competitive  
**Implications**: Use on-demand DynamoDB, CloudFront caching, Lambda memory optimization, S3 lifecycle policies

#### Principle 6: Biblical Integration
**Statement**: Platform must integrate biblical resources and Christian perspective  
**Rationale**: Differentiate from secular platforms, serve ministry needs  
**Implications**: Bible verse lookup, scripture references, Christian templates, ministry-focused features

#### Principle 7: Censorship Resistance
**Statement**: Platform must resist external pressure to censor conservative Christian content  
**Rationale**: Core mission is providing safe space for Christian conservative voices  
**Implications**: Clear content policies, legal protections, backup strategies, multi-cloud consideration

#### Principle 8: Scalability Without Complexity
**Statement**: Architecture must scale to millions of users without adding complexity  
**Rationale**: Small team, limited resources, need for simplicity  
**Implications**: Serverless auto-scaling, managed services, avoid custom infrastructure

### 1.3 Policies - IT Governance Policies

**Document Type**: IT Policies  
**Audience**: All IT Staff, Contractors  
**Purpose**: Mandatory rules for technology usage

#### Policy 1: Data Classification and Handling

**Policy Statement**: All data must be classified and handled according to sensitivity level

**Data Classifications**:
- **Public**: Videos/articles with public visibility, platform marketing content
- **Internal**: User emails, subscription data, usage statistics
- **Confidential**: Password hashes, payment information, admin logs
- **Restricted**: System credentials, API keys, encryption keys

**Handling Requirements**:
- Public: No restrictions, CDN delivery allowed
- Internal: Encrypted at rest, access logging required
- Confidential: Encrypted at rest/transit, MFA for access, audit logging
- Restricted: AWS Secrets Manager only, no code commits, rotation every 90 days

#### Policy 2: Access Control

**Policy Statement**: All system access must follow least privilege principle

**Requirements**:
- User accounts: Email + password (SHA-256, upgrading to bcrypt)
- Admin accounts: MFA required (to be implemented)
- Super User accounts: MFA + IP whitelist (to be implemented)
- Service accounts: IAM roles with minimal permissions
- API access: JWT tokens with 24-hour expiration
- Database access: IAM authentication, no shared credentials

#### Policy 3: Code Management

**Policy Statement**: All code must be version controlled and reviewed

**Requirements**:
- Git repository for all code (currently GitHub)
- Branch protection for main/production branches
- Code review required for all changes (to be implemented)
- No secrets in code repositories
- Automated testing before deployment (to be implemented)
- Deployment via CI/CD pipeline (to be implemented)

#### Policy 4: Backup and Recovery

**Policy Statement**: All critical data must be backed up with tested recovery procedures

**Requirements**:
- DynamoDB: Point-in-time recovery enabled (to be implemented)
- S3: Versioning enabled, lifecycle policies for archival
- Lambda: Code stored in version control
- Recovery Time Objective (RTO): 4 hours
- Recovery Point Objective (RPO): 1 hour
- Quarterly disaster recovery testing (to be implemented)

#### Policy 5: Security Incident Response

**Policy Statement**: Security incidents must be detected, reported, and resolved promptly

**Requirements**:
- CloudWatch alarms for suspicious activity (to be implemented)
- AWS GuardDuty enabled (to be implemented)
- Incident response plan documented (to be implemented)
- Security incidents reported within 1 hour
- Post-incident review within 48 hours
- User notification within 72 hours if data breach

#### Policy 6: Change Management

**Policy Statement**: All production changes must follow change management process

**Requirements**:
- Change request for all production deployments (to be implemented)
- Testing in non-production environment first
- Rollback plan documented before deployment
- Change window: Off-peak hours (2 AM - 6 AM EST)
- Emergency changes: Approval from IT Director
- Post-deployment verification required

### 1.4 Roadmap - Strategic IT Roadmap

**Document Type**: Multi-Year IT Roadmap  
**Audience**: Executive Leadership, IT Leadership  
**Purpose**: Plan technology investments over 3 years

#### 2025 Roadmap - Stabilization & Security

**Q1 2025 (Jan-Mar)**: Security Hardening
- Migrate JWT secrets to AWS Secrets Manager
- Implement AWS WAF for API Gateway
- Upgrade password hashing from SHA-256 to bcrypt
- Enable CloudTrail audit logging
- Add MFA for admin accounts
- **Investment**: $15K (engineering time)

**Q2 2025 (Apr-Jun)**: Reliability & Backup
- Implement DynamoDB point-in-time recovery
- Create disaster recovery runbook
- Add CloudWatch alarms and SNS alerts
- Implement health check endpoints
- Quarterly DR testing
- **Investment**: $10K (engineering time)

**Q3 2025 (Jul-Sep)**: Infrastructure as Code
- Convert all infrastructure to Terraform
- Implement CI/CD pipeline (AWS CodePipeline)
- Add automated testing (unit + integration)
- Blue-green deployment strategy
- **Investment**: $25K (engineering time)

**Q4 2025 (Oct-Dec)**: Performance Optimization
- Implement ElastiCache Redis for caching
- Add API versioning (v1, v2)
- Optimize Lambda memory allocation
- CloudFront caching optimization
- **Investment**: $20K (engineering + AWS costs)

**2025 Total Investment**: $70K

#### 2026 Roadmap - Scalability & Growth

**Q1 2026**: Multi-Region Deployment
- Deploy to us-west-2 (disaster recovery)
- Route 53 failover routing
- Cross-region DynamoDB replication
- Multi-region S3 replication
- **Investment**: $40K

**Q2 2026**: Advanced Features
- Implement GraphQL API (alongside REST)
- Add OpenSearch for full-text search
- AI-powered content recommendations
- Advanced analytics dashboard
- **Investment**: $50K

**Q3 2026**: Mobile Applications
- React Native mobile app (iOS + Android)
- Push notifications
- Offline video playback
- Mobile-optimized UI
- **Investment**: $80K

**Q4 2026**: Enterprise Features
- SSO integration (SAML, OAuth)
- White-label capabilities
- Advanced admin controls
- Custom branding for churches
- **Investment**: $60K

**2026 Total Investment**: $230K

#### 2027 Roadmap - Intelligence & Expansion

**Q1 2027**: AI/ML Integration
- AI-powered sermon outline generator
- Automated content moderation
- Personalization engine
- Predictive analytics
- **Investment**: $70K

**Q2 2027**: Live Streaming
- Live video streaming capability
- Real-time chat integration
- Multi-camera support
- DVR functionality
- **Investment**: $90K

**Q3 2027**: Community Features
- Discussion forums
- Bible study groups
- Prayer request system
- Event calendar
- **Investment**: $60K

**Q4 2027**: Monetization Expansion
- Add Stripe payment processing
- Donation/tithing integration
- Merchandise marketplace
- Affiliate program
- **Investment**: $50K

**2027 Total Investment**: $270K

**3-Year Total Investment**: $570K  
**Expected 3-Year Revenue**: $2.5M  
**3-Year ROI**: 340%


---

## 2. STANDARDS (IT Standards & Policies)

### 2.1 Technology Standards

**Document Type**: Technology Standards Catalog  
**Audience**: Development Teams, Architects  
**Purpose**: Define approved technologies and versions

#### Cloud Platform Standards

**Approved Cloud Provider**: Amazon Web Services (AWS)
- **Primary Region**: us-east-1 (N. Virginia)
- **DR Region**: us-west-2 (Oregon) - planned 2026
- **Rationale**: AWS serverless ecosystem, cost-effectiveness, deep service integration

**Prohibited**: Google Cloud Platform, Microsoft Azure (unless specific business case approved)

#### Compute Standards

**Approved**:
- AWS Lambda (Python 3.9+) - Primary compute platform
- AWS Fargate - For long-running video processing (>15 min)
- **Prohibited**: EC2 instances (unless justified for specific workload)

**Lambda Configuration Standards**:
```yaml
Runtime: python3.9 or python3.11
Architecture: x86_64 (arm64 for cost optimization where applicable)
Memory: 
  - Minimum: 256 MB
  - Maximum: 3008 MB (only for video processing)
  - Default: 512 MB
Timeout:
  - API functions: 30 seconds
  - Processing functions: 900 seconds (15 min max)
Environment Variables: Use AWS Secrets Manager for sensitive data
```

#### Database Standards

**Approved**:
- Amazon DynamoDB - Primary NoSQL database
- **Billing Mode**: On-Demand (PAY_PER_REQUEST)
- **Encryption**: Server-side encryption enabled (default AWS managed keys)

**Table Design Standards**:
- Primary key: Single attribute (HASH key)
- Global Secondary Indexes: Maximum 5 per table
- Attribute naming: snake_case (e.g., user_id, created_at)
- Timestamps: ISO 8601 format (e.g., 2025-01-15T10:30:00Z)

**Prohibited**: 
- Amazon RDS (unless relational data model required)
- Self-managed databases (MongoDB, PostgreSQL on EC2)

#### Storage Standards

**Approved**:
- Amazon S3 - Primary object storage
- **Bucket Naming**: lowercase-with-hyphens (e.g., my-video-downloads-bucket)
- **Encryption**: SSE-S3 (AES-256) enabled by default
- **Versioning**: Enabled for critical buckets
- **Lifecycle Policies**: Archive to Glacier after 1 year, delete after 7 years

**S3 Folder Structure Standard**:
```
bucket-name/
├── videos/           (MP4, WebM, MOV files)
├── thumbnails/       (JPEG images, 3 per video)
├── images/           (Article featured images)
└── backups/          (Database exports, logs)
```

**Prohibited**: Third-party storage providers (Dropbox, Google Drive)

#### API Standards

**API Gateway Configuration**:
- **Type**: REST API (HTTP API for simple use cases)
- **Authentication**: JWT tokens via Authorization header
- **CORS**: Enabled for all endpoints
- **Throttling**: 10,000 requests/second (default)
- **Caching**: Enabled for read-heavy endpoints (TTL: 300 seconds)

**API Versioning Standard**:
```
Format: /v{version}/{resource}
Example: /v1/articles, /v2/articles
Version in URL path (not header)
Maintain v1 for 12 months after v2 release
```

**API Response Standards**:
```json
Success (200):
{
  "statusCode": 200,
  "data": {...},
  "message": "Success message"
}

Error (4xx/5xx):
{
  "statusCode": 400,
  "error": "Error type",
  "message": "Human-readable error message"
}
```

#### Programming Language Standards

**Approved Languages**:
- **Python 3.9+**: Primary backend language (Lambda functions)
- **JavaScript (ES6+)**: Frontend development
- **SQL**: DynamoDB queries (PartiQL)

**Python Standards**:
- **Style Guide**: PEP 8
- **Linting**: pylint, flake8
- **Formatting**: black (auto-formatter)
- **Type Hints**: Required for all function signatures
- **Docstrings**: Required for all public functions

**JavaScript Standards**:
- **Style Guide**: Airbnb JavaScript Style Guide
- **Linting**: ESLint
- **Formatting**: Prettier
- **Framework**: Vanilla JS (Angular planned for Phase 4)

#### Security Standards

**Authentication Standard**:
- **Method**: JWT (JSON Web Tokens)
- **Algorithm**: HS256 (HMAC with SHA-256)
- **Expiration**: 24 hours
- **Storage**: localStorage (client-side)
- **Transmission**: Authorization header (Bearer token)

**Password Standards**:
- **Minimum Length**: 8 characters
- **Complexity**: At least 1 uppercase, 1 lowercase, 1 number
- **Hashing**: bcrypt (cost factor 12) - upgrading from SHA-256
- **Storage**: Hashed passwords only, never plaintext
- **Reset**: Email-based reset with time-limited tokens

**Encryption Standards**:
- **At Rest**: AES-256 (AWS managed keys)
- **In Transit**: TLS 1.2+ (HTTPS only)
- **Secrets**: AWS Secrets Manager (never in code)
- **API Keys**: Rotated every 90 days

#### Monitoring Standards

**CloudWatch Configuration**:
- **Log Retention**: 30 days (standard), 90 days (critical)
- **Metrics**: Custom metrics for business KPIs
- **Alarms**: SNS notifications for critical errors
- **Dashboards**: Real-time monitoring for all services

**Required Metrics**:
- Lambda invocations, errors, duration
- API Gateway request count, latency, 4xx/5xx errors
- DynamoDB read/write capacity, throttles
- S3 storage size, request count
- CloudFront cache hit ratio, data transfer

### 2.2 Development Standards

**Document Type**: Development Standards  
**Audience**: Development Teams  
**Purpose**: Ensure code quality and consistency

#### Code Repository Standards

**Version Control**: Git (GitHub)
- **Repository Structure**: Monorepo (all services in one repo)
- **Branch Strategy**: GitFlow
  - `main`: Production-ready code
  - `develop`: Integration branch
  - `feature/*`: Feature development
  - `hotfix/*`: Production bug fixes
- **Commit Messages**: Conventional Commits format
  ```
  feat: Add Bible verse search functionality
  fix: Resolve thumbnail generation timeout
  docs: Update API documentation
  ```

#### Code Review Standards

**Requirements**:
- All code changes require pull request
- Minimum 1 approval from senior developer
- Automated tests must pass
- No merge conflicts
- Code coverage >80% (to be implemented)

**Review Checklist**:
- [ ] Code follows style guide
- [ ] No hardcoded secrets or credentials
- [ ] Error handling implemented
- [ ] Logging added for debugging
- [ ] Documentation updated
- [ ] Security considerations addressed

#### Testing Standards

**Test Pyramid**:
```
        /\
       /  \  E2E Tests (10%)
      /____\
     /      \ Integration Tests (30%)
    /________\
   /          \ Unit Tests (60%)
  /____________\
```

**Unit Testing**:
- **Framework**: pytest (Python), Jest (JavaScript)
- **Coverage**: Minimum 80% code coverage
- **Mocking**: Use moto for AWS service mocking
- **Naming**: test_function_name_scenario_expected_result

**Integration Testing**:
- Test Lambda function with real AWS services (dev environment)
- Test API Gateway endpoints end-to-end
- Test DynamoDB queries with test data

**End-to-End Testing**:
- Selenium for frontend testing (to be implemented)
- Postman collections for API testing
- User journey testing (registration → upload → view)

#### Deployment Standards

**Environments**:
- **Development**: Local development, frequent changes
- **Staging**: Pre-production testing, mirrors production
- **Production**: Live user environment, change-controlled

**Deployment Process**:
1. Code merged to `develop` branch
2. Automated tests run in CI/CD pipeline
3. Deploy to staging environment
4. Manual QA testing in staging
5. Approval from tech lead
6. Deploy to production (blue-green deployment)
7. Monitor for errors (15-minute observation period)
8. Rollback if issues detected

**Deployment Windows**:
- **Standard Changes**: Tuesday/Thursday, 2 AM - 6 AM EST
- **Emergency Changes**: Anytime with approval
- **Blackout Periods**: Major Christian holidays (Christmas, Easter)

### 2.3 Naming Conventions

**Document Type**: Naming Standards  
**Audience**: All IT Staff  
**Purpose**: Ensure consistent naming across all resources

#### AWS Resource Naming

**Lambda Functions**:
```
Format: {service-name}-{environment}
Examples:
  - auth-api-prod
  - video-downloader-staging
  - thumbnail-generator-dev
```

**DynamoDB Tables**:
```
Format: {resource-name}-{environment}
Examples:
  - users-prod
  - video-metadata-staging
  - articles-dev
```

**S3 Buckets**:
```
Format: {org}-{purpose}-{environment}
Examples:
  - cct-video-downloads-prod
  - cct-backups-prod
  - cct-logs-staging
```

**API Gateway**:
```
Format: {service-name}-api-{environment}
Examples:
  - auth-api-prod
  - articles-api-staging
```

**CloudWatch Log Groups**:
```
Format: /aws/lambda/{function-name}
Examples:
  - /aws/lambda/auth-api-prod
  - /aws/lambda/video-downloader-prod
```

#### Code Naming Conventions

**Python**:
- **Functions**: snake_case (e.g., get_user_by_email)
- **Classes**: PascalCase (e.g., UserManager)
- **Constants**: UPPER_SNAKE_CASE (e.g., MAX_FILE_SIZE)
- **Private**: _leading_underscore (e.g., _internal_function)

**JavaScript**:
- **Functions**: camelCase (e.g., getUserByEmail)
- **Classes**: PascalCase (e.g., UserManager)
- **Constants**: UPPER_SNAKE_CASE (e.g., MAX_FILE_SIZE)
- **Private**: #private_field (ES2022+)

**Database**:
- **Tables**: lowercase-hyphen (e.g., video-metadata)
- **Attributes**: snake_case (e.g., user_id, created_at)
- **Indexes**: {table}-{attribute}-index (e.g., users-email-index)

### 2.4 Security Standards

**Document Type**: Security Standards  
**Audience**: All IT Staff, Security Team  
**Purpose**: Define mandatory security controls

#### Authentication & Authorization

**JWT Token Standard**:
```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "user_id": "uuid",
    "email": "user@example.com",
    "role": "user|admin|super_user",
    "exp": 1704153600
  }
}
```

**Role-Based Access Control (RBAC)**:
```
Super User (Level 3)
  ├── All admin capabilities
  ├── Create/delete super users
  ├── System-wide configuration
  └── Unlimited storage/videos

Admin (Level 2)
  ├── User management (except super users)
  ├── Content moderation
  ├── Subscription management
  └── Unlimited storage/videos

User (Level 1)
  ├── Upload videos (quota-limited)
  ├── Create articles
  ├── Manage own content
  └── Subject to subscription limits
```

#### Data Protection Standards

**Encryption Requirements**:
- **At Rest**: All S3 buckets, DynamoDB tables encrypted (AES-256)
- **In Transit**: TLS 1.2+ for all API calls, HTTPS only
- **Secrets**: AWS Secrets Manager for all credentials
- **Passwords**: bcrypt hashing (cost factor 12)

**Data Retention**:
- **User Data**: Retained until account deletion + 30 days
- **Videos**: Retained until user deletion or manual removal
- **Articles**: Retained until author deletion or manual removal
- **Logs**: 30 days (standard), 90 days (security logs)
- **Backups**: 7 years (compliance requirement)

**Data Deletion**:
- **User Deletion**: Soft delete (30-day grace period), then hard delete
- **Video Deletion**: Immediate removal from S3, metadata soft deleted
- **Article Deletion**: Soft delete (30-day recovery), then hard delete
- **Right to be Forgotten**: Full data export + deletion within 30 days (GDPR)

#### Network Security Standards

**API Gateway Security**:
- **CORS**: Configured for all endpoints
- **Throttling**: 10,000 req/sec (burst: 5,000)
- **WAF**: AWS WAF enabled (to be implemented)
  - SQL injection protection
  - XSS protection
  - Rate limiting per IP
  - Geo-blocking (if needed)

**CloudFront Security**:
- **HTTPS**: Required (redirect HTTP to HTTPS)
- **TLS**: Minimum TLS 1.2
- **Origin Access Identity**: S3 bucket access via CloudFront only
- **Signed URLs**: For private content (to be implemented)

#### Vulnerability Management

**Scanning Requirements**:
- **Dependency Scanning**: Weekly (npm audit, pip-audit)
- **Code Scanning**: On every commit (to be implemented)
- **Infrastructure Scanning**: Monthly (AWS Config, Security Hub)
- **Penetration Testing**: Annual (third-party)

**Patch Management**:
- **Critical Vulnerabilities**: Patched within 24 hours
- **High Vulnerabilities**: Patched within 7 days
- **Medium Vulnerabilities**: Patched within 30 days
- **Low Vulnerabilities**: Patched within 90 days


---

## 3. VISIONS (Future State Architecture)

### 3.1 Target Architecture Vision (2027)

**Document Type**: Future State Architecture Vision  
**Audience**: Executive Leadership, IT Leadership  
**Purpose**: Describe desired end-state architecture in 3 years

#### Vision Statement

By 2027, Christian Conservatives Today will be a **globally distributed, AI-powered, multi-platform ministry ecosystem** serving 100,000+ users across web, mobile, and smart TV platforms, with 99.99% uptime, sub-second response times, and intelligent content recommendations powered by AWS AI/ML services.

#### Target Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    GLOBAL USER ACCESS LAYER                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │ Web App  │  │ iOS App  │  │ Android  │  │ Smart TV │      │
│  │ (Angular)│  │ (Native) │  │ (Native) │  │ (Roku)   │      │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    GLOBAL CDN & API LAYER                       │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ CloudFront (Multi-Region) + Route 53 (Geo-Routing)  │      │
│  └──────────────────────────────────────────────────────┘      │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ API Gateway (REST + GraphQL) + AWS AppSync          │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              MICROSERVICES LAYER (Multi-Region)                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Auth Service │  │ Video Service│  │ Article Svc  │         │
│  │ (Lambda)     │  │ (Lambda+ECS) │  │ (Lambda)     │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Billing Svc  │  │ Search Svc   │  │ AI/ML Svc    │         │
│  │ (Lambda)     │  │ (OpenSearch) │  │ (Bedrock)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Live Stream  │  │ Community    │  │ Analytics    │         │
│  │ (MediaLive)  │  │ (Lambda)     │  │ (QuickSight) │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CACHING & MESSAGING LAYER                    │
│  ┌──────────────────────────────────────────────────┐          │
│  │ ElastiCache Redis (Session, API Cache)          │          │
│  └──────────────────────────────────────────────────┘          │
│  ┌──────────────────────────────────────────────────┐          │
│  │ EventBridge (Event-Driven Architecture)         │          │
│  └──────────────────────────────────────────────────┘          │
│  ┌──────────────────────────────────────────────────┐          │
│  │ SQS (Async Processing Queues)                   │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              DATA LAYER (Multi-Region Replication)              │
│  ┌──────────────────────────────────────────────────┐          │
│  │ DynamoDB Global Tables (us-east-1, us-west-2)   │          │
│  │ - users, video-metadata, articles, subscriptions│          │
│  └──────────────────────────────────────────────────┘          │
│  ┌──────────────────────────────────────────────────┐          │
│  │ S3 (Multi-Region Replication)                   │          │
│  │ - videos/, thumbnails/, images/                 │          │
│  └──────────────────────────────────────────────────┘          │
│  ┌──────────────────────────────────────────────────┐          │
│  │ OpenSearch (Full-Text Search)                   │          │
│  │ - Video search, article search, user search     │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI/ML & ANALYTICS LAYER                      │
│  ┌──────────────────────────────────────────────────┐          │
│  │ AWS Bedrock (Content Generation, Moderation)    │          │
│  └──────────────────────────────────────────────────┘          │
│  ┌──────────────────────────────────────────────────┐          │
│  │ SageMaker (Recommendation Engine)               │          │
│  └──────────────────────────────────────────────────┘          │
│  ┌──────────────────────────────────────────────────┐          │
│  │ QuickSight (Business Intelligence Dashboards)   │          │
│  └──────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

#### Key Architectural Changes (Current → Future)

**1. Multi-Region Deployment**
- **Current**: Single region (us-east-1)
- **Future**: Active-active in us-east-1 and us-west-2
- **Benefit**: 99.99% uptime, disaster recovery, lower latency

**2. Mobile Applications**
- **Current**: Web-only (HTML/JavaScript)
- **Future**: Native iOS, Android, Roku/Fire TV apps
- **Benefit**: Reach mobile users, offline playback, push notifications

**3. Advanced Search**
- **Current**: Basic DynamoDB queries
- **Future**: OpenSearch with full-text search, faceted search, autocomplete
- **Benefit**: Better content discovery, improved user experience

**4. AI/ML Integration**
- **Current**: Optional AWS Bedrock for URL summarization
- **Future**: AI-powered recommendations, content moderation, sermon generation
- **Benefit**: Personalized experience, automated moderation, ministry tools

**5. Live Streaming**
- **Current**: Pre-recorded videos only
- **Future**: AWS MediaLive for live church services, conferences
- **Benefit**: Real-time ministry, event broadcasting, interactive chat

**6. Caching Layer**
- **Current**: CloudFront CDN only
- **Future**: ElastiCache Redis for API responses, session management
- **Benefit**: Sub-second response times, reduced database load

**7. Event-Driven Architecture**
- **Current**: Direct Lambda invocations, S3 triggers
- **Future**: EventBridge for event routing, SQS for async processing
- **Benefit**: Decoupled services, better scalability, easier debugging

**8. GraphQL API**
- **Current**: REST APIs only
- **Future**: GraphQL via AWS AppSync (alongside REST)
- **Benefit**: Flexible queries, reduced over-fetching, better mobile performance

#### Target Performance Metrics (2027)

```
Metric                    | Current (2025) | Target (2027)
--------------------------|----------------|---------------
Uptime                    | 99.5%          | 99.99%
API Response Time (p95)   | 500ms          | 100ms
Video Load Time           | 3 seconds      | 1 second
Search Results            | 2 seconds      | 200ms
Concurrent Users          | 1,000          | 50,000
Monthly Active Users      | 100            | 100,000
Total Videos              | 500            | 1,000,000
Total Articles            | 150            | 100,000
Storage Capacity          | 500GB          | 500TB
```

### 3.2 Business Capability Model (Future State)

**Document Type**: Business Capability Map  
**Audience**: Business Leaders, IT Leadership  
**Purpose**: Define future business capabilities enabled by technology

#### Core Capabilities (Revenue-Generating)

**1. Content Management**
- Video hosting and streaming (current + enhanced)
- Article publishing and blogging (current + enhanced)
- Live streaming (new - 2026)
- Podcast hosting (new - 2027)
- E-book publishing (new - 2027)

**2. User Management**
- Authentication and authorization (current + SSO)
- Subscription management (current + Stripe)
- Profile management (current + enhanced)
- White-label accounts (new - 2026)

**3. Community Engagement**
- Comments and discussions (current)
- Forums and groups (new - 2027)
- Prayer requests (new - 2027)
- Event calendar (new - 2027)
- Live chat (new - 2026)

**4. Revenue Generation**
- Subscription billing (current + Stripe)
- Donation processing (new - 2027)
- Merchandise sales (new - 2027)
- Affiliate program (new - 2027)
- Advertising (optional - 2027)

#### Supporting Capabilities

**5. Content Discovery**
- Search and filtering (current + OpenSearch)
- Recommendations (new - AI-powered)
- Categorization and tagging (current + enhanced)
- Trending content (new - 2026)
- Personalization (new - AI-powered)

**6. Analytics and Insights**
- Usage analytics (basic + QuickSight)
- Content performance (new - 2026)
- User behavior tracking (new - 2026)
- Revenue analytics (new - 2026)
- Ministry impact metrics (new - 2027)

**7. Content Creation Tools**
- Video editor (new - 2027)
- Sermon outline generator (new - AI-powered)
- Bible study tools (current + enhanced)
- Graphics creator (new - 2027)
- Teleprompter (new - 2027)

**8. Administration**
- User management (current + enhanced)
- Content moderation (current + AI-powered)
- Subscription management (current + enhanced)
- System configuration (current + enhanced)
- Reporting and dashboards (new - QuickSight)

### 3.3 Technology Vision

**Document Type**: Technology Vision Statement  
**Audience**: IT Leadership, Development Teams  
**Purpose**: Articulate technology direction and principles

#### Vision Statement

**"By 2027, Christian Conservatives Today will operate on a cloud-native, AI-enhanced, globally distributed platform that empowers ministry leaders with cutting-edge tools while maintaining simplicity, security, and biblical integrity."**

#### Technology Pillars

**Pillar 1: Serverless-First**
- Continue AWS Lambda as primary compute
- Add AWS Fargate for containerized workloads
- Minimize operational overhead
- Auto-scaling by default

**Pillar 2: AI-Powered**
- AWS Bedrock for content generation and moderation
- SageMaker for personalized recommendations
- Automated sermon outline generation
- Intelligent content tagging

**Pillar 3: Multi-Platform**
- Web (Angular SPA)
- Mobile (iOS, Android native apps)
- Smart TV (Roku, Fire TV, Apple TV)
- API-first design for third-party integrations

**Pillar 4: Globally Distributed**
- Multi-region active-active deployment
- Edge computing with Lambda@Edge
- Global CDN with CloudFront
- Sub-100ms latency worldwide

**Pillar 5: Event-Driven**
- EventBridge for event routing
- SQS for async processing
- SNS for notifications
- Decoupled microservices

**Pillar 6: Data-Driven**
- Real-time analytics with QuickSight
- Machine learning insights
- A/B testing framework
- Predictive analytics

#### Technology Adoption Strategy

**Adopt** (Actively invest in):
- AWS Bedrock (AI/ML)
- AWS AppSync (GraphQL)
- OpenSearch (full-text search)
- ElastiCache Redis (caching)
- EventBridge (event-driven)

**Trial** (Experiment with):
- AWS MediaLive (live streaming)
- SageMaker (ML models)
- Lambda@Edge (edge computing)
- AWS Amplify (mobile backend)

**Assess** (Monitor for future):
- AWS IoT (smart devices)
- AWS RoboMaker (robotics)
- Quantum computing (AWS Braket)

**Hold** (Avoid new investment):
- EC2 instances (use Lambda/Fargate instead)
- Self-managed databases (use managed services)
- Monolithic architecture (continue microservices)

---

## 4. LANDSCAPES (Current State Architecture)

### 4.1 Application Landscape

**Document Type**: Application Portfolio  
**Audience**: IT Leadership, Business Leaders  
**Purpose**: Document all applications and their relationships

#### Application Inventory

**Frontend Applications**:
```
Application         | Technology      | Users  | Status
--------------------|-----------------|--------|--------
Web Portal          | HTML/JS/Bootstrap| All   | Production
Admin Dashboard     | HTML/JS         | Admins | Production
Login Portal        | HTML/JS         | All    | Production
Video Player        | HTML5 Video     | All    | Production
Article Editor      | Quill.js        | Authors| Production
```

**Backend Services (Lambda Functions)**:
```
Service             | Language | Purpose              | Status
--------------------|----------|----------------------|--------
auth-api            | Python   | Authentication       | Production
admin-api           | Python   | Admin operations     | Production
tag-api             | Python   | Video metadata       | Production
router              | Python   | Job routing          | Production
downloader          | Python   | Video processing     | Production
articles-api        | Python   | Article management   | Production
paypal-billing-api  | Python   | Subscription billing | Production
thumbnail-generator | Python   | Thumbnail creation   | Production
url-analysis-api    | Python   | URL scraping/AI      | Production
comments-api        | Python   | User comments        | Production
news-api            | Python   | News management      | Production
resources-api       | Python   | Resource management  | Production
```

#### Application Dependencies

```
Web Portal
  ├── auth-api (authentication)
  ├── tag-api (video listing)
  ├── articles-api (article listing)
  └── CloudFront (content delivery)

Admin Dashboard
  ├── admin-api (user/video management)
  ├── tag-api (metadata management)
  └── paypal-billing-api (subscription management)

Video Processing Pipeline
  ├── router (job orchestration)
  ├── downloader (yt-dlp processing)
  ├── thumbnail-generator (FFmpeg)
  └── tag-api (metadata storage)

Article System
  ├── articles-api (CRUD operations)
  ├── Bible API (external - verse lookup)
  └── AWS Bedrock (optional - AI summaries)

Billing System
  ├── paypal-billing-api (subscription management)
  ├── PayPal API (external - payment processing)
  └── router (quota enforcement)
```

### 4.2 Technology Landscape

**Document Type**: Technology Inventory  
**Audience**: IT Leadership, Architects  
**Purpose**: Document all technologies in use

#### Infrastructure Components

**Compute**:
- AWS Lambda (9 functions, Python 3.9)
- AWS Fargate (planned for long video processing)

**Storage**:
- Amazon S3 (1 bucket: my-video-downloads-bucket)
  - videos/ (500GB)
  - thumbnails/ (50GB)
- Amazon DynamoDB (4 tables, on-demand billing)
  - users (100 items)
  - video-metadata (500 items)
  - articles (150 items)
  - download-jobs (1000 items)

**Networking**:
- Amazon CloudFront (1 distribution)
- Amazon API Gateway (6 REST APIs)
- Amazon Route 53 (DNS management)

**Security**:
- AWS IAM (roles and policies)
- AWS Secrets Manager (planned - not yet implemented)
- AWS WAF (planned - not yet implemented)

**Monitoring**:
- Amazon CloudWatch (logs and metrics)
- Amazon SNS (email notifications)

**AI/ML**:
- AWS Bedrock (Claude Instant - optional)

#### External Integrations

**Payment Processing**:
- PayPal Subscriptions API
- PayPal Webhooks

**Content APIs**:
- Bible API (bible-api.com) - Free tier
- YouTube API (thumbnail extraction)

**Video Processing**:
- yt-dlp (open source)
- FFmpeg (open source)

#### Development Tools

**Version Control**:
- Git (GitHub repository)

**IDE/Editors**:
- VS Code
- PyCharm

**Testing**:
- Manual testing (no automated tests yet)
- Postman (API testing)

**Deployment**:
- AWS CLI (manual deployments)
- ZIP file uploads to Lambda

### 4.3 Data Landscape

**Document Type**: Data Architecture  
**Audience**: Data Architects, Developers  
**Purpose**: Document data structures and flows

#### Data Entities

**Core Entities**:
```
User
  ├── user_id (PK)
  ├── email (GSI)
  ├── password_hash
  ├── first_name, last_name
  ├── role (user|admin|super_user)
  ├── subscription_tier
  ├── storage_used, storage_limit
  └── video_count, video_limit

Video
  ├── video_id (PK)
  ├── filename
  ├── title
  ├── tags[]
  ├── owner (user email)
  ├── visibility (public|private)
  ├── video_type (local|youtube|rumble|facebook)
  ├── external_url
  └── upload_date

Article
  ├── article_id (PK)
  ├── title
  ├── content (HTML)
  ├── author, author_email
  ├── category
  ├── scripture_references[]
  ├── tags[]
  ├── visibility (public|private)
  ├── featured_image
  ├── reading_time
  └── view_count

DownloadJob
  ├── job_id (PK)
  ├── url
  ├── filename
  ├── status (pending|processing|completed|failed)
  ├── progress
  └── error_message
```

#### Data Flows

**Video Upload Flow**:
```
User → Admin API (presigned URL) → S3 (direct upload) → 
S3 Event → Thumbnail Generator → S3 (thumbnails) → 
Tag API (metadata) → DynamoDB
```

**Video Download Flow**:
```
User → Router API (quota check) → DynamoDB (users) →
Router → Downloader Lambda (yt-dlp) → S3 (video) →
Downloader → Thumbnail Generator (FFmpeg) → S3 (thumbnails) →
Downloader → Tag API (metadata) → DynamoDB
```

**Article Creation Flow**:
```
User → Articles API (create) → DynamoDB (articles) →
Articles API → Bible API (verse lookup) → Articles API →
Articles API → Users Table (author name) → DynamoDB
```

**Subscription Flow**:
```
User → PayPal Billing API → PayPal API (create subscription) →
PayPal → Webhook → PayPal Billing API → DynamoDB (users) →
Router API (quota enforcement) → Allow/Deny upload
```

### 4.4 Integration Landscape

**Document Type**: Integration Architecture  
**Audience**: Integration Architects, Developers  
**Purpose**: Document all system integrations

#### Internal Integrations

**Synchronous (REST APIs)**:
```
Frontend → API Gateway → Lambda Functions → DynamoDB/S3
- auth-api: User authentication
- admin-api: Admin operations
- tag-api: Video metadata
- articles-api: Article management
- paypal-billing-api: Subscription management
```

**Asynchronous (Events)**:
```
S3 Upload Event → Lambda (thumbnail-generator)
PayPal Webhook → Lambda (paypal-billing-api)
SNS Topic → Email (notifications)
```

**Service-to-Service**:
```
router → downloader (Lambda invocation)
admin-api → thumbnail-generator (Lambda invocation)
articles-api → users table (DynamoDB query)
```

#### External Integrations

**Bible API Integration**:
- **Protocol**: REST/HTTPS
- **Endpoint**: https://bible-api.com/{reference}
- **Authentication**: None (public API)
- **Rate Limit**: None documented
- **Fallback**: None (single point of failure)
- **Usage**: Article editor verse lookup

**PayPal Integration**:
- **Protocol**: REST/HTTPS + Webhooks
- **Endpoints**: 
  - https://api-m.sandbox.paypal.com (sandbox)
  - https://api-m.paypal.com (production)
- **Authentication**: OAuth 2.0 (client credentials)
- **Rate Limit**: 10,000 requests/day
- **Fallback**: Manual subscription management
- **Usage**: Subscription creation, cancellation, webhook events

**AWS Bedrock Integration**:
- **Protocol**: AWS SDK (boto3)
- **Model**: Claude Instant (anthropic.claude-instant-v1)
- **Authentication**: IAM role
- **Rate Limit**: 20 requests/minute
- **Fallback**: Disabled via environment variable
- **Usage**: URL content summarization (optional)

**YouTube API Integration**:
- **Protocol**: REST/HTTPS
- **Endpoint**: https://www.youtube.com/oembed
- **Authentication**: None (public API)
- **Rate Limit**: None for oembed
- **Fallback**: Default thumbnail
- **Usage**: External video thumbnail extraction


---

## 5. OUTLINES (Solution Architecture)

### 5.1 Video Processing Solution Architecture

**Document Type**: Solution Architecture Document  
**Audience**: Development Teams, Technical Architects  
**Purpose**: Define architecture for video download and processing system

#### Business Requirements

**Functional Requirements**:
- Download videos from YouTube, Rumble, Facebook
- Support videos up to 4 hours in length
- Generate 3 thumbnails per video (10%, 50%, 90%)
- Store videos in S3 with CloudFront delivery
- Track download progress and status
- Enforce storage quotas per user

**Non-Functional Requirements**:
- Process videos within 15 minutes (Lambda) or route to Fargate
- 99.5% success rate for downloads
- Support concurrent downloads (up to 100)
- Cost per video: <$0.10

#### Solution Components

**Component 1: Router Lambda**
- **Purpose**: Orchestrate download jobs and enforce quotas
- **Technology**: Python 3.9, 256 MB, 30 sec timeout
- **Inputs**: URL, owner email, title, tags, visibility
- **Outputs**: Job ID, status
- **Logic**:
  1. Validate user quota (storage + video count)
  2. Create job entry in DynamoDB
  3. Send SNS notification (job started)
  4. Invoke downloader Lambda asynchronously
  5. Return job ID to user

**Component 2: Downloader Lambda**
- **Purpose**: Download video using yt-dlp and upload to S3
- **Technology**: Python 3.9, 3008 MB, 900 sec timeout
- **Layers**: yt-dlp-layer, ffmpeg-layer
- **Inputs**: Job ID, URL, filename, metadata
- **Outputs**: S3 video file, thumbnails, metadata
- **Logic**:
  1. Update job status: processing
  2. Download video to /tmp using yt-dlp
  3. Upload video to S3 (videos/)
  4. Generate 3 thumbnails with FFmpeg
  5. Upload thumbnails to S3 (thumbnails/)
  6. Save metadata to DynamoDB
  7. Update job status: completed
  8. Send SNS notification (success/failure)

**Component 3: Thumbnail Generator Lambda**
- **Purpose**: Generate thumbnails for uploaded videos
- **Technology**: Python 3.9, 1024 MB, 300 sec timeout
- **Trigger**: S3 event (video upload)
- **Layers**: ffmpeg-layer
- **Logic**:
  1. Download video from S3 to /tmp
  2. Get video duration with ffprobe
  3. Extract frames at 10%, 50%, 90%
  4. Upload thumbnails to S3
  5. Clean up /tmp

**Component 4: TAG API**
- **Purpose**: Store and retrieve video metadata
- **Technology**: Python 3.9, 512 MB, 60 sec timeout
- **Database**: DynamoDB (video-metadata table)
- **Endpoints**:
  - POST /tags?action=add_video (create metadata)
  - GET /tags?action=list (list videos with pagination)
  - PUT /tags/{video_id} (update metadata)

#### Data Flow Diagram

```
User Request
    │
    ▼
Router Lambda
    ├─→ Check Quota (DynamoDB users table)
    ├─→ Create Job (DynamoDB download-jobs table)
    ├─→ Send Notification (SNS)
    └─→ Invoke Downloader Lambda
            │
            ▼
        Downloader Lambda
            ├─→ Download Video (yt-dlp)
            ├─→ Upload to S3 (videos/)
            ├─→ Generate Thumbnails (FFmpeg)
            ├─→ Upload Thumbnails (S3 thumbnails/)
            ├─→ Save Metadata (DynamoDB)
            └─→ Send Notification (SNS)
                    │
                    ▼
                CloudFront CDN
                    │
                    ▼
                User Playback
```

#### Error Handling

**Timeout Handling**:
- Lambda timeout (15 min): Route to Fargate (future)
- Network timeout: Retry 3 times with exponential backoff
- S3 upload failure: Retry with multipart upload

**Failure Scenarios**:
- Invalid URL: Return 400 error, update job status: failed
- Quota exceeded: Return 403 error, don't create job
- Download failure: Update job status: failed, send SNS notification
- Thumbnail generation failure: Log error, continue (thumbnails optional)

#### Performance Optimization

**Lambda Optimization**:
- Memory: 3008 MB (maximum for video processing)
- Timeout: 900 seconds (15 minutes)
- /tmp storage: 512 MB (ephemeral storage)
- Concurrent executions: 100 (reserved concurrency)

**S3 Optimization**:
- Multipart upload for files >100 MB
- Transfer acceleration for faster uploads
- Lifecycle policy: Archive to Glacier after 1 year

**Cost Optimization**:
- Use best format selection (avoid 4K unless needed)
- Compress thumbnails (JPEG quality 85)
- Delete /tmp files after processing
- Use on-demand DynamoDB (no provisioned capacity)

### 5.2 Article Publishing Solution Architecture

**Document Type**: Solution Architecture Document  
**Audience**: Development Teams, Technical Architects  
**Purpose**: Define architecture for article publishing with Bible integration

#### Business Requirements

**Functional Requirements**:
- Rich text editor with formatting (bold, italic, headers, lists)
- Bible verse search and insertion (KJV, ASV, YLT)
- Article templates (Sermon, Political Commentary, Bible Study)
- Category management (Sermons, Politics, Devotionals, etc.)
- Public/private visibility control
- Featured image upload
- Social media sharing

**Non-Functional Requirements**:
- Article creation time: <5 seconds
- Bible verse lookup: <2 seconds
- Support 10,000+ articles
- Full-text search capability
- Mobile-responsive editor

#### Solution Components

**Component 1: Articles API Lambda**
- **Purpose**: CRUD operations for articles
- **Technology**: Python 3.9, 512 MB, 60 sec timeout
- **Database**: DynamoDB (articles table)
- **External APIs**: Bible API (bible-api.com)
- **Endpoints**:
  - POST /articles?action=create
  - GET /articles?action=list
  - GET /articles?action=get&article_id={id}
  - PUT /articles?action=update
  - DELETE /articles?action=delete
  - GET /articles?action=bible_verse&reference={ref}
  - GET /articles?action=search&q={query}

**Component 2: Rich Text Editor (Quill.js)**
- **Technology**: JavaScript, Quill.js library
- **Features**:
  - Toolbar: Headers, bold, italic, underline, lists, links, images
  - Bible verse lookup modal
  - Template selection dropdown
  - Auto-save to localStorage (draft)
  - Preview mode
  - Markdown toggle

**Component 3: Bible Integration**
- **External API**: bible-api.com
- **Supported Translations**: KJV, ASV (1901), YLT (NT only)
- **Search Format**: "John 3:16", "1 John 1:9", "Romans 8:28"
- **Fallback**: KJV if translation not available
- **Caching**: None (real-time lookup)

**Component 4: Featured Image Upload**
- **Storage**: S3 (images/ folder)
- **Upload Method**: Presigned URL from Admin API
- **Image Processing**: Client-side compression (JavaScript)
- **Max Size**: 5 MB
- **Formats**: JPEG, PNG, WebP

#### Data Model

**Article Entity**:
```json
{
  "article_id": "uuid",
  "title": "string",
  "content": "html",
  "author": "string (display name)",
  "author_email": "string",
  "category": "enum",
  "template_used": "string",
  "scripture_references": ["array"],
  "tags": ["array"],
  "visibility": "public|private",
  "featured_image": "url",
  "reading_time": "number (minutes)",
  "view_count": "number",
  "likes_count": "number",
  "created_at": "iso8601",
  "updated_at": "iso8601"
}
```

#### Processing Logic

**Article Creation Flow**:
1. User fills form (title, content, category, tags, visibility)
2. User clicks "Publish"
3. Frontend validates required fields
4. Frontend sends POST to Articles API
5. Articles API extracts scripture references (regex)
6. Articles API calculates reading time (word count / 200)
7. Articles API gets author name from users table
8. Articles API saves to DynamoDB
9. Articles API returns article_id
10. Frontend redirects to article view

**Bible Verse Lookup Flow**:
1. User enters reference (e.g., "John 3:16")
2. User selects translation (KJV, ASV, YLT)
3. Frontend sends GET to Articles API
4. Articles API formats reference (john3:16)
5. Articles API calls Bible API
6. Articles API cleans verse text (remove line breaks)
7. Articles API returns formatted verse
8. Frontend displays in modal
9. User clicks "Insert"
10. Frontend inserts as blockquote in editor

#### Search Implementation

**Current**: Basic DynamoDB scan with filtering
**Future**: OpenSearch with full-text indexing

**Search Logic**:
1. User enters search query
2. Frontend sends GET to Articles API
3. Articles API scans articles table
4. Articles API filters by:
   - Title contains query (case-insensitive)
   - Content contains query
   - Author contains query
   - Tags contain query
5. Articles API calculates relevance score
6. Articles API sorts by relevance + date
7. Articles API returns results
8. Frontend displays with highlighting

### 5.3 Subscription Billing Solution Architecture

**Document Type**: Solution Architecture Document  
**Audience**: Development Teams, Technical Architects  
**Purpose**: Define architecture for PayPal subscription system

#### Business Requirements

**Functional Requirements**:
- 4 subscription tiers (Free, Premium, Pro, Enterprise)
- PayPal payment processing
- Automatic quota enforcement
- Subscription upgrade/downgrade
- Cancellation with grace period
- Usage tracking (storage + video count)

**Non-Functional Requirements**:
- Payment processing: <10 seconds
- Quota check: <100ms
- 99.9% billing accuracy
- PCI-DSS compliant (PayPal handles)

#### Solution Components

**Component 1: PayPal Billing API Lambda**
- **Purpose**: Manage subscriptions and quotas
- **Technology**: Python 3.9, 256 MB, 30 sec timeout
- **External API**: PayPal Subscriptions API
- **Endpoints**:
  - POST /paypal?action=create_subscription
  - POST /paypal?action=cancel_subscription
  - GET /paypal?action=get_subscription_status
  - POST /paypal?action=webhook (PayPal events)

**Component 2: Router Quota Enforcement**
- **Purpose**: Check user quota before allowing uploads
- **Technology**: Integrated in router Lambda
- **Logic**:
  1. Get user from DynamoDB (users table)
  2. Check storage_used vs storage_limit
  3. Check video_count vs video_limit
  4. If admin/super_user: Allow (unlimited)
  5. If within limits: Allow
  6. If exceeded: Deny with upgrade message

**Component 3: PayPal Webhook Handler**
- **Purpose**: Process PayPal subscription events
- **Events Handled**:
  - BILLING.SUBSCRIPTION.CREATED
  - BILLING.SUBSCRIPTION.ACTIVATED
  - BILLING.SUBSCRIPTION.CANCELLED
  - BILLING.SUBSCRIPTION.EXPIRED
- **Logic**:
  1. Verify PayPal signature
  2. Parse event payload
  3. Update user record in DynamoDB
  4. Send confirmation email (SNS)

**Component 4: Automated Downgrade Service**
- **Purpose**: Downgrade expired subscriptions
- **Trigger**: CloudWatch Events (daily at midnight UTC)
- **Logic**:
  1. Scan users table for expired subscriptions
  2. Check next_billing_date < today
  3. Downgrade to free tier
  4. Update storage_limit and video_limit
  5. Send notification email

#### Subscription Tiers

```
Tier        | Price    | Storage | Videos | Features
------------|----------|---------|--------|----------
Free        | $0       | 2GB     | 50     | Basic
Premium     | $9.99    | 25GB    | 500    | Priority
Pro         | $24.99   | 100GB   | 2000   | Analytics
Enterprise  | $99.99   | ∞       | ∞      | White-label
```

#### Payment Flow

```
User Clicks "Upgrade"
    │
    ▼
PayPal Billing API
    ├─→ Create PayPal Subscription
    ├─→ Return Approval URL
    └─→ Redirect User to PayPal
            │
            ▼
        User Approves Payment
            │
            ▼
        PayPal Webhook
            ├─→ SUBSCRIPTION.ACTIVATED event
            ├─→ PayPal Billing API
            ├─→ Update User Record (DynamoDB)
            ├─→ Increase Limits
            └─→ Send Confirmation Email
                    │
                    ▼
                User Can Upload More
```

#### Quota Enforcement Logic

```python
def check_storage_quota(user_email):
    user = get_user(user_email)
    
    # Admin/Super User: Unlimited
    if user['role'] in ['admin', 'super_user']:
        return {'allowed': True}
    
    # Check video count
    if user['video_count'] >= user['video_limit']:
        return {
            'allowed': False,
            'message': 'Video limit reached. Upgrade to upload more.'
        }
    
    # Check storage (90% threshold)
    if user['storage_used'] >= (user['storage_limit'] * 0.9):
        return {
            'allowed': False,
            'message': 'Storage limit nearly reached. Upgrade for more space.'
        }
    
    return {'allowed': True}
```

---

## 6. DESIGNS (Technical Specifications)

### 6.1 Database Design

**Document Type**: Database Schema Specification  
**Audience**: Database Administrators, Developers  
**Purpose**: Define detailed database structure

#### DynamoDB Table: users

**Primary Key**: user_id (String)  
**Global Secondary Index**: email-index (email)  
**Billing Mode**: On-Demand

**Attributes**:
```
user_id: String (UUID) - Primary Key
email: String (unique, indexed)
password_hash: String (bcrypt, cost 12)
first_name: String
last_name: String
role: String (user|admin|super_user)
active: Boolean (default: true)
subscription_tier: String (free|premium|pro|enterprise)
subscription_status: String (active|pending|cancelled|expired)
subscription_id: String (PayPal subscription ID)
payment_provider: String (paypal|stripe)
billing_cycle: String (monthly|annual)
next_billing_date: String (ISO 8601)
storage_used: Number (bytes)
storage_limit: Number (bytes)
video_count: Number
video_limit: Number
created_at: String (ISO 8601)
updated_at: String (ISO 8601)
```

**Access Patterns**:
1. Get user by user_id (primary key)
2. Get user by email (GSI: email-index)
3. List all users (scan)
4. Update user attributes (update_item)
5. Delete user (delete_item)

#### DynamoDB Table: video-metadata

**Primary Key**: video_id (String)  
**Billing Mode**: On-Demand

**Attributes**:
```
video_id: String (filename) - Primary Key
filename: String
title: String
tags: List<String>
owner: String (user email)
visibility: String (public|private)
video_type: String (local|youtube|rumble|facebook|external)
external_url: String (optional)
s3_key: String (videos/filename.mp4)
url: String (original source URL)
upload_date: String (ISO 8601)
created_at: String (ISO 8601)
updated_at: String (ISO 8601)
```

**Access Patterns**:
1. Get video by video_id (primary key)
2. List all videos (scan with pagination)
3. Filter videos by tag (scan with filter)
4. Filter videos by owner (scan with filter)
5. Filter videos by visibility (scan with filter)

#### DynamoDB Table: articles

**Primary Key**: article_id (String)  
**Billing Mode**: On-Demand

**Attributes**:
```
article_id: String (UUID) - Primary Key
title: String
content: String (HTML)
author: String (display name)
author_email: String
category: String (sermon|politics|devotional|apologetics|ministry|bible_study|general)
template_used: String (sermon|political|service_notes|bible_study|custom)
scripture_references: List<String>
tags: List<String>
visibility: String (public|private)
featured_image: String (URL)
reading_time: Number (minutes)
view_count: Number
likes_count: Number
created_at: String (ISO 8601)
updated_at: String (ISO 8601)
```

**Access Patterns**:
1. Get article by article_id (primary key)
2. List all articles (scan with pagination)
3. Filter articles by category (scan with filter)
4. Filter articles by author (scan with filter)
5. Search articles by keyword (scan with filter)

#### DynamoDB Table: download-jobs

**Primary Key**: job_id (String)  
**Billing Mode**: On-Demand

**Attributes**:
```
job_id: String (UUID) - Primary Key
url: String
filename: String
title: String
tags: List<String>
status: String (pending|processing|downloading|completed|failed)
progress: Number (0-100)
error_message: String (optional)
started_at: String (ISO 8601)
updated_at: String (ISO 8601)
completed_at: String (ISO 8601, optional)
```

**Access Patterns**:
1. Get job by job_id (primary key)
2. List recent jobs (scan with filter on started_at)
3. List active jobs (scan with filter on status)
4. Update job status (update_item)

### 6.2 API Design Specification

**Document Type**: API Reference Documentation  
**Audience**: Frontend Developers, API Consumers  
**Purpose**: Define API contracts and examples

#### Authentication API

**Base URL**: https://r6l0z3605f.execute-api.us-east-1.amazonaws.com/prod/auth

**POST /auth?action=register**
```
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}

Response (201):
{
  "message": "User registered successfully",
  "user_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**POST /auth?action=login**
```
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response (200):
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "role": "user"
  }
}
```

### 6.3 Security Design

**Document Type**: Security Architecture Specification  
**Audience**: Security Team, Developers  
**Purpose**: Define security controls and implementation

#### JWT Token Structure

**Header**:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**:
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "role": "user",
  "exp": 1704153600
}
```

**Signature**:
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key_from_secrets_manager
)
```

#### IAM Role Policies

**Lambda Execution Role**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:*:table/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::my-video-downloads-bucket/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
```

---

## 7. APPENDICES

### Appendix A: Glossary

**CSVLOD**: Considerations, Standards, Visions, Landscapes, Outlines, Designs - EA framework by Svyatoslav Kotusev

**5-Fold Ministry**: Biblical leadership roles (Ephesians 4:11) - Apostles, Prophets, Evangelists, Pastors, Teachers

**Serverless**: Cloud computing model where infrastructure is fully managed by cloud provider

**DynamoDB**: AWS NoSQL database service with automatic scaling

**Lambda**: AWS serverless compute service for running code without servers

**CloudFront**: AWS content delivery network (CDN) for global content distribution

**JWT**: JSON Web Token - standard for securely transmitting information between parties

**RBAC**: Role-Based Access Control - authorization model based on user roles

### Appendix B: References

1. Kotusev, S. (2018). "The Practice of Enterprise Architecture: A Modern Approach to Business and IT Alignment"
2. AWS Well-Architected Framework: https://aws.amazon.com/architecture/well-architected/
3. AWS Serverless Application Lens: https://docs.aws.amazon.com/wellarchitected/latest/serverless-applications-lens/
4. Project README: README.md
5. Technical Documentation: TECHNICAL_DOCUMENTATION.md
6. Progress Tracking: PROGRESS.md
7. Enterprise Analysis: ENTERPRISE_ARCHITECTURE_ANALYSIS.md

### Appendix C: Document Control

**Document Owner**: IT Director, Christian Conservatives Today  
**Review Cycle**: Quarterly  
**Last Updated**: January 2025  
**Next Review**: April 2025  
**Version**: 1.0  
**Status**: Approved

**Change Log**:
- v1.0 (Jan 2025): Initial CSVLOD framework documentation created

---

**END OF DOCUMENT**
