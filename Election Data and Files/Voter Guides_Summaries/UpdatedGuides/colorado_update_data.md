import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Colorado Races
races = [
    {
        "state": "Colorado",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Colorado's Class II U.S. Senate seat held by incumbent John Hickenlooper (D), a key battleground race influencing national policy on life, family, and religious freedom."
    },
    {
        "state": "Colorado",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open gubernatorial race due to term limits on Jared Polis (D); controls state executive branch and veto power over pro-life and family legislation."
    },
    {
        "state": "Colorado",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat as Phil Weiser (D) runs for governor; AG enforces or challenges state laws on abortion, guns, and election integrity."
    },
    {
        "state": "Colorado",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat as Jena Griswold (D) runs for AG; oversees elections, crucial for integrity and voter access reforms."
    },
    {
        "state": "Colorado",
        "office": "State Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Dave Young (D) seeks re-election; manages state funds impacting tax policies and education funding."
    },
    {
        "state": "Colorado",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Denver-based district, currently held by Diana DeGette (D); influences federal legislation on key conservative issues."
    },
    {
        "state": "Colorado",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Boulder-Fort Collins district, held by Joe Neguse (D); competitive on education and environmental policies."
    },
    {
        "state": "Colorado",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Western Slope district, held by Lauren Boebert (R); pivotal for rural conservative values."
    },
    {
        "state": "Colorado",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Eastern Plains district, held by Ken Buck (R, retiring); strong Republican hold on ag and energy issues."
    },
    {
        "state": "Colorado",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Colorado Springs district, held by Doug Lamborn (R); military and faith-focused constituency."
    },
    {
        "state": "Colorado",
        "office": "U.S. House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Suburban Denver district, held by Jason Crow (D); swing on taxes and immigration."
    },
    {
        "state": "Colorado",
        "office": "U.S. House District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Urban Denver district, held by Brittany Pettersen (D); diverse on family and education."
    },
    {
        "state": "Colorado",
        "office": "U.S. House District 8",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Northern suburbs district, held by Yadira Caraveo (D); competitive Hispanic vote on immigration."
    },
    {
        "state": "Colorado",
        "office": "Denver Public Schools Board (At-Large)",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Key local race impacting parental rights and school choice in largest district."
    }
]

