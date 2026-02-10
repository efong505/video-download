import json
import boto3
import os
import requests
from datetime import datetime, timedelta

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
purchases_table = dynamodb.Table('book_purchases')

BUCKET_NAME = 'my-video-downloads-bucket'
BOOK_PDF_KEY = 'books/the-necessary-evil-full-second-edition-E-book.pdf'
PAYPAL_IPN_URL = 'https://ipnpb.paypal.com/cgi-bin/webscr'  # Live

def lambda_handler(event, context):
    try:
        method = event.get('httpMethod', 'POST')
        
        if method == 'OPTIONS':
            return cors_response(200, '')
        
        query_params = event.get('queryStringParameters') or {}
        action = query_params.get('action')
        
        if action == 'ipn':
            return handle_paypal_ipn(event)
        elif action == 'generate_link':
            return generate_download_link(event)
        else:
            return cors_response(404, {'error': 'Endpoint not found'})
            
    except Exception as e:
        print(f'Error: {str(e)}')
        return cors_response(500, {'error': str(e)})

def handle_paypal_ipn(event):
    """Handle PayPal Instant Payment Notification"""
    try:
        body = event.get('body', '')
        print(f'Received IPN: {body}')
        
        # Verify IPN with PayPal
        verify_params = 'cmd=_notify-validate&' + body
        verify_response = requests.post(PAYPAL_IPN_URL, data=verify_params)
        
        if verify_response.text != 'VERIFIED':
            print(f'IPN verification failed: {verify_response.text}')
            return cors_response(400, {'error': 'IPN verification failed'})
        
        # Parse IPN data
        ipn_data = {}
        for param in body.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                ipn_data[key] = value
        
        payment_status = ipn_data.get('payment_status')
        txn_id = ipn_data.get('txn_id')
        payer_email = ipn_data.get('payer_email')
        item_name = ipn_data.get('item_name')
        mc_gross = ipn_data.get('mc_gross')
        
        if payment_status == 'Completed':
            download_url = generate_signed_url(BOOK_PDF_KEY, 7)
            
            purchases_table.put_item(Item={
                'transaction_id': txn_id,
                'email': payer_email,
                'product': item_name,
                'amount': mc_gross,
                'download_url': download_url,
                'purchase_date': datetime.utcnow().isoformat(),
                'expiry_date': (datetime.utcnow() + timedelta(days=7)).isoformat()
            })
            
            send_download_email(payer_email, download_url, txn_id)
            send_admin_notification(payer_email, txn_id, mc_gross)
            
            return cors_response(200, {'status': 'processed'})
        else:
            return cors_response(200, {'status': 'ignored'})
            
    except Exception as e:
        print(f'IPN error: {str(e)}')
        return cors_response(500, {'error': str(e)})

def generate_download_link(event):
    """Generate download link for manual requests"""
    try:
        query_params = event.get('queryStringParameters') or {}
        email = query_params.get('email')
        txn_id = query_params.get('txn_id')
        
        if not email or not txn_id:
            return cors_response(400, {'error': 'Email and transaction ID required'})
        
        download_url = generate_signed_url(BOOK_PDF_KEY, 7)
        
        purchases_table.put_item(Item={
            'transaction_id': txn_id,
            'email': email,
            'product': 'The Necessary Evil - Digital PDF',
            'download_url': download_url,
            'purchase_date': datetime.utcnow().isoformat(),
            'expiry_date': (datetime.utcnow() + timedelta(days=7)).isoformat()
        })
        
        return cors_response(200, {'download_url': download_url})
        
    except Exception as e:
        return cors_response(500, {'error': str(e)})

def generate_signed_url(key, expiry_days=7):
    """Generate pre-signed S3 URL"""
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': BUCKET_NAME,
            'Key': key,
            'ResponseContentDisposition': 'attachment; filename="The-Necessary-Evil-Second-Edition.pdf"'
        },
        ExpiresIn=expiry_days * 24 * 60 * 60
    )
    return url

def send_download_email(customer_email, download_url, txn_id):
    """Send download link to customer"""
    message = f"""Thank you for purchasing "The Necessary Evil"!

Your digital PDF is ready for download:

{download_url}

This link expires in 7 days. Please download and save your book.

Transaction ID: {txn_id}

Questions? Contact: contact@christianconservativestoday.com

Edward Fong
ChristianConservativesToday.com"""

    requests.post(
        'https://niexv1rw75.execute-api.us-east-1.amazonaws.com/subscribe',
        json={
            'email': customer_email,
            'subject': 'Your Book Download - The Necessary Evil',
            'message': message
        }
    )

def send_admin_notification(customer_email, txn_id, amount):
    """Notify admin of new sale"""
    message = f"""New digital book sale!

Customer: {customer_email}
Transaction: {txn_id}
Amount: ${amount}
Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC

Download link sent automatically."""

    requests.post(
        'https://niexv1rw75.execute-api.us-east-1.amazonaws.com/subscribe',
        json={
            'email': 'contact@christianconservativestoday.com',
            'subject': 'New Book Sale - Digital PDF',
            'message': message
        }
    )

def cors_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
        },
        'body': json.dumps(body) if isinstance(body, dict) else body
    }
