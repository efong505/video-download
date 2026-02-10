# Update newsletter_api/index.py with confirmation system

CONFIRMATION_CODE = """
# Add to imports
import uuid
from email_templates import get_confirmation_email, get_welcome_email

# Update subscribe() function
def subscribe(event, headers):
    body = json.loads(event['body'])
    confirmation_token = str(uuid.uuid4())
    
    subscriber = {
        'email': body['email'],
        'first_name': body.get('first_name', ''),
        'last_name': body.get('last_name', ''),
        'phone': body.get('phone', ''),
        'campaigns': body.get('campaigns', ['general']),
        'status': 'pending',  # Changed from 'active'
        'confirmation_token': confirmation_token,
        'subscribed_at': datetime.utcnow().isoformat(),
        'source': body.get('source', 'website')
    }
    
    subscribers_table.put_item(Item=subscriber)
    
    # Send confirmation email
    confirmation_link = f"https://christianconservativestoday.com/confirm-email.html?token={confirmation_token}"
    email_html = get_confirmation_email(subscriber['first_name'] or 'Friend', confirmation_link)
    
    try:
        ses.send_email(
            Source='noreply@christianconservativestoday.com',
            Destination={'ToAddresses': [subscriber['email']]},
            Message={
                'Subject': {'Data': 'Please Confirm Your Subscription to Christian Conservatives Today'},
                'Body': {'Html': {'Data': email_html}}
            }
        )
    except Exception as e:
        print(f'Failed to send confirmation email: {e}')
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Please check your email to confirm subscription'})}

# Add new confirm_email() function
def confirm_email(event, headers):
    params = event.get('queryStringParameters') or {}
    token = params.get('token')
    
    if not token:
        return {'statusCode': 400, 'headers': headers, 'body': json.dumps({'error': 'token required'})}
    
    # Find subscriber by confirmation token
    response = subscribers_table.scan(
        FilterExpression='confirmation_token = :token',
        ExpressionAttributeValues={':token': token}
    )
    
    subscribers = response.get('Items', [])
    if not subscribers:
        return {'statusCode': 404, 'headers': headers, 'body': json.dumps({'error': 'Invalid or expired token'})}
    
    subscriber = subscribers[0]
    
    # Update status to active and remove token
    subscribers_table.update_item(
        Key={'email': subscriber['email']},
        UpdateExpression='SET #status = :status REMOVE confirmation_token',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': 'active'}
    )
    
    # Send welcome email
    email_html = get_welcome_email(subscriber['first_name'] or 'Friend')
    email_html = email_html.replace('{{email}}', subscriber['email'])
    
    try:
        ses.send_email(
            Source='noreply@christianconservativestoday.com',
            Destination={'ToAddresses': [subscriber['email']]},
            Message={
                'Subject': {'Data': 'Welcome to Christian Conservatives Today!'},
                'Body': {'Html': {'Data': email_html}}
            }
        )
    except Exception as e:
        print(f'Failed to send welcome email: {e}')
    
    return {'statusCode': 200, 'headers': headers, 'body': json.dumps({'message': 'Email confirmed successfully'})}

# Add to lambda_handler actions
elif action == 'confirm_email':
    return confirm_email(event, headers)
"""

print("Copy this code into newsletter_api/index.py")
print("\nSteps:")
print("1. Add email_templates.py to newsletter_api/ folder")
print("2. Update subscribe() function with confirmation logic")
print("3. Add confirm_email() function")
print("4. Add 'confirm_email' action to lambda_handler")
print("5. Deploy: cd newsletter_api && zip -r function.zip . && aws lambda update-function-code --function-name newsletter_api --zip-file fileb://function.zip")
