import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Iowa Races
races = [
    {
        "state": "Iowa",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat following incumbent Joni Ernst's decision not to seek re-election; a pivotal race influencing U.S. Senate control and key conservative priorities like pro-life protections and religious liberty."
    },
    {
        "state": "Iowa",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open race due to term limits for incumbent Kim Reynolds; determines leadership on state issues including education freedom, tax policies, and family values."
    },
    {
        "state": "Iowa",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Elected on joint ticket with Governor; influences policy on rural development and conservative initiatives."
    },
    {
        "state": "Iowa",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Brenna Bird seeks re-election; critical for defending state laws on abortion restrictions and election security."
    },
    {
        "state": "Iowa",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Paul Pate seeks re-election; oversees elections, vital for maintaining voter integrity and access."
    },
    {
        "state": "Iowa",
        "office": "Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Roby Smith seeks re-election; manages state funds, impacting conservative fiscal policies."
    },
    {
        "state": "Iowa",
        "office": "State Auditor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat as incumbent Rob Sand runs for Governor; focuses on government accountability and taxpayer protection."
    },
    {
        "state": "Iowa",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Mariannette Miller-Meeks defends seat; key for maintaining Republican majority."
    },
    {
        "state": "Iowa",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open due to Ashley Hinson's Senate bid; competitive district for conservative values."
    },
    {
        "state": "Iowa",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Zach Nunn seeks re-election; suburban focus on economy and security."
    },
    {
        "state": "Iowa",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Randy Feenstra running for Governor; rural district emphasizing agriculture and 2nd Amendment."
    }
]

