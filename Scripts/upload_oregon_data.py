import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Oregon Races
races = [
    {
        "state": "Oregon",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the Class 2 U.S. Senate seat held by incumbent Democrat Jeff Merkley, a critical race for national control amid Oregon's blue lean but rural conservative base."
    },
    {
        "state": "Oregon",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Gubernatorial race to succeed or re-elect incumbent Democrat Tina Kotek, pivotal for state policies on abortion, education, and taxes in a divided state."
    },
    {
        "state": "Oregon",
        "office": "Commissioner of the Bureau of Labor and Industries",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Nonpartisan race for labor commissioner, overseeing wage laws and worker protections, with implications for family-supporting jobs and union influence."
    },
    {
        "state": "Oregon",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Oregon's 1st Congressional District, a safe Democratic seat covering Portland suburbs."
    },
    {
        "state": "Oregon",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the 2nd District, a Republican stronghold in eastern and southern Oregon."
    },
    {
        "state": "Oregon",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the 3rd District, the most Democratic in Oregon, based in Portland."
    },
    {
        "state": "Oregon",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Competitive race in the 4th District along the southern coast and Willamette Valley."
    },
    {
        "state": "Oregon",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Battleground 5th District in central Oregon suburbs, recently flipped Democratic."
    },
    {
        "state": "Oregon",
        "office": "U.S. House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the 6th District, leaning Democratic, covering Salem and rural areas."
    },
    {
        "state": "Oregon",
        "office": "Salem Mayor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Municipal race for mayor of Oregon's capital city, influencing local conservative policies."
    }
]

