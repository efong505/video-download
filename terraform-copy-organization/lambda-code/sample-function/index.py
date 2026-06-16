import json
import boto3
import os
from datetime import datetime

# Initialize AWS clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Get environment variables
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE')
S3_BUCKET = os.environ.get('S3_BUCKET')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'tutorial')

def lambda_handler(event, context):
    """
    Sample Lambda function that demonstrates:
    - DynamoDB operations
    - S3 operations
    - SNS notifications
    - API Gateway integration
    """
    
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        action = body.get('action', 'test')
        
        # Generate unique ID
        timestamp = int(datetime.now().timestamp())
        item_id = f"item-{timestamp}"
        
        # Perform action based on request
        if action == 'write_dynamodb':
            result = write_to_dynamodb(item_id, timestamp, body)
        elif action == 'write_s3':
            result = write_to_s3(item_id, body)
        elif action == 'send_notification':
            result = send_sns_notification(body)
        else:
            result = test_function()
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Success',
                'action': action,
                'result': result,
                'environment': ENVIRONMENT,
                'timestamp': timestamp
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Error',
                'error': str(e)
            })
        }

def test_function():
    """Test function to verify Lambda is working"""
    return {
        'status': 'Lambda function is working',
        'dynamodb_table': DYNAMODB_TABLE,
        's3_bucket': S3_BUCKET,
        'sns_topic': SNS_TOPIC_ARN
    }

def write_to_dynamodb(item_id, timestamp, data):
    """Write item to DynamoDB table"""
    table = dynamodb.Table(DYNAMODB_TABLE)
    
    item = {
        'id': item_id,
        'timestamp': timestamp,
        'status': 'active',
        'data': json.dumps(data),
        'created_at': datetime.now().isoformat()
    }
    
    table.put_item(Item=item)
    
    return {
        'dynamodb_write': 'success',
        'item_id': item_id
    }

def write_to_s3(item_id, data):
    """Write object to S3 bucket"""
    key = f"test-data/{item_id}.json"
    
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=key,
        Body=json.dumps(data),
        ContentType='application/json'
    )
    
    return {
        's3_write': 'success',
        'bucket': S3_BUCKET,
        'key': key
    }

def send_sns_notification(data):
    """Send SNS notification"""
    message = data.get('message', 'Test notification from Lambda')
    
    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject='Tutorial Lambda Notification',
        Message=message
    )
    
    return {
        'sns_publish': 'success',
        'message_id': response['MessageId']
    }
