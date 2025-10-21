# Article Analytics & View Tracking

## Overview
Comprehensive analytics system for tracking article performance, engagement metrics, and content insights.

## Features

### View Tracking
- **Automatic View Counting**: Every article view increments the view counter
- **Real-time Updates**: View counts update immediately when articles are accessed
- **Persistent Storage**: View counts stored in DynamoDB articles table

### Analytics Dashboard (Admin)
Located in Admin Dashboard → Analytics tab

**Overall Statistics:**
- Total Articles count
- Total Views across all articles
- Average Views per Article

**Top 10 Most Viewed Articles:**
- Ranked list of most popular content
- Shows title, author, category, and view count
- Direct links to view articles

**Category Performance:**
- Articles count per category
- Total views per category
- Average views per category
- Sorted by total views (highest first)

### Public Display
**Articles Listing Page:**
- View count displayed on each article card
- Format: "👁️ X views" in article metadata
- Visible to all users

**Individual Article Page:**
- View count shown in article metadata
- Updates on each page load

## Technical Implementation

### Backend (articles_api/index.py)

**View Count Increment:**
```python
# In get_article() function
articles_table.update_item(
    Key={'article_id': article_id},
    UpdateExpression='SET view_count = if_not_exists(view_count, :zero) + :inc',
    ExpressionAttributeValues={':inc': 1, ':zero': 0}
)
```

**Analytics Endpoint:**
- **URL**: `GET /articles?action=analytics`
- **Query Parameters**:
  - `article_id` (optional): Get analytics for specific article
  - No parameters: Get overall analytics

**Response Format:**
```json
{
  "analytics": {
    "total_articles": 45,
    "total_views": 1250,
    "average_views": 27.8,
    "top_articles": [
      {
        "article_id": "abc123",
        "title": "Article Title",
        "view_count": 150,
        "author": "John Doe",
        "category": "sermon"
      }
    ],
    "category_stats": {
      "sermon": {
        "count": 10,
        "views": 450
      }
    }
  }
}
```

### Frontend

**Admin Dashboard (admin.html):**
- New "Analytics" tab between Articles and Resources
- Loads analytics on tab activation
- Displays stats cards and tables
- Category performance breakdown

**Articles Page (articles.html):**
- View count in article card metadata
- Format: `<span class="ms-3">👁️ ${viewCount} views</span>`

**Article Page (article.html):**
- View count in article header metadata
- Increments automatically on page load

## Database Schema

**articles table:**
```
{
  "article_id": "string",
  "title": "string",
  "content": "string",
  "author": "string",
  "view_count": number,  // Default: 0
  "likes_count": number, // Default: 0
  "created_at": "ISO timestamp",
  ...
}
```

## Usage

### For Admins
1. Navigate to Admin Dashboard
2. Click "Analytics" tab
3. View overall statistics and top articles
4. Review category performance
5. Click "View" button to see specific articles

### For Authors
- View counts visible on articles listing page
- Track your article performance
- Compare with other articles in same category

### For Readers
- See which articles are most popular
- View counts help identify trending content
- Engagement metrics visible on all public articles

## Metrics Tracked

### Current Metrics
- **View Count**: Total number of times article has been viewed
- **Likes Count**: Placeholder for future like functionality
- **Reading Time**: Estimated reading time in minutes
- **Category**: Article category for grouping
- **Tags**: Article tags for filtering

### Future Enhancements
- Time-based analytics (views per day/week/month)
- User engagement tracking (time spent reading)
- Comment count integration
- Share count tracking
- Geographic analytics
- Referral source tracking

## Performance Considerations

- View count updates use conditional expressions to handle missing fields
- Analytics endpoint scans entire articles table (consider pagination for large datasets)
- Client-side caching not implemented (each page load fetches fresh data)
- No rate limiting on view count increments

## Security

- View counts are public information
- Analytics dashboard requires admin/super_user role
- Individual article analytics accessible to all authenticated users
- No PII stored in analytics data

## API Endpoints

**Get Overall Analytics:**
```
GET /articles?action=analytics
```

**Get Article-Specific Analytics:**
```
GET /articles?action=analytics&article_id=abc123
```

**Increment View Count:**
```
GET /articles?action=get&article_id=abc123
// View count incremented automatically
```

## Deployment Notes

- No additional Lambda functions required
- Uses existing articles_api Lambda
- No new DynamoDB tables needed
- No CloudWatch Events required
- Backward compatible with existing articles

## Testing Checklist

- [ ] View count increments on article page load
- [ ] Analytics dashboard loads without errors
- [ ] Top 10 articles display correctly
- [ ] Category stats calculate accurately
- [ ] View counts display on articles listing
- [ ] Admin-only access enforced for analytics tab
- [ ] Zero view articles handled correctly
- [ ] Large view counts format properly (1,234 vs 1234)

## Known Limitations

- No view deduplication (same user can increment multiple times)
- No bot detection or filtering
- No time-series data (can't see views over time)
- Analytics endpoint scans full table (may be slow with many articles)
- No export functionality for analytics data
