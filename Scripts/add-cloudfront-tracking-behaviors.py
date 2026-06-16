"""
Add CloudFront cache behaviors for /track/open/* and /track/click/*
that route to the API Gateway origin.
"""
import boto3
import json

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
cloudfront = session.client('cloudfront')

DISTRIBUTION_ID = 'E3N00R2D2NE9C5'
API_GATEWAY_DOMAIN = 'niexv1rw75.execute-api.us-east-1.amazonaws.com'

# Get current distribution config
print(f'Getting distribution config for {DISTRIBUTION_ID}...')
response = cloudfront.get_distribution_config(Id=DISTRIBUTION_ID)
config = response['DistributionConfig']
etag = response['ETag']

print(f'Current ETag: {etag}')

# Check if behaviors already exist
existing_patterns = []
if config.get('CacheBehaviors') and config['CacheBehaviors'].get('Items'):
    existing_patterns = [b['PathPattern'] for b in config['CacheBehaviors']['Items']]
    print(f'Existing cache behaviors: {len(existing_patterns)}')

if 'track/open/*' in existing_patterns and 'track/click/*' in existing_patterns:
    print('✅ Tracking behaviors already exist!')
    exit(0)

# Initialize CacheBehaviors if not present
if 'CacheBehaviors' not in config:
    config['CacheBehaviors'] = {'Quantity': 0, 'Items': []}
elif 'Items' not in config['CacheBehaviors']:
    config['CacheBehaviors']['Items'] = []

# Check if API Gateway origin exists
origin_id = 'tracking-api-gateway'
origin_exists = any(o['Id'] == origin_id for o in config['Origins']['Items'])

if not origin_exists:
    print(f'Adding API Gateway origin: {API_GATEWAY_DOMAIN}')
    config['Origins']['Items'].append({
        'Id': origin_id,
        'DomainName': API_GATEWAY_DOMAIN,
        'OriginPath': '/subscribe',
        'CustomHeaders': {'Quantity': 0},
        'CustomOriginConfig': {
            'HTTPPort': 80,
            'HTTPSPort': 443,
            'OriginProtocolPolicy': 'https-only',
            'OriginSslProtocols': {'Quantity': 1, 'Items': ['TLSv1.2']},
            'OriginReadTimeout': 30,
            'OriginKeepaliveTimeout': 5
        }
    })
    config['Origins']['Quantity'] += 1

# Create tracking behaviors
tracking_behaviors = [
    {
        'PathPattern': 'track/open/*',
        'TargetOriginId': origin_id,
        'ViewerProtocolPolicy': 'redirect-to-https',
        'AllowedMethods': {
            'Quantity': 2,
            'Items': ['GET', 'HEAD'],
            'CachedMethods': {'Quantity': 2, 'Items': ['GET', 'HEAD']}
        },
        'SmoothStreaming': False,
        'Compress': False,
        'CachePolicyId': '4135ea2d-6df8-44a3-9df3-4b5a84be39ad',
        'OriginRequestPolicyId': 'b689b0a8-53d0-40ab-baf2-68738e2966ac',
        'TrustedSigners': {'Enabled': False, 'Quantity': 0},
        'TrustedKeyGroups': {'Enabled': False, 'Quantity': 0},
        'FieldLevelEncryptionId': '',
        'LambdaFunctionAssociations': {'Quantity': 0}
    },
    {
        'PathPattern': 'track/click/*',
        'TargetOriginId': origin_id,
        'ViewerProtocolPolicy': 'redirect-to-https',
        'AllowedMethods': {
            'Quantity': 2,
            'Items': ['GET', 'HEAD'],
            'CachedMethods': {'Quantity': 2, 'Items': ['GET', 'HEAD']}
        },
        'SmoothStreaming': False,
        'Compress': False,
        'CachePolicyId': '4135ea2d-6df8-44a3-9df3-4b5a84be39ad',
        'OriginRequestPolicyId': 'b689b0a8-53d0-40ab-baf2-68738e2966ac',
        'TrustedSigners': {'Enabled': False, 'Quantity': 0},
        'TrustedKeyGroups': {'Enabled': False, 'Quantity': 0},
        'FieldLevelEncryptionId': '',
        'LambdaFunctionAssociations': {'Quantity': 0}
    }
]

# Add new behaviors
for behavior in tracking_behaviors:
    if behavior['PathPattern'] not in existing_patterns:
        print(f'Adding behavior: {behavior["PathPattern"]}')
        config['CacheBehaviors']['Items'].append(behavior)
        config['CacheBehaviors']['Quantity'] += 1

# Update distribution
print('Updating CloudFront distribution...')
cloudfront.update_distribution(
    Id=DISTRIBUTION_ID,
    DistributionConfig=config,
    IfMatch=etag
)

print('\n✅ CloudFront distribution updated successfully!')
print('⏳ Distribution is now deploying (takes 5-10 minutes)')
print('\nTracking URLs will work once deployment completes:')
print(f'  https://christianconservativestoday.com/track/open/{{tracking_id}}')
print(f'  https://christianconservativestoday.com/track/click/{{tracking_id}}')
print('\nCheck deployment status:')
print(f'  aws cloudfront get-distribution --id {DISTRIBUTION_ID} --profile ekewaka --query "Distribution.Status"')
