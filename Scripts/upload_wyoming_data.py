import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Wyoming Races
races = [
    {
        "state": "Wyoming",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Election for U.S. Senator from Wyoming, critical for advancing conservative values in national policy on life, liberty, and family."
    },
    {
        "state": "Wyoming",
        "office": "U.S. House At-Large",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "At-large congressional district race, key for representing Wyoming's rural and conservative interests in Congress."
    },
    {
        "state": "Wyoming",
        "office": "Governor and Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open gubernatorial race due to term limits, pivotal for steering state policies on energy, education, and family protections."
    },
    {
        "state": "Wyoming",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Oversees elections and business filings, essential for safeguarding election integrity and economic freedom."
    },
    {
        "state": "Wyoming",
        "office": "State Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Manages state investments and finances, crucial for fiscal conservatism and taxpayer protection."
    },
    {
        "state": "Wyoming",
        "office": "State Auditor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Audits state expenditures, vital for accountability and preventing government waste."
    },
    {
        "state": "Wyoming",
        "office": "Superintendent of Public Instruction",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Leads education policy, important for promoting school choice and parental rights."
    }
]

# Wyoming Candidates  
candidates = [
    {
        "name": "Cynthia Lummis",
        "state": "Wyoming",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Cynthia Lummis was born on a cattle ranch in Laramie County, Wyoming. A three-time graduate of the University of Wyoming in animal science, biology, and law, she has deep roots in ranching and public service. Sworn into the U.S. Senate in 2021 as Wyoming's first female senator, she previously served as Wyoming State Treasurer and in the U.S. House, where she was a founding member of the House Freedom Caucus. Lummis has fought federal overreach, championed energy independence, and protected public lands for multiple use. After leaving Congress in 2016, she managed family ranches and developments. Widowed, she is a devoted mother to daughter Annaliese, and grandmother to Gus, Al, and Bennett. Her career reflects unwavering commitment to Wyoming values, fiscal responsibility, and principled conservatism.",
        "faith_statement": "I attend the Trinity Lutheran Church in Cheyenne, Wyoming. I am a strong Christian and my faith guides my decisions as a mother, friend, neighbor and public servant.",
        "website": "https://www.lummis.senate.gov",
        "positions": {
            "ABORTION": "Strongly pro-life, supports defunding Planned Parenthood and advancing protections for the unborn at federal and state levels.",
            "EDUCATION": "Advocates for school choice, parental rights, and opposing federal overreach in curricula to ensure local control.",
            "RELIGIOUS-FREEDOM": "Champions religious liberty, co-sponsoring bills to protect faith-based organizations and student groups on campuses.",
            "GUNS": "Fierce defender of Second Amendment rights, opposes red-flag laws and supports national reciprocity for concealed carry.",
            "TAXES": "Pushes for tax cuts, simplification, and eliminating the death tax to promote economic growth and family farms.",
            "IMMIGRATION": "Supports secure borders, ending catch-and-release, and merit-based immigration to protect American workers.",
            "FAMILY-VALUES": "Upholds traditional marriage and family structures, opposing gender ideology in schools and promoting parental authority.",
            "ELECTION-INTEGRITY": "Backs voter ID requirements and audits to ensure transparent, secure elections."
        },
        "endorsements": ["Gun Owners of America", "National Right to Life", "Family Research Council"]
    },
    {
        "name": "Harriet Hageman",
        "state": "Wyoming",
        "office": "U.S. House At-Large",
        "party": "Republican",
        "bio": "Congresswoman Harriet Hageman represents Wyoming's at-large district, bringing 34 years of litigation experience challenging federal overreach. Raised on a ranch, she attended Casper College on a livestock judging scholarship and earned degrees from the University of Wyoming. Admitted to practice before the U.S. Supreme Court, she has fought for water and property rights, exposing federal mismanagement of lands and wildlife. In Congress, she chairs the House Natural Resources Subcommittee on Water, Wildlife, and Fisheries, serves on Judiciary, and co-chairs the Congressional Coal Caucus. A mother and rancher, Hageman is known for her no-nonsense approach to reining in the regulatory state and defending American energy production.",
        "faith_statement": "Faith, freedom, and integrity guide everything I do. I align my votes with biblical principles as reflected in congressional scorecards.",
        "website": "https://hageman.house.gov",
        "positions": {
            "ABORTION": "Pro-life, supports state-level protections and opposes federal funding for abortion providers.",
            "EDUCATION": "Prioritizes parental involvement and school choice, laser-focused on core education without ideological indoctrination.",
            "RELIGIOUS-FREEDOM": "Defends faith-based freedoms against government infringement, supporting resolutions to protect religious expression.",
            "GUNS": "Staunch Second Amendment advocate, fights bureaucratic restrictions on gun ownership and carry rights.",
            "TAXES": "Advocates for lower taxes and reduced federal spending to empower families and businesses.",
            "IMMIGRATION": "Enforces strict border security, ends sanctuary policies, and prioritizes American citizens.",
            "FAMILY-VALUES": "Promotes faith and family as core values, opposes policies eroding traditional structures.",
            "ELECTION-INTEGRITY": "Pushes for voter ID, paper ballots, and measures to prevent fraud in federal elections."
        },
        "endorsements": ["NRA", "Heritage Action", "Susan B. Anthony Pro-Life America"]
    },
    {
        "name": "Eric Barlow",
        "state": "Wyoming",
        "office": "Governor and Lieutenant Governor",
        "party": "Republican",
        "bio": "State Senator Eric Barlow, born in 1966, is a fifth-generation rancher and businessman from Gillette, Wyoming. A former House Speaker, he has served in the legislature since 2013, focusing on energy, agriculture, and fiscal conservatism. Barlow owns Barlow Ranch and has a background in oil and gas. Married with children, he emphasizes Wyoming's rural values and has led efforts on property rights and economic development. His gubernatorial bid asserts strong conservative stripes, promising to protect freedoms and promote prosperity.",
        "faith_statement": "No publicly disclosed faith statement, though events feature prayers invoking divine guidance.",
        "website": "https://ericbarlow.com",
        "positions": {
            "ABORTION": "Pro-life, supports Wyoming's trigger law and opposes expansions of abortion access.",
            "EDUCATION": "Backs school choice and parental rights, opposing federal mandates.",
            "RELIGIOUS-FREEDOM": "Defends religious liberty against government overreach.",
            "GUNS": "Strong Second Amendment supporter, advocates permitless carry.",
            "TAXES": "Committed to low taxes and fiscal restraint to support families.",
            "IMMIGRATION": "Prioritizes border security and state cooperation with federal enforcement.",
            "FAMILY-VALUES": "Upholds traditional family structures and parental authority.",
            "ELECTION-INTEGRITY": "Supports voter ID and election audits for transparency."
        },
        "endorsements": ["Wyoming Farm Bureau", "Wyoming Stock Growers Association"]
    },
    {
        "name": "Brent Bien",
        "state": "Wyoming",
        "office": "Governor and Lieutenant Governor",
        "party": "Republican",
        "bio": "Brent Bien, a Wyoming native and University of Wyoming engineering graduate, is a retired Marine Corps Colonel, Naval Aviator, and combat veteran with 275 missions in the Balkans, Iraq, and Afghanistan. Holding a postgraduate degree from the Naval War College, he transitioned to business before launching his gubernatorial campaign. Married to a Navy nurse, father of three daughters, and from a military family, Bien is a patriot dedicated to the American Dream, exceptionalism, and spirit. His platform focuses on protecting freedoms, accountability, and traditional values.",
        "faith_statement": "No publicly disclosed faith statement, but emphasizes defending traditional values and family.",
        "website": "https://brentbien.com",
        "positions": {
            "ABORTION": "Pro-life, supports protections for the unborn and family-centered policies.",
            "EDUCATION": "Promotes school choice and parental involvement in education.",
            "RELIGIOUS-FREEDOM": "Safeguards religious liberties as foundational to freedom.",
            "GUNS": "Defends Second Amendment rights unequivocally.",
            "TAXES": "Advocates fiscal responsibility and low taxes for economic freedom.",
            "IMMIGRATION": "Enforces secure borders to protect Wyoming communities.",
            "FAMILY-VALUES": "Prioritizes nuclear family health and traditional marriage.",
            "ELECTION-INTEGRITY": "Ensures secure, transparent elections with voter verification."
        },
        "endorsements": ["Veterans for America First"]
    },
    {
        "name": "Joseph Kibler",
        "state": "Wyoming",
        "office": "Governor and Lieutenant Governor",
        "party": "Republican",
        "bio": "Joseph Kibler is a grassroots conservative running for Wyoming Governor in 2026, emphasizing faith-driven leadership without political machines. A husband and father, he advocates for property rights, addiction recovery, and principled governance. Active in community meetings and social surveys, Kibler challenges scripted politics, urging Wyomingites to 'Be Something Different.' His campaign builds on partnerships rooted in Wyoming values, focusing on long-term consequences over short-term gains.",
        "faith_statement": "I believe the Scriptures are the fully inspired, error-free Word of God. Faith in Christ informs my decisions through Bible-based principles, including the Trinity, salvation by grace, male church leadership, and traditional marriage as between one man and one woman.",
        "website": "https://joseph4wy.com",
        "positions": {
            "ABORTION": "Pro-life, viewing life as sacred from conception, opposing all abortions except to save the mother's life.",
            "EDUCATION": "Supports parental rights and school choice, banning ideological indoctrination in public schools.",
            "RELIGIOUS-FREEDOM": "Protects faith-based expression and opposes government infringement on religious practice.",
            "GUNS": "Upholds Second Amendment as God-given right for self-defense.",
            "TAXES": "Advocates minimal taxation to preserve family resources and freedom.",
            "IMMIGRATION": "Secures borders to protect American sovereignty and resources.",
            "FAMILY-VALUES": "Defines marriage biblically, promotes nuclear families, and counters gender ideology.",
            "ELECTION-INTEGRITY": "Requires voter ID and paper trails for trustworthy elections."
        },
        "endorsements": ["Grassroots Conservatives of Wyoming"]
    },
    {
        "name": "Chuck Gray",
        "state": "Wyoming",
        "office": "Secretary of State",
        "party": "Republican",
        "bio": "Chuck Gray, elected Wyoming's 24th Secretary of State in 2022, oversees elections, business registrations, and securities. A former state representative since 2017, he sponsored Wyoming's voter ID law. Born around 1990, Gray moved to Wyoming in 2013 and focuses on election security and conservative principles. Married with children, he prioritizes transparency and limited government.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://sos.wyo.gov",
        "positions": {
            "ABORTION": "Pro-life, supports state restrictions.",
            "EDUCATION": "Backs parental rights in education.",
            "RELIGIOUS-FREEDOM": "Defends religious liberties.",
            "GUNS": "Supports Second Amendment protections.",
            "TAXES": "Favors low taxes and fiscal conservatism.",
            "IMMIGRATION": "Advocates border security.",
            "FAMILY-VALUES": "Upholds traditional family values.",
            "ELECTION-INTEGRITY": "Champion of voter ID, audits, and prohibiting foreign funding in elections."
        },
        "endorsements": ["Wyoming Republican Party"]
    },
    {
        "name": "Curt Meier",
        "state": "Wyoming",
        "office": "State Treasurer",
        "party": "Republican",
        "bio": "Curt Meier, sworn in as Wyoming's 31st State Treasurer in 2019, manages state investments and unclaimed property. A longtime state senator from 1995-2019, he has a background in farming and ranching in Newcastle. Born in 1953, Meier is committed to fiscal responsibility and taxpayer protection. Married with family, he serves on national treasurer associations.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://statetreasurer.wyo.gov",
        "positions": {
            "ABORTION": "Pro-life stance aligned with conservative values.",
            "EDUCATION": "Supports efficient funding for education.",
            "RELIGIOUS-FREEDOM": "Protects faith-based initiatives.",
            "GUNS": "Second Amendment defender.",
            "TAXES": "Strong advocate for low taxes and balanced budgets.",
            "IMMIGRATION": "Supports legal immigration and security.",
            "FAMILY-VALUES": "Promotes family-supporting policies.",
            "ELECTION-INTEGRITY": "Ensures fiscal oversight in elections."
        },
        "endorsements": ["National Association of State Treasurers"]
    },
    {
        "name": "Kristi Ellis",
        "state": "Wyoming",
        "office": "State Auditor",
        "party": "Republican",
        "bio": "Kristi Ellis, Wyoming's State Auditor since 2023, oversees financial audits and accountability. Elected in 2022, she has experience in state government and community leadership. A conservative focused on transparency, Ellis ensures taxpayer dollars are used efficiently. Family-oriented, she prioritizes Wyoming's fiscal health.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://sao.wyo.gov",
        "positions": {
            "ABORTION": "Pro-life supporter.",
            "EDUCATION": "Backs accountable education spending.",
            "RELIGIOUS-FREEDOM": "Defends religious protections.",
            "GUNS": "Supports gun rights.",
            "TAXES": "Emphasizes fiscal audits for tax efficiency.",
            "IMMIGRATION": "Favors secure policies.",
            "FAMILY-VALUES": "Upholds traditional values.",
            "ELECTION-INTEGRITY": "Promotes transparent financial reporting in elections."
        },
        "endorsements": ["Wyoming Farm Bureau"]
    },
    {
        "name": "Megan Degenfelder",
        "state": "Wyoming",
        "office": "Superintendent of Public Instruction",
        "party": "Republican",
        "bio": "Megan Degenfelder, Wyoming's Superintendent since 2023, is a sixth-generation Wyomingite from a ranching and oil family. A University of Wyoming graduate, she taught high school, served in the legislature, and focused on education policy. Elected in 2022, she prioritizes student outcomes and parental rights. Married with children, she advocates for Wyoming's kids.",
        "faith_statement": "No publicly disclosed faith statement.",
        "website": "https://edu.wyoming.gov",
        "positions": {
            "ABORTION": "Pro-life alignment.",
            "EDUCATION": "Expands school choice via ESAs, protects parental rights, bans CRT and gender ideology.",
            "RELIGIOUS-FREEDOM": "Supports faith-based education options.",
            "GUNS": "Respects Second Amendment in school safety contexts.",
            "TAXES": "Efficient education funding.",
            "IMMIGRATION": "Focuses on citizen students.",
            "FAMILY-VALUES": "Empowers families in education decisions.",
            "ELECTION-INTEGRITY": "Ensures fair school board elections."
        },
        "endorsements": ["Wyoming Education Association", "Heritage Foundation"]
    }
]

