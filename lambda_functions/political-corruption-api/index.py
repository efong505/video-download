import json
import boto3
import uuid
from datetime import datetime
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('political-corruption-tracker')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj)
    raise TypeError

def lambda_handler(event, context):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,Authorization',
        'Access-Control-Allow-Methods': 'GET,POST,OPTIONS'
    }
    
    if event['httpMethod'] == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': ''}
    
    try:
        params = event.get('queryStringParameters') or {}
        action = params.get('action', 'list')
        
        if action == 'list':
            status = params.get('status', 'all')
            response = table.scan()
            reports = response.get('Items', [])
            
            if status != 'all':
                reports = [r for r in reports if r.get('status') == status]
            
            reports.sort(key=lambda x: x.get('votes', 0), reverse=True)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'reports': reports}, default=decimal_default)
            }
        
        elif action == 'report':
            body = json.loads(event['body'])
            auth_header = event.get('headers', {}).get('Authorization', '')
            user_id = auth_header.replace('Bearer ', '') if auth_header else None
            
            if not user_id:
                return {'statusCode': 401, 'headers': headers, 'body': json.dumps({'error': 'Unauthorized'})}
            
            report_id = str(uuid.uuid4())
            item = {
                'report_id': report_id,
                'official_name': body['official_name'],
                'office': body.get('office', ''),
                'location': body.get('location', ''),
                'category': body['category'],
                'description': body['description'],
                'evidence_url': body.get('evidence_url', ''),
                'incident_date': body.get('incident_date', ''),
                'votes': 0,
                'status': 'active',
                'created_at': datetime.utcnow().isoformat(),
                'submitted_by': user_id,
                'voted_by': []
            }
            
            table.put_item(Item=item)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'Report submitted', 'report_id': report_id})
            }
        
        elif action == 'vote':
            body = json.loads(event['body'])
            auth_header = event.get('headers', {}).get('Authorization', '')
            user_id = auth_header.replace('Bearer ', '') if auth_header else None
            
            if not user_id:
                return {'statusCode': 401, 'headers': headers, 'body': json.dumps({'error': 'Unauthorized'})}
            
            report_id = body['report_id']
            response = table.get_item(Key={'report_id': report_id})
            report = response.get('Item')
            
            if not report:
                return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Report not found'})}
            
            voted_by = report.get('voted_by', [])
            votes = report.get('votes', 0)
            
            if user_id in voted_by:
                voted_by.remove(user_id)
                votes = max(0, votes - 1)
            else:
                voted_by.append(user_id)
                votes += 1
            
            table.update_item(
                Key={'report_id': report_id},
                UpdateExpression='SET votes = :v, voted_by = :vb',
                ExpressionAttributeValues={':v': votes, ':vb': voted_by}
            )
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'votes': votes})
            }
        
        else:
            return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'Invalid action'})}
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
