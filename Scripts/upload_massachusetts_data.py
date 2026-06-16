import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Massachusetts Races
races = [
    {
        "state": "Massachusetts",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Democratic Senator Ed Markey faces a primary challenge from Representative Seth Moulton, while Republicans see an opportunity to contest this deep-blue seat in a midterm election."
    },
    {
        "state": "Massachusetts",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Democratic Governor Maura Healey seeks re-election in a competitive Republican primary featuring business leaders and veterans aiming to flip the state executive."
    },
    {
        "state": "Massachusetts",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Elected on a joint ticket with the Governor, this race will determine the state's second-highest executive office amid debates on fiscal policy and social issues."
    },
    {
        "state": "Massachusetts",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Democratic Attorney General Andrea Campbell runs for re-election, focusing on reproductive rights and consumer protection in a state with strong progressive leanings."
    },
    {
        "state": "Massachusetts",
        "office": "Boston Mayor",
        "election_date": "2025-11-04",
        "race_type": "general",
        "description": "Incumbent Mayor Michelle Wu faces challenger Josh Kraft in this nonpartisan race for control of the state's largest city, influencing urban policies on housing and public safety."
    }
]

# Massachusetts Candidates  
candidates = [
    {
        "name": "Maura Healey",
        "state": "Massachusetts",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Maura Healey, born in 1971 in Newburyport, Massachusetts, is the state's first openly lesbian governor and a former Attorney General. A star basketball player at Harvard, she earned a law degree from Northeastern University and clerked for federal judges before joining the AG's office in 2001. As AG from 2015-2023, she sued the Trump administration over 80 times, championed consumer protections, and led on climate and LGBTQ+ rights. Elected governor in 2022 with 64% of the vote, Healey has focused on housing affordability, clean energy, and economic recovery post-COVID. Married to Joanna Goldman since 2020, she has no children but is an advocate for family leave and child care. Her accomplishments include expanding paid family leave and passing a $4 billion housing bond. Currently, she navigates budget challenges amid migrant influxes and education reforms. Healey's leadership emphasizes equity and progressive values, making her a national figure in Democratic politics.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.mass.gov/orgs/governors-office",
        "positions": {
            "ABORTION": "Strongly pro-choice; signed ROE Act in 2020 as AG to codify abortion rights up to viability, expanded access post-Dobbs, and opposes any restrictions.",
            "EDUCATION": "Supports public school funding increases, opposes widespread school choice vouchers, emphasizes equity in funding but limited parental opt-outs on curriculum.",
            "RELIGIOUS-FREEDOM": "Defends separation of church and state; supports LGBTQ+ rights over religious exemptions in adoption and health care.",
            "GUNS": "Advocates strict gun control; expanded red-flag laws, assault weapon bans, and licensing requirements as AG.",
            "TAXES": "Progressive taxation; raised taxes on high earners for education and child care, opposes broad cuts.",
            "IMMIGRATION": "Sanctuary state policies; provides benefits to undocumented immigrants, expanded driver's licenses for all.",
            "FAMILY-VALUES": "Supports same-sex marriage, gender-affirming care for minors, and comprehensive sex education including LGBTQ+ topics.",
            "ELECTION-INTEGRITY": "Opposes strict voter ID; expanded mail-in voting and automatic registration."
        },
        "endorsements": ["Planned Parenthood", "NARAL Pro-Choice Massachusetts", "Massachusetts Teachers Association"]
    },
    {
        "name": "Brian Shortsleeve",
        "state": "Massachusetts",
        "office": "Governor",
        "party": "Republican",
        "bio": "Brian Shortsleeve, a Marine Corps veteran and business leader, was born in Massachusetts and served as a combat engineer in the Gulf War, earning commendations for leadership. After military service, he built a career in finance and transportation, becoming CEO of a venture capital firm and serving as MBTA Chief Administrative Officer under Governor Charlie Baker from 2015-2019, where he reformed budgeting and operations. A father of three and husband, Shortsleeve emphasizes family and fiscal responsibility, drawing from his blue-collar roots. He launched his gubernatorial bid in May 2025, positioning himself as a reformer against 'Beacon Hill insiders.' His accomplishments include streamlining MBTA finances and growing his firm to manage $500 million in assets. Shortsleeve's campaign focuses on affordability, public safety, and ending sanctuary policies, appealing to suburban conservatives frustrated with high costs and crime.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://brianshortsleeve.com/",
        "positions": {
            "ABORTION": "Pro-life; supports restrictions after 15 weeks, parental consent, and defunding Planned Parenthood.",
            "EDUCATION": "Strongly supports school choice and vouchers; champions parental rights to opt out of controversial curricula like gender ideology.",
            "RELIGIOUS-FREEDOM": "Defends religious liberty; opposes mandates that infringe on faith-based organizations in adoption or health care.",
            "GUNS": "Firm 2nd Amendment defender; vows to veto gun control bills, streamline licensing, and protect lawful owners.",
            "TAXES": "Advocates deep tax cuts; eliminate surcharges, veto new taxes, and tie spending to outcomes.",
            "IMMIGRATION": "Secure borders; end sanctuary status, reform shelter laws, cooperate with federal enforcement.",
            "FAMILY-VALUES": "Traditional marriage advocate; protects parental rights, opposes gender transitions for minors.",
            "ELECTION-INTEGRITY": "Supports voter ID, paper ballots, and audits to prevent fraud."
        },
        "endorsements": ["Massachusetts Family Institute", "Massachusetts Citizens for Life", "NRA"]
    },
    {
        "name": "Michael Minogue",
        "state": "Massachusetts",
        "office": "Governor",
        "party": "Republican",
        "bio": "Michael Minogue, born in 1964 in New Jersey but a long-time Massachusetts resident, is a decorated Army Ranger veteran who served in combat operations. He founded Abiomed in 1981, growing it into a global medical device leader with $1 billion in revenue before selling to Johnson & Johnson in 2022. A husband and father of five, Minogue is a devout Catholic philanthropist supporting veterans and education. He entered politics as a Trump ally, hosting fundraisers and donating millions to GOP causes. Announcing his bid in October 2025, Minogue promises 'affordability, accountability, and opportunity,' critiquing Healey's spending. His accomplishments include saving thousands of lives through heart pump innovations and board service at Mass General. Minogue's campaign targets working families with promises of tax relief and economic growth.",
        "faith_statement": "Husband, father, veteran, believer...living with purpose (John 2:9-11). My faith guides my commitment to public service and family.",
        "website": "https://minogueforma.com/",
        "positions": {
            "ABORTION": "Pro-life from conception; supports heartbeat bills, ultrasound requirements, and alternatives to abortion funding.",
            "EDUCATION": "Expands school choice; empowers parents with veto power over indoctrination in schools.",
            "RELIGIOUS-FREEDOM": "Protects churches and faith groups from government overreach in conscience matters.",
            "GUNS": "2nd Amendment absolutist; opposes all infringements, supports concealed carry expansion.",
            "TAXES": "Flat tax proposal; slash corporate rates to attract jobs, eliminate income tax on overtime.",
            "IMMIGRATION": "Enforce laws; end benefits for illegals, build border wall support at state level.",
            "FAMILY-VALUES": "Biblical family model; bans gender ideology in schools, protects traditional marriage.",
            "ELECTION-INTEGRITY": "Voter ID mandatory; same-day voting, no mail-in expansions."
        },
        "endorsements": ["Massachusetts Family Institute", "Massachusetts Citizens for Life", "Federation for American Immigration Reform"]
    },
    {
        "name": "Ed Markey",
        "state": "Massachusetts",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Ed Markey, born in 1946 in Malden, Massachusetts, is a lifelong public servant and the state's senior senator since 2013, after 37 years in the House. A Catholic altar boy turned lawyer from Boston College, he clerked for a state court before winning his first election in 1976. Married to Susan Blumenthal with no children, Markey is known for environmental advocacy, co-authoring the Green New Deal. Re-elected in 2020 with 66%, he faces a 2026 primary from Seth Moulton. Accomplishments include the Affordable Care Act and Paris Climate Agreement. At 80, his tenure focuses on climate, tech regulation, and progressive causes amid generational debates.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.markey.senate.gov/",
        "positions": {
            "ABORTION": "Pro-choice; co-sponsor of bills to codify Roe, opposes any gestational limits.",
            "EDUCATION": "Fully funds public schools; against vouchers, supports federal DEI mandates.",
            "RELIGIOUS-FREEDOM": "Prioritizes LGBTQ+ protections over religious objections in federal law.",
            "GUNS": "Assault weapons ban supporter; universal background checks and red-flag laws.",
            "TAXES": "Raise on wealthy; close loopholes for corporations.",
            "IMMIGRATION": "Path to citizenship; opposes wall, supports DACA expansion.",
            "FAMILY-VALUES": "Same-sex marriage advocate; gender-affirming care access.",
            "ELECTION-INTEGRITY": "HR1 supporter; automatic registration, no ID requirements."
        },
        "endorsements": ["Sierra Club", "League of Conservation Voters", "Planned Parenthood"]
    },
    {
        "name": "Seth Moulton",
        "state": "Massachusetts",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Seth Moulton, born in 1978 in Salem, Massachusetts, is a Marine veteran who served four tours in Iraq, earning a Bronze Star. A Harvard and Kennedy School graduate, he worked in business before upsetting a 20-year incumbent in 2014 for the 6th District House seat. Married to Liz Moynihan with two daughters, Moulton is a moderate Democrat critiquing party extremes. His 2026 Senate bid against Markey emphasizes generational change. Accomplishments include VA reforms and infrastructure bills. Moulton's leadership blends military discipline with pragmatic policy.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://sethmoulton.com/",
        "positions": {
            "ABORTION": "Pro-choice; defends reproductive rights but notes personal moral qualms post-20 weeks.",
            "EDUCATION": "Invest in public education; limited school choice, supports charter schools.",
            "RELIGIOUS-FREEDOM": "Balances with civil rights; supports exemptions where possible.",
            "GUNS": "Assault weapons ban; background checks, but respects hunting rights.",
            "TAXES": "Targeted increases on ultra-wealthy; middle-class relief.",
            "IMMIGRATION": "Comprehensive reform; secure borders with humane paths.",
            "FAMILY-VALUES": "Supports marriage equality; parental involvement in education.",
            "ELECTION-INTEGRITY": "Modernize voting; secure systems without suppression."
        },
        "endorsements": ["VoteVets", "Everytown for Gun Safety", "Human Rights Campaign"]
    },
    {
        "name": "John Deaton",
        "state": "Massachusetts",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "John Deaton, a Navy veteran and cryptocurrency lawyer, was born in 1968 in Rhode Island but practices in Massachusetts. After military service, he built a firm specializing in blockchain, becoming a vocal advocate for crypto regulation. Married with three daughters, Deaton ran for Senate in 2024, garnering 40% against Warren. A cancer survivor, he emphasizes resilience. Poised for 2026, his campaign targets independents on economy and tech. Accomplishments include pro bono work for veterans and policy papers on digital assets.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://johndeatonforsenate.com/",
        "positions": {
            "ABORTION": "Pro-life with exceptions; supports 15-week limit, ultrasound mandates.",
            "EDUCATION": "School choice expansion; parental rights first in curriculum decisions.",
            "RELIGIOUS-FREEDOM": "Strong protections; against compelled speech on gender issues.",
            "GUNS": "2A supporter; oppose federal overreach, focus on mental health.",
            "TAXES": "Simplify code; cut rates, eliminate estate tax.",
            "IMMIGRATION": "Merit-based; secure borders, E-Verify nationwide.",
            "FAMILY-VALUES": "Traditional values; oppose transgender sports in girls' categories.",
            "ELECTION-INTEGRITY": "Voter ID, clean rolls; audit processes."
        },
        "endorsements": ["Massachusetts Family Institute", "National Right to Life", "Gun Owners of America"]
    },
    {
        "name": "Michelle Wu",
        "state": "Massachusetts",
        "office": "Boston Mayor",
        "party": "Democrat",
        "bio": "Michelle Wu, born in 1985 in Chicago to Taiwanese immigrants, moved to Boston for Harvard Law. Elected to City Council in 2013, she became the first Asian-American woman mayor in 2021 with 64% of the vote. Mother of three young children with Conor Pewarski, Wu focuses on family policies like free preschool. As mayor, she implemented rent control, free MBTA fares for youth, and climate initiatives. Her upbringing in immigrant communities shapes her equity focus. Facing re-election in 2025, Wu navigates housing crises and public safety debates.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.boston.gov/departments/mayors-office",
        "positions": {
            "ABORTION": "Pro-choice advocate; expanded clinic access, sued Trump over funding cuts.",
            "EDUCATION": "Universal pre-K; opposes privatization, integrates DEI in curriculum.",
            "RELIGIOUS-FREEDOM": "Supports inclusive policies; faith leaders in equity councils.",
            "GUNS": "Strict controls; licensing reforms, violence interrupter programs.",
            "TAXES": "Progressive; commercial rent stabilization, millionaire's tax support.",
            "IMMIGRATION": "Sanctuary city; aid for immigrants, opposes ICE cooperation.",
            "FAMILY-VALUES": "LGBTQ+ inclusive; gender-neutral facilities, family leave expansion.",
            "ELECTION-INTEGRITY": "Ranked-choice voting; accessible polling."
        },
        "endorsements": ["Planned Parenthood", "Boston Teachers Union", "GLAAD"]
    },
    {
        "name": "Josh Kraft",
        "state": "Massachusetts",
        "office": "Boston Mayor",
        "party": "Democrat",
        "bio": "Josh Kraft, born in 1967, is the son of Patriots owner Robert Kraft and a nonprofit leader. Harvard-educated, he headed the Patriots Foundation, raising millions for education and health. With wife Jessica and four children, Kraft's philanthropy includes criminal justice reform. Entering politics in 2025, he challenges Wu on affordability and safety. His business acumen promises pragmatic governance. Accomplishments: Launched Read Boston literacy program, serving 10,000 kids.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://joshforboston.com/",
        "positions": {
            "ABORTION": "Pro-choice; supports access in urban health care.",
            "EDUCATION": "Boost public funding; partnerships with charters for choice.",
            "RELIGIOUS-FREEDOM": "Collaborative with faith communities on social services.",
            "GUNS": "Common-sense reforms; focus on illegal trafficking.",
            "TAXES": "Balanced budget; incentives for development.",
            "IMMIGRATION": "Humane policies; integration support.",
            "FAMILY-VALUES": "Family-first; affordable child care.",
            "ELECTION-INTEGRITY": "Secure, accessible voting."
        },
        "endorsements": ["Boston Chamber of Commerce", "AFT", "Mass League of Women Voters"]
    },
    {
        "name": "Andrea Campbell",
        "state": "Massachusetts",
        "office": "Attorney General",
        "party": "Democrat",
        "bio": "Andrea Campbell, born in 1982 in Boston's Roxbury, is the daughter of a single mother and civil rights activist. Boston College Law grad, she served on City Council before winning AG in 2022. Married with two children, Campbell prioritizes justice reform. As AG, she sued opioid makers and protected abortion access. Her 2026 re-election focuses on Trump-era fights. Accomplishments: $600 million opioid settlement.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.mass.gov/orgs/office-of-attorney-general-andrea-joy-campbell",
        "positions": {
            "ABORTION": "Defender of rights; shield laws for providers.",
            "EDUCATION": "Equity focus; anti-discrimination suits.",
            "RELIGIOUS-FREEDOM": "Balanced with civil rights.",
            "GUNS": "Enforces strict laws; ghost gun bans.",
            "TAXES": "Consumer protection from scams.",
            "IMMIGRATION": "Opposes federal overreach.",
            "FAMILY-VALUES": "DV protections, LGBTQ+ rights.",
            "ELECTION-INTEGRITY": "Voting rights enforcement."
        },
        "endorsements": ["NAACP", "ACLU", "NARAL"]
    }
]