# Wyoming Summary
summary = {
    "state": "Wyoming",
    "title": "Wyoming 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Wyoming 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 7
**Total Candidates Profiled:** 9
**Election Dates:**
- 2026-08-18 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Wyoming POLITICAL LANDSCAPE

### **The Equality State**

Wyoming is a **deep-red conservative stronghold**:
- **Energy & Economy:** Powered by coal, oil, and gas, Wyoming leads in per-capita energy production, with conservatives fighting federal green mandates to protect jobs and low taxes.
- **Rural Values:** 90% rural land, emphasizing ranching, hunting, and self-reliance; conservatives dominate with GOP supermajorities in legislature.
- **Urban-Rural Divide:** Cheyenne and Casper lean moderate, but Albany and Laramie counties show liberal pockets; rural counties like Campbell and Sweetwater are staunchly conservative.
- **Frontier Spirit:** World's first to grant women suffrage, now a bastion for gun rights and limited government.

### **Why Wyoming Matters**

Wyoming is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Trigger law bans most abortions post-Roe, but faces court challenges; 2025 upheld restrictions, with 20+ pregnancy centers statewide.
- ✅ **Second Amendment:** Permitless carry since 2011, top-ranked gun rights; no assault weapon bans.
- ✅ **School Choice:** Launched ESA program in 2025 for 1,000+ students, expanding parental options amid homeschool growth.
- ✅ **Religious Liberty:** Strong protections via 2025 Educational Religious Freedom Act; low threats from urban areas.
- ✅ **Family Values:** Traditional marriage enshrined, parental consent for minors' care; opposes gender transitions for youth.
- ✅ **Election Integrity:** Voter ID mandatory since 2021, paper ballots, no mail-in expansions.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** Retaining this seat ensures conservative firewall against national progressive agendas on life, borders, and faith; Wyoming's voice in confirming judges vital.

**Cynthia Lummis (Republican)** - Incumbent Senator

**Faith Statement:** "I attend the Trinity Lutheran Church in Cheyenne, Wyoming. I am a strong Christian and my faith guides my decisions as a mother, friend, neighbor and public servant."

**Background:**
- Ranch-born, UW triple graduate in science and law.
- Former Treasurer, Congresswoman, Freedom Caucus founder.
- Manages family ranches; mother, grandmother.

**Christian Conservative Analysis:**
- **Pro-Life:** Cosponsored defund Planned Parenthood; 100% NRLC rating.
- **Religious Liberty:** Led campus faith protections bill.
- **Education/Parental Rights:** Opposes federal curricula mandates.
- **Family Values:** Biblical alignment on marriage, family policy.
- **Overall Assessment:** 9/10 - Principled Lutheran faith drives pro-family votes, though occasional bipartisan fiscal deals.

**Key Positions:**
- **ABORTION:** Strongly pro-life, supports defunding Planned Parenthood and advancing protections for the unborn at federal and state levels.
- **EDUCATION:** Advocates for school choice, parental rights, and opposing federal overreach in curricula to ensure local control.
- **RELIGIOUS FREEDOM:** Champions religious liberty, co-sponsoring bills to protect faith-based organizations and student groups on campuses.
- **GUNS:** Fierce defender of Second Amendment rights, opposes red-flag laws and supports national reciprocity for concealed carry.
- **TAXES:** Pushes for tax cuts, simplification, and eliminating the death tax to promote economic growth and family farms.
- **Energy Independence:** Fights green mandates to protect Wyoming jobs.

**Endorsements:** Gun Owners of America, National Right to Life, Family Research Council

**Website:** https://www.lummis.senate.gov

**Why It Matters:** Losing this seat risks federal assaults on Wyoming's pro-life laws and energy sector.

---

### **U.S. House At-Large** - 2026-11-03

**Context:** Sole representative amplifies Wyoming's rural voice; key for blocking gun control and advancing energy bills.

**Harriet Hageman (Republican)** - Incumbent Representative

**Faith Statement:** "Faith, freedom, and integrity guide everything I do. I align my votes with biblical principles as reflected in congressional scorecards."

**Background:**
- Ranch-raised litigator with 34 years fighting feds.
- UW law graduate, Supreme Court admitted.
- Chairs water/wildlife subcommittee; mother, rancher.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports state bans, opposes funding abortions.
- **Religious Liberty:** Backs resolutions protecting expression.
- **Education/Parental Rights:** Prioritizes family-led education.
- **Family Values:** Strong biblical family advocate.
- **Overall Assessment:** 9/10 - Rancher faith fuels anti-overreach fight.

**Key Positions:**
- **ABORTION:** Pro-life, supports state-level protections and opposes federal funding for abortion providers.
- **EDUCATION:** Prioritizes parental involvement and school choice, laser-focused on core education without ideological indoctrination.
- **RELIGIOUS FREEDOM:** Defends faith-based freedoms against government infringement, supporting resolutions to protect religious expression.
- **GUNS:** Staunch Second Amendment advocate, fights bureaucratic restrictions on gun ownership and carry rights.
- **TAXES:** Advocates for lower taxes and reduced federal spending to empower families and businesses.
- **Border Security:** Enforces strict border security, ends sanctuary policies.

**Endorsements:** NRA, Heritage Action, Susan B. Anthony Pro-Life America

**Website:** https://hageman.house.gov

**Why It Matters:** Secures Wyoming's firewall against D.C. liberalism.

---

## 🔴 2026 STATEWIDE RACES

### **Governor and Lieutenant Governor** - 2026-11-03

**Context:** Open seat post-Gordon; winner shapes pro-life enforcement, school choice expansion, and energy policy amid federal threats.

**Eric Barlow (Republican)** - State Senator

**Faith Statement:** "No publicly disclosed faith statement, though events feature prayers invoking divine guidance."

**Background:**
- Fifth-gen rancher, businessman from Gillette.
- Former House Speaker, energy/ag advocate.
- Married, children; rural values champion.

**Christian Conservative Analysis:**
- **Pro-Life:** Voted for trigger law enforcement.
- **Religious Liberty:** Supports faith protections.
- **Education/Parental Rights:** Backs choice programs.
- **Family Values:** Aligns with traditional stances.
- **Overall Assessment:** 8/10 - Conservative record strong, faith implied via events.

**Key Positions:**
- **ABORTION:** Pro-life, supports Wyoming's trigger law and opposes expansions.
- **EDUCATION:** Backs school choice and parental rights, opposing federal mandates.
- **RELIGIOUS FREEDOM:** Defends religious liberty against government overreach.
- **GUNS:** Strong Second Amendment supporter, advocates permitless carry.
- **TAXES:** Committed to low taxes and fiscal restraint to support families.
- **Energy:** Protects Wyoming's fossil fuels.

**Endorsements:** Wyoming Farm Bureau, Wyoming Stock Growers

**Website:** https://ericbarlow.com

**Brent Bien (Republican)** - Retired Marine Colonel

**Faith Statement:** "No publicly disclosed faith statement, but emphasizes defending traditional values and family."

**Background:**
- UW engineer, combat vet with 275 missions.
- Navy family; husband, father of three.
- Patriot focused on exceptionalism.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports unborn protections.
- **Religious Liberty:** Safeguards faith freedoms.
- **Education/Parental Rights:** Promotes choice.
- **Family Values:** Traditional family defender.
- **Overall Assessment:** 8/10 - Military discipline aligns with biblical valor.

**Key Positions:**
- **ABORTION:** Pro-life, supports protections for the unborn and family-centered policies.
- **EDUCATION:** Promotes school choice and parental involvement in education.
- **RELIGIOUS FREEDOM:** Safeguards religious liberties as foundational to freedom.
- **GUNS:** Defends Second Amendment rights unequivocally.
- **TAXES:** Advocates fiscal responsibility and low taxes for economic freedom.
- **Veterans:** Prioritizes military families.

**Endorsements:** Veterans for America First

**Website:** https://brentbien.com

**Joseph Kibler (Republican)** - Grassroots Activist

**Faith Statement:** "I believe the Scriptures are the fully inspired, error-free Word of God. Faith in Christ informs my decisions through Bible-based principles, including the Trinity, salvation by grace, male church leadership, and traditional marriage."

**Background:**
- Husband, father; community advocate.
- Speaks on property rights, recovery.
- Grassroots, anti-machine conservative.

**Christian Conservative Analysis:**
- **Pro-Life:** Views life sacred from conception.
- **Religious Liberty:** Opposes infringement.
- **Education/Parental Rights:** Bans indoctrination.
- **Family Values:** Biblical marriage/family.
- **Overall Assessment:** 10/10 - Explicit evangelical faith integrates politics.

**Key Positions:**
- **ABORTION:** Pro-life, opposing all except mother's life.
- **EDUCATION:** Supports rights, choice; bans CRT/gender ideology.
- **RELIGIOUS FREEDOM:** Protects faith expression.
- **GUNS:** God-given self-defense right.
- **TAXES:** Minimal to preserve family freedom.
- **Addiction:** Faith-based recovery support.

**Endorsements:** Grassroots Conservatives of Wyoming

**Website:** https://joseph4wy.com

**Why It Matters:** Governor enforces pro-family laws, from abortion bans to school reforms.

### **Secretary of State** - 2026-11-03

**Context:** Guards election sanctity; incumbent's voter ID push sets tone for secure 2026 vote.

**Chuck Gray (Republican)** - Incumbent

**Faith Statement:** "No publicly disclosed faith statement."

**Background:**
- Elected 2022, former Rep.
- Voter ID sponsor; family man.
- Focus: transparency, security.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports restrictions.
- **Religious Liberty:** Defends protections.
- **Education/Parental Rights:** Backs rights.
- **Family Values:** Traditional alignment.
- **Overall Assessment:** 8/10 - Election focus aids integrity.

**Key Positions:**
- **ABORTION:** Pro-life supporter.
- **EDUCATION:** Parental rights advocate.
- **RELIGIOUS FREEDOM:** Defends liberties.
- **GUNS:** Supports rights.
- **TAXES:** Fiscal conservatism.
- **ELECTION-INTEGRITY:** Voter ID, audits, no foreign funds.

**Endorsements:** Wyoming GOP

**Website:** https://sos.wyo.gov

**Why It Matters:** Prevents fraud, ensures Christian votes count.

### **State Treasurer** - 2026-11-03

**Context:** Manages funds for pro-life centers, schools; fiscal hawk needed.

**Curt Meier (Republican)** - Incumbent

**Faith Statement:** "No publicly disclosed faith statement."

**Background:**
- Senator 1995-2019, farmer/rancher.
- Sworn 2019; taxpayer champion.
- Newcastle roots, family.

**Christian Conservative Analysis:**
- **Pro-Life:** Conservative alignment.
- **Religious Liberty:** Supports initiatives.
- **Education/Parental Rights:** Efficient funding.
- **Family Values:** Family policies.
- **Overall Assessment:** 7/10 - Fiscal strength aids values.

**Key Positions:**
- **ABORTION:** Pro-life.
- **EDUCATION:** Accountable spending.
- **RELIGIOUS FREEDOM:** Protections.
- **GUNS:** Defender.
- **TAXES:** Low taxes, balanced budgets.
- **Investments:** Ethical, conservative.

**Endorsements:** NAST

**Website:** https://statetreasurer.wyo.gov

**Why It Matters:** Funds align with biblical stewardship.

### **State Auditor** - 2026-11-03

**Context:** Audits waste, ensures accountability for family programs.

**Kristi Ellis (Republican)** - Incumbent

**Faith Statement:** "No publicly disclosed faith statement."

**Background:**
- Elected 2022, government experience.
- Transparency focus; community leader.
- Family-oriented conservative.

**Christian Conservative Analysis:**
- **Pro-Life:** Supporter.
- **Religious Liberty:** Defends.
- **Education/Parental Rights:** Accountable.
- **Family Values:** Upholds.
- **Overall Assessment:** 7/10 - Audit role bolsters integrity.

**Key Positions:**
- **ABORTION:** Pro-life.
- **EDUCATION:** Fair funding.
- **RELIGIOUS FREEDOM:** Protections.
- **GUNS:** Rights.
- **TAXES:** Efficiency audits.
- **Accountability:** Taxpayer first.

**Endorsements:** Farm Bureau

**Website:** https://sao.wyo.gov

**Why It Matters:** Prevents corruption eroding values.

### **Superintendent of Public Instruction** - 2026-11-03

**Context:** Directs ESA growth, bans woke curricula; key for godly education.

**Megan Degenfelder (Republican)** - Incumbent

**Faith Statement:** "No publicly disclosed faith statement."

**Background:**
- 6th-gen rancher/oil family.
- UW grad, teacher, legislator.
- Mother; student outcomes focus.

**Christian Conservative Analysis:**
- **Pro-Life:** Alignment.
- **Religious Liberty:** Faith options.
- **Education/Parental Rights:** ESA champion.
- **Family Values:** Empowers families.
- **Overall Assessment:** 9/10 - Choice expands Christian schooling.

**Key Positions:**
- **ABORTION:** Pro-life.
- **EDUCATION:** ESAs, parental rights, bans CRT/gender.
- **RELIGIOUS FREEDOM:** Faith-based options.
- **GUNS:** School safety rights.
- **TAXES:** Efficient ed funding.
- **Outcomes:** Choices boost results.

**Endorsements:** Heritage, Ed Assoc.

**Website:** https://edu.wyoming.gov

**Why It Matters:** Shapes next gen's worldview.

---

## 🎯 KEY ISSUES FOR Wyoming CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Trigger law bans abortions post-15 weeks, upheld 2025; defunds Planned Parenthood.
- 25 pregnancy centers, adoption incentives.
- Parental consent for minors.
- No state funding for abortions.
- 2025 victory: Blocked expansion bills.

**Progressive Position:**
- Court challenges to trigger law via equal protection.
- Push for travel funding, provider shields.
- Union-backed expansions.

**Christian Conservative Action:**
- Join Wyoming Right to Life (wyrtl.org).
- Support HB 143 enforcement.
- Volunteer at centers like Alpha Center.
- Vote pro-life in primaries.

### **School Choice & Parental Rights**

**Conservative Position:**
- 2025 ESA for special needs, expanding to all; 1,500 participants.
- Parental rights law bans secrecy on gender transitions.
- CRT/gender bans in HB 206.
- Homeschool co-ops booming, 5% students.
- 2025 win: Religious freedom in schools.

**Progressive Position:**
- Union opposition to ESAs as 'vouchers for rich.'
- DEI mandates in teacher training.
- Threats to choice via funding cuts.

**Christian Conservative Action:**
- Run for school boards via Wyoming Family Alliance.
- Support SF 109 expansion.
- Join Parents Defending Education.
- Lobby for biblical curricula opt-outs.

### **Religious Freedom**

**Conservative Position:**
- 2025 Educational Religious Freedom Act protects student groups.
- No major threats; strong church exemptions.
- Faith-based foster care upheld.
- Recent win: Blocked anti-discrimination overreach.

**Progressive Position:**
- Urban pushes for LGBTQ+ mandates conflicting faith.
- School prayer challenges.
- Funding battles for secular programs.

**Christian Conservative Action:**
- Partner with Alliance Defending Freedom.
- Support HB 161 protections.
- Host church forums on liberty.
- Pray against erosion.

### **Guns**

**Conservative Position:**
- Permitless carry, constitutional carry top-ranked.
- No red flags, assault bans.
- School guardian programs.
- 2025: Preempted local restrictions.

**Progressive Position:**
- Urban calls for storage laws.
- Federal ATF challenges.
- Background check expansions.

**Christian Conservative Action:**
- Join Wyoming Gun Owners (wyominggunowners.org).
- Lobby against fed encroachments.
- Train church security teams.
- Vote NRA-endorsed.

### **Taxes**

**Conservative Position:**
- No income/sales tax; property low.
- 4% severance tax cut 2025.
- Surplus rebates to families.
- Recent: Blocked hikes.

**Progressive Position:**
- Push for income tax on wealthy.
- Green energy surcharges.
- Spending on social programs.

**Christian Conservative Action:**
- Support Wyoming Taxpayers Assoc.
- Oppose new taxes via petitions.
- Tithe wisely, steward resources.
- Elect fiscal hawks.

### **Immigration**

**Conservative Position:**
- State-federal cooperation, E-Verify for jobs.
- Border rancher aid.
- No sanctuary cities.
- 2025: Blocked DACA expansions.

**Progressive Position:**
- Refugee resettlement pushes.
- Driver licenses for illegals.
- Sanctuary in Laramie.

**Christian Conservative Action:**
- Aid legal immigrants via churches.
- Support SB 12 enforcement.
- Border prayer vigils.
- Vote secure-border candidates.

### **Family Values**

**Conservative Position:**
- Traditional marriage constitutional.
- Parental rights in medical/gender.
- Anti-porn library filters.
- 2025: Banned youth transitions.

**Progressive Position:**
- Gender-affirming care mandates.
- Same-sex adoption pushes.
- Drag events in schools.

**Christian Conservative Action:**
- Wyoming Family Alliance (wyomingfamily.org).
- Support HF 685 bans.
- Family devotions on values.
- Mobilize for purity laws.

### **Election Integrity**

**Conservative Position:**
- Voter ID, paper ballots since 2021.
- No mass mail-in; audits required.
- Banned ranked-choice 2025.
- Recent: Foreign funding ban.

**Progressive Position:**
- Automatic registration pushes.
- Drop boxes expansions.
- Challenges to ID laws.

**Christian Conservative Action:**
- Train poll watchers via True the Vote.
- Support Chuck Gray retention.
- Church reg drives.
- Pray for honest counts.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- **2026-05-14** - Voter registration deadline (continuous, but updates 14 days prior)
- **2026-07-15** - Early voting begins
- **2026-08-18** - Primary Election
- **2026-11-03** - General Election

**Voter Registration:** sos.wyo.gov (same-day at polls)

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
✅ **Share on social media** with #WyomingFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Wyoming CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Wyoming coverage
- **Wyoming Right to Life** - Pro-life ratings
- **Wyoming Family Alliance** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Wyoming Secretary of State**: sos.wyo.gov
- **County Election Offices**: Via county clerk websites
- **Early Voting Locations**: County clerk offices/polling sites

### **Conservative Organizations:**
- **Wyoming Right to Life**: wyrtl.org
- **Wyoming Family Alliance**: wyomingfamily.org
- **Wyoming Gun Owners**: wyominggunowners.org
- **Wyoming School Choice**: Via Dept of Ed
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Wyoming CHRISTIANS

**2026 Elections Matter:**
- Governor race determines pro-life enforcement.
- Senate/House affect federal border, gun laws.
- Supt impacts school gender policies.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Energy jobs preserved
✅ Low taxes sustained
✅ Rural families empowered

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Energy sector crippled
❌ Taxes hiked on families
❌ Urban liberalism dominates

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Cynthia Lummis, Harriet Hageman, Eric Barlow, Brent Bien, Joseph Kibler and families
- Wyoming Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Wyoming
- Revival and awakening in Wyoming
- God's will in Wyoming elections

**Scripture for Wyoming Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Wyoming coverage, email contact@ekewaka.com

**Wyoming CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Wyoming races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Wyoming'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Wyoming races...")
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

print(f"\nChecking for existing Wyoming candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Wyoming'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Wyoming candidates...")
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

print("\nProcessing Wyoming summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Wyoming'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Wyoming data upload complete!")