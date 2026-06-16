import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Illinois Races
races = [
    {
        "state": "Illinois",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat following retirement of Sen. Dick Durbin; critical for national balance of power and conservative influence on federal judiciary and life issues."
    },
    {
        "state": "Illinois",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent JB Pritzker seeks third term; key battle for state control over abortion laws, taxes, and education policy."
    },
    {
        "state": "Illinois",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Runs on ticket with Governor; influences state administration and ties to federal Senate ambitions."
    },
    {
        "state": "Illinois",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Enforces state laws on election integrity, religious freedom, and pro-life protections."
    },
    {
        "state": "Illinois",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Oversees elections; pivotal for voter integrity and access."
    },
    {
        "state": "Illinois",
        "office": "State Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Manages state funds; impacts fiscal policies on taxes and family support programs."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Chicago South Side district; influences urban policy on family values and immigration."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "South suburban district; key for gun rights and education reform."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "West suburban district; focuses on taxes and religious liberty."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Chicago Latino district; immigration and family policies central."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "North Side district; balances urban conservative voices."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Western suburbs; swing district for school choice."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Chicago West Side; economic and pro-life issues."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Northwest suburbs; foreign policy and taxes."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 9",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "North Shore; environmental vs. energy independence."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 10",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "North suburbs; competitive on gun rights."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 11",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Southern suburbs; rural-urban divide on immigration."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 12",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Downstate; strong conservative base for life issues."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 13",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Central IL; education and family values."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 14",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Northwest collar counties; swing for taxes."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 15",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Downstate; agriculture and gun rights."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 16",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Rockford area; manufacturing and immigration."
    },
    {
        "state": "Illinois",
        "office": "U.S. House District 17",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Western IL; rural conservative stronghold."
    }
]

