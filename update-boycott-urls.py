import boto3
import sys

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

# Use ekewaka profile
session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('boycott-tracker')

# Updated URLs for existing companies
url_updates = {
    'Target': 'https://www.foxbusiness.com/retail/target-removes-some-lgbtq-merchandise-after-customer-backlash',
    'Bud Light / Anheuser-Busch': 'https://www.nbcnews.com/business/business-news/bud-light-sales-decline-dylan-mulvaney-backlash-rcna82745',
    'Disney': 'https://www.reuters.com/business/media-telecom/disney-faces-florida-backlash-over-dont-say-gay-bill-2022-03-10/',
    'Nike': 'https://www.cnbc.com/2018/09/04/nikes-online-sales-jumped-31percent-after-company-unveiled-kaepernick-campaign.html',
    "Ben & Jerry's": 'https://www.bbc.com/news/business-57886155',
    'Gillette': 'https://www.bbc.com/news/business-46857614',
    'Starbucks': 'https://www.usatoday.com/story/money/2015/11/08/starbucks-red-cups-controversy/75354396/',
    "Kohl's": 'https://www.newsweek.com/kohls-faces-boycott-calls-over-pride-month-collection-1803456',
    'North Face': 'https://www.washingtonexaminer.com/news/business/north-face-boycott-calls-drag-queen-partnership',
    'Chick-fil-A': 'https://www.businessinsider.com/chick-fil-a-hires-diversity-equity-and-inclusion-officer-2021-5',
    "Hershey's": 'https://www.newsweek.com/hersheys-faces-boycott-calls-over-international-womens-day-campaign-1786313',
    "Jack Daniel's": 'https://www.newsweek.com/jack-daniels-faces-boycott-calls-over-dei-policies-1819644'
}

def update_urls():
    print("Updating source URLs for boycott companies...\n")
    
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
    
    print("✅ Done! All URLs updated.")

if __name__ == '__main__':
    update_urls()
