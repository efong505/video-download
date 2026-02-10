import boto3

db = boto3.resource('dynamodb')
table = db.Table('state-summaries')

# Get all summaries
summaries = table.scan()['Items']

# Update each with title and election_year
for summary in summaries:
    state = summary['state']
    
    # Set title and election_year
    title = f"{state} 2025-2026 Elections - Complete Christian Conservatives Today Guide"
    election_year = "2025-2026"
    
    # Update the item
    table.update_item(
        Key={'state': state},
        UpdateExpression='SET title = :title, election_year = :year',
        ExpressionAttributeValues={
            ':title': title,
            ':year': election_year
        }
    )
    
    print(f"Updated {state}: {title}")

print("\nAll summaries updated!")
