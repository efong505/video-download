# PowerShell script to list all states with summary guides in DynamoDB

Write-Host "Fetching states with summary guides from DynamoDB..." -ForegroundColor Cyan
Write-Host ""

# Python script to query DynamoDB
$pythonScript = @"
import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')

result = table.scan()
states = sorted([item['state'] for item in result['Items']])

print(f'Total States with Summary Guides: {len(states)}')
print('')
print('States:')
for i, state in enumerate(states, 1):
    print(f'{i:2}. {state}')
"@

# Execute Python script
python -c $pythonScript

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
