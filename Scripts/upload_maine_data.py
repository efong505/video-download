import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Maine Races
races = [
    {
        "state": "Maine",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Republican Senator Susan Collins seeks re-election in a highly competitive race against strong Democratic challengers in a blue-leaning state."
    },
    {
        "state": "Maine",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open race due to term limits on incumbent Janet Mills, who is running for U.S. Senate; a battleground for conservative values in state leadership."
    },
    {
        "state": "Maine",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Democratic incumbent Chellie Pingree faces Republican challengers in the urban southern district."
    },
    {
        "state": "Maine",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Democratic incumbent Jared Golden defends against former Republican Governor Paul LePage in the rural northern district."
    }
]

# Maine Candidates  
candidates = [
    {
        "name": "Susan Collins",
        "state": "Maine",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Susan Margaret Collins, born December 7, 1952, in Caribou, Maine, is a lifelong public servant and the senior U.S. Senator from Maine. Raised in a political family—her father was a state representative—she graduated from St. Lawrence University in 1975 with a degree in government. Collins began her career as a staff assistant to Senator William Cohen, rising through roles in the Department of Labor and as New England regional director for President George H.W. Bush. Elected to the Senate in 1996, she has served five terms, chairing the Senate Aging Committee and serving on Intelligence and Homeland Security. Known for bipartisanship, she has championed veterans' affairs, mental health, and rural broadband. Married to Thomas Daffron since 2012, she has no children but is an avid reader and dog lover. Her accomplishments include the Opioid Crisis Response Act and confirming Ketanji Brown Jackson to the Supreme Court.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.collins.senate.gov",
        "positions": {
            "ABORTION": "Supports Roe v. Wade protections; voted against late-term abortion bans but for defunding Planned Parenthood; moderate pro-choice stance emphasizing exceptions.",
            "EDUCATION": "Supports school choice and charter schools; advocates for increased funding for rural education and vocational training.",
            "RELIGIOUS-FREEDOM": "Strong supporter of religious liberty; co-sponsored First Amendment Defense Act and opposed mandates infringing on faith-based organizations.",
            "GUNS": "Supports universal background checks and red flag laws; opposed assault weapons ban; earned NRA endorsement for defending 2nd Amendment rights.",
            "TAXES": "Advocates for tax cuts for middle class; supported 2017 Tax Cuts and Jobs Act; pushes for estate tax repeal.",
            "IMMIGRATION": "Supports border security funding and DREAM Act; favors comprehensive reform with pathway to citizenship for DACA recipients.",
            "FAMILY-VALUES": "Supports traditional marriage but voted for same-sex marriage repeal repeal; emphasizes parental rights in education.",
            "ELECTION-INTEGRITY": "Supports Voter ID laws and automatic voter registration; co-sponsored Election Security Act to prevent foreign interference."
        },
        "endorsements": ["National Rifle Association", "U.S. Chamber of Commerce", "Veterans of Foreign Wars"]
    },
    {
        "name": "Bill Clarke",
        "state": "Maine",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Bill Clarke is a Portland-based entrepreneur and founder of Geek Team, a tech support company. Born and raised in Maine, he has a background in IT and small business ownership. Previously ran for office with the U.S. Taxpayers' Party, Clarke announced his 2026 Senate bid on October 17, 2025, positioning himself as a conservative challenger to Susan Collins. A vocal critic of progressivism, he focuses on fiscal conservatism, anti-abortion advocacy, and traditional values. Married with family, Clarke is active in local community tech education programs. His accomplishments include growing Geek Team into a regional success and advocating for small business tax relief.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.billclarke.us",
        "positions": {
            "ABORTION": "Strongly pro-life; calls Planned Parenthood 'evil' and supports total ban on abortions with no exceptions.",
            "EDUCATION": "Advocates for school choice and vouchers; opposes critical race theory in schools.",
            "RELIGIOUS-FREEDOM": "Defends Christian values against government overreach; supports protections for faith-based adoption agencies.",
            "GUNS": "Absolute 2nd Amendment defender; opposes all gun control measures including red flag laws.",
            "TAXES": "Flat tax proponent; seeks elimination of income tax and property tax reform.",
            "IMMIGRATION": "Supports strict border wall and deportation of illegals; ends sanctuary policies.",
            "FAMILY-VALUES": "Opposes LGBTQ agenda; supports traditional marriage and parental rights against gender ideology.",
            "ELECTION-INTEGRITY": "Demands strict Voter ID and paper ballots; audits all elections for fraud."
        },
        "endorsements": ["Maine Republican Party Conservatives", "Pro-Life Alliance", "Gun Owners of America"]
    },
    {
        "name": "Janet Mills",
        "state": "Maine",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Janet T. Mills, born May 30, 1947, in Farmington, Maine, is a former Governor and current U.S. Senate candidate. Daughter of a federal judge, she graduated from University of Maine and University of Leeds Law School. Serving as District Attorney for Androscoggin County from 1980-2013, she prosecuted high-profile cases including the Oxford Hills child abuse scandal. Elected Attorney General in 2013, she defended environmental protections and opioid settlements. As Governor from 2019-2026, she navigated COVID-19, expanded healthcare, and signed abortion rights expansions. Unmarried, no children, she is known for her tough, independent style and love of hiking. Accomplishments include $800 million opioid settlement and climate action plans.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.janetmills.com",
        "positions": {
            "ABORTION": "Strong pro-choice; signed laws protecting late-term abortions and shielding providers from out-of-state bans.",
            "EDUCATION": "Supports public school funding; opposes vouchers; pushes for universal pre-K.",
            "RELIGIOUS-FREEDOM": "Supports separation of church and state; opposes faith-based exemptions for LGBTQ discrimination.",
            "GUNS": "Supports red flag laws and assault weapons bans; opposes concealed carry expansions.",
            "TAXES": "Raised taxes on wealthy; supports progressive taxation for social programs.",
            "IMMIGRATION": "Supports sanctuary state policies; pathway to citizenship and DACA protections.",
            "FAMILY-VALUES": "Supports same-sex marriage and gender-affirming care; emphasizes inclusive families.",
            "ELECTION-INTEGRITY": "Opposes Voter ID; supports mail-in voting and automatic registration."
        },
        "endorsements": ["Planned Parenthood", "EMILY's List", "AFL-CIO"]
    },
    {
        "name": "James Libby",
        "state": "Maine",
        "office": "Governor",
        "party": "Republican",
        "bio": "James D. Libby, born November 14, 1960, is a Maine State Senator from District 22 and 2026 gubernatorial candidate. A Naples native, he graduated from University of Maine with degrees in history and education. A former teacher, coach, and business owner, Libby served in the Maine House from 2014-2022 before the Senate. Married to Cindy with three children, he coaches youth sports and is active in community education. Known for fiscal conservatism, he has authored books on Maine history. Accomplishments include sponsoring tax relief bills and education reform legislation.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.jimlibbyforgovernor.com",
        "positions": {
            "ABORTION": "Pro-life; supports restrictions post-Roe and defunding Planned Parenthood.",
            "EDUCATION": "Strong school choice advocate; supports vouchers and charter expansion.",
            "RELIGIOUS-FREEDOM": "Protects faith-based organizations from anti-discrimination laws conflicting with beliefs.",
            "GUNS": "Defends 2nd Amendment; opposes red flag laws and magazine bans.",
            "TAXES": "Income tax elimination; property tax caps for seniors.",
            "IMMIGRATION": "Enforce federal laws; end sanctuary status.",
            "FAMILY-VALUES": "Traditional marriage; bans on gender transition for minors.",
            "ELECTION-INTEGRITY": "Mandatory Voter ID; same-day voting only."
        },
        "endorsements": ["Maine Republican Party", "National Federation of Independent Business", "Maine Heritage Policy Center"]
    },
    {
        "name": "Owen McCarthy",
        "state": "Maine",
        "office": "Governor",
        "party": "Republican",
        "bio": "Owen McCarthy is a Gorham businessman and co-founder of MedRhythms, a healthcare tech firm using music for stroke recovery. Born in Patten, he graduated from University of Maine with engineering degrees. An entrepreneur, he built MedRhythms into a national innovator. Married with family, McCarthy announced his 2026 bid on June 11, 2025, as a political outsider focusing on economic growth. Accomplishments include FDA approvals for MedRhythms tech and job creation in biotech.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://owenformaine.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions; supports parental consent for minors.",
            "EDUCATION": "Expands school choice; invests in STEM and vocational programs.",
            "RELIGIOUS-FREEDOM": "Safeguards faith in public life; opposes compelled speech laws.",
            "GUNS": "Strong 2nd Amendment supporter; background checks only.",
            "TAXES": "Reduce business taxes; eliminate sales tax on essentials.",
            "IMMIGRATION": "Secure borders; legal immigration reform.",
            "FAMILY-VALUES": "Promotes nuclear family policies; parental rights in curriculum.",
            "ELECTION-INTEGRITY": "Voter ID required; audit processes strengthened."
        },
        "endorsements": ["U.S. Chamber of Commerce", "Maine Biotech Association", "Gorham Business Leaders"]
    },
    {
        "name": "Shenna Bellows",
        "state": "Maine",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Shenna Bellows, born March 25, 1975, is Maine's Secretary of State and 2026 gubernatorial candidate. Raised in Manchester, she graduated from Bowdoin College and University of Maine Law School. A civil rights attorney, she served in the Maine Senate from 2010-2016, focusing on voting rights. Elected Secretary in 2021, she defended election integrity amid challenges. Married to Grady Chapman with two children, Bellows is a Unitarian Universalist active in community service. Accomplishments include expanding voter access and removing Trump from 2023 ballot.",
        "faith_statement": "As a Unitarian Universalist, I draw on principles of justice, equity, and compassion in public service.",
        "website": "https://www.shennabellows.com",
        "positions": {
            "ABORTION": "Pro-choice; protects reproductive rights including late-term access.",
            "EDUCATION": "Fully funds public schools; opposes privatization.",
            "RELIGIOUS-FREEDOM": "Ensures separation; protects minority faiths from majority imposition.",
            "GUNS": "Universal background checks; red flag implementation.",
            "TAXES": "Fair share tax on ultra-wealthy; closes loopholes.",
            "IMMIGRATION": "Welcoming policies; supports asylum seekers.",
            "FAMILY-VALUES": "Inclusive families; gender-affirming care protections.",
            "ELECTION-INTEGRITY": "Expands access; opposes suppression laws."
        },
        "endorsements": ["ACLU", "League of Women Voters", "Maine Education Association"]
    },
    {
        "name": "Ronald Russell",
        "state": "Maine",
        "office": "U.S. House District 1",
        "party": "Republican",
        "bio": "Ronald Russell, born in Fort Fairfield, Maine, is a retired U.S. Army Green Beret with 30 years of service, including combat in Iraq and Afghanistan. Raised on a potato farm, his mother was a teacher, father a farmer. After retiring, he founded Far Ridgeline Engagements, a defense contracting firm sold in 2022. Unsuccessful 2022 House bid; now state rep. Married with family, Russell is a veteran advocate. Accomplishments include Special Forces leadership and small business success.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://ronrussellforcongress.com",
        "positions": {
            "ABORTION": "Pro-life; supports heartbeat bill and adoption incentives.",
            "EDUCATION": "School choice priority; curriculum transparency for parents.",
            "RELIGIOUS-FREEDOM": "Protects military chaplains' rights; faith in public squares.",
            "GUNS": "Constitutional carry; opposes federal overreach.",
            "TAXES": "No new taxes; cut federal spending.",
            "IMMIGRATION": "Build the wall; end chain migration.",
            "FAMILY-VALUES": "Traditional values; oppose gender ideology in schools.",
            "ELECTION-INTEGRITY": "Voter ID mandatory; clean voter rolls."
        },
        "endorsements": ["Veterans for America First", "NRA", "Maine GOP Veterans Caucus"]
    },
    {
        "name": "Eric Small",
        "state": "Maine",
        "office": "U.S. House District 1",
        "party": "Republican",
        "bio": "Eric Small is Sanford's Police Chief since 2024, with 20+ years in law enforcement starting in Berwick PD. A lifelong Mainer, he rose to deputy chief before leading Sanford. Announced 2026 House bid July 28, 2025, focusing on crime and public safety. Married with children, Small coaches youth sports and volunteers in community policing. Accomplishments include reducing Sanford crime rates and implementing mental health response teams.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.ericsmallforcongress.com",
        "positions": {
            "ABORTION": "Pro-life advocate; supports state restrictions.",
            "EDUCATION": "Parental rights first; expand trade schools.",
            "RELIGIOUS-FREEDOM": "Defends law enforcement's faith expressions.",
            "GUNS": "Pro-2A; responsible ownership training.",
            "TAXES": "Lower taxes to boost local economies.",
            "IMMIGRATION": "Secure borders to protect communities.",
            "FAMILY-VALUES": "Strong families through safety policies.",
            "ELECTION-INTEGRITY": "Secure elections via ID and audits."
        },
        "endorsements": ["Fraternal Order of Police", "Maine Sheriffs' Association", "Local Business Owners"]
    },
    {
        "name": "Paul LePage",
        "state": "Maine",
        "office": "U.S. House District 2",
        "party": "Republican",
        "bio": "Paul LePage, born October 9, 1948, in Lewiston, Maine, is former two-term Governor (2011-2019) and 2026 House candidate. Orphaned young, he worked multiple jobs, earning a master's from University of Maine. Mayor of Waterville 2006-2011, then governor focusing on tax cuts and welfare reform. Moved to Florida post-term, returned for 2022 bid. Married to Ann with dual citizenship children. Accomplishments include surplus budgets and right-to-work law.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://paulepage.com",
        "positions": {
            "ABORTION": "Pro-life; supports 20-week ban and defunding Planned Parenthood.",
            "EDUCATION": "School choice and charter schools; oppose Common Core.",
            "RELIGIOUS-FREEDOM": "Vetoed bills infringing on faith; supports Bible in schools option.",
            "GUNS": "Constitutional carry; opposed expansions of controls.",
            "TAXES": "Cut income tax twice; income tax elimination goal.",
            "IMMIGRATION": "Strict enforcement; opposed driver's licenses for illegals.",
            "FAMILY-VALUES": "Traditional marriage; welfare reform for family stability.",
            "ELECTION-INTEGRITY": "Voter ID required; opposed ranked-choice voting."
        },
        "endorsements": ["Club for Growth", "NRA", "Federation for American Immigration Reform"]
    }
]

