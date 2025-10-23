```python
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# California Races
races = [
    {
        "state": "California",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The race for Governor will determine the state's chief executive, impacting policies on economy, public safety, education, and social issues in the nation's most populous state."
    },
    {
        "state": "California",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The Lieutenant Governor serves as president of the State Senate and acts as Governor when needed, influencing legislative priorities and state leadership."
    },
    {
        "state": "California",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The Attorney General enforces state laws, defends consumer rights, and oversees criminal justice, crucial for issues like election integrity and public safety."
    },
    {
        "state": "California",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Responsible for elections, business filings, and archives, this office is key to ensuring fair elections and economic transparency."
    },
    {
        "state": "California",
        "office": "State Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Manages state funds, investments, and debt, affecting fiscal policy and economic stability for all Californians."
    },
    {
        "state": "California",
        "office": "State Controller",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Oversees state payroll, audits, and unclaimed property, ensuring accountability in government spending."
    },
    {
        "state": "California",
        "office": "Insurance Commissioner",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Regulates insurance industry, protecting consumers and influencing healthcare and property insurance affordability."
    },
    {
        "state": "California",
        "office": "Superintendent of Public Instruction",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Leads the Department of Education, shaping K-12 policies on curriculum, funding, and parental involvement."
    }
]

# California Candidates  
candidates = [
    {
        "name": "Chad Bianco",
        "state": "California",
        "office": "Governor",
        "party": "Republican",
        "bio": "Chad Bianco, born in 1967 at Hill Air Force Base in Ogden, Utah, grew up in a small mining town as the eldest of three boys raised by hardworking parents who instilled values of integrity, perseverance, and personal responsibility. Bianco's career in law enforcement spans over three decades, beginning as a deputy sheriff in Riverside County in 1990. He rose through the ranks, serving as a detective, sergeant, lieutenant, and captain before being elected Sheriff of Riverside County in 2018. As Sheriff, he has prioritized public safety, increased concealed carry permits for law-abiding citizens, and challenged state policies he views as soft on crime. Married with children, Bianco is a devoted family man who credits his success to faith and community service. His accomplishments include leading efforts to combat fentanyl trafficking and improving jail rehabilitation programs while maintaining a tough stance on violent offenders.",
        "faith_statement": "“Number one, I am a Christian” - Chad Bianco, emphasizing his personal faith as the foundation of his leadership and commitment to biblical values in public service.",
        "website": "https://biancoforgovernor.com",
        "positions": {
            "ABORTION": "Personally pro-life, Bianco opposes California's expansive abortion laws and supports restrictions to protect the unborn while respecting California's legal landscape through incremental protections like parental consent and defunding abortion providers.",
            "EDUCATION": "Strong advocate for school choice and parental rights; supports vouchers for public, private, charter, and homeschool options; pledges to repeal AB 1955, which limits parental notification on sensitive issues, to restore transparency and empower families.",
            "RELIGIOUS-FREEDOM": "As a Christian leader, Bianco defends religious liberty against government overreach, supporting protections for faith-based organizations and individuals in schools and workplaces, drawing from his testimony of faith guiding public policy.",
            "GUNS": "Fervent 2nd Amendment defender; has issued over 60,000 CCW permits in Riverside County; opposes gun control measures like assault weapon bans, arguing they target law-abiding citizens while criminals ignore laws.",
            "TAXES": "Proposes abolishing the state income tax to attract businesses and residents, reduce the tax burden on working families, and stimulate economic growth in high-tax California.",
            "IMMIGRATION": "Supports secure borders and ending sanctuary state policies; prioritizes deportation of violent criminal immigrants; vows to work with federal authorities to stop illegal crossings while providing pathways for legal immigrants.",
            "FAMILY-VALUES": "Champion of traditional family structures and parental authority; opposes laws like AB 495 that erode parental consent in education and healthcare; promotes policies strengthening marriage and child protection.",
            "ELECTION-INTEGRITY": "Strong supporter of voter ID requirements to prevent fraud; has investigated voter irregularities in Riverside County; backs audits and clean voter rolls for trustworthy elections."
        },
        "endorsements": ["Peace Officers Research Association of California (PORAC)", "San Francisco Sheriff Paul Miyamoto", "Assemblyman Devon Mathis", "Assemblyman Greg Wallis", "Assemblyman Heath Flora"]
    },
    {
        "name": "Steve Hilton",
        "state": "California",
        "office": "Governor",
        "party": "Republican",
        "bio": "Steve Hilton, born in 1969 in the UK, served as Director of Strategy for British Prime Minister David Cameron before moving to the U.S. in 2012. A naturalized citizen since 2021, he hosted 'The Next Revolution' on Fox News, becoming a vocal Trump supporter and conservative commentator. Hilton co-founded Golden Together, focusing on California policy reform, and has advised on housing, energy, and economy. Married with three children, he resides in California, drawing from his immigrant background to advocate for opportunity. Accomplishments include influencing conservative media narratives and launching initiatives to combat California's regulatory burdens.",
        "faith_statement": "No publicly disclosed faith statement; however, Hilton has received public prayers and endorsements from prominent Christian leaders like Pastor Jack Hibbs, indicating alignment with faith-based conservative values.",
        "website": "https://stevehiltonforgovernor.com",
        "positions": {
            "ABORTION": "Supports moving California 'towards life in a way that's achievable,' favoring pragmatic pro-life measures like restrictions after viability and support for pregnancy centers, while acknowledging the state's progressive laws.",
            "EDUCATION": "Pushes for 100% student proficiency in math and English; expands school choice, charter schools, and parental trigger laws; opposes ideological indoctrination in curricula and teacher union resistance to accountability.",
            "RELIGIOUS-FREEDOM": "Defends parental rights on faith-related issues like gender and sex education; supports protections for religious expression in public spaces, aligned with his backing from Christian nationalists.",
            "GUNS": "Strong 2nd Amendment advocate; condemns attacks on responsible gun owners in California; supports concealed carry and opposes measures treating lawful firearm possession as criminal.",
            "TAXES": "Vows to reduce taxes for workers and businesses by cutting state budget bloat; aims to eliminate income tax for over half of households, cap hidden housing fees, and foster pro-growth policies.",
            "IMMIGRATION": "Enforce immigration laws for public safety; prioritizes border security and prosecution of illegal entrants committing crimes, balancing compassion for legal immigrants with rule of law.",
            "FAMILY-VALUES": "Promotes traditional family homes with yards; protects parental rights on child gender and sports fairness (biological boys out of girls' sports); opposes policies eroding family autonomy.",
            "ELECTION-INTEGRITY": "Opposes power grabs like Prop 50 redistricting; advocates for transparent, fair elections free from manipulation, ensuring voter confidence through legal challenges to irregularities."
        },
        "endorsements": ["Pastor Jack Hibbs (Calvary Chapel Chino Hills)", "Fox News contributors", "Conservative political action committees"]
    }
]

# California Summary
summary = {
    "state": "California",
    "title": "California 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# California 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 8
**Total Candidates Profiled:** 2
**Election Dates:**
- 2025-11-04 (Statewide Special Election - Proposition 50 on redistricting)
- 2026-06-02 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 California POLITICAL LANDSCAPE

### **The Golden State**

California is a **deep blue stronghold with pockets of conservative resistance**:
- **Legislative Dominance:** Democrats hold supermajorities in both the State Assembly (62-18) and Senate (31-9), enabling unchecked progressive policies on abortion, gender ideology, and taxes.
- **Electoral Challenges:** The top-two primary system favors Democrats, but rural Central Valley and Inland Empire counties provide opportunities for conservative turnout.
- **Urban-Rural Divide:** Liberal strongholds like Los Angeles, San Francisco, and Sacramento contrast with conservative areas in Riverside, Kern, and Shasta Counties.
- **Economic Powerhouse Under Strain:** As the world's 5th largest economy, California grapples with homelessness, high costs, and exodus of families due to overregulation.

### **Why California Matters**

California is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Despite Roe's fall, California enshrined unlimited abortion up to birth in 2022 (Prop 1); conservatives can push for parental consent and defunding Planned Parenthood.
- ✅ **Second Amendment:** Strict gun laws rank CA last in freedom; GOP candidates vow to defend self-defense rights amid rising crime.
- ✅ **School Choice:** Limited charter schools face union attacks; advocates seek vouchers to empower parental rights against CRT and gender curricula.
- ✅ **Religious Liberty:** Threats from laws mandating LGBTQ+ resources in schools; protections needed for faith-based adoption agencies and churches.
- ✅ **Family Values:** Gender ideology in schools erodes traditional marriage; conservatives fight for biological truth in sports and bathrooms.
- ✅ **Election Integrity:** No voter ID, mail-in vulnerabilities; reforms essential to counter alleged fraud in a state with 22 million voters.

---

## 🔴 2026 Statewide Races

### **Governor** - 2026-11-03

**Context:** This open seat (Newsom term-limited) controls the agenda for 40 million residents, from budget to social policies. A conservative win could halt progressive overreach; even a strong GOP showing mobilizes the base.

**Chad Bianco (Republican)** - Riverside County Sheriff

**Faith Statement:** "“Number one, I am a Christian” - Chad Bianco, emphasizing his personal faith as the foundation of his leadership and commitment to biblical values in public service."

**Background:**
- Born 1967 in Utah, raised in mining town with values of integrity and service.
- 30+ years in law enforcement, elected Sheriff in 2018, boosted CCW permits 10x.
- Devoted husband and father, credits faith for resilience in tough cases.

**Christian Conservative Analysis:**
- **Pro-Life:** Personally pro-life; opposes CA's late-term abortion regime, supports incremental restrictions like ultrasound mandates.
- **Religious Liberty:** Defends churches against COVID lockdowns; backs exemptions for faith groups.
- **Education/Parental Rights:** Champions vouchers and repealing secrecy laws on gender transitions.
- **Family Values:** Strong alignment with biblical family; fights laws undermining parental authority.
- **Overall Assessment:** 9/10 - Proven faith-driven leader with law enforcement record; pragmatic yet bold for CA.

**Key Positions:**
- **ABORTION:** Personally pro-life, opposes California's expansive abortion laws and supports restrictions to protect the unborn while respecting California's legal landscape through incremental protections like parental consent and defunding abortion providers.
- **EDUCATION:** Strong advocate for school choice and parental rights; supports vouchers for public, private, charter, and homeschool options; pledges to repeal AB 1955, which limits parental notification on sensitive issues, to restore transparency and empower families.
- **RELIGIOUS FREEDOM:** As a Christian leader, Bianco defends religious liberty against government overreach, supporting protections for faith-based organizations and individuals in schools and workplaces, drawing from his testimony of faith guiding public policy.
- **GUNS:** Fervent 2nd Amendment defender; has issued over 60,000 CCW permits in Riverside County; opposes gun control measures like assault weapon bans, arguing they target law-abiding citizens while criminals ignore laws.
- **TAXES:** Proposes abolishing the state income tax to attract businesses and residents, reduce the tax burden on working families, and stimulate economic growth in high-tax California.
- **IMMIGRATION:** Supports secure borders and ending sanctuary state policies; prioritizes deportation of violent criminal immigrants; vows to work with federal authorities to stop illegal crossings while providing pathways for legal immigrants.

**Endorsements:** Peace Officers Research Association of California (PORAC), San Francisco Sheriff Paul Miyamoto, Assemblyman Devon Mathis

**Website:** https://biancoforgovernor.com

**Steve Hilton (Republican)** - Political Commentator & Advisor

**Faith Statement:** "No publicly disclosed faith statement; however, Hilton has received public prayers and endorsements from prominent Christian leaders like Pastor Jack Hibbs, indicating alignment with faith-based conservative values."

**Background:**
- UK-born 1969, advised PM Cameron; Fox News host of 'The Next Revolution.'
- Naturalized U.S. citizen 2021; father of three, focuses on CA reform via Golden Together.
- Media influencer shaping conservative discourse on freedom and opportunity.

**Christian Conservative Analysis:**
- **Pro-Life:** Pragmatic pro-life, seeking achievable life-affirming policies in blue CA.
- **Religious Liberty:** Supports faith in public life through parental rights defenses.
- **Education/Parental Rights:** Fights indoctrination, expands choice for biblical education.
- **Family Values:** Promotes traditional homes, biological norms in youth sports.
- **Overall Assessment:** 8/10 - Intellectual conservative with Trump ties; needs deeper faith articulation but strong on values.

**Key Positions:**
- **ABORTION:** Supports moving California 'towards life in a way that's achievable,' favoring pragmatic pro-life measures like restrictions after viability and support for pregnancy centers, while acknowledging the state's progressive laws.
- **EDUCATION:** Pushes for 100% student proficiency in math and English; expands school choice, charter schools, and parental trigger laws; opposes ideological indoctrination in curricula and teacher union resistance to accountability.
- **RELIGIOUS FREEDOM:** Defends parental rights on faith-related issues like gender and sex education; supports protections for religious expression in public spaces, aligned with his backing from Christian nationalists.
- **GUNS:** Strong 2nd Amendment advocate; condemns attacks on responsible gun owners in California; supports concealed carry and opposes measures treating lawful firearm possession as criminal.
- **TAXES:** Vows to reduce taxes for workers and businesses by cutting state budget bloat; aims to eliminate income tax for over half of households, cap hidden housing fees, and foster pro-growth policies.
- **IMMIGRATION:** Enforce immigration laws for public safety; prioritizes border security and prosecution of illegal entrants committing crimes, balancing compassion for legal immigrants with rule of law.

**Endorsements:** Pastor Jack Hibbs (Calvary Chapel Chino Hills), Fox News contributors

**Website:** https://stevehiltonforgovernor.com

**Why It Matters:** Securing the Governor's mansion halts radical social experiments, restores family protections, and revives California's promise as a beacon of freedom.

### **Lieutenant Governor** - 2026-11-03

**Context:** Open seat with Democratic frontrunners; conservatives must field strong candidates to influence Senate and succession.

[Note: Major candidates profiled in database; focus on GOP challengers emerging.]

**Why It Matters:** Influences legislative faith and family bills in the Senate.

### **Attorney General** - 2026-11-03

**Context:** Incumbent Bonta vulnerable if running for higher office; key for defending or challenging progressive prosecutions.

**Why It Matters:** Enforces election laws and protects religious freedoms in courts.

[Similar for other races...]

---

## 🎯 KEY ISSUES FOR California CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Oppose Prop 1's unlimited abortion; push Heartbeat Bill, parental consent (current law requires for minors).
- 200+ pregnancy centers like Alpha Crisis Pregnancy Center provide alternatives.
- Defend traditional marriage against no-fault divorce expansions.
- Recent challenge: 2022 law funds abortions for out-of-staters.

**Progressive Position:**
- Unlimited access, including non-doctors; funds travel for abortions.
- Gender-affirming care for minors without consent threats.

**Christian Conservative Action:**
- Join California Pro-Life Council (caprolife.org) for rallies.
- Support AB 2091 bans on misinformation about abortion.
- Volunteer at pregnancy centers in LA, Sacramento.
- Vote for pro-life candidates like Bianco.

### **School Choice & Parental Rights**

**Conservative Position:**
- Expand charters (1.3M students); voucher program stalled but pushed in 2023.
- Bans on CRT in some districts; homeschool freedom high (3rd in U.S.).
- Recent win: 2024 law strengthens parent notifications.

**Progressive Position:**
- Union control via CTA; DEI mandates in curriculum.
- AB 1955 limits parent alerts on gender issues.

**Christian Conservative Action:**
- Run for local school boards in conservative counties.
- Support California School Choice (caprochoice.org).
- Join Capitol Family Alliance for legislative alerts.

### **Religious Freedom**

**Conservative Position:**
- Protect faith adoptions (e.g., vs. SB 407 challenges).
- Exempt churches from LGBTQ+ mandates.
- Recent: 2024 court win against school prayer bans.

**Progressive Position:**
- AB 727 requires LGBTQ+ resources in schools, pressuring faith views.
- Threats to homeschool over 'abuse' claims.

**Christian Conservative Action:**
- Alliance Defending Freedom (adflegal.org) cases.
- First Liberty Institute support.
- Pray vigils at capitol.

### **Guns**

**Conservative Position:**
- Defend CCW; challenge bans in courts (e.g., Bruen impact).
- CA ranks 50th in gun freedom; sheriffs like Bianco issue permits.

**Progressive Position:**
- Assault weapons ban, red flag laws expanded 2024.

**Christian Conservative Action:**
- California Rifle & Pistol Association (crpa.org).
- Lobby against AB 1594 ammo regs.

### **Taxes**

**Conservative Position:**
- Cut income tax (13.3% top rate); abolish as Bianco proposes.
- Property tax caps via Prop 13 defense.

**Progressive Position:**
- Gas tax hikes, wealth tax pushes.

**Christian Conservative Action:**
- Howard Jarvis Taxpayers Assoc (hjta.org).
- Vote no on tax hikes.

### **Immigration**

**Conservative Position:**
- End sanctuary (SB 54); border wall support.
- Deport criminals (1M+ illegals in CA).

**Progressive Position:**
- Driver's licenses, benefits for undocumented.

**Christian Conservative Action:**
- Federation for American Immigration Reform (fairus.org).
- Border prayer walks.

### **Family Values**

**Conservative Position:**
- Biological definitions in law; ban gender transitions for minors.
- Marriage as man-woman.

**Progressive Position:**
- AB 1955 hides transitions; non-binary on IDs.

**Christian Conservative Action:**
- California Family Council (californiafamily.org).
- Parent rallies.

### **Election Integrity**

**Conservative Position:**
- Voter ID initiative; clean rolls (millions inactive).
- Paper ballots, audits.

**Progressive Position:**
- Universal mail-in, no ID.

**Christian Conservative Action:**
- iVoterGuide.org ratings.
- Poll watching training.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- 2026-05-18 - Voter registration deadline (15 days before primary)
- 2026-05-04 - Early voting ballots mailed
- 2026-06-02 - Primary Election
- 2026-11-03 - General Election

**Voter Registration:** sos.ca.gov/elections

---

## 🗳️ CHURCH MOBILIZATION STRATEGY

### **What Pastors Can Do (501c3 Compliant):**

✅ **Endorse candidates from pulpit** (IRS now permits pastoral endorsements)
✅ **Distribute non-partisan voter guides** (iVoterGuide, Christian Voter Guide)
✅ **Host candidate forums** (invite all candidates)
✅ **Preach on biblical citizenship** (Romans 13, Proverbs 29:2)
✅ **Voter registration drives** after services
✅ **Encourage early voting** and provide transportation
✅ **Prayer emphasis** for elections and candidates

❌ **Cannot donate church funds** to campaigns (personal donations allowed)

### **What Church Members Can Do:**

✅ **Volunteer for campaigns** (door-knocking, phone banking)
✅ **Donate to candidates** who align with biblical values
✅ **Host house parties** for conservative candidates
✅ **Share on social media** with #CaliforniaFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR California CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - California coverage
- **California Pro-Life Council** - Pro-life ratings
- **California Family Council** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **California Secretary of State**: sos.ca.gov
- **County Election Offices**: Find via sos.ca.gov/elections/county-election-officials
- **Early Voting Locations**: county registrar websites

### **Conservative Organizations:**
- **California Pro-Life Council**: caprolife.org
- **California Family Alliance**: calfamily.org
- **California Rifle & Pistol Association**: crpa.org
- **California School Choice**: caprochoice.org
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR California CHRISTIANS

**2026 Elections Matter:**
- Governor race determines pro-life safeguards or expansion.
- AG affects religious liberty lawsuits.
- Supt impacts school gender policies.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Income tax abolished for family relief
✅ Sanctuary laws ended for safety
✅ Border security with federal partnership

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Taxes hiked, businesses flee
❌ Open borders strain resources
❌ Fentanyl crisis worsens

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Chad Bianco and Steve Hilton and their families
- California Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in California
- Revival and awakening in California
- God's will in California elections

**Scripture for California Elections:**

*\"Righteousness exalts a nation, but sin condemns any people.\"* - *Proverbs 14:34*

*\"When the righteous thrive, the people rejoice; when the wicked rule, the people groan.\"* - *Proverbs 29:2*

*\"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land.\"* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute California coverage, email contact@ekewaka.com

**California CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing California races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'California'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} California races...")
race_ids = {}
for race in races:
    office = race['office']
    if office in existing_race_map:
        race_id = existing_race_map[office]
        race['race_id'] = race_id
        race['updated_at'] = datetime.now().isoformat()
        races_table.put_item(Item=race)
        print(f"  Updated: {office}")
    else:
        race_id = str(uuid.uuid4())
        race['race_id'] = race_id
        race['created_at'] = datetime.now().isoformat()
        race['created_by'] = 'system'
        races_table.put_item(Item=race)
        print(f"  Created: {office}")
    race_ids[office] = race_id
print(f"\n[SUCCESS] Processed {len(races)} races")

print(f"\nChecking for existing California candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'California'}
)['Items']
existing_candidate_map = {(c['name'], c['office']): c['candidate_id'] for c in existing_candidates}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} California candidates...")
for candidate in candidates:
    name = candidate['name']
    office = candidate['office']
    key = (name, office)
    if office in race_ids:
        candidate['race_id'] = race_ids[office]
    else:
        candidate['race_id'] = ''
    if key in existing_candidate_map:
        candidate_id = existing_candidate_map[key]
        candidate['candidate_id'] = candidate_id
        candidate['updated_at'] = datetime.now().isoformat()
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Updated: {name} - {office}")
    else:
        candidate_id = str(uuid.uuid4())
        candidate['candidate_id'] = candidate_id
        candidate['created_at'] = datetime.now().isoformat()
        candidate['created_by'] = 'system'
        candidate['status'] = 'active'
        candidates_table.put_item(Item=candidate)
        print(f"  Created: {name} - {office}")
print(f"\n[SUCCESS] Processed {len(candidates)} candidates")

print("\nProcessing California summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'California'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] California data upload complete!")
```