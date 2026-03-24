"""
Scheduled Content Publisher Lambda
Runs every 5 minutes via EventBridge to check for scheduled content that should be published
"""
import json
import boto3
from datetime import datetime, timezone
from decimal import Decimal

# Initialize AWS services
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
lambda_client = boto3.client('lambda', region_name='us-east-1')
news_table = dynamodb.Table('news-table')
articles_table = dynamodb.Table('articles')
subscribers_table = dynamodb.Table('email_subscribers')

def lambda_handler(event, context):
    """
    Check for scheduled news articles and articles that should be published
    """
    try:
        print("Starting scheduled publisher check...")
        current_time = datetime.now(timezone.utc)
        
        published_count = 0
        
        # Check news items
        news_response = news_table.scan(
            FilterExpression='#status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'scheduled'}
        )
        
        news_items = news_response.get('Items', [])
        print(f"Found {len(news_items)} scheduled news items")
        
        for item in news_items:
            if should_publish(item, current_time):
                publish_news(item, current_time)
                published_count += 1
        
        # Check articles
        print(f"Scanning articles table for scheduled items...")
        print(f"Table name: {articles_table.name}")
        print(f"Table ARN: {articles_table.table_arn}")
        
        # First, do a full scan with pagination to see all items
        all_articles = []
        scan_kwargs = {}
        
        while True:
            response = articles_table.scan(**scan_kwargs)
            all_articles.extend(response.get('Items', []))
            
            # Check if there are more items to scan
            last_key = response.get('LastEvaluatedKey')
            if not last_key:
                break
            scan_kwargs['ExclusiveStartKey'] = last_key
        
        print(f"Total articles in table: {len(all_articles)}")
        
        # Log status values
        status_counts = {}
        for item in all_articles:
            status = item.get('status', 'no-status')
            status_counts[status] = status_counts.get(status, 0) + 1
        print(f"Status breakdown: {status_counts}")
        
        # Now do the filtered scan with pagination
        article_items = []
        scan_kwargs = {
            'FilterExpression': '#status = :status',
            'ExpressionAttributeNames': {'#status': 'status'},
            'ExpressionAttributeValues': {':status': 'scheduled'}
        }
        
        while True:
            response = articles_table.scan(**scan_kwargs)
            article_items.extend(response.get('Items', []))
            
            last_key = response.get('LastEvaluatedKey')
            if not last_key:
                break
            scan_kwargs['ExclusiveStartKey'] = last_key
        
        print(f"Found {len(article_items)} scheduled articles")
        
        # Debug: Print article IDs and scheduled times
        for item in article_items:
            article_id = item.get('article_id', 'unknown')
            title = item.get('title', 'untitled')
            scheduled_time = item.get('scheduled_publish', 'none')
            print(f"  - Article {article_id}: {title} (scheduled for {scheduled_time})")
        
        for item in article_items:
            if should_publish(item, current_time):
                publish_article(item, current_time)
                published_count += 1
        
        total_checked = len(news_items) + len(article_items)
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'Scheduled publisher completed',
                'checked': total_checked,
                'published': published_count
            })
        }
        
    except Exception as e:
        print(f"Error in scheduled publisher: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

def should_publish(item, current_time):
    """Check if item should be published"""
    scheduled_publish = item.get('scheduled_publish', '')
    
    if not scheduled_publish:
        print(f"Item {item.get('news_id') or item.get('article_id')} has no scheduled_publish time, skipping")
        return False
    
    try:
        # Handle both timezone-aware and timezone-naive datetime strings
        scheduled_str = scheduled_publish.replace('Z', '+00:00')
        scheduled_time = datetime.fromisoformat(scheduled_str)
        
        # Ensure scheduled_time is timezone-aware
        if scheduled_time.tzinfo is None:
            scheduled_time = scheduled_time.replace(tzinfo=timezone.utc)
        
        return scheduled_time <= current_time
    except Exception as e:
        print(f"Error parsing scheduled time '{scheduled_publish}': {str(e)}")
        return False

def publish_news(item, current_time):
    """Publish a news item"""
    try:
        print(f"Publishing news item {item['news_id']}: {item.get('title', 'Untitled')}")
        
        news_table.update_item(
            Key={'news_id': item['news_id']},
            UpdateExpression='SET #status = :status, updated_at = :updated_at',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'published',
                ':updated_at': current_time.isoformat()
            }
        )
        
        send_article_notifications(item['news_id'], item.get('title', 'New Article'), 'news')
    except Exception as e:
        print(f"Error publishing news {item['news_id']}: {str(e)}")

def publish_article(item, current_time):
    """Publish an article"""
    try:
        print(f"Publishing article {item['article_id']}: {item.get('title', 'Untitled')}")
        
        articles_table.update_item(
            Key={'article_id': item['article_id']},
            UpdateExpression='SET #status = :status, updated_at = :updated_at',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={
                ':status': 'published',
                ':updated_at': current_time.isoformat()
            }
        )
        
        send_article_notifications(item['article_id'], item.get('title', 'New Article'), 'article')
    except Exception as e:
        print(f"Error publishing article {item['article_id']}: {str(e)}")

def send_article_notifications(content_id, title, content_type='news'):
    """Send notifications to subscribers about new article"""
    try:
        response = subscribers_table.scan(
            FilterExpression='#status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': 'active'}
        )
        
        notification_count = 0
        link_path = f'/news-article.html?id={content_id}' if content_type == 'news' else f'/article.html?id={content_id}'
        
        for subscriber in response.get('Items', []):
            try:
                lambda_client.invoke(
                    FunctionName='notifications_api',
                    InvocationType='Event',
                    Payload=json.dumps({
                        'action': 'send_notification',
                        'user_email': subscriber['email'],
                        'notification_type': 'article_published',
                        'title': 'New Article Published',
                        'message': f'Check out our latest {content_type}: {title}',
                        'link': link_path
                    })
                )
                notification_count += 1
            except Exception as e:
                print(f"Failed to notify {subscriber['email']}: {str(e)}")
        
        print(f"Sent {notification_count} notifications for {content_type} {content_id}")
        
    except Exception as e:
        print(f"Failed to send article notifications: {str(e)}")
