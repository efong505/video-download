import boto3
import base64
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
articles_table = dynamodb.Table('articles')
bucket_name = 'my-video-downloads-bucket'

def convert_base64_to_s3():
    response = articles_table.scan()
    articles = response.get('Items', [])
    
    for article in articles:
        article_id = article.get('article_id')
        featured_image = article.get('featured_image', '')
        
        if featured_image and featured_image.startswith('data:image'):
            print(f"\nConverting image for: {article.get('title')}")
            
            # Extract base64 data
            header, encoded = featured_image.split(',', 1)
            image_data = base64.b64decode(encoded)
            
            # Determine image type
            if 'jpeg' in header or 'jpg' in header:
                ext = 'jpg'
                content_type = 'image/jpeg'
            elif 'png' in header:
                ext = 'png'
                content_type = 'image/png'
            else:
                ext = 'jpg'
                content_type = 'image/jpeg'
            
            # Upload to S3 (publicly readable via bucket policy)
            filename = f"article-images/{article_id}.{ext}"
            s3.put_object(
                Bucket=bucket_name,
                Key=filename,
                Body=image_data,
                ContentType=content_type,
                CacheControl='max-age=31536000',
                Metadata={'public': 'true'}
            )
            
            # Get CloudFront URL
            image_url = f"https://d271vky579caz9.cloudfront.net/{filename}"
            
            # Update article
            articles_table.update_item(
                Key={'article_id': article_id},
                UpdateExpression='SET featured_image = :img',
                ExpressionAttributeValues={':img': image_url}
            )
            
            print(f"  Uploaded to: {image_url}")

if __name__ == '__main__':
    print("Converting base64 images to S3 URLs...")
    convert_base64_to_s3()
    print("\n✓ Done! Now run: python regenerate_all_article_previews.py")