# Illinois Candidates  
candidates = [
    {
        "name": "JB Pritzker",
        "state": "Illinois",
        "office": "Governor",
        "party": "Democrat",
        "bio": "J.B. Pritzker, born January 19, 1965, in Chicago, is a billionaire businessman, philanthropist, and the 43rd Governor of Illinois since 2019. A member of the prominent Pritzker family, known for Hyatt Hotels, he graduated from Duke University and earned a J.D. from Northwestern University School of Law. Pritzker founded Pritzker Group, a private equity firm, and has donated millions to education and health causes. Married to M.K. Pritzker, he has two children and resides in Chicago. As governor, he navigated the COVID-19 pandemic, expanded abortion access via the Reproductive Health Act, raised the minimum wage, legalized marijuana, and invested in infrastructure. Critics accuse him of high taxes and soft-on-crime policies. Pritzker's wealth, estimated at $3.5 billion, funds his campaigns heavily. He seeks a third term to continue progressive reforms amid national speculation of higher office ambitions.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.illinois.gov/gov",
        "positions": {
            "ABORTION": "Strongly pro-choice; signed Reproductive Health Act protecting abortion rights up to birth, funds abortion providers, opposes any restrictions and supports national codification post-Roe.",
            "EDUCATION": "Opposes school choice vouchers; invests in public schools, supports DEI programs, resists parental rights bills on curriculum transparency.",
            "RELIGIOUS-FREEDOM": "Supports LGBTQ+ rights over religious objections; signed laws allowing state intervention in faith-based adoptions if discriminatory.",
            "GUNS": "Enacted assault weapons ban, red-flag laws, raised age for rifles to 21; advocates federal gun control to reduce urban violence.",
            "TAXES": "Raised income and gas taxes for revenue; proposes progressive tax but settled for flat rate; claims investments in families justify increases.",
            "IMMIGRATION": "Sanctuary state policies; provides driver's licenses and healthcare to undocumented; opposes federal border wall and mass deportations.",
            "FAMILY-VALUES": "Supports same-sex marriage, gender-affirming care for minors without parental consent in some cases; promotes inclusive family definitions.",
            "ELECTION-INTEGRITY": "Opposes voter ID; expanded mail-in voting; claims 2020 election secure but resists audits."
        },
        "endorsements": ["Planned Parenthood", "Everytown for Gun Safety", "AFL-CIO"]
    },
    {
        "name": "Darren Bailey",
        "state": "Illinois",
        "office": "Governor",
        "party": "Republican",
        "bio": "Darren Bailey, born March 17, 1966, in Louisville, Illinois, is a third-generation farmer, businessman, and conservative politician from rural Clay County. He and his wife Cindy have been married for over 40 years, raising three children and now grandchildren on their family farm, where they grow corn, soybeans, and raise cattle. Bailey graduated from Eastern Illinois University with a degree in agriculture. Before politics, he owned a seed dealership and served on local school and library boards. Elected to the Illinois House in 2018 and Senate in 2020, he resigned in 2023 after his 2022 gubernatorial run. As a state legislator, he championed farm bills, tax cuts, and pro-life measures. In 2022, he won the GOP nomination but lost to Pritzker by 12 points, self-funding $60 million. Now running again with running mate Aaron Del Mar, Bailey emphasizes rural-urban unity, crime reduction, and freedom from government overreach. Tragically, in October 2025, his son, daughter-in-law, and two grandchildren perished in a helicopter crash, strengthening his resolve through faith.",
        "faith_statement": "Bailey centers his campaign on Christian faith, stating, 'My entry into politics came after prayer; I couldn't ignore God's call to serve and unite people against progressive policies that harm families. I love Jesus Christ as my Lord and Savior, and my values are rooted in biblical principles of life, liberty, and family.'",
        "website": "https://baileyforillinois.com",
        "positions": {
            "ABORTION": "Unequivocally pro-life; supports total ban on abortions, including exceptions only for mother's life; compared abortion deaths to Holocaust, vows to defund Planned Parenthood and protect unborn from conception.",
            "EDUCATION": "Strong advocate for school choice and vouchers; parental rights to review curricula, ban CRT and gender ideology in K-12; increase funding for homeschooling tax credits.",
            "RELIGIOUS-FREEDOM": "Defends faith-based organizations from state mandates; opposes compelled speech on gender; supports protections for churches and Christian businesses.",
            "GUNS": "Staunch 2nd Amendment defender; repeals assault weapons ban, concealed carry expansions, opposes red-flag laws as due process violations.",
            "TAXES": "Flat tax reduction, eliminate property taxes; cut spending on non-essentials to return money to families; no new taxes.",
            "IMMIGRATION": "Secure borders with wall support; end sanctuary policies, deport criminals, E-Verify for jobs to protect American workers.",
            "FAMILY-VALUES": "Traditional marriage only; parental consent for gender transitions, ban puberty blockers for minors; promote nuclear family through tax incentives.",
            "ELECTION-INTEGRITY": "Voter ID mandatory; paper ballots, same-day voting; audit 2020 election, prosecute fraud to restore trust."
        },
        "endorsements": ["National Right to Life", "NRA", "Illinois Family Institute"]
    },
    {
        "name": "James Mendrick",
        "state": "Illinois",
        "office": "Governor",
        "party": "Republican",
        "bio": "James Mendrick, born in 1965, is the DuPage County Sheriff since 2018, a law enforcement veteran with over 30 years in policing. Raised in Chicago's working-class neighborhoods, he graduated from the Chicago Police Academy and served as an officer before rising through ranks in DuPage. Married to Mary, with three adult children, Mendrick is a family man who coaches youth sports and volunteers at his parish. As sheriff, he implemented community policing, reduced opioid overdoses via treatment programs, and stood against state mandates during COVID, earning national attention for defying Pritzker's orders. Announced for governor in February 2025 with running mate Dr. Robert Renteria, a Hispanic activist and author, Mendrick focuses on public safety, border security, and economic revival. His campaign pledges to make Illinois safe again, cut taxes, and empower local law enforcement over Springfield bureaucrats. With a no-nonsense style, he appeals to suburban conservatives tired of Chicago crime spillover.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://mendrickforgovernor.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions for rape, incest, mother's life; supports 15-week ban, defund abortions from state budget.",
            "EDUCATION": "School choice expansion; parental bill of rights, remove woke indoctrination from classrooms.",
            "RELIGIOUS-FREEDOM": "Protects faith communities from hate crimes; opposes anti-discrimination laws overriding religious convictions.",
            "GUNS": "Full 2nd Amendment restoration; end FOID card delays, train and arm teachers for school safety.",
            "TAXES": "Freeze property taxes, income tax cut; audit state spending for waste.",
            "IMMIGRATION": "End sanctuary status; partner with ICE, secure southern border to stop fentanyl flow.",
            "FAMILY-VALUES": "Defend traditional marriage; protect children from gender confusion, promote family tax relief.",
            "ELECTION-INTEGRITY": "Strict voter ID; clean rolls, monitor polls to prevent fraud."
        },
        "endorsements": ["Illinois Sheriffs' Association", "Fraternal Order of Police", "DuPage County GOP"]
    },
    {
        "name": "Juliana Stratton",
        "state": "Illinois",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Juliana Stratton, born September 8, 1965, in Chicago, is an attorney and the 48th Lieutenant Governor of Illinois since 2019, the first Black woman in the role. Raised on Chicago's South Side by a single mother, she overcame poverty, earning a B.A. from University of Illinois at Urbana-Champaign and J.D. from Northern Illinois University College of Law. Before politics, Stratton prosecuted domestic violence cases and taught at DePaul University. Married to Hilmon Sorey III, she has two children and is active in community mentoring. Elected to Illinois House in 2016, she focused on criminal justice reform. As Lt. Gov., she launched workforce programs and equity initiatives. Entering the 2026 Senate race first after Durbin's retirement, Stratton pledges no corporate PACs, emphasizing middle-class uplift. Backed by Pritzker, she raised over $2 million early, positioning as a fighter against GOP extremism on abortion and voting rights.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://julianastratton.com",
        "positions": {
            "ABORTION": "Pro-choice absolutist; defends unlimited access, including late-term; fights national bans.",
            "EDUCATION": "Fully fund public schools; oppose vouchers as diverting resources from equity.",
            "RELIGIOUS-FREEDOM": "Balances with civil rights; supports protections but prioritizes anti-discrimination.",
            "GUNS": "Universal background checks, ban assault weapons; close loopholes for safety.",
            "TAXES": "Make permanent child tax credit; tax the rich more for social programs.",
            "IMMIGRATION": "Path to citizenship; protect DACA, increase refugee intake.",
            "FAMILY-VALUES": "Inclusive families; gender-affirming care access, LGBTQ+ protections.",
            "ELECTION-INTEGRITY": "Expand voting access; oppose suppression tactics like ID laws."
        },
        "endorsements": ["EMILY's List", "Governor JB Pritzker", "Senator Tammy Duckworth"]
    },
    {
        "name": "Don Tracy",
        "state": "Illinois",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Don Tracy, born around 1961, is a Springfield attorney with nearly 50 years in law, serving as Senior Counsel at Brown, Hay & Stephens, Illinois' oldest firm where Abraham Lincoln practiced. Son of a prominent family owning a major food distribution company, Tracy graduated from University of Illinois and earned his J.D. from Southern Illinois University. Married with children, he resides in Springfield and is involved in local charities. Tracy chaired the Illinois GOP from 2021-2024, rebuilding after losses, and previously led the state bar association. Known for bipartisan work on ethics reform, he self-funded $2 million for his 2026 Senate bid announced in August 2025, aiming to flip the seat blue. Campaign focuses on lowering costs, public safety, and Midwestern values, criticizing D.C. elites. As ex-GOP leader, he bridges moderates and conservatives, pledging to confirm pro-life judges and secure borders.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.dontracyforil.com",
        "positions": {
            "ABORTION": "Pro-life; supports restrictions post-Roe, defund Planned Parenthood federally.",
            "EDUCATION": "School choice vouchers; empower parents over unions, ban federal DEI mandates.",
            "RELIGIOUS-FREEDOM": "Strong First Amendment defender; protect faith-based exemptions from mandates.",
            "GUNS": "2nd Amendment absolutist; repeal federal overreaches, support concealed carry reciprocity.",
            "TAXES": "Cut federal taxes, simplify code; end inflation-driving spending.",
            "IMMIGRATION": "Build wall, end catch-and-release; merit-based legal immigration.",
            "FAMILY-VALUES": "Traditional values; oppose gender ideology in schools, protect parental rights.",
            "ELECTION-INTEGRITY": "Voter ID nationwide; secure elections with audits and citizenship verification."
        },
        "endorsements": ["Illinois GOP", "National Federation of Independent Business", "U.S. Chamber of Commerce"]
    }
]

