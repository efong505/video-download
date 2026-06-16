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

# Additional companies to boycott
additional_companies = [
    {
        'company_name': 'Walmart',
        'category': 'ESG/DEI',
        'reason': 'Implemented aggressive DEI policies, removed certain Christian-themed items while promoting LGBTQ+ merchandise, and pressured suppliers on ESG compliance.',
        'alternatives': 'Local stores, Costco, Sam\'s Club, online Christian retailers',
        'source_url': '',  # Add your curated source
        'status': 'watching'
    },
    {
        'company_name': 'Levi\'s',
        'category': 'Anti-Conservative',
        'reason': 'Vocal support for gun control, partnered with anti-gun organizations, and promoted progressive political causes over traditional American values.',
        'alternatives': 'Wrangler, Lee, Carhartt, local clothing stores',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Patagonia',
        'category': 'Anti-Conservative',
        'reason': 'Extreme environmental activism, anti-Trump messaging, donated company to climate change causes, promotes far-left political agenda.',
        'alternatives': 'Columbia, North Face alternatives, Carhartt, local outdoor stores',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Dick\'s Sporting Goods',
        'category': 'Anti-Conservative',
        'reason': 'Stopped selling firearms and ammunition, destroyed guns in inventory, hired gun control lobbyists, and alienated Second Amendment supporters.',
        'alternatives': 'Bass Pro Shops, Cabela\'s, Academy Sports, local gun shops',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Oreo / Mondelez',
        'category': 'Woke Marketing',
        'reason': 'Created LGBTQ+ themed cookies and marketing campaigns, promoted gender ideology and progressive social causes.',
        'alternatives': 'Hydrox, Newman\'s Own, local bakeries, homemade cookies',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Skittles / Mars',
        'category': 'Woke Marketing',
        'reason': 'Removed rainbow from packaging for Pride Month claiming LGBTQ+ community "owns" the rainbow, promoted progressive gender ideology.',
        'alternatives': 'Other candy brands, local candy stores, Jelly Belly',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Doritos / PepsiCo',
        'category': 'Woke Marketing',
        'reason': 'Featured transgender activist in Spanish marketing campaign, promoted gender ideology and progressive social causes.',
        'alternatives': 'Fritos, local chip brands, Utz, Cape Cod chips',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Miller Lite',
        'category': 'Woke Marketing',
        'reason': 'Released feminist ad attacking traditional beer marketing and masculinity, similar to Gillette\'s toxic masculinity campaign.',
        'alternatives': 'Coors, Yuengling, local craft breweries',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Cracker Barrel',
        'category': 'Other',
        'reason': 'Once a conservative favorite, shifted to promote plant-based meat alternatives and progressive menu changes, alienating traditional customer base.',
        'alternatives': 'Local diners, Bob Evans, family-owned restaurants',
        'source_url': '',
        'status': 'watching'
    },
    {
        'company_name': 'Listerine / Johnson & Johnson',
        'category': 'Woke Marketing',
        'reason': 'Promoted LGBTQ+ Pride campaigns and progressive social messaging in advertising.',
        'alternatives': 'Scope, Crest, natural mouthwash brands',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Maybelline / L\'Oreal',
        'category': 'Woke Marketing',
        'reason': 'Featured transgender influencer Dylan Mulvaney in makeup campaigns, promoted gender ideology.',
        'alternatives': 'Revlon, CoverGirl, Christian-owned beauty brands',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Kate Spade',
        'category': 'Woke Marketing',
        'reason': 'Promoted LGBTQ+ Pride collections and progressive social causes, partnered with controversial activists.',
        'alternatives': 'Coach, Michael Kors, local boutiques',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Sephora',
        'category': 'Woke Marketing',
        'reason': 'Aggressive LGBTQ+ Pride marketing, promoted gender ideology in beauty industry, partnered with transgender activists.',
        'alternatives': 'Ulta, local beauty stores, Christian-owned cosmetics',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Adidas',
        'category': 'Woke Marketing',
        'reason': 'Featured transgender model in women\'s swimwear campaign, promoted gender ideology and progressive causes.',
        'alternatives': 'New Balance, Reebok, Under Armour, local athletic stores',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Ulta Beauty',
        'category': 'Woke Marketing',
        'reason': 'Featured transgender influencer Dylan Mulvaney as face of women\'s beauty brand, promoted gender ideology.',
        'alternatives': 'Sally Beauty, local beauty stores, Christian-owned cosmetics',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Tractor Supply Co.',
        'category': 'ESG/DEI',
        'reason': 'Implemented DEI policies and Pride initiatives despite rural conservative customer base, later reversed after backlash.',
        'alternatives': 'Rural King, local farm supply stores, Fleet Farm',
        'source_url': '',
        'status': 'resolved'
    },
    {
        'company_name': 'Ford Motor Company',
        'category': 'ESG/DEI',
        'reason': 'Aggressive DEI policies, LGBTQ+ Pride marketing, ESG initiatives, and progressive corporate activism.',
        'alternatives': 'Toyota, Honda, Chevrolet, local dealerships',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Jaguar',
        'category': 'Woke Marketing',
        'reason': 'Rebranded with bizarre woke marketing campaign removing traditional car imagery, promoting abstract progressive messaging.',
        'alternatives': 'BMW, Mercedes, Lexus, American car brands',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Planet Fitness',
        'category': 'Anti-Christian',
        'reason': 'Allowed biological males in women\'s locker rooms, banned member who complained, promoted gender ideology over women\'s safety.',
        'alternatives': 'Anytime Fitness, local gyms, YMCA, home workouts',
        'source_url': '',
        'status': 'active'
    },
    {
        'company_name': 'Costco',
        'category': 'Censorship',
        'reason': 'Removed Christian-themed books from shelves while keeping other religious materials, selective censorship of conservative content.',
        'alternatives': 'Sam\'s Club, BJ\'s Wholesale, local stores',
        'source_url': '',
        'status': 'watching'
    }
]

def add_companies():
    print("Adding additional boycott companies to tracker...\n")
    
    for company in additional_companies:
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
    
    print(f"\n✅ Done! Added {len(additional_companies)} more companies to boycott tracker.")
    print("\n📝 Note: Source URLs are empty - you can add your curated sources via the admin page.")

if __name__ == '__main__':
    add_companies()
