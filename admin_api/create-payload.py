import json

# Create proper API Gateway event structure
payload = {
    "httpMethod": "POST",
    "body": json.dumps({
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "output_name": "test-video.mp4",
        "title": "Test Video",
        "owner": "system"
    }),
    "headers": {
        "Content-Type": "application/json"
    }
}

# Write to file with proper encoding
with open('payload.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f)

print("Payload created successfully")
