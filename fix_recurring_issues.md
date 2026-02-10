# Recurring Issues - Complete Fix Guide

## Issue 1: Scripture Lookup Not Working

### Root Cause
- Lambda function missing `requests` library
- Bible API (bible-api.com) needs proper error handling
- KJV translation URL needs explicit parameter

### Fix Steps
1. Check Lambda deployment package includes requests library
2. Verify `get_bible_verse()` function in articles_api/index.py
3. Redeploy Lambda with proper dependencies

### Deployment Command
```powershell
cd articles_api
pip install -r requirements.txt -t .
Compress-Archive -Path * -DestinationPath articles-api.zip -Force
aws lambda update-function-code --function-name articles-api --zip-file fileb://articles-api.zip
```

## Issue 2: JWT Token Expiration (24 Hours)

### Root Cause
- Token expires but localStorage still has expired token
- No expiration check on page load
- User appears logged in but API calls fail with 401/403

### Fix: Add Token Expiration Check
Add this to create-article.html and edit-article.html at page load:

```javascript
function checkTokenExpiration() {
    const token = localStorage.getItem('auth_token');
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    
    try {
        // Decode JWT token (middle part)
        const payload = JSON.parse(atob(token.split('.')[1]));
        const exp = payload.exp * 1000; // Convert to milliseconds
        const now = Date.now();
        
        if (now >= exp) {
            // Token expired
            alert('Your session has expired. Please log in again.');
            localStorage.removeItem('auth_token');
            localStorage.removeItem('user_data');
            window.location.href = 'login.html';
            return false;
        }
        return true;
    } catch (e) {
        console.error('Token validation error:', e);
        window.location.href = 'login.html';
        return false;
    }
}

// Call on page load
document.addEventListener('DOMContentLoaded', function() {
    if (!checkTokenExpiration()) {
        return; // Stop page initialization if token expired
    }
    // ... rest of initialization code
});
```

## Issue 3: Article Author Showing Email Instead of Name

### Root Cause
- `articles_api/index.py` create_article() not setting author_name field
- Users table uses user_id as primary key (not email)
- Need to scan by email to get first_name/last_name

### Fix: Update articles_api/index.py

```python
def get_user_name(email):
    """Get user's full name from email"""
    try:
        response = users_table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        items = response.get('Items', [])
        if items:
            user = items[0]
            first_name = user.get('first_name', '')
            last_name = user.get('last_name', '')
            if first_name or last_name:
                return f"{first_name} {last_name}".strip()
        return email
    except Exception as e:
        print(f"Error getting user name: {e}")
        return email

def create_article(event, headers):
    # ... existing code ...
    
    article = {
        'article_id': article_id,
        'title': body['title'],
        'content': body.get('content', ''),
        'author': user_info['email'],
        'author_name': get_user_name(user_info['email']),  # ADD THIS LINE
        # ... rest of fields
    }
```

### Deployment
```powershell
cd articles_api
Compress-Archive -Path index.py -DestinationPath articles-api.zip -Force
aws lambda update-function-code --function-name articles-api --zip-file fileb://articles-api.zip
```

## Migration Script for Existing Articles

```python
# update_article_author_names.py
import boto3

dynamodb = boto3.resource('dynamodb')
articles_table = dynamodb.Table('articles-table')
users_table = dynamodb.Table('users')

def get_user_name(email):
    try:
        response = users_table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        items = response.get('Items', [])
        if items:
            user = items[0]
            first_name = user.get('first_name', '')
            last_name = user.get('last_name', '')
            if first_name or last_name:
                return f"{first_name} {last_name}".strip()
        return email
    except:
        return email

# Scan all articles
response = articles_table.scan()
articles = response.get('Items', [])

print(f"Found {len(articles)} articles")

for article in articles:
    article_id = article['article_id']
    author_email = article.get('author', '')
    
    if author_email:
        author_name = get_user_name(author_email)
        
        print(f"Updating {article['title'][:50]}...")
        print(f"  Author: {author_email} -> {author_name}")
        
        articles_table.update_item(
            Key={'article_id': article_id},
            UpdateExpression='SET author_name = :author_name',
            ExpressionAttributeValues={':author_name': author_name}
        )

print("\nAll articles updated!")
```

