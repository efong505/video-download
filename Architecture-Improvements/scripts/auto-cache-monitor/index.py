import boto3
import json
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')
elasticache = boto3.client('elasticache')
apigateway = boto3.client('apigateway')

DYNAMODB_READ_THRESHOLD = 2000000  # 2M reads/day = break-even point
API_REQUEST_THRESHOLD = 500000     # 500K requests/day = break-even point

def lambda_handler(event, context):
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)
    
    # Main platform tables
    main_tables = ['Videos', 'Articles', 'News', 'Races', 'Candidates']
    # Shopping system tables (added Nov 2025)
    shopping_tables = ['Products', 'Orders', 'Cart', 'Reviews']
    
    all_tables = main_tables + shopping_tables
    total_reads = 0
    
    for table in all_tables:
        try:
            response = cloudwatch.get_metric_statistics(
                Namespace='AWS/DynamoDB',
                MetricName='ConsumedReadCapacityUnits',
                Dimensions=[{'Name': 'TableName', 'Value': table}],
                StartTime=start_time,
                EndTime=end_time,
                Period=86400,
                Statistics=['Sum']
            )
            if response['Datapoints']:
                total_reads += response['Datapoints'][0]['Sum']
        except Exception as e:
            print(f"Error checking {table}: {e}")
    
    total_requests = 0
    try:
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/ApiGateway',
            MetricName='Count',
            Dimensions=[{'Name': 'ApiName', 'Value': 'TechCrossAPI'}],
            StartTime=start_time,
            EndTime=end_time,
            Period=86400,
            Statistics=['Sum']
        )
        if response['Datapoints']:
            total_requests = response['Datapoints'][0]['Sum']
    except Exception as e:
        print(f"Error checking API Gateway: {e}")
    
    print(f"Traffic: {total_reads} reads, {total_requests} requests")
    
    actions = []
    
    if total_reads >= DYNAMODB_READ_THRESHOLD:
        if not is_elasticache_enabled():
            enable_elasticache()
            actions.append(f"ElastiCache enabled ({total_reads} reads/day)")
    
    if total_requests >= API_REQUEST_THRESHOLD:
        if not is_api_cache_enabled():
            enable_api_cache()
            actions.append(f"API cache enabled ({total_requests} requests/day)")
    
    return {'statusCode': 200, 'body': json.dumps({'reads': total_reads, 'requests': total_requests, 'actions': actions})}

def is_elasticache_enabled():
    try:
        elasticache.describe_cache_clusters(CacheClusterId='techcross-cache')
        return True
    except:
        return False

def is_api_cache_enabled():
    try:
        apis = apigateway.get_rest_apis()
        for api in apis['items']:
            if api['name'] == 'TechCrossAPI':
                stages = apigateway.get_stages(restApiId=api['id'])
                for stage in stages['item']:
                    if stage.get('cacheClusterEnabled'):
                        return True
        return False
    except:
        return False

def enable_elasticache():
    try:
        elasticache.create_cache_cluster(
            CacheClusterId='techcross-cache',
            CacheNodeType='cache.t3.micro',
            Engine='redis',
            NumCacheNodes=1,
            Port=6379
        )
        print("ElastiCache enabled")
    except Exception as e:
        print(f"Error: {e}")

def enable_api_cache():
    try:
        apis = apigateway.get_rest_apis()
        for api in apis['items']:
            if api['name'] == 'TechCrossAPI':
                stages = apigateway.get_stages(restApiId=api['id'])
                for stage in stages['item']:
                    apigateway.update_stage(
                        restApiId=api['id'],
                        stageName=stage['stageName'],
                        patchOperations=[
                            {'op': 'replace', 'path': '/cacheClusterEnabled', 'value': 'true'},
                            {'op': 'replace', 'path': '/cacheClusterSize', 'value': '0.5'}
                        ]
                    )
                    print("API cache enabled")
    except Exception as e:
        print(f"Error: {e}")
