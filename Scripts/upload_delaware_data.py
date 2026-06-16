import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Delaware Races
races = [
    {
        "state": "Delaware",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the Class I U.S. Senate seat currently held by Chris Coons (D), a key race in a solidly Democratic state where conservatives seek to challenge the incumbent on issues like religious liberty and family values."
    },
    {
        "state": "Delaware",
        "office": "U.S. House At-Large District",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Delaware's single congressional district, held by Sarah McBride (D), focusing on national issues with local impact on education and immigration."
    },
    {
        "state": "Delaware",
        "office": "State Senate District 14",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Kent County district race between incumbent Kyra Hoffner (D) and challenger Mark Pugh (R), significant for conservative gains in rural areas."
    },
    {
        "state": "Delaware",
        "office": "State Representative District 20",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Sussex County district race following the 2025 special election won by Alonna Berry (D), with Nikki Miller (R) seeking a rematch to advance pro-family policies."
    }
]

# Delaware Candidates  
candidates = [
    # U.S. Senate
    {
        "name": "Chris Coons",
        "state": "Delaware",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Christopher Andrew Coons, born September 9, 1963, in Greenwich, Connecticut, is a U.S. Senator from Delaware since 2010. A graduate of Amherst College and Yale Law School, Coons served as New Castle County Executive before his Senate tenure. Married to Annie Lingenfelter, he has three children. Coons is known for bipartisan work on foreign policy and criminal justice reform, chairing the Senate Ethics Committee. His career includes private law practice and county government leadership, where he balanced budgets and promoted economic development.",
        "faith_statement": "As a Presbyterian who attends a Catholic church, Senator Coons has shared that his Christian faith shapes his commitment to justice, compassion, and bridging divides. In interviews, he has stated, 'My faith calls me to love my neighbor, even when we disagree, and to work for the common good.' (From Fox News Livin' The Bream Podcast, March 2025).",
        "website": "https://www.coons.senate.gov",
        "positions": {
            "ABORTION": "Pro-choice; supports federal protection for reproductive rights, including access to abortion care, and opposes restrictions post-Roe.",
            "EDUCATION": "Supports public school funding and opposes widespread school choice vouchers, emphasizing equity in education.",
            "RELIGIOUS-FREEDOM": "Supports protections for religious liberty but backs LGBTQ+ rights, including nondiscrimination laws that some conservatives view as conflicting.",
            "GUNS": "Favors common-sense gun reforms like universal background checks and red-flag laws while respecting Second Amendment rights.",
            "TAXES": "Advocates for progressive taxation and closing corporate loopholes to fund social programs.",
            "IMMIGRATION": "Supports comprehensive reform with pathway to citizenship and border security measures.",
            "FAMILY-VALUES": "Supports same-sex marriage and gender-affirming care for minors, opposing traditional marriage amendments.",
            "ELECTION-INTEGRITY": "Opposes strict voter ID laws, favoring expanded access like automatic registration."
        },
        "endorsements": ["Planned Parenthood", "Everytown for Gun Safety", "Human Rights Campaign"]
    },
    {
        "name": "Eric Hansen",
        "state": "Delaware",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Eric Hansen, a longtime Walmart executive and businessman from Newark, Delaware, ran for U.S. Senate in 2024. With a background in supply chain management at Procter & Gamble and Walmart, Hansen focuses on economic growth and reducing regulations. Married with children, he emphasizes family and community service through local business initiatives. His 2024 campaign highlighted tax relief and job creation, positioning him as a fresh voice against career politicians.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.erichansenforsenate.com",
        "positions": {
            "ABORTION": "Pro-life; supports state-level restrictions on abortion after 15 weeks and opposes federal funding for Planned Parenthood.",
            "EDUCATION": "Supports school choice and parental rights in curriculum decisions, including bans on critical race theory.",
            "RELIGIOUS-FREEDOM": "Strong advocate for religious liberty protections, opposing mandates that infringe on faith-based organizations.",
            "GUNS": "Strong Second Amendment supporter; opposes new gun control measures and supports concealed carry reciprocity.",
            "TAXES": "Favors tax cuts for individuals and businesses to stimulate economic growth.",
            "IMMIGRATION": "Calls for secure borders, ending sanctuary policies, and merit-based immigration reform.",
            "FAMILY-VALUES": "Supports traditional marriage and parental rights against gender ideology in schools.",
            "ELECTION-INTEGRITY": "Advocates for voter ID requirements and paper ballots to ensure election security."
        },
        "endorsements": ["National Rifle Association", "Family Research Council", "Delaware State GOP"]
    },
    # U.S. House
    {
        "name": "Sarah McBride",
        "state": "Delaware",
        "office": "U.S. House At-Large District",
        "party": "Democrat",
        "bio": "Sarah McBride, born August 9, 1990, in Wilmington, Delaware, is the first openly transgender member of Congress, elected in 2024. A graduate of American University, she served as spokesperson for the Human Rights Campaign and Delaware's First Lady during her father-in-law's governorship. Married to Andrew Cray before his passing, McBride has one child. Her work focuses on LGBTQ+ rights, healthcare, and economic equity.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://mcbride.house.gov",
        "positions": {
            "ABORTION": "Pro-choice; champion for reproductive justice and access to abortion services.",
            "EDUCATION": "Supports inclusive education and opposes parental rights bills that limit LGBTQ+ discussions.",
            "RELIGIOUS-FREEDOM": "Prioritizes nondiscrimination protections over religious exemptions in certain cases.",
            "GUNS": "Supports assault weapons bans and enhanced background checks.",
            "TAXES": "Favors raising taxes on the wealthy to fund social services.",
            "IMMIGRATION": "Supports DREAM Act and humane border policies.",
            "FAMILY-VALUES": "Advocates for LGBTQ+ family rights, including gender-affirming care.",
            "ELECTION-INTEGRITY": "Opposes voter suppression tactics like ID laws."
        },
        "endorsements": ["Human Rights Campaign", "Planned Parenthood", "Brady Campaign"]
    },
    {
        "name": "John Whalen III",
        "state": "Delaware",
        "office": "U.S. House At-Large District",
        "party": "Republican",
        "bio": "John Whalen III, a small business owner and Army veteran from Millsboro, Delaware, ran for U.S. House in 2024. With experience in logistics and community leadership, Whalen served in the Delaware National Guard. Married with family, he prioritizes veterans' affairs and economic freedom. His campaign emphasizes reducing government overreach and supporting working families.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://whalende.com",
        "positions": {
            "ABORTION": "Pro-life; supports defunding Planned Parenthood and state protections for the unborn.",
            "EDUCATION": "Advocates for school choice, vouchers, and parental control over education.",
            "RELIGIOUS-FREEDOM": "Defends faith-based institutions from government mandates.",
            "GUNS": "Upholds Second Amendment rights, opposing gun control legislation.",
            "TAXES": "Pushes for lower taxes and deregulation to boost small businesses.",
            "IMMIGRATION": "Enforces border security and ends chain migration.",
            "FAMILY-VALUES": "Promotes traditional family structures and opposes gender ideology in public schools.",
            "ELECTION-INTEGRITY": "Requires voter ID and audits to prevent fraud."
        },
        "endorsements": ["U.S. Chamber of Commerce", "National Federation of Independent Business", "Veterans of Foreign Wars"]
    },
    # State Senate District 14
    {
        "name": "Kyra Hoffner",
        "state": "Delaware",
        "office": "State Senate District 14",
        "party": "Democrat",
        "bio": "Kyra Hoffner, elected in 2022, represents Kent County's District 14. A former teacher and community organizer, she focuses on education and environmental issues. Married with children, Hoffner has a background in public service through local nonprofits. Her accomplishments include sponsoring bills for affordable housing and mental health support.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://senatedems.delaware.gov/hoffner",
        "positions": {
            "ABORTION": "Pro-choice; supports Delaware's protective abortion laws.",
            "EDUCATION": "Invests in public schools and teacher pay raises.",
            "RELIGIOUS-FREEDOM": "Balances with equality laws.",
            "GUNS": "Supports safe storage laws and background checks.",
            "TAXES": "Progressive taxation for infrastructure.",
            "IMMIGRATION": "Welcoming policies for immigrants.",
            "FAMILY-VALUES": "Inclusive family policies.",
            "ELECTION-INTEGRITY": "Expanded voting access."
        },
        "endorsements": ["Delaware Education Association", "Sierra Club", "Planned Parenthood DE"]
    },
    {
        "name": "Mark Pugh",
        "state": "Delaware",
        "office": "State Senate District 14",
        "party": "Republican",
        "bio": "Mark Pugh, a Pentecostal pastor and former professional wrestler known as Mark Briscoe, is a Smyrna resident running for State Senate District 14. Ordained in the Elim Pentecostal Church, where he recently became national leader, Pugh has overcome personal tragedies through faith. Married with family, he owns a construction business and coaches youth wrestling. His 2022 campaign focused on fiscal responsibility and family values; he aims to bring common sense to Dover.",
        "faith_statement": "As a devoted Pentecostal Christian, Pastor Pugh has preached, 'Faith is the anchor in life's storms; it calls us to stand for righteousness in public life, protecting the unborn and upholding biblical marriage.' (From Kensington Temple sermon, March 2024).",
        "website": "https://commonsense302.com",
        "positions": {
            "ABORTION": "Pro-life; advocates for heartbeat bills and support for pregnancy centers.",
            "EDUCATION": "Pushes for school choice and bans on divisive concepts in classrooms.",
            "RELIGIOUS-FREEDOM": "Strong protections for churches and faith-based adoption agencies.",
            "GUNS": "Defends Second Amendment; opposes red-flag laws.",
            "TAXES": "Cuts property taxes and eliminates corporate welfare.",
            "IMMIGRATION": "Secure borders and legal immigration only.",
            "FAMILY-VALUES": "Traditional marriage and parental rights against transgender policies in schools.",
            "ELECTION-INTEGRITY": "Voter ID and same-day voting."
        },
        "endorsements": ["Elim Pentecostal Church", "Delaware Family Policy Council", "National Right to Life"]
    },
    # State Rep District 20
    {
        "name": "Alonna Berry",
        "state": "Delaware",
        "office": "State Representative District 20",
        "party": "Democrat",
        "bio": "Alonna Berry, elected in the 2025 special election, represents Sussex County's District 20. A community advocate and former nonprofit director, she focuses on healthcare access and small business support. Married with children, Berry has volunteered in local schools and food banks. Her narrow victory highlighted her commitment to coastal communities.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice; defends access to reproductive healthcare.",
            "EDUCATION": "Fully funds public education.",
            "RELIGIOUS-FREEDOM": "Supports equality alongside faith rights.",
            "GUNS": "Reasonable gun safety measures.",
            "TAXES": "Fair share from corporations.",
            "IMMIGRATION": "Pathways for Dreamers.",
            "FAMILY-VALUES": "Support for all families.",
            "ELECTION-INTEGRITY": "Secure and accessible voting."
        },
        "endorsements": ["Delaware Democratic Party", "AARP", "League of Women Voters"]
    },
    {
        "name": "Nikki Miller",
        "state": "Delaware",
        "office": "State Representative District 20",
        "party": "Republican",
        "bio": "Dr. Nikki Miller, a veterinarian and Milton business owner, ran in the 2025 special election and is seeking the District 20 seat in 2026. A Lake Forest High School graduate, she serves on local boards and is active in animal welfare. Married with family, Miller's campaign emphasizes rural economic development and quality of life in Sussex County.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.nikkimillerforde.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions; supports alternatives to abortion.",
            "EDUCATION": "Empowers parents with choice options.",
            "RELIGIOUS-FREEDOM": "Safeguards for religious expression.",
            "GUNS": "Protects hunting and self-defense rights.",
            "TAXES": "Reduces burdensome regulations on farmers.",
            "IMMIGRATION": "Enforce laws and secure borders.",
            "FAMILY-VALUES": "Prioritizes nuclear family support.",
            "ELECTION-INTEGRITY": "Photo ID for voters."
        },
        "endorsements": ["Delaware Farm Bureau", "Sussex County GOP", "Delaware State Chamber of Commerce"]
    }
]