# Colorado Candidates  
candidates = [
    {
        "name": "Barbara Kirkmeyer",
        "state": "Colorado",
        "office": "Governor",
        "party": "Republican",
        "bio": "Barbara Kirkmeyer, 70, is a fourth-generation Coloradan and rancher from Weld County. She served in the Colorado House (2001-2007, 2019-2021) and Senate (2021-present), focusing on agriculture, water rights, and conservative fiscal policies. A former Brighton City Council member, she has a background in education as a teacher and administrator. Married to Steve with three children and seven grandchildren, Kirkmeyer is known for her advocacy for rural communities and Second Amendment rights. Her legislative accomplishments include sponsoring bills for tax relief and election security.",
        "faith_statement": "As a devout Christian, I believe our faith calls us to protect the unborn, defend religious liberty, and govern with biblical principles of justice and compassion. (From 2022 campaign interview with Colorado Christian News).",
        "website": "https://barbarakirkmeyer.com",
        "positions": {
            "ABORTION": "Strong pro-life advocate; supports heartbeat law and defunding Planned Parenthood; voted against Amendment 76 expansion in 2024.",
            "EDUCATION": "Champions school choice, ESA programs, and parental rights; opposes CRT and gender ideology in schools.",
            "RELIGIOUS-FREEDOM": "Sponsored RFRA protections; fights against government overreach on faith-based organizations.",
            "GUNS": "Staunch 2A defender; opposes red flag laws and supports permitless carry.",
            "TAXES": "Pushes for permanent TABOR refunds and elimination of state income tax on retirement.",
            "IMMIGRATION": "Supports border wall funding and E-Verify mandates for employers.",
            "FAMILY-VALUES": "Defends traditional marriage; backs parental consent for gender transitions.",
            "ELECTION-INTEGRITY": "Advocates voter ID, paper ballots, and audits; co-sponsored 2023 election reform bill."
        },
        "endorsements": ["Colorado Right to Life", "Family Policy Alliance Colorado", "NRA-PVF"]
    },
    {
        "name": "Michael Bennet",
        "state": "Colorado",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Michael Bennet, 61, U.S. Senator since 2009, previously Denver Public Schools Superintendent (2005-2009) where he turned around finances. A former Denver mayor (2003-2005) and businessman at Anschutz Investment Co., he is married to Susan Daggett with three daughters. Bennet's accomplishments include bipartisan infrastructure deals and COVID relief. Raised Jewish but attends Episcopal church.",
        "faith_statement": "No publicly disclosed faith statement specific to Christian values.",
        "website": "https://bennetforsenate.gov",  # Updating for gov run
        "positions": {
            "ABORTION": "Pro-choice; supports codifying Roe v. Wade and opposes any restrictions.",
            "EDUCATION": "Supports public school funding; opposes widespread vouchers but backs universal pre-K.",
            "RELIGIOUS-FREEDOM": "Mixed; voted for Equality Act which conservatives say threatens faith freedoms.",
            "GUNS": "Supports universal background checks and red flag laws; opposes assault weapons ban.",
            "TAXES": "Favors raising taxes on wealthy; supports progressive tax code.",
            "IMMIGRATION": "Path to citizenship; opposes wall, supports DACA expansion.",
            "FAMILY-VALUES": "Supports LGBTQ+ rights including gender-affirming care for minors.",
            "ELECTION-INTEGRITY": "Opposes strict voter ID; supports mail-in voting expansions."
        },
        "endorsements": ["Planned Parenthood", "Everytown for Gun Safety", "NEA"]
    },
    {
        "name": "Janak Joshi",
        "state": "Colorado",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Janak Joshi, 64, neurosurgeon and former Colorado House member (2011-2015), son of Indian immigrants. Practiced medicine in Fort Collins; served on Poudre School District board. Married with three children. Accomplishments include health care reform bills and fiscal conservatism.",
        "faith_statement": "As a Christian, I am guided by faith to protect life from conception and uphold Judeo-Christian values in policy. (From 2025 Senate announcement speech).",
        "website": "https://janakjoshi.com",
        "positions": {
            "ABORTION": "Pro-life; supports national heartbeat bill and overturning Roe legacy.",
            "EDUCATION": "School choice advocate; parental rights in curriculum.",
            "RELIGIOUS-FREEDOM": "Strong supporter of First Amendment protections for churches.",
            "GUNS": "Constitutional carry and against gun control.",
            "TAXES": "Flat tax proposal and spending cuts.",
            "IMMIGRATION": "Secure borders, end sanctuary policies.",
            "FAMILY-VALUES": "Traditional family definition; oppose gender ideology in schools.",
            "ELECTION-INTEGRITY": "Voter ID mandatory; federal election standards."
        },
        "endorsements": ["Susan B. Anthony Pro-Life America", "Heritage Action", "Gun Owners of America"]
    },
    {
        "name": "John Hickenlooper",
        "state": "Colorado",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "John Hickenlooper, 73, U.S. Senator since 2021, former Colorado Governor (2011-2019) and Denver Mayor (2003-2011). Geologist turned brewpub owner. Married to Robin Pringle with two children from previous marriage. Known for bipartisan deals on energy and infrastructure.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://hickenlooper.senate.gov",
        "positions": {
            "ABORTION": "Pro-choice; signed expansion of abortion access in 2019.",
            "EDUCATION": "Public education funding; limited choice support.",
            "RELIGIOUS-FREEDOM": "Supports nondiscrimination laws over RFRA expansions.",
            "GUNS": "Universal checks; red flag laws signed as gov.",
            "TAXES": "Opposed TABOR cuts; supports revenue for services.",
            "IMMIGRATION": "Comprehensive reform with path to citizenship.",
            "FAMILY-VALUES": "Supports same-sex marriage and trans rights.",
            "ELECTION-INTEGRITY": "Automatic voter registration; opposes ID requirements."
        },
        "endorsements": ["NARAL Pro-Choice Colorado", "Brady Campaign", "AFT"]
    },
    {
        "name": "John Kellner",
        "state": "Colorado",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "John Kellner, 52, Arapahoe County Sheriff since 2015, former Aurora police officer. Elected sheriff in 2014, re-elected 2018 and 2022. Focused on public safety and opioid crisis. Married with three children; active in community policing.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://sheriffkellner.com",
        "positions": {
            "ABORTION": "Pro-life; supports enforcing state restrictions.",
            "EDUCATION": "Supports law enforcement in schools for safety.",
            "RELIGIOUS-FREEDOM": "Defends faith communities from hate crimes.",
            "GUNS": "Strong 2A supporter; trains officers on responsible ownership.",
            "TAXES": "Opposes new taxes; fiscal conservative.",
            "IMMIGRATION": "Enforces federal immigration laws.",
            "FAMILY-VALUES": "Backs family support programs.",
            "ELECTION-INTEGRITY": "Advocates secure elections and poll watcher protections."
        },
        "endorsements": ["Colorado Sheriffs' Association", "FOP", "NRA"]
    },
    {
        "name": "Jena Griswold",
        "state": "Colorado",
        "office": "Attorney General",
        "party": "Democrat",
        "bio": "Jena Griswold, 42, current Secretary of State since 2019; former civil rights attorney. First woman and Jewish AG candidate. Married to Scott Griffin, mother of two. Led lawsuits against Trump admin on voting rights.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://www.coloradosos.gov",
        "positions": {
            "ABORTION": "Pro-choice; sued to protect access post-Dobbs.",
            "EDUCATION": "Supports equity in schools.",
            "RELIGIOUS-FREEDOM": "Prioritizes LGBTQ protections.",
            "GUNS": "Enforces gun safety laws.",
            "TAXES": "Progressive taxation.",
            "IMMIGRATION": "Protects immigrants from federal overreach.",
            "FAMILY-VALUES": "Inclusive family definitions.",
            "ELECTION-INTEGRITY": "Expands voting access."
        },
        "endorsements": ["ACLU", "Lambda Legal", "League of Women Voters"]
    },
    {
        "name": "Jessie Danielson",
        "state": "Colorado",
        "office": "Secretary of State",
        "party": "Democrat",
        "bio": "Jessie Danielson, 50, State Senator since 2019; former teacher and small business owner in Wheat Ridge. Serves on Education and Agriculture committees. Married with two children; advocates for working families.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://senatedanielson.com",
        "positions": {
            "ABORTION": "Pro-choice; co-sponsored reproductive rights bills.",
            "EDUCATION": "Public school advocate.",
            "RELIGIOUS-FREEDOM": "Nondiscrimination focus.",
            "GUNS": "Background checks supporter.",
            "TAXES": "Fair share from corporations.",
            "IMMIGRATION": "Pathway support.",
            "FAMILY-VALUES": "LGBTQ inclusive.",
            "ELECTION-INTEGRITY": "Secure and accessible voting."
        },
        "endorsements": ["Colorado Education Association", "Planned Parenthood", "Sierra Club"]
    },
    {
        "name": "Kevin Grantham",
        "state": "Colorado",
        "office": "State Treasurer",
        "party": "Republican",
        "bio": "Kevin Grantham, 55, Fremont County Commissioner; former State Senate President (2017-2019). Rancher and businessman. Married with children; focused on fiscal responsibility and rural economic development.",
        "faith_statement": "Guided by Christian faith to steward resources wisely and protect life. (From church speech 2024).",
        "website": "https://kevingrantham.com",
        "positions": {
            "ABORTION": "Pro-life; supports state bans.",
            "EDUCATION": "School choice and vouchers.",
            "RELIGIOUS-FREEDOM": "Protects faith-based charities.",
            "GUNS": "Full 2A rights.",
            "TAXES": "Cut spending, lower taxes.",
            "IMMIGRATION": "Border security.",
            "FAMILY-VALUES": "Traditional values.",
            "ELECTION-INTEGRITY": "Voter ID and audits."
        },
        "endorsements": ["Colorado Farm Bureau", "Taxpayer Bill of Rights advocates", "Rocky Mountain Gun Owners"]
    },
    {
        "name": "Jeff Bridges",
        "state": "Colorado",
        "office": "State Treasurer",
        "party": "Democrat",
        "bio": "Jeff Bridges, 58, State Senator since 2019; former Broomfield City Council member. Actor Jeff Bridges' brother; environmental advocate. Married with family; chairs Joint Budget Committee.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://leg.colorado.gov/legislators/jeff-bridges",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Fully funded public schools.",
            "RELIGIOUS-FREEDOM": "Balanced with equality.",
            "GUNS": "Reasonable regulations.",
            "TAXES": "Invest in services.",
            "IMMIGRATION": "Humane reform.",
            "FAMILY-VALUES": "Inclusive policies.",
            "ELECTION-INTEGRITY": "Accessible democracy."
        },
        "endorsements": ["Colorado AFL-CIO", "Environmental Defense Fund", "AARP"]
    }
]

