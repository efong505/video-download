import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Alabama Races
races = [
    {
        "state": "Alabama",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat following incumbent Tommy Tuberville's run for Governor. Critical battleground for conservative values in the U.S. Senate."
    },
    {
        "state": "Alabama",
        "office": "U.S. House District 1",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Republican-held district pivotal for maintaining conservative majority in Congress."
    },
    {
        "state": "Alabama",
        "office": "U.S. House District 2",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open due to Barry Moore's Senate bid; key for House control."
    },
    {
        "state": "Alabama",
        "office": "U.S. House District 3",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Incumbent Mike Rogers' seat; influences national security and conservative policies."
    },
    {
        "state": "Alabama",
        "office": "U.S. House District 4",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Long-held Republican district essential for fiscal conservatism."
    },
    {
        "state": "Alabama",
        "office": "U.S. House District 5",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Gary Palmer's district; focus on religious liberty and family values."
    },
    {
        "state": "Alabama",
        "office": "U.S. House District 6",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Strong conservative district defending 2nd Amendment rights."
    },
    {
        "state": "Alabama",
        "office": "U.S. House District 7",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Democratic-held; opportunity for conservative flip to advance pro-life agenda."
    },
    {
        "state": "Alabama",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat determining Alabama's leadership on pro-life laws, school choice, and family protections."
    },
    {
        "state": "Alabama",
        "office": "Lieutenant Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Influences state senate leadership and conservative policy priorities."
    },
    {
        "state": "Alabama",
        "office": "Attorney General",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat; vital for defending religious liberty and election integrity in courts."
    },
    {
        "state": "Alabama",
        "office": "Secretary of State",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Open seat; key for secure elections and voter ID enforcement."
    },
    {
        "state": "Alabama",
        "office": "State Treasurer",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Manages state funds; crucial for fiscal conservatism and low taxes."
    }
]