## Issue 4: Pennsylvania Election Data - Duplicate Candidates

### Root Cause
- Grok AI generated same candidates multiple times across different chunk2 files
- 119 candidate entries but only 51 unique candidates (68 duplicates)
- Malformed JSON in chunk files (missing braces, commas, endorsements)
- Database vs Summary count mismatch (summary showed fake numbers)

### Symptoms
- Duplicate candidates appearing in election map
- Incorrect race/candidate counts in summary
- Missing emojis in summary chunks
- JSON syntax errors during upload

### Fix Steps

#### 1. Identify Clean Data
```powershell
# Search for candidates across all chunk files
Get-ChildItem -Path "Election Chunks/COMPLETE_STATE_TEMPLATES/Pennsylvania" -Filter "chunk2*.txt" | Select-String "candidate_name"

# Only chunk2a_output.txt had clean, complete data
```

#### 2. Clean Slate Upload
```python
# clean_slate_upload.py
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('summaries')

# Delete all Pennsylvania data
print("Deleting Pennsylvania races...")
response = races_table.scan(FilterExpression='state = :state', ExpressionAttributeValues={':state': 'Pennsylvania'})
for item in response['Items']:
    races_table.delete_item(Key={'race_id': item['race_id']})

print("Deleting Pennsylvania candidates...")
response = candidates_table.scan(FilterExpression='state = :state', ExpressionAttributeValues={':state': 'Pennsylvania'})
for item in response['Items']:
    candidates_table.delete_item(Key={'candidate_id': item['candidate_id']})

print("Deleting Pennsylvania summary...")
response = summaries_table.scan(FilterExpression='state = :state', ExpressionAttributeValues={':state': 'Pennsylvania'})
for item in response['Items']:
    summaries_table.delete_item(Key={'state': item['state']})

print("Running fresh upload...")
import subprocess
subprocess.run(['python', 'upload_pennsylvania_data.py'])
```

#### 3. Update Combine Script to Use Only Clean Data
```python
# combine_pennsylvania_chunks.py
chunk_files = [
    'chunk1_output.txt',
    'chunk2a_output.txt',  # ONLY use chunk2a - has clean data
    'chunk5a_output.txt',
    'chunk5b_output.txt'
]
```

#### 4. Fix Summary Counts Manually
Edit chunk5a_output.txt to show actual database counts:
```markdown
## 📊 Database Summary
- **Total Races**: 341
- **Total Candidates**: 12 (10 from chunk2a + 2 manually added)
```

#### 5. Add Missing Candidates
```python
# add_missing_candidates.py
import boto3
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
candidates_table = dynamodb.Table('candidates')

candidates = [
    {
        'candidate_id': str(uuid.uuid4()),
        'state': 'Pennsylvania',
        'office': 'U.S. House District 7',
        'candidate_name': 'Ryan Crosswell',
        'party': 'Republican',
        # ... full data from chunk2j_output.txt
    },
    {
        'candidate_id': str(uuid.uuid4()),
        'state': 'Pennsylvania',
        'office': 'U.S. House District 7',
        'candidate_name': 'Carol Obando-Derstine',
        'party': 'Independent',
        # ... full data from chunk2j_output.txt
    }
]

for candidate in candidates:
    candidates_table.put_item(Item=candidate)
```

### Prevention

1. **Always verify chunk data before upload**:
   - Check for duplicate candidate names
   - Validate JSON syntax
   - Count unique candidates vs total entries

