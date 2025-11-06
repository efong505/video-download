# Week 2: ElastiCache Redis Implementation

## Overview

Add Amazon ElastiCache (Redis) as a caching layer to:
- Reduce DynamoDB read costs by 80%
- Improve response times by 90% (2s → 200ms)
- Handle traffic spikes without throttling
- Reduce database load

**Time Required:** 12-16 hours
**Cost Impact:** +$15/month (saves $100/month on DynamoDB)
**Risk Level:** Medium (requires VPC configuration)

---

## Architecture Changes

### Current (Direct Database Access)
```
Lambda → DynamoDB (every request)
Cost: $0.25 per million reads
Latency: 10-50ms per request
```

### New (Cache Layer)
```
Lambda → ElastiCache (90% of requests)
       → DynamoDB (10% cache misses)
       
Cost: $0.25 per million reads (only 10% hit DB)
Latency: 1-2ms from cache
```

---

## Cache Strategy

### What to Cache
✅ **Articles** - Rarely change, frequently read
✅ **Video metadata** - Static after upload
✅ **User profiles** - Read on every request
✅ **Election data** - Updated weekly
✅ **Resources** - Rarely change

❌ **Don't Cache:**
- Download jobs (real-time status)
- Analytics events (write-heavy)
- Comments (frequently updated)

### Cache TTL (Time To Live)
- Articles: 1 hour (3600s)
- Videos: 30 minutes (1800s)
- User profiles: 15 minutes (900s)
- Election data: 24 hours (86400s)
- Resources: 2 hours (7200s)

---

## Step 1: Create VPC (If Not Exists)

ElastiCache requires VPC. Check if you have one:

```bash
aws ec2 describe-vpcs
```

If no VPC, create one:

### AWS Console Method:
1. Go to VPC Dashboard
2. Click "Create VPC"
3. **VPC settings:**
   - Name: cct-vpc
   - IPv4 CIDR: 10.0.0.0/16
4. Click "Create VPC"

### AWS CLI Method (Bash):
```bash
#!/bin/bash
# create-vpc.sh

# Create VPC
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=cct-vpc}]' \
    --query 'Vpc.VpcId' \
    --output text)

echo "Created VPC: $VPC_ID"

# Create subnets in different AZs
SUBNET1_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.1.0/24 \
    --availability-zone us-east-1a \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=cct-subnet-1a}]' \
    --query 'Subnet.SubnetId' \
    --output text)

SUBNET2_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.2.0/24 \
    --availability-zone us-east-1b \
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=cct-subnet-1b}]' \
    --query 'Subnet.SubnetId' \
    --output text)

echo "Created Subnets: $SUBNET1_ID, $SUBNET2_ID"

# Create Internet Gateway
IGW_ID=$(aws ec2 create-internet-gateway \
    --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=cct-igw}]' \
    --query 'InternetGateway.InternetGatewayId' \
    --output text)

# Attach to VPC
aws ec2 attach-internet-gateway \
    --vpc-id $VPC_ID \
    --internet-gateway-id $IGW_ID

echo "Created and attached Internet Gateway: $IGW_ID"

# Create route table
ROUTE_TABLE_ID=$(aws ec2 create-route-table \
    --vpc-id $VPC_ID \
    --tag-specifications 'ResourceType=route-table,Tags=[{Key=Name,Value=cct-route-table}]' \
    --query 'RouteTable.RouteTableId' \
    --output text)

# Add route to internet
aws ec2 create-route \
    --route-table-id $ROUTE_TABLE_ID \
    --destination-cidr-block 0.0.0.0/0 \
    --gateway-id $IGW_ID

# Associate subnets with route table
aws ec2 associate-route-table \
    --subnet-id $SUBNET1_ID \
    --route-table-id $ROUTE_TABLE_ID

aws ec2 associate-route-table \
    --subnet-id $SUBNET2_ID \
    --route-table-id $ROUTE_TABLE_ID

echo "✅ VPC setup complete!"
echo "VPC ID: $VPC_ID"
echo "Subnet 1: $SUBNET1_ID"
echo "Subnet 2: $SUBNET2_ID"
```

