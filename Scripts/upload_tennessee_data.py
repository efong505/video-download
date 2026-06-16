import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Tennessee Races
races = [
    {
        "state": "Tennessee",
        "office": "U.S. House - District 7 (Special)",
        "election_date": "2025-12-02",
        "race_type": "general",
        "description": "Special election to fill the vacancy in Tennessee's 7th Congressional District following Rep. Mark Green's resignation. Critical for maintaining Republican control in a red district."
    },
    {
        "state": "Tennessee",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the Class II U.S. Senate seat held by incumbent Bill Hagerty (R). A safe Republican seat pivotal for conservative priorities on the national stage."
    },
    {
        "state": "Tennessee",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open gubernatorial race due to term limits for Gov. Bill Lee. Key battle for conservative leadership in a state with strong Republican dominance."
    },
    {
        "state": "Tennessee",
        "office": "U.S. House - District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Diana Harshbarger (R) seeks re-election in this solidly Republican district."
    },
    {
        "state": "Tennessee",
        "office": "U.S. House - District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Tim Burchett (R) faces re-election in a competitive but leaning Republican district."
    },
    {
        "state": "Tennessee",
        "office": "U.S. House - District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Chuck Fleischmann (R) in a safe Republican seat focused on economic issues."
    },
    {
        "state": "Tennessee",
        "office": "U.S. House - District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Scott DesJarlais (R) defends his conservative stronghold."
    },
    {
        "state": "Tennessee",
        "office": "U.S. House - District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Andy Ogles (R) in a district blending urban Nashville suburbs."
    },
    {
        "state": "Tennessee",
        "office": "U.S. House - District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat as Rep. John Rose (R) runs for governor; key rural conservative battle."
    },
    {
        "state": "Tennessee",
        "office": "U.S. House - District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Full-term election following the 2025 special; winner of special likely favored."
    },
    {
        "state": "Tennessee",
        "office": "U.S. House - District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent David Kustoff (R) in a safe GOP district."
    },
    {
        "state": "Tennessee",
        "office": "U.S. House - District 9",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Steve Cohen (D) in the Democratic-leaning Memphis district."
    }
]

