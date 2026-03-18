# Multi-Tenant Email System - Testing Guide

## Test Environment
- **API Gateway**: https://olmcyxwc1a.execute-api.us-east-1.amazonaws.com/prod/user-email
- **Frontend**: https://christianconservativestoday.com/user-email-dashboard.html
- **Lambda Functions**: user-email-api, email-sender
- **DynamoDB Tables**: user-email-subscribers, user-email-campaigns, user-email-events

## Test Scenarios

### 1. User Authentication Test
**Objective**: Verify JWT token validation works

**Steps**:
1. Login at https://christianconservativestoday.com/login.html
2. Check localStorage for `auth_token`
3. Navigate to user-email-dashboard.html
4. Verify dashboard loads without 401 errors

**Expected Result**: Dashboard displays quota cards with user's limits

---

### 2. Add Subscriber Test
**Objective**: Test subscriber creation with quota enforcement

**Steps**:
1. Go to user-email-subscribers.html
2. Click "Add Subscriber"
3. Fill form:
   - Email: test@example.com
   - First Name: Test
   - Last Name: User
   - Phone: 555-1234
4. Click "Add"

**Expected Result**: 
- Success message appears
- Subscriber appears in table
- Quota count increments

**Test Quota Limit**:
1. Add subscribers until quota reached
2. Try adding one more
3. Expected: Error message with upgrade prompt

---

### 3. List Subscribers Test
**Objective**: Verify data isolation (users only see their subscribers)

**Steps**:
1. Login as User A, add 3 subscribers
2. Logout, login as User B, add 2 subscribers
3. Check User A sees only 3 subscribers
4. Check User B sees only 2 subscribers

**Expected Result**: Complete data isolation between users

---

### 4. Create Campaign Test
**Objective**: Test campaign creation and draft saving

**Steps**:
1. Go to user-email-campaign-create.html
2. Enter:
   - Title: "Test Newsletter"
   - Subject: "Hello {{first_name}}!"
   - Content: "Hi {{first_name}}, this is a test. {{unsubscribe_link}}"
3. Click "Save Draft"

**Expected Result**: 
- Success message
- Campaign appears in dashboard with "draft" status

---

### 5. Send Campaign Test
**Objective**: Test email sending via SQS

**Steps**:
1. Create campaign (from Test 4)
2. Click "Send Now"
3. Confirm dialog
4. Check CloudWatch logs for email-sender Lambda
5. Check email inbox for test@example.com

**Expected Result**:
- Campaign status changes to "sending" then "sent"
- Email received with mail merge applied
- Tracking pixel present in email HTML
- Unsubscribe link works

---

### 6. Quota Enforcement Test
**Objective**: Verify monthly send limits

**Steps**:
1. Check user's email_monthly_limit (e.g., 1000)
2. Send campaigns until limit reached
3. Try sending one more campaign

**Expected Result**: Error message "Monthly email limit reached"

---

### 7. Tracking Pixel Test
**Objective**: Verify open tracking works

**Steps**:
1. Send test campaign
2. Open email in browser
3. Check DynamoDB user-email-events table
4. Look for event_type: "opened"

**Expected Result**: Event logged with correct user_id, campaign_id, subscriber_email

---

### 8. Mail Merge Test
**Objective**: Verify personalization tokens work

**Test Data**:
- Subscriber: John Doe (john@example.com)
- Campaign content: "Hello {{first_name}} {{last_name}}, your email is {{email}}"

**Expected Email**: "Hello John Doe, your email is john@example.com"

---

### 9. Unsubscribe Test
**Objective**: Test unsubscribe link functionality

**Steps**:
1. Send campaign with {{unsubscribe_link}}
2. Click unsubscribe link in email
3. Check subscriber status in DynamoDB

**Expected Result**: Status changes from "active" to "unsubscribed"

---

### 10. Delete Subscriber Test
**Objective**: Test subscriber deletion

**Steps**:
1. Go to user-email-subscribers.html
2. Click "Delete" on a subscriber
3. Confirm deletion
4. Check quota count decrements

**Expected Result**: Subscriber removed, quota updated

---

## API Testing (curl commands)

### Add Subscriber
```bash
curl -X POST "https://olmcyxwc1a.execute-api.us-east-1.amazonaws.com/prod/user-email?action=add_subscriber" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","first_name":"Test","last_name":"User"}'
```

