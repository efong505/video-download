# URL Analysis API Implementation Tutorial

## Overview

This tutorial provides two approaches for implementing URL analysis with AI-powered summarization:
- **Option 1 (Recommended)**: Single function with context parameter
- **Option 2**: Separate functions for articles and resources

---

## Option 1: Single Function with Context Parameter (RECOMMENDED)

### Why This Approach?
- Single codebase to maintain
- No duplicate code
- Easy to add more contexts later
- Lower AWS costs (one function vs two)
- Simpler architecture

### Step 1: Update Lambda Function Code

**File: `url_analysis_api/index.py`**

**Note:** This function requires the `requests` library via Lambda Layer (see Step 2 for setup).

```python
import json
import boto3
import os
from html.parser import HTMLParser
import re
import requests

# AWS Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# Environment variable to enable/disable AI
USE_AI_SUMMARY = os.environ.get('USE_AI_SUMMARY', 'false').lower() == 'true'

class MetaTagParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_tags = {}
        self.title = None
        self.in_title = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            name = attrs_dict.get('name', '').lower()
            property_name = attrs_dict.get('property', '').lower()
            content = attrs_dict.get('content', '')
            
            if name == 'description':
                self.meta_tags['description'] = content
            elif property_name == 'og:title':
                self.meta_tags['og_title'] = content
            elif property_name == 'og:description':
                self.meta_tags['og_description'] = content
            elif property_name == 'og:image':
                self.meta_tags['og_image'] = content
    
    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
    }
    
    try:
        if event.get('httpMethod') == 'OPTIONS':
            return {'statusCode': 200, 'headers': headers, 'body': ''}
        
        body = json.loads(event.get('body', '{}'))
        url = body.get('url')
        context_type = body.get('context', 'resource')  # 'resource' or 'article'
        
        if not url:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'URL required'})
            }
        
        # Analyze URL with context
        result = analyze_url(url, context_type)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def analyze_url(url, context_type='resource'):
    """Extract meta tags and optionally generate AI summary"""
    
    # Fetch webpage with enhanced headers to bypass bot detection
    try:
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        response = session.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        return {'error': f'Failed to fetch URL: {str(e)}'}
    
    # Extract meta tags
    parser = MetaTagParser()
    parser.feed(html)
    
    # Get text content for AI summary
    text_content = extract_text_content(html)
    
    # Build result
    result = {
        'url': url,
        'title': parser.meta_tags.get('og_title') or parser.title or 'Untitled',
        'description': parser.meta_tags.get('og_description') or parser.meta_tags.get('description') or '',
        'image': parser.meta_tags.get('og_image') or '',
        'ai_enabled': USE_AI_SUMMARY,
        'context': context_type
    }
    
    # Generate AI summary if enabled
    if USE_AI_SUMMARY and text_content:
        try:
            ai_summary = generate_ai_summary(text_content, result['title'], context_type)
            result['ai_summary'] = ai_summary
        except Exception as e:
            result['ai_error'] = str(e)
    
    return result

def extract_text_content(html):
    """Extract main text content from HTML"""
    # Remove script and style tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', html)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Limit to first 3000 characters for AI processing
    return text[:3000]

def generate_ai_summary(content, title, context_type='resource'):
    """Generate summary using AWS Bedrock Claude"""
    
    # Different prompts based on context
    if context_type == 'article':
        prompt = f"""Summarize this article in 2-3 sentences from a Christian conservative perspective. Focus on key facts and biblical relevance if applicable.

Title: {title}

Content: {content}

Summary:"""
    else:  # resource context
        prompt = f"""Summarize this page in 2-3 sentences. If there is a Christian reference to this page, highlight how it is beneficial from a Christian conservative perspective focusing on key facts and biblical relevance if applicable.

Title: {title}

Content: {content}

Summary:"""
    
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',
        body=json.dumps(request_body)
    )
    
    response_body = json.loads(response['body'].read())
    summary = response_body['content'][0]['text'].strip()
    
    return summary
```

### Step 2: Create Lambda Layer for Requests Library

The `requests` library is not included in Lambda by default. Create a layer:

#### PowerShell (Windows)
```powershell
cd c:\Users\Ed\Documents\Programming\AWS\Downloader\url_analysis_api
mkdir python
pip install requests -t python
Compress-Archive -Path python -DestinationPath requests-layer.zip -Force
aws lambda publish-layer-version --layer-name requests-layer --zip-file fileb://requests-layer.zip --compatible-runtimes python3.9 python3.10 python3.11 python3.12
```

