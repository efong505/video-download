# State Election Contributor System - Deployment Guide

## Overview
Complete state-by-state election coverage system with interactive map, contributor management, candidate profiles, and election calendar.

## Components Created

### 1. Backend API (`contributors_api/index.py`)
Lambda function managing three resources:
- **Contributors**: State correspondents with verification status
- **Candidates**: Republican candidate profiles by state
- **Events**: Election calendar (primaries, debates, rallies)

### 2. Frontend Pages
- **election-map.html**: Interactive state map for public viewing
- **admin-contributors.html**: Admin interface for managing system

## AWS Deployment Steps

### Step 1: Create DynamoDB Tables

```bash
# Contributors Table
aws dynamodb create-table \
    --table-name contributors \
    --attribute-definitions AttributeName=contributor_id,AttributeType=S \
    --key-schema AttributeName=contributor_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

# Candidates Table
aws dynamodb create-table \
    --table-name candidates \
    --attribute-definitions AttributeName=candidate_id,AttributeType=S \
    --key-schema AttributeName=candidate_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

# Election Events Table
aws dynamodb create-table \
    --table-name election-events \
    --attribute-definitions AttributeName=event_id,AttributeType=S \
    --key-schema AttributeName=event_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

### Step 2: Deploy Lambda Function

```bash
cd contributors_api
zip -r function.zip index.py
aws lambda create-function \
    --function-name contributors-api \
    --runtime python3.11 \
    --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
    --handler index.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 30
```

### Step 3: Create API Gateway

```bash
# Create REST API
aws apigateway create-rest-api --name contributors-api

# Get API ID and create resource
aws apigateway create-resource \
    --rest-api-id YOUR_API_ID \
    --parent-id ROOT_RESOURCE_ID \
    --path-part contributors

# Create methods (GET, POST, PUT, DELETE, OPTIONS)
# Link to Lambda function
# Deploy to prod stage
```

### Step 4: Update Frontend Configuration

Replace `YOUR_API_GATEWAY_URL` in both HTML files with your actual API Gateway endpoint:
- election-map.html (line 91)
- admin-contributors.html (line 127)

### Step 5: Upload to S3

```bash
aws s3 cp election-map.html s3://my-video-downloads-bucket/
aws s3 cp admin-contributors.html s3://my-video-downloads-bucket/
```

### Step 6: Add Navigation Links

Add to main navigation in videos.html, articles.html, etc.:
```html
<a href="election-map.html" class="nav-link">🗺️ Election Map</a>
```

Add to admin.html navigation:
```html
<a href="admin-contributors.html" class="nav-link">🗺️ Contributors</a>
```

## Features Implemented

### ✅ Interactive State Map
- 50 state cards with visual indicators
- Green highlight for states with active contributors
- Click to view state-specific coverage

### ✅ Contributor Management
- Admin can assign users as state correspondents
- Verification badge system
- Bio and status tracking
- Multiple contributors per state supported

### ✅ Candidate Profiles
- Republican candidate tracking by state
- Office, bio, website links
- Created by contributors or admins

### ✅ Election Calendar
- State-specific and national events
- Event types: Primary, General, Debate, Rally
- Date-sorted display

### ✅ Role-Based Access
- Public: View state coverage, candidates, events
- Contributors: Add/edit candidates and events for their state
- Admins: Full management of contributors, candidates, events

## API Endpoints

### Contributors
- `GET ?resource=contributors` - List all
- `GET ?resource=contributors&state=Texas` - Filter by state
- `POST ?resource=contributors` - Create (admin only)
- `PUT ?resource=contributors` - Update (admin only)
- `DELETE ?resource=contributors&contributor_id=ID` - Delete (admin only)

### Candidates
- `GET ?resource=candidates` - List all
- `GET ?resource=candidates&state=Texas` - Filter by state
- `POST ?resource=candidates` - Create (authenticated)
- `PUT ?resource=candidates` - Update (authenticated)
- `DELETE ?resource=candidates&candidate_id=ID` - Delete (admin only)

### Events
- `GET ?resource=events` - List all
- `GET ?resource=events&state=Texas` - Filter by state
- `POST ?resource=events` - Create (authenticated)
- `PUT ?resource=events` - Update (authenticated)
- `DELETE ?resource=events&event_id=ID` - Delete (admin only)

## Database Schema

### Contributors Table
```
contributor_id (PK)
user_email
state
status (active/inactive)
bio
verified (boolean)
created_at
updated_at
```

### Candidates Table
```
candidate_id (PK)
name
state
office
party (default: Republican)
bio
website
photo_url
status
created_by
created_at
updated_at
```

### Election Events Table
```
event_id (PK)
title
state
event_date
event_type (primary/general/debate/rally)
description
created_by
created_at
```

## Testing

1. **Create a contributor**: Use admin-contributors.html
2. **View state map**: Open election-map.html, click a state
3. **Add candidate**: As contributor or admin
4. **Add event**: As contributor or admin
5. **Verify public view**: Check election-map.html without login

## Next Steps

1. Deploy Lambda function and create DynamoDB tables
2. Set up API Gateway with CORS
3. Update API URLs in HTML files
4. Upload HTML files to S3
5. Add navigation links to existing pages
6. Test contributor workflow
7. Populate initial data for key states

## Cost Estimate

- DynamoDB: ~$1-5/month (PAY_PER_REQUEST)
- Lambda: ~$0.20/month (1M requests free tier)
- API Gateway: ~$3.50/month (1M requests)
- S3: Negligible (static files)

**Total: ~$5-10/month**
