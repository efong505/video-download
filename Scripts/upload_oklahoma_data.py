import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Oklahoma Races
races = [
    {
        "state": "Oklahoma",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Republican Senator James Lankford seeks reelection in this solidly conservative state, facing Democratic challengers in a race critical for maintaining GOP control of the Senate."
    },
    {
        "state": "Oklahoma",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat due to term limits for incumbent Republican Kevin Stitt; a crowded Republican primary will determine the nominee in this red state, with implications for conservative policies on education and abortion."
    },
    {
        "state": "Oklahoma",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Republican Matt Pinnell is not seeking reelection; multiple Republicans vie for the nomination in a race influencing state leadership on family values and economic issues."
    },
    {
        "state": "Oklahoma",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat as incumbent Republican Gentner Drummond runs for governor; candidates will focus on law enforcement, religious liberty, and election integrity."
    },
    {
        "state": "Oklahoma",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Republican Kevin Hern seeks reelection in this safe GOP district covering eastern Oklahoma."
    },
    {
        "state": "Oklahoma",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Republican Josh Brecheen faces voters in this rural, conservative district."
    },
    {
        "state": "Oklahoma",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Longtime incumbent Republican Frank Lucas runs in this agricultural stronghold."
    },
    {
        "state": "Oklahoma",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Republican Tom Cole, a powerful committee chair, seeks another term."
    },
    {
        "state": "Oklahoma",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Republican Stephanie Bice represents the Oklahoma City area in this competitive but leaning GOP district."
    }
]