# Illinois Summary
summary = {
    "state": "Illinois",
    "title": "Illinois 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Illinois 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 23  
**Total Candidates Profiled:** 5  
**Election Dates:**  
- 2026-03-17 (Primary Election)  
- 2026-11-03 (General Election)  

---

## 🔴 Illinois POLITICAL LANDSCAPE

### **The Land of Lincoln**

Illinois is a **Democratic stronghold with conservative strongholds in rural areas**:  
- **Urban Dominance:** Chicago and Cook County deliver overwhelming Democratic margins, funding progressive policies like abortion expansion.  
- **Rural Resistance:** Downstate counties like those in southern Illinois vote 70%+ Republican, defending life and guns.  
- **Urban-Rural Divide:** Chicago (blue) vs. counties like McHenry and DuPage (purple/red).  
- **Unique State Factor:** Highest property taxes in U.S., driving exodus; sanctuary policies strain resources.

### **Why Illinois Matters**

Illinois is **WINNABLE** for Christian conservatives:  
- ✅ **Pro-Life Leadership:** Despite 2019 Reproductive Health Act allowing late-term abortions, rural wins could trigger restrictions; 2022 ballot initiatives failed narrowly.  
- ✅ **Second Amendment:** Assault weapons ban (2023) faces lawsuits; GOP control could repeal for concealed carry expansion.  
- ✅ **School Choice:** No vouchers yet, but parental rights bills passed House; expand Invest in Kids program.  
- ✅ **Religious Liberty:** Protects via 2021 law, but threats from DEI mandates; defend against gender ideology.  
- ✅ **Family Values:** Same-sex marriage since 2014; fight gender-affirming care for minors.  
- ✅ **Tax Relief:** Flat 4.95% rate, but high burdens; cuts could retain families.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** Open seat after Dick Durbin's retirement; winner shapes Supreme Court confirmations, federal abortion bans, and religious freedom protections. A conservative flip aids national pro-life agenda.

**Juliana Stratton (Democrat)** - Lieutenant Governor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**  
- Raised on Chicago's South Side, overcame poverty as daughter of single mom.  
- Prosecutor of domestic violence, taught law at DePaul.  
- First Black female Lt. Gov., focused on equity and workforce training.  
- Married with two children, mentors youth.

**Christian Conservative Analysis:**  
- **Pro-Life:** 2/10 - Champions unlimited abortion access, including taxpayer-funded late-term procedures.  
- **Religious Liberty:** 3/10 - Prioritizes LGBTQ+ over faith exemptions in adoptions.  
- **Education/Parental Rights:** 2/10 - Opposes choice, supports union-backed public schools with DEI.  
- **Family Values:** 1/10 - Backs gender care for minors without consent hurdles.  
- **Overall Assessment:** 2/10 - Progressive warrior undermining biblical principles.

**Key Positions:**  
- **ABORTION:** Unlimited access; fights any restrictions as "extremist."  
- **EDUCATION:** Fund publics exclusively; resist parental curriculum vetoes.  
- **RELIGIOUS FREEDOM:** Civil rights trump faith objections.  
- **GUNS:** Ban assaults, universal checks.  
- **TAXES:** Tax wealthy for social equity.  
- **IMMIGRATION:** Sanctuary expansion, DACA permanent.

**Endorsements:** EMILY's List, JB Pritzker, Tammy Duckworth

**Website:** https://julianastratton.com

**Don Tracy (Republican)** - Attorney & Former IL GOP Chair

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**  
- Springfield lawyer 50 years, at Lincoln's old firm.  
- Family in food distribution; chaired IL GOP 2021-2024.  
- Bipartisan ethics reformer, self-funds campaign.  
- Married with family, community philanthropist.

**Christian Conservative Analysis:**  
- **Pro-Life:** 8/10 - Supports post-Roe limits, defunds Planned Parenthood.  
- **Religious Liberty:** 8/10 - Defends churches from mandates.  
- **Education/Parental Rights:** 7/10 - Vouchers and bans on indoctrination.  
- **Family Values:** 8/10 - Opposes gender ideology in schools.  
- **Overall Assessment:** 8/10 - Solid conservative, bridges for broader appeal.

**Key Positions:**  
- **ABORTION:** Restrictions, no federal funding.  
- **EDUCATION:** Choice and parental rights.  
- **RELIGIOUS FREEDOM:** First Amendment priority.  
- **GUNS:** Full 2A restoration.  
- **TAXES:** Cuts and simplification.  
- **IMMIGRATION:** Secure borders.

**Endorsements:** Illinois GOP, NFIB, U.S. Chamber

**Website:** https://www.dontracyforil.com

**Why It Matters:** Senate control decides if Roe's reversal sticks or reverses, impacting every unborn child nationwide.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** Pritzker's third-term bid vs. GOP challengers; controls state AG enforcement on life laws, school curricula, and taxes hurting families.

**JB Pritzker (Democrat)** - Incumbent Governor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**  
- Chicago billionaire, Hyatt heir; Duke/Northwestern grad.  
- Founded Pritzker Group; philanthropist in education.  
- Married with two kids; navigated COVID with mandates.  
- Expanded abortion, legalized weed, raised wages.

**Christian Conservative Analysis:**  
- **Pro-Life:** 1/10 - Codified unlimited abortions, funds providers.  
- **Religious Liberty:** 2/10 - Mandates override faith on gender.  
- **Education/Parental Rights:** 1/10 - No choice, pushes inclusive curricula.  
- **Family Values:** 1/10 - Gender-affirming for kids.  
- **Overall Assessment:** 1/10 - Architect of moral decay in IL.

**Key Positions:**  
- **ABORTION:** Protections to birth, national push.  
- **EDUCATION:** Public investment, no vouchers.  
- **RELIGIOUS FREEDOM:** Subordinate to equality laws.  
- **GUNS:** Strict controls.  
- **TAXES:** Progressive hikes.  
- **CRIME:** Soft policies blamed for Chicago violence.

**Endorsements:** Planned Parenthood, Everytown, AFL-CIO

**Website:** https://gov.illinois.gov

**Darren Bailey (Republican)** - Farmer & Former State Senator

**Faith Statement:** "My entry into politics came after prayer; I couldn't ignore God's call... I love Jesus Christ as my Lord and Savior."

**Background:**  
- Third-gen farmer in Clay County; EIU ag degree.  
- Family man, 40+ year marriage, farm operator.  
- House/Senate 2019-2023; 2022 nominee.  
- Focuses rural revival post-family tragedy.

**Christian Conservative Analysis:**  
- **Pro-Life:** 10/10 - Total ban advocate.  
- **Religious Liberty:** 9/10 - Protects believers.  
- **Education/Parental Rights:** 10/10 - Full choice.  
- **Family Values:** 10/10 - Biblical marriage.  
- **Overall Assessment:** 10/10 - Faith-driven warrior.

**Key Positions:**  
- **ABORTION:** Ban all, defund.  
- **EDUCATION:** Vouchers, ban CRT.  
- **RELIGIOUS FREEDOM:** Exemptions for faith.  
- **GUNS:** Repeal bans.  
- **TAXES:** Cuts across board.  
- **IMMIGRATION:** End sanctuary.

**Endorsements:** National Right to Life, NRA, IL Family Institute

**Website:** https://baileyforillinois.com

**James Mendrick (Republican)** - DuPage County Sheriff

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**  
- 30+ years law enforcement; Chicago native.  
- Sheriff since 2018, defied COVID mandates.  
- Married with three kids; youth coach.  
- Running mate Dr. Robert Renteria for diversity.

**Christian Conservative Analysis:**  
- **Pro-Life:** 7/10 - 15-week limits.  
- **Religious Liberty:** 8/10 - Anti-hate protections.  
- **Education/Parental Rights:** 8/10 - Rights bills.  
- **Family Values:** 8/10 - Protect kids from confusion.  
- **Overall Assessment:** 8/10 - Law-and-order conservative.

**Key Positions:**  
- **ABORTION:** Restrictions with exceptions.  
- **EDUCATION:** Choice expansion.  
- **RELIGIOUS FREEDOM:** Balance with safety.  
- **GUNS:** Arm teachers.  
- **TAXES:** Freeze properties.  
- **CRIME:** Back the blue.

**Endorsements:** IL Sheriffs' Assoc., FOP, DuPage GOP

**Website:** https://mendrickforgovernor.com

**Why It Matters:** Governor sets tone for IL's soul—life-affirming or death-enabling.

---

## 🎯 KEY ISSUES FOR Illinois CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**  
- IL's Reproductive Health Act (2019) allows abortions to birth; push for 15-week ban via HB 4692.  
- 200+ pregnancy centers via swingrighttolife.org.  
- Parental consent required for minors.  
- Defund via budget fights.  
- 2022 trigger law repeal victory blocked.

**Progressive Position:**  
- Unlimited access, including non-doctors.  
- $40M+ in state abortion funds.  
- Expansion bills yearly.

**Christian Conservative Action:**  
- Join Illinois Federation for Right to Life.  
- Support HB 4692.  
- Volunteer at centers.  
- Vote pro-life in primaries.

### **School Choice & Parental Rights**

**Conservative Position:**  
- Invest in Kids tax credit for private schools serves 10K kids.  
- HB 4301 parental rights law passed 2023.  
- Bans on CRT/gender in 2024 bills.  
- Homeschool deregulated.  
- Recent win: No DEI in K-12.

**Progressive Position:**  
- Teachers unions block choice.  
- Mandatory inclusive curricula.  
- Threats to voucher sunset.

**Christian Conservative Action:**  
- Run for school boards via ilschoolchoice.org.  
- Back SB 2336.  
- Join Parents Defending Education.

### **Religious Freedom**

**Conservative Position:**  
- IL Religious Freedom Act (2021) shields worship.  
- Exemptions for faith adoptions.  
- No compelled pronoun use.  
- Win: 2024 church vaccine exemption.

**Progressive Position:**  
- LGBTQ+ bills override exemptions.  
- Drag queen story hours mandated.  
- Funding cuts for discriminatory faiths.

**Christian Conservative Action:**  
- Alliance Defending Freedom cases.  
- Support HB 4968.  
- Church forums on liberty.

### **Guns**

**Conservative Position:**  
- FOID cards for carry; challenge assault ban.  
- Constitutional carry push.  
- Protect hunters/farmers.  
- 2023 ban lawsuit ongoing.

**Progressive Position:**  
- Red-flag, 21+ for rifles.  
- Ban high-capacity mags.  
- Urban safety over rights.

**Christian Conservative Action:**  
- Join Illinois State Rifle Assoc.  
- Lobby against SB 1231.  
- Train church security.

### **Taxes**

**Conservative Position:**  
- Flat 4.95%; cut to 3.5%.  
- Property tax caps.  
- No income on retirement.  
- Recent: Grocery tax freeze.

**Progressive Position:**  
- Hikes for equity.  
- Wealth tax proposals.  
- Corporate minimums.

**Christian Conservative Action:**  
- Taxpayer Bill of Rights via iltaxpayers.com.  
- Oppose graduated tax.  
- Family deduction advocacy.

### **Immigration**

**Conservative Position:**  
- End sanctuary via HB 4301 repeal.  
- E-Verify mandate.  
- Border aid.  
- 2024 migrant hotel backlash win.

**Progressive Position:**  
- Licenses/healthcare for undocumented.  
- Welcome centers.  
- Oppose ICE cooperation.

**Christian Conservative Action:**  
- FAIR federation.  
- Support secure borders bill.  
- Volunteer border aid.

### **Family Values**

**Conservative Position:**  
- Traditional marriage defense.  
- Ban minor transitions HB 68.  
- Parental notification.  
- 2023 gender care limits.

**Progressive Position:**  
- Inclusive laws.  
- No consent for care.  
- Pride in schools.

**Christian Conservative Action:**  
- Illinois Family Institute.  
- Back HB 1858.  
- Family policy petitions.

### **Election Integrity**

**Conservative Position:**  
- Voter ID HB 4596.  
- Clean rolls.  
- Paper backups.  
- 2020 audit calls.

**Progressive Position:**  
- Auto-registration.  
- No ID.  
- Mail-in expansion.

**Christian Conservative Action:**  
- iVoterGuide.  
- Poll watcher training.  
- Support SB 1916.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**  
- 2026-01-05 - Voter registration deadline for primary  
- 2026-02-01 - Early voting begins  
- 2026-03-17 - Primary Election  
- 2026-10-05 - Voter registration deadline for general  
- 2026-10-20 - Early voting begins  
- 2026-11-03 - General Election  

**Voter Registration:** https://www.illinois.gov/elections

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
✅ **Share on social media** with #IllinoisFaithVote  
✅ **Pray daily** for elections and candidates  
✅ **Vote early** and bring friends/family to polls  
✅ **Serve as poll watchers** to ensure election integrity  

---

## 📞 RESOURCES FOR Illinois CHRISTIAN VOTERS

### **Voter Guide Organizations:**  
- **iVoterGuide.org** - Illinois coverage  
- **Illinois Right to Life** - Pro-life ratings  
- **Illinois Family Institute** - Faith-based education  
- **Christian Voter Guide** - Biblical alignment  

### **Election Information:**  
- **Illinois Secretary of State**: https://www.ilsos.gov/elections  
- **County Election Offices**: Search via ilsos.gov  
- **Early Voting Locations**: County clerk websites  

### **Conservative Organizations:**  
- **Illinois Right to Life**: https://illinoisrighttolife.org  
- **Illinois Family Alliance**: https://illinoisfamily.org  
- **Illinois State Rifle Association**: https://www.isra.org  
- **Illinois Policy Institute** (School Choice): https://www.illinoispolicy.org  
- **Alliance Defending Freedom** - Religious liberty  
- **First Liberty Institute** - Religious freedom  

---

## 🔥 BOTTOM LINE FOR Illinois CHRISTIANS

**2026 Elections Matter:**  
- U.S. Senate determines federal pro-life judges.  
- Governor affects state abortion expansions.  
- House seats impact immigration enforcement.  
- Overall state direction at stake  

**If Conservatives Win:**  

✅ Pro-life protections maintained/strengthened  
✅ School choice expanded, parental rights protected  
✅ Religious liberty defended  
✅ Traditional family values upheld  
✅ Second Amendment rights secured  
✅ Election integrity ensured  
✅ Tax cuts retain families  
✅ Border security stops crime  
✅ Rural voices amplified  

**If Progressives Win:**  

❌ Abortion expansion, pro-life laws repealed  
❌ School choice gutted, CRT/gender ideology in schools  
❌ Religious liberty attacked  
❌ Family values eroded, parental rights stripped  
❌ Gun rights restricted  
❌ Election integrity weakened  
❌ Taxes crush middle class  
❌ Sanctuary invites chaos  
❌ Chicago dominates downstate  

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**  

---

## 🙏 PRAYER POINTS

**Pray for:**  
- Darren Bailey and family amid tragedy  
- Illinois Governor/leadership  
- Conservative candidates in all races  
- Church mobilization and Christian voter turnout  
- Protection from voter fraud  
- Wisdom for Christian voters in Illinois  
- Revival and awakening in Illinois  
- God's will in Illinois elections  

**Scripture for Illinois Elections:**  

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*  

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*  

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*  

---  

**Last Updated:** October 2025  
**Source:** Christian Conservatives Today Election Coverage  
**Contact:** For questions or to contribute Illinois coverage, email contact@ekewaka.com  

**Illinois CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Illinois races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Illinois'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Illinois races...")
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

print(f"\nChecking for existing Illinois candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Illinois'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Illinois candidates...")
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

print("\nProcessing Illinois summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Illinois'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Illinois data upload complete!")