import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('resources-table')

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    if event.get('httpMethod') == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    action = event.get('queryStringParameters', {}).get('action') if event.get('queryStringParameters') else None
    
    try:
        if action == 'list':
            return list_resources(headers)
        elif action == 'create':
            return create_resource(event, headers)
        elif action == 'delete':
            return delete_resource(event, headers)
        else:
            return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Invalid action'})}
    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}

def list_resources(headers):
    response = table.scan()
    resources = response.get('Items', [])
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps(resources, default=str)}

def create_resource(event, headers):
    body = json.loads(event.get('body', '{}'))
    resource_id = body.get('id')
    name = body.get('name')
    category = body.get('category')
    url = body.get('url')
    description = body.get('description', '')
    
    if not all([resource_id, name, category, url]):
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Missing required fields'})}
    
    table.put_item(Item={
        'resource_id': resource_id,
        'name': name,
        'category': category,
        'url': url,
        'description': description
    })
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Resource created'})}

def delete_resource(event, headers):
    resource_id = event.get('queryStringParameters', {}).get('resource_id')
    if not resource_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Missing resource_id'})}
    
    table.delete_item(Key={'resource_id': resource_id})
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Resource deleted'})}
