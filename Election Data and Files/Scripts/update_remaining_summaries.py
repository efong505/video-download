import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')

states_to_update = ['Virginia', 'Georgia', 'Nebraska', 'New Mexico', 'Texas']

for state in states_to_update:
    print(f"\nUpdating {state}...")
    result = table.get_item(Key={'state': state})
    item = result['Item']
    
    # Update the content
    old_content = item['content']
    new_content = old_content.replace(
        '❌ **Cannot endorse candidates** from pulpit',
        ''
    ).replace(
        '❌ **Cannot endorse candidates from pulpit**',
        ''
    ).replace(
        '❌ **Cannot donate church funds** to campaigns',
        '❌ **Cannot donate church funds** to campaigns (personal donations allowed)'
    ).replace(
        '❌ **Cannot allow campaign materials** in church',
        ''
    )
    
    # Add endorsement line after "What Pastors Can Do"
    if '### **What Pastors Can Do (501c3 Compliant):**' in new_content:
        new_content = new_content.replace(
            '### **What Pastors Can Do (501c3 Compliant):**\n\n✅',
            '### **What Pastors Can Do (501c3 Compliant):**\n\n✅ **Endorse candidates from pulpit** (IRS now permits pastoral endorsements)\n✅'
        )
    
    # Update in DynamoDB
    item['content'] = new_content
    item['last_updated'] = datetime.utcnow().isoformat()
    table.put_item(Item=item)
    print(f"[SUCCESS] {state} updated")

print("\n[SUCCESS] All 5 states updated in DynamoDB!")
