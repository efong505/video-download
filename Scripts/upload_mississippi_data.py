import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Mississippi Races
races = [
    {
        "state": "Mississippi",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Mississippi's Class 2 U.S. Senate seat, currently held by incumbent Cindy Hyde-Smith (R). This race is pivotal for maintaining conservative control in the Senate and advancing pro-life, Second Amendment, and religious liberty priorities."
    },
    {
        "state": "Mississippi",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Northern Mississippi district held by incumbent Trent Kelly (R). Key for conservative representation in agriculture-heavy region."
    },
    {
        "state": "Mississippi",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Delta and Jackson district held by incumbent Bennie Thompson (D). Opportunity for conservatives to flip with strong grassroots effort."
    },
    {
        "state": "Mississippi",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Central Mississippi district held by incumbent Michael Guest (R). Solid conservative seat defending family values and election integrity."
    },
    {
        "state": "Mississippi",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Southern Gulf Coast district held by incumbent Mike Ezell (R). Focus on border security and economic growth."
    },
    {
        "state": "Mississippi",
        "office": "Jackson Mayor",
        "election_date": "2025-06-03",
        "race_type": "general",
        "description": "Mayoral race in state capital Jackson, recently won by John Horhn (D). Highlights urban challenges like crime and infrastructure for Christian conservatives."
    }
]

