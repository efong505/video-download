import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Missouri Races
races = [
    {
        "state": "Missouri",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The Attorney General race will determine the state's top law enforcement official, crucial for defending conservative values on abortion, religious liberty, and election integrity."
    },
    {
        "state": "Missouri",
        "office": "State Auditor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The State Auditor oversees fiscal accountability, impacting conservative priorities like tax relief and government transparency."
    },
    {
        "state": "Missouri",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Competitive urban district covering St. Louis, key for maintaining Republican gains in federal representation."
    },
    {
        "state": "Missouri",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Suburban St. Louis district, targeted by Democrats but held by Republicans, vital for House majority."
    },
    {
        "state": "Missouri",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Safely Republican district in central Missouri, focus on strong conservative turnout."
    },
    {
        "state": "Missouri",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Rural conservative stronghold, emphasizing agriculture and Second Amendment rights."
    },
    {
        "state": "Missouri",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Kansas City district with Democratic incumbent, opportunity for conservative challengers."
    },
    {
        "state": "Missouri",
        "office": "U.S. House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Kansas City suburbs, lean Republican, key for border security and family values."
    },
    {
        "state": "Missouri",
        "office": "U.S. House District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Springfield area, solid Republican seat defending pro-life and gun rights."
    },
    {
        "state": "Missouri",
        "office": "U.S. House District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Southeastern Missouri, conservative bastion focused on economic and faith issues."
    }
]

