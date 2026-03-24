# 7 Mountains Backend Integration - Phase 4 Setup Guide

## Overview
This guide walks through setting up the complete backend infrastructure for the 7 Mountains tracking system.

## Prerequisites
- AWS CLI configured with `ekewaka` profile
- Python 3.12 installed
- PowerShell (for deployment scripts)
- Access to AWS Console

---

## Step 1: Create DynamoDB Tables (5 minutes)

Run the table creation script:

```powershell
python create_mountains_tables.py
```

This creates 3 tables:
- **mountain-pledges** - Tracks user pledges per mountain
- **mountain-badges** - Stores earned badges (pledge, contributor, warrior, champion)
- **mountain-contributions** - Logs all content contributions per mountain

**Verify tables created:**
```powershell
aws dynamodb list-tables --region us-east-1 --profile ekewaka
```

You should see the 3 new tables in the output.

---

## Step 2: Create Lambda Function (10 minutes)

### Option A: AWS Console (Recommended for first time)

1. **Go to AWS Lambda Console**
   - Navigate to: https://console.aws.amazon.com/lambda
   - Click "Create function"

2. **Configure function:**
   - Function name: `mountains-api`
   - Runtime: Python 3.12
   - Architecture: x86_64
   - Execution role: Use existing role → `lambda-execution-role`

3. **Click "Create function"**

4. **Deploy code:**
   ```powershell
   .\deploy-mountains-api.ps1
   ```

5. **Configure function settings:**
   - Timeout: 30 seconds
   - Memory: 512 MB

6. **Add DynamoDB permissions:**
   - Go to Configuration → Permissions
   - Click on the execution role
   - Add policy: `AmazonDynamoDBFullAccess`

### Option B: AWS CLI (Advanced)

```powershell
# Create function
aws lambda create-function `
    --function-name mountains-api `
    --runtime python3.12 `
    --role arn:aws:iam::371751795928:role/lambda-execution-role `
    --handler index.lambda_handler `
    --zip-file fileb://mountains_api/function.zip `
    --timeout 30 `
    --memory-size 512 `
    --region us-east-1 `
    --profile ekewaka
```

---

## Step 3: Create API Gateway (15 minutes)

### Create REST API

1. **Go to API Gateway Console**
   - Navigate to: https://console.aws.amazon.com/apigateway
   - Click "Create API" → REST API → Build

2. **Configure API:**
   - API name: `mountains-api`
   - Description: "7 Mountains tracking and leaderboard API"
   - Endpoint Type: Regional

3. **Create resource:**
   - Click "Actions" → "Create Resource"
   - Resource Name: `mountains`
   - Resource Path: `/mountains`
   - Enable CORS: ✅ Check

4. **Create methods:**

   For each action, create a method:
   
   **POST /mountains** (for pledges and contributions)
   - Integration type: Lambda Function
   - Lambda Function: `mountains-api`
   - Use Lambda Proxy integration: ✅ Check

   **GET /mountains** (for getting pledges, badges, leaderboards)
   - Integration type: Lambda Function
   - Lambda Function: `mountains-api`
   - Use Lambda Proxy integration: ✅ Check

5. **Enable CORS:**
   - Select `/mountains` resource
   - Actions → Enable CORS
   - Click "Enable CORS and replace existing CORS headers"

6. **Deploy API:**
   - Actions → Deploy API
   - Deployment stage: `prod`
   - Click "Deploy"

7. **Note your API endpoint:**
   - Copy the "Invoke URL" (e.g., `https://abc123.execute-api.us-east-1.amazonaws.com/prod`)

---

## Step 4: Test API Endpoints (10 minutes)

### Test with PowerShell

```powershell
# Set your API endpoint
$API_URL = "https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod"
$TOKEN = "YOUR-JWT-TOKEN"  # Get from localStorage after logging in

# Test 1: Create a pledge
$body = @{
    mountain = "family"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$API_URL/mountains?action=create_pledge" `
    -Method POST `
    -Headers @{
        "Authorization" = "Bearer $TOKEN"
        "Content-Type" = "application/json"
    } `
    -Body $body

# Test 2: Get user pledges
Invoke-RestMethod -Uri "$API_URL/mountains?action=get_pledges" `
    -Method GET `
    -Headers @{
        "Authorization" = "Bearer $TOKEN"
    }

