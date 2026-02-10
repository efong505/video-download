import boto3
import json

def find_video_url(search_term):
    dynamodb = boto3.resource('dynamodb')
    
    # Search in video-metadata table
    metadata_table = dynamodb.Table('video-metadata')
    response = metadata_table.scan()
    
    for item in response['Items']:
        title = item.get('title', '').lower()
        filename = item.get('filename', '').lower()
        
        if 'chicago' in title or 'ice' in title or search_term.lower() in title:
            print(f"Found in video-metadata:")
            print(f"  Title: {item.get('title')}")
            print(f"  Filename: {item.get('filename')}")
            print(f"  URL: {item.get('url')}")
            print(f"  Upload Date: {item.get('upload_date')}")
            print()
    
    # Search in download-jobs table
    jobs_table = dynamodb.Table('download-jobs')
    response = jobs_table.scan()
    
    for item in response['Items']:
        title = item.get('title', '').lower()
        filename = item.get('filename', '').lower()
        
        if 'chicago' in title or 'ice' in title or search_term.lower() in title:
            print(f"Found in download-jobs:")
            print(f"  Job ID: {item.get('job_id')}")
            print(f"  Title: {item.get('title')}")
            print(f"  Filename: {item.get('filename')}")
            print(f"  URL: {item.get('url')}")
            print(f"  Status: {item.get('status')}")
            print()

if __name__ == "__main__":
    find_video_url("chicago ice arrest")