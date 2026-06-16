import boto3
import sys
sys.stdout.reconfigure(encoding='utf-8')

accounts = [
    ('ekewaka', '371751795928', None),
    ('default', '372110294325', None),
    ('child-account', '628478946937', None),
    ('ekewaka', '846247542066', 'arn:aws:iam::846247542066:role/OrganizationAccountAccessRole')
]

for profile, account_id, role_arn in accounts:
    print(f"\nChecking account {account_id} ({profile})...")
    
    try:
        if role_arn:
            # Assume role
            sts = boto3.Session(profile_name=profile).client('sts')
            response = sts.assume_role(RoleArn=role_arn, RoleSessionName='api-search')
            creds = response['Credentials']
            apigw = boto3.client(
                'apigateway',
                region_name='us-east-1',
                aws_access_key_id=creds['AccessKeyId'],
                aws_secret_access_key=creds['SecretAccessKey'],
                aws_session_token=creds['SessionToken']
            )
        else:
            # Use profile directly
            apigw = boto3.Session(profile_name=profile, region_name='us-east-1').client('apigateway')
        
        apis = apigw.get_rest_apis()
        for api in apis['items']:
            if api['id'] == 'niexv1rw75':
                print(f"  ✓ FOUND: {api['name']}")
                resources = apigw.get_resources(restApiId=api['id'])
                print(f"  Resources:")
                for r in resources['items']:
                    print(f"    {r['path']}")
                exit(0)
        
        print(f"  ✗ Not found")
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\n❌ API niexv1rw75 not found in any of the 4 accounts")