### PowerShell Method:
```powershell
# create-vpc.ps1

# Create VPC
$VpcId = (aws ec2 create-vpc `
    --cidr-block 10.0.0.0/16 `
    --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=cct-vpc}]' `
    --query 'Vpc.VpcId' `
    --output text)

Write-Host "Created VPC: $VpcId" -ForegroundColor Green

# Create subnets
$Subnet1Id = (aws ec2 create-subnet `
    --vpc-id $VpcId `
    --cidr-block 10.0.1.0/24 `
    --availability-zone us-east-1a `
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=cct-subnet-1a}]' `
    --query 'Subnet.SubnetId' `
    --output text)

$Subnet2Id = (aws ec2 create-subnet `
    --vpc-id $VpcId `
    --cidr-block 10.0.2.0/24 `
    --availability-zone us-east-1b `
    --tag-specifications 'ResourceType=subnet,Tags=[{Key=Name,Value=cct-subnet-1b}]' `
    --query 'Subnet.SubnetId' `
    --output text)

Write-Host "Created Subnets: $Subnet1Id, $Subnet2Id" -ForegroundColor Green

# Create Internet Gateway
$IgwId = (aws ec2 create-internet-gateway `
    --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=cct-igw}]' `
    --query 'InternetGateway.InternetGatewayId' `
    --output text)

aws ec2 attach-internet-gateway --vpc-id $VpcId --internet-gateway-id $IgwId

Write-Host "Created Internet Gateway: $IgwId" -ForegroundColor Green

Write-Host "✅ VPC setup complete!" -ForegroundColor Green
```

---

## Step 2: Create Security Group

### AWS Console Method:
1. Go to EC2 → Security Groups
2. Click "Create security group"
3. **Details:**
   - Name: elasticache-sg
   - Description: Security group for ElastiCache Redis
   - VPC: Select your VPC
4. **Inbound rules:**
   - Type: Custom TCP
   - Port: 6379
   - Source: Custom (your VPC CIDR: 10.0.0.0/16)
5. Click "Create security group"

### AWS CLI Method:
```bash
# Create security group
SG_ID=$(aws ec2 create-security-group \
    --group-name elasticache-sg \
    --description "Security group for ElastiCache Redis" \
    --vpc-id $VPC_ID \
    --query 'GroupId' \
    --output text)

# Add inbound rule for Redis (port 6379)
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 6379 \
    --cidr 10.0.0.0/16

echo "Security Group ID: $SG_ID"
```

---

## Step 3: Create Subnet Group

ElastiCache requires a subnet group with at least 2 subnets in different AZs.

### AWS Console Method:
1. Go to ElastiCache → Subnet Groups
2. Click "Create subnet group"
3. **Details:**
   - Name: cct-cache-subnet-group
   - Description: Subnet group for CCT cache
   - VPC: Select your VPC
4. **Subnets:**
   - Add both subnets (us-east-1a and us-east-1b)
5. Click "Create"

### AWS CLI Method:
```bash
aws elasticache create-cache-subnet-group \
    --cache-subnet-group-name cct-cache-subnet-group \
    --cache-subnet-group-description "Subnet group for CCT cache" \
    --subnet-ids $SUBNET1_ID $SUBNET2_ID
```

---

## Step 4: Create ElastiCache Redis Cluster

### AWS Console Method:
1. Go to ElastiCache → Redis clusters
2. Click "Create Redis cluster"
3. **Cluster settings:**
   - Cluster mode: Disabled
   - Name: cct-cache
   - Description: Cache for Christian Conservatives Today
4. **Location:**
   - AWS Cloud
   - Multi-AZ: Disabled (for cost savings)
5. **Cluster settings:**
   - Engine version: 7.0 (latest)
   - Port: 6379
   - Parameter group: default.redis7
   - Node type: cache.t3.micro (cheapest, $15/month)
   - Number of replicas: 0 (for cost savings)
6. **Subnet group:**
   - Select: cct-cache-subnet-group
7. **Security:**
   - Security groups: elasticache-sg
   - Encryption at rest: Disabled (optional)
   - Encryption in transit: Disabled (optional)
8. **Backup:**
   - Enable automatic backups: No (for cost savings)
9. Click "Create"

### AWS CLI Method (Bash):
```bash
#!/bin/bash
# create-elasticache.sh

aws elasticache create-cache-cluster \
    --cache-cluster-id cct-cache \
    --engine redis \
    --cache-node-type cache.t3.micro \
    --num-cache-nodes 1 \
    --cache-subnet-group-name cct-cache-subnet-group \
    --security-group-ids $SG_ID \
    --engine-version 7.0 \
    --port 6379 \
    --preferred-maintenance-window sun:05:00-sun:06:00

echo "✅ ElastiCache cluster creation initiated"
echo "This will take 5-10 minutes..."

# Wait for cluster to be available
aws elasticache wait cache-cluster-available --cache-cluster-id cct-cache

echo "✅ ElastiCache cluster is ready!"

# Get endpoint
REDIS_ENDPOINT=$(aws elasticache describe-cache-clusters \
    --cache-cluster-id cct-cache \
    --show-cache-node-info \
    --query 'CacheClusters[0].CacheNodes[0].Endpoint.Address' \
    --output text)

echo "Redis Endpoint: $REDIS_ENDPOINT:6379"
```