2. **Use deduplication script**:
```python
# deduplicate_chunks_v2.py
import json

seen = set()
unique_candidates = []

for candidate in all_candidates:
    key = (candidate['candidate_name'], candidate['office'])
    if key not in seen:
        seen.add(key)
        unique_candidates.append(candidate)

print(f"Original: {len(all_candidates)}, Unique: {len(unique_candidates)}")
```

3. **Clean slate approach for corrupted data**:
   - Delete all state data
   - Upload fresh from verified clean files
   - Don't try to merge/update corrupted data

4. **Verify summary counts match database**:
```python
# verify_counts.py
import boto3

dynamodb = boto3.resource('dynamodb')
races = dynamodb.Table('races').scan(FilterExpression='state = :state', ExpressionAttributeValues={':state': 'Pennsylvania'})
candidates = dynamodb.Table('candidates').scan(FilterExpression='state = :state', ExpressionAttributeValues={':state': 'Pennsylvania'})

print(f"Races: {len(races['Items'])}")
print(f"Candidates: {len(candidates['Items'])}")
```

### Files Created
- `Election Chunks/COMPLETE_STATE_TEMPLATES/Pennsylvania/clean_slate_upload.py`
- `Election Chunks/COMPLETE_STATE_TEMPLATES/Pennsylvania/deduplicate_chunks_v2.py`
- `Election Chunks/COMPLETE_STATE_TEMPLATES/Pennsylvania/add_missing_candidates.py`
- `Election Chunks/COMPLETE_STATE_TEMPLATES/Pennsylvania/remove_duplicates.py`

## Issue 5: Missing Emojis in Summary Chunks

### Root Cause
- Templates didn't include emoji formatting instructions
- AI-generated output lacked visual indicators
- Frontend expects specific emojis for display

### Required Emojis
- 🚨 Critical/Important items
- ❌ Negative/Oppose positions
- ✅ Positive/Support positions
- 📊 Data/Statistics
- 🔴 Republican
- 🔵 Democrat

### Fix
Update CHUNK_5A and CHUNK_5B templates:
```markdown
## 📊 Database Summary
- **Total Races**: {count}
- **Total Candidates**: {count}

## 🚨 Critical Races
- 🔴 Republican incumbent
- 🔵 Democrat challenger
- ✅ Pro-life position
- ❌ Pro-choice position
```

### Deployment
Regenerate summary chunks with emoji formatting, then update database:
```powershell
python combine_pennsylvania_chunks.py
python upload_pennsylvania_data.py
```

## Issue 6: Candidates Appearing in "Other Candidates" Section

### Root Cause
- Candidates added to database without `race_id` field
- Frontend election-map.html filters candidates by race_id
- Candidates without race_id appear in "Other Candidates" section at bottom

### Symptoms
- Candidates show under "Other Candidates" instead of their race
- Candidates not grouped with other candidates for same office
- Missing from main race display

### Frontend Logic (election-map.html line 682)
```javascript
const unassignedCandidates = stateCandidates.filter(c => !c.race_id || c.race_id === '');
if (unassignedCandidates.length > 0) {
    candidatesHTML += '<div class="alert alert-secondary mt-3"><strong>Other Candidates</strong></div>';
    // Display unassigned candidates separately
}
```

### Fix: Add race_id to Candidates

```python
# fix_candidate_race_ids.py
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Find the race_id for the office
response = races_table.scan(
    FilterExpression='#st = :state AND office = :office',
    ExpressionAttributeNames={'#st': 'state'},
    ExpressionAttributeValues={
        ':state': 'Pennsylvania',
        ':office': 'U.S. House District 7'
    }
)

race_id = response['Items'][0]['race_id']
print(f"Found race_id: {race_id}")

# Find candidates for this office
response = candidates_table.scan(
    FilterExpression='#st = :state AND office = :office',
    ExpressionAttributeNames={'#st': 'state'},
    ExpressionAttributeValues={
        ':state': 'Pennsylvania',
        ':office': 'U.S. House District 7'
    }
)

# Update candidates missing race_id
for candidate in response['Items']:
    if not candidate.get('race_id'):
        print(f"Updating {candidate['name']} ({candidate['party']})...")
        candidates_table.update_item(
            Key={'candidate_id': candidate['candidate_id']},
            UpdateExpression='SET race_id = :race_id',
            ExpressionAttributeValues={':race_id': race_id}
        )
        print(f"  Added race_id: {race_id}")
```