#### Bash (Linux/Mac)
```bash
cd ~/AWS/Downloader/url_analysis_api
mkdir python
pip install requests -t python
zip -r requests-layer.zip python
aws lambda publish-layer-version --layer-name requests-layer --zip-file fileb://requests-layer.zip --compatible-runtimes python3.9 python3.10 python3.11 python3.12
```

**Note the Layer ARN from the output** (e.g., `arn:aws:lambda:us-east-1:371751795928:layer:requests-layer:1`)

### Step 3: Deploy Updated Function

#### PowerShell (Windows)
```powershell
cd c:\Users\Ed\Documents\Programming\AWS\Downloader\url_analysis_api
Compress-Archive -Path index.py -DestinationPath function.zip -Force
aws lambda update-function-code --function-name url-analysis-api --zip-file fileb://function.zip

# Attach the layer (replace with your Layer ARN)
aws lambda update-function-configuration --function-name url-analysis-api --layers arn:aws:lambda:us-east-1:371751795928:layer:requests-layer:1
```

#### Bash (Linux/Mac)
```bash
cd ~/AWS/Downloader/url_analysis_api
zip function.zip index.py
aws lambda update-function-code --function-name url-analysis-api --zip-file fileb://function.zip

# Attach the layer (replace with your Layer ARN)
aws lambda update-function-configuration --function-name url-analysis-api --layers arn:aws:lambda:us-east-1:371751795928:layer:requests-layer:1
```

#### AWS Console
1. Go to **AWS Lambda Console**
2. Find `url-analysis-api` function
3. Click **Upload from** → **.zip file**
4. Upload the `function.zip` file
5. Click **Save**
6. Scroll down to **Layers** → **Add a layer**
7. Select **Custom layers** → `requests-layer` → Version 1
8. Click **Add**

### Step 4: Update Frontend Files

#### admin.html (Resources Section)

Find the `analyzeResourceUrl()` function and update the fetch call:

```javascript
// OLD:
body: JSON.stringify({url: url})

// NEW:
body: JSON.stringify({url: url, context: 'resource'})
```

#### create-article.html

Find the `analyzeUrl()` function and update the fetch call:

```javascript
// OLD:
body: JSON.stringify({url: url})

// NEW:
body: JSON.stringify({url: url, context: 'article'})
```

#### edit-article.html

Find the `analyzeUrl()` function and update the fetch call:

```javascript
// OLD:
body: JSON.stringify({url: url})

// NEW:
body: JSON.stringify({url: url, context: 'article'})
```

### Step 5: Upload Updated HTML Files

#### PowerShell
```powershell
cd c:\Users\Ed\Documents\Programming\AWS\Downloader
aws s3 cp admin.html s3://my-video-downloads-bucket/ --content-type "text/html"
aws s3 cp create-article.html s3://my-video-downloads-bucket/ --content-type "text/html"
aws s3 cp edit-article.html s3://my-video-downloads-bucket/ --content-type "text/html"
```

#### Bash
```bash
cd ~/AWS/Downloader
aws s3 cp admin.html s3://my-video-downloads-bucket/ --content-type "text/html"
aws s3 cp create-article.html s3://my-video-downloads-bucket/ --content-type "text/html"
aws s3 cp edit-article.html s3://my-video-downloads-bucket/ --content-type "text/html"
```

#### AWS Console
1. Go to **S3 Console**
2. Open `my-video-downloads-bucket`
3. Click **Upload**
4. Select `admin.html`, `create-article.html`, `edit-article.html`
5. Click **Upload**

---

## Option 2: Separate Lambda Functions

### Why This Approach?
- Complete separation of concerns
- Independent scaling
- Easier to understand for beginners
- Can have different IAM permissions per function

### Drawbacks
- Duplicate code
- More functions to maintain
- Higher AWS costs
- More complex architecture

### Step 1: Create Article Analysis Function

#### Create Directory

**PowerShell:**
```powershell
cd c:\Users\Ed\Documents\Programming\AWS\Downloader
mkdir article_analysis_api
cd article_analysis_api
```

**Bash:**
```bash
cd ~/AWS/Downloader
mkdir article_analysis_api
cd article_analysis_api
```

#### Create index.py

**File: `article_analysis_api/index.py`**

