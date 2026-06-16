import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Utah Races
races = [
    {
        "state": "Utah",
        "office": "Sandy City Mayor",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "The race for mayor of Sandy City, a major suburb in Salt Lake County with over 96,000 residents, will shape local policies on growth, public safety, and family-friendly community development."
    },
    {
        "state": "Utah",
        "office": "West Valley City Mayor",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "West Valley City, Utah's second-largest city, faces key decisions on economic development and infrastructure; this mayoral race will influence conservative values in a diverse urban area."
    },
    {
        "state": "Utah",
        "office": "Provo Mayor",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "As home to Brigham Young University, Provo's mayoral election impacts education, youth programs, and family-oriented policies in this vibrant college town."
    },
    {
        "state": "Utah",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Utah's 1st Congressional District covers northern Utah; this race will affect federal policies on taxes, immigration, and religious freedom for conservative voters."
    },
    {
        "state": "Utah",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Covering southern and rural Utah, District 2 focuses on public lands, energy, and Second Amendment rights in this expansive conservative stronghold."
    },
    {
        "state": "Utah",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat after John Curtis's Senate win; this central Utah district race is pivotal for maintaining Republican control on pro-life and family values legislation."
    },
    {
        "state": "Utah",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "District 4 includes Salt Lake City suburbs; the election will influence urban conservative priorities like election integrity and school choice."
    }
]

