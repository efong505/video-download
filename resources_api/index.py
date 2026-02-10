import json
import boto3

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
        elif action == 'update':
            return update_resource(event, headers)
        elif action == 'delete':
            return delete_resource(event, headers)
        elif action == 'get_order':
            return get_category_order(headers)
        elif action == 'save_order':
            return save_category_order(event, headers)
        elif action == 'get_categories':
            return get_categories(headers)
        elif action == 'save_categories':
            return save_categories(event, headers)
        else:
            return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Invalid action'})}
    except Exception as e:
        return {'statusCode': 500, 'headers': headers, 'body': json.dumps({'error': str(e)})}

def list_resources(headers):
    response = table.scan()
    resources = response.get('Items', [])
    # Normalize resource_id to id for frontend compatibility
    for resource in resources:
        if 'resource_id' in resource and resource['resource_id'] not in ['_category_order', '_categories']:
            resource['id'] = resource['resource_id']
            # Convert string category to array for backward compatibility
            if 'category' in resource and isinstance(resource['category'], str):
                resource['category'] = [resource['category']]
    # Filter out the category order and categories items
    resources = [r for r in resources if r.get('resource_id') not in ['_category_order', '_categories']]
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
    
    # Ensure category is always an array
    if isinstance(category, str):
        category = [category]
    elif not isinstance(category, list):
        category = []
    
    table.put_item(Item={
        'resource_id': resource_id,
        'name': name,
        'category': category,
        'url': url,
        'description': description
    })
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Resource created'})}

def update_resource(event, headers):
    body = json.loads(event.get('body', '{}'))
    resource_id = body.get('id')
    name = body.get('name')
    category = body.get('category')
    url = body.get('url')
    description = body.get('description', '')
    
    if not all([resource_id, name, category, url]):
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Missing required fields'})}
    
    # Ensure category is always an array
    if isinstance(category, str):
        category = [category]
    elif not isinstance(category, list):
        category = []
    
    table.put_item(Item={
        'resource_id': resource_id,
        'name': name,
        'category': category,
        'url': url,
        'description': description
    })
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Resource updated'})}

def delete_resource(event, headers):
    resource_id = event.get('queryStringParameters', {}).get('resource_id')
    if not resource_id:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Missing resource_id'})}
    
    table.delete_item(Key={'resource_id': resource_id})
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Resource deleted'})}

def get_category_order(headers):
    try:
        response = table.get_item(Key={'resource_id': '_category_order'})
        if 'Item' in response:
            return {'statusCode': 200, 'headers': headers, 'body': json.dumps(response['Item']['order'])}
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps([])}
    except:
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps([])}

def save_category_order(event, headers):
    body = json.loads(event.get('body', '{}'))
    order = body.get('order', [])
    
    table.put_item(Item={'resource_id': '_category_order', 'order': order})
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Order saved'})}

def get_categories(headers):
    try:
        response = table.get_item(Key={'resource_id': '_categories'})
        if 'Item' in response:
            return {'statusCode': 200, 'headers': headers, 'body': json.dumps(response['Item']['categories'])}
        # Return default categories if none exist
        default_categories = ['Research Resources', 'Educational', 'Financial', 'News & Media', 'Ministry Tools', 'Apologetics']
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps(default_categories)}
    except:
        default_categories = ['Research Resources', 'Educational', 'Financial', 'News & Media', 'Ministry Tools', 'Apologetics']
        return {'statusCode': 200, 'headers': headers, 'body': json.dumps(default_categories)}

def save_categories(event, headers):
    body = json.loads(event.get('body', '{}'))
    categories = body.get('categories', [])
    
    table.put_item(Item={'resource_id': '_categories', 'categories': categories})
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Categories saved'})}
