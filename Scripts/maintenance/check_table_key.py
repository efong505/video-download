import boto3

db = boto3.client('dynamodb')
response = db.describe_table(TableName='state-summaries')

print("Key Schema:")
for key in response['Table']['KeySchema']:
    print(f"  {key['AttributeName']} ({key['KeyType']})")