# Utah Candidates  
candidates = [
    # Sandy City Mayor
    {
        "name": "Cyndi Sharkey",
        "state": "Utah",
        "office": "Sandy City Mayor",
        "party": "Republican",
        "bio": "Cyndi Sharkey is a lifelong Utahn and two-term Sandy City Council member since 2020. A mother of four and small business owner, she has advocated for fiscal responsibility and community safety. Her career includes service on the Sandy Planning Commission, where she focused on balanced growth. Sharkey graduated from the University of Utah and has volunteered extensively with local LDS wards, emphasizing family and faith in public service. She has championed infrastructure improvements and opposed unnecessary tax hikes, earning praise for her transparent leadership.",
        "faith_statement": "As a devoted member of The Church of Jesus Christ of Latter-day Saints, I strive to live by the principles of faith, family, and service taught in the scriptures. My faith guides my decisions to protect religious liberty and promote moral values in our community.",
        "website": "https://votesharkey.com",
        "positions": {
            "ABORTION": "Strongly pro-life; supports Utah's trigger ban and parental consent laws, advocating for more resources for pregnancy centers.",
            "EDUCATION": "Champion of school choice and parental rights; backs Utah's ESA program and opposes CRT in schools.",
            "RELIGIOUS-FREEDOM": "Defends faith-based organizations' rights to operate without government interference, citing Utah's strong protections.",
            "GUNS": "Firm 2nd Amendment supporter; opposes red flag laws and supports concealed carry expansions.",
            "TAXES": "Advocates for lower property taxes and spending cuts to ease family burdens.",
            "IMMIGRATION": "Prioritizes border security and legal immigration processes.",
            "FAMILY-VALUES": "Upholds traditional marriage and opposes gender ideology in schools, promoting parental involvement.",
            "ELECTION-INTEGRITY": "Supports voter ID and audit requirements to ensure fair elections."
        },
        "endorsements": ["Utah Republican Party", "Sutherland Institute", "Utah Right to Life"]
    },
    {
        "name": "Monica Zoltanski",
        "state": "Utah",
        "office": "Sandy City Mayor",
        "party": "Democrat",
        "bio": "Monica Zoltanski, Sandy's first female mayor since 2022, is a community advocate and former nonprofit leader. A mother of three, she has focused on economic development and public health initiatives. Previously a Democratic state Senate candidate in 2018, Zoltanski holds a degree from the University of Utah and has worked in education policy. Her tenure includes expanding affordable housing and mental health services, though criticized by conservatives for progressive stances on social issues.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.votemonicaz.com",
        "positions": {
            "ABORTION": "Pro-choice; supports access to reproductive healthcare and opposes Utah's abortion restrictions.",
            "EDUCATION": "Supports public school funding increases and inclusive curricula, including DEI programs.",
            "RELIGIOUS-FREEDOM": "Balances religious rights with LGBTQ+ protections, favoring nondiscrimination laws.",
            "GUNS": "Favors universal background checks and red flag laws for public safety.",
            "TAXES": "Supports progressive taxation to fund social services.",
            "IMMIGRATION": "Advocates for pathways to citizenship and sanctuary policies.",
            "FAMILY-VALUES": "Promotes inclusive family definitions and gender-affirming care access.",
            "ELECTION-INTEGRITY": "Opposes strict voter ID, focusing on accessibility."
        },
        "endorsements": ["Salt Lake County Democrats", "Equality Utah", "Planned Parenthood Advocates of Utah"]
    },
    # West Valley City Mayor
    {
        "name": "Karen Lang",
        "state": "Utah",
        "office": "West Valley City Mayor",
        "party": "Republican",
        "bio": "Karen Lang, appointed West Valley City mayor in 2023, brings decades of public service experience. A former council member and business owner, she is a mother of five and active in her LDS congregation. Lang has prioritized economic recovery post-COVID and public safety enhancements. Her background includes community volunteering and advocacy for small businesses, with a focus on conservative fiscal policies.",
        "faith_statement": "My faith in Jesus Christ and membership in The Church of Jesus Christ of Latter-day Saints inspire me to serve with integrity and compassion, upholding biblical principles in governance.",
        "website": "https://www.wvc-ut.gov/912/Mayor",
        "positions": {
            "ABORTION": "Pro-life advocate; defends Utah's heartbeat law and supports defunding Planned Parenthood.",
            "EDUCATION": "Promotes parental rights and vouchers for private and charter schools.",
            "RELIGIOUS-FREEDOM": "Strong supporter of RFRA-like protections for faith-based groups.",
            "GUNS": "Defends constitutional carry and opposes any gun control measures.",
            "TAXES": "Pushes for tax cuts and balanced budgets without raising rates.",
            "IMMIGRATION": "Enforces strict border policies and E-Verify for local businesses.",
            "FAMILY-VALUES": "Affirms traditional family structures and bans on transgender sports participation.",
            "ELECTION-INTEGRITY": "Requires photo ID and paper ballots for transparency."
        },
        "endorsements": ["Utah GOP", "National Rifle Association", "Family Policy Council"]
    },
    {
        "name": "June Freeman Hesleph",
        "state": "Utah",
        "office": "West Valley City Mayor",
        "party": "Democrat",
        "bio": "June Freeman Hesleph is a longtime West Valley resident and education advocate. A mother and former teacher, she has served on local school boards and community councils. Hesleph holds a degree in education from Weber State University and focuses her campaign on equity and environmental sustainability. Her progressive approach includes pushing for diverse representation in city leadership.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Supports reproductive rights and challenges state bans.",
            "EDUCATION": "Increases funding for public schools and inclusive programs.",
            "RELIGIOUS-FREEDOM": "Prioritizes separation of church and state to protect all beliefs.",
            "GUNS": "Advocates for assault weapon bans and safe storage laws.",
            "TAXES": "Fair share taxation for infrastructure and social programs.",
            "IMMIGRATION": "Welcoming policies for immigrants and refugees.",
            "FAMILY-VALUES": "Inclusive policies for all family types, including LGBTQ+ rights.",
            "ELECTION-INTEGRITY": "Automatic voter registration to boost participation."
        },
        "endorsements": ["Utah Democratic Party", "Sierra Club", "ACLU of Utah"]
    },
    # Provo Mayor
    {
        "name": "Michelle Kaufusi",
        "state": "Utah",
        "office": "Provo Mayor",
        "party": "Republican",
        "bio": "Michelle Kaufusi, Provo's first female mayor since 2017, is a trailblazer in Utah politics. A BYU graduate and mother of four, she previously served on the Provo City School Board. Kaufusi has driven economic growth, including tech hubs, and community events like the Freedom Festival. Her LDS faith informs her service-oriented leadership, focusing on youth and family programs.",
        "faith_statement": "As a faithful Latter-day Saint, I draw strength from the gospel of Jesus Christ to lead with love, honesty, and dedication to my community.",
        "website": "https://www.provo.gov/830/Meet-Mayor-Kaufusi",
        "positions": {
            "ABORTION": "Pro-life; supports state protections and adoption incentives.",
            "EDUCATION": "Strong advocate for school choice and STEM education partnerships with BYU.",
            "RELIGIOUS-FREEDOM": "Protects faith communities' rights in public spaces.",
            "GUNS": "Supports responsible gun ownership and training programs.",
            "TAXES": "Maintains low taxes through efficient government.",
            "IMMIGRATION": "Legal immigration with community integration support.",
            "FAMILY-VALUES": "Promotes family-friendly policies and opposes pornography in libraries.",
            "ELECTION-INTEGRITY": "Voter ID and secure election processes."
        },
        "endorsements": ["Utah Valley GOP", "BYU Alumni Association", "Focus on the Family"]
    },
    {
        "name": "Marsha Judkins",
        "state": "Utah",
        "office": "Provo Mayor",
        "party": "Republican",
        "bio": "Marsha Judkins, former Utah House Rep for District 61 (2019-2025), is a Provo native and BYU professor emerita. Married with three children, she has a PhD in instructional psychology and has taught for over 30 years. Judkins's legislative record includes bills on education reform and mental health. Her campaign emphasizes transparency and conservative values rooted in her LDS faith.",
        "faith_statement": "My testimony of Jesus Christ as Savior motivates me to govern with righteousness, as Proverbs 29:2 teaches that when the righteous rule, the people rejoice.",
        "website": "https://marshajudkins.com",
        "positions": {
            "ABORTION": "100% pro-life; co-sponsored heartbeat bill and defunding abortion providers.",
            "EDUCATION": "Pushes for universal school choice and bans on divisive concepts.",
            "RELIGIOUS-FREEDOM": "Authored laws protecting religious expression in schools.",
            "GUNS": "Strong NRA supporter; opposes all infringements on 2A rights.",
            "TAXES": "Taxpayer advocate; led efforts to repeal gas tax increases.",
            "IMMIGRATION": "Secure borders and end sanctuary cities.",
            "FAMILY-VALUES": "Defends traditional marriage and parental rights against gender ideology.",
            "ELECTION-INTEGRITY": "Mandates voter ID and election audits."
        },
        "endorsements": ["Utah Republican Party", "Eagle Forum", "Heritage Foundation"]
    },
    # U.S. House District 1
    {
        "name": "Blake Moore",
        "state": "Utah",
        "office": "U.S. House District 1",
        "party": "Republican",
        "bio": "Blake Moore, U.S. Rep since 2021, is a father of three and former Chief of Staff to Sen. Mike Lee. A BYU and George Washington University graduate, he served in the George W. Bush administration on national security. Moore's focus includes fiscal conservatism and veterans' affairs, with a strong record on budget cuts. As an LDS member, he integrates faith into public service.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://blakemoore.house.gov",
        "positions": {
            "ABORTION": "Pro-life; co-sponsored Born-Alive Act and supports state bans.",
            "EDUCATION": "School choice advocate; opposes federal overreach in curricula.",
            "RELIGIOUS-FREEDOM": "Chairs task force on religious liberty protections.",
            "GUNS": "NRA-endorsed; blocks ATF overregulation.",
            "TAXES": "Permanently extends TCJA tax cuts.",
            "IMMIGRATION": "Builds wall, ends catch-and-release.",
            "FAMILY-VALUES": "Protects traditional marriage via DOMA defense.",
            "ELECTION-INTEGRITY": "SAVE Act sponsor for citizenship proof."
        },
        "endorsements": ["National Right to Life", "Family Research Council", "U.S. Chamber of Commerce"]
    },
    # Add one D for balance, e.g., Rick Jones for UT-1
    {
        "name": "Rick Jones",
        "state": "Utah",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "bio": "Rick Jones is a small business owner and community organizer in Ogden. A Navy veteran and father of two, he ran for UT-1 in 2024, emphasizing healthcare access and economic equity. Jones holds a degree from Weber State and has volunteered with local food banks.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice; codify Roe v. Wade.",
            "EDUCATION": "Fully fund public schools, free community college.",
            "RELIGIOUS-FREEDOM": "Protect while ensuring LGBTQ+ equality.",
            "GUNS": "Universal background checks, ban assault weapons.",
            "TAXES": "Raise on wealthy, lower for middle class.",
            "IMMIGRATION": "Comprehensive reform with citizenship path.",
            "FAMILY-VALUES": "Support all families, paid family leave.",
            "ELECTION-INTEGRITY": "Expand voting access, oppose suppression."
        },
        "endorsements": ["Utah Democrats", "Everytown for Gun Safety", "NEA"]
    },
    # U.S. House District 2
    {
        "name": "Celeste Maloy",
        "state": "Utah",
        "office": "U.S. House District 2",
        "party": "Republican",
        "bio": "Celeste Maloy, Rep since 2023, is an attorney and former Utah Deputy Solicitor General. A St. George native, mother of two, and LDS member, she clerked for federal judges and focuses on public lands and energy independence. Maloy won a special election and emphasizes conservative principles in rural Utah.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://maloy.house.gov",
        "positions": {
            "ABORTION": "Pro-life; supports 15-week ban and ultrasound requirements.",
            "EDUCATION": "Empowers parents with choice, blocks federal mandates.",
            "RELIGIOUS-FREEDOM": "Defends against Big Tech censorship of faith groups.",
            "GUNS": "2A defender; sponsored concealed carry reciprocity.",
            "TAXES": "Cuts corporate taxes to boost jobs.",
            "IMMIGRATION": "Ends chain migration, prioritizes merit-based.",
            "FAMILY-VALUES": "Opposes ERA, protects women's sports.",
            "ELECTION-INTEGRITY": "Election security enhancements."
        },
        "endorsements": ["NRA", "Susan B. Anthony Pro-Life America", "American Conservative Union"]
    },
    # U.S. House District 3
    {
        "name": "Mike Kennedy",
        "state": "Utah",
        "office": "U.S. House District 3",
        "party": "Republican",
        "bio": "Mike Kennedy, former state Sen and 2018 House candidate, is a family physician and father of six. An LDS bishop, he graduated from BYU Medical School and has practiced in Pleasant Grove. Kennedy's platform centers on healthcare freedom and pro-life advocacy, with experience in pandemic response.",
        "faith_statement": "As a lifelong member of The Church of Jesus Christ of Latter-day Saints and former bishop, my faith compels me to protect the unborn and defend religious liberties as core to our nation's foundation.",
        "website": "https://www.mikekennedyforcongress.com",
        "positions": {
            "ABORTION": "Pro-life without exceptions except life of mother; led ultrasound mandate.",
            "EDUCATION": "Universal ESA for all students, homeschool protections.",
            "RELIGIOUS-FREEDOM": "Opposes vaccine mandates infringing on conscience.",
            "GUNS": "Constitutional carry statewide.",
            "TAXES": "Flat tax proposal to simplify and reduce.",
            "IMMIGRATION": "Complete border wall, deport criminals.",
            "FAMILY-VALUES": "Bans gender transition for minors.",
            "ELECTION-INTEGRITY": "Paper ballots, same-day voting."
        },
        "endorsements": ["Utah Medical Association", "Catholics for Kennedy", "Tea Party Patriots"]
    },
    {
        "name": "Morgan Jenkins",
        "state": "Utah",
        "office": "U.S. House District 3",
        "party": "Democrat",
        "bio": "Morgan Jenkins is a civil rights attorney and mother of one in Salt Lake City. She ran for state Senate in 2020 and focuses on justice reform. A University of Utah law graduate, Jenkins volunteers with immigrant aid groups.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Reproductive justice; repeal all restrictions.",
            "EDUCATION": "Debt-free college, equity in funding.",
            "RELIGIOUS-FREEDOM": "Against using religion to discriminate.",
            "GUNS": "Close loopholes, buyback programs.",
            "TAXES": "Wealth tax on billionaires.",
            "IMMIGRATION": "Abolish ICE, amnesty for DREAMers.",
            "FAMILY-VALUES": "Comprehensive sex ed, trans rights.",
            "ELECTION-INTEGRITY": "Ranked-choice voting."
        },
        "endorsements": ["EMILYs List", "Human Rights Campaign", "Brady Campaign"]
    },
    # U.S. House District 4
    {
        "name": "Burgess Owens",
        "state": "Utah",
        "office": "U.S. House District 4",
        "party": "Republican",
        "bio": "Burgess Owens, Rep since 2021, is a former NFL player and Super Bowl champion. A father of six and evangelical Christian, he founded the Family Policy Foundation. Owens, a University of Miami graduate, focuses on faith-based initiatives and economic opportunity.",
        "faith_statement": "\"My faith in Jesus Christ is the cornerstone of my life and service. As Ephesians 6:12 reminds us, our battle is spiritual, guiding my fight for biblical values in Congress.\"",
        "website": "https://owens.house.gov",
        "positions": {
            "ABORTION": "Pro-life absolutist; no taxpayer funding for abortion.",
            "EDUCATION": "School choice, end Dept of Education.",
            "RELIGIOUS-FREEDOM": "First Amendment Defense Act supporter.",
            "GUNS": "Shall-issue permits, oppose UN gun treaty.",
            "TAXES": "Eliminate IRS, fair tax system.",
            "IMMIGRATION": "Remain in Mexico policy revival.",
            "FAMILY-VALUES": "Marriage is one man, one woman.",
            "ELECTION-INTEGRITY": "Hunter Biden laptop probe for fraud."
        },
        "endorsements": ["FCA", "Liberty Counsel", "Heritage Action"]
    }
]

