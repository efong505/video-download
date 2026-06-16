import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Maryland Races
races = [
    {
        "state": "Maryland",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The gubernatorial race will determine the state's chief executive, impacting policies on education, taxes, and public safety in this Democratic stronghold with conservative pockets on the Eastern Shore."
    },
    {
        "state": "Maryland",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Running on a joint ticket with the Governor, this race influences succession and key administrative roles."
    },
    {
        "state": "Maryland",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The Attorney General enforces state laws, a critical role in defending or challenging reproductive rights and election integrity."
    },
    {
        "state": "Maryland",
        "office": "Comptroller",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Oversees state finances and audits, affecting fiscal policies aligned with conservative tax relief goals."
    },
    {
        "state": "Maryland",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "A competitive district spanning the Eastern Shore and rural areas, key for conservative representation in Congress."
    },
    {
        "state": "Maryland",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Urban district including parts of Baltimore, heavily Democratic but watched for turnout shifts."
    },
    {
        "state": "Maryland",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Baltimore-based district, solid Democratic hold."
    },
    {
        "state": "Maryland",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Prince George's County district, strong Democratic lean."
    },
    {
        "state": "Maryland",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Southern Maryland district, Democratic incumbent."
    },
    {
        "state": "Maryland",
        "office": "U.S. House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Western Maryland and suburbs, potential swing with conservative voters."
    },
    {
        "state": "Maryland",
        "office": "U.S. House District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Baltimore City core, deep blue."
    },
    {
        "state": "Maryland",
        "office": "U.S. House District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Suburban Montgomery County, Democratic stronghold."
    }
]

