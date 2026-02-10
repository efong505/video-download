import boto3
import base64
from io import BytesIO

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')
articles_table = dynamodb.Table('articles')

BUCKET = 'my-video-downloads-bucket'
CLOUDFRONT_DOMAIN = 'd271vky579caz9.cloudfront.net'

# Scan all articles
response = articles_table.scan()
articles = response.get('Items', [])

print(f"Found {len(articles)} articles")

converted = 0
for article in articles:
    article_id = article['article_id']
    featured_image = article.get('featured_image', '')
    
    # Check if it's a base64 image
    if featured_image.startswith('data:image/'):
        print(f"\nConverting article: {article['title'][:50]}...")
        
        # Extract base64 data
        header, encoded = featured_image.split(',', 1)
        image_data = base64.b64decode(encoded)
        
        # Determine file extension
        if 'jpeg' in header or 'jpg' in header:
            ext = 'jpg'
        elif 'png' in header:
            ext = 'png'
        else:
            ext = 'jpg'
        
        # Upload to S3
        s3_key = f'article-images/{article_id}.{ext}'
        s3.put_object(
            Bucket=BUCKET,
            Key=s3_key,
            Body=image_data,
            ContentType=f'image/{ext}'
        )
        
        # Generate CloudFront URL
        cloudfront_url = f'https://{CLOUDFRONT_DOMAIN}/{s3_key}'
        
        # Update article
        articles_table.update_item(
            Key={'article_id': article_id},
            UpdateExpression='SET featured_image = :url',
            ExpressionAttributeValues={':url': cloudfront_url}
        )
        
        print(f"  Converted to: {cloudfront_url}")
        converted += 1

print(f"\nConverted {converted} articles from base64 to S3 URLs")