# Test 3: Track contribution
$body = @{
    mountain = "family"
    content_type = "video"
    content_id = "test-video-123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$API_URL/mountains?action=track_contribution" `
    -Method POST `
    -Headers @{
        "Authorization" = "Bearer $TOKEN"
        "Content-Type" = "application/json"
    } `
    -Body $body

# Test 4: Get leaderboard
Invoke-RestMethod -Uri "$API_URL/mountains?action=get_leaderboard&mountain=family" `
    -Method GET `
    -Headers @{
        "Authorization" = "Bearer $TOKEN"
    }
```

---

## Step 5: Update Frontend (Next Phase)

Once API is working, update the 7 Mountains hub pages to call these endpoints:

### JavaScript Integration Example

```javascript
const MOUNTAINS_API = 'https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/mountains';

// Take pledge
async function takePledge(mountain) {
    const token = localStorage.getItem('auth_token');
    
    const response = await fetch(`${MOUNTAINS_API}?action=create_pledge`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mountain })
    });
    
    const data = await response.json();
    
    if (data.badge_awarded) {
        alert(`🎉 Pledge taken! You earned the ${data.badge_awarded.badge_type} badge!`);
    }
}

// Get user badges
async function loadBadges() {
    const token = localStorage.getItem('auth_token');
    
    const response = await fetch(`${MOUNTAINS_API}?action=get_badges`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    const data = await response.json();
    displayBadges(data.badges);
}

// Track contribution (call when user uploads content)
async function trackContribution(mountain, contentType, contentId) {
    const token = localStorage.getItem('auth_token');
    
    const response = await fetch(`${MOUNTAINS_API}?action=track_contribution`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            mountain,
            content_type: contentType,
            content_id: contentId
        })
    });
    
    const data = await response.json();
    
    if (data.badge_awarded) {
        alert(`🏆 New badge earned: ${data.badge_awarded.badge_type}!`);
    }
}

// Load leaderboard
async function loadLeaderboard(mountain) {
    const token = localStorage.getItem('auth_token');
    
    const response = await fetch(`${MOUNTAINS_API}?action=get_leaderboard&mountain=${mountain}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    
    const data = await response.json();
    displayLeaderboard(data.leaderboard);
}
```

---

## API Endpoints Reference

### 1. Create Pledge
**Endpoint:** `POST /mountains?action=create_pledge`  
**Body:**
```json
{
    "mountain": "family"
}
```
**Response:**
```json
{
    "message": "Pledge recorded for family mountain",
    "pledge": { ... },
    "badge_awarded": { ... }
}
```

### 2. Get User Pledges
**Endpoint:** `GET /mountains?action=get_pledges`  
**Response:**
```json
{
    "pledges": [
        {
            "user_id": "...",
            "mountain": "family",
            "pledge_date": "2025-01-23T10:30:00",
            "active": true
        }
    ]
}
```

### 3. Award Badge
**Endpoint:** `POST /mountains?action=award_badge`  
**Body:**
```json
{
    "mountain": "family",
    "badge_type": "warrior"
}
```

### 4. Get User Badges
**Endpoint:** `GET /mountains?action=get_badges`  
**Response:**
```json
{
    "badges": [
        {
            "badge_id": "...",
            "user_id": "...",
            "mountain": "family",
            "badge_type": "pledge",
            "earned_date": "2025-01-23T10:30:00"
        }
    ]
}
```

### 5. Track Contribution
**Endpoint:** `POST /mountains?action=track_contribution`  
**Body:**
```json
{
    "mountain": "family",
    "content_type": "video",
    "content_id": "video-123"
}
```
**Response:**
```json
{
    "message": "Contribution tracked for family mountain",
    "contribution": { ... },
    "total_contributions": 5,
    "badge_awarded": { ... }  // Only if milestone reached
}
```

### 6. Get Leaderboard
**Endpoint:** `GET /mountains?action=get_leaderboard&mountain=family`  
**Response:**
```json
{
    "mountain": "family",
    "leaderboard": [
        {
            "user_id": "...",
            "name": "John Doe",
            "email": "john@example.com",
            "contribution_count": 42
        }
    ]
}
```

---

## Badge System

Badges are automatically awarded based on activity:

| Badge Type | Requirement | When Awarded |
|------------|-------------|--------------|
| **Pledge** | Take pledge | Immediately when pledge created |
| **Contributor** | 5 contributions | After 5th contribution to a mountain |
| **Warrior** | 25 contributions | After 25th contribution to a mountain |
| **Champion** | 100 contributions | After 100th contribution to a mountain |

---

## Troubleshooting

### Issue: "Unauthorized" error
**Solution:** Ensure JWT token is valid and included in Authorization header

### Issue: "Invalid mountain" error
**Solution:** Mountain must be one of: family, religion, education, media, art, economics, government

### Issue: Lambda timeout
**Solution:** Increase Lambda timeout to 30 seconds in function configuration

### Issue: DynamoDB access denied
**Solution:** Add AmazonDynamoDBFullAccess policy to lambda-execution-role

### Issue: CORS errors
**Solution:** Enable CORS on API Gateway and redeploy

---

## Cost Estimate

**DynamoDB:**
- On-demand pricing: $0.25 per million write requests
- Expected: <$1/month for first 1000 users

**Lambda:**
- Free tier: 1M requests/month
- Expected: Free for first year

**API Gateway:**
- Free tier: 1M requests/month
- Expected: Free for first year

**Total estimated cost:** <$1/month

---

## Next Steps

After Phase 4 is complete:

1. ✅ Test all 6 API endpoints
2. ✅ Verify badges are awarded correctly
3. ✅ Check leaderboards populate
4. 🔄 Update frontend hub pages with API calls
5. 🔄 Add pledge buttons to landing page
6. 🔄 Display user badges on profile page
7. 🔄 Show leaderboards on each mountain hub

Then proceed to **Phase 5: Templates & Resources**

---

## Support

If you encounter issues:
1. Check CloudWatch Logs for Lambda errors
2. Verify DynamoDB tables exist and have correct schema
3. Test API endpoints with Postman before frontend integration
4. Ensure JWT tokens are valid and not expired
