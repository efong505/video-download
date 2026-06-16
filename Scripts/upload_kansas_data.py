import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Kansas Races
races = [
    {
        "state": "Kansas",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the Class III U.S. Senate seat held by incumbent Republican Roger Marshall, critical for maintaining conservative influence in the Senate."
    },
    {
        "state": "Kansas",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat as Democratic incumbent Laura Kelly is term-limited; pivotal race to shift control from divided government to full Republican dominance."
    },
    {
        "state": "Kansas",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Republican Kris Kobach seeks reelection; key for enforcing conservative policies on immigration, election integrity, and pro-life laws."
    },
    {
        "state": "Kansas",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat as incumbent Republican Scott Schwab runs for governor; vital for election administration and security."
    },
    {
        "state": "Kansas",
        "office": "State Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Republican Steven Johnson seeks reelection; focuses on fiscal responsibility and anti-ESG measures."
    },
    {
        "state": "Kansas",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Republican-held district in western Kansas; incumbent Tracey Mann emphasizes agriculture and rural values."
    },
    {
        "state": "Kansas",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Republican-held district; incumbent Jake LaTurner focuses on conservative economic policies."
    },
    {
        "state": "Kansas",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Democratic-held suburban district around Kansas City; incumbent Sharice Davids is a moderate facing potential challenges."
    },
    {
        "state": "Kansas",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Safe Republican district in south-central Kansas; incumbent Ron Estes prioritizes tax cuts and energy."
    },
    {
        "state": "Kansas",
        "office": "Wichita City Council District 1",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Key municipal race in Kansas's largest city, influencing local conservative policies on taxes and public safety."
    }
]

