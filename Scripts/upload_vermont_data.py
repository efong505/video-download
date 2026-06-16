import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Vermont Races
races = [
    {
        "state": "Vermont",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The gubernatorial race will determine leadership in a predominantly Democratic state, with implications for moderate policies on taxes, environment, and social issues."
    },
    {
        "state": "Vermont",
        "office": "U.S. House of Representatives (At-Large)",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Vermont's single congressional district race impacts federal representation on key issues like healthcare, climate, and reproductive rights."
    },
    {
        "state": "Vermont",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "This role presides over the state Senate and can influence legislative priorities, especially in a divided chamber."
    },
    {
        "state": "Vermont",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Oversees elections and business registrations, critical for election integrity and economic development."
    },
    {
        "state": "Vermont",
        "office": "State Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Manages state finances, investments, and unclaimed property, affecting fiscal policy and taxpayer funds."
    },
    {
        "state": "Vermont",
        "office": "Auditor of Accounts",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Conducts audits of state agencies, ensuring accountability in government spending."
    },
    {
        "state": "Vermont",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Enforces state laws, protects consumers, and litigates on behalf of the state."
    },
    {
        "state": "Vermont",
        "office": "Burlington City Council (Ward 2)",
        "election_date": "2025-03-04",
        "race_type": "general",
        "description": "Key municipal race in Vermont's largest city, influencing local policies on housing and public safety."
    }
]

