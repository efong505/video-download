import boto3
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
lambda_client = session.client('lambda')

payload = {
    'manual_trigger': True,
    'user_id': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2',
    'enrollment_id': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2:election-map-transition-sequence'
}

print("Triggering Email #1 for hawaiianintucson@gmail.com...")

response = lambda_client.invoke(
    FunctionName='email-drip-processor',
    InvocationType='RequestResponse',
    Payload=json.dumps(payload)
)

result = json.loads(response['Payload'].read())
print(f"Response: {json.dumps(result, indent=2)}")