# Oklahoma Candidates  
candidates = [
    {
        "name": "James Lankford",
        "state": "Oklahoma",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "James Lankford, born in 1968 in Dallas, Texas, is an ordained Southern Baptist minister who dedicated over 20 years to youth ministry before entering politics. He served as Director of Student Ministry for the Baptist General Convention of Oklahoma for 15 years, focusing on faith-based leadership and community service. Elected to the U.S. House in 2010, Lankford quickly rose to prominence as a fiscal conservative and social values advocate. Appointed to the Senate in 2014 after Tom Coburn's retirement, he won full terms in 2016 and 2022. Married to Cindy, with three children, Lankford emphasizes family and faith in his public life. His accomplishments include leading efforts on government ethics, border security, and religious liberty protections. As a key GOP leader, he chairs subcommittees on intelligence and homeland security, authoring bills to combat human trafficking and enhance election integrity. Lankford's ministry background informs his commitment to biblical principles in governance, making him a steadfast voice for Christian conservatives.",
        "faith_statement": "As an ordained Southern Baptist minister, my faith in Jesus Christ guides every decision I make in public service. I believe government should protect religious liberty so believers can live out their convictions without fear.",
        "website": "https://www.lankford.senate.gov",
        "positions": {
            "ABORTION": "Pro-life: Supports national bans after 15 weeks, defunds Planned Parenthood, and has a 100% pro-life voting record, including backing the Born-Alive Abortion Survivors Protection Act.",
            "EDUCATION": "Strong supporter of school choice, including vouchers and charter schools; advocates for parental rights in curriculum decisions to counter CRT and gender ideology.",
            "RELIGIOUS-FREEDOM": "Champion of religious liberty; led Supreme Court case on legislative prayer and opposes mandates infringing on faith-based hiring and services.",
            "GUNS": "Firm 2nd Amendment defender; A+ NRA rating, opposes red-flag laws, and supports concealed carry reciprocity nationwide.",
            "TAXES": "Advocates permanent TCJA tax cuts, elimination of death tax, and balanced budgets to reduce federal overreach.",
            "IMMIGRATION": "Secure borders first; co-authored border security bills, supports wall funding, and ends catch-and-release policies.",
            "FAMILY-VALUES": "Upholds traditional marriage, opposes gender transition for minors, and promotes parental rights against state overreach in family matters.",
            "ELECTION-INTEGRITY": "Requires voter ID, paper ballots, and audits; led Senate investigations into 2020 irregularities."
        },
        "endorsements": ["Family Research Council", "National Right to Life", "NRA"]
    },
    {
        "name": "N'Kiyla Thomas",
        "state": "Oklahoma",
        "office": "U.S. Senate",
        "party": "Democratic",
        "bio": "N'Kiyla 'Jasmine' Thomas, a registered nurse and mother from Oklahoma, announced her candidacy for U.S. Senate in 2026, driven by personal experiences raising a child with autism and navigating healthcare challenges. Born and raised in Oklahoma, Thomas has worked as a frontline nurse, witnessing disparities in rural healthcare and education. Her campaign emphasizes people over politics, focusing on community-driven solutions for working families. With a background in advocacy for autism resources and rural access, she aims to fight corporate influence in Washington. Married with children, Thomas draws from her resilience as a single mother to champion equity and opportunity. Though new to elected office, her grassroots approach and nursing expertise position her as a fresh voice against entrenched power. She pledges to expand early intervention for disabilities and improve mental health services, reflecting her commitment to underserved Oklahomans.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.jasmineforok.com",
        "positions": {
            "ABORTION": "Pro-choice: Supports restoring Roe v. Wade protections, opposes state bans, and ensures access to reproductive healthcare without restrictions.",
            "EDUCATION": "Fully fund public schools, oppose vouchers that divert funds; emphasizes inclusive education for special needs and anti-discrimination policies.",
            "RELIGIOUS-FREEDOM": "Protects individual rights while ensuring separation of church and state; opposes using faith to discriminate in public services.",
            "GUNS": "Universal background checks and red-flag laws; supports responsible gun ownership but prioritizes ending gun violence.",
            "TAXES": "Raise taxes on wealthy corporations, close loopholes to fund social programs and infrastructure.",
            "IMMIGRATION": "Pathway to citizenship for Dreamers, comprehensive reform with humane border policies and asylum protections.",
            "FAMILY-VALUES": "Supports LGBTQ+ rights, gender-affirming care for minors with parental consent, and inclusive family policies.",
            "ELECTION-INTEGRITY": "Automatic voter registration, no voter ID barriers; focuses on accessibility over suppression."
        },
        "endorsements": ["Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "Gentner Drummond",
        "state": "Oklahoma",
        "office": "Governor",
        "party": "Republican",
        "bio": "Gentner Frederick Drummond, born October 1, 1963, in Pawhuska, Oklahoma, is a fifth-generation rancher, decorated Air Force fighter pilot, and current Attorney General. A Yale Law graduate, he served as an assistant district attorney, private attorney, and Osage County DA before his 2022 AG election. As AG, Drummond has aggressively enforced pro-life laws, defended religious liberties, and challenged federal overreach on borders. Married to Sally Ash, with three children, he credits his Catholic faith and family ranching heritage for his tough-on-crime stance. His military service includes flying F-15s, earning the Distinguished Flying Cross. Drummond's accomplishments include suing over opioid settlements and protecting Second Amendment rights. Announcing his 2026 gubernatorial bid in January 2025, he positions himself as a Trump ally focused on law and order, economic growth, and conservative values in the Sooner State.",
        "faith_statement": "As a Catholic, I am guided by my faith to protect the unborn, defend religious freedoms, and uphold justice for all Oklahomans.",
        "website": "https://drummondok.com",
        "positions": {
            "ABORTION": "Pro-life enforcer: Defended Oklahoma's near-total ban, sued providers violating heartbeat law, opposes exceptions beyond rape/incest/life of mother.",
            "EDUCATION": "Supports school choice and vouchers; backs parental rights bills banning CRT and transgender policies in schools.",
            "RELIGIOUS-FREEDOM": "Defended faith-based hiring rights in courts; opposes Biden's anti-discrimination mandates on religious groups.",
            "GUNS": "Strong 2A advocate; challenged ATF pistol brace rule, supports permitless carry expansion.",
            "TAXES": "Permanent income tax cut, eliminate state sales tax on groceries to ease family burdens.",
            "IMMIGRATION": "Secure borders, support Texas razor wire, end sanctuary policies in Oklahoma.",
            "FAMILY-VALUES": "Traditional marriage defender, opposes gender ideology in schools, promotes adoption over abortion.",
            "ELECTION-INTEGRITY": "Voter ID mandatory, audit elections, prosecute fraud aggressively."
        },
        "endorsements": ["Oklahoma FOP", "Oklahoma Farm Bureau", "National Federation of Independent Business"]
    },
    {
        "name": "Charles McCall",
        "state": "Oklahoma",
        "office": "Governor",
        "party": "Republican",
        "bio": "Charles Adelbert McCall III, born April 19, 1970, in Atoka, Oklahoma, is a fifth-generation Sooner, community banker, and former longest-serving House Speaker (2016-2024). A University of Oklahoma graduate with a law degree from Oklahoma City University, McCall entered politics in 2006, rising to lead the GOP supermajority. Married to Judy, with three children, he emphasizes faith, family, and freedom, rooted in his Baptist upbringing. As Speaker, he passed historic tax cuts, criminal justice reform, and pro-life measures. Announcing his gubernatorial run in February 2025, McCall pledges to combat 'woke' policies and boost rural economies. His banking career at First National Bank focused on small business lending, reflecting his commitment to opportunity. McCall's leadership style blends fiscal conservatism with compassionate governance, making him a formidable contender in the open race.",
        "faith_statement": "My Baptist faith teaches that righteousness exalts a nation; I will govern with biblical principles to protect life and liberty.",
        "website": "https://mccallforoklahoma.com",
        "positions": {
            "ABORTION": "Pro-life: Authored bills strengthening bans, defunding abortion providers, no exceptions for rape/incest.",
            "EDUCATION": "Expanded school choice via ESA program; bans on gender transitions and DEI in public schools.",
            "RELIGIOUS-FREEDOM": "Sponsored protections for faith-based adoption agencies; opposes federal mandates on contraception.",
            "GUNS": "Permitless carry author; NRA-endorsed, fights federal gun control.",
            "TAXES": "Largest tax cut in state history as Speaker; aims for zero income tax long-term.",
            "IMMIGRATION": "E-Verify for employers, end benefits for illegals, support border wall.",
            "FAMILY-VALUES": "Traditional family promotion, parental consent for abortions, anti-LGBTQ curriculum influence.",
            "ELECTION-INTEGRITY": "Voter ID, same-day registration limits, election audits required."
        },
        "endorsements": ["Oklahoma Chamber of Commerce", "Oklahoma Farm Bureau", "Americans for Prosperity"]
    },
    {
        "name": "Cyndi Munson",
        "state": "Oklahoma",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Cyndi Munson, born May 24, 1985, in Oklahoma City, is the daughter of a Vietnam War veteran and South Korean immigrant, making her the first Asian-American woman elected to the Oklahoma Legislature in 2014. A Master's holder in leadership from the University of Nebraska, she worked in non-profits and as a community organizer before serving as House Democratic Leader since 2021. Married with children, Munson overcame personal challenges to advocate for working families. Her accomplishments include expanding Medicaid access and protecting voting rights. Launching her 2026 gubernatorial bid in April 2025 as the first Democrat, she focuses on education funding, reproductive rights, and economic equity. As a bridge-builder in a red state, Munson emphasizes inclusive policies for rural and urban Oklahomans alike.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.cyndimunson.com",
        "positions": {
            "ABORTION": "Pro-choice: Seeks to repeal trigger ban, restore access up to viability, protect providers from harassment.",
            "EDUCATION": "Increase teacher pay, fully fund public schools, oppose vouchers that starve public education.",
            "RELIGIOUS-FREEDOM": "Balances rights; opposes using religion to deny services like contraception or same-sex marriage.",
            "GUNS": "Background checks, assault weapon bans, close gun show loopholes to reduce violence.",
            "TAXES": "Progressive taxation, raise on high earners to fund education and healthcare.",
            "IMMIGRATION": "Protect DACA, expand work visas, humane asylum processing.",
            "FAMILY-VALUES": "Inclusive families, supports adoption equality, gender-affirming care access.",
            "ELECTION-INTEGRITY": "Expand voting access, end gerrymandering, no photo ID requirements."
        },
        "endorsements": ["Planned Parenthood", "Oklahoma Education Association", "Everytown"]
    },
    {
        "name": "Brian Hill",
        "state": "Oklahoma",
        "office": "Lieutenant Governor",
        "party": "Republican",
        "bio": "Brian Hill, a Fairview rancher and state Representative since 2018, announced his 2026 Lt. Gov bid in September 2025. A University of Oklahoma agriculture graduate, Hill manages a family cattle operation and serves on the House Agriculture Committee. Married to Kara with three children, his faith-driven life emphasizes rural values and conservative principles. As a legislator, he championed tax cuts and pro-life bills. Hill's campaign focuses on economic development and family protections in rural Oklahoma.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life: Supports total bans, no exceptions.",
            "EDUCATION": "School choice advocate, parental rights.",
            "RELIGIOUS-FREEDOM": "Protects faith-based institutions.",
            "GUNS": "2A supporter.",
            "TAXES": "Cut taxes for families.",
            "IMMIGRATION": "Secure borders.",
            "FAMILY-VALUES": "Traditional marriage.",
            "ELECTION-INTEGRITY": "Voter ID."
        },
        "endorsements": ["Oklahoma Farm Bureau"]
    },
    {
        "name": "J.J. Humphrey",
        "state": "Oklahoma",
        "office": "Lieutenant Governor",
        "party": "Republican",
        "bio": "State Rep. J.J. Humphrey, a Lane pastor and businessman, entered the Lt. Gov race in July 2025. Elected in 2012, he focuses on Second Amendment rights and rural issues. Married with children, Humphrey's pastoral background informs his faith-based conservatism.",
        "faith_statement": "As a pastor, I lead with biblical truth to defend life and liberty.",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life absolutist.",
            "EDUCATION": "School choice, anti-CRT.",
            "RELIGIOUS-FREEDOM": "Strong defender.",
            "GUNS": "NRA-backed.",
            "TAXES": "Reduce government spending.",
            "IMMIGRATION": "Enforce laws.",
            "FAMILY-VALUES": "Biblical family.",
            "ELECTION-INTEGRITY": "Secure voting."
        },
        "endorsements": ["NRA"]
    },
    {
        "name": "Kelly Forbes",
        "state": "Oklahoma",
        "office": "Lieutenant Governor",
        "party": "Democrat",
        "bio": "Kelly Forbes, an Oklahoma City attorney and community leader, is the Democratic candidate for Lt. Gov. With a focus on women's rights and education, she brings legal expertise to advocate for equality.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Public school funding.",
            "RELIGIOUS-FREEDOM": "Separation of church and state.",
            "GUNS": "Reasonable controls.",
            "TAXES": "Fair taxation.",
            "IMMIGRATION": "Reform.",
            "FAMILY-VALUES": "Inclusive.",
            "ELECTION-INTEGRITY": "Accessible voting."
        },
        "endorsements": ["Oklahoma Democrats"]
    },
    {
        "name": "Jon Echols",
        "state": "Oklahoma",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "Former House Rep. Jon Echols, a fifth-generation Oklahoman and attorney, announced for AG in February 2025. Served 2010-2022, focusing on budget and energy. Married with family, conservative leader.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Choice.",
            "RELIGIOUS-FREEDOM": "Defender.",
            "GUNS": "2A.",
            "TAXES": "Cuts.",
            "IMMIGRATION": "Security.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "ID."
        },
        "endorsements": ["Oklahoma GOP"]
    },
    {
        "name": "Jeff Starling",
        "state": "Oklahoma",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "Energy Secretary Jeff Starling, a litigator, announced in October 2025. Private sector background, national experience.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Parental rights.",
            "RELIGIOUS-FREEDOM": "Protect.",
            "GUNS": "Support.",
            "TAXES": "Lower.",
            "IMMIGRATION": "Border.",
            "FAMILY-VALUES": "Values.",
            "ELECTION-INTEGRITY": "Secure."
        },
        "endorsements": ["Energy industry"]
    },
    {
        "name": "Nick Coffey",
        "state": "Oklahoma",
        "office": "Attorney General",
        "party": "Democrat",
        "bio": "Former federal prosecutor Nick Coffey launched in October 2025, emphasizing justice reform and consumer protection.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Public funding.",
            "RELIGIOUS-FREEDOM": "Balanced.",
            "GUNS": "Controls.",
            "TAXES": "Progressive.",
            "IMMIGRATION": "Reform.",
            "FAMILY-VALUES": "Inclusive.",
            "ELECTION-INTEGRITY": "Access."
        },
        "endorsements": ["Oklahoma Trial Lawyers"]
    }
]

