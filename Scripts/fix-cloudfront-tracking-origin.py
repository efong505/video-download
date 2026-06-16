import boto3

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
cf = session.client('cloudfront')

dist_id = 'E3N00R2D2NE9C5'

# Get current config
response = cf.get_distribution_config(Id=dist_id)
config = response['DistributionConfig']
etag = response['ETag']

# Update tracking-api-gateway origin to point to olmcyxwc1a
for origin in config['Origins']['Items']:
    if origin['Id'] == 'tracking-api-gateway':
        origin['DomainName'] = 'olmcyxwc1a.execute-api.us-east-1.amazonaws.com'
        origin['OriginPath'] = '/prod'
        print(f"Updated origin: {origin['Id']} -> {origin['DomainName']}{origin['OriginPath']}")

# Update distribution
cf.update_distribution(
    Id=dist_id,
    DistributionConfig=config,
    IfMatch=etag
)

print("✓ CloudFront updated, deploying...")
