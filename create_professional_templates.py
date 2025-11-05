import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
templates_table = dynamodb.Table('newsletter_templates')

templates = [
    {
        'template_id': str(uuid.uuid4()),
        'name': 'Modern Gradient',
        'description': 'Professional gradient header with clean layout',
        'html': '''
<div style="max-width: 600px; margin: 0 auto; font-family: 'Segoe UI', Arial, sans-serif; background: #ffffff;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 50px 20px; text-align: center;">
        <h1 style="color: white; margin: 0; font-size: 32px; font-weight: 600;">Christian Conservatives Today</h1>
        <p style="color: #f0f0f0; margin: 15px 0 0 0; font-size: 16px;">Faith • Family • Freedom</p>
    </div>
    <div style="padding: 40px 30px;">
        <p style="color: #333; font-size: 16px; line-height: 1.6;">Your content here...</p>
    </div>
    <div style="background: #f8f9fa; padding: 30px; text-align: center; border-top: 1px solid #e0e0e0;">
        <p style="margin: 0 0 15px 0; color: #666; font-size: 14px;">Stay connected with us</p>
        <p style="margin: 0; font-size: 12px; color: #999;">
            <a href="https://christianconservativestoday.com" style="color: #667eea; text-decoration: none; margin: 0 10px;">Website</a> | 
            <a href="{{unsubscribe_link}}" style="color: #999; text-decoration: none; margin: 0 10px;">Unsubscribe</a>
        </p>
    </div>
</div>
        ''',
        'created_at': datetime.utcnow().isoformat()
    },
    {
        'template_id': str(uuid.uuid4()),
        'name': 'Classic Newsletter',
        'description': 'Traditional newsletter layout with sidebar',
        'html': '''
<div style="max-width: 600px; margin: 0 auto; font-family: Georgia, serif; background: #ffffff; border: 1px solid #ddd;">
    <div style="background: #2c3e50; padding: 30px; text-align: center;">
        <h1 style="color: #ecf0f1; margin: 0; font-size: 28px;">Christian Conservatives Today</h1>
        <p style="color: #bdc3c7; margin: 10px 0 0 0;">Defending Faith and Values</p>
    </div>
    <div style="padding: 30px; background: #ecf0f1;">
        <div style="background: white; padding: 25px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
            <p style="color: #2c3e50; font-size: 16px; line-height: 1.8;">Your content here...</p>
        </div>
    </div>
    <div style="background: #34495e; padding: 20px; text-align: center;">
        <p style="margin: 0; font-size: 12px; color: #bdc3c7;">
            © Christian Conservatives Today | <a href="{{unsubscribe_link}}" style="color: #3498db; text-decoration: none;">Unsubscribe</a>
        </p>
    </div>
</div>
        ''',
        'created_at': datetime.utcnow().isoformat()
    },
    {
        'template_id': str(uuid.uuid4()),
        'name': 'Patriotic Theme',
        'description': 'Red, white, and blue patriotic design',
        'html': '''
<div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; background: #ffffff;">
    <div style="background: #1e3a8a; padding: 5px 0;"></div>
    <div style="background: #dc2626; padding: 5px 0;"></div>
    <div style="background: white; padding: 40px 30px; text-align: center; border-bottom: 3px solid #1e3a8a;">
        <h1 style="color: #1e3a8a; margin: 0; font-size: 30px; font-weight: bold;">Christian Conservatives Today</h1>
        <p style="color: #dc2626; margin: 10px 0 0 0; font-size: 14px; font-weight: 600; letter-spacing: 2px;">ONE NATION UNDER GOD</p>
    </div>
    <div style="padding: 40px 30px; background: #f8fafc;">
        <p style="color: #1e293b; font-size: 16px; line-height: 1.7;">Your content here...</p>
    </div>
    <div style="background: #1e3a8a; padding: 25px; text-align: center;">
        <p style="margin: 0 0 10px 0; color: white; font-size: 14px;">God Bless America</p>
        <p style="margin: 0; font-size: 12px; color: #93c5fd;">
            <a href="https://christianconservativestoday.com" style="color: white; text-decoration: none; margin: 0 10px;">Visit Us</a> | 
            <a href="{{unsubscribe_link}}" style="color: #93c5fd; text-decoration: none; margin: 0 10px;">Unsubscribe</a>
        </p>
    </div>
</div>
        ''',
        'created_at': datetime.utcnow().isoformat()
    },
    {
        'template_id': str(uuid.uuid4()),
        'name': 'Minimalist Clean',
        'description': 'Simple, elegant design with lots of white space',
        'html': '''
<div style="max-width: 600px; margin: 0 auto; font-family: 'Helvetica Neue', Arial, sans-serif; background: #ffffff;">
    <div style="padding: 60px 40px 40px 40px; text-align: center;">
        <h1 style="color: #1a1a1a; margin: 0; font-size: 24px; font-weight: 300; letter-spacing: 3px;">CHRISTIAN CONSERVATIVES TODAY</h1>
        <div style="width: 60px; height: 2px; background: #1a1a1a; margin: 20px auto;"></div>
    </div>
    <div style="padding: 0 40px 60px 40px;">
        <p style="color: #4a4a4a; font-size: 16px; line-height: 1.8; font-weight: 300;">Your content here...</p>
    </div>
    <div style="padding: 30px 40px; text-align: center; border-top: 1px solid #e5e5e5;">
        <p style="margin: 0; font-size: 11px; color: #999; letter-spacing: 1px;">
            <a href="https://christianconservativestoday.com" style="color: #1a1a1a; text-decoration: none; margin: 0 15px;">WEBSITE</a>
            <a href="{{unsubscribe_link}}" style="color: #999; text-decoration: none; margin: 0 15px;">UNSUBSCRIBE</a>
        </p>
    </div>
</div>
        ''',
        'created_at': datetime.utcnow().isoformat()
    },
    {
        'template_id': str(uuid.uuid4()),
        'name': 'Bold Impact',
        'description': 'Eye-catching design with large typography',
        'html': '''
<div style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; background: #0f172a;">
    <div style="padding: 50px 30px; text-align: center; background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);">
        <h1 style="color: #fbbf24; margin: 0; font-size: 36px; font-weight: bold; text-transform: uppercase;">Stand Strong</h1>
        <p style="color: #e2e8f0; margin: 15px 0 0 0; font-size: 18px;">Christian Conservatives Today</p>
    </div>
    <div style="padding: 40px 30px; background: white;">
        <p style="color: #1e293b; font-size: 16px; line-height: 1.7;">Your content here...</p>
    </div>
    <div style="background: #fbbf24; padding: 30px; text-align: center;">
        <p style="margin: 0 0 15px 0; color: #0f172a; font-size: 16px; font-weight: bold;">Join the Movement</p>
        <p style="margin: 0; font-size: 12px; color: #78350f;">
            <a href="https://christianconservativestoday.com" style="color: #0f172a; text-decoration: none; margin: 0 10px; font-weight: 600;">VISIT WEBSITE</a> | 
            <a href="{{unsubscribe_link}}" style="color: #78350f; text-decoration: none; margin: 0 10px;">Unsubscribe</a>
        </p>
    </div>
</div>
        ''',
        'created_at': datetime.utcnow().isoformat()
    }
]

for template in templates:
    templates_table.put_item(Item=template)
    print(f"Created template: {template['name']}")

print("\n✓ All 5 professional templates created successfully!")