```python
import json
import boto3
import os
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlparse
import re

# AWS Bedrock client
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# Environment variable to enable/disable AI
USE_AI_SUMMARY = os.environ.get('USE_AI_SUMMARY', 'false').lower() == 'true'

class MetaTagParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta_tags = {}
        self.title = None
        self.in_title = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag == 'title':
            self.in_title = True
        elif tag == 'meta':
            name = attrs_dict.get('name', '').lower()
            property_name = attrs_dict.get('property', '').lower()
            content = attrs_dict.get('content', '')
            
            if name == 'description':
                self.meta_tags['description'] = content
            elif property_name == 'og:title':
                self.meta_tags['og_title'] = content
            elif property_name == 'og:description':
                self.meta_tags['og_description'] = content
            elif property_name == 'og:image':
                self.meta_tags['og_image'] = content
    
    def handle_data(self, data):
        if self.in_title:
            self.title = data.strip()
    
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
    }
    
    try:
        if event.get('httpMethod') == 'OPTIONS':
            return {'statusCode': 200, 'headers': headers, 'body': ''}
        
        body = json.loads(event.get('body', '{}'))
        url = body.get('url')
        
        if not url:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'URL required'})
            }
        
        # Analyze URL
        result = analyze_url(url)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(result)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }

def analyze_url(url):
    """Extract meta tags and optionally generate AI summary"""
    
    # Fetch webpage
    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return {'error': f'Failed to fetch URL: {str(e)}'}
    
    # Extract meta tags
    parser = MetaTagParser()
    parser.feed(html)
    
    # Get text content for AI summary
    text_content = extract_text_content(html)
    
    # Build result
    result = {
        'url': url,
        'title': parser.meta_tags.get('og_title') or parser.title or 'Untitled',
        'description': parser.meta_tags.get('og_description') or parser.meta_tags.get('description') or '',
        'image': parser.meta_tags.get('og_image') or '',
        'ai_enabled': USE_AI_SUMMARY
    }
    
    # Generate AI summary if enabled
    if USE_AI_SUMMARY and text_content:
        try:
            ai_summary = generate_ai_summary(text_content, result['title'])
            result['ai_summary'] = ai_summary
        except Exception as e:
            result['ai_error'] = str(e)
    
    return result

def extract_text_content(html):
    """Extract main text content from HTML"""
    # Remove script and style tags
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', ' ', html)
    
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Limit to first 3000 characters for AI processing
    return text[:3000]

def generate_ai_summary(content, title):
    """Generate summary using AWS Bedrock Claude - ARTICLE CONTEXT"""
    
    prompt = f"""Summarize this article in 2-3 sentences from a Christian conservative perspective. Focus on key facts and biblical relevance if applicable.

Title: {title}

Content: {content}

Summary:"""
    
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',
        body=json.dumps(request_body)
    )
    
    response_body = json.loads(response['body'].read())
    summary = response_body['content'][0]['text'].strip()
    
    return summary
```

### Step 2: Create Lambda Function

#### PowerShell
```powershell
cd c:\Users\Ed\Documents\Programming\AWS\Downloader\article_analysis_api
Compress-Archive -Path index.py -DestinationPath function.zip -Force
aws lambda create-function --function-name article-analysis-api --runtime python3.9 --role arn:aws:iam::371751795928:role/lambda-execution-role --handler index.lambda_handler --zip-file fileb://function.zip --timeout 30 --memory-size 256 --environment "Variables={USE_AI_SUMMARY=true}"
```

#### Bash
```bash
cd ~/AWS/Downloader/article_analysis_api
zip function.zip index.py
aws lambda create-function --function-name article-analysis-api --runtime python3.9 --role arn:aws:iam::371751795928:role/lambda-execution-role --handler index.lambda_handler --zip-file fileb://function.zip --timeout 30 --memory-size 256 --environment "Variables={USE_AI_SUMMARY=true}"
```

#### AWS Console
1. Go to **AWS Lambda Console** → **Create function**
2. Function name: `article-analysis-api`
3. Runtime: **Python 3.9**
4. Execution role: **Use existing role** → `lambda-execution-role`
5. Click **Create function**
6. Upload `function.zip` (Code source → Upload from → .zip file)
7. **Configuration** → **Environment variables** → Add `USE_AI_SUMMARY=true`
8. **Configuration** → **General configuration** → Timeout: 30 seconds, Memory: 256 MB

### Step 3: Create API Gateway