# Vermont Candidates  
candidates = [
    {
        "name": "Phil Scott",
        "state": "Vermont",
        "office": "Governor",
        "party": "Republican",
        "bio": "Phil Scott, born August 4, 1958, in Barre, Vermont, is a businessman, stock car racer, and politician serving as the 82nd Governor since 2017. Raised in a working-class family, Scott graduated from Vermont Technical College with a degree in automotive technology. He owned a construction business and raced stock cars for over 30 years, winning multiple championships. Married to Diana Scott, they have two daughters and reside in Berlin, Vermont. Before governorship, he served as Lieutenant Governor (2011-2017) and in the Vermont Senate (2001-2011), focusing on transportation and economic development. As governor, Scott has balanced budgets, invested in infrastructure, and navigated Vermont's progressive legislature with vetoes on tax hikes and gun control measures, earning high approval ratings in a blue state.",
        "faith_statement": "As an Episcopalian, Governor Scott has stated, 'My faith guides me to serve with compassion and integrity, emphasizing community and stewardship of God's creation.'",
        "website": "https://governor.vermont.gov",
        "positions": {
            "ABORTION": "Pro-choice with limits; supports reproductive rights enshrined in the state constitution but vetoed extreme expansions.",
            "EDUCATION": "Supports school choice through town tuitioning program but opposes vouchers for religious schools; emphasizes local control and parental involvement.",
            "RELIGIOUS-FREEDOM": "Strong supporter of religious liberty, signing protections for faith-based organizations while balancing LGBTQ+ rights.",
            "GUNS": "Moderate 2nd Amendment advocate; vetoed assault weapons ban but signed universal background checks.",
            "TAXES": "Opposes broad tax increases; vetoed carbon tax and property tax hikes to protect working families.",
            "IMMIGRATION": "Supports humane border security and pathways to citizenship; focuses on integrating immigrants into Vermont's workforce.",
            "FAMILY-VALUES": "Supports traditional family structures but inclusive of modern families; promotes parental rights in education.",
            "ELECTION-INTEGRITY": "Backs voter ID and secure elections; reformed absentee ballot processes for transparency."
        },
        "endorsements": ["Vermont Chamber of Commerce", "National Federation of Independent Business", "Gun Owners of Vermont"]
    },
    {
        "name": "Esther Charlestin",
        "state": "Vermont",
        "office": "Governor",
        "party": "Democratic",
        "bio": "Esther Charlestin is a community organizer and former nonprofit leader challenging for governor. Born in Haiti and immigrating young, she earned a degree in social work from the University of Vermont. With over 20 years in advocacy, she directed Vermont's Haitian-American Community Alliance and worked on housing equity. Married with three children, she resides in Winooski. Her career highlights include leading anti-poverty initiatives and serving on local school boards, focusing on equity and justice.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.estherforvermont.com",
        "positions": {
            "ABORTION": "Strong pro-choice advocate; supports full access to reproductive healthcare without restrictions.",
            "EDUCATION": "Opposes school choice vouchers; prioritizes public school funding and equity programs.",
            "RELIGIOUS-FREEDOM": "Supports separation of church and state; prioritizes LGBTQ+ protections over religious exemptions.",
            "GUNS": "Favors strict gun control, including bans on assault weapons and red-flag laws.",
            "TAXES": "Supports progressive taxation to fund social services; backs carbon tax for climate action.",
            "IMMIGRATION": "Advocates for sanctuary policies and expanded immigrant rights.",
            "FAMILY-VALUES": "Emphasizes inclusive family policies, including gender-affirming care for youth.",
            "ELECTION-INTEGRITY": "Opposes voter ID; supports expanded mail-in voting."
        },
        "endorsements": ["Vermont AFL-CIO", "Planned Parenthood Vermont", "Vermont NEA"]
    },
    {
        "name": "Becca Balint",
        "state": "Vermont",
        "office": "U.S. House of Representatives (At-Large)",
        "party": "Democratic",
        "bio": "Becca Balint, born in 1968, is a former Vermont State Senator and educator serving as U.S. Representative since 2023. Raised in a Jewish family, she holds a master's in history from the University of Massachusetts. A high school teacher for 25 years, she advocated for LGBTQ+ rights and mental health. Married to Rachel, with two children, she lives in Brattleboro. As Senate President Pro Tempore, she championed climate action and healthcare expansion.",
        "faith_statement": "Balint, identifying as Jewish, has said, 'My spirituality informs my commitment to justice and compassion in public service.' No explicit Christian faith statement.",
        "website": "https://balint.house.gov",
        "positions": {
            "ABORTION": "Fierce defender of reproductive rights; co-sponsored bills to codify Roe v. Wade nationally.",
            "EDUCATION": "Prioritizes public education funding; opposes private school vouchers.",
            "RELIGIOUS-FREEDOM": "Supports broad religious freedoms but prioritizes anti-discrimination laws.",
            "GUNS": "Strong gun safety advocate; backs universal background checks and assault weapon bans.",
            "TAXES": "Supports raising taxes on wealthy to fund social programs.",
            "IMMIGRATION": "Advocates for comprehensive reform with paths to citizenship.",
            "FAMILY-VALUES": "Supports LGBTQ+ families and gender-affirming care.",
            "ELECTION-INTEGRITY": "Focuses on expanding access; opposes restrictive voting laws."
        },
        "endorsements": ["EMILY's List", "Sierra Club", "Everytown for Gun Safety"]
    },
    {
        "name": "Mark Coester",
        "state": "Vermont",
        "office": "U.S. House of Representatives (At-Large)",
        "party": "Republican",
        "bio": "Mark Coester is a businessman and Air Force veteran running for Congress. Born in Vermont, he served 20 years in the military, retiring as a colonel. He owns a manufacturing firm in Essex Junction and has led local chambers. Married with four children, he emphasizes economic growth and veterans' issues.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://markcoester.com",
        "positions": {
            "ABORTION": "Pro-life; supports restrictions after viability and defunding Planned Parenthood.",
            "EDUCATION": "Strong school choice proponent; backs vouchers and parental rights in curriculum.",
            "RELIGIOUS-FREEDOM": "Defends religious liberties against government overreach.",
            "GUNS": "Staunch 2nd Amendment defender; opposes new restrictions.",
            "TAXES": "Advocates for tax cuts and deregulation to boost economy.",
            "IMMIGRATION": "Supports secure borders and merit-based immigration.",
            "FAMILY-VALUES": "Upholds traditional marriage and opposes gender ideology in schools.",
            "ELECTION-INTEGRITY": "Backs voter ID and paper ballots for secure elections."
        },
        "endorsements": ["Vermont Republican Party", "U.S. Chamber of Commerce", "NRA"]
    },
    {
        "name": "John Rodgers",
        "state": "Vermont",
        "office": "Lieutenant Governor",
        "party": "Republican",
        "bio": "John Rodgers, born in 1960, is a dairy farmer and former state representative serving as Lieutenant Governor since 2025. Raised on a family farm in Albany, he graduated from Vermont Technical College. With 40 years in agriculture, he leads Rodgers Hollow Farm, producing milk and maple syrup. Married to Susan, with two sons, he lives in Irasburg. Elected to the House in 2016, he focused on rural broadband and farming subsidies.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://ltgov.vermont.gov",
        "positions": {
            "ABORTION": "Moderate; supports some restrictions but respects state law.",
            "EDUCATION": "Supports rural school consolidation and vocational training.",
            "RELIGIOUS-FREEDOM": "Backs protections for faith-based farms and communities.",
            "GUNS": "Strong supporter of hunting rights and concealed carry.",
            "TAXES": "Opposes farm tax increases; favors property tax relief.",
            "IMMIGRATION": "Supports legal immigration for agricultural workers.",
            "FAMILY-VALUES": "Emphasizes family farms and traditional rural values.",
            "ELECTION-INTEGRITY": "Advocates for transparent voting processes."
        },
        "endorsements": ["Vermont Farm Bureau", "Northeast Kingdom Republicans", "Dairy Farmers of Vermont"]
    },
    {
        "name": "Sarah Copeland Hanzas",
        "state": "Vermont",
        "office": "Secretary of State",
        "party": "Democratic",
        "bio": "Sarah Copeland Hanzas, born in 1978, is an attorney and former legislator serving as Secretary of State since 2023. Raised in Corinth, she earned a law degree from Northeastern University. She practiced environmental law and served eight years in the House, chairing the Judiciary Committee. Married with two children, she lives in Norwich. Key accomplishments include election reforms and consumer protections.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://sos.vermont.gov",
        "positions": {
            "ABORTION": "Pro-choice; defended reproductive rights legislation.",
            "EDUCATION": "Supports public education equity and teacher pay raises.",
            "RELIGIOUS-FREEDOM": "Balances with anti-discrimination; supports secular governance.",
            "GUNS": "Favors background checks and storage laws.",
            "TAXES": "Backs fair share taxation for infrastructure.",
            "IMMIGRATION": "Supports inclusive policies for refugees.",
            "FAMILY-VALUES": "Promotes paid family leave and child care access.",
            "ELECTION-INTEGRITY": "Modernized voting access while ensuring security."
        },
        "endorsements": ["Vermont Democratic Party", "League of Women Voters", "ACLU of Vermont"]
    }
]

