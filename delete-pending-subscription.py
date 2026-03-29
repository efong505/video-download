import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')

subscribers_table = dynamodb.Table('email_subscribers')

try:
    subscribers_table.delete_item(Key={'email': 'ekewaka@gmail.com'})
    print("✅ Deleted pending subscription for ekewaka@gmail.com from email_subscribers table")
except Exception as e:
    print(f"❌ Error deleting subscription: {e}")