# Oklahoma Summary
summary = {
    "state": "Oklahoma",
    "title": "Oklahoma 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Oklahoma 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 9
**Total Candidates Profiled:** 12
**Election Dates:**
- 2026-06-16 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Oklahoma POLITICAL LANDSCAPE

### **The Sooner State**

Oklahoma is a **deep-red stronghold**:
- **Bible Belt Heartland:** Home to the highest percentage of evangelicals in the U.S. (Pew Research), with over 70% identifying as Christian; churches drive conservative mobilization.
- **Energy & Agriculture Powerhouse:** Oil, gas, and farming fuel the economy, fostering rugged individualism and limited government ethos.
- **Urban-Rural Divide:** Oklahoma City and Tulsa lean purple with diverse populations, while rural counties like those in the Panhandle are 80%+ Republican strongholds.
- **Native American Influence:** 39 tribes add cultural depth, but conservative values dominate state politics.

### **Why Oklahoma Matters**

Oklahoma is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Strictest abortion laws in nation post-Dobbs; near-total ban enforced, but threats from ballot initiatives loom.
- ✅ **Second Amendment:** Permitless carry since 2019; top-ranked gun rights state by NRA.
- ✅ **School Choice:** Universal ESA program launched 2024, empowering parental rights amid Walters' Bible-in-schools push.
- ✅ **Religious Liberty:** Strong state RFRA; AG defended faith-based hiring against federal mandates.
- ✅ **Family Values:** Bans on gender-affirming care for minors; traditional marriage enshrined.
- ✅ **Election Integrity:** Voter ID required; paper ballots and audits standard.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** Retaining this seat ensures GOP Senate majority; Lankford's conservative record on life and liberty is vital against national progressive tides.

**James Lankford (Republican)** - Incumbent U.S. Senator

**Faith Statement:** "As an ordained Southern Baptist minister, my faith in Jesus Christ guides every decision I make in public service. I believe government should protect religious liberty so believers can live out their convictions without fear."

**Background:**
- Ordained minister with 20+ years in youth ministry.
- Elected to House 2010, Senate 2014; family man with three children.
- Led anti-trafficking and border security efforts.

**Christian Conservative Analysis:**
- **Pro-Life:** 100% rating; sponsored Born-Alive Act.
- **Religious Liberty:** Won Supreme Court case on prayer.
- **Education/Parental Rights:** School choice champion.
- **Family Values:** Opposes gender ideology.
- **Overall Assessment:** 9/10 - Exemplary biblical alignment, minor immigration compromises.

**Key Positions:**
- **ABORTION:** National 15-week ban, defund Planned Parenthood.
- **EDUCATION:** Vouchers, ban CRT.
- **RELIGIOUS FREEDOM:** Protect faith hiring.
- **GUNS:** A+ NRA, reciprocity.
- **TAXES:** Permanent cuts.
- **Oil & Gas:** Deregulate energy.

**Endorsements:** Family Research Council, NRA, National Right to Life

**Website:** https://www.lankford.senate.gov

**N'Kiyla Thomas (Democrat)** - Nurse & Advocate

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Frontline nurse, mother of autistic child.
- Grassroots activist for healthcare equity.
- First-time candidate challenging GOP dominance.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports expansion.
- **Religious Liberty:** Favors separation.
- **Education/Parental Rights:** Public funding focus.
- **Family Values:** Inclusive policies.
- **Overall Assessment:** 2/10 - Clashes with biblical values on life and family.

**Key Positions:**
- **ABORTION:** Restore Roe.
- **EDUCATION:** Anti-voucher.
- **RELIGIOUS FREEDOM:** No discrimination via faith.
- **GUNS:** Background checks.
- **TAXES:** Tax the rich.
- **Healthcare Access:** Expand Medicaid.

**Endorsements:** Planned Parenthood, Everytown

**Website:** https://www.jasmineforok.com

**Why It Matters:** Senate control hinges on defending Lankford's pro-life firewall.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** Open seat amplifies stakes for advancing Stitt's legacy on choice and life amid primary chaos.

**Gentner Drummond (Republican)** - Attorney General

**Faith Statement:** "As a Catholic, I am guided by my faith to protect the unborn, defend religious freedoms, and uphold justice for all Oklahomans."

**Background:**
- Yale Law grad, F-15 pilot, rancher.
- Enforced abortion bans as AG.
- Trump ally, family of three.

**Christian Conservative Analysis:**
- **Pro-Life:** Sued violators of heartbeat law.
- **Religious Liberty:** Defended church hiring.
- **Education/Parental Rights:** Backed Walters' reforms.
- **Family Values:** Anti-gender care.
- **Overall Assessment:** 8/10 - Strong enforcer, occasional pragmatism.

**Key Positions:**
- **ABORTION:** Enforce total ban.
- **EDUCATION:** Vouchers expansion.
- **RELIGIOUS FREEDOM:** RFRA enforcer.
- **GUNS:** Permitless carry.
- **TAXES:** Grocery tax repeal.
- **Energy Deregulation:** Boost production.

**Endorsements:** Oklahoma FOP, Farm Bureau

**Website:** https://drummondok.com

**Charles McCall (Republican)** - Former House Speaker

**Faith Statement:** "My Baptist faith teaches that righteousness exalts a nation; I will govern with biblical principles to protect life and liberty."

**Background:**
- Banker, fifth-gen Oklahoman.
- Passed tax cuts, pro-life laws.
- Father of three, rural roots.

**Christian Conservative Analysis:**
- **Pro-Life:** No-rape exceptions.
- **Religious Liberty:** Adoption protections.
- **Education/Parental Rights:** ESA author.
- **Family Values:** Anti-DEI.
- **Overall Assessment:** 9/10 - Fiscal hawk with faith core.

**Key Positions:**
- **ABORTION:** Strengthen bans.
- **EDUCATION:** Ban transgender policies.
- **RELIGIOUS FREEDOM:** Oppose mandates.
- **GUNS:** NRA hero.
- **TAXES:** Zero income tax goal.
- **Rural Development:** Ag incentives.

**Endorsements:** Chamber of Commerce, AFP

**Website:** https://mccallforoklahoma.com

**Cyndi Munson (Democrat)** - House Democratic Leader

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Asian-American trailblazer, organizer.
- Expanded Medicaid fights.
- Veteran & immigrant daughter.

**Christian Conservative Analysis:**
- **Pro-Life:** Expansion advocate.
- **Religious Liberty:** Separation emphasis.
- **Education/Parental Rights:** Teacher unions.
- **Family Values:** LGBTQ support.
- **Overall Assessment:** 1/10 - Progressive threat to values.

**Key Positions:**
- **ABORTION:** Repeal bans.
- **EDUCATION:** Fund publics only.
- **RELIGIOUS FREEDOM:** Anti-discrimination.
- **GUNS:** Assault bans.
- **TAXES:** Wealth tax.
- **Healthcare:** Universal access.

**Endorsements:** OEA, Planned Parenthood

**Website:** https://www.cyndimunson.com

**Why It Matters:** Governor sets pro-life enforcement tone for decade.

### **Lieutenant Governor** - 2026-11-03

**Context:** Influences education policy; conservative win bolsters Walters' Bible curriculum.

**Brian Hill (Republican)** - State Rep.

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Rancher, ag committee member.
- Tax cut champion.
- Family-focused conservative.

**Christian Conservative Analysis:**
- **Pro-Life:** Solid record.
- **Religious Liberty:** Supporter.
- **Education/Parental Rights:** Choice backer.
- **Family Values:** Traditional.
- **Overall Assessment:** 7/10 - Reliable rural voice.

**Key Positions:**
- **ABORTION:** Bans.
- **EDUCATION:** Vouchers.
- **RELIGIOUS FREEDOM:** Protect.
- **GUNS:** 2A.
- **TAXES:** Cuts.
- **Ag Policy:** Farm aid.

**Endorsements:** Farm Bureau

**Website:** ""

**J.J. Humphrey (Republican)** - State Rep. & Pastor

**Faith Statement:** "As a pastor, I lead with biblical truth to defend life and liberty."

**Background:**
- Lane pastor, gun rights advocate.
- Rural business owner.
- Faith leader.

**Christian Conservative Analysis:**
- **Pro-Life:** Absolutist.
- **Religious Liberty:** Strong.
- **Education/Parental Rights:** Anti-woke.
- **Family Values:** Biblical.
- **Overall Assessment:** 8/10 - Pastoral authenticity.

**Key Positions:**
- **ABORTION:** Total ban.
- **EDUCATION:** Parental control.
- **RELIGIOUS FREEDOM:** Defender.
- **GUNS:** Permitless.
- **TAXES:** Low.
- **Rural Health:** Access.

**Endorsements:** NRA

**Website:** ""

**Kelly Forbes (Democrat)** - Attorney

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- OKC lawyer, women's rights.
- Community organizer.
- Equity fighter.

**Christian Conservative Analysis:**
- **Pro-Life:** Opposed.
- **Religious Liberty:** Limited.
- **Education/Parental Rights:** Union ally.
- **Family Values:** Progressive.
- **Overall Assessment:** 2/10 - Values clash.

**Key Positions:**
- **ABORTION:** Access.
- **EDUCATION:** Public fund.
- **RELIGIOUS FREEDOM:** Balanced.
- **GUNS:** Controls.
- **TAXES:** Fair.
- **Equality:** DEI.

**Endorsements:** OK Democrats

**Website:** ""

**Why It Matters:** Lt. Gov. tie-breaker on faith-based bills.

### **Attorney General** - 2026-11-03

**Context:** Successor to Drummond must safeguard pro-life, 2A in courts.

**Jon Echols (Republican)** - Former Rep.

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Attorney, House leader.
- Budget expert.
- Family man.

**Christian Conservative Analysis:**
- **Pro-Life:** Voter.
- **Religious Liberty:** Backer.
- **Education/Parental Rights:** Choice.
- **Family Values:** Conservative.
- **Overall Assessment:** 7/10 - Policy wonk.

**Key Positions:**
- **ABORTION:** Enforce.
- **EDUCATION:** Rights.
- **RELIGIOUS FREEDOM:** Defend.
- **GUNS:** Support.
- **TAXES:** Cut.
- **Energy:** Pro-fossil.

**Endorsements:** OK GOP

**Website:** ""

**Jeff Starling (Republican)** - Energy Sec.

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Litigator, private sector.
- National experience.
- Business focus.

**Christian Conservative Analysis:**
- **Pro-Life:** Aligned.
- **Religious Liberty:** Protect.
- **Education/Parental Rights:** Support.
- **Family Values:** Traditional.
- **Overall Assessment:** 6/10 - Energy emphasis.

**Key Positions:**
- **ABORTION:** Ban.
- **EDUCATION:** Choice.
- **RELIGIOUS FREEDOM:** Yes.
- **GUNS:** Yes.
- **TAXES:** Lower.
- **Litigation:** Tough.

**Endorsements:** Energy groups

**Website:** ""

**Nick Coffey (Democrat)** - Ex-Prosecutor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Federal prosecutor.
- Justice reform.
- First D candidate.

**Christian Conservative Analysis:**
- **Pro-Life:** No.
- **Religious Liberty:** Limited.
- **Education/Parental Rights:** Public.
- **Family Values:** Inclusive.
- **Overall Assessment:** 1/10 - Reformist threat.

**Key Positions:**
- **ABORTION:** Choice.
- **EDUCATION:** Fund.
- **RELIGIOUS FREEDOM:** Separation.
- **GUNS:** Checks.
- **TAXES:** Progressive.
- **Criminal Justice:** Reform.

**Endorsements:** Trial Lawyers

**Website:** ""

**Why It Matters:** AG defends faith in lawsuits.

---

## 🎯 KEY ISSUES FOR Oklahoma CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Near-total abortion ban since 2022; only life-saving exceptions.
- 200+ pregnancy centers via SoonerLife.
- Parental consent for minors' abortions.
- No state funding for Planned Parenthood.
- Victory: Blocked expansion efforts in 2024.

**Progressive Position:**
- Ballot push for repeal via initiative.
- Federal funding battles.
- Provider harassment suits.

**Christian Conservative Action:**
- Join Oklahoma Right to Life.
- Support HB 1690 enforcement.
- Volunteer at crisis centers.
- Vote pro-life in primaries.

### **School Choice & Parental Rights**

**Conservative Position:**
- Universal ESA for 2024-25, $7,500 vouchers.
- Parental Bill of Rights (2023).
- Bans on CRT, gender ideology (2022).
- Homeschool freedom top-ranked.
- Walters' Bible mandate win.

**Progressive Position:**
- Union opposition to choice.
- DEI in Tulsa schools.
- Threats to voucher constitutionality.

**Christian Conservative Action:**
- Run for local boards.
- Back SB 1 funding.
- Join Parents' Rights in Education.
- Oppose ACLU suits.

### **Religious Freedom**

**Conservative Position:**
- State RFRA (2000) stronger than federal.
- Defended Bible curriculum.
- Faith adoption exemptions.
- Prayer in schools protected.
- 2025 AG win on hiring.

**Progressive Position:**
- Lawsuits against Bible mandate.
- Anti-discrimination on gender/sexuality.
- Federal Title IX threats.

**Christian Conservative Action:**
- Support First Liberty cases.
- Lobby for expansions.
- Church forums on liberty.
- Vote RFRA defenders.

### **Guns**

**Conservative Position:**
- Permitless carry (2019), no training needed.
- Constitutional carry for 21+.
- Preemption over local bans.
- Stand Your Ground.
- A+ gun rights state.

**Progressive Position:**
- OKC red-flag pushes.
- Assault weapon calls post-Uvalde.
- Federal ATF challenges.

**Christian Conservative Action:**
- NRA membership.
- Oppose H.R.8.
- Train church security.
- Vote 2A candidates.

### **Taxes**

**Conservative Position:**
- Largest cut 2023 ($800M).
- Groceries sales tax 0% goal.
- Corporate incentives.
- No income tax hike.
- Surplus to rebates.

**Progressive Position:**
- Raise on oil for schools.
- Wealth tax proposals.
- Close 'loopholes'.

**Christian Conservative Action:**
- Support AFP.
- Contact on HB 1935.
- Tithe wisely, vote cuts.
- Promote prosperity gospel economics.

### **Immigration**

**Conservative Position:**
- E-Verify mandatory 2022.
- No sanctuary cities.
- AG sued Biden on borders.
- Razor wire support.
- Local law enforcement aid.

**Progressive Position:**
- DACA protections in OKC.
- Work visas expansion.
- Humane reform calls.

**Christian Conservative Action:**
- Border prayer vigils.
- Support FAIR.
- Report illegals.
- Vote secure candidates.

### **Family Values**

**Conservative Position:**
- Minors gender care ban (2023).
- Traditional marriage amendment.
- Anti-porn in libraries.
- Adoption preference for straights? No, faith-based.
- Covenant marriage option.

**Progressive Position:**
- Trans rights in Tulsa.
- Same-sex adoption push.
- Drag story hours.

**Christian Conservative Action:**
- Family Policy Council.
- Oppose EQ ADV.
- Home school co-ops.
- Biblical parenting classes.

### **Election Integrity**

**Conservative Position:**
- Voter ID since 2016.
- Paper ballots, audits.
- No mail drop boxes.
- Felon wait full sentence.
- 2024 clean sweeps.

**Progressive Position:**
- Auto registration bills.
- End ID barriers.
- Count every vote mantra.

**Christian Conservative Action:**
- Poll watcher training.
- iVoterGuide use.
- Prayer for honest counts.
- Support EAC reforms.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- **2026-04-10** - Voter registration deadline
- **2026-06-06** - Early voting begins
- **2026-06-16** - Primary Election
- **2026-11-03** - General Election

**Voter Registration:** https://oklahoma.gov/elections/voter-registration.html

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
✅ **Share on social media** with #OklahomaFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Oklahoma CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Oklahoma coverage
- **Oklahoma Right to Life** - Pro-life ratings
- **Family Policy Alliance of Oklahoma** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Oklahoma Secretary of State**: https://oklahoma.gov/elections.html
- **County Election Offices**: Find via state site
- **Early Voting Locations**: County election boards

### **Conservative Organizations:**
- **Oklahoma Right to Life**: https://www.okrtl.org
- **Family Policy Alliance of Oklahoma**: https://fpaok.org
- **Oklahoma Second Amendment Association**: https://www.osaacarry.org
- **Oklahoma School Choice Coalition**: https://oklahomaschoolchoice.org
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Oklahoma CHRISTIANS

**2026 Elections Matter:**
- Governor race determines abortion enforcement.
- Senate affects national pro-life bills.
- Lt. Gov. shapes school Bible policy.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Energy boom sustained
✅ Rural faith communities empowered
✅ Tax relief for families

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Energy regulations choke farms
❌ Tax hikes burden churches
❌ Woke mandates in classrooms

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- James Lankford, Gentner Drummond, Charles McCall and their families
- Oklahoma Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Oklahoma
- Revival and awakening in Oklahoma
- God's will in Oklahoma elections

**Scripture for Oklahoma Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Oklahoma coverage, email contact@ekewaka.com

**Oklahoma CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Oklahoma races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Oklahoma'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Oklahoma races...")
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

print(f"\nChecking for existing Oklahoma candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Oklahoma'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Oklahoma candidates...")
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

print("\nProcessing Oklahoma summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Oklahoma'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Oklahoma data upload complete!")