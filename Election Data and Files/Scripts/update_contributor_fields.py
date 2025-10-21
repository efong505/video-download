"""
Add first_name, last_name, and phone_number fields to existing contributors
Usage: python update_contributor_fields.py "email@example.com" --first_name "John" --last_name "Doe" --phone "555-1234"
"""
import boto3
import sys

db = boto3.resource('dynamodb')
table = db.Table('contributors')

def update_contributor(email, first_name=None, last_name=None, phone_number=None):
    response = table.scan(
        FilterExpression='user_email = :email',
        ExpressionAttributeValues={':email': email}
    )
    
    if not response['Items']:
        print(f"Contributor not found: {email}")
        return False
    
    contributor = response['Items'][0]
    
    update_expr = []
    expr_values = {}
    
    if first_name:
        update_expr.append('first_name = :fn')
        expr_values[':fn'] = first_name
    
    if last_name:
        update_expr.append('last_name = :ln')
        expr_values[':ln'] = last_name
    
    if phone_number:
        update_expr.append('phone_number = :pn')
        expr_values[':pn'] = phone_number
    
    if update_expr:
        table.update_item(
            Key={'contributor_id': contributor['contributor_id']},
            UpdateExpression='SET ' + ', '.join(update_expr),
            ExpressionAttributeValues=expr_values
        )
        print(f"Updated {email}")
        if first_name: print(f"  First name: {first_name}")
        if last_name: print(f"  Last name: {last_name}")
        if phone_number: print(f"  Phone: {phone_number}")
        return True
    
    print("No fields to update")
    return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python update_contributor_fields.py EMAIL [--first_name NAME] [--last_name NAME] [--phone NUMBER]")
        sys.exit(1)
    
    email = sys.argv[1]
    first_name = None
    last_name = None
    phone_number = None
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--first_name' and i + 1 < len(sys.argv):
            first_name = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--last_name' and i + 1 < len(sys.argv):
            last_name = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--phone' and i + 1 < len(sys.argv):
            phone_number = sys.argv[i + 1]
            i += 2
        else:
            i += 1
    
    update_contributor(email, first_name, last_name, phone_number)
