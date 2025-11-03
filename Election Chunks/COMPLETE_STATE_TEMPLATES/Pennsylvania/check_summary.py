import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

response = summaries_table.get_item(Key={'state': 'Pennsylvania'})
content = response['Item']['content']

# Find the line with Total Candidates
for line in content.split('\n'):
    if 'Total Candidates' in line:
        print(line)
        break