# Maryland Candidates  
candidates = [
    {
        "name": "Wes Moore",
        "state": "Maryland",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Wes Moore, born in 1978 in Takoma Park, Maryland, is the current Governor serving since 2023. A Rhodes Scholar and combat veteran, Moore graduated from Johns Hopkins University and Oxford. He authored 'The Other Wes Moore,' a bestselling book about choices and fate. Before politics, he led the anti-poverty organization City Year and served as CEO of the Robin Hood Foundation in New York. Elected in 2022, Moore has focused on economic development, cutting middle-class taxes, and expanding reproductive rights. Married to Dawn Moore, a clinical psychologist, they have two daughters. His administration highlights record-low unemployment and crime reductions, positioning him as a pragmatic Democrat bridging divides. Moore's military service in the Army paratroopers and Bronze Star underscore his leadership. As governor, he's championed data-driven policies for equity, including investments in education and public safety. Critics note his progressive stances on social issues, but supporters praise bipartisan efforts like Republican endorsements for reelection.",
        "faith_statement": "Governor Moore, a devout Christian, has shared: 'My faith in God guides my service to Marylanders, reminding me that leadership is about lifting others as Christ lifted the marginalized.'",
        "website": "https://wesmoore.com",
        "positions": {
            "ABORTION": "Strongly pro-choice; signed proclamation enshrining reproductive freedom in the state constitution, protecting access post-Roe.",
            "EDUCATION": "Supports increased public school funding and universal pre-K; opposes widespread school choice but backs targeted scholarships.",
            "RELIGIOUS-FREEDOM": "Endorses broad protections but prioritizes LGBTQ+ rights; supported opt-out policies in recent SCOTUS case.",
            "GUNS": "Advocates for stricter gun control, including assault weapon bans and red-flag laws to reduce urban violence.",
            "TAXES": "Cut taxes for middle-class families; proposes progressive taxation to fund social programs without broad increases.",
            "IMMIGRATION": "Supports pathway to citizenship and sanctuary policies; focuses on humane border security and DACA protections.",
            "FAMILY-VALUES": "Promotes inclusive family policies, including gender-affirming care; emphasizes parental involvement in education.",
            "ELECTION-INTEGRITY": "Backs automatic voter registration and early voting expansion; opposes strict ID requirements."
        },
        "endorsements": ["Maryland AFL-CIO", "Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "Larry Hogan",
        "state": "Maryland",
        "office": "Governor",
        "party": "Republican",
        "bio": "Lawrence Joseph Hogan Jr., born in 1956 in Washington, D.C., served as Maryland's 62nd Governor from 2015 to 2023. Son of former Congressman Larry Hogan Sr., he founded Hogan Companies, a real estate firm, building a successful business career. Elected in a 2014 landslide as a moderate Republican, Hogan focused on economic growth, vetoing tax hikes and expanding charter schools. He navigated the COVID-19 pandemic with bipartisan praise, though criticized for school mask mandates. A cancer survivor (non-Hodgkin's lymphoma diagnosed 2015), Hogan underwent chemotherapy while governing. Married to June Wilkinson, a former Panamanian cabinet secretary, they have four children. Post-governorship, he ran unsuccessfully for U.S. Senate in 2024. Known for crossing party lines, Hogan earned high approval ratings. His administration cut $3.3 billion in taxes and invested in Bay restoration. As a fiscal conservative, he balanced budgets without broad cuts to services. Speculated for 2026 comeback, Hogan emphasizes unity over partisanship.",
        "faith_statement": "No publicly disclosed faith statement, though raised Catholic and attends Episcopalian services.",
        "website": "https://larryhogan.com",
        "positions": {
            "ABORTION": "Self-identifies as pro-choice; vetoed expansions but opposed federal bans; supports state protections with limits after viability.",
            "EDUCATION": "Strong advocate for school choice and charter expansion; increased funding for education while promoting accountability.",
            "RELIGIOUS-FREEDOM": "Supported religious exemptions in health mandates; defended faith-based adoption agencies.",
            "GUNS": "Enacted some gun safety laws like bump stock ban but protected concealed carry; NRA 'B' rating.",
            "TAXES": "Cut taxes by $3.3B; opposes new hikes, favors flat tax reforms for fairness.",
            "IMMIGRATION": "Supports legal immigration and border security; opposed sanctuary cities but backed DREAMers.",
            "FAMILY-VALUES": "Upholds traditional marriage but supports foster care reforms; emphasizes family economic stability.",
            "ELECTION-INTEGRITY": "Pushed for voter ID and paper ballots; sued over 2020 irregularities."
        },
        "endorsements": ["U.S. Chamber of Commerce", "NRA", "Maryland Farm Bureau"]
    },
    {
        "name": "John Myrick",
        "state": "Maryland",
        "office": "Governor",
        "party": "Republican",
        "bio": "John A. Myrick, a lifelong Marylander from Lanham in Prince George's County, is a U.S. Navy veteran and public servant announcing his 2026 gubernatorial bid in February 2025. With over 20 years in federal law enforcement, including roles at the Department of Justice and Homeland Security, Myrick specialized in counterterrorism and border security. He ran for U.S. Senate in 2024, emphasizing fiscal conservatism and public safety. A small business owner in real estate, Myrick is committed to community service, volunteering with local veterans' groups. Married with children, his family values drive his campaign against 'career politicians.' Myrick pledges to cut regulations, boost police funding, and protect Second Amendment rights. Tapped former Delegate Brenda Thiam as Lt. Gov. running mate in May 2025, aiming to appeal to diverse GOP voters. His platform targets Maryland's high taxes and crime, drawing from military discipline to promise accountable leadership. As an outsider, Myrick critiques both parties for fiscal irresponsibility.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://johnmyrickformdgovernor.org",
        "positions": {
            "ABORTION": "Pro-life; supports restrictions after 15 weeks and opposes state funding for abortions.",
            "EDUCATION": "Champions school choice vouchers and parental rights in curriculum decisions.",
            "RELIGIOUS-FREEDOM": "Strong defender of faith-based organizations against government overreach.",
            "GUNS": "Firm 2nd Amendment supporter; opposes red-flag laws and assault weapon bans.",
            "TAXES": "Advocates deep tax cuts and elimination of state income tax for low earners.",
            "IMMIGRATION": "Enforces strict border security; ends sanctuary policies in Maryland.",
            "FAMILY-VALUES": "Promotes traditional marriage and bans gender ideology in schools.",
            "ELECTION-INTEGRITY": "Mandates voter ID and audits all elections for transparency."
        },
        "endorsements": ["National Federation of Independent Business", "Veterans of Foreign Wars", "Maryland Republican Party"]
    },
    {
        "name": "Anthony G. Brown",
        "state": "Maryland",
        "office": "Attorney General",
        "party": "Democrat",
        "bio": "Anthony Gregory Brown, born in 1961 in New York City, is Maryland's 48th Attorney General since 2023. A Harvard Law graduate and Army JAG officer, Brown served two terms as Lieutenant Governor (2007-2015) under Martin O'Malley. He ran for governor in 2018 but lost the primary. As AG, Brown has sued the Trump administration over immigration and environmental policies, protecting reproductive rights. Married to Karmen Walker, a judge, they have two children. Brown's military service includes deploying to the Middle East. His focus includes consumer protection and civil rights enforcement. Critics from conservative groups call for investigations into his office's partisanship.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://www.marylandattorneygeneral.gov",
        "positions": {
            "ABORTION": "Vigorous defender of reproductive rights; leads multistate lawsuits against restrictions.",
            "EDUCATION": "Supports public school equity; opposes voucher expansions.",
            "RELIGIOUS-FREEDOM": "Balances with anti-discrimination; challenged parental opt-outs in LGBTQ+ curricula.",
            "GUNS": "Enforces strict gun laws; backs federal assault weapon bans.",
            "TAXES": "Favors progressive taxation to fund social services.",
            "IMMIGRATION": "Protects immigrant rights; opposes family separations.",
            "FAMILY-VALUES": "Inclusive policies for diverse families; supports gender-affirming care.",
            "ELECTION-INTEGRITY": "Expands access; fights voter suppression claims."
        },
        "endorsements": ["ACLU", "NAACP", "Sierra Club"]
    },
    {
        "name": "Brooke Lierman",
        "state": "Maryland",
        "office": "Comptroller",
        "party": "Democrat",
        "bio": "Brooke Elizabeth Lierman, born 1979 in Baltimore, is Maryland's 34th Comptroller since 2023, the first woman elected to the office. A former state delegate, she focused on women's rights and fiscal transparency. Lierman graduated from Goucher College and University of Baltimore School of Law. As Comptroller, she audits state spending and chairs the Board of Public Works. Married to Ben Sutherland, they have two children. Her career includes nonprofit work in child welfare. Lierman pushes for pay equity and environmental fiscal policies.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://www.marylandcomptroller.gov",
        "positions": {
            "ABORTION": "Pro-choice; supports state funding for access.",
            "EDUCATION": "Invests in public education funding; cautious on choice programs.",
            "RELIGIOUS-FREEDOM": "Upholds while prioritizing equality.",
            "GUNS": "Supports control measures in budget oversight.",
            "TAXES": "Audits for fair tax collection; backs middle-class relief.",
            "IMMIGRATION": "Inclusive fiscal policies for all residents.",
            "FAMILY-VALUES": "Family leave expansions and child care funding.",
            "ELECTION-INTEGRITY": "Transparent financial reporting for elections."
        },
        "endorsements": ["Emily's List", "Maryland League of Women Voters"]
    },
    {
        "name": "Andy Harris",
        "state": "Maryland",
        "office": "U.S. House District 1",
        "party": "Republican",
        "bio": "Andrew Peter Harris, M.D., born 1957 in Brooklyn, NY, is the U.S. Representative for MD-1 since 2011. A Johns Hopkins-trained anesthesiologist, Harris served in the Maryland Senate and House. Married to Sylvia Harris, they have five children. As Freedom Caucus Chairman, he pushes conservative agendas on spending and borders. Harris's medical background informs health policy critiques. He's a fiscal hawk, opposing omnibus bills.",
        "faith_statement": "'My Catholic faith compels me to protect the unborn and defend religious liberties in public life.'",
        "website": "https://harris.house.gov",
        "positions": {
            "ABORTION": "Pro-life; supports national heartbeat ban and defunds Planned Parenthood.",
            "EDUCATION": "Promotes school choice and opposes federal overreach in curricula.",
            "RELIGIOUS-FREEDOM": "Backs protections for faith-based groups; opposes mandates conflicting with beliefs.",
            "GUNS": "Strong 2nd Amendment defender; NRA A-rating, blocks gun control bills.",
            "TAXES": "Permanent TCJA extensions; cuts spending to reduce deficits.",
            "IMMIGRATION": "Secure borders; ends chain migration and sanctuary cities.",
            "FAMILY-VALUES": "Traditional marriage; protects parental rights against gender ideology.",
            "ELECTION-INTEGRITY": "Voter ID nationwide; audits 2020 election."
        },
        "endorsements": ["NRA", "Family Research Council", "National Right to Life"]
    }
]

# Maryland Summary
summary = {
    "state": "Maryland",
    "title": "Maryland 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Maryland 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 12
**Total Candidates Profiled:** 6
**Election Dates:**
- 2026-06-23 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Maryland POLITICAL LANDSCAPE

### **The Old Line State**

Maryland is a **deeply Democratic stronghold with conservative strongholds**:
- **Urban Dominance:** Baltimore City and Prince George's County deliver overwhelming Democratic margins, driven by progressive policies on social issues.
- **Rural Resilience:** The Eastern Shore and Western Maryland provide conservative counterbalance, emphasizing guns, faith, and limited government.
- **Urban-Rural Divide:** Baltimore's urban core contrasts with rural Somerset and Garrett Counties, where evangelicals and Catholics form voting blocs.
- **Chesapeake Factor:** Bay pollution and fishing rights unite conservatives across divides for environmental stewardship without green mandates.

### **Why Maryland Matters**

Maryland is **CHALLENGING but STRATEGIC** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Post-2024 amendment, abortion is enshrined; conservatives fight incremental restrictions amid expansion threats.
- ✅ **Second Amendment:** Strict laws prevail, but rural districts push back against bans; key for national carry reciprocity.
- ✅ **School Choice:** Limited BOOST scholarships exist; expand to counter DEI in public schools.
- ✅ **Religious Liberty:** SCOTUS Mahmoud v. Taylor victory mandates opt-outs for faith conflicts; defend against urban mandates.
- ✅ **Family Values:** Same-sex marriage since 2012; protect parental rights amid gender ideology pushes.
- ✅ **Bay Restoration:** Faith-based environmentalism aligns conservatives with stewardship mandates.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** This marquee race shapes Maryland's trajectory on life, liberty, and fiscal sanity in a blue state where conservative turnout can flip rural seats.

**Wes Moore (Democrat)** - Incumbent Governor

**Faith Statement:** "My faith in God guides my service to Marylanders, reminding me that leadership is about lifting others as Christ lifted the marginalized."

**Background:**
- Rhodes Scholar and Army veteran from Takoma Park.
- Bestselling author of 'The Other Wes Moore' on redemption.
- CEO of anti-poverty nonprofit; married with two daughters.

**Christian Conservative Analysis:**
- **Pro-Life:** 2/10 - Enshrined abortion rights; no restrictions supported.
- **Religious Liberty:** 4/10 - Backs opt-outs but prioritizes inclusivity over faith exemptions.
- **Education/Parental Rights:** 3/10 - Funds public schools heavily; limited choice.
- **Family Values:** 2/10 - Inclusive policies erode traditional definitions.
- **Overall Assessment:** 3/10 - Pragmatic but progressive; appeals to moderates, not biblical values.

**Key Positions:**
- **ABORTION:** Strongly pro-choice; constitutional protections.
- **EDUCATION:** Universal pre-K; opposes vouchers.
- **RELIGIOUS FREEDOM:** Balances with anti-discrimination.
- **GUNS:** Stricter controls.
- **TAXES:** Middle-class cuts, progressive hikes.
- **BAY POLLUTION:** Funds restoration without overregulation.

**Endorsements:** Planned Parenthood, AFL-CIO

**Website:** https://wesmoore.com

**Larry Hogan (Republican)** - Former Governor

**Faith Statement:** No publicly disclosed faith statement, though raised Catholic and attends Episcopalian services.

**Background:**
- Businessman and cancer survivor from D.C. suburbs.
- Served 2015-2023; high approval for bipartisanship.
- Married to June Wilkinson; four children.

**Christian Conservative Analysis:**
- **Pro-Life:** 5/10 - Vetoed expansions; claims pro-choice but past restrictions.
- **Religious Liberty:** 7/10 - Defended faith adoptions; balanced mandates.
- **Education/Parental Rights:** 8/10 - Expanded charters; accountability focus.
- **Family Values:** 6/10 - Traditional lean but moderate on social.
- **Overall Assessment:** 7/10 - Fiscal hawk aligns; moderate on life issues limits full endorsement.

**Key Positions:**
- **ABORTION:** Pro-choice with viability limits.
- **EDUCATION:** Charter expansion.
- **RELIGIOUS FREEDOM:** Exemptions in policies.
- **GUNS:** Some safety laws, pro-carry.
- **TAXES:** $3.3B cuts.
- **BAY POLLUTION:** Invested in cleanup.

**Endorsements:** U.S. Chamber, NRA

**Website:** https://larryhogan.com

**John Myrick (Republican)** - Navy Veteran

**Faith Statement:** No publicly disclosed faith statement.

**Background:**
- Law enforcement expert from Prince George's County.
- 2024 Senate candidate; small business owner.
- Married with children; tapped Brenda Thiam as mate.

**Christian Conservative Analysis:**
- **Pro-Life:** 9/10 - Supports 15-week limits; defund abortions.
- **Religious Liberty:** 9/10 - Shields faith groups.
- **Education/Parental Rights:** 9/10 - Vouchers and curriculum control.
- **Family Values:** 9/10 - Traditional protections.
- **Overall Assessment:** 9/10 - True conservative warrior for Maryland values.

**Key Positions:**
- **ABORTION:** Restrictions post-15 weeks.
- **EDUCATION:** School choice priority.
- **RELIGIOUS FREEDOM:** Anti-overreach.
- **GUNS:** Full 2A defense.
- **TAXES:** Eliminate low-income tax.
- **BAY POLLUTION:** Balanced stewardship.

**Endorsements:** NFIB, VFW

**Website:** https://johnmyrickformdgovernor.org

**Why It Matters:** Governor sets agenda on life protections; conservative win halts progressive overreach.

---

### **Attorney General** - 2026-11-03

**Context:** AG enforces laws on elections and rights; conservatives seek challenger to counter pro-choice litigations.

**Anthony G. Brown (Democrat)** - Incumbent

**Faith Statement:** No publicly disclosed faith statement.

**Background:**
- Harvard Law; Army JAG from NYC.
- Ex-Lt. Gov.; married to judge Karmen Walker.
- Sued Trump admin on immigration.

**Christian Conservative Analysis:**
- **Pro-Life:** 1/10 - Leads abortion defense suits.
- **Religious Liberty:** 3/10 - Challenges faith opt-outs.
- **Education/Parental Rights:** 2/10 - Backs public mandates.
- **Family Values:** 1/10 - Inclusive over traditional.
- **Overall Assessment:** 2/10 - Partisan progressive.

**Key Positions:**
- **ABORTION:** Defends access.
- **EDUCATION:** Equity focus.
- **RELIGIOUS FREEDOM:** Anti-discrimination priority.
- **GUNS:** Enforces bans.
- **TAXES:** Progressive support.

**Endorsements:** ACLU

**Website:** https://www.marylandattorneygeneral.gov

**Why It Matters:** AG can shield or shred election integrity; vote to protect ballots.

---

### **Comptroller** - 2026-11-03

**Context:** Fiscal watchdog role; audit transparency aids conservative tax fights.

**Brooke Lierman (Democrat)** - Incumbent

**Faith Statement:** No publicly disclosed faith statement.

**Background:**
- Baltimore native; Goucher Law grad.
- Ex-delegate; married with two kids.
- First female Comptroller.

**Christian Conservative Analysis:**
- **Pro-Life:** 2/10 - Funds access.
- **Religious Liberty:** 4/10 - Neutral audits.
- **Education/Parental Rights:** 3/10 - Public funding.
- **Family Values:** 3/10 - Leave expansions.
- **Overall Assessment:** 3/10 - Fiscal progressive.

**Key Positions:**
- **ABORTION:** Pro-choice funding.
- **EDUCATION:** Invests publicly.
- **RELIGIOUS FREEDOM:** Upholds equality.
- **GUNS:** Control oversight.
- **TAXES:** Fair collection.

**Endorsements:** Emily's List

**Website:** https://www.marylandcomptroller.gov

**Why It Matters:** Comptroller checks spending; conservative voice cuts waste.

---

### **U.S. House District 1** - 2026-11-03

**Context:** Eastern Shore's conservative bastion; hold for pro-life, pro-gun voice in D.C.

**Andy Harris (Republican)** - Incumbent

**Faith Statement:** "My Catholic faith compels me to protect the unborn and defend religious liberties in public life."

**Background:**
- Anesthesiologist from Brooklyn; Johns Hopkins alum.
- State legislator; married with five kids.
- Freedom Caucus leader.

**Christian Conservative Analysis:**
- **Pro-Life:** 10/10 - Heartbeat ban sponsor.
- **Religious Liberty:** 9/10 - Faith protections.
- **Education/Parental Rights:** 9/10 - Choice advocate.
- **Family Values:** 10/10 - Traditional defender.
- **Overall Assessment:** 10/10 - Gold standard for conservatives.

**Key Positions:**
- **ABORTION:** National bans.
- **EDUCATION:** Vouchers.
- **RELIGIOUS FREEDOM:** Exemptions.
- **GUNS:** NRA A.
- **TAXES:** TCJA permanent.

**Endorsements:** NRA, FRC

**Website:** https://harris.house.gov

**Why It Matters:** Retain to block federal overreach on values.

---

[Note: Other US House districts held by Democrats; focus turnout to challenge incumbents like Sarbanes (2), Sarbanes (3), etc., but no major challengers yet.]

---

## 🎯 KEY ISSUES FOR Maryland CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Incremental bans post-15 weeks; 50+ pregnancy centers via Maryland Right to Life.
- Parental consent for minors; defund abortions in Medicaid.
- Recent: Blocked late-term expansions.
- Challenges: 2024 amendment cements access.

**Progressive Position:**
- Unlimited up to birth; state-funded travel.
- Attacks on centers as 'deceptive.'

**Christian Conservative Action:**
- Join Maryland Right to Life (mdrtl.org).
- Support HB 777 restrictions.
- Volunteer at centers; vote pro-life tickets.

### **School Choice & Parental Rights**

**Conservative Position:**
- BOOST program aids 5,000 students; expand to $20M.
- Bans CRT/gender lessons in 2024 law.
- Homeschool freedom strong; 10% enrollment.
- Wins: SCOTUS opt-out mandate.

**Progressive Position:**
- Union dominance; DEI mandates.
- Veto choice expansions.

**Christian Conservative Action:**
- Run for school boards in rural counties.
- Back SB 1000 choice bill.
- Join Maryland Family Institute (marylandfamily.org).

### **Religious Freedom**

**Conservative Position:**
- Protections via Article 36; faith exemptions in adoptions.
- SCOTUS win blocks LGBTQ+ curriculum force.
- Threats: Urban non-discrimination overrides.

**Progressive Position:**
- Mandates inclusivity over belief.

**Christian Conservative Action:**
- Support Alliance Defending Freedom cases.
- Lobby for RFRA strengthening.
- Church forums on liberty.

### **Guns**

**Conservative Position:**
- Rural carry rights; oppose 2023 bans.
- Preemption for uniform laws.
- Status: Strict but Eastern Shore resists.

**Progressive Position:**
- Assault bans, mag limits.

**Christian Conservative Action:**
- Join Maryland Shall Issue (mdshallissue.org).
- Oppose HB 4 expansions.
- Train church safety teams.

### **Taxes**

**Conservative Position:**
- Hogan-era $3B cuts; flat tax push.
- No new hikes; audit waste.

**Progressive Position:**
- Soak-the-rich increases.

**Christian Conservative Action:**
- Support Taxpayer Bill of Rights.
- Contact delegates on budgets.
- Promote tithing as stewardship.

### **Immigration**

**Conservative Position:**
- End sanctuary in Baltimore; E-Verify mandate.
- Secure borders protect jobs.

**Progressive Position:**
- Pathways without enforcement.

**Christian Conservative Action:**
- Back FAIR legislation.
- Volunteer border aid missions.
- Pray for just reform.

### **Family Values**

**Conservative Position:**
- Traditional marriage defense; parental notification.
- Ban gender transitions for minors.

**Progressive Position:**
- Full LGBTQ+ affirmations.

**Christian Conservative Action:**
- Join Family Policy Alliance.
- Host Bible studies on Proverbs 22:6.
- Oppose HB 881.

### **Election Integrity**

**Conservative Position:**
- Voter ID, paper trails; audit 2020 anomalies.
- Clean rolls via ERIC opt-out.

**Progressive Position:**
- Mail-in expansion without checks.

**Christian Conservative Action:**
- Become poll watchers.
- Support SB 598 ID bill.
- Prayer vigils for honest counts.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- **2026-05-01** - Voter registration deadline (continuous, but 21 days pre-primary)
- **2026-06-01** - Early voting begins
- **2026-06-23** - Primary Election
- **2026-11-03** - General Election

**Voter Registration:** elections.maryland.gov/voter_registration

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
✅ **Share on social media** with #MarylandFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Maryland CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Maryland coverage
- **Maryland Right to Life** - Pro-life ratings
- **Maryland Family Institute** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Maryland Secretary of State**: elections.maryland.gov
- **County Election Offices**: Via state site search
- **Early Voting Locations**: County boards list

### **Conservative Organizations:**
- **Maryland Right to Life**: mdrtl.org
- **Maryland Family Institute**: marylandfamily.org
- **Maryland Shall Issue**: mdshallissue.org
- **Maryland BOOST for Kids**: marylandboostforkids.org
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Maryland CHRISTIANS

**2026 Elections Matter:**
- Governor determines abortion defenses.
- AG affects election safeguards.
- House seats impact federal life bills.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Bay cleanup without green taxes
✅ Tax relief for families
✅ Rural voices amplified

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Sanctuary state harms communities
❌ Tax hikes burden working families
❌ Urban policies ignore rural faith

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Larry Hogan, John Myrick, and their families
- Maryland Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Maryland
- Revival and awakening in Maryland
- God's will in Maryland elections

**Scripture for Maryland Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Maryland coverage, email contact@ekewaka.com

**Maryland CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Maryland races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Maryland'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Maryland races...")
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

print(f"\nChecking for existing Maryland candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Maryland'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Maryland candidates...")
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

print("\nProcessing Maryland summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Maryland'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Maryland data upload complete!")