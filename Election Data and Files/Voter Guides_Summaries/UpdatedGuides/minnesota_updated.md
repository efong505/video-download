import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Arizona Races
races = [
    {
        "state": "Arizona",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The race for Governor will determine the state's chief executive, impacting policy on education, economy, border security, and social issues critical to Christian conservatives."
    },
    {
        "state": "Arizona",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Newly created office serving as successor to the Governor, influencing state leadership and policy continuity."
    },
    {
        "state": "Arizona",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The Attorney General enforces laws, including those protecting life, religious liberty, and election integrity."
    },
    {
        "state": "Arizona",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Oversees elections, crucial for ensuring secure and fair voting processes."
    },
    {
        "state": "Arizona",
        "office": "State Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Manages state finances, including funding for pro-family programs and tax relief initiatives."
    },
    {
        "state": "Arizona",
        "office": "Superintendent of Public Instruction",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Leads the Department of Education, shaping school choice, parental rights, and curriculum free from ideological indoctrination."
    },
    {
        "state": "Arizona",
        "office": "State Mine Inspector",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Ensures safety in mining operations, supporting Arizona's economy and worker protections."
    },
    {
        "state": "Arizona",
        "office": "Corporation Commission (2 seats)",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Regulates utilities and corporations, impacting energy costs and economic freedom."
    },
    {
        "state": "Arizona",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Competitive district influencing national policy on life, liberty, and family values."
    },
    {
        "state": "Arizona",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Represents northern Arizona, key for conservative voices in Congress."
    },
    {
        "state": "Arizona",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Democratic stronghold, opportunity to flip for pro-life and pro-family policies."
    },
    {
        "state": "Arizona",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Rural district vital for agriculture and Second Amendment rights."
    },
    {
        "state": "Arizona",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Conservative area focusing on border security and economic growth."
    },
    {
        "state": "Arizona",
        "office": "U.S. House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Swing district critical for maintaining Republican majority."
    },
    {
        "state": "Arizona",
        "office": "U.S. House District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Urban district with Latino voters, key for immigration and family policies."
    },
    {
        "state": "Arizona",
        "office": "U.S. House District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Strong Republican hold, defending against progressive challenges."
    },
    {
        "state": "Arizona",
        "office": "U.S. House District 9",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Phoenix suburbs, battleground for conservative values."
    }
]

