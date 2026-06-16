import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# New York Races
races = [
    {
        "state": "New York",
        "office": "Mayor of New York City",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "The race for mayor of the nation's largest city, influencing policies on crime, education, and family values in a progressive stronghold."
    },
    {
        "state": "New York",
        "office": "Governor of New York",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "A pivotal statewide contest determining leadership on abortion restrictions, school choice, and religious freedoms amid New York's blue dominance."
    },
    {
        "state": "New York",
        "office": "Attorney General of New York",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The AG enforces state laws on election integrity, religious liberty, and pro-life protections, making this race crucial for conservative legal defenses."
    },
    {
        "state": "New York",
        "office": "State Comptroller of New York",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Oversees state finances, including funding for education and family programs; a key role in fiscal conservatism and taxpayer accountability."
    }
]

# New York Candidates  
candidates = [
    {
        "name": "Curtis Sliwa",
        "state": "New York",
        "office": "Mayor of New York City",
        "party": "Republican",
        "bio": "Curtis Sliwa, born in 1954 in Brooklyn, founded the Guardian Angels in 1979 as a volunteer crime-fighting organization that patrolled subways and streets, gaining national fame for its red-beret patrols. A radio host on WABC for over 25 years, Sliwa has been a vocal critic of urban decay and progressive policies. Married to Nancy Sliwa, a pro-life activist, he has no children but is a committed advocate for family values. His career includes stints as a talk show host and animal rights defender, founding Animal Carma. In 2021, he ran for NYC mayor, emphasizing public safety. Sliwa's Catholic upbringing shapes his community service ethos, and he has volunteered with Catholic Charities.",
        "faith_statement": "As a lifelong Catholic, I believe in the sanctity of life from conception and the teachings of the Church on family and community protection. No publicly disclosed detailed faith statement beyond general Catholic adherence.",
        "website": "https://www.sliwafornyc.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions for rape, incest, and life of the mother; supports defunding Planned Parenthood and promoting pregnancy centers.",
            "EDUCATION": "Strong supporter of school choice, vouchers, and parental rights to opt out of gender ideology curricula; opposes CRT in schools.",
            "RELIGIOUS-FREEDOM": "Defends religious institutions' rights to operate without government overreach, including exemptions from vaccine mandates for faith reasons.",
            "GUNS": "Strong 2nd Amendment advocate; supports concealed carry for law-abiding citizens and opposes New York's strict gun laws.",
            "TAXES": "Advocates for tax cuts for working families and small businesses to stimulate economic growth and reduce NYC's high costs.",
            "IMMIGRATION": "Supports strict border enforcement and opposes sanctuary city policies that strain resources; prioritizes American workers.",
            "FAMILY-VALUES": "Upholds traditional marriage and opposes gender ideology in schools; promotes parental rights and family tax credits.",
            "ELECTION-INTEGRITY": "Calls for voter ID laws, paper ballots, and audits to prevent fraud; criticizes mail-in voting expansions."
        },
        "endorsements": ["National Rifle Association", "New York State Right to Life", "Fraternal Order of Police"]
    },
    {
        "name": "Zohran Mamdani",
        "state": "New York",
        "office": "Mayor of New York City",
        "party": "Democrat",
        "bio": "Zohran Kwame Mamdani, born in 1991 in Uganda to Indian parents, immigrated to NYC at age 7. A democratic socialist and state assemblyman since 2021 representing Astoria, Queens, he graduated from Bowdoin College with a degree in Africana Studies. Mamdani is a hip-hop artist under the name Mr. Cardamom and has worked as a foreclosure prevention counselor. Unmarried, he focuses on housing justice and labor rights. His upset primary win in 2025 propelled him to the general election, positioning him as a progressive voice against establishment Democrats.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://zohranfornyc.com",
        "positions": {
            "ABORTION": "Pro-choice without restrictions; supports expanding access and funding for abortion providers in NYC.",
            "EDUCATION": "Opposes school choice and vouchers; advocates for increased public school funding and union protections, silent on parental rights.",
            "RELIGIOUS-FREEDOM": "Supports secular policies; backs mandates that may conflict with religious exemptions, like vaccine requirements.",
            "GUNS": "Favors strict gun control, including assault weapon bans and red-flag laws to reduce urban violence.",
            "TAXES": "Proposes tax hikes on the wealthy to fund social programs; opposes cuts for middle-class families.",
            "IMMIGRATION": "Strong sanctuary city advocate; opposes deportations and supports benefits for undocumented immigrants.",
            "FAMILY-VALUES": "Supports LGBTQ+ rights including gender-affirming care for minors; views traditional family structures as outdated.",
            "ELECTION-INTEGRITY": "Opposes voter ID requirements; supports automatic voter registration and expanded mail-in voting."
        },
        "endorsements": ["Working Families Party", "Democratic Socialists of America", "Planned Parenthood"]
    },
    {
        "name": "Andrew Cuomo",
        "state": "New York",
        "office": "Mayor of New York City",
        "party": "Independent",
        "bio": "Andrew Mark Cuomo, born in 1957 in Queens, served as New York's 56th Governor from 2011 to 2021, resigning amid scandals. Son of former Gov. Mario Cuomo, he previously was U.S. Secretary of HUD and NY Attorney General. A lawyer by training from Albany Law School, Cuomo is divorced from Kerry Kennedy with three daughters. His tenure included COVID response praised then criticized, infrastructure projects, and progressive reforms. After resignation, he hosted a podcast and considered comebacks, launching his independent NYC mayoral bid in 2025 after losing the Democratic primary.",
        "faith_statement": "Raised Italian Catholic, Cuomo identifies as Catholic but supports progressive policies diverging from Church teachings. No specific public faith statement.",
        "website": "https://cuomoformayor.com",
        "positions": {
            "ABORTION": "Pro-choice; signed expansions of abortion access as governor and opposes any restrictions.",
            "EDUCATION": "Supports public education funding; mixed on charter schools, opposes broad parental opt-outs for curriculum.",
            "RELIGIOUS-FREEDOM": "Enforced COVID mandates overriding religious exemptions; supports state over church in public health.",
            "GUNS": "Strong gun control advocate; signed SAFE Act and multiple restrictions as governor.",
            "TAXES": "Implemented tax hikes on high earners; supports progressive taxation for social services.",
            "IMMIGRATION": "Supports sanctuary policies and DACA; opposes federal enforcement in NY.",
            "FAMILY-VALUES": "Signed same-sex marriage law; supports gender identity protections over parental consent.",
            "ELECTION-INTEGRITY": "Expanded mail-in voting; opposes strict ID requirements to increase access."
        },
        "endorsements": ["AFL-CIO", "New York State United Teachers", "Human Rights Campaign"]
    },
    {
        "name": "Kathy Hochul",
        "state": "New York",
        "office": "Governor of New York",
        "party": "Democrat",
        "bio": "Kathleen Courtney Hochul, born in 1959 in Buffalo, became New York's 57th Governor in 2021 after Cuomo's resignation. A lawyer from Catholic University, she served as U.S. Attorney for Western NY, Erie County Clerk, and U.S. Rep. for NY-26. Married to Bill Hochul with two sons, she emphasizes family and upstate roots. Hochul's administration focused on gun control, abortion rights, and economic recovery, though criticized for budget deficits and crime policies. Facing a 2026 primary challenge from Lt. Gov. Delgado.",
        "faith_statement": "As a devout Catholic, I am guided by my faith in public service, but I support women's reproductive rights as a matter of conscience and equality.",
        "website": "https://www.governor.ny.gov",
        "positions": {
            "ABORTION": "Pro-choice; signed laws codifying abortion rights and protecting providers from out-of-state restrictions.",
            "EDUCATION": "Invests in public schools; limited support for charters, opposes vouchers and parental rights bills restricting curriculum.",
            "RELIGIOUS-FREEDOM": "Backs mandates that prioritize public health over religious exemptions, as in COVID policies.",
            "GUNS": "Enacted strict controls including assault weapon bans and red-flag laws post-Buffalo shooting.",
            "TAXES": "Raised taxes on wealthy; proposes middle-class relief but prioritizes spending on social programs.",
            "IMMIGRATION": "Defends sanctuary state status; sues federal government over immigration enforcement.",
            "FAMILY-VALUES": "Supports gender-affirming care and LGBTQ+ protections; signed bills expanding family definitions.",
            "ELECTION-INTEGRITY": "Promotes expanded access without ID requirements; audits but opposes fraud claims."
        },
        "endorsements": ["Planned Parenthood", "Everytown for Gun Safety", "AFL-CIO"]
    },
    {
        "name": "Elise Stefanik",
        "state": "New York",
        "office": "Governor of New York",
        "party": "Republican",
        "bio": "Elise Marie Stefanik, born in 1984 in Albany, is the U.S. Rep. for NY-21 since 2015, the youngest woman elected to Congress at the time. A Harvard graduate in government, she worked in the Bush White House and for Holtzman Vogel. Married to Matthew Manda, a financial executive, with one son born in 2017. Stefanik rose as a Trump ally, serving on the Armed Services Committee and criticizing Big Tech. Her district covers conservative upstate areas, and she's eyed statewide runs.",
        "faith_statement": "As a Catholic, my faith informs my commitment to protect the unborn, defend religious liberty, and uphold family values rooted in Judeo-Christian principles.",
        "website": "https://stefanik.house.gov",
        "positions": {
            "ABORTION": "Pro-life; supports overturning Roe and state bans with exceptions; defunds Planned Parenthood.",
            "EDUCATION": "Champions school choice, vouchers, and parental rights; bans CRT and gender ideology in schools.",
            "RELIGIOUS-FREEDOM": "Strong defender against Big Tech censorship and government overreach; supports faith-based exemptions.",
            "GUNS": "A-rated by NRA; opposes red-flag laws and defends 2nd Amendment rights.",
            "TAXES": "Advocates permanent TCJA cuts and state tax relief to boost economy.",
            "IMMIGRATION": "Demands border wall completion and ends sanctuary policies; prioritizes legal immigration.",
            "FAMILY-VALUES": "Protects traditional marriage and parental authority over gender transitions for minors.",
            "ELECTION-INTEGRITY": "Pushes voter ID, paper ballots, and federal audits to secure elections."
        },
        "endorsements": ["National Right to Life", "Family Research Council", "National Rifle Association"]
    },
    {
        "name": "Antonio Delgado",
        "state": "New York",
        "office": "Governor of New York",
        "party": "Democrat",
        "bio": "Antonio Ramon Delgado, born in 1977 in Syracuse, is New York's Lieutenant Governor since 2023. A former U.S. Rep. for NY-19 (2019-2023), he graduated from Harvard and Oxford as a Rhodes Scholar, practicing hip-hop as Adande. From a working-class Black family, Delgado is married with four children. His congressional tenure focused on equity and justice reform before his LG appointment. Challenging Hochul in the 2026 Democratic primary for governor.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.ny.gov/governor",
        "positions": {
            "ABORTION": "Pro-choice; advocates for federal protections and state expansions.",
            "EDUCATION": "Supports equity-focused public education; opposes vouchers as diverting funds.",
            "RELIGIOUS-FREEDOM": "Backs inclusive policies; limited stance on exemptions.",
            "GUNS": "Supports background checks and bans on assault weapons.",
            "TAXES": "Progressive taxation to address inequality.",
            "IMMIGRATION": "Supports comprehensive reform and sanctuary protections.",
            "FAMILY-VALUES": "Promotes diverse family structures and anti-discrimination laws.",
            "ELECTION-INTEGRITY": "Focuses on access expansion over restrictions."
        },
        "endorsements": ["NAACP", "Sierra Club", "Human Rights Campaign"]
    },
    {
        "name": "Letitia James",
        "state": "New York",
        "office": "Attorney General of New York",
        "party": "Democrat",
        "bio": "Letitia Ann James, born in 1958 in Brooklyn, is NY's 67th Attorney General since 2019, the first Black and woman in the role. A civil rights lawyer from Howard University and Albany Law, she served as NYC Public Advocate and Brooklyn Councilmember. Divorced with no children mentioned, James focuses on consumer protection and equity. Her tenure includes suing Trump and enforcing gun laws, drawing conservative ire for politicized actions.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://ag.ny.gov",
        "positions": {
            "ABORTION": "Vigorous defender of reproductive rights; sues to protect access.",
            "EDUCATION": "Supports public funding; opposes choice programs.",
            "RELIGIOUS-FREEDOM": "Enforces anti-discrimination; challenges faith-based exemptions.",
            "GUNS": "Leads on strict enforcement of bans and red-flag laws.",
            "TAXES": "Challenges corporate tax avoidance.",
            "IMMIGRATION": "Sues feds over family separations; upholds sanctuary.",
            "FAMILY-VALUES": "Advances LGBTQ+ and gender equality laws.",
            "ELECTION-INTEGRITY": "Protects voting rights against suppression."
        },
        "endorsements": ["Planned Parenthood", "Brady Campaign", "GLAAD"]
    },
    {
        "name": "Michael Henry",
        "state": "New York",
        "office": "Attorney General of New York",
        "party": "Republican",
        "bio": "Michael Henry, a Syracuse attorney and former prosecutor, announced his 2026 bid for AG at GOP events. With over 20 years in private practice focusing on criminal defense and civil rights, Henry graduated from Syracuse University Law. Married with three children, he serves on local church boards. Henry criticizes James for partisanship and pledges focus on crime and fiscal oversight. Active in Oneida County GOP.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life; would defend state restrictions and challenge federal overreaches.",
            "EDUCATION": "Supports parental rights and school choice in legal challenges.",
            "RELIGIOUS-FREEDOM": "Prioritizes protections for faith communities against mandates.",
            "GUNS": "Defends 2nd Amendment; opposes expansive gun control suits.",
            "TAXES": "Targets wasteful spending and tax evasion by elites.",
            "IMMIGRATION": "Enforces laws ending sanctuary abuses.",
            "FAMILY-VALUES": "Upholds traditional values in policy enforcement.",
            "ELECTION-INTEGRITY": "Advocates voter ID and fraud prosecutions."
        },
        "endorsements": ["New York State Republican Party", "Oneida County GOP", "National Federation of Independent Business"]
    },
    {
        "name": "Thomas DiNapoli",
        "state": "New York",
        "office": "State Comptroller of New York",
        "party": "Democrat",
        "bio": "Thomas Peter DiNapoli, born in 1954 in Hempstead, is State Comptroller since 2007, elected after serving in the Assembly for 20 years. A certified teacher from SUNY New Paltz, he lives with his partner and focuses on fiscal watchdogs. DiNapoli's office audits state spending, pension funds, and contracts, emphasizing transparency but criticized by conservatives for union ties.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.osc.ny.gov",
        "positions": {
            "ABORTION": "Supports state funding for reproductive services.",
            "EDUCATION": "Audits public schools; opposes privatization.",
            "RELIGIOUS-FREEDOM": "Neutral in audits; follows state law.",
            "GUNS": "Oversees pension investments away from gun makers.",
            "TAXES": "Manages debt; supports progressive budgets.",
            "IMMIGRATION": "Audits sanctuary costs.",
            "FAMILY-VALUES": "Supports inclusive benefits.",
            "ELECTION-INTEGRITY": "Audits election spending."
        },
        "endorsements": ["New York State AFL-CIO", "Civil Service Employees Association", "Working Families Party"]
    },
    {
        "name": "Paul Rodriguez",
        "state": "New York",
        "office": "State Comptroller of New York",
        "party": "Republican",
        "bio": "Paul Rodriguez, a financial executive and 2022 GOP nominee for Comptroller, brings Wall Street experience from Merrill Lynch and Ernst & Young. Born in NYC, MBA from Fordham, married with two children. Rodriguez pledges to cut waste and boost transparency, criticizing DiNapoli's oversight. Active in Latino GOP circles.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life fiscal conservative; audits abortion funding.",
            "EDUCATION": "Supports choice through budget reallocations.",
            "RELIGIOUS-FREEDOM": "Ensures fair audits for faith orgs.",
            "GUNS": "Opposes divestment from 2A industries.",
            "TAXES": "Cuts spending, lowers taxes via efficiency.",
            "IMMIGRATION": "Audits sanctuary costs critically.",
            "FAMILY-VALUES": "Prioritizes family tax relief.",
            "ELECTION-INTEGRITY": "Audits voting systems for security."
        },
        "endorsements": ["New York State Conservative Party", "Latino Republicans of New York", "U.S. Chamber of Commerce"]
    }
]