# Missouri Candidates  
candidates = [
    {
        "name": "Will Scharf",
        "state": "Missouri",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "Will Scharf is a dedicated conservative leader and former clerk to Justice Clarence Thomas on the U.S. Supreme Court. Born and raised in Missouri, Scharf graduated from Princeton University and Harvard Law School, where he honed his skills in constitutional law. He has served as a federal prosecutor and advisor to Missouri Governor Mike Parson, fighting for law and order. Married to his college sweetheart, Scharf is a father of three and an active member of his local Presbyterian church, where he teaches Sunday school. His accomplishments include leading legal challenges against election irregularities in 2020 and advocating for Second Amendment rights. Currently, he practices law in St. Louis, focusing on civil liberties cases.",
        "faith_statement": "As a committed Christian, I believe our rights come from God, not government. My faith guides my commitment to protect the unborn, defend religious liberty, and uphold biblical justice in every decision as Attorney General.",
        "website": "https://willscharf.com",
        "positions": {
            "ABORTION": "Pro-life without exception; supports enforcing Missouri's trigger ban and challenging any expansions, including parental consent and defunding Planned Parenthood.",
            "EDUCATION": "Strong advocate for school choice via MOScholars; parental rights paramount, opposes CRT and gender ideology in public schools.",
            "RELIGIOUS-FREEDOM": "Will defend faith-based organizations from discrimination; supports Missouri Religious Liberty in Schools Awareness Act.",
            "GUNS": "Second Amendment absolutist; opposes all federal overreach like SAPA enforcement to nullify ATF rules.",
            "TAXES": "Supports further cuts like capital gains exemption; fiscal conservative reducing government waste.",
            "IMMIGRATION": "Secure borders first; backs state deportation assistance and E-Verify mandates for employers.",
            "FAMILY-VALUES": "Traditional marriage only; bans gender-affirming care for minors, protects parental rights in upbringing.",
            "ELECTION-INTEGRITY": "Voter ID required; audits all elections, cleans voter rolls regularly."
        },
        "endorsements": ["Missouri Right to Life", "Family Research Council", "National Rifle Association"]
    },
    {
        "name": "Elad Gross",
        "state": "Missouri",
        "office": "Attorney General",
        "party": "Democrat",
        "bio": "Elad Gross is a civil rights attorney and former prosecutor in Kansas City. A graduate of the University of Missouri-Kansas City School of Law, Gross has spent his career defending marginalized communities and challenging corporate overreach. He ran for AG in 2024, emphasizing consumer protection. Married with two children, Gross is involved in his synagogue and local Jewish community center. His key accomplishments include winning settlements against predatory lenders. Currently in private practice, he focuses on environmental justice.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://eladgross.com",
        "positions": {
            "ABORTION": "Pro-choice; seeks to expand access post-Amendment 3, repeal waiting periods and bans.",
            "EDUCATION": "Public school funding priority; opposes vouchers draining resources from public education.",
            "RELIGIOUS-FREEDOM": "Protects all faiths but opposes using religion to discriminate against LGBTQ+ rights.",
            "GUNS": "Supports universal background checks and red-flag laws to curb gun violence.",
            "TAXES": "Raise taxes on wealthy; close corporate loopholes for education and healthcare funding.",
            "IMMIGRATION": "Pathway to citizenship; opposes state-level deportations, focuses on humane reform.",
            "FAMILY-VALUES": "Inclusive families; supports gender-affirming care and marriage equality.",
            "ELECTION-INTEGRITY": "Automatic voter registration; opposes strict ID laws as suppressive."
        },
        "endorsements": ["Planned Parenthood", "Everytown for Gun Safety", "ACLU"]
    },
    {
        "name": "Dave Gregory",
        "state": "Missouri",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "Dave Gregory is a veteran prosecutor and rancher from rural Missouri. A University of Missouri graduate, he served as Jackson County prosecutor for over a decade, tackling opioid crises and human trafficking. Married to his high school sweetheart, they have four children and run a family farm. Active in his Baptist church, Gregory leads youth ministry. Accomplishments include securing convictions in high-profile corruption cases. He now consults on rural economic development.",
        "faith_statement": "My Christian faith compels me to seek justice for the voiceless, from the unborn to crime victims. As AG, I'll protect Missouri's families with biblical principles.",
        "website": "https://davegregorymo.com",
        "positions": {
            "ABORTION": "Unwavering pro-life; enforce all restrictions, support 2026 ballot ban initiative.",
            "EDUCATION": "Expand school choice; empower parents against woke indoctrination in schools.",
            "RELIGIOUS-FREEDOM": "Shield churches from COVID-style mandates; promote faith in public life.",
            "GUNS": "Constitutional carry defender; block federal gun grabs at state level.",
            "TAXES": "No new taxes; audit state spending for efficiency.",
            "IMMIGRATION": "End sanctuary policies; cooperate with ICE for deportations.",
            "FAMILY-VALUES": "Biblical family structure; ban transgender sports participation.",
            "ELECTION-INTEGRITY": "Paper ballots only; prosecute voter fraud aggressively."
        },
        "endorsements": ["Missouri Farm Bureau", "Eagle Forum", "Heritage Action"]
    },
    {
        "name": "Scott Fitzpatrick",
        "state": "Missouri",
        "office": "State Auditor",
        "party": "Republican",
        "bio": "Scott Fitzpatrick, current State Auditor, is a fourth-generation farmer from northern Missouri. A Rockhurst University alumnus, he served in the Missouri House before winning statewide in 2022. Married with three children, Fitzpatrick coaches youth sports at his Methodist church. Key accomplishments: Exposing $500M in government waste and launching MOScholars oversight. He focuses on agricultural policy and fiscal reform.",
        "faith_statement": "As a follower of Christ, I audit with integrity, stewarding taxpayer dollars as unto the Lord, ensuring accountability for future generations.",
        "website": "https://auditor.mo.gov",
        "positions": {
            "ABORTION": "Pro-life advocate; audits defund Planned Parenthood compliance.",
            "EDUCATION": "MOScholars champion; transparency in school spending for parental rights.",
            "RELIGIOUS-FREEDOM": "Protects faith-based nonprofits from regulatory burdens.",
            "GUNS": "Supports rural gun rights; audits ATF overreach impacts.",
            "TAXES": "Led capital gains tax cut; ongoing waste reduction audits.",
            "IMMIGRATION": "Audits welfare use by undocumented; supports border funding.",
            "FAMILY-VALUES": "Family farm tax breaks; opposes gender ideology in curricula.",
            "ELECTION-INTEGRITY": "Audits election finances; recommends voter roll purges."
        },
        "endorsements": ["Missouri Chamber of Commerce", "National Federation of Independent Business", "Focus on the Family"]
    },
    {
        "name": "Karla May",
        "state": "Missouri",
        "office": "State Auditor",
        "party": "Democrat",
        "bio": "State Senator Karla May is a lifelong St. Louis resident and community advocate. Holding degrees from University of Missouri-St. Louis, she has served in the legislature since 2013, chairing budget committees. Mother of two, May is active in her AME church choir. Accomplishments: Expanding Medicaid and criminal justice reform. She runs a consulting firm for nonprofits.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://karlamaymo.com",
        "positions": {
            "ABORTION": "Reproductive justice; audit barriers to access under Amendment 3.",
            "EDUCATION": "Fully fund public schools; oppose voucher diversions.",
            "RELIGIOUS-FREEDOM": "Balanced protections without favoring one faith.",
            "GUNS": "Audit gun violence prevention programs' effectiveness.",
            "TAXES": "Progressive taxation; close loopholes for the rich.",
            "IMMIGRATION": "Audit humane treatment in detention centers.",
            "FAMILY-VALUES": "Support diverse family structures; paid family leave.",
            "ELECTION-INTEGRITY": "Expand access; audit suppression tactics."
        },
        "endorsements": ["Missouri AFL-CIO", "NAACP", "Sierra Club"]
    },
    {
        "name": "Ann Wagner",
        "state": "Missouri",
        "office": "U.S. House District 2",
        "party": "Republican",
        "bio": "U.S. Rep. Ann Wagner, serving since 2013, is a former state treasurer and ambassador. A Ball State graduate, she built a career in finance and diplomacy. Married to Ray, with four children and eight grandchildren, Wagner attends St. Louis Catholic church. Accomplishments: Banking reforms post-2008 crisis, pro-life votes. She focuses on economic security.",
        "faith_statement": "My Catholic faith informs my service; I fight for life, family, and freedom as God-given rights.",
        "website": "https://wagner.house.gov",
        "positions": {
            "ABORTION": "100% pro-life rating; co-sponsors national bans.",
            "EDUCATION": "School choice federally; parental rights bills.",
            "RELIGIOUS-FREEDOM": "RFRA defender; protects conscience rights.",
            "GUNS": "NRA-endorsed; blocks assault weapon bans.",
            "TAXES": "Permanent TCJA; cuts for families.",
            "IMMIGRATION": "Border wall funding; end catch-and-release.",
            "FAMILY-VALUES": "Traditional marriage; anti-trafficking leader.",
            "ELECTION-INTEGRITY": "Election security task force member."
        },
        "endorsements": ["Susan B. Anthony Pro-Life America", "U.S. Chamber of Commerce", "NRA"]
    },
    {
        "name": "Fred Wellman",
        "state": "Missouri",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "bio": "Fred Wellman is a podcast host and veteran from St. Louis suburbs. A West Point graduate and Army veteran, he served in Iraq. Father of three, Wellman is active in his Episcopal church. Launched campaign in 2025 against Wagner. Accomplishments: Veteran advocacy podcast reaching millions. Runs a media company.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://fredwellman.com",
        "positions": {
            "ABORTION": "Pro-choice; codify Roe protections.",
            "EDUCATION": "Public school investments; student debt relief.",
            "RELIGIOUS-FREEDOM": "Inclusive protections for all beliefs.",
            "GUNS": "Background checks; assault weapons ban.",
            "TAXES": "Biden-era cuts for middle class.",
            "IMMIGRATION": "Comprehensive reform with citizenship path.",
            "FAMILY-VALUES": "LGBTQ+ equality; family leave expansion.",
            "ELECTION-INTEGRITY": "HR1 voting rights supporter."
        },
        "endorsements": ["VoteVets", "EMILY's List", "Brady Campaign"]
    }
]