# Vermont Summary
summary = {
    "state": "Vermont",
    "title": "Vermont 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Vermont 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 8
**Total Candidates Profiled:** 6
**Election Dates:**
- 2025-03-04 (Municipal/Town Meeting)
- 2026-08-11 (Primaries)
- 2026-11-03 (General Election)

---

## 🔴 Vermont POLITICAL LANDSCAPE

### **The Green Mountain State**

Vermont is a **deeply progressive stronghold**:
- **Legislature:** Democrats and Progressives hold supermajorities in both chambers, pushing expansive social welfare and environmental agendas.
- **Electoral History:** No Republican presidential win since 1988; U.S. House seat Democratic since 2007.
- **Urban-Rural Divide:** Progressive strongholds in Burlington (Chittenden County) and Montpelier contrast with conservative-leaning Northeast Kingdom counties like Essex and Orleans.
- **Unique State Factor:** Town Meeting Day democracy fosters grassroots activism, but low population (650,000) amplifies progressive voices.

### **Why Vermont Matters**

Vermont is **CHALLENGING** for Christian conservatives:
- ✅ **Pro-Life Leadership:** State constitution protects abortion up to birth (Article 22); no restrictions, defying national trends.
- ✅ **Second Amendment:** Strong gun culture in rural areas, but legislature passed assault weapons ban in 2018 (vetoed by Gov. Scott).
- ✅ **School Choice:** Town tuitioning allows public funds to private/religious schools, but recent laws (Act 73, 2025) restrict religious school funding.
- ✅ **Religious Liberty:** Constitution guarantees free exercise (Article 3), but threats from LGBTQ+ mandates and school policies.
- ✅ **Family Values:** Same-sex marriage since 2009; gender ideology in schools without parental opt-outs.
- ✅ **Election Integrity:** Same-day registration aids access but raises fraud concerns among conservatives.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** This race shapes Vermont's moderate vs. progressive divide, impacting veto power on tax hikes, gun laws, and social policies critical to Christian families.

**Phil Scott (Republican)** - Incumbent Governor

**Faith Statement:** "As an Episcopalian, Governor Scott has stated, 'My faith guides me to serve with compassion and integrity, emphasizing community and stewardship of God's creation.'"

**Background:**
- Lifelong Vermonter, stock car racer, and construction business owner.
- Served as Lt. Gov. and state senator before 2017 election.
- Family man with two daughters; resides on family farm.

**Christian Conservative Analysis:**
- **Pro-Life:** Mixed; pro-choice but vetoed late-term expansions (4/10).
- **Religious Liberty:** Strong defender, settling lawsuits for faith-based schools (8/10).
- **Education/Parental Rights:** Supports tuitioning to religious schools but signed equity mandates (6/10).
- **Family Values:** Promotes inclusive policies, weak on gender issues (5/10).
- **Overall Assessment:** 6/10 - Moderate Republican bulwark against extremism, but compromises on life issues.

**Key Positions:**
- **ABORTION:** Pro-choice with limits; supports reproductive rights enshrined in the state constitution but vetoed extreme expansions.
- **EDUCATION:** Supports school choice through town tuitioning program but opposes vouchers for religious schools; emphasizes local control and parental involvement.
- **RELIGIOUS FREEDOM:** Strong supporter of religious liberty, signing protections for faith-based organizations while balancing LGBTQ+ rights.
- **GUNS:** Moderate 2nd Amendment advocate; vetoed assault weapons ban but signed universal background checks.
- **TAXES:** Opposes broad tax increases; vetoed carbon tax and property tax hikes to protect working families.
- **IMMIGRATION:** Supports humane border security and pathways to citizenship; focuses on integrating immigrants into Vermont's workforce.

**Endorsements:** Vermont Chamber of Commerce, National Federation of Independent Business, Gun Owners of Vermont

**Website:** https://governor.vermont.gov

**Esther Charlestin (Democratic)** - Community Organizer

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Haitian immigrant, social work graduate from UVM.
- Led anti-poverty nonprofits and school boards.
- Mother of three in Winooski.

**Christian Conservative Analysis:**
- **Pro-Life:** Fully pro-choice, no limits (1/10).
- **Religious Liberty:** Prioritizes secularism over faith exemptions (2/10).
- **Education/Parental Rights:** Opposes choice, favors union control (2/10).
- **Family Values:** Inclusive but erodes traditional norms (1/10).
- **Overall Assessment:** 1/10 - Embodiment of progressive overreach threatening biblical values.

**Key Positions:**
- **ABORTION:** Strong pro-choice advocate; supports full access to reproductive healthcare without restrictions.
- **EDUCATION:** Opposes school choice vouchers; prioritizes public school funding and equity programs.
- **RELIGIOUS FREEDOM:** Supports separation of church and state; prioritizes LGBTQ+ protections over religious exemptions.
- **GUNS:** Favors strict gun control, including bans on assault weapons and red-flag laws.
- **TAXES:** Supports progressive taxation to fund social services; backs carbon tax for climate action.
- **IMMIGRATION:** Advocates for sanctuary policies and expanded immigrant rights.

**Endorsements:** Vermont AFL-CIO, Planned Parenthood Vermont, Vermont NEA

**Website:** https://www.estherforvermont.com

**Why It Matters:** A Scott victory preserves veto power against radical left policies eroding family and faith.

---

### **U.S. House of Representatives (At-Large)** - 2026-11-03

**Context:** Controls federal votes on life, guns, and taxes; Vermont's rep influences progressive bloc in Congress.

**Becca Balint (Democratic)** - Incumbent U.S. Representative

**Faith Statement:** "Balint, identifying as Jewish, has said, 'My spirituality informs my commitment to justice and compassion in public service.' No explicit Christian faith statement."

**Background:**
- Former teacher and state senate president.
- Advocate for LGBTQ+ and mental health.
- Wife and mother in Brattleboro.

**Christian Conservative Analysis:**
- **Pro-Life:** Extreme pro-choice (1/10).
- **Religious Liberty:** Weak, prioritizes identity politics (2/10).
- **Education/Parental Rights:** Anti-choice, pro-DEI (1/10).
- **Family Values:** Redefines family away from biblical model (1/10).
- **Overall Assessment:** 1/10 - Progressive ideologue advancing secular humanism.

**Key Positions:**
- **ABORTION:** Fierce defender of reproductive rights; co-sponsored bills to codify Roe v. Wade nationally.
- **EDUCATION:** Prioritizes public education funding; opposes private school vouchers.
- **RELIGIOUS FREEDOM:** Supports broad religious freedoms but prioritizes anti-discrimination laws.
- **GUNS:** Strong gun safety advocate; backs universal background checks and assault weapon bans.
- **TAXES:** Supports raising taxes on wealthy to fund social programs.
- **IMMIGRATION:** Advocates for comprehensive reform with paths to citizenship.

**Endorsements:** EMILY's List, Sierra Club, Everytown for Gun Safety

**Website:** https://balint.house.gov

**Mark Coester (Republican)** - Businessman & Veteran

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Air Force colonel, manufacturing owner.
- Father of four in Essex Junction.
- Focus on economy and vets.

**Christian Conservative Analysis:**
- **Pro-Life:** Solid restrictions (8/10).
- **Religious Liberty:** Strong defender (9/10).
- **Education/Parental Rights:** Pro-choice and rights (8/10).
- **Family Values:** Traditional alignment (8/10).
- **Overall Assessment:** 8/10 - True conservative voice for Vermont's rural Christians.

**Key Positions:**
- **ABORTION:** Pro-life; supports restrictions after viability and defunding Planned Parenthood.
- **EDUCATION:** Strong school choice proponent; backs vouchers and parental rights in curriculum.
- **RELIGIOUS FREEDOM:** Defends religious liberties against government overreach.
- **GUNS:** Staunch 2nd Amendment defender; opposes new restrictions.
- **TAXES:** Advocates for tax cuts and deregulation to boost economy.
- **IMMIGRATION:** Supports secure borders and merit-based immigration.

**Endorsements:** Vermont Republican Party, U.S. Chamber of Commerce, NRA

**Website:** https://markcoester.com

**Why It Matters:** Flipping this seat advances national conservative priorities like life and liberty.

---

### **Lieutenant Governor** - 2026-11-03

**Context:** Influences senate ties; key for blocking progressive bills on family and faith.

**John Rodgers (Republican)** - Incumbent Lt. Governor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Dairy farmer and former rep.
- Family farm leader in Irasburg.
- Husband and father of two.

**Christian Conservative Analysis:**
- **Pro-Life:** Moderate but rural pro-family (5/10).
- **Religious Liberty:** Supports farm faith freedoms (7/10).
- **Education/Parental Rights:** Rural education advocate (6/10).
- **Family Values:** Strong traditional rural ethos (7/10).
- **Overall Assessment:** 6/10 - Practical conservative for working Christians.

**Key Positions:**
- **ABORTION:** Moderate; supports some restrictions but respects state law.
- **EDUCATION:** Supports rural school consolidation and vocational training.
- **RELIGIOUS FREEDOM:** Backs protections for faith-based farms and communities.
- **GUNS:** Strong supporter of hunting rights and concealed carry.
- **TAXES:** Opposes farm tax increases; favors property tax relief.
- **IMMIGRATION:** Supports legal immigration for agricultural workers.

**Endorsements:** Vermont Farm Bureau, Northeast Kingdom Republicans, Dairy Farmers of Vermont

**Website:** https://ltgov.vermont.gov

**Why It Matters:** Retains balance against Democratic supermajority.

---

### **Secretary of State** - 2026-11-03

**Context:** Oversees elections; vital for integrity in a same-day registration state.

**Sarah Copeland Hanzas (Democratic)** - Incumbent Secretary of State

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Environmental attorney and legislator.
- Mother of two in Norwich.

**Christian Conservative Analysis:**
- **Pro-Life:** Pro-choice defender (1/10).
- **Religious Liberty:** Secular priority (2/10).
- **Education/Parental Rights:** Public equity focus (2/10).
- **Family Values:** Progressive family policies (2/10).
- **Overall Assessment:** 2/10 - Enables left-wing voting access without safeguards.

**Key Positions:**
- **ABORTION:** Pro-choice; defended reproductive rights legislation.
- **EDUCATION:** Supports public education equity and teacher pay raises.
- **RELIGIOUS FREEDOM:** Balances with anti-discrimination; supports secular governance.
- **GUNS:** Favors background checks and storage laws.
- **TAXES:** Backs fair share taxation for infrastructure.
- **IMMIGRATION:** Supports inclusive policies for refugees.

**Endorsements:** Vermont Democratic Party, League of Women Voters, ACLU of Vermont

**Website:** https://sos.vermont.gov

**Why It Matters:** Ensures fair elections or risks fraud perceptions.

---

## 🎯 KEY ISSUES FOR Vermont CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Challenge Article 22's unlimited abortion; support heartbeat bills.
- 15 pregnancy centers statewide, like Vermont Right to Life affiliates.
- No parental consent; push for notification laws.
- State funds abortions via Medicaid; defund efforts ongoing.
- Recent victory: Amended law targeting pro-life centers (2025).

**Progressive Position:**
- Expand access, fund via taxes.
- Attacks on centers as "discriminatory."
- Battles over funding for comprehensive care.

**Christian Conservative Action:**
- Join Vermont Right to Life (vtprolife.com).
- Support H.123 for restrictions.
- Volunteer at centers in Burlington.
- Vote pro-life in governor race.

### **School Choice & Parental Rights**

**Conservative Position:**
- Town tuitioning sends $150M+ to private/religious schools annually.
- Parental rights bill (S.102) bans CRT in K-12.
- Homeschooling free, 5,000 students.
- Win: Reinstated Christian school in sports (2025).

**Progressive Position:**
- Act 73 (2025) cuts religious school funding.
- Teachers unions dominate; DEI mandates.
- Threats to tuitioning via equity audits.

**Christian Conservative Action:**
- Run for school boards in rural districts.
- Support S.7 for expanded choice.
- Join Vermont Christian School Alliance.

### **Religious Freedom**

**Conservative Position:**
- Article 3 protects worship; ADF settlements affirm school choice.
- Exemptions for faith-based adoptions.
- Bans on prayer in schools challenged.

**Progressive Position:**
- LGBTQ+ bills override exemptions (H.120).
- Secular curriculum mandates.
- Funding cuts to religious entities.

**Christian Conservative Action:**
- Partner with Alliance Defending Freedom.
- Lobby against H.145.
- Host forums via Christian Action Ministry Network.

### **Guns**

**Conservative Position:**
- Constitutional carry since 2018; 60% gun ownership.
- Vetoed bans; rural hunting culture.
- Preemption laws protect local rights.

**Progressive Position:**
- Universal checks, red-flag laws enacted.
- Assault ban attempts ongoing.
- Storage mandates.

**Christian Conservative Action:**
- Join Gun Owners of Vermont.
- Oppose H.127.
- Train church safety teams.

### **Taxes**

**Conservative Position:**
- No income/sales tax hikes; property relief for seniors.
- Scott vetoes carbon tax.
- Flat income tax advocacy.

**Progressive Position:**
- Progressive brackets, capital gains tax.
- Education fund via property hikes.
- Wealth tax proposals.

**Christian Conservative Action:**
- Support tax cap initiatives.
- Donate to Ethan Allen Institute.
- Vote against overrides.

### **Immigration**

**Conservative Position:**
- Legal pathways for farm workers; E-Verify push.
- Border security funding.
- Integration via civics.

**Progressive Position:**
- Sanctuary state expansions.
- Driver's licenses for undocumented.
- Refugee resettlement priorities.

**Christian Conservative Action:**
- Advocate balanced reform.
- Join Federation for American Immigration Reform.
- Support vetting bills.

### **Family Values**

**Conservative Position:**
- Traditional marriage defense; parental consent for transitions.
- Bans on gender ideology books.
- Faith-based counseling protections.

**Progressive Position:**
- Gender-affirming care mandates.
- No-advice clauses for conversion therapy.
- Inclusive curricula.

**Christian Conservative Action:**
- Back S.20 for parental rights.
- Engage Vermont Family Alliance.
- Family prayer vigils.

### **Election Integrity**

**Conservative Position:**
- Voter ID pilots; paper trails.
- Audit requirements.
- Limit mail-in expansions.

**Progressive Position:**
- Same-day registration; no ID.
- Automatic voter rolls.
- Drop boxes statewide.

**Christian Conservative Action:**
- Train poll watchers via Heritage Action.
- Support S.9 for audits.
- Church registration drives.

---

## 📅 CRITICAL DATES

**2025-2026 Election Calendar:**
- **2025-01-30** - Municipal filing deadline
- **2025-03-04** - Town Meeting Day (Municipal)
- **2026-05-28** - Statewide filing deadline
- **2026-08-11** - Primaries
- **2026-11-03** - General Election

**Voter Registration:** Vermont allows same-day registration at polls. Visit sos.vermont.gov/elections

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
✅ **Share on social media** with #VermontFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Vermont CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Vermont coverage
- **Vermont Right to Life** - Pro-life ratings (vtprolife.com)
- **Christian Action Ministry Network VT** - Faith-based education (christianactionministry.org)
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Vermont Secretary of State**: sos.vermont.gov
- **County Election Offices**: Contact town clerk via mytownclerk.vermont.gov
- **Early Voting Locations**: Available 30 days prior at town offices

### **Conservative Organizations:**
- **Vermont Right to Life**: vtprolife.com
- **Christian Action Ministry Network**: christianactionministry.org
- **Gun Owners of Vermont**: gunownersvt.org
- **Ethan Allen Institute** (School Choice): ethanallen.org
- **Alliance Defending Freedom** - Religious liberty (adflegal.org)
- **First Liberty Institute** - Religious freedom (firstliberty.org)

---

## 🔥 BOTTOM LINE FOR Vermont CHRISTIANS

**2026 Elections Matter:**
- Governor race determines vetoes on abortion expansions.
- U.S. House affects federal pro-life funding.
- Lt. Gov. impacts senate blocks on gender bills.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Rural economies bolstered
✅ Tax relief for families
✅ Faith-based schools funded

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Farm taxes hiked
❌ Sanctuary policies dominate
❌ Secular mandates enforced

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Phil Scott and Mark Coester and their families
- Vermont Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Vermont
- Revival and awakening in Vermont
- God's will in Vermont elections

**Scripture for Vermont Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Vermont coverage, email contact@ekewaka.com

**VERMONT CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Vermont races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Vermont'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Vermont races...")
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

print(f"\nChecking for existing Vermont candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Vermont'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Vermont candidates...")
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

print("\nProcessing Vermont summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Vermont'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Vermont data upload complete!")