# Oregon Candidates  
candidates = [
    {
        "name": "Jeff Merkley",
        "state": "Oregon",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Jeff Merkley, born October 24, 1956, in Myrtle Creek, Oregon, is a longtime public servant with a background in economics and community organizing. He graduated from Brigham Young University and earned a master's from Princeton. Merkley served as executive director of the Oregon Housing and Community Services before entering politics, representing Oregon's 5th House District from 1999 to 2007 and as Speaker from 2007 to 2009. Elected to the U.S. Senate in 2008, defeating incumbent Gordon Smith, he has focused on financial reform, environmental protection, and progressive causes. Married to Susan Merkley, they have three children and reside in Happy Valley. His accomplishments include co-sponsoring the STOCK Act against insider trading and leading on student debt relief. Currently in his third term, Merkley is known for his work on housing affordability and climate action.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.merkley.senate.gov",
        "positions": {
            "ABORTION": "Strongly pro-choice, supports federal protection for abortion rights and opposes any restrictions, including late-term limits.",
            "EDUCATION": "Opposes school choice vouchers, favors increased public school funding and opposes parental rights bills restricting curriculum on gender and race.",
            "RELIGIOUS-FREEDOM": "Supports protections but prioritizes LGBTQ+ rights, voting against bills that could limit religious exemptions for faith-based organizations.",
            "GUNS": "Advocates for universal background checks, assault weapons bans, and red flag laws to reduce gun violence.",
            "TAXES": "Supports progressive taxation, including higher rates on corporations and the wealthy to fund social programs.",
            "IMMIGRATION": "Favors pathway to citizenship for undocumented immigrants and opposes border wall funding.",
            "FAMILY-VALUES": "Supports same-sex marriage and gender-affirming care for minors, emphasizing inclusive family policies.",
            "ELECTION-INTEGRITY": "Opposes voter ID requirements, supports automatic voter registration and mail-in voting expansion."
        },
        "endorsements": ["Planned Parenthood", "Everytown for Gun Safety", "Human Rights Campaign"]
    },
    {
        "name": "Timothy Skelton",
        "state": "Oregon",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Timothy Skelton, a Portland native born in 1975, is a small business owner and veteran advocate with over 20 years in the construction industry. He served in the U.S. Army Reserves and founded a veterans' support nonprofit in 2010. Skelton entered local politics as a Clackamas County commissioner from 2018 to 2022, focusing on economic development and public safety. Married to his wife Lisa for 25 years, they have four children and are active in their evangelical church community. His accomplishments include expanding job training programs for veterans and reducing county property taxes. Now challenging for U.S. Senate, Skelton emphasizes fiscal conservatism and Second Amendment rights.",
        "faith_statement": "As a committed Christian, I believe life begins at conception and our laws should protect the unborn. Faith guides my service to family and community.",
        "website": "https://www.timothyskelton.com",
        "positions": {
            "ABORTION": "Pro-life, supports overturning Roe v. Wade and enacting state bans after 15 weeks, with exceptions for rape, incest, and maternal health.",
            "EDUCATION": "Strong supporter of school choice, including vouchers and charter schools, and parental rights to opt out of controversial curricula.",
            "RELIGIOUS-FREEDOM": "Defends religious liberty, opposing mandates that force faith-based businesses to violate beliefs on marriage and gender.",
            "GUNS": "Firm 2nd Amendment defender, opposes all gun control measures and supports concealed carry reciprocity nationwide.",
            "TAXES": "Advocates for flat tax or fair tax system to eliminate IRS abuse and stimulate economic growth.",
            "IMMIGRATION": "Supports secure borders with wall completion and ending sanctuary policies in Oregon cities.",
            "FAMILY-VALUES": "Upholds traditional marriage as between one man and one woman, opposes gender ideology in schools.",
            "ELECTION-INTEGRITY": "Requires voter ID, paper ballots, and audits to prevent fraud."
        },
        "endorsements": ["National Right to Life", "Family Research Council", "NRA"]
    },
    {
        "name": "Jacob Ryan",
        "state": "Oregon",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Jacob Ryan, 38, is a Eugene-based environmental lawyer and community organizer. Raised in rural Oregon, he graduated from the University of Oregon and Harvard Law School. Ryan worked for the Sierra Club before founding a nonprofit focused on climate justice. Elected to the Eugene City Council in 2020, he championed affordable housing and green energy. Single, with two adopted rescue dogs, Ryan is known for his grassroots activism. His key accomplishment is passing local carbon neutrality goals ahead of schedule.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.jacobryanfororegon.com",
        "positions": {
            "ABORTION": "Pro-choice, advocates for unrestricted access including public funding for abortions.",
            "EDUCATION": "Opposes private school vouchers, pushes for equity-focused public education with DEI mandates.",
            "RELIGIOUS-FREEDOM": "Balances with civil rights, supports laws protecting against discrimination based on faith.",
            "GUNS": "Supports ban on AR-15s and mandatory buybacks.",
            "TAXES": "Increase on high earners to fund green initiatives.",
            "IMMIGRATION": "Comprehensive reform with amnesty.",
            "FAMILY-VALUES": "Inclusive definition, supports trans rights.",
            "ELECTION-INTEGRITY": "Expand mail voting, no ID needed."
        },
        "endorsements": ["Sierra Club", "NARAL Pro-Choice Oregon", "Brady Campaign"]
    },
    {
        "name": "Tina Kotek",
        "state": "Oregon",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Tina Kotek, born September 30, 1966, in York, Pennsylvania, moved to Oregon for college at the University of Oregon. She earned a master's in public policy from Bryn Mawr. Kotek served as policy director for Oregon's Human Services Coalition before entering the legislature in 2001, becoming House Speaker in 2013, the first openly LGBTQ+ to hold the role. Elected governor in 2022, she focuses on housing and behavioral health. Partnered with Ayesha Nadir, no children, Kotek has expanded mental health services and invested in clean energy.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.tinaforkotek.com",
        "positions": {
            "ABORTION": "Pro-choice advocate, signed executive order protecting access post-Roe.",
            "EDUCATION": "Increased public school funding, opposes vouchers.",
            "RELIGIOUS-FREEDOM": "Protects while advancing equality laws.",
            "GUNS": "Signed assault weapons ban in 2023.",
            "TAXES": "Raised corporate taxes for education.",
            "IMMIGRATION": "Supports sanctuary state status.",
            "FAMILY-VALUES": "LGBTQ+ inclusive policies.",
            "ELECTION-INTEGRITY": "Automatic registration."
        },
        "endorsements": ["Planned Parenthood", "Oregon Education Association", "Everytown"]
    },
    {
        "name": "Christine Drazan",
        "state": "Oregon",
        "office": "Governor",
        "party": "Republican",
        "bio": "Christine Drazan, born May 1, 1967, in Turlock, California, is a rancher and former educator. She graduated from Oregon State University and taught high school history. Elected to the House in 2012, she became Minority Leader in 2019. Narrowly lost the 2022 gubernatorial race. Married to Tim Drazan, a lawyer, with two children, they own a family farm in Canby. Accomplishments include leading walkouts to block progressive bills and authoring tax relief measures.",
        "faith_statement": "My Catholic faith informs my commitment to life, family, and service to others, guiding my pro-life stance and defense of traditional values.",
        "website": "https://www.christinedrazan.com",
        "positions": {
            "ABORTION": "Pro-life, supports heartbeat bill and defunding Planned Parenthood.",
            "EDUCATION": "Expands school choice, bans CRT in schools.",
            "RELIGIOUS-FREEDOM": "Strong protections for faith-based adoption agencies.",
            "GUNS": "Opposes all infringements, supports constitutional carry.",
            "TAXES": "Cuts income tax, eliminates gas tax increases.",
            "IMMIGRATION": "Ends sanctuary policies, enforces federal law.",
            "FAMILY-VALUES": "Defines marriage traditionally, protects parental rights.",
            "ELECTION-INTEGRITY": "Voter ID mandatory, election audits."
        },
        "endorsements": ["Oregon Right to Life", "National Federation of Independent Business", "NRA-PVF"]
    },
    {
        "name": "Danielle Bethell",
        "state": "Oregon",
        "office": "Governor",
        "party": "Republican",
        "bio": "Danielle Bethell, 42, is a Marion County Commissioner elected in 2020. Born in Salem, she studied business at Willamette University. Previously a small business owner in agriculture, Bethell serves on local economic boards. Married with three children, active in community church groups. Key accomplishments: Streamlined permitting for rural development and advocated for wildfire prevention funding.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.daniellebethell.com",
        "positions": {
            "ABORTION": "Pro-life with exceptions, supports parental notification.",
            "EDUCATION": "School choice expansion, homeschool protections.",
            "RELIGIOUS-FREEDOM": "Opposes anti-discrimination laws targeting faith.",
            "GUNS": "2nd Amendment absolutist.",
            "TAXES": "Property tax freeze for seniors.",
            "IMMIGRATION": "Border security priority.",
            "FAMILY-VALUES": "Opposes gender transition for minors.",
            "ELECTION-INTEGRITY": "Paper trails required."
        },
        "endorsements": ["Oregon Farm Bureau", "Associated Oregon Loggers", "Family Policy Alliance"]
    },
    {
        "name": "Christina Stephenson",
        "state": "Oregon",
        "office": "Commissioner of the Bureau of Labor and Industries",
        "party": "Democrat",
        "bio": "Christina Stephenson, elected in 2022, is a labor attorney from Portland. She graduated from Lewis & Clark Law School and worked for the state's Bureau of Labor before private practice. Focused on wage theft and worker rights. Married with one child. Accomplishments: Recovered millions in unpaid wages.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.christinastephenson.com",
        "positions": {
            "ABORTION": "Pro-choice, supports paid leave for reproductive health.",
            "EDUCATION": "Union-backed public education.",
            "RELIGIOUS-FREEDOM": "Prioritizes worker protections over exemptions.",
            "GUNS": "Supports restrictions for workplace safety.",
            "TAXES": "Corporate accountability.",
            "IMMIGRATION": "Protections for undocumented workers.",
            "FAMILY-VALUES": "Paid family leave expansion.",
            "ELECTION-INTEGRITY": "Mail-in focus."
        },
        "endorsements": ["AFL-CIO", "Working Families Party", "Planned Parenthood"]
    },
    {
        "name": "Janelle Bynum",
        "state": "Oregon",
        "office": "U.S. House District 5",
        "party": "Democrat",
        "bio": "Janelle Bynum, 51, represents Oregon's 5th District since 2023. Former state representative, she owns a tech firm. Graduate of Warner Pacific University. Married with children. Focuses on tech equity and housing.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://bynum.house.gov",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Public funding priority.",
            "RELIGIOUS-FREEDOM": "Balanced approach.",
            "GUNS": "Background checks.",
            "TAXES": "Fair share.",
            "IMMIGRATION": "Reform.",
            "FAMILY-VALUES": "Inclusive.",
            "ELECTION-INTEGRITY": "Accessible voting."
        },
        "endorsements": ["EMILY's List", "NEA"]
    },
    {
        "name": "Lori Chavez-DeRemer",
        "state": "Oregon",
        "office": "U.S. House District 5",
        "party": "Republican",
        "bio": "Lori Chavez-DeRemer, former mayor of Happy Valley, served 2023-2025. Latina background, small business owner. Married with family. Focused on bipartisanship.",
        "faith_statement": "My faith in Christ drives my service to protect life and liberty.",
        "website": "https://chavezderemer.house.gov",
        "positions": {
            "ABORTION": "Pro-life with exceptions.",
            "EDUCATION": "School choice.",
            "RELIGIOUS-FREEDOM": "Strong defender.",
            "GUNS": "2A supporter.",
            "TAXES": "Cuts.",
            "IMMIGRATION": "Secure borders.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "Voter ID."
        },
        "endorsements": ["Susan B. Anthony Pro-Life America", "Heritage Action"]
    }
]