# Mississippi Candidates  
candidates = [
    {
        "name": "Cindy Hyde-Smith",
        "state": "Mississippi",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Cindy Hyde-Smith, born in 1959 in Brookhaven, Mississippi, is a lifelong public servant and the state's first female U.S. Senator. Raised on a cattle farm by educator parents, she graduated from Copiah-Lincoln Community College and Mississippi State University with a degree in political science. Hyde-Smith began her career as a model and actress before entering politics, serving in the Mississippi State Senate from 2000 to 2018, where she chaired the Agriculture Committee. Appointed to the U.S. Senate in 2018 by Gov. Phil Bryant to replace Thad Cochran, she won a special election that year and a full term in 2020. As Commissioner of Agriculture from 2011-2018, she promoted Mississippi's farming industry, earning praise for disaster relief efforts post-tornadoes. Married to Mike Hyde-Smith, a lawyer, they have one daughter, Perry, and are active members of their Baptist church. Hyde-Smith's accomplishments include authoring the FARM Act to protect family farms and leading on pro-life legislation. Currently, she serves on the Agriculture, Nutrition, and Forestry Committee and the Appropriations Committee, fighting for rural broadband and conservative values. Her farm roots inform her commitment to Second Amendment rights and low taxes, making her a steadfast voice for Mississippi's conservative heartland.",
        "faith_statement": "As a Christian, Senator Hyde-Smith believes in the sanctity of life and the need for federal policies that strengthen America's families.",
        "website": "https://www.hydesmith.senate.gov",
        "positions": {
            "ABORTION": "Strongly pro-life; co-sponsored the Heartbeat Protection Act banning abortions after 6 weeks; opposes taxpayer funding for Planned Parenthood; supported overturning Roe v. Wade and Mississippi's 15-week ban upheld by SCOTUS.",
            "EDUCATION": "Supports school choice and parental rights; backed Education Freedom Scholarships for low-income families to access private or homeschool options; opposes federal overreach in curricula.",
            "RELIGIOUS-FREEDOM": "Defends religious liberty; co-sponsored the Religious Freedom Restoration Act enhancements; fought IRS bias against Christian groups like Christians Engaged.",
            "GUNS": "A-rated by NRA; staunch 2nd Amendment defender; opposed red-flag laws and universal background checks that infringe on law-abiding citizens.",
            "TAXES": "Advocates permanent TCJA tax cuts; fights for no tax on tips and overtime; supports balanced budgets to reduce federal spending.",
            "IMMIGRATION": "Secure borders first; co-sponsored bill requiring DNA tests for family asylum claims; backs wall funding and E-Verify mandates.",
            "FAMILY-VALUES": "Promotes traditional marriage and parental rights; opposes gender ideology in schools; supports family tax credits and adoption incentives.",
            "ELECTION-INTEGRITY": "Supports Voter ID nationwide; co-sponsored SAVE Act for proof of citizenship; combats mail-in fraud with signature verification."
        },
        "endorsements": ["National Right to Life", "NRA", "Family Research Council"]
    },
    {
        "name": "Scott Colom",
        "state": "Mississippi",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Scott Colom, born in 1985 in Columbus, Mississippi, is a civil rights advocate and the first Black district attorney for Mississippi's 16th Circuit. Son of civil rights attorney Derrick Colom, he grew up immersed in justice work, witnessing his father's defense of marginalized communities. Colom earned a bachelor's from Harvard University and a law degree from Yale, where he was editor of the Yale Law Journal. Returning to Mississippi, he worked as a public defender before winning election as DA in 2015, focusing on restorative justice over mass incarceration. In 2023, President Biden nominated him for federal judgeship, blocked by Sen. Hyde-Smith. Married to attorney LaKoshia Roberts, they have three children and reside in Columbus. Colom's accomplishments include prosecuting violent crimes while reforming juvenile justice and expanding victim services. As DA, he launched community programs reducing recidivism by 20%. Now running for Senate, he aims to address economic inequality, healthcare access, and criminal justice reform, drawing on his prosecutorial experience to bridge divides in a red state.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://scottcolom.com",
        "positions": {
            "ABORTION": "Pro-choice; supports restoring Roe v. Wade protections; opposes state bans like Mississippi's 15-week law as infringing on women's rights.",
            "EDUCATION": "Invest in public schools; opposes vouchers diverting funds from under-resourced districts; supports teacher pay raises and universal pre-K.",
            "RELIGIOUS-FREEDOM": "Protects all faiths equally; opposes using religion to discriminate against LGBTQ+; supports separation of church and state.",
            "GUNS": "Common-sense reforms; background checks and red-flag laws; opposes assault weapons bans but supports closing gun show loopholes.",
            "TAXES": "Raise minimum wage to $15; tax cuts for working families; close corporate loopholes to fund social programs.",
            "IMMIGRATION": "Path to citizenship for Dreamers; comprehensive reform with border security; opposes family separations.",
            "FAMILY-VALUES": "Inclusive families; supports LGBTQ+ rights and paid family leave; parental involvement in education decisions.",
            "ELECTION-INTEGRITY": "Expand access; automatic voter registration; opposes strict ID laws as suppressive."
        },
        "endorsements": ["Sierra Club", "Planned Parenthood", "Everytown for Gun Safety"]
    },
    {
        "name": "Ty Pinkins",
        "state": "Mississippi",
        "office": "U.S. Senate",
        "party": "Independent",
        "bio": "Ty Pinkins, born in Vicksburg, Mississippi, is a U.S. Army veteran and civil rights attorney challenging the two-party system. After 21 years in the Army, including three combat tours in Iraq earning a Bronze Star, he transitioned to law, earning degrees from Howard University and the University of Mississippi. Pinkins practiced corporate law before founding his firm, focusing on economic justice. Married with children, he emphasizes family stability amid Mississippi's poverty. Unsuccessful Democratic runs for Senate in 2024 and Secretary of State in 2023 led him to run independent in 2026, citing party 'gatekeepers.' His accomplishments include advocating for voting rights and small business loans for minorities. Pinkins' campaign targets rural economic revival, healthcare expansion, and criminal justice reform, positioning himself as a pragmatic outsider.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.typinkins.com",
        "positions": {
            "ABORTION": "Pro-choice with limits; supports access post-Roe; focuses on maternal health in underserved areas.",
            "EDUCATION": "Equal funding for public schools; opposes privatization; vocational training emphasis.",
            "RELIGIOUS-FREEDOM": "Broad protections; against theocracy; inclusive policies.",
            "GUNS": "Reasonable regulations; mental health checks; veteran support for gun owners.",
            "TAXES": "Fair taxation; relief for low-income; corporate accountability.",
            "IMMIGRATION": "Humane reform; work visas for economy; secure but fair borders.",
            "FAMILY-VALUES": "Support all families; economic policies for stability; anti-poverty focus.",
            "ELECTION-INTEGRITY": "Secure and accessible; ranked-choice voting; anti-corruption."
        },
        "endorsements": ["Veterans for Peace", "NAACP"]
    },
    {
        "name": "Trent Kelly",
        "state": "Mississippi",
        "office": "U.S. House District 1",
        "party": "Republican",
        "bio": "Trent Kelly, born in 1966 in Saltillo, Mississippi, is a retired Army National Guard Colonel and U.S. Congressman since 2015. A fifth-generation Mississippian, he graduated from University of Mississippi with degrees in history and law. Kelly served as District Attorney for 1st Judicial District (2004-2012) before a special election win for Congress. Deployed to Iraq as JAG officer, he earned Bronze Star. Married to Sheena Kelly, a teacher, they have two children and attend First Baptist Church. Kelly's career highlights include prosecuting child predators and authoring the Amy, Vicky, and Andy Child Pornography Victim Assistance Act. In Congress, he chairs Seapower Subcommittee, securing $1B+ for military bases. A conservative stalwart, he fights for rural broadband, farm subsidies, and pro-life policies.",
        "faith_statement": "As a devout United Methodist, Rep. Kelly draws strength from his faith in serving constituents and defending biblical values in policy.",
        "website": "https://trentkelly.house.gov",
        "positions": {
            "ABORTION": "Pro-life; 100% SBA rating; supports defunding Planned Parenthood.",
            "EDUCATION": "School choice advocate; parental rights in curriculum.",
            "RELIGIOUS-FREEDOM": "Protects faith-based organizations; opposes anti-discrimination mandates on religious entities.",
            "GUNS": "NRA A-rated; blocks gun control expansions.",
            "TAXES": "Permanent tax cuts; fiscal conservatism.",
            "IMMIGRATION": "Border wall supporter; end catch-and-release.",
            "FAMILY-VALUES": "Traditional marriage; anti-trafficking laws.",
            "ELECTION-INTEGRITY": "Voter ID; audit requirements."
        },
        "endorsements": ["NRA", "National Right to Life", "American Farm Bureau"]
    },
    {
        "name": "Cliff Johnson",
        "state": "Mississippi",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "bio": "Cliff Johnson, a fifth-generation Mississippian born in 1960s, is Director of the MacArthur Justice Center at Ole Miss School of Law. Raised in rural Mississippi, he graduated from Mississippi College and Columbia Law. Johnson's career spans civil rights litigation, representing death row inmates and police misconduct victims. Married with children, he teaches future lawyers while advocating for economic justice. Announced 2026 run focusing on healthcare, Social Security, and environmental protection. Accomplishments include securing exonerations and reforms in solitary confinement bans.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://cliffjohnsonforcongress.com",
        "positions": {
            "ABORTION": "Pro-choice; reproductive rights access.",
            "EDUCATION": "Fully fund public schools; oppose vouchers.",
            "RELIGIOUS-FREEDOM": "Inclusive protections; against faith-based discrimination.",
            "GUNS": "Universal background checks; assault weapon limits.",
            "TAXES": "Wealth tax on ultra-rich; middle-class relief.",
            "IMMIGRATION": "Pathway for undocumented; humane enforcement.",
            "FAMILY-VALUES": "LGBTQ+ inclusion; family leave.",
            "ELECTION-INTEGRITY": "Voter expansion; end gerrymandering."
        },
        "endorsements": ["ACLU", "Sierra Club"]
    },
    {
        "name": "Bennie Thompson",
        "state": "Mississippi",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "bio": "Bennie Thompson, born 1951 in Bolton, MS, has represented District 2 since 1993. A Hinds Community College grad, he taught school before politics. Married to Sheila, two children. Longtime chair of Homeland Security Committee. Focuses on infrastructure and disaster relief for Delta.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://benniethompson.house.gov",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Public school funding.",
            "RELIGIOUS-FREEDOM": "Separation of church and state.",
            "GUNS": "Gun safety measures.",
            "TAXES": "Progressive taxation.",
            "IMMIGRATION": "Reform with citizenship.",
            "FAMILY-VALUES": "Inclusive policies.",
            "ELECTION-INTEGRITY": "Voting rights expansion."
        },
        "endorsements": ["AFL-CIO", "NAACP"]
    },
    {
        "name": "Michael Guest",
        "state": "Mississippi",
        "office": "U.S. House District 3",
        "party": "Republican",
        "bio": "Michael Guest, born 1976, is former DA now Congressman since 2019. University of MS law grad. Married, three kids. Chairs Ethics Committee. Pro-life leader.",
        "faith_statement": "Deeply rooted in Christian faith guiding service.",
        "website": "https://guest.house.gov",
        "positions": {
            "ABORTION": "Pro-life absolutist.",
            "EDUCATION": "School choice.",
            "RELIGIOUS-FREEDOM": "Strong defender.",
            "GUNS": "2A protector.",
            "TAXES": "Cut taxes.",
            "IMMIGRATION": "Secure borders.",
            "FAMILY-VALUES": "Traditional values.",
            "ELECTION-INTEGRITY": "Voter ID."
        },
        "endorsements": ["FRC", "NRA"]
    },
    {
        "name": "Michael Chiaradio",
        "state": "Mississippi",
        "office": "U.S. House District 3",
        "party": "Democrat",
        "bio": "Michael Chiaradio, political newcomer, focuses on economic equity. Background in community organizing.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Public investment.",
            "RELIGIOUS-FREEDOM": "Inclusive.",
            "GUNS": "Reforms.",
            "TAXES": "Fair share.",
            "IMMIGRATION": "Reform.",
            "FAMILY-VALUES": "Supportive.",
            "ELECTION-INTEGRITY": "Access."
        },
        "endorsements": ["Democrats"]
    },
    {
        "name": "Mike Ezell",
        "state": "Mississippi",
        "office": "U.S. House District 4",
        "party": "Republican",
        "bio": "Mike Ezell, born 1959, former sheriff now Congressman since 2023. MS State grad. Married, kids. Law enforcement background.",
        "faith_statement": "Faith-driven public servant.",
        "website": "https://ezell.house.gov",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Choice.",
            "RELIGIOUS-FREEDOM": "Protector.",
            "GUNS": "Pro-2A.",
            "TAXES": "Low taxes.",
            "IMMIGRATION": "Border security.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "Secure elections."
        },
        "endorsements": ["NRA", "Police groups"]
    },
    {
        "name": "Paul James Blackman",
        "state": "Mississippi",
        "office": "U.S. House District 4",
        "party": "Democrat",
        "bio": "Paul Blackman, Navy veteran, newcomer advocating veterans' issues and coastal economy.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Public schools.",
            "RELIGIOUS-FREEDOM": "Balanced.",
            "GUNS": "Veteran-focused reforms.",
            "TAXES": "Middle-class cuts.",
            "IMMIGRATION": "Veteran pathways.",
            "FAMILY-VALUES": "Military families.",
            "ELECTION-INTEGRITY": "Fair access."
        },
        "endorsements": ["Veterans groups"]
    },
    {
        "name": "John Horhn",
        "state": "Mississippi",
        "office": "Jackson Mayor",
        "party": "Democrat",
        "bio": "John Horhn, born 1953, state senator since 1988, won 2025 mayoral race. Tougaloo College and Jackson State grad. Longtime advocate for Jackson revitalization.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://johnhorhn.com",
        "positions": {
            "ABORTION": "Pro-choice.",
            "EDUCATION": "Urban public schools.",
            "RELIGIOUS-FREEDOM": "City protections.",
            "GUNS": "Crime reduction measures.",
            "TAXES": "Local revenue.",
            "IMMIGRATION": "Inclusive city.",
            "FAMILY-VALUES": "Community support.",
            "ELECTION-INTEGRITY": "Local voting."
        },
        "endorsements": ["Local unions"]
    }
]