# Maine Summary
summary = {
    "state": "Maine",
    "title": "Maine 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Maine 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 4
**Total Candidates Profiled:** 9
**Election Dates:**
- 2026-06-09 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Maine POLITICAL LANDSCAPE

### **The Pine Tree State**

Maine is a **moderate blue-leaning state with strong rural conservative roots**:
- **Political History:** Voted Democratic in presidential elections since 1992 but splits electoral votes; GOP holds one Senate seat via Susan Collins.
- **Legislature:** Democrats control both chambers since 2012, passing progressive laws on abortion and guns.
- **Urban-Rural Divide:** Portland and southern coast lean left; northern and western counties conservative strongholds like Aroostook.
- **Unique State Factor:** Ranked-choice voting since 2018 alters dynamics, favoring moderates.

### **Why Maine Matters**

Maine is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** No gestational limits on abortion post-Dobbs; LD 1619 expanded access—urgent need to restrict.
- ✅ **Second Amendment:** Strong rights but red flag law passed 2023; defend against further erosion.
- ✅ **School Choice:** Limited programs; push for ESA expansion amid teachers' union dominance.
- ✅ **Religious Liberty:** Protections exist but threats from LGBTQ bills; safeguard faith-based services.
- ✅ **Family Values:** Same-sex marriage since 2012; combat gender ideology in schools.
- ✅ **Election Integrity:** Ranked-choice controversial; ensure Voter ID via referendum.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** This race decides Senate control; Collins' moderate seat vulnerable in blue Maine, impacting pro-life confirmations and religious protections.

**Susan Collins (Republican)** - Incumbent U.S. Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Lifelong Mainer from Caribou; St. Lawrence University grad.
- Senate service since 1996; chairs Aging Committee.
- Bipartisan dealmaker; no children, married to Thomas Daffron.

**Christian Conservative Analysis:**
- **Pro-Life:** Moderate; supported Roe codification but defunded Planned Parenthood—mixed record (6/10).
- **Religious Liberty:** Strong; co-sponsored defense acts (9/10).
- **Education/Parental Rights:** Supports choice but funds public schools (7/10).
- **Family Values:** Voted for same-sex marriage (5/10).
- **Overall Assessment:** 7/10—Reliable on guns/faith but weak on life; key moderate ally.

**Key Positions:**
- **ABORTION:** Roe protections with exceptions.
- **EDUCATION:** Charter expansion, rural funding.
- **RELIGIOUS FREEDOM:** First Amendment safeguards.
- **GUNS:** Background checks, no assault ban.
- **TAXES:** Middle-class cuts.
- **IMMIGRATION:** Secure borders with DREAMers.

**Endorsements:** NRA, U.S. Chamber, VFW

**Website:** https://www.collins.senate.gov

**Bill Clarke (Republican)** - Tech Entrepreneur

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Portland native; Geek Team founder.
- Small business owner; prior Taxpayers' Party run.
- Family man focused on community tech.

**Christian Conservative Analysis:**
- **Pro-Life:** Absolute; labels Planned Parenthood 'evil' (10/10).
- **Religious Liberty:** Defends against progressives (10/10).
- **Education/Parental Rights:** Anti-CRT, choice advocate (9/10).
- **Family Values:** Opposes LGBTQ agenda (10/10).
- **Overall Assessment:** 9.5/10—True conservative warrior.

**Key Positions:**
- **ABORTION:** Total ban.
- **EDUCATION:** Vouchers, transparency.
- **RELIGIOUS FREEDOM:** Faith exemptions.
- **GUNS:** No restrictions.
- **TAXES:** Flat tax.
- **IMMIGRATION:** Deportations.

**Endorsements:** Pro-Life Alliance, Gun Owners of America

**Website:** https://www.billclarke.us

**Janet Mills (Democrat)** - Former Governor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Farmington native; UMaine Law grad.
- DA and AG; term-limited governor.
- Independent style; avid hiker.

**Christian Conservative Analysis:**
- **Pro-Life:** Extreme pro-choice; expanded late-term (1/10).
- **Religious Liberty:** Separation strict (3/10).
- **Education/Parental Rights:** Union ally (2/10).
- **Family Values:** Inclusive agenda (1/10).
- **Overall Assessment:** 1/10—Threat to values.

**Key Positions:**
- **ABORTION:** Unlimited access.
- **EDUCATION:** Public funding only.
- **RELIGIOUS FREEDOM:** No exemptions.
- **GUNS:** Red flags, bans.
- **TAXES:** Raise on rich.
- **IMMIGRATION:** Sanctuary.

**Endorsements:** Planned Parenthood, EMILY's List

**Website:** https://www.janetmills.com

**Why It Matters:** Losing Collins hands Dems Senate power to codify abortion nationwide.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** Open seat post-Mills; controls vetoes on life, guns, education—pivotal for conservative resurgence.

**James Libby (Republican)** - State Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Naples resident; UMaine history/education.
- Teacher, coach, author; Senate since 2022.
- Married, three kids; youth sports leader.

**Christian Conservative Analysis:**
- **Pro-Life:** Restrictions advocate (9/10).
- **Religious Liberty:** Protects faith orgs (8/10).
- **Education/Parental Rights:** Choice champion (9/10).
- **Family Values:** Traditional focus (9/10).
- **Overall Assessment:** 9/10—Proven legislator for values.

**Key Positions:**
- **ABORTION:** Post-Roe limits.
- **EDUCATION:** Vouchers.
- **RELIGIOUS FREEDOM:** Belief protections.
- **GUNS:** Oppose controls.
- **TAXES:** No income tax.
- **IMMIGRATION:** Enforce laws.

**Endorsements:** NFIB, Maine Heritage

**Website:** https://www.jimlibbyforgovernor.com

**Owen McCarthy (Republican)** - Businessman

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Patten native; UMaine engineer.
- MedRhythms co-founder; FDA innovator.
- Family man; job creator.

**Christian Conservative Analysis:**
- **Pro-Life:** Exceptions but firm (8/10).
- **Religious Liberty:** Public faith support (8/10).
- **Education/Parental Rights:** STEM choice (8/10).
- **Family Values:** Nuclear promotion (8/10).
- **Overall Assessment:** 8/10—Fresh outsider voice.

**Key Positions:**
- **ABORTION:** Parental consent.
- **EDUCATION:** Vocational expansion.
- **RELIGIOUS FREEDOM:** No compelled speech.
- **GUNS:** 2A strong.
- **TAXES:** Business cuts.
- **IMMIGRATION:** Legal reform.

**Endorsements:** Chamber, Biotech Assoc

**Website:** https://owenformaine.com

**Shenna Bellows (Democrat)** - Secretary of State

**Faith Statement:** "As a Unitarian Universalist, I draw on principles of justice, equity, and compassion in public service."

**Background:**
- Manchester; Bowdoin/Law grad.
- Civil rights lawyer; Senate alum.
- Married, two kids; voter advocate.

**Christian Conservative Analysis:**
- **Pro-Life:** Pro-choice protector (1/10).
- **Religious Liberty:** Minority focus (4/10).
- **Education/Parental Rights:** Access over choice (2/10).
- **Family Values:** LGBTQ inclusive (1/10).
- **Overall Assessment:** 2/10—Election access threat.

**Key Positions:**
- **ABORTION:** Full protections.
- **EDUCATION:** Public only.
- **RELIGIOUS FREEDOM:** Separation.
- **GUNS:** Checks.
- **TAXES:** Fair share.
- **IMMIGRATION:** Welcoming.

**Endorsements:** ACLU, LWV

**Website:** https://www.shennabellows.com

**Why It Matters:** Governor shapes pro-family policies for a generation.

---

## 🔴 2026 CONGRESSIONAL RACES

### **U.S. House District 1** - 2026-11-03

**Context:** Urban district; flip needed to boost GOP House majority on life/gun bills.

**Ronald Russell (Republican)** - Army Veteran

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Fort Fairfield farm kid; Green Beret retiree.
- Defense firm founder; state rep.
- Married family; veteran leader.

**Christian Conservative Analysis:**
- **Pro-Life:** Heartbeat support (9/10).
- **Religious Liberty:** Military faith defender (9/10).
- **Education/Parental Rights:** Transparency (8/10).
- **Family Values:** Oppose ideology (9/10).
- **Overall Assessment:** 9/10—Warrior for values.

**Key Positions:**
- **ABORTION:** Bans.
- **EDUCATION:** Choice.
- **RELIGIOUS FREEDOM:** Chaplains.
- **GUNS:** Carry.
- **TAXES:** Cuts.
- **IMMIGRATION:** Wall.

**Endorsements:** NRA, Veterans First

**Website:** https://ronrussellforcongress.com

**Eric Small (Republican)** - Police Chief

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Sanford chief; 20+ years LE.
- Community volunteer; youth coach.
- Family; safety focus.

**Christian Conservative Analysis:**
- **Pro-Life:** State limits (8/10).
- **Religious Liberty:** LE expressions (8/10).
- **Education/Parental Rights:** Rights first (8/10).
- **Family Values:** Safety for families (8/10).
- **Overall Assessment:** 8/10—Law/order conservative.

**Key Positions:**
- **ABORTION:** Restrictions.
- **EDUCATION:** Trade schools.
- **RELIGIOUS FREEDOM:** Public square.
- **GUNS:** Ownership.
- **TAXES:** Local boosts.
- **IMMIGRATION:** Secure.

**Endorsements:** FOP, Sheriffs

**Website:** https://www.ericsmallforcongress.com

**Why It Matters:** Controls southern Maine voice on federal values.

### **U.S. House District 2** - 2026-11-03

**Context:** Rural swing; LePage's return could reclaim for conservatives on ag/family issues.

**Paul LePage (Republican)** - Former Governor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Lewiston orphan; UMaine master's.
- Waterville mayor; two-term gov.
- Married Ann; dual-citizen kids.

**Christian Conservative Analysis:**
- **Pro-Life:** 20-week ban (9/10).
- **Religious Liberty:** Bible option (9/10).
- **Education/Parental Rights:** Choice (9/10).
- **Family Values:** Welfare reform (9/10).
- **Overall Assessment:** 9/10—Proven fighter.

**Key Positions:**
- **ABORTION:** Restrictions.
- **EDUCATION:** Charters.
- **RELIGIOUS FREEDOM:** Veto protections.
- **GUNS:** Carry.
- **TAXES:** Cuts.
- **IMMIGRATION:** Enforcement.

**Endorsements:** Club for Growth, NRA

**Website:** https://paulepage.com

**Why It Matters:** Northern Maine's conservative heart—key for rural values.

---

## 🎯 KEY ISSUES FOR Maine CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Push LD 1619 repeal; enact 15-week limit.
- 50+ pregnancy centers via Maine Right to Life.
- Parental consent for minors mandatory.
- Block state funding for abortions.
- Recent: Defeated 2024 expansion attempt.

**Progressive Position:**
- Unlimited access via Mills' laws.
- Shield providers from bans.
- Fund Planned Parenthood expansions.
- Attack pro-life as 'extremist.'

**Christian Conservative Action:**
- Join Christian Civic League.
- Support Voter ID for Question 1.
- Volunteer MaineRTL.org events.
- Vote pro-life in primaries.

### **School Choice & Parental Rights**

**Conservative Position:**
- ESA program since 2023; expand to $10K/child.
- Parental Bill of Rights passed 2024.
- Banned CRT/gender books in K-12.
- Homeschool deregulated.
- Win: Blocked union monopoly 2025.

**Progressive Position:**
- Union control via Mills funding.
- DEI mandates in curriculum.
- Oppose choice as 'segregation.'

**Christian Conservative Action:**
- Run for school boards in rural counties.
- Back LD 1505 choice bill.
- Join Maine Parents Union.

### **Religious Freedom**

**Conservative Position:**
- Maine RFRA protects faith orgs.
- Exempt adoptions from LGBTQ laws.
- School prayer allowed.
- Threats: 2025 gender care mandates.

**Progressive Position:**
- Compel speech in anti-discrimination.
- Remove Trump via faith-neutral rulings.
- Fund secular over faith schools.

**Christian Conservative Action:**
- Support ADF cases in Maine.
- Lobby against compelled pronouns.
- Church forums on liberty.

### **Guns**

**Conservative Position:**
- Constitutional carry since 2015.
- No red flag until 2023 compromise.
- Preempt local bans.
- Challenge: Mills' assault push.

**Progressive Position:**
- Red flag expansion ballot 2025.
- Universal checks, mag limits.
- Post-Lewiston reforms.

**Christian Conservative Action:**
- Join MEGunRights.org.
- Oppose Question 2 red flag.
- Train church safety teams.

### **Taxes**

**Conservative Position:**
- Flat 5.8% income; cut to 5%.
- Property relief for elders.
- No sales tax on guns/ammo.
- LePage surpluses model.

**Progressive Position:**
- 3% surtax on $100K+.
- Corporate minimum.
- Fund green energy.

**Christian Conservative Action:**
- Support tax cap referendums.
- Donate to Maine Heritage.
- Advocate tithing-friendly policies.

### **Immigration**

**Conservative Position:**
- End sanctuary jails.
- E-Verify for jobs.
- Border aid funding.
- Rural impact: Farm labor balance.

**Progressive Position:**
- Driver's licenses for undocumented.
- Asylum expansion.
- Mills' welcoming executive.

**Christian Conservative Action:**
- Join FAIR chapters.
- Lobby for enforcement bills.
- Church aid to legal immigrants.

### **Family Values**

**Conservative Position:**
- Traditional marriage amendment push.
- Ban transitions for minors.
- Parental opt-out curriculum.
- Win: 2024 sports ban for trans.

**Progressive Position:**
- Gender-affirming in schools.
- Same-sex adoption mandates.
- Erase 'mother/father' terms.

**Christian Conservative Action:**
- Support Family Policy Council.
- Homeschool co-ops.
- Biblical marriage sermons.

### **Election Integrity**

**Conservative Position:**
- Voter ID Question 1 2026.
- End ranked-choice.
- Paper ballots, audits.
- Bellows controversies.

**Progressive Position:**
- Automatic registration.
- Mail-in expansion.
- Oppose ID as suppression.

**Christian Conservative Action:**
- Poll watch training.
- Support Voter ID PAC.
- Church registration drives.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- 2026-05-01 - Voter registration deadline
- 2026-10-01 - Early voting begins
- 2026-06-09 - Primary Election
- 2026-11-03 - General Election

**Voter Registration:** https://www.maine.gov/sos/cec/cec/reg.html

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
✅ **Share on social media** with #MaineFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Maine CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Maine coverage
- **Maine Right to Life** - Pro-life ratings
- **Christian Civic League of Maine** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Maine Secretary of State**: https://www.maine.gov/sos/
- **County Election Offices**: Contact local clerk via sos.maine.gov
- **Early Voting Locations**: Check county sites or app.

### **Conservative Organizations:**
- **Maine Right to Life**: https://www.mainertl.org/
- **Christian Civic League**: https://www.cclmaine.org/
- **Maine Gun Rights**: https://www.megunrights.org/
- **Maine School Choice**: https://www.maineschoolchoice.org/
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Maine CHRISTIANS

**2026 Elections Matter:**
- Senate race determines SCOTUS pro-life justices.
- Governor affects abortion bans and school choice.
- House seats impact federal family funding.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Rural economy boosted via tax cuts
✅ Border security for safe communities
✅ Faith in public life restored

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Taxes hiked on families
❌ Sanctuary chaos increases crime
❌ Secular agenda dominates

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Susan Collins, Bill Clarke, James Libby, Owen McCarthy, Ronald Russell, Eric Small, Paul LePage and their families
- Maine Governor transition
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Maine
- Revival and awakening in Maine
- God's will in Maine elections

**Scripture for Maine Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Maine coverage, email contact@ekewaka.com

**Maine CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Maine races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Maine'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Maine races...")
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

print(f"\nChecking for existing Maine candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Maine'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Maine candidates...")
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

print("\nProcessing Maine summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Maine'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Maine data upload complete!")