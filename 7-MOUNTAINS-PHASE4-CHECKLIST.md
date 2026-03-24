# 7 Mountains Phase 4 - Implementation Checklist

## Pre-Implementation ✅

- [x] Phase 1 complete (Landing page)
- [x] Phase 2 complete (7 mountain hub pages)
- [x] Phase 3 complete (Navigation integration)
- [x] Backend code written
- [x] Documentation created
- [x] Deployment scripts ready

---

## Database Setup (5 minutes)

- [ ] Run `python create_mountains_tables.py`
- [ ] Verify 3 tables created in DynamoDB console
- [ ] Check tables are in "Active" status
- [ ] Confirm on-demand billing mode

**Tables to verify:**
- [ ] mountain-pledges
- [ ] mountain-badges  
- [ ] mountain-contributions

---

## Lambda Deployment (10 minutes)

- [ ] Navigate to `mountains_api` directory
- [ ] Run `.\deploy-mountains-api.ps1`
- [ ] Verify function created in Lambda console
- [ ] Check function name is `mountains-api`
- [ ] Confirm runtime is Python 3.12
- [ ] Verify timeout is 30 seconds
- [ ] Check memory is 512 MB
- [ ] Confirm execution role is `lambda-execution-role`

**Permissions to verify:**
- [ ] DynamoDB Full Access attached to role
- [ ] CloudWatch Logs access (automatic)

---

## API Gateway Setup (15 minutes)

### Create API
- [ ] Go to API Gateway console
- [ ] Create new REST API
- [ ] Name: `mountains-api`
- [ ] Endpoint type: Regional

### Create Resource
- [ ] Create resource `/mountains`
- [ ] Enable CORS on resource

### Create Methods
- [ ] Add POST method
  - [ ] Integration type: Lambda Function
  - [ ] Lambda: `mountains-api`
  - [ ] Use Lambda Proxy integration: ✅
- [ ] Add GET method
  - [ ] Integration type: Lambda Function
  - [ ] Lambda: `mountains-api`
  - [ ] Use Lambda Proxy integration: ✅

### Enable CORS
- [ ] Select `/mountains` resource
- [ ] Actions → Enable CORS
- [ ] Accept default headers
- [ ] Click "Enable CORS and replace existing CORS headers"

### Deploy API
- [ ] Actions → Deploy API
- [ ] Stage: `prod`
- [ ] Click "Deploy"
- [ ] Copy Invoke URL
- [ ] Save URL for frontend integration

**API URL:** `https://____________.execute-api.us-east-1.amazonaws.com/prod`

---

## Testing (10 minutes)

### Test 1: Create Pledge
- [ ] Get JWT token from localStorage after login
- [ ] Use Postman or PowerShell to test
- [ ] Endpoint: `POST /mountains?action=create_pledge`
- [ ] Body: `{"mountain": "family"}`
- [ ] Verify 200 response
- [ ] Check pledge created in DynamoDB
- [ ] Confirm badge awarded

### Test 2: Get Pledges
- [ ] Endpoint: `GET /mountains?action=get_pledges`
- [ ] Verify returns array of pledges
- [ ] Check pledge from Test 1 is included

### Test 3: Track Contribution
- [ ] Endpoint: `POST /mountains?action=track_contribution`
- [ ] Body: `{"mountain": "family", "content_type": "video", "content_id": "test-123"}`
- [ ] Verify 200 response
- [ ] Check contribution logged in DynamoDB

### Test 4: Get Badges
- [ ] Endpoint: `GET /mountains?action=get_badges`
- [ ] Verify returns array of badges
- [ ] Check "pledge" badge from Test 1 is included

### Test 5: Get Leaderboard
- [ ] Endpoint: `GET /mountains?action=get_leaderboard&mountain=family`
- [ ] Verify returns leaderboard array
- [ ] Check your user appears with contribution count

### Test 6: Badge Milestones
- [ ] Track 5 contributions to same mountain
- [ ] Verify "contributor" badge awarded
- [ ] Track 25 contributions
- [ ] Verify "warrior" badge awarded

---

## Frontend Integration (Phase 5 prep)

