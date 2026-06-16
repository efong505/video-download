import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

# Upload file
try:
    s3_client.upload_file('test.txt')
    print("Upload successful")
except ClientError as e:
    print(f"Upload failed: {e}")

# Download file
try:
    s3_client.download_file('test.txt')
    print("Download successful")
except ClientError as e:
    print(f"Download failed: {e}")

# List objects
response = s3_client.list_objects_v2(Bucket='demo-ekewaka-v3-event-notifications')
for obj in response.get('Contents', []):
    print(obj['Key'])

# Multipart upload with retry logic
from botocore.config import Config

config = Config(
    retries={'max_attempts': 10, 'mode': 'adaptive'},
    max_pool_connections=50
)

s3_client = boto3.client('s3', config=config)
