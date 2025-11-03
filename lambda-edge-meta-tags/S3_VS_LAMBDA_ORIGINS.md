# S3 Origin vs Lambda Origin

## What is a CloudFront Origin?

An **origin** is where CloudFront fetches content when it's not in the cache. CloudFront can have multiple origins and route requests to different origins based on URL paths.

---

## S3 Origin (Current Setup)

### How It Works
```
1. User requests: https://christianconservativestoday.com/article.html?id=123
2. CloudFront checks cache → MISS
3. CloudFront fetches from S3: s3://techcross-videos/article.html
4. S3 returns static HTML file (same file for all article IDs)
5. CloudFront caches and serves to user
6. User's browser loads HTML and JavaScript
7. JavaScript fetches article data from DynamoDB
8. JavaScript renders article content
```

### Characteristics
- **Static files**: HTML, CSS, JS, images stored in S3 bucket
- **Same file for everyone**: article.html is identical for all users
- **Client-side rendering**: Browser JavaScript fetches and displays data
- **Fast**: S3 is optimized for static file delivery
- **Cheap**: $0.023 per 10,000 requests
- **No computation**: Just file retrieval

### Social Media Crawler Problem
```
Facebook crawler requests: article.html?id=123
↓
Gets static HTML with generic meta tags:
<meta property="og:image" content="techcrosslogo.jpg">
<meta property="og:title" content="Christian Conservatives Today">
↓
Facebook shows generic image/title (not article-specific)
```

---

## Lambda Origin (Server-Side Rendering)

### How It Would Work
```
1. User requests: https://christianconservativestoday.com/article.html?id=123
2. CloudFront checks cache → MISS
3. CloudFront calls Lambda Function URL
4. Lambda function executes:
   a. Parses URL parameter (id=123)
   b. Queries DynamoDB for article 123
   c. Generates HTML with article-specific meta tags
   d. Returns custom HTML
5. CloudFront caches Lambda response
6. CloudFront serves to user
```

### Characteristics
- **Dynamic generation**: HTML created on-demand for each article
- **Different HTML per article**: article.html?id=123 ≠ article.html?id=456
- **Server-side rendering**: Lambda generates complete HTML before sending
- **Computation required**: Lambda executes Python code, queries database
- **More expensive**: $0.20 per 1,000 requests (Lambda invocation + duration)
- **Database access**: Lambda can query DynamoDB in same region

### Social Media Crawler Solution
```
Facebook crawler requests: article.html?id=123
↓
Lambda generates HTML with article-specific meta tags:
<meta property="og:image" content="article-123-featured-image.jpg">
<meta property="og:title" content="BREAKING: Trump Reinstates Nigeria...">
↓
Facebook shows article-specific image/title ✓
```

---

## Side-by-Side Comparison

| Feature | S3 Origin | Lambda Origin |
|---------|-----------|---------------|
| **Content Type** | Static files | Dynamically generated |
| **HTML per Request** | Same file | Custom HTML per article |
| **Database Access** | No (browser JS does it) | Yes (Lambda queries) |
| **Computation** | None | Python code execution |
| **Cost (1,000 views)** | $0.023 | $0.20 |
| **Speed** | Very fast | Fast (adds ~50-200ms) |
| **Caching** | Simple (file-based) | Complex (per URL+params) |
| **Social Media Meta** | Generic/static | Article-specific |
| **Setup Complexity** | Simple | Moderate |

---

## Hybrid Approach (Best of Both Worlds)

CloudFront can use **multiple origins** with **path-based routing**:

```
CloudFront Distribution:
├── Default Origin: S3 (for most files)
│   ├── index.html
│   ├── videos.html
│   ├── assets/css/*
│   ├── assets/js/*
│   └── images/*
│
└── Custom Origin: Lambda Function URL (only for articles)
    ├── /article.html
    └── /news-article.html
```

### Configuration Example
```
Cache Behavior #1 (Priority 0):
  Path Pattern: /article.html*
  Origin: Lambda Function URL
  Cache Policy: Cache based on query string (id parameter)

Cache Behavior #2 (Priority 1):
  Path Pattern: /news-article.html*
  Origin: Lambda Function URL
  Cache Policy: Cache based on query string (id parameter)

Default Cache Behavior:
  Path Pattern: *
  Origin: S3 Bucket
  Cache Policy: Standard S3 caching
```

### Request Flow
```
Request: /index.html
→ CloudFront → S3 Origin → Static file

Request: /article.html?id=123
→ CloudFront → Lambda Origin → DynamoDB → Generated HTML

Request: /assets/css/style.css
→ CloudFront → S3 Origin → Static file
```

---

## Why Lambda@Edge Doesn't Work

Lambda@Edge is **NOT an origin** - it's a function that runs **at the edge** before/after origin requests:

```
WRONG (Lambda@Edge):
User → CloudFront Edge (Tokyo) → Lambda@Edge → DynamoDB (us-east-1) ❌
                                                  Cannot access!

RIGHT (Lambda Function URL as Origin):
User → CloudFront Edge (Tokyo) → Lambda (us-east-1) → DynamoDB (us-east-1) ✓
                                  Same region!
```

Lambda@Edge runs at 200+ edge locations worldwide and cannot access regional services like DynamoDB.

Lambda Function URL runs in a specific region (us-east-1) and can access DynamoDB in the same region.

---

## Cost Analysis for Your Use Case

Assuming 50 article shares per month:

### S3 Origin (Current)
- 50 crawler requests: $0.023 per 10,000 = **$0.0001**
- 50 user requests: $0.023 per 10,000 = **$0.0001**
- **Total: $0.0002/month**
- **Issue**: Generic social media previews

### Lambda Origin (Server-Side Rendering)
- 50 crawler requests: $0.20 per 1,000 = **$0.01**
- 50 user requests: $0.20 per 1,000 = **$0.01**
- **Total: $0.02/month**
- **Benefit**: Article-specific social media previews

### Cost Increase
- **100x more expensive** ($0.02 vs $0.0002)
- But still only **$0.02/month** in absolute terms
- Free tier covers 1M Lambda requests/month

---

## Decision Framework

### Use S3 Origin (Current) If:
- ✓ Generic social media previews are acceptable
- ✓ Cost optimization is priority
- ✓ Simple architecture preferred
- ✓ Client-side rendering is sufficient

### Use Lambda Origin If:
- ✓ Article-specific social previews are critical
- ✓ SEO with dynamic meta tags is important
- ✓ Willing to manage more complex infrastructure
- ✓ Budget allows for higher costs at scale

---

## Current Status

**Active**: S3 Origin (static files)  
**Inactive**: Lambda@Edge (disabled, architecturally incompatible)  
**Not Implemented**: Lambda Function URL as origin (discussed but not built)

Your site currently uses S3 origin for all files with static Open Graph meta tags as fallback.
