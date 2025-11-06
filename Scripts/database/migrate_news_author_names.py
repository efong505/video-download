import boto3
from decimal import Decimal
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Initialize AWS services
dynamodb = boto3.resource('dynamodb')
news_table = dynamodb.Table('news-table')
users_table = dynamodb.Table('users')

def get_user_name(email):
    """Get user's full name from email"""
    try:
        # Scan for user by email since email is not the primary key
        response = users_table.scan(
            FilterExpression='email = :email',
            ExpressionAttributeValues={':email': email}
        )
        
        if response.get('Items'):
            user = response['Items'][0]
            first_name = user.get('first_name', '')
            last_name = user.get('last_name', '')
            if first_name or last_name:
                return f"{first_name} {last_name}".strip()
        return email
    except Exception as e:
        print(f"Error getting user name for {email}: {e}")
        return email

def migrate_news_articles():
    """Update all news articles with author_name field"""
    print("Starting migration of news articles...")
    
    # Scan all news articles
    response = news_table.scan()
    news_items = response.get('Items', [])
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    
    for news in news_items:
        news_id = news.get('news_id')
        author_email = news.get('author')
        current_author_name = news.get('author_name')
        
        if not author_email:
            print(f"[WARN] Skipping {news_id}: No author email")
            skipped_count += 1
            continue
        
        # Get the proper author name
        author_name = get_user_name(author_email)
        
        # Only update if author_name is missing, is an email, or different
        # Check if current_author_name looks like an email (contains @)
        needs_update = (
            not current_author_name or 
            '@' in str(current_author_name) or 
            current_author_name != author_name
        )
        
        if needs_update:
            try:
                news_table.update_item(
                    Key={'news_id': news_id},
                    UpdateExpression='SET author_name = :author_name',
                    ExpressionAttributeValues={':author_name': author_name}
                )
                print(f"[OK] Updated {news_id}: {author_email} -> {author_name}")
                updated_count += 1
            except Exception as e:
                print(f"[ERROR] Error updating {news_id}: {e}")
                error_count += 1
        else:
            print(f"[SKIP] Skipped {news_id}: Already has correct author_name")
            skipped_count += 1
    
    print("\n" + "="*60)
    print("Migration Complete!")
    print(f"[OK] Updated: {updated_count}")
    print(f"[SKIP] Skipped: {skipped_count}")
    print(f"[ERROR] Errors: {error_count}")
    print(f"[TOTAL] Total: {len(news_items)}")
    print("="*60)

if __name__ == '__main__':
    migrate_news_articles()
