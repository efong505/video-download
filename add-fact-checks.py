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
table = dynamodb.Table('fact-checks')

# Fact-check items aligned with Christian conservative values
fact_checks = [
    {
        'claim': 'Christianity is declining in America',
        'verdict': 'misleading',
        'category': 'Religion',
        'source': 'Mainstream Media',
        'source_url': '',
        'explanation': 'While mainline Protestant denominations have declined, evangelical Christianity and non-denominational churches have grown significantly. Church attendance may have shifted, but Christian faith remains strong in America with over 70% identifying as Christian. The narrative ignores the rise of home churches, online ministries, and vibrant evangelical communities.'
    },
    {
        'claim': 'The Founding Fathers intended a complete separation of church and state',
        'verdict': 'false',
        'category': 'Government',
        'source': 'Secular Activists',
        'source_url': '',
        'explanation': 'The phrase "separation of church and state" does not appear in the Constitution. The First Amendment prevents government establishment of religion and protects free exercise. The Founders were deeply religious, referenced God in founding documents, and intended to prevent government interference with religion, not remove faith from public life. Congressional sessions opened with prayer from day one.'
    },
    {
        'claim': 'Climate change is the greatest threat to humanity',
        'verdict': 'misleading',
        'category': 'Science',
        'source': 'Progressive Politicians',
        'source_url': '',
        'explanation': 'While climate is changing, apocalyptic predictions have consistently failed. Greater threats include nuclear war, pandemics, loss of religious freedom, breakdown of family, and moral decay. Climate models have been wrong for decades. The focus on climate often ignores human flourishing, economic development, and stewardship principles that balance environmental care with human needs.'
    },
    {
        'claim': 'Gender is a social construct separate from biological sex',
        'verdict': 'false',
        'category': 'Science',
        'source': 'Gender Ideology Activists',
        'source_url': '',
        'explanation': 'Biological sex is determined by chromosomes (XX or XY), reproductive anatomy, and hormones. Gender dysphoria is a psychological condition affecting a tiny percentage of the population. The Bible clearly teaches God created male and female (Genesis 1:27). Modern gender ideology contradicts basic biology, harms children through irreversible medical interventions, and undermines parental rights.'
    },
    {
        'claim': 'Christian businesses must participate in same-sex weddings',
        'verdict': 'false',
        'category': 'Religion',
        'source': 'LGBTQ Activists',
        'source_url': '',
        'explanation': 'The First Amendment protects religious freedom and free exercise. Multiple Supreme Court cases (Masterpiece Cakeshop, 303 Creative) have affirmed that Christians cannot be compelled to violate their religious beliefs. Forcing participation in ceremonies that contradict one\'s faith violates constitutional rights. Religious liberty is a fundamental American freedom.'
    },
    {
        'claim': 'Voter ID laws are racist and suppress minority votes',
        'verdict': 'false',
        'category': 'Government',
        'source': 'Democratic Politicians',
        'source_url': '',
        'explanation': 'Voter ID is required for countless activities (banking, flying, buying alcohol). Most countries require voter ID. Studies show no suppression of minority voting in states with ID laws. The claim assumes minorities are incapable of obtaining ID, which is itself racist. Voter ID ensures election integrity and prevents fraud, protecting everyone\'s vote.'
    },
    {
        'claim': 'January 6th was an armed insurrection worse than 9/11',
        'verdict': 'false',
        'category': 'Government',
        'source': 'Democratic Politicians & Media',
        'source_url': '',
        'explanation': 'No firearms were confiscated from protesters. The only person shot was an unarmed protester (Ashli Babbitt) by Capitol Police. Comparing a protest that got out of hand to 9/11 (3,000 deaths, coordinated terrorist attack) is absurd. Many participants were let in by police. FBI found no evidence of coordinated insurrection. Political prisoners remain jailed without trial.'
    },
    {
        'claim': 'Trump colluded with Russia to steal the 2016 election',
        'verdict': 'false',
        'category': 'Government',
        'source': 'Democratic Politicians & Media',
        'source_url': '',
        'explanation': 'The Mueller Report found no evidence of collusion after 2+ years and $32 million investigation. The Steele Dossier was debunked as Clinton campaign opposition research. FBI agents involved (Strzok, Page) showed clear bias. Durham Report revealed FBI had no basis to open investigation. This was a coordinated hoax to undermine a duly elected president.'
    },
    {
        'claim': 'Hunter Biden\'s laptop was Russian disinformation',
        'verdict': 'false',
        'category': 'Media',
        'source': '51 Intelligence Officials & Media',
        'source_url': '',
        'explanation': 'The laptop is 100% authentic, confirmed by FBI, New York Times, Washington Post, and CBS. It contains evidence of Biden family corruption, influence peddling, and potential crimes. 51 intelligence officials lied to influence the 2020 election. Social media censored the story. This was election interference by intelligence community and media to protect Biden.'
    },
    {
        'claim': 'COVID vaccines prevent transmission and infection',
        'verdict': 'false',
        'category': 'Health',
        'source': 'CDC, Fauci, Biden Administration',
        'source_url': '',
        'explanation': 'Vaccinated people still get and spread COVID. CDC Director Walensky admitted vaccines don\'t prevent transmission. Biden, Fauci, and media repeatedly claimed vaccines would stop spread - this was false. Natural immunity is stronger than vaccine immunity. Mandates were based on false premise that vaccines stop transmission. Many suffered vaccine injuries.'
    },
    {
        'claim': 'Masks effectively prevent COVID transmission',
        'verdict': 'misleading',
        'category': 'Health',
        'source': 'CDC & Public Health Officials',
        'source_url': '',
        'explanation': 'Cochrane Review (gold standard) found masks make little to no difference. Cloth masks are ineffective. N95 masks may provide minimal benefit if worn properly (most don\'t). States without mask mandates had similar or better outcomes than masked states. Children were harmed by masking (speech delays, social development). Mask mandates were political theater, not science.'
    },
    {
        'claim': 'School choice and vouchers hurt public education',
        'verdict': 'false',
        'category': 'Education',
        'source': 'Teachers Unions',
        'source_url': '',
        'explanation': 'School choice improves outcomes for all students through competition. Parents, not government, should control their children\'s education. Public schools have failed inner-city minorities for decades while unions protect bad teachers. Vouchers give poor families the same choices wealthy families have. Competition drives improvement. Teachers unions oppose choice to protect their monopoly, not children.'
    },
    {
        'claim': 'Critical Race Theory is not taught in K-12 schools',
        'verdict': 'false',
        'category': 'Education',
        'source': 'School Boards & Media',
        'source_url': '',
        'explanation': 'CRT principles (systemic racism, white privilege, equity over equality) are embedded throughout curricula. Teachers admit teaching it. Whistleblowers have exposed training materials. The semantic argument that "CRT is only in law schools" is gaslighting. Parents see the racist content in their children\'s homework. Schools teach children to judge by skin color, not character.'
    },
    {
        'claim': 'Defunding police will reduce crime and help communities',
        'verdict': 'false',
        'category': 'Government',
        'source': 'Progressive Politicians',
        'source_url': '',
        'explanation': 'Every city that defunded police saw massive crime increases. Murders, carjackings, and violent crime skyrocketed. Poor and minority communities suffer most from lack of policing. Criminals are emboldened when police are defunded. Even progressive cities are refunding police after disaster. Law and order protects the vulnerable; defunding police is deadly ideology.'
    },
    {
        'claim': 'Abortion is healthcare and women\'s rights',
        'verdict': 'false',
        'category': 'Family',
        'source': 'Abortion Activists',
        'source_url': '',
        'explanation': 'Abortion ends a human life - this is biological fact. The unborn child has unique DNA, heartbeat, and brain activity. "Healthcare" heals; abortion kills. The baby has no voice or rights. Science and ultrasound technology prove life begins at conception. Most abortions are elective, not for health reasons. Adoption is the loving alternative. Every life has value from conception.'
    },
    {
        'claim': 'The 2020 election was the most secure in history',
        'verdict': 'misleading',
        'category': 'Government',
        'source': 'CISA & Media',
        'source_url': '',
        'explanation': 'Mass mail-in ballots, ballot harvesting, drop boxes, and relaxed signature verification created unprecedented opportunities for fraud. Swing states stopped counting simultaneously. Statistical anomalies and impossible vote spikes occurred. Courts refused to hear evidence on procedural grounds. Big Tech censored fraud allegations. Audits found irregularities. "Most secure" claim was political, not factual.'
    },
    {
        'claim': 'Diversity, Equity, and Inclusion (DEI) promotes fairness',
        'verdict': 'false',
        'category': 'Economics',
        'source': 'Corporate America & Universities',
        'source_url': '',
        'explanation': 'DEI is discrimination rebranded. It judges people by immutable characteristics (race, gender) rather than merit and character. "Equity" means equal outcomes through discrimination, not equal opportunity. DEI creates hostile environments for conservatives and Christians. It\'s Marxist ideology dividing people by identity groups. True fairness is colorblind meritocracy and equal treatment under law.'
    },
    {
        'claim': 'Socialism has never been tried properly',
        'verdict': 'false',
        'category': 'Economics',
        'source': 'Socialist Activists',
        'source_url': '',
        'explanation': 'Socialism has been tried repeatedly: USSR, China, Cuba, Venezuela, North Korea, Cambodia, East Germany. Every attempt resulted in poverty, oppression, and death. Over 100 million killed by socialist regimes. The problem is socialism itself - centralized control destroys freedom and prosperity. Capitalism has lifted billions from poverty. Free markets and private property create wealth; socialism destroys it.'
    },
    {
        'claim': 'Drag Queen Story Hour is just about reading to children',
        'verdict': 'false',
        'category': 'Family',
        'source': 'LGBTQ Activists',
        'source_url': '',
        'explanation': 'DQSH exposes children to adult sexual content and gender ideology. Drag is adult entertainment, not children\'s programming. Multiple registered sex offenders have participated. It grooms children to accept inappropriate sexual content. Parents are right to protect children from sexualization. Libraries should promote literacy, not political agendas. Children\'s innocence should be protected.'
    },
    {
        'claim': 'White privilege is systemic and affects all aspects of society',
        'verdict': 'misleading',
        'category': 'Media',
        'source': 'Critical Race Theorists',
        'source_url': '',
        'explanation': 'America has made enormous progress on race. Legal discrimination ended 60 years ago. Affirmative action discriminates in favor of minorities. Asian Americans outperform whites economically despite being minorities. Success correlates with family structure, education, and work ethic, not race. "White privilege" ignores poor whites and successful minorities. It\'s divisive ideology that judges by skin color, contradicting MLK\'s dream.'
    }
]

def add_fact_checks():
    print("Adding fact-check items to database...\n")
    
    for fact in fact_checks:
        fact_id = str(uuid.uuid4())
        item = {
            'id': fact_id,
            'claim': fact['claim'],
            'verdict': fact['verdict'],
            'category': fact['category'],
            'source': fact['source'],
            'source_url': fact['source_url'],
            'explanation': fact['explanation'],
            'agree_votes': 0,
            'disagree_votes': 0,
            'voted_by': {},
            'submitted_by': 'admin',
            'created_at': datetime.utcnow().isoformat()
        }
        
        try:
            table.put_item(Item=item)
            print(f"✅ Added: {fact['claim'][:60]}...")
        except Exception as e:
            print(f"❌ Failed to add fact-check: {e}")
    
    print(f"\n✅ Done! Added {len(fact_checks)} fact-check items.")
    print("\n📝 Note: Source URLs are empty - you can add specific sources via the fact-check page or admin interface.")

if __name__ == '__main__':
    add_fact_checks()