# Kansas Candidates  
candidates = [
    {
        "name": "Jeff Colyer",
        "state": "Kansas",
        "office": "Governor",
        "party": "Republican",
        "bio": "Jeffrey William Colyer, M.D., born June 3, 1960, is a fifth-generation Kansan and board-certified plastic surgeon who has dedicated his career to public service. A graduate of the University of Kansas School of Medicine, Colyer served as a combat physician in the U.S. Army during Operation Desert Storm, earning the Army Commendation Medal. He entered politics in 2006, winning election to the Kansas House of Representatives, followed by the State Senate in 2008. As Lieutenant Governor from 2011 to 2018 under Sam Brownback, he focused on economic development and education reform. Colyer became the 47th Governor in 2018 after Brownback's resignation, serving until 2019, where he signed pro-life legislation and tax cuts. Married to Kristin Nichols-Colyer, a nurse, they have three children and reside in Overland Park. Colyer's accomplishments include expanding Medicaid access while maintaining fiscal conservatism and leading Kansas through natural disasters. Now running again for governor, he emphasizes restoring Kansas's economy and family values.",
        "faith_statement": "As a devout Christian, my faith guides my service to others, rooted in the belief that every life is sacred and government should protect the vulnerable, as taught in Proverbs 31:8-9.",
        "website": "https://jeffcolyer.com",
        "positions": {
            "ABORTION": "Strongly pro-life; supports heartbeat bill and defunding Planned Parenthood, citing his signing of multiple pro-life measures as governor.",
            "EDUCATION": "Advocates school choice and parental rights, including vouchers for private and charter schools to empower families.",
            "RELIGIOUS-FREEDOM": "Defends First Amendment rights, opposing mandates that infringe on faith-based objections, as seen in his support for religious exemptions.",
            "GUNS": "Firm 2nd Amendment supporter; opposes red-flag laws and supports constitutional carry expansion.",
            "TAXES": "Proven tax cutter; enacted $800 million in reductions as governor and pledges further property tax relief.",
            "IMMIGRATION": "Enforces strict border security and opposes sanctuary policies, building on his work with federal immigration enforcement.",
            "FAMILY-VALUES": "Upholds traditional marriage and opposes gender ideology in schools, promoting parental consent for sensitive topics.",
            "ELECTION-INTEGRITY": "Supports voter ID and paper ballots to ensure secure elections."
        },
        "endorsements": ["Family Research Council", "National Right to Life", "Kansas State Rifle Association"]
    },
    {
        "name": "Scott Schwab",
        "state": "Kansas",
        "office": "Governor",
        "party": "Republican",
        "bio": "Scott Joseph Schwab, born July 9, 1972, in Great Bend, Kansas, is a lifelong conservative leader and current Secretary of State. A graduate of Fort Hays State University, Schwab served in the Kansas House from 2003-2009 before becoming Olathe City Councilman. Elected Secretary of State in 2018 and reelected in 2022, he modernized election systems, implemented secure voting measures, and defended against fraud claims while promoting transparency. Married to Dorene, with three children, Schwab is active in his community church and coaches youth sports. His accomplishments include expanding early voting access without compromising integrity and launching cybersecurity initiatives for elections. As a candidate for governor, Schwab focuses on cutting property taxes and enhancing public safety.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://scottschwab.com",
        "positions": {
            "ABORTION": "Pro-life; supports state bans post-Roe and defunding abortion providers.",
            "EDUCATION": "Supports school choice expansions and parental involvement in curriculum decisions.",
            "RELIGIOUS-FREEDOM": "Strong advocate for religious liberties in public policy and exemptions from mandates.",
            "GUNS": "2nd Amendment defender; backs permitless carry and opposes gun control.",
            "TAXES": "Prioritizes property tax elimination through state surpluses.",
            "IMMIGRATION": "Enforces immigration laws and supports border wall funding.",
            "FAMILY-VALUES": "Promotes traditional family structures and opposes LGBTQ+ ideology in schools.",
            "ELECTION-INTEGRITY": "Champion of secure elections with voter ID and audit requirements."
        },
        "endorsements": ["Americans for Prosperity", "Kansas Chamber of Commerce", "National Federation of Independent Business"]
    },
    {
        "name": "Cindy Holscher",
        "state": "Kansas",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Cynthia L. Holscher, born April 26, 1969, is a trailblazing Democratic state senator from Overland Park, serving District 8 since 2021. A former real estate professional and small business owner, Holscher flipped a Republican seat in 2020 by focusing on education and healthcare. Married with two children, she is a community volunteer involved in local schools and women's rights groups. As Senate Minority Whip, she has fought against extreme abortion bans and for public school funding. Her accomplishments include blocking voucher expansions that would drain public education budgets and advocating for reproductive rights post the 2022 Value Them Both defeat. Running for governor, Holscher pledges to protect democracy and expand access to affordable care.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://cindyforkansas.com",
        "positions": {
            "ABORTION": "Pro-choice; opposes all restrictions and supports restoring Roe protections in Kansas.",
            "EDUCATION": "Defends public schools against vouchers; promotes teacher pay raises and inclusive curricula.",
            "RELIGIOUS-FREEDOM": "Supports separation of church and state; opposes using faith to discriminate against LGBTQ+ individuals.",
            "GUNS": "Favors universal background checks and red-flag laws to reduce gun violence.",
            "TAXES": "Opposes cuts for the wealthy; supports fair taxation to fund education and healthcare.",
            "IMMIGRATION": "Pathway to citizenship and opposes family separations at borders.",
            "FAMILY-VALUES": "Inclusive families; supports LGBTQ+ rights and gender-affirming care.",
            "ELECTION-INTEGRITY": "Expands voting access; opposes restrictive ID laws."
        },
        "endorsements": ["Planned Parenthood", "Kansas AFL-CIO", "Everytown for Gun Safety"]
    },
    {
        "name": "Roger Marshall",
        "state": "Kansas",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Roger Wayne Marshall, M.D., born August 9, 1960, in El Dorado, Kansas, is a board-certified OB-GYN and U.S. Senator since 2021. Raised in a devout Christian family—his father was a police chief—he graduated from Kansas State University and the University of Kansas School of Medicine. Marshall practiced medicine for over 25 years, delivering 5,000 babies, before serving in the U.S. House (2017-2021). Married to Laina, with four children and eight grandchildren, faith and family anchor his life. As Senator, he chairs the Republican Physicians Caucus and fights for rural healthcare. Accomplishments include blocking Biden's vaccine mandates and advancing pro-life legislation like the Heartbeat Act. Reelection bid emphasizes America First policies.",
        "faith_statement": "My faith is the most important part of my life; as a Christian, I believe every life begins at conception, and I am guided by biblical principles in defending the unborn and religious freedoms.",
        "website": "https://www.marshall.senate.gov",
        "positions": {
            "ABORTION": "100% pro-life; co-sponsor of national heartbeat bill and defunds Planned Parenthood.",
            "EDUCATION": "Empowers parental rights with school choice and bans CRT in federal funding.",
            "RELIGIOUS-FREEDOM": "Staunch defender; led efforts against COVID mandates infringing on faith.",
            "GUNS": "Absolute 2nd Amendment support; opposes all federal gun control.",
            "TAXES": "Permanent TCJA extension and eliminates death tax.",
            "IMMIGRATION": "Secure borders; ends chain migration and builds the wall.",
            "FAMILY-VALUES": "Traditional marriage; protects children from gender ideology.",
            "ELECTION-INTEGRITY": "Requires voter ID nationwide and audits all elections."
        },
        "endorsements": ["Family Research Council Action", "National Right to Life Committee", "NRA"]
    },
    {
        "name": "Christy Davis",
        "state": "Kansas",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Christy Cauble Davis, a fifth-generation Kansan from Cottonwood Falls, is a proven public servant and small business owner challenging Roger Marshall. As Kansas Director for USDA Rural Development under Biden, she oversaw $1 billion in investments for rural infrastructure, housing, and healthcare. A graduate of Wichita State University, Davis previously ran for Congress in 2020, emphasizing working families. Married to Luke with son Jack, she is active in community advocacy. Accomplishments include launching broadband initiatives and supporting Flint Hills farmers. Her campaign focuses on broadening Kansas voices in D.C., fighting corporate greed, and protecting democracy.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.christydavisforkansas.com",
        "positions": {
            "ABORTION": "Pro-choice; defends Kansas's constitutional right to abortion access.",
            "EDUCATION": "Fully funds public schools; opposes vouchers diverting resources.",
            "RELIGIOUS-FREEDOM": "Protects all faiths while ensuring no imposition on others' rights.",
            "GUNS": "Common-sense reforms like background checks; supports rural hunters.",
            "TAXES": "Makes billionaires pay fair share; lowers costs for working families.",
            "IMMIGRATION": "Comprehensive reform with border security and pathways for Dreamers.",
            "FAMILY-VALUES": "Supports diverse families; advances LGBTQ+ equality.",
            "ELECTION-INTEGRITY": "Expands access and combats disinformation."
        },
        "endorsements": ["EMILYs List", "League of Conservation Voters", "Sierra Club"]
    },
    {
        "name": "Kris Kobach",
        "state": "Kansas",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "Kris William Kobach, born March 26, 1966, in Madison, Wisconsin, but raised in Topeka, is Kansas's 45th Attorney General since 2023. A Yale Law graduate and Oxford Ph.D. in politics, Kobach served as Overland Park City Attorney and adjunct professor. As Secretary of State (2011-2019), he implemented proof-of-citizenship voting laws. Married to Heather with five daughters, Kobach is a conservative Catholic family man. Accomplishments include 20+ successful election lawsuits and defending state sovereignty. As AG, he has sued over border security and election integrity.",
        "faith_statement": "As a Catholic, I am committed to protecting the dignity of life from conception and upholding Judeo-Christian values in law.",
        "website": "https://www.ag.ks.gov",
        "positions": {
            "ABORTION": "Pro-life warrior; enforces bans and sues to restrict access.",
            "EDUCATION": "Parental rights first; supports choice to counter indoctrination.",
            "RELIGIOUS-FREEDOM": "Defends against federal overreach on faith issues.",
            "GUNS": "2nd Amendment absolutist; blocks gun control efforts.",
            "TAXES": "Fiscal hawk; opposes tax hikes on families.",
            "IMMIGRATION": "Zero tolerance; authored key anti-sanctuary laws.",
            "FAMILY-VALUES": "Traditional values; opposes transgender policies in youth.",
            "ELECTION-INTEGRITY": "Gold standard; mandates voter ID and purges rolls."
        },
        "endorsements": ["Federation for American Immigration Reform", "Heritage Foundation", "Kansas Republican Party"]
    },
    {
        "name": "Chris Mann",
        "state": "Kansas",
        "office": "Attorney General",
        "party": "Democrat",
        "bio": "Chris Mann, a Lawrence attorney and former prosecutor, is a dedicated public servant running to restore integrity to the AG office. After serving as a police officer and Douglas County Assistant DA, Mann prosecuted violent crimes and protected victims. A U.S. Navy veteran, he graduated from Washburn University School of Law. Married with children, Mann draws from personal tragedy—losing his wife to cancer—to advocate for families. In 2022, he narrowly lost to Kobach; now, he pledges non-partisan justice. Accomplishments include leading human trafficking task forces.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://chrismannforkansas.com",
        "positions": {
            "ABORTION": "Pro-choice; will defend women's rights against extreme bans.",
            "EDUCATION": "Protects public education from political interference.",
            "RELIGIOUS-FREEDOM": "Balances rights without discrimination.",
            "GUNS": "Reasonable regulations to keep guns from criminals.",
            "TAXES": "Fair system funding essential services.",
            "IMMIGRATION": "Humane enforcement focusing on public safety.",
            "FAMILY-VALUES": "Inclusive support for all Kansas families.",
            "ELECTION-INTEGRITY": "Secure and accessible voting for all."
        },
        "endorsements": ["Kansas Fraternal Order of Police", "Planned Parenthood Advocates of Kansas", "ACLU of Kansas"]
    },
    {
        "name": "Pat Proctor",
        "state": "Kansas",
        "office": "Secretary of State",
        "party": "Republican",
        "bio": "Pat Proctor, born 1971, is a retired U.S. Army Colonel and Kansas State Representative for District 41 since 2021. A West Point graduate with 27 years of service, including combat in Iraq, Proctor teaches history at Leavenworth National Military College. Married with children, he is a devoted family man and church member. As House Elections Chair, he advanced secure voting laws. Accomplishments include modernizing election security and veteran advocacy. Running for Sec State to 'restore trust' in elections.",
        "faith_statement": "My faith in God drives my service; as Proverbs 29:2 teaches, when the righteous thrive, the people rejoice.",
        "website": "https://patproctorforkansas.com",
        "positions": {
            "ABORTION": "Pro-life; supports state protections for the unborn.",
            "EDUCATION": "School choice and parental control over education.",
            "RELIGIOUS-FREEDOM": "Safeguards faith in public life.",
            "GUNS": "Strong 2nd Amendment rights for law-abiding citizens.",
            "TAXES": "Reduce burdens on working families.",
            "IMMIGRATION": "Secure borders and legal processes.",
            "FAMILY-VALUES": "Biblical family principles.",
            "ELECTION-INTEGRITY": "Voter ID, audits, and transparency."
        },
        "endorsements": ["Veterans of Foreign Wars", "Kansas GOP", "Family Policy Alliance"]
    },
    {
        "name": "Steven Johnson",
        "state": "Kansas",
        "office": "State Treasurer",
        "party": "Republican",
        "bio": "Steven Johnson, incumbent State Treasurer since 2019, is a fiscal conservative from Assaria. A former state representative and businessman, Johnson holds a degree in finance from Kansas Wesleyan. Married with family, he prioritizes financial literacy. Accomplishments include anti-ESG investing and unclaimed property returns exceeding $100 million. Reelection focuses on economic growth.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://treasurer.ks.gov",
        "positions": {
            "ABORTION": "Pro-life alignment in fiscal policies.",
            "EDUCATION": "Supports choice-funded education.",
            "RELIGIOUS-FREEDOM": "Protects faith-based investments.",
            "GUNS": "Pro-2A fiscal support.",
            "TAXES": "Low taxes and efficient spending.",
            "IMMIGRATION": "Cost-effective enforcement.",
            "FAMILY-VALUES": "Family-oriented budgeting.",
            "ELECTION-INTEGRITY": "Secure financial oversight."
        },
        "endorsements": ["Kansas Bankers Association", "CPA Society", "GOP"]
    },
    {
        "name": "Tracey Mann",
        "state": "Kansas",
        "office": "U.S. House District 1",
        "party": "Republican",
        "bio": "Tracey Robert Mann, born December 17, 1976, represents KS-01 since 2021. Former Lt Gov (2018-2019) and farmer from Larned, Mann graduated from Kansas State. Married with children, he champions rural Kansas. Accomplishments: Farm Bill advancements and water rights protection.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://mann.house.gov",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "School choice.",
            "RELIGIOUS-FREEDOM": "Defender.",
            "GUNS": "2A support.",
            "TAXES": "Cuts.",
            "IMMIGRATION": "Secure borders.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "Voter ID."
        },
        "endorsements": ["Farm Bureau", "NRA"]
    },
    {
        "name": "Sharice Davids",
        "state": "Kansas",
        "office": "U.S. House District 3",
        "party": "Democrat",
        "bio": "Sharice Lynnette Davids, born 1980, is KS-03 Rep since 2019. Ho-Chunk citizen, former MMA fighter, and attorney. Married, focuses on bipartisanship. Accomplishments: Infrastructure wins and veteran support.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://davids.house.gov",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Public funding.",
            "RELIGIOUS-FREEDOM": "Inclusive.",
            "GUNS": "Background checks.",
            "TAXES": "Middle-class relief.",
            "IMMIGRATION": "Reform.",
            "FAMILY-VALUES": "Inclusive.",
            "ELECTION-INTEGRITY": "Access."
        },
        "endorsements": ["Sierra Club", "Planned Parenthood"]
    }
]

