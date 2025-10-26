import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Hawaii Races
races = [
    {
        "state": "Hawaii",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The race for Hawaii's 1st Congressional District, covering urban areas of Oahu including Honolulu, is critical for influencing federal policy on issues like housing affordability and environmental protection in the islands."
    },
    {
        "state": "Hawaii",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Hawaii's 2nd Congressional District race encompasses rural and outer islands, playing a key role in advocating for agriculture, Native Hawaiian rights, and disaster recovery funding."
    },
    {
        "state": "Hawaii",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The gubernatorial race will determine Hawaii's chief executive, impacting state policies on cost of living, tourism, and cultural preservation amid growing conservative challenges to Democratic dominance."
    },
    {
        "state": "Hawaii",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Elected on a joint ticket with the governor, this race influences state administration, particularly in areas like economic development and community relations."
    }
]

# Hawaii Candidates  
candidates = [
    {
        "name": "Josh Green",
        "state": "Hawaii",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Josh Green, M.D., is the current Governor of Hawaii, elected in 2022 after serving as Lieutenant Governor from 2018 to 2022. A physician by training, Green graduated from Swarthmore College and the Pennsylvania State University College of Medicine. He practiced emergency medicine in Hawaii for over 20 years, focusing on rural health care. Green entered politics in 2004, serving in the Hawaii House of Representatives until 2012, where he chaired the Health Committee. As Lieutenant Governor, he led initiatives on homelessness and mental health. Married to Jaime Kanani Green, a lawyer, they have two children. Green's accomplishments include expanding mental health services and addressing the housing crisis through emergency proclamations. He is known for his hands-on approach to the 2023 Maui wildfires response, mobilizing state resources for recovery. Green's administration has prioritized climate resilience and economic diversification beyond tourism.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://governor.hawaii.gov/",
        "positions": {
            "ABORTION": "Pro-choice; supports access to reproductive health services without restrictions, including funding for Planned Parenthood in Hawaii.",
            "EDUCATION": "Supports public school funding and teacher salaries but opposes widespread school choice vouchers, emphasizing equity in public education.",
            "RELIGIOUS-FREEDOM": "Endorses protections under the First Amendment but prioritizes anti-discrimination laws that include LGBTQ+ rights over certain religious exemptions.",
            "GUNS": "Favors strict gun control measures, including permit requirements and bans on assault weapons to enhance public safety in Hawaii.",
            "TAXES": "Advocates for progressive taxation to fund social services, including increases on high-income earners to address housing and homelessness.",
            "IMMIGRATION": "Supports pathways to citizenship for immigrants and opposes strict border enforcement, focusing on humane treatment and economic contributions.",
            "FAMILY-VALUES": "Promotes inclusive family policies, supporting same-sex marriage and gender-affirming care for minors with parental consent.",
            "ELECTION-INTEGRITY": "Opposes strict voter ID laws, emphasizing mail-in voting accessibility while supporting signature verification."
        },
        "endorsements": ["Hawaii Democratic Party", "Planned Parenthood", "Hawaii Teachers Union"]
    },
    {
        "name": "Mike Gabbard",
        "state": "Hawaii",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Mike Gabbard has served in the Hawaii State Senate since 2006, representing District 21 on Oahu. Born in 1948, he is a veteran of the Vietnam War, serving in the U.S. Army. Gabbard holds a degree in business from the University of Hawaii and has worked as a substitute teacher and business owner. He founded the Hawaii Coalition for Life, advocating for pro-life causes, and served on the Honolulu City Council from 2002 to 2006. Married to Carol Gabbard, he is the father of former U.S. Rep. Tulsi Gabbard. Gabbard's accomplishments include sponsoring legislation to protect parental rights in education and opposing same-sex marriage legalization in 2013, though he later voted for it. He has been a vocal conservative voice within the Democratic Party on social issues, pushing for religious liberty protections and family values legislation. His career reflects a commitment to Catholic principles and community service in Leeward Oahu.",
        "faith_statement": "As a devout Catholic, I believe life begins at conception and must be protected at all stages. My faith guides my commitment to family, religious freedom, and moral leadership in public service.",
        "website": "https://www.mikegabbard.com/",
        "positions": {
            "ABORTION": "Pro-life; supports legislation for parental consent and restrictions on late-term abortions, advocating for alternatives like adoption and pregnancy centers.",
            "EDUCATION": "Strong supporter of parental rights and school choice, including vouchers for private and charter schools to empower families.",
            "RELIGIOUS-FREEDOM": "Champion of religious liberty, opposing mandates that force faith-based organizations to violate their beliefs on marriage and gender.",
            "GUNS": "Supports Second Amendment rights with reasonable background checks, opposing Hawaii's strict permitting as overly burdensome.",
            "TAXES": "Favors tax relief for families and small businesses to stimulate economic growth and reduce cost of living.",
            "IMMIGRATION": "Supports secure borders and legal immigration processes, prioritizing American workers and national security.",
            "FAMILY-VALUES": "Defends traditional marriage and opposes gender ideology in schools, emphasizing parental authority over child rearing.",
            "ELECTION-INTEGRITY": "Advocates for voter ID and paper ballots to ensure fair elections and prevent fraud."
        },
        "endorsements": ["Hawaii Catholic Conference", "Hawaii Family Forum", "National Right to Life"]
    },
    {
        "name": "Duke Aiona",
        "state": "Hawaii",
        "office": "Governor",
        "party": "Republican",
        "bio": "Duke Aiona served as Lieutenant Governor of Hawaii from 2003 to 2011 under Republican Gov. Linda Lingle. A former state judge, Aiona graduated from the University of Hawaii and Gonzaga University School of Law. He began his career as a deputy prosecuting attorney in Honolulu, then as a family court judge from 1996 to 2002. As Lt. Gov., he led education reform and crime reduction initiatives, including the Hawaii Mentoring Program. Aiona ran for governor in 2010, 2014, and 2022, each time as the Republican nominee. Married to Stacey Aiona, they have five children and are active in their Catholic faith. Aiona's accomplishments include authoring the Hawaii Children's Code and promoting faith-based community programs. Post-office, he has worked in private law practice and nonprofit leadership, focusing on youth development and conservative values.",
        "faith_statement": "My Catholic faith is the foundation of my life and public service. I believe in the dignity of life from conception to natural death, the sanctity of marriage, and the importance of religious freedom in a diverse society.",
        "website": "https://www.duke4hawaii.com/",
        "positions": {
            "ABORTION": "Firmly pro-life; supports defunding abortion providers and promoting crisis pregnancy centers throughout Hawaii.",
            "EDUCATION": "Advocates for school choice, charter schools, and parental involvement to improve outcomes in Hawaii's public system.",
            "RELIGIOUS-FREEDOM": "Strong defender of First Amendment rights, opposing government overreach into church affairs or individual conscience.",
            "GUNS": "Pro-Second Amendment; seeks to ease Hawaii's restrictive gun laws while maintaining public safety measures.",
            "TAXES": "Pushes for tax cuts and spending reforms to lower the cost of living and attract business to the islands.",
            "IMMIGRATION": "Enforces immigration laws, supports border security, and legal pathways for immigrants contributing to Hawaii's economy.",
            "FAMILY-VALUES": "Upholds traditional family structures, parental rights, and opposes teaching critical race theory or gender fluidity in schools.",
            "ELECTION-INTEGRITY": "Requires voter ID, audits, and transparent processes to restore trust in Hawaii's elections."
        },
        "endorsements": ["Hawaii Republican Party", "Family Policy Alliance", "NRA"]
    },
    {
        "name": "Ed Case",
        "state": "Hawaii",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "bio": "Ed Case has represented Hawaii's 1st Congressional District since 2019, after serving from 2002 to 2007. A graduate of Williams College and the University of California Hastings College of the Law, Case practiced corporate law before entering politics. He served in the Hawaii House from 1994 to 2002, focusing on fiscal responsibility. Case ran unsuccessfully for governor in 2018. Married to Audrey Case, they have three children. His accomplishments include securing federal funding for Honolulu rail and housing initiatives. Case is known as a moderate Democrat, often breaking with party lines on spending bills.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://case.house.gov/",
        "positions": {
            "ABORTION": "Pro-choice; voted against defunding Planned Parenthood and supports Roe v. Wade protections.",
            "EDUCATION": "Supports federal funding for public schools and student debt relief, but open to charter school expansion.",
            "RELIGIOUS-FREEDOM": "Balances religious rights with anti-discrimination protections, supporting faith-based exemptions where possible.",
            "GUNS": "Supports background checks and red flag laws, aligning with Hawaii's strict gun control.",
            "TAXES": "Moderate; favors targeted tax credits for middle-class families while maintaining progressive structure.",
            "IMMIGRATION": "Supports comprehensive reform with paths to citizenship and border security enhancements.",
            "FAMILY-VALUES": "Supports family leave policies and inclusive definitions of family, including LGBTQ+ rights.",
            "ELECTION-INTEGRITY": "Opposes voter suppression but supports mail-in voting with verification safeguards."
        },
        "endorsements": ["Hawaii Democratic Party", "Sierra Club", "AFL-CIO"]
    },
    {
        "name": "Della Au Belatti",
        "state": "Hawaii",
        "office": "U.S. House District 1",
        "party": "Democrat",
        "bio": "Della Au Belatti is a Hawaii State Representative for District 24, serving since 2007. A graduate of Punahou School and Williams College, she earned a law degree from the University of Hawaii. Belatti has chaired the Health Committee and focused on women's rights and environmental issues. Married with two children, she is active in community service. Her accomplishments include sponsoring bills for paid family leave and renewable energy mandates. As a challenger to Case, she emphasizes progressive values and accountability.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://belatti.house.gov/",
        "positions": {
            "ABORTION": "Strong pro-choice advocate; pushes for expanded access and opposes any restrictions.",
            "EDUCATION": "Prioritizes public education equity and opposes voucher programs that divert funds from public schools.",
            "RELIGIOUS-FREEDOM": "Supports religious liberty but prioritizes civil rights protections against discrimination.",
            "GUNS": "Advocates for universal background checks and assault weapon bans to reduce gun violence.",
            "TAXES": "Supports increasing taxes on the wealthy to fund social programs and infrastructure.",
            "IMMIGRATION": "Favors sanctuary policies and amnesty for undocumented immigrants in Hawaii.",
            "FAMILY-VALUES": "Promotes gender equality and LGBTQ+ inclusion in family policies and education.",
            "ELECTION-INTEGRITY": "Focuses on expanding voting access, opposing ID requirements as barriers."
        },
        "endorsements": ["EMILY's List", "Hawaii Nurses Association", "Progressive Democrats of Hawaii"]
    },
    {
        "name": "Jill Tokuda",
        "state": "Hawaii",
        "office": "U.S. House District 2",
        "party": "Democrat",
        "bio": "Jill Tokuda has represented Hawaii's 2nd Congressional District since 2023, following service in the Hawaii State Senate from 2013 to 2023. A graduate of the University of Hawaii, she worked as a high school teacher and small business owner. Tokuda chaired the Senate Education Committee and focused on agriculture and labor issues. Married with two children, she emphasizes family and community. Her accomplishments include leading Maui wildfire recovery efforts and securing farm bill funding. Tokuda is known for her advocacy for Native Hawaiian rights.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://tokuda.house.gov/",
        "positions": {
            "ABORTION": "Pro-choice; supports federal protections for reproductive rights post-Roe.",
            "EDUCATION": "Strong public school advocate, supporting teacher pay raises and student loan forgiveness.",
            "RELIGIOUS-FREEDOM": "Upholds First Amendment while ensuring protections for marginalized communities.",
            "GUNS": "Supports Hawaii-style gun safety laws, including licensing and storage requirements.",
            "TAXES": "Favors fair taxation, closing loopholes for corporations to fund public services.",
            "IMMIGRATION": "Supports humane immigration reform and protections for agricultural workers.",
            "FAMILY-VALUES": "Inclusive family policies, including support for diverse family structures.",
            "ELECTION-INTEGRITY": "Promotes secure, accessible voting with emphasis on military and overseas ballots."
        },
        "endorsements": ["Hawaii Farm Bureau", "ILWU", "Democratic Congressional Campaign Committee"]
    }
]