#### PowerShell
```powershell
# Create REST API
$API_ID = (aws apigateway create-rest-api --name article-analysis-api --endpoint-configuration types=REGIONAL --query 'id' --output text)
$ROOT_ID = (aws apigateway get-resources --rest-api-id $API_ID --query 'items[0].id' --output text)

# Create /analyze resource
$RESOURCE_ID = (aws apigateway create-resource --rest-api-id $API_ID --parent-id $ROOT_ID --path-part analyze --query 'id' --output text)

# Create POST method
aws apigateway put-method --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method POST --authorization-type NONE

# Create OPTIONS method for CORS
aws apigateway put-method --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method OPTIONS --authorization-type NONE

# Integrate POST with Lambda
aws apigateway put-integration --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method POST --type AWS_PROXY --integration-http-method POST --uri "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:371751795928:function:article-analysis-api/invocations"

# Configure OPTIONS for CORS
aws apigateway put-integration --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method OPTIONS --type MOCK --request-templates '{\"application/json\":\"{\\\"statusCode\\\": 200}\"}'

aws apigateway put-method-response --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method OPTIONS --status-code 200 --response-parameters "method.response.header.Access-Control-Allow-Headers=false,method.response.header.Access-Control-Allow-Methods=false,method.response.header.Access-Control-Allow-Origin=false"

aws apigateway put-integration-response --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method OPTIONS --status-code 200 --response-parameters '{\"method.response.header.Access-Control-Allow-Headers\":\"'"'"'Content-Type,Authorization'"'"'\",\"method.response.header.Access-Control-Allow-Methods\":\"'"'"'GET,POST,OPTIONS'"'"'\",\"method.response.header.Access-Control-Allow-Origin\":\"'"'"'*'"'"'\"}'

# Grant API Gateway permission to invoke Lambda
aws lambda add-permission --function-name article-analysis-api --statement-id apigateway-invoke --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:us-east-1:371751795928:$API_ID/*/*"

# Deploy API
aws apigateway create-deployment --rest-api-id $API_ID --stage-name prod

Write-Host "API Endpoint: https://$API_ID.execute-api.us-east-1.amazonaws.com/prod/analyze"
```

#### Bash
```bash
# Create REST API
API_ID=$(aws apigateway create-rest-api --name article-analysis-api --endpoint-configuration types=REGIONAL --query 'id' --output text)
ROOT_ID=$(aws apigateway get-resources --rest-api-id $API_ID --query 'items[0].id' --output text)

# Create /analyze resource
RESOURCE_ID=$(aws apigateway create-resource --rest-api-id $API_ID --parent-id $ROOT_ID --path-part analyze --query 'id' --output text)

# Create POST method
aws apigateway put-method --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method POST --authorization-type NONE

# Create OPTIONS method for CORS
aws apigateway put-method --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method OPTIONS --authorization-type NONE

# Integrate POST with Lambda
aws apigateway put-integration --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method POST --type AWS_PROXY --integration-http-method POST --uri "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:371751795928:function:article-analysis-api/invocations"

# Configure OPTIONS for CORS
aws apigateway put-integration --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method OPTIONS --type MOCK --request-templates '{"application/json":"{\"statusCode\": 200}"}'

aws apigateway put-method-response --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method OPTIONS --status-code 200 --response-parameters "method.response.header.Access-Control-Allow-Headers=false,method.response.header.Access-Control-Allow-Methods=false,method.response.header.Access-Control-Allow-Origin=false"

aws apigateway put-integration-response --rest-api-id $API_ID --resource-id $RESOURCE_ID --http-method OPTIONS --status-code 200 --response-parameters '{"method.response.header.Access-Control-Allow-Headers":"'"'"'Content-Type,Authorization'"'"'","method.response.header.Access-Control-Allow-Methods":"'"'"'GET,POST,OPTIONS'"'"'","method.response.header.Access-Control-Allow-Origin":"'"'"'*'"'"'"}'

# Grant API Gateway permission to invoke Lambda
aws lambda add-permission --function-name article-analysis-api --statement-id apigateway-invoke --action lambda:InvokeFunction --principal apigateway.amazonaws.com --source-arn "arn:aws:execute-api:us-east-1:371751795928:$API_ID/*/*"

# Deploy API
aws apigateway create-deployment --rest-api-id $API_ID --stage-name prod

echo "API Endpoint: https://$API_ID.execute-api.us-east-1.amazonaws.com/prod/analyze"
```

#### AWS Console
1. Go to **API Gateway Console** → **Create API** → **REST API**
2. API name: `article-analysis-api`
3. Click **Create API**
4. **Actions** → **Create Resource**
   - Resource Name: `analyze`
   - Resource Path: `/analyze`
5. Select `/analyze` → **Actions** → **Create Method** → **POST**
   - Integration type: Lambda Function
   - Lambda Function: `article-analysis-api`
   - Save and confirm
6. Select `/analyze` → **Actions** → **Enable CORS**
   - Accept defaults and enable
7. **Actions** → **Deploy API**
   - Stage: `prod`
8. Note the **Invoke URL**

### Step 4: Update Frontend Files

#### admin.html (Resources)
Keep existing URL: `https://q65k3dbpd7.execute-api.us-east-1.amazonaws.com/prod/analyze`