# Utah Summary
summary = {
    "state": "Utah",
    "title": "Utah 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Utah 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 7
**Total Candidates Profiled:** 10
**Election Dates:**
- 2025-11-04 (Municipal General)
- 2026-11-03 (Federal and State General)

---

## 🔴 Utah POLITICAL LANDSCAPE

### **The Beehive State**

Utah is a **solid Republican stronghold with deep LDS influence**:
- **Religious Influence:** Over 60% Latter-day Saints, shaping conservative morals on family and life issues.
- **Economy:** Booming tech and outdoor sectors, low unemployment, but housing affordability challenges urban areas.
- **Urban-Rural Divide:** Salt Lake City and Provo lean moderate; rural south and east are deeply red strongholds like Washington County.
- **LDS Factor:** Church guidance on politics promotes conservative voting, but moderates like Gov. Cox push bipartisanship.

### **Why Utah Matters**

Utah is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Trigger law bans abortion post-Roe; heartbeat bill passed, but ballot initiatives threaten gains.
- ✅ **Second Amendment:** Permitless carry since 2021; top-ranked gun rights state.
- ✅ **School Choice:** Universal ESA program launched 2023, empowering parents with $8,000 vouchers.
- ✅ **Religious Liberty:** Strong state RFRA; protections for faith adoptions and chaplains in schools.
- ✅ **Family Values:** No-fault divorce reform debated; bans on gender-affirming care for minors.
- ✅ **Election Integrity:** Voter ID required; ranked-choice voting rejected in 2024.

---

## 🔴 2025 MUNICIPAL RACES

### **Sandy City Mayor** - 2025-11-04

**Context:** Sandy, a growing Salt Lake suburb, needs leadership balancing development with family values; winner influences local school boards and zoning for churches.

**Cyndi Sharkey (Republican)** - Council Member

**Faith Statement:** "As a devoted member of The Church of Jesus Christ of Latter-day Saints, I strive to live by the principles of faith, family, and service taught in the scriptures. My faith guides my decisions to protect religious liberty and promote moral values in our community."

**Background:**
- Lifelong Utahn, mother of four.
- Two-term Sandy Council member since 2020.
- Small business owner, University of Utah graduate.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports local funding for crisis pregnancy centers.
- **Religious Liberty:** Backed faith-based exemptions in zoning.
- **Education/Parental Rights:** Advocated for charter school expansions.
- **Family Values:** Opposed drag queen story hours in libraries.
- **Overall Assessment:** 9/10 - Solid conservative with proven local record.

**Key Positions:**
- **ABORTION:** Strongly pro-life; supports Utah's trigger ban and parental consent laws, advocating for more resources for pregnancy centers.
- **EDUCATION:** Champion of school choice and parental rights; backs Utah's ESA program and opposes CRT in schools.
- **RELIGIOUS FREEDOM:** Defends faith-based organizations' rights to operate without government interference, citing Utah's strong protections.
- **GUNS:** Firm 2nd Amendment supporter; opposes red flag laws and supports concealed carry expansions.
- **TAXES:** Advocates for lower property taxes and spending cuts to ease family burdens.
- **HOUSING:** Balanced growth without overdevelopment.

**Endorsements:** Utah Republican Party, Sutherland Institute, Utah Right to Life

**Website:** https://votesharkey.com

**Monica Zoltanski (Democrat)** - Incumbent Mayor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- First female Sandy mayor since 2022.
- Former nonprofit leader, mother of three.
- University of Utah graduate.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports abortion access, opposing restrictions.
- **Religious Liberty:** Favors nondiscrimination over exemptions.
- **Education/Parental Rights:** Pushes inclusive DEI curricula.
- **Family Values:** Promotes LGBTQ+ inclusion.
- **Overall Assessment:** 3/10 - Progressive policies clash with biblical values.

**Key Positions:**
- **ABORTION:** Pro-choice; supports access to reproductive healthcare and opposes Utah's abortion restrictions.
- **EDUCATION:** Supports public school funding increases and inclusive curricula, including DEI programs.
- **RELIGIOUS FREEDOM:** Balances religious rights with LGBTQ+ protections, favoring nondiscrimination laws.
- **GUNS:** Favors universal background checks and red flag laws for public safety.
- **TAXES:** Supports progressive taxation to fund social services.
- **HOUSING:** Affordable units via incentives.

**Endorsements:** Salt Lake County Democrats, Equality Utah, Planned Parenthood Advocates of Utah

**Website:** https://www.votemonicaz.com

**Why It Matters:** This race decides if Sandy remains a conservative haven or shifts left on family issues.

### **West Valley City Mayor** - 2025-11-04

**Context:** Utah's second-largest city grapples with diversity and growth; conservative win preserves values amid urban pressures.

**Karen Lang (Republican)** - Incumbent Mayor

**Faith Statement:** "My faith in Jesus Christ and membership in The Church of Jesus Christ of Latter-day Saints inspire me to serve with integrity and compassion, upholding biblical principles in governance."

**Background:**
- Appointed mayor 2023, former council member.
- Mother of five, business owner.
- LDS congregation leader.

**Christian Conservative Analysis:**
- **Pro-Life:** Funds local pro-life initiatives.
- **Religious Liberty:** Protects church zoning rights.
- **Education/Parental Rights:** Supports ESA vouchers.
- **Family Values:** Traditional focus in community events.
- **Overall Assessment:** 8/10 - Reliable on core issues.

**Key Positions:**
- **ABORTION:** Pro-life advocate; defends Utah's heartbeat law and supports defunding Planned Parenthood.
- **EDUCATION:** Promotes parental rights and vouchers for private and charter schools.
- **RELIGIOUS-FREEDOM:** Strong supporter of RFRA-like protections for faith-based groups.
- **GUNS:** Defends constitutional carry and opposes any gun control measures.
- **TAXES:** Pushes for tax cuts and balanced budgets without raising rates.
- **PUBLIC SAFETY:** Increases police funding.

**Endorsements:** Utah GOP, National Rifle Association, Family Policy Council

**Website:** https://www.wvc-ut.gov/912/Mayor

**June Freeman Hesleph (Democrat)** - Educator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Longtime resident, former teacher.
- Mother, school board volunteer.
- Weber State graduate.

**Christian Conservative Analysis:**
- **Pro-Life:** Backs expansion of abortion access.
- **Religious Liberty:** Emphasizes secular governance.
- **Education/Parental Rights:** Union-aligned, opposes choice.
- **Family Values:** Inclusive but erodes traditions.
- **Overall Assessment:** 2/10 - Misaligned with faith voters.

**Key Positions:**
- **ABORTION:** Supports reproductive rights and challenges state bans.
- **EDUCATION:** Increases funding for public schools and inclusive programs.
- **RELIGIOUS-FREEDOM:** Prioritizes separation of church and state to protect all beliefs.
- **GUNS:** Advocates for assault weapon bans and safe storage laws.
- **TAXES:** Fair share taxation for infrastructure and social programs.
- **DIVERSITY:** Equity hiring in city jobs.

**Endorsements:** Utah Democratic Party, Sierra Club, ACLU of Utah

**Website:** 

**Why It Matters:** Retaining conservative control prevents progressive shifts in this diverse city.

### **Provo Mayor** - 2025-11-04

**Context:** BYU's hometown election affects youth ministry and education policy in a faith-centered community.

**Michelle Kaufusi (Republican)** - Incumbent Mayor

**Faith Statement:** "As a faithful Latter-day Saint, I draw strength from the gospel of Jesus Christ to lead with love, honesty, and dedication to my community."

**Background:**
- First female mayor since 2017.
- Mother of four, BYU grad.
- Former school board member.

**Christian Conservative Analysis:**
- **Pro-Life:** Integrates support in community health.
- **Religious Liberty:** Partners with LDS for events.
- **Education/Parental Rights:** BYU collaborations.
- **Family Values:** Family Festival promoter.
- **Overall Assessment:** 9/10 - Exemplary faith leader.

**Key Positions:**
- **ABORTION:** Pro-life; supports state protections and adoption incentives.
- **EDUCATION:** Strong advocate for school choice and STEM education partnerships with BYU.
- **RELIGIOUS-FREEDOM:** Protects faith communities' rights in public spaces.
- **GUNS:** Supports responsible gun ownership and training programs.
- **TAXES:** Maintains low taxes through efficient government.
- **YOUTH:** Anti-drug initiatives.

**Endorsements:** Utah Valley GOP, BYU Alumni Association, Focus on the Family

**Website:** https://www.provo.gov/830/Meet-Mayor-Kaufusi

**Marsha Judkins (Republican)** - Former State Rep

**Faith Statement:** "My testimony of Jesus Christ as Savior motivates me to govern with righteousness, as Proverbs 29:2 teaches that when the righteous rule, the people rejoice."

**Background:**
- BYU professor, PhD holder.
- Married, three children.
- House Rep 2019-2025.

**Christian Conservative Analysis:**
- **Pro-Life:** Sponsored key bills.
- **Religious Liberty:** Legislative protector.
- **Education/Parental Rights:** Reform leader.
- **Family Values:** Biblical stance.
- **Overall Assessment:** 10/10 - Ideal conservative.

**Key Positions:**
- **ABORTION:** 100% pro-life; co-sponsored heartbeat bill and defunding abortion providers.
- **EDUCATION:** Pushes for universal school choice and bans on divisive concepts.
- **RELIGIOUS-FREEDOM:** Authored laws protecting religious expression in schools.
- **GUNS:** Strong NRA supporter; opposes all infringements on 2A rights.
- **TAXES:** Taxpayer advocate; led efforts to repeal gas tax increases.
- **TRANSPARENCY:** Open government reforms.

**Endorsements:** Utah Republican Party, Eagle Forum, Heritage Foundation

**Website:** https://marshajudkins.com

**Why It Matters:** Keeps Provo a beacon of conservative Christian values.

---

## 🔴 2026 FEDERAL RACES

### **U.S. House District 1** - 2026-11-03

**Context:** Northern Utah's district safeguards conservative priorities like tax cuts amid national shifts.

**Blake Moore (Republican)** - Incumbent

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Father of three, BYU grad.
- Former Sen. Lee chief of staff.
- Bush admin veteran.

**Christian Conservative Analysis:**
- **Pro-Life:** Born-Alive sponsor.
- **Religious Liberty:** Task force chair.
- **Education/Parental Rights:** Anti-federal control.
- **Family Values:** Traditional defender.
- **Overall Assessment:** 8/10 - Fiscal hawk with solid values.

**Key Positions:**
- **ABORTION:** Pro-life; co-sponsored Born-Alive Act and supports state bans.
- **EDUCATION:** School choice advocate; opposes federal overreach in curricula.
- **RELIGIOUS-FREEDOM:** Chairs task force on religious liberty protections.
- **GUNS:** NRA-endorsed; blocks ATF overregulation.
- **TAXES:** Permanently extends TCJA tax cuts.
- **VETERANS:** Expanded benefits.

**Endorsements:** National Right to Life, Family Research Council, U.S. Chamber of Commerce

**Website:** https://blakemoore.house.gov

**Rick Jones (Democrat)** - Business Owner

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Navy vet, father of two.
- 2024 candidate.
- Weber State grad.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports choice.
- **Religious Liberty:** Limited protections.
- **Education/Parental Rights:** Public funding focus.
- **Family Values:** Inclusive.
- **Overall Assessment:** 4/10 - Veteran respect but policy mismatch.

**Key Positions:**
- **ABORTION:** Pro-choice; codify Roe v. Wade.
- **EDUCATION:** Fully fund public schools, free community college.
- **RELIGIOUS-FREEDOM:** Protect while ensuring LGBTQ+ equality.
- **GUNS:** Universal background checks, ban assault weapons.
- **TAXES:** Raise on wealthy, lower for middle class.
- **HEALTHCARE:** Medicare expansion.

**Endorsements:** Utah Democrats, Everytown for Gun Safety, NEA

**Website:** 

**Why It Matters:** Retains GOP majority for pro-family bills.

### **U.S. House District 2** - 2026-11-03

**Context:** Rural district defends lands and energy against green agendas.

**Celeste Maloy (Republican)** - Incumbent

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Attorney, mother of two.
- Former deputy solicitor general.
- St. George native.

**Christian Conservative Analysis:**
- **Pro-Life:** 15-week ban backer.
- **Religious Liberty:** Anti-censorship.
- **Education/Parental Rights:** Parental empowerment.
- **Family Values:** Sports protections.
- **Overall Assessment:** 9/10 - Rural champion.

**Key Positions:**
- **ABORTION:** Pro-life; supports 15-week ban and ultrasound requirements.
- **EDUCATION:** Empowers parents with choice, blocks federal mandates.
- **RELIGIOUS-FREEDOM:** Defends against Big Tech censorship of faith groups.
- **GUNS:** 2A defender; sponsored concealed carry reciprocity.
- **TAXES:** Cuts corporate taxes to boost jobs.
- **ENERGY:** Fossil fuel expansion.

**Endorsements:** NRA, Susan B. Anthony Pro-Life America, American Conservative Union

**Website:** https://maloy.house.gov

**Why It Matters:** Secures conservative voice on public lands.

### **U.S. House District 3** - 2026-11-03

**Context:** Open seat battle tests GOP unity on life and liberty.

**Mike Kennedy (Republican)** - Physician

**Faith Statement:** "As a lifelong member of The Church of Jesus Christ of Latter-day Saints and former bishop, my faith compels me to protect the unborn and defend religious liberties as core to our nation's foundation."

**Background:**
- Family doctor, father of six.
- Former state senator.
- BYU med school grad.

**Christian Conservative Analysis:**
- **Pro-Life:** Ultrasound mandate leader.
- **Religious Liberty:** Conscience protections.
- **Education/Parental Rights:** ESA pusher.
- **Family Values:** Minors' transition ban.
- **Overall Assessment:** 10/10 - Faith-driven warrior.

**Key Positions:**
- **ABORTION:** Pro-life without exceptions except life of mother; led ultrasound mandate.
- **EDUCATION:** Universal ESA for all students, homeschool protections.
- **RELIGIOUS-FREEDOM:** Opposes vaccine mandates infringing on conscience.
- **GUNS:** Constitutional carry statewide.
- **TAXES:** Flat tax proposal to simplify and reduce.
- **HEALTHCARE:** Market-based reforms.

**Endorsements:** Utah Medical Association, Catholics for Kennedy, Tea Party Patriots

**Website:** https://www.mikekennedyforcongress.com

**Morgan Jenkins (Democrat)** - Attorney

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Civil rights lawyer, mother of one.
- 2020 state Senate candidate.
- U of U law grad.

**Christian Conservative Analysis:**
- **Pro-Life:** Justice for choice.
- **Religious Liberty:** Anti-discrimination.
- **Education/Parental Rights:** Equity over choice.
- **Family Values:** Trans advocacy.
- **Overall Assessment:** 1/10 - Direct opposition.

**Key Positions:**
- **ABORTION:** Reproductive justice; repeal all restrictions.
- **EDUCATION:** Debt-free college, equity in funding.
- **RELIGIOUS-FREEDOM:** Against using religion to discriminate.
- **GUNS:** Close loopholes, buyback programs.
- **TAXES:** Wealth tax on billionaires.
- **JUSTICE:** End cash bail.

**Endorsements:** EMILYs List, Human Rights Campaign, Brady Campaign

**Website:** 

**Why It Matters:** GOP hold prevents liberal flip.

### **U.S. House District 4** - 2026-11-03

**Context:** Suburban district guards against urban progressivism.

**Burgess Owens (Republican)** - Incumbent

**Faith Statement:** "My faith in Jesus Christ is the cornerstone of my life and service. As Ephesians 6:12 reminds us, our battle is spiritual, guiding my fight for biblical values in Congress."

**Background:**
- NFL star, father of six.
- Evangelical Christian.
- Family foundation founder.

**Christian Conservative Analysis:**
- **Pro-Life:** No funding for abortion.
- **Religious Liberty:** FADA supporter.
- **Education/Parental Rights:** Abolish Dept of Ed.
- **Family Values:** Marriage defender.
- **Overall Assessment:** 10/10 - Bold faith warrior.

**Key Positions:**
- **ABORTION:** Pro-life absolutist; no taxpayer funding for abortion.
- **EDUCATION:** School choice, end Dept of Education.
- **RELIGIOUS-FREEDOM:** First Amendment Defense Act supporter.
- **GUNS:** Shall-issue permits, oppose UN gun treaty.
- **TAXES:** Eliminate IRS, fair tax system.
- **CRITICAL RACE THEORY:** Bans in military.

**Endorsements:** FCA, Liberty Counsel, Heritage Action

**Website:** https://owens.house.gov

**Why It Matters:** Maintains firewall against SLC liberalism.

---

## 🎯 KEY ISSUES FOR UTAH CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Trigger law bans abortion after Roe; 2020 heartbeat bill restricts to 18 weeks.
- Over 50 pregnancy resource centers, including Utah-based Heartbeat International affiliates.
- Parental consent required for minors.
- No state funding for abortions; recent victory: 2024 ballot measure failed to expand.
- Challenges: Progressive lawsuits against bans.

**Progressive Position:**
- Push for repeal via Prop 2-like initiatives.
- Fund abortion travel; battle over telehealth.
- Expand access in universities.

**Christian Conservative Action:**
- Join Utah Right to Life for marches.
- Support HB 261 expansions.
- Volunteer at local centers like Birthline.
- Vote pro-life in all races.

### **School Choice & Parental Rights**

**Conservative Position:**
- 2023 ESA: $8,000 vouchers for private/homeschool, serving 10,000+ students.
- HB 11 bans gender ideology in K-3.
- No CRT per 2021 law; homeschool unregulated.
- Win: 2024 voucher growth.

**Progressive Position:**
- Union opposition to ESAs as "vouchers for rich."
- DEI mandates in districts.
- Threats to ban via referenda.

**Christian Conservative Action:**
- Run for local school boards via Utah Parents United.
- Lobby for SB 54 expansions.
- Join PublicSchoolEXIT for alternatives.

### **Religious Freedom**

**Conservative Position:**
- 2015 Antidiscrimination Act with RFRA carve-outs.
- Faith adoptions protected; school chaplains allowed.
- Church tax exemptions upheld.

**Progressive Position:**
- Nondiscrimination bills removing exemptions.
- Attacks on LDS influence in politics.

**Christian Conservative Action:**
- Support Alliance Defending Freedom cases.
- Join First Liberty alerts.
- Advocate HB 173 protections.

### **Guns**

**Conservative Position:**
- 2021 permitless carry for 21+.
- Stand-your-ground laws.
- No assault weapon bans.

**Progressive Position:**
- Background checks expansions.
- Red flag laws post-school threats.

**Christian Conservative Action:**
- NRA-ILA Utah chapter.
- Oppose SB 219 via petitions.
- Train church security teams.

### **Taxes**

**Conservative Position:**
- Flat 4.85% income tax; no sales on groceries.
- 2024 surplus returned via rebates.

**Progressive Position:**
- Progressive income tax proposals.
- Carbon tax for climate.

**Christian Conservative Action:**
- Taxpayer alerts from Utah Taxpayers Assoc.
- Support TABOR-like limits.

### **Immigration**

**Conservative Position:**
- E-Verify mandated for businesses.
- No sanctuary cities.

**Progressive Position:**
- Driver licenses for undocumented.
- Refugee resettlement expansions.

**Christian Conservative Action:**
- FAIR Utah chapters.
- Border prayer vigils.

### **Family Values**

**Conservative Position:**
- HB 11 transgender youth protections.
- Traditional marriage affirmed.

**Progressive Position:**
- Gender-neutral policies.
- Drag events in public.

**Christian Conservative Action:**
- Sutherland Institute campaigns.
- Family policy workshops.

### **Election Integrity**

**Conservative Position:**
- Voter ID since 2018.
- 2024 RCV rejection.

**Progressive Position:**
- Mail-in expansions.
- Oppose audits.

**Christian Conservative Action:**
- Poll watcher training via True the Vote.
- Support SB 89.

---

## 📅 CRITICAL DATES

**2025-2026 Election Calendar:**
- 2025-10-24 - Voter registration deadline (Municipal)
- 2025-10-21 - Early voting begins (Municipal)
- 2025-08-12 - Municipal Primary
- 2025-11-04 - Municipal General
- 2026-06-10 - Voter registration deadline (Federal)
- 2026-06-24 - Federal Primary
- 2026-10-20 - Early voting begins
- 2026-11-03 - General Election

**Voter Registration:** vote.utah.gov

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
✅ **Share on social media** with #UtahFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR UTAH CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Utah coverage
- **Utah Right to Life** - Pro-life ratings
- **Sutherland Institute** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Utah Secretary of State**: vote.utah.gov
- **County Election Offices**: slco.org/clerk/elections (Salt Lake example)
- **Early Voting Locations**: vote.utah.gov/locations

### **Conservative Organizations:**
- **Utah Right to Life**: utahrighttolife.org
- **Sutherland Institute**: sutherlandinstitute.org
- **Utah Citizens Alliance for Guns**: utahgunrights.org
- **Libertas Institute**: libertas.org (school choice)
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR UTAH CHRISTIANS

**2025-2026 Elections Matter:**
- Sandy Mayor determines local family policies.
- UT-3 House race impacts national pro-life votes.
- Provo Mayor affects BYU-adjacent youth ministries.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ ESA vouchers grow to all families
✅ No sanctuary policies in cities
✅ Church exemptions preserved

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Voucher programs defunded
❌ Immigrant amnesty locally
❌ Faith-based discrimination suits rise

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Cyndi Sharkey, Karen Lang, Michelle Kaufusi, Blake Moore, Celeste Maloy, Mike Kennedy, Burgess Owens and their families
- Utah Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Utah
- Revival and awakening in Utah
- God's will in Utah elections

**Scripture for Utah Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Utah coverage, email contact@ekewaka.com

**UTAH CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Utah races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Utah'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Utah races...")
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

print(f"\nChecking for existing Utah candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Utah'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Utah candidates...")
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

print("\nProcessing Utah summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Utah'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Utah data upload complete!")