import boto3
import json
import uuid
import sys
from datetime import datetime

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

# Use ekewaka profile
session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('boycott-tracker')

# Known companies to boycott based on anti-Christian/conservative actions
boycott_companies = [
    {
        'company_name': 'Target',
        'category': 'Woke Marketing',
        'reason': 'Promoted LGBTQ+ agenda with Pride Month displays targeting children, including "tuck-friendly" swimwear. Faced massive backlash from Christian and conservative customers.',
        'alternatives': 'Walmart, local Christian-owned stores, online retailers like MyPillow',
        'source_url': 'https://www.foxbusiness.com/retail/target-removes-some-lgbtq-merchandise-after-customer-backlash',
        'status': 'active'
    },
    {
        'company_name': 'Bud Light / Anheuser-Busch',
        'category': 'Woke Marketing',
        'reason': 'Partnered with transgender activist Dylan Mulvaney for marketing campaign, alienating core conservative customer base and mocking traditional values.',
        'alternatives': 'Coors, Yuengling, local craft breweries',
        'source_url': 'https://www.nbcnews.com/business/business-news/bud-light-sales-decline-dylan-mulvaney-backlash-rcna82745',
        'status': 'active'
    },
    {
        'company_name': 'Disney',
        'category': 'Anti-Christian',
        'reason': 'Actively promotes LGBTQ+ content in children\'s programming, opposed Florida\'s Parental Rights in Education bill, and pushes progressive ideology in entertainment.',
        'alternatives': 'Angel Studios (The Chosen, Sound of Freedom), PureFlix, DryBar Comedy',
        'source_url': 'https://www.reuters.com/business/media-telecom/disney-faces-florida-backlash-over-dont-say-gay-bill-2022-03-10/',
        'status': 'active'
    },
    {
        'company_name': 'Nike',
        'category': 'Anti-Conservative',
        'reason': 'Featured Colin Kaepernick in advertising campaigns despite his anti-American protests. Promotes social justice messaging over patriotic values.',
        'alternatives': 'New Balance, Under Armour, Reebok, local athletic stores',
        'source_url': 'https://www.cnbc.com/2018/09/04/nikes-online-sales-jumped-31percent-after-company-unveiled-kaepernick-campaign.html',
        'status': 'active'
    },
    {
        'company_name': 'Ben & Jerry\'s',
        'category': 'Anti-Conservative',
        'reason': 'Consistently promotes far-left political causes, anti-Israel stance, and progressive activism. Openly hostile to conservative values.',
        'alternatives': 'Blue Bell, Breyers, local ice cream shops, homemade ice cream',
        'source_url': 'https://www.bbc.com/news/business-57886155',
        'status': 'active'
    },
    {
        'company_name': 'Gillette',
        'category': 'Woke Marketing',
        'reason': 'Released "toxic masculinity" ad campaign attacking traditional manhood and conservative values about masculinity.',
        'alternatives': 'Harry\'s, Dollar Shave Club, Barbasol, traditional safety razors',
        'source_url': 'https://www.bbc.com/news/business-46857614',
        'status': 'active'
    },
    {
        'company_name': 'Starbucks',
        'category': 'Anti-Christian',
        'reason': 'Removed "Christmas" from holiday cups, promotes LGBTQ+ activism, and has shown hostility toward Christian employees and values.',
        'alternatives': 'Black Rifle Coffee, local Christian-owned coffee shops, Dunkin\' Donuts',
        'source_url': 'https://www.usatoday.com/story/money/2015/11/08/starbucks-red-cups-controversy/75354396/',
        'status': 'active'
    },
    {
        'company_name': 'Kohl\'s',
        'category': 'Woke Marketing',
        'reason': 'Promoted Pride Month merchandise and LGBTQ+ agenda in stores, similar to Target\'s controversial campaigns.',
        'alternatives': 'JCPenney, Belk, local department stores, online Christian retailers',
        'source_url': 'https://www.newsweek.com/kohls-faces-boycott-calls-over-pride-month-collection-1803456',
        'status': 'active'
    },
    {
        'company_name': 'North Face',
        'category': 'Anti-Conservative',
        'reason': 'Refused to fulfill order for Christian organization, promoted drag queen events, and pushed progressive social agenda.',
        'alternatives': 'Carhartt, Columbia, Patagonia alternatives, local outdoor stores',
        'source_url': 'https://www.washingtonexaminer.com/news/business/north-face-boycott-calls-drag-queen-partnership',
        'status': 'active'
    },
    {
        'company_name': 'Chick-fil-A',
        'category': 'Other',
        'reason': 'Once a Christian conservative favorite, but shifted away from traditional values by ending donations to Christian organizations and hiring DEI officer.',
        'alternatives': 'Local Christian-owned restaurants, In-N-Out Burger (still Christian-owned)',
        'source_url': 'https://www.businessinsider.com/chick-fil-a-hires-diversity-equity-and-inclusion-officer-2021-5',
        'status': 'watching'
    },
    {
        'company_name': 'Hershey\'s',
        'category': 'Woke Marketing',
        'reason': 'Featured transgender woman in International Women\'s Day campaign, promoting gender ideology over biological reality.',
        'alternatives': 'Mars, Nestle, local chocolate makers, See\'s Candies',
        'source_url': 'https://www.newsweek.com/hersheys-faces-boycott-calls-over-international-womens-day-campaign-1786313',
        'status': 'active'
    },
    {
        'company_name': 'Jack Daniel\'s',
        'category': 'ESG/DEI',
        'reason': 'Implemented aggressive DEI policies and ESG initiatives, promoting progressive corporate activism over traditional values.',
        'alternatives': 'Jim Beam, Wild Turkey, local distilleries',
        'source_url': 'https://www.newsweek.com/jack-daniels-faces-boycott-calls-over-dei-policies-1819644',
        'status': 'active'
    }
]

def add_companies():
    print("Adding known boycott companies to tracker...")
    
    for company in boycott_companies:
        boycott_id = str(uuid.uuid4())
        item = {
            'boycott_id': boycott_id,
            'company_name': company['company_name'],
            'category': company['category'],
            'reason': company['reason'],
            'alternatives': company['alternatives'],
            'source_url': company['source_url'],
            'status': company['status'],
            'boycott_votes': 0,
            'voted_by': [],
            'reported_by': 'admin',
            'created_at': datetime.utcnow().isoformat()
        }
        
        try:
            table.put_item(Item=item)
            print(f"✅ Added: {company['company_name']}")
        except Exception as e:
            print(f"❌ Failed to add {company['company_name']}: {e}")
    
    print("\n✅ Done! All companies added to boycott tracker.")

if __name__ == '__main__':
    add_companies()
