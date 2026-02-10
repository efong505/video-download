import json
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Returns list of videos from S3 videos/ folder
    """
    try:
        bucket = 'my-video-downloads-bucket'
        
        # List videos in the videos/ folder
        response = s3_client.list_objects_v2(
            Bucket=bucket,
            Prefix='videos/',
            Delimiter='/'
        )
        
        videos = []
        if 'Contents' in response:
            for obj in response['Contents']:
                key = obj['Key']
                if key.endswith('.mp4') and key != 'videos/':
                    filename = key.replace('videos/', '')
                    videos.append({
                        'filename': filename,
                        'name': filename.replace('.mp4', '').replace('_', ' '),
                        'size': obj['Size'],
                        'lastModified': obj['LastModified'].isoformat()
                    })
        
        # Sort by last modified (newest first)
        videos.sort(key=lambda x: x['lastModified'], reverse=True)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'videos': videos,
                'count': len(videos)
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }