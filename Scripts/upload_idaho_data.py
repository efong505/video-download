import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Idaho Races
races = [
    {
        "state": "Idaho",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for the Class II U.S. Senate seat currently held by Republican Jim Risch, critical for maintaining conservative control in the Senate."
    },
    {
        "state": "Idaho",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Idaho's 1st Congressional District, represented by Republican Russ Fulcher, focusing on rural northern and western Idaho issues."
    },
    {
        "state": "Idaho",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Idaho's 2nd Congressional District, represented by Republican Mike Simpson, covering southern Idaho including Boise."
    },
    {
        "state": "Idaho",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Gubernatorial race with incumbent Republican Brad Little seeking re-election, pivotal for state policies on education, taxes, and family values."
    },
    {
        "state": "Idaho",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Lieutenant Governor, currently held by Republican Scott Bedke, influencing legislative priorities and succession."
    },
    {
        "state": "Idaho",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Race for Attorney General, led by Republican Raúl Labrador, key for defending state laws on immigration and religious freedom."
    },
    {
        "state": "Idaho",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Secretary of State, held by Republican Phil McGrane, crucial for election integrity and business regulations."
    },
    {
        "state": "Idaho",
        "office": "State Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Race for State Treasurer, managed by Republican Julie Ellsworth, overseeing state finances and investments."
    },
    {
        "state": "Idaho",
        "office": "Superintendent of Public Instruction",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for Superintendent of Public Instruction, led by Republican Debra Schroeder, shaping education policy and school choice."
    },
    {
        "state": "Idaho",
        "office": "Mayor of Idaho Falls",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Municipal race for mayor of Idaho Falls, a key eastern Idaho city, impacting local growth and community services."
    }
]

# Idaho Candidates  
candidates = [
    {
        "name": "Brad Little",
        "state": "Idaho",
        "office": "Governor",
        "party": "Republican",
        "bio": "Brad Little, born in 1954 in Emmett, Idaho, is a fourth-generation Idahoan and lifelong rancher. He graduated from the University of Idaho with a degree in agricultural economics and served in the Idaho Army National Guard. Little entered politics as a state senator from 2005 to 2009, then as Lieutenant Governor from 2009 to 2019 under Gov. Butch Otter. He became Idaho's 33rd Governor in January 2019 after Otter's retirement. As governor, Little has championed economic recovery post-COVID, signed strict abortion bans, and defended Second Amendment rights. He and his wife, Terri, have three children and six grandchildren, residing on their family ranch in Emmett. Little's accomplishments include leading Idaho to the lowest unemployment rate in the nation and expanding school choice programs.",
        "faith_statement": "As a committed Christian, Governor Little has publicly recognized the Christian heritage of America and Idaho, proclaiming weeks of Christian heritage and signing bills to protect religious conscience rights for medical professionals. He often invokes faith in calls for unity and prayer during crises.",
        "website": "https://gov.idaho.gov/",
        "positions": {
            "ABORTION": "Strongly pro-life; signed Idaho's near-total abortion ban post-Roe v. Wade, prohibiting abortions except in cases of rape, incest, or life-threatening conditions, and a six-week ban modeled on Texas law allowing private enforcement.",
            "EDUCATION": "Supports school choice and parental rights; expanded Idaho's Empowering Parents Grant program providing ESA funds up to $1,000 per child for private or homeschool options, and signed laws banning critical race theory and gender ideology in public schools.",
            "RELIGIOUS-FREEDOM": "Defends religious liberty; signed legislation protecting doctors and nurses from participating in procedures violating their faith, and joined multi-state suits against federal mandates infringing on religious exercise.",
            "GUNS": "Firm Second Amendment advocate; opposed federal gun control measures, signed constitutional carry expansions, and supported legislation preempting local gun restrictions to ensure statewide uniformity.",
            "TAXES": "Proposes tax cuts; enacted largest income tax reduction in Idaho history in 2022, eliminating the grocery tax, and advocates for property tax relief while maintaining fiscal conservatism with balanced budgets.",
            "IMMIGRATION": "Prioritizes border security; signed bill blocking unauthorized immigrants from public services, joined Republican governors in supporting Trump's immigration policies, and increased state resources for border enforcement.",
            "FAMILY-VALUES": "Upholds traditional values; supports parental rights in education, signed bans on gender-affirming care for minors, and promotes policies strengthening marriage and family through economic stability.",
            "ELECTION-INTEGRITY": "Ensures secure elections; implemented voter ID requirements, expanded early voting with safeguards, and defended Idaho's election processes against unfounded fraud claims while promoting transparency."
        },
        "endorsements": ["President Donald Trump", "Idaho Republican Party", "National Rifle Association"]
    },
    {
        "name": "Paulette Jordan",
        "state": "Idaho",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Paulette Jordan, born in 1979, is a member of the Coeur d'Alene Tribe and a proud Idaho native from Post Falls. She earned a degree in American government from the University of Idaho and served as a state representative for District 5 from 2015 to 2019. Jordan made history as the Democratic nominee for governor in 2018, narrowly losing to Brad Little, and ran for U.S. Senate in 2020. A former athlete and advocate for Native American rights, she has focused on education equity and environmental protection. Jordan is single and resides in Post Falls, dedicating her career to public service and tribal sovereignty.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://jordanforgovernor.com/",
        "positions": {
            "ABORTION": "Pro-choice; advocates for restoring Roe v. Wade protections, opposes Idaho's abortion bans, and supports access to reproductive health services including abortion up to viability.",
            "EDUCATION": "Emphasizes public school funding; opposes voucher programs, pushes for increased teacher pay and universal pre-K, but supports inclusive curricula without bans on DEI topics.",
            "RELIGIOUS-FREEDOM": "Supports separation of church and state; backs protections for all faiths but opposes laws allowing refusal of services based on religious beliefs, prioritizing LGBTQ+ rights.",
            "GUNS": "Favors reasonable gun control; supports universal background checks and red flag laws while respecting hunting traditions, but seeks to close loopholes in assault weapon sales.",
            "TAXES": "Progressive taxation; proposes raising taxes on high earners to fund social services, opposes cuts that benefit corporations, and supports property tax relief for low-income families.",
            "IMMIGRATION": "Path to citizenship; advocates for comprehensive reform, opposes strict border measures, and supports sanctuary policies and DACA protections for Dreamers.",
            "FAMILY-VALUES": "Inclusive family policies; supports same-sex marriage, gender-affirming care, and comprehensive sex education, emphasizing equality over traditional definitions.",
            "ELECTION-INTEGRITY": "Expands access; opposes strict voter ID, supports mail-in voting expansion, and focuses on inclusivity rather than fraud prevention measures."
        },
        "endorsements": ["Idaho Democratic Party", "Planned Parenthood", "Sierra Club"]
    },
    {
        "name": "Jim Risch",
        "state": "Idaho",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "James E. 'Jim' Risch, born in 1943 in Milwaukee, Wisconsin, moved to Idaho as a child and graduated from the University of Idaho with degrees in history and law. A rancher and attorney, he served as Ada County prosecutor, state senator, and Lieutenant Governor before becoming governor in 2006-2007. Elected to the U.S. Senate in 2008, Risch chairs the Foreign Relations Committee and focuses on national security. Married to Vicki Risch, they have three children and five grandchildren, living on their Boise-area ranch. His accomplishments include authoring the Uyghur Forced Labor Prevention Act and defending Idaho's water rights.",
        "faith_statement": "As a devout Catholic, Senator Risch has stated that his faith informs his commitment to the sanctity of life and religious freedom, often citing it in support for pro-life legislation and protections against religious persecution globally.",
        "website": "https://www.risch.senate.gov/",
        "positions": {
            "ABORTION": "Unequivocally pro-life; co-sponsored bills to defund Planned Parenthood, prohibit federal funding for abortions, and supports a national ban, believing life begins at conception.",
            "EDUCATION": "Promotes school choice; backs federal vouchers and tax credits for private education, opposes federal overreach in curricula, and supports parental rights in challenging indoctrination.",
            "RELIGIOUS-FREEDOM": "Champion of religious liberty; introduced legislation to protect faith-based organizations from discrimination and combats global religious persecution through the Frank Wolf International Religious Freedom Act.",
            "GUNS": "Staunch 2nd Amendment defender; co-sponsored bills prohibiting state excise taxes on firearms, opposed all gun control measures, and supports concealed carry reciprocity nationwide.",
            "TAXES": "Advocates tax relief; voted for the 2017 Tax Cuts and Jobs Act, pushes for permanent extension of individual cuts, and opposes tax increases on middle-class families.",
            "IMMIGRATION": "Enforces strict borders; supports Trump's wall, ending chain migration, and merit-based system, co-sponsored bills to limit asylum claims and deport criminal aliens.",
            "FAMILY-VALUES": "Traditional values advocate; opposes same-sex marriage federally, supports bans on gender transition for minors, and promotes policies reinforcing nuclear family structures.",
            "ELECTION-INTEGRITY": "Secures elections; backs voter ID mandates, paper ballots, and federal audits to prevent fraud, criticizing mail-in voting expansions without safeguards."
        },
        "endorsements": ["President Donald Trump", "National Right to Life Committee", "Family Research Council"]
    },
    {
        "name": "Todd Achilles",
        "state": "Idaho",
        "office": "U.S. Senate",
        "party": "Independent",
        "bio": "Todd Achilles, a Boise native and Army veteran, served as a Democratic state representative for District 17 from 2023 until resigning in July 2025 to run for U.S. Senate. He holds a degree from Boise State University and has worked in public policy and veterans' affairs. As a former Democrat now independent, Achilles focuses on bipartisanship and public lands preservation. Married with children, he resides in Boise and aims to bridge divides in a polarized Congress.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.achillesforidaho.com/",
        "positions": {
            "ABORTION": "Supports access with limits; favors restoring Roe v. Wade, opposes total bans but supports restrictions after viability and parental notification for minors.",
            "EDUCATION": "Invests in public schools; opposes vouchers diverting funds, advocates for teacher pay raises and mental health resources without ideological bans.",
            "RELIGIOUS-FREEDOM": "Protects all beliefs; supports nondiscrimination laws including for LGBTQ+, opposes using religion to deny services, emphasizes tolerance.",
            "GUNS": "Balanced approach; supports background checks and assault weapon limits while protecting hunting rights, focuses on mental health over restrictions.",
            "TAXES": "Fair taxation; proposes closing corporate loopholes, progressive rates on wealthy, and rebates for working families without broad cuts.",
            "IMMIGRATION": "Humane reform; supports pathway to citizenship for DREAMers, increased border security with technology, and ending family separations.",
            "FAMILY-VALUES": "Modern inclusivity; backs marriage equality, gender-affirming care access, and family leave policies for all configurations.",
            "ELECTION-INTEGRITY": "Enhances access; supports automatic registration, opposes restrictive ID laws, prioritizes cybersecurity over fraud narratives."
        },
        "endorsements": ["Veterans for Peace", "League of Conservation Voters", "Idaho Education Association"]
    },
    {
        "name": "Russ Fulcher",
        "state": "Idaho",
        "office": "U.S. House District 1",
        "party": "Republican",
        "bio": "Russell 'Russ' Fulcher, born in 1962 in Boise, is a businessman and former state senator. He graduated from Boise State University and served in the Idaho Legislature from 2005 to 2018, including as Majority Leader. Elected to Congress in 2018, he represents Idaho's 1st District. A real estate developer, Fulcher and his wife, Patricia, have five children and live in Meridian. Key accomplishments include sponsoring the SHUSH Act to reduce noise over national parks and defending Idaho's agriculture.",
        "faith_statement": "As a committed Christian, Rep. Fulcher integrates his faith into public service, supporting pro-life causes and religious liberty, often attending church events and citing biblical principles in policy advocacy.",
        "website": "https://fulcher.house.gov/",
        "positions": {
            "ABORTION": "Pro-life absolutist; co-sponsored Life at Conception Act, opposes all abortions, and supports defunding Planned Parenthood entirely.",
            "EDUCATION": "School choice proponent; backs federal ESA expansions and opposes Common Core remnants, emphasizing local control and parental involvement.",
            "RELIGIOUS-FREEDOM": "Defends faith-based rights; voted against Equality Act provisions seen as infringing on religious exercise, supports conscience protections.",
            "GUNS": "2A champion; opposes ATF overreach, supports national reciprocity, and introduced bills to protect gun manufacturers from lawsuits.",
            "TAXES": "Tax cutter; advocates permanent TCJA extensions, eliminates estate tax, and pushes for flat tax considerations.",
            "IMMIGRATION": "Secure borders first; supports wall funding, E-Verify mandates, and ending birthright citizenship for children of illegals.",
            "FAMILY-VALUES": "Traditional defender; opposes ERA, supports parental rights against gender ideology, and promotes abstinence education.",
            "ELECTION-INTEGRITY": "Voter ID required; backs Election Integrity Act for photo ID and same-day voting, combats non-citizen voting."
        },
        "endorsements": ["Idaho Farm Bureau", "Gun Owners of America", "Heritage Action"]
    },
    {
        "name": "Mike Simpson",
        "state": "Idaho",
        "office": "U.S. House District 2",
        "party": "Republican",
        "bio": "Michael K. 'Mike' Simpson, born in 1950 in Idaho Falls, is a dentist and long-serving congressman since 1999. He graduated from Utah State and Case Western Reserve University School of Dentistry. Before Congress, he served in the Idaho Legislature for 12 years. Married to Lynnette, they have three children and reside in Idaho Falls. Simpson chairs the Interior Appropriations Subcommittee, securing funding for national labs and water projects.",
        "faith_statement": "A practicing member of The Church of Jesus Christ of Latter-day Saints, Rep. Simpson's faith guides his commitment to family, community service, and ethical governance, often participating in interfaith dialogues.",
        "website": "https://simpson.house.gov/",
        "positions": {
            "ABORTION": "Pro-life with exceptions; supports restrictions post-viability, defunds abortion providers, but allows in cases of rape/incest.",
            "EDUCATION": "Local control advocate; opposes federal standards, supports career-tech funding and choice options like charters.",
            "RELIGIOUS-FREEDOM": "Protects conscience; voted for RFRA expansions, opposes mandates forcing faith violations in healthcare.",
            "GUNS": "Strong 2A supporter; blocks funding for gun registries, supports concealed carry, fights red flag laws.",
            "TAXES": "Relief focused; extended TCJA, cuts corporate rates, protects deductions for families and businesses.",
            "IMMIGRATION": "Enforcement priority; funds border security, supports merit immigration, reduces chain migration.",
            "FAMILY-VALUES": "Family-centric; backs adoption incentives, opposes no-fault divorce expansions, supports faith-based initiatives.",
            "ELECTION-INTEGRITY": "Safeguards elections; supports voter ID, audits, and limits on mail ballots to prevent fraud."
        },
        "endorsements": ["U.S. Chamber of Commerce", "National Federation of Independent Business", "Idaho Mining Association"]
    },
    {
        "name": "Scott Bedke",
        "state": "Idaho",
        "office": "Lieutenant Governor",
        "party": "Republican",
        "bio": "Scott Bedke, a Oakley rancher born in 1958, served 22 years in the Idaho House, including as Speaker from 2012-2023. Elected Lt. Gov. in 2023, he focuses on agriculture and rural issues. Graduated from the University of Idaho, married to Marla with four children. Accomplishments include leading budget reforms and water rights protections.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://bedkeforidaho.com/",
        "positions": {
            "ABORTION": "Pro-life; supported total bans and defunding abortions.",
            "EDUCATION": "School choice; expanded ESAs.",
            "RELIGIOUS-FREEDOM": "Defends liberties; backs conscience laws.",
            "GUNS": "2A supporter; constitutional carry.",
            "TAXES": "Cuts advocate; grocery tax repeal.",
            "IMMIGRATION": "Border security; E-Verify.",
            "FAMILY-VALUES": "Traditional; parental rights.",
            "ELECTION-INTEGRITY": "Voter ID; secure processes."
        },
        "endorsements": ["Governor Brad Little", "Senator Jim Risch"]
    },
    {
        "name": "Raúl Labrador",
        "state": "Idaho",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "Raúl Labrador, born in 1967 in Venezuela, immigrated young and became a U.S. citizen. A former congressman (2011-2019), he now serves as AG since 2023. J.D. from University of Idaho, married with five children. Known for conservative lawsuits against ObamaCare.",
        "faith_statement": "As an evangelical Christian, AG Labrador credits his faith for his pro-life stance and family values, often speaking at church events.",
        "website": "https://www.ag.idaho.gov/",
        "positions": {
            "ABORTION": "Pro-life enforcer; defended bans in court.",
            "EDUCATION": "Parental rights; sued over indoctrination.",
            "RELIGIOUS-FREEDOM": "Sues for protections; anti-discrimination suits.",
            "GUNS": "2A defender; challenged restrictions.",
            "TAXES": "Low taxes; fiscal conservative.",
            "IMMIGRATION": "Strict enforcement; border suits.",
            "FAMILY-VALUES": "Traditional; opposed gender care.",
            "ELECTION-INTEGRITY": "Fraud fighter; audit supporter."
        },
        "endorsements": ["Idaho Freedom Foundation", "Federation for American Immigration Reform"]
    },
    {
        "name": "Phil McGrane",
        "state": "Idaho",
        "office": "Secretary of State",
        "party": "Republican",
        "bio": "Phil McGrane, Ada County Clerk since 2005, elected Sec. State in 2022. Involved in elections for decades, he ensures secure processes. Married with family in Meridian.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://sos.idaho.gov/",
        "positions": {
            "ABORTION": "Pro-life; supports state bans.",
            "EDUCATION": "Choice advocate.",
            "RELIGIOUS-FREEDOM": "Protector.",
            "GUNS": "2A backer.",
            "TAXES": "Relief supporter.",
            "IMMIGRATION": "Secure borders.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "Voter ID, audits."
        },
        "endorsements": ["Idaho Republican Party"]
    },
    {
        "name": "Julie Ellsworth",
        "state": "Idaho",
        "office": "State Treasurer",
        "party": "Republican",
        "bio": "Julie Ellsworth, elected 2018, former state rep. Manages $20B+ in assets. BS from BYU, married with three children.",
        "faith_statement": "LDS member; faith informs fiscal stewardship.",
        "website": "https://sto.idaho.gov/",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Choice.",
            "RELIGIOUS-FREEDOM": "Defender.",
            "GUNS": "2A.",
            "TAXES": "Cuts.",
            "IMMIGRATION": "Enforce.",
            "FAMILY-VALUES": "Support.",
            "ELECTION-INTEGRITY": "Secure."
        },
        "endorsements": ["Idaho Bankers Association"]
    },
    {
        "name": "Debra Schroeder",
        "state": "Idaho",
        "office": "Superintendent of Public Instruction",
        "party": "Republican",
        "bio": "Debra Schroeder, elected 2022, former teacher and principal. Focuses on literacy and standards. Married, family in Nampa.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.sde.idaho.gov/",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Standards, choice.",
            "RELIGIOUS-FREEDOM": "School prayer.",
            "GUNS": "Safe schools.",
            "TAXES": "Fund education.",
            "IMMIGRATION": "Legal.",
            "FAMILY-VALUES": "Parental rights.",
            "ELECTION-INTEGRITY": "Transparent."
        },
        "endorsements": ["Idaho Association of School Administrators"]
    },
    {
        "name": "Jeff Alldridge",
        "state": "Idaho",
        "office": "Mayor of Idaho Falls",
        "party": "Republican",
        "bio": "Jeff Alldridge, Idaho Falls native, business owner in construction. Community leader, focuses on growth. Married with family.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://jeff4if.com/",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Local control.",
            "RELIGIOUS-FREEDOM": "Support.",
            "GUNS": "2A.",
            "TAXES": "Low.",
            "IMMIGRATION": "Enforce.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "Secure."
        },
        "endorsements": ["Idaho Falls Chamber of Commerce"]
    },
    {
        "name": "Lisa Burtenshaw",
        "state": "Idaho",
        "office": "Mayor of Idaho Falls",
        "party": "Nonpartisan",
        "bio": "Lisa Burtenshaw, local educator and volunteer. Advocates for families and infrastructure.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Personal choice.",
            "EDUCATION": "Funding.",
            "RELIGIOUS-FREEDOM": "Inclusive.",
            "GUNS": "Responsible.",
            "TAXES": "Relief.",
            "IMMIGRATION": "Humane.",
            "FAMILY-VALUES": "Supportive.",
            "ELECTION-INTEGRITY": "Accessible."
        },
        "endorsements": ["Local teachers union"]
    },
    {
        "name": "Christian Ashcraft",
        "state": "Idaho",
        "office": "Mayor of Idaho Falls",
        "party": "Nonpartisan",
        "bio": "Christian Ashcraft, entrepreneur and veteran. Emphasizes economic development.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Choice.",
            "RELIGIOUS-FREEDOM": "Defend.",
            "GUNS": "Protect.",
            "TAXES": "Cut.",
            "IMMIGRATION": "Secure.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "ID required."
        },
        "endorsements": ["Veterans groups"]
    }
]

# Idaho Summary
summary = {
    "state": "Idaho",
    "title": "Idaho 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Idaho 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 10  
**Total Candidates Profiled:** 16  
**Election Dates:**  
- 2025-11-04 (Municipal Elections)  
- 2026-11-03 (General Elections)  

---

## 🔴 Idaho POLITICAL LANDSCAPE

### **The Gem State**

Idaho is a **deep-red conservative stronghold**:  
- **Legislature:** Republican supermajorities in both House (59-11) and Senate (28-7), enabling swift passage of pro-life and pro-family laws.  
- **Voter Base:** Over 60% Republican registration, with evangelicals and LDS members driving turnout on moral issues.  
- **Urban-Rural Divide:** Boise metro leans purple with growth attracting transplants, while rural counties like those in the Panhandle and Magic Valley remain solidly conservative; key battlegrounds include Ada and Bonneville Counties.  
- **Unique State Factor:** Strong LDS influence in eastern Idaho shapes family values, while outdoor recreation culture bolsters gun rights advocacy.  

### **Why Idaho Matters**

Idaho is **CRITICAL** for Christian conservatives:  
- ✅ **Pro-Life Leadership:** Nation's strictest abortion laws, including a total ban with civil penalties; heartbeat law upheld, but faces federal challenges.  
- ✅ **Second Amendment:** Constitutional carry since 2020, preemption laws block local restrictions; top-ranked for gun freedom.  
- ✅ **School Choice:** Empowering Parents Grants provide ESAs up to $1,000/child; bans on CRT and gender ideology protect biblical worldview in schools.  
- ✅ **Religious Liberty:** Conscience protections for healthcare workers; RFRA strengthened against Big Tech censorship.  
- ✅ **Family Values:** Minors' gender care ban, parental consent for sex ed; traditional marriage affirmed.  
- ✅ **Election Security:** Voter ID required, paper ballots; low fraud but vigilant against mail-in risks.  

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** This race secures Senate GOP majority for judicial confirmations advancing pro-life rulings; Idaho's seat is a firewall against liberal gains.  

**Jim Risch (Republican)** - Incumbent U.S. Senator  

**Faith Statement:** "As a devout Catholic, Senator Risch has stated that his faith informs his commitment to the sanctity of life and religious freedom, often citing it in support for pro-life legislation and protections against religious persecution globally."  

**Background:**  
- Fourth-generation Idahoan, rancher, and J.D. from University of Idaho.  
- Served as Governor (2006-2007), Lt. Gov., and prosecutor; elected to Senate in 2008.  
- Married to Vicki with three children; chairs Foreign Relations Committee.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Perfect record; co-sponsored defund Planned Parenthood, national ban pushes (100/100 rating).  
- **Religious Liberty:** Led global persecution fights; RFRA defender (exemplary).  
- **Education/Parental Rights:** Backed choice bills, opposed fed overreach (strong).  
- **Family Values:** Opposed ERA, gender bans; biblical alignment high.  
- **Overall Assessment:** 9/10 - Seasoned defender, but age (83 in 2026) raises succession concerns; unwavering on core issues.  

**Key Positions:**  
- **ABORTION:** Unequivocally pro-life; co-sponsored bills to defund Planned Parenthood, prohibit federal funding for abortions, and supports a national ban, believing life begins at conception.  
- **EDUCATION:** Promotes school choice; backs federal vouchers and tax credits for private education, opposes federal overreach in curricula, and supports parental rights in challenging indoctrination.  
- **RELIGIOUS FREEDOM:** Champion of religious liberty; introduced legislation to protect faith-based organizations from discrimination and combats global religious persecution through the Frank Wolf International Religious Freedom Act.  
- **GUNS:** Staunch 2nd Amendment defender; co-sponsored bills prohibiting state excise taxes on firearms, opposed all gun control measures, and supports concealed carry reciprocity nationwide.  
- **TAXES:** Advocates tax relief; voted for the 2017 Tax Cuts and Jobs Act, pushes for permanent extension of individual cuts, and opposes tax increases on middle-class families.  
- **IMMIGRATION:** Enforces strict borders; supports Trump's wall, ending chain migration, and merit-based system, co-sponsored bills to limit asylum claims and deport criminal aliens.  

**Endorsements:** President Donald Trump, National Right to Life Committee, Family Research Council  

**Website:** https://www.risch.senate.gov/  

**Todd Achilles (Independent)** - Challenger  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Army veteran, Boise State grad, former Dem state rep (2023-2025).  
- Resigned to run independently, focusing on bipartisanship.  
- Married with children in Boise.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Moderate; supports Roe restoration, not bans (poor).  
- **Religious Liberty:** Inclusive but prioritizes LGBTQ+ over conscience (weak).  
- **Education/Parental Rights:** Public funding focus, opposes choice (inadequate).  
- **Family Values:** Backs equality, gender care (misaligned).  
- **Overall Assessment:** 3/10 - Independent appeal masks progressive lean; risks diluting conservative voice.  

**Key Positions:**  
- **ABORTION:** Supports access with limits; favors restoring Roe v. Wade, opposes total bans but supports restrictions after viability and parental notification for minors.  
- **EDUCATION:** Invests in public schools; opposes vouchers diverting funds, advocates for teacher pay raises and mental health resources without ideological bans.  
- **RELIGIOUS FREEDOM:** Protects all beliefs; supports nondiscrimination laws including for LGBTQ+, opposes using religion to deny services, emphasizes tolerance.  
- **GUNS:** Balanced approach; supports background checks and assault weapon limits while protecting hunting rights, focuses on mental health over restrictions.  
- **TAXES:** Fair taxation; proposes closing corporate loopholes, progressive rates on wealthy, and rebates for working families without broad cuts.  

**Endorsements:** Veterans for Peace, League of Conservation Voters  

**Website:** https://www.achillesforidaho.com/  

**Why It Matters:** Retaining Risch ensures Senate confirmations of justices who protect unborn life and religious freedoms for generations.  

### **U.S. House District 1** - 2026-11-03

**Context:** Covers northern Idaho; vital for rural conservative priorities like timber and mining against environmental overreach.  

**Russ Fulcher (Republican)** - Incumbent Congressman  

**Faith Statement:** "As a committed Christian, Rep. Fulcher integrates his faith into public service, supporting pro-life causes and religious liberty, often attending church events and citing biblical principles in policy advocacy."  

**Background:**  
- Boise businessman, BS from Boise State.  
- State Majority Leader (2012-2018); elected 2018.  
- Married to Patricia with five children.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Life at Conception Act sponsor (100/100).  
- **Religious Liberty:** Voted against Equality Act threats (solid).  
- **Education/Parental Rights:** ESA expansions (strong).  
- **Family Values:** Abstinence ed, gender bans (aligned).  
- **Overall Assessment:** 9/10 - Reliable Freedom Caucus ally; bolsters Trump agenda.  

**Key Positions:**  
- **ABORTION:** Pro-life absolutist; co-sponsored Life at Conception Act, opposes all abortions, and supports defunding Planned Parenthood entirely.  
- **EDUCATION:** School choice proponent; backs federal ESA expansions and opposes Common Core remnants, emphasizing local control and parental involvement.  
- **RELIGIOUS-FREEDOM:** Defends faith-based rights; voted against Equality Act provisions seen as infringing on religious exercise, supports conscience protections.  
- **GUNS:** 2A champion; opposes ATF overreach, supports national reciprocity, and introduced bills to protect gun manufacturers from lawsuits.  
- **TAXES:** Tax cutter; advocates permanent TCJA extensions, eliminates estate tax, and pushes for flat tax considerations.  

**Endorsements:** Idaho Farm Bureau, Gun Owners of America  

**Website:** https://fulcher.house.gov/  

**Why It Matters:** Fulcher's re-election safeguards northern Idaho's hunting heritage and blocks green energy mandates harming families.  

### **U.S. House District 2** - 2026-11-03

**Context:** Includes Boise; tests conservative hold amid urban growth, key for appropriations protecting INL labs and farms.  

**Mike Simpson (Republican)** - Incumbent Congressman  

**Faith Statement:** "A practicing member of The Church of Jesus Christ of Latter-day Saints, Rep. Simpson's faith guides his commitment to family, community service, and ethical governance, often participating in interfaith dialogues."  

**Background:**  
- Idaho Falls dentist, DMD from Case Western.  
- State legislator 1984-1998; Congress since 1999.  
- Married to Lynnette with three children.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Defunds abortions, viability limits (90/100).  
- **Religious Liberty:** RFRA supporter (good).  
- **Education/Parental Rights:** Charter funding (solid).  
- **Family Values:** Adoption incentives (aligned).  
- **Overall Assessment:** 8/10 - Appropriations power secures wins, though occasional bipartisan compromises.  

**Key Positions:**  
- **ABORTION:** Pro-life with exceptions; supports restrictions post-viability, defunds abortion providers, but allows in cases of rape/incest.  
- **EDUCATION:** Local control advocate; opposes federal standards, supports career-tech funding and choice options like charters.  
- **RELIGIOUS-FREEDOM:** Protects conscience; voted for RFRA expansions, opposes mandates forcing faith violations in healthcare.  
- **GUNS:** Strong 2A supporter; blocks funding for gun registries, supports concealed carry, fights red flag laws.  
- **TAXES:** Relief focused; extended TCJA, cuts corporate rates, protects deductions for families and businesses.  

**Endorsements:** U.S. Chamber of Commerce, National Federation of Independent Business  

**Website:** https://simpson.house.gov/  

**Why It Matters:** Simpson's expertise funds faith-based initiatives and blocks funding for woke programs in schools.  

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** Incumbent race shapes state direction on life issues; GOP primary could test Trump's influence.  

**Brad Little (Republican)** - Incumbent Governor  

**Faith Statement:** "As a committed Christian, Governor Little has publicly recognized the Christian heritage of America and Idaho, proclaiming weeks of Christian heritage and signing bills to protect religious conscience rights for medical professionals. He often invokes faith in calls for unity and prayer during crises."  

**Background:**  
- Emmett rancher, UI ag econ grad, National Guard vet.  
- Lt. Gov. 2009-2019; governor since 2019.  
- Married to Terri with three children.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Signed total ban, heartbeat law (100/100).  
- **Religious Liberty:** Conscience bills, mandate suits (exemplary).  
- **Education/Parental Rights:** ESA expansions, CRT bans (strong).  
- **Family Values:** Gender care ban for minors (high alignment).  
- **Overall Assessment:** 9/10 - Proven leader; Trump endorsement solidifies base.  

**Key Positions:**  
- **ABORTION:** Strongly pro-life; signed Idaho's near-total abortion ban post-Roe v. Wade, prohibiting abortions except in cases of rape, incest, or life-threatening conditions, and a six-week ban modeled on Texas law allowing private enforcement.  
- **EDUCATION:** Supports school choice and parental rights; expanded Idaho's Empowering Parents Grant program providing ESA funds up to $1,000 per child for private or homeschool options, and signed laws banning critical race theory and gender ideology in public schools.  
- **RELIGIOUS FREEDOM:** Defends religious liberty; signed legislation protecting doctors and nurses from participating in procedures violating their faith, and joined multi-state suits against federal mandates infringing on religious exercise.  
- **GUNS:** Firm Second Amendment advocate; opposed federal gun control measures, signed constitutional carry expansions, and supported legislation preempting local gun restrictions to ensure statewide uniformity.  
- **TAXES:** Proposes tax cuts; enacted largest income tax reduction in Idaho history in 2022, eliminating the grocery tax, and advocates for property tax relief while maintaining fiscal conservatism with balanced budgets.  

**Endorsements:** President Donald Trump, Idaho Republican Party, National Rifle Association  

**Website:** https://gov.idaho.gov/  

**Paulette Jordan (Democrat)** - Challenger  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Coeur d'Alene Tribe member, UI gov grad.  
- State rep 2015-2019; 2018 nominee.  
- Single, Post Falls resident.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Pro-choice advocate (0/100).  
- **Religious Liberty:** Separation emphasis (weak).  
- **Education/Parental Rights:** Public focus, no bans (poor).  
- **Family Values:** Inclusive, gender care support (opposed).  
- **Overall Assessment:** 2/10 - Historic but progressive; threat to biblical policies.  

**Key Positions:**  
- **ABORTION:** Pro-choice; advocates for restoring Roe v. Wade protections, opposes Idaho's abortion bans, and supports access to reproductive health services including abortion up to viability.  
- **EDUCATION:** Emphasizes public school funding; opposes voucher programs, pushes for increased teacher pay and universal pre-K, but supports inclusive curricula without bans on DEI topics.  
- **RELIGIOUS FREEDOM:** Supports separation of church and state; backs protections for all faiths but opposes laws allowing refusal of services based on religious beliefs, prioritizing LGBTQ+ rights.  

**Endorsements:** Idaho Democratic Party, Planned Parenthood  

**Website:** https://jordanforgovernor.com/  

**Why It Matters:** Little's win fortifies Idaho as pro-life beacon, blocking progressive encroachments on family sanctity.  

### **Lieutenant Governor** - 2026-11-03

**Context:** Succession role; influences rural policy and ethics.  

**Scott Bedke (Republican)** - Incumbent  

**Faith Statement:** "No publicly disclosed faith statement"  

**Background:**  
- Oakley rancher, UI grad.  
- House Speaker 2012-2023; Lt. Gov. since 2023.  
- Married to Marla with four children.  

**Christian Conservative Analysis:**  
- **Pro-Life:** Ban supporter (95/100).  
- **Religious Liberty:** Backed protections.  
- **Education/Parental Rights:** ESA leader.  
- **Family Values:** Parental rights.  
- **Overall Assessment:** 8/10 - Rancher roots resonate.  

**Key Positions:**  
- **ABORTION:** Pro-life; supported total bans and defunding abortions.  
- **EDUCATION:** School choice; expanded ESAs.  
- **RELIGIOUS FREEDOM:** Defends liberties; backs conscience laws.  

**Endorsements:** Governor Brad Little, Senator Jim Risch  

**Website:** https://bedkeforidaho.com/  

**Why It Matters:** Bedke ensures conservative continuity in executive branch.  

[Similar structure for AG, Sec State, Treasurer, Supt - abbreviated for length]  

**Raúl Labrador (Republican) - Attorney General**  
Faith: Evangelical Christian. Positions: Enforces bans, sues feds. Assessment: 9/10. Website: https://www.ag.idaho.gov/  

**Phil McGrane (Republican) - Secretary of State**  
Faith: N/A. Positions: Voter ID enforcer. Assessment: 8/10. Website: https://sos.idaho.gov/  

**Julie Ellsworth (Republican) - State Treasurer**  
Faith: LDS. Positions: Fiscal conservative. Assessment: 7/10. Website: https://sto.idaho.gov/  

**Debra Schroeder (Republican) - Superintendent**  
Faith: N/A. Positions: Choice advocate. Assessment: 8/10. Website: https://www.sde.idaho.gov/  

---

## 🎯 KEY ISSUES FOR Idaho CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**  
- Total abortion ban since 2022, exceptions limited; 50+ pregnancy centers statewide.  
- Parental consent required for minors' abortions.  
- No state funding for Planned Parenthood.  
- Recent victory: Upheld heartbeat law against ACLU suit.  

**Progressive Position:**  
- Ballot pushes to repeal bans via initiative.  
- Federal funding battles for clinics.  
- Expansion via telehealth abortions.  

**Christian Conservative Action:**  
- Join Idaho Chooses Life for rallies.  
- Support HCR 1 pro-life resolution.  
- Volunteer at centers like Boise's Mustard Seed.  
- Vote pro-life in all races.  

### **School Choice & Parental Rights**

**Conservative Position:**  
- ESAs for 10,000+ students; homeschool tax credits.  
- 2023 law bans gender ideology K-12.  
- Homeschool freedom with no notification required.  
- Win: Blocked fed DEI grants.  

**Progressive Position:**  
- Union-backed public monopoly.  
- DEI mandates in teacher training.  
- Threats to choice via funding cuts.  

**Christian Conservative Action:**  
- Run for school boards via Blinded By Sight.  
- Back S 1234 parental bill.  
- Join Idaho Family Policy Center.  

### **Religious Freedom**

**Conservative Position:**  
- 2025 conscience law shields doctors from euthanasia.  
- Preempts local anti-faith ordinances.  
- Protects church vaccine exemptions.  

**Progressive Position:**  
- Nondiscrimination bills forcing service.  
- Attacks on faith adoptions.  

**Christian Conservative Action:**  
- Alliance Defending Freedom cases.  
- Support First Liberty suits.  
- Pray against Big Tech censorship.  

### **Guns**

**Conservative Position:**  
- Permitless carry for 18+; no assault bans.  
- Preemption since 2018.  
- NRA A+ ranking.  

**Progressive Position:**  
- Local safe storage laws.  
- Red flag pushes.  

**Christian Conservative Action:**  
- Join Idaho Firearms Federation.  
- Lobby H 215 reciprocity.  
- Train church security.  

### **Taxes**

**Conservative Position:**  
- 5.8% flat income; no sales on groceries.  
- Property relief via rebates.  
- Surplus to taxpayers.  

**Progressive Position:**  
- Wealth taxes, carbon fees.  

**Christian Conservative Action:**  
- Oppose S 1001 hikes.  
- Support Idaho Freedom Foundation.  

### **Immigration**

**Conservative Position:**  
- E-Verify mandate 2024.  
- No benefits for illegals.  
- Border ops funding.  

**Progressive Position:**  
- Sanctuary cities.  
- Driver licenses for undocumented.  

**Christian Conservative Action:**  
- Back FAIR endorsements.  
- Report violations.  

### **Family Values**

**Conservative Position:**  
- Minors transition ban upheld.  
- Covenant marriage option.  
- Anti-porn libraries.  

**Progressive Position:**  
- Drag shows in schools.  
- No-fault divorce expansion.  

**Christian Conservative Action:**  
- Family Policy Alliance events.  
- S 1100 support.  

### **Election Integrity**

**Conservative Position:**  
- Strict ID, no mass mail.  
- Audits post-2020.  
- Paper trail required.  

**Progressive Position:**  
- Automatic registration.  
- Rank-choice voting.  

**Christian Conservative Action:**  
- Poll watch via Eagle Forum.  
- Oppose HJR 4.  
- iVoterGuide use.  

---

## 📅 CRITICAL DATES

**2025-2026 Election Calendar:**  
- 2025-10-07 - Voter registration deadline (municipal)  
- 2025-10-20 - Early voting begins (municipal)  
- 2025-11-04 - Municipal Election  
- 2026-05-15 - Primary Election  
- 2026-10-09 - Voter registration deadline (general)  
- 2026-10-26 - Early voting begins  
- 2026-11-03 - General Election  

**Voter Registration:** https://voteidaho.gov/  

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
✅ **Share on social media** with #IdahoFaithVote  
✅ **Pray daily** for elections and candidates  
✅ **Vote early** and bring friends/family to polls  
✅ **Serve as poll watchers** to ensure election integrity  

---

## 📞 RESOURCES FOR Idaho CHRISTIAN VOTERS

### **Voter Guide Organizations:**  
- **iVoterGuide.org** - Idaho coverage  
- **Idaho Chooses Life** - Pro-life ratings  
- **Idaho Family Policy Center** - Faith-based education  
- **Christian Voter Guide** - Biblical alignment  

### **Election Information:**  
- **Idaho Secretary of State**: https://sos.idaho.gov/  
- **County Election Offices**: Search voteidaho.gov by county  
- **Early Voting Locations**: Available at county clerks  

### **Conservative Organizations:**  
- **Idaho Chooses Life**: https://idaholife.org/  
- **Idaho Family Policy Center**: https://idahofamily.org/  
- **Idaho Firearms Federation**: https://idahofirearms.org/  
- **Blinded By Sight (School Choice)**: https://blindedbysight.org/  
- **Alliance Defending Freedom** - Religious liberty  
- **First Liberty Institute** - Religious freedom  

---

## 🔥 BOTTOM LINE FOR Idaho CHRISTIANS

**2025-2026 Elections Matter:**  
- Governor race determines abortion enforcement.  
- Senate seat affects national pro-life judges.  
- House districts protect rural family farms.  
- Overall state direction at stake  

**If Conservatives Win:**  

✅ Pro-life protections maintained/strengthened  
✅ School choice expanded, parental rights protected  
✅ Religious liberty defended  
✅ Traditional family values upheld  
✅ Second Amendment rights secured  
✅ Election integrity ensured  
✅ Rural economies boosted via tax cuts  
✅ Border security enhanced  
✅ Faith in public life affirmed  

**If Progressives Win:**  

❌ Abortion expansion, pro-life laws repealed  
❌ School choice gutted, CRT/gender ideology in schools  
❌ Religious liberty attacked  
❌ Family values eroded, parental rights stripped  
❌ Gun rights restricted  
❌ Election integrity weakened  
❌ Taxes hiked on families  
❌ Open borders strain resources  
❌ Faith marginalized in policy  

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**  

---

## 🙏 PRAYER POINTS

**Pray for:**  
- Brad Little, Jim Risch, Russ Fulcher, Mike Simpson and their families  
- Idaho Governor/leadership  
- Conservative candidates in all races  
- Church mobilization and Christian voter turnout  
- Protection from voter fraud  
- Wisdom for Christian voters in Idaho  
- Revival and awakening in Idaho  
- God's will in Idaho elections  

**Scripture for Idaho Elections:**  

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*  

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*  

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*  

---

**Last Updated:** October 2025  
**Source:** Christian Conservatives Today Election Coverage  
**Contact:** For questions or to contribute Idaho coverage, email contact@ekewaka.com  

**Idaho CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Idaho races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Idaho'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Idaho races...")
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

print(f"\nChecking for existing Idaho candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Idaho'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Idaho candidates...")
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

print("\nProcessing Idaho summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Idaho'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Idaho data upload complete!")