#### create-article.html
Update to new API endpoint:
```javascript
const ARTICLE_ANALYSIS_API = 'https://YOUR_NEW_API_ID.execute-api.us-east-1.amazonaws.com/prod/analyze';

// In analyzeUrl() function:
const response = await fetch(ARTICLE_ANALYSIS_API, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({url: url})
});
```

#### edit-article.html
Update to new API endpoint:
```javascript
const ARTICLE_ANALYSIS_API = 'https://YOUR_NEW_API_ID.execute-api.us-east-1.amazonaws.com/prod/analyze';

// In analyzeUrl() function:
const response = await fetch(ARTICLE_ANALYSIS_API, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({url: url})
});
```

### Step 5: Upload Updated HTML Files

Same as Option 1 Step 4.

---

## Comparison Table

| Feature | Option 1 (Single Function) | Option 2 (Separate Functions) |
|---------|---------------------------|------------------------------|
| Code Maintenance | ✅ Single codebase | ❌ Duplicate code |
| Complexity | ✅ Simple | ❌ More complex |
| AWS Costs | ✅ Lower | ❌ Higher |
| Scalability | ✅ Easy to add contexts | ❌ Need new function each time |
| Separation of Concerns | ⚠️ Shared function | ✅ Complete separation |
| Deployment | ✅ One deployment | ❌ Multiple deployments |

## Recommendation

**Use Option 1** unless you have specific requirements for complete separation of article and resource analysis.

---

## Testing

### Test Resource Context (Option 1)
```bash
curl -X POST https://q65k3dbpd7.execute-api.us-east-1.amazonaws.com/prod/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://wallbuilders.com/", "context": "resource"}'
```

### Test Article Context (Option 1)
```bash
curl -X POST https://q65k3dbpd7.execute-api.us-east-1.amazonaws.com/prod/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://crossexamined.org/dr-frank-turek/", "context": "article"}'
```

### Test Article Function (Option 2)
```bash
curl -X POST https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/analyze \
  -H "Content-Type: application/json" \
  -d '{"url": "https://crossexamined.org/dr-frank-turek/"}'
```

---

## AI Toggle Management

### PowerShell Toggle Script (Recommended)

A convenient PowerShell script `toggle-ai.ps1` is provided for easy AI management:

**File: `toggle-ai.ps1`**
```powershell
# Toggle AI Summary for URL Analysis API
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("enable", "disable", "status")]
    [string]$Action
)

$FunctionName = "url-analysis-api"

switch ($Action) {
    "enable" {
        Write-Host "Enabling AI Summary..." -ForegroundColor Yellow
        aws lambda update-function-configuration --function-name $FunctionName --environment "Variables={USE_AI_SUMMARY=true}"
        Write-Host "AI Summary enabled successfully!" -ForegroundColor Green
    }
    "disable" {
        Write-Host "Disabling AI Summary..." -ForegroundColor Yellow
        aws lambda update-function-configuration --function-name $FunctionName --environment "Variables={USE_AI_SUMMARY=false}"
        Write-Host "AI Summary disabled successfully!" -ForegroundColor Green
    }
    "status" {
        Write-Host "Checking AI Summary status..." -ForegroundColor Yellow
        $config = aws lambda get-function-configuration --function-name $FunctionName | ConvertFrom-Json
        $status = $config.Environment.Variables.USE_AI_SUMMARY
        Write-Host "AI Summary is currently: $status" -ForegroundColor Cyan
    }
}
```

**Usage:**
```powershell
# Enable AI summarization
.\toggle-ai.ps1 enable

# Disable AI summarization
.\toggle-ai.ps1 disable

# Check current status
.\toggle-ai.ps1 status
```

**Benefits:**
- Simple one-command toggle
- Color-coded output for clarity
- Built-in status checking
- No need to remember complex AWS CLI commands

---

## Troubleshooting

### Lambda Permission Issues
```bash
aws iam attach-role-policy --role-name lambda-execution-role --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
```

### Check Lambda Logs
```bash
aws logs tail /aws/lambda/url-analysis-api --follow
```

### Update Environment Variable (Manual)
```bash
aws lambda update-function-configuration --function-name url-analysis-api --environment "Variables={USE_AI_SUMMARY=true}"
```

---

## Cost Estimation

### Option 1 (Single Function)
- Lambda invocations: $0.20 per 1M requests
- Claude 3 Haiku: ~$0.00025 per request
- **Total**: ~$0.25 per 1000 analyses

### Option 2 (Separate Functions)
- Lambda invocations: $0.40 per 1M requests (2 functions)
- Claude 3 Haiku: ~$0.00025 per request
- **Total**: ~$0.45 per 1000 analyses

**Savings with Option 1**: ~44% lower costs