# Arizona Candidates  
candidates = [
    {
        "name": "Katie Hobbs",
        "state": "Arizona",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Katie Hobbs, born in Phoenix, Arizona, in 1969, is a social worker turned politician. She earned a bachelor's from Northern Arizona University and a master's in social work from Arizona State University. Hobbs began her career advocating for abused children and later served as a state representative (2013-2019), Senate minority leader, and Secretary of State (2019-2023). Elected Governor in 2022, she is married to Patrick Goodman, a therapist, and they have two children. Hobbs has focused on education funding, water conservation, and reproductive rights, vetoing numerous Republican bills on abortion and guns.",
        "faith_statement": "No publicly disclosed faith statement. Hobbs has spoken about her Catholic upbringing but supports pro-choice policies.",
        "website": "https://azgovernor.gov/",
        "positions": {
            "ABORTION": "Pro-choice; signed repeal of 1864 ban, supports access up to viability with exceptions for health.",
            "EDUCATION": "Opposes universal vouchers; invests in public schools, supports teacher pay raises but criticizes ESA expansion.",
            "RELIGIOUS-FREEDOM": "Supports separation of church and state; vetoed Ten Commandments in schools bill.",
            "GUNS": "Supports universal background checks and red flag laws; vetoed permitless carry expansions.",
            "TAXES": "Opposes tax cuts for wealthy; focuses on fair taxation and rebates for families.",
            "IMMIGRATION": "Supports humane border policies; opposes family separations and mass deportations.",
            "FAMILY-VALUES": "Supports LGBTQ+ rights and gender-affirming care; promotes inclusive family policies.",
            "ELECTION-INTEGRITY": "Defends mail-in voting; opposes voter suppression laws."
        },
        "endorsements": ["EMILYs List", "Planned Parenthood", "Arizona Education Association"]
    },
    {
        "name": "Karrin Taylor Robson",
        "state": "Arizona",
        "office": "Governor",
        "party": "Republican",
        "bio": "Karrin Taylor Robson, born in 1966 in Mesa, Arizona, is a businesswoman and philanthropist. She graduated from Arizona State University with degrees in history and political science, then earned a law degree from ASU. Robson co-founded a real estate firm and served on the Arizona Board of Regents (2017-2021). Married to Chuck Robson, a heart surgeon, they have four children and reside in Phoenix. She ran for Governor in 2022, emphasizing border security and economic growth, and is endorsed by Trump for 2026.",
        "faith_statement": "No publicly disclosed faith statement, but supports freedom of religion and has attended evangelical events.",
        "website": "https://karrinforarizona.com/",
        "positions": {
            "ABORTION": "Pro-life after 15 weeks with exceptions; opposes late-term abortions.",
            "EDUCATION": "Supports ESA expansion and school choice; parental rights in curriculum.",
            "RELIGIOUS-FREEDOM": "Strong supporter of religious liberty protections for faith-based organizations.",
            "GUNS": "Defends Second Amendment; opposes new restrictions.",
            "TAXES": "Advocates for tax cuts and deregulation to boost economy.",
            "IMMIGRATION": "Secure borders; finish the wall and enforce E-Verify.",
            "FAMILY-VALUES": "Traditional marriage; opposes gender ideology in schools.",
            "ELECTION-INTEGRITY": "Voter ID required; clean voter rolls."
        },
        "endorsements": ["Donald Trump", "Arizona Free Enterprise Club", "Center for Arizona Policy"]
    },
    {
        "name": "Andy Biggs",
        "state": "Arizona",
        "office": "Governor",
        "party": "Republican",
        "bio": "Andy Biggs, born in 1958 in Tucson, Arizona, is a lawyer and politician. He holds a bachelor's from Brigham Young University and a law degree from ASU. Biggs served in the Arizona House (2003-2007) and Senate (2011-2017), including as president. Elected to Congress in 2016, he chairs the House Freedom Caucus. Married to Cindy Biggs, they have five children and are active in the LDS Church. Biggs focuses on fiscal conservatism and border security.",
        "faith_statement": "As a devout Mormon, Biggs has stated, 'My faith guides my service to protect life, liberty, and family values rooted in biblical principles.'",
        "website": "https://biggs.house.gov/",
        "positions": {
            "ABORTION": "Pro-life from conception; supports defunding Planned Parenthood.",
            "EDUCATION": "School choice and vouchers; ban CRT and gender ideology.",
            "RELIGIOUS-FREEDOM": "Protects faith-based exemptions; opposes mandates infringing on beliefs.",
            "GUNS": "Strong Second Amendment defender; no new gun laws.",
            "TAXES": "Cut taxes, reduce spending; balanced budget.",
            "IMMIGRATION": "Build wall, end sanctuary cities; mass deportations.",
            "FAMILY-VALUES": "Traditional family; parental rights over gender transitions.",
            "ELECTION-INTEGRITY": "Paper ballots, voter ID; audit every election."
        },
        "endorsements": ["Heritage Action", "National Right to Life", "Family Research Council"]
    },
    {
        "name": "David Schweikert",
        "state": "Arizona",
        "office": "Governor",
        "party": "Republican",
        "bio": "David Schweikert, born in 1962 in Los Angeles, moved to Arizona young. He earned a bachelor's from Arizona State University and an MBA from ASU. Schweikert served in the Arizona House (1991-1995), as Maricopa County Treasurer (2005-2007), and in Congress since 2011. Married to Joyce Schweikert, they have four children. Known for fiscal hawkishness and election reform advocacy.",
        "faith_statement": "As a Catholic, Schweikert has said, 'My faith compels me to defend the unborn and protect religious freedoms for all.'",
        "website": "https://schweikert.house.gov/",
        "positions": {
            "ABORTION": "Pro-life; supports heartbeat bill and restrictions.",
            "EDUCATION": "Empower parents with choice; oppose federal overreach.",
            "RELIGIOUS-FREEDOM": "Introduced WORSHIP Act to protect places of worship.",
            "GUNS": "Second Amendment absolutist; no infringements.",
            "TAXES": "Flat tax proposal; eliminate IRS.",
            "IMMIGRATION": "Secure borders; E-Verify mandatory.",
            "FAMILY-VALUES": "Protect traditional marriage; family tax credits.",
            "ELECTION-INTEGRITY": "Voter ID, proof of citizenship; end mail-in abuse."
        },
        "endorsements": ["NRA", "Americans for Prosperity", "CatholicVote"]
    },
    {
        "name": "Kris Mayes",
        "state": "Arizona",
        "office": "Attorney General",
        "party": "Democrat",
        "bio": "Kris Mayes, born in 1963 in Tulsa, Oklahoma, moved to Arizona for college. She graduated from Princeton and ASU Law. Mayes served as Arizona Corporation Commissioner (2019-2023) and won AG in 2022 by 280 votes. A former journalist, she is married with two children and focuses on consumer protection and reproductive rights.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://www.azag.gov/",
        "positions": {
            "ABORTION": "Pro-choice; defended access and sued to block bans.",
            "EDUCATION": "Supports public funding; warned on ESA discrimination.",
            "RELIGIOUS-FREEDOM": "Opposes taxpayer-funded religious schools.",
            "GUNS": "Supports reasonable regulations like background checks.",
            "TAXES": "Fair taxation; opposes corporate giveaways.",
            "IMMIGRATION": "Humane enforcement; opposes extreme measures.",
            "FAMILY-VALUES": "Inclusive policies for all families.",
            "ELECTION-INTEGRITY": "Protects voting rights; opposes suppression."
        },
        "endorsements": ["Planned Parenthood", "ACLU", "League of Women Voters"]
    },
    {
        "name": "Warren Petersen",
        "state": "Arizona",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "Warren Petersen, born in 1976 in Mesa, Arizona, is a real estate professional. He holds a bachelor's from BYU. Elected to Arizona House in 2012, Senate in 2016, and Senate President since 2023. Married with children, Petersen is a conservative leader on fiscal and social issues.",
        "faith_statement": "As a Christian conservative, Petersen has affirmed, 'Faith guides my commitment to protect the unborn and defend religious liberties.'",
        "website": "https://www.azleg.gov/Senate/Senate-member/?legislature=56&session=134&legislator=1654",
        "positions": {
            "ABORTION": "Pro-life; supports restrictions and defunding abortion providers.",
            "EDUCATION": "School choice advocate; parental rights bills.",
            "RELIGIOUS-FREEDOM": "Strong protections for faith-based adoption and schools.",
            "GUNS": "Second Amendment supporter; oppose red flag laws.",
            "TAXES": "Tax cuts and spending caps.",
            "IMMIGRATION": "Enforce laws; border security funding.",
            "FAMILY-VALUES": "Traditional values; oppose gender ideology.",
            "ELECTION-INTEGRITY": "Voter ID; clean rolls."
        },
        "endorsements": ["Arizona Chamber of Commerce", "Center for Arizona Policy", "NRA"]
    },
    {
        "name": "Rodney Glassman",
        "state": "Arizona",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "Rodney Glassman, born in 1974 in Tucson, is a lawyer and businessman. He graduated from ASU Law. Ran for U.S. Senate in 2010 and Tucson Mayor. Father of four, Glassman emphasizes law enforcement and economic growth.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://rodneyglassman.com/",
        "positions": {
            "ABORTION": "Pro-life with exceptions; enforce state laws.",
            "EDUCATION": "Support vouchers and charter schools.",
            "RELIGIOUS-FREEDOM": "Protect faith-based businesses.",
            "GUNS": "Defend gun rights.",
            "TAXES": "Lower taxes for families.",
            "IMMIGRATION": "Secure borders; work with Trump.",
            "FAMILY-VALUES": "Promote traditional families.",
            "ELECTION-INTEGRITY": "Proof of citizenship voting."
        },
        "endorsements": ["Arizona Police Association", "U.S. Chamber of Commerce"]
    },
    {
        "name": "Adrian Fontes",
        "state": "Arizona",
        "office": "Secretary of State",
        "party": "Democrat",
        "bio": "Adrian Fontes, born in 1970 in Inglewood, California, is a Marine veteran and lawyer. ASU Law graduate, he served as Maricopa County Recorder (2017-2021) and Secretary of State since 2023. Married to Norma Fontes, they have three children. Fontes reformed election processes post-2020.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://azsos.gov/",
        "positions": {
            "ABORTION": "Supports access; defended Prop 139.",
            "EDUCATION": "Public school advocate.",
            "RELIGIOUS-FREEDOM": "Neutral; focuses on equal protection.",
            "GUNS": "Reasonable regulations.",
            "TAXES": "Progressive taxation.",
            "IMMIGRATION": "Path to citizenship.",
            "FAMILY-VALUES": "Inclusive families.",
            "ELECTION-INTEGRITY": "Secure mail-in; combats misinformation."
        },
        "endorsements": ["VoteVets", "Arizona AFL-CIO"]
    },
    {
        "name": "Alexander Kolodin",
        "state": "Arizona",
        "office": "Secretary of State",
        "party": "Republican",
        "bio": "Alexander Kolodin, born in 1986 in Russia, immigrated young. ASU Law graduate, elected to Arizona House in 2022 for District 3. Focuses on election security and conservative reforms. Single, no children mentioned.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://www.azleg.gov/house/House-member/?legislature=56&session=134&legislator=2005",
        "positions": {
            "ABORTION": "Pro-life restrictions.",
            "EDUCATION": "Ban CRT; parental rights.",
            "RELIGIOUS-FREEDOM": "Protect Christian values.",
            "GUNS": "Full Second Amendment.",
            "TAXES": "Cut spending.",
            "IMMIGRATION": "Strict enforcement.",
            "FAMILY-VALUES": "Traditional marriage.",
            "ELECTION-INTEGRITY": "Hand-counted paper ballots."
        },
        "endorsements": ["FreedomWorks", "AZGOP"]
    },
    {
        "name": "Elijah Norton",
        "state": "Arizona",
        "office": "State Treasurer",
        "party": "Republican",
        "bio": "Elijah Norton, Arizona GOP treasurer and businessman. First candidate for 2026 Treasurer. Background in finance, focuses on fiscal responsibility. Family details not public.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "School choice.",
            "RELIGIOUS-FREEDOM": "Support protections.",
            "GUNS": "Pro-2A.",
            "TAXES": "Reduce taxes.",
            "IMMIGRATION": "Border security.",
            "FAMILY-VALUES": "Traditional values.",
            "ELECTION-INTEGRITY": "Voter ID."
        },
        "endorsements": ["AZGOP"]
    },
    {
        "name": "Tom Horne",
        "state": "Arizona",
        "office": "Superintendent of Public Instruction",
        "party": "Republican",
        "bio": "Tom Horne, born in 1945 in New York, is a lawyer and former AG (2011-2015). Elected Supt in 2022. Harvard and ASU Law graduate. Married, two children. Advocates for Holocaust education and anti-CRT measures.",
        "faith_statement": "As a Jewish person, Horne has said, 'Religious freedom is paramount; no negative reference to any faith is immoral.'",
        "website": "https://www.azed.gov/",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Ban CRT; support ESAs with limits.",
            "RELIGIOUS-FREEDOM": "Protect all faiths; Holocaust education.",
            "GUNS": "School safety measures.",
            "TAXES": "Efficient funding.",
            "IMMIGRATION": "Enforce laws.",
            "FAMILY-VALUES": "Parental rights.",
            "ELECTION-INTEGRITY": "Secure schools."
        },
        "endorsements": ["Arizona School Boards Association"]
    },
    {
        "name": "Kimberly Yee",
        "state": "Arizona",
        "office": "Superintendent of Public Instruction",
        "party": "Republican",
        "bio": "Kimberly Yee, born in 1982 in Phoenix, is the current Treasurer since 2019. First Asian American in statewide office. ASU journalism graduate. Married to Marvin Yee, two children. Yee challenges Horne in primary.",
        "faith_statement": "Yee has prayed publicly, stating, 'Faith and family guide my service to Arizona.'",
        "website": "https://www.aztreasury.gov/",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Full ESA support; no limits on purchases.",
            "RELIGIOUS-FREEDOM": "Protect faith-based schools.",
            "GUNS": "Pro-2A.",
            "TAXES": "Tax relief.",
            "IMMIGRATION": "Secure borders.",
            "FAMILY-VALUES": "Family priorities.",
            "ELECTION-INTEGRITY": "Transparent elections."
        },
        "endorsements": ["Former Republican Superintendents", "Goldwater Institute"]
    },
    {
        "name": "Brett Newby",
        "state": "Arizona",
        "office": "Superintendent of Public Instruction",
        "party": "Democrat",
        "bio": "Brett Newby is an educator and Board Certified Behavior Analyst. Father and advocate for public schools. Runs to fully fund education and empower teachers.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://www.brettnewby.com/",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Increase public funding; oppose vouchers.",
            "RELIGIOUS-FREEDOM": "Separation of church and state.",
            "GUNS": "Gun safety in schools.",
            "TAXES": "Fund education via taxes.",
            "IMMIGRATION": "Support immigrant students.",
            "FAMILY-VALUES": "Inclusive education.",
            "ELECTION-INTEGRITY": "Accessible voting."
        },
        "endorsements": ["Arizona Education Association"]
    },
    {
        "name": "Gina Swoboda",
        "state": "Arizona",
        "office": "U.S. House District 1",
        "party": "Republican",
        "bio": "Gina Swoboda, AZGOP Chair since 2023. Background in elections and conservative activism. Trump-endorsed for CD1 after Schweikert's gubernatorial run.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "School choice.",
            "RELIGIOUS-FREEDOM": "Protect freedoms.",
            "GUNS": "2A rights.",
            "TAXES": "Cut taxes.",
            "IMMIGRATION": "Secure borders.",
            "FAMILY-VALUES": "Traditional values.",
            "ELECTION-INTEGRITY": "Clean voter rolls."
        },
        "endorsements": ["Donald Trump"]
    },
    {
        "name": "Brian Del Vecchio",
        "state": "Arizona",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "bio": "Brian Del Vecchio is an attorney and activist running in Democratic primary for CD1.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Public schools.",
            "RELIGIOUS-FREEDOM": "Equal protections.",
            "GUNS": "Background checks.",
            "TAXES": "Fair share.",
            "IMMIGRATION": "Reform.",
            "FAMILY-VALUES": "Inclusive.",
            "ELECTION-INTEGRITY": "Expand access."
        },
        "endorsements": []
    },
    {
        "name": "Juan Ciscomani",
        "state": "Arizona",
        "office": "U.S. House District 6",
        "party": "Republican",
        "bio": "Juan Ciscomani, born in Tucson, is a first-generation American. Served in Gov. Ducey's office. Elected to Congress in 2022. Married with children.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://ciscomani.house.gov/",
        "positions": {
            "ABORTION": "Pro-life with exceptions.",
            "EDUCATION": "School choice.",
            "RELIGIOUS-FREEDOM": "Support protections.",
            "GUNS": "2A.",
            "TAXES": "Cut taxes.",
            "IMMIGRATION": "Bipartisan reform.",
            "FAMILY-VALUES": "Family focus.",
            "ELECTION-INTEGRITY": "Secure elections."
        },
        "endorsements": ["U.S. Chamber"]
    },
    {
        "name": "JoAnna Mendoza",
        "state": "Arizona",
        "office": "U.S. House District 6",
        "party": "Democrat",
        "bio": "JoAnna Mendoza, Marine veteran with 20 years service. Drill instructor and educator. Runs to protect democracy and veterans.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Fund public schools.",
            "RELIGIOUS-FREEDOM": "Freedom for all.",
            "GUNS": "Safety measures.",
            "TAXES": "Middle-class relief.",
            "IMMIGRATION": "Humane paths.",
            "FAMILY-VALUES": "Support military families.",
            "ELECTION-INTEGRITY": "Protect voting."
        },
        "endorsements": ["EMILYs List", "VoteVets"]
    }
]

