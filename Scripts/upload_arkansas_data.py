import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Arkansas Races
races = [
    {
        "state": "Arkansas",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Republican Sen. Tom Cotton seeks re-election in a race critical for maintaining conservative control of the Senate."
    },
    {
        "state": "Arkansas",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Rep. Rick Crawford (R) defends his seat in the northeastern Arkansas district."
    },
    {
        "state": "Arkansas",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Contested race for Central Arkansas seat held by Rep. French Hill (R)."
    },
    {
        "state": "Arkansas",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Rep. Steve Womack (R) faces Democratic challengers in the northwest district."
    },
    {
        "state": "Arkansas",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Rep. Bruce Westerman (R) seeks re-election in southern Arkansas."
    },
    {
        "state": "Arkansas",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Gov. Sarah Huckabee Sanders (R) runs for re-election, pivotal for conservative policies."
    },
    {
        "state": "Arkansas",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Lt. Gov. Leslie Rutledge (R) up for re-election."
    },
    {
        "state": "Arkansas",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent AG Tim Griffin (R) defends role in upholding state laws."
    },
    {
        "state": "Arkansas",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Competitive Republican primary for this key election oversight position."
    },
    {
        "state": "Arkansas",
        "office": "Auditor of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Dennis Milligan (R) seeks another term."
    },
    {
        "state": "Arkansas",
        "office": "Treasurer of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent John Thurston (R) up for re-election."
    },
    {
        "state": "Arkansas",
        "office": "Commissioner of State Lands",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open race with Republican contenders."
    }
]