### Prevention

1. **Always include race_id when adding candidates**:
```python
candidate = {
    'candidate_id': str(uuid.uuid4()),
    'state': 'Pennsylvania',
    'office': 'U.S. House District 7',
    'race_id': 'def72b7d-c33e-408f-8c1a-2d82956bc219',  # REQUIRED
    'name': 'Candidate Name',
    'party': 'Republican',
    # ... other fields
}
```

2. **Verify race exists before adding candidates**:
```python
# Get race_id first
race_response = races_table.scan(
    FilterExpression='#st = :state AND office = :office',
    ExpressionAttributeNames={'#st': 'state'},
    ExpressionAttributeValues={':state': state, ':office': office}
)
if not race_response['Items']:
    print(f"ERROR: Race not found for {office}")
    exit(1)
race_id = race_response['Items'][0]['race_id']
```

3. **Check for unassigned candidates after upload**:
```python
# verify_candidate_assignments.py
response = candidates_table.scan(
    FilterExpression='#st = :state',
    ExpressionAttributeNames={'#st': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)

unassigned = [c for c in response['Items'] if not c.get('race_id')]
if unassigned:
    print(f"WARNING: {len(unassigned)} candidates without race_id:")
    for c in unassigned:
        print(f"  - {c['name']} ({c['office']})")
```

### Files Created
- `Election Chunks/COMPLETE_STATE_TEMPLATES/Pennsylvania/fix_candidate_race_ids.py`

## Issue 7: Summary Guide Shows Wrong Counts

### Root Cause
- Summary text in `state-summaries` table contains hardcoded counts
- Counts don't update automatically when database changes
- After clean slate upload or data fixes, summary still shows old counts

### Symptoms
- Election Overview shows different count than summary guide
- Summary shows 119 candidates but database has 12
- Counts don't match after uploading fresh data

### Fix: Update Summary with Actual Database Counts

```python
# update_summary_counts.py
import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')

# Get actual counts
races_response = races_table.scan(
    FilterExpression='#st = :state',
    ExpressionAttributeNames={'#st': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)
actual_races = len(races_response['Items'])

candidates_response = candidates_table.scan(
    FilterExpression='#st = :state',
    ExpressionAttributeNames={'#st': 'state'},
    ExpressionAttributeValues={':state': 'Pennsylvania'}
)
actual_candidates = len(candidates_response['Items'])

print(f"Actual: Races={actual_races}, Candidates={actual_candidates}")

# Get and update summary
summary_response = summaries_table.get_item(Key={'state': 'Pennsylvania'})
current_summary = summary_response['Item']['content']

updated_summary = current_summary.replace(
    '**Total Races**: 341', f'**Total Races**: {actual_races}'
).replace(
    '**Total Candidates**: 119', f'**Total Candidates**: {actual_candidates}'
).replace(
    '**Total Candidates Profiled:** 119', f'**Total Candidates Profiled:** {actual_candidates}'
)

summaries_table.update_item(
    Key={'state': 'Pennsylvania'},
    UpdateExpression='SET content = :summary',
    ExpressionAttributeValues={':summary': updated_summary}
)

print("Summary updated!")
```

### CRITICAL: Check Actual Text Pattern First

The summary might use different text patterns than expected:
- Expected: `**Total Candidates**: 119`
- Actual: `**Total Candidates Profiled:** 119`

**Always check the actual text before running replace**:
```python
# check_summary.py
response = summaries_table.get_item(Key={'state': 'Pennsylvania'})
content = response['Item']['content']
for line in content.split('\n'):
    if 'Total Candidates' in line or 'Total Races' in line:
        print(line)  # See exact text pattern
```

