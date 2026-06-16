import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Washington Races
races = [
    {
        "state": "Washington",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "This competitive district in southwest Washington represents a key opportunity for Christian conservatives to flip a seat held by a moderate Democrat, impacting national debates on life, family, and borders."
    },
    {
        "state": "Washington",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Central Washington's rural district is a Republican stronghold, but internal conservative challenges could strengthen pro-life and Second Amendment voices in Congress."
    },
    {
        "state": "Washington",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Eastern Washington's District 5 is a conservative bastion where victories reinforce tax cuts, gun rights, and religious liberty against progressive overreach."
    },
    {
        "state": "Washington",
        "office": "U.S. House District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "A battleground district spanning central Washington, this race could expand conservative influence on education freedom and family values."
    },
    {
        "state": "Washington",
        "office": "State Senate District 5",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Special election in suburban Eastside district; a Republican win flips a seat, bolstering defenses for parental rights and election security in Olympia."
    },
    {
        "state": "Washington",
        "office": "State Senate District 26",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Kitsap Peninsula special election; conservatives aim to hold this swing seat to protect pro-life policies and school choice amid Democratic dominance."
    }
]

# Washington Candidates  
candidates = [
    {
        "name": "Joe Kent",
        "state": "Washington",
        "office": "U.S. House District 3",
        "party": "Republican",
        "bio": "Joe Kent is a combat-veteran Green Beret who served 11 deployments in Iraq and Afghanistan, earning a Bronze Star with Valor. Tragically, he lost his wife, Shannon, an Air Force veteran, to an ISIS-inspired attack in 2019 while she advocated for Yazidi genocide survivors. Raised in the Pacific Northwest on a family farm, Joe embodies rural Washington values of hard work, faith, and patriotism. A father to three young children, he homeschools them to instill Christian principles and self-reliance. After leaving the military, Joe worked in national security, focusing on counter-terrorism. His campaign draws on personal loss to champion secure borders and family protection. As a committed Christian, Joe's faith sustains his fight against radical ideologies threatening American freedoms. He has been endorsed by President Trump and conservative leaders for his unapologetic stance on life and liberty. Joe's military discipline and principled conservatism make him a fierce defender of Washington's working families against Washington, D.C. elites.",
        "faith_statement": "As a devoted Christian, my faith in Jesus Christ guides every decision. It compels me to protect the unborn, defend religious liberty, and serve with humility, just as Christ sacrificed for us. In the United for Faith and Freedom interview, I shared how Scripture calls us to justice and mercy in public life.",
        "website": "https://joekentforcongress.com",
        "positions": {
            "ABORTION": "Pro-life without exception; supports national ban to end the 'stain on our humanity' comparable to slavery, protecting the unborn from conception.",
            "EDUCATION": "Strong advocate for school choice, vouchers, and parental rights; opposes federal indoctrination, empowers families to select faith-based or homeschool options.",
            "RELIGIOUS-FREEDOM": "Fierce defender of First Amendment; opposes government mandates infringing on church autonomy or faith-based adoption agencies.",
            "GUNS": "Unyielding Second Amendment supporter; opposes all infringements, including red-flag laws, as a veteran who values self-defense for families.",
            "TAXES": "Cut taxes across the board; eliminate IRS weaponization, promote fair flat tax to unleash economic freedom for working Americans.",
            "IMMIGRATION": "Secure borders immediately with wall completion; end sanctuary policies, deport criminals, prioritize American workers over amnesty.",
            "FAMILY-VALUES": "Traditional marriage, opposes gender ideology in schools; protects parental authority against state overreach on children's upbringing.",
            "ELECTION-INTEGRITY": "Mandate voter ID nationwide; paper ballots, audit reforms to restore trust post-2020 irregularities."
        },
        "endorsements": ["President Donald Trump", "House Freedom Caucus", "National Right to Life"]
    },
    {
        "name": "Marie Gluesenkamp Perez",
        "state": "Washington",
        "office": "U.S. House District 3",
        "party": "Democrat",
        "bio": "Marie Gluesenkamp Perez is the U.S. Representative for Washington's 3rd District, elected in 2022 after flipping the seat from Republican control. A small business owner running an auto shop with her husband in Vancouver, she grew up in rural Colorado and Idaho, learning the value of hard work from her construction worker father. Married with two young children, Marie emphasizes practical solutions for working families. Before Congress, she advocated for trade workers and rural communities. As a moderate Democrat, she has crossed party lines on issues like gun rights and veterans' affairs, earning bipartisan respect. Her focus on infrastructure and economic relief resonates in her blue-collar district spanning the Columbia River Gorge.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://gluesenkampperez.house.gov",
        "positions": {
            "ABORTION": "Pro-choice; supports access up to viability, codifying Roe v. Wade protections in federal law.",
            "EDUCATION": "Invest in public schools; opposes vouchers, focuses on teacher pay and equity programs.",
            "RELIGIOUS-FREEDOM": "Supports protections but backs LGBTQ+ anti-discrimination laws that may conflict with faith-based exemptions.",
            "GUNS": "Moderate; supports background checks and red-flag laws while opposing assault weapon bans.",
            "TAXES": "Raise on wealthy; expand child tax credit for middle-class relief.",
            "IMMIGRATION": "Path to citizenship; comprehensive reform with border security enhancements.",
            "FAMILY-VALUES": "Supports LGBTQ+ rights, gender-affirming care for minors with parental consent.",
            "ELECTION-INTEGRITY": "Opposes voter ID mandates; focuses on expanding access like mail-in voting."
        },
        "endorsements": ["EMILY's List", "Everytown for Gun Safety", "Sierra Club"]
    },
    {
        "name": "Jerrod Sessler",
        "state": "Washington",
        "office": "U.S. House District 4",
        "party": "Republican",
        "bio": "Jerrod Sessler is a U.S. Army veteran and small business owner from Benton City, dedicated to restoring America's Christian heritage. Serving in Iraq, he witnessed the cost of weak leadership and radical threats, fueling his passion for secure borders and constitutional defense. A father and husband, Jerrod prioritizes family protection, drawing from his evangelical faith to advocate for biblical values in policy. After military service, he built a successful construction firm, employing local workers and understanding rural economic struggles. His 2024 primary challenge against incumbent Dan Newhouse highlighted his unyielding conservatism, rejecting compromise on core issues. Endorsed by Trump allies, Jerrod's straightforward style resonates with Central Washington's farmers and veterans seeking bold representation.",
        "faith_statement": "As an evangelical Christian, I believe America was founded on Judeo-Christian principles. Faith compels me to fight moral decay, protect the unborn, and ensure laws reflect God's design for family and society. Gospel preaching inspires my service.",
        "website": "https://jerrodsessler.com",
        "positions": {
            "ABORTION": "Absolute pro-life; no exceptions, national ban to affirm life's sanctity from conception.",
            "EDUCATION": "School choice priority; defund public indoctrination, promote homeschooling and faith-based alternatives.",
            "RELIGIOUS-FREEDOM": "Uncompromised; repeal laws forcing faith groups to violate beliefs on marriage or gender.",
            "GUNS": "Full Second Amendment restoration; repeal all gun control, arm teachers for school safety.",
            "TAXES": "Abolish IRS; flat tax or fair tax to end progressive theft from hardworking families.",
            "IMMIGRATION": "Zero tolerance; mass deportations, end chain migration, ban from terror-linked nations.",
            "FAMILY-VALUES": "Biblical marriage only; ban gender transition for minors, teach traditional roles in schools.",
            "ELECTION-INTEGRITY": "Voter ID mandatory; end mail-in, prosecute fraud to prevent stolen elections."
        },
        "endorsements": ["President Donald Trump", "FreedomWorks", "Gun Owners of America"]
    },
    {
        "name": "Dan Newhouse",
        "state": "Washington",
        "office": "U.S. House District 4",
        "party": "Republican",
        "bio": "Dan Newhouse is the incumbent U.S. Representative for Washington's 4th District, a seventh-generation Yakima Valley farmer serving since 2015. With a background in agriculture and state government as Director of Agriculture, Dan understands rural Washington's needs. A family man with wife Carol and five children, he farms tree fruit and hops, advocating for trade deals benefiting exporters. As a moderate Republican, he has worked across the aisle on water rights and veteran affairs while defending conservative priorities like border security. His votes, including impeaching Trump, have drawn primary challenges, but his district loyalty keeps him strong.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://newhouse.house.gov",
        "positions": {
            "ABORTION": "Pro-life; supports restrictions post-viability, exceptions for rape/incest/life of mother.",
            "EDUCATION": "Supports school choice expansions; focuses on vocational training for rural youth.",
            "RELIGIOUS-FREEDOM": "Backs RFRA protections; opposes mandates on faith-based organizations.",
            "GUNS": "Strong NRA supporter; opposes federal gun control measures.",
            "TAXES": "Extend TCJA cuts; close loopholes for corporations.",
            "IMMIGRATION": "Secure borders; pathway for DREAMers with enforcement.",
            "FAMILY-VALUES": "Traditional family support; opposes federal overreach on gender issues.",
            "ELECTION-INTEGRITY": "Supports voter ID; secure mail-in processes."
        },
        "endorsements": ["National Federation of Independent Business", "Farm Bureau", "U.S. Chamber of Commerce"]
    },
    {
        "name": "Michael Baumgartner",
        "state": "Washington",
        "office": "U.S. House District 5",
        "party": "Republican",
        "bio": "Michael Baumgartner is the newly elected Representative for Washington's 5th District, winning the open seat in 2024 after serving as Spokane's Mayor and State Senator. A Gonzaga University graduate with a Master's from University of Kent, he worked in finance before public service. Married to Kelly with three children, Michael is a devout Catholic whose faith informs his pro-life commitment. As mayor, he balanced budgets and revitalized downtown Spokane. In the Senate, he championed tax relief and education reform. His conservative record includes opposing carbon taxes and supporting veterans. Endorsed by national Republicans, Michael's blend of fiscal discipline and community focus positions him to defend Eastern Washington's values in Congress.",
        "faith_statement": "As a Catholic, my faith teaches the dignity of life from conception and the duty to serve the poor and vulnerable. It guides my pro-life advocacy and commitment to religious liberty.",
        "website": "https://baumgartner.house.gov",
        "positions": {
            "ABORTION": "Pro-life advocate; supports restrictions with exceptions for rape, incest, mother's life; backs IVF protections.",
            "EDUCATION": "Empower parental choice with vouchers; reform for accountability and STEM focus.",
            "RELIGIOUS-FREEDOM": "Defend conscience rights; protect faith-based charities from anti-discrimination mandates.",
            "GUNS": "Second Amendment defender; oppose assault weapons ban, support concealed carry reciprocity.",
            "TAXES": "Cut rates, eliminate death tax; balance budget through spending restraint.",
            "IMMIGRATION": "Enforce laws, finish wall; merit-based system prioritizing skilled workers.",
            "FAMILY-VALUES": "Promote traditional marriage; oppose gender ideology in youth sports and curricula.",
            "ELECTION-INTEGRITY": "Require photo ID; audit systems for transparency and fraud prevention."
        },
        "endorsements": ["National Right to Life", "Family Research Council", "Heritage Foundation"]
    },
    {
        "name": "Carmela Conroy",
        "state": "Washington",
        "office": "U.S. House District 5",
        "party": "Democrat",
        "bio": "Carmela Conroy is a former Washington State Senator and Army veteran running to represent the 5th District. With degrees in nursing and law, she served in the Gulf War and practiced healthcare law. A mother of three, Carmela focuses on veterans' care and rural health access. As senator, she pushed for mental health funding and opioid crisis response. Her moderate Democratic approach appeals to independents in Spokane and the Inland Empire.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice; protect access including late-term in health cases.",
            "EDUCATION": "Fully fund public education; oppose privatization via vouchers.",
            "RELIGIOUS-FREEDOM": "Balance with equality laws; support inclusive policies.",
            "GUNS": "Universal background checks; assault weapons restrictions.",
            "TAXES": "Fair share from wealthy; invest in infrastructure.",
            "IMMIGRATION": "Humane reform; expand DACA protections.",
            "FAMILY-VALUES": "Support diverse families; advance LGBTQ+ equality.",
            "ELECTION-INTEGRITY": "Automatic registration; combat suppression."
        },
        "endorsements": ["Planned Parenthood", "Veterans of Foreign Wars", "AFL-CIO"]
    },
    {
        "name": "Michelle Caldier",
        "state": "Washington",
        "office": "State Senate District 26",
        "party": "Republican",
        "bio": "Dr. Michelle Caldier is a pediatric dentist and foster mother of 28 children, serving as State Representative since 2015 and now challenging for Senate in the 26th District. Raised in a military family, she earned her DDS from NYU and practices in Gig Harbor. Married to Eric, a Navy veteran, Michelle's pro-family ethos stems from fostering traumatized kids, informing her advocacy for parental rights. In Olympia, she authored bills for child welfare reform and against gender transitions for minors. A Catholic, her faith drives compassion with conviction. Endorsed by pro-life groups, Michelle fights Democratic dominance to safeguard Kitsap's values.",
        "faith_statement": "My Catholic faith teaches the sanctity of life and family as society's foundation. It motivates my foster care and policies protecting vulnerable children from ideological harms.",
        "website": "https://caldierforsenate.com",
        "positions": {
            "ABORTION": "Pro-life; supports heartbeat bans, defunds Planned Parenthood.",
            "EDUCATION": "Parental rights bill author; school choice, ban CRT and gender ideology.",
            "RELIGIOUS-FREEDOM": "Protects faith-based adoption; opposes compelled speech on pronouns.",
            "GUNS": "Defends self-defense rights; opposes magazine bans.",
            "TAXES": "No new taxes; cut sales tax on groceries.",
            "IMMIGRATION": "Enforce federal laws; end sanctuary state status.",
            "FAMILY-VALUES": "Traditional definitions; parental consent for transitions.",
            "ELECTION-INTEGRITY": "Voter ID; same-day voting only."
        },
        "endorsements": ["Washington State Republican Party", "Family Policy Institute", "National Federation of Republican Women"]
    },
    {
        "name": "Debora Juarez",
        "state": "Washington",
        "office": "State Senate District 26",
        "party": "Democrat",
        "bio": "Debora Juarez is the appointed interim Senator for the 26th District, a former Seattle City Councilmember and tribal attorney. Of Duwamish and Lumbee descent, she champions equity and indigenous rights. Mother and community leader, Debora focuses on housing affordability and criminal justice reform.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice; expand access and funding.",
            "EDUCATION": "Equity-focused; DEI programs in curricula.",
            "RELIGIOUS-FREEDOM": "Subordinate to anti-discrimination.",
            "GUNS": "Strict controls; ban assault weapons.",
            "TAXES": "Progressive taxation for services.",
            "IMMIGRATION": "Sanctuary protections; amnesty paths.",
            "FAMILY-VALUES": "Inclusive; gender-affirming care.",
            "ELECTION-INTEGRITY": "Vote by mail expansion."
        },
        "endorsements": ["Washington Education Association", "ACLU", "Planned Parenthood"]
    },
    {
        "name": "Chad Magendanz",
        "state": "Washington",
        "office": "State Senate District 5",
        "party": "Republican",
        "bio": "Chad Magendanz is a tech executive and former State Representative seeking the 5th Senate District seat. With a background at Microsoft and founding a software firm, Chad brings business acumen to policy. Married with four children, he coaches youth sports and serves on Issaquah school boards. Previously in Olympia, he passed bipartisan education and public safety bills. A fiscal conservative, Chad opposes tax hikes and champions parental involvement. His 2024 near-miss motivates a comeback to flip the suburban Eastside blue.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://chadmagendanz.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions; supports informed consent laws.",
            "EDUCATION": "Parental rights; expand charter schools and choice.",
            "RELIGIOUS-FREEDOM": "Safeguard faith expressions in public spaces.",
            "GUNS": "Responsible ownership; background checks ok, no bans.",
            "TAXES": "No income tax; cut property taxes for families.",
            "IMMIGRATION": "Legal pathways; secure borders first.",
            "FAMILY-VALUES": "Protect minors from ideological curricula.",
            "ELECTION-INTEGRITY": "Voter ID; transparent counting."
        },
        "endorsements": ["Association of Washington Business", "Washington Policy Center", "Eastside Republican Club"]
    },
    {
        "name": "Victoria Hunt",
        "state": "Washington",
        "office": "State Senate District 5",
        "party": "Democrat",
        "bio": "Victoria Hunt is the appointed Senator for the 5th District, a community organizer and former nonprofit leader. Mother of two, she advocates for affordable housing and mental health. Appointed after Ramos's passing, Victoria focuses on equity in East King County suburbs.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Full access protections.",
            "EDUCATION": "Inclusive public funding.",
            "RELIGIOUS-FREEDOM": "Equality over exemptions.",
            "GUNS": "Gun safety reforms.",
            "TAXES": "Fund social programs.",
            "IMMIGRATION": "Protect immigrants.",
            "FAMILY-VALUES": "Diverse family support.",
            "ELECTION-INTEGRITY": "Access expansion."
        },
        "endorsements": ["Washington State Labor Council", "Evergreen Freedom Foundation critics", "Democratic Party"]
    }
]