# Arkansas Candidates  
candidates = [
    {
        "name": "Tom Cotton",
        "state": "Arkansas",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Thomas Bryant Cotton, born May 13, 1977, in Dardanelle, Arkansas, is a sixth-generation Arkansan raised on his family's cattle farm in Yell County. He graduated from Harvard College with an A.B. in government and later earned a J.D. from Harvard Law School. Cotton served as an Army officer, deploying to Iraq and Afghanistan, earning a Bronze Star for combat leadership. Elected to the U.S. House in 2012, he joined the Senate in 2015. Married to Anna Cotton, a lawyer, they have two sons, Gabriel and Daniel. Cotton's career highlights include authoring the RESPECT for Marriage Act amendments and leading on national security issues.",
        "faith_statement": "As a devout Southern Baptist, Sen. Cotton has stated, 'My faith in Jesus Christ guides my service to Arkansas and America, grounding my commitment to life, liberty, and justice for all.'",
        "website": "https://www.cotton.senate.gov",
        "positions": {
            "ABORTION": "Strongly pro-life; supports defunding Planned Parenthood, national abortion ban after 15 weeks, and overturning Roe v. Wade, which he celebrated as a victory for the unborn.",
            "EDUCATION": "Advocates for school choice, vouchers, and parental rights; opposes federal overreach in curriculum, supporting Arkansas's LEARNS Act expansion.",
            "RELIGIOUS-FREEDOM": "Fierce defender of religious liberty; co-sponsored First Amendment Defense Act to protect faith-based organizations from discrimination.",
            "GUNS": "A-rated by NRA; staunch 2nd Amendment advocate, opposes red-flag laws and universal background checks, supports concealed carry reciprocity.",
            "TAXES": "Supports permanent extension of 2017 Tax Cuts and Jobs Act; pushes for lower corporate rates to boost Arkansas jobs.",
            "IMMIGRATION": "Calls for border wall completion, ending chain migration, and merit-based system; criticizes sanctuary cities and supports E-Verify.",
            "FAMILY-VALUES": "Upholds traditional marriage; supports parental rights in education against gender ideology; backs bans on transgender sports participation.",
            "ELECTION-INTEGRITY": "Strong supporter of voter ID laws, paper ballots, and purging non-citizens from rolls; co-sponsored SAVE Act."
        },
        "endorsements": ["National Right to Life", "Family Research Council", "NRA"]
    },
    {
        "name": "Hallie Shoffner",
        "state": "Arkansas",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Hallie Shoffner is a sixth-generation Arkansas farmer from northeast Arkansas, running her family's farm while raising her children. A dedicated community leader, she has advocated for rural families and workers facing economic challenges. Shoffner launched her Senate bid in July 2025 to challenge the status quo and fight for working Arkansans. Her background in agriculture informs her focus on fair economic policies and family support.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.hallieshoffner.com",
        "positions": {
            "ABORTION": "Supports reproductive rights, including access to abortion services up to viability, opposing state bans and emphasizing women's health.",
            "EDUCATION": "Favors increased public school funding, teacher pay raises; supports universal pre-K but cautious on vouchers to avoid defunding public schools.",
            "RELIGIOUS-FREEDOM": "Believes in protecting religious liberty while ensuring no discrimination based on faith; supports separation of church and state.",
            "GUNS": "Advocates for universal background checks and red-flag laws to prevent gun violence, while respecting hunting traditions.",
            "TAXES": "Pushes for fair taxation on the wealthy to fund social programs; opposes cuts that benefit corporations over families.",
            "IMMIGRATION": "Supports pathway to citizenship for DREAMers, comprehensive reform with border security but opposes wall funding.",
            "FAMILY-VALUES": "Promotes inclusive family policies, including LGBTQ+ rights and gender-affirming care access for youth.",
            "ELECTION-INTEGRITY": "Opposes restrictive voter ID laws; supports automatic registration and mail-in voting expansion."
        },
        "endorsements": ["EMILY's List", "Planned Parenthood Action Fund"]
    },
    {
        "name": "Sarah Huckabee Sanders",
        "state": "Arkansas",
        "office": "Governor",
        "party": "Republican",
        "bio": "Sarah Huckabee Sanders, born August 13, 1982, in Hope, Arkansas, is the 47th Governor since 2023, the first woman in that role. Daughter of former Gov. Mike Huckabee, she graduated from Ouachita Baptist University. Sanders served as White House Press Secretary under Trump and managed his 2016 campaign. Married to Bryan Sanders, a political consultant, they have three children: Huck, Scarlett, and George. Her accomplishments include signing the LEARNS Act for education reform and pro-life protections.",
        "faith_statement": "'As a Christian, my faith in God guides every decision I make as Governor, from protecting the unborn to defending religious liberty for all Arkansans.'",
        "website": "https://governor.arkansas.gov",
        "positions": {
            "ABORTION": "Signed trigger law banning nearly all abortions post-Roe; supports heartbeat bill and defunding Planned Parenthood.",
            "EDUCATION": "Authored LEARNS Act expanding school choice, vouchers up to $6,600, teacher merit pay, and banning CRT/ind indoctrination.",
            "RELIGIOUS-FREEDOM": "Enacted Arkansas Religious Freedom Restoration Act; protects faith-based adoption agencies.",
            "GUNS": "Signed permitless carry law; opposes any gun control, supports constitutional carry.",
            "TAXES": "Cut income taxes, eliminated grocery tax; advocates for flat tax to spur growth.",
            "IMMIGRATION": "Supports state enforcement of federal laws, E-Verify for businesses, opposes sanctuary policies.",
            "FAMILY-VALUES": "Bans gender-affirming care for minors; defines marriage as man-woman; promotes parental rights.",
            "ELECTION-INTEGRITY": "Requires voter ID, photo ID for absentee; audits election processes."
        },
        "endorsements": ["Susan B. Anthony Pro-Life America", "Alliance Defending Freedom", "NRA"]
    },
    {
        "name": "Fred Love",
        "state": "Arkansas",
        "office": "Governor",
        "party": "Democrat",
        "bio": "State Sen. Fred Love, representing District 15 since 2023, previously served in the House from 2011-2023. A Little Rock native, he is a small business owner in real estate and community development. Love focuses on education, economic growth, and healthcare access. Married with children, he is committed to bipartisan solutions for Arkansas families.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Supports restoring Roe v. Wade protections; opposes total bans, favors exceptions for health.",
            "EDUCATION": "Pushes for full public school funding, teacher raises; supports pre-K expansion without vouchers draining public funds.",
            "RELIGIOUS-FREEDOM": "Protects religious liberty but opposes using it to discriminate against LGBTQ+ individuals.",
            "GUNS": "Supports background checks and closing loopholes; balances rights with public safety.",
            "TAXES": "Favors progressive taxation to invest in infrastructure and education; opposes corporate giveaways.",
            "IMMIGRATION": "Advocates humane reform, DACA protections, and workforce integration.",
            "FAMILY-VALUES": "Inclusive policies for all families, including support for adoption and foster care reforms.",
            "ELECTION-INTEGRITY": "Ensures access with early voting; supports secure but non-suppressive ID laws."
        },
        "endorsements": ["Arkansas Education Association", "AFL-CIO"]
    },
    {
        "name": "Tim Griffin",
        "state": "Arkansas",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "John Timothy Griffin, born August 21, 1968, in Charlotte, NC, but raised in Magnolia, AR, is the 57th AG since 2023. A fifth-generation Arkansan, son of a minister, he graduated from Ouachita Baptist University and Harvard Law. Served as U.S. Attorney, Lt. Gov., and U.S. Rep. Married to Elizabeth Griffin, they have three children. Griffin has sued the Biden admin over 100 times on conservative issues.",
        "faith_statement": "'My Christian faith, instilled by my father, a Baptist minister, compels me to defend the vulnerable, from the unborn to religious communities.'",
        "website": "https://arkansasag.gov",
        "positions": {
            "ABORTION": "Defends state ban in court; pro-life absolutist, no exceptions except mother's life.",
            "EDUCATION": "Supports school choice and parental rights; backs bans on divisive concepts.",
            "RELIGIOUS-FREEDOM": "Filed suits protecting faith-based groups; authored religious liberty opinions.",
            "GUNS": "Pro-2A; defended permitless carry against challenges.",
            "TAXES": "Advocates low taxes; sued feds over regulatory costs.",
            "IMMIGRATION": "Sues over border policies; supports state crackdowns on illegal immigration.",
            "FAMILY-VALUES": "Opposes gender ideology in schools; protects traditional values.",
            "ELECTION-INTEGRITY": "Enforces voter ID; investigates fraud claims."
        },
        "endorsements": ["Faith & Freedom Coalition", "National Sheriffs' Association"]
    },
    {
        "name": "French Hill",
        "state": "Arkansas",
        "office": "U.S. House District 2",
        "party": "Republican",
        "bio": "James French Hill, born December 5, 1956, in Los Angeles but ninth-generation Arkansan, is U.S. Rep. since 2015. Wharton MBA, banker, founded Crews & Associates. Served on Little Rock City Board. Married to Martha Hill, five children. Focuses on financial services and economic growth.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://hill.house.gov",
        "positions": {
            "ABORTION": "Pro-life; supports restrictions and defunding abortion providers.",
            "EDUCATION": "Backs school choice and workforce training; opposes federal mandates.",
            "RELIGIOUS-FREEDOM": "Supports protections for faith communities.",
            "GUNS": "Strong 2A supporter; NRA endorsed.",
            "TAXES": "Led tax reform efforts; permanent TCJA extension.",
            "IMMIGRATION": "Secure borders, legal immigration pathways.",
            "FAMILY-VALUES": "Traditional family support; parental rights.",
            "ELECTION-INTEGRITY": "Voter ID and secure elections."
        },
        "endorsements": ["U.S. Chamber of Commerce", "NRA"]
    },
    {
        "name": "Chris Jones",
        "state": "Arkansas",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "bio": "Christopher Michael Jones, born October 13, 1976, is a nuclear engineer, ordained Baptist minister, and 2022 gubernatorial nominee. PhD from University of Arkansas, works at Entergy. First African-American major party nominee for AR governor. Married to Sarah, three children. Advocates for education and economic justice.",
        "faith_statement": "'As an ordained minister, my faith calls me to serve the least of these, bridging divides with compassion and justice.'",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice with limits; supports exceptions and access.",
            "EDUCATION": "Invest in public schools, teacher pay; universal pre-K.",
            "RELIGIOUS-FREEDOM": "Protects all faiths; opposes theocracy.",
            "GUNS": "Common-sense reforms like background checks.",
            "TAXES": "Fair share from wealthy; middle-class relief.",
            "IMMIGRATION": "Comprehensive reform, DREAMers.",
            "FAMILY-VALUES": "Inclusive, supporting all families.",
            "ELECTION-INTEGRITY": "Secure and accessible voting."
        },
        "endorsements": ["Sierra Club", "Planned Parenthood"]
    },
    {
        "name": "Steve Womack",
        "state": "Arkansas",
        "office": "U.S. House District 3",
        "party": "Republican",
        "bio": "Stephen Allen Womack, born January 18, 1957, in Russellville, AR, is Rep. since 2011. Army National Guard veteran, retired Brig. Gen., former Mayor of Rogers. BS from Arkansas Tech. Married to Terry, three children. Senior on House Rules Committee.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://womack.house.gov",
        "positions": {
            "ABORTION": "Pro-life; Hyde Amendment supporter.",
            "EDUCATION": "School choice advocate.",
            "RELIGIOUS-FREEDOM": "Defends faith-based rights.",
            "GUNS": "NRA A-rated; pro-2A.",
            "TAXES": "Tax cutter.",
            "IMMIGRATION": "Border security first.",
            "FAMILY-VALUES": "Traditional values.",
            "ELECTION-INTEGRITY": "Voter ID laws."
        },
        "endorsements": ["Heritage Action", "NRA"]
    },
    {
        "name": "Robb Ryerse",
        "state": "Arkansas",
        "office": "U.S. House District 3",
        "party": "Democrat",
        "bio": "Robb Ryerse is a former evangelical pastor, author, and political organizer. Ran for Congress in 2018 as Republican but now Democrat. Focuses on faith-informed progressive values. Author of 'Running for Our Lives.' Committed to honest politics and climate action.",
        "faith_statement": "'My evangelical faith compels me to fight for justice, truth, and moral integrity in politics.'",
        "website": "https://www.robbforcongress.com",
        "positions": {
            "ABORTION": "Pro-choice; reproductive justice as faith issue.",
            "EDUCATION": "Fully fund public education; oppose vouchers.",
            "RELIGIOUS-FREEDOM": "Inclusive liberty for all beliefs.",
            "GUNS": "End gun violence epidemic with reforms.",
            "TAXES": "Tax the rich; invest in people.",
            "IMMIGRATION": "Humane borders, amnesty paths.",
            "FAMILY-VALUES": "Protect all families, LGBTQ+ rights.",
            "ELECTION-INTEGRITY": "No suppression; expand access."
        },
        "endorsements": ["Progressive Change Campaign Committee"]
    }
]

