"""
Add remaining source URLs for fact-checks that weren't auto-matched
"""

import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('fact-checks')

# Get all fact-checks without URLs
response = table.scan()
items = response.get('Items', [])

# Manual mappings for remaining items
manual_updates = {
    'Defunding police will reduce crime': 'https://www.heritage.org/crime-and-justice/commentary/the-truth-about-crime-and-police',
    'Christianity is declining in America': 'https://www.pewresearch.org/religion/2019/10/17/in-u-s-decline-of-christianity-continues-at-rapid-pace/',
    "Hunter Biden's laptop was Russian disinformation": 'https://nypost.com/2020/10/14/email-reveals-how-hunter-biden-introduced-ukrainian-biz-man-to-dad/',
    'Gender is a social construct': 'https://www.heritage.org/gender/commentary/sex-isnt-spectrum-and-trans-activists-know-it',
    'Trump colluded with Russia': 'https://www.justice.gov/archives/sco/file/1373816/download'
}

print("Adding remaining source URLs...\n")
updated_count = 0

for item in items:
    claim = item.get('claim', '')
    current_url = item.get('source_url', '')
    
    # Skip if already has a URL
    if current_url:
        continue
    
    # Find matching manual URL
    matched_url = None
    for keyword, url in manual_updates.items():
        if keyword.lower() in claim.lower():
            matched_url = url
            break
    
    if matched_url:
        table.update_item(
            Key={'id': item['id']},
            UpdateExpression='SET source_url = :url',
            ExpressionAttributeValues={':url': matched_url}
        )
        print(f"✅ Updated: {claim[:70]}...")
        print(f"   URL: {matched_url}\n")
        updated_count += 1

print(f"\n✅ Updated {updated_count} remaining fact-check items!")
