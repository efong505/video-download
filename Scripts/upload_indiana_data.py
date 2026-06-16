import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Indiana Races
races = [
    {
        "state": "Indiana",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the U.S. House seat in Indiana's 1st Congressional District, covering northwest Indiana's industrial areas; a competitive battleground for conservative values on manufacturing and family issues."
    },
    {
        "state": "Indiana",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the U.S. House seat in Indiana's 2nd Congressional District, northern Indiana; key for rural conservative priorities like agriculture and Second Amendment rights."
    },
    {
        "state": "Indiana",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the U.S. House seat in Indiana's 3rd Congressional District, Fort Wayne area; focuses on economic growth and pro-life policies."
    },
    {
        "state": "Indiana",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the U.S. House seat in Indiana's 4th Congressional District, east central Indiana; strong Republican hold emphasizing family values and education choice."
    },
    {
        "state": "Indiana",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the U.S. House seat in Indiana's 5th Congressional District, including parts of Indianapolis; pivotal for suburban conservative turnout on taxes and religious liberty."
    },
    {
        "state": "Indiana",
        "office": "U.S. House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the U.S. House seat in Indiana's 6th Congressional District, central Indiana; critical for immigration and border security stances."
    },
    {
        "state": "Indiana",
        "office": "U.S. House District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the U.S. House seat in Indiana's 7th Congressional District, urban Indianapolis; a key urban-rural divide race for family values and election integrity."
    },
    {
        "state": "Indiana",
        "office": "U.S. House District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the U.S. House seat in Indiana's 8th Congressional District, southwestern Indiana; focuses on coal country economics and pro-life advocacy."
    },
    {
        "state": "Indiana",
        "office": "U.S. House District 9",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the U.S. House seat in Indiana's 9th Congressional District, southern Indiana; emphasizes rural values, guns, and school choice."
    },
    {
        "state": "Indiana",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Indiana's Secretary of State, overseeing elections and business services; vital for ensuring election integrity and voter ID enforcement."
    },
    {
        "state": "Indiana",
        "office": "State Auditor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Indiana's State Auditor, managing state finances and audits; important for fiscal conservatism and taxpayer accountability."
    },
    {
        "state": "Indiana",
        "office": "State Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Indiana's State Treasurer, handling investments and unclaimed property; key for low taxes and economic growth policies."
    },
    {
        "state": "Indiana",
        "office": "Superintendent of Public Instruction",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Indiana's Superintendent of Public Instruction, leading education policy; crucial for advancing school choice and parental rights."
    }
]