# Mississippi Summary
summary = {
    "state": "Mississippi",
    "title": "Mississippi 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Mississippi 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 6
**Total Candidates Profiled:** 11
**Election Dates:**
- 2025-06-03 (Municipal General)
- 2026-03-10 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Mississippi POLITICAL LANDSCAPE

### **The Magnolia State**

Mississippi is a **deep-red conservative stronghold**:
- **Evangelical Heartland:** Over 80% Christian, with strong Baptist and Pentecostal influences driving pro-life and family values policies.
- **Rural Dominance:** Agriculture and faith-based communities shape GOP supermajorities in legislature.
- **Urban-Rural Divide:** Jackson (Hinds County) leans Democratic (60% Black population), while rural counties like Rankin and DeSoto are 70%+ Republican.
- **Bible Belt Legacy:** Historical religious revivals fuel ongoing cultural conservatism.

### **Why Mississippi Matters**

Mississippi is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** 15-week abortion ban (Jackson Women's Health Org. v. Dobbs upheld by SCOTUS); no exceptions for rape/incest; 40+ pregnancy centers funded statewide.
- ✅ **Second Amendment:** Permitless carry since 2016; top-5 gun ownership; minimal restrictions.
- ✅ **School Choice:** Expanding Education Scholarship Accounts (ESA) for 2025; $10M+ for private/homeschool; bans on CRT/gender ideology.
- ✅ **Religious Liberty:** 2014 Protecting Freedom of Conscience Act shields faith-based adoptions; strong RFRA protections.
- ✅ **Family Values:** Traditional marriage amendment; parental consent for minors' abortions; anti-grooming laws.
- ✅ **Election Integrity:** Strict Voter ID; paper ballots; post-2020 audits.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** Controls national conservative agenda; Mississippi's seat vital for 51 GOP votes; impacts judiciary confirmations for life issues.

**Cindy Hyde-Smith (Republican)** - Incumbent U.S. Senator

**Faith Statement:** "As a Christian, Senator Hyde-Smith believes in the sanctity of life and the need for federal policies that strengthen America's families."

**Background:**
- Brookhaven farm girl; first female MS Senator.
- State Senate/Agriculture Commissioner; won 2018 special.
- Married, one daughter; Baptist church active.

**Christian Conservative Analysis:**
- **Pro-Life:** 100% NRLC rating; led MS heartbeat bill to SCOTUS victory.
- **Religious Liberty:** Blocked IRS targeting Christians; RFRA supporter.
- **Education/Parental Rights:** ESA expansion; anti-woke curricula.
- **Family Values:** Traditional marriage defender; adoption incentives.
- **Overall Assessment:** 9/10 - Battle-tested MAGA ally, Trump-endorsed.

**Key Positions:**
- **ABORTION:** Bans post-6 weeks; defund Planned Parenthood.
- **EDUCATION:** Vouchers for faith schools; parental opt-outs.
- **RELIGIOUS FREEDOM:** Protect chaplains, faith exemptions.
- **GUNS:** NRA A+; no red flags.
- **TAXES:** Permanent cuts; no tax on Social Security.
- **BORDER SECURITY:** Wall, DNA family tests.

**Endorsements:** National Right to Life, NRA, Family Research Council

**Website:** https://www.hydesmith.senate.gov

**Scott Colom (Democrat)** - District Attorney

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Columbus native; first Black DA in district.
- Harvard/Yale educated; Biden judicial nominee.
- Married, three kids; civil rights family legacy.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports abortion expansion; opposes bans.
- **Religious Liberty:** Neutral; focuses secular equality.
- **Education/Parental Rights:** Public funding only; anti-voucher.
- **Family Values:** Inclusive; LGBTQ+ protections.
- **Overall Assessment:** 2/10 - Progressive agenda erodes biblical principles.

**Key Positions:**
- **ABORTION:** Restore Roe; access for all.
- **EDUCATION:** Teacher raises; no privatization.
- **RELIGIOUS FREEDOM:** Anti-discrimination laws.
- **GUNS:** Background checks.
- **TAXES:** Raise corporate rates.
- **BORDER SECURITY:** Citizenship paths.

**Endorsements:** Planned Parenthood, Everytown

**Website:** https://scottcolom.com

**Ty Pinkins (Independent)** - Army Veteran Attorney

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Vicksburg lawyer; 21-year Army service, Bronze Star.
- 2024 Senate run; economic justice focus.
- Married, children; outsider reformer.

**Christian Conservative Analysis:**
- **Pro-Life:** Limited access; health-focused.
- **Religious Liberty:** Broad but secular.
- **Education/Parental Rights:** Public equity.
- **Family Values:** Economic support.
- **Overall Assessment:** 3/10 - Pragmatic but left-leaning.

**Key Positions:**
- **ABORTION:** With limits; maternal care.
- **EDUCATION:** Vocational public.
- **RELIGIOUS FREEDOM:** Inclusive.
- **GUNS:** Mental health checks.
- **TAXES:** Fair relief.
- **BORDER SECURITY:** Work visas.

**Endorsements:** NAACP, Veterans for Peace

**Website:** https://www.typinkins.com

**Why It Matters:** Retaining this seat ensures pro-life judges and border security.

### **U.S. House District 1** - 2026-11-03

**Context:** Rural north MS; agriculture, military bases; flip risk low but turnout key.

**Trent Kelly (Republican)** - Incumbent Congressman

**Faith Statement:** "As a devout United Methodist, Rep. Kelly draws strength from his faith in serving constituents and defending biblical values in policy."

**Background:**
- Saltillo native; Army Colonel, Bronze Star.
- Former DA; since 2015 special election.
- Married, two kids; church leader.

**Christian Conservative Analysis:**
- **Pro-Life:** 100% pro-life votes.
- **Religious Liberty:** Faith protections.
- **Education/Parental Rights:** Choice supporter.
- **Family Values:** Anti-trafficking.
- **Overall Assessment:** 8/10 - Solid defender.

**Key Positions:**
- **ABORTION:** Defund abortions.
- **EDUCATION:** Parental rights.
- **RELIGIOUS FREEDOM:** Exemptions.
- **GUNS:** A-rated NRA.
- **TAXES:** Cuts.
- **BORDER SECURITY:** Wall.

**Endorsements:** NRA, Farm Bureau

**Website:** https://trentkelly.house.gov

**Cliff Johnson (Democrat)** - Ole Miss Professor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Civil rights lawyer; MacArthur Center director.
- Columbia Law; exonerations expert.
- Family man; public servant.

**Christian Conservative Analysis:**
- **Pro-Life:** Pro-choice.
- **Religious Liberty:** Secular.
- **Education/Parental Rights:** Public only.
- **Family Values:** Inclusive.
- **Overall Assessment:** 1/10 - Woke activist.

**Key Positions:**
- **ABORTION:** Rights access.
- **EDUCATION:** Fund publics.
- **RELIGIOUS FREEDOM:** No favoritism.
- **GUNS:** Checks.
- **TAXES:** Wealth tax.
- **BORDER SECURITY:** Reform.

**Endorsements:** ACLU

**Website:** https://cliffjohnsonforcongress.com

**Why It Matters:** Protects farm families from liberal overreach.

### **U.S. House District 2** - 2026-11-03

**Context:** Poorest district; Delta poverty; potential conservative surge with mobilization.

**Bennie Thompson (Democrat)** - Incumbent Congressman

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Bolton teacher; since 1993.
- Homeland Security chair.
- Married, family.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports choice.
- **Religious Liberty:** Neutral.
- **Education/Parental Rights:** Public focus.
- **Family Values:** Broad.
- **Overall Assessment:** 2/10 - Longtime liberal.

**Key Positions:**
- **ABORTION:** Pro-choice.
- **EDUCATION:** Funding.
- **RELIGIOUS FREEDOM:** Separation.
- **GUNS:** Safety.
- **TAXES:** Progressive.
- **BORDER SECURITY:** Reform.

**Endorsements:** NAACP

**Website:** https://benniethompson.house.gov

**Why It Matters:** Flipping ends Delta neglect.

### **U.S. House District 3** - 2026-11-03

**Context:** Central MS; growing suburbs; safe GOP but watch turnout.

**Michael Guest (Republican)** - Incumbent Congressman

**Faith Statement:** "Deeply rooted in Christian faith guiding service."

**Background:**
- Former DA; since 2019.
- Ethics chair.
- Family man.

**Christian Conservative Analysis:**
- **Pro-Life:** Strong record.
- **Religious Liberty:** Defender.
- **Education/Parental Rights:** Choice.
- **Family Values:** Traditional.
- **Overall Assessment:** 9/10 - Integrity leader.

**Key Positions:**
- **ABORTION:** Bans.
- **EDUCATION:** Vouchers.
- **RELIGIOUS FREEDOM:** Protections.
- **GUNS:** 2A.
- **TAXES:** Cuts.
- **BORDER SECURITY:** Secure.

**Endorsements:** FRC

**Website:** https://guest.house.gov

**Michael Chiaradio (Democrat)** - Activist

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Community organizer.

**Christian Conservative Analysis:**
- **Pro-Life:** Choice.
- **Religious Liberty:** Inclusive.
- **Education/Parental Rights:** Public.
- **Family Values:** Modern.
- **Overall Assessment:** 1/10 - Progressive.

**Key Positions:**
- **ABORTION:** Access.
- **EDUCATION:** Equity.
- **RELIGIOUS FREEDOM:** Balanced.
- **GUNS:** Control.
- **TAXES:** Raise rich.
- **BORDER SECURITY:** Humane.

**Endorsements:** Progressives

**Website:** ""

**Why It Matters:** Maintains central conservative voice.

### **U.S. House District 4** - 2026-11-03

**Context:** Gulf Coast; hurricanes, ports; border proximity.

**Mike Ezell (Republican)** - Incumbent Congressman

**Faith Statement:** "Faith-driven public servant."

**Background:**
- Former sheriff; since 2023.
- Law enforcement hero.

**Christian Conservative Analysis:**
- **Pro-Life:** Committed.
- **Religious Liberty:** Supporter.
- **Education/Parental Rights:** Choice.
- **Family Values:** Strong.
- **Overall Assessment:** 8/10 - Tough on crime.

**Key Positions:**
- **ABORTION:** Pro-life.
- **EDUCATION:** Parental.
- **RELIGIOUS FREEDOM:** Faith free.
- **GUNS:** Pro-carry.
- **TAXES:** Low.
- **BORDER SECURITY:** Enforcement.

**Endorsements:** NRA

**Website:** https://ezell.house.gov

**Paul James Blackman (Democrat)** - Navy Veteran

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Veteran advocate.

**Christian Conservative Analysis:**
- **Pro-Life:** Choice.
- **Religious Liberty:** Veteran focus.
- **Education/Parental Rights:** Public.
- **Family Values:** Military.
- **Overall Assessment:** 3/10 - Moderate Dem.

**Key Positions:**
- **ABORTION:** Rights.
- **EDUCATION:** Funding.
- **RELIGIOUS FREEDOM:** Inclusive.
- **GUNS:** Veteran checks.
- **TAXES:** Relief.
- **BORDER SECURITY:** Pathways.

**Endorsements:** VFW

**Website:** ""

**Why It Matters:** Secures southern borders.

### **Jackson Mayor** - 2025-06-03

**Context:** Capital city crisis; crime, water; won by Horhn (D); lessons for urban outreach.

**John Horhn (Democrat)** - Mayor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- State senator 30+ years.
- Revitalization focus.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports access.
- **Religious Liberty:** City neutral.
- **Education/Parental Rights:** Urban public.
- **Family Values:** Community.
- **Overall Assessment:** 2/10 - Liberal urban.

**Key Positions:**
- **ABORTION:** Pro-choice.
- **EDUCATION:** Local funding.
- **RELIGIOUS FREEDOM:** Inclusive.
- **GUNS:** Crime control.
- **TAXES:** Revenue.
- **BORDER SECURITY:** N/A.

**Endorsements:** Unions

**Website:** https://johnhorhn.com

**Why It Matters:** Urban strongholds test conservative messaging.

---

## 🎯 KEY ISSUES FOR Mississippi CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- 15-week ban; trigger law post-Roe for total ban.
- 50+ pregnancy centers; $5M state funding.
- Parental consent required.
- Defund abortions in Medicaid.
- 2024 victories: Ultrasound mandates.

**Progressive Position:**
- Challenge bans via courts.
- Expand access via clinics.
- Fund abortions publicly.
- Remove consent laws.

**Christian Conservative Action:**
- Join MS Right to Life (msrighttolife.com).
- Support HB 1499 trigger law.
- Volunteer at centers.
- Vote pro-life in all races.

### **School Choice & Parental Rights**

**Conservative Position:**
- ESA program for 5K students; $7K grants.
- 2024 bans on CRT, gender transitions.
- Homeschool freedom; no reporting.
- Literacy-based promotion wins.

**Progressive Position:**
- Union control; oppose vouchers.
- DEI mandates.
- Threaten choice funds.

**Christian Conservative Action:**
- Run for school boards.
- Back SB 2799 expansion.
- Join Parents Defending Education.

### **Religious Freedom**

**Conservative Position:**
- 2014 Conscience Act; faith adoptions.
- School prayer protections.
- Chaplain programs.
- RFRA upheld.

**Progressive Position:**
- Anti-discrimination suits.
- Remove chaplains.
- Secular curricula.

**Christian Conservative Action:**
- Support ADF (adflegal.org).
- Lobby for expansions.
- Church forums.

### **Guns**

**Conservative Position:**
- Permitless carry; stand-your-ground.
- No assault bans.
- Preemption laws.

**Progressive Position:**
- Red flags; mag limits.
- Waiting periods.

**Christian Conservative Action:**
- NRA training.
- Oppose HB 1355 controls.
- 2A rallies.

### **Taxes**

**Conservative Position:**
- No income tax; low property.
- Grocery tax cut 2022.
- Balanced budget.

**Progressive Position:**
- Wealth taxes; corporate hikes.

**Christian Conservative Action:**
- Support ALEC models.
- Vote fiscal hawks.

### **Immigration**

**Conservative Position:**
- E-Verify; sanctuary bans.
- Border aid.

**Progressive Position:**
- Sanctuary cities.
- DACA expansion.

**Christian Conservative Action:**
- FAIR advocacy.
- Local enforcement.

### **Family Values**

**Conservative Position:**
- Traditional marriage.
- Anti-porn libraries.
- Parental notification.

**Progressive Position:**
- Gender affirmation.
- Drag shows.

**Christian Conservative Action:**
- FRC Action.
- School board runs.

### **Election Integrity**

**Conservative Position:**
- Voter ID; audits.
- Paper ballots.

**Progressive Position:**
- Mail-in expansion.
- No ID.

**Christian Conservative Action:**
- Poll watching.
- iVoterGuide use.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- 2026-02-06 - Voter registration deadline (Primary)
- 2026-02-24 - Early voting begins (Primary)
- 2026-03-10 - Primary Election
- 2026-10-04 - Voter registration deadline (General)
- 2026-10-20 - Early voting begins (General)
- 2026-11-03 - General Election

**Voter Registration:** https://www.sos.ms.gov/elections-voting/pages/register-to-vote.aspx

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
✅ **Share on social media** with #MSFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Mississippi CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - MS coverage
- **Mississippi Right to Life** - Pro-life ratings
- **American Family Association** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Mississippi Secretary of State**: https://www.sos.ms.gov
- **County Election Offices**: Search via sos.ms.gov
- **Early Voting Locations**: County clerk offices

### **Conservative Organizations:**
- **Mississippi Right to Life**: https://msrighttolife.com
- **Family Research Council Action**: https://frcaction.org
- **Mississippi NRA**: https://www.nraila.org
- **Mississippi ESA Coalition**: https://esams.org
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Mississippi CHRISTIANS

**2026 Elections Matter:**
- U.S. Senate determines pro-life judges.
- House races affect border funding.
- District 2 flip impacts Delta families.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Rural economy boosted
✅ Faith centers funded
✅ Biblical governance advanced

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Urban crime surges
❌ Tax hikes burden families
❌ Secular agenda dominates

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Cindy Hyde-Smith and her family
- Mississippi Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Mississippi
- Revival and awakening in Mississippi
- God's will in Mississippi elections

**Scripture for Mississippi Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Mississippi coverage, email contact@ekewaka.com

**MISSISSIPPI CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Mississippi races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Mississippi'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Mississippi races...")
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

print(f"\nChecking for existing Mississippi candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Mississippi'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Mississippi candidates...")
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

print("\nProcessing Mississippi summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Mississippi'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Mississippi data upload complete!")