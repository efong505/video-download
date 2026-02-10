# Video Analytics & Playlists Implementation

## Overview
Implemented two key video features: **Video Analytics Dashboard** and **Video Playlists/Collections**.

## Feature 1: Video Analytics Dashboard ✅

### Components Created
1. **DynamoDB Table**: `video-analytics`
   - Tracks individual video views with timestamp
   - Schema: video_id (PK), timestamp (SK), date

2. **TAG API Enhancement**: `tag_api/index.py`
   - `track_view` action: Records video views
   - `analytics` action: Returns top videos and stats
   - Updates view_count in video-metadata table

3. **Analytics Dashboard**: `video-analytics.html`
   - Total views, total videos, avg views per video
   - Top 10 videos with view counts
   - Clean purple gradient design

4. **View Tracking**: `videos.html`
   - Automatic tracking when video plays
   - Minimal overhead, fire-and-forget

### Deployment
```powershell
.\deploy-video-analytics.ps1
```

### Access
https://christianconservativestoday.com/video-analytics.html

---

## Feature 2: Video Playlists ✅

### Components Created
1. **DynamoDB Table**: `video-playlists`
   - Schema: playlist_id (PK), name, description, owner, videos[], created_at

2. **Playlists API**: `playlists_api/index.py`
   - Actions: create, list, get, update, delete
   - add_video, remove_video
   - Owner-based filtering

3. **Playlists Page**: `playlists.html`
   - Create/edit/delete playlists
   - View playlist cards with video count
   - User-specific playlists

### Deployment
```powershell
.\deploy-playlists.ps1
```

**Note**: Update `PLAYLISTS_API` URL in playlists.html after creating API Gateway endpoint.

---

## Database Schema

### video-analytics
```
video_id: String (PK)
timestamp: Number (SK)
date: String
```

### video-playlists
```
playlist_id: String (PK)
name: String
description: String
owner: String
videos: List<String>
created_at: String
```

### video-metadata (enhanced)
```
... existing fields ...
view_count: Number (new)
```

---

## API Endpoints

### TAG API (Enhanced)
- `POST /tags?action=track_view` - Track video view
- `GET /tags?action=analytics` - Get analytics data
- `GET /tags?action=analytics&video_id=X` - Get specific video stats

### Playlists API (New)
- `POST /playlists?action=create` - Create playlist
- `GET /playlists?action=list&owner=X` - List user playlists
- `GET /playlists?action=get&playlist_id=X` - Get playlist details
- `POST /playlists?action=update` - Update playlist
- `POST /playlists?action=delete&playlist_id=X` - Delete playlist
- `POST /playlists?action=add_video` - Add video to playlist
- `POST /playlists?action=remove_video` - Remove video from playlist

---

## Next Steps

1. **Deploy Analytics**:
   ```powershell
   python create_video_analytics_table.py
   .\deploy-video-analytics.ps1
   ```

2. **Deploy Playlists**:
   ```powershell
   python create_playlists_table.py
   .\deploy-playlists.ps1
   ```

3. **Create API Gateway** for playlists-api Lambda

4. **Update playlists.html** with correct API Gateway URL

5. **Add Playlist Button** to videos.html (optional enhancement)

---

## Future Enhancements

### Analytics
- [ ] Watch time tracking
- [ ] Geographic data
- [ ] Referrer tracking
- [ ] Export analytics to CSV

### Playlists
- [ ] Public/private playlists
- [ ] Playlist sharing
- [ ] Playlist view page with video player
- [ ] Drag-and-drop video ordering
- [ ] Add to playlist button on video cards

---

## Files Created

**Analytics**:
- create_video_analytics_table.py
- tag_api/index.py (modified)
- video-analytics.html
- videos.html (modified)
- deploy-video-analytics.ps1

**Playlists**:
- create_playlists_table.py
- playlists_api/index.py
- playlists.html
- deploy-playlists.ps1

**Documentation**:
- docs/VIDEO_FEATURES_IMPLEMENTATION.md
