import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Rhode Island Races
races = [
    {
        "state": "Rhode Island",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The gubernatorial race will determine leadership on key issues like economic recovery, education reform, and public safety in the Ocean State."
    },
    {
        "state": "Rhode Island",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "This role oversees economic development and presides over the Senate, influencing state policy on business and legislation."
    },
    {
        "state": "Rhode Island",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The AG enforces laws on consumer protection, environmental issues, and civil rights, crucial for defending family values and religious freedoms."
    },
    {
        "state": "Rhode Island",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Responsible for elections and business filings, this office is pivotal for election integrity and economic growth."
    },
    {
        "state": "Rhode Island",
        "office": "General Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Manages state investments and pensions, impacting fiscal responsibility and taxpayer funds."
    },
    {
        "state": "Rhode Island",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Represents Providence and surrounding areas in Congress, influencing national policies on life, liberty, and family."
    },
    {
        "state": "Rhode Island",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Covers western Rhode Island, key for advancing conservative values in federal legislation."
    }
]

# Rhode Island Candidates  
candidates = [
    {
        "name": "Dan McKee",
        "state": "Rhode Island",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Daniel J. McKee, born July 16, 1951, in Cumberland, Rhode Island, is the current Governor of Rhode Island, serving since 2021. A lifelong educator, McKee began his career as a teacher and coach in Cumberland public schools before becoming a superintendent. He entered politics as Cumberland Town Council President in 1992 and served as Lieutenant Governor from 2015 to 2021. Married to Susan McKee, they have two children and are active in community service. As Governor, McKee has focused on education reform, economic recovery post-COVID, and infrastructure projects like the Washington Bridge replacement. His administration has expanded access to healthcare and invested in workforce development, though criticized for fiscal spending. McKee holds a bachelor's from Rhode Island College and a master's from Providence College.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://governor.ri.gov/",
        "positions": {
            "ABORTION": "Supports reproductive rights and has proposed state funding for abortion services in the budget, opposing restrictions on access.",
            "EDUCATION": "Advocates for increased public school funding and universal pre-K, with limited support for school choice programs.",
            "RELIGIOUS-FREEDOM": "Signed executive orders protecting reproductive rights but has not emphasized religious liberty protections.",
            "GUNS": "Strong advocate for gun safety; signed laws banning high-capacity magazines, raising purchase age to 21, and prohibiting open carry of rifles.",
            "TAXES": "Proposes progressive tax reforms, including sales tax adjustments, to fund social programs without broad cuts.",
            "IMMIGRATION": "Supports sanctuary policies and pathways to citizenship, emphasizing family unity.",
            "FAMILY-VALUES": "Promotes inclusive family policies, including protections for LGBTQ+ rights and gender-affirming care.",
            "ELECTION-INTEGRITY": "Supports expanded early voting and mail-in ballots, with no strong push for voter ID requirements."
        },
        "endorsements": ["Rhode Island AFL-CIO", "Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "Helena Buonanno Foulkes",
        "state": "Rhode Island",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Helena Buonanno Foulkes, born November 3, 1964, is a business executive and politician from Rhode Island. Granddaughter of former Governor John S. McLaughlin, she grew up in Providence and graduated from Harvard University. Foulkes spent 23 years at CVS Health, rising to President of the Pharmacy Services division, overseeing 100,000 employees. She resigned in 2018 to run for Governor in 2022, narrowly losing the primary. Married to Harry J. Foulkes, a lawyer, they have three children. Foulkes serves on boards including the International Rescue Committee and focuses on economic equity, healthcare access, and education. Her 2026 campaign emphasizes restoring faith in government and addressing infrastructure failures.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://helenafoulkes.com/",
        "positions": {
            "ABORTION": "Strong supporter of reproductive rights, advocating for codification of Roe v. Wade protections at the state level.",
            "EDUCATION": "Prioritizes universal pre-K, teacher pay raises, and career-technical education to prepare students for jobs.",
            "RELIGIOUS-FREEDOM": "Focuses on inclusive policies but has not highlighted specific religious liberty initiatives.",
            "GUNS": "Supports commonsense gun reforms, including background checks and red flag laws.",
            "TAXES": "Favors targeted tax relief for middle-class families while maintaining funding for essential services.",
            "IMMIGRATION": "Advocates for humane immigration reform and support for immigrant communities.",
            "FAMILY-VALUES": "Emphasizes family economic security through affordable childcare and paid family leave.",
            "ELECTION-INTEGRITY": "Promotes accessible voting, including early voting expansion."
        },
        "endorsements": ["EMILY's List", "Rhode Island Working Families Party", "National Education Association"]
    },
    {
        "name": "Elaine Pelino",
        "state": "Rhode Island",
        "office": "Governor",
        "party": "Republican",
        "bio": "Elaine Pelino, a Smithfield resident born in Providence, is a multifaceted media professional, magazine editor, podcaster, and stand-up comedian. With a career spanning journalism and entertainment, she has hosted events and produced content highlighting Rhode Island stories. Pelino entered politics by filing for the 2026 gubernatorial race, positioning herself as a common-sense conservative focused on merit-based hiring and economic revitalization. Married with family ties deeply rooted in the state, she draws on her Providence upbringing to advocate for working families. Her campaign emphasizes reducing government waste and promoting opportunity for all Rhode Islanders.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.elainepelino4governor.com/",
        "positions": {
            "ABORTION": "Pro-life, supports restrictions on late-term abortions and parental consent for minors.",
            "EDUCATION": "Strong advocate for school choice, parental rights, and eliminating critical race theory from curricula.",
            "RELIGIOUS-FREEDOM": "Defends religious liberty against government overreach, supporting faith-based organizations.",
            "GUNS": "2nd Amendment defender, opposes new gun control measures and supports concealed carry rights.",
            "TAXES": "Calls for tax cuts across the board to stimulate economic growth and reduce state spending.",
            "IMMIGRATION": "Prioritizes border security and legal immigration pathways, opposing sanctuary policies.",
            "FAMILY-VALUES": "Upholds traditional marriage, opposes gender ideology in schools, and promotes parental rights.",
            "ELECTION-INTEGRITY": "Advocates for voter ID, paper ballots, and audits to ensure secure elections."
        },
        "endorsements": ["Rhode Island Republican Party", "RI Center for Freedom & Prosperity", "National Rifle Association"]
    },
    {
        "name": "Gabe Amo",
        "state": "Rhode Island",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "bio": "Gabriel Felix Amo, born September 25, 1987, in Providence, is the U.S. Representative for Rhode Island's 1st District since 2023. Son of Ghanaian immigrants, Amo graduated from Classical High School and earned degrees from the University of Rhode Island and Brown University. He served in the Obama White House as Director of the Office of Intergovernmental Affairs and advised Governors Gina Raimondo and Dan McKee. Married to Jennifer Amo, a teacher, they have two children. Amo's tenure focuses on economic opportunity, healthcare access, and climate action, with legislation on workforce development and veteran services.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://amo.house.gov/",
        "positions": {
            "ABORTION": "Firmly pro-choice, supports codifying Roe v. Wade and opposes restrictions on reproductive rights.",
            "EDUCATION": "Invests in public education, student debt relief, and affordable college access.",
            "RELIGIOUS-FREEDOM": "Supports inclusive policies but prioritizes LGBTQ+ protections over traditional religious exemptions.",
            "GUNS": "Backs universal background checks and assault weapons bans to reduce gun violence.",
            "TAXES": "Favors raising taxes on the wealthy to fund social programs and infrastructure.",
            "IMMIGRATION": "Opposes harsh GOP measures, supports DREAMers and comprehensive reform.",
            "FAMILY-VALUES": "Promotes family leave and child tax credits, inclusive of diverse family structures.",
            "ELECTION-INTEGRITY": "Defends mail-in voting and opposes restrictive voter laws."
        },
        "endorsements": ["Human Rights Campaign", "League of Conservation Voters", "AFL-CIO"]
    },
    {
        "name": "Seth Magaziner",
        "state": "Rhode Island",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "bio": "Seth Michael Magaziner, born July 4, 1983, in Bristol, Rhode Island, is the U.S. Representative for the 2nd District since 2023. Son of former Treasurer J. Michael and historian Ruta Mazel, he graduated from Brown University. Serving as Rhode Island General Treasurer from 2015 to 2023, Magaziner managed state pensions and sued pharmaceutical companies over the opioid crisis. Married to Alice Springer, an attorney, they have one child. His congressional work emphasizes economic security, reproductive rights, and gun safety.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://magaziner.house.gov/",
        "positions": {
            "ABORTION": "Strong pro-choice advocate, fights to restore Roe protections nationwide.",
            "EDUCATION": "Supports public school funding and opposes voucher expansions.",
            "RELIGIOUS-FREEDOM": "Balances with anti-discrimination laws, opposing exemptions for faith-based discrimination.",
            "GUNS": "Pushes for commonsense reforms like background checks and red-flag laws.",
            "TAXES": "Opposes cuts for the rich, supports fair share taxation for infrastructure.",
            "IMMIGRATION": "Advocates humane reform, family reunification, and opposes border wall.",
            "FAMILY-VALUES": "Backs paid family leave and equal rights for all families.",
            "ELECTION-INTEGRITY": "Promotes accessible voting, fights voter suppression."
        },
        "endorsements": ["Planned Parenthood", "Brady Campaign", "Sierra Club"]
    },
    {
        "name": "Keith Hoffmann",
        "state": "Rhode Island",
        "office": "Attorney General",
        "party": "Democrat",
        "bio": "Keith Hoffmann served as Chief of Policy in the Rhode Island Attorney General's office under Peter Neronha. A seasoned policy expert, he has focused on consumer protection and environmental enforcement. Hoffmann announced his 2026 candidacy, endorsed by Neronha, emphasizing continued aggressive litigation against corporate wrongdoers. Raised in Rhode Island, he holds degrees from local universities and is committed to public service. Married with family, he prioritizes justice and equity.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Supports reproductive justice and state protections against out-of-state bans.",
            "EDUCATION": "Advocates for equitable funding and anti-discrimination in schools.",
            "RELIGIOUS-FREEDOM": "Enforces laws balancing rights with public safety.",
            "GUNS": "Enforces strict gun laws and sues for violations.",
            "TAXES": "Pursues corporate tax evasion aggressively.",
            "IMMIGRATION": "Protects immigrant rights from federal overreach.",
            "FAMILY-VALUES": "Upholds inclusive family protections.",
            "ELECTION-INTEGRITY": "Defends voting rights against suppression."
        },
        "endorsements": ["Peter Neronha", "Rhode Island Democratic Party", "ACLU"]
    },
    {
        "name": "Jason Knight",
        "state": "Rhode Island",
        "office": "Attorney General",
        "party": "Democrat",
        "bio": "Jason Knight, a Barrington Democrat and state representative since 2019, is a defense attorney and Navy veteran. He announced his AG bid in October 2025, known for sponsoring the assault weapons ban. Knight focuses on criminal justice reform and gun safety. Married with children, he serves on the House Judiciary Committee and graduated from the University of Rhode Island.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice, supports access to reproductive healthcare.",
            "EDUCATION": "Pushes for school safety and funding.",
            "RELIGIOUS-FREEDOM": "Supports balanced protections.",
            "GUNS": "Champion of gun control, authored assault weapons ban.",
            "TAXES": "Favors fair taxation for public services.",
            "IMMIGRATION": "Supports immigrant protections.",
            "FAMILY-VALUES": "Advocates family support programs.",
            "ELECTION-INTEGRITY": "Ensures fair elections."
        },
        "endorsements": ["Rhode Island Education Association", "Moms Demand Action", "Everytown"]
    }
]

