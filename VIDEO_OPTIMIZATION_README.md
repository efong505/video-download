# Video Optimization Scripts

Re-optimize existing S3 videos with FFmpeg `faststart` flag for progressive streaming.

## Problem
Videos without the `faststart` flag have metadata (moov atom) at the END of the file, requiring full download before playback starts.

## Solution
These scripts add the `faststart` flag to move metadata to the BEGINNING, enabling instant progressive playback.

---

## Scripts

### PowerShell (Windows) - **RECOMMENDED**
```powershell
.\optimize-existing-videos.ps1
```

### Python (Cross-platform)
```bash
python optimize-existing-videos.py
```

---

## Features

✅ **Safe**: Creates `.backup` files before modifying  
✅ **Smart**: Skips already-optimized videos  
✅ **Fast**: Uses `-c copy` (no re-encoding)  
✅ **Filtered**: Choose which videos to optimize by size  
✅ **Progress**: Shows real-time progress and results  

---

## Usage

### Step 1: Run Script
```powershell
cd c:\Users\Ed\Documents\Programming\AWS\Downloader
.\optimize-existing-videos.ps1
```

### Step 2: Choose Filter
```
Filter options:
1. Optimize ALL videos
2. Optimize videos larger than 100 MB
3. Optimize videos larger than 500 MB
4. Optimize videos larger than 1 GB
5. Exit

Select option (1-5):
```

**Recommendation**: Start with option 4 (1GB+) for biggest impact

### Step 3: Confirm
```
Will optimize 15 videos

Continue? (yes/no): yes
```

### Step 4: Wait
Script will:
1. Download video from S3
2. Check if already optimized (skip if yes)
3. Run FFmpeg with `-movflags +faststart`
4. Create backup (`.backup` suffix)
5. Upload optimized version
6. Show progress

---

## Example Output

```
[1/15] sermon-2024-01-15.mp4 (1250.5 MB)
  Downloading...
  Downloaded: 1250.5 MB
  Optimizing with FFmpeg...
  Optimized: 1250.5 MB
  Creating backup...
  Uploading optimized version...
  ✓ Optimized and uploaded

[2/15] conference-keynote.mp4 (850.2 MB)
  Downloading...
  Downloaded: 850.2 MB
  ✓ Already optimized, skipping
```

---

## Results Summary

```
OPTIMIZATION COMPLETE
✓ Success:  12
⊘ Skipped:  2 (already optimized)
✗ Failed:   1
⚠ Error:    0

Backups created with .backup suffix
```

---

## Performance Impact

### Before Optimization
- **Large videos (1GB+)**: Must download fully before playback
- **User experience**: Long wait, buffering
- **Bounce rate**: High (users leave)

### After Optimization
- **Large videos (1GB+)**: Start playing in 1-2 seconds
- **User experience**: Instant playback, smooth streaming
- **Bounce rate**: Low (users stay)

---

## Technical Details

### What FFmpeg Does
```bash
ffmpeg -i input.mp4 -c copy -movflags +faststart output.mp4
```

- `-c copy`: Copy streams without re-encoding (FAST)
- `-movflags +faststart`: Move moov atom to beginning
- **Time**: 30-60 seconds per GB
- **Quality**: Identical (no re-encoding)
- **Size**: Same (just rearranging)

### File Structure

**Before (Not Optimized)**
```
[mdat - Video Data] [moov - Metadata]
↑ Must download entire file before playback
```

**After (Optimized)**
```
[moov - Metadata] [mdat - Video Data]
↑ Can start playing immediately
```

---

## Safety Features

### Backups
Every video gets a backup before modification:
```
videos/sermon.mp4         ← Optimized version
videos/sermon.mp4.backup  ← Original version
```

### Restore Backup
```bash
# Restore single video
aws s3 cp s3://my-video-downloads-bucket/videos/sermon.mp4.backup s3://my-video-downloads-bucket/videos/sermon.mp4

# Restore all videos
aws s3 cp s3://my-video-downloads-bucket/videos/ s3://my-video-downloads-bucket/videos/ --recursive --exclude "*" --include "*.backup" --metadata-directive REPLACE
```

### Delete Backups (After Verification)
```bash
# Delete all backups
aws s3 rm s3://my-video-downloads-bucket/videos/ --recursive --exclude "*" --include "*.backup"
```

---

## Requirements

### Software
- **FFmpeg**: Must be installed and in PATH
- **AWS CLI**: Configured with credentials
- **PowerShell 5.1+** (Windows) or **Python 3.6+** (cross-platform)

### Permissions
- S3 read/write access to `my-video-downloads-bucket` bucket
- Sufficient disk space (2x largest video size)

### Check FFmpeg
```bash
ffmpeg -version
```

If not installed:
- **Windows**: Download from https://ffmpeg.org/download.html
- **Linux**: `sudo apt install ffmpeg`
- **macOS**: `brew install ffmpeg`

---

## Cost Estimate

### AWS Costs
- **S3 GET**: $0.0004 per 1000 requests
- **S3 PUT**: $0.005 per 1000 requests
- **Data Transfer**: Free (same region)

**Example**: 50 videos = $0.0003 (negligible)

### Time Estimate
- **100 MB video**: ~5 seconds
- **500 MB video**: ~20 seconds
- **1 GB video**: ~40 seconds
- **5 GB video**: ~3 minutes

**Example**: 20 videos @ 1GB each = ~15 minutes

---

## Troubleshooting

### "FFmpeg not found"
Install FFmpeg and add to PATH

### "Access Denied"
Check AWS credentials: `aws s3 ls s3://my-video-downloads-bucket/videos/`

### "Disk space error"
Free up space (need 2x largest video size)

### "Timeout"
Increase timeout in script or process videos in smaller batches

### "Already optimized"
Video already has faststart flag, no action needed

---

## Recommendations

### Priority Order
1. **Start with 1GB+ videos** (biggest impact)
2. **Then 500MB+ videos** (good impact)
3. **Then 100MB+ videos** (moderate impact)
4. **Skip <100MB videos** (minimal impact)

### Best Time to Run
- **Off-peak hours**: Less user impact
- **Weekend**: More time for large batches
- **After backup**: Ensure backups exist

### Verification
After optimization, test playback:
1. Open video in browser
2. Check if playback starts immediately
3. Verify no quality loss
4. Test on slow connection

---

## Next Steps

1. **Run script** on 1GB+ videos first
2. **Test playback** on a few videos
3. **Verify results** look good
4. **Run on remaining** videos
5. **Delete backups** after 1 week (if all good)

---

## Support

Issues? Check:
1. FFmpeg installed: `ffmpeg -version`
2. AWS credentials: `aws s3 ls`
3. Disk space: `df -h` (Linux/Mac) or `Get-PSDrive` (Windows)
4. Script logs for error messages
