import json
import boto3
import urllib.parse
import urllib.request
from datetime import datetime
from decimal import Decimal

sns = boto3.client('sns')
ses = boto3.client('ses', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb')
orders_table = dynamodb.Table('Orders')

SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:371751795928:platform-critical-alerts'
PAYPAL_VERIFY_URL = 'https://ipnpb.paypal.com/cgi-bin/webscr'

def lambda_handler(event, context):
    try:
        body = event.get('body', '')
        ipn_data = urllib.parse.parse_qs(body)
        
        # Verify IPN
        verify_data = body + '&cmd=_notify-validate'
        req = urllib.request.Request(PAYPAL_VERIFY_URL, verify_data.encode('utf-8'))
        response = urllib.request.urlopen(req)
        
        if response.read().decode('utf-8') != 'VERIFIED':
            return {'statusCode': 400, 'body': 'Invalid IPN'}
        
        payment_status = ipn_data.get('payment_status', [''])[0]
        
        if payment_status == 'Completed':
            txn_id = ipn_data.get('txn_id', [''])[0]
            payer_email = ipn_data.get('payer_email', [''])[0]
            payer_name = ipn_data.get('first_name', [''])[0] + ' ' + ipn_data.get('last_name', [''])[0]
            item_name = ipn_data.get('item_name', [''])[0]
            amount = ipn_data.get('mc_gross', ['0'])[0]
            address = f"{ipn_data.get('address_street', [''])[0]}, {ipn_data.get('address_city', [''])[0]}, {ipn_data.get('address_state', [''])[0]} {ipn_data.get('address_zip', [''])[0]}, {ipn_data.get('address_country', [''])[0]}"
            
            timestamp = datetime.utcnow().isoformat()
            
            orders_table.put_item(Item={
                'order_id': txn_id,
                'user_id': payer_email,
                'user_email': payer_email,
                'user_name': payer_name,
                'items': [{
                    'product_id': 'paperback',
                    'name': item_name,
                    'price': Decimal(amount),
                    'quantity': 1
                }],
                'subtotal': Decimal(amount),
                'tax': Decimal('0'),
                'total': Decimal(amount),
                'status': 'paid',
                'payment_status': 'paid',
                'payment_method': 'PayPal',
                'shipping_address': address,
                'order_date': timestamp,
                'created_at': timestamp,
                'updated_at': timestamp
            })
            
            ses.send_email(
                Source='Christian Conservatives Today <contact@christianconservativestoday.com>',
                Destination={'ToAddresses': [payer_email]},
                Message={
                    'Subject': {'Data': 'Order Confirmation - Paperback Book'},
                    'Body': {'Text': {'Data': f"""Thank you for your order, {payer_name}!

Your paperback order has been received and will ship within 3-5 business days.

Order Details:
Transaction ID: {txn_id}
Product: {item_name}
Amount: ${amount}

Shipping Address:
{address}

You'll receive a tracking number once your order ships.

Thank you for your purchase!

Christian Conservatives Today
https://christianconservativestoday.com"""}}
                }
            )
            
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=f'New Paperback Order - ${amount}',
                Message=f"""NEW PAPERBACK ORDER

Transaction ID: {txn_id}
Customer: {payer_name}
Email: {payer_email}
Product: {item_name}
Amount: ${amount}

Shipping Address:
{address}

Date: {timestamp}"""
            )
        
        return {'statusCode': 200, 'body': 'IPN processed'}
        
    except Exception as e:
        print(f'Error: {str(e)}')
        import traceback
        traceback.print_exc()
        return {'statusCode': 500, 'body': str(e)}
