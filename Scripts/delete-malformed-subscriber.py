import boto3
session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
ddb = session.resource('dynamodb')
table = ddb.Table('book-subscribers')
email = "test-drip-$(get-date -format 'yyyymmddhhmmss')@example.com"
table.delete_item(Key={'email': email})
print(f'Deleted: {email}')