# Missouri Summary
summary = {
    "state": "Missouri",
    "title": "Missouri 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Missouri 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 10
**Total Candidates Profiled:** 7
**Election Dates:**
- 2026-08-04 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Missouri POLITICAL LANDSCAPE

### **The Show-Me State**

Missouri is a **solid Republican stronghold**:
- **Governance:** Republican trifecta with supermajorities in legislature; Governor Mike Kehoe (R) advancing conservative agenda.
- **Values Alignment:** Strong pro-life laws, though challenged by 2024 Amendment 3; leading in school choice with MOScholars.
- **Urban-Rural Divide:** Blue strongholds in St. Louis (Jackson County) and Kansas City (Jackson/Clay Counties); overwhelming red in rural areas like Ozarks and Bootheel.
- **Border Battles:** Proximity to sanctuary cities in Illinois fuels immigration crackdowns.

### **Why Missouri Matters**

Missouri is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Near-total ban reinstated in 2025 courts, but 2026 ballot fight to codify; 50+ pregnancy centers statewide.
- ✅ **Second Amendment:** Permitless carry since 2017; SAPA challenged federally but state defiant.
- ✅ **School Choice:** Universal ESA via MOScholars, $6,500/child; homeschool freedom robust.
- ✅ **Religious Liberty:** New 2025 laws protect faith in schools; bans on discrimination against believers.
- ✅ **Family Values:** Parental consent for abortions upheld; transgender care bans for minors.
- ✅ **Election Security:** Voter ID law; regular roll cleanings by SOS.

---

## 🔴 2026 STATEWIDE RACES

### **Attorney General** - 2026-11-03

**Context:** Open seat after Andrew Bailey's FBI move; winner enforces pro-life, fights federal overreach on guns/immigration. Impacts 2026 ballot on abortion ban.

**Will Scharf (Republican)** - Former SCOTUS Clerk

**Faith Statement:** "As a committed Christian, I believe our rights come from God, not government. My faith guides my commitment to protect the unborn, defend religious liberty, and uphold biblical justice in every decision as Attorney General."

**Background:**
- Princeton/Harvard Law grad; clerked for Justice Thomas.
- Federal prosecutor; advised Gov. Parson on elections.
- St. Louis father of three; Presbyterian Sunday school teacher.

**Christian Conservative Analysis:**
- **Pro-Life:** Led 2020 election suits; vows to defend trigger ban, prosecute aiding abortions.
- **Religious Liberty:** Backed school prayer bills; sues over faith discrimination.
- **Education/Parental Rights:** Supports MOScholars audits for accountability.
- **Family Values:** Aligns with biblical marriage; anti-trafficking focus.
- **Overall Assessment:** 9/10 - Unwavering defender of Judeo-Christian principles.

**Key Positions:**
- **ABORTION:** Pro-life without exception; supports enforcing Missouri's trigger ban and challenging any expansions, including parental consent and defunding Planned Parenthood.
- **EDUCATION:** Strong advocate for school choice via MOScholars; parental rights paramount, opposes CRT and gender ideology in public schools.
- **RELIGIOUS FREEDOM:** Will defend faith-based organizations from discrimination; supports Missouri Religious Liberty in Schools Awareness Act.
- **GUNS:** Second Amendment absolutist; opposes all federal overreach like SAPA enforcement to nullify ATF rules.
- **TAXES:** Supports further cuts like capital gains exemption; fiscal conservative reducing government waste.
- **IMMIGRATION:** Secure borders first; backs state deportation assistance and E-Verify mandates for employers.

**Endorsements:** Missouri Right to Life, Family Research Council, National Rifle Association

**Website:** https://willscharf.com

**Dave Gregory (Republican)** - Rancher Prosecutor

**Faith Statement:** "My Christian faith compels me to seek justice for the voiceless, from the unborn to crime victims. As AG, I'll protect Missouri's families with biblical principles."

**Background:**
- U. Missouri grad; Jackson County prosecutor 10+ years.
- Fought opioids/trafficking; family farm with wife, four kids.
- Baptist youth leader in rural MO.

**Christian Conservative Analysis:**
- **Pro-Life:** Convicted clinic violators; pushes 2026 ban ballot.
- **Religious Liberty:** Defended church gatherings during COVID.
- **Education/Parental Rights:** Rural school choice advocate.
- **Family Values:** Biblical family policies; anti-porn in schools.
- **Overall Assessment:** 8/10 - Grounded in rural faith values.

**Key Positions:**
- **ABORTION:** Unwavering pro-life; enforce all restrictions, support 2026 ballot ban initiative.
- **EDUCATION:** Expand school choice; empower parents against woke indoctrination in schools.
- **RELIGIOUS FREEDOM:** Shield churches from COVID-style mandates; promote faith in public life.
- **GUNS:** Constitutional carry defender; block federal gun grabs at state level.
- **TAXES:** No new taxes; audit state spending for efficiency.
- **IMMIGRATION:** End sanctuary policies; cooperate with ICE for deportations.

**Endorsements:** Missouri Farm Bureau, Eagle Forum, Heritage Action

**Website:** https://davegregorymo.com

**Elad Gross (Democrat)** - Civil Rights Attorney

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- UMKC Law; prosecutor turned consultant.
- Synagogue member; mother of two in KC.
- Settlements vs. lenders.

**Christian Conservative Analysis:**
- **Pro-Life:** Opposes bans; seeks expansions.
- **Religious Liberty:** Favors secular neutrality.
- **Education/Parental Rights:** Public funding only.
- **Family Values:** Inclusive but erodes traditions.
- **Overall Assessment:** 3/10 - Clashes with biblical worldview.

**Key Positions:**
- **ABORTION:** Pro-choice; seeks to expand access post-Amendment 3, repeal waiting periods and bans.
- **EDUCATION:** Public school funding priority; opposes vouchers draining resources from public education.
- **RELIGIOUS FREEDOM:** Protects all faiths but opposes using religion to discriminate against LGBTQ+ rights.
- **GUNS:** Supports universal background checks and red-flag laws to curb gun violence.
- **TAXES:** Raise taxes on wealthy; close corporate loopholes for education and healthcare funding.

**Endorsements:** Planned Parenthood, Everytown for Gun Safety, ACLU

**Website:** https://eladgross.com

**Why It Matters:** Controls enforcement of conservative laws like abortion bans and gun rights.

---

## 🔴 2026 STATEWIDE RACES

### **State Auditor** - 2026-11-03

**Context:** Incumbent Fitzpatrick seeks re-election; audits impact tax cuts, school choice funding. Key for transparency in redistricting fights.

**Scott Fitzpatrick (Republican)** - Incumbent Auditor

**Faith Statement:** "As a follower of Christ, I audit with integrity, stewarding taxpayer dollars as unto the Lord, ensuring accountability for future generations."

**Background:**
- Rockhurst grad; MO House veteran.
- Farmer with wife, three kids; Methodist coach.
- Exposed $500M waste; MOScholars launch.

**Christian Conservative Analysis:**
- **Pro-Life:** Audits Planned Parenthood funding blocks.
- **Religious Liberty:** Reviews faith group grants.
- **Education/Parental Rights:** Oversees ESA transparency.
- **Family Values:** Farm family tax audits.
- **Overall Assessment:** 9/10 - Faithful fiscal watchdog.

**Key Positions:**
- **ABORTION:** Pro-life advocate; audits defund Planned Parenthood compliance.
- **EDUCATION:** MOScholars champion; transparency in school spending for parental rights.
- **RELIGIOUS FREEDOM:** Protects faith-based nonprofits from regulatory burdens.
- **GUNS:** Supports rural gun rights; audits ATF overreach impacts.
- **TAXES:** Led capital gains tax cut; ongoing waste reduction audits.

**Endorsements:** Missouri Chamber of Commerce, National Federation of Independent Business, Focus on the Family

**Website:** https://auditor.mo.gov

**Karla May (Democrat)** - State Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- UMSL degrees; Senate since 2013.
- AME choir; mom of two in St. Louis.
- Medicaid expansion leader.

**Christian Conservative Analysis:**
- **Pro-Life:** Pushes access expansions.
- **Religious Liberty:** Neutral but progressive tilt.
- **Education/Parental Rights:** Anti-voucher.
- **Family Values:** Broad but not biblical focus.
- **Overall Assessment:** 4/10 - Misfit for conservatives.

**Key Positions:**
- **ABORTION:** Reproductive justice; audit barriers to access under Amendment 3.
- **EDUCATION:** Fully fund public schools; oppose voucher diversions.
- **RELIGIOUS FREEDOM:** Balanced protections without favoring one faith.

**Endorsements:** Missouri AFL-CIO, NAACP, Sierra Club

**Website:** https://karlamaymo.com

**Why It Matters:** Ensures conservative policies like tax cuts aren't wasted.

---

## 🔴 2026 FEDERAL RACES

### **U.S. House District 2** - 2026-11-03

**Context:** Suburban battleground; Wagner defends against Wellman amid redistricting. Influences national House control on life, borders.

**Ann Wagner (Republican)** - Incumbent

**Faith Statement:** "My Catholic faith informs my service; I fight for life, family, and freedom as God-given rights."

**Background:**
- Ball State; ex-treasurer/ambassador.
- Catholic mom/grandma in Ballwin.
- Banking reforms post-crisis.

**Christian Conservative Analysis:**
- **Pro-Life:** 100% rating; national ban co-sponsor.
- **Religious Liberty:** RFRA protector.
- **Education/Parental Rights:** Federal choice bills.
- **Family Values:** Anti-trafficking faith lead.
- **Overall Assessment:** 10/10 - Gold standard conservative.

**Key Positions:**
- **ABORTION:** 100% pro-life rating; co-sponsors national bans.
- **EDUCATION:** School choice federally; parental rights bills.
- **RELIGIOUS FREEDOM:** RFRA defender; protects conscience rights.
- **GUNS:** NRA-endorsed; blocks assault weapon bans.
- **TAXES:** Permanent TCJA; cuts for families.

**Endorsements:** Susan B. Anthony Pro-Life America, U.S. Chamber of Commerce, NRA

**Website:** https://wagner.house.gov

**Fred Wellman (Democrat)** - Veteran Podcaster

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- West Point/Iraq vet; podcast host.
- Episcopal dad of three in suburbs.
- Veteran advocacy millions reached.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports expansions.
- **Religious Liberty:** Inclusive only.
- **Education/Parental Rights:** Debt relief over choice.
- **Family Values:** LGBTQ+ focus.
- **Overall Assessment:** 2/10 - Progressive threat.

**Key Positions:**
- **ABORTION:** Pro-choice; codify Roe protections.
- **EDUCATION:** Public school investments; student debt relief.
- **RELIGIOUS FREEDOM:** Inclusive protections for all beliefs.

**Endorsements:** VoteVets, EMILY's List, Brady Campaign

**Website:** https://fredwellman.com

**Why It Matters:** Flipping loses GOP House edge on faith issues.

[Note: Other districts lean safe; focus turnout for Luetkemeyer (3), Hartzler successors (4), etc.]

---

## 🎯 KEY ISSUES FOR Missouri CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Near-total ban post-2025 court; exceptions only life-saving.
- 50+ pregnancy centers; parental consent upheld Oct 2025.
- No state funding abortions; 2026 ballot to ban outright.
- Recent victories: Trigger law defense.
- Challenges: Amendment 3 expansions.

**Progressive Position:**
- Full access via Amendment 3; repeal waits/bans.
- Fund clinics; challenge consent laws.
- Interstate travel protections.

**Christian Conservative Action:**
- Join Missouri Right to Life (missourilife.org).
- Support 2026 ban amendment petitions.
- Volunteer at centers; pray for SCOTUS reversals.
- Vote pro-life in AG/Auditor races.

### **School Choice & Parental Rights**

**Conservative Position:**
- MOScholars ESA universal, $6,500/child for private/homeschool.
- 2025 court upheld funding; CRT/gender bans in law.
- Homeschool deregulated; open enrollment bills.
- Recent wins: 40% participation surge.

**Progressive Position:**
- Vouchers drain publics; union control.
- DEI mandates; threaten choice programs.
- Fund public equity over private.

**Christian Conservative Action:**
- Run for school boards via Missouri Homeschool Assoc.
- Support HB 711 open enrollment.
- Join Parents Defending Education MO chapter.

### **Religious Freedom**

**Conservative Position:**
- 2025 Awareness Act posts freedoms in schools.
- Protects student groups' faith standards.
- Bans discrimination vs. believers; college association rights.
- Strong RFRA state analog.

**Progressive Position:**
- Secular schools; no prayer/ Ten Commandments.
- LGBTQ+ over faith accommodations.
- Challenge faith-based adoptions.

**Christian Conservative Action:**
- Alliance Defending Freedom MO events.
- Support HB 75 Protection Act.
- Host church forums on liberty threats.

### **Guns**

**Conservative Position:**
- Permitless carry 2017; no assault bans.
- SAPA nullifies feds; 2025 SCOTUS loss appealed.
- Rural protections; CCW reciprocity broad.

**Progressive Position:**
- Background checks/red flags.
- Assault ban pushes; local controls.

**Christian Conservative Action:**
- NRA MO training; lobby against feds.
- Join Missouri Firearms Federation.
- Vote 2A defenders in House races.

### **Taxes**

**Conservative Position:**
- 2025 capital gains repeal; flat tax path.
- TCJA permanent; fuel tax indexed low.
- Waste audits save $500M+.

**Progressive Position:**
- Wealth taxes; corporate hikes.
- Fund social via raises.

**Christian Conservative Action:**
- Support Fitzpatrick audits.
- Missouri Club for Growth donations.
- Advocate no-new-taxes pledges.

### **Immigration**

**Conservative Position:**
- 2025 Kehoe orders track undocumented.
- E-Verify mandates; state ICE aid.
- No sanctuary; deport felons.

**Progressive Position:**
- Citizenship paths; humane borders.
- Oppose tracking/deportations.

**Christian Conservative Action:**
- Federation for American Immigration Reform MO.
- Support border bills in Congress.
- Church aid to legal immigrants only.

### **Family Values**

**Conservative Position:**
- Trans care ban minors; traditional marriage.
- Parental rights in medical/education.
- Anti-porn/trafficking funds.

**Progressive Position:**
- Gender affirming; equality expansions.
- Strip parental vetoes.

**Christian Conservative Action:**
- Missouri Family Policy Alliance (hypothetical; use FRC).
- Lobby SB 66 child protections.
- Family devotions on Proverbs 22:6.

### **Election Integrity**

**Conservative Position:**
- Voter ID/photo; roll cleanings.
- Paper ballots; fraud prosecutions.
- 2025 audits enhanced.

**Progressive Position:**
- Auto-reg; no ID barriers.
- Claim suppression.

**Christian Conservative Action:**
- Poll watcher training via SOS.
- Support clean rolls via Hoskins.
- Pray against fraud; Romans 13 obedience.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- **2026-10-06** - Voter registration deadline
- **2026-09-22** - Absentee voting begins
- **2026-08-04** - Primary Election
- **2026-11-03** - General Election

**Voter Registration:** sos.mo.gov/elections/govotemissouri/register

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
✅ **Share on social media** with #MissouriFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Missouri CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Missouri coverage
- **Missouri Right to Life** - Pro-life ratings
- **Missouri Family Policy Council** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Missouri Secretary of State**: sos.mo.gov
- **County Election Offices**: Find via county clerk websites
- **Early Voting Locations**: Absentee via mail/in-person at clerks

### **Conservative Organizations:**
- **Missouri Right to Life**: missourilife.org
- **Missouri Family Alliance**: (use familyresearchcouncil.org/mo)
- **Missouri Firearms Federation**: mofirearms.com
- **Missouri School Choice**: edchoice.org/states/missouri
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Missouri CHRISTIANS

**2026 Elections Matter:**
- AG race determines abortion ban enforcement
- Auditor affects school choice funding
- House seats impact national pro-life votes
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Capital gains cuts permanent
✅ Border tracking enhanced
✅ Waste audits save families money

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Tax hikes on workers
❌ Open borders chaos
❌ Bloated government spending

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Will Scharf, Dave Gregory, Scott Fitzpatrick, Ann Wagner and their families
- Missouri Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Missouri
- Revival and awakening in Missouri
- God's will in Missouri elections

**Scripture for Missouri Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Missouri coverage, email contact@ekewaka.com

**Missouri CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Missouri races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Missouri'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Missouri races...")
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

print(f"\nChecking for existing Missouri candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Missouri'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Missouri candidates...")
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

print("\nProcessing Missouri summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Missouri'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Missouri data upload complete!")