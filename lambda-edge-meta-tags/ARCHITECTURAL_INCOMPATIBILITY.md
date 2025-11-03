# Lambda@Edge Architectural Incompatibility

## Status: ABANDONED - Architecturally Incompatible

## Problem Statement
Attempted to use Lambda@Edge to serve dynamic Open Graph meta tags for social media sharing by fetching article data from DynamoDB and generating HTML with article-specific og:image, og:title, and og:description tags.

## Why It Failed
**Lambda@Edge cannot access DynamoDB** because:
- Lambda@Edge runs at CloudFront edge locations (200+ worldwide)
- DynamoDB tables exist in specific AWS regions (our tables are in us-east-1)
- Edge locations cannot make cross-region API calls to DynamoDB
- Results in `ResourceNotFoundException` when attempting `dynamodb.Table().get_item()`

## Evidence
- Deployed Lambda@Edge version 5 to us-east-1
- Associated with CloudFront distribution E3N00R2D2NE9C5
- CloudWatch logs confirmed function executed and detected crawlers
- All DynamoDB GetItem operations failed with ResourceNotFoundException
- Verified article exists in DynamoDB and IAM permissions are correct
- Confirmed table name is 'news-table' not 'News'

## What Was Attempted
1. Initial deployment with environment variables (Lambda@Edge doesn't support them)
2. Hardcoded table names in code
3. Fixed table name from 'News' to 'news-table'
4. Verified IAM role has AmazonDynamoDBFullAccess
5. Confirmed article 87d89265-d111-46d3-a03f-cfe5f0f9e68a exists in news-table

## Architectural Limitation
```
Request Flow (DOESN'T WORK):
User/Crawler → CloudFront Edge (Tokyo) → Lambda@Edge (Tokyo) → DynamoDB (us-east-1) ❌
                                                                   Cannot access!
```

Lambda@Edge is designed for:
- URL rewriting
- Header manipulation
- A/B testing
- Simple request/response modifications
- **NOT for database access**

## Alternative Solution: Server-Side Rendering with Lambda Function URL

### How It Would Work
```
S3 Origin (Current - Static Files):
User → CloudFront → S3 Bucket → Static HTML file
Cost: $0.023 per 10,000 requests

Lambda Origin (Server-Side Rendering):
User → CloudFront → Lambda Function URL → DynamoDB → Generated HTML
Cost: $0.20 per 1,000 requests (after free tier)
```

### Implementation Approach
1. Create Lambda function with Function URL (not Lambda@Edge)
2. Lambda can access DynamoDB (same region)
3. Configure CloudFront with two origins:
   - **S3 origin**: Default for all static files
   - **Lambda origin**: Only for article.html and news-article.html paths
4. Lambda generates HTML with dynamic meta tags
5. CloudFront caches Lambda responses

### Cost Comparison
| Solution | Cost per 1,000 article views | Free Tier |
|----------|------------------------------|-----------|
| S3 Origin (Static) | $0.023 | 20,000 requests/month |
| Lambda Origin (SSR) | $0.20 | 1M requests/month |

### Toggle Between Origins
Would require CloudFront distribution configuration changes:
- Enable: Add Lambda Function URL as origin, create cache behavior for article paths
- Disable: Remove cache behavior, revert to S3 origin only

## Current Status
- Lambda@Edge disabled using `toggle-lambda-edge.ps1`
- CloudFront serving static HTML from S3 (default behavior)
- Static Open Graph meta tags in place (fallback)
- Server-side rendering NOT implemented (only discussed)

## Recommendation
**Keep static meta tags** unless article-specific social sharing images are critical business requirement. The cost and complexity of server-side rendering may not justify the benefit.

## Files in This Directory
- `index.py`: Lambda@Edge function code (non-functional due to DynamoDB limitation)
- `requirements.txt`: boto3 dependency
- `README.md`: Original implementation documentation
- `LAMBDA_EDGE_DYNAMIC_META_TAGS.md`: Detailed documentation (now outdated)
- `toggle-lambda-edge.ps1`: Script to enable/disable Lambda@Edge association
- `ARCHITECTURAL_INCOMPATIBILITY.md`: This file

## Lessons Learned
- Lambda@Edge is for edge computing, not backend data access
- Always verify service limitations before implementation
- Static meta tags are sufficient for most social sharing use cases
- Server-side rendering adds significant complexity and cost
