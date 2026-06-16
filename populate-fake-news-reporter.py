import boto3
import uuid
import sys
from datetime import datetime

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('fake-news-reports')

sample_reports = [
    {
        'outlet_name': 'CNN',
        'category': 'False Claim',
        'claim': 'Trump called neo-Nazis "very fine people" after Charlottesville',
        'truth': 'Trump explicitly condemned neo-Nazis in the same press conference, saying "I\'m not talking about the neo-Nazis and white nationalists because they should be condemned totally."',
        'source_url': 'https://www.cnn.com/2017/08/15/politics/trump-charlottesville-delay/index.html',
        'evidence_url': 'https://www.politifact.com/article/2019/apr/26/context-trumps-very-fine-people-both-sides-remarks/',
        'votes': 1456,
        'status': 'debunked'
    },
    {
        'outlet_name': 'MSNBC',
        'category': 'Hoax',
        'claim': 'Russian collusion with Trump campaign proven by Mueller Report',
        'truth': 'Mueller Report found no evidence of conspiracy or coordination between Trump campaign and Russia.',
        'source_url': 'https://www.msnbc.com/rachel-maddow-show',
        'evidence_url': 'https://www.justice.gov/archives/sco/file/1373816/download',
        'votes': 1823,
        'status': 'debunked'
    },
    {
        'outlet_name': 'New York Times',
        'category': 'False Claim',
        'claim': 'Hunter Biden laptop is Russian disinformation',
        'truth': 'FBI confirmed laptop is authentic. 51 intelligence officials who signed letter had no evidence it was Russian disinformation.',
        'source_url': 'https://www.nytimes.com/2020/10/19/us/politics/hunter-biden-email-russian-disinformation.html',
        'evidence_url': 'https://www.cbsnews.com/news/hunter-biden-laptop-investigation/',
        'votes': 2134,
        'status': 'debunked'
    },
    {
        'outlet_name': 'Washington Post',
        'category': 'False Claim',
        'claim': 'Trump told Georgia officials to "find the fraud" in phone call',
        'truth': 'Trump actually said "find the fraud" not "find votes." WaPo later issued correction after audio was released.',
        'source_url': 'https://www.washingtonpost.com/politics/trump-call-georgia-investigator/2021/01/09/7a55c7fa-51cf-11eb-83e3-322644d82356_story.html',
        'evidence_url': 'https://www.wsj.com/articles/washington-post-corrects-story-on-trump-call-with-georgia-investigator-11615850142',
        'votes': 967,
        'status': 'debunked'
    },
    {
        'outlet_name': 'ABC News',
        'category': 'Misleading',
        'claim': 'COVID-19 vaccines prevent transmission of the virus',
        'truth': 'CDC later admitted vaccines do not prevent transmission, only reduce severity of symptoms.',
        'source_url': 'https://abcnews.go.com/Health/covid-19-vaccines/story?id=72308244',
        'evidence_url': 'https://www.cdc.gov/coronavirus/2019-ncov/vaccines/effectiveness/why-measure-effectiveness/breakthrough-cases.html',
        'votes': 1245,
        'status': 'debunked'
    },
    {
        'outlet_name': 'CNN',
        'category': 'False Claim',
        'claim': 'Jussie Smollett attacked by MAGA supporters in hate crime',
        'truth': 'Smollett staged the attack and paid two Nigerian brothers to assault him. He was convicted of lying to police.',
        'source_url': 'https://www.cnn.com/2019/01/29/entertainment/jussie-smollett-attack/index.html',
        'evidence_url': 'https://www.nbcchicago.com/news/local/jussie-smollett-found-guilty-on-5-of-6-counts/2707195/',
        'votes': 1678,
        'status': 'debunked'
    },
    {
        'outlet_name': 'NBC News',
        'category': 'False Claim',
        'claim': 'Covington Catholic students harassed Native American elder',
        'truth': 'Full video showed Nathan Phillips approached students and got in their face. Students did nothing wrong.',
        'source_url': 'https://www.nbcnews.com/news/us-news/native-american-elder-nathan-phillips-incident-covington-catholic-students-n960096',
        'evidence_url': 'https://www.cnn.com/2019/01/21/us/maga-hat-teens-native-american-second-video/index.html',
        'votes': 1534,
        'status': 'debunked'
    },
    {
        'outlet_name': 'MSNBC',
        'category': 'Propaganda',
        'claim': 'January 6th was an armed insurrection worse than 9/11',
        'truth': 'No firearms were confiscated from protesters. No one charged with insurrection. Comparing to 9/11 (3000 deaths) is absurd propaganda.',
        'source_url': 'https://www.msnbc.com/morning-joe',
        'evidence_url': 'https://www.factcheck.org/2021/03/capitol-protesters-were-armed-with-variety-of-weapons/',
        'votes': 1892,
        'status': 'investigating'
    }
]

print("Populating fake-news-reports table...")
for report in sample_reports:
    item = {
        'report_id': str(uuid.uuid4()),
        'outlet_name': report['outlet_name'],
        'category': report['category'],
        'claim': report['claim'],
        'truth': report['truth'],
        'votes': report['votes'],
        'status': report.get('status', 'active'),
        'created_at': datetime.utcnow().isoformat(),
        'submitted_by': 'effa3242-cf64-4021-b2b0-c8a5a9dfd6d2',
        'voted_by': []
    }
    if report.get('source_url'):
        item['source_url'] = report['source_url']
    if report.get('evidence_url'):
        item['evidence_url'] = report['evidence_url']
    
    table.put_item(Item=item)
    print(f"✓ Added: {report['claim'][:60]}...")

print(f"\n✅ Successfully populated {len(sample_reports)} fake news reports")
