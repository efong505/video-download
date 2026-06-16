import boto3
import uuid
import sys
from datetime import datetime

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('media-bias-tracker')

sample_reports = [
    {
        'outlet_name': 'CNN',
        'category': 'Anti-Conservative',
        'description': 'Consistently frames conservative viewpoints as extremist while presenting liberal positions as mainstream and reasonable.',
        'severity': 'severe',
        'evidence_url': 'https://www.newsbusters.org/cnn',
        'votes': 847,
        'status': 'verified'
    },
    {
        'outlet_name': 'MSNBC',
        'category': 'Anti-Christian',
        'description': 'Regular mockery of Christian beliefs and portrayal of evangelical Christians as dangerous to democracy.',
        'severity': 'severe',
        'evidence_url': 'https://www.mrctv.org/msnbc',
        'votes': 623,
        'status': 'verified'
    },
    {
        'outlet_name': 'New York Times',
        'category': 'Omission',
        'description': 'Systematically omits coverage of Hunter Biden laptop story and Biden family corruption allegations.',
        'severity': 'severe',
        'evidence_url': 'https://nypost.com/2020/10/14/email-reveals-how-hunter-biden-introduced-ukrainian-biz-man-to-dad/',
        'votes': 1203,
        'status': 'verified'
    },
    {
        'outlet_name': 'Washington Post',
        'category': 'False Reporting',
        'description': 'Published false "Russian bounties" story that was later debunked but never properly retracted.',
        'severity': 'severe',
        'evidence_url': 'https://www.wsj.com/articles/russian-bounties-story-falls-apart-11619395842',
        'votes': 891,
        'status': 'verified'
    },
    {
        'outlet_name': 'ABC News',
        'category': 'Censorship',
        'description': 'Refused to air Amy Robach segment on Jeffrey Epstein despite having evidence years before arrest.',
        'severity': 'severe',
        'evidence_url': 'https://www.projectveritas.com/news/breaking-abc-news-anchor-amy-robach-caught-on-hot-mic-saying-network/',
        'votes': 567,
        'status': 'verified'
    },
    {
        'outlet_name': 'NPR',
        'category': 'Anti-Conservative',
        'description': 'Refused to cover Hunter Biden laptop story, calling it a "distraction" despite being publicly funded.',
        'severity': 'moderate',
        'evidence_url': 'https://www.npr.org/2020/10/22/926935118/we-dont-want-to-waste-our-time-on-stories-that-are-not-really-stories',
        'votes': 445,
        'status': 'verified'
    },
    {
        'outlet_name': 'CBS News',
        'category': 'Propaganda',
        'description': 'Edited Kamala Harris 60 Minutes interview to remove word salad answers and make her appear more coherent.',
        'severity': 'severe',
        'evidence_url': '',
        'votes': 723,
        'status': 'active'
    },
    {
        'outlet_name': 'NBC News',
        'category': 'Anti-Christian',
        'description': 'Portrayed Kyle Rittenhouse as white supremacist despite evidence showing self-defense.',
        'severity': 'moderate',
        'evidence_url': 'https://www.foxnews.com/media/nbc-news-kyle-rittenhouse-white-supremacist',
        'votes': 512,
        'status': 'verified'
    }
]

print("Populating media-bias-tracker table...")
for report in sample_reports:
    item = {
        'report_id': str(uuid.uuid4()),
        'outlet_name': report['outlet_name'],
        'category': report['category'],
        'description': report['description'],
        'severity': report['severity'],
        'votes': report['votes'],
        'status': report.get('status', 'active'),
        'created_at': datetime.utcnow().isoformat(),
        'submitted_by': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2',
        'voted_by': []
    }
    if report['evidence_url']:
        item['evidence_url'] = report['evidence_url']
    
    table.put_item(Item=item)
    print(f"✓ Added: {report['outlet_name']}")

print(f"\n✅ Successfully populated {len(sample_reports)} media bias reports")
