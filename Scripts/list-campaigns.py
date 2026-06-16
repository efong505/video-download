import boto3
session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
ddb = session.resource('dynamodb')
table = ddb.Table('user-email-campaigns')
resp = table.query(
    KeyConditionExpression='user_id = :uid',
    ExpressionAttributeValues={':uid': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2'}
)
for c in resp['Items']:
    print(f"{c['campaign_id'][:8]}... | {c.get('campaign_name','')} | seq {c.get('sequence_number',0)} | group {c.get('campaign_group','')}")