### Update Hub Pages
- [ ] Add pledge button to each mountain hub
- [ ] Add JavaScript function `takePledge(mountain)`
- [ ] Display success message when pledge taken
- [ ] Show badge earned notification

### Update Upload Forms
- [ ] Add mountain dropdown to video upload
- [ ] Add mountain dropdown to article creation
- [ ] Call `trackContribution()` after successful upload
- [ ] Show badge notification if milestone reached

### Profile Page
- [ ] Add badges section
- [ ] Load user badges with `getUserBadges()`
- [ ] Display badge icons with mountain names
- [ ] Show badge earned dates

### Leaderboard Sections
- [ ] Add leaderboard tab to each mountain hub
- [ ] Load leaderboard with `getLeaderboard(mountain)`
- [ ] Display top 50 contributors
- [ ] Show contribution counts
- [ ] Highlight current user if in top 50

---

## Documentation Review

- [ ] Read `7-MOUNTAINS-PHASE4-SETUP.md`
- [ ] Review `7-MOUNTAINS-API-REFERENCE.md`
- [ ] Check `7-MOUNTAINS-PHASE4-SUMMARY.md`
- [ ] Understand all 6 API endpoints
- [ ] Know badge progression system
- [ ] Understand contribution tracking

---

## Production Deployment

### Backend
- [ ] All DynamoDB tables active
- [ ] Lambda function deployed
- [ ] API Gateway configured
- [ ] All endpoints tested
- [ ] CORS working correctly

### Frontend (Next Phase)
- [ ] Hub pages updated with pledge buttons
- [ ] Upload forms track contributions
- [ ] Profile displays badges
- [ ] Leaderboards show on hubs
- [ ] All JavaScript functions working

### Testing
- [ ] Test pledge flow end-to-end
- [ ] Test contribution tracking
- [ ] Test badge awards
- [ ] Test leaderboard display
- [ ] Test on mobile devices
- [ ] Test with multiple users

---

## Post-Launch Monitoring

### Week 1
- [ ] Monitor CloudWatch Logs for errors
- [ ] Check DynamoDB table sizes
- [ ] Verify badge awards working
- [ ] Track API usage
- [ ] Gather user feedback

### Week 2
- [ ] Review leaderboard accuracy
- [ ] Check contribution counts
- [ ] Verify pledge tracking
- [ ] Monitor costs (should be <$1)
- [ ] Plan Phase 5 templates

---

## Success Criteria

Phase 4 is complete when:

✅ All 3 DynamoDB tables exist and active  
✅ Lambda function deployed successfully  
✅ API Gateway configured with 6 endpoints  
✅ All endpoints tested and working  
✅ Badges auto-award at milestones  
✅ Leaderboards populate correctly  
✅ Documentation complete  
✅ Ready for frontend integration  

---

## Troubleshooting

### Issue: Tables not creating
**Check:** AWS credentials configured correctly  
**Fix:** Run `aws configure` with ekewaka profile

### Issue: Lambda deployment fails
**Check:** PyJWT installed in mountains_api directory  
**Fix:** Run `pip install PyJWT -t mountains_api`

### Issue: API Gateway 403 errors
**Check:** Lambda permissions  
**Fix:** Add Lambda invoke permission to API Gateway

### Issue: CORS errors
**Check:** CORS enabled on API Gateway  
**Fix:** Enable CORS and redeploy API

### Issue: Unauthorized errors
**Check:** JWT token valid  
**Fix:** Login again to get fresh token

---

## Time Estimates

| Task | Time |
|------|------|
| Database setup | 5 min |
| Lambda deployment | 10 min |
| API Gateway setup | 15 min |
| Testing | 10 min |
| **Total** | **40 min** |

---

## Next Phase

After Phase 4 complete:

**Phase 5: Templates & Resources** (1-2 hours)
- Create ministry templates per mountain
- Add template selector to upload forms
- Pre-fill content based on mountain
- Launch beta testing

---

## Quick Start

Run this command to start:
```powershell
.\setup-phase4.ps1
```

This will guide you through all steps automatically.

---

**Status:** Ready to implement ✅  
**Estimated completion:** 40 minutes  
**Next phase:** Templates & Resources (Phase 5)