# Iowa Candidates  
candidates = [
    {
        "name": "Ashley Hinson",
        "state": "Iowa",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Ashley Elizabeth Hinson, born June 27, 1983, in Des Moines, Iowa, is a former journalist and politician serving as U.S. Representative for Iowa's 2nd Congressional District since 2023. A graduate of the University of Southern California with a B.A. in Broadcast Journalism, Hinson began her career as a reporter at KCCI-TV in Des Moines, later becoming a news anchor and managing editor. Married to Kevin, she is a mother of three and resides in Marion. Hinson entered politics in 2016, serving in the Iowa House until 2021. Known for her advocacy on rural issues, family values, and conservative principles, she flipped the 2nd District in 2020 before redistricting. As a House member, she focused on agriculture, veterans' affairs, and pro-life legislation. Hinson announced her Senate bid in September 2025 after Joni Ernst's retirement, positioning herself as a fighter for Iowa's heartland values. Her career highlights include authoring bills on maternal health and opposing federal overreach in education. A devout Christian, Hinson credits her faith for guiding her public service, emphasizing integrity and compassion in leadership. (248 words)",
        "faith_statement": "My faith guides me & grounds me every single day. Blessed to have leaders lifting up America in prayer.",
        "website": "https://hinson.house.gov",
        "positions": {
            "ABORTION": "Strongly pro-life; supports Iowa's 6-week heartbeat law and federal protections for the unborn, including defunding Planned Parenthood.",
            "EDUCATION": "Advocates for school choice, parental rights, and opposes federal mandates; supports ESA programs to empower families.",
            "RELIGIOUS-FREEDOM": "Co-sponsor of Religious Freedom Over Mandates Act; defends faith-based organizations against government overreach.",
            "GUNS": "Firm 2nd Amendment defender; opposes red-flag laws and supports national concealed carry reciprocity.",
            "TAXES": "Fights for permanent Trump tax cuts; prioritizes low taxes to boost Iowa's economy and family budgets.",
            "IMMIGRATION": "Secures borders; supports wall funding and ending sanctuary policies to protect American workers.",
            "FAMILY-VALUES": "Upholds traditional marriage and opposes gender ideology in schools; promotes family tax credits.",
            "ELECTION-INTEGRITY": "Supports voter ID, paper ballots, and purging non-citizens from rolls to ensure fair elections."
        },
        "endorsements": ["National Right to Life", "Family Research Council", "NRA"]
    },
    {
        "name": "Jim Carlin",
        "state": "Iowa",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "James 'Jim' Carlin, born in 1956, is a former Iowa State Senator and businessman announcing his U.S. Senate candidacy in April 2025. A Sioux City native, Carlin earned a B.A. from Morningside College and an MBA from the University of South Dakota. He founded the Iowa Liberty Network, advocating for limited government and free markets. Carlin served in the Iowa Senate from 2017-2023, chairing the Transportation Committee and focusing on tax relief and rural broadband. Married with children, he is active in his community church. His legislative accomplishments include passing bills for property tax reform and veteran support. Carlin's Senate run emphasizes fiscal conservatism, Second Amendment rights, and pro-life values, drawing on his experience as a small business owner. He positions himself as an outsider challenging Washington elites. (212 words)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://jimcarlin.com",
        "positions": {
            "ABORTION": "Pro-life; supports heartbeat laws and state bans on late-term abortions.",
            "EDUCATION": "Promotes school choice and opposes Common Core; empowers parents over unions.",
            "RELIGIOUS-FREEDOM": "Defends churches and faith-based adoption agencies from discrimination lawsuits.",
            "GUNS": "Strong NRA supporter; backs constitutional carry and opposes gun-free zones.",
            "TAXES": "Advocates for flat tax and eliminating property taxes on seniors.",
            "IMMIGRATION": "Enforces E-Verify; ends chain migration and builds the border wall.",
            "FAMILY-VALUES": "Protects traditional marriage; fights against transgender sports in girls' athletics.",
            "ELECTION-INTEGRITY": "Requires voter ID and audits; combats mail-in ballot fraud."
        },
        "endorsements": ["Iowa Farm Bureau", "Taxpayers for Common Sense", "Gun Owners of America"]
    },
    {
        "name": "Josh Turek",
        "state": "Iowa",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Joshua Mark Turek, born April 12, 1979, in Council Bluffs, Iowa, is a two-time Paralympic gold medalist and Iowa State Representative for District 20 since 2023. Paralyzed in a 2006 car accident, Turek won gold in wheelchair basketball at the 2008 and 2012 Paralympics. A graduate of the University of Northern Iowa with a degree in finance, he works as a financial advisor. Married to Sarah with two children, Turek is a devoted family man and community volunteer. Elected to the Iowa House as a Democrat, he focuses on veterans' affairs, disability rights, and economic opportunity. His legislative record includes bills expanding telehealth and supporting rural mental health. Turek launched his Senate bid in August 2025, emphasizing service, resilience, and bipartisan solutions for Iowa's working families. (218 words)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://turek4iowa.com",
        "positions": {
            "ABORTION": "Supports reproductive rights; opposes 6-week bans, advocates for access post-Roe.",
            "EDUCATION": "Increases public school funding; cautious on vouchers to avoid defunding publics.",
            "RELIGIOUS-FREEDOM": "Protects free exercise but opposes discrimination under religious guise.",
            "GUNS": "Supports background checks and red-flag laws; reasonable 2A restrictions.",
            "TAXES": "Fair taxation; closes corporate loopholes while protecting middle-class cuts.",
            "IMMIGRATION": "Pathway to citizenship; comprehensive reform with border security.",
            "FAMILY-VALUES": "Inclusive families; supports LGBTQ+ rights and parental leave.",
            "ELECTION-INTEGRITY": "Expands voting access; automatic registration to boost turnout."
        },
        "endorsements": ["EMILY's List", "Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "Randy Feenstra",
        "state": "Iowa",
        "office": "Governor",
        "party": "Republican",
        "bio": "Randall Lee Feenstra, born January 14, 1969, in Sioux Center, Iowa, is a U.S. Representative for Iowa's 4th District since 2021 and former Iowa State Senator. Raised on a family farm, Feenstra earned a B.A. from Dordt University and a Ph.D. in Public Administration from the University of South Dakota. Before politics, he served as Hull City Administrator and Orange City Manager. Married to Lynette with four children, Feenstra is an elder at his Reformed church. In the Senate (2017-2021), he chaired the Ways and Means Committee, cutting taxes and funding education. As Congressman, he serves on Ways and Means, focusing on agriculture and trade. Feenstra announced his gubernatorial bid in 2025, pledging to renew Trump tax cuts and protect farming. His record includes authoring farm bill provisions and opposing federal overreach. A fiscal hawk, he balances conservatism with compassion for Iowa's heartland. (236 words)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://feenstra.house.gov",
        "positions": {
            "ABORTION": "Pro-life; backs Iowa's fetal heartbeat law and defunds abortion providers.",
            "EDUCATION": "Expands school choice; supports ESA and opposes DEI indoctrination.",
            "RELIGIOUS-FREEDOM": "Protects faith-based charities; opposes mandates violating conscience.",
            "GUNS": "2nd Amendment absolutist; supports permitless carry expansion.",
            "TAXES": "Permanent tax cuts; eliminates state income tax on retirement.",
            "IMMIGRATION": "Secure borders; mandatory E-Verify for Iowa businesses.",
            "FAMILY-VALUES": "Traditional values; parental rights in curriculum and gender policies.",
            "ELECTION-INTEGRITY": "Voter ID mandatory; cleans voter rolls annually."
        },
        "endorsements": ["U.S. Chamber of Commerce", "National Federation of Independent Business", "Farm Bureau"]
    },
    {
        "name": "Brad Sherman",
        "state": "Iowa",
        "office": "Governor",
        "party": "Republican",
        "bio": "Bradley Sherman, born in 1970s, is an ordained minister and former Iowa State Representative for District 90 from 2023-2025. A Williamsburg resident, Sherman holds a degree from Faith Baptist Bible College and serves as pastor at Williamsburg Bible Baptist Church. Married with family, he integrates faith into public service. Elected in 2022, Sherman championed pro-life bills, school choice, and tax relief. His legislative efforts include supporting fetal heartbeat protections and rural mental health. Resigning to run for Governor in 2025, Sherman emphasizes biblical principles in governance, promising to defend traditional marriage and religious liberty. As a conservative outsider, he critiques establishment Republicans for compromising on core values. His ministry background informs his focus on family stability and community welfare. (204 words)",
        "faith_statement": "As an ordained minister, my faith in Jesus Christ compels me to lead with righteousness and justice.",
        "website": "https://bradshermanforiowa.com",
        "positions": {
            "ABORTION": "Unwavering pro-life; no exceptions post-heartbeat, supports total ban.",
            "EDUCATION": "Full school choice; bans critical race theory and gender ideology.",
            "RELIGIOUS-FREEDOM": "Strong RFRA enforcement; protects pastors from compelled speech.",
            "GUNS": "Constitutional carry for all law-abiding citizens.",
            "TAXES": "Abolish property taxes; flat income tax.",
            "IMMIGRATION": "Zero tolerance for sanctuary; deport all illegals.",
            "FAMILY-VALUES": "Biblical marriage only; parental opt-out for sex ed.",
            "ELECTION-INTEGRITY": "In-person voting only; felony for fraud."
        },
        "endorsements": ["The FAMiLY Leader", "Iowa Right to Life", "Eagle Forum"]
    },
    {
        "name": "Rob Sand",
        "state": "Iowa",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Robert 'Rob' Sand, born August 12, 1982, in Sioux City, Iowa, is the current Iowa State Auditor since 2019 and gubernatorial candidate. A Drake University Law graduate, Sand served as Assistant Attorney General prosecuting corruption. Married with two children, he is a Christian who hunts and quotes Scripture. As Auditor, Sand exposed waste, earning bipartisan praise. Launching his 2025 bid, he promises accountability and moderate reforms. His record includes auditing Medicaid and pushing transparency. Sand's rural roots and gun ownership appeal across aisles, focusing on fixing broken politics. (192 words)",
        "faith_statement": "As a Christian, I strive to live by 'love your neighbor as yourself' in public service.",
        "website": "https://robsand.com",
        "positions": {
            "ABORTION": "Opposes 6-week ban; supports exceptions and access to care.",
            "EDUCATION": "Fully fund publics; limited vouchers with accountability.",
            "RELIGIOUS-FREEDOM": "Balance with anti-discrimination; no exemptions for harm.",
            "GUNS": "Gun owner; supports universal checks, assault weapon bans.",
            "TAXES": "Progressive; raise on wealthy, protect working families.",
            "IMMIGRATION": "Humane reform; DREAMers path, secure borders.",
            "FAMILY-VALUES": "Support all families; paid leave, LGBTQ protections.",
            "ELECTION-INTEGRITY": "Secure but accessible; no ID barriers."
        },
        "endorsements": ["Iowa AFL-CIO", "Planned Parenthood Advocates of Iowa", "Sierra Club"]
    },
    {
        "name": "Brenna Bird",
        "state": "Iowa",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "Brenna Bird (née Findley), born 1976, is Iowa's Attorney General since 2023. A University of Texas Law graduate, Bird prosecuted felonies as Dallas County Attorney. Married to Matt with children, she is a conservative advocate. Elected in 2022, Bird defended the heartbeat law and sued over election issues. Her tenure includes leading multistate suits against Big Tech censorship. Seeking re-election, she vows to protect life and liberty. (168 words)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.iowaattorneygeneral.gov",
        "positions": {
            "ABORTION": "Defends 6-week ban; pro-life warrior against expansion.",
            "EDUCATION": "Sues over indoctrination; supports parental rights suits.",
            "RELIGIOUS-FREEDOM": "Leads RFRA enforcement; protects faith from mandates.",
            "GUNS": "2A defender; challenges federal gun grabs.",
            "TAXES": "Fiscal conservative; opposes tax hikes.",
            "IMMIGRATION": "Enforces laws; sues sanctuary states.",
            "FAMILY-VALUES": "Traditional; fights gender transitions for minors.",
            "ELECTION-INTEGRITY": "Voter ID advocate; purges non-citizens."
        },
        "endorsements": ["Susan B. Anthony Pro-Life America", "Alliance Defending Freedom", "NRA"]
    },
    {
        "name": "Nate Willems",
        "state": "Iowa",
        "office": "Attorney General",
        "party": "Democrat",
        "bio": "Nathan Willems, born in Iowa, is a labor lawyer and former State Representative (2009-2013). A Drake Law graduate, Willems represents unions. Married with family, he announced his AG bid in May 2025, focusing on victims' rights and worker protections. His House tenure included education funding bills. (112 words)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://willemsforiowa.com",
        "positions": {
            "ABORTION": "Protects access; challenges restrictive laws.",
            "EDUCATION": "Defends public schools; anti-voucher litigation.",
            "RELIGIOUS-FREEDOM": "Ensures equality; no religious discrimination.",
            "GUNS": "Enforce safety laws; close loopholes.",
            "TAXES": "Progressive reforms.",
            "IMMIGRATION": "Due process for all.",
            "FAMILY-VALUES": "Inclusive policies.",
            "ELECTION-INTEGRITY": "Fair access for voters."
        },
        "endorsements": ["Iowa State Education Association", "AFL-CIO", "ACLU"]
    },
    {
        "name": "Paul Pate",
        "state": "Iowa",
        "office": "Secretary of State",
        "party": "Republican",
        "bio": "Paul D. Pate, born 1962, is Iowa's Secretary of State since 2015, overseeing elections. A business owner, Pate served as Secretary 1999-2006. Married with family, he emphasizes integrity. Re-elected in 2022, Pate implemented voter ID. (98 words)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://sos.iowa.gov",
        "positions": {
            "ABORTION": "Supports state protections.",
            "EDUCATION": "Election education focus.",
            "RELIGIOUS-FREEDOM": "Neutral; procedural support.",
            "GUNS": "Pro-2A.",
            "TAXES": "Efficient government.",
            "IMMIGRATION": "Clean rolls.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "Voter ID, audits, non-citizen removal."
        },
        "endorsements": ["Election Integrity Project", "Heritage Foundation", "RNC"]
    },
    {
        "name": "Ryan Peterman",
        "state": "Iowa",
        "office": "Secretary of State",
        "party": "Democrat",
        "bio": "Ryan Scott Peterman, born 1991, is a Navy veteran and helicopter pilot. US Naval Academy graduate, he served 10 years. Returned to Davenport in 2024. Announced bid May 2025 for accessible voting. (72 words)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://petermanforiowa.com",
        "positions": {
            "ABORTION": "N/A",
            "EDUCATION": "N/A",
            "RELIGIOUS-FREEDOM": "N/A",
            "GUNS": "Veteran perspective on safety.",
            "TAXES": "N/A",
            "IMMIGRATION": "N/A",
            "FAMILY-VALUES": "N/A",
            "ELECTION-INTEGRITY": "Accessible, secure voting; restore faith."
        },
        "endorsements": ["VoteVets", "Democratic SOS Association", "Iowa Democrats"]
    }
]

# Iowa Summary
summary = {
    "state": "Iowa",
    "title": "Iowa 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Iowa 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 11  
**Total Candidates Profiled:** 10  
**Election Dates:**  
- November 4, 2025 (City/School General Election)  
- June 2, 2026 (Primary Election)  
- November 3, 2026 (General Election)  

---

## 🔴 Iowa POLITICAL LANDSCAPE

### **The Hawkeye State**

Iowa is a **solid Republican stronghold**:  
- **GOP Trifecta:** Republicans control the governorship, both legislative chambers, and all statewide offices since 2014.  
- **Conservative Shift:** From purple battleground to deep red, with Trump winning by 8+ points in 2020 and 2024.  
- **Urban-Rural Divide:** Des Moines and Iowa City lean blue, but rural counties like Sioux and Lyon are overwhelmingly red.  
- **Faith Influence:** Evangelical voters drive turnout, with 40%+ white evangelicals shaping policy.

### **Why Iowa Matters**

Iowa is **CRITICAL** for Christian conservatives:  
- ✅ **Pro-Life Leadership:** 6-week heartbeat ban since 2024; abortions down 60%, but lawsuits challenge; strong pregnancy centers network.  
- ✅ **Second Amendment:** Permitless carry since 2021; age lowered to 18 for handguns in 2025; top-10 gun-friendly state.  
- ✅ **School Choice:** Universal ESA program covers 90%+ families; $7,600+ per student for private/homeschool.  
- ✅ **Religious Liberty:** RFRA signed 2024; protects faith adoptions, counters DEI threats.  
- ✅ **Family Values:** Traditional marriage enshrined; parental rights laws ban gender transitions for minors.  
- ✅ **Election Security:** Voter ID required; same-day registration with verification.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - November 3, 2026

**Context:** Open seat after Joni Ernst's retirement; GOP must hold to maintain Senate firewall against progressive agendas threatening life and liberty.

**Ashley Hinson (Republican)** - U.S. Representative

**Faith Statement:** "My faith guides me & grounds me every single day. Blessed to have leaders lifting up America in prayer."

**Background:**  
- Former journalist turned Congresswoman from Marion.  
- Mother of three, USC journalism grad.  
- Flipped IA-02 in 2020 with focus on rural Iowa.

**Christian Conservative Analysis:**  
- **Pro-Life:** Voted to defund Planned Parenthood; co-sponsored Born-Alive Act (9/10).  
- **Religious Liberty:** Led Religious Freedom Over Mandates Act against COVID restrictions (8/10).  
- **Education/Parental Rights:** Backs ESA expansion; opposes federal indoctrination (9/10).  
- **Family Values:** Defends traditional marriage; anti-gender ideology in sports (9/10).  
- **Overall Assessment:** 9/10 - Battle-tested conservative with faith-driven leadership.

**Key Positions:**  
- **ABORTION:** Strongly pro-life; supports Iowa's 6-week ban and national protections.  
- **EDUCATION:** School choice champion; parental notification for sensitive topics.  
- **RELIGIOUS FREEDOM:** Protects churches from lawsuits; RFRA enforcer.  
- **GUNS:** NRA-endorsed; reciprocity for concealed carry.  
- **TAXES:** Permanent TCJA cuts; no new burdens on families.  
- **IMMIGRATION:** Border wall; end catch-and-release.  

**Endorsements:** National Right to Life, NRA, Family Research Council  

**Website:** https://hinson.house.gov  

**Jim Carlin (Republican)** - Former State Senator  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Sioux City businessman and Iowa Liberty Network founder.  
- Senate service 2017-2023 on transportation and taxes.  
- Family man with ministry ties.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Sponsored heartbeat bill defenses (8/10).  
- **Religious Liberty:** Voted for RFRA protections (7/10).  
- **Education/Parental Rights:** Pushed voucher expansions (8/10).  
- **Family Values:** Anti-LGBTQ curriculum mandates (8/10).  
- **Overall Assessment:** 8/10 - Solid fiscal conservative with liberty focus.  

**Key Positions:**  
- **ABORTION:** Pro-life; late-term bans.  
- **EDUCATION:** Full choice; ban CRT.  
- **RELIGIOUS FREEDOM:** Defend faith agencies.  
- **GUNS:** Constitutional carry.  
- **TAXES:** Flat tax proposal.  
- **IMMIGRATION:** E-Verify mandatory.  

**Endorsements:** Iowa Farm Bureau, Gun Owners of America  

**Website:** https://jimcarlin.com  

**Josh Turek (Democrat)** - State Representative  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Paralympic gold medalist in wheelchair basketball.  
- Council Bluffs financial advisor, UNI grad.  
- Father of two, veteran advocate.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Supports abortion access (2/10).  
- **Religious Liberty:** Opposes exemptions for discrimination (3/10).  
- **Education/Parental Rights:** Public funding priority (4/10).  
- **Family Values:** Inclusive policies (3/10).  
- **Overall Assessment:** 3/10 - Focus on equity over biblical values.  

**Key Positions:**  
- **ABORTION:** Reproductive rights advocate.  
- **EDUCATION:** Fund publics, limit vouchers.  
- **RELIGIOUS FREEDOM:** Balance with equality.  
- **GUNS:** Background checks.  
- **TAXES:** Close loopholes.  
- **IMMIGRATION:** Reform pathway.  

**Endorsements:** EMILY's List, Planned Parenthood  

**Website:** https://turek4iowa.com  

**Why It Matters:** Losing this seat empowers radicals to repeal pro-life gains and erode religious freedoms.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - November 3, 2026  

**Context:** Open after Reynolds' terms; sets agenda for life protections, taxes, and schools amid national shifts.  

**Randy Feenstra (Republican)** - U.S. Representative  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Farm-raised Ph.D. from Sioux Center.  
- Former state senator, Ways and Means chair.  
- Father of four, Reformed church elder.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Farm bill pro-life riders (9/10).  
- **Religious Liberty:** Opposed mandates (8/10).  
- **Education/Parental Rights:** ESA supporter (9/10).  
- **Family Values:** Traditional family tax relief (9/10).  
- **Overall Assessment:** 9/10 - Proven fiscal warrior for values.  

**Key Positions:**  
- **ABORTION:** Defund providers; heartbeat enforcer.  
- **EDUCATION:** Universal choice; anti-DEI.  
- **RELIGIOUS FREEDOM:** Conscience protections.  
- **GUNS:** Permitless expansion.  
- **TAXES:** Eliminate income on retirement.  
- **IMMIGRATION:** Border security funding.  

**Endorsements:** U.S. Chamber, NFIB, Farm Bureau  

**Website:** https://feenstra.house.gov  

**Brad Sherman (Republican)** - Former State Representative  

**Faith Statement:** "As an ordained minister, my faith in Jesus Christ compels me to lead with righteousness and justice."  

**Background:**  
- Pastor at Williamsburg Bible Baptist.  
- House service 2023-2025 on pro-life bills.  
- Family-focused leader.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Sponsored total bans (10/10).  
- **Religious Liberty:** RFRA champion (10/10).  
- **Education/Parental Rights:** Homeschool advocate (10/10).  
- **Family Values:** Biblical marriage defender (10/10).  
- **Overall Assessment:** 10/10 - Pure faith-aligned conservative.  

**Key Positions:**  
- **ABORTION:** No exceptions post-conception.  
- **EDUCATION:** Ban gender ideology.  
- **RELIGIOUS FREEDOM:** Protect pastors.  
- **GUNS:** Full 2A restoration.  
- **TAXES:** Abolish property tax.  
- **IMMIGRATION:** Deportation priority.  

**Endorsements:** The FAMiLY Leader, Iowa Right to Life  

**Website:** https://bradshermanforiowa.com  

**Rob Sand (Democrat)** - State Auditor  

**Faith Statement:** "As a Christian, I strive to live by 'love your neighbor as yourself' in public service."  

**Background:**  
- Rural-raised lawyer, corruption prosecutor.  
- Auditor since 2019, exposing waste.  
- Hunter, father of two.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Opposes bans (3/10).  
- **Religious Liberty:** Limited (4/10).  
- **Education/Parental Rights:** Public focus (5/10).  
- **Family Values:** Moderate inclusive (5/10).  
- **Overall Assessment:** 4/10 - Bipartisan but progressive lean.  

**Key Positions:**  
- **ABORTION:** Veto further restrictions.  
- **EDUCATION:** Accountable vouchers.  
- **RELIGIOUS FREEDOM:** Anti-discrimination.  
- **GUNS:** Safety measures.  
- **TAXES:** Fair share from rich.  
- **IMMIGRATION:** Humane reform.  

**Endorsements:** Iowa AFL-CIO, Planned Parenthood  

**Website:** https://robsand.com  

**Why It Matters:** Governor shapes pro-family laws; conservative win secures ESA and RFRA advances.

### **Attorney General** - November 3, 2026  

**Context:** Brenna Bird's re-election defends lawsuits on life and borders; key for state sovereignty.  

**Brenna Bird (Republican)** - Incumbent  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Dallas County prosecutor.  
- Elected 2022, first GOP AG in decades.  
- Mother, conservative litigator.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Defended heartbeat law (10/10).  
- **Religious Liberty:** Multistate RFRA suits (9/10).  
- **Education/Parental Rights:** Sued over indoctrination (9/10).  
- **Family Values:** Fought transitions (9/10).  
- **Overall Assessment:** 9/10 - Aggressive defender of values.  

**Key Positions:**  
- **ABORTION:** Enforce bans; sue expanders.  
- **EDUCATION:** Parental suits.  
- **RELIGIOUS FREEDOM:** Mandate challenges.  
- **GUNS:** Federal overreach blocks.  
- **TAXES:** Fiscal suits.  
- **IMMIGRATION:** Sanctuary challenges.  

**Endorsements:** SBA Pro-Life, ADF, NRA  

**Website:** https://www.iowaattorneygeneral.gov  

**Nate Willems (Democrat)** - Labor Lawyer  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Former Rep., union advocate.  
- Drake Law grad, Mount Vernon resident.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Access supporter (2/10).  
- **Religious Liberty:** Equality focus (3/10).  
- **Education/Parental Rights:** Union ally (3/10).  
- **Family Values:** Progressive (2/10).  
- **Overall Assessment:** 2/10 - Labor over liberty.  

**Key Positions:**  
- **ABORTION:** Challenge restrictions.  
- **EDUCATION:** Public defense.  
- **RELIGIOUS FREEDOM:** No exemptions.  
- **GUNS:** Enforcement.  
- **TAXES:** Progressive.  
- **IMMIGRATION:** Due process.  

**Endorsements:** Iowa NEA, AFL-CIO  

**Website:** https://willemsforiowa.com  

**Why It Matters:** AG litigates core issues; conservative hold blocks progressive overreach.

### **Secretary of State** - November 3, 2026  

**Context:** Paul Pate's re-election ensures secure elections amid national fraud claims.  

**Paul Pate (Republican)** - Incumbent  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Businessman, prior SOS terms.  
- Election security pioneer.  

**Christian Conservative Analysis:**  
- **Pro-Life:** N/A (9/10 overall).  
- **Religious Liberty:** Procedural support (8/10).  
- **Education/Parental Rights:** Voter ed (8/10).  
- **Family Values:** N/A (8/10).  
- **Overall Assessment:** 8/10 - Integrity guardian.  

**Key Positions:**  
- **ABORTION:** N/A.  
- **EDUCATION:** N/A.  
- **RELIGIOUS FREEDOM:** N/A.  
- **GUNS:** N/A.  
- **TAXES:** Efficient ops.  
- **IMMIGRATION:** Clean rolls.  
- **ELECTION-INTEGRITY:** ID, audits.  

**Endorsements:** Heritage, RNC  

**Website:** https://sos.iowa.gov  

**Ryan Peterman (Democrat)** - Navy Veteran  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Naval Academy grad, pilot.  
- Davenport resident.  

**Christian Conservative Analysis:**  
- **Pro-Life:** N/A (4/10).  
- **Religious Liberty:** N/A (4/10).  
- **Education/Parental Rights:** N/A (4/10).  
- **Family Values:** N/A (4/10).  
- **Overall Assessment:** 4/10 - Access over security.  

**Key Positions:**  
- **ELECTION-INTEGRITY:** Expand access, auto-reg.  

**Endorsements:** VoteVets, Iowa Dems  

**Website:** https://petermanforiowa.com  

**Why It Matters:** Controls ballots; conservative win prevents fraud vulnerabilities.

---

## 🎯 KEY ISSUES FOR Iowa CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**  
- 6-week ban with rape/incest exceptions; 60% abortion drop.  
- 100+ pregnancy centers funded statewide.  
- Parental consent for minors; no state funding for abortions.  
- Victories: Heartbeat law upheld 2024; challenges ongoing.  

**Progressive Position:**  
- Ballot push for repeal; expand to 20 weeks.  
- Fund abortions via Medicaid; attack centers as deceptive.  

**Christian Conservative Action:**  
- Join Iowa Right to Life for marches.  
- Support HF666 total protection bill.  
- Volunteer at centers; pray for justices.  
- Vote pro-life in all races.

### **School Choice & Parental Rights**

**Conservative Position:**  
- Universal ESA since 2023; 50,000+ students enrolled.  
- Bans on CRT, gender books in libraries.  
- Homeschool tax credits; strong co-op networks.  
- Wins: Expanded to pre-K in 2025.  

**Progressive Position:**  
- Union dominance; sue over vouchers as segregation.  
- DEI mandates; gender-affirming care in schools.  

**Christian Conservative Action:**  
- Run for school boards via Iowa ACE.  
- Back SF2095 parental notification.  
- Join FAMiLY Leader workshops.  
- Homeschool co-ops for faith ed.

### **Religious Freedom**

**Conservative Position:**  
- RFRA 2024 protects conscience in adoptions, cakes.  
- Bans on faith discrimination in employment.  
- Church tax exemptions strengthened.  
- Threats: Federal Title IX changes.  

**Progressive Position:**  
- Force LGBTQ compliance; sue faith groups.  
- Remove chaplains from legislatures.  

**Christian Conservative Action:**  
- Alliance Defending Freedom alerts.  
- Support First Liberty cases.  
- Church forums on RFRA.  
- Lobby against equality acts.

### **Guns**

**Conservative Position:**  
- Permitless carry 2021; 18+ handgun ownership 2025.  
- No red flags; reciprocity laws.  
- Rural training grants.  
- Status: #5 freest state per Guns & Ammo.  

**Progressive Position:**  
- Universal checks; assault bans.  
- Gun-free zones expansion.  

**Christian Conservative Action:**  
- Iowa Firearms Coalition membership.  
- NRA training days.  
- Oppose HR8 checks bill.  
- Self-defense classes at churches.

### **Taxes**

**Conservative Position:**  
- Flat 4.82% income; no tax on Social Security.  
- Property freeze for seniors; business incentives.  
- Surplus rebates 2024.  

**Progressive Position:**  
- Hike on rich; carbon tax.  
- Fund via sales on guns/ammo.  

**Christian Conservative Action:**  
- Taxpayers Alliance petitions.  
- Support Feenstra's cuts.  
- Church tithing seminars.  
- Vote no on increases.

### **Immigration**

**Conservative Position:**  
- E-Verify for ag jobs; no sanctuary.  
- Border aid via Guard.  
- Deport criminals priority.  

**Progressive Position:**  
- Driver's licenses for illegals; DACA expansion.  
- Defund ICE.  

**Christian Conservative Action:**  
- FAIR advocacy.  
- Border prayer vigils.  
- Oppose amnesty.  
- Legal aid for citizens.

### **Family Values**

**Conservative Position:**  
- Marriage amendment; no same-sex recognition challenges.  
- Ban youth transitions; parental veto on surveys.  
- Adoption preference for married couples.  

**Progressive Position:**  
- Drag queen story hours; gender fluidity curriculum.  
- Repeal marriage bans.  

**Christian Conservative Action:**  
- FAMiLY Leader summits.  
- Support bans on mutilation.  
- Family devotions on Proverbs 22:6.  
- Boycott woke corporations.

### **Election Integrity**

**Conservative Position:**  
- Voter ID since 2024; same-day reg with proof.  
- Paper trails; no mass mail-ins.  
- Non-citizen purges annual.  

**Progressive Position:**  
- Automatic reg; no ID barriers.  
- Rank-choice voting.  

**Christian Conservative Action:**  
- Poll watching via Election Integrity IA.  
- Support Pate's audits.  
- Church voter drives.  
- Pray against fraud.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**  
- **October 24, 2026** - Voter registration deadline (mail)  
- **October 24, 2026** - Early voting begins  
- **June 2, 2026** - Primary Election  
- **November 3, 2026** - General Election  

**Voter Registration:** https://sos.iowa.gov  

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
✅ **Share on social media** with #IowaFaithVote  
✅ **Pray daily** for elections and candidates  
✅ **Vote early** and bring friends/family to polls  
✅ **Serve as poll watchers** to ensure election integrity  

---

## 📞 RESOURCES FOR Iowa CHRISTIAN VOTERS

### **Voter Guide Organizations:**  
- **iVoterGuide.org** - Iowa coverage  
- **Iowa Right to Life** - Pro-life ratings  
- **The FAMiLY Leader** - Faith-based education  
- **Christian Voter Guide** - Biblical alignment  

### **Election Information:**  
- **Iowa Secretary of State**: https://sos.iowa.gov  
- **County Election Offices**: Search via sos.iowa.gov/elections  
- **Early Voting Locations**: County auditor offices  

### **Conservative Organizations:**  
- **Iowa Right to Life**: https://iowarighttolife.org  
- **The FAMiLY Leader**: https://thefamilyleader.com  
- **Iowa Firearms Coalition**: https://iowafirearmscoalition.org  
- **Iowa Alliance for Choice in Education**: https://www.iowaace.org  
- **Alliance Defending Freedom** - Religious liberty  
- **First Liberty Institute** - Religious freedom  

---

## 🔥 BOTTOM LINE FOR Iowa CHRISTIANS

**2026 Elections Matter:**  
- U.S. Senate determines national pro-life firewall.  
- Governor affects ESA expansion and taxes.  
- AG impacts heartbeat law defenses.  
- Overall state direction at stake  

**If Conservatives Win:**  

✅ Pro-life protections maintained/strengthened  
✅ School choice expanded, parental rights protected  
✅ Religious liberty defended  
✅ Traditional family values upheld  
✅ Second Amendment rights secured  
✅ Election integrity ensured  
✅ Rural Iowa revitalized  
✅ Tax cuts for families  
✅ Border security funded  

**If Progressives Win:**  

❌ Abortion expansion, pro-life laws repealed  
❌ School choice gutted, CRT/gender ideology in schools  
❌ Religious liberty attacked  
❌ Family values eroded, parental rights stripped  
❌ Gun rights restricted  
❌ Election integrity weakened  
❌ Urban policies dominate rural  
❌ Tax hikes on workers  
❌ Open borders strain resources  

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**  

---

## 🙏 PRAYER POINTS

**Pray for:**  
- Ashley Hinson, Randy Feenstra, and their families  
- Iowa Governor/leadership  
- Conservative candidates in all races  
- Church mobilization and Christian voter turnout  
- Protection from voter fraud  
- Wisdom for Christian voters in Iowa  
- Revival and awakening in Iowa  
- God's will in Iowa elections  

**Scripture for Iowa Elections:**  

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*  

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*  

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*  

---  

**Last Updated:** October 2025  
**Source:** Christian Conservatives Today Election Coverage  
**Contact:** For questions or to contribute Iowa coverage, email contact@ekewaka.com  

**Iowa CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Iowa races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Iowa'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Iowa races...")
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

print(f"\nChecking for existing Iowa candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Iowa'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Iowa candidates...")
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

print("\nProcessing Iowa summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Iowa'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Iowa data upload complete!")