### PowerShell Method:
```powershell
# create-elasticache.ps1

aws elasticache create-cache-cluster `
    --cache-cluster-id cct-cache `
    --engine redis `
    --cache-node-type cache.t3.micro `
    --num-cache-nodes 1 `
    --cache-subnet-group-name cct-cache-subnet-group `
    --security-group-ids $SgId `
    --engine-version 7.0 `
    --port 6379 `
    --preferred-maintenance-window sun:05:00-sun:06:00

Write-Host "✅ ElastiCache cluster creation initiated" -ForegroundColor Green
Write-Host "This will take 5-10 minutes..." -ForegroundColor Yellow

# Wait for cluster
aws elasticache wait cache-cluster-available --cache-cluster-id cct-cache

Write-Host "✅ ElastiCache cluster is ready!" -ForegroundColor Green

# Get endpoint
$RedisEndpoint = (aws elasticache describe-cache-clusters `
    --cache-cluster-id cct-cache `
    --show-cache-node-info `
    --query 'CacheClusters[0].CacheNodes[0].Endpoint.Address' `
    --output text)

Write-Host "Redis Endpoint: $RedisEndpoint:6379" -ForegroundColor Cyan
```

---

## Step 5: Update Lambda VPC Configuration

Lambda must be in same VPC as ElastiCache to access it.

### AWS Console Method:
1. Go to Lambda → Functions → articles-api
2. Configuration → VPC
3. Click "Edit"
4. **VPC:** Select your VPC
5. **Subnets:** Select both subnets
6. **Security groups:** Select elasticache-sg
7. Click "Save"

### AWS CLI Method:
```bash
# Update Lambda VPC configuration
aws lambda update-function-configuration \
    --function-name articles-api \
    --vpc-config SubnetIds=$SUBNET1_ID,$SUBNET2_ID,SecurityGroupIds=$SG_ID
```

**Repeat for these Lambda functions:**
- articles-api
- video-list-api
- news-api
- resources-api
- contributors-api

---

## Step 6: Add Redis Python Library

Create Lambda layer with redis library:

```bash
# Create directory
mkdir python
cd python

# Install redis
pip install redis -t .

# Create layer package
cd ..
zip -r redis-layer.zip python

# Upload to Lambda
aws lambda publish-layer-version \
    --layer-name redis-layer \
    --description "Redis client for Python" \
    --zip-file fileb://redis-layer.zip \
    --compatible-runtimes python3.12

# Get layer ARN
LAYER_ARN=$(aws lambda list-layer-versions \
    --layer-name redis-layer \
    --query 'LayerVersions[0].LayerVersionArn' \
    --output text)

# Attach to Lambda functions
aws lambda update-function-configuration \
    --function-name articles-api \
    --layers $LAYER_ARN
```

---

## Step 7: Update Lambda Code

### cache_helper.py (Reusable Cache Module)

```python
import redis
import json
import os
from functools import wraps

# Redis connection
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2
)

def cache_get(key):
    """Get value from cache"""
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Cache get error: {e}")
        return None

def cache_set(key, value, ttl=3600):
    """Set value in cache with TTL"""
    try:
        redis_client.setex(key, ttl, json.dumps(value))
        return True
    except Exception as e:
        print(f"Cache set error: {e}")
        return False

def cache_delete(key):
    """Delete key from cache"""
    try:
        redis_client.delete(key)
        return True
    except Exception as e:
        print(f"Cache delete error: {e}")
        return False