# Arizona Summary
summary = {
    "state": "Arizona",
    "title": "Arizona 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Arizona 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 18
**Total Candidates Profiled:** 20
**Election Dates:**
- 2025-11-04 (Local/Municipal Elections)
- 2026-08-04 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Arizona POLITICAL LANDSCAPE

### **The Grand Canyon State**

Arizona is a **battleground state leaning purple**:
- **Border Security:** As a frontier state, Arizona faces daily challenges from illegal immigration, straining resources and impacting family safety.
- **Economic Powerhouse:** Booming tech and tourism sectors drive growth, but high housing costs threaten family stability.
- **Urban-Rural Divide:** Phoenix metro (Maricopa County) leans Democratic, while rural counties like Mohave and Yavapai are solidly Republican strongholds.
- **Evangelical Influence:** Growing megachurches and Christian universities like Arizona Christian University mobilize conservative voters.

### **Why Arizona Matters**

Arizona is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Prop 139 (2024) enshrined abortion rights up to viability, but conservatives fight for heartbeat bills and defunding Planned Parenthood; 15-week ban struck down in 2025.
- ✅ **Second Amendment:** Permitless carry since 2010; no assault weapon bans, strong protections for self-defense.
- ✅ **School Choice:** Universal ESA program serves 80,000+ students (2025), empowering parents against woke curricula.
- ✅ **Religious Liberty:** Robust RFRA-like protections; ongoing battles over faith-based adoption agencies.
- ✅ **Family Values:** Parental rights laws ban gender transitions for minors; traditional marriage upheld.
- ✅ **Election Integrity:** Proof of citizenship required for state elections; paper ballots and audits standard.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** This race controls veto power over pro-life bills, school choice expansions, and border funding—pivotal for reversing progressive gains.

**Katie Hobbs (Democrat)** - Incumbent Governor

**Faith Statement:** "No publicly disclosed faith statement. Hobbs has spoken about her Catholic upbringing but supports pro-choice policies."

**Background:**
- Social worker turned politician; ASU master's in social work.
- First Democrat governor in 15 years; married with two children.
- Vetoed 174 bills in 2025, including Ten Commandments display.

**Christian Conservative Analysis:**
- **Pro-Life:** 2/10 - Championed Prop 139; blocked restrictions.
- **Religious Liberty:** 3/10 - Vetoed faith protections.
- **Education/Parental Rights:** 4/10 - Opposes ESA growth.
- **Family Values:** 2/10 - Supports gender-affirming care.
- **Overall Assessment:** 3/10 - Progressive policies undermine biblical values; not aligned with Christian conservatives.

**Key Positions:**
- **ABORTION:** Pro-choice up to viability; exceptions unlimited.
- **EDUCATION:** Public school funding; criticizes vouchers as discriminatory.
- **RELIGIOUS FREEDOM:** Strict separation; opposes religious displays in schools.
- **GUNS:** Universal checks; red flag laws.
- **TAXES:** No cuts for wealthy; rebates for low-income.
- **Border Security:** Humane policies; opposes wall expansion.

**Endorsements:** EMILYs List, Planned Parenthood.

**Website:** https://azgovernor.gov/

**Karrin Taylor Robson (Republican)** - Businesswoman

**Faith Statement:** "No publicly disclosed faith statement, but supports freedom of religion and has attended evangelical events."

**Background:**
- ASU law graduate; co-founded real estate firm.
- Board of Regents; four children with husband Chuck.
- 2022 GOP nominee; Trump-endorsed.

**Christian Conservative Analysis:**
- **Pro-Life:** 8/10 - Supports 15-week ban with exceptions.
- **Religious Liberty:** 9/10 - Defends faith-based exemptions.
- **Education/Parental Rights:** 9/10 - ESA champion.
- **Family Values:** 8/10 - Opposes woke indoctrination.
- **Overall Assessment:** 8/10 - Strong conservative; aligns with biblical family priorities.

**Key Positions:**
- **ABORTION:** Restrictions after 15 weeks; promote adoption.
- **EDUCATION:** Expand choice; ban CRT.
- **RELIGIOUS FREEDOM:** Protect churches from mandates.
- **GUNS:** Full 2A rights.
- **TAXES:** Permanent cuts; deregulation.
- **Border Security:** Finish wall; E-Verify.

**Endorsements:** Donald Trump, Center for Arizona Policy.

**Website:** https://karrinforarizona.com/

**Andy Biggs (Republican)** - U.S. Representative

**Faith Statement:** "As a devout Mormon, Biggs has stated, 'My faith guides my service to protect life, liberty, and family values rooted in biblical principles.'"

**Background:**
- BYU and ASU Law; Arizona Senate President (2013-2017).
- Freedom Caucus chair; five children.
- Fiscal hawk in Congress.

**Christian Conservative Analysis:**
- **Pro-Life:** 10/10 - Defunds abortions; heartbeat bill supporter.
- **Religious Liberty:** 10/10 - Opposes contraceptive mandates.
- **Education/Parental Rights:** 9/10 - Vouchers and bans on ideology.
- **Family Values:** 10/10 - Traditional marriage defender.
- **Overall Assessment:** 10/10 - Exemplary alignment with Christian conservatism.

**Key Positions:**
- **ABORTION:** Ban from conception; no taxpayer funding.
- **EDUCATION:** Universal choice; end federal indoctrination.
- **RELIGIOUS FREEDOM:** RFRA enforcer.
- **GUNS:** No restrictions.
- **TAXES:** Flat tax; balanced budget.
- **Border Security:** Mass deportations.

**Endorsements:** Heritage Action, National Right to Life.

**Website:** https://biggs.house.gov/

**Why It Matters:** Governor sets agenda for life-affirming laws in a border state.

### **Attorney General** - 2026-11-03

**Context:** AG enforces (or blocks) pro-life and election laws; key for defending RFRA.

**Kris Mayes (Democrat)** - Incumbent AG

**Faith Statement:** "No publicly disclosed faith statement."

**Background:**
- Princeton and ASU Law; Corporation Commissioner.
- Won by 280 votes in 2022; two children.
- Sued to protect abortion access.

**Christian Conservative Analysis:**
- **Pro-Life:** 1/10 - Blocked bans; pro-choice advocate.
- **Religious Liberty:** 4/10 - Opposes religious charters.
- **Education/Parental Rights:** 3/10 - Warned on ESA discrimination.
- **Family Values:** 2/10 - Supports expansive rights.
- **Overall Assessment:** 2/10 - Actively undermines conservative priorities.

**Key Positions:**
- **ABORTION:** Full access; sued Trump admin.
- **EDUCATION:** Public focus; anti-voucher.
- **RELIGIOUS FREEDOM:** No taxpayer religious schools.
- **GUNS:** Regulations.
- **TAXES:** Progressive.
- **Border Security:** Humane.

**Endorsements:** ACLU, Planned Parenthood.

**Website:** https://www.azag.gov/

**Warren Petersen (Republican)** - Senate President

**Faith Statement:** "As a Christian conservative, Petersen has affirmed, 'Faith guides my commitment to protect the unborn and defend religious liberties.'"

**Background:**
- BYU graduate; real estate.
- House 2013, Senate 2017; married with children.

**Christian Conservative Analysis:**
- **Pro-Life:** 9/10 - Sponsored restrictions.
- **Religious Liberty:** 9/10 - Faith adoption protections.
- **Education/Parental Rights:** 8/10 - Choice bills.
- **Family Values:** 9/10 - Anti-gender ideology.
- **Overall Assessment:** 9/10 - Reliable defender of values.

**Key Positions:**
- **ABORTION:** Enforce limits.
- **EDUCATION:** Parental consent.
- **RELIGIOUS FREEDOM:** Strong RFRA.
- **GUNS:** Pro-2A.
- **TAXES:** Cuts.
- **Border Security:** Enforcement.

**Endorsements:** Center for Arizona Policy, NRA.

**Website:** https://www.azleg.gov/

**Why It Matters:** AG can shield or strike down faith-based laws.

### **Secretary of State** - 2026-11-03

**Context:** Oversees elections; vital for integrity amid 2020 controversies.

**Adrian Fontes (Democrat)** - Incumbent

**Faith Statement:** "No publicly disclosed faith statement."

**Background:**
- Marine veteran; ASU Law.
- Maricopa Recorder; three children.

**Christian Conservative Analysis:**
- **Pro-Life:** 3/10 - Supports access.
- **Religious Liberty:** 5/10 - Neutral.
- **Education/Parental Rights:** 4/10 - Public advocate.
- **Family Values:** 3/10 - Inclusive.
- **Overall Assessment:** 4/10 - Weak on security.

**Key Positions:**
- **ABORTION:** Protected Prop 139.
- **EDUCATION:** Funding public.
- **RELIGIOUS FREEDOM:** Equal.
- **GUNS:** Checks.
- **TAXES:** Fair.
- **Border Security:** Reform.

**Endorsements:** VoteVets.

**Website:** https://azsos.gov/

**Alexander Kolodin (Republican)** - State Rep

**Faith Statement:** "No publicly disclosed faith statement."

**Background:**
- Russian immigrant; ASU Law.
- Elected 2022; far-right.

**Christian Conservative Analysis:**
- **Pro-Life:** 8/10 - Restrictions.
- **Religious Liberty:** 8/10 - Protections.
- **Education/Parental Rights:** 9/10 - Bans on woke.
- **Family Values:** 8/10 - Traditional.
- **Overall Assessment:** 8/10 - Strong on integrity.

**Key Positions:**
- **ABORTION:** Limits.
- **EDUCATION:** No CRT.
- **RELIGIOUS FREEDOM:** Christian defense.
- **GUNS:** Full rights.
- **TAXES:** Low.
- **Border Security:** Strict.

**Endorsements:** AZGOP.

**Website:** https://www.azleg.gov/

**Why It Matters:** Ensures fraud-free elections for faith voters.

### **State Treasurer** - 2026-11-03

**Context:** Manages funds for ESAs and tax relief.

**Elijah Norton (Republican)** - GOP Treasurer

**Faith Statement:** "No publicly disclosed faith statement."

**Background:**
- Finance expert; first candidate.

**Christian Conservative Analysis:**
- **Pro-Life:** 7/10.
- **Religious Liberty:** 7/10.
- **Education/Parental Rights:** 8/10 - ESA funding.
- **Family Values:** 7/10.
- **Overall Assessment:** 7/10 - Fiscal focus aids families.

**Key Positions:**
- **ABORTION:** Pro-life.
- **EDUCATION:** Choice.
- **RELIGIOUS FREEDOM:** Support.
- **GUNS:** Pro.
- **TAXES:** Relief.
- **Border Security:** Yes.

**Endorsements:** AZGOP.

**Website:** ""

**Why It Matters:** Directs dollars to pro-family programs.

### **Superintendent of Public Instruction** - 2026-11-03

**Context:** Shapes curriculum; battle over woke vs. parental rights.

**Tom Horne (Republican)** - Incumbent

**Faith Statement:** "As a Jewish person, Horne has said, 'Religious freedom is paramount; no negative reference to any faith is immoral.'"

**Background:**
- Harvard/ASU Law; former AG.
- Holocaust education advocate.

**Christian Conservative Analysis:**
- **Pro-Life:** 7/10.
- **Religious Liberty:** 8/10 - All faiths.
- **Education/Parental Rights:** 8/10 - Anti-CRT.
- **Family Values:** 7/10.
- **Overall Assessment:** 7/10 - Good on indoctrination.

**Key Positions:**
- **ABORTION:** Pro-life.
- **EDUCATION:** Ban ideology; ESAs with oversight.
- **RELIGIOUS FREEDOM:** Holocaust/faith ed.
- **GUNS:** School safety.
- **TAXES:** Efficient.
- **Border Security:** Enforce.

**Endorsements:** Arizona School Boards.

**Website:** https://www.azed.gov/

**Kimberly Yee (Republican)** - Treasurer

**Faith Statement:** "Yee has prayed publicly, stating, 'Faith and family guide my service to Arizona.'"

**Background:**
- ASU journalism; first Asian statewide.
- Married, two kids.

**Christian Conservative Analysis:**
- **Pro-Life:** 8/10.
- **Religious Liberty:** 8/10.
- **Education/Parental Rights:** 9/10 - Unlimited ESAs.
- **Family Values:** 9/10.
- **Overall Assessment:** 9/10 - Pro-choice powerhouse.

**Key Positions:**
- **ABORTION:** Pro-life.
- **EDUCATION:** Full ESA freedom.
- **RELIGIOUS FREEDOM:** Faith schools.
- **GUNS:** Pro.
- **TAXES:** Relief.
- **Border Security:** Secure.

**Endorsements:** Goldwater Institute.

**Website:** https://www.aztreasury.gov/

**Brett Newby (Democrat)** - Educator

**Faith Statement:** "No publicly disclosed faith statement."

**Background:**
- Behavior analyst; father.

**Christian Conservative Analysis:**
- **Pro-Life:** 2/10.
- **Religious Liberty:** 3/10.
- **Education/Parental Rights:** 2/10 - Anti-voucher.
- **Family Values:** 3/10.
- **Overall Assessment:** 2/10 - Public school lock.

**Key Positions:**
- **ABORTION:** Pro-choice.
- **EDUCATION:** Fund public; end vouchers.
- **RELIGIOUS FREEDOM:** Separation.
- **GUNS:** Safety.
- **TAXES:** Increase for ed.
- **Border Security:** Support students.

**Endorsements:** AEA.

**Website:** https://www.brettnewby.com/

**Why It Matters:** Controls what kids learn—biblical truth or ideology.

---

## 🎯 KEY ISSUES FOR ARIZONA CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- 15-week ban struck (2025); push heartbeat bill.
- 200+ pregnancy centers; parental consent laws.
- No state funding for abortions.
- Victories: Repeal 1864 ban attempt failed.
- Challenges: Prop 139 expansion.

**Progressive Position:**
- Viability access; fund Planned Parenthood.
- Remove consent requirements.
- Battles over telehealth abortions.

**Christian Conservative Action:**
- Join Arizona Right to Life (azrtl.org).
- Support HB 2677 heartbeat bill.
- Volunteer at centers; pray for justices.
- Vote pro-life; iVoterGuide ratings.

### **School Choice & Parental Rights**

**Conservative Position:**
- Universal ESA: $7,000/child (2025); 80k students.
- Bans on CRT/gender ideology (HB 2898).
- Homeschool freedom; no mandates.
- Wins: Expanded ESAs despite costs.

**Progressive Position:**
- Union control; DEI in curriculum.
- Threats to defund choice programs.

**Christian Conservative Action:**
- Run for school boards via AZ School Boards Assoc.
- Support SB 1163 parental rights.
- Join Center for AZ Policy (azpolicy.org).

### **Religious Freedom**

**Conservative Position:**
- RFRA protects faith adoptions.
- No religious charters blocked (2025).
- Holocaust ed mandated.

**Progressive Position:**
- Taxpayer secularism; anti-faith exemptions.

**Christian Conservative Action:**
- Alliance Defending Freedom cases.
- Oppose HB 2618 religious school ban.
- First Liberty Institute (firstliberty.org).

### **Guns**

**Conservative Position:**
- Permitless carry; no bans.
- Stand Your Ground law.

**Progressive Position:**
- Red flag laws; assault bans.

**Christian Conservative Action:**
- AZ Citizens for Gun Safety? No, NRA (nraila.org).
- Support SB 1165 protections.

### **Taxes**

**Conservative Position:**
- Cuts via TCJA extension; rebates.

**Progressive Position:**
- Raise on wealthy; green taxes.

**Christian Conservative Action:**
- Goldwater Institute (goldwaterinstitute.org).
- Oppose Prop 208 surcharge.

### **Immigration**

**Conservative Position:**
- E-Verify; wall funding.
- Oppose sanctuary.

**Progressive Position:**
- DACA expansion; amnesty.

**Christian Conservative Action:**
- FAIR (fairus.org); border prayer vigils.

### **Family Values**

**Conservative Position:**
- Minors gender ban (SB 1025).
- Traditional marriage.

**Progressive Position:**
- Gender care access; LGBTQ+ curricula.

**Christian Conservative Action:**
- Family Policy Alliance (familypolicyalliance.org).
- Support HB 2062 parental notification.

### **Election Integrity**

**Conservative Position:**
- Proof citizenship; audits.
- Paper ballots.

**Progressive Position:**
- Mail-in expansion; no ID.

**Christian Conservative Action:**
- True the Vote; poll watching.
- Support HCR 2025 audits.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- **2026-04-06** - Candidate filing deadline
- **2026-07-30** - Voter registration deadline for primary
- **2026-08-04** - Primary Election
- **2026-10-05** - Voter registration deadline for general
- **2026-10-07** - Early voting begins
- **2026-11-03** - General Election

**Voter Registration:** azsos.gov/vote

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
✅ **Share on social media** with #AZFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR ARIZONA CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Arizona coverage
- **Arizona Right to Life** - Pro-life ratings (azrtl.org)
- **Center for Arizona Policy** - Faith-based education (azpolicy.org)
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Arizona Secretary of State**: azsos.gov
- **County Election Offices**: Contact via azsos.gov/elections
- **Early Voting Locations**: azsos.gov/elections/locations

### **Conservative Organizations:**
- **Arizona Right to Life**: azrtl.org
- **Center for Arizona Policy**: azpolicy.org
- **Arizona Citizens Defense League**: azcdl.org
- **Goldwater Institute**: goldwaterinstitute.org
- **Alliance Defending Freedom** - Religious liberty (adflegal.org)
- **First Liberty Institute** - Religious freedom (firstliberty.org)

---

## 🔥 BOTTOM LINE FOR ARIZONA CHRISTIANS

**2026 Elections Matter:**
- Governor determines pro-life vetoes.
- AG enforces family laws.
- SOS guards ballot box.
- Supt shapes godly education.
- Overall state direction at stake.

**If Conservatives Win:**

✅ Pro-life protections strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Border secured, families safe
✅ Tax relief for hardworking parents
✅ ESA funding unlimited

**If Progressives Win:**

❌ Abortion up to birth, bans repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Open borders chaos
❌ Tax hikes on families
❌ Woke indoctrination mandatory

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Katie Hobbs, Karrin Taylor Robson, Andy Biggs, David Schweikert and families
- Arizona Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Arizona
- Revival and awakening in Arizona
- God's will in Arizona elections

**Scripture for ARIZONA Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Arizona coverage, email contact@ekewaka.com

**ARIZONA CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Arizona races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Arizona'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Arizona races...")
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

print(f"\nChecking for existing Arizona candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Arizona'}
)['Items']
existing_candidate_map = {(c['name'], c['office']): c['candidate_id'] for c in existing_candidates}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Arizona candidates...")
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

print("\nProcessing Arizona summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Arizona'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Arizona data upload complete!")