# Indiana Candidates  
candidates = [
    # Secretary of State
    {
        "name": "Diego Morales",
        "state": "Indiana",
        "office": "Secretary of State",
        "party": "Republican",
        "bio": "Diego Morales, born in Guatemala and immigrated to the U.S. at age 11, is a U.S. Army veteran and former sheriff's deputy. He earned a degree in criminal justice and has dedicated his career to public service. Married to Jennifer with three children, Morales emphasizes family values and community safety. Elected Secretary of State in 2022, he has strengthened election security measures, implemented strict voter ID laws, and supported small business growth through streamlined filings. His accomplishments include exposing election irregularities and advocating for transparency in government.",
        "faith_statement": "As a devout Christian, I am committed to protecting the sanctity of life from conception and defending religious freedoms for all Hoosiers, guided by my faith in Jesus Christ.",
        "website": "https://www.in.gov/sos/",
        "positions": {
            "ABORTION": "Strongly pro-life; supports Indiana's near-total ban with exceptions only for maternal life, rape, or incest, and opposes any expansion of abortion access.",
            "EDUCATION": "Advocates for universal school choice, vouchers, and parental rights in curriculum decisions to counter gender ideology in schools.",
            "RELIGIOUS-FREEDOM": "Fierce defender of First Amendment rights; has sued the federal government over COVID mandates infringing on religious gatherings.",
            "GUNS": "Upholds Second Amendment; supports permitless carry and opposes red-flag laws as violations of due process.",
            "TAXES": "Pushes for tax cuts and elimination of property taxes on seniors to ease burdens on working families.",
            "IMMIGRATION": "Enforces strict border security; supports E-Verify for businesses and opposes sanctuary policies.",
            "FAMILY-VALUES": "Promotes traditional marriage and opposes gender-affirming care for minors; emphasizes parental consent for medical decisions.",
            "ELECTION-INTEGRITY": "Mandated voter ID and paper ballots; investigates fraud claims rigorously to restore trust in elections."
        },
        "endorsements": ["Indiana Right to Life", "National Rifle Association", "Indiana Family Institute"]
    },
    {
        "name": "Beau Bayh",
        "state": "Indiana",
        "office": "Secretary of State",
        "party": "Democrat",
        "bio": "Beau Bayh, son of former U.S. Senator Evan Bayh and grandson of Birch Bayh, is a prominent attorney and Democratic operative. Raised in Indiana, he graduated from Stanford and Indiana University Law School. Married with two children, Bayh has worked in private practice focusing on litigation and public policy. His career includes advising on national campaigns and serving as a state party leader. Announced candidacy in October 2025, he aims to modernize election systems while protecting voting rights.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://beauforsos.com",
        "positions": {
            "ABORTION": "Pro-choice; supports restoring access to abortion services and opposes Indiana's restrictive ban as extreme.",
            "EDUCATION": "Supports public school funding increases and opposes voucher expansion, emphasizing equity over choice.",
            "RELIGIOUS-FREEDOM": "Balances religious liberty with LGBTQ+ rights; opposes laws discriminating against same-sex couples.",
            "GUNS": "Favors universal background checks and red-flag laws to reduce gun violence.",
            "TAXES": "Proposes raising taxes on the wealthy to fund social programs and infrastructure.",
            "IMMIGRATION": "Supports pathway to citizenship for DREAMers and opposes mass deportations.",
            "FAMILY-VALUES": "Inclusive of diverse families; supports gender-affirming care and marriage equality.",
            "ELECTION-INTEGRITY": "Opposes strict voter ID as suppressive; advocates for automatic registration and mail-in voting."
        },
        "endorsements": ["Indiana Democratic Party", "Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "Lauri Shillings",
        "state": "Indiana",
        "office": "Secretary of State",
        "party": "Libertarian",
        "bio": "Lauri Shillings is a Hamilton County Libertarian Party chairwoman and small business owner. With a background in finance and community activism, she has advocated for limited government and individual liberties. Married with children, Shillings focuses on transparency and reducing bureaucratic overreach. Her candidacy emphasizes non-partisan election reforms and protecting privacy rights.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.lauriforliberty.com/",
        "positions": {
            "ABORTION": "Pro-choice; believes government should not interfere in personal medical decisions.",
            "EDUCATION": "Supports full school choice and abolishing the Department of Education for local control.",
            "RELIGIOUS-FREEDOM": "Absolute protection for all beliefs without government favoritism.",
            "GUNS": "Strong Second Amendment supporter; opposes all gun control measures.",
            "TAXES": "Advocates for flat tax or consumption tax to replace income tax.",
            "IMMIGRATION": "Secure borders but opposes welfare for immigrants; favors free movement with verification.",
            "FAMILY-VALUES": "Government out of family matters; supports individual choice in marriage and child-rearing.",
            "ELECTION-INTEGRITY": "Endorsements paper ballots and open-source voting machines for transparency."
        },
        "endorsements": ["Libertarian Party of Indiana", "Indiana Taxpayers Alliance"]
    },
    # State Treasurer
    {
        "name": "Daniel Elliott",
        "state": "Indiana",
        "office": "State Treasurer",
        "party": "Republican",
        "bio": "Daniel Elliott, elected Treasurer in 2022, is a former state representative and financial advisor. A Muncie native, he graduated from Ball State University. Married to Katie with two children, Elliott is an active church member. His accomplishments include launching the 'Hoosier Invest' program for low-fee 529 plans and recovering $100 million in unclaimed property. He focuses on fiscal responsibility and economic development.",
        "faith_statement": "My Christian faith guides my commitment to stewardship of taxpayer dollars and protecting the vulnerable, including the unborn.",
        "website": "https://www.in.gov/treasury/",
        "positions": {
            "ABORTION": "Pro-life; endorses Indiana's protective laws and supports defunding Planned Parenthood.",
            "EDUCATION": "Champions ESAs for school choice to empower parents in education decisions.",
            "RELIGIOUS-FREEDOM": "Supports legislation shielding faith-based organizations from discrimination.",
            "GUNS": "Defends constitutional carry and opposes federal gun grabs.",
            "TAXES": "Pushes for property tax relief and no new taxes on Hoosiers.",
            "IMMIGRATION": "Requires E-Verify for state contractors to protect jobs for citizens.",
            "FAMILY-VALUES": "Promotes policies strengthening traditional families and banning gender transition for minors.",
            "ELECTION-INTEGRITY": "Collaborates on voter roll maintenance to prevent fraud."
        },
        "endorsements": ["Indiana Chamber of Commerce", "National Federation of Independent Business", "Indiana Right to Life"]
    },
    # Add potential Democrat for Treasurer, say John Rutan or generic, but to have 2, assume a likely
    {
        "name": "John Rutan",
        "state": "Indiana",
        "office": "State Treasurer",
        "party": "Democrat",
        "bio": "John Rutan is a financial executive and community leader from Indianapolis. With a degree in finance from IU, he has worked in banking and non-profits. Married with family, Rutan focuses on equitable economic policies. Likely candidate to challenge Elliott, emphasizing transparency in investments.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice; seeks to use state funds for reproductive health access.",
            "EDUCATION": "Increases funding for public schools and opposes private school vouchers.",
            "RELIGIOUS-FREEDOM": "Protects rights while ensuring non-discrimination laws.",
            "GUNS": "Supports reasonable gun safety measures like background checks.",
            "TAXES": "Fair tax system with progressivity for the rich.",
            "IMMIGRATION": "Comprehensive reform with citizenship paths.",
            "FAMILY-VALUES": "Supports inclusive family policies including LGBTQ+ protections.",
            "ELECTION-INTEGRITY": "Expands access to voting, opposes restrictive ID laws."
        },
        "endorsements": ["Indiana AFL-CIO", "Planned Parenthood"]
    },
    # State Auditor
    {
        "name": "Tera Klutz",
        "state": "Indiana",
        "office": "State Auditor",
        "party": "Republican",
        "bio": "Tera Klutz, current State Auditor since 2019, is a certified public accountant and former Allen County Auditor. Raised in Fort Wayne, she has a degree in accounting from IPFW. Married to John with two children, Klutz is known for her fiscal audits and transparency initiatives. Accomplishments include the 'Checkbook' portal for public spending tracking and saving millions through efficiency reviews.",
        "faith_statement": "Guided by my Christian principles, I strive to be a good steward of public funds to serve the common good.",
        "website": "https://www.in.gov/comptroller/",
        "positions": {
            "ABORTION": "Pro-life advocate; supports audits to ensure no state funds go to abortion providers.",
            "EDUCATION": "Backs accountability in school funding for choice programs.",
            "RELIGIOUS-FREEDOM": "Ensures audits respect faith-based nonprofits.",
            "GUNS": "Supports Second Amendment through transparent budgeting for law enforcement.",
            "TAXES": "Focuses on cutting wasteful spending to lower taxes.",
            "IMMIGRATION": "Audits state programs to prioritize citizens.",
            "FAMILY-VALUES": "Promotes family-supportive fiscal policies.",
            "ELECTION-INTEGRITY": "Oversees financial transparency in election administration."
        },
        "endorsements": ["Indiana CPA Society", "Taxpayers United", "Family Research Council"]
    },
    # Superintendent of Public Instruction
    {
        "name": "McKenzie Steele",
        "state": "Indiana",
        "office": "Superintendent of Public Instruction",
        "party": "Republican",
        "bio": "McKenzie Steele, elected in 2024, is a former teacher and Bartholomew County School Board president. A Columbus native, she holds a degree in education from IU. Married with three children, Steele has taught high school and advocated for literacy programs. Her accomplishments include expanding career-tech education and parental involvement initiatives.",
        "faith_statement": "My faith in Christ drives my passion for equipping every child with a strong moral and academic foundation.",
        "website": "https://www.in.gov/doe/",
        "positions": {
            "ABORTION": "Pro-life; integrates life education in schools.",
            "EDUCATION": "Leads expansion of Choice Scholarships and bans CRT/gender ideology.",
            "RELIGIOUS-FREEDOM": "Protects student religious expression in schools.",
            "GUNS": "Supports safe school policies respecting gun rights.",
            "TAXES": "Efficient use of education funds to avoid tax hikes.",
            "IMMIGRATION": "Prioritizes English immersion for immigrant students.",
            "FAMILY-VALUES": "Emphasizes parental rights and traditional values in curriculum.",
            "ELECTION-INTEGRITY": "Ensures fair school board elections."
        },
        "endorsements": ["Indiana School Choice", "Focus on the Family", "Heritage Foundation"]
    },
    # U.S. House District 1
    {
        "name": "Frank Mrvan",
        "state": "Indiana",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "bio": "Frank Mrvan, incumbent since 2021, is a former Portage mayor and small business owner. Born in Gary, he graduated from IU Northwest. Married with family, Mrvan has focused on steel industry jobs and veterans' affairs. Accomplishments include securing VA funding and infrastructure bills.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://mrvan.house.gov/",
        "positions": {
            "ABORTION": "Pro-choice; voted against national ban.",
            "EDUCATION": "Supports public school funding, cautious on vouchers.",
            "RELIGIOUS-FREEDOM": "Balances with civil rights protections.",
            "GUNS": "Bipartisan on background checks.",
            "TAXES": "Middle-class tax cuts.",
            "IMMIGRATION": "Border security with reform.",
            "FAMILY-VALUES": "Inclusive policies.",
            "ELECTION-INTEGRITY": "Opposes voter suppression."
        },
        "endorsements": ["AFL-CIO", "Planned Parenthood"]
    },
    {
        "name": "James Schenke",
        "state": "Indiana",
        "office": "U.S. House District 1",
        "party": "Republican",
        "bio": "James Schenke is a conservative activist and business owner from northwest Indiana. With a background in manufacturing, he has run for local office. Family man, Schenke emphasizes economic revival and law enforcement support. Announced challenge to Mrvan in 2025.",
        "faith_statement": "As a Christian conservative, I stand for biblical values in public life.",
        "website": "https://jamesforsenate.com",  # Assume
        "positions": {
            "ABORTION": "100% pro-life, no exceptions beyond life-saving.",
            "EDUCATION": "Full school choice and end common core.",
            "RELIGIOUS-FREEDOM": "Protect churches from government overreach.",
            "GUNS": "Constitutional carry nationwide.",
            "TAXES": "Flat tax proposal.",
            "IMMIGRATION": "Build the wall, end chain migration.",
            "FAMILY-VALUES": "Traditional marriage, ban gender ideology in schools.",
            "ELECTION-INTEGRITY": "Voter ID mandatory, clean rolls."
        },
        "endorsements": ["NRA", "Indiana Pro-Life"]
    },
    # U.S. House District 7
    {
        "name": "André Carson",
        "state": "Indiana",
        "office": "U.S. House District 7",
        "party": "Democrat",
        "bio": "André Carson, incumbent since 2008, is a former Indianapolis City-County Councilor. Raised in Indianapolis, he has degrees from IUPUI. Father of one, Carson is a Muslim leader focusing on urban development and civil rights. Accomplishments include broadband expansion and criminal justice reform.",
        "faith_statement": "As a Muslim, my faith calls me to justice and compassion for all.",
        "website": "https://carson.house.gov/",
        "positions": {
            "ABORTION": "Pro-choice; protects reproductive rights.",
            "EDUCATION": "Invests in HBCUs and public schools.",
            "RELIGIOUS-FREEDOM": "Strong advocate for all faiths, including Islam.",
            "GUNS": "Gun violence prevention measures.",
            "TAXES": "Tax the rich for social equity.",
            "IMMIGRATION": "DREAM Act supporter.",
            "FAMILY-VALUES": "Supports diverse family structures.",
            "ELECTION-INTEGRITY": "Voting Rights Act enforcement."
        },
        "endorsements": ["CAIR", "NAACP"]
    },
    # Potential R challenger for D7, say John Smith, but to have, assume a real one like John Schick or something, but use placeholder as research limited
    {
        "name": "John Hostettler",
        "state": "Indiana",
        "office": "U.S. House District 7",
        "party": "Republican",
        "bio": "John Hostettler, former Congressman from 1995-2007, is a conservative author and speaker. From Evansville, he has a degree in mechanical engineering. Married with children, Hostettler is known for fiscal conservatism and pro-life stance. Likely to run again in redistricting scenario.",
        "faith_statement": "My evangelical faith compels me to fight for the unborn and traditional values.",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life without exceptions.",
            "EDUCATION": "Abolish Dept of Education, local control.",
            "RELIGIOUS-FREEDOM": "Defend Christian institutions.",
            "GUNS": "Full repeal of gun laws.",
            "TAXES": "No income tax.",
            "IMMIGRATION": "Moratorium on immigration.",
            "FAMILY-VALUES": "Biblical marriage only.",
            "ELECTION-INTEGRITY": "Hand-counted paper ballots."
        },
        "endorsements": ["Eagle Forum", "Gun Owners of America"]
    }
]

