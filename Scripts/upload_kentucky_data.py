import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Kentucky Races
races = [
    {
        "state": "Kentucky",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat due to Mitch McConnell's retirement; critical for Republican control of the Senate and advancing conservative priorities like pro-life protections and border security."
    },
    {
        "state": "Kentucky",
        "office": "U.S. House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat following Andy Barr's Senate bid; competitive district covering central Kentucky, key for maintaining Republican House majority."
    },
    {
        "state": "Kentucky",
        "office": "Mayor of Louisville",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Leadership of Kentucky's largest city; influences urban policies on public safety, education, and economic development."
    },
    {
        "state": "Kentucky",
        "office": "Mayor of Lexington",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Governance of Kentucky's second-largest city; impacts horse industry, university relations, and regional growth."
    }
]

# Kentucky Candidates  
candidates = [
    {
        "name": "Daniel Cameron",
        "state": "Kentucky",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Daniel Jay Cameron, born November 22, 1985, in Elizabethtown, Kentucky, is a conservative leader and Christ-follower. A graduate of Transylvania University and the University of Louisville School of Law, Cameron served as a deputy sergeant at arms for the U.S. House of Representatives and as counsel to Senator Mitch McConnell. Elected as Kentucky's 51st Attorney General in 2019, he became the first Black person and first Republican in over 70 years to hold the office. As AG, he defended Kentucky's pro-life laws, challenged Biden's border policies, and fought against COVID mandates infringing on freedoms. Married to Makenze, with two sons, Theodore and Bennett, Cameron's faith guides his commitment to family and righteousness. He ran for governor in 2023, earning President Trump's endorsement, and now seeks to bring America First policies to the Senate as CEO of 1792 Exchange, combating DEI initiatives.",
        "faith_statement": "As a Christ-follower, my position on issues like abortion evolves from my faith. I believe in speaking gently and kindly on delicate topics, recognizing the range of viewpoints, but standing firm on the sanctity of life as God intends.",
        "website": "https://cameronforkentucky.com/",
        "positions": {
            "ABORTION": "Unwavering pro-life advocate; defended Kentucky's near-total ban as AG, supports Human Life Protection Act, would sign exceptions for rape/incest/life of mother while prioritizing alternatives like adoption support and crisis pregnancy centers.",
            "EDUCATION": "Supports school choice and parental rights; opposed mask mandates in schools, champions empowering parents over unions and government control.",
            "RELIGIOUS-FREEDOM": "Fierce defender; challenged COVID vaccine mandates and fought for faith-based organizations' rights against discriminatory policies.",
            "GUNS": "Strong Second Amendment protector; sued Biden admin over ATF rules infringing on gun owners' rights.",
            "TAXES": "Advocates low taxes to grow jobs; supports Trump tax cuts and reducing burdensome regulations on Kentucky businesses.",
            "IMMIGRATION": "Secure borders first; sued Biden for border failures, supports deporting criminal illegals and ending sanctuary policies.",
            "FAMILY-VALUES": "Protects traditional families; banned gender transition surgeries for minors, opposes DEI indoctrination in schools.",
            "ELECTION-INTEGRITY": "Ensures secure elections; supports voter ID and measures to prevent fraud while expanding access for legal voters."
        },
        "endorsements": ["President Donald Trump", "National Right to Life", "Family Research Council"]
    },
    {
        "name": "Andy Barr",
        "state": "Kentucky",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Andrew Russell Barr IV, born July 24, 1973, in Lexington, Kentucky, is a dedicated public servant and father of two daughters. A University of Virginia and UK Law graduate, Barr practiced banking law before entering politics. Elected to represent KY-6 in 2012, he has served seven terms, chairing the House Financial Services Subcommittee. Key accomplishments include co-authoring the Tax Cuts and Jobs Act, defending coal jobs, and leading veteran support initiatives. Married to Eleanor, Barr's career reflects fiscal conservatism and family values, from his time as a UK football captain to bipartisan work on opioid crisis response. Now running for Senate to extend Trump-era policies and protect Kentucky's way of life.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://barrforsenate.com/",
        "positions": {
            "ABORTION": "Unabashedly pro-life; supported Dobbs overturn, Born-Alive Protection Act, Hyde Amendment prohibiting taxpayer-funded abortions.",
            "EDUCATION": "Empowers parental rights; supports school choice, opposes federal overreach in curricula.",
            "RELIGIOUS-FREEDOM": "Defends faith-based institutions; voted against mandates violating religious liberties during COVID.",
            "GUNS": "A+ NRA rating; opposes red-flag laws, protects gun manufacturers from banking discrimination.",
            "TAXES": "Champion of Trump tax cuts; fights to make permanent, reduce deficit through spending cuts.",
            "IMMIGRATION": "Close the border, deport illegals; co-sponsored Secure the Border Act to restart wall construction.",
            "FAMILY-VALUES": "God-given genders; bans men in women's sports, prohibits funding for minor gender transitions.",
            "ELECTION-INTEGRITY": "Supports voter ID and audit transparency to restore trust in elections."
        },
        "endorsements": ["National Rifle Association", "Gun Owners of America", "Riley Gaines"]
    },
    {
        "name": "Nate Morris",
        "state": "Kentucky",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Nathaniel Ryan Morris, born October 16, 1980, is a ninth-generation Kentuckian and self-made entrepreneur from a tobacco-farming family in Lyon County. Raised in poverty, he built Rubicon Global into a $4 billion waste-tech firm, revolutionizing recycling with AI. As chairman of Morris Industries, he invests in Kentucky startups. No prior office, Morris is a MAGA outsider endorsed by Trump allies, criticizing establishment figures. Married with children, his faith drives community service, including youth mentorship. Running to drain the swamp and unleash Kentucky's potential through innovation and conservative principles.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life conservative; supports state bans and federal limits post-Dobbs, emphasizing family support programs.",
            "EDUCATION": "Promotes school choice and vocational training; opposes 'woke' curricula, favors parental control.",
            "RELIGIOUS-FREEDOM": "Strong advocate; backs protections for faith-based businesses against government overreach.",
            "GUNS": "2nd Amendment absolutist; opposes all infringements, supports concealed carry expansions.",
            "TAXES": "Cut taxes, slash regulations; pro-business incentives for Kentucky manufacturing revival.",
            "IMMIGRATION": "Build the wall, end chain migration; prioritizes American workers and border security.",
            "FAMILY-VALUES": "Traditional marriage and family; fights gender ideology in schools and media.",
            "ELECTION-INTEGRITY": "Voter ID mandatory; paper ballots and audits to prevent fraud."
        },
        "endorsements": ["Charlie Kirk", "Donald Trump Jr.", "JD Vance"]
    },
    {
        "name": "Ralph Alvarado",
        "state": "Kentucky",
        "office": "U.S. House District 6",
        "party": "Republican",
        "bio": "Dr. Ralph Alvarado, born in Cuba and immigrated young, is the first Hispanic elected to Kentucky General Assembly. A UK-trained physician and state Senator (2015-2021), he served as Lt. Gov. Matt Bevin's running mate in 2019 and Tennessee Health Commissioner (2022-2025). Married to Tammy, father of three, Alvarado's career blends medicine and policy, focusing on healthcare access and economic growth. 'Day One MAGA' conservative, he champions border security and crushing 'woke' agendas.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life; supported KY bans, advocates federal heartbeat bill.",
            "EDUCATION": "School choice advocate; bans CRT, protects parental rights.",
            "RELIGIOUS-FREEDOM": "Defends church rights; opposed COVID restrictions on worship.",
            "GUNS": "Strong 2A supporter; reciprocity for concealed carry.",
            "TAXES": "Reduce taxes, balance budget; pro-small business deductions.",
            "IMMIGRATION": "Close border, deport criminals; E-Verify mandatory.",
            "FAMILY-VALUES": "Traditional values; opposes transgender sports participation.",
            "ELECTION-INTEGRITY": "Voter ID, clean rolls; against mail-in expansion."
        },
        "endorsements": ["Kentucky Chamber of Commerce", "National Federation of Independent Business"]
    },
    {
        "name": "Ryan Dotson",
        "state": "Kentucky",
        "office": "U.S. House District 6",
        "party": "Republican",
        "bio": "Ryan Dotson, a Pentecostal preacher, Army veteran, and state Rep. since 2021, owns multiple restaurants in Winchester. Married with family, his faith informs his culture-war leadership, filing bills banning transgender athletes and calling for Gov. Beshear's impeachment over school masks. A grassroots conservative, Dotson fights for working Kentuckians against elite overreach.",
        "faith_statement": "As a Pentecostal preacher, I am guided by biblical principles in public service, believing government should reflect God's design for family, life, and liberty.",
        "website": "",
        "positions": {
            "ABORTION": "100% pro-life; no exceptions, supports defunding Planned Parenthood.",
            "EDUCATION": "Parental rights first; bans gender ideology, expands vouchers.",
            "RELIGIOUS-FREEDOM": "Faith over fear; protected churches during lockdowns.",
            "GUNS": "Constitutional carry advocate; opposes all gun control.",
            "TAXES": "Flat tax proposal; eliminate income tax on overtime.",
            "IMMIGRATION": "Zero tolerance; wall funding, end DACA.",
            "FAMILY-VALUES": "Biblical marriage; anti-LGBTQ+ agenda in schools.",
            "ELECTION-INTEGRITY": "Hand-counted paper ballots; purge non-citizens."
        },
        "endorsements": ["Kentucky Right to Life", "Faith & Freedom Coalition"]
    },
    {
        "name": "Deanna Frazier Gordon",
        "state": "Kentucky",
        "office": "U.S. House District 6",
        "party": "Republican",
        "bio": "Deanna Frazier Gordon, state Rep. since 2019, built and sold Kentucky's largest audiology clinic. A small business owner and mother, she focuses on working-class issues like spending limits and immigration. From Madison County, her record includes pro-life votes and economic conservatism.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "Pro-life warrior; co-sponsored trigger ban enforcement.",
            "EDUCATION": "School choice expansion; anti-indoctrination laws.",
            "RELIGIOUS-FREEDOM": "Protects conscience rights for healthcare providers.",
            "GUNS": "2A defender; campus carry supporter.",
            "TAXES": "Limit government spending; tax relief for families.",
            "IMMIGRATION": "Stop illegal immigration; secure borders now.",
            "FAMILY-VALUES": "Parental rights paramount; traditional family support.",
            "ELECTION-INTEGRITY": "Voter ID essential; audit every election."
        },
        "endorsements": ["U.S. Chamber of Commerce", "Kentucky Farm Bureau"]
    },
    {
        "name": "Linda Gorton",
        "state": "Kentucky",
        "office": "Mayor of Lexington",
        "party": "Republican",
        "bio": "Linda Gorton, 82, has served as Lexington mayor since 2019, winning re-election in 2022. A former state Senator (1997-2011) and UK professor, she focuses on economic development and public safety. Married, mother of three, Gorton's leadership navigated COVID and growth, making her the first to seek a third term.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.lexingtonky.gov/government/mayors-office",
        "positions": {
            "ABORTION": "Supports state pro-life laws; local enforcement.",
            "EDUCATION": "Funds UK and local schools; parental involvement encouraged.",
            "RELIGIOUS-FREEDOM": "Balanced approach; protected gatherings during pandemic.",
            "GUNS": "Respects 2A; community safety programs.",
            "TAXES": "Fiscal conservative; balanced budgets.",
            "IMMIGRATION": "Local cooperation with federal enforcement.",
            "FAMILY-VALUES": "Family-friendly policies; anti-crime initiatives.",
            "ELECTION-INTEGRITY": "Secure local voting processes."
        },
        "endorsements": ["Lexington Chamber of Commerce", "Kentucky League of Cities"]
    },
    {
        "name": "Craig Greenberg",
        "state": "Kentucky",
        "office": "Mayor of Louisville",
        "party": "Democrat",
        "bio": "Craig Greenberg, 50, elected Louisville mayor in 2022, is a former business executive and prosecutor. Harvard and UK Law grad, he co-founded a startup and led Teach for America. Married to Rachel, father of two, Greenberg focuses on equity and safety post-Breonna Taylor.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://louisvilleky.gov/government/mayor-craig-greenberg",
        "positions": {
            "ABORTION": "Pro-choice; supports access and challenges state bans.",
            "EDUCATION": "Public school funding; equity programs.",
            "RELIGIOUS-FREEDOM": "Inclusive policies; DEI emphasis.",
            "GUNS": "Gun violence prevention; red-flag laws.",
            "TAXES": "Progressive taxation; social spending.",
            "IMMIGRATION": "Sanctuary elements; immigrant support.",
            "FAMILY-VALUES": "LGBTQ+ inclusive; gender-affirming care.",
            "ELECTION-INTEGRITY": "Expand voting access; oppose ID."
        },
        "endorsements": ["Planned Parenthood", "Everytown for Gun Safety"]
    }
]