# Washington Summary
summary = {
    "state": "Washington",
    "title": "Washington 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Washington 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 6  
**Total Candidates Profiled:** 10  
**Election Dates:**  
- 2025-11-04 (General Election)  
- 2026-11-03 (General Election)  

---

## 🔴 Washington POLITICAL LANDSCAPE

### **The Evergreen State**

Washington is a **deep blue stronghold with conservative strongholds in the east**:  
- **Partisan Control:** Democratic trifecta since 2018; supermajorities in legislature (29-20 Senate, 59-39 House).  
- **Voter Trends:** Biden +18 in 2020; Seattle/King County 70%+ Dem, eastern/rural 60%+ GOP.  
- **Urban-Rural Divide:** Seattle (ultra-liberal tech hub), Spokane (swing conservative), rural counties like Yakima (solid red).  
- **Tech & Trade Influence:** Boeing, Amazon drive economy but fuel progressive taxes and regulations.  

### **Why Washington Matters**

Washington is **WINNABLE** for Christian conservatives:  
- ✅ **Pro-Life Leadership:** State allows abortion to birth; recent laws fund out-of-state travel—urgent need for restrictions.  
- ✅ **Second Amendment:** Mixed; I-594 background checks burden owners, but rural resistance strong.  
- ✅ **School Choice:** Limited ESA program; push for expansion against teachers' unions.  
- ✅ **Religious Liberty:** Threats from anti-discrimination bills forcing faith groups to affirm LGBTQ+ views.  
- ✅ **Family Values:** Gender ideology in schools; no parental notification on transitions.  
- ✅ **Border Impacts:** Sanctuary state policies strain resources amid migrant surges.  

---

## 🔴 2025 STATE LEGISLATIVE RACES

### **State Senate District 5** - 2025-11-04

**Context:** Suburban Eastside special election vacated by Democrat Bill Ramos's death; Republican flip could narrow Dem supermajority, protecting parental rights and tax relief.

**Chad Magendanz (Republican)** - Tech Executive & Former Rep

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**  
- Microsoft alum, founded software firm.  
- Coached youth sports, served Issaquah school board.  
- Near-win in 2024 shows momentum.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Supports restrictions; voted for informed consent.  
- **Religious Liberty:** Backs faith exemptions in adoption.  
- **Education/Parental Rights:** Champions notification laws; opposes secret transitions.  
- **Family Values:** Aligns biblically on marriage, youth protection.  
- **Overall Assessment:** 8/10—Solid fiscal conservative, strong on families but moderate tone aids bipartisanship.  

**Key Positions:**  
- **ABORTION:** Pro-life with exceptions; informed consent mandates.  
- **EDUCATION:** Charter expansion, parental opt-outs from DEI.  
- **RELIGIOUS FREEDOM:** Protect conscience against state mandates.  
- **GUNS:** Background checks ok, no bans.  
- **TAXES:** Oppose capital gains tax hikes.  
- **IMMIGRATION:** Legal enforcement, no sanctuary expansion.  

**Endorsements:** Association of Washington Business, Washington Policy Center  

**Website:** https://chadmagendanz.com  

**Victoria Hunt (Democrat)** - Community Organizer  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Appointed interim; nonprofit leader.  
- Focus on housing equity.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Opposes all restrictions.  
- **Religious Liberty:** Prioritizes inclusion over exemptions.  
- **Education/Parental Rights:** Supports gender-affirming without notice.  
- **Family Values:** Redefines traditional norms.  
- **Overall Assessment:** 2/10—Progressive agenda erodes biblical foundations.  

**Key Positions:**  
- **ABORTION:** Full access, state-funded.  
- **EDUCATION:** DEI mandatory.  
- **RELIGIOUS FREEDOM:** Anti-discrimination trumps faith.  
- **GUNS:** Assault ban.  
- **TAXES:** Wealth taxes.  
- **IMMIGRATION:** Sanctuary expansions.  

**Endorsements:** WA Labor Council  

**Website:**  

**Why It Matters:** Flipping LD5 halts radical bills threatening WA families' core values.  

### **State Senate District 26** - 2025-11-04

**Context:** Kitsap special after Emily Randall's congressional win; hold for GOP maintains balance against pro-abortion pushes.

**Michelle Caldier (Republican)** - Dentist & Foster Mom  

**Faith Statement:** "My Catholic faith teaches the sanctity of life and family as society's foundation. It motivates my foster care and policies protecting vulnerable children from ideological harms."  

**Background:**  
- Fostered 28 kids; pediatric dentist.  
- Authored child welfare reforms.  
- Military family roots.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Heartbeat bill sponsor.  
- **Religious Liberty:** Fights compelled affirmation.  
- **Education/Parental Rights:** Bans secret transitions.  
- **Family Values:** Biblical defender.  
- **Overall Assessment:** 9/10—Faith-driven warrior for kids and liberty.  

**Key Positions:**  
- **ABORTION:** Heartbeat ban, defund PP.  
- **EDUCATION:** Choice, ban CRT/gender lessons.  
- **RELIGIOUS FREEDOM:** Faith adoption protections.  
- **GUNS:** Oppose mag bans.  
- **TAXES:** Cut grocery sales tax.  
- **IMMIGRATION:** End sanctuary.  

**Endorsements:** WA GOP, Family Policy Institute  

**Website:** https://caldierforsenate.com  

**Debora Juarez (Democrat)** - Tribal Attorney  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Seattle Council alum.  
- Indigenous rights advocate.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Funds abortions.  
- **Religious Liberty:** Subsumes to equity.  
- **Education/Parental Rights:** Indoctrination push.  
- **Family Values:** Redefines norms.  
- **Overall Assessment:** 1/10—Cultural Marxism threat.  

**Key Positions:**  
- **ABORTION:** To birth access.  
- **EDUCATION:** Equity curricula.  
- **RELIGIOUS FREEDOM:** No exemptions.  
- **GUNS:** Strict controls.  
- **TAXES:** Progressive hikes.  
- **IMMIGRATION:** Amnesty.  

**Endorsements:** ACLU  

**Website:**  

**Why It Matters:** Retaining LD26 shields pro-life gains from Olympia radicals.  

---

## 🔴 2026 FEDERAL RACES

### **U.S. House District 3** - 2026-11-03

**Context:** Rural southwest battleground; GOP flip restores conservative voice on borders, life amid national midterms.

**Joe Kent (Republican)** - Green Beret Veteran  

**Faith Statement:** "As a devoted Christian, my faith in Jesus Christ guides every decision. It compels me to protect the unborn, defend religious liberty, and serve with humility, just as Christ sacrificed for us. In the United for Faith and Freedom interview, I shared how Scripture calls us to justice and mercy in public life."  

**Background:**  
- 11 deployments, Bronze Star.  
- Lost wife to ISIS; fathers three.  
- Homeschools kids.  

**Christian Conservative Analysis:**  
- **Pro-Life:** National ban advocate.  
- **Religious Liberty:** Anti-mandate warrior.  
- **Education/Parental Rights:** Choice champion.  
- **Family Values:** Traditional protector.  
- **Overall Assessment:** 10/10—Faith-fueled patriot.  

**Key Positions:**  
- **ABORTION:** No exceptions ban.  
- **EDUCATION:** Vouchers, anti-indoctrination.  
- **RELIGIOUS FREEDOM:** First Amendment absolute.  
- **GUNS:** Full 2A.  
- **TAXES:** Flat tax.  
- **IMMIGRATION:** Wall, deportations.  

**Endorsements:** Trump, Freedom Caucus  

**Website:** https://joekentforcongress.com  

**Marie Gluesenkamp Perez (Democrat)** - Auto Shop Owner  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Flipped seat 2022.  
- Rural roots, two kids.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Roe codifier.  
- **Religious Liberty:** Conflicts with equality.  
- **Education/Parental Rights:** Union ally.  
- **Family Values:** LGBTQ+ priority.  
- **Overall Assessment:** 3/10—Moderate but enables left.  

**Key Positions:**  
- **ABORTION:** Viability access.  
- **EDUCATION:** Public investment.  
- **RELIGIOUS FREEDOM:** Balanced with rights.  
- **GUNS:** Checks, flags.  
- **TAXES:** Child credit.  
- **IMMIGRATION:** Citizenship path.  

**Endorsements:** EMILY's List  

**Website:** https://gluesenkampperez.house.gov  

**Why It Matters:** Victory sends pro-life message to D.C.  

### **U.S. House District 4** - 2026-11-03

**Context:** Ag-heavy district; conservative primary winner solidifies GOP hold, advances biblical policies.

**Jerrod Sessler (Republican)** - Army Veteran  

**Faith Statement:** "As an evangelical Christian, I believe America was founded on Judeo-Christian principles. Faith compels me to fight moral decay, protect the unborn, and ensure laws reflect God's design for family and society. Gospel preaching inspires my service."  

**Background:**  
- Iraq vet, construction owner.  
- Family man from Benton City.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Absolute ban.  
- **Religious Liberty:** Uncompromised.  
- **Education/Parental Rights:** Defund public.  
- **Family Values:** Biblical only.  
- **Overall Assessment:** 9/10—Bold but controversial.  

**Key Positions:**  
- **ABORTION:** Conception protection.  
- **EDUCATION:** Homeschool promotion.  
- **RELIGIOUS FREEDOM:** Repeal conflicts.  
- **GUNS:** Arm teachers.  
- **TAXES:** Abolish IRS.  
- **IMMIGRATION:** Mass deport.  

**Endorsements:** Trump, GOA  

**Website:** https://jerrodsessler.com  

**Dan Newhouse (Republican)** - Farmer  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- 7th-gen farmer.  
- Ag director alum.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Restrictions.  
- **Religious Liberty:** Supports.  
- **Education/Parental Rights:** Choice.  
- **Family Values:** Traditional.  
- **Overall Assessment:** 6/10—Moderate compromises.  

**Key Positions:**  
- **ABORTION:** Post-viability limits.  
- **EDUCATION:** Vocational.  
- **RELIGIOUS FREEDOM:** RFRA.  
- **GUNS:** NRA.  
- **TAXES:** TCJA extend.  
- **IMMIGRATION:** DREAMers path.  

**Endorsements:** Farm Bureau  

**Website:** https://newhouse.house.gov  

**Why It Matters:** True conservative ousts RINO, strengthens national fight.  

### **U.S. House District 5** - 2026-11-03

**Context:** Spokane-based GOP seat; hold amplifies voice for Eastern WA's Christian heartland.

**Michael Baumgartner (Republican)** - Former Mayor  

**Faith Statement:** "As a Catholic, my faith teaches the dignity of life from conception and the duty to serve the poor and vulnerable. It guides my pro-life advocacy and commitment to religious liberty."  

**Background:**  
- Spokane mayor, state senator.  
- Finance to public service.  
- Three kids.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Advocate with exceptions.  
- **Religious Liberty:** Conscience rights.  
- **Education/Parental Rights:** Charters.  
- **Family Values:** Youth protection.  
- **Overall Assessment:** 8/10—Faith-integrated conservative.  

**Key Positions:**  
- **ABORTION:** Restrictions, IVF ok.  
- **EDUCATION:** Vouchers.  
- **RELIGIOUS FREEDOM:** Defend charities.  
- **GUNS:** No bans.  
- **TAXES:** Cut death tax.  
- **IMMIGRATION:** Merit-based.  

**Endorsements:** NRLC, FRC  

**Website:** https://baumgartner.house.gov  

**Carmela Conroy (Democrat)** - Army Nurse  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Gulf War vet, lawyer.  
- Mental health focus.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Full choice.  
- **Religious Liberty:** Equality first.  
- **Education/Parental Rights:** Public only.  
- **Family Values:** Diverse.  
- **Overall Assessment:** 2/10—Progressive.  

**Key Positions:**  
- **ABORTION:** Protected access.  
- **EDUCATION:** No privatization.  
- **RELIGIOUS FREEDOM:** Inclusive.  
- **GUNS:** Safety reforms.  
- **TAXES:** Infrastructure fund.  
- **IMMIGRATION:** DACA expand.  

**Endorsements:** VFW  

**Website:**  

**Why It Matters:** Secures red wall against blue wave.  

### **U.S. House District 8** - 2026-11-03

**Context:** Central WA swing; pickup expands conservative bloc on ag, energy, values.

**Kim Schrier (Democrat)** - Pediatrician Incumbent  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Doctor, Sammamish mom.  
- Flipped 2018.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Choice advocate.  
- **Religious Liberty:** Limited.  
- **Education/Parental Rights:** Union-backed.  
- **Family Values:** Modern.  
- **Overall Assessment:** 3/10—Swing but left-leaning.  

**Key Positions:**  
- **ABORTION:** Codify Roe.  
- **EDUCATION:** Teacher pay.  
- **RELIGIOUS FREEDOM:** Anti-bias.  
- **GUNS:** Checks.  
- **TAXES:** Middle relief.  
- **IMMIGRATION:** Reform.  

**Endorsements:** AMA  

**Website:** https://schrier.house.gov  

**Carmen Goers (Republican)** - Rancher  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Family rancher.  
- 2024 challenger.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Strong.  
- **Religious Liberty:** Defender.  
- **Education/Parental Rights:** Choice.  
- **Family Values:** Traditional.  
- **Overall Assessment:** 7/10—Rural conservative.  

**Key Positions:**  
- **ABORTION:** Restrictions.  
- **EDUCATION:** Vouchers.  
- **RELIGIOUS FREEDOM:** Protections.  
- **GUNS:** 2A full.  
- **TAXES:** Cuts.  
- **IMMIGRATION:** Secure.  

**Endorsements:** WA Farm Bureau  

**Website:** https://carmengoers.com  

**Why It Matters:** Flip turns WA bluer to purple, aids national majorities.  

---

## 🎯 KEY ISSUES FOR Washington CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**  
- Oppose SB 5999 allowing birth abortions; push heartbeat laws.  
- 50+ pregnancy centers via Heartbeat WA.  
- Parental consent upheld but challenged.  
- Defund Planned Parenthood via budget fights.  
- 2023 victory: Near-ban on late-term passed House.  

**Progressive Position:**  
- Codify unlimited access via Initiative 109.  
- State funds travel for abortions.  
- Battle over chemical abortion pills.  

**Christian Conservative Action:**  
- Join Human Life of WA (humanlife.org).  
- Support HB 1925 restrictions.  
- Volunteer at centers like Care Net.  
- Vote pro-life in LD5,26.  

### **School Choice & Parental Rights**

**Conservative Position:**  
- ESA for 10k students; expand to all.  
- HB 1310 notification law.  
- Bans on CRT (HB 1454 failed).  
- Homeschool freedom top-ranked.  
- 2024 win: Blocked gender books.  

**Progressive Position:**  
- Union blocks choice; WEA $10M against.  
- DEI mandates in teacher training.  
- Threats to homeschool oversight.  

**Christian Conservative Action:**  
- Run for school boards via WA Policy.  
- Back SB 5171 expansion.  
- Join Parental Rights Org (parentalrights.org).  

### **Religious Freedom**

**Conservative Position:**  
- Uphold RFRA against baker cases.  
- Protect adoption agencies (won 2022).  
- Oppose pronoun mandates.  
- Faith exemptions in healthcare.  
- Recent: Blocked anti-faith bill.  

**Progressive Position:**  
- SB 5180 forces affirmation.  
- Tax faith groups for non-compliance.  
- School prayer bans.  

**Christian Conservative Action:**  
- Alliance Defending Freedom cases.  
- Support First Liberty (firstliberty.org).  
- Lobby HB 1196 protections.  

### **Guns**

**Conservative Position:**  
- Preemption law holds; no local bans.  
- CCW reciprocity.  
- Oppose I-1639 expansions.  
- Rural training funded.  
- 2023: Armed teachers pilot.  

**Progressive Position:**  
- Assault ban push (SB 5078).  
- Red-flag laws expanded.  
- Ammo taxes proposed.  

**Christian Conservative Action:**  
- NRA-WA chapters.  
- Join Citizens Committee Guns (ccrkba.org).  
- Vote against Seattle bans.  

### **Taxes**

**Conservative Position:**  
- No income tax (Const. Art. VII).  
- Cut property via 61% lid.  
- Oppose capital gains (I-1631).  
- Business incentives.  
- 2025: Blocked wealth tax.  

**Progressive Position:**  
- Carbon fee hikes.  
- Sales tax on rich.  
- Union dues mandates.  

**Christian Conservative Action:**  
- WA Policy Center (washingtonpolicy.org).  
- Support TABOR-like initiative.  
- Donate to anti-tax PACs.  

### **Immigration**

**Conservative Position:**  
- End sanctuary (HB 1179).  
- E-Verify mandate.  
- Oppose driver's licenses for illegals.  
- Border aid.  
- 2024: Blocked amnesty.  

**Progressive Position:**  
- Sanctuary expansions.  
- In-state tuition for undocumented.  
- Decrim sanctuary cities.  

**Christian Conservative Action:**  
- WA State GOP border caucus.  
- Join FAIR (fairus.org).  
- Lobby enforcement bills.  

### **Family Values**

**Conservative Position:**  
- Traditional marriage (no change needed).  
- Ban transitions minors (HB 1907).  
- Oppose drag shows kids.  
- Parental curriculum veto.  
- Win: Blocked nonbinary IDs.  

**Progressive Position:**  
- Gender self-ID.  
- Affirm care schools.  
- Erase parental role.  

**Christian Conservative Action:**  
- Family Policy Institute (fpiw.org).  
- Support CPAC WA events.  
- Church forums on values.  

### **Election Integrity**

**Conservative Position:**  
- Voter ID bill (HB 1052 failed).  
- Paper backups.  
- Audit 2020 anomalies.  
- End drop boxes.  
- 2025: Pushed same-day vote.  

**Progressive Position:**  
- All-mail expansion.  
- No ID, auto-reg.  
- Felon voting immediate.  

**Christian Conservative Action:**  
- iVoterGuide WA.  
- Join Election Integrity WA.  
- Poll watch training.  

---

## 📅 CRITICAL DATES

**2025 Election Calendar:**  
- **2025-10-27** - Voter registration deadline  
- **2025-10-24** - Early voting begins  
- **2025-08-05** - Primary Election  
- **2025-11-04** - General Election  

**2026 Election Calendar:**  
- **2026-10-26** - Voter registration deadline  
- **2026-10-23** - Early voting begins  
- **2026-08-04** - Primary Election  
- **2026-11-03** - General Election  

**Voter Registration:** VoteWA.gov  

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
✅ **Share on social media** with #WAFaithVote  
✅ **Pray daily** for elections and candidates  
✅ **Vote early** and bring friends/family to polls  
✅ **Serve as poll watchers** to ensure election integrity  

---

## 📞 RESOURCES FOR Washington CHRISTIAN VOTERS

### **Voter Guide Organizations:**  
- **iVoterGuide.org** - Washington coverage  
- **Washington State Right to Life** - Pro-life ratings (wsrtl.org)  
- **Family Policy Institute of WA** - Faith-based education (fpiw.org)  
- **Christian Voter Guide** - Biblical alignment  

### **Election Information:**  
- **Washington Secretary of State**: sos.wa.gov/elections  
- **County Election Offices**: Find via VoteWA.gov  
- **Early Voting Locations**: County auditor sites  

### **Conservative Organizations:**  
- **Washington State Right to Life**: wsrtl.org  
- **Family Policy Institute**: fpiw.org  
- **Citizens Committee for the Right to Keep & Bear Arms**: ccrkba.org  
- **Washington Policy Center**: washingtonpolicy.org  
- **Alliance Defending Freedom** - Religious liberty (adflegal.org)  
- **First Liberty Institute** - Religious freedom (firstliberty.org)  

---

## 🔥 BOTTOM LINE FOR Washington CHRISTIANS

**2025-2026 Elections Matter:**  
- LD5 Senate determines parental rights laws.  
- LD26 affects pro-life funding battles.  
- WA-3 flip impacts national border security.  
- Overall state direction at stake  

**If Conservatives Win:**  

✅ Pro-life protections maintained/strengthened  
✅ School choice expanded, parental rights protected  
✅ Religious liberty defended  
✅ Traditional family values upheld  
✅ Second Amendment rights secured  
✅ Election integrity ensured  
✅ Rural economies boosted via tax cuts  
✅ Border security for safe communities  
✅ Faith freedoms from Olympia overreach  

**If Progressives Win:**  

❌ Abortion expansion, pro-life laws repealed  
❌ School choice gutted, CRT/gender ideology in schools  
❌ Religious liberty attacked  
❌ Family values eroded, parental rights stripped  
❌ Gun rights restricted  
❌ Election integrity weakened  
❌ Taxes hike on families  
❌ Sanctuary chaos increases crime  
❌ Indoctrination in classrooms  

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**  

---

## 🙏 PRAYER POINTS

**Pray for:**  
- Joe Kent, Jerrod Sessler, Michelle Caldier, Chad Magendanz, Michael Baumgartner and families  
- Washington Governor/leadership  
- Conservative candidates in all races  
- Church mobilization and Christian voter turnout  
- Protection from voter fraud  
- Wisdom for Christian voters in Washington  
- Revival and awakening in Washington  
- God's will in Washington elections  

**Scripture for Washington Elections:**  

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*  

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*  

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*  

---

**Last Updated:** October 2025  
**Source:** Christian Conservatives Today Election Coverage  
**Contact:** For questions or to contribute Washington coverage, email contact@ekewaka.com  

**Washington CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Washington races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Washington'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Washington races...")
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

print(f"\nChecking for existing Washington candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Washington'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Washington candidates...")
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

print("\nProcessing Washington summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Washington'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Washington data upload complete!")