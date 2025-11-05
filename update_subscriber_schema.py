import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
subscribers_table = dynamodb.Table('email_subscribers')

# Scan all subscribers
response = subscribers_table.scan()
subscribers = response.get('Items', [])

print(f"Found {len(subscribers)} subscribers to update")

for sub in subscribers:
    email = sub['email']
    
    # Add missing fields
    update_expr = 'SET '
    expr_values = {}
    expr_names = {}
    updates = []
    
    # Add first_name if missing (use name field or extract from email)
    if 'first_name' not in sub:
        if 'name' in sub and sub['name']:
            parts = sub['name'].split()
            first_name = parts[0] if parts else email.split('@')[0]
        else:
            first_name = email.split('@')[0]
        updates.append('#first_name = :first_name')
        expr_values[':first_name'] = first_name
        expr_names['#first_name'] = 'first_name'
    
    # Add last_name if missing
    if 'last_name' not in sub:
        if 'name' in sub and sub['name']:
            parts = sub['name'].split()
            last_name = parts[-1] if len(parts) > 1 else ''
        else:
            last_name = ''
        updates.append('last_name = :last_name')
        expr_values[':last_name'] = last_name
    
    # Add phone if missing
    if 'phone' not in sub:
        updates.append('phone = :phone')
        expr_values[':phone'] = ''
    
    # Add campaigns if missing
    if 'campaigns' not in sub:
        updates.append('campaigns = :campaigns')
        expr_values[':campaigns'] = ['general']
    
    if updates:
        update_expr += ', '.join(updates)
        
        if expr_names:
            subscribers_table.update_item(
                Key={'email': email},
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_names,
                ExpressionAttributeValues=expr_values
            )
        else:
            subscribers_table.update_item(
                Key={'email': email},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_values
            )
        
        print(f"Updated: {email}")

print("\nAll subscribers updated successfully!")