Then add replace patterns for ALL variations found.

### Prevention

1. **Always update summary after data changes**:
```bash
python update_summary_counts.py
```

2. **Verify counts match before considering upload complete**:
```python
# At end of upload script
print("\nVerifying counts...")
races_count = len(races_table.scan(FilterExpression='#st = :state', ...)['Items'])
candidates_count = len(candidates_table.scan(FilterExpression='#st = :state', ...)['Items'])
print(f"Database: {races_count} races, {candidates_count} candidates")
print("Update summary if counts don't match!")
```

3. **Use dynamic counts in summary generation**:
- Instead of hardcoding counts in chunk5a_output.txt
- Calculate actual counts and inject into summary template
- Or update summary immediately after upload

### Files Created
- `Election Chunks/COMPLETE_STATE_TEMPLATES/Pennsylvania/update_summary_counts.py`

## Issue 8: Lambda Function Not Receiving API Gateway Requests

### Root Cause
- API Gateway lacks permission to invoke Lambda function
- Lambda execution role missing required permissions (SES, CloudWatch Logs)
- Integration configured but permission not granted

### Symptoms
- API returns "Internal server error" with no logs
- Lambda function exists but never executes
- CloudWatch log group doesn't exist
- curl/fetch requests fail with 500 error

### Fix Steps

#### 1. Grant API Gateway Permission to Invoke Lambda
```bash
aws lambda add-permission \
  --function-name contact-form-api \
  --statement-id apigateway-invoke \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:us-east-1:371751795928:k2zbtkeh67/*/*/contact"
```

#### 2. Add SES Permissions to Lambda Role
```bash
aws iam attach-role-policy \
  --role-name lambda-execution-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonSESFullAccess
```

#### 3. Add CloudWatch Logs Permissions
```bash
aws iam attach-role-policy \
  --role-name lambda-execution-role \
  --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
```

#### 4. Test the Endpoint
```bash
curl -k -X POST https://k2zbtkeh67.execute-api.us-east-1.amazonaws.com/prod/contact \
  -H "Content-Type: application/json" \
  -d '{"to_email":"contact@christianconservativestoday.com","subject":"Test","message":"Test message"}'
```

Should return: `{"message": "Email sent successfully"}`

### Prevention

1. **Always add Lambda invoke permission when creating API Gateway integration**:
```bash
aws lambda add-permission \
  --function-name <function-name> \
  --statement-id apigateway-invoke \
  --action lambda:InvokeFunction \
  --principal apigateway.amazonaws.com \
  --source-arn "arn:aws:execute-api:<region>:<account-id>:<api-id>/*/*/<resource>"
```

2. **Verify Lambda role has required service permissions** before deployment:
- SES for email sending
- CloudWatch Logs for logging
- DynamoDB for database access
- S3 for file operations

3. **Test Lambda directly first** before testing through API Gateway:
```bash
aws lambda invoke \
  --function-name contact-form-api \
  --payload '{"httpMethod":"POST","body":"{}"}' \
  response.json
```

4. **Check CloudWatch logs** to verify Lambda is executing:
```bash
aws logs tail /aws/lambda/contact-form-api --follow
```

### Related Files
- `contact_form_api/index.py` - Lambda function code
- `deploy-contact-form.ps1` - Deployment script
- `book.html` - Frontend form using the API

## Summary

1. **Scripture Lookup**: Redeploy articles-api Lambda with requests library
2. **Token Expiration**: Add checkTokenExpiration() to create/edit article pages
3. **Author Names**: Update articles_api create_article() + run migration script
4. **Pennsylvania Duplicates**: Use clean slate upload, verify chunk data, deduplicate before upload
5. **Missing Emojis**: Update templates with emoji formatting, regenerate chunks
6. **Lambda Not Invoked**: Add API Gateway invoke permission + required IAM policies

All issues have been fixed before - this guide consolidates the solutions.