# Massachusetts Summary
summary = {
    "state": "Massachusetts",
    "title": "Massachusetts 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Massachusetts 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 5
**Total Candidates Profiled:** 9
**Election Dates:**
- 2025-11-04 (Boston Municipal General)
- 2026-09-01 (State Primary)
- 2026-11-03 (Statewide General)

---

## 🔴 Massachusetts POLITICAL LANDSCAPE

### **The Bay State**

Massachusetts is a **deep-blue Democratic stronghold**:
- **Progressive Policies:** Dominated by liberal elites in Boston and Cambridge, with strong unions and academia driving agendas on climate, abortion, and LGBTQ+ rights.
- **Legacy Influences:** Kennedy family shadow lingers, but shifted to radical progressivism under Healey, emphasizing equity over individual liberties.
- **Urban-Rural Divide:** Boston and suburbs lean left (Suffolk, Middlesex counties), while western rural areas (Berkshires, Plymouth) offer conservative pockets.
- **Unique State Factor:** Highest-in-nation education spending yet failing schools; sanctuary policies strain budgets with migrant costs exceeding $1B annually.

### **Why Massachusetts Matters**

Massachusetts is **WINNABLE** for Christian conservatives:
- ✅ **Pro-Life Leadership:** ROE Act codified unlimited abortion, but 2024 ballot failure shows cracks; push for parental consent.
- ✅ **Second Amendment:** Strictest laws (2nd toughest nationally); fight assault bans, expand carry rights.
- ✅ **School Choice:** Limited inter-district options; expand vouchers against teachers' unions.
- ✅ **Religious Liberty:** Threats from gender mandates; protect faith adoptions, church autonomy.
- ✅ **Family Values:** Same-sex marriage pioneer; defend traditional definitions, ban youth transitions.
- ✅ **Economic Freedom:** High taxes drive exodus; cut rates to retain families.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** This seat held by 79-year-old Ed Markey since 2013 is a prime target for generational change and conservative incursion in a state that hasn't elected a GOP senator since 1971. The race impacts national climate and tech policy, with Markey's Green New Deal clashing against fiscal conservatives.

**Ed Markey (Democrat)** - Incumbent Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Lifelong politician from Malden, Catholic roots but secular policy focus.
- Harvard Law grad, House member 1976-2013.
- Married, no children; environmental crusader.

**Christian Conservative Analysis:**
- **Pro-Life:** F grade; co-sponsors federal abortion expansions, opposes Hyde Amendment.
- **Religious Liberty:** Weak; prioritizes secularism over faith exemptions.
- **Education/Parental Rights:** Union ally; blocks choice expansions.
- **Family Values:** Supports gender ideology in schools.
- **Overall Assessment:** 2/10 - Ideological opponent to biblical principles.

**Key Positions:**
- **ABORTION:** Codify Roe federally; no limits.
- **EDUCATION:** Federal funding for DEI; no vouchers.
- **RELIGIOUS FREEDOM:** Subordinate to civil rights laws.
- **GUNS:** Ban assault weapons.
- **TAXES:** Soak the rich.

**Endorsements:** Sierra Club, Planned Parenthood

**Website:** https://www.markey.senate.gov/

**Seth Moulton (Democrat)** - Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Iraq vet, Harvard/Kennedy grad.
- Moderate Dem, family man with two daughters.
- House since 2015.

**Christian Conservative Analysis:**
- **Pro-Life:** Mixed; pro-choice but conscience on late-term.
- **Religious Liberty:** Better balance than Markey.
- **Education/Parental Rights:** Supports charters.
- **Family Values:** Marriage equality supporter.
- **Overall Assessment:** 4/10 - Moderate but still progressive.

**Key Positions:**
- **ABORTION:** Defend rights with exceptions.
- **EDUCATION:** Invest in publics, some choice.
- **RELIGIOUS FREEDOM:** Case-by-case exemptions.
- **GUNS:** Background checks.
- **TAXES:** Middle-class cuts.

**Endorsements:** VoteVets, Everytown

**Website:** https://sethmoulton.com/

**John Deaton (Republican)** - Attorney

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Navy vet, crypto lawyer, cancer survivor.
- Father of three, 2024 nominee.
- Resilience story.

**Christian Conservative Analysis:**
- **Pro-Life:** Solid record; supports limits.
- **Religious Liberty:** Strong defender.
- **Education/Parental Rights:** Choice advocate.
- **Family Values:** Traditional stances.
- **Overall Assessment:** 8/10 - Aligned on core issues.

**Key Positions:**
- **ABORTION:** 15-week ban.
- **EDUCATION:** Vouchers, opt-outs.
- **RELIGIOUS FREEDOM:** Protect conscience.
- **GUNS:** No federal bans.
- **TAXES:** Simplify, cut.

**Endorsements:** Massachusetts Family Institute, NRA

**Website:** https://johndeatonforsenate.com/

**Why It Matters:** Flipping this seat halts radical climate spending, advances pro-life federal protections.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** Healey's re-election tests GOP unity in primary; winner shapes state on abortion shields, taxes, and borders amid $50B budget.

**Maura Healey (Democrat)** - Incumbent Governor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Ex-AG, Harvard athlete.
- Lesbian married, no kids.
- Progressive icon.

**Christian Conservative Analysis:**
- **Pro-Life:** Zero; expanded abortion access.
- **Religious Liberty:** Hostile to exemptions.
- **Education/Parental Rights:** Union-backed.
- **Family Values:** Redefines family.
- **Overall Assessment:** 1/10 - Anti-faith agenda.

**Key Positions:**
- **ABORTION:** Unlimited access.
- **EDUCATION:** Equity over choice.
- **RELIGIOUS FREEDOM:** LGBTQ+ priority.
- **GUNS:** Strict licensing.
- **TAXES:** Hike on rich.
- **IMMIGRATION:** Sanctuary expansion.

**Endorsements:** NARAL, MTA

**Website:** https://www.mass.gov/orgs/governors-office

**Brian Shortsleeve (Republican)** - Veteran/CEO

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Marine vet, MBTA reformer.
- Father of three.
- Business leader.

**Christian Conservative Analysis:**
- **Pro-Life:** Committed restrictor.
- **Religious Liberty:** Defender.
- **Education/Parental Rights:** Strong choice.
- **Family Values:** Traditional.
- **Overall Assessment:** 7/10 - Solid reformer.

**Key Positions:**
- **ABORTION:** Post-15 week limits.
- **EDUCATION:** Vouchers.
- **RELIGIOUS FREEDOM:** Protect churches.
- **GUNS:** Full 2A.
- **TAXES:** Cuts across board.
- **IMMIGRATION:** End sanctuary.

**Endorsements:** MCFL, MFI

**Website:** https://brianshortsleeve.com/

**Michael Minogue (Republican)** - CEO/Veteran

**Faith Statement:** "Husband, father, veteran, believer...living with purpose (John 2:9-11). My faith guides my commitment to public service and family."

**Background:**
- Abiomed founder, Army Ranger.
- Father of five, Catholic.
- Trump donor.

**Christian Conservative Analysis:**
- **Pro-Life:** From conception.
- **Religious Liberty:** Biblical priority.
- **Education/Parental Rights:** Opt-out rights.
- **Family Values:** Biblical model.
- **Overall Assessment:** 9/10 - Faith-driven leader.

**Key Positions:**
- **ABORTION:** Heartbeat ban.
- **EDUCATION:** Parental veto.
- **RELIGIOUS FREEDOM:** No overreach.
- **GUNS:** Absolutist.
- **TAXES:** Flat tax.
- **IMMIGRATION:** Enforce laws.

**Endorsements:** MFI, NRA

**Website:** https://minogueforma.com/

**Why It Matters:** GOP win restores fiscal sanity, protects life from Beacon Hill radicals.

### **Attorney General** - 2026-11-03

**Context:** Campbell's role in shielding abortion clinics makes this a flashpoint for pro-life advocates seeking accountability.

**Andrea Campbell (Democrat)** - Incumbent AG

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Roxbury native, BC Law.
- Mother of two.
- Justice reformer.

**Christian Conservative Analysis:**
- **Pro-Life:** Adversary; sues pro-life groups.
- **Religious Liberty:** Weak.
- **Education/Parental Rights:** N/A.
- **Family Values:** Progressive.
- **Overall Assessment:** 2/10 - Rights enforcer against conservatives.

**Key Positions:**
- **ABORTION:** Shield providers.
- **EDUCATION:** Anti-discrimination.
- **RELIGIOUS FREEDOM:** Civil rights first.
- **GUNS:** Enforce bans.
- **TAXES:** Consumer suits.
- **IMMIGRATION:** Protect migrants.

**Endorsements:** ACLU, NAACP

**Website:** https://www.mass.gov/orgs/office-of-attorney-general-andrea-joy-campbell

**Why It Matters:** Conservative AG ends weaponized law against faith and family.

---

## 🔴 2025 MUNICIPAL RACES

### **Boston Mayor** - 2025-11-04

**Context:** Wu's progressive policies on housing and safety divide the city; Kraft offers centrist alternative in diverse electorate.

**Michelle Wu (Democrat)** - Incumbent Mayor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Taiwanese immigrant, Harvard Law.
- Mother of three.
- Council to mayor.

**Christian Conservative Analysis:**
- **Pro-Life:** Opposes restrictions.
- **Religious Liberty:** Inclusive but secular.
- **Education/Parental Rights:** DEI push.
- **Family Values:** Gender-neutral.
- **Overall Assessment:** 3/10 - Urban progressive.

**Key Positions:**
- **ABORTION:** Clinic protections.
- **EDUCATION:** Free pre-K, DEI.
- **RELIGIOUS FREEDOM:** Faith in equity.
- **GUNS:** Violence prevention.
- **TAXES:** Rent control.
- **IMMIGRATION:** Sanctuary.

**Endorsements:** Planned Parenthood, BTU

**Website:** https://www.boston.gov/departments/mayors-office

**Josh Kraft (Democrat)** - Philanthropist

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Kraft heir, nonprofit head.
- Father of four.
- Patriots Foundation.

**Christian Conservative Analysis:**
- **Pro-Life:** Standard pro-choice.
- **Religious Liberty:** Collaborative.
- **Education/Parental Rights:** Partnerships.
- **Family Values:** Family-first.
- **Overall Assessment:** 5/10 - Pragmatic moderate.

**Key Positions:**
- **ABORTION:** Access support.
- **EDUCATION:** Charters.
- **RELIGIOUS FREEDOM:** Community ties.
- **GUNS:** Trafficking focus.
- **TAXES:** Incentives.
- **IMMIGRATION:** Integration.

**Endorsements:** Chamber, AFT

**Website:** https://joshforboston.com/

**Why It Matters:** Boston's mayor influences state trends on family and safety.

---

## 🎯 KEY ISSUES FOR Massachusetts CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Challenge ROE Act's unlimited abortions; push H.510 for 24-week limit.
- 150+ pregnancy centers via MCFL network.
- Require parental consent for minors.
- Defund abortion via state budget fights.
- 2024 ballot loss shows voter shift.

**Progressive Position:**
- Abortion as 'health care' up to birth; Healey's shield law hides out-of-state seekers.
- Fund Planned Parenthood $10M+ annually.
- Block consent bills.

**Christian Conservative Action:**
- Join Massachusetts Citizens for Life (masscitizensforlife.org).
- Support H.414 parental notification.
- Volunteer at crisis centers.
- Vote pro-life in all races.

### **School Choice & Parental Rights**

**Conservative Position:**
- Expand METCO inter-district to true vouchers; $100M for ESAs.
- Parental Rights Act (S.172) bans secret gender transitions.
- No CRT/gender lessons without opt-out.
- Homeschool deregulation.
- 2025 win: SCOTUS opt-out ruling applied.

**Progressive Position:**
- Union control via MTA; $7B public spend, no choice.
- DEI mandates in all districts.
- Secret policies per court ruling.

**Christian Conservative Action:**
- Run for school boards via MFI.
- Back S.172.
- Join Pioneer Institute (pioneerinstitute.org).

### **Religious Freedom**

**Conservative Position:**
- Protect faith adoptions from state interference.
- Exempt churches from gender mandates.
- Defend prayer in schools.
- Recent: ADF wins against pronoun laws.

**Progressive Position:**
- Compel speech; lawsuits against exemptions.
- Ban conversion therapy.
- Secular curricula.

**Christian Conservative Action:**
- Support First Liberty cases.
- Lobby H.2263 exemptions.
- Join Alliance Defending Freedom.

### **Guns**

**Conservative Position:**
- Repeal assault ban (Ch. 180); constitutional carry.
- GOAL fights licensing delays.
- Focus criminals, not owners.

**Progressive Position:**
- 2nd toughest laws; red-flag expansions.
- Ban large magazines.
- Post-2024: More restrictions.

**Christian Conservative Action:**
- Join GOAL (goal.org).
- Oppose H.0019.
- Train responsibly.

### **Taxes**

**Conservative Position:**
- Cut income tax from 5% to 4%; eliminate surtax.
- Property relief for seniors.
- FAIR Share failed; push rebates.

**Progressive Position:**
- Millionaire's tax adds $1B; hike sales/gas.
- Spend on migrants.

**Christian Conservative Action:**
- Support MFI tax reform.
- Vote fiscal hawks.
- Contact reps on S.1 budget.

### **Immigration**

**Conservative Position:**
- End sanctuary; roll back Lunn decision.
- E-Verify for jobs.
- Reform Right to Shelter.

**Progressive Position:**
- $1B+ on hotels; licenses for all.
- Resist ICE.

**Christian Conservative Action:**
- Back FAIR (fairus.org/MA).
- Push H.2870.
- Report fraud.

### **Family Values**

**Conservative Position:**
- Define marriage traditionally; ban youth hormones.
- Protect women's sports.
- MCFL family programs.

**Progressive Position:**
- Gender ideology in schools; transitions funded.
- Polyamory recognition pushes.

**Christian Conservative Action:**
- MFI marriage defense.
- Oppose H.2950.
- Home educate.

### **Election Integrity**

**Conservative Position:**
- Voter ID; paper trails.
- Clean rolls via ERIC opt-out.
- Audit 2024 anomalies.

**Progressive Position:**
- No ID; mail-in universal.
- Automatic registration.

**Christian Conservative Action:**
- Join Election Integrity MA.
- Volunteer watchers.
- Support S.1284 ID bill.

---

## 📅 CRITICAL DATES

**2025-2026 Election Calendar:**
- 2025-10-25 - Voter registration deadline (Boston General)
- 2025-10-27 - Early voting begins (Boston)
- 2026-08-24 - Primary registration deadline
- 2026-09-01 - Primary Election
- 2026-10-24 - General registration deadline
- 2026-11-03 - General Election

**Voter Registration:** Register at registertovotema.gov or sec.state.ma.us

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
✅ **Share on social media** with #MAFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Massachusetts CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Massachusetts coverage
- **Massachusetts Citizens for Life** - Pro-life ratings
- **Massachusetts Family Institute** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Massachusetts Secretary of State**: sec.state.ma.us
- **County Election Offices**: Search via sec.state.ma.us/divisions/elections
- **Early Voting Locations**: Check voteearlyma.com

### **Conservative Organizations:**
- **Massachusetts Citizens for Life**: masscitizensforlife.org
- **Massachusetts Family Institute**: mafamily.org
- **Gun Owners' Action League**: goal.org
- **Pioneer Institute**: pioneerinstitute.org
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Massachusetts CHRISTIANS

**2025-2026 Elections Matter:**
- U.S. Senate determines federal pro-life blocks.
- Governor race affects abortion shields, taxes.
- Boston Mayor impacts urban family policies.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Tax relief for families
✅ End to sanctuary burdens
✅ Economic revival

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Tax hikes on working families
❌ Migrant costs explode
❌ Indoctrination in classrooms

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Maura Healey, Brian Shortsleeve, Michael Minogue and families
- Massachusetts Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Massachusetts
- Revival and awakening in Massachusetts
- God's will in Massachusetts elections

**Scripture for Massachusetts Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Massachusetts coverage, email contact@ekewaka.com

**Massachusetts CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Massachusetts races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Massachusetts'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Massachusetts races...")
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

print(f"\nChecking for existing Massachusetts candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Massachusetts'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Massachusetts candidates...")
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

print("\nProcessing Massachusetts summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Massachusetts'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Massachusetts data upload complete!")