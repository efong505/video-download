import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('video-metadata')

def scan_and_delete_empty_videos():
    """Scan Videos table and delete entries with empty filenames"""
    
    print("Scanning Videos table for empty filenames...")
    
    response = table.scan()
    items = response['Items']
    
    # Handle pagination
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items.extend(response['Items'])
    
    print(f"Total videos found: {len(items)}")
    
    # Find videos with empty or missing filenames
    empty_videos = []
    for item in items:
        filename = item.get('filename', '').strip()
        video_id = item.get('video_id', '').strip()
        
        if not filename or not video_id:
            empty_videos.append(item)
            print(f"Found invalid video: video_id='{video_id}', filename='{filename}'")
    
    print(f"\nFound {len(empty_videos)} videos with empty filenames")
    
    if empty_videos:
        confirm = input(f"\nDelete {len(empty_videos)} invalid video(s)? (yes/no): ")
        
        if confirm.lower() == 'yes':
            deleted_count = 0
            for video in empty_videos:
                try:
                    video_id = video.get('video_id', '')
                    if video_id:
                        table.delete_item(Key={'video_id': video_id})
                        deleted_count += 1
                        print(f"Deleted video_id: {video_id}")
                except Exception as e:
                    print(f"Error deleting video_id {video_id}: {e}")
            
            print(f"\nDeleted {deleted_count} invalid videos")
        else:
            print("Deletion cancelled")
    else:
        print("No invalid videos found")

if __name__ == '__main__':
    scan_and_delete_empty_videos()
