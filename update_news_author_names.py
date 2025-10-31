import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
news_table = dynamodb.Table('news-table')
users_table = dynamodb.Table('users')

def get_user_name(email):
    """Get user's full name from email"""
    try:
        response = users_table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        items = response.get('Items', [])
        if items:
            user = items[0]
            first_name = user.get('first_name', '')
            last_name = user.get('last_name', '')
            if first_name or last_name:
                return f"{first_name} {last_name}".strip()
        return email
    except Exception as e:
        print(f"  Error getting user name: {e}")
        return email

# Scan all news items
response = news_table.scan()
news_items = response.get('Items', [])

print(f"Found {len(news_items)} news articles")

# Update each news item with author_name
for news in news_items:
    news_id = news['news_id']
    author_email = news.get('author', '')
    
    if author_email:
        author_name = get_user_name(author_email)
        
        print(f"Updating {news['title'][:50]}...")
        print(f"  Author: {author_email} -> {author_name}")
        
        news_table.update_item(
            Key={'news_id': news_id},
            UpdateExpression='SET author_name = :author_name',
            ExpressionAttributeValues={':author_name': author_name}
        )

print("\nAll news articles updated!")
