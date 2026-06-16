import boto3
import uuid
import sys
from datetime import datetime

# Fix Windows encoding
sys.stdout.reconfigure(encoding='utf-8')

session = boto3.Session(profile_name='ekewaka')
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('political-corruption-tracker')

# Cases from Kash Patel's "Government Gangsters"
government_gangsters_reports = [
    {
        'official_name': 'James Comey',
        'office': 'Former FBI Director',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Leaked classified memos to media to trigger special counsel. Signed fraudulent FISA warrants against Trump campaign. Lied to Congress about Steele Dossier verification.',
        'evidence_url': 'https://www.justice.gov/storage/120919-examination.pdf',
        'incident_date': '2016-10-21',
        'votes': 2845,
        'status': 'active'
    },
    {
        'official_name': 'Andrew McCabe',
        'office': 'Former FBI Deputy Director',
        'location': 'Federal',
        'category': 'Fraud',
        'description': 'Lied to FBI investigators and Inspector General about media leaks. Opened counterintelligence investigation against Trump without predicate.',
        'evidence_url': 'https://oig.justice.gov/reports/2018/o20180413.pdf',
        'incident_date': '2017-05-09',
        'votes': 1923,
        'status': 'active'
    },
    {
        'official_name': 'Peter Strzok',
        'office': 'Former FBI Agent',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Led Crossfire Hurricane investigation with extreme bias. Texts revealed "insurance policy" against Trump. Changed Comey\'s Clinton exoneration from "grossly negligent" to "extremely careless".',
        'evidence_url': 'https://www.justice.gov/storage/120919-examination.pdf',
        'incident_date': '2016-07-31',
        'votes': 2156,
        'status': 'active'
    },
    {
        'official_name': 'Lisa Page',
        'office': 'Former FBI Attorney',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Exchanged anti-Trump texts with Strzok while working on Clinton email and Russia investigations. Demonstrated clear bias in investigations.',
        'evidence_url': 'https://www.justice.gov/storage/120919-examination.pdf',
        'incident_date': '2016-08-15',
        'votes': 1678,
        'status': 'active'
    },
    {
        'official_name': 'John Brennan',
        'office': 'Former CIA Director',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Pushed Steele Dossier to Obama and intelligence community. Briefed Harry Reid to trigger public Russia collusion narrative. Lied about spying on Senate Intelligence Committee.',
        'evidence_url': 'https://www.dni.gov/files/ODNI/documents/assessments/ICA-declass-16MAR21.pdf',
        'incident_date': '2016-07-28',
        'votes': 2534,
        'status': 'active'
    },
    {
        'official_name': 'James Clapper',
        'office': 'Former Director of National Intelligence',
        'location': 'Federal',
        'category': 'Fraud',
        'description': 'Lied to Congress about NSA surveillance of Americans. Leaked classified information to CNN. Pushed Russia collusion narrative he knew was false.',
        'evidence_url': 'https://www.dni.gov/files/documents/ICA_2017_01.pdf',
        'incident_date': '2017-01-06',
        'votes': 1987,
        'status': 'active'
    },
    {
        'official_name': 'Sally Yates',
        'office': 'Former Deputy Attorney General',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Signed fraudulent FISA warrant against Carter Page. Ambushed Michael Flynn with FBI interview. Refused to defend Trump\'s travel ban.',
        'evidence_url': 'https://www.justice.gov/storage/120919-examination.pdf',
        'incident_date': '2017-01-24',
        'votes': 1765,
        'status': 'active'
    },
    {
        'official_name': 'Bruce Ohr',
        'office': 'Former DOJ Official',
        'location': 'Federal',
        'category': 'Conflict of Interest',
        'description': 'Funneled Steele Dossier to FBI while wife worked for Fusion GPS. Failed to disclose conflicts of interest. Acted as back channel after Steele was terminated.',
        'evidence_url': 'https://www.justice.gov/storage/120919-examination.pdf',
        'incident_date': '2016-11-21',
        'votes': 1543,
        'status': 'active'
    },
    {
        'official_name': 'Christopher Steele',
        'office': 'Foreign Intelligence Agent',
        'location': 'United Kingdom',
        'category': 'Fraud',
        'description': 'Created fraudulent dossier paid for by Clinton campaign. Lied to FBI about media contacts. Used Russian disinformation to target Trump campaign.',
        'evidence_url': 'https://www.justice.gov/storage/120919-examination.pdf',
        'incident_date': '2016-06-20',
        'votes': 2876,
        'status': 'active'
    },
    {
        'official_name': 'Kevin Clinesmith',
        'office': 'Former FBI Attorney',
        'location': 'Federal',
        'category': 'Fraud',
        'description': 'Altered CIA email to falsely claim Carter Page was NOT a CIA source, enabling fraudulent FISA warrant. Pleaded guilty to making false statement.',
        'evidence_url': 'https://www.justice.gov/usao-ct/pr/fbi-attorney-admits-altering-email-used-fisa-application-during-crossfire-hurricane',
        'incident_date': '2017-06-19',
        'votes': 1432,
        'status': 'resolved'
    },
    {
        'official_name': 'Robert Mueller',
        'office': 'Special Counsel',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Ran 2-year investigation knowing no collusion existed. Hired team of Democrat donors. Destroyed evidence (Strzok/Page phones). Ignored Clinton/Russia connections.',
        'evidence_url': 'https://www.justice.gov/archives/sco/file/1373816/download',
        'incident_date': '2017-05-17',
        'votes': 2234,
        'status': 'active'
    },
    {
        'official_name': 'Andrew Weissmann',
        'office': 'Mueller Team Prosecutor',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Attended Clinton election night party. Used prosecutorial misconduct tactics. Withheld exculpatory evidence. Targeted Trump associates with process crimes.',
        'evidence_url': 'https://www.justice.gov/archives/sco/file/1373816/download',
        'incident_date': '2017-05-17',
        'votes': 1654,
        'status': 'active'
    },
    {
        'official_name': 'Rod Rosenstein',
        'office': 'Former Deputy Attorney General',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Appointed Mueller without proper predicate. Discussed wearing wire to record Trump. Signed fraudulent FISA warrant. Scope memo for Mueller was overly broad.',
        'evidence_url': 'https://www.justice.gov/storage/120919-examination.pdf',
        'incident_date': '2017-05-17',
        'votes': 1876,
        'status': 'active'
    },
    {
        'official_name': 'Alexander Vindman',
        'office': 'Former NSC Official',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Leaked classified Trump-Zelensky call to trigger impeachment. Insubordinate to chain of command. Coordinated with Schiff staff on whistleblower complaint.',
        'evidence_url': 'https://www.whitehouse.gov/wp-content/uploads/2019/09/Unclassified09.2019.pdf',
        'incident_date': '2019-07-25',
        'votes': 1789,
        'status': 'active'
    },
    {
        'official_name': 'Eric Ciaramella',
        'office': 'CIA Analyst (alleged whistleblower)',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Alleged Ukraine whistleblower who coordinated with Schiff staff before filing complaint. Had no firsthand knowledge. Previously worked with Biden.',
        'evidence_url': 'https://www.realclearinvestigations.com/articles/2019/10/30/whistleblower_exposed_close_to_biden_brennan_dnc_oppo_researcher_120996.html',
        'incident_date': '2019-08-12',
        'votes': 1567,
        'status': 'active'
    },
    {
        'official_name': 'Merrick Garland',
        'office': 'Attorney General',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Weaponized DOJ against parents at school boards. Authorized raid on Trump\'s home. Appointed special counsel against Trump while protecting Biden.',
        'evidence_url': 'https://www.justice.gov/opa/pr/attorney-general-merrick-b-garland-statement-appointment-special-counsel',
        'incident_date': '2022-11-18',
        'votes': 3234,
        'status': 'active'
    },
    {
        'official_name': 'Christopher Wray',
        'office': 'FBI Director',
        'location': 'Federal',
        'category': 'Abuse of Power',
        'description': 'Authorized Mar-a-Lago raid. Downplayed Hunter Biden laptop as Russian disinformation. Targeted parents as domestic terrorists. Protected FBI corruption.',
        'evidence_url': 'https://www.fbi.gov/news/press-releases',
        'incident_date': '2022-08-08',
        'votes': 2987,
        'status': 'active'
    },
    {
        'official_name': 'Alejandro Mayorkas',
        'office': 'DHS Secretary',
        'location': 'Federal',
        'category': 'Constitutional Violation',
        'description': 'Refused to enforce immigration laws. Opened border causing humanitarian crisis. Lied to Congress about border security. Impeached by House.',
        'evidence_url': 'https://www.dhs.gov/news',
        'incident_date': '2021-02-02',
        'votes': 2654,
        'status': 'active'
    }
]

print("Adding Government Gangsters corruption cases to tracker...\n")
for report in government_gangsters_reports:
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

print(f"\n✅ Successfully added {len(government_gangsters_reports)} Government Gangsters cases")
print(f"\nTotal corruption reports now in tracker: {10 + len(government_gangsters_reports)}")
