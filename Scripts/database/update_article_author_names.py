import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
articles_table = dynamodb.Table('articles')
users_table = dynamodb.Table('users')

def get_user_name(email):
    """Get user's display name from users table"""
    try:
        # Scan users table to find user by email
        response = users_table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        
        users = response.get('Items', [])
        if users:
            user = users[0]
            first_name = user.get('first_name', '')
            last_name = user.get('last_name', '')
            
            if first_name and last_name:
                return f"{first_name} {last_name}"
            elif first_name:
                return first_name
            elif last_name:
                return last_name
        
        return email
    except Exception as e:
        print(f"Error getting user name for {email}: {e}")
        return email

def update_article_author_names():
    """Update all articles to have author_name field"""
    try:
        # Scan all articles
        response = articles_table.scan()
        articles = response.get('Items', [])
        
        print(f"Found {len(articles)} articles")
        updated_count = 0
        
        for article in articles:
            article_id = article.get('article_id')
            author = article.get('author', '')
            author_email = article.get('author_email', '')
            
            # Check if author field contains email
            if '@' in author:
                # Author field has email, need to update
                author_name = get_user_name(author)
                
                print(f"Updating article {article_id}: {author} -> {author_name}")
                
                articles_table.update_item(
                    Key={'article_id': article_id},
                    UpdateExpression='SET author = :name, author_email = :email',
                    ExpressionAttributeValues={
                        ':name': author_name,
                        ':email': author
                    }
                )
                updated_count += 1
            elif not author_email and author:
                # Has author name but no author_email, set it
                print(f"Setting author_email for article {article_id}")
                articles_table.update_item(
                    Key={'article_id': article_id},
                    UpdateExpression='SET author_email = :email',
                    ExpressionAttributeValues={':email': author}
                )
                updated_count += 1
        
        print(f"\nMigration complete! Updated {updated_count} articles")
        
    except Exception as e:
        print(f"Error during migration: {e}")

if __name__ == '__main__':
    print("Starting article author name migration...")
    update_article_author_names()