# Tennessee Candidates  
candidates = [
    {
        "name": "Marsha Blackburn",
        "state": "Tennessee",
        "office": "Governor",
        "party": "Republican",
        "bio": "Marsha Blackburn, born in 1952 in Laurel, Mississippi, moved to Tennessee as a child and has deep roots in the Volunteer State. She graduated from Mississippi State University with a degree in home economics and began her career in sales and marketing, rising to vice president at a biomedical firm. A mother of two and grandmother, Blackburn entered politics in 1998, serving in the Tennessee State Senate where she led the charge against a state income tax. Elected to Congress in 2002 for TN-07, she became the first woman to represent Tennessee in the U.S. House. In 2018, she won the U.S. Senate seat, defeating Democrat Phil Bredesen. Known for her business acumen and conservative leadership, Blackburn has authored books on leadership and family values. As a small businesswoman, she championed economic freedom and was instrumental in the Music Modernization Act. Her accomplishments include repealing the military COVID vaccine mandate and authoring the Kids Online Safety Act. Currently, she serves on key Senate committees including Finance, Commerce, and Judiciary, focusing on privacy and technology. Blackburn's career reflects a commitment to faith, family, and freedom, making her a formidable candidate for governor.",
        "faith_statement": "This isn't just a culture war—it's a war between Judeo-Christian values and Marxism. As a committed Christian, I draw strength from Scripture, like John 11:25, 'I am the resurrection and the life.' My faith guides my service to protect religious liberty and biblical principles in public life.",
        "website": "https://www.blackburn.senate.gov",
        "positions": {
            "ABORTION": "Unwavering pro-life advocate; supports Tennessee's trigger ban and heartbeat bill, opposes federal funding for Planned Parenthood, and fights to defund abortions globally.",
            "EDUCATION": "Strong supporter of school choice, vouchers, and parental rights; opposes federal overreach in curricula, backs bans on CRT and gender ideology in schools.",
            "RELIGIOUS-FREEDOM": "Defends First Amendment rights; authored bills protecting faith-based adoption agencies and opposed Respect for Marriage Act to safeguard religious liberties.",
            "GUNS": "Staunch 2nd Amendment defender; supports permitless carry expansion and opposes red flag laws, earning NRA endorsements.",
            "TAXES": "Anti-tax warrior; led defeat of TN income tax, pushes for tax cuts and spending reductions to promote economic growth.",
            "IMMIGRATION": "Secure borders first; advocates wall construction, ends chain migration, and harsher penalties for smuggling.",
            "FAMILY-VALUES": "Champions traditional marriage, parental rights, and protections against gender transition for minors; supports family tax credits.",
            "ELECTION-INTEGRITY": "Mandates voter ID, paper ballots, and audits; co-sponsored Election Integrity Act to prevent fraud."
        },
        "endorsements": ["National Right to Life", "Family Research Council", "NRA"]
    },
    {
        "name": "John Rose",
        "state": "Tennessee",
        "office": "Governor",
        "party": "Republican",
        "bio": "John Rose, an 8th-generation farmer from rural Tennessee, was born and raised in Cookeville, embodying the Volunteer State's agricultural heritage. He graduated from Cookeville High School, studied agriculture at Tennessee Tech University, earned a Master's in Agricultural Economics from Purdue, and a law degree from Vanderbilt. Starting young on the family farm, Rose now operates it with his wife Chelsea, a former Miss Tennessee, and their three children, including surviving the tragic loss of their son Mack in 2019. A small business owner in IT training, Rose volunteered extensively with FFA, the Tennessee State Fair, and hosted community events like the Lancaster Independence Day Parade. Entering politics in 2018, he flipped TN-06 from Democrat to Republican, winning re-election in 2020, 2022, and 2024. As a House Agriculture Committee member, he advanced farm bills and rural broadband. Rose's accomplishments include leading efforts on debt reduction and military support. A delegate at the 2024 RNC, he is a Trump ally, positioning him as a fresh conservative voice for governor.",
        "faith_statement": "As a dedicated Christian attending Jefferson Avenue Church of Christ, I believe in renewing Christian values in society. Faith is the foundation of my life and leadership, guiding me to protect life, family, and freedom as per biblical principles.",
        "website": "https://johnrose.com",
        "positions": {
            "ABORTION": "Pro-life from conception; supports TN's abortion bans and defunding Planned Parenthood, opposes any exceptions beyond life of mother.",
            "EDUCATION": "Expands school choice and vouchers; champions parental rights, bans on CRT, and protects against gender ideology in public schools.",
            "RELIGIOUS-FREEDOM": "Fights for faith-based exemptions; opposes laws infringing on religious conscience, supports protections for churches and believers.",
            "GUNS": "Absolute 2nd Amendment supporter; backs constitutional carry and opposes all gun control measures.",
            "TAXES": "No new taxes; advocates income tax elimination and spending cuts to balance budget.",
            "IMMIGRATION": "Secure borders with wall; ends sanctuary cities, deports criminals, and reforms legal immigration.",
            "FAMILY-VALUES": "Defends traditional marriage and family; bans gender-affirming care for minors, promotes parental authority.",
            "ELECTION-INTEGRITY": "Requires voter ID and citizenship proof; supports audits and paper trails to ensure fair elections."
        },
        "endorsements": ["President Donald Trump", "U.S. Chamber of Commerce", "Farm Bureau"]
    },
    {
        "name": "Carnita Atwater",
        "state": "Tennessee",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Dr. Carnita Atwater, a trailblazing community advocate, grew up on a 300-acre family farm in rural Tennessee, learning resilience from an early age driving tractors at 6. The first woman of color to run for governor, she started a lawn service at 12 and pursued a multifaceted career in healthcare and education: nurse, hospital administrator, adjunct professor, and dean of medical studies. With over 40 years serving Tennesseans, Atwater founded initiatives feeding 10,000 homeless annually, donating 5,000 book bags to children, and creating 100 jobs for ex-felons and single parents. A licensed social worker and teacher, she witnessed the assassination of MLK at 9, fueling her fight against injustice. Previously running for Memphis mayor in 2023, Atwater's 'Resurrection of Hope' plan addresses equity, health care, and poverty. Her accomplishments include the Tennessee Universal Health Care proposal and environmental revitalization efforts. As a mother and lifelong Tennessean, she brings boots-on-the-ground experience to challenge the status quo.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice; advocates restoring reproductive rights, opposing TN's trigger ban, and expanding access to women's health services.",
            "EDUCATION": "Fully funds public schools, opposes vouchers; supports inclusive curricula and teacher pay raises.",
            "RELIGIOUS-FREEDOM": "Protects all faiths while opposing discrimination; supports separation of church and state.",
            "GUNS": "Common-sense reforms like universal background checks and red flag laws to curb gun violence.",
            "TAXES": "Progressive taxation; closes corporate loopholes to fund social programs.",
            "IMMIGRATION": "Pathway to citizenship; opposes family separations and supports immigrant rights.",
            "FAMILY-VALUES": "Inclusive families; protects LGBTQ+ rights, gender-affirming care, and parental consent reforms.",
            "ELECTION-INTEGRITY": "Expands voting access; opposes restrictive ID laws seen as suppressive."
        },
        "endorsements": ["Planned Parenthood", "NAACP", "Sierra Club"]
    },
    {
        "name": "Bill Hagerty",
        "state": "Tennessee",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Bill Hagerty, born in 1959 in Gallatin, Tennessee, is a lifelong conservative and businessman serving as U.S. Senator since 2021. An Eagle Scout from Sumner County, he graduated from Princeton in architecture and earned an MBA from Vanderbilt. Hagerty's career spans global consulting with Boston Consulting Group, venture capital investments, and executive roles in NYSE-listed firms. As U.S. Ambassador to Japan under Trump, he strengthened alliances. From 2011-2014, as TN Economic Development Commissioner under Gov. Haslam, he cut bureaucracy by 40%, saving millions, and made TN #1 for foreign investment jobs. Married to Chrissy with four children, Hagerty lives in Nashville and volunteers in civic organizations. Elected in 2020 defeating Mark Warner, he serves on Banking, Foreign Relations, Appropriations, and Rules committees. Key accomplishments include the Taiwan Allies Fund Act and blocking Chinese investments. A fiscal hawk, he fights inflation and China threats, positioning him for re-election.",
        "faith_statement": "As an Episcopalian and conservative Christian raised to love Christ, I swore my oath on the Bible. Faith informs my commitment to Judeo-Christian principles, guiding my defense of religious liberty and moral leadership.",
        "website": "https://www.hagerty.senate.gov",
        "positions": {
            "ABORTION": "Pro-life; supports overturning Roe, backs state bans, and defunds Planned Parenthood.",
            "EDUCATION": "School choice and parental rights; opposes federal indoctrination, supports vouchers.",
            "RELIGIOUS-FREEDOM": "Strong protector; voted against Respect for Marriage Act to safeguard faith-based freedoms.",
            "GUNS": "2nd Amendment absolutist; opposes all infringements, supports national reciprocity.",
            "TAXES": "Tax cuts for growth; extends TCJA, fights IRS expansion.",
            "IMMIGRATION": "Border security; wall funding, ends catch-and-release, merit-based system.",
            "FAMILY-VALUES": "Traditional values; opposes same-sex marriage codification, protects against gender ideology.",
            "ELECTION-INTEGRITY": "Voter ID nationwide; audits and citizenship verification to prevent fraud."
        },
        "endorsements": ["National Federation of Independent Business", "Heritage Foundation", "NRA"]
    },
    {
        "name": "Matt Van Epps",
        "state": "Tennessee",
        "office": "U.S. House - District 7 (Special)",
        "party": "Republican",
        "bio": "Matt Van Epps, a West Point graduate and combat veteran, was born in Tennessee and dedicated his life to service. Commissioned as an Army officer, he served a decade on active duty as a helicopter pilot, including deployments to Iraq and Afghanistan, earning decorations for valor. Transitioning to civilian life, Van Epps became Tennessee's Commissioner of General Services, streamlining operations and saving taxpayer dollars. A proven conservative leader, he has called for Christian unity in politics and prioritizes service over partisanship. Married with children, Van Epps resides in the district, volunteering in community and veteran causes. Endorsed by President Trump, he won the 2025 GOP primary for the special election, positioning him to continue Mark Green's legacy. His background in leadership and fiscal responsibility makes him a strong advocate for rural Tennessee families facing economic challenges.",
        "faith_statement": "As a committed Christian, I call for unity among believers to advance biblical values in governance. Faith drives my service to protect life and liberty for all Tennesseans.",
        "website": "https://www.mattfortn.com",
        "positions": {
            "ABORTION": "Pro-life; supports TN bans and federal protections for the unborn.",
            "EDUCATION": "School choice expansion; parental rights over curricula, opposes woke indoctrination.",
            "RELIGIOUS-FREEDOM": "Defends churches and believers; opposes government overreach on faith.",
            "GUNS": "Strong 2A supporter; permitless carry and no new restrictions.",
            "TAXES": "Cut wasteful spending; no income tax, lower burdens on families.",
            "IMMIGRATION": "Secure borders; deport illegals, support legal pathways.",
            "FAMILY-VALUES": "Traditional family protections; bans on minor transitions.",
            "ELECTION-INTEGRITY": "Voter ID and audits essential for trust."
        },
        "endorsements": ["President Donald Trump", "Tennessee Farm Bureau", "Veterans of Foreign Wars"]
    },
    {
        "name": "Aftyn Behn",
        "state": "Tennessee",
        "office": "U.S. House - District 7 (Special)",
        "party": "Democrat",
        "bio": "Aftyn Behn, born in 1989, is a rising progressive star and licensed social worker representing TN House District 51 since 2023. A University of Texas psychology honors graduate and Vanderbilt MSSW holder, Behn started as a community organizer in Nashville, advocating for equity and mental health. Elected in a 2023 special, she became the youngest member of the TN House, focusing on healthcare access and education funding. As a former case manager for homeless youth, Behn's work addresses systemic inequalities. Winning the 2025 Democratic primary for the 7th Congressional special, she challenges the GOP hold, dubbed 'Tennessee's AOC' for her bold vision. Committed to working families, she opposes payday lending and pushes Medicaid expansion. Her leadership in community coalitions highlights her dedication to inclusive policies.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice; fights TN bans, supports reproductive freedom.",
            "EDUCATION": "Fully fund public schools; opposes vouchers draining resources.",
            "RELIGIOUS-FREEDOM": "Balanced protections; opposes using faith to discriminate.",
            "GUNS": "Background checks and assault weapon bans to save lives.",
            "TAXES": "Fair share from wealthy; invest in social services.",
            "IMMIGRATION": "Humane reform; DREAMers path, end separations.",
            "FAMILY-VALUES": "Inclusive; protects LGBTQ+ and diverse families.",
            "ELECTION-INTEGRITY": "Expand access; automatic registration, no suppression."
        },
        "endorsements": ["EMILY's List", "Progressive Change Campaign Committee", "Nashville Democrats"]
    }
]

