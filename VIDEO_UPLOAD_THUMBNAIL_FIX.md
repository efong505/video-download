# Video Upload & Thumbnail Generation Fix

## Problem Summary
Videos uploaded via `user-upload.html` and `admin.html` upload forms were not triggering automatic thumbnail generation because:
1. S3 event trigger only fires for videos in `videos/` folder
2. Upload forms put videos in bucket root
3. Thumbnail generator expects videos in `videos/` folder

## Solution Overview
**Three options to fix this:**

### Option 1: Update Upload Forms to Use `videos/` Prefix (RECOMMENDED)
Modify upload forms to upload directly to `videos/` folder

### Option 2: Update S3 Trigger & Lambda to Support Root Uploads
Modify S3 event trigger and Lambda function to handle both locations

### Option 3: Manual Thumbnail Generation
Keep current setup and manually trigger thumbnails after upload

---

## Current Configuration

### S3 Event Trigger
```json
{
    "LambdaFunctionConfigurations": [
        {
            "Id": "video-upload-trigger",
            "LambdaFunctionArn": "arn:aws:lambda:us-east-1:371751795928:function:thumbnail-generator",
            "Events": ["s3:ObjectCreated:*"],
            "Filter": {
                "Key": {
                    "FilterRules": [
                        {"Name": "Prefix", "Value": "videos/"},
                        {"Name": "Suffix", "Value": ".mp4"}
                    ]
                }
            }
        }
    ]
}
```

### Thumbnail Generator Lambda
- Expects videos at: `s3://my-video-downloads-bucket/videos/{filename}`
- Generates thumbnails at: `s3://my-video-downloads-bucket/thumbnails/{filename}_thumb_2.jpg`

---

## OPTION 1: Update Upload Forms (RECOMMENDED)

### Why This Option?
- ✅ Minimal changes required
- ✅ Works with existing S3 trigger
- ✅ Automatic thumbnail generation
- ✅ Consistent with download system

### Changes Required

#### 1. Update `user-upload.html` (Line ~420)
```javascript
// BEFORE:
const urlResponse = await fetch(`${ADMIN_API}?action=upload_url`, {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ filename: filename })
});

// AFTER:
const urlResponse = await fetch(`${ADMIN_API}?action=upload_url`, {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ filename: `videos/${filename}` })  // Add videos/ prefix
});
```

#### 2. Update `admin.html` (Line ~2800)
```javascript
// BEFORE:
const urlResponse = await fetch(`${ADMIN_API}?action=upload_url`, {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({filename: filename})
});

// AFTER:
const urlResponse = await fetch(`${ADMIN_API}?action=upload_url`, {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${authToken}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({filename: `videos/${filename}`})  // Add videos/ prefix
});
```

#### 3. Update Video Metadata Storage
Both files need to store filename WITHOUT `videos/` prefix in DynamoDB:

```javascript
// After successful upload, when adding metadata:
await fetch(`${TAG_API}?action=add_video`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        video_id: filename,  // Keep original filename
        filename: filename,  // Keep original filename
        title: title || filename,
        tags: tags,
        owner: currentUser.email,
        visibility: visibility,
        size: file.size  // Add file size
    })
});
```

### Deployment
```powershell
# Push updated HTML files to S3
.\s3-push.ps1
```

---

## OPTION 2: Update S3 Trigger & Lambda

### Why This Option?
- ✅ Supports both upload locations
- ✅ More flexible
- ❌ More complex changes
- ❌ Requires Lambda redeployment

### Changes Required

#### 1. Update S3 Event Trigger
```bash
# Remove prefix filter to trigger on all .mp4 uploads
aws s3api put-bucket-notification-configuration \
  --bucket my-video-downloads-bucket \
  --notification-configuration '{
    "LambdaFunctionConfigurations": [{
      "Id": "video-upload-trigger",
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:371751795928:function:thumbnail-generator",
      "Events": ["s3:ObjectCreated:*"],
      "Filter": {
        "Key": {
          "FilterRules": [
            {"Name": "Suffix", "Value": ".mp4"}
          ]
        }
      }
    }]
  }'
```

