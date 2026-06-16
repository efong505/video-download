import boto3
import uuid
import sys
from datetime import datetime

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('corporate-wokeness-tracker')

sample_reports = [
    {
        'company_name': 'Disney',
        'category': 'LGBTQ Agenda',
        'description': 'Publicly opposed Florida Parental Rights bill, pushed LGBTQ content in children\'s programming, and stated goal to have 50% of characters be LGBTQ or racial minorities.',
        'impact': 'Exposing children to inappropriate sexual content and undermining parental authority',
        'source_url': 'https://www.foxnews.com/media/disney-exec-admits-gay-agenda-adding-queerness-childrens-programming',
        'votes': 2341,
        'status': 'active'
    },
    {
        'company_name': 'Bud Light',
        'category': 'LGBTQ Agenda',
        'description': 'Partnered with transgender influencer Dylan Mulvaney for marketing campaign, alienating core customer base.',
        'impact': 'Promoting gender ideology and mocking biological reality',
        'source_url': 'https://www.foxbusiness.com/retail/bud-light-dylan-mulvaney-partnership-backlash',
        'votes': 3456,
        'status': 'active'
    },
    {
        'company_name': 'Target',
        'category': 'LGBTQ Agenda',
        'description': 'Sold "tuck-friendly" swimsuits for children and Pride merchandise designed by Satanist artist.',
        'impact': 'Sexualizing children and promoting occult imagery',
        'source_url': 'https://www.foxnews.com/media/target-faces-boycott-calls-over-lgbtq-pride-collection-tuck-friendly-swimsuits',
        'votes': 2789,
        'status': 'active'
    },
    {
        'company_name': 'BlackRock',
        'category': 'ESG',
        'description': 'Forces ESG policies on companies through investment control, prioritizing woke agenda over shareholder returns.',
        'impact': 'Weaponizing capital to force social engineering on American businesses',
        'source_url': 'https://www.heritage.org/energy-economics/commentary/blackrocks-esg-agenda-threatens-american-energy-and-economy',
        'votes': 1876,
        'status': 'active'
    },
    {
        'company_name': 'Nike',
        'category': 'Anti-Christian',
        'description': 'Released "Satan Shoes" with Lil Nas X containing human blood and satanic imagery, mocking Christianity.',
        'impact': 'Normalizing satanism and attacking Christian values',
        'source_url': 'https://www.bbc.com/news/world-us-canada-56614470',
        'votes': 1654,
        'status': 'monitoring'
    },
    {
        'company_name': 'Gillette',
        'category': 'Anti-Conservative',
        'description': 'Released "toxic masculinity" ad attacking traditional manhood and portraying men as inherently problematic.',
        'impact': 'Demonizing masculinity and traditional male values',
        'source_url': 'https://www.wsj.com/articles/gillettes-metoo-ad-proves-to-be-polarizing-11547582400',
        'votes': 1432,
        'status': 'monitoring'
    },
    {
        'company_name': 'Coca-Cola',
        'category': 'CRT',
        'description': 'Required employees to complete training telling them to "be less white" and embrace critical race theory.',
        'impact': 'Promoting racial division and discrimination against white employees',
        'source_url': 'https://www.newsweek.com/coca-cola-facing-backlash-says-less-white-learning-plan-was-about-workplace-inclusion-1570875',
        'votes': 1987,
        'status': 'active'
    },
    {
        'company_name': 'Bank of America',
        'category': 'DEI',
        'description': 'Implemented hiring quotas based on race and gender rather than merit, discriminating against qualified candidates.',
        'impact': 'Institutionalizing reverse discrimination and lowering standards',
        'source_url': 'https://www.americanbanker.com/news/bank-of-america-sets-ambitious-diversity-goals',
        'votes': 1234,
        'status': 'active'
    },
    {
        'company_name': 'PayPal',
        'category': 'Censorship',
        'description': 'Attempted to fine users $2,500 for "misinformation" and deplatformed conservative organizations.',
        'impact': 'Financial censorship of conservative speech',
        'source_url': 'https://www.foxbusiness.com/politics/paypal-backlash-policy-misinformation',
        'votes': 2156,
        'status': 'active'
    },
    {
        'company_name': 'American Airlines',
        'category': 'DEI',
        'description': 'Prioritized diversity over merit in pilot hiring, raising safety concerns.',
        'impact': 'Compromising passenger safety for woke ideology',
        'source_url': 'https://www.dailymail.co.uk/news/article-11930945/American-Airlines-United-Airlines-diversity-hiring-practices.html',
        'votes': 1765,
        'status': 'active'
    }
]

print("Populating corporate-wokeness-tracker table...")
for report in sample_reports:
    item = {
        'report_id': str(uuid.uuid4()),
        'company_name': report['company_name'],
        'category': report['category'],
        'description': report['description'],
        'impact': report['impact'],
        'votes': report['votes'],
        'status': report.get('status', 'active'),
        'created_at': datetime.utcnow().isoformat(),
        'submitted_by': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2',
        'voted_by': []
    }
    if report.get('source_url'):
        item['source_url'] = report['source_url']
    
    table.put_item(Item=item)
    print(f"✓ Added: {report['company_name']}")

print(f"\n✅ Successfully populated {len(sample_reports)} corporate wokeness reports")
