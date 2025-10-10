#!/bin/bash

FORCE_FARGATE=false
FORMAT="auto"

while [[ $# -gt 0 ]]; do
    case $1 in
        --force-fargate)
            FORCE_FARGATE=true
            shift
            ;;
        --format)
            FORMAT="$2"
            shift 2
            ;;
        *)
            if [ -z "$URL" ]; then
                URL="$1"
            elif [ -z "$OUTPUT" ]; then
                OUTPUT="$1"
            fi
            shift
            ;;
    esac
done

if [ -z "$URL" ]; then
    echo "Usage: $0 'video-url' ['output-name.mp4'] [--force-fargate] [--format 'format-id']"
    echo "Examples:"
    echo "  $0 'video-url' 'video.mp4' --format 'hls-2143'  # Force 720p"
    echo "  $0 'video-url' 'video.mp4' --format 'auto'      # Auto-select best"
    exit 1
fi

OUTPUT="${OUTPUT:-video.mp4}"
API="https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod"

echo "🎥 Downloading: $URL"

FORMAT_VALUE="best"
if [ "$FORMAT" != "auto" ]; then
    FORMAT_VALUE="$FORMAT"
fi

BODY="{\"url\":\"$URL\",\"format\":\"$FORMAT_VALUE\",\"output_name\":\"$OUTPUT\""
if [ "$FORCE_FARGATE" = true ]; then
    BODY="$BODY,\"force_fargate\":true"
fi
BODY="$BODY}"

RESPONSE=$(curl -s -X POST "$API/download" -H "Content-Type: application/json" -d "$BODY")

TITLE=$(echo "$RESPONSE" | jq -r '.video_info.title // "Unknown"')
METHOD=$(echo "$RESPONSE" | jq -r '.routing.method // "Unknown"')
COST=$(echo "$RESPONSE" | jq -r '.cost_estimate.total_usd // "Unknown"')
TASK_ID=$(echo "$RESPONSE" | jq -r '.task_id // null')

echo "✅ Started: $TITLE"
echo "🔀 Method: $METHOD"
if [ "$FORCE_FARGATE" = true ]; then
    echo "⚡ Forced Fargate routing"
fi
echo "💰 Cost: $COST"

if [ "$TASK_ID" != "null" ]; then
    echo "📊 Monitoring task: $TASK_ID"
    while true; do
        sleep 5
        STATUS_RESPONSE=$(curl -s "$API/status/$TASK_ID")
        STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status // "Unknown"')
        PROGRESS=$(echo "$STATUS_RESPONSE" | jq -r '.progress // "Unknown"')
        
        echo "Status: $STATUS | $PROGRESS"
        
        if [ "$STATUS" = "STOPPED" ] || [ "$STATUS" = "FAILED" ]; then
            break
        fi
    done
fi

sleep 10
VIDEO_RESPONSE=$(curl -s "$API/video/$OUTPUT")
VIDEO_URL=$(echo "$VIDEO_RESPONSE" | jq -r '.signed_url // null')

if [ "$VIDEO_URL" != "null" ]; then
    echo "🎬 Ready: $VIDEO_URL"
else
    echo "⏳ Still processing..."
fi