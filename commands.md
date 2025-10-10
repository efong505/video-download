# Here are the complete commands for both Bash and PowerShell:

## **Bash Commands**

### **1. Start Download**
```bash
# Basic download
curl -X POST https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "format": "best",
    "output_name": "my_video.mp4"
  }'

# Save task_id for progress tracking
RESPONSE=$(curl -s -X POST https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://rumble.com/v6zwc14--flyover-conservatives-10.6.25-10pm.html",
    "format": "720p", 
    "output_name": "video.mp4"
  }')

TASK_ID=$(echo $RESPONSE | jq -r '.task_id // empty')
echo "Task ID: $TASK_ID"
```

### **2. Check Progress**
```bash
# Check status once
curl -s https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/status/$TASK_ID | jq

# Monitor progress (polls every 10 seconds)
while true; do
  STATUS=$(curl -s https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/status/$TASK_ID)
  echo "$(date): $(echo $STATUS | jq -r '.progress // "Unknown"') - $(echo $STATUS | jq -r '.speed // "Unknown"')"
  
  if [[ $(echo $STATUS | jq -r '.status') == "completed" ]] || [[ $(echo $STATUS | jq -r '.status') == "failed" ]]; then
    break
  fi
  
  sleep 10
done
```

## **PowerShell Commands**

### **1. Start Download**
```powershell
# Basic download
$body = @{
    url = "https://www.youtube.com/watch?v=VIDEO_ID"
    format = "best"
    output_name = "my_video.mp4"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download" -Method POST -ContentType "application/json" -Body $body

# Save task_id for progress tracking
$body = @{
    url = "https://rumble.com/v6zwc14--flyover-conservatives-10.6.25-10pm.html"
    format = "720p"
    output_name = "video.mp4"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download" -Method POST -ContentType "application/json" -Body $body
$taskId = $response.task_id
Write-Host "Task ID: $taskId"
```

### **2. Check Progress**
```powershell
# Check status once
Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/status/$taskId"

# Monitor progress (polls every 10 seconds)
do {
    $status = Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/status/$taskId"
    Write-Host "$(Get-Date -Format 'HH:mm:ss'): $($status.progress) - $($status.speed)"
    
    if ($status.status -eq "completed" -or $status.status -eq "failed") {
        break
    }
    
    Start-Sleep 10
} while ($true)
```

## **Complete Example Workflows**

### **Bash Complete Workflow**
```bash
#!/bin/bash
# Download and monitor progress

echo "Starting download..."
RESPONSE=$(curl -s -X POST https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://rumble.com/v6zwc14--flyover-conservatives-10.6.25-10pm.html",
    "format": "best",
    "output_name": "flyover_conservatives.mp4"
  }')

echo "Response: $(echo $RESPONSE | jq)"

TASK_ID=$(echo $RESPONSE | jq -r '.task_id // empty')

if [ -n "$TASK_ID" ]; then
    echo "Monitoring progress for task: $TASK_ID"
    
    while true; do
        STATUS=$(curl -s https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/status/$TASK_ID)
        PROGRESS=$(echo $STATUS | jq -r '.progress // "Unknown"')
        SPEED=$(echo $STATUS | jq -r '.speed // "Unknown"')
        STATE=$(echo $STATUS | jq -r '.status // "Unknown"')
        
        echo "$(date '+%H:%M:%S'): [$STATE] $PROGRESS @ $SPEED"
        
        if [[ "$STATE" == "completed" ]] || [[ "$STATE" == "failed" ]]; then
            echo "Download $STATE!"
            break
        fi
        
        sleep 10
    done
else
    echo "No task ID - likely completed via Lambda"
fi
```

### **PowerShell Complete Workflow**
```powershell
# Download and monitor progress

Write-Host "Starting download..."
$body = @{
    url = "https://rumble.com/v6zwc14--flyover-conservatives-10.6.25-10pm.html"
    format = "best"
    output_name = "flyover_conservatives.mp4"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download" -Method POST -ContentType "application/json" -Body $body

Write-Host "Response:" ($response | ConvertTo-Json -Depth 3)

$taskId = $response.task_id

if ($taskId) {
    Write-Host "Monitoring progress for task: $taskId"
    
    do {
        $status = Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/status/$taskId"
        
        Write-Host "$(Get-Date -Format 'HH:mm:ss'): [$($status.status)] $($status.progress) @ $($status.speed)"
        
        if ($status.status -eq "completed" -or $status.status -eq "failed") {
            Write-Host "Download $($status.status)!"
            break
        }
        
        Start-Sleep 10
    } while ($true)
} else {
    Write-Host "No task ID - likely completed via Lambda"
}
```

## **Quick Commands**

### **One-liner Download (Bash)**
```bash
curl -X POST https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download -H "Content-Type: application/json" -d '{"url":"YOUR_URL","format":"best","output_name":"video.mp4"}' | jq
```

### **One-liner Download (PowerShell)**
```powershell
Invoke-RestMethod -Uri "https://qdk8y6nna6.execute-api.us-east-1.amazonaws.com/prod/download" -Method POST -ContentType "application/json" -Body '{"url":"YOUR_URL","format":"best","output_name":"video.mp4"}'
```

These commands give you complete control over video downloads with real-time progress monitoring!
