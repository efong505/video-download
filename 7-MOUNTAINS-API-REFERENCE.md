# 7 Mountains API - Quick Reference Card

## Base URL
```
https://lcmogvl3v2.execute-api.us-east-1.amazonaws.com/prod/mountains
```

## Account
- AWS Profile: `ekewaka` (Account: 371751795928)
- Region: us-east-1

## Authentication
All endpoints require JWT token in Authorization header:
```
Authorization: Bearer YOUR_JWT_TOKEN
```

---

## Endpoints

### 1️⃣ Create Pledge
```http
POST /mountains?action=create_pledge
Content-Type: application/json

{
    "mountain": "family"
}
```
**Returns:** Pledge record + "pledge" badge

---

### 2️⃣ Get User Pledges
```http
GET /mountains?action=get_pledges
```
**Returns:** Array of all user's pledges

---

### 3️⃣ Award Badge (Admin)
```http
POST /mountains?action=award_badge
Content-Type: application/json

{
    "mountain": "family",
    "badge_type": "warrior"
}
```
**Badge Types:** pledge, contributor, warrior, champion

---

### 4️⃣ Get User Badges
```http
GET /mountains?action=get_badges
```
**Returns:** Array of all user's badges

---

### 5️⃣ Track Contribution
```http
POST /mountains?action=track_contribution
Content-Type: application/json

{
    "mountain": "family",
    "content_type": "video",
    "content_id": "abc123"
}
```
**Content Types:** video, article, prayer, event  
**Auto-awards badges:** 5 contributions = contributor, 25 = warrior, 100 = champion

---

### 6️⃣ Get Leaderboard
```http
GET /mountains?action=get_leaderboard&mountain=family
```
**Returns:** Top 50 contributors for specified mountain

---

## Valid Mountains
- `family`
- `religion`
- `education`
- `media`
- `art`
- `economics`
- `government`

---

## Badge Progression

| Badge | Requirement | Icon |
|-------|-------------|------|
| Pledge | Take pledge | 🤝 |
| Contributor | 5 contributions | ⭐ |
| Warrior | 25 contributions | ⚔️ |
| Champion | 100 contributions | 🏆 |

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid mountain/content type) |
| 401 | Unauthorized (missing/invalid token) |
| 409 | Conflict (pledge already exists) |
| 500 | Server error |

---

## JavaScript Examples

### Take Pledge
```javascript
async function takePledge(mountain) {
    const token = localStorage.getItem('auth_token');
    const response = await fetch(`${API_URL}?action=create_pledge`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ mountain })
    });
    return await response.json();
}
```

### Track Upload
```javascript
async function trackUpload(mountain, contentType, contentId) {
    const token = localStorage.getItem('auth_token');
    const response = await fetch(`${API_URL}?action=track_contribution`, {
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
    return await response.json();
}
```

### Load Leaderboard
```javascript
async function loadLeaderboard(mountain) {
    const token = localStorage.getItem('auth_token');
    const response = await fetch(`${API_URL}?action=get_leaderboard&mountain=${mountain}`, {
        method: 'GET',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    return await response.json();
}
```

---

## Testing with curl

```bash
# Create pledge
curl -X POST "https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/mountains?action=create_pledge" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mountain":"family"}'

# Get leaderboard
curl "https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/mountains?action=get_leaderboard&mountain=family" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Integration Checklist

- [x] Create DynamoDB tables
- [x] Deploy Lambda function
- [x] Create API Gateway
- [x] Test all 6 endpoints
- [x] Add pledge buttons to hub pages
- [x] Track contributions on upload
- [x] Display badges on profile
- [x] Show leaderboards on hubs
- [ ] Add badge icons to navbar
- [ ] Create badge showcase page
