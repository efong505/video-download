# Shopping System - Architecture Requirements

**Created:** November 6, 2025  
**Purpose:** Mandatory architecture patterns that Shopping system MUST implement

---

## Overview

The Shopping system must follow the same enterprise-grade architecture patterns being implemented across the platform. These are **non-negotiable** for production readiness.

---

## 1. SQS Message Queues (Week 1 - REQUIRED)

### Queues to Create:
- `order-processing-queue` + `order-processing-dlq`
- `payment-processing-queue` + `payment-processing-dlq`
- `email-notification-queue` + `email-notification-dlq`
- `inventory-update-queue` + `inventory-update-dlq`

### Implementation:
- **NO direct Lambda invocations** - all async operations use SQS
- Configure visibility timeout: 5 minutes (payment), 1 minute (email)
- Max retries: 3 before DLQ
- Message retention: 4 days

### Benefits:
- Automatic retries on failure
- No Lambda timeout issues
- Fault tolerance
- Better error tracking

### Cost: +$2/month

---

## 2. ElastiCache Redis (Week 2 - REQUIRED)

### What to Cache:
- **Product catalog** - 80% of reads (1 hour TTL)
- **Cart data** - Reduce DynamoDB by 90% (30 min TTL)
- **User sessions** - Fast authentication (24 hour TTL)
- **Popular queries** - Search results, filters (15 min TTL)

### Configuration:
- Instance: cache.t3.micro
- Engine: Redis 7.x
- VPC: Required
- Security group: Lambda access only

### Expected Results:
- 90% faster response times
- 40% cost reduction on DynamoDB
- 80%+ cache hit rate

### Cost: +$15/month (saves $50/month on DynamoDB)

---

## 3. Circuit Breakers (Week 3 - REQUIRED)

### Wrap These External APIs:
- PayPal payment API
- Stripe payment API
- AWS SES email sending
- Any third-party integrations

### Configuration:
- Failure threshold: 5 failures in 1 minute
- Timeout: 30 seconds
- Half-open retry: After 60 seconds

### Benefits:
- Prevent cascading failures
- Graceful degradation
- Better error messages to users

### Cost: $0 (code-level only)

---

## 4. Rate Limiting (Week 3 - REQUIRED)

### API Limits:
- **Payment APIs:** 10 requests/min per user
- **Cart APIs:** 100 requests/min per user
- **Admin APIs:** 50 requests/min per admin
- **Public APIs:** 1000 requests/min total

### Implementation:
- API Gateway usage plans
- DynamoDB rate-limits table
- Return 429 status when exceeded

### Benefits:
- Prevent abuse
- Protect payment processors
- Cost control

### Cost: $0

---

## 5. API Gateway Caching (Week 4 - REQUIRED)

### Cache These Endpoints:
- `GET /products` - 5 min TTL
- `GET /categories` - 1 hour TTL
- `GET /featured` - 15 min TTL
- `GET /bestsellers` - 15 min TTL
- `GET /products/{id}` - 10 min TTL

### Configuration:
- Cache size: 0.5 GB
- Cache key: Include query parameters
- Invalidate on: Product updates

### Benefits:
- Instant responses
- Reduced Lambda invocations
- Lower costs

### Cost: +$10/month (saves $30/month on Lambda)

---

## Updated Implementation Timeline

**Original:** 7 weeks  
**New:** 9 weeks (add 2 weeks for architecture)

| Week | Focus | Architecture Component |
|------|-------|------------------------|
| 1 | Database + SQS | SQS queues for all async ops |
| 2 | APIs + ElastiCache | Redis caching layer |
| 3 | Payment + Fault Tolerance | Circuit breakers + Rate limiting |
| 4 | Frontend + API Cache | API Gateway caching |
| 5 | Checkout + Orders | Use queues for order processing |
| 6 | Admin Interface | Admin rate limiting |
| 7 | Behavioral Tracking | Track via SQS queue |
| 8 | Marketing Automation | Email via SQS queue |
| 9 | Testing + Launch | Load testing, monitoring |

---

## Updated Cost Estimates

### AWS Costs (Monthly):

