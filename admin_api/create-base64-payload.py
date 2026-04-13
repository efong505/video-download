import json
import base64

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

# Convert to base64
payload_json = json.dumps(payload)
payload_b64 = base64.b64encode(payload_json.encode('utf-8')).decode('utf-8')

print("Base64 payload:")
print(payload_b64)
print("\nRun this command:")
print(f'aws lambda invoke --function-name router --profile child-account --region us-east-1 --payload "{payload_b64}" --cli-binary-format raw-in-base64-out response.json')
