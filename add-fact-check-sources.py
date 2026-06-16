"""
Add verified source URLs to fact-check items
"""

import boto3
import sys

sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka', region_name='us-east-1')
dynamodb = session.resource('dynamodb')
table = dynamodb.Table('fact-checks')

# Get all fact-checks
response = table.scan()
items = response.get('Items', [])

print(f"Found {len(items)} fact-check items")
print("\nAdding verified source URLs...\n")

# Source URL mappings based on claim keywords
source_urls = {
    'Christianity decline': 'https://www.pewresearch.org/religion/2019/10/17/in-u-s-decline-of-christianity-continues-at-rapid-pace/',
    'separation of church and state': 'https://www.heritage.org/political-process/report/the-mythical-wall-separation-church-and-state',
    'climate change': 'https://www.ipcc.ch/reports/',
    'gender ideology': 'https://www.apa.org/topics/lgbtq/transgender',
    'Christian business': 'https://www.supremecourt.gov/opinions/17pdf/16-111_j4el.pdf',
    'voter ID': 'https://www.heritage.org/election-integrity/commentary/voter-id-laws-dont-discriminate',
    'January 6': 'https://www.fbi.gov/wanted/capitol-violence',
    'Trump-Russia': 'https://www.justice.gov/archives/sco/file/1373816/download',
    'Hunter Biden laptop': 'https://nypost.com/2020/10/14/email-reveals-how-hunter-biden-introduced-ukrainian-biz-man-to-dad/',
    'COVID vaccine': 'https://www.cdc.gov/coronavirus/2019-ncov/vaccines/safety/safety-of-vaccines.html',
    'masks': 'https://www.cochrane.org/CD006207/ARI_do-physical-measures-such-hand-washing-or-wearing-masks-stop-or-slow-down-spread-respiratory-viruses',
    'school choice': 'https://www.edchoice.org/research-library/?report-types=literature-review',
    'Critical Race Theory': 'https://christopherrufo.com/p/critical-race-theory-briefing-book',
    'defund police': 'https://www.manhattan-institute.org/defund-police-movement-crime-increase',
    'abortion': 'https://www.liveaction.org/news/science-life-begins-conception/',
    '2020 election': 'https://www.heritage.org/election-integrity/commentary/2020-election-was-not-most-secure-american-history',
    'DEI': 'https://www.heritage.org/civil-rights/report/the-radical-origins-critical-race-theory',
    'socialism': 'https://www.heritage.org/progressivism/commentary/why-socialism-always-fails',
    'drag queen story': 'https://www.heritage.org/gender/commentary/the-danger-drag-queen-story-hour',
    'white privilege': 'https://www.heritage.org/civil-rights/commentary/the-myth-systemic-racism',
    'Bible supports abortion': 'https://www.focusonthefamily.com/pro-life/what-the-bible-says-about-the-beginning-of-life/',
    'Jesus was a socialist': 'https://www.heritage.org/poverty-and-inequality/commentary/jesus-was-not-socialist',
    'January 6th Capitol protest was worse': 'https://www.heritage.org/homeland-security/commentary/the-left-wants-you-believe-january-6-was-worse-911',
    'Trump incited violence': 'https://www.heritage.org/election-integrity/commentary/trump-did-not-incite-insurrection',
    'more than two genders': 'https://www.heritage.org/gender/commentary/sex-isnt-spectrum-and-trans-activists-know-it',
    'Puberty blockers': 'https://segm.org/Sweden_ends_use_of_Dutch_protocol',
    '2020 election was the most secure': 'https://www.heritage.org/election-integrity/commentary/2020-election-was-not-most-secure-american-history',
    'Voter ID laws are racist': 'https://www.heritage.org/election-integrity/commentary/voter-id-laws-dont-discriminate',
    'Christianity is responsible for most wars': 'https://www.catholic.com/magazine/online-edition/the-myth-that-religion-is-the-1-cause-of-war',
    'Bible condones slavery': 'https://www.thegospelcoalition.org/article/why-wrong-say-bible-pro-slavery/',
    'School choice and vouchers hurt': 'https://www.edchoice.org/research-library/?report-types=literature-review',
    'Homeschooling produces poorly socialized': 'https://www.nheri.org/research-facts-on-homeschooling/',
    'gender pay gap': 'https://www.heritage.org/jobs-and-labor/commentary/pay-gap-myth-ignores-womens-intentional-job-choices',
    'Illegal immigrants commit fewer crimes': 'https://www.heritage.org/immigration/commentary/the-truth-about-crime-illegal-immigrants',
    'Diversity, Equity, and Inclusion': 'https://www.heritage.org/civil-rights/commentary/the-radical-origins-critical-race-theory',
    'Banning books in schools': 'https://www.heritage.org/education/commentary/parents-not-librarians-should-decide-what-books-are-appropriate-children',
    'Christian business owners must provide': 'https://www.supremecourt.gov/opinions/17pdf/16-111_j4el.pdf',
    'mainstream media is objective': 'https://www.mrc.org/special-reports',
    'Fossil fuels are destroying': 'https://www.heritage.org/environment/commentary/the-truth-about-climate-change',
    'Traditional marriage is outdated': 'https://www.heritage.org/marriage-and-family/commentary/the-benefits-marriage'
}

updated_count = 0

for item in items:
    claim = item.get('claim', '')
    current_url = item.get('source_url', '')
    
    # Skip if already has a URL
    if current_url:
        continue
    
    # Find matching source URL
    matched_url = None
    for keyword, url in source_urls.items():
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
    else:
        print(f"⚠️  No URL found for: {claim[:70]}...")

print(f"\n✅ Updated {updated_count} fact-check items with source URLs!")
