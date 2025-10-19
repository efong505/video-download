#!/bin/bash

# Check Download Status Script
# Monitors ECS task status and progress
# Usage: ./check-status.sh [TASK_ID]
# If no TASK_ID provided, lists all running tasks

TASK_ID="$1"
API="https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod"

if [ -z "$TASK_ID" ]; then
    echo "🔍 Finding running downloads..."
    TASKS=$(aws ecs list-tasks --cluster video-downloader-cluster --desired-status RUNNING --query "taskArns[]" --output text)
    
    if [ -n "$TASKS" ]; then
        echo "📋 Running tasks:"
        for task in $TASKS; do
            task_id=$(basename "$task")
            echo "  - $task_id"
        done
        
        task_count=$(echo "$TASKS" | wc -w)
        if [ "$task_count" -eq 1 ]; then
            TASK_ID=$(basename "$TASKS")
            echo "🎯 Checking status of: $TASK_ID"
        else
            echo "💡 Usage: $0 TASK_ID"
            exit 0
        fi
    else
        echo "❌ No running downloads found"
        exit 0
    fi
fi

echo "📊 Monitoring task: $TASK_ID"
echo "Press Ctrl+C to stop monitoring"
echo ""

while true; do
    TIMESTAMP=$(date +"%H:%M:%S")
    STATUS_RESPONSE=$(curl -s "$API/status/$TASK_ID")
    
    if [ $? -eq 0 ] && [ -n "$STATUS_RESPONSE" ]; then
        STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status // "Unknown"')
        PROGRESS=$(echo "$STATUS_RESPONSE" | jq -r '.progress // "Unknown"')
        SPEED=$(echo "$STATUS_RESPONSE" | jq -r '.speed // "Unknown"')
        ETA=$(echo "$STATUS_RESPONSE" | jq -r '.eta // "Unknown"')
        
        echo "[$TIMESTAMP] Status: $STATUS | Progress: $PROGRESS | Speed: $SPEED | ETA: $ETA"
        
        if [ "$STATUS" = "STOPPED" ]; then
            echo "✅ Download completed!"
            break
        elif [ "$STATUS" = "FAILED" ]; then
            echo "❌ Download failed!"
            break
        fi
    else
        echo "⚠️  Status check failed"
    fi
    
    sleep 3
done