# Alabama Candidates  
candidates = [
    {
        "name": "Tommy Tuberville",
        "state": "Alabama",
        "office": "Governor",
        "party": "Republican",
        "bio": "Tommy Tuberville, born September 18, 1954, in Camden, Arkansas, is a retired college football coach and current U.S. Senator from Alabama, now seeking the governorship. Raised by a World War II veteran father who earned five Bronze Stars and a Purple Heart, Tuberville developed a strong sense of duty early on. He played football at Southern Arkansas University before embarking on a coaching career that spanned over three decades. Tuberville achieved national prominence as head coach at Auburn University from 1999 to 2008, where he led the Tigers to an undefeated 13-0 season in 2004, a SEC Championship, and a Sugar Bowl victory. He later coached at the University of Cincinnati and Texas Tech University. Elected to the U.S. Senate in 2020, Tuberville has been a staunch conservative voice, focusing on military affairs, agriculture, and Second Amendment rights. Married to Suzanne since 1986, they have four children and ten grandchildren. Tuberville's family values are rooted in his Christian faith, which he credits for guiding his public service. As governor, he aims to expand school choice, protect life, and secure borders.",
        "faith_statement": "I accepted Christ in 1988 while serving as a youth pastor at a church. My faith in Jesus Christ guides my life and decisions in public service.",
        "website": "https://tuberville.senate.gov",
        "positions": {
            "ABORTION": "Strongly pro-life; supports Alabama's total ban with exceptions only for maternal health. Voted to defund Planned Parenthood and protect unborn from conception.",
            "EDUCATION": "Advocates for universal school choice and parental rights; opposes federal overreach in curricula and supports CHOOSE Act expansion.",
            "RELIGIOUS-FREEDOM": "Defends First Amendment rights; sponsored bills to protect faith-based organizations from discrimination.",
            "GUNS": "A-rated by NRA; fierce defender of 2nd Amendment, opposes red flag laws and universal background checks.",
            "TAXES": "Pushes for permanent tax cuts and elimination of death tax to promote economic growth.",
            "IMMIGRATION": "Supports border wall completion and ending sanctuary cities; prioritizes American workers.",
            "FAMILY-VALUES": "Upholds traditional marriage and opposes gender ideology in schools; champions parental consent for medical transitions.",
            "ELECTION-INTEGRITY": "Backs voter ID laws and paper ballots; fought against 2020 election irregularities."
        },
        "endorsements": ["NRA", "National Right to Life", "Family Research Council"]
    },
    {
        "name": "Will Boyd",
        "state": "Alabama",
        "office": "Governor",
        "party": "Democrat",
        "bio": "Dr. Will Boyd, a pastor, engineer, and businessman, announced his candidacy for Alabama Governor in June 2025. Born and raised in Alabama, Boyd earned a PhD in engineering and has built a successful career in business while serving as senior pastor at New Rising Star Missionary Baptist Church in Birmingham. He has run for office multiple times, including Birmingham City Council and U.S. Senate, driven by a passion for equality and fairness. As a faith leader, Boyd emphasizes servant leadership and community service, founding initiatives to support underserved families. Married with children, his family is central to his life. Boyd's platform focuses on expanding Medicaid, improving education access, and economic development to lift all Alabamians. He critiques the current administration's refusal to expand healthcare and aims to provide compassionate governance rooted in his Christian values.",
        "faith_statement": "As a Baptist pastor, my faith compels me to serve the least of these, guided by Jesus' call to love and justice for all.",
        "website": "https://drwillboyd.com",
        "positions": {
            "ABORTION": "Supports reproductive rights with access to safe abortions, emphasizing women's health and autonomy.",
            "EDUCATION": "Invests in public schools, opposes vouchers that drain funds; promotes equitable funding and teacher pay raises.",
            "RELIGIOUS-FREEDOM": "Protects all faiths while preventing imposition on others; supports separation of church and state.",
            "GUNS": "Favors universal background checks and red flag laws to reduce gun violence without infringing rights.",
            "TAXES": "Progressive taxation to fund social services; closes corporate loopholes for fair share.",
            "IMMIGRATION": "Pathway to citizenship for Dreamers; humane border policies with comprehensive reform.",
            "FAMILY-VALUES": "Inclusive family policies supporting LGBTQ+ rights and gender-affirming care.",
            "ELECTION-INTEGRITY": "Expands voting access; opposes restrictive ID laws that disenfranchise minorities."
        },
        "endorsements": ["Planned Parenthood", "Alabama Education Association", "ACLU"]
    },
    {
        "name": "Steve Marshall",
        "state": "Alabama",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Steve Marshall, born October 26, 1964, in Atmore, Alabama, is the current Attorney General and a 2026 U.S. Senate candidate. A graduate of UNC Chapel Hill and University of Alabama School of Law, Marshall practiced law in Scottsboro before serving as Chilton County District Attorney from 2011 to 2017. Appointed AG in 2017 by Gov. Kay Ivey, he won full terms in 2018 and 2022. Marshall has defended Alabama's pro-life laws, sued the Biden administration over immigration, and protected election integrity. Widowed in 2018 after his wife's battle with mental illness, he is a devoted father. His faith drives his commitment to justice and family values. As Senator, he pledges to fight for conservative principles in Washington.",
        "faith_statement": "No publicly disclosed faith statement, but his actions reflect strong Christian conservative values in defending life and liberty.",
        "website": "https://stevemarshallforsenate.com",
        "positions": {
            "ABORTION": "Defended Alabama's total abortion ban in courts; pro-life from conception with no exceptions beyond maternal life.",
            "EDUCATION": "Supports school choice via CHOOSE Act; empowers parents against woke indoctrination.",
            "RELIGIOUS-FREEDOM": "Led lawsuits protecting faith-based adoptions and church rights during COVID.",
            "GUNS": "Strong 2A advocate; opposed federal gun control measures.",
            "TAXES": "Fights for tax relief and state sovereignty over IRS overreach.",
            "IMMIGRATION": "Sued Biden over border policies; demands secure borders and deportation of criminals.",
            "FAMILY-VALUES": "Protects traditional marriage; opposes transgender athletes in women's sports.",
            "ELECTION-INTEGRITY": "Enforced voter ID; investigated 2020 fraud claims."
        },
        "endorsements": ["Trump Campaign", "NRA", "Alabama Farmers Federation"]
    },
    {
        "name": "Barry Moore",
        "state": "Alabama",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Barry Moore, born 1966 in Enterprise, Alabama, is a U.S. Congressman and 2026 Senate candidate. Raised on a family farm in Coffee County, Moore served in the U.S. Marine Corps Reserve and built a small business in the music industry. Elected to Alabama House in 2010, he championed conservative reforms before winning U.S. House District 2 in 2020. Married to Heather since 1992, they have four children and attend Hillcrest Baptist Church. Moore's faith journey, shared publicly, transformed his life from addiction to public service. As Senator, he vows to defend the unborn, secure borders, and restore fiscal sanity.",
        "faith_statement": "My guiding light will be my faith in Jesus Christ. Heather and I found redemption through Christ, and it compels me to serve with integrity.",
        "website": "https://barrymooreforalabama.com",
        "positions": {
            "ABORTION": "100% pro-life; co-sponsored Heartbeat Act and defunding Planned Parenthood.",
            "EDUCATION": "Pushes parental rights bills; supports ESA expansion for school choice.",
            "RELIGIOUS-FREEDOM": "Authored legislation protecting religious exemptions in healthcare.",
            "GUNS": "A+ NRA rating; opposes all gun control, including assault weapon bans.",
            "TAXES": "Advocates flat tax and abolishing IRS; cuts wasteful spending.",
            "IMMIGRATION": "Build the wall; ends chain migration and birthright citizenship for illegals.",
            "FAMILY-VALUES": "Biblical view of marriage; bans gender transition for minors.",
            "ELECTION-INTEGRITY": "Mandates voter ID nationwide; audits 2020 election."
        },
        "endorsements": ["FreedomWorks", "Heritage Action", "Gun Owners of America"]
    },
    {
        "name": "Jared Hudson",
        "state": "Alabama",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Jared Hudson, a former Navy SEAL, founded DeliverFund to combat child sex trafficking. Born in Alabama, Hudson served as a SEAL operator and sniper, later entering law enforcement. After military service, he ran for sheriff and now seeks the Senate to fight human trafficking and secure borders. Married with children, Hudson's faith fuels his warrior spirit. His nonprofit has led to hundreds of arrests. As Senator, he commits to America First policies protecting families and values.",
        "faith_statement": "No publicly disclosed faith statement, but his anti-trafficking work aligns with Christian calls to protect the vulnerable.",
        "website": "https://hudsonforalabama.com",
        "positions": {
            "ABORTION": "Pro-life advocate; supports bans and defunding abortion providers.",
            "EDUCATION": "Empowers parents with choice; eliminates Common Core remnants.",
            "RELIGIOUS-FREEDOM": "Protects churches from government shutdowns and mandates.",
            "GUNS": "Unwavering 2A defender; veteran who knows importance of armed citizens.",
            "TAXES": "Cuts taxes to stimulate growth; audits federal spending.",
            "IMMIGRATION": "Secures borders to stop trafficking; mass deportations.",
            "FAMILY-VALUES": "Fights child exploitation; upholds traditional family structures.",
            "ELECTION-INTEGRITY": "Voter ID and clean rolls; combats foreign interference."
        },
        "endorsements": ["Veterans for America First", "Anti-Trafficking Coalition", "Alabama Law Enforcement"]
    },
    {
        "name": "Katherine Robertson",
        "state": "Alabama",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "Katherine Robertson, born circa 1984 in Selma, is chief counsel to Alabama AG and 2026 AG candidate. A graduate of Vanderbilt and University of Alabama Law, she clerked for federal judges before joining the AG's office in 2015. Robertson has litigated pro-life cases, election challenges, and religious liberty suits. Married, her faith informs her dedication to justice. Endorsed by RAGA, she aims to continue defending conservative values in courts.",
        "faith_statement": "No publicly disclosed faith statement, but her defense of life and liberty reflects deep Christian convictions.",
        "website": "https://katherineforag.com",
        "positions": {
            "ABORTION": "Fiercely pro-life; litigated to uphold Alabama's ban.",
            "EDUCATION": "Defends parental rights in court against indoctrination.",
            "RELIGIOUS-FREEDOM": "Sued over COVID restrictions on churches.",
            "GUNS": "Protects 2A in lawsuits against federal overreach.",
            "TAXES": "Supports state challenges to federal tax mandates.",
            "IMMIGRATION": "Enforces laws against sanctuary policies.",
            "FAMILY-VALUES": "Opposes gender ideology mandates.",
            "ELECTION-INTEGRITY": "Secures elections through litigation."
        },
        "endorsements": ["RAGA", "Alliance Defending Freedom", "Alabama Pro-Life"]
    },
    {
        "name": "Jay Mitchell",
        "state": "Alabama",
        "office": "Attorney General",
        "party": "Republican",
        "bio": "Jay Mitchell, born August 26, 1976, served as Alabama Supreme Court Justice from 2019-2025 before resigning to run for AG. A Samford Law graduate, he practiced civil litigation and was general counsel for Alabama Policy Institute. Elected in 2018, Mitchell authored opinions upholding pro-life laws. Married with family, his conservative jurisprudence stems from faith. He pledges to be a 'warrior' for Trump agenda.",
        "faith_statement": "No publicly disclosed, but his API work advances Christian family policies.",
        "website": "https://jayforalabama.com",
        "positions": {
            "ABORTION": "Authored rulings enforcing bans; absolute pro-life.",
            "EDUCATION": "Upholds school choice in judicial opinions.",
            "RELIGIOUS-FREEDOM": "Protected faith exemptions in adoption cases.",
            "GUNS": "Struck down gun control attempts.",
            "TAXES": "Defends low-tax regimes.",
            "IMMIGRATION": "Enforces strict enforcement.",
            "FAMILY-VALUES": "Biblical marriage definitions.",
            "ELECTION-INTEGRITY": "Voter ID enforcer."
        },
        "endorsements": ["Alabama Policy Institute", "Federalist Society", "NRA"]
    },
    {
        "name": "Will Ainsworth",
        "state": "Alabama",
        "office": "Lieutenant Governor",
        "party": "Republican",
        "bio": "Will Ainsworth, Alabama's current Lt. Gov since 2019, seeks re-election. Born in Birmingham, raised in Boaz, he graduated from UAB and built a business in outdoor recreation. Elected to Alabama House in 2014, Ainsworth championed school choice and pro-life bills. Married to Kendall with three children, his Christian values guide his service. As Lt. Gov, he presides over the Senate and advances conservative legislation.",
        "faith_statement": "Raised with core Christian conservative values; faith compels me to lead with righteousness and compassion.",
        "website": "https://ltgov.alabama.gov",
        "positions": {
            "ABORTION": "Sponsored heartbeat bill; unwavering pro-life.",
            "EDUCATION": "Architect of CHOOSE Act for ESA.",
            "RELIGIOUS-FREEDOM": "Protects faith-based initiatives.",
            "GUNS": "Expands permitless carry.",
            "TAXES": "Pushes tax cuts.",
            "IMMIGRATION": "Border security funding.",
            "FAMILY-VALUES": "Parental rights champion.",
            "ELECTION-INTEGRITY": "Voter ID advocate."
        },
        "endorsements": ["Alabama Farmers Federation", "Business Council of Alabama", "Christian Coalition"]
    },
    {
        "name": "Wes Allen",
        "state": "Alabama",
        "office": "Lieutenant Governor",
        "party": "Republican",
        "bio": "Wes Allen, current Secretary of State, is running for Lt. Gov. A Troy University graduate, he served in the Army and business before Alabama House 2018-2022. As SOS since 2023, Allen enforced election security. Married with family, faith drives his public service.",
        "faith_statement": "No publicly disclosed, but supports faith-based policies.",
        "website": "https://sos.alabama.gov",
        "positions": {
            "ABORTION": "Pro-life defender.",
            "EDUCATION": "School choice supporter.",
            "RELIGIOUS-FREEDOM": "Election protections for churches.",
            "GUNS": "2A rights.",
            "TAXES": "Fiscal conservative.",
            "IMMIGRATION": "Secure borders.",
            "FAMILY-VALUES": "Traditional values.",
            "ELECTION-INTEGRITY": "Purged voter rolls."
        },
        "endorsements": ["Election Integrity Project", "GOP"]
    },
    {
        "name": "Caroleene Dobson",
        "state": "Alabama",
        "office": "Secretary of State",
        "party": "Republican",
        "bio": "Caroleene Dobson, former congressional candidate, seeks SOS. Auburn Law grad, she clerked federally and practiced in DC. Married, mother, conservative activist.",
        "faith_statement": "No disclosed.",
        "website": "https://caroleenedobson.com",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Choice.",
            "RELIGIOUS-FREEDOM": "Protect.",
            "GUNS": "Defend.",
            "TAXES": "Cut.",
            "IMMIGRATION": "Secure.",
            "FAMILY-VALUES": "Uphold.",
            "ELECTION-INTEGRITY": "ID laws."
        },
        "endorsements": ["Women for Trump"]
    },
    {
        "name": "Andrew Sorrell",
        "state": "Alabama",
        "office": "Secretary of State",
        "party": "Republican",
        "bio": "Andrew Sorrell, State Auditor, running for SOS. Youngest state auditor, focuses on transparency.",
        "faith_statement": "No disclosed.",
        "website": "https://auditor.alabama.gov",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Choice.",
            "RELIGIOUS-FREEDOM": "Support.",
            "GUNS": "2A.",
            "TAXES": "Low.",
            "IMMIGRATION": "Enforce.",
            "FAMILY-VALUES": "Traditional.",
            "ELECTION-INTEGRITY": "Secure."
        },
        "endorsements": ["GOP"]
    },
    {
        "name": "Young Boozer",
        "state": "Alabama",
        "office": "State Treasurer",
        "party": "Republican",
        "bio": "Incumbent Treasurer Young Boozer seeks re-election. Banking background, fiscal expert.",
        "faith_statement": "No disclosed.",
        "website": "https://treasury.alabama.gov",
        "positions": {
            "ABORTION": "Pro-life.",
            "EDUCATION": "Fund choice.",
            "RELIGIOUS-FREEDOM": "Protect.",
            "GUNS": "Support.",
            "TAXES": "Conservative management.",
            "IMMIGRATION": "State role.",
            "FAMILY-VALUES": "Values.",
            "ELECTION-INTEGRITY": "Financial oversight."
        },
        "endorsements": ["Bankers Association"]
    }
]

