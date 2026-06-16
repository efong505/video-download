import boto3
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Assume role into child account
sts = boto3.Session(profile_name='ekewaka').client('sts')
response = sts.assume_role(
    RoleArn='arn:aws:iam::846247542066:role/OrganizationAccountAccessRole',
    RoleSessionName='find-api-session'
)

creds = response['Credentials']

# Create API Gateway client with assumed credentials
apigw = boto3.client(
    'apigateway',
    region_name='us-east-1',
    aws_access_key_id=creds['AccessKeyId'],
    aws_secret_access_key=creds['SecretAccessKey'],
    aws_session_token=creds['SessionToken']
)

# Search for niexv1rw75
apis = apigw.get_rest_apis()
for api in apis['items']:
    if api['id'] == 'niexv1rw75':
        print(f"✓ FOUND: {api['id']} - {api['name']}")
        print(f"  Account: 846247542066 (aws-ekewaka-child)")
        
        # Get resources
        resources = apigw.get_resources(restApiId=api['id'])
        print(f"\n  Resources:")
        for r in resources['items']:
            print(f"    {r['path']}")
        break
else:
    print("✗ API niexv1rw75 NOT found in account 846247542066")
