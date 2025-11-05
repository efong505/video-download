import boto3
import json

lambda_client = boto3.client('lambda')
dynamodb = boto3.resource('dynamodb')
subscribers_table = dynamodb.Table('email_subscribers')

def notify_article_published(article_id, article_title):
    """Send notification to subscribers when article is published"""
    try:
        # Get active subscribers who want article notifications
        response = subscribers_table.scan()
        subscribers = response.get('Items', [])
        active_subscribers = [s for s in subscribers if s.get('status') == 'active']
        
        for subscriber in active_subscribers:
            try:
                lambda_client.invoke(
                    FunctionName='notifications_api',
                    InvocationType='Event',
                    Payload=json.dumps({
                        'body': json.dumps({
                            'action': 'send_notification',
                            'type': 'article_published',
                            'recipient_email': subscriber['email'],
                            'subject': 'New Article Published',
                            'message': f'A new article has been published: "{article_title}"',
                            'link': f'https://christianconservativestoday.com/article.html?id={article_id}'
                        })
                    })
                )
            except Exception as e:
                print(f'Failed to notify {subscriber["email"]}: {e}')
    except Exception as e:
        print(f'Error sending article notifications: {e}')

# This function can be called from admin_api when publishing articles
