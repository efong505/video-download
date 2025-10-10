#!/bin/bash

echo "🔍 Getting latest task logs..."

# Get logs from the known latest stream
aws logs get-log-events --log-group-name "/ecs/video-downloader" --log-stream-name "ecs/video-downloader/11eaa74b5bd647e0b310d29d967bc722" --query "events[].message" --output text