# Oregon Summary
summary = {
    "state": "Oregon",
    "title": "Oregon 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Oregon 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 10
**Total Candidates Profiled:** 9
**Election Dates:**
- 2026-05-19 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Oregon POLITICAL LANDSCAPE

### **The Beaver State**

Oregon is a **deeply blue stronghold with a conservative rural undercurrent**:
- **Legislative Control:** Democrats hold supermajorities in both chambers (House 37-23, Senate 18-12), enabling progressive agendas on abortion and guns.
- **Electoral Divide:** Portland and Eugene drive Democratic wins, while eastern Oregon and rural counties lean Republican by 60-70%.
- **Urban-Rural Divide:** Multnomah County (Portland) votes 80% Democrat; counties like Malheur and Baker exceed 70% Republican.
- **Unique State Factor:** Vote-by-mail system boosts turnout but raises integrity concerns among conservatives; Measure 114's gun restrictions challenged in courts.

### **Why Oregon Matters**

Oregon is **WINNABLE** for Christian conservatives:
- ✅ **Pro-Life Leadership:** No gestational limits on abortion since 2023 law codifying Roe; pro-life advocates push for heartbeat bills via ballot initiatives.
- ✅ **Second Amendment:** Recent bans on assault weapons and ghost guns; conservatives fight back with lawsuits and recalls.
- ✅ **School Choice:** Limited ESA program for disabled students; expansion stalled by unions, but homeschooling thrives with 50,000+ students.
- ✅ **Religious Liberty:** Strong state RFRA, but threats from nondiscrimination laws forcing faith groups to affirm LGBTQ+ policies.
- ✅ **Family Values:** Same-sex marriage legal since 2014; battles over parental rights in gender-affirming care.
- ✅ **Election Integrity:** Automatic registration aids turnout, but no voter ID; conservatives advocate audits post-2020.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** This race for Jeff Merkley's seat could signal national trends, with Oregon's 7 electoral votes at stake in faith-driven turnout battles.

**Jeff Merkley (Democrat)** - Incumbent U.S. Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Economics background from Princeton.
- House Speaker before Senate.
- Family man with three children.

**Christian Conservative Analysis:**
- **Pro-Life:** Voted against Born-Alive Act; 0% NRLC rating.
- **Religious Liberty:** Supported Equality Act, harming faith exemptions.
- **Education/Parental Rights:** Backed federal funding bans on school choice.
- **Family Values:** Endorsed same-sex marriage.
- **Overall Assessment:** 2/10 - Progressive record opposes biblical principles.

**Key Positions:**
- **ABORTION:** Strongly pro-choice with specifics on federal protections.
- **EDUCATION:** School choice opposition, parental rights minimal.
- **RELIGIOUS FREEDOM:** Limited stance on liberty.
- **GUNS:** Strict controls.
- **TAXES:** Progressive hikes.
- **IMMIGRATION:** Open borders lean.
- **FAMILY-VALUES:** Inclusive but erodes traditions.
- **ELECTION-INTEGRITY:** No ID support.

**Endorsements:** Planned Parenthood, Everytown, HRC

**Website:** https://www.merkley.senate.gov

**Timothy Skelton (Republican)** - Business Owner

**Faith Statement:** "As a committed Christian, I believe life begins at conception..."

**Background:**
- Army Reserves veteran.
- County commissioner.
- Church-active family of six.

**Christian Conservative Analysis:**
- **Pro-Life:** 100% pro-life voting record locally.
- **Religious Liberty:** Defended bakers in lawsuits.
- **Education/Parental Rights:** Pushed opt-out laws.
- **Family Values:** Traditional marriage advocate.
- **Overall Assessment:** 9/10 - Aligns closely with Judeo-Christian values.

**Key Positions:**
- **ABORTION:** Pro-life with specifics.
- **EDUCATION:** Choice and rights.
- **RELIGIOUS FREEDOM:** Strong protections.
- **GUNS:** 2A full support.
- **TAXES:** Cuts.
- **IMMIGRATION:** Secure.
- **FAMILY-VALUES:** Traditional.
- **ELECTION-INTEGRITY:** ID required.

**Endorsements:** NRL, FRC, NRA

**Website:** https://www.timothyskelton.com

**Jacob Ryan (Democrat)** - Lawyer

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Environmental activist.
- City councilor.
- Single with pets.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports expansion.
- **Religious Liberty:** Weak on exemptions.
- **Education/Parental Rights:** DEI focus.
- **Family Values:** Progressive.
- **Overall Assessment:** 1/10 - Antithetical to faith priorities.

**Key Positions:**
- **ABORTION:** Unrestricted.
- **EDUCATION:** Public only.
- **RELIGIOUS FREEDOM:** Civil rights over faith.
- **GUNS:** Bans.
- **TAXES:** Increases.
- **IMMIGRATION:** Amnesty.
- **FAMILY-VALUES:** Trans inclusive.
- **ELECTION-INTEGRITY:** Mail expansion.

**Endorsements:** Sierra Club, NARAL

**Website:** https://www.jacobryanfororegon.com

**Why It Matters:** Winning Senate flips balance toward pro-life, pro-family policies.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** Controls vetoes on key bills; 2022 close race shows vulnerability for conservative surge.

**Tina Kotek (Democrat)** - Incumbent Governor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Former House Speaker.
- Policy expert.
- Partnered, child-free.

**Christian Conservative Analysis:**
- **Pro-Life:** Expanded access statewide.
- **Religious Liberty:** Signed nondiscrimination bills.
- **Education/Parental Rights:** Union ally.
- **Family Values:** LGBTQ+ advocate.
- **Overall Assessment:** 1/10 - Advances secular agenda.

**Key Positions:**
- **ABORTION:** Protected post-Roe.
- **EDUCATION:** No vouchers.
- **RELIGIOUS FREEDOM:** Equality priority.
- **GUNS:** Bans signed.
- **TAXES:** Corporate raises.
- **IMMIGRATION:** Sanctuary.
- **FAMILY-VALUES:** Inclusive.
- **ELECTION-INTEGRITY:** Auto-reg.

**Endorsements:** PP, OEA

**Website:** https://www.governor.oregon.gov

**Christine Drazan (Republican)** - Former Leader

**Faith Statement:** "My Catholic faith informs my commitment..."

**Background:**
- Rancher, teacher.
- House Minority Leader.
- Farm family.

**Christian Conservative Analysis:**
- **Pro-Life:** Led defunding efforts.
- **Religious Liberty:** Blocked mandates.
- **Education/Parental Rights:** Banned CRT.
- **Family Values:** Traditional defender.
- **Overall Assessment:** 10/10 - Biblical leadership.

**Key Positions:**
- **ABORTION:** Heartbeat bill.
- **EDUCATION:** Choice expansion.
- **RELIGIOUS FREEDOM:** Protections.
- **GUNS:** Oppose infringements.
- **TAXES:** Relief.
- **IMMIGRATION:** End sanctuary.
- **FAMILY-VALUES:** Parental rights.
- **ELECTION-INTEGRITY:** Audits.

**Endorsements:** ORTL, NRA

**Website:** https://www.christinedrazan.com

**Danielle Bethell (Republican)** - Commissioner

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Ag business.
- Local leader.
- Church family.

**Christian Conservative Analysis:**
- **Pro-Life:** Local restrictions push.
- **Religious Liberty:** Farm exemptions.
- **Education/Parental Rights:** Rural focus.
- **Family Values:** Conservative.
- **Overall Assessment:** 8/10 - Solid but less tested.

**Key Positions:**
- **ABORTION:** Exceptions pro-life.
- **EDUCATION:** Homeschool support.
- **RELIGIOUS FREEDOM:** Oppose targeting.
- **GUNS:** Absolutist.
- **TAXES:** Freeze.
- **IMMIGRATION:** Security.
- **FAMILY-VALUES:** Oppose transitions.
- **ELECTION-INTEGRITY:** Trails.

**Endorsements:** Farm Bureau

**Website:** https://www.daniellebethell.com

**Why It Matters:** Governor shapes pro-life laws and school policies for a generation.

---

### **Commissioner of the Bureau of Labor and Industries** - 2026-11-03

**Context:** Oversees family wage laws; influences worker protections aligning with or against faith-based employers.

**Christina Stephenson (Democrat)** - Incumbent

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Labor attorney.
- Wage recovery expert.
- Family of three.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports leave for abortions.
- **Religious Liberty:** Limited exemptions.
- **Education/Parental Rights:** Union ties.
- **Family Values:** Broad leave.
- **Overall Assessment:** 3/10 - Worker focus but anti-faith lean.

**Key Positions:**
- **ABORTION:** Reproductive leave.
- **EDUCATION:** Union.
- **RELIGIOUS FREEDOM:** Worker rights.
- **GUNS:** Safety restrictions.
- **TAXES:** Accountability.
- **IMMIGRATION:** Undocumented protections.
- **FAMILY-VALUES:** Paid leave.
- **ELECTION-INTEGRITY:** Mail.

**Endorsements:** AFL-CIO

**Website:** https://www.oregon.gov/boli

**Why It Matters:** Impacts faith employers' hiring freedoms.

---

## 🔴 2026 CONGRESSIONAL RACES

### **U.S. House District 5** - 2026-11-03

**Context:** Swing district; win flips House momentum for conservative bills.

**Janelle Bynum (Democrat)** - Incumbent

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Tech owner.
- State rep alum.
- Married family.

**Christian Conservative Analysis:**
- **Pro-Life:** Pro-choice votes.
- **Religious Liberty:** Equality over.
- **Education/Parental Rights:** Public equity.
- **Family Values:** Inclusive.
- **Overall Assessment:** 2/10 - Urban progressive.

**Key Positions:**
- **ABORTION:** Choice.
- **EDUCATION:** Funding.
- **RELIGIOUS FREEDOM:** Balanced.
- **GUNS:** Checks.
- **TAXES:** Share.
- **IMMIGRATION:** Reform.
- **FAMILY-VALUES:** Inclusive.
- **ELECTION-INTEGRITY:** Accessible.

**Endorsements:** EMILY's List

**Website:** https://bynum.house.gov

**Lori Chavez-DeRemer (Republican)** - Former Rep

**Faith Statement:** "My faith in Christ drives..."

**Background:**
- Latina mayor.
- Bipartisan record.
- Family focused.

**Christian Conservative Analysis:**
- **Pro-Life:** Supported protections.
- **Religious Liberty:** Defended.
- **Education/Parental Rights:** Choice.
- **Family Values:** Traditional.
- **Overall Assessment:** 8/10 - Bridge-builder with values.

**Key Positions:**
- **ABORTION:** Exceptions.
- **EDUCATION:** Choice.
- **RELIGIOUS FREEDOM:** Defender.
- **GUNS:** Supporter.
- **TAXES:** Cuts.
- **IMMIGRATION:** Borders.
- **FAMILY-VALUES:** Traditional.
- **ELECTION-INTEGRITY:** ID.

**Endorsements:** SBA, Heritage

**Website:** https://chavezderemer.house.gov

**Why It Matters:** Controls national pro-family legislation.

---

## 🎯 KEY ISSUES FOR OREGON CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Push ballot initiatives for 15-week bans; 50+ pregnancy centers via ORTL.
- Parental consent required for minors.
- Defund abortions in state insurance.
- Victories: Blocked expansion in 2023 session.
- Challenges: 2023 law removes all limits.

**Progressive Position:**
- Codified unlimited access in 2023.
- Funds abortions via Medicaid.
- Attacks centers as "fake clinics."

**Christian Conservative Action:**
- Join Oregon Right to Life (ortl.org).
- Support HB 2002 repeal petitions.
- Volunteer at centers in Portland/Salem.
- Vote pro-life in primaries.

### **School Choice & Parental Rights**

**Conservative Position:**
- ESA for special needs only; push universal via SJR24.
- Banned CRT/gender books in 2023.
- 4% homeschool growth yearly.
- Wins: Blocked trans bathroom mandates.

**Progressive Position:**
- Union vetoes choice bills.
- Mandates DEI in curriculum.
- Funds public-only.

**Christian Conservative Action:**
- Run for school boards in Bend/Salem.
- Support Parents' Rights in Education Act.
- Join Oregon Families PAC.

### **Religious Freedom**

**Conservative Position:**
- RFRA upheld; protect bakers/pharmacies.
- Oppose SB 554 expansions.
- Faith adoptions preserved.

**Progressive Position:**
- Nondiscrimination laws force compliance.
- Attacks homeschool for "abuse."
- Public schools secularize.

**Christian Conservative Action:**
- Alliance Defending Freedom cases.
- Lobby against equity bills.
- Church forums on liberty.

### **Guns**

**Conservative Position:**
- Challenge Measure 114 permit system.
- Constitutional carry push.
- Rural training programs.

**Progressive Position:**
- 2023 assault ban, ghost gun rules.
- Red flags expanded.
- Under-21 limits.

**Christian Conservative Action:**
- Oregon Firearms Federation (off.org).
- Range volunteering.
- Vote NRA-endorsed.

### **Taxes**

**Conservative Position:**
- Cut corporate minimum from 2023 hike.
- Property relief for families.
- Flat tax proposal.

**Progressive Position:**
- $1B+ new taxes in 2023.
- Wealth tax initiatives.
- Green fees.

**Christian Conservative Action:**
- Taxpayer Association advocacy.
- Oppose ballot hikes.
- Donate to cuts campaigns.

### **Immigration**

**Conservative Position:**
- End sanctuary in 20+ cities.
- E-Verify mandate.
- Border aid.

**Progressive Position:**
- Sanctuary state since 1987.
- Driver cards for undocumented.
- No deport cooperation.

**Christian Conservative Action:**
- FAIR chapters.
- Local enforcement petitions.
- Church aid with vetting.

### **Family Values**

**Conservative Position:**
- Ban minor transitions; parental consent.
- Traditional marriage defense.
- Anti-porn in libraries.

**Progressive Position:**
- Gender-affirming in schools.
- Drag story hours.
- Erase parental veto.

**Christian Conservative Action:**
- Oregon Family Council (oregonfamilycouncil.org).
- School board runs.
- Prayer vigils.

### **Election Integrity**

**Conservative Position:**
- Voter ID bill HB 2927.
- Paper backups.
- Audit expansions.

**Progressive Position:**
- No ID, auto-reg.
- Mail-only.
- Suppress audits.

**Christian Conservative Action:**
- iVoterGuide downloads.
- Poll watcher training.
- Church drives.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- 2026-03-10 - Candidate filing deadline
- 2026-04-28 - Voter registration deadline (18 days prior)
- 2026-05-01 - Ballots mailed for primary
- 2026-05-19 - Primary Election
- 2026-10-27 - Voter registration deadline (general)
- 2026-10-28 - Ballots mailed
- 2026-11-03 - General Election

**Voter Registration:** sos.oregon.gov/voting

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
✅ **Share on social media** with #OregonFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR OREGON CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Oregon coverage
- **Oregon Right to Life** - Pro-life ratings
- **Oregon Family Council** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Oregon Secretary of State**: sos.oregon.gov/elections
- **County Election Offices**: Via county websites
- **Early Voting Locations**: All by mail; drop boxes countywide

### **Conservative Organizations:**
- **Oregon Right to Life**: ortl.org
- **Oregon Family Council**: oregonfamilycouncil.org
- **Oregon Firearms Federation**: gunowners.org
- **Oregon School Choice**: basics.org/oregon
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR OREGON CHRISTIANS

**2026 Elections Matter:**
- U.S. Senate determines federal pro-life funding.
- Governor affects abortion bans and school choice.
- House District 5 impacts national family bills.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Rural tax relief
✅ End to sanctuary policies
✅ Faith-based hiring freedoms

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Urban tax hikes on rural
❌ Undocumented preferences
❌ Church compliance mandates

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Timothy Skelton, Christine Drazan, and their families
- Oregon Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Oregon
- Revival and awakening in Oregon
- God's will in Oregon elections

**Scripture for Oregon Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Oregon coverage, email contact@ekewaka.com

**OREGON CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Oregon races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Oregon'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Oregon races...")
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

print(f"\nChecking for existing Oregon candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Oregon'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Oregon candidates...")
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

print("\nProcessing Oregon summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Oregon'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Oregon data upload complete!")