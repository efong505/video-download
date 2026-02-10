import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('video-metadata')

# Scan for JD Vance videos
response = table.scan()

print(f"Total videos in metadata table: {len(response['Items'])}")
print("\nSearching for JD Vance videos...")

jd_vance_videos = [item for item in response['Items'] if 'vance' in item.get('title', '').lower()]

if jd_vance_videos:
    print(f"\nFound {len(jd_vance_videos)} JD Vance video(s):")
    for video in jd_vance_videos:
        print(f"\n{'='*60}")
        print(json.dumps(video, indent=2, default=str))
else:
    print("\nNo JD Vance videos found in metadata table!")
    print("\nThis means the video exists in TAG API response but NOT in DynamoDB.")
    print("The video might be cached or coming from a different source.")
