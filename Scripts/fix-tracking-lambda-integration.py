"""
Fix the tracking API routes to call email-subscription-handler Lambda
which has the actual tracking pixel logic.
"""
import boto3

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
apigw = session.client('apigateway')
lambda_client = session.client('lambda')

api_id = 'olmcyxwc1a'
lambda_arn = 'arn:aws:lambda:us-east-1:371751795928:function:email-subscription-handler'

# Get resources
resources = apigw.get_resources(restApiId=api_id)['items']

# Find the tracking resources
open_resource = [r for r in resources if r['path'] == '/track/open/{tracking_id}'][0]
click_resource = [r for r in resources if r['path'] == '/track/click/{tracking_id}'][0]

print('Updating Lambda integration for /track/open/{tracking_id}...')
apigw.put_integration(
    restApiId=api_id,
    resourceId=open_resource['id'],
    httpMethod='GET',
    type='AWS_PROXY',
    integrationHttpMethod='POST',
    uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
)

print('Updating Lambda integration for /track/click/{tracking_id}...')
apigw.put_integration(
    restApiId=api_id,
    resourceId=click_resource['id'],
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
            FunctionName='email-subscription-handler',
            StatementId=f'apigateway-track-{path}-{api_id}',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f'arn:aws:execute-api:us-east-1:371751795928:{api_id}/*/*'
        )
        print(f'  Added permission for {path}')
    except lambda_client.exceptions.ResourceConflictException:
        print(f'  Permission for {path} already exists')

# Deploy
print('Deploying API...')
apigw.create_deployment(
    restApiId=api_id,
    stageName='prod',
    description='Fix tracking Lambda integration'
)

print('\nDone! Tracking routes now call email-subscription-handler')
print(f'Test URL: https://{api_id}.execute-api.us-east-1.amazonaws.com/prod/track/open/dGVzdA==')
