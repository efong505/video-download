#!/bin/bash

# AWS Video Downloader Script
API_BASE="https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod"

# Check if URL provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <video_url> [output_name]"
    echo "Example: $0 'https://rumble.com/video-url' 'my_video.mp4'"
    exit 1
fi

URL="$1"
OUTPUT_NAME="$2"

# Generate output name if not provided
if [ -z "$OUTPUT_NAME" ]; then
    URL_PART=$(basename "$URL" | sed 's/[^a-zA-Z0-9._-]/_/g' | cut -c1-50)
    OUTPUT_NAME="${URL_PART}.mp4"
fi

echo "🎥 AWS Video Downloader"
echo "URL: $URL"
echo "Output: $OUTPUT_NAME"
echo ""

# Start download
echo "⏳ Starting download..."
RESPONSE=$(curl -s -X POST "$API_BASE/download" \
    -H "Content-Type: application/json" \
    -d "{\"url\":\"$URL\",\"format\":\"best\",\"output_name\":\"$OUTPUT_NAME\"}")

if [ $? -ne 0 ]; then
    echo "❌ Failed to start download"
    exit 1
fi

# Parse response
TITLE=$(echo "$RESPONSE" | jq -r '.video_info.title // "Unknown"')
DURATION=$(echo "$RESPONSE" | jq -r '.video_info.duration // "Unknown"')
METHOD=$(echo "$RESPONSE" | jq -r '.routing.method // "Unknown"')
REASON=$(echo "$RESPONSE" | jq -r '.routing.reason // "Unknown"')
COST=$(echo "$RESPONSE" | jq -r '.cost_estimate.total_usd // "Unknown"')
TASK_ID=$(echo "$RESPONSE" | jq -r '.task_id // null')

echo "✅ Download initiated!"
echo "📹 Video: $TITLE"
echo "⏱️  Duration: $DURATION"
echo "🔀 Method: $METHOD ($REASON)"
echo "💰 Cost: $COST"

if [ "$TASK_ID" != "null" ] && [ "$TASK_ID" != "" ]; then
    echo "🔍 Task ID: $TASK_ID"
    echo ""
    echo "⏳ Monitoring progress..."
    
    while true; do
        sleep 5
        STATUS_RESPONSE=$(curl -s "$API_BASE/status/$TASK_ID")
        
        if [ $? -eq 0 ]; then
            STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status // "Unknown"')
            PROGRESS=$(echo "$STATUS_RESPONSE" | jq -r '.progress // "Unknown"')
            SPEED=$(echo "$STATUS_RESPONSE" | jq -r '.speed // "Unknown"')
            
            echo "📊 Status: $STATUS | Progress: $PROGRESS | Speed: $SPEED"
            
            if [ "$STATUS" = "STOPPED" ]; then
                echo "✅ Download completed!"
                break
            elif [ "$STATUS" = "FAILED" ]; then
                echo "❌ Download failed!"
                exit 1
            fi
        else
            echo "⚠️  Status check failed, retrying..."
        fi
    done
else
    echo "⏳ Lambda processing (no progress tracking)..."
    ESTIMATED_TIME=$(echo "$RESPONSE" | jq -r '.routing.estimated_time // "Unknown"')
    echo "⏱️  Estimated completion: ~$ESTIMATED_TIME"
fi

# Get video URL
echo ""
echo "🔗 Getting video URL..."
VIDEO_RESPONSE=$(curl -s "$API_BASE/video/$OUTPUT_NAME")

if [ $? -eq 0 ]; then
    VIDEO_URL=$(echo "$VIDEO_RESPONSE" | jq -r '.signed_url // null')
    
    if [ "$VIDEO_URL" != "null" ] && [ "$VIDEO_URL" != "" ]; then
        echo "🎬 Video ready!"
        echo "🔗 URL: $VIDEO_URL"
        echo "⏰ Expires: 24 hours"
    else
        echo "❌ Failed to get video URL"
    fi
else
    echo "❌ Failed to get video URL"
fi