import json
import boto3
from datetime import datetime, timedelta
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
    
    articles_table = dynamodb.Table('articles')
    articles_response = articles_table.scan()
    articles = [a for a in articles_response.get('Items', []) if a.get('created_at', '') > week_ago and a.get('status') == 'published']
    articles.sort(key=lambda x: x.get('views', 0), reverse=True)
    top_articles = articles[:3]
    
    news_table = dynamodb.Table('news-table')
    news_response = news_table.scan()
    news = [n for n in news_response.get('Items', []) if n.get('created_at', '') > week_ago and n.get('status') == 'published']
    news.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    latest_news = news[:3]
    
    prayers_table = dynamodb.Table('prayer-requests')
    prayers_response = prayers_table.scan()
    prayers = [p for p in prayers_response.get('Items', []) if p.get('status') == 'approved']
    prayers.sort(key=lambda x: x.get('prayer_count', 0), reverse=True)
    urgent_prayers = prayers[:3]
    
    events_table = dynamodb.Table('events')
    events_response = events_table.scan()
    events = [e for e in events_response.get('Items', []) if e.get('date', '') >= datetime.utcnow().isoformat()[:10] and e.get('status') == 'upcoming']
    events.sort(key=lambda x: x.get('date', ''))
    upcoming_events = events[:3]
    
    html_content = generate_digest_html(top_articles, latest_news, urgent_prayers, upcoming_events)
    
    newsletter_data = {
        'action': 'create_newsletter',
        'title': f'Weekly Digest - {datetime.utcnow().strftime("%B %d, %Y")}',
        'subject': f'📬 Your Weekly Christian Conservative Digest - {datetime.utcnow().strftime("%b %d")}',
        'content': html_content,
        'status': 'ready',
        'created_by': 'auto-digest'
    }
    
    create_response = lambda_client.invoke(
        FunctionName='newsletter_api',
        InvocationType='RequestResponse',
        Payload=json.dumps({'httpMethod': 'POST', 'body': json.dumps(newsletter_data)})
    )
    
    create_result = json.loads(create_response['Payload'].read())
    create_body = json.loads(create_result.get('body', '{}'))
    newsletter_id = create_body.get('newsletter_id')
    
    if newsletter_id:
        lambda_client.invoke(
            FunctionName='newsletter_api',
            InvocationType='RequestResponse',
            Payload=json.dumps({'httpMethod': 'POST', 'body': json.dumps({'action': 'send_newsletter', 'newsletter_id': newsletter_id})})
        )
    
    return {'statusCode': 200, 'body': json.dumps({'message': 'Weekly digest generated and sent'})}

def generate_digest_html(articles, news, prayers, events):
    html = '''
    <div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; background: #ffffff;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 28px;">📬 Weekly Digest</h1>
            <p style="color: #f0f0f0; margin: 10px 0 0 0;">Your Christian Conservative Update</p>
        </div>
        
        <div style="padding: 30px 20px;">
    '''
    
    if articles:
        html += '<h2 style="color: #333; border-bottom: 3px solid #667eea; padding-bottom: 10px;">📖 Top Articles This Week</h2>'
        for article in articles:
            html += f'''
            <div style="margin: 20px 0; padding: 15px; background: #f8f9fa; border-left: 4px solid #667eea; border-radius: 4px;">
                <h3 style="margin: 0 0 10px 0; color: #667eea;"><a href="https://christianconservativestoday.com/article.html?id={article.get('article_id')}" style="color: #667eea; text-decoration: none;">{article.get('title', 'Untitled')}</a></h3>
                <p style="margin: 0; color: #666; font-size: 14px;">{article.get('summary', '')[:150]}...</p>
            </div>
            '''
    
    if news:
        html += '<h2 style="color: #333; border-bottom: 3px solid #764ba2; padding-bottom: 10px; margin-top: 30px;">📰 Latest News</h2>'
        for item in news:
            html += f'''
            <div style="margin: 20px 0; padding: 15px; background: #f8f9fa; border-left: 4px solid #764ba2; border-radius: 4px;">
                <h3 style="margin: 0 0 10px 0; color: #764ba2;"><a href="https://christianconservativestoday.com/news.html?id={item.get('news_id')}" style="color: #764ba2; text-decoration: none;">{item.get('title', 'Untitled')}</a></h3>
                <p style="margin: 0; color: #666; font-size: 14px;">{item.get('summary', '')[:150]}...</p>
            </div>
            '''
    
    if prayers:
        html += '<h2 style="color: #333; border-bottom: 3px solid #e74c3c; padding-bottom: 10px; margin-top: 30px;">🙏 Prayer Requests</h2>'
        for prayer in prayers:
            html += f'''
            <div style="margin: 20px 0; padding: 15px; background: #fff5f5; border-left: 4px solid #e74c3c; border-radius: 4px;">
                <h3 style="margin: 0 0 10px 0; color: #e74c3c;">{prayer.get('title', 'Prayer Request')}</h3>
                <p style="margin: 0 0 10px 0; color: #666; font-size: 14px;">{prayer.get('description', '')[:150]}...</p>
                <a href="https://christianconservativestoday.com/prayer-wall.html" style="color: #e74c3c; text-decoration: none; font-size: 14px;">🙏 Pray Now</a>
            </div>
            '''
    
    if events:
        html += '<h2 style="color: #333; border-bottom: 3px solid #27ae60; padding-bottom: 10px; margin-top: 30px;">📅 Upcoming Events</h2>'
        for event in events:
            html += f'''
            <div style="margin: 20px 0; padding: 15px; background: #f0fff4; border-left: 4px solid #27ae60; border-radius: 4px;">
                <h3 style="margin: 0 0 10px 0; color: #27ae60;">{event.get('title', 'Event')}</h3>
                <p style="margin: 0 0 5px 0; color: #666; font-size: 14px;">📅 {event.get('date', '')} at {event.get('time', '')}</p>
                <p style="margin: 0 0 5px 0; color: #666; font-size: 14px;">📍 {event.get('location', '')}</p>
                <a href="https://christianconservativestoday.com/events-calendar.html" style="color: #27ae60; text-decoration: none; font-size: 14px;">View Calendar</a>
            </div>
            '''
    
    html += '''
        </div>
        
        <div style="background: #f8f9fa; padding: 20px; text-align: center; border-top: 1px solid #ddd;">
            <p style="margin: 0 0 10px 0; color: #666; font-size: 14px;">Stay connected with Christian Conservatives Today</p>
            <p style="margin: 0; font-size: 12px; color: #999;">
                <a href="https://christianconservativestoday.com" style="color: #667eea; text-decoration: none;">Visit Website</a> | 
                <a href="{{unsubscribe_link}}" style="color: #999; text-decoration: none;">Unsubscribe</a>
            </p>
        </div>
    </div>
    '''
    
    return html
