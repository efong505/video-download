import json
import boto3
import traceback

ses = boto3.client('ses', region_name='us-east-1')

def lambda_handler(event, context):
    print(f'Event: {json.dumps(event)}')
    
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }
    
    try:
        if event.get('httpMethod') == 'OPTIONS':
            return {'statusCode': 200, 'headers': headers, 'body': ''}
        
        body = json.loads(event.get('body', '{}'))
        print(f'Body: {json.dumps(body)}')
        
        to_email = body.get('to_email', 'contact@christianconservativestoday.com')
        subject = body.get('subject', 'Contact Form Submission')
        message = body.get('message', '')
        
        print(f'Sending email to {to_email}')
        
        response = ses.send_email(
            Source='contact@christianconservativestoday.com',
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': message}}
            }
        )
        
        print(f'SES Response: {json.dumps(response, default=str)}')
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Email sent successfully'})
        }
    except Exception as e:
        print(f'Error: {str(e)}')
        print(f'Traceback: {traceback.format_exc()}')
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
