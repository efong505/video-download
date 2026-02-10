import boto3

dynamodb = boto3.resource('dynamodb')
articles_table = dynamodb.Table('articles')

# Get first 5 articles
response = articles_table.scan(Limit=5)

print("Checking featured_image URLs in articles:\n")
for article in response['Items']:
    article_id = article.get('article_id', 'NO ID')
    title = article.get('title', 'NO TITLE')[:50]
    featured_image = article.get('featured_image', 'NO IMAGE')
    
    print(f"Article: {title}")
    print(f"ID: {article_id}")
    
    if not featured_image or featured_image == 'NO IMAGE':
        print("  [X] NO FEATURED IMAGE")
    elif featured_image.startswith('data:'):
        print(f"  [X] BASE64 IMAGE (length: {len(featured_image)})")
    elif featured_image.startswith('http://'):
        print(f"  [!] HTTP (not HTTPS): {featured_image[:100]}")
    elif featured_image.startswith('https://'):
        print(f"  [OK] HTTPS URL: {featured_image[:100]}")
    else:
        print(f"  [?] UNKNOWN FORMAT: {featured_image[:100]}")
    
    print()