**Original Plan:**
- DynamoDB: $6
- Lambda: $4.50
- S3: $0.75
- SES: $1
- **Total: $12.25/month**

**With Architecture Improvements:**
- DynamoDB: $3 (50% reduction from caching)
- Lambda: $2.50 (44% reduction from caching)
- S3: $0.75 (unchanged)
- SES: $1 (unchanged)
- **SQS: +$2**
- **ElastiCache: +$15**
- **API Gateway Cache: +$10**
- **Total: $34.25/month**

**Net Change:** +$22/month  
**But:** Much faster, more reliable, production-ready

---

## Monitoring Requirements

### CloudWatch Dashboards:
- SQS queue depths (all 4 queues)
- DLQ message counts (alert if > 0)
- Cache hit rates (target >80%)
- Lambda error rates
- API Gateway 4xx/5xx rates
- Payment success rates

### Alarms:
- DLQ has messages (critical)
- Cache hit rate < 70% (warning)
- Payment API errors > 5% (critical)
- Rate limit breaches (info)

### Logs:
- All payment transactions
- All order creations
- All email sends
- All cache misses

---

## Deployment Scripts Required

Create in `Shopping/scripts/`:

1. **deploy-shopping-sqs.ps1** - Create all SQS queues
2. **deploy-shopping-cache.ps1** - Set up ElastiCache
3. **deploy-shopping-apis.ps1** - Deploy Lambda functions
4. **test-shopping-integration.ps1** - Test all components
5. **rollback-shopping.ps1** - Rollback deployment
6. **monitor-shopping.ps1** - Check health status

---

## Safe Deployment Pattern

### Phase 1: Infrastructure (Week 1-2)
1. Create SQS queues (no Lambda changes yet)
2. Deploy ElastiCache (no Lambda changes yet)
3. Test infrastructure independently

### Phase 2: Backend (Week 3-4)
1. Update one Lambda at a time to use SQS
2. Update one Lambda at a time to use cache
3. Test each Lambda after update
4. Monitor for 24 hours between updates

### Phase 3: Frontend (Week 5-6)
1. Deploy frontend with feature flags
2. Enable for 10% of users
3. Monitor for issues
4. Gradually increase to 100%

### Phase 4: Marketing (Week 7-8)
1. Deploy tracking system
2. Deploy marketing automation
3. Test email flows
4. Enable for all users

---

## Rollback Strategy

### If SQS Issues:
```powershell
.\rollback-shopping.ps1 -Component SQS
```
Reverts to direct Lambda invocation

### If Cache Issues:
```powershell
.\rollback-shopping.ps1 -Component Cache
```
Reverts to direct DynamoDB reads

### If Payment Issues:
```powershell
.\rollback-shopping.ps1 -Component Payment
```
Disables new payment flow, uses backup

---

## Success Criteria

Before launching Shopping system:

- [ ] All SQS queues created and tested
- [ ] ElastiCache deployed and cache hit rate >80%
- [ ] Circuit breakers tested with intentional failures
- [ ] Rate limiting tested and working
- [ ] API Gateway cache enabled and working
- [ ] All monitoring dashboards created
- [ ] All alarms configured
- [ ] Rollback scripts tested
- [ ] Load testing completed (100 concurrent users)
- [ ] Security audit passed

---

## Non-Negotiable Requirements

These are **REQUIRED** before Shopping system goes to production:

1. ✅ SQS queues for all async operations
2. ✅ ElastiCache for product/cart caching
3. ✅ Circuit breakers on external APIs
4. ✅ Rate limiting on all APIs
5. ✅ API Gateway caching on read endpoints
6. ✅ CloudWatch monitoring and alarms
7. ✅ Rollback scripts for all components
8. ✅ Load testing completed

**Do NOT skip these to save time. They are essential for production.**

---

## Questions?

Refer to main Architecture-Improvements documentation:
- `Architecture-Improvements/00-MASTER-PLAN.md`
- `Architecture-Improvements/01-SQS-IMPLEMENTATION.md`
- `Architecture-Improvements/02-ELASTICACHE-IMPLEMENTATION.md`
- `Architecture-Improvements/scripts/README.md`

Or ask in the main architecture implementation session.