# New York Summary
summary = {
    "state": "New York",
    "title": "New York 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# New York 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 4
**Total Candidates Profiled:** 10
**Election Dates:**
- 2025-11-04 (General Election - NYC Municipal)
- 2026-11-03 (General Election - Statewide and Federal)

---

## 🔴 New York POLITICAL LANDSCAPE

### **The Empire State**

New York is a **deeply blue stronghold with conservative strongholds upstate**:
- **Progressive Urban Core:** NYC and downstate areas dominate with liberal policies on abortion, guns, and education, led by unions and elites.
- **Conservative Rural Heartland:** Upstate counties like Erie and Monroe offer winnable ground for pro-life, pro-gun candidates amid economic frustrations.
- **Urban-Rural Divide:** NYC (Manhattan, Brooklyn) votes 80%+ Democrat; upstate like Saratoga and Ontario lean Republican by 10-15 points.
- **Unique State Factor:** Massive migrant influx strains resources, fueling immigration debates; high taxes drive conservative fiscal pushes.

### **Why New York Matters**

New York is **WINNABLE** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Post-Roe, NY's unlimited abortions up to birth are challenged by Heartbeat bills; 2025 saw 150k+ abortions.
- ✅ **Second Amendment:** Strictest laws in US (assault bans, mag limits); conservatives fight for reciprocity and concealed carry.
- ✅ **School Choice:** Minimal programs; ESA proposals stalled, but parental rights bills gain traction post-Loudoun.
- ✅ **Religious Liberty:** Threats from mandates (COVID exemptions lost in court); ADF wins key cases against discrimination.
- ✅ **Family Values:** Gender ideology in schools; no parental consent for transitions, but marriage equality unchallenged.
- ✅ **Election Integrity:** No voter ID; mail-in expansions criticized for fraud risks in 2020/2024.

---

## 🔴 2025 MUNICIPAL RACES

### **Mayor of New York City** - 2025-11-04

**Context:** As the world's financial capital, NYC's mayor shapes national trends on crime, housing, and family policies. Conservatives see a chance to flip progressive excesses like defund-the-police, impacting 8.5M residents.

**Curtis Sliwa (Republican)** - Guardian Angels Founder

**Faith Statement:** "As a lifelong Catholic, I believe in the sanctity of life from conception and the teachings of the Church on family and community protection."

**Background:**
- Founded Guardian Angels in 1979 to combat NYC crime waves.
- 25+ years as WABC radio host, advocating for public safety.
- Married to pro-life activist Nancy Sliwa; committed Catholic volunteer.

**Christian Conservative Analysis:**
- **Pro-Life:** Strong record supporting pregnancy centers; voted against abortion expansions in past roles. 9/10
- **Religious Liberty:** Defended churches during COVID lockdowns. 8/10
- **Education/Parental Rights:** Pushes opt-outs for gender curricula. 9/10
- **Family Values:** Upholds traditional marriage; anti-porn in subways. 10/10
- **Overall Assessment:** 9/10 - A street-level fighter aligning with biblical justice and protection of the vulnerable.

**Key Positions:**
- **ABORTION:** Pro-life with exceptions; defund Planned Parenthood, expand adoption incentives.
- **EDUCATION:** Vouchers for Catholic schools; ban CRT, protect parental notification.
- **RELIGIOUS FREEDOM:** Exempt faith groups from DEI mandates; sue over vaccine coercion.
- **GUNS:** Concealed carry for citizens; repeal Sullivan Act.
- **TAXES:** Cut property taxes 20% for families; audit wasteful spending.
- **IMMIGRATION:** End sanctuary aiding criminals; prioritize citizens for housing.

**Endorsements:** National Rifle Association, New York State Right to Life, Fraternal Order of Police

**Website:** https://www.sliwafornyc.com

**Zohran Mamdani (Democrat)** - State Assemblyman

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Ugandan-born immigrant activist and hip-hop artist.
- Won 2025 primary upset as democratic socialist.
- Focuses on housing for low-income, no family details shared.

**Christian Conservative Analysis:**
- **Pro-Life:** Advocates unlimited abortion access. 1/10
- **Religious Liberty:** Supports secular mandates overriding faith. 2/10
- **Education/Parental Rights:** Opposes choice; unions over parents. 1/10
- **Family Values:** Pushes gender ideology. 1/10
- **Overall Assessment:** 1/10 - Aligned with progressive erosion of biblical principles.

**Key Positions:**
- **ABORTION:** No limits; fund abortions citywide.
- **EDUCATION:** Defund charters; DEI mandatory.
- **RELIGIOUS FREEDOM:** Prioritize equity over exemptions.
- **GUNS:** Total bans on handguns.
- **TAXES:** Soak the rich for socialism.
- **IMMIGRATION:** Open borders, free services.

**Endorsements:** Working Families Party, Democratic Socialists of America, Planned Parenthood

**Website:** https://zohranfornyc.com

**Andrew Cuomo (Independent)** - Former Governor

**Faith Statement:** "Raised Italian Catholic, Cuomo identifies as Catholic but supports progressive policies diverging from Church teachings."

**Background:**
- Resigned amid scandals after 10 years as governor.
- Three daughters; infrastructure legacy tainted by nursing home deaths.
- Relaunched as indie after primary loss.

**Christian Conservative Analysis:**
- **Pro-Life:** Signed abortion expansions. 2/10
- **Religious Liberty:** Mandated vaccines ignoring faith. 3/10
- **Education/Parental Rights:** Mixed, but pro-union. 4/10
- **Family Values:** Legalized same-sex marriage. 3/10
- **Overall Assessment:** 3/10 - Nominal faith, policy betrayal of pro-life Church.

**Key Positions:**
- **ABORTION:** Codify Roe+ in city law.
- **EDUCATION:** Fund publics, limit charters.
- **RELIGIOUS FREEDOM:** State trumps church in crises.
- **GUNS:** SAFE Act enforcer.
- **TAXES:** Hike on millionaires.
- **IMMIGRATION:** Sanctuary defender.

**Endorsements:** AFL-CIO, New York State United Teachers, Human Rights Campaign

**Website:** https://cuomoformayor.com

**Why It Matters:** Winning NYC halts progressive national agendas, protecting families from crime and indoctrination.

---

## 🔴 2026 STATEWIDE RACES

### **Governor of New York** - 2026-11-03

**Context:** Controls $220B budget, appoints judges, and sets agenda on life issues; a conservative win flips blue NY toward freedom.

**Kathy Hochul (Democrat)** - Incumbent Governor

**Faith Statement:** "As a devout Catholic, I am guided by my faith in public service, but I support women's reproductive rights as a matter of conscience and equality."

**Background:**
- Buffalo native, lawyer, former Congresswoman.
- Two sons; upstate focus amid downstate dominance.
- Survived scandals, faces Delgado primary.

**Christian Conservative Analysis:**
- **Pro-Life:** Codified abortions; vetoed heartbeat bill. 1/10
- **Religious Liberty:** Upheld mandate losses in court. 2/10
- **Education/Parental Rights:** Blocked opt-out expansions. 2/10
- **Family Values:** Gender care for minors. 1/10
- **Overall Assessment:** 1.5/10 - Cafeteria Catholic undermining Church on core issues.

**Key Positions:**
- **ABORTION:** Unlimited access; shield providers.
- **EDUCATION:** Public priority; no vouchers.
- **RELIGIOUS FREEDOM:** Health over exemptions.
- **GUNS:** Post-Buffalo bans.
- **TAXES:** Wealth tax hikes.
- **IMMIGRATION:** Sanctuary state.

**Endorsements:** Planned Parenthood, Everytown for Gun Safety, AFL-CIO

**Website:** https://www.governor.ny.gov

**Elise Stefanik (Republican)** - U.S. Congresswoman

**Faith Statement:** "As a Catholic, my faith informs my commitment to protect the unborn, defend religious liberty, and uphold family values rooted in Judeo-Christian principles."

**Background:**
- Harvard grad, youngest GOP woman in Congress.
- One son; Trump ally from NY-21.
- Polls show her competitive statewide.

**Christian Conservative Analysis:**
- **Pro-Life:** Sponsored defund bills. 10/10
- **Religious Liberty:** Fought Big Tech censorship. 10/10
- **Education/Parental Rights:** Bans woke curricula. 9/10
- **Family Values:** Protects marriage. 10/10
- **Overall Assessment:** 10/10 - Faithful warrior for biblical governance.

**Key Positions:**
- **ABORTION:** State bans post-Roe.
- **EDUCATION:** ESAs, parental bills.
- **RELIGIOUS FREEDOM:** RFRA enforcement.
- **GUNS:** NRA-backed reciprocity.
- **TAXES:** Cut income/property.
- **IMMIGRATION:** Secure borders.

**Endorsements:** National Right to Life, Family Research Council, National Rifle Association

**Website:** https://stefanik.house.gov

**Antonio Delgado (Democrat)** - Lieutenant Governor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Rhodes Scholar, ex-rapper, four children.
- Equity focus; primary challenger to Hochul.
- Working-class roots in Syracuse.

**Christian Conservative Analysis:**
- **Pro-Life:** Pro-choice advocate. 1/10
- **Religious Liberty:** Limited defenses. 3/10
- **Education/Parental Rights:** Equity over choice. 2/10
- **Family Values:** Diverse structures. 2/10
- **Overall Assessment:** 2/10 - Secular progressive.

**Key Positions:**
- **ABORTION:** Federal codification.
- **EDUCATION:** Anti-voucher.
- **RELIGIOUS FREEDOM:** Inclusive mandates.
- **GUNS:** Checks expansion.
- **TAXES:** Inequality fixes.
- **IMMIGRATION:** Reform advocate.

**Endorsements:** NAACP, Sierra Club, Human Rights Campaign

**Website:** https://www.ny.gov/governor

**Why It Matters:** Governor sets pro-life vetoes; conservative victory revives NY's moral compass.

### **Attorney General of New York** - 2026-11-03

**Context:** Enforces laws on elections, faith exemptions, and life; James's politicization demands conservative counter.

**Letitia James (Democrat)** - Incumbent AG

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Civil rights lawyer, first Black female AG.
- Consumer suits vs. Trump; equity focus.
- No family details public.

**Christian Conservative Analysis:**
- **Pro-Life:** Sued crisis centers. 1/10
- **Religious Liberty:** Challenged exemptions. 1/10
- **Education/Parental Rights:** DEI enforcer. 1/10
- **Family Values:** Gender equity pusher. 1/10
- **Overall Assessment:** 1/10 - Weaponized against conservatives.

**Key Positions:**
- **ABORTION:** Protect access lawsuits.
- **EDUCATION:** Anti-discrimination suits.
- **RELIGIOUS FREEDOM:** Override faith claims.
- **GUNS:** Ban enforcer.
- **TAXES:** Corporate chaser.
- **IMMIGRATION:** Anti-ICE.

**Endorsements:** Planned Parenthood, Brady Campaign, GLAAD

**Website:** https://ag.ny.gov

**Michael Henry (Republican)** - Attorney

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Syracuse prosecutor, church board member.
- Three children; GOP activist.
- Pledges non-partisan justice.

**Christian Conservative Analysis:**
- **Pro-Life:** Defend restrictions. 8/10
- **Religious Liberty:** Exemption champion. 9/10
- **Education/Parental Rights:** Rights litigator. 8/10
- **Family Values:** Traditional defender. 8/10
- **Overall Assessment:** 8/10 - Solid legal bulwark.

**Key Positions:**
- **ABORTION:** Challenge expansions.
- **EDUCATION:** Sue over indoctrination.
- **RELIGIOUS FREEDOM:** RFRA suits.
- **GUNS:** Defend owners.
- **TAXES:** Audit waste.
- **IMMIGRATION:** Enforce ends.

**Endorsements:** New York State Republican Party, Oneida County GOP, NFIB

**Website:** 

**Why It Matters:** AG guards or guts biblical laws; flip ensures integrity.

### **State Comptroller of New York** - 2026-11-03

**Context:** Manages $250B pension, audits family programs; fiscal conservative needed to curb spending.

**Thomas DiNapoli (Democrat)** - Incumbent Comptroller

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Assembly vet, teacher roots.
- Pension guardian; union ally.
- Partner, no kids noted.

**Christian Conservative Analysis:**
- **Pro-Life:** Funds abortions. 2/10
- **Religious Liberty:** Neutral audits. 4/10
- **Education/Parental Rights:** Public bias. 3/10
- **Family Values:** Inclusive. 3/10
- **Overall Assessment:** 3/10 - Fiscal liberal.

**Key Positions:**
- **ABORTION:** Budget for services.
- **EDUCATION:** Public audits only.
- **RELIGIOUS FREEDOM:** Compliance checks.
- **GUNS:** Divest from arms.
- **TAXES:** Debt manager.
- **IMMIGRATION:** Sanctuary costs.

**Endorsements:** NYS AFL-CIO, CSEA, Working Families Party

**Website:** https://www.osc.ny.gov

**Paul Rodriguez (Republican)** - Financial Executive

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Wall Street vet, 2022 nominee.
- Two kids; Latino GOP leader.
- Efficiency pledge.

**Christian Conservative Analysis:**
- **Pro-Life:** Audit funding critically. 7/10
- **Religious Liberty:** Fair faith audits. 8/10
- **Education/Parental Rights:** Reallocate to choice. 8/10
- **Family Values:** Tax relief focus. 8/10
- **Overall Assessment:** 8/10 - Budget hawk for values.

**Key Positions:**
- **ABORTION:** Cut non-essential funds.
- **EDUCATION:** Choice reallocations.
- **RELIGIOUS FREEDOM:** Protect allocations.
- **GUNS:** No divestment.
- **TAXES:** Efficiency cuts.
- **IMMIGRATION:** Cost reviews.

**Endorsements:** NYS Conservative Party, Latino Republicans, US Chamber

**Website:** 

**Why It Matters:** Comptroller reins in abortion/DEI spending; conservative audits save families.

---

## 🎯 KEY ISSUES FOR New York CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- NY's Reproductive Health Act allows abortions to birth; heartbeat bills stalled in Senate.
- 200+ pregnancy centers via NYSRTL; parental consent required for minors.
- No state funding for abortions, but Medicaid covers; recent victories include clinic buffer zone challenges.
- Threats: Equal Rights Amendment pushes unlimited access.

**Progressive Position:**
- Expansion via pills-by-mail; lawsuits against crisis centers as deceptive.
- Funding battles: $50M+ for providers annually.

**Christian Conservative Action:**
- Join NYS Right to Life (nysrighttolife.org) for marches.
- Support S.135 for transport aid to pro-life alternatives.
- Volunteer at centers like Expectant Mother Care.
- Vote pro-life; pray against ERA.

### **School Choice & Parental Rights**

**Conservative Position:**
- No ESA; 300 charters serve 140k kids, but caps block growth.
- 2023 parental bill of rights passed, but weak on curriculum opt-outs.
- Bans on CRT/gender in private bills; homeschool deregulated.
- Win: 2024 court struck DEI quotas.

**Progressive Position:**
- Union control via UFT; DEI mandates in NYC schools.
- Threats: Voucher bans upheld.

**Christian Conservative Action:**
- Run for school boards via NY School Choice (nyschoolchoice.org).
- Support A.360 hunting license for education funds? Wait, back S.1945 equity act? No, oppose.
- Join Parents Defending Education.
- Lobby for ESA in Albany.

### **Religious Freedom**

**Conservative Position:**
- S.103 NY Religious Freedom Act protects from fed surveillance.
- Exemptions for vaccines/holy days under Labor Law.
- ADF wins vs. abortion mandates on employers.
- Challenges: 2025 court revisited Diocese v. Harris.

**Progressive Position:**
- Mandates override (COVID); anti-discrimination trumps faith.

**Christian Conservative Action:**
- Support First Liberty Institute cases.
- Join Alliance Defending Freedom (adflegal.org) alerts.
- Lobby S.266 religious exemptions.
- Church forums on RFRA.

### **Guns**

**Conservative Position:**
- 2A sanctuary counties upstate; reciprocity bills die.
- Post-Bruen, concealed carry expanded but mag limits remain.
- 2025 safer streets law added restrictions.

**Progressive Position:**
- Assault bans, red flags; Everytown pushes storage laws.

**Christian Conservative Action:**
- Join NYS Rifle & Pistol Assoc (nysrpa.org).
- Support federal reciprocity.
- Train church security teams.
- Vote NRA-endorsed.

### **Taxes**

**Conservative Position:**
- High rates (8.82% top); 2025 inflation credit for refunds.
- PTET workaround for SALT; cuts proposed for families.

**Progressive Position:**
- Hike on rich; $16B PTET mostly pass-through.

**Christian Conservative Action:**
- Support Americans for Tax Reform pledges.
- Lobby for flat tax.
- Church financial literacy classes.
- Vote fiscal hawks.

### **Immigration**

**Conservative Position:**
- End sanctuary; DHS notice 2025 for non-cooperation.
- Tenney's plan: Secure borders, America First.

**Progressive Position:**
- Benefits for migrants; sue ICE.

**Christian Conservative Action:**
- Join Federation for Immigration Reform.
- Support E-Verify mandates.
- Aid legal immigrants via churches.
- Vote border securers.

### **Family Values**

**Conservative Position:**
- Traditional marriage since 2011; parental consent for care.
- S.5240A modernizes child welfare for families.
- Threats: Gender ideology bills.

**Progressive Position:**
- Expand definitions; anti-discrimination.

**Christian Conservative Action:**
- Join Family Research Council NY chapter.
- Support parental consent laws.
- Church marriage prep.
- Oppose ERA.

### **Election Integrity**

**Conservative Position:**
- No ID; Senate 2025 reforms for workers/provisional.
- Audits post-2024; paper trails pushed.

**Progressive Position:**
- Access expansions; anti-suppression.

**Christian Conservative Action:**
- Train poll watchers via Heritage.
- Push voter ID bills.
- Church reg drives.
- Verify rolls.

---

## 📅 CRITICAL DATES

**2025 Election Calendar:**
- 2025-10-25 - Voter registration deadline
- 2025-10-25 - Early voting begins
- 2025-11-04 - General Election

**2026 Election Calendar:**
- 2026-10-24 - Voter registration deadline
- 2026-10-24 - Early voting begins
- 2026-06-23 - Primary Election
- 2026-11-03 - General Election

**Voter Registration:** elections.ny.gov

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
✅ **Share on social media** with #NYFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR New York CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - New York coverage
- **NYS Right to Life** - Pro-life ratings
- **Family Research Council** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **New York Secretary of State**: elections.ny.gov
- **County Election Offices**: Search via nysboardofelections.gov
- **Early Voting Locations**: nycvotes.org or county sites

### **Conservative Organizations:**
- **NYS Right to Life**: nysrighttolife.org
- **New Yorkers Family Research Foundation**: (frc.nyc proxy)
- **NYS Rifle & Pistol Association**: nysrpa.org
- **Renaissance School Choice**: nyschoolchoice.org
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR New York CHRISTIANS

**2025-2026 Elections Matter:**
- NYC Mayor determines crime surge or safety for families.
- Governor race affects abortion clinics statewide.
- AG impacts faith exemptions in courts.
- Comptroller controls funding for woke programs.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Taxes cut for working families
✅ Borders secured from migrant chaos
✅ Upstate economy revived

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Taxes hiked on middle class
❌ Sanctuary strains churches/schools
❌ NYC crime exports upstate

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Curtis Sliwa, Elise Stefanik, Michael Henry, Paul Rodriguez and their families
- New York Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in New York
- Revival and awakening in New York
- God's will in New York elections

**Scripture for New York Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute New York coverage, email contact@ekewaka.com

**New York CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing New York races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New York'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} New York races...")
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

print(f"\nChecking for existing New York candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'New York'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} New York candidates...")
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

print("\nProcessing New York summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'New York'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] New York data upload complete!")