# Delaware Summary
summary = {
    "state": "Delaware",
    "title": "Delaware 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Delaware 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 4
**Total Candidates Profiled:** 8
**Election Dates:**
- 2026-09-15 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Delaware POLITICAL LANDSCAPE

### **The First State**

Delaware is a **solidly Democratic stronghold**:
- **Federal Dominance:** Both U.S. Senators and the at-large House seat held by Democrats since 2010, with Biden's home state loyalty.
- **State Government:** Democratic trifecta since 2009, controlling the General Assembly and governorship under John Carney until 2025.
- **Urban-Rural Divide:** Liberal Wilmington and suburbs contrast with conservative Sussex and Kent Counties, where rural voters push back on progressive policies.
- **Corporate Influence:** As the 'Corporate Capital,' Delaware's business-friendly laws attract donations that favor status quo.

### **Why Delaware Matters**

Delaware is **CHALLENGING but STRATEGIC** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Post-Roe, Democrats expanded abortion access up to birth; conservatives fight for heartbeat bills and defunding Planned Parenthood.
- ✅ **Second Amendment:** Strict gun laws including assault weapon bans; GOP seeks reciprocity and concealed carry expansion.
- ✅ **School Choice:** Limited vouchers; advocates push for ESA programs to empower parental rights.
- ✅ **Religious Liberty:** Threats from nondiscrimination laws impacting faith-based groups; need stronger RFRA protections.
- ✅ **Family Values:** Same-sex marriage since 2013; battle over gender ideology in schools and parental consent.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** Incumbent Chris Coons seeks a fourth term in a race that tests conservative mobilization in a blue state, impacting national debates on life and liberty.

**Chris Coons (Democrat)** - Incumbent U.S. Senator

**Faith Statement:** "My faith calls me to love my neighbor, even when we disagree, and to work for the common good."

**Background:**
- Yale Law graduate and former county executive.
- Bipartisan dealmaker on foreign aid.
- Family man with three children.

**Christian Conservative Analysis:**
- **Pro-Life:** 0/10 - Consistently pro-choice, cosponsoring abortion expansion bills.
- **Religious Liberty:** 4/10 - Supports faith dialogue but backs LGBTQ+ mandates over exemptions.
- **Education/Parental Rights:** 3/10 - Opposes choice vouchers, favors union-backed public schools.
- **Family Values:** 2/10 - Affirms same-sex marriage and gender care.
- **Overall Assessment:** 3/10 - Faith-informed but progressive priorities conflict with biblical conservatism.

**Key Positions:**
- **ABORTION:** Supports federal codification of Roe.
- **EDUCATION:** Increased public school funding, no choice expansion.
- **RELIGIOUS FREEDOM:** Balances with equality acts.
- **GUNS:** Universal checks and red-flag laws.
- **TAXES:** Close corporate loopholes.
- **IMMIGRATION:** Pathway to citizenship.

**Endorsements:** Planned Parenthood, Everytown.

**Website:** https://www.coons.senate.gov

**Eric Hansen (Republican)** - Businessman

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Walmart executive with supply chain expertise.
- Focus on economic reform.
- Husband and father committed to community.

**Christian Conservative Analysis:**
- **Pro-Life:** 8/10 - Backs restrictions and alternatives.
- **Religious Liberty:** 9/10 - Opposes faith-infringing mandates.
- **Education/Parental Rights:** 9/10 - Strong school choice advocate.
- **Family Values:** 8/10 - Traditional family focus.
- **Overall Assessment:** 8/10 - Solid conservative, needs faith emphasis for evangelicals.

**Key Positions:**
- **ABORTION:** 15-week limits.
- **EDUCATION:** Vouchers and CRT bans.
- **RELIGIOUS FREEDOM:** RFRA strengthening.
- **GUNS:** No new controls.
- **TAXES:** Cuts for growth.
- **IMMIGRATION:** Secure borders.

**Endorsements:** NRA, FRC.

**Website:** https://www.erichansenforsenate.com

**Why It Matters:** Flipping this seat advances national pro-life agenda.

### **U.S. House At-Large District** - 2026-11-03

**Context:** Sarah McBride's historic tenure faces challenge on family values and economy.

**Sarah McBride (Democrat)** - Incumbent Congresswoman

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- First transgender Congress member.
- HRC spokesperson.
- Advocate for equality.

**Christian Conservative Analysis:**
- **Pro-Life:** 0/10 - Vocal pro-choice.
- **Religious Liberty:** 2/10 - Prioritizes LGBTQ+ over faith exemptions.
- **Education/Parental Rights:** 1/10 - Opposes restrictions on gender topics.
- **Family Values:** 1/10 - Champions transgender rights.
- **Overall Assessment:** 1/10 - Clashes with biblical views on gender and life.

**Key Positions:**
- **ABORTION:** Full access.
- **EDUCATION:** Inclusive curricula.
- **RELIGIOUS FREEDOM:** Nondiscrimination first.
- **GUNS:** Ban assaults.
- **TAXES:** Tax the rich.
- **IMMIGRATION:** DREAMers.

**Endorsements:** HRC, PP.

**Website:** https://mcbride.house.gov

**John Whalen III (Republican)** - Veteran Businessman

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Army vet and small business owner.
- National Guard service.
- Family-focused leader.

**Christian Conservative Analysis:**
- **Pro-Life:** 9/10 - Defund PP.
- **Religious Liberty:** 8/10 - Protect churches.
- **Education/Parental Rights:** 9/10 - Choice and rights.
- **Family Values:** 9/10 - Traditional structures.
- **Overall Assessment:** 9/10 - Strong ally for conservatives.

**Key Positions:**
- **ABORTION:** State protections.
- **EDUCATION:** Parental control.
- **RELIGIOUS FREEDOM:** Defend faith.
- **GUNS:** Full rights.
- **TAXES:** Lower rates.
- **IMMIGRATION:** Enforce laws.

**Endorsements:** US Chamber, VFW.

**Website:** https://whalende.com

**Why It Matters:** Controls local impact on federal policies.

---

## 🔴 2026 STATE RACES

### **State Senate District 14** - 2026-11-03

**Context:** Rural Kent County battle for conservative voice in Dover.

**Kyra Hoffner (Democrat)** - Incumbent State Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Former teacher.
- Housing advocate.
- Mother in community service.

**Christian Conservative Analysis:**
- **Pro-Life:** 2/10 - Supports expansion.
- **Religious Liberty:** 5/10 - Equality focus.
- **Education/Parental Rights:** 4/10 - Public funding priority.
- **Family Values:** 3/10 - Inclusive policies.
- **Overall Assessment:** 4/10 - Moderate Dem, limited alignment.

**Key Positions:**
- **ABORTION:** Protective laws.
- **EDUCATION:** Teacher raises.
- **RELIGIOUS FREEDOM:** Balanced.
- **GUNS:** Safety measures.
- **TAXES:** Infrastructure funding.

**Endorsements:** DEA, Sierra Club.

**Website:** https://senatedems.delaware.gov/hoffner

**Mark Pugh (Republican)** - Pastor & Businessman

**Faith Statement:** "Faith is the anchor... stand for righteousness."

**Background:**
- Pentecostal leader.
- Wrestler turned pastor.
- Construction owner.

**Christian Conservative Analysis:**
- **Pro-Life:** 10/10 - Heartbeat advocate.
- **Religious Liberty:** 10/10 - Church protections.
- **Education/Parental Rights:** 10/10 - Choice champion.
- **Family Values:** 10/10 - Biblical marriage.
- **Overall Assessment:** 10/10 - Ideal faith-driven conservative.

**Key Positions:**
- **ABORTION:** Limits and centers.
- **EDUCATION:** Vouchers, bans.
- **RELIGIOUS FREEDOM:** Strong RFRA.
- **GUNS:** No restrictions.
- **TAXES:** Property cuts.

**Endorsements:** Elim Church, DFPC.

**Website:** https://commonsense302.com

**Why It Matters:** Gains ground in assembly for pro-family bills.

### **State Representative District 20** - 2026-11-03

**Context:** Sussex County rematch after close 2025 special; key for rural conservatism.

**Alonna Berry (Democrat)** - Incumbent State Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Nonprofit director.
- Coastal advocate.
- Family volunteer.

**Christian Conservative Analysis:**
- **Pro-Life:** 3/10 - Access supporter.
- **Religious Liberty:** 4/10 - Equality emphasis.
- **Education/Parental Rights:** 5/10 - Public focus.
- **Family Values:** 4/10 - Broad support.
- **Overall Assessment:** 4/10 - Community-oriented but liberal.

**Key Positions:**
- **ABORTION:** Healthcare access.
- **EDUCATION:** Full funding.
- **RELIGIOUS FREEDOM:** Nondiscrim.
- **GUNS:** Storage laws.
- **TAXES:** Corporate share.

**Endorsements:** DE Dems, AARP.

**Website:** ""

**Nikki Miller (Republican)** - Veterinarian

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Local vet and board member.
- Sussex native.
- Business owner.

**Christian Conservative Analysis:**
- **Pro-Life:** 7/10 - Exceptions with alternatives.
- **Religious Liberty:** 8/10 - Expression safeguards.
- **Education/Parental Rights:** 8/10 - Parent empowerment.
- **Family Values:** 8/10 - Nuclear priority.
- **Overall Assessment:** 8/10 - Practical conservative for rural DE.

**Key Positions:**
- **ABORTION:** Exceptions, alternatives.
- **EDUCATION:** Choice options.
- **RELIGIOUS FREEDOM:** Safeguards.
- **GUNS:** Hunting rights.
- **TAXES:** Farmer relief.

**Endorsements:** Farm Bureau, Sussex GOP.

**Website:** https://www.nikkimillerforde.com

**Why It Matters:** Shifts balance toward conservative legislation.

---

## 🎯 KEY ISSUES FOR Delaware CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Push for 6-week bans and parental consent; 50 pregnancy centers statewide.
- Defend against Dem expansions allowing late-term abortions.
- Recent challenge: 2024 law protecting providers from out-of-state suits.
- Victories: Limited funding battles won in 2023 budget.

**Progressive Position:**
- Codify Roe protections up to viability.
- State-funded abortions via Medicaid.
- Threats: Bills to repeal any future restrictions.

**Christian Conservative Action:**
- Join Delaware Citizens for Life (delawarerighttolife.org).
- Support HB 140 for consent laws.
- Volunteer at centers like Birthright of DE.
- Vote pro-life in all races.

### **School Choice & Parental Rights**

**Conservative Position:**
- Expand Opportunity Scholarships; current program serves 1,500 students.
- Ban CRT and gender ideology via HB 309.
- Homeschool freedom with minimal regs.
- Wins: 2024 parental notification law.

**Progressive Position:**
- Union control blocks vouchers.
- DEI mandates in curriculum.
- Threats to charter schools funding.

**Christian Conservative Action:**
- Run for local school boards in Sussex.
- Support SB 50 for ESAs.
- Join Delaware Family Policy Council (defpc.org).

### **Religious Freedom**

**Conservative Position:**
- Strengthen state RFRA against adoption mandates.
- Protect churches from COVID-style closures.
- Oppose bills forcing faith groups to affirm LGBTQ+.

**Progressive Position:**
- Nondiscrim laws overriding exemptions.
- Public funding cuts for faith schools.

**Christian Conservative Action:**
- Partner with Alliance Defending Freedom.
- Lobby against SB 13.
- Host forums with First Liberty Institute.

### **Guns**

**Conservative Position:**
- Reciprocity for carry permits.
- Oppose mag bans and red flags.
- Protect hunting in state parks.

**Progressive Position:**
- Assault ban and buybacks.
- Training mandates.

**Christian Conservative Action:**
- Delaware State Shooters Assoc (dssa.org).
- Support HB 102 for reciprocity.
- Train as poll watchers with gun rights focus.

### **Taxes**

**Conservative Position:**
- Cut property taxes 10%.
- End corporate subsidies for woke firms.
- Flat tax proposal.

**Progressive Position:**
- Raise on high earners.
- Corporate minimum tax.

**Christian Conservative Action:**
- Back Grover Norquist's no-tax pledge candidates.
- Join Americans for Tax Reform.

### **Immigration**

**Conservative Position:**
- End sanctuary status in cities.
- E-Verify for jobs.
- Border wall funding.

**Progressive Position:**
- Driver's licenses for undocumented.
- Sanctuary expansions.

**Christian Conservative Action:**
- Support FAIR (fairus.org) chapters.
- Vote against amnesty bills.

### **Family Values**

**Conservative Position:**
- Reaffirm traditional marriage.
- Ban gender transitions for minors.
- Parental opt-out for sex ed.

**Progressive Position:**
- Gender-neutral policies.
- Conversion therapy bans.

**Christian Conservative Action:**
- DFPC marriage defense.
- Oppose HB 267.

### **Election Integrity**

**Conservative Position:**
- Voter ID mandatory.
- Paper trails and audits.
- Clean voter rolls.

**Progressive Position:**
- Mail-in expansion.
- No ID.

**Christian Conservative Action:**
- Train with Election Integrity DE.
- Serve as watchers.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- 2026-07-14 - Filing deadline
- 2026-09-15 - Primary Election
- 2026-10-24 - Voter registration deadline
- 2026-11-03 - General Election

**Voter Registration:** elections.delaware.gov/voter-registration

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
✅ **Share on social media** with #DEFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Delaware CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Delaware coverage
- **Delaware Citizens for Life** - Pro-life ratings (delawarerighttolife.org)
- **Delaware Family Policy Council** - Faith-based education (defpc.org)
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Delaware Secretary of State**: elections.delaware.gov
- **County Election Offices**: Contact local supervisors via state site
- **Early Voting Locations**: Available 10 days pre-election at designated sites

### **Conservative Organizations:**
- **Delaware Citizens for Life**: delawarerighttolife.org
- **Delaware Family Alliance**: Via DFPC
- **Delaware State Shooters Association**: dssa.org
- **Delaware Charter Schools Network**: for choice (decharter.org)
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Delaware CHRISTIANS

**2026 Elections Matter:**
- U.S. Senate determines federal pro-life funding.
- House seat affects school choice bills.
- Legislative seats impact state gender laws.
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
✅ Border security prioritized

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Corporate taxes hike families
❌ Sanctuary state expansion
❌ Indoctrination in classrooms

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Eric Hansen, John Whalen III, Mark Pugh, Nikki Miller and their families
- Delaware Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Delaware
- Revival and awakening in Delaware
- God's will in Delaware elections

**Scripture for Delaware Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Delaware coverage, email contact@ekewaka.com

**DELAWARE CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Delaware races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Delaware'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Delaware races...")
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

print(f"\nChecking for existing Delaware candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Delaware'}
)['Items']
existing_candidate_map = {(c['name'], c['office']): c['candidate_id'] for c in existing_candidates}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Delaware candidates...")
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

print("\nProcessing Delaware summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Delaware'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Delaware data upload complete!")