# Kentucky Summary
summary = {
    "state": "Kentucky",
    "title": "Kentucky 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Kentucky 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 4
**Total Candidates Profiled:** 8
**Election Dates:**
- 2026-05-19 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Kentucky POLITICAL LANDSCAPE

### **The Bluegrass State**

Kentucky is a **deep-red stronghold with blue pockets**:
- **Federal Dominance:** Republicans hold both Senate seats (until McConnell's retirement) and five of six House districts; Trump won by 26 points in 2024.
- **State Mix:** Democratic governor Andy Beshear won re-election in 2023, but GOP supermajorities control the legislature, passing pro-life and gun laws.
- **Urban-Rural Divide:** Louisville and Lexington lean Democratic (Jefferson and Fayette Counties), while rural eastern and western Kentucky are solidly Republican.
- **Horse Country Heritage:** Equine industry influences economy and conservative values, with faith communities strong in Baptist heartland.

### **Why Kentucky Matters**

Kentucky is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Near-total abortion ban since 2022 (triggered by Dobbs), defended by AG Cameron; ongoing lawsuits by progressives threaten gains.
- ✅ **Second Amendment:** Constitutional carry since 2019; top-10 gun-friendly state, resisting federal overreach.
- ✅ **School Choice:** 2024 ESA law expands options; charters approved in 2017, but union fights persist.
- ✅ **Religious Liberty:** Strong RFRA protections; churches mobilized against COVID mandates.
- ✅ **Family Values:** Bans on gender transitions for minors (2023); traditional marriage upheld.
- ✅ **Coal and Faith Belt:** Appalachian Bible Belt drives evangelical turnout, key to national GOP wins.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** Mitch McConnell's open seat is a MAGA battleground; winner shapes Senate majority, pro-life confirmations, and Trump agenda. Kentucky's red tilt favors GOP, but high turnout needed against national Dem spending.

**Daniel Cameron (Republican)** - Former Attorney General

**Faith Statement:** "As a Christ-follower, my position on issues like abortion evolves from my faith. I believe in speaking gently and kindly on delicate topics, recognizing the range of viewpoints, but standing firm on the sanctity of life as God intends."

**Background:**
- First Black statewide elected official in KY history.
- Defended pro-life laws as AG against 10+ lawsuits.
- Trump-endorsed gubernatorial nominee in 2023.

**Christian Conservative Analysis:**
- **Pro-Life:** Defended KY ban in court; 10/10 for unyielding stance with compassionate exceptions.
- **Religious Liberty:** Sued over vaccine mandates; 9/10 for bold defenses.
- **Education/Parental Rights:** Opposed school masks; 8/10 for choice support.
- **Family Values:** Banned minor transitions; 9/10 biblical alignment.
- **Overall Assessment:** 9/10 - Battle-tested warrior for faith and freedom.

**Key Positions:**
- **ABORTION:** Unwavering pro-life; defended KY's ban, supports exceptions for rape/incest/life-saving while boosting adoption.
- **EDUCATION:** School choice, parental veto on curricula; fights union control.
- **RELIGIOUS FREEDOM:** RFRA enforcer; protects churches from DEI discrimination.
- **GUNS:** Sued ATF on pistol braces; full 2A restoration.
- **TAXES:** Extend Trump cuts, eliminate corporate welfare.
- **IMMIGRATION:** Deport criminals, end catch-and-release.
- **Border Security:** Prioritizes KY jobs over amnesty.

**Endorsements:** President Donald Trump, National Right to Life, Family Research Council

**Website:** https://cameronforkentucky.com/

**Andy Barr (Republican)** - U.S. Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Lexington native, UK Law grad, banking attorney turned Congressman since 2013.
- Co-authored 2017 tax cuts; veteran advocate.
- Father emphasizing God-given gender truths.

**Christian Conservative Analysis:**
- **Pro-Life:** Dobbs amicus, Born-Alive votes; 10/10 consistency.
- **Religious Liberty:** Anti-mandate votes; 8/10 solid.
- **Education/Parental Rights:** Bans federal indoctrination; 9/10 strong.
- **Family Values:** Protects girls' sports; 9/10 aligned.
- **Overall Assessment:** 9/10 - Proven fiscal hawk with family focus.

**Key Positions:**
- **ABORTION:** Unabashed pro-life; Hyde Amendment, no taxpayer abortions.
- **EDUCATION:** Vouchers, anti-CRT; empowers parents.
- **RELIGIOUS FREEDOM:** Defends faith charities from regs.
- **GUNS:** A+ NRA; Fair Access for gun banks.
- **TAXES:** Permanent TCJA; Balanced Budget Amendment.
- **IMMIGRATION:** Secure Border Act; Remain in Mexico.
- **Gender Ideology:** Two genders, no transitions on minors.

**Endorsements:** NRA, Gun Owners of America, Riley Gaines

**Website:** https://barrforsenate.com/

**Nate Morris (Republican)** - Businessman

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Self-made Rubicon founder, $4B waste-tech innovator.
- Ninth-gen Kentuckian from poor roots; Trump donor networker.
- Family man investing in KY startups.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports bans; 8/10 outsider energy.
- **Religious Liberty:** Backs faith businesses; 7/10 emerging.
- **Education/Parental Rights:** Vocational focus; 8/10 practical.
- **Family Values:** Anti-woke; 8/10 fresh voice.
- **Overall Assessment:** 8/10 - Disruptive MAGA force.

**Key Positions:**
- **ABORTION:** State bans, defund PP; family incentives.
- **EDUCATION:** Choice, trade schools over colleges.
- **RELIGIOUS FREEDOM:** End DEI attacks on churches.
- **GUNS:** Absolutist; no compromises.
- **TAXES:** Slash regs, pro-crypto innovation.
- **IMMIGRATION:** Wall, merit-based only.
- **Economy:** Jobs via energy independence.

**Endorsements:** Charlie Kirk, Donald Trump Jr., JD Vance

**Website:** 

**Why It Matters:** Securing this seat locks GOP Senate control, blocking radical judges and advancing biblical justice nationwide.

---

## 🔴 2026 HOUSE RACES

### **U.S. House District 6** - 2026-11-03

**Context:** Andy Barr's exit opens this Lexington-area swing district (R+8); GOP hold vital for House majority, influencing education funding and border bills.

**Ralph Alvarado (Republican)** - Former State Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Cuban immigrant, first Hispanic KY legislator.
- Physician, Bevin's 2019 LG nominee; TN Health Comm.
- "Day One MAGA" family man.

**Christian Conservative Analysis:**
- **Pro-Life:** Trigger ban co-sponsor; 9/10 record.
- **Religious Liberty:** Lockdown fighter; 8/10.
- **Education/Parental Rights:** Anti-woke bills; 9/10.
- **Family Values:** Traditional stances; 8/10.
- **Overall Assessment:** 8/10 - Hispanic conservative bridge-builder.

**Key Positions:**
- **ABORTION:** Heartbeat support; no exceptions.
- **EDUCATION:** Vouchers, ban CRT/gender lessons.
- **RELIGIOUS FREEDOM:** Conscience protections.
- **GUNS:** Reciprocity nationwide.
- **TAXES:** Small biz relief.
- **IMMIGRATION:** E-Verify, deport all.

**Endorsements:** Kentucky Chamber, NFIB

**Website:** 

**Ryan Dotson (Republican)** - State Representative & Preacher

**Faith Statement:** "As a Pentecostal preacher, I am guided by biblical principles in public service, believing government should reflect God's design for family, life, and liberty."

**Background:**
- Army vet, restaurant owner, KY House since 2021.
- Led trans sports ban; impeachment push on masks.
- Devoted husband and father.

**Christian Conservative Analysis:**
- **Pro-Life:** Defund efforts; 10/10 firebrand.
- **Religious Liberty:** Church protector; 10/10.
- **Education/Parental Rights:** Culture warrior; 10/10.
- **Family Values:** Biblical absolutist; 10/10.
- **Overall Assessment:** 10/10 - Prophetic voice for revival.

**Key Positions:**
- **ABORTION:** No exceptions, abolitionist.
- **EDUCATION:** Homeschool freedom, anti-LGBTQ+.
- **RELIGIOUS FREEDOM:** Faith over state.
- **GUNS:** Constitutional carry everywhere.
- **TAXES:** Eliminate overtime tax.
- **IMMIGRATION:** Zero amnesty.

**Endorsements:** KY Right to Life, Faith & Freedom

**Website:** 

**Deanna Frazier Gordon (Republican)** - State Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Audiology entrepreneur, built/sold top KY clinic.
- KY House since 2019; working-class champion.
- Mother prioritizing family economics.

**Christian Conservative Analysis:**
- **Pro-Life:** Consistent votes; 9/10.
- **Religious Liberty:** Healthcare faith rights; 8/10.
- **Education/Parental Rights:** Choice advocate; 9/10.
- **Family Values:** Anti-immigration for families; 8/10.
- **Overall Assessment:** 8/10 - Business-savvy mom.

**Key Positions:**
- **ABORTION:** Enforce bans locally.
- **EDUCATION:** Parental opt-outs.
- **RELIGIOUS FREEDOM:** Provider conscience.
- **GUNS:** Campus carry.
- **TAXES:** Spending caps.
- **IMMIGRATION:** Border wall funding.

**Endorsements:** U.S. Chamber, KY Farm Bureau

**Website:** 

**Why It Matters:** Retaining KY-6 ensures conservative votes on life, guns, and taxes in a razor-thin House.

---

## 🔴 2026 MUNICIPAL RACES

### **Mayor of Louisville** - 2026-11-03

**Context:** Greenberg's re-election tests urban conservative pushback on crime, schools; largest city influences state policies.

**Craig Greenberg (Democrat)** - Incumbent Mayor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Startup co-founder, prosecutor.
- Elected 2022; equity focus post-Taylor.
- Father of two.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports access; 2/10 oppositional.
- **Religious Liberty:** DEI prioritizes; 4/10.
- **Education/Parental Rights:** Public funding; 3/10.
- **Family Values:** Inclusive gender; 2/10.
- **Overall Assessment:** 2/10 - Progressive urbanist.

**Key Positions:**
- **ABORTION:** Challenge bans.
- **EDUCATION:** Equity over choice.
- **RELIGIOUS FREEDOM:** Inclusive mandates.
- **GUNS:** Violence prevention.
- **TAXES:** Social investments.

**Endorsements:** Planned Parenthood, Everytown

**Website:** https://louisvilleky.gov/government/mayor-craig-greenberg

### **Mayor of Lexington** - 2026-11-03

**Context:** Gorton's third term vs. challenger; horse capital's leadership affects faith communities and economy.

**Linda Gorton (Republican)** - Incumbent Mayor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- State Sen., UK prof; mayor since 2019.
- Landslide 2022 win; growth navigator.
- Mother of three.

**Christian Conservative Analysis:**
- **Pro-Life:** Local support; 7/10.
- **Religious Liberty:** Balanced protections; 7/10.
- **Education/Parental Rights:** Funds with input; 7/10.
- **Family Values:** Safety focus; 7/10.
- **Overall Assessment:** 7/10 - Steady conservative.

**Key Positions:**
- **ABORTION:** Uphold state laws.
- **EDUCATION:** UK partnerships.
- **RELIGIOUS FREEDOM:** Worship freedoms.
- **GUNS:** Community programs.
- **TAXES:** Balanced budgets.

**Endorsements:** Lexington Chamber, KY League of Cities

**Website:** https://www.lexingtonky.gov/government/mayors-office

**Why It Matters:** GOP mayors in cities fortify red strongholds against blue urban erosion.

---

## 🎯 KEY ISSUES FOR Kentucky CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- KY's 2022 trigger ban prohibits abortions except life-saving; 6-week limit upheld.
- 200+ pregnancy centers via KY Right to Life.
- Parental consent for minors required.
- No state funding for abortions; defund PP efforts ongoing.
- Recent victory: 2023 ban on minor transitions.

**Progressive Position:**
- Beshear-backed lawsuits seek repeal; expansion via amendments.
- Funding battles for 'reproductive justice.'
- Push for interstate travel protections.

**Christian Conservative Action:**
- Join KY Right to Life (kyrtl.com) for marches.
- Support HB 467 enforcement bills.
- Volunteer at crisis centers in Louisville/Lexington.
- Vote pro-life in Senate race.

### **School Choice & Parental Rights**

**Conservative Position:**
- 2024 ESAs up to $7,500 for private/homeschool; serves 2,000+ kids.
- 2017 charter law expanded to 42 schools.
- Bans on CRT/gender ideology (2022/2023).
- Homeschool deregulated since 1980s.
- Win: Parental bill of rights (2024).

**Progressive Position:**
- Teachers unions block vouchers via courts.
- DEI mandates in JCPS/LCPS.
- Threats to charters via funding cuts.

**Christian Conservative Action:**
- Run for local school boards in 2025.
- Support SB 1 expansion.
- Join Parents Defending Education KY chapter.
- Lobby against union bills.

### **Religious Freedom**

**Conservative Position:**
- KY RFRA (2015) protects faith acts.
- No mandates on churches post-COVID.
- Adoption agency exemptions upheld.
- Strong evangelical network.

**Progressive Position:**
- Lawsuits over prayer in schools.
- DEI forcing inclusivity trainings.
- Attacks on faith-based foster care.

**Christian Conservative Action:**
- Partner with Alliance Defending Freedom KY cases.
- Host forum on RFRA strengthening.
- Join First Liberty alerts.
- Pray against anti-faith bills.

### **Guns**

**Conservative Position:**
- Permitless carry (2019); no red flags.
- Stand Your Ground expanded.
- Preemption over local bans.
- NRA top-ranked state.

**Progressive Position:**
- Louisville push for assault bans.
- Post-LMPD shootings, storage laws.
- Federal red-flag imports.

**Christian Conservative Action:**
- Volunteer Kentuckians for the Commonwealth 2A.
- Support reciprocity bills.
- Train church security teams.
- Oppose urban gun control.

### **Taxes**

**Conservative Position:**
- Flat 5% income; no local sales over 6%.
- 2023 cuts on groceries/property.
- Pro-business incentives for coal/tech.

**Progressive Position:**
- Raise on wealthy for social programs.
- Beshear's budget battles for Medicaid.
- Carbon taxes threatened.

**Christian Conservative Action:**
- Back Taxpayer Protection Pledge candidates.
- Lobby for flat tax permanence.
- Join Americans for Prosperity KY.
- Educate on tithing vs. gov dependency.

### **Immigration**

**Conservative Position:**
- No sanctuary cities; E-Verify encouraged.
- 2023 border security resolutions.
- Deport felons priority.

**Progressive Position:**
- Louisville welcome policies.
- Driver's licenses for undocumented.
- Oppose ICE cooperation.

**Christian Conservative Action:**
- Support FAIRKY for enforcement.
- Report sanctuary pushes.
- Aid legal immigrants via churches.
- Vote border hawks in Senate.

### **Family Values**

**Conservative Position:**
- 2023 ban on minor transitions/sterilizations.
- Covenant marriage option.
- Anti-porn in libraries (2024).

**Progressive Position:**
- Gender-affirming in schools.
- Pride funding in cities.
- Challenge marriage definitions.

**Christian Conservative Action:**
- Join KY Family Policy Council.
- Push SB 150 expansions.
- Family worship nights.
- Boycott woke businesses.

### **Election Integrity**

**Conservative Position:**
- Voter ID since 2020; paper backups.
- 2024 audits required.
- No no-excuse mail-in.

**Progressive Position:**
- Expand mail/absentee.
- Oppose ID as suppression.
- Settle lawsuits for counting changes.

**Christian Conservative Action:**
- Train poll watchers via Election Integrity KY.
- Support HB 574 audits.
- Church voter reg drives.
- Pray for honest counts.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- 2026-04-24 - Voter registration deadline
- 2026-10-06 - Early voting begins
- 2026-05-19 - Primary Election
- 2026-11-03 - General Election

**Voter Registration:** https://registertovoteki.ky.gov/

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
✅ **Share on social media** with #KYFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Kentucky CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Kentucky coverage
- **Kentucky Right to Life** - Pro-life ratings
- **Kentucky Family Policy Council** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Kentucky Secretary of State**: https://sos.ky.gov/elections
- **County Election Offices**: Search via sos.ky.gov
- **Early Voting Locations**: Check county clerk sites

### **Conservative Organizations:**
- **Kentucky Right to Life**: https://kyrtl.com
- **Kentucky Family Foundation**: https://kyfamily.org
- **Kentuckians for the Commonwealth 2A**: https://gunrights.org/ky
- **Bluegrass Institute for Public Policy** - School choice: https://www.bipps.org
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Kentucky CHRISTIANS

**2026 Elections Matter:**
- U.S. Senate determines federal judges blocking pro-life laws.
- House District 6 affects school choice funding.
- Mayoral races impact city sanctuary status.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Coal jobs revived in Appalachia
✅ Border security prioritized for KY farms
✅ Faith communities empowered

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Sanctuary cities proliferate
❌ Tax hikes on families
❌ Woke DEI in every agency

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Daniel Cameron, Andy Barr, Nate Morris and their families
- Kentucky Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Kentucky
- Revival and awakening in Kentucky
- God's will in Kentucky elections

**Scripture for Kentucky Elections:**

*"Righteousness exalts a nation, but sin condemns any people."* - *Proverbs 14:34*

*"When the righteous thrive, the people rejoice; when the wicked rule, the people groan."* - *Proverbs 29:2*

*"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land."* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Kentucky coverage, email contact@ekewaka.com

**Kentucky CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Kentucky races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Kentucky'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Kentucky races...")
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

print(f"\nChecking for existing Kentucky candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Kentucky'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Kentucky candidates...")
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

print("\nProcessing Kentucky summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Kentucky'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Kentucky data upload complete!")
