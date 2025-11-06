import boto3
import json

# Create Lambda client
lambda_client = boto3.client('lambda')

# Trigger thumbnail generation for the specific video
payload = {
    "filename": "1000003114.mp4",
    "bucket": "my-video-downloads-bucket"
}

try:
    response = lambda_client.invoke(
        FunctionName='thumbnail-generator',
        InvocationType='Event',
        Payload=json.dumps(payload)
    )
    print(f"Thumbnail generation triggered successfully: {response}")
except Exception as e:
    print(f"Error: {e}")