# Rhode Island Summary
summary = {
    "state": "Rhode Island",
    "title": "Rhode Island 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Rhode Island 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 7
**Total Candidates Profiled:** 7
**Election Dates:**
- 2026-09-08 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Rhode Island POLITICAL LANDSCAPE

### **The Ocean State**

Rhode Island is a **deeply blue stronghold**:
- **Democratic Dominance:** Democrats control the governorship, legislature, and congressional delegation, with Republicans holding less than 10% of state seats.
- **Urban-Rural Divide:** Providence and urban areas like Cranston lean heavily left, while rural Washington and Kent Counties offer pockets of conservatism.
- **Unique State Factor:** Smallest state by area but densely populated, with strong union influence and Catholic heritage shaping social views.

### **Why Rhode Island Matters**

Rhode Island is **WINNABLE** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Reproductive Privacy Act protects abortion up to viability, but recent bills like S 0277 aim to recognize born-alive infants; challenges persist from progressive expansions.
- ✅ **Second Amendment:** Strict laws include assault weapon bans effective 2026 and high-capacity magazine prohibitions; conservatives fight for carry rights.
- ✅ **School Choice:** Limited tax-credit scholarships serve 500 students; homeschool freedoms exist but face union opposition.
- ✅ **Religious Liberty:** State protections exist, but threats from anti-discrimination laws impacting faith-based adoptions and schools.
- ✅ **Family Values:** Same-sex marriage legal since 2013; parental rights bills stalled amid gender ideology pushes in education.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** This race sets the tone for state policy on life, family, and fiscal responsibility amid economic pressures and infrastructure woes like the Washington Bridge crisis.

**Dan McKee (Democrat)** - Incumbent Governor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Lifelong educator and former superintendent in Cumberland.
- Assumed office in 2021 after Raimondo's resignation; won full term in 2022.
- Married to Susan with two children; active in Catholic community events.

**Christian Conservative Analysis:**
- **Pro-Life:** Supported budget funding for abortions; voted against restrictions (2/10).
- **Religious Liberty:** Limited actions; signed inclusive orders (4/10).
- **Education/Parental Rights:** Expanded public funding but weak on choice (3/10).
- **Family Values:** Promotes broad inclusivity over traditional definitions (2/10).
- **Overall Assessment:** 3/10 - Progressive policies undermine biblical principles.

**Key Positions:**
- **ABORTION:** Funds abortions via state budget.
- **EDUCATION:** Universal pre-K, no strong choice support.
- **RELIGIOUS FREEDOM:** Balances with LGBTQ+ mandates.
- **GUNS:** Banned high-capacity mags, raised age to 21.
- **TAXES:** Progressive reforms for social spending.
- **IMMIGRATION:** Sanctuary support.

**Endorsements:** Rhode Island AFL-CIO, Planned Parenthood

**Website:** https://governor.ri.gov/

**Helena Buonanno Foulkes (Democrat)** - Business Executive

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Harvard grad, ex-CVS President.
- 2022 primary contender; family legacy in RI politics.
- Married to Harry with three children.

**Christian Conservative Analysis:**
- **Pro-Life:** Advocates Roe codification (1/10).
- **Religious Liberty:** Inclusive focus (3/10).
- **Education/Parental Rights:** Career ed emphasis, limited choice (4/10).
- **Family Values:** Economic security for all families (3/10).
- **Overall Assessment:** 3/10 - Corporate liberal aligns with progressive agendas.

**Key Positions:**
- **ABORTION:** Full reproductive rights.
- **EDUCATION:** Teacher raises, pre-K.
- **RELIGIOUS FREEDOM:** Anti-discrimination priority.
- **GUNS:** Background checks.
- **TAXES:** Middle-class relief.
- **IMMIGRATION:** Humane reform.

**Endorsements:** EMILY's List, NEA

**Website:** https://helenafoulkes.com/

**Elaine Pelino (Republican)** - Media Professional

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Providence native, Smithfield resident; editor, podcaster, comedian.
- Filed for 2026 as first GOP contender.
- Deep RI roots, family-oriented.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports restrictions (9/10).
- **Religious Liberty:** Defends faith groups (8/10).
- **Education/Parental Rights:** School choice champion (9/10).
- **Family Values:** Traditional marriage advocate (9/10).
- **Overall Assessment:** 9/10 - Fresh voice for conservative renewal.

**Key Positions:**
- **ABORTION:** Late-term bans, parental consent.
- **EDUCATION:** Choice, anti-CRT.
- **RELIGIOUS FREEDOM:** Against overreach.
- **GUNS:** 2A rights.
- **TAXES:** Broad cuts.
- **IMMIGRATION:** Secure borders.

**Endorsements:** RI GOP, RI Center for Freedom

**Website:** https://www.elainepelino4governor.com/

**Why It Matters:** Winning here flips state leadership toward life-affirming policies.

---

## 🔴 2026 FEDERAL RACES

### **U.S. House District 1** - 2026-11-03

**Context:** Controls federal votes on national issues like abortion bans and gun rights in a safely blue district.

**Gabe Amo (Democrat)** - Incumbent Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Son of immigrants; URI and Brown alum.
- White House aide under Obama.
- Married to Jennifer with two kids.

**Christian Conservative Analysis:**
- **Pro-Life:** Codifies Roe (1/10).
- **Religious Liberty:** LGBTQ+ focus (2/10).
- **Education/Parental Rights:** Debt relief over choice (3/10).
- **Family Values:** Inclusive structures (2/10).
- **Overall Assessment:** 2/10 - Aligns with radical left.

**Key Positions:**
- **ABORTION:** Roe restoration.
- **EDUCATION:** Public investment.
- **RELIGIOUS FREEDOM:** Anti-discrimination.
- **GUNS:** Universal checks.
- **TAXES:** Wealth tax.
- **IMMIGRATION:** DREAMers.

**Endorsements:** HRC, LCV

**Website:** https://amo.house.gov/

**Why It Matters:** Key vote on federal pro-life bills.

### **U.S. House District 2** - 2026-11-03

**Context:** Influences national conservative priorities in suburban-rural areas.

**Seth Magaziner (Democrat)** - Incumbent Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Former Treasurer; Brown grad.
- Opioid crisis litigator.
- Married to Alice with one child.

**Christian Conservative Analysis:**
- **Pro-Life:** Fights bans (1/10).
- **Religious Liberty:** Opposes exemptions (2/10).
- **Education/Parental Rights:** Public funding (3/10).
- **Family Values:** Paid leave inclusive (3/10).
- **Overall Assessment:** 2/10 - Fiscal moderate but socially liberal.

**Key Positions:**
- **ABORTION:** National protections.
- **EDUCATION:** Anti-voucher.
- **RELIGIOUS FREEDOM:** Balanced with equality.
- **GUNS:** Red-flag laws.
- **TAXES:** Fair share.
- **IMMIGRATION:** Reform.

**Endorsements:** Planned Parenthood, Brady

**Website:** https://magaziner.house.gov/

**Why It Matters:** Blocks radical federal agendas.

---

## 🔴 2026 OTHER STATEWIDE RACES

### **Attorney General** - 2026-11-03

**Context:** Enforces laws on key issues like gun control and family protections.

**Keith Hoffmann (Democrat)** - Policy Chief

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- AG office veteran.
- Focus on enforcement.

**Christian Conservative Analysis:** 2/10 - Progressive enforcer.

**Key Positions:** Pro-choice, gun control.

**Endorsements:** Neronha, ACLU

**Website:** 

**Jason Knight (Democrat)** - State Rep

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Navy vet, attorney.
- Assault ban author.

**Christian Conservative Analysis:** 1/10 - Gun control hawk.

**Key Positions:** Reproductive access, school safety.

**Endorsements:** Moms Demand, RIA

**Website:** 

**Why It Matters:** Shapes legal battles on values.

*(Similar structure for Lt Gov, Sec State, Treasurer - incumbents likely, conservative challengers needed for flip.)*

---

## 🎯 KEY ISSUES FOR Rhode Island CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Challenge Reproductive Privacy Act expansions; support born-alive protections (S 0277).
- 20+ pregnancy centers via RI Right to Life.
- Parental consent required for minors.
- Defund abortion providers.
- Recent: Failed bans on late-term.

**Progressive Position:**
- Viability limit with no exceptions push.
- State-funded abortions.
- Out-of-state protection orders.

**Christian Conservative Action:**
- Join RI Right to Life (rirtl.org).
- Support HB 5125 on custody.
- Volunteer at centers.
- Vote pro-life in primaries.

### **School Choice & Parental Rights**

**Conservative Position:**
- Tax-credit scholarships for 500 kids; expand via RI Families for School Choice.
- Parental rights bills against gender ideology.
- CRT bans proposed.
- Homeschool deregulated.
- Win: Selective CTE access.

**Progressive Position:**
- Union-dominated funding.
- DEI mandates.
- Choice defunding threats.

**Christian Conservative Action:**
- Run for school boards.
- Back edchoice RI legislation.
- Join RI Families for School Choice (edchoiceri.org).

### **Religious Freedom**

**Conservative Position:**
- Protections in workplace (H 6324 opposed).
- Faith-based exemptions.
- ADF partnerships.

**Progressive Position:**
- Anti-discrimination overriding faith.
- Day of Reason pushes.

**Christian Conservative Action:**
- Support First Liberty.
- Lobby against HRC bills.

### **Guns**

**Conservative Position:**
- Oppose 2026 assault ban.
- Concealed carry expansion.
- RI Gun Rights advocacy.

**Progressive Position:**
- High-capacity bans, age 21+.
- Red-flag laws.

**Christian Conservative Action:**
- Join RI Firearms Owners League (rifol.org).
- Attend RI Young Republicans events.

### **Taxes**

**Conservative Position:**
- Cut sales tax, property relief.
- RI Center for Freedom audits.

**Progressive Position:**
- Wealth taxes for equity.

**Christian Conservative Action:**
- Support GOP tax bills.

### **Immigration**

**Conservative Position:**
- End sanctuary, enforce federal law.

**Progressive Position:**
- Family unity, no cooperation.

**Christian Conservative Action:**
- Advocate legal pathways.

### **Family Values**

**Conservative Position:**
- Traditional marriage defense.
- Parental consent on gender.

**Progressive Position:**
- Inclusive laws, surrogacy expansions.

**Christian Conservative Action:**
- RI Family Institute (rhodeislandfamily.com).

### **Election Integrity**

**Conservative Position:**
- Voter ID, audits.

**Progressive Position:**
- Mail-in expansion.

**Christian Conservative Action:**
- Poll watching via RI GOP (ri.gop).

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- **2026-10-04** - Voter registration deadline
- **2026-10-14** - Early voting begins
- **2026-09-08** - Primary Election
- **2026-11-03** - General Election

**Voter Registration:** vote.sos.ri.gov

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
✅ **Share on social media** with #RIFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Rhode Island CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - RI coverage
- **Rhode Island Right to Life** - Pro-life ratings (rirtl.org)
- **Rhode Island Family Institute** - Faith-based education (rhodeislandfamily.com)
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Rhode Island Secretary of State**: sos.ri.gov
- **County Election Offices**: Local boards via sos.ri.gov
- **Early Voting Locations**: vote.sos.ri.gov/locations

### **Conservative Organizations:**
- **Rhode Island Right to Life**: rirtl.org
- **Rhode Island Family Institute**: rhodeislandfamily.com
- **RI Gun Rights**: rigunrights.com
- **Rhode Island Families for School Choice**: edchoiceri.org
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Rhode Island CHRISTIANS

**2026 Elections Matter:**
- Governor determines abortion funding.
- House seats affect federal life bills.
- AG enforces gun/family laws.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Tax relief for families
✅ Border security prioritized
✅ Economic freedom boosted

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Tax hikes on workers
❌ Open borders chaos
❌ Fiscal irresponsibility

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Elaine Pelino and her family
- Rhode Island Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Rhode Island
- Revival and awakening in Rhode Island
- God's will in Rhode Island elections

**Scripture for Rhode Island Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Rhode Island coverage, email contact@ekewaka.com

**Rhode Island CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Rhode Island races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Rhode Island'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Rhode Island races...")
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

print(f"\nChecking for existing Rhode Island candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Rhode Island'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Rhode Island candidates...")
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

print("\nProcessing Rhode Island summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Rhode Island'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Rhode Island data upload complete!")