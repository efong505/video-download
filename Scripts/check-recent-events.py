import boto3, json
session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
ddb = session.resource('dynamodb')
table = ddb.Table('user-email-events')
resp = table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'},
    ScanIndexForward=False,
    Limit=10
)
for e in resp['Items']:
    print(f"{e.get('event_type')} | {e.get('subscriber_email')} | {e.get('campaign_id')} | {e.get('metadata','')}")
