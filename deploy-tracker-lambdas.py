import boto3
import zipfile
import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
lambda_client = session.client('lambda', region_name='us-east-1')
iam_client = session.client('iam', region_name='us-east-1')

# Get or create Lambda execution role
role_name = 'tracker-lambda-role'
try:
    role_response = iam_client.get_role(RoleName=role_name)
    role_arn = role_response['Role']['Arn']
    print(f"✓ Using existing role: {role_arn}")
except iam_client.exceptions.NoSuchEntityException:
    print(f"Creating IAM role: {role_name}...")
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    role_response = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
        Description='Execution role for tracker Lambda functions'
    )
    role_arn = role_response['Role']['Arn']
    
    # Attach policies
    iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
    )
    iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn='arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess'
    )
    print(f"✓ Created role: {role_arn}")
    print("⏳ Waiting 10 seconds for role to propagate...")
    import time
    time.sleep(10)

functions = [
    {'name': 'media-bias-api', 'handler': 'index.lambda_handler'},
    {'name': 'fake-news-api', 'handler': 'index.lambda_handler'},
    {'name': 'corporate-wokeness-api', 'handler': 'index.lambda_handler'},
    {'name': 'political-corruption-api', 'handler': 'index.lambda_handler'}
]

for func in functions:
    func_name = func['name']
    func_dir = f'lambda_functions/{func_name}'
    zip_file = f'{func_name}.zip'
    
    print(f"\n📦 Packaging {func_name}...")
    with zipfile.ZipFile(zip_file, 'w') as zf:
        zf.write(f'{func_dir}/index.py', 'index.py')
    
    with open(zip_file, 'rb') as f:
        zip_content = f.read()
    
    try:
        print(f"🚀 Deploying {func_name}...")
        lambda_client.create_function(
            FunctionName=func_name,
            Runtime='python3.11',
            Role=role_arn,
            Handler=func['handler'],
            Code={'ZipFile': zip_content},
            Timeout=30,
            MemorySize=256
        )
        print(f"✓ Created Lambda function: {func_name}")
    except lambda_client.exceptions.ResourceConflictException:
        print(f"⚠ Function {func_name} exists, updating code...")
        lambda_client.update_function_code(
            FunctionName=func_name,
            ZipFile=zip_content
        )
        print(f"✓ Updated Lambda function: {func_name}")
    
    os.remove(zip_file)

print("\n✅ All Lambda functions deployed successfully")