#### 2. Update `thumbnail_generator/index.py`
```python
def process_video(bucket, filename):
    """Process a single video file"""
    base_name = filename.replace('.mp4', '')
    thumb_key = f"thumbnails/{base_name}_thumb_2.jpg"
    
    # Check both locations for video file
    video_key = None
    try:
        # Try videos/ folder first
        s3_client.head_object(Bucket=bucket, Key=f"videos/{filename}")
        video_key = f"videos/{filename}"
    except:
        try:
            # Try bucket root
            s3_client.head_object(Bucket=bucket, Key=filename)
            video_key = filename
        except:
            print(f"Video file not found: {filename}")
            return
    
    # Check if thumbnail already exists
    try:
        s3_client.head_object(Bucket=bucket, Key=thumb_key)
        print(f"Thumbnail already exists: {thumb_key}")
        return
    except:
        pass
    
    print(f"Processing video: {video_key}")
    
    # Download video from S3
    video_path = f"/tmp/{filename}"
    s3_client.download_file(bucket, video_key, video_path)
    
    # Generate thumbnails
    generate_thumbnails(video_path, filename, bucket)
    
    # Cleanup
    os.remove(video_path)
```

#### 3. Deploy Updated Lambda
```powershell
.\deploy-thumbnail-generator.ps1
```

---

## OPTION 3: Manual Thumbnail Generation

### When to Use
- Quick fix for existing videos
- One-off uploads
- Testing

### For Uploaded Videos (Bucket Root)
```bash
# Move video to videos/ folder to trigger automatic generation
aws s3 cp s3://my-video-downloads-bucket/VIDEO.mp4 s3://my-video-downloads-bucket/videos/VIDEO.mp4
```

### For Embedded Videos
```javascript
// In admin.html or user-upload.html, after adding external video:
try {
    await fetch(`${ADMIN_API}?action=generate_thumbnail`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            filename: videoId,
            video_type: videoType,  // 'youtube', 'rumble', 'facebook'
            external_url: url
        })
    });
} catch (error) {
    console.log('Thumbnail generation failed (non-critical):', error);
}
```

---

## Testing

### Test Upload Form
1. Upload a test video via `user-upload.html`
2. Wait 10-15 seconds
3. Check for thumbnail:
```bash
aws s3 ls s3://my-video-downloads-bucket/thumbnails/ | findstr test-video
```

### Test Embed Form
1. Add external video (YouTube/Rumble)
2. Check for thumbnail:
```bash
aws s3 ls s3://my-video-downloads-bucket/thumbnails/ | findstr youtube
```

### Verify Video Playback
1. Go to `videos.html`
2. Find uploaded video
3. Click play - should show thumbnail and play video

---

## Current Status

### ✅ Working
- Download from URL (via router Lambda) → Automatic thumbnails
- Manual thumbnail generation via Lambda invoke
- External video thumbnail fetching (YouTube)

### ❌ Not Working (Before Fix)
- Upload via user-upload.html → No automatic thumbnails
- Upload via admin.html → No automatic thumbnails

### ✅ Fixed (After Moving Video)
- `funny-christian-conserviative.mp4` → Thumbnail generated at `thumbnails/funny-christian-conserviative_thumb_2.jpg`

---

## Recommended Implementation

**Use Option 1** - Update upload forms to use `videos/` prefix:

1. Minimal code changes (2 lines in each file)
2. Works with existing infrastructure
3. Consistent with download system
4. Automatic thumbnail generation
5. No Lambda redeployment needed

### Implementation Steps
1. Update `user-upload.html` line ~420
2. Update `admin.html` line ~2800
3. Test with a small video file
4. Deploy to S3: `.\s3-push.ps1`
5. Verify thumbnail generation

---

## Troubleshooting

### Thumbnail Not Generated
```bash
# Check CloudWatch logs
aws logs tail /aws/lambda/thumbnail-generator --since 5m --follow

# Check if video exists
aws s3 ls s3://my-video-downloads-bucket/videos/

# Check if thumbnail exists
aws s3 ls s3://my-video-downloads-bucket/thumbnails/

# Manually trigger
aws lambda invoke --function-name thumbnail-generator \
  --payload '{"filename":"VIDEO.mp4","bucket":"my-video-downloads-bucket"}' \
  response.json
```

### Video Not Playing
```bash
# Check CloudFront URL
https://d271vky579caz9.cloudfront.net/videos/VIDEO.mp4

# Check video metadata
aws dynamodb get-item --table-name video-metadata \
  --key '{"video_id":{"S":"VIDEO.mp4"}}'
```

---

## Related Files
- `user-upload.html` - User video upload form
- `admin.html` - Admin video upload form
- `thumbnail_generator/index.py` - Thumbnail generation Lambda
- `admin_api/index.py` - Presigned URL generation
- `videos.html` - Video display page
