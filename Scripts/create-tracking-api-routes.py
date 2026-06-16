"""
Add /track/open/{tracking_id} and /track/click/{tracking_id} routes to API Gateway
that call the tracking-api Lambda function.
"""
import boto3
import json

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
apigw = session.client('apigateway')
lambda_client = session.client('lambda')

# Find or create an API Gateway for tracking
apis = apigw.get_rest_apis()['items']

# Look for existing subscription/email API
api_id = None
for api in apis:
    if 'email' in api['name'].lower() or 'subscription' in api['name'].lower():
        api_id = api['id']
        api_name = api['name']
        print(f'Using existing API: {api_name} ({api_id})')
        break

if not api_id:
    print('No suitable API found. Creating new one...')
    response = apigw.create_rest_api(
        name='email-tracking-api',
        description='Email open and click tracking',
        endpointConfiguration={'types': ['REGIONAL']}
    )
    api_id = response['id']
    print(f'Created API: {api_id}')

# Get root resource
resources = apigw.get_resources(restApiId=api_id)
root_id = [r['id'] for r in resources['items'] if r['path'] == '/'][0]

# Create /track resource
print('Creating /track resource...')
try:
    track_resource = apigw.create_resource(
        restApiId=api_id,
        parentId=root_id,
        pathPart='track'
    )
    track_id = track_resource['id']
except apigw.exceptions.ConflictException:
    track_id = [r['id'] for r in resources['items'] if r['path'] == '/track'][0]
    print('  /track already exists')

# Create /track/open resource
print('Creating /track/open resource...')
try:
    open_resource = apigw.create_resource(
        restApiId=api_id,
        parentId=track_id,
        pathPart='open'
    )
    open_id = open_resource['id']
except apigw.exceptions.ConflictException:
    open_id = [r['id'] for r in resources['items'] if r['path'] == '/track/open'][0]
    print('  /track/open already exists')

# Create /track/open/{tracking_id} resource
print('Creating /track/open/{tracking_id} resource...')
try:
    open_param_resource = apigw.create_resource(
        restApiId=api_id,
        parentId=open_id,
        pathPart='{tracking_id}'
    )
    open_param_id = open_param_resource['id']
except apigw.exceptions.ConflictException:
    open_param_id = [r['id'] for r in resources['items'] if r['path'] == '/track/open/{tracking_id}'][0]
    print('  /track/open/{tracking_id} already exists')

# Create /track/click resource
print('Creating /track/click resource...')
try:
    click_resource = apigw.create_resource(
        restApiId=api_id,
        parentId=track_id,
        pathPart='click'
    )
    click_id = click_resource['id']
except apigw.exceptions.ConflictException:
    click_id = [r['id'] for r in resources['items'] if r['path'] == '/track/click'][0]
    print('  /track/click already exists')

# Create /track/click/{tracking_id} resource
print('Creating /track/click/{tracking_id} resource...')
try:
    click_param_resource = apigw.create_resource(
        restApiId=api_id,
        parentId=click_id,
        pathPart='{tracking_id}'
    )
    click_param_id = click_param_resource['id']
except apigw.exceptions.ConflictException:
    click_param_id = [r['id'] for r in resources['items'] if r['path'] == '/track/click/{tracking_id}'][0]
    print('  /track/click/{tracking_id} already exists')

# Add GET method to /track/open/{tracking_id}
print('Adding GET method to /track/open/{tracking_id}...')
try:
    apigw.put_method(
        restApiId=api_id,
        resourceId=open_param_id,
        httpMethod='GET',
        authorizationType='NONE'
    )
except apigw.exceptions.ConflictException:
    print('  Method already exists')

# Add Lambda integration for open tracking
print('Adding Lambda integration for open tracking...')
lambda_arn = f'arn:aws:lambda:us-east-1:371751795928:function:tracking-api'
apigw.put_integration(
    restApiId=api_id,
    resourceId=open_param_id,
    httpMethod='GET',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
)

# Add GET method to /track/click/{tracking_id}
print('Adding GET method to /track/click/{tracking_id}...')
try:
    apigw.put_method(
        restApiId=api_id,
        resourceId=click_param_id,
        httpMethod='GET',
        authorizationType='NONE'
    )
except apigw.exceptions.ConflictException:
    print('  Method already exists')

# Add Lambda integration for click tracking
print('Adding Lambda integration for click tracking...')
apigw.put_integration(
    restApiId=api_id,
    resourceId=click_param_id,
    httpMethod='GET',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
)

# Add Lambda permissions
print('Adding Lambda permissions...')
for path in ['open', 'click']:
    try:
        lambda_client.add_permission(
            FunctionName='tracking-api',
            StatementId=f'apigateway-{path}-{api_id}',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:us-east-1:371751795928:{api_id}/*/*'
        )
    except lambda_client.exceptions.ResourceConflictException:
        print(f'  Permission for {path} already exists')

# Deploy API
print('Deploying API...')
deployment = apigw.create_deployment(
    restApiId=api_id,
    stageName='prod',
    description='Add tracking routes'
)

print(f'\n✅ Tracking routes created!')
print(f'API Gateway ID: {api_id}')
print(f'Endpoints:')
print(f'  https://{api_id}.execute-api.us-east-1.amazonaws.com/prod/track/open/{{tracking_id}}')
print(f'  https://{api_id}.execute-api.us-east-1.amazonaws.com/prod/track/click/{{tracking_id}}')
print(f'\nNow update email_sender Lambda to use this API Gateway URL for tracking.')