def cache_decorator(key_prefix, ttl=3600):
    """Decorator for caching function results"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{args[0]}" if args else key_prefix
            
            # Try cache first
            cached = cache_get(cache_key)
            if cached:
                print(f"✅ Cache HIT: {cache_key}")
                return cached
            
            # Cache miss - call function
            print(f"❌ Cache MISS: {cache_key}")
            result = func(*args, **kwargs)
            
            # Store in cache
            cache_set(cache_key, result, ttl)
            
            return result
        return wrapper
    return decorator
```

### articles_api/index.py (Updated with Cache)

```python
import boto3
import json
from cache_helper import cache_get, cache_set, cache_delete, cache_decorator

dynamodb = boto3.resource('dynamodb')
articles_table = dynamodb.Table('articles')

@cache_decorator('article', ttl=3600)  # Cache for 1 hour
def get_article(article_id):
    """Get article with caching"""
    response = articles_table.get_item(Key={'article_id': article_id})
    return response.get('Item')

def list_articles():
    """List articles with caching"""
    cache_key = 'articles:list'
    
    # Try cache
    cached = cache_get(cache_key)
    if cached:
        return cached
    
    # Cache miss - query DynamoDB
    response = articles_table.scan()
    articles = response['Items']
    
    # Cache for 30 minutes
    cache_set(cache_key, articles, ttl=1800)
    
    return articles

def update_article(article_id, updates):
    """Update article and invalidate cache"""
    # Update in DynamoDB
    articles_table.update_item(
        Key={'article_id': article_id},
        UpdateExpression='SET #title = :title, #content = :content',
        ExpressionAttributeNames={
            '#title': 'title',
            '#content': 'content'
        },
        ExpressionAttributeValues={
            ':title': updates['title'],
            ':content': updates['content']
        }
    )
    
    # Invalidate cache
    cache_delete(f'article:{article_id}')
    cache_delete('articles:list')
    
    return {'success': True}

def lambda_handler(event, context):
    path = event.get('rawPath') or event.get('path')
    method = event.get('requestContext', {}).get('http', {}).get('method') or event.get('httpMethod')
    
    if path == '/articles' and method == 'GET':
        articles = list_articles()
        return {
            'statusCode': 200,
            'body': json.dumps(articles)
        }
    
    elif path.startswith('/articles/') and method == 'GET':
        article_id = path.split('/')[-1]
        article = get_article(article_id)
        return {
            'statusCode': 200,
            'body': json.dumps(article)
        }
    
    elif path.startswith('/articles/') and method == 'PUT':
        article_id = path.split('/')[-1]
        body = json.loads(event['body'])
        result = update_article(article_id, body)
        return {
            'statusCode': 200,
            'body': json.dumps(result)
        }
```

---

## Step 8: Add Environment Variables

```bash
# Get Redis endpoint
REDIS_ENDPOINT=$(aws elasticache describe-cache-clusters \
    --cache-cluster-id cct-cache \
    --show-cache-node-info \
    --query 'CacheClusters[0].CacheNodes[0].Endpoint.Address' \
    --output text)

# Update Lambda environment variables
aws lambda update-function-configuration \
    --function-name articles-api \
    --environment "Variables={
        REDIS_HOST=$REDIS_ENDPOINT,
        REDIS_PORT=6379
    }"
```

---

## Testing

### Test 1: Direct Redis Connection

```python
# test_redis.py
import redis

redis_client = redis.Redis(
    host='your-endpoint.cache.amazonaws.com',
    port=6379,
    decode_responses=True
)

# Test set
redis_client.set('test_key', 'Hello Redis!')

# Test get
value = redis_client.get('test_key')
print(f"Value: {value}")

# Test TTL
redis_client.setex('temp_key', 10, 'Expires in 10 seconds')
print(f"TTL: {redis_client.ttl('temp_key')} seconds")
```

### Test 2: Cache Hit Rate

```bash
# Monitor cache statistics
aws cloudwatch get-metric-statistics \
    --namespace AWS/ElastiCache \
    --metric-name CacheHits \
    --dimensions Name=CacheClusterId,Value=cct-cache \
    --start-time 2025-01-01T00:00:00Z \
    --end-time 2025-01-02T00:00:00Z \
    --period 3600 \
    --statistics Sum
```

---

## Monitoring

### Key Metrics
- **CacheHits** - Successful cache retrievals
- **CacheMisses** - Cache misses (DB queries)
- **CacheHitRate** - Percentage of hits (target: >80%)
- **CPUUtilization** - CPU usage (target: <75%)
- **NetworkBytesIn/Out** - Network traffic
- **Evictions** - Items removed due to memory pressure

### CloudWatch Dashboard

Create dashboard to monitor cache performance:

```bash
aws cloudwatch put-dashboard \
    --dashboard-name CCT-Cache-Dashboard \
    --dashboard-body file://dashboard.json
```

---

## Cost Analysis

### Monthly Costs
- **cache.t3.micro:** $12.96/month
- **Data transfer:** ~$2/month
- **Total:** ~$15/month

### Savings
- **DynamoDB reads:** -$100/month (80% reduction)
- **Lambda duration:** -$20/month (faster execution)
- **Net savings:** $105/month

**ROI:** 7x return on investment

---

## Rollback Plan

```bash
# 1. Remove Lambda VPC configuration
aws lambda update-function-configuration \
    --function-name articles-api \
    --vpc-config SubnetIds=[],SecurityGroupIds=[]

# 2. Revert Lambda code (remove cache logic)
# Deploy previous version

# 3. Delete ElastiCache cluster
aws elasticache delete-cache-cluster \
    --cache-cluster-id cct-cache

# 4. Delete subnet group
aws elasticache delete-cache-subnet-group \
    --cache-subnet-group-name cct-cache-subnet-group
```

---

## Success Criteria

✅ ElastiCache cluster created and available
✅ Lambda functions in VPC with cache access
✅ Redis library added to Lambda layer
✅ Cache helper module implemented
✅ Cache hit rate >80% after 24 hours
✅ Response times <200ms for cached content
✅ DynamoDB read costs reduced by 80%

**Next:** Week 3 - Circuit Breakers & Rate Limiting