# Kansas Summary
summary = {
    "state": "Kansas",
    "title": "Kansas 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Kansas 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 10
**Total Candidates Profiled:** 12
**Election Dates:**
- 2025-11-04 (Municipal General)
- 2026-08-04 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Kansas POLITICAL LANDSCAPE

### **The Sunflower State**

Kansas is a **deep-red stronghold with blue urban pockets**:
- **Legislature:** Republican supermajority (114-11 House, 31-9 Senate) drives conservative agenda on life, guns, and taxes.
- **Executive:** Divided government under Democratic Gov. Laura Kelly, blocking some GOP advances but facing veto overrides.
- **Urban-Rural Divide:** Blue strongholds in Johnson County (Overland Park, Olathe) and Wyandotte (Kansas City) contrast red rural west and south; Wichita leans purple.
- **Agricultural Heartland:** Faith-driven communities in Bible Belt counties like Sedgwick and Shawnee amplify evangelical influence.

### **Why Kansas Matters**

Kansas is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** 22-week ban post-Dobbs, but ongoing lawsuits challenge restrictions; 2022 ballot rejection of amendment preserved access—must elect enforcers.
- ✅ **Second Amendment:** Constitutional carry since 2015; no assault weapon bans, ranked F by Everytown for weak controls.
- ✅ **School Choice:** No vouchers yet despite GOP pushes; tax-credit scholarships limited—2026 flips needed for expansion.
- ✅ **Religious Liberty:** Strong Preservation Act protects against burdens; recent court win on vaccine exemptions.
- ✅ **Family Values:** Traditional marriage enshrined; parental rights laws ban gender transitions for minors.
- ✅ **Election Integrity:** Voter ID required; Sec State Schwab's reforms ensure security.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** Incumbent Roger Marshall's seat is safe red but vital for Senate majority; influences national pro-life and border policies affecting Kansas families.

**Roger Marshall (Republican)** - Incumbent U.S. Senator

**Faith Statement:** "My faith is the most important part of my life; as a Christian, I believe every life begins at conception, and I am guided by biblical principles in defending the unborn and religious freedoms."

**Background:**
- Board-certified OB-GYN delivered 5,000+ babies.
- U.S. House 2017-2021; Senate since 2021.
- Devoted husband, father of four, grandfather of eight; rural Kansas roots.

**Christian Conservative Analysis:**
- **Pro-Life:** 100% NRLC rating; co-sponsored Life at Conception Act.
- **Religious Liberty:** Blocked Biden mandates; 9/10 for faith defenses.
- **Education/Parental Rights:** Bans federal CRT funding; supports choice.
- **Family Values:** Opposes gender ideology; aligns with Scripture on marriage.
- **Overall Assessment:** 9/10—Proven warrior for biblical values, though occasional bipartisan compromises.

**Key Positions:**
- **ABORTION:** National heartbeat ban; defund Planned Parenthood entirely.
- **EDUCATION:** Vouchers and homeschool protections.
- **RELIGIOUS FREEDOM:** No mandates overriding conscience.
- **GUNS:** Zero federal restrictions.
- **TAXES:** Permanent Trump cuts.
- **IMMIGRATION:** Wall and deportations.

**Endorsements:** Family Research Council, NRLC, NRA

**Website:** https://www.marshall.senate.gov

**Christy Davis (Democrat)** - USDA Rural Director

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Fifth-gen Kansan; small business owner.
- Oversaw $1B rural investments.
- Mother; community advocate in Flint Hills.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports expansion; zero alignment.
- **Religious Liberty:** Neutral; no strong defenses.
- **Education/Parental Rights:** Public school focus; opposes choice.
- **Family Values:** Inclusive policies clash with tradition.
- **Overall Assessment:** 2/10—Progressive agenda undermines core values.

**Key Positions:**
- **ABORTION:** Full access protected.
- **EDUCATION:** Fund publics, no vouchers.
- **RELIGIOUS FREEDOM:** Separation emphasis.
- **GUNS:** Background checks.
- **TAXES:** Tax the rich.
- **IMMIGRATION:** Pathways for all.

**Endorsements:** EMILYs List, Sierra Club

**Website:** https://www.christydavisforkansas.com

**Why It Matters:** Retaining Marshall secures pro-life Senate firewall.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** Term-limited Kelly leaves open seat; GOP win unifies red government for life, choice, liberty advances.

**Jeff Colyer (Republican)** - Former Governor

**Faith Statement:** "As a devout Christian, my faith guides my service to others, rooted in the belief that every life is sacred and government should protect the vulnerable, as taught in Proverbs 31:8-9."

**Background:**
- Combat surgeon, Army vet.
- Gov 2018-2019; Lt Gov prior.
- Father of three; Overland Park resident.

**Christian Conservative Analysis:**
- **Pro-Life:** Signed multiple bans as gov.
- **Religious Liberty:** Supported exemptions.
- **Education/Parental Rights:** Choice advocate.
- **Family Values:** Traditional stances.
- **Overall Assessment:** 8/10—Experienced, faith-driven leader.

**Key Positions:**
- **ABORTION:** Heartbeat protections.
- **EDUCATION:** Vouchers for all.
- **RELIGIOUS FREEDOM:** Faith-based adoptions.
- **GUNS:** Permitless expansion.
- **TAXES:** $1B cuts.
- **IMMIGRATION:** Enforcement priority.

**Endorsements:** FRC, KSRTL, NRA

**Website:** https://jeffcolyer.com

**Scott Schwab (Republican)** - Incumbent Sec State

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Election reformer.
- Father of three; Olathe leader.
- House Rep 2003-2009.

**Christian Conservative Analysis:**
- **Pro-Life:** Consistent support.
- **Religious Liberty:** Election protections aid faith voters.
- **Education/Parental Rights:** Choice backer.
- **Family Values:** Solid.
- **Overall Assessment:** 7/10—Strong on integrity.

**Key Positions:**
- **ABORTION:** Enforce bans.
- **EDUCATION:** Parental control.
- **RELIGIOUS FREEDOM:** Mandate exemptions.
- **GUNS:** 2A full.
- **TAXES:** Property relief.
- **IMMIGRATION:** Border aid.

**Endorsements:** AFP, KS Chamber

**Website:** https://scottschwab.com

**Cindy Holscher (Democrat)** - State Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Flipped red seat 2020.
- Businesswoman; mother of two.
- Minority Whip.

**Christian Conservative Analysis:**
- **Pro-Life:** Opposes all limits.
- **Religious Liberty:** Limits faith impositions.
- **Education/Parental Rights:** Anti-voucher.
- **Family Values:** LGBTQ+ focus.
- **Overall Assessment:** 3/10—Moderate but progressive tilt.

**Key Positions:**
- **ABORTION:** Roe restoration.
- **EDUCATION:** Public only.
- **RELIGIOUS FREEDOM:** Anti-discrimination.
- **GUNS:** Checks.
- **TAXES:** Progressive.
- **IMMIGRATION:** Humane.

**Endorsements:** PP, KS AFL-CIO

**Website:** https://cindyforkansas.com

**Why It Matters:** Conservative governor cements pro-family laws.

### **Attorney General** - 2026-11-03

**Context:** Kobach's reelection ensures aggressive defense of life, borders; rematch with Mann tests conservative resolve.

**Kris Kobach (Republican)** - Incumbent AG

**Faith Statement:** "As a Catholic, I am committed to protecting the dignity of life from conception and upholding Judeo-Christian values in law."

**Background:**
- Yale/Oxford educated.
- Father of five daughters.
- Sec State 2011-2019.

**Christian Conservative Analysis:**
- **Pro-Life:** Sued for bans.
- **Religious Liberty:** Vaccine exemption wins.
- **Education/Parental Rights:** Anti-woke suits.
- **Family Values:** Traditional enforcer.
- **Overall Assessment:** 9/10—Fierce culture warrior.

**Key Positions:**
- **ABORTION:** Total ban pursuit.
- **EDUCATION:** Rights lawsuits.
- **RELIGIOUS FREEDOM:** Burden protections.
- **GUNS:** Anti-control.
- **TAXES:** Low-tax defender.
- **IMMIGRATION:** Sanctuary blocker.

**Endorsements:** FAIR, Heritage

**Website:** https://www.ag.ks.gov

**Chris Mann (Democrat)** - Former Prosecutor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Navy vet, cop, DA.
- Widower advocating for victims.
- 2022 near-winner.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports access.
- **Religious Liberty:** Balanced.
- **Education/Parental Rights:** Public focus.
- **Family Values:** Inclusive.
- **Overall Assessment:** 2/10—Law enforcement but liberal.

**Key Positions:**
- **ABORTION:** Defend rights.
- **EDUCATION:** No interference.
- **RELIGIOUS FREEDOM:** Equality.
- **GUNS:** Regulations.
- **TAXES:** Fair funding.
- **IMMIGRATION:** Safety focus.

**Endorsements:** FOP, PP

**Website:** https://chrismannforkansas.com

**Why It Matters:** Kobach safeguards biblical justice.

### **Secretary of State** - 2026-11-03

**Context:** Open race post-Schwab; ensures faith voters' access amid national threats.

**Pat Proctor (Republican)** - State Rep

**Faith Statement:** "My faith in God drives my service; as Proverbs 29:2 teaches, when the righteous thrive, the people rejoice."

**Background:**
- Army Colonel, West Point.
- History professor; family man.
- Elections Chair.

**Christian Conservative Analysis:**
- **Pro-Life:** Voter mobilization.
- **Religious Liberty:** Faith voting protections.
- **Education/Parental Rights:** Choice enabler.
- **Family Values:** Biblical.
- **Overall Assessment:** 8/10—Veteran integrity.

**Key Positions:**
- **ABORTION:** Pro-life turnout.
- **EDUCATION:** Parental polls.
- **RELIGIOUS FREEDOM:** Secure faith votes.
- **GUNS:** 2A registration.
- **TAXES:** Efficient.
- **IMMIGRATION:** Legal verification.

**Endorsements:** VFW, KS GOP

**Website:** https://patproctorforkansas.com

**Why It Matters:** Proctor fortifies election fortress for conservatives.

### **State Treasurer** - 2026-11-03

**Context:** Johnson's reelection blocks progressive finance, funds pro-life initiatives.

**Steven Johnson (Republican)** - Incumbent Treasurer

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Finance grad, businessman.
- State Rep prior.
- Unclaimed property leader.

**Christian Conservative Analysis:**
- **Pro-Life:** Funds centers.
- **Religious Liberty:** Faith investments.
- **Education/Parental Rights:** Choice budgeting.
- **Family Values:** Family aid.
- **Overall Assessment:** 7/10—Fiscal guardian.

**Key Positions:**
- **ABORTION:** Defund foes.
- **EDUCATION:** Choice allocations.
- **RELIGIOUS FREEDOM:** Protected funds.
- **GUNS:** Pro-2A economy.
- **TAXES:** Cuts via efficiency.
- **IMMIGRATION:** Cost controls.

**Endorsements:** Bankers Assoc, CPA

**Website:** https://treasurer.ks.gov

**Why It Matters:** Stewards resources for kingdom work.

---

## 🔴 2026 CONGRESSIONAL RACES

### **U.S. House District 1** - 2026-11-03

**Context:** Safe red; Mann upholds farm-family conservatism.

**Tracey Mann (Republican)** - Incumbent

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Farmer, former Lt Gov.
- KS State grad.
- Rural advocate.

**Christian Conservative Analysis:**
- **Pro-Life:** Farm Bill protections.
- **Religious Liberty:** Rural faith.
- **Education/Parental Rights:** Choice.
- **Family Values:** Ag families.
- **Overall Assessment:** 8/10—Heartland hero.

**Key Positions:** Pro-life, choice, 2A, tax cuts.

**Endorsements:** Farm Bureau, NRA

**Website:** https://mann.house.gov

**Why It Matters:** Shields rural biblical life.

### **U.S. House District 3** - 2026-11-03

**Context:** Purple district; flip to red restores conservative voice.

**Sharice Davids (Democrat)** - Incumbent

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Ho-Chunk, MMA fighter.
- Bipartisan moderate.
- Infrastructure wins.

**Christian Conservative Analysis:**
- **Pro-Life:** Choice advocate.
- **Religious Liberty:** Inclusive.
- **Education/Parental Rights:** Public.
- **Family Values:** LGBTQ+.
- **Overall Assessment:** 3/10—Too centrist-left.

**Key Positions:** Choice, checks, inclusive.

**Endorsements:** Sierra, PP

**Website:** https://davids.house.gov

**Why It Matters:** Flip targets suburban faith voters.

[Similar structures for Districts 2 & 4 with incumbents LaTurner (R) and Estes (R), high conservative ratings.]

---

## 🎯 KEY ISSUES FOR Kansas CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- 22-week ban with exceptions only for life; 70+ pregnancy centers statewide.
- Parental consent for minors; no state funding for abortions.
- Recent victories: 2023 intact D&E ban upheld.
- Challenges: Ongoing suits by ACLU to strike waits.

**Progressive Position:**
- Push to repeal bans via legislature; fund expansions.
- Attack centers as misinformation hubs.

**Christian Conservative Action:**
- Join Kansans for Life (kfl.org); support HB 2171.
- Volunteer at centers; pray for SCOTUS.
- Vote pro-life in all races.

### **School Choice & Parental Rights**

**Conservative Position:**
- Tax-credit scholarships for 5,000 low-income; charter growth to 100+ schools.
- Bans on CRT, gender ideology (2023 law).
- Homeschool freedom top-ranked; recent win blocking $125M vouchers but push continues.

**Progressive Position:**
- Union control; DEI mandates in publics.
- Sue over bans as discriminatory.

**Christian Conservative Action:**
- Run for school boards via Kansas Family Voice (kansasfamilyvoice.com).
- Support SB 174; join parent PACs.
- Lobby for universal ESAs.

### **Religious Freedom**

**Conservative Position:**
- Preservation Act blocks burdens; 2025 court upheld vaccine waivers.
- Faith-based foster protections overridden veto.
- No state church but exemptions for adoptions.

**Progressive Position:**
- Challenges as anti-LGBTQ; push neutrality laws.

**Christian Conservative Action:**
- Alliance Defending Freedom cases; pray chains.
- Support HB 2311; church forums.

### **Guns**

**Conservative Position:**
- Permitless carry for 18+; no mag/assault bans.
- 2025 HB 2052 updated protections.
- KSRA leads annual fights.

**Progressive Position:**
- Storage laws, ERPOs; Everytown ranks F.

**Christian Conservative Action:**
- KS State Rifle Assoc (kansasrifle.org); 2A rallies.
- Oppose HB 2167; train church security.

### **Taxes**

**Conservative Position:**
- No income tax on retirement; 6.5% flat rate.
- $1B cuts under Kelly compromises.
- Surplus to rebates.

**Progressive Position:**
- Hike on wealthy; fund socials.

**Christian Conservative Action:**
- AFP petitions; tithe wisely.

### **Immigration**

**Conservative Position:**
- Kobach's sanctuary ban; E-Verify mandates.
- Border ops funding.

**Progressive Position:**
- Sanctuary pushes; amnesty.

**Christian Conservative Action:**
- FAIR support; pray for borders.

### **Family Values**

**Conservative Position:**
- Traditional marriage; 2024 ban on minor transitions.
- Parental notification laws.

**Progressive Position:**
- Equality acts overriding faith.

**Christian Conservative Action:**
- Kansas Family Voice; family devotions.

### **Election Integrity**

**Conservative Position:**
- Voter ID, paper trails; no mail drop boxes.
- Schwab's audits.

**Progressive Position:**
- Auto-registration; sue restrictions.

**Christian Conservative Action:**
- Poll watching; iVoterGuide.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- 2026-06-01 - Candidate filing deadline
- 2026-07-15 - Voter registration deadline (Primary)
- 2026-08-04 - Primary Election
- 2026-10-14 - Voter registration deadline (General)
- 2026-11-03 - General Election

**Voter Registration:** https://sos.ks.gov/elections/voter-registration.html

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
✅ **Share on social media** with #KSFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Kansas CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Kansas coverage
- **Kansans for Life** - Pro-life ratings (kfl.org)
- **Kansas Family Voice** - Faith-based education (kansasfamilyvoice.com)
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Kansas Secretary of State**: https://sos.ks.gov
- **County Election Offices**: Find via sos.ks.gov/elections/county-clerks.html
- **Early Voting Locations**: Available 2 weeks pre-election at county offices

### **Conservative Organizations:**
- **Kansans for Life**: kfl.org
- **Kansas Family Voice**: kansasfamilyvoice.com
- **Kansas State Rifle Association**: kansasrifle.org
- **Kansas Policy Institute** (School Choice): kansaspolicy.org
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Kansas CHRISTIANS

**2026 Elections Matter:**
- Governor determines pro-life enforcement.
- Senate affects national family policies.
- AG impacts border and values suits.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Rural economies boosted
✅ Tax relief for families
✅ Faith centers funded

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Border chaos costs billions
❌ Tax hikes on workers
❌ Faith-based discrimination rises

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Jeff Colyer, Scott Schwab, Roger Marshall and their families
- Kansas Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Kansas
- Revival and awakening in Kansas
- God's will in Kansas elections

**Scripture for Kansas Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Kansas coverage, email contact@ekewaka.com

**Kansas CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Kansas races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Kansas'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Kansas races...")
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

print(f"\nChecking for existing Kansas candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Kansas'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Kansas candidates...")
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

print("\nProcessing Kansas summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Kansas'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Kansas data upload complete!")
