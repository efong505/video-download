import json
import boto3
from botocore.exceptions import ClientError
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Generate signed URL for S3 video file
    """
    try:
        # Get filename from path parameter
        filename = event['pathParameters']['filename']
        bucket = os.environ['S3_BUCKET']
        
        # Generate signed URL (valid for 1 hour)
        signed_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': filename},
            ExpiresIn=3600
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, OPTIONS'
            },
            'body': json.dumps({
                'signed_url': signed_url,
                'expires_in': 3600
            })
        }
        
    except ClientError as e:
        return {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'File not found'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': str(e)})
        }