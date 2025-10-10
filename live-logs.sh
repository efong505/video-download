#!/bin/bash

TASK_ID="$1"

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
        else
            echo "💡 Usage: $0 TASK_ID"
            exit 0
        fi
    else
        echo "❌ No running downloads found"
        exit 0
    fi
fi

echo "📺 Live Download Logs for Task: $TASK_ID"
echo "Press Ctrl+C to stop monitoring"
echo ""

LOG_STREAM="ecs/video-downloader/$TASK_ID"
START_TIME=$(date -d '5 minutes ago' +%s)000

while true; do
    LOGS=$(aws logs get-log-events --log-group-name "/ecs/video-downloader" --log-stream-name "$LOG_STREAM" --start-time "$START_TIME" --query "events[*].[timestamp,message]" --output json 2>/dev/null)
    
    if [ $? -eq 0 ] && [ "$LOGS" != "[]" ]; then
        echo "$LOGS" | jq -r '.[] | @base64' | while read -r log; do
            decoded=$(echo "$log" | base64 -d)
            timestamp=$(echo "$decoded" | jq -r '.[0]')
            message=$(echo "$decoded" | jq -r '.[1]')
            
            # Convert timestamp to readable format
            readable_time=$(date -d "@$(echo "$timestamp / 1000" | bc)" +"%H:%M:%S")
            
            # Color code messages
            if echo "$message" | grep -q '\[download\]'; then
                echo -e "\033[32m[$readable_time] $message\033[0m"  # Green for download progress
            elif echo "$message" | grep -q -i 'error\|failed'; then
                echo -e "\033[31m[$readable_time] $message\033[0m"  # Red for errors
            elif echo "$message" | grep -q -i 'complete\|success\|uploaded'; then
                echo -e "\033[36m[$readable_time] $message\033[0m"  # Cyan for completion
            else
                echo "[$readable_time] $message"
            fi
            
            START_TIME=$((timestamp + 1))
        done
    fi
    
    sleep 2
done