# Tennessee Summary
summary = {
    "state": "Tennessee",
    "title": "Tennessee 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Tennessee 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 12
**Total Candidates Profiled:** 6
**Election Dates:**
- 2025-12-02 (U.S. House District 7 Special General)
- 2026-11-03 (Primary August 6, 2026; General for all other races)

---

## 🔴 Tennessee POLITICAL LANDSCAPE

### **The Volunteer State**

Tennessee is a **deep-red conservative stronghold**:
- **GOP Dominance:** Republicans hold supermajorities in the state legislature (75-24 House, 27-6 Senate), the governorship, both U.S. Senate seats, and 8 of 9 U.S. House districts.
- **Faith and Values:** Bible Belt heartland with high church attendance; evangelical Christians drive policy on life, family, and religious liberty.
- **Urban-Rural Divide:** Blue pockets in Nashville (Davidson County) and Memphis (Shelby County) contrast red rural East and Middle Tennessee; Chattanooga leans purple.
- **Economic Engine:** No state income tax attracts businesses; auto manufacturing (Nissan, VW) and tourism (Dollywood, Graceland) fuel growth.

### **Why Tennessee Matters**

Tennessee is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Trigger ban post-Roe with heartbeat law; near-total restrictions except rape/incest/ectopic, but ongoing lawsuits from Memphis providers.
- ✅ **Second Amendment:** Permitless carry since 2021; top-ranked gun rights, no assault weapon bans.
- ✅ **School Choice:** Expanded ESAs in 2025 session; vouchers for 20,000+ students, despite urban opposition.
- ✅ **Religious Liberty:** Strong protections via 2023 law shielding faith-based orgs; resisted federal marriage codification.
- ✅ **Family Values:** Banned gender-affirming care for minors (2023); parental consent for abortion upheld.
- ✅ **Election Integrity:** Strict voter ID, no mail drop boxes; paper ballots and audits standard.

---

## 🔴 2025 U.S. HOUSE RACES

### **U.S. House - District 7 (Special) - December 2, 2025**

**Context:** Vacancy from Rep. Mark Green's (R) resignation creates a must-win for GOP in this red rural-Memphis exurb district (R+16). Controls conservative votes on national issues like border security.

**Matt Van Epps (Republican)** - Combat Veteran

**Faith Statement:** "As a committed Christian, I call for unity among believers to advance biblical values in governance. Faith drives my service to protect life and liberty for all Tennesseans."

**Background:**
- West Point grad, Lt. Col. in Army National Guard with Iraq/Afghanistan deployments.
- TN Commissioner of General Services, saved taxpayer millions.
- Trump-endorsed family man prioritizing service.

**Christian Conservative Analysis:**
- **Pro-Life:** Backed TN bans; vows federal defunding of abortions.
- **Religious Liberty:** Shields churches from mandates.
- **Education/Parental Rights:** Vouchers and anti-CRT.
- **Family Values:** Traditional protections, minor gender care ban.
- **Overall Assessment:** 9/10 - Battle-tested conservative aligning with biblical justice.

**Key Positions:**
- **ABORTION:** Pro-life; supports TN bans and federal protections for the unborn.
- **EDUCATION:** School choice expansion; parental rights over curricula, opposes woke indoctrination.
- **RELIGIOUS FREEDOM:** Defends churches and believers; opposes government overreach on faith.
- **GUNS:** Strong 2A supporter; permitless carry and no new restrictions.
- **TAXES:** Cut wasteful spending; no income tax, lower burdens on families.
- **IMMIGRATION:** Secure borders; deport illegals, support legal pathways.

**Endorsements:** President Donald Trump, Tennessee Farm Bureau, Veterans of Foreign Wars

**Website:** https://www.mattfortn.com

**Aftyn Behn (Democrat)** - State Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Progressive social worker, youngest TN House member (Dist. 51).
- Organized for equity, mental health; Vanderbilt MSSW grad.
- Challenges GOP dominance with inclusive vision.

**Christian Conservative Analysis:**
- **Pro-Life:** Opposes bans, eroding protections.
- **Religious Liberty:** Risks faith freedoms via inclusivity mandates.
- **Education/Parental Rights:** Public funding focus weakens choice.
- **Family Values:** Pushes gender-affirming care, conflicting with Scripture.
- **Overall Assessment:** 2/10 - Progressive agenda clashes with core Christian tenets.

**Key Positions:**
- **ABORTION:** Pro-choice; fights TN bans, supports reproductive freedom.
- **EDUCATION:** Fully fund public schools; opposes vouchers draining resources.
- **RELIGIOUS FREEDOM:** Balanced protections; opposes using faith to discriminate.
- **GUNS:** Background checks and assault weapon bans to save lives.
- **TAXES:** Fair share from wealthy; invest in social services.
- **IMMIGRATION:** Humane reform; DREAMers path, end separations.

**Endorsements:** EMILY's List, Progressive Change Campaign Committee

**Website:** N/A

**Why It Matters:** Retaining Dist. 7 ensures conservative firewall against liberal encroachments on life and borders.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate - November 3, 2026**

**Context:** Incumbent Bill Hagerty (R) seeks re-election in safe seat (R+15); influences national conservative agenda on China, economy.

**Bill Hagerty (Republican)** - Incumbent Senator

**Faith Statement:** "As an Episcopalian and conservative Christian raised to love Christ, I swore my oath on the Bible. Faith informs my commitment to Judeo-Christian principles, guiding my defense of religious liberty and moral leadership."

**Background:**
- Princeton/Vanderbilt grad, ex-Ambassador to Japan.
- TN Economic Commissioner; spurred #1 foreign investment.
- Father of four, Nashville resident, Eagle Scout.

**Christian Conservative Analysis:**
- **Pro-Life:** Supported Roe overturn, state bans.
- **Religious Liberty:** Opposed marriage act threatening faiths.
- **Education/Parental Rights:** Choice advocate, anti-federal control.
- **Family Values:** Traditional stances, family priorities.
- **Overall Assessment:** 9/10 - Principled defender of biblical economics and liberty.

**Key Positions:**
- **ABORTION:** Pro-life; supports overturning Roe, backs state bans, and defunds Planned Parenthood.
- **EDUCATION:** School choice and parental rights; opposes federal indoctrination, supports vouchers.
- **RELIGIOUS FREEDOM:** Strong protector; voted against Respect for Marriage Act to safeguard faith-based freedoms.
- **GUNS:** 2nd Amendment absolutist; opposes all infringements, supports national reciprocity.
- **TAXES:** Tax cuts for growth; extends TCJA, fights IRS expansion.
- **IMMIGRATION:** Border security; wall funding, ends catch-and-release, merit-based system.

**Endorsements:** National Federation of Independent Business, Heritage Foundation, NRA

**Website:** https://www.hagerty.senate.gov

**Why It Matters:** Hagerty's win solidifies Senate conservative majority for life-affirming laws.

### **U.S. House Districts 1-9 - November 3, 2026**

**Context:** 8 GOP-held seats defend majority; open Dist. 6 (Rose for Gov) vulnerable; Dist. 9 Cohen (D) safe blue. Focus on rural conservatives vs. urban liberals.

**Key Races Highlight:** Dist. 6 open - Likely conservative primary; Dist. 7 full-term post-special.

**Why It Matters:** Maintains GOP House edge for blocking progressive overreach on family and faith.

---

## 🔴 2026 STATEWIDE RACES

### **Governor - November 3, 2026**

**Context:** Open due to Lee's term limits; GOP primary pits heavyweights; sets tone for pro-life, low-tax policies in Bible Belt bastion.

**Marsha Blackburn (Republican)** - U.S. Senator

**Faith Statement:** "This isn't just a culture war—it's a war between Judeo-Christian values and Marxism. As a committed Christian, I draw strength from Scripture, like John 11:25, 'I am the resurrection and the life.' My faith guides my service to protect religious liberty and biblical principles in public life."

**Background:**
- Mississippi State grad, biomedical VP turned politician.
- Defeated income tax; first woman TN Senator.
- Mother/grandmother, authored leadership books.

**Christian Conservative Analysis:**
- **Pro-Life:** Led defund efforts, heartbeat support.
- **Religious Liberty:** Authored adoption protections.
- **Education/Parental Rights:** Voucher champion, anti-CRT.
- **Family Values:** Traditional marriage defender.
- **Overall Assessment:** 10/10 - Embodiment of faith-driven conservatism.

**Key Positions:**
- **ABORTION:** Unwavering pro-life advocate; supports Tennessee's trigger ban and heartbeat bill, opposes federal funding for Planned Parenthood, and fights to defund abortions globally.
- **EDUCATION:** Strong supporter of school choice, vouchers, and parental rights; opposes federal overreach in curricula, backs bans on CRT and gender ideology in schools.
- **RELIGIOUS-FREEDOM:** Defends First Amendment rights; authored bills protecting faith-based adoption agencies and opposed Respect for Marriage Act to safeguard religious liberties.
- **GUNS:** Staunch 2nd Amendment defender; supports permitless carry expansion and opposes red flag laws, earning NRA endorsements.
- **TAXES:** Anti-tax warrior; led defeat of TN income tax, pushes for tax cuts and spending reductions to promote economic growth.
- **IMMIGRATION:** Secure borders first; advocates wall construction, ends chain migration, and harsher penalties for smuggling.

**Endorsements:** National Right to Life, Family Research Council, NRA

**Website:** https://www.blackburn.senate.gov

**John Rose (Republican)** - U.S. Representative

**Faith Statement:** "As a dedicated Christian attending Jefferson Avenue Church of Christ, I believe in renewing Christian values in society. Faith is the foundation of my life and leadership, guiding me to protect life, family, and freedom as per biblical principles."

**Background:**
- 8th-gen farmer, Purdue/Vanderbilt degrees.
- Flipped TN-06 red; Ag Committee leader.
- Family man, Trump delegate, lost son Mack.

**Christian Conservative Analysis:**
- **Pro-Life:** Absolute from conception, no exceptions.
- **Religious Liberty:** Clergy protections priority.
- **Education/Parental Rights:** Homeschool freedom advocate.
- **Family Values:** Biblical marriage, anti-gender ideology.
- **Overall Assessment:** 9/10 - Rural faith warrior.

**Key Positions:**
- **ABORTION:** Pro-life from conception; supports TN's abortion bans and defunding Planned Parenthood, opposes any exceptions beyond life of mother.
- **EDUCATION:** Expands school choice and vouchers; champions parental rights, bans on CRT, and protects against gender ideology in public schools.
- **RELIGIOUS-FREEDOM:** Fights for faith-based exemptions; opposes laws infringing on religious conscience, supports protections for churches and believers.
- **GUNS:** Absolute 2nd Amendment supporter; backs constitutional carry and opposes all gun control measures.
- **TAXES:** No new taxes; advocates income tax elimination and spending cuts to balance budget.
- **IMMIGRATION:** Secure borders with wall; ends sanctuary cities, deports criminals, and reforms legal immigration.

**Endorsements:** President Donald Trump, U.S. Chamber of Commerce, Farm Bureau

**Website:** https://johnrose.com

**Carnita Atwater (Democrat)** - Community Advocate

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Farm-raised nurse/educator, first Black woman gov candidate.
- Feeds homeless, jobs for ex-felons; health dean.
- 'Resurrection of Hope' equity plan author.

**Christian Conservative Analysis:**
- **Pro-Life:** Abortion expansion threatens bans.
- **Religious Liberty:** Inclusivity risks conscience rights.
- **Education/Parental Rights:** Anti-voucher harms choice.
- **Family Values:** LGBTQ push erodes traditions.
- **Overall Assessment:** 1/10 - Equity focus ignores biblical absolutes.

**Key Positions:**
- **ABORTION:** Pro-choice; advocates restoring reproductive rights, opposing TN's trigger ban, and expanding access to women's health services.
- **EDUCATION:** Fully funds public schools, opposes vouchers; supports inclusive curricula and teacher pay raises.
- **RELIGIOUS-FREEDOM:** Protects all faiths while opposing discrimination; supports separation of church and state.
- **GUNS:** Common-sense reforms like universal background checks and red flag laws to curb gun violence.
- **TAXES:** Progressive taxation; closes corporate loopholes to fund social programs.
- **IMMIGRATION:** Pathway to citizenship; opposes family separations and supports immigrant rights.

**Endorsements:** Planned Parenthood, NAACP, Sierra Club

**Website:** N/A

**Why It Matters:** Conservative governor preserves TN's pro-life fortress against national liberal tides.

---

## 🎯 KEY ISSUES FOR Tennessee CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- TN's 2022 trigger ban (6-week limit) and 2023 AG opinion closing loopholes; 95 pregnancy centers statewide.
- Parental consent required; defunded Planned Parenthood.
- Recent victory: 2025 upheld bans despite Nashville suits.
- Challenges: Federal funding pushes, Memphis clinics.

**Progressive Position:**
- Expansion via lawsuits; Medicaid for abortions.
- Remove consent, fund providers.

**Christian Conservative Action:**
- Join Tennessee Right to Life (tennrighttolife.com) for marches.
- Support HB 2670 anti-abortion trafficking bill.
- Volunteer at centers; vote pro-life in primaries.
- Biblical reminder: Psalm 139:13-16.

### **School Choice & Parental Rights**

**Conservative Position:**
- 2025 ESA expansion to $214M, 30,000 slots; universal vouchers proposed.
- 2021 parental rights law; 2023 CRT/gender bans in K-12.
- Homeschool co-ops booming; 150,000+ participants.
- Win: Blocked federal Title IX overreach.

**Progressive Position:**
- Union-backed public monopoly; DEI mandates.
- Challenge bans as discriminatory.

**Christian Conservative Action:**
- Run for local school boards via Excel Leadership.
- Back SB 800 voucher bill.
- Join Tennessee Home Education Association.
- Engage: Proverbs 22:6.

### **Religious Freedom**

**Conservative Position:**
- 2023 Religious Liberty Protection Act shields orgs from discrimination suits.
- No state church tax; protections for adoption, counseling.
- Upheld bakery cases; resisted federal marriage bill.
- Threats: Campus DEI quotas.

**Progressive Position:**
- Inclusivity laws forcing compliance.
- Remove exemptions.

**Christian Conservative Action:**
- Support Alliance Defending Freedom cases.
- Lobby for expansions via Family Action TN.
- Host forums; pray for justices.
- Scripture: 1st Amendment echo of Acts 5:29.

### **Guns**

**Conservative Position:**
- 2021 permitless carry (21+); no mag bans, open carry.
- #3 in Guns & Ammo rankings; preemption laws.
- Recent: Blocked red flags in 2025.

**Progressive Position:**
- Universal checks, assault bans.
- Local restrictions.

**Christian Conservative Action:**
- Join Tennessee Firearms Association.
- Oppose HB 1390 gun-free zones.
- Train safely; defend self-defense rights.
- Reference: Luke 22:36.

### **Taxes**

**Conservative Position:**
- No income tax since 2025 Hall cut; sales tax 7% avg.
- 2025 property tax freeze for seniors.
- Surplus to rebates; low corp rate 6.5%.

**Progressive Position:**
- Hike on rich, expand services.

**Christian Conservative Action:**
- Support Americans for Prosperity TN.
- Vote no-tax hikes.
- Tithe wisely; steward resources.
- Malachi 3:10.

### **Immigration**

**Conservative Position:**
- 2024 E-Verify mandate for businesses; sanctuary ban.
- Local law enforcement aids ICE.
- Challenges: Border influx via I-40.

**Progressive Position:**
- Sanctuary expansion, amnesty.

**Christian Conservative Action:**
- Back Federation for American Immigration Reform.
- Report illegals; secure borders.
- Welcome legal; Leviticus 19:34 balanced.

### **Family Values**

**Conservative Position:**
- 2023 minor gender care ban upheld; marriage amendment push.
- Adoption incentives; anti-porn in schools.
- Win: Blocked drag shows for kids.

**Progressive Position:**
- Gender fluidity, same-sex normalization.

**Christian Conservative Action:**
- Join Tennessee Family Action (tnfamilyaction.org).
- Support HB 1234 parental notification.
- Mentor families; Ephesians 6:4.

### **Election Integrity**

**Conservative Position:**
- Voter ID since 2011; no unsolicited mail ballots.
- 2025 audit enhancements; felony for fraud.
- High turnout via faith mobilization.

**Progressive Position:**
- Auto-registration, drop boxes.

**Christian Conservative Action:**
- Train as poll watchers via Heritage Action.
- Verify rolls; push SB 750.
- Vote early; Proverbs 29:2.

---

## 📅 CRITICAL DATES

**2025-2026 Election Calendar:**
- 2025-11-02 - Voter registration deadline (Special)
- 2025-11-12 to 2025-11-26 - Early voting (Special)
- 2026-07-03 - Voter registration deadline (Primary)
- 2026-08-06 - Primary Election
- 2026-10-05 - Voter registration deadline (General)
- 2026-10-19 to 2026-11-01 - Early voting (General)
- 2026-11-03 - General Election

**Voter Registration:** Go to GoVoteTN.gov or county election office.

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
✅ **Share on social media** with #TennesseeFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Tennessee CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Tennessee coverage
- **Tennessee Right to Life** - Pro-life ratings
- **Tennessee Family Action** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Tennessee Secretary of State**: sos.tn.gov/elections
- **County Election Offices**: Search at GoVoteTN.gov
- **Early Voting Locations**: Available at county sites or app

### **Conservative Organizations:**
- **Tennessee Right to Life**: tennrighttolife.com
- **Tennessee Family Action**: tnfamilyaction.org
- **Tennessee Firearms Association**: tfa.org
- **Tennessee School Choice Network**: tnschoolchoice.org
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Tennessee CHRISTIANS

**2025-2026 Elections Matter:**
- U.S. House Dist. 7 determines conservative votes on borders.
- U.S. Senate Hagerty affects national pro-life laws.
- Governor race sets state family protections.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ No income tax preserved
✅ Border security bolstered
✅ Rural economies thrive

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Tax hikes on families
❌ Sanctuary state risks
❌ Urban liberal dominance grows

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Marsha Blackburn, John Rose, Bill Hagerty, Matt Van Epps and their families
- Tennessee Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Tennessee
- Revival and awakening in Tennessee
- God's will in Tennessee elections

**Scripture for Tennessee Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Tennessee coverage, email contact@ekewaka.com

**Tennessee CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Tennessee races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Tennessee'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Tennessee races...")
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

print(f"\nChecking for existing Tennessee candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Tennessee'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Tennessee candidates...")
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

print("\nProcessing Tennessee summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Tennessee'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Tennessee data upload complete!")