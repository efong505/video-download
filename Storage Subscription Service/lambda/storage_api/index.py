import boto3
import json
import jwt
import os
import base64
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('StorageUsers')
files_table = dynamodb.Table('StorageFiles')

BUCKET = os.environ.get('S3_BUCKET', 'storage-subscription-bucket-75470')
JWT_SECRET = os.environ.get('JWT_SECRET', 'your-secret-key-change-this')

def lambda_handler(event, context):
    # Handle OPTIONS for CORS preflight
    if event.get('httpMethod') == 'OPTIONS' or event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return response(200, {})
    
    try:
        # Verify JWT - try different header case variations
        headers = event.get('headers', {})
        token = headers.get('Authorization') or headers.get('authorization', '')
        token = token.replace('Bearer ', '').replace('bearer ', '')
        
        if not token:
            return response(401, {'error': 'No token provided'})
        
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            user_id = payload['userId']
            email = payload['email']
        except:
            return response(401, {'error': 'Invalid token'})
        
        method = event['httpMethod']
        
        if method == 'POST':
            return upload_file(event, user_id, email)
        elif method == 'GET':
            return handle_get(event, user_id)
        elif method == 'DELETE':
            return delete_file(event, user_id)
        else:
            return response(405, {'error': 'Method not allowed'})
    except Exception as e:
        return response(500, {'error': str(e)})

def upload_file(event, user_id, email):
    body = json.loads(event['body'])
    file_name = body.get('fileName')
    file_size = body.get('fileSize')
    file_content = body.get('fileContent')  # base64
    file_type = body.get('fileType', 'application/octet-stream')
    
    if not file_name or not file_content:
        return response(400, {'error': 'fileName and fileContent required'})
    
    # Get user quota
    user = users_table.get_item(Key={'email': email})['Item']
    storage_used = int(user['storageUsed'])
    storage_quota = int(user['storageQuota'])
    
    if storage_used + file_size > storage_quota:
        return response(403, {'error': 'Storage quota exceeded', 'storageUsed': storage_used, 'storageQuota': storage_quota})
    
    # Upload to S3
    s3_key = f"users/{user_id}/{file_name}"
    file_bytes = base64.b64decode(file_content)
    
    s3.put_object(
        Bucket=BUCKET,
        Key=s3_key,
        Body=file_bytes,
        ContentType=file_type
    )
    
    # Update storage used
    users_table.update_item(
        Key={'email': email},
        UpdateExpression='SET storageUsed = storageUsed + :size',
        ExpressionAttributeValues={':size': Decimal(str(file_size))}
    )
    
    # Save file metadata
    file_id = f"{user_id}#{file_name}"
    files_table.put_item(Item={
        'fileId': file_id,
        'userId': user_id,
        'fileName': file_name,
        'fileSize': Decimal(str(file_size)),
        'fileType': file_type,
        's3Key': s3_key,
        'uploadedAt': datetime.utcnow().isoformat()
    })
    
    return response(200, {
        'message': 'File uploaded successfully',
        'fileName': file_name,
        'fileSize': file_size,
        'storageUsed': storage_used + file_size
    })

def handle_get(event, user_id):
    params = event.get('queryStringParameters') or {}
    file_name = params.get('fileName')
    
    if file_name:
        # Generate presigned URL for download
        s3_key = f"users/{user_id}/{file_name}"
        try:
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': BUCKET, 'Key': s3_key},
                ExpiresIn=3600
            )
            return response(200, {'downloadUrl': url, 'fileName': file_name})
        except:
            return response(404, {'error': 'File not found'})
    else:
        # List all files
        try:
            result = s3.list_objects_v2(Bucket=BUCKET, Prefix=f"users/{user_id}/")
            files = []
            
            if 'Contents' in result:
                for obj in result['Contents']:
                    file_name = obj['Key'].replace(f"users/{user_id}/", '')
                    if file_name:  # Skip directory itself
                        files.append({
                            'fileName': file_name,
                            'fileSize': obj['Size'],
                            'lastModified': obj['LastModified'].isoformat()
                        })
            
            return response(200, {'files': files, 'count': len(files)})
        except ClientError as e:
            return response(200, {'files': [], 'count': 0})
        except Exception as e:
            return response(200, {'files': [], 'count': 0})

def delete_file(event, user_id):
    params = event.get('queryStringParameters') or {}
    file_name = params.get('fileName')
    
    if not file_name:
        return response(400, {'error': 'fileName parameter required'})
    
    s3_key = f"users/{user_id}/{file_name}"
    
    try:
        # Get file size
        obj = s3.head_object(Bucket=BUCKET, Key=s3_key)
        file_size = obj['ContentLength']
        
        # Delete from S3
        s3.delete_object(Bucket=BUCKET, Key=s3_key)
        
        # Update storage used
        file_id = f"{user_id}#{file_name}"
        file_record = files_table.get_item(Key={'fileId': file_id})
        
        if 'Item' in file_record:
            email = users_table.scan(
                FilterExpression='userId = :uid',
                ExpressionAttributeValues={':uid': user_id}
            )['Items'][0]['email']
            
            users_table.update_item(
                Key={'email': email},
                UpdateExpression='SET storageUsed = storageUsed - :size',
                ExpressionAttributeValues={':size': Decimal(str(file_size))}
            )
            
            # Delete file metadata
            files_table.delete_item(Key={'fileId': file_id})
        
        return response(200, {'message': 'File deleted successfully', 'fileName': file_name})
    except Exception as e:
        return response(404, {'error': 'File not found'})

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': json.dumps(body)
    }