### List Subscribers
```bash
curl "https://olmcyxwc1a.execute-api.us-east-1.amazonaws.com/prod/user-email?action=list_subscribers" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create Campaign
```bash
curl -X POST "https://olmcyxwc1a.execute-api.us-east-1.amazonaws.com/prod/user-email?action=create_campaign" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","subject":"Hello","content":"<p>Test email</p>"}'
```

### Send Campaign
```bash
curl -X POST "https://olmcyxwc1a.execute-api.us-east-1.amazonaws.com/prod/user-email?action=send_campaign" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"campaign_id":"CAMPAIGN_ID_HERE"}'
```

---

## Performance Testing

### Load Test Scenario
**Objective**: Test system under load

**Setup**:
- 10 concurrent users
- Each user adds 50 subscribers
- Each user sends 5 campaigns

**Metrics to Monitor**:
- Lambda execution time
- DynamoDB read/write capacity
- SQS queue depth
- Email delivery rate

**Expected Performance**:
- API response time: <500ms
- Email delivery: >95% success rate
- No Lambda timeouts
- No DynamoDB throttling

---

## Security Testing

### Test 1: Cross-User Data Access
**Objective**: Verify users cannot access other users' data

**Steps**:
1. Get User A's token
2. Try to list User B's subscribers using User A's token
3. Try to send User B's campaign using User A's token

**Expected Result**: All attempts fail with 403 Forbidden

### Test 2: Token Validation
**Objective**: Verify expired/invalid tokens rejected

**Steps**:
1. Use expired JWT token
2. Use malformed token
3. Use no token

**Expected Result**: All return 401 Unauthorized

---

## Monitoring & Alerts

### CloudWatch Metrics to Monitor
1. **Lambda Errors**: user-email-api, email-sender
2. **Lambda Duration**: Should be <1000ms for user-email-api
3. **SQS Queue Depth**: Should drain quickly
4. **DynamoDB Throttles**: Should be 0

### CloudWatch Logs to Check
1. `/aws/lambda/user-email-api` - API requests/responses
2. `/aws/lambda/email-sender` - Email sending logs
3. Look for ERROR, FAILED, TIMEOUT keywords

---

## Rollback Plan

### If Critical Bug Found:
1. **Disable API Gateway**: Prevents new requests
   ```bash
   aws apigateway update-stage --rest-api-id olmcyxwc1a --stage-name prod --patch-operations op=replace,path=/deploymentId,value=PREVIOUS_DEPLOYMENT_ID
   ```

2. **Stop SQS Processing**: Remove Lambda trigger
   ```bash
   aws lambda delete-event-source-mapping --uuid c7370096-7db4-4403-9e07-3bace23829f8
   ```

3. **Revert Lambda Code**: Deploy previous version
   ```bash
   aws lambda update-function-code --function-name user-email-api --s3-bucket BACKUP_BUCKET --s3-key backup.zip
   ```

---

## Success Criteria

### Technical Metrics
- ✅ Email Delivery Rate: >95%
- ✅ API Response Time: <500ms
- ✅ System Uptime: >99.9%
- ✅ Data Isolation: 100% (no cross-user leaks)

### Business Metrics
- ✅ User Adoption: 20% of paid users use email feature
- ✅ Campaigns Sent: 100+ in first month
- ✅ Subscriber Growth: 1000+ subscribers added

### User Satisfaction
- ✅ Feature Rating: >4.5/5 stars
- ✅ Support Tickets: <10% of users need help
- ✅ Churn Rate: <5% monthly

---

## Known Issues & Limitations

### Current Limitations
1. **No CSV Import**: Manual subscriber entry only (Week 1-4 scope)
2. **No Analytics Dashboard**: Basic stats only (future enhancement)
3. **No A/B Testing**: Single campaign version only
4. **No Scheduling**: Send now only, no future scheduling

### Future Enhancements (Post-Launch)
- CSV bulk import
- Advanced analytics with charts
- A/B testing for subject lines
- Campaign scheduling
- Email templates library
- Segmentation by tags

---

## Test Completion Checklist

- [ ] User authentication working
- [ ] Add subscriber with quota enforcement
- [ ] List subscribers with data isolation
- [ ] Create campaign and save draft
- [ ] Send campaign via SQS
- [ ] Quota limits enforced (subscribers and sends)
- [ ] Tracking pixel logs opens
- [ ] Mail merge tokens replaced
- [ ] Unsubscribe link works
- [ ] Delete subscriber updates quota
- [ ] API endpoints respond <500ms
- [ ] No cross-user data leaks
- [ ] CloudWatch logs show no errors
- [ ] Email delivery >95%

---

## Contact for Issues
- **Developer**: Amazon Q
- **Documentation**: docs/MULTI_TENANT_EMAIL_SYSTEM_DESIGN.md
- **API Endpoint**: https://olmcyxwc1a.execute-api.us-east-1.amazonaws.com/prod/user-email