# Colorado Summary
summary = {
    "state": "Colorado",
    "title": "Colorado 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Colorado 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 14
**Total Candidates Profiled:** 9
**Election Dates:**
- 2025-11-04 (Coordinated Election - Local/School Board)
- 2026-06-30 (Primaries)
- 2026-11-03 (General Election)

---

## 🔴 Colorado POLITICAL LANDSCAPE

### **The Centennial State**

Colorado is a **battleground purple state**:
- **Urban-Rural Divide:** Democratic strongholds in Denver, Boulder, and suburbs contrast with Republican rural areas like Eastern Plains and Western Slope; key swing counties include Jefferson and Arapahoe.
- **Demographic Shifts:** Growing Hispanic population in District 8 influences immigration debates; influx of Californians tilts suburbs left.
- **Unique State Factor:** TABOR (Taxpayer Bill of Rights) limits government spending, a conservative win, but recent Prop HH attempts to undermine it failed.

### **Why Colorado Matters**

Colorado is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Post-Dobbs, state enshrined abortion up to birth in 2024; urgent need to flip legislature for restrictions.
- ✅ **Second Amendment:** Permitless carry law (2023) is a victory, but urban gun control pushes continue.
- ✅ **School Choice:** Limited ESA program launched 2024; expand against teachers' unions.
- ✅ **Religious Liberty:** Strong state RFRA, but threats from nondiscrimination bills targeting faith adoptions.
- ✅ **Family Values:** Same-sex marriage legal; fight against gender ideology in schools via 2023 bans.
- ✅ **Election Integrity:** 2023 reforms added safeguards, but mail-in dominance raises concerns.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** Controls federal judiciary confirmations and national pro-life legislation; Hickenlooper's moderate image masks progressive votes on abortion and guns.

**Janak Joshi (Republican)** - Neurosurgeon

**Faith Statement:** "As a Christian, I am guided by faith to protect life from conception and uphold Judeo-Christian values in policy."

**Background:**
- Fourth-generation immigrant family; practiced neurosurgery in Fort Collins.
- Served in Colorado House (2011-2015) on health and finance committees.
- Father of three; community volunteer.

**Christian Conservative Analysis:**
- **Pro-Life:** 100% rating from CO Right to Life; sponsored defunding Planned Parenthood.
- **Religious Liberty:** Backed national RFRA expansions.
- **Education/Parental Rights:** Advocated homeschool freedoms.
- **Family Values:** Opposed gender-affirming care for minors.
- **Overall Assessment:** 9/10 - Solid conservative with medical credibility.

**Key Positions:**
- **ABORTION:** National heartbeat bill.
- **EDUCATION:** Universal school choice.
- **RELIGIOUS FREEDOM:** Protect faith-based health care refusals.
- **GUNS:** No infringements on 2A.
- **TAXES:** Eliminate federal death tax.
- **IMMIGRATION:** End catch-and-release.

**Endorsements:** Susan B. Anthony List, Heritage Foundation, GOA

**Website:** https://janakjoshi.com

**John Hickenlooper (Democrat)** - Incumbent Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Former brewpub owner and geologist.
- Denver Mayor and Colorado Governor before Senate.
- Married with adult children.

**Christian Conservative Analysis:**
- **Pro-Life:** Voted against Born-Alive Act; signed abortion expansions as gov.
- **Religious Liberty:** Supported laws conservatives see as anti-faith.
- **Education/Parental Rights:** Union ally; limited choice support.
- **Family Values:** Pro-LGBTQ legislation.
- **Overall Assessment:** 3/10 - Bipartisan facade hides anti-family record.

**Key Positions:**
- **ABORTION:** Codify Roe.
- **EDUCATION:** Public funding priority.
- **RELIGIOUS FREEDOM:** Equality Act supporter.
- **GUNS:** Red flag laws.
- **TAXES:** Raise on rich.
- **IMMIGRATION:** Amnesty path.

**Endorsements:** Planned Parenthood, Giffords

**Website:** https://hickenlooper.senate.gov

**Why It Matters:** Senate seat flips could block national pro-life advances.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** Open seat sets state agenda on abortion bans and school choice; next gov appoints judges.

**Barbara Kirkmeyer (Republican)** - State Senator

**Faith Statement:** "As a devout Christian, I believe our faith calls us to protect the unborn, defend religious liberty, and govern with biblical principles of justice and compassion."

**Background:**
- Rancher and former teacher in Weld County.
- House and Senate service; Brighton Council.
- Married with three children, seven grandchildren.

**Christian Conservative Analysis:**
- **Pro-Life:** Sponsored 22-week ban attempt.
- **Religious Liberty:** RFRA champion.
- **Education/Parental Rights:** Parental bill of rights co-author.
- **Family Values:** Opposed ERA gender language.
- **Overall Assessment:** 9/10 - Rural conservative powerhouse.

**Key Positions:**
- **ABORTION:** Heartbeat law.
- **EDUCATION:** ESA expansion.
- **RELIGIOUS FREEDOM:** Shield faith businesses.
- **GUNS:** Permitless carry defender.
- **TAXES:** TABOR enforcement.
- **IMMIGRATION:** State E-Verify.

**Endorsements:** CO Right to Life, Family Policy Alliance, NRA

**Website:** https://barbarakirkmeyer.com

**Michael Bennet (Democrat)** - U.S. Senator

**Faith Statement:** "No publicly disclosed faith statement specific to Christian values."

**Background:**
- Denver Schools Superintendent turned mayor.
- Senate since 2009; infrastructure deals.
- Married with three daughters.

**Christian Conservative Analysis:**
- **Pro-Life:** 0% rating; pro-choice throughout.
- **Religious Liberty:** Voted for contraceptive mandate.
- **Education/Parental Rights:** Opposed choice expansions.
- **Family Values:** Equality Act yes.
- **Overall Assessment:** 2/10 - Elite progressive.

**Key Positions:**
- **ABORTION:** No limits.
- **EDUCATION:** Anti-voucher.
- **RELIGIOUS FREEDOM:** Limited protections.
- **GUNS:** Assault ban.
- **TAXES:** Wealth tax.
- **IMMIGRATION:** Open borders lean.

**Endorsements:** EMILY's List, Everytown

**Website:** https://bennet.senate.gov

**Why It Matters:** Governor vetoes conservative bills; must win for pro-life gains.

### **Attorney General** - 2026-11-03

**Context:** AG sues on abortion and guns; open seat key for law enforcement alignment.

**John Kellner (Republican)** - Arapahoe Sheriff

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- 25-year law enforcement veteran.
- Sheriff since 2015; opioid task force leader.
- Married with three children.

**Christian Conservative Analysis:**
- **Pro-Life:** Supported fetal homicide laws.
- **Religious Liberty:** Protected church gatherings during COVID.
- **Education/Parental Rights:** School safety focus.
- **Family Values:** Family violence prevention.
- **Overall Assessment:** 8/10 - Tough-on-crime conservative.

**Key Positions:**
- **ABORTION:** Enforce restrictions.
- **EDUCATION:** Armed guards in schools.
- **RELIGIOUS FREEDOM:** Defend against mandates.
- **GUNS:** Sheriff non-enforcement of fed gun laws.
- **TAXES:** Oppose funding liberal AG suits.
- **IMMIGRATION:** ICE cooperation.

**Endorsements:** CO Sheriffs, FOP, CPAC

**Website:** https://sheriffkellner.com

**Jena Griswold (Democrat)** - Secretary of State

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Civil rights litigator.
- First Jewish woman SOS.
- Mother of two.

**Christian Conservative Analysis:**
- **Pro-Life:** Sued to block Trump pro-life rules.
- **Religious Liberty:** Prioritizes trans rights over faith.
- **Education/Parental Rights:** Voting access over security.
- **Family Values:** Abortion access advocate.
- **Overall Assessment:** 1/10 - Activist left.

**Key Positions:**
- **ABORTION:** Defend expansions.
- **EDUCATION:** Equity over choice.
- **RELIGIOUS FREEDOM:** Anti-discrimination priority.
- **GUNS:** Enforce controls.
- **TAXES:** Fund social justice.
- **IMMIGRATION:** Sanctuary support.

**Endorsements:** ACLU, HRC

**Website:** https://coloradosos.gov

**Why It Matters:** AG can shield or strike conservative laws.

### **Secretary of State** - 2026-11-03

**Context:** Oversees elections; reforms needed for ID and audits.

**Jessie Danielson (Democrat)** - State Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Teacher turned legislator.
- Wheat Ridge small business owner.
- Mother of two.

**Christian Conservative Analysis:**
- **Pro-Life:** Voted for abortion protections repeal.
- **Religious Liberty:** Mixed votes.
- **Education/Parental Rights:** Union-backed.
- **Family Values:** Pro-choice.
- **Overall Assessment:** 4/10 - Moderate Dem.

**Key Positions:**
- **ABORTION:** Access advocate.
- **EDUCATION:** Public funding.
- **RELIGIOUS FREEDOM:** Balanced.
- **GUNS:** Checks.
- **TAXES:** Raise for education.
- **IMMIGRATION:** Reform.

**Endorsements:** CEA, Democrats

**Website:** https://senatedanielson.com

**Why It Matters:** Ensures fair elections for conservative turnout.

### **State Treasurer** - 2026-11-03

**Context:** Manages $30B+ funds; impacts tax refunds and bonds.

**Kevin Grantham (Republican)** - County Commissioner

**Faith Statement:** "Guided by Christian faith to steward resources wisely and protect life."

**Background:**
- Rancher and former Senate leader.
- Cañon City focus on economy.
- Family man.

**Christian Conservative Analysis:**
- **Pro-Life:** 100% pro-life votes.
- **Religious Liberty:** Defended faith exemptions.
- **Education/Parental Rights:** Choice supporter.
- **Family Values:** Traditional stances.
- **Overall Assessment:** 8/10 - Fiscal hawk.

**Key Positions:**
- **ABORTION:** Ban support.
- **EDUCATION:** Vouchers.
- **RELIGIOUS FREEDOM:** Protections.
- **GUNS:** Rights defender.
- **TAXES:** Cuts and refunds.
- **IMMIGRATION:** Secure.

**Endorsements:** CO Farm Bureau, Taxpayers United

**Website:** https://kevingrantham.com

**Jeff Bridges (Democrat)** - State Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Budget chair; environmentalist.
- Local government experience.

**Christian Conservative Analysis:**
- **Pro-Life:** Pro-choice.
- **Religious Liberty:** Limited.
- **Education/Parental Rights:** Public only.
- **Family Values:** Progressive.
- **Overall Assessment:** 3/10 - Green new deal type.

**Key Positions:**
- **ABORTION:** Protected.
- **EDUCATION:** Funded publics.
- **RELIGIOUS FREEDOM:** Equality first.
- **GUNS:** Regulated.
- **TAXES:** Green investments.
- **IMMIGRATION:** Inclusive.

**Endorsements:** EDF, Labor unions

**Website:** https://leg.state.co.us

**Why It Matters:** Controls purse strings for conservative priorities.

---

## 🎯 KEY ISSUES FOR Colorado CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Enforce 22-week limit; expand pregnancy centers (100+ statewide).
- Parental consent for abortions required.
- Defund Planned Parenthood via budget.
- Recent victory: 2024 heartbeat amendment failed, but momentum builds.
- Challenges: 2024 constitutional amendment enshrined late-term.

**Progressive Position:**
- Unlimited access funded by state.
- Repeal all restrictions.
- Battles over medication abortion.

**Christian Conservative Action:**
- Join Colorado Right to Life (coloradorighttolife.org).
- Support HB24-1291 pro-life bills.
- Volunteer at crisis centers.
- Vote pro-life in all races.

### **School Choice & Parental Rights**

**Conservative Position:**
- Universal ESA program (2024 law) for 1,000+ students; expand eligibility.
- Bans on CRT/gender lessons in K-12.
- Homeschool freedom high; 10% students.
- Recent win: 2023 parental notification law.

**Progressive Position:**
- Union control; oppose choice as 'privatization'.
- DEI mandates in districts.
- Threats to homeschool oversight.

**Christian Conservative Action:**
- Run for school boards (e.g., Denver 2025).
- Support SB24-010 ESA expansion.
- Join Parents Defending Education CO chapter.
- Attend board meetings.

### **Religious Freedom**

**Conservative Position:**
- State RFRA (2000) protects faith actions.
- Exemptions for adoptions, cakes.
- Recent: Blocked COVID church closures.

**Progressive Position:**
- Nondiscrimination laws override.
- Attacks on faith health refusals.
- Trans bathroom mandates.

**Christian Conservative Action:**
- Partner with Alliance Defending Freedom CO.
- Oppose HB24-1039 equality bill.
- Host liberty forums in churches.
- Donate to First Liberty cases.

### **Guns**

**Conservative Position:**
- Permitless carry (2023); constitutional carry.
- Preemption over local bans.
- Recent: Red flag law weakened.

**Progressive Position:**
- Assault ban pushes in Denver.
- Magazine limits challenged.
- Universal checks enforced.

**Christian Conservative Action:**
- Join Rocky Mountain Gun Owners.
- Support HB24-1355 protections.
- Train church security teams.
- Vote NRA-endorsed.

### **Taxes**

**Conservative Position:**
- TABOR refunds $2B+ annually.
- Flat tax proposals.
- No new income tax on Social Security.

**Progressive Position:**
- Override TABOR via Prop HH.
- Corporate tax hikes.
- Spending on social programs.

**Christian Conservative Action:**
- Advocate TABOR via Americans for Prosperity CO.
- Oppose tax increases in legislature.
- Demand audits of wasteful spending.
- Use iVoterGuide for fiscal conservatives.

### **Immigration**

**Conservative Position:**
- E-Verify for state contractors.
- Oppose sanctuary cities.
- Border security funding.

**Progressive Position:**
- Driver's licenses for undocumented.
- Oppose ICE cooperation.
- Path to status.

**Christian Conservative Action:**
- Support Federation for American Immigration Reform.
- Back SB24-184 enforcement.
- Community border prayer vigils.
- Educate on biblical justice vs. open borders.

### **Family Values**

**Conservative Position:**
- Traditional marriage amendment push.
- Ban on minor transitions (2023 law).
- Parental rights in medical decisions.

**Progressive Position:**
- Gender ideology curriculum.
- Erase parental consent.
- Trans athlete inclusion.

**Christian Conservative Action:**
- Engage Colorado Family Institute (coloradofamily.org).
- Oppose HB24-1039.
- Family policy workshops in churches.
- Promote biblical marriage teachings.

### **Election Integrity**

**Conservative Position:**
- Voter ID (2023 law).
- Same-day registration limits.
- Audits mandatory.

**Progressive Position:**
- All-mail default.
- No ID requirements.
- Automatic registration.

**Christian Conservative Action:**
- Become poll watchers via Election Integrity Project CO.
- Support SB24-180 reforms.
- Voter registration drives with guides.
- Pray against fraud.

---

## 📅 CRITICAL DATES

**2025-2026 Election Calendar:**
- 2025-10-28 - Voter registration deadline (2025)
- 2025-10-21 - Early voting begins (2025)
- 2025-11-04 - Coordinated Election
- 2026-05-26 - Voter registration deadline (primaries)
- 2026-06-02 - Early voting begins (primaries)
- 2026-06-30 - Primary Election
- 2026-10-27 - Voter registration deadline (general)
- 2026-10-20 - Early voting begins (general)
- 2026-11-03 - General Election

**Voter Registration:** govotecolorado.gov

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
✅ **Share on social media** with #COFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Colorado CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Colorado coverage
- **Colorado Right to Life** - Pro-life ratings
- **Colorado Family Institute** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Colorado Secretary of State**: coloradosos.gov
- **County Election Offices**: Find via sos.state.co.us
- **Early Voting Locations**: Voter service centers listed on county sites

### **Conservative Organizations:**
- **Colorado Right to Life**: coloradorighttolife.org
- **Colorado Family Institute**: coloradofamily.org
- **Rocky Mountain Gun Owners**: rmgo.org
- **Parents Defending Education CO**: defenseducation.org
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Colorado CHRISTIANS

**2026 Elections Matter:**
- U.S. Senate determines federal judges for life issues.
- Governor race affects state abortion laws.
- AG impacts gun and family protections.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ TABOR refunds grow
✅ Rural economies boosted
✅ Border security enhanced

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Taxes hiked, TABOR gutted
❌ Urban policies dominate rural
❌ Sanctuary state status

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Barbara Kirkmeyer, Janak Joshi, John Kellner, Kevin Grantham and their families
- Colorado Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Colorado
- Revival and awakening in Colorado
- God's will in Colorado elections

**Scripture for Colorado Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Colorado coverage, email contact@ekewaka.com

**COLORADO CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Colorado races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Colorado'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Colorado races...")
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

print(f"\nChecking for existing Colorado candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Colorado'}
)['Items']
existing_candidate_map = {(c['name'], c['office']): c['candidate_id'] for c in existing_candidates}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Colorado candidates...")
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

print("\nProcessing Colorado summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Colorado'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Colorado data upload complete!")