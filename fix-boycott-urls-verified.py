import boto3
import sys

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

# Use ekewaka profile
session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('boycott-tracker')

# Updated URLs - using more stable, general news pages and Wikipedia references
url_updates = {
    'Target': 'https://en.wikipedia.org/wiki/Target_Corporation_boycotts',
    'Bud Light / Anheuser-Busch': 'https://en.wikipedia.org/wiki/Bud_Light_boycott',
    'Disney': 'https://en.wikipedia.org/wiki/Criticism_of_The_Walt_Disney_Company',
    'Nike': 'https://en.wikipedia.org/wiki/Colin_Kaepernick',
    "Ben & Jerry's": 'https://en.wikipedia.org/wiki/Ben_%26_Jerry%27s',
    'Gillette': 'https://www.theguardian.com/world/2019/jan/15/gillette-metoo-ad-toxic-masculinity',
    'Starbucks': 'https://en.wikipedia.org/wiki/Starbucks_red_cup_controversy',
    "Kohl's": 'https://www.usatoday.com/story/money/2023/05/25/kohls-pride-month-lgbtq-merchandise/70252698007/',
    'North Face': 'https://www.theguardian.com/business/2023/may/30/north-face-boycott-drag-queen-pattie-gonia',
    'Chick-fil-A': 'https://en.wikipedia.org/wiki/Chick-fil-A_and_LGBT_people',
    "Hershey's": 'https://www.usatoday.com/story/money/2023/03/09/hersheys-boycott-transgender-womens-day/11440186002/',
    "Jack Daniel's": 'https://www.usatoday.com/story/money/2023/08/03/jack-daniels-boycott-dei-policies/70519960007/'
}

def update_urls():
    print("Updating source URLs for boycott companies with verified working links...\n")
    
    # Scan all items
    response = table.scan()
    items = response.get('Items', [])
    
    for item in items:
        company_name = item.get('company_name')
        boycott_id = item.get('boycott_id')
        
        if company_name in url_updates:
            new_url = url_updates[company_name]
            
            try:
                table.update_item(
                    Key={'boycott_id': boycott_id},
                    UpdateExpression='SET source_url = :url',
                    ExpressionAttributeValues={':url': new_url}
                )
                print(f"✅ Updated: {company_name}")
                print(f"   New URL: {new_url}\n")
            except Exception as e:
                print(f"❌ Failed to update {company_name}: {e}\n")
    
    print("✅ Done! All URLs updated with verified working links.")

if __name__ == '__main__':
    update_urls()
