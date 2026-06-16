import boto3

dynamodb = boto3.client('dynamodb', region_name='us-east-1')

# List all tables
tables = dynamodb.list_tables()['TableNames']
print(f"Tables: {tables}\n")

# Try common table names
for table_name in ['StateSummaries', 'state-summaries', 'ElectionData', 'election-data']:
    if table_name in tables:
        print(f"Scanning {table_name}...")
        table = boto3.resource('dynamodb', region_name='us-east-1').Table(table_name)
        response = table.scan(FilterExpression='contains(#s, :nm)', 
                            ExpressionAttributeNames={'#s': 'state'},
                            ExpressionAttributeValues={':nm': 'New Mexico'})
        if response['Items']:
            print(f"Found in {table_name}: {response['Items'][0].keys()}")