# Arkansas Summary
summary = {
    "state": "Arkansas",
    "title": "Arkansas 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Arkansas 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 12
**Total Candidates Profiled:** 9
**Election Dates:**
- 2026-03-03 (Preferential Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Arkansas POLITICAL LANDSCAPE

### **The Natural State**

Arkansas is a **solidly conservative stronghold**:
- **GOP Dominance:** Republicans hold supermajorities in the legislature (82-18 House, 29-6 Senate), all statewide offices, and both U.S. Senate seats since 2014.
- **Evangelical Influence:** Over 50% white evangelical Protestants per Pew, driving social conservative policies.
- **Urban-Rural Divide:** Little Rock/Pulaski County leans Democratic (20% of population), while rural northwest (Benton/Washington Counties) and south are deep red strongholds.
- **Bible Belt Heartland:** Strong church attendance shapes pro-life, pro-family laws; recent Christian nationalism debates over Ten Commandments displays.

### **Why Arkansas Matters**

Arkansas is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Trigger law bans abortions except to save mother's life; heartbeat bill passed; defunded Planned Parenthood; Arkansas Right to Life active.
- ✅ **Second Amendment:** Permitless carry since 2021; no assault weapon bans; top-10 gun-friendly state per Guns & Ammo.
- ✅ **School Choice:** LEARNS Act (2023) provides $730M in vouchers, teacher raises, bans on CRT/gender ideology.
- ✅ **Religious Liberty:** 2022 constitutional amendment strengthens RFRA; protects faith-based foster care.
- ✅ **Family Values:** Bans gender-affirming care for minors (2021); traditional marriage enshrined; parental rights expanded.
- ✅ **Election Security:** Strict voter ID, photo for absentee; paper trails required.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** Retaining Sen. Cotton's seat ensures GOP Senate majority, blocking progressive agendas on life and liberty.

**Tom Cotton (Republican)** - Incumbent U.S. Senator

**Faith Statement:** "As a devout Southern Baptist, Sen. Cotton has stated, 'My faith in Jesus Christ guides my service to Arkansas and America, grounding my commitment to life, liberty, and justice for all.'"

**Background:**
- Sixth-generation farmer from Yell County cattle ranch.
- Harvard grad, Army Bronze Star veteran (Iraq/Afghanistan deployments).
- Elected to Senate 2014; married with two sons.

**Christian Conservative Analysis:**
- **Pro-Life:** 100% SBA Pro-Life score; led defund Planned Parenthood efforts.
- **Religious Liberty:** Co-sponsored FADA; defended faith adoptions.
- **Education/Parental Rights:** School choice champion; opposes indoctrination.
- **Family Values:** Traditional marriage defender; anti-gender ideology.
- **Overall Assessment:** 9/10 - Battle-tested warrior for biblical values.

**Key Positions:**
- **ABORTION:** National 15-week ban; celebrate Roe overturn.
- **EDUCATION:** Vouchers, parental control over curriculum.
- **RELIGIOUS FREEDOM:** Protect churches from LGBTQ+ lawsuits.
- **GUNS:** NRA A+; reciprocity nationwide.
- **TAXES:** Permanent TCJA cuts for families.
- **IMMIGRATION:** Wall, end chain migration.

**Endorsements:** National Right to Life, FRC, NRA

**Website:** https://www.cotton.senate.gov

**Hallie Shoffner (Democrat)** - Farmer & Mother

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Sixth-generation northeast AR farmer.
- Community advocate for rural workers.
- Launched 2025 bid against economic elites.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports abortion access; opposes bans.
- **Religious Liberty:** Favors separation; risks faith protections.
- **Education/Parental Rights:** Public funding focus; voucher skeptic.
- **Family Values:** Inclusive but erodes traditional norms.
- **Overall Assessment:** 3/10 - Prioritizes progressive over biblical priorities.

**Key Positions:**
- **ABORTION:** Up to viability with health exceptions.
- **EDUCATION:** Boost public schools, universal pre-K.
- **RELIGIOUS FREEDOM:** No discrimination via faith.
- **GUNS:** Background checks, red flags.
- **TAXES:** Tax wealthy for programs.
- **IMMIGRATION:** Citizenship paths, no wall.

**Endorsements:** EMILY's List, Planned Parenthood

**Why It Matters:** Senate control decides national pro-life, religious freedom battles.

---

### **U.S. House District 2** - 2026-11-03

**Context:** Central AR seat influences banking, education policy; hold for conservative voice.

**French Hill (Republican)** - Incumbent U.S. Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Ninth-generation Arkansan, Wharton MBA banker.
- Little Rock City Director; founded investment firm.
- Married with five children.

**Christian Conservative Analysis:**
- **Pro-Life:** Defends unborn via Hyde support.
- **Religious Liberty:** Backs faith protections.
- **Education/Parental Rights:** Choice advocate.
- **Family Values:** Traditional family policies.
- **Overall Assessment:** 8/10 - Reliable on core issues.

**Key Positions:**
- **ABORTION:** Restrictions, defund providers.
- **EDUCATION:** Workforce training, choice.
- **RELIGIOUS FREEDOM:** Community protections.
- **GUNS:** Strong 2A, NRA-backed.
- **TAXES:** TCJA permanence.
- **IMMIGRATION:** Secure borders.

**Endorsements:** U.S. Chamber, NRA

**Website:** https://hill.house.gov

**Chris Jones (Democrat)** - Nuclear Engineer & Minister

**Faith Statement:** "'As an ordained minister, my faith calls me to serve the least of these, bridging divides with compassion and justice.'"

**Background:**
- PhD nuclear engineer at Entergy.
- First Black major-party AR gov nominee (2022).
- Married with three children.

**Christian Conservative Analysis:**
- **Pro-Life:** Choice with limits; not absolutist.
- **Religious Liberty:** Inclusive but risks overreach.
- **Education/Parental Rights:** Public focus.
- **Family Values:** Broad inclusivity.
- **Overall Assessment:** 4/10 - Faith-driven but progressive tilt.

**Key Positions:**
- **ABORTION:** Access with exceptions.
- **EDUCATION:** Teacher pay, pre-K.
- **RELIGIOUS FREEDOM:** All faiths protected.
- **GUNS:** Reforms for safety.
- **TAXES:** Middle-class relief.
- **IMMIGRATION:** Humane reform.

**Endorsements:** Sierra Club, Planned Parenthood

**Why It Matters:** Shapes federal family, education laws impacting AR churches.

---

### **U.S. House District 3** - 2026-11-03

**Context:** NW AR growth area; retain for rules committee influence on conservative bills.

**Steve Womack (Republican)** - Incumbent U.S. Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Army Brig. Gen. veteran, Rogers Mayor.
- Arkansas Tech grad.
- Married with three children.

**Christian Conservative Analysis:**
- **Pro-Life:** Consistent Hyde votes.
- **Religious Liberty:** Defender.
- **Education/Parental Rights:** Choice supporter.
- **Family Values:** Aligned with traditions.
- **Overall Assessment:** 8/10 - Steady conservative.

**Key Positions:**
- **ABORTION:** Pro-life restrictions.
- **EDUCATION:** School choice.
- **RELIGIOUS FREEDOM:** Faith rights.
- **GUNS:** NRA A.
- **TAXES:** Cuts.
- **IMMIGRATION:** Security.

**Endorsements:** Heritage Action, NRA

**Website:** https://womack.house.gov

**Robb Ryerse (Democrat)** - Former Pastor

**Faith Statement:** "'My evangelical faith compels me to fight for justice, truth, and moral integrity in politics.'"

**Background:**
- Evangelical pastor, author on faith/politics.
- 2018 congressional candidate.
- Focus on progressive faith values.

**Christian Conservative Analysis:**
- **Pro-Life:** Choice as justice.
- **Religious Liberty:** Inclusive.
- **Education/Parental Rights:** Public investment.
- **Family Values:** LGBTQ+ inclusive.
- **Overall Assessment:** 2/10 - Rejects core conservatism.

**Key Positions:**
- **ABORTION:** Reproductive justice.
- **EDUCATION:** Fund publics.
- **RELIGIOUS FREEDOM:** For all.
- **GUNS:** End violence.
- **TAXES:** Tax rich.
- **IMMIGRATION:** Amnesty.

**Endorsements:** Progressive groups

**Why It Matters:** Affects national security, family policy from AR perspective.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** Re-electing Sanders preserves pro-life, school choice advances against national blue wave.

**Sarah Huckabee Sanders (Republican)** - Incumbent Governor

**Faith Statement:** "'As a Christian, my faith in God guides every decision I make as Governor, from protecting the unborn to defending religious liberty for all Arkansans.'"

**Background:**
- Daughter of Gov. Mike Huckabee; Ouachita Baptist grad.
- Trump Press Secretary; first female AR Gov.
- Married with three children.

**Christian Conservative Analysis:**
- **Pro-Life:** Banned abortions; monument to unborn.
- **Religious Liberty:** RFRA enforcer.
- **Education/Parental Rights:** LEARNS Act pioneer.
- **Family Values:** Gender care ban.
- **Overall Assessment:** 10/10 - Biblical leadership exemplar.

**Key Positions:**
- **ABORTION:** Total ban enforced.
- **EDUCATION:** Vouchers, bans on ideology.
- **RELIGIOUS FREEDOM:** State protections.
- **GUNS:** Permitless carry.
- **TAXES:** Grocery tax elimination.
- **IMMIGRATION:** E-Verify mandate.

**Endorsements:** SBA, ADF, NRA

**Website:** https://governor.arkansas.gov

**Fred Love (Democrat)** - State Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Little Rock real estate owner.
- House 2011-2023; Senate since 2023.
- Focus on economic development.

**Christian Conservative Analysis:**
- **Pro-Life:** Opposes bans.
- **Religious Liberty:** Balanced.
- **Education/Parental Rights:** Public priority.
- **Family Values:** Inclusive.
- **Overall Assessment:** 3/10 - Democratic standard.

**Key Positions:**
- **ABORTION:** Roe restoration.
- **EDUCATION:** Funding boost.
- **RELIGIOUS FREEDOM:** Anti-discrimination.
- **GUNS:** Checks.
- **TAXES:** Progressive.
- **IMMIGRATION:** Reform.

**Endorsements:** AR Education Assoc.

**Why It Matters:** Governor sets pro-family agenda tone.

---

### **Attorney General** - 2026-11-03

**Context:** AG defends state laws on life, guns, faith from federal challenges.

**Tim Griffin (Republican)** - Incumbent Attorney General

**Faith Statement:** "'My Christian faith, instilled by my father, a Baptist minister, compels me to defend the vulnerable, from the unborn to religious communities.'"

**Background:**
- Fifth-gen Arkansan; Harvard Law.
- U.S. Rep, Lt. Gov; Army Reserve Col.
- Married with three children.

**Christian Conservative Analysis:**
- **Pro-Life:** Sued to uphold ban.
- **Religious Liberty:** 100+ suits for faith.
- **Education/Parental Rights:** Defends bans.
- **Family Values:** Anti-gender ideology.
- **Overall Assessment:** 9/10 - Legal bulwark.

**Key Positions:**
- **ABORTION:** Absolutist defense.
- **EDUCATION:** Parental rights.
- **RELIGIOUS FREEDOM:** RFRA suits.
- **GUNS:** Carry defender.
- **TAXES:** Anti-regulatory.
- **IMMIGRATION:** Border suits.

**Endorsements:** Faith & Freedom, Sheriffs

**Website:** https://arkansasag.gov

**Why It Matters:** Shields AR conservatism legally.

---

## 🎯 KEY ISSUES FOR Arkansas CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Trigger ban (Act 156, 2021) prohibits abortions except life-saving; 20+ pregnancy centers statewide.
- Parental consent required for minors; no state funding for abortions.
- Recent victories: Blocked 2024 abortion amendment via signatures.

**Progressive Position:**
- Push for Roe restoration via initiatives; fund expansions despite bans.
- Challenges in courts over exceptions.

**Christian Conservative Action:**
- Join Arkansas Right to Life (arighttolife.org) for marches.
- Support HB 1239 pro-life bills.
- Volunteer at Little Rock Family Institute centers.
- Vote pro-life in primaries.

### **School Choice & Parental Rights**

**Conservative Position:**
- LEARNS Act: $730M vouchers, ESA up to $6,600; literacy tutors.
- Bans CRT, gender ideology (Act 647); homeschool freedom high.
- Wins: Blocked teachers' union overreach 2024.

**Progressive Position:**
- Union control, DEI mandates; sue over voucher 'diversion'.

**Christian Conservative Action:**
- Run for local school boards via AR Families First.
- Back SB 359 expansions.
- Join Parents Defending Education.
- Attend TFAW training.

### **Religious Freedom**

**Conservative Position:**
- 2022 Amendment bolsters RFRA; protects bakers, florists.
- Faith-based exemptions in adoption; Ten Commandments law (struck down, appealing).
- Strong church-state balance.

**Progressive Position:**
- Lawsuits claiming discrimination; push secular curricula.

**Christian Conservative Action:**
- Support First Liberty Institute cases.
- Lobby for HB 1615 protections.
- Join AR Baptist Convention advocacy.
- Pray for justices.

### **Guns**

**Conservative Position:**
- Permitless carry (2021); no mag limits, open carry.
- Stand Your Ground; preemption over local bans.
- Top reciprocity state.

**Progressive Position:**
- Red-flag laws, assault bans post-school shootings.

**Christian Conservative Action:**
- NRA-ILA volunteer.
- Defend Act 898.
- Join AR Gun Rights (argunrights.org).
- Train church security.

### **Taxes**

**Conservative Position:**
- Flat 4.9% income; no tax on retirement/Social Security.
- Grocery tax phased out; property tax relief for seniors.
- Pro-growth cuts.

**Progressive Position:**
- Raise on wealthy, corporate; fund social programs.

**Christian Conservative Action:**
- Support Club for Growth.
- Oppose hikes via petitions.
- Join AR Policy Foundation.
- Tithe wisely.

### **Immigration**

**Conservative Position:**
- E-Verify mandate; sanctuary ban.
- State-federal cooperation; oppose DACA expansion.
- Border security funding.

**Progressive Position:**
- Sanctuary pushes; amnesty.

**Christian Conservative Action:**
- FAIR advocacy.
- Support HB 1887.
- Border prayer vigils.
- Vet refugees biblically.

### **Family Values**

**Conservative Position:**
- Minors' gender care ban (2021); sports ban for trans.
- Marriage amendment; no same-sex adoption mandates.
- Pornography age verification.

**Progressive Position:**
- Gender-affirming access; LGBTQ+ curricula.

**Christian Conservative Action:**
- Family Council (familycouncil.org) events.
- Back Fairness in Women's Sports Act.
- Home educate.
- Counsel biblically.

### **Election Integrity**

**Conservative Position:**
- Strict photo ID; absentee limits.
- Audits, paper ballots; non-citizen purge.
- No ranked-choice.

**Progressive Position:**
- Mail-in expansion; oppose ID as suppression.

**Christian Conservative Action:**
- iVoterGuide.org ratings.
- Poll watch via Election Integrity AR.
- Register congregants.
- Pray against fraud.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- **2026-02-03** - Voter registration deadline for primary
- **2026-02-17** - Early voting begins for primary
- **2026-03-03** - Primary Election
- **2026-10-05** - Voter registration deadline for general
- **2026-10-20** - Early voting begins for general
- **2026-11-03** - General Election

**Voter Registration:** https://www.sos.arkansas.gov/elections/voter-registration

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
✅ **Share on social media** with #ArkansasFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Arkansas CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Arkansas coverage
- **Arkansas Right to Life** - Pro-life ratings
- **Family Council** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Arkansas Secretary of State**: https://www.sos.arkansas.gov/elections
- **County Election Offices**: Search via sos.arkansas.gov
- **Early Voting Locations**: County clerk offices

### **Conservative Organizations:**
- **Arkansas Right to Life**: https://arighttolife.org
- **Family Council**: https://familycouncil.org
- **Arkansas Gun Rights**: https://argunrights.org
- **Arkansas Families First**: School choice advocacy
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Arkansas CHRISTIANS

**2026 Elections Matter:**
- U.S. Senate determines national pro-life barriers.
- Governor race affects school choice funding.
- House seats impact family policy votes.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Tax cuts for working families
✅ Border security enhanced
✅ Rural faith communities empowered

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Tax hikes on families
❌ Open borders chaos
❌ Urban liberal dominance

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Tom Cotton, Sarah Huckabee Sanders, and their families
- Arkansas Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Arkansas
- Revival and awakening in Arkansas
- God's will in Arkansas elections

**Scripture for Arkansas Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Arkansas coverage, email contact@ekewaka.com

**Arkansas CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Arkansas races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Arkansas'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Arkansas races...")
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

print(f"\nChecking for existing Arkansas candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Arkansas'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Arkansas candidates...")
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

print("\nProcessing Arkansas summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Arkansas'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Arkansas data upload complete!")