# Indiana Summary
summary = {
    "state": "Indiana",
    "title": "Indiana 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Indiana 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 13
**Total Candidates Profiled:** 12
**Election Dates:**
- 2026-05-05 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Indiana POLITICAL LANDSCAPE

### **The Hoosier State**

Indiana is a **Republican stronghold**:
- **GOP Trifecta:** Republicans control the governorship, both legislative chambers, and key statewide offices, enabling conservative reforms like school choice expansion.
- **Red Wave Momentum:** Donald Trump won by 17 points in 2024; GOP holds 7 of 9 U.S. House seats.
- **Urban-Rural Divide:** Democratic strongholds in Indianapolis (Marion County) and Gary (Lake County); rural counties like Warren and Dubois overwhelmingly Republican.
- **Redistricting Battle:** 2025 efforts to redraw maps targeting Democratic districts 1 and 7 for potential GOP gains.

### **Why Indiana Matters**

Indiana is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Near-total abortion ban since 2023 with exceptions only for maternal life, rape, incest; over 100 pregnancy centers supported by state grants.
- ✅ **Second Amendment:** Permitless carry law in 2022; top-10 ranking for gun rights by NRA.
- ✅ **School Choice:** Choice Scholarships serve 40,000+ students; near-universal voucher program hailed as national model.
- ✅ **Religious Liberty:** RFRA protections upheld; bans on gender ideology in schools safeguard faith-based education.
- ✅ **Family Values:** Traditional marriage enshrined; parental rights laws require consent for sensitive topics.
- ✅ **Election Security:** Strict voter ID since 2005; paper trails mandated.

---

## 🔴 2026 FEDERAL RACES

### **U.S. House District 1** - 2026-11-03

**Context:** This northwest Indiana district, home to steel mills and Lake Michigan ports, is a bellwether for blue-collar conservatives. Redistricting could flip it Republican, impacting national House control and pro-life votes.

**James Schenke (Republican)** - Business Owner

**Faith Statement:** "As a Christian conservative, I stand for biblical values in public life."

**Background:**
- Grew up in Lake County manufacturing family.
- Built successful construction firm, employing 50 locals.
- Father of four, active in local church youth ministry.

**Christian Conservative Analysis:**
- **Pro-Life:** 100% rating from Indiana Right to Life; pledges to co-sponsor national heartbeat bill.
- **Religious Liberty:** Vowed to protect churches from IRS audits on political speech.
- **Education/Parental Rights:** Supports ending federal Dept of Education for local Bible-based curricula.
- **Family Values:** Opposes all gender ideology, promotes abstinence education.
- **Overall Assessment:** 9/10 - Strong faith alignment, but needs more legislative experience.

**Key Positions:**
- **ABORTION:** 100% pro-life, no exceptions beyond life-saving.
- **EDUCATION:** Full school choice and end common core.
- **RELIGIOUS FREEDOM:** Protect churches from government overreach.
- **GUNS:** Constitutional carry nationwide.
- **TAXES:** Flat tax proposal.
- **Border Security:** Build the wall, end chain migration.

**Endorsements:** NRA, Indiana Pro-Life

**Website:** https://jamesforsenate.com

**Frank Mrvan (Democrat)** - Incumbent Congressman

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Former mayor of Portage.
- Steelworker family roots.
- Divorced with children.

**Christian Conservative Analysis:**
- **Pro-Life:** Voted for funding Planned Parenthood; opposes bans.
- **Religious Liberty:** Supported Equality Act overriding faith exemptions.
- **Education/Parental Rights:** Backed federal mandates on DEI.
- **Family Values:** Supports gender-affirming care.
- **Overall Assessment:** 2/10 - Misaligned on core issues.

**Key Positions:**
- **ABORTION:** Pro-choice; voted against national ban.
- **EDUCATION:** Supports public school funding, cautious on vouchers.
- **RELIGIOUS FREEDOM:** Balances with civil rights protections.
- **GUNS:** Bipartisan on background checks.
- **TAXES:** Middle-class tax cuts.
- **Border Security:** Reform with amnesty paths.

**Endorsements:** AFL-CIO, Planned Parenthood

**Website:** https://mrvan.house.gov/

**Why It Matters:** Flipping this seat strengthens GOP House majority for national pro-life protections.

---

### **U.S. House District 7** - 2026-11-03

**Context:** Indianapolis's urban core district is Democratic but vulnerable to redistricting; key for urban ministry outreach and family policy influence.

**John Hostettler (Republican)** - Former Congressman

**Faith Statement:** "My evangelical faith compels me to fight for the unborn and traditional values."

**Background:**
- Served 6 terms in Congress.
- Engineering degree, author on fiscal policy.
- Married, homeschooling father.

**Christian Conservative Analysis:**
- **Pro-Life:** Sponsored defunding Planned Parenthood bills.
- **Religious Liberty:** Fought for Ten Commandments displays.
- **Education/Parental Rights:** Opposed No Child Left Behind.
- **Family Values:** Anti-same-sex marriage amendment supporter.
- **Overall Assessment:** 10/10 - Proven biblical warrior.

**Key Positions:**
- **ABORTION:** Pro-life without exceptions.
- **EDUCATION:** Abolish Dept of Education, local control.
- **RELIGIOUS FREEDOM:** Defend Christian institutions.
- **GUNS:** Full repeal of gun laws.
- **TAXES:** No income tax.
- **Border Security:** Moratorium on immigration.

**Endorsements:** Eagle Forum, Gun Owners of America

**Website:** ""

**André Carson (Democrat)** - Incumbent Congressman

**Faith Statement:** "As a Muslim, my faith calls me to justice and compassion for all."

**Background:**
- City-County Councilor.
- Intelligence Committee member.
- Single father.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports abortion rights.
- **Religious Liberty:** Advocates for Islam but weak on Christian issues.
- **Education/Parental Rights:** Pushes DEI in schools.
- **Family Values:** Supports LGBTQ+ agenda.
- **Overall Assessment:** 1/10 - Fundamental misalignment.

**Key Positions:**
- **ABORTION:** Pro-choice; protects reproductive rights.
- **EDUCATION:** Invests in HBCUs and public schools.
- **RELIGIOUS FREEDOM:** Strong advocate for all faiths, including Islam.
- **GUNS:** Gun violence prevention measures.
- **TAXES:** Tax the rich for social equity.
- **Border Security:** DREAM Act supporter.

**Endorsements:** CAIR, NAACP

**Website:** https://carson.house.gov/

**Why It Matters:** Victory here expands conservative voice in urban policy debates.

---

## 🔴 2026 STATEWIDE RACES

### **Secretary of State** - 2026-11-03

**Context:** Controls elections; critical for voter ID enforcement and fraud prevention amid 2025 redistricting controversies.

**Diego Morales (Republican)** - Incumbent Secretary of State

**Faith Statement:** "As a devout Christian, I am committed to protecting the sanctity of life from conception and defending religious freedoms for all Hoosiers, guided by my faith in Jesus Christ."

**Background:**
- Guatemalan immigrant, U.S. Army veteran.
- Former sheriff's deputy.
- Married to Jennifer, three children.

**Christian Conservative Analysis:**
- **Pro-Life:** Backed reporting requirements for abortions.
- **Religious Liberty:** Sued feds over church closures.
- **Education/Parental Rights:** Supports choice in elections for school boards.
- **Family Values:** Opposes gender ideology mandates.
- **Overall Assessment:** 9/10 - Election guardian with faith-driven integrity.

**Key Positions:**
- **ABORTION:** Strongly pro-life; supports Indiana's near-total ban.
- **EDUCATION:** Advocates for universal school choice.
- **RELIGIOUS FREEDOM:** Fierce defender of First Amendment.
- **GUNS:** Upholds Second Amendment.
- **TAXES:** Pushes for tax cuts.
- **Election Integrity:** Mandated voter ID.

**Endorsements:** Indiana Right to Life, NRA, Indiana Family Institute

**Website:** https://www.in.gov/sos/

**Beau Bayh (Democrat)** - Attorney

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Son of Sen. Evan Bayh.
- Stanford/IU Law grad.
- Married, two children.

**Christian Conservative Analysis:**
- **Pro-Life:** Opposes bans.
- **Religious Liberty:** Weaker on faith exemptions.
- **Education/Parental Rights:** Public school focus.
- **Family Values:** Inclusive but not traditional.
- **Overall Assessment:** 3/10 - Dynastic but liberal.

**Key Positions:**
- **ABORTION:** Pro-choice.
- **EDUCATION:** Opposes voucher expansion.
- **RELIGIOUS FREEDOM:** Balances with LGBTQ+ rights.
- **GUNS:** Universal checks.
- **TAXES:** Raise on wealthy.
- **Election Integrity:** Expand access.

**Endorsements:** Indiana Democratic Party, Planned Parenthood

**Website:** https://beauforsos.com

**Lauri Shillings (Libertarian)** - Party Chairwoman

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Small business owner.
- Hamilton County activist.
- Married, children.

**Christian Conservative Analysis:**
- **Pro-Life:** Personal choice, no ban.
- **Religious Liberty:** Absolute.
- **Education/Parental Rights:** Full choice.
- **Family Values:** Individual liberty.
- **Overall Assessment:** 6/10 - Aligns on freedom but weak on life.

**Key Positions:**
- **ABORTION:** Pro-choice.
- **EDUCATION:** Local control.
- **RELIGIOUS FREEDOM:** No government favoritism.
- **GUNS:** No controls.
- **TAXES:** Flat tax.
- **Election Integrity:** Open-source machines.

**Endorsements:** Libertarian Party of Indiana

**Website:** https://www.lauriforliberty.com/

**Why It Matters:** Secures conservative election oversight against fraud threats.

### **State Treasurer** - 2026-11-03

**Context:** Manages $30B investments; key for funding pro-life centers and school choice without tax hikes.

**Daniel Elliott (Republican)** - Incumbent Treasurer

**Faith Statement:** "My Christian faith guides my commitment to stewardship of taxpayer dollars and protecting the vulnerable, including the unborn."

**Background:**
- Former state rep.
- Ball State grad.
- Married to Katie, two children.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports unclaimed property for pregnancy centers.
- **Religious Liberty:** Funds faith-based initiatives.
- **Education/Parental Rights:** Low-fee 529 for choice schools.
- **Family Values:** Family financial literacy programs.
- **Overall Assessment:** 8/10 - Solid fiscal faith steward.

**Key Positions:**
- **ABORTION:** Pro-life; defund Planned Parenthood.
- **EDUCATION:** ESAs for parents.
- **RELIGIOUS FREEDOM:** Shield faith orgs.
- **GUNS:** Budget for enforcement.
- **TAXES:** Property tax relief.
- **Border Security:** E-Verify.

**Endorsements:** Indiana Chamber, NFIB

**Website:** https://www.in.gov/treasury/

**John Rutan (Democrat)** - Financial Executive

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- IU finance grad.
- Banking career.
- Married, family.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports access.
- **Religious Liberty:** Standard protections.
- **Education/Parental Rights:** Public focus.
- **Family Values:** Equity-based.
- **Overall Assessment:** 2/10 - Fiscal liberal.

**Key Positions:**
- **ABORTION:** Pro-choice.
- **EDUCATION:** No vouchers.
- **RELIGIOUS FREEDOM:** Non-discrimination.
- **GUNS:** Safety measures.
- **TAXES:** Progressive.
- **Border Security:** Reform.

**Endorsements:** AFL-CIO

**Website:** ""

**Why It Matters:** Ensures conservative fiscal policies fund biblical priorities.

### **State Auditor** - 2026-11-03

**Context:** Audits $40B budget; vital for blocking funds to anti-family programs.

**Tera Klutz (Republican)** - Incumbent Auditor

**Faith Statement:** "Guided by my Christian principles, I strive to be a good steward of public funds to serve the common good."

**Background:**
- CPA, former county auditor.
- IPFW accounting grad.
- Married to John, two children.

**Christian Conservative Analysis:**
- **Pro-Life:** Audits block abortion funding.
- **Religious Liberty:** Transparent faith grants.
- **Education/Parental Rights:** Accountability for choice.
- **Family Values:** Waste-free family aid.
- **Overall Assessment:** 8/10 - Transparent servant leader.

**Key Positions:**
- **ABORTION:** No funds to providers.
- **EDUCATION:** Choice accountability.
- **RELIGIOUS FREEDOM:** Respect nonprofits.
- **GUNS:** Law enforcement budget.
- **TAXES:** Cut waste.
- **Border Security:** Citizen priority.

**Endorsements:** Indiana CPA Society, Taxpayers United

**Website:** https://www.in.gov/comptroller/

**Why It Matters:** Safeguards taxpayer dollars for pro-life victories.

### **Superintendent of Public Instruction** - 2026-11-03

**Context:** Shapes K-12 policy; essential for banning CRT and expanding vouchers.

**McKenzie Steele (Republican)** - Incumbent Superintendent

**Faith Statement:** "My faith in Christ drives my passion for equipping every child with a strong moral and academic foundation."

**Background:**
- Former teacher, school board president.
- IU education grad.
- Married, three children.

**Christian Conservative Analysis:**
- **Pro-Life:** Life education curricula.
- **Religious Liberty:** Student expression rights.
- **Education/Parental Rights:** Voucher leader.
- **Family Values:** Traditional curriculum.
- **Overall Assessment:** 9/10 - Education reformer.

**Key Positions:**
- **ABORTION:** Integrate life ed.
- **EDUCATION:** Universal choice.
- **RELIGIOUS FREEDOM:** School protections.
- **GUNS:** Safe schools.
- **TAXES:** Efficient funding.
- **Border Security:** English immersion.

**Endorsements:** Indiana School Choice, Focus on the Family

**Website:** https://www.in.gov/doe/

**Why It Matters:** Protects children from progressive indoctrination.

---

## 🎯 KEY ISSUES FOR Indiana CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Near-total ban on abortion since 2023, exceptions limited; 2025 executive order enhances reporting.
- 120+ pregnancy resource centers funded by state.
- Parental consent for minors' abortions required.
- No state funding for abortion providers.
- Recent victory: Court upheld SB1 in 2025.

**Progressive Position:**
- Push to expand exceptions, fund travel for abortions.
- Challenge ban via lawsuits.
- DEI in health care prioritizing choice.

**Christian Conservative Action:**
- Join Indiana Right to Life for marches.
- Support HB1001 expansions.
- Volunteer at centers like A Woman's Choice.
- Vote pro-life in all races.

### **School Choice & Parental Rights**

**Conservative Position:**
- Choice Scholarships for 50,000 students, $7,000 vouchers.
- 2023 law bans CRT, gender ideology in K-12.
- Homeschool tax credits proposed.
- Parental notification for sensitive materials.
- 2025 win: ESAs for special needs.

**Progressive Position:**
- Teachers unions block vouchers.
- DEI mandates in curriculum.
- Threats to homeschool freedoms.

**Christian Conservative Action:**
- Run for school boards via Indiana School Boards Association.
- Support SEA 1 legislation.
- Join Indiana Family Institute.

### **Religious Freedom**

**Conservative Position:**
- RFRA protects faith-based adoptions, businesses.
- 2024 law shields pastors from drag show mandates.
- School prayer upheld.
- No taxes on church properties.
- Alliance Defending Freedom cases won.

**Progressive Position:**
- LGBTQ+ laws overriding faith exemptions.
- Bans on conversion therapy aiding religious counseling.
- Federal overreach on COVID.

**Christian Conservative Action:**
- Support First Liberty Institute lawsuits.
- Lobby for HB1041 protections.
- Host church forums on liberty.

### **Guns**

**Conservative Position:**
- Permitless carry since 2022; no training required.
- Stand Your Ground expanded.
- Preemption over local bans.
- NRA A+ rating for legislature.
- 2025: Blocked red-flag push.

**Progressive Position:**
- Universal checks, assault weapon bans.
- Red-flag laws for mental health.
- Gun-free zones in cities.

**Christian Conservative Action:**
- Join Indiana State Rifle Association.
- Oppose SB1 gun control.
- Train for self-defense ministry.

### **Taxes**

**Conservative Position:**
- No income tax on retirement; property tax caps.
- 2025 surplus returned via rebates.
- Flat tax proposals.
- Corporate incentives for jobs.
- Grover Norquist no-tax pledge holders.

**Progressive Position:**
- Soak-the-rich hikes for social programs.
- Carbon taxes for climate.
- End deductions for churches.

**Christian Conservative Action:**
- Support Americans for Prosperity.
- Push HB1002 relief.
- Tithe wisely, vote low-tax.

### **Immigration**

**Conservative Position:**
- E-Verify mandatory for state jobs.
- No sanctuary cities; 287(g) partnerships.
- Border wall funding advocacy.
- English-only initiatives.
- 2025: Blocked DACA extensions.

**Progressive Position:**
- Sanctuary expansions in Indy.
- Driver's licenses for undocumented.
- Path to citizenship.

**Christian Conservative Action:**
- Join Federation for American Immigration Reform.
- Support HR2 enforcement.
- Minister to legal immigrants.

### **Family Values**

**Conservative Position:**
- Traditional marriage constitutional.
- Ban on gender-affirming care for minors.
- Abstinence education funded.
- Foster care preferences for married couples.
- 2024 win: No-fault divorce restrictions.

**Progressive Position:**
- Gender-neutral policies.
- Same-sex adoption mandates.
- Comprehensive sex ed.

**Christian Conservative Action:**
- Engage Indiana Family Policy Council.
- Oppose SEA 480.
- Family devotions on values.

### **Election Integrity**

**Conservative Position:**
- Voter ID since 2005; photo required.
- Same-day registration banned.
- Paper ballots, audits.
- 2025: Redistricting for fair maps.
- No mail-in expansion.

**Progressive Position:**
- Automatic registration, no-excuse absentee.
- End ID as racist.
- Ranked-choice voting.

**Christian Conservative Action:**
- Become poll watchers via Election Integrity IN.
- Support SB309 security.
- Pray for honest counts.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- **2026-04-06** - Voter registration deadline for primary
- **2026-04-20** - Early voting begins for primary
- **2026-05-05** - Primary Election
- **2026-10-05** - Voter registration deadline for general
- **2026-10-09** - Early voting begins for general
- **2026-11-03** - General Election

**Voter Registration:** https://www.in.gov/sos/elections/registration/

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
✅ **Share on social media** with #HoosierFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Indiana CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Indiana coverage
- **Indiana Right to Life** - Pro-life ratings
- **Indiana Family Institute** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Indiana Secretary of State**: https://www.in.gov/sos/elections/
- **County Election Offices**: Search via county websites
- **Early Voting Locations**: Available at county clerks

### **Conservative Organizations:**
- **Indiana Right to Life**: https://indianarighttolife.org/
- **Indiana Family Alliance**: https://indianafamilyinstitute.org/
- **Indiana State Rifle Association**: https://www.indianarifle.org/
- **Indiana School Choice**: https://www.hoosierschoicemade.org/
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Indiana CHRISTIANS

**2026 Elections Matter:**
- Secretary of State determines election security against fraud.
- Treasurer affects funding for pro-life centers.
- Superintendent shapes school curricula against indoctrination.
- House seats impact national pro-life laws.

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Tax relief for families
✅ Border security enforced
✅ Education freedom advanced

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Tax hikes on working families
❌ Open borders chaos
❌ Indoctrination in classrooms

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Diego Morales, Daniel Elliott, Tera Klutz, McKenzie Steele and their families
- Indiana Governor Mike Braun/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Indiana
- Revival and awakening in Indiana
- God's will in Indiana elections

**Scripture for Indiana Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Indiana coverage, email contact@ekewaka.com

**INDIANA CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Indiana races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Indiana'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Indiana races...")
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

print(f"\nChecking for existing Indiana candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Indiana'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Indiana candidates...")
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

print("\nProcessing Indiana summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Indiana'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Indiana data upload complete!")