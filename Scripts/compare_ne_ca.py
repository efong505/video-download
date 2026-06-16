import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('state-summaries')

ne = table.get_item(Key={'state': 'Nebraska'})['Item']
ca = table.get_item(Key={'state': 'California'})['Item']

with open('comparison.txt', 'w', encoding='utf-8') as f:
    f.write(f"NEBRASKA ({len(ne['content'])} chars):\n")
    f.write("="*80 + "\n")
    f.write(ne['content'][:3000] + "\n\n")
    f.write("="*80 + "\n")
    f.write(f"CALIFORNIA ({len(ca['content'])} chars):\n")
    f.write("="*80 + "\n")
    f.write(ca['content'][:3000])

print(f"Nebraska: {len(ne['content'])} chars")
print(f"California: {len(ca['content'])} chars")
print("Comparison written to comparison.txt")
