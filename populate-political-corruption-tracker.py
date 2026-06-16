import boto3
import uuid
import sys
from datetime import datetime

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('political-corruption-tracker')

sample_reports = [
    {
        'official_name': 'Joe Biden',
        'office': 'President',
        'location': 'Federal',
        'category': 'Conflict of Interest',
        'description': 'Hunter Biden business dealings with China and Ukraine while father was VP. Emails show "10% for the big guy." Biden family received millions from foreign entities.',
        'evidence_url': 'https://nypost.com/2020/10/14/email-reveals-how-hunter-biden-introduced-ukrainian-biz-man-to-dad/',
        'incident_date': '2020-10-14',
        'votes': 3456,
        'status': 'active'
    },
    {
        'official_name': 'Nancy Pelosi',
        'office': 'Former Speaker of the House',
        'location': 'California',
        'category': 'Conflict of Interest',
        'description': 'Husband Paul Pelosi made millions in stock trades based on insider information from congressional briefings. Consistent pattern of suspicious timing.',
        'evidence_url': 'https://www.businessinsider.com/nancy-pelosi-husband-paul-big-tech-stocks-congress-conflicts-2021-7',
        'incident_date': '2021-07-01',
        'votes': 2789,
        'status': 'active'
    },
    {
        'official_name': 'Adam Schiff',
        'office': 'Representative',
        'location': 'California',
        'category': 'Fraud',
        'description': 'Repeatedly claimed to have "evidence" of Trump-Russia collusion that never materialized. Lied to American people for years.',
        'evidence_url': 'https://www.foxnews.com/politics/adam-schiff-trump-russia-collusion-evidence',
        'incident_date': '2017-03-22',
        'votes': 2134,
        'status': 'active'
    },
    {
        'official_name': 'Eric Swalwell',
        'office': 'Representative',
        'location': 'California',
        'category': 'Conflict of Interest',
        'description': 'Had relationship with Chinese spy Fang Fang while serving on House Intelligence Committee. Refused to answer questions about relationship.',
        'evidence_url': 'https://www.axios.com/2020/12/08/china-spy-california-politicians',
        'incident_date': '2020-12-08',
        'votes': 1876,
        'status': 'active'
    },
    {
        'official_name': 'Ilhan Omar',
        'office': 'Representative',
        'location': 'Minnesota',
        'category': 'Fraud',
        'description': 'Campaign finance violations, married brother for immigration fraud, funneled campaign funds to husband\'s consulting firm.',
        'evidence_url': 'https://www.foxnews.com/politics/ilhan-omar-campaign-finance-violations',
        'incident_date': '2019-08-27',
        'votes': 1654,
        'status': 'investigating'
    },
    {
        'official_name': 'Gavin Newsom',
        'office': 'Governor',
        'location': 'California',
        'category': 'Abuse of Power',
        'description': 'Attended French Laundry dinner maskless during strict COVID lockdowns he imposed on citizens. Rules for thee but not for me.',
        'evidence_url': 'https://www.politico.com/states/california/story/2020/11/18/newsom-attended-french-laundry-party-with-more-households-than-california-advises-1337695',
        'incident_date': '2020-11-06',
        'votes': 2456,
        'status': 'resolved'
    },
    {
        'official_name': 'Andrew Cuomo',
        'office': 'Former Governor',
        'location': 'New York',
        'category': 'Abuse of Power',
        'description': 'Covered up nursing home deaths during COVID, sent COVID patients to nursing homes causing thousands of deaths, then lied about numbers.',
        'evidence_url': 'https://www.nytimes.com/2021/02/12/nyregion/new-york-nursing-homes-cuomo.html',
        'incident_date': '2020-03-25',
        'votes': 3123,
        'status': 'resolved'
    },
    {
        'official_name': 'Lori Lightfoot',
        'office': 'Former Mayor',
        'location': 'Chicago, IL',
        'category': 'Constitutional Violation',
        'description': 'Banned church services during COVID while allowing protests. Violated First Amendment religious freedom rights.',
        'evidence_url': 'https://www.chicagotribune.com/coronavirus/ct-coronavirus-chicago-churches-lightfoot-20200515-story.html',
        'incident_date': '2020-05-15',
        'votes': 1789,
        'status': 'resolved'
    },
    {
        'official_name': 'Maxine Waters',
        'office': 'Representative',
        'location': 'California',
        'category': 'Abuse of Power',
        'description': 'Called for harassment of Trump administration officials in public. Incited mob violence and intimidation.',
        'evidence_url': 'https://www.cnn.com/2018/06/25/politics/maxine-waters-trump-officials/index.html',
        'incident_date': '2018-06-23',
        'votes': 1567,
        'status': 'active'
    },
    {
        'official_name': 'Chuck Schumer',
        'office': 'Senate Majority Leader',
        'location': 'New York',
        'category': 'Abuse of Power',
        'description': 'Threatened Supreme Court justices by name saying "you will pay the price" for abortion ruling. Intimidation of judiciary.',
        'evidence_url': 'https://www.washingtonpost.com/politics/2020/03/05/schumers-threat-supreme-court-justices-was-worse-than-it-looked/',
        'incident_date': '2020-03-04',
        'votes': 1432,
        'status': 'active'
    }
]

print("Populating political-corruption-tracker table...")
for report in sample_reports:
    item = {
        'report_id': str(uuid.uuid4()),
        'official_name': report['official_name'],
        'office': report['office'],
        'location': report['location'],
        'category': report['category'],
        'description': report['description'],
        'votes': report['votes'],
        'status': report.get('status', 'active'),
        'created_at': datetime.utcnow().isoformat(),
        'submitted_by': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2',
        'voted_by': []
    }
    if report.get('evidence_url'):
        item['evidence_url'] = report['evidence_url']
    if report.get('incident_date'):
        item['incident_date'] = report['incident_date']
    
    table.put_item(Item=item)
    print(f"✓ Added: {report['official_name']}")

print(f"\n✅ Successfully populated {len(sample_reports)} political corruption reports")
