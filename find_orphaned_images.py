#!/usr/bin/env python3
"""
Find and delete orphaned images in S3 bucket.
Orphaned images are those that exist in S3 but are not referenced in any article or news item.
"""

import boto3
import json
from urllib.parse import urlparse

# Initialize AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Configuration
BUCKET_NAME = 'my-video-downloads-bucket'
ARTICLES_TABLE = 'articles'
NEWS_TABLE = 'news-table'

# Image prefixes to check
IMAGE_PREFIXES = ['images/', 'news-images/']

def get_all_s3_images():
    """Get all image files from S3"""
    print(f"Scanning S3 bucket: {BUCKET_NAME}")
    images = []
    
    for prefix in IMAGE_PREFIXES:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=BUCKET_NAME, Prefix=prefix)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    # Only include actual image files
                    if key.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                        images.append({
                            'key': key,
                            'size': obj['Size'],
                            'last_modified': obj['LastModified']
                        })
    
    print(f"Found {len(images)} images in S3")
    return images

def get_referenced_images():
    """Get all images referenced in articles and news"""
    print("Scanning DynamoDB for referenced images...")
    referenced = set()
    
    # Scan articles table
    articles_table = dynamodb.Table(ARTICLES_TABLE)
    try:
        response = articles_table.scan()
        articles = response.get('Items', [])
        
        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = articles_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            articles.extend(response.get('Items', []))
        
        for article in articles:
            featured_image = article.get('featured_image', '')
            if featured_image and BUCKET_NAME in featured_image:
                # Extract S3 key from URL
                key = featured_image.split('.com/')[-1]
                referenced.add(key)
        
        print(f"Found {len(articles)} articles with {len([a for a in articles if a.get('featured_image')])} featured images")
    except Exception as e:
        print(f"Error scanning articles: {e}")
    
    # Scan news table
    news_table = dynamodb.Table(NEWS_TABLE)
    try:
        response = news_table.scan()
        news_items = response.get('Items', [])
        
        # Handle pagination
        while 'LastEvaluatedKey' in response:
            response = news_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            news_items.extend(response.get('Items', []))
        
        for news in news_items:
            featured_image = news.get('featured_image', '')
            if featured_image and BUCKET_NAME in featured_image:
                # Extract S3 key from URL
                key = featured_image.split('.com/')[-1]
                referenced.add(key)
        
        print(f"Found {len(news_items)} news items with {len([n for n in news_items if n.get('featured_image')])} featured images")
    except Exception as e:
        print(f"Error scanning news: {e}")
    
    print(f"Total referenced images: {len(referenced)}")
    return referenced

def find_orphaned_images():
    """Find images in S3 that are not referenced in DynamoDB"""
    s3_images = get_all_s3_images()
    referenced_images = get_referenced_images()
    
    orphaned = []
    for img in s3_images:
        if img['key'] not in referenced_images:
            orphaned.append(img)
    
    return orphaned

def format_size(bytes):
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} TB"

def main():
    print("=" * 60)
    print("Orphaned Image Finder")
    print("=" * 60)
    print()
    
    orphaned = find_orphaned_images()
    
    if not orphaned:
        print("\n✓ No orphaned images found!")
        return
    
    print(f"\n⚠ Found {len(orphaned)} orphaned images:")
    print()
    
    total_size = sum(img['size'] for img in orphaned)
    
    # Sort by size descending
    orphaned.sort(key=lambda x: x['size'], reverse=True)
    
    for i, img in enumerate(orphaned, 1):
        print(f"{i}. {img['key']}")
        print(f"   Size: {format_size(img['size'])}")
        print(f"   Last Modified: {img['last_modified']}")
        print()
    
    print(f"Total wasted storage: {format_size(total_size)}")
    print()
    
    # Ask if user wants to delete
    response = input("Do you want to delete these orphaned images? (yes/no): ").strip().lower()
    
    if response == 'yes':
        print("\nDeleting orphaned images...")
        deleted_count = 0
        failed_count = 0
        
        for img in orphaned:
            try:
                s3.delete_object(Bucket=BUCKET_NAME, Key=img['key'])
                print(f"✓ Deleted: {img['key']}")
                deleted_count += 1
            except Exception as e:
                print(f"✗ Failed to delete {img['key']}: {e}")
                failed_count += 1
        
        print()
        print(f"Deleted: {deleted_count}")
        print(f"Failed: {failed_count}")
        print(f"Freed storage: {format_size(sum(img['size'] for img in orphaned[:deleted_count]))}")
    else:
        print("\nNo images deleted.")
        print("\nTo delete specific images manually, use:")
        print("aws s3 rm s3://my-video-downloads-bucket/<key>")

if __name__ == '__main__':
    main()
