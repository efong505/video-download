import boto3
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
apigateway = session.client('apigateway', region_name='us-east-1')
lambda_client = session.client('lambda', region_name='us-east-1')

# Use existing API Gateway
api_id = 'diz6ceeb22'
print(f"Using existing API Gateway: {api_id}")

# Get root resource
resources = apigateway.get_resources(restApiId=api_id)
root_id = [r for r in resources['items'] if r['path'] == '/'][0]['id']

endpoints = [
    {'path': 'media-bias', 'function': 'media-bias-api'},
    {'path': 'fake-news', 'function': 'fake-news-api'},
    {'path': 'corporate-wokeness', 'function': 'corporate-wokeness-api'},
    {'path': 'political-corruption', 'function': 'political-corruption-api'}
]

for endpoint in endpoints:
    path = endpoint['path']
    function_name = endpoint['function']
    
    print(f"\n📍 Setting up /{path}...")
    
    # Create resource
    try:
        resource = apigateway.create_resource(
            restApiId=api_id,
            parentId=root_id,
            pathPart=path
        )
        resource_id = resource['id']
        print(f"✓ Created resource: /{path}")
    except apigateway.exceptions.ConflictException:
        # Resource exists, get it
        resources = apigateway.get_resources(restApiId=api_id)
        resource = [r for r in resources['items'] if r.get('pathPart') == path][0]
        resource_id = resource['id']
        print(f"⚠ Resource /{path} exists, using existing")
    
    # Create ANY method
    try:
        apigateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='ANY',
            authorizationType='NONE'
        )
        print(f"✓ Created ANY method")
    except apigateway.exceptions.ConflictException:
        print(f"⚠ ANY method exists")
    
    # Set up Lambda integration
    function_arn = f"arn:aws:lambda:us-east-1:371751795928:function:{function_name}"
    uri = f"arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{function_arn}/invocations"
    
    try:
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='ANY',
            type='AWS_PROXY',
            integrationHttpMethod='POST',
            uri=uri
        )
        print(f"✓ Created Lambda integration")
    except Exception as e:
        print(f"⚠ Integration exists or error: {e}")
    
    # Add Lambda permission
    try:
        lambda_client.add_permission(
            FunctionName=function_name,
            StatementId=f'apigateway-{path}',
            Action='lambda:InvokeFunction',
            Principal='apigateway.amazonaws.com',
            SourceArn=f"arn:aws:execute-api:us-east-1:371751795928:{api_id}/*/*/{path}"
        )
        print(f"✓ Added Lambda permission")
    except lambda_client.exceptions.ResourceConflictException:
        print(f"⚠ Lambda permission exists")
    
    # Create OPTIONS method for CORS
    try:
        apigateway.put_method(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            authorizationType='NONE'
        )
        
        apigateway.put_integration(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            type='MOCK',
            requestTemplates={'application/json': '{"statusCode": 200}'}
        )
        
        apigateway.put_method_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Headers': True,
                'method.response.header.Access-Control-Allow-Methods': True,
                'method.response.header.Access-Control-Allow-Origin': True
            }
        )
        
        apigateway.put_integration_response(
            restApiId=api_id,
            resourceId=resource_id,
            httpMethod='OPTIONS',
            statusCode='200',
            responseParameters={
                'method.response.header.Access-Control-Allow-Headers': "'Content-Type,Authorization'",
                'method.response.header.Access-Control-Allow-Methods': "'GET,POST,OPTIONS'",
                'method.response.header.Access-Control-Allow-Origin': "'*'"
            }
        )
        print(f"✓ Created OPTIONS method for CORS")
    except Exception as e:
        print(f"⚠ OPTIONS method exists or error: {e}")

# Deploy API
print(f"\n🚀 Deploying API to prod stage...")
apigateway.create_deployment(
    restApiId=api_id,
    stageName='prod',
    description='Tracker APIs deployment'
)

print(f"\n✅ All API endpoints configured successfully")
print(f"\n📡 API Base URL: https://{api_id}.execute-api.us-east-1.amazonaws.com/prod")
print(f"\nEndpoints:")
for endpoint in endpoints:
    print(f"  - https://{api_id}.execute-api.us-east-1.amazonaws.com/prod/{endpoint['path']}")