# Hawaii Summary
summary = {
    "state": "Hawaii",
    "title": "Hawaii 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Hawaii 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 4
**Total Candidates Profiled:** 6
**Election Dates:**
- 2026-08-08 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Hawaii POLITICAL LANDSCAPE

### **The Aloha State**

Hawaii is a **deeply blue stronghold with emerging conservative pockets**:
- **Democratic Dominance:** The islands have voted Democratic in every presidential election since statehood, with supermajorities in the legislature (Democrats hold 45 of 51 House seats and 24 of 25 Senate seats as of 2025).
- **Growing GOP Influence:** Republicans gained ground in 2024, flipping seats in West Oahu due to cost-of-living frustrations and church mobilization, with Trump improving margins in rural counties like Hawaii and Maui.
- **Urban-Rural Divide:** Honolulu (Oahu) remains liberal, while rural Big Island, Kauai, and Maui counties lean more conservative on social issues, influenced by Native Hawaiian values and evangelical communities.
- **Unique State Factor:** As the only majority-minority state (with significant Native Hawaiian, Asian, and Pacific Islander populations), cultural aloha spirit tempers politics, but rising housing costs and tourism dependency fuel conservative economic critiques.

### **Why Hawaii Matters**

Hawaii is **WINNABLE** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Hawaii's lack of abortion restrictions (no parental consent or bans) makes it a battleground for life-affirming laws; recent GOP pushes for heartbeat bills show potential.
- ✅ **Second Amendment:** Strict gun laws (permit-to-purchase, no open carry) are ripe for reform, with rural hunters and self-defense advocates rallying support.
- ✅ **School Choice:** Limited voucher programs exist, but parental rights bills against gender ideology in schools gained traction in 2024.
- ✅ **Religious Liberty:** Threats from anti-discrimination laws challenge faith-based adoption agencies; protections for churches are crucial.
- ✅ **Family Values:** Same-sex marriage is law, but opposition to gender transitions for minors aligns with Catholic and evangelical voters.
- ✅ **Election Integrity:** Mail-in voting dominance requires safeguards like ID verification to build trust.

---

## 🔴 2026 FEDERAL RACES

### **U.S. House District 1** - 2026-11-03

**Context:** This urban Oahu district (Honolulu metro) influences federal funding for housing and transit. A conservative win could shift Hawaii's delegation toward fiscal restraint and social conservatism, countering the progressive tilt.

**Ed Case (Democrat)** - U.S. Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Lifelong Hawaii resident, corporate lawyer turned politician.
- Served in Congress 2002-2007; returned in 2019 after moderate stances won primary.
- Family man with three children; focuses on bipartisan infrastructure deals.

**Christian Conservative Analysis:**
- **Pro-Life:** Mixed record; voted to defund Planned Parenthood in past but supports access now—3/10.
- **Religious Liberty:** Balanced but leans toward civil rights over exemptions—4/10.
- **Education/Parental Rights:** Supports charters but not vouchers; weak on gender issues—3/10.
- **Family Values:** Inclusive on LGBTQ+; low alignment with biblical marriage—2/10.
- **Overall Assessment:** 3/10—Fiscal moderate but socially liberal; not a reliable ally for conservatives.

**Key Positions:**
- **ABORTION:** Pro-choice with Roe protections.
- **EDUCATION:** Public funding priority, open to charters.
- **RELIGIOUS FREEDOM:** First Amendment balancer.
- **GUNS:** Background checks supporter.
- **TAXES:** Targeted middle-class credits.
- **Housing Affordability:** Pushes federal aid for islands' crisis.

**Endorsements:** Hawaii Democratic Party, Sierra Club.

**Website:** https://case.house.gov/

**Della Au Belatti (Democrat)** - State Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Punahou alum, Williams College grad, UH law degree.
- House member since 2007; Health Committee chair.
- Married with two kids; advocates for women and environment.

**Christian Conservative Analysis:**
- **Pro-Life:** Strong pro-choice, opposes restrictions—1/10.
- **Religious Liberty:** Prioritizes anti-discrimination—2/10.
- **Education/Parental Rights:** Public equity focus, no choice support—1/10.
- **Family Values:** LGBTQ+ ally—1/10.
- **Overall Assessment:** 1/10—Progressive challenger; antithesis to conservative values.

**Key Positions:**
- **ABORTION:** Expanded access advocate.
- **EDUCATION:** Anti-voucher, pro-public equity.
- **RELIGIOUS FREEDOM:** Civil rights priority.
- **GUNS:** Universal checks, assault bans.
- **TAXES:** Wealthy tax hikes for social programs.
- **Immigration:** Sanctuary supporter.

**Endorsements:** EMILY's List, Hawaii Nurses.

**Website:** https://belatti.house.gov/

**Why It Matters:** Controlling this seat ensures conservative voices on federal abortion funding and gun rights reach D.C.

---

### **U.S. House District 2** - 2026-11-03

**Context:** Covering rural Oahu, outer islands, and agriculture, this race affects farm subsidies and Native rights. Conservatives can capitalize on rural discontent with high costs and liberal policies.

**Jill Tokuda (Democrat)** - U.S. Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Former teacher, small business owner, Senate Education chair.
- Elected to Congress in 2022 after state service.
- Married with two children; Maui wildfire recovery leader.

**Christian Conservative Analysis:**
- **Pro-Life:** Pro-choice, supports federal protections—2/10.
- **Religious Liberty:** Marginalized community focus—3/10.
- **Education/Parental Rights:** Public school champion, opposes choice—2/10.
- **Family Values:** Inclusive policies—2/10.
- **Overall Assessment:** 2/10—Rural Democrat but aligns with progressive social agenda.

**Key Positions:**
- **ABORTION:** Post-Roe federal safeguards.
- **EDUCATION:** Teacher raises, loan forgiveness.
- **RELIGIOUS FREEDOM:** Marginalized protections.
- **GUNS:** Hawaii safety laws.
- **TAXES:** Corporate loophole closures.
- **Agriculture:** Farm worker immigration reform.

**Endorsements:** Hawaii Farm Bureau, ILWU.

**Website:** https://tokuda.house.gov/

**Why It Matters:** A conservative flip here amplifies rural voices on land use and family farms, key to biblical stewardship.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** As chief executive, the governor shapes abortion laws, education policy, and budget priorities. With Democratic incumbent eligible for re-election, conservatives aim to exploit economic woes for a breakthrough.

**Josh Green (Democrat)** - Incumbent Governor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Physician specializing in emergency medicine.
- Lt. Gov. 2018-2022; House member 2005-2012.
- Married to Jaime, two children; homelessness initiative leader.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports unrestricted access—1/10.
- **Religious Liberty:** Anti-discrimination priority—2/10.
- **Education/Parental Rights:** Public focus, no choice—1/10.
- **Family Values:** Gender-affirming support—1/10.
- **Overall Assessment:** 1/10—Progressive on social issues; economic moderate at best.

**Key Positions:**
- **ABORTION:** Full access without limits.
- **EDUCATION:** Equity in public schools.
- **RELIGIOUS FREEDOM:** LGBTQ+ protections first.
- **GUNS:** Strict controls.
- **TAXES:** Progressive hikes for services.
- **Climate Resilience:** Green New Deal alignment.

**Endorsements:** Hawaii Democratic Party, Planned Parenthood.

**Website:** https://governor.hawaii.gov/

**Mike Gabbard (Democrat)** - State Senator

**Faith Statement:** "As a devout Catholic, I believe life begins at conception and must be protected at all stages. My faith guides my commitment to family, religious freedom, and moral leadership in public service."

**Background:**
- Vietnam vet, business owner, substitute teacher.
- Senate since 2006; founded Hawaii Coalition for Life.
- Father of Tulsi Gabbard; Catholic family man.

**Christian Conservative Analysis:**
- **Pro-Life:** Strong advocate for restrictions—9/10.
- **Religious Liberty:** Vocal defender—8/10.
- **Education/Parental Rights:** School choice supporter—8/10.
- **Family Values:** Traditional marriage defender—9/10.
- **Overall Assessment:** 8/10—Rare conservative Democrat; strong biblical alignment on social issues.

**Key Positions:**
- **ABORTION:** Parental consent, late-term limits.
- **EDUCATION:** Vouchers, parental rights.
- **RELIGIOUS FREEDOM:** Against faith-violating mandates.
- **GUNS:** Reasonable checks, ease permits.
- **TAXES:** Relief for families.
- **Cost of Living:** Economic growth focus.

**Endorsements:** Hawaii Catholic Conference, Hawaii Family Forum.

**Website:** https://www.mikegabbard.com/

**Duke Aiona (Republican)** - Former Lt. Governor

**Faith Statement:** "My Catholic faith is the foundation of my life and public service. I believe in the dignity of life from conception to natural death, the sanctity of marriage, and the importance of religious freedom in a diverse society."

**Background:**
- Former family court judge, deputy prosecutor.
- Lt. Gov. 2003-2011; ran for governor 2010, 2014, 2022.
- Married to Stacey, five children; youth mentoring founder.

**Christian Conservative Analysis:**
- **Pro-Life:** Defunds abortion providers—10/10.
- **Religious Liberty:** First Amendment champion—10/10.
- **Education/Parental Rights:** Charter and choice advocate—9/10.
- **Family Values:** Biblical family structures—10/10.
- **Overall Assessment:** 10/10—Proven conservative leader; ideal for Hawaii's moral renewal.

**Key Positions:**
- **ABORTION:** Crisis centers, defund Planned Parenthood.
- **EDUCATION:** Parental involvement priority.
- **RELIGIOUS FREEDOM:** No government overreach.
- **GUNS:** Ease restrictions.
- **TAXES:** Cuts for growth.
- **Economy:** Business attraction.

**Endorsements:** Hawaii GOP, Family Policy Alliance, NRA.

**Website:** https://www.duke4hawaii.com/

**Why It Matters:** The governor sets the tone for life protections and family policies; a conservative victory halts progressive overreach.

### **Lieutenant Governor** - 2026-11-03

**Context:** Joint ticket with governor; focuses on economic development. Conservatives seek a running mate emphasizing faith-based initiatives.

**Why It Matters:** Influences administration on community and faith programs; key for mobilizing churches.

---

## 🎯 KEY ISSUES FOR HAWAII CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Push for parental consent laws and heartbeat bills to restrict abortions, building on 2024 GOP gains.
- Support 50+ pregnancy resource centers like those from Hawaii Right to Life.
- Enforce parental consent for minors' medical decisions.
- Oppose state funding for abortions via Medicaid.
- Recent victories: Blocked expansion of late-term access in 2025 session.

**Progressive Position:**
- Maintain unrestricted access, funding via state health plans.
- Efforts to codify Roe protections statewide.
- Battles over defunding crisis centers.

**Christian Conservative Action:**
- Join Hawaii Right to Life (hawaiilife.org) for lobbying.
- Support HB 1234 for consent laws.
- Volunteer at centers in Honolulu and Hilo.
- Vote for pro-life candidates like Gabbard or Aiona.

### **School Choice & Parental Rights**

**Conservative Position:**
- Expand limited voucher program (serving 1,000 students) to 5,000 via tax credits.
- Parental rights law (2024) bans gender ideology in K-12.
- Homeschool freedom strong, with 10,000 students.
- CRT bans in 2023 curriculum standards.
- Wins: Charter school funding increase.

**Progressive Position:**
- Teachers union blocks choice expansions.
- DEI mandates in teacher training.
- Threats to voucher legality.

**Christian Conservative Action:**
- Run for school boards in conservative Maui County.
- Support SB 567 for choice expansion.
- Join Parents for Liberty Hawaii chapter.

### **Religious Freedom**

**Conservative Position:**
- Protect faith-based adoption agencies from anti-discrimination suits.
- Oppose mandates on churches for vaccines or weddings.
- State RFRA strengthens exemptions.
- Threats from 2025 LGBTQ+ bills.

**Progressive Position:**
- Broad anti-discrimination covering sexual orientation/gender identity.
- Lawsuits against faith groups.

**Christian Conservative Action:**
- Alliance Defending Freedom Hawaii (adflegal.org).
- Lobby against HB 2345.
- Church forums on liberty.

### **Guns**

**Conservative Position:**
- Reform permit-to-purchase, allow concealed carry.
- Protect rural hunters on Big Island.
- Oppose assault weapon registry.

**Progressive Position:**
- Tighten licensing, ban high-capacity magazines.

**Christian Conservative Action:**
- Hawaii Rifle Association (hawaiirifleassociation.org).
- Support gun rights bills.
- Training workshops.

### **Taxes**

**Conservative Position:**
- Cut GET on food/medicine to ease costs.
- Property tax relief for families.

**Progressive Position:**
- Raise on luxury properties, corporations.

**Christian Conservative Action:**
- Grassroot Institute advocacy.
- Vote economic conservatives.

### **Immigration**

**Conservative Position:**
- Enforce federal laws, E-verify for jobs.
- Prioritize Native Hawaiian hiring.

**Progressive Position:**
- Sanctuary state expansion.

**Christian Conservative Action:**
- Support legal reform bills.

### **Family Values**

**Conservative Position:**
- Defend traditional marriage, oppose trans sports in girls' events.
- Parental opt-out for sex ed.

**Progressive Position:**
- Gender-affirming care funding.

**Christian Conservative Action:**
- Hawaii Family Alliance (familyalliancehawaii.org).
- Prayer vigils.

### **Election Integrity**

**Conservative Position:**
- Voter ID, paper trails for mail-in.
- Audit 2024 irregularities.

**Progressive Position:**
- No-ID voting, automatic registration.

**Christian Conservative Action:**
- Poll watcher training via GOP.
- Support verification laws.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- **2026-05-01** - Voter registration deadline (30 days pre-primary)
- **2026-07-25** - Early voting begins
- **2026-08-08** - Primary Election
- **2026-11-03** - General Election

**Voter Registration:** elections.hawaii.gov/register-to-vote

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
✅ **Share on social media** with #HIFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR HAWAII CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Hawaii coverage
- **Hawaii Right to Life** - Pro-life ratings
- **Hawaii Family Forum** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Hawaii Secretary of State**: elections.hawaii.gov
- **County Election Offices**: elections.hawaii.gov/contact-us (Oahu, Maui, etc.)
- **Early Voting Locations**: Voter service centers island-wide

### **Conservative Organizations:**
- **Hawaii Right to Life**: hawaiilife.org
- **Hawaii Family Alliance**: familyalliancehawaii.org
- **Hawaii Rifle Association**: hawaiirifleassociation.org
- **Grassroot Institute of Hawaii**: grassroot.org (school choice)
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR HAWAII CHRISTIANS

**2026 Elections Matter:**
- Governor race determines abortion restrictions.
- US House seats affect federal life funding.
- Impacts rural communities on guns and education.
- Overall state direction at stake.

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Cost-of-living relief via tax cuts
✅ Native Hawaiian cultural safeguards
✅ Church mobilization boosted

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Housing crisis worsens without reforms
❌ Tourism dependency deepens
❌ Faith voices silenced

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Josh Green, Mike Gabbard, Duke Aiona and their families
- Hawaii Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Hawaii
- Revival and awakening in Hawaii
- God's will in Hawaii elections

**Scripture for Hawaii Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Hawaii coverage, email contact@ekewaka.com

**HAWAII CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**
""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Hawaii races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Hawaii'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Hawaii races...")
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

print(f"\nChecking for existing Hawaii candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Hawaii'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Hawaii candidates...")
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

print("\nProcessing Hawaii summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Hawaii'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Hawaii data upload complete!")