# Alabama Summary
summary = {
    "state": "Alabama",
    "title": "Alabama 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Alabama 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 13
**Total Candidates Profiled:** 13
**Election Dates:**
- 2025-08-26 (Municipal Elections)
- 2026-05-19 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Alabama POLITICAL LANDSCAPE

### **The Heart of Dixie**

Alabama is a **deep red stronghold**:
- **Bible Belt Core:** Home to over 86% Christians, with strong evangelical influence shaping laws on life and family.
- **Conservative Dominance:** GOP supermajorities in legislature; Trump won by 25% in 2024.
- **Urban-Rural Divide:** Birmingham and Mobile lean blue, but rural counties like Marshall and Etowah deliver overwhelming red margins.
- **Military Heritage:** Largest defense employer in South; values national security and 2A rights.

### **Why Alabama Matters**

Alabama is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Total abortion ban since 2022; only maternal health exception, leading national resistance to expansion.
- ✅ **Second Amendment:** Permitless carry since 2023; no assault weapon bans, top-10 gun-friendly state.
- ✅ **School Choice:** CHOOSE Act provides $7K ESAs to 24K students in 2025; expands parental rights.
- ✅ **Religious Liberty:** 1998 Amendment and Gov. Ivey's 2023 EO protect faith from burdens.
- ✅ **Family Values:** Bans gender transitions for minors; traditional marriage enshrined.
- ✅ **Election Security:** Strict voter ID; SOS purges rolls regularly.

---

## 🔴 2026 FEDERAL RACES

### **U.S. Senate** - 2026-11-03

**Context:** Open seat as Tuberville eyes Governor; determines Senate firewall for pro-life, 2A. Alabama's vote could tip national balance toward righteousness.

**Steve Marshall (Republican)** - Attorney General

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Born 1964 in Atmore; UNC/UA Law grad.
- Chilton Co. DA, AG since 2017; defended pro-life laws.
- Widowed father; justice warrior.

**Christian Conservative Analysis:**
- **Pro-Life:** Litigated ban's constitutionality; 10/10 unyielding defender.
- **Religious Liberty:** Sued Biden over faith mandates; 9/10 protector.
- **Education/Parental Rights:** Backed CHOOSE Act suits; 8/10.
- **Family Values:** Opposed woke policies; 9/10 biblical.
- **Overall Assessment:** 9/10 - Proven fighter, but more public faith needed.

**Key Positions:**
- **ABORTION:** Enforces total ban; no expansions.
- **EDUCATION:** Parental control over curricula.
- **RELIGIOUS FREEDOM:** Shields churches from discrimination.
- **GUNS:** Rejects federal grabs.
- **TAXES:** Challenges IRS overreach.
- **IMMIGRATION:** Sues for border enforcement.
- **FAMILY-VALUES:** Bans transgender sports.
- **ELECTION-INTEGRITY:** Voter ID enforcer.

**Endorsements:** Trump, NRA, Farmers Fed.

**Website:** https://stevemarshallforsenate.com

**Barry Moore (Republican)** - U.S. Congressman

**Faith Statement:** "My guiding light will be my faith in Jesus Christ."

**Background:**
- Farm-raised in Coffee Co.; Marine vet, businessman.
- AL House to Congress; family man at Baptist church.
- Overcame addiction via faith.

**Christian Conservative Analysis:**
- **Pro-Life:** Heartbeat bill co-sponsor; 10/10.
- **Religious Liberty:** Exemptions in healthcare; 10/10.
- **Education/Parental Rights:** ESA pusher; 10/10.
- **Family Values:** Biblical marriage; 10/10.
- **Overall Assessment:** 10/10 - Faith-driven conservative.

**Key Positions:**
- **ABORTION:** Defund PP; life at conception.
- **EDUCATION:** Eliminate federal indoctrination.
- **RELIGIOUS FREEDOM:** Protect exemptions.
- **GUNS:** No red flags.
- **TAXES:** Abolish IRS.
- **IMMIGRATION:** End chain migration.
- **FAMILY-VALUES:** Ban transitions.
- **ELECTION-INTEGRITY:** Nationwide ID.

**Endorsements:** FreedomWorks, Heritage.

**Website:** https://barrymooreforalabama.com

**Jared Hudson (Republican)** - Navy SEAL Veteran

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- SEAL sniper; founded anti-trafficking nonprofit.
- Law enforcement; family protector.
- Warrior against evil.

**Christian Conservative Analysis:**
- **Pro-Life:** Anti-trafficking aligns with protecting innocents; 9/10.
- **Religious Liberty:** Defends vulnerable; 8/10.
- **Education/Parental Rights:** Choice for safety; 8/10.
- **Family Values:** Fights exploitation; 9/10.
- **Overall Assessment:** 8/10 - Action over words.

**Key Positions:**
- **ABORTION:** Ban providers.
- **EDUCATION:** Parent empowerment.
- **RELIGIOUS FREEDOM:** Church protections.
- **GUNS:** Armed citizens.
- **TAXES:** Audit spending.
- **IMMIGRATION:** Stop trafficking.
- **FAMILY-VALUES:** Protect kids.
- **ELECTION-INTEGRITY:** Clean rolls.

**Endorsements:** Vets for America First.

**Website:** https://hudsonforalabama.com

**Why It Matters:** Senate seat safeguards national pro-life firewall.

---

## 🔴 2026 STATEWIDE RACES

### **Governor** - 2026-11-03

**Context:** Open; sets tone for CHOOSE Act, abortion defenses. Christian voters can exalt righteousness.

**Tommy Tuberville (Republican)** - U.S. Senator

**Faith Statement:** "I accepted Christ in 1988 as youth pastor."

**Background:**
- Football coach legend; Auburn undefeated 2004.
- Senate since 2020; vet family.
- Father of 4, 10 grandkids.

**Christian Conservative Analysis:**
- **Pro-Life:** Defunded PP; 9/10.
- **Religious Liberty:** Sponsored protections; 9/10.
- **Education/Parental Rights:** School choice; 9/10.
- **Family Values:** Traditional upholder; 9/10.
- **Overall Assessment:** 9/10 - Coach to conservative leader.

**Key Positions:**
- **ABORTION:** Total ban supporter.
- **EDUCATION:** Universal choice.
- **RELIGIOUS FREEDOM:** Anti-discrimination.
- **GUNS:** NRA A-rated.
- **TAXES:** Permanent cuts.
- **IMMIGRATION:** Wall builder.
- **FAMILY-VALUES:** Oppose ideology.
- **ELECTION-INTEGRITY:** Voter ID.

**Endorsements:** NRA, Right to Life.

**Website:** https://tuberville.senate.gov

**Will Boyd (Democrat)** - Pastor/Businessman

**Faith Statement:** "Faith compels service to the least."

**Background:**
- PhD engineer; Birmingham pastor.
- Multiple runs; family man.
- Equality advocate.

**Christian Conservative Analysis:**
- **Pro-Life:** Supports choice; 2/10.
- **Religious Liberty:** Separation focus; 4/10.
- **Education/Parental Rights:** Public funding; 3/10.
- **Family Values:** Inclusive; 3/10.
- **Overall Assessment:** 3/10 - Progressive twist on faith.

**Key Positions:**
- **ABORTION:** Access rights.
- **EDUCATION:** Equitable public.
- **RELIGIOUS FREEDOM:** No imposition.
- **GUNS:** Background checks.
- **TAXES:** Progressive.
- **IMMIGRATION:** Reform.
- **FAMILY-VALUES:** LGBTQ support.
- **ELECTION-INTEGRITY:** Expand access.

**Endorsements:** Planned Parenthood.

**Website:** https://drwillboyd.com

**Why It Matters:** Governor vetoes threats to life, family.

### **Attorney General** - 2026-11-03

**Context:** Open; defends bans in court. Key for liberty suits.

**Katherine Robertson (Republican)** - Chief Counsel

**Faith Statement:** "No publicly disclosed"

**Background:**
- Vanderbilt/UA Law; federal clerk.
- AG office litigator; pro-life warrior.
- Married mother.

**Christian Conservative Analysis:**
- **Pro-Life:** Upheld bans; 10/10.
- **Religious Liberty:** COVID suits; 10/10.
- **Education/Parental Rights:** Rights defender; 9/10.
- **Family Values:** Anti-woke; 9/10.
- **Overall Assessment:** 9.5/10 - Legal powerhouse.

**Key Positions:**
- **ABORTION:** Enforce bans.
- **EDUCATION:** Sue indoctrination.
- **RELIGIOUS FREEDOM:** Exemption wins.
- **GUNS:** 2A suits.
- **TAXES:** Vs. federal.
- **IMMIGRATION:** Sanctuary blocks.
- **FAMILY-VALUES:** Gender bans.
- **ELECTION-INTEGRITY:** Litigation.

**Endorsements:** RAGA, ADF.

**Website:** https://katherineforag.com

**Jay Mitchell (Republican)** - Former Justice

**Faith Statement:** "No publicly disclosed"

**Background:**
- Samford Law; API counsel.
- Supreme Court 2019-25; opinions on life.
- Family conservative.

**Christian Conservative Analysis:**
- **Pro-Life:** Ruled for bans; 10/10.
- **Religious Liberty:** Adoption protections; 10/10.
- **Education/Parental Rights:** Choice opinions; 9/10.
- **Family Values:** Marriage defs; 10/10.
- **Overall Assessment:** 10/10 - Judicial conservative.

**Key Positions:**
- **ABORTION:** Absolute life.
- **EDUCATION:** Parent power.
- **RELIGIOUS FREEDOM:** Faith adoptions.
- **GUNS:** Strike controls.
- **TAXES:** Low regimes.
- **IMMIGRATION:** Strict.
- **FAMILY-VALUES:** Biblical.
- **ELECTION-INTEGRITY:** ID.

**Endorsements:** Federalist Society.

**Website:** https://jayforalabama.com

**Why It Matters:** AG shields biblical laws.

### **Lieutenant Governor** - 2026-11-03

**Context:** Senate president role; advances bills on family, guns.

**Will Ainsworth (Republican)** - Incumbent

**Faith Statement:** "Core Christian values guide me."

**Background:**
- UAB grad; outdoor business.
- House to Lt Gov; family of 5.
- CHOOSE Act architect.

**Christian Conservative Analysis:**
- **Pro-Life:** Heartbeat sponsor; 10/10.
- **Religious Liberty:** Faith initiatives; 9/10.
- **Education/Parental Rights:** ESA leader; 10/10.
- **Family Values:** Rights champ; 10/10.
- **Overall Assessment:** 10/10 - Proven leader.

**Key Positions:**
- **ABORTION:** Unwavering ban.
- **EDUCATION:** Expand ESAs.
- **RELIGIOUS FREEDOM:** Protect initiatives.
- **GUNS:** Permitless carry.
- **TAXES:** Cuts.
- **IMMIGRATION:** Funding security.
- **FAMILY-VALUES:** Consent laws.
- **ELECTION-INTEGRITY:** ID.

**Endorsements:** Farmers Fed.

**Website:** https://ltgov.alabama.gov

**Wes Allen (Republican)** - Secretary of State

**Faith Statement:** "No publicly disclosed"

**Background:**
- Army vet; House 2018-22.
- SOS since 2023; roll purges.
- Family servant.

**Christian Conservative Analysis:**
- **Pro-Life:** Defender; 9/10.
- **Religious Liberty:** Church votes; 8/10.
- **Education/Parental Rights:** Choice; 8/10.
- **Family Values:** Traditional; 8/10.
- **Overall Assessment:** 8/10 - Election focus.

**Key Positions:**
- **ABORTION:** Support bans.
- **EDUCATION:** Choice funds.
- **RELIGIOUS FREEDOM:** Voter protections.
- **GUNS:** Rights.
- **TAXES:** Conservative.
- **IMMIGRATION:** Borders.
- **FAMILY-VALUES:** Values.
- **ELECTION-INTEGRITY:** Purges rolls.

**Endorsements:** GOP.

**Website:** https://sos.alabama.gov

**Why It Matters:** Influences pro-family legislation.

### **Secretary of State** - 2026-11-03

**Context:** Oversees elections; ensures integrity for faith vote.

**Caroleene Dobson (Republican)** - Activist

**Faith Statement:** "No disclosed"

**Background:**
- Auburn Law; DC practice.
- 2024 congressional run.
- Mother conservative.

**Christian Conservative Analysis:**
- **Pro-Life:** Advocate; 8/10.
- **Religious Liberty:** 8/10.
- **Education/Parental Rights:** 8/10.
- **Family Values:** 8/10.
- **Overall Assessment:** 8/10 - Emerging voice.

**Key Positions:**
- **ABORTION:** Pro-life.
- **EDUCATION:** Choice.
- **RELIGIOUS FREEDOM:** Protect.
- **GUNS:** Defend.
- **TAXES:** Cut.
- **IMMIGRATION:** Secure.
- **FAMILY-VALUES:** Uphold.
- **ELECTION-INTEGRITY:** Strict ID.

**Endorsements:** Women for Trump.

**Website:** https://caroleenedobson.com

**Andrew Sorrell (Republican)** - Auditor

**Faith Statement:** "No disclosed"

**Background:**
- Youngest auditor; transparency.
- Fiscal watchdog.

**Christian Conservative Analysis:**
- **Pro-Life:** 7/10.
- **Religious Liberty:** 7/10.
- **Education/Parental Rights:** 7/10.
- **Family Values:** 7/10.
- **Overall Assessment:** 7/10 - Fiscal strength.

**Key Positions:**
- **ABORTION:** Support.
- **EDUCATION:** Fund choice.
- **RELIGIOUS FREEDOM:** Yes.
- **GUNS:** Yes.
- **TAXES:** Oversight.
- **IMMIGRATION:** Enforce.
- **FAMILY-VALUES:** Traditional.
- **ELECTION-INTEGRITY:** Audits.

**Endorsements:** GOP.

**Website:** https://auditor.alabama.gov

**Why It Matters:** Secures Christian turnout.

### **State Treasurer** - 2026-11-03

**Context:** Manages funds for conservative priorities like pregnancy centers.

**Young Boozer (Republican)** - Incumbent

**Faith Statement:** "No disclosed"

**Background:**
- Banking exec; term-limited? Seeks re.
- Fiscal steward.

**Christian Conservative Analysis:**
- **Pro-Life:** Funds life; 8/10.
- **Religious Liberty:** 8/10.
- **Education/Parental Rights:** 8/10.
- **Family Values:** 8/10.
- **Overall Assessment:** 8/10 - Steward.

**Key Positions:**
- **ABORTION:** Life funding.
- **EDUCATION:** Choice allocations.
- **RELIGIOUS FREEDOM:** Support.
- **GUNS:** Neutral.
- **TAXES:** Efficient.
- **IMMIGRATION:** State costs.
- **FAMILY-VALUES:** Values.
- **ELECTION-INTEGRITY:** Secure funds.

**Endorsements:** Bankers.

**Website:** https://treasury.alabama.gov

**Why It Matters:** Funds righteousness.

---

## 🎯 KEY ISSUES FOR Alabama CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Total ban since 2022; ectopic/rape exceptions debated but held firm.
- 200+ pregnancy centers; $10M state funding.
- Parental consent for minors.
- No public funding for abortion.
- Victory: SCOTUS upheld IVF post-2024.

**Progressive Position:**
- Push repeal via SB34; fund expansions.
- Attack centers as deceptive.
- Remove consent laws.

**Christian Conservative Action:**
- Join Alabama Right to Life (alabamarighttolife.org).
- Support HB50 refinements.
- Volunteer at centers; pray vigils.
- Vote pro-life only.

### **School Choice & Parental Rights**

**Conservative Position:**
- CHOOSE Act: $7K ESAs for 24K students 2025-26.
- Bans CRT/gender in public schools.
- Homeschool liberty strong.
- Win: 5K public enrollment drop to choice.

**Progressive Position:**
- Union opposition; DEI mandates.
- Voucher drains public funds.

**Christian Conservative Action:**
- Run for school boards.
- Back API bills (alabamapolicy.org).
- Join Scholarships for Kids.

### **Religious Freedom**

**Conservative Position:**
- 1998 Amendment bars burdens.
- Ivey EO 2023 enforces.
- Ranked 20th nationally; protects refusals.
- Win: No church shutdowns post-COVID.

**Progressive Position:**
- ACLU suits against exemptions.
- Impose on faith adoptions.

**Christian Conservative Action:**
- ADF cases (adflegal.org).
- Support First Liberty.
- Church forums.

### **Guns**

**Conservative Position:**
- Permitless carry 2023; no mag limits.
- Stand Your Ground.
- NRA paradise.

**Progressive Position:**
- Background expansions.
- Assault bans.

**Christian Conservative Action:**
- Alabama Firearms Assoc (alabamafirearmsassociation.org).
- NRA training.
- Lobby against controls.

### **Taxes**

**Conservative Position:**
- No income tax hikes; grocery tax cut.
- Boozer manages $50B wisely.

**Progressive Position:**
- Raise for social programs.

**Christian Conservative Action:**
- Support cuts via API.
- Tithe wisely.

### **Immigration**

**Conservative Position:**
- AG suits vs. Biden; no sanctuary.
- E-verify mandates.

**Progressive Position:**
- Pathways, amnesty.

**Christian Conservative Action:**
- Border prayer; FAIR support.

### **Family Values**

**Conservative Position:**
- Minors transition ban 2022.
- Marriage amendment.

**Progressive Position:**
- Gender ideology push.

**Christian Conservative Action:**
- Family Policy Alliance.
- Parent groups.

### **Election Integrity**

**Conservative Position:**
- Voter ID since 2018; purges.
- Paper audits.

**Progressive Position:**
- Mail-in expansions.

**Christian Conservative Action:**
- Poll watch; iVoterGuide.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- 2026-10-19 - Voter registration deadline
- 2026-10-24 - Absentee request deadline
- 2026-05-19 - Primary Election
- 2026-11-03 - General Election

**Voter Registration:** sos.alabama.gov

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
✅ **Share on social media** with #AlabamaFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Alabama CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Alabama coverage
- **Alabama Right to Life** - Pro-life ratings (alabamarighttolife.org)
- **Alabama Policy Institute** - Faith-based education (alabamapolicy.org)
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Alabama Secretary of State**: sos.alabama.gov
- **County Election Offices**: Find via county name + "elections"
- **Early Voting Locations**: Absentee only; county probate offices

### **Conservative Organizations:**
- **Alabama Right to Life**: alabamarighttolife.org
- **Alabama Policy Institute**: alabamapolicy.org
- **Alabama Firearms Association**: alabamafirearmsassociation.org
- **Scholarships for Kids**: scholarshipsforkids.org
- **Alliance Defending Freedom** - Religious liberty (adflegal.org)
- **First Liberty Institute** - Religious freedom (firstliberty.org)

---

## 🔥 BOTTOM LINE FOR Alabama CHRISTIANS

**2026 Elections Matter:**
- Senate race determines pro-life Senate.
- Governor affects CHOOSE expansion.
- AG impacts court defenses.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ Border security funded
✅ Tax cuts sustained
✅ Military heritage honored

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ Sanctuary states
❌ Tax hikes
✅ Woke policies imposed

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Tommy Tuberville, Steve Marshall, Barry Moore, Jared Hudson, Katherine Robertson, Jay Mitchell, Will Ainsworth, Wes Allen, Caroleene Dobson, Andrew Sorrell, Young Boozer and families
- Alabama Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Alabama
- Revival and awakening in Alabama
- God's will in Alabama elections

**Scripture for Alabama Elections:**

*\"Righteousness exalts a nation, but sin condemns any people.\"* - *Proverbs 14:34*

*\"When the righteous thrive, the people rejoice; when the wicked rule, the people groan.\"* - *Proverbs 29:2*

*\"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land.\"* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Alabama coverage, email contact@ekewaka.com

**Alabama CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Alabama races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Alabama'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Alabama races...")
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

print(f"\nChecking for existing Alabama candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Alabama'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Alabama candidates...")
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

print("\nProcessing Alabama summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Alabama'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Alabama data upload complete!")