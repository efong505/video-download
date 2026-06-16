import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
races_table = dynamodb.Table('races')
candidates_table = dynamodb.Table('candidates')
summaries_table = dynamodb.Table('state-summaries')

# Alaska Races
races = [
    {
        "state": "Alaska",
        "office": "U.S. Senate",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The race for Alaska's U.S. Senate seat held by incumbent Dan Sullivan (R) is pivotal for conservative priorities, including pro-life protections and Second Amendment rights, in a state with ranked-choice voting that amplifies independent voices."
    },
    {
        "state": "Alaska",
        "office": "U.S. House At-Large",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "Alaska's sole congressional district will decide representation on federal issues like resource development and family values, with incumbent Nick Begich (R) facing Democratic challengers."
    },
    {
        "state": "Alaska",
        "office": "Governor",
        "election_date": "2026-11-03",
        "race_type": "general",
        "description": "The open gubernatorial race, with Gov. Mike Dunleavy eligible but not running, will shape state policies on abortion restrictions, school choice, and election integrity amid a crowded Republican field."
    }
]

# Alaska Candidates  
candidates = [
    {
        "name": "Dan Sullivan",
        "state": "Alaska",
        "office": "U.S. Senate",
        "party": "Republican",
        "bio": "Daniel Scott Sullivan, born November 13, 1964, in Fairview Park, Ohio, is a U.S. Marine Corps veteran, attorney, and politician serving as Alaska's junior U.S. Senator since 2015. A graduate of Harvard University (BA in economics, magna cum laude) and Georgetown University (JD/MS in Foreign Service, cum laude), Sullivan served active duty in the Marines from 1993-1997 and 2004-2006, deploying to Afghanistan, and in the reserves until 2024, retiring as colonel. He clerked for federal and state judges, practiced law in Anchorage, and worked in the Bush administration as Assistant Secretary of State for Economic and Business Affairs (2006-2009). Appointed Alaska Attorney General (2009-2010) and Natural Resources Commissioner (2010-2013) under Gov. Sean Parnell, Sullivan defeated incumbent Sen. Mark Begich in 2014 and won re-election in 2020. Married to Julie Fate since 1994, with three daughters, he attends Catholic services and emphasizes family and faith in public life. Sullivan's career highlights include advancing Alaska's energy independence and defending military readiness.",
        "faith_statement": "As a pro-life Catholic, I am guided by my faith to protect the sanctity of life from conception and uphold religious liberty for all Alaskans.",
        "website": "https://www.sullivan.senate.gov/",
        "positions": {
            "ABORTION": "Strongly pro-life; supports overturning Roe v. Wade (which he celebrated in 2022) and opposes abortion except in cases of rape, incest, or life of the mother; advocates for adoption incentives and defunding Planned Parenthood.",
            "EDUCATION": "Supports school choice and parental rights; backed expansion of voucher programs and opposes federal overreach in curricula like CRT.",
            "RELIGIOUS-FREEDOM": "Defends religious liberty; co-sponsored Religious Freedom Restoration Act enhancements and opposed mandates infringing on faith-based organizations.",
            "GUNS": "Staunch 2nd Amendment defender; earned NRA endorsement, opposed red-flag laws, and supported concealed carry reciprocity.",
            "TAXES": "Advocates tax cuts; voted for TCJA extension and opposes new taxes on oil and gas to protect PFD dividends.",
            "IMMIGRATION": "Supports secure borders; backs wall funding, E-Verify, and ending chain migration while allowing legal pathways for skilled workers.",
            "FAMILY-VALUES": "Upholds traditional marriage and parental rights; voted against Respect for Marriage Act initially but supported final version; opposes gender ideology in schools.",
            "ELECTION-INTEGRITY": "Endorses voter ID and audit requirements; criticized RCV but supports paper ballots and same-day voting."
        },
        "endorsements": ["NRA", "Alaska Family Action", "Family Research Council"]
    },
    {
        "name": "Ann Diener",
        "state": "Alaska",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Ann Diener, a Democrat and newspaper sales executive, announced her candidacy for U.S. Senate in Alaska's 2026 election, challenging incumbent Republican Dan Sullivan. Originally from Vista, California, Diener moved to Alaska three years ago from an overdeveloped California, seeking a better quality of life. She grew up in what she considers her hometown of Vista and has experience in renewable energy goals. In 2022, she spent time understanding Alaskan electoral politics and worked for Les Gara's gubernatorial campaign. Diener emphasizes bringing people together for sustainable growth, attracting more residents to Alaska, and addressing issues like overdevelopment. As a sales executive at an Alaska newspaper, she brings media and business acumen to her campaign. Her platform focuses on unity and projects for economic and environmental sustainability. Family details are not publicly detailed, but her move to Alaska reflects a commitment to the state's future. Diener's candidacy marks her as the Democratic challenger in a state where Republicans hold strongholds, positioning her to appeal to moderates and progressives on issues like renewable energy and community building. (212 words)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.anndienerforsenate.com/",
        "positions": {
            "ABORTION": "No publicly disclosed detailed position",
            "EDUCATION": "No publicly disclosed detailed position",
            "RELIGIOUS-FREEDOM": "No publicly disclosed detailed position",
            "GUNS": "No publicly disclosed detailed position",
            "TAXES": "No publicly disclosed detailed position",
            "IMMIGRATION": "No publicly disclosed detailed position",
            "FAMILY-VALUES": "No publicly disclosed detailed position",
            "ELECTION-INTEGRITY": "No publicly disclosed detailed position"
        },
        "endorsements": []
    },
    {
        "name": "Mary Peltola",
        "state": "Alaska",
        "office": "U.S. Senate",
        "party": "Democrat",
        "bio": "Mary Sattler Peltola, born August 31, 1973, in Anchorage, is a Yup'ik politician, former tribal judge, and ex-U.S. Representative (2022-2025). Raised in rural Yukon-Kuskokwim Delta communities like Kwethluk and Bethel, daughter of pilot-teacher Ward Sattler and Yup'ik Elizabeth Williams, Peltola is the first Alaska Native and woman in Congress from Alaska. She studied elementary education at universities in Colorado and Alaska (1991-1998), worked as a fish technician, and won Miss National Congress of American Indians in 1995. Married three times—with four biological and three stepchildren—her third husband, Eugene 'Buzzy' Peltola Jr., died in a 2023 plane crash. Peltola served in the Alaska House (1999-2009), Bethel City Council (2011-2013), as a lobbyist (2015-2017), executive director of Kuskokwim River Inter-Tribal Fish Commission (post-2016), and tribal judge (2020-2021). Elected to Congress in 2022 special election via ranked-choice voting, defeating Sarah Palin, she focused on fisheries, veterans' food security, and rural health before losing re-election in 2024.",
        "faith_statement": "As an Orthodox Christian in the Orthodox Church in America, my faith informs my commitment to service, community, and justice for all Alaskans.",
        "website": "https://marypeltola.com/",
        "positions": {
            "ABORTION": "Pro-choice; supports codifying Roe v. Wade and appeared at Planned Parenthood rallies; opposes restrictions and backs federal funding for reproductive care.",
            "EDUCATION": "Supports public school funding and opposes vouchers; advocates for Native language programs but resists parental rights bills limiting DEI.",
            "RELIGIOUS-FREEDOM": "Supports broad protections but prioritizes LGBTQ+ rights; voted against bills seen as discriminating against non-religious views.",
            "GUNS": "Moderate; earned rare NRA endorsement in 2024 for supporting rural hunting rights but backs universal background checks.",
            "TAXES": "Opposes cuts for wealthy; supports raising corporate taxes to fund social programs and protect PFD from oil volatility.",
            "IMMIGRATION": "Supports pathways to citizenship; opposed border wall and E-Verify mandates, emphasizing humane treatment and DACA protections.",
            "FAMILY-VALUES": "Supports LGBTQ+ inclusion and gender-affirming care; backs same-sex marriage and opposes parental consent for abortions.",
            "ELECTION-INTEGRITY": "Defends ranked-choice voting; opposes strict voter ID as barrier to Native voters."
        },
        "endorsements": ["Planned Parenthood", "EMILY's List", "AFL-CIO"]
    },
    {
        "name": "Dave Bronson",
        "state": "Alaska",
        "office": "Governor",
        "party": "Republican",
        "bio": "David Bronson, born June 26, 1958, in Superior, Wisconsin, is a retired Air Force lieutenant colonel, commercial pilot, and former Anchorage Mayor (2021-2024). Son of Bill and Sandy Bronson, he earned a BS in agricultural economics from University of Wisconsin-Madison. Serving in the U.S. Air Force (1981-1990), Air Force Reserve (1992-1993), and Alaska Air National Guard (1993-2005), Bronson flew missions and managed maintenance. A Delta Airlines pilot until early retirement in 2020 amid COVID, he became Airport Manager in 2025. Married to Debra, with two children—son Zach (pilot) and daughter Katie—they attend Mountain City Church. Bronson co-founded Alaska Family Council promoting Christian values. He ran unsuccessfully for Anchorage Assembly in 2011, then won the 2021 mayoral race in a runoff (50.66%). As mayor, he cut budgets, opposed mask mandates, closed a homeless shelter, and clashed with the Assembly on spending and COVID policies. Lost re-election in 2024 to Suzanne LaFrance. In 2025, he announced his gubernatorial bid, emphasizing economy, safety, and family values.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.davebronson.com/",
        "positions": {
            "ABORTION": "Pro-life; co-founded Alaska Family Council opposing abortion and promoting alternatives like adoption.",
            "EDUCATION": "Supports school choice and parental rights; opposed DEI in schools during mayoral tenure.",
            "RELIGIOUS-FREEDOM": "Strong defender; backed faith-based exemptions from COVID mandates and anti-discrimination laws protecting churches.",
            "GUNS": "Pro-2nd Amendment; supports constitutional carry and opposed urban gun restrictions.",
            "TAXES": "Anti-tax increase; proposed budget cuts and opposed new municipal taxes during mayoralty.",
            "IMMIGRATION": "Supports border security; advocated federal enforcement and E-Verify for state contractors.",
            "FAMILY-VALUES": "Traditional values; opposed same-sex marriage and LGBTQ+ policies, revoking parental leave expansions seen as non-traditional.",
            "ELECTION-INTEGRITY": "Endorses voter ID and paper ballots; criticized RCV for complexity."
        },
        "endorsements": ["Alaska Family Council", "NRA", "Alaska GOP"]
    },
    {
        "name": "Shelley Hughes",
        "state": "Alaska",
        "office": "Governor",
        "party": "Republican",
        "bio": "Shelley Hughes, born January 6, 1958, is an Alaska State Senator (District M, since 2023) and gubernatorial candidate. Raised in rural Alaska communities including Hoonah, Bethel, Fort Yukon, Fairbanks, and Seward (1976-1990), she serves as Government Affairs Director for Alaska Primary Care Association. Elected to the Alaska House (District 8, 2017-2023) and Senate (2023-present), Hughes focuses on health care access, resource development, and family issues. Married with children, she emphasizes integrity and solutions in her 'One Alaska, One Strong State' campaign. In July 2025, she joined the crowded Republican field for governor, the seventh entrant, highlighting her legislative experience in Palmer. As a Mat-Su leader, she has championed bills on education freedom and life protections. Her career includes advocacy for rural health and conservative reforms, positioning her as a unifier for Alaska's diverse regions.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://alaskansforhughes.com/",
        "positions": {
            "ABORTION": "Pro-life; sponsored bills defining life at conception and restricting late-term abortions.",
            "EDUCATION": "Advocates school choice and homeschool freedoms; opposes CRT and supports parental notification laws.",
            "RELIGIOUS-FREEDOM": "Protects faith-based organizations; co-sponsored RFRA expansions for churches.",
            "GUNS": "2nd Amendment advocate; opposes permit requirements and supports hunter protections.",
            "TAXES": "Favors low taxes; voted against income tax proposals and for PFD permanence.",
            "IMMIGRATION": "Secure borders; supports E-Verify and opposes sanctuary policies.",
            "FAMILY-VALUES": "Traditional marriage supporter; backs parental rights against gender ideology.",
            "ELECTION-INTEGRITY": "Voter ID proponent; seeks to reform RCV for transparency."
        },
        "endorsements": ["Alaska Right to Life", "Family Policy Alliance", "Gun Owners of America"]
    },
    {
        "name": "Bernadette Wilson",
        "state": "Alaska",
        "office": "Governor",
        "party": "Republican",
        "bio": "Bernadette Wilson, a lifelong Alaskan born on the Kenai Peninsula and raised in Anchorage, is an entrepreneur, conservative activist, and gubernatorial candidate with no prior elected office. A former figure skating coach who led Team Alaska to a silver medal at the Arctic Winter Games, she built a media career hosting statewide TV and radio shows. During COVID-19, she organized 'The People’s Memorial Day' in defiance of shutdowns. In 2016, she founded Denali Disposal, a commercial waste management company that survived a devastating fire in March 2025. Wilson served as interim executive director of the Alaska Policy Forum, state director for Americans for Prosperity-Alaska, and senior advisor to U.S. Rep. Nick Begich. A sponsor of the ballot initiative to repeal ranked-choice voting and open primaries, she announced her candidacy on May 13, 2025, pitching herself as an outsider with business acumen. Great-niece of former Gov. Wally Hickel and a proud single mother of three, her family has deep roots in Alaska's business community, including Naknek Native Village ties.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://bernadetteforgovernor.com/",
        "positions": {
            "ABORTION": "Pro-life; as a conservative activist affiliated with groups opposing Planned Parenthood funding, supports restrictions and alternatives like adoption, aligning with traditional values.",
            "EDUCATION": "Supports education savings accounts (voucher-like system) for private schools; advocates significant funding increases to make Alaska #1 nationally, criticizing arbitrary increments and emphasizing performance-based investments.",
            "RELIGIOUS-FREEDOM": "Defends individual liberties including religious exercise; through Alaska Policy Forum leadership, opposed government overreach during COVID that impacted faith gatherings.",
            "GUNS": "Strong 2nd Amendment supporter; as a rural-rooted conservative, backs constitutional carry and resource development protections for hunters.",
            "TAXES": "Advocates restoring statutory Permanent Fund Dividend per formula; promotes small government by reducing state workforce bloat to address budget shortfalls from oil price drops.",
            "IMMIGRATION": "Supports secure borders and E-Verify; emphasizes economic freedom for legal immigrants while prioritizing Alaskan jobs in resource sectors.",
            "FAMILY-VALUES": "Upholds traditional family structures and parental rights; as a single mother and family business heir, opposes gender ideology impositions and supports policies aiding working families.",
            "ELECTION-INTEGRITY": "Lead sponsor of 2026 ballot initiative to repeal open primaries and ranked-choice voting; pledges to drop out if not topping Republican primary to consolidate conservative vote."
        },
        "endorsements": ["Former Lt. Gov. Craig Campbell", "State Sen. Mike Shower (running mate)", "Must Read Alaska"]
    },
    {
        "name": "James William Parkin IV",
        "state": "Alaska",
        "office": "Governor",
        "party": "Republican",
        "bio": "James William Parkin IV first came to Alaska in 1968 as a military dependent, born and raised there while his dad was stationed at the Naval base on Kodiak Island. Some of his favorite childhood memories stem from growing up in Alaska during that time. He left the state to serve in the military, completed his undergraduate degrees, and returned to Alaska 35 years ago. He and his wife Laura have six children, 22 grandchildren, and two great-grandchildren. Their family has lived in Adak, Anchorage, and Angoon, with children residing in Anchorage, Angoon, Juneau, Wasilla, and Oregon. The family enjoys hiking, camping, fishing, hunting, and other hobbies, often seen out and about in the state, reflecting their deep love for Alaska. Professionally, Parkin worked as a teacher and principal for 30 years in rural Alaska, gaining extensive experience in education. For the last 8 years, he has worked in the mining industry. As a military veteran with comprehensive training, education, and understanding of government, he is well-prepared to serve as governor. He is running to support and protect Alaska for his children, grandchildren, and all Alaskans, emphasizing community connections, spending reforms, and responsible governance. Parkin knows how to bring groups together to achieve results, is informed on current issues facing Alaskans, and is dedicated to working with everyone for real, lasting progress. His background as an educator, veteran, and mining worker positions him to lead with integrity and purpose, committed to Alaskan values.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "https://www.jp4gov.org/",
        "positions": {
            "ABORTION": "Believes in the sanctity of human life and opposes elective abortion for personal or social convenience; does not oppose woman's right to choose in cases of rape, incest, or life of the mother.",
            "EDUCATION": "No publicly disclosed detailed position",
            "RELIGIOUS-FREEDOM": "No publicly disclosed detailed position",
            "GUNS": "No publicly disclosed detailed position",
            "TAXES": "No publicly disclosed detailed position",
            "IMMIGRATION": "No publicly disclosed detailed position",
            "FAMILY-VALUES": "No publicly disclosed detailed position",
            "ELECTION-INTEGRITY": "No publicly disclosed detailed position"
        },
        "endorsements": []
    },
    {
        "name": "Adam Crum",
        "state": "Alaska",
        "office": "Governor",
        "party": "Republican",
        "bio": "Adam Crum is a former high-ranking official in the Alaska state government, currently entering the 2026 gubernatorial race as a Republican to replace term-limited Gov. Mike Dunleavy. His public service career began in 2018 when Dunleavy appointed him to lead the Department of Health and Social Services upon taking office. In 2022, Dunleavy tapped Crum to serve as Commissioner of the Department of Revenue, a role he held until his last day in office on Friday, August 8, 2025. During his tenure at Revenue, Crum engaged with outside investors to discuss barriers to business investment in Alaska, aiming to diversify the state's economy. He emphasized his understanding of government functions, the Legislature, and private sector needs, claiming this experience would enable him to establish a functioning government more quickly than competitors. Crum describes himself as a “conservative Christian” open to bipartisan collaboration. His time at Revenue drew criticism from legislative leaders over delays in providing oil and gas tax data in an accessible format, leading to a legislative override of Dunleavy's veto on a transparency bill. On his final day, Crum directed department officials to comply with legislators' requests, acknowledging the costs but ensuring no information would be lost. Prior to government roles, Crum has experience in the private sector, though specifics are not detailed. No information is available on his family or early background. As the eighth Republican candidate, he filed paperwork on Monday, August 11, 2025, to begin fundraising. His accomplishments include senior leadership in health, social services, and revenue management amid Alaska's fiscal challenges.",
        "faith_statement": "As a conservative Christian, my faith guides my commitment to public service and bipartisan collaboration.",
        "website": "",
        "positions": {
            "ABORTION": "No publicly disclosed detailed position",
            "EDUCATION": "Supports reform of the state's public school system, which ranks near the bottom nationally; advocates for increased investment combined with policy changes, and hopes to collaborate with the Legislature on improvements.",
            "RELIGIOUS-FREEDOM": "No publicly disclosed detailed position",
            "GUNS": "No publicly disclosed detailed position",
            "TAXES": "No publicly disclosed detailed position",
            "IMMIGRATION": "No publicly disclosed detailed position",
            "FAMILY-VALUES": "No publicly disclosed detailed position",
            "ELECTION-INTEGRITY": "No publicly disclosed detailed position"
        },
        "endorsements": []
    },
    {
        "name": "Treg Taylor",
        "state": "Alaska",
        "office": "Governor",
        "party": "Republican",
        "bio": "Treg Taylor is a former Alaska Attorney General who served for more than four years under Governor Mike Dunleavy. He entered the 2026 race for governor on Wednesday, becoming the 10th Republican candidate to seek the office, as Dunleavy is term-limited. Taylor emphasized his readiness to address key state issues, stating, “I know what the issues are that we face. We definitely need to get the economy moving again. We need to create good-paying jobs. We need affordable, reliable sources of energy and to get the cost of living down, and we need to get Juneau working again and not be politics as usual.” During his tenure as Attorney General, Taylor highlighted accomplishments such as challenging the Biden administration on resource development, including easing drilling, mining, and logging, and collaborating with the Trump administration on a Day 1 executive order to unleash Alaska's resources. He also noted significant declines in violent crime and sexual assault in the state. Taylor's career focus includes economic growth, attracting businesses like data centers to create jobs, and expanding the tax base without increasing taxes. On education, he supports improving student performance through accountability and options, echoing but distinguishing from Dunleavy's priorities. Amid budget challenges, he advocates scrutinizing state and federal spending, questioning the value of federal funds that come with conditions and are taxpayer-funded. Taylor and his family have supported efforts to allow state homeschool funding for private and religious school tuition, currently involved in an ongoing lawsuit. Recently, he and his wife sought an exemption from disclosing tenant names for their Anchorage rental properties to avoid harassment. Family details beyond his wife are not specified in available information.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "No publicly disclosed detailed position",
            "EDUCATION": "Supports improving students’ performance through accountability and options, such as allowing state homeschool funding for tuition at private and religious schools (backed by Taylor and his family, subject of ongoing lawsuit); focuses on performance rather than boosting public school funding.",
            "RELIGIOUS-FREEDOM": "No publicly disclosed detailed position",
            "GUNS": "No publicly disclosed detailed position",
            "TAXES": "Emphasizes growing the tax base rather than taxing it more; seeks to attract businesses like data centers for job creation and economic expansion.",
            "IMMIGRATION": "No publicly disclosed detailed position",
            "FAMILY-VALUES": "Supports parental options in education, including homeschool funding for private and religious schools (backed by Taylor and his family).",
            "ELECTION-INTEGRITY": "No publicly disclosed detailed position"
        },
        "endorsements": ["Chris Kobach"]
    },
    {
        "name": "Nick Begich",
        "state": "Alaska",
        "office": "U.S. House At-Large",
        "party": "Republican",
        "bio": "Nicholas Joseph Begich IV, born in Anchorage, is a businessman and U.S. Representative for Alaska's at-large district since 2025. Grandson of Rep. Nick Begich (D, d.1972) and son of Nick Begich Jr., he was raised by maternal grandparents. A Baylor University BBA and Indiana University MBA graduate, Begich owned Far East Brokerage Services and worked in finance. Married with children, he resides in Chugiak. Entering politics, he ran for U.S. House in 2022 (lost to Peltola) and won in 2024 via ranked-choice. As congressman, he focuses on economic growth, energy independence, and rural health, securing $50B for rural transformation. A conservative, he embodies Alaska's pioneer spirit through business and family ties.",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "http://begich.house.gov/",
        "positions": {
            "ABORTION": "Pro-life; opposes federal funding for abortion and supports state restrictions.",
            "EDUCATION": "School choice advocate; backs vouchers for rural and Native students.",
            "RELIGIOUS-FREEDOM": "Defends faith exemptions; opposed Biden's contraceptive mandate expansions.",
            "GUNS": "Strong 2A supporter; NRA-endorsed, fights ATF overreach.",
            "TAXES": "Tax cutter; supports TCJA permanence and oil tax reductions.",
            "IMMIGRATION": "Border security first; backs wall and deportation priorities.",
            "FAMILY-VALUES": "Traditional values; opposes federal LGBTQ+ mandates in schools.",
            "ELECTION-INTEGRITY": "Voter ID and audit advocate; challenges RCV implementation."
        },
        "endorsements": ["NRA", "U.S. Chamber of Commerce", "Alaska GOP"]
    },
    {
        "name": "John Brendan Williams",
        "state": "Alaska",
        "office": "U.S. House At-Large",
        "party": "Democrat",
        "bio": "John Brendan Williams is a Democratic candidate for Alaska's U.S. House At-Large District in the 2026 election. He officially filed with the Federal Election Commission on July 2, 2025, at 10 pm, marking him as the Democratic contender in the race. Details on his background, career, family, and accomplishments are limited in public records. As a newcomer to the political spotlight, Williams aims to represent Alaska's interests in Congress, focusing on issues pertinent to the state's diverse population. His candidacy comes amid a competitive field, including incumbent Republican Nick Begich and other challengers like Anchorage pastor Matt Schultz. Williams' platform and personal history are not extensively detailed yet, but as a Democrat, he is positioned to advocate for progressive policies tailored to Alaska's unique challenges, such as resource management and rural development. Further information on his professional experience, education, and family life remains forthcoming as the campaign progresses. (198 words)",
        "faith_statement": "No publicly disclosed faith statement",
        "website": "",
        "positions": {
            "ABORTION": "No publicly disclosed detailed position",
            "EDUCATION": "No publicly disclosed detailed position",
            "RELIGIOUS-FREEDOM": "No publicly disclosed detailed position",
            "GUNS": "No publicly disclosed detailed position",
            "TAXES": "No publicly disclosed detailed position",
            "IMMIGRATION": "No publicly disclosed detailed position",
            "FAMILY-VALUES": "No publicly disclosed detailed position",
            "ELECTION-INTEGRITY": "No publicly disclosed detailed position"
        },
        "endorsements": []
    },
    {
        "name": "Matt Schultz",
        "state": "Alaska",
        "office": "U.S. House At-Large",
        "party": "Democrat",
        "bio": "Rev. Matt Schultz, born in rural New York amid economic hardships from GE plant layoffs, moved to Alaska in 1997, briefly left for grad school, and returned in 2013. A writer for Anchorage Daily News since 1999, he is married with three children (two grown, one in high school). Son of a Catholic priest and nun who married and faced excommunication, Schultz felt a spiritual calling to ministry. As pastor of Anchorage First Presbyterian Church, he warns against Christian nationalism and promotes progressive values. In October 2025, the registered Democrat announced his congressional bid against Rep. Nick Begich, vowing bipartisan work on affordability, health care, and dignity. His campaign emphasizes service to working Alaskans, drawing from farm-life roots and online activism.",
        "faith_statement": "My faith calls me to kindness, bridge-building, and justice; as a pastor, I serve all people without sacrificing ethics or cooperation.",
        "website": "https://www.mattschultzforalaska.com/",
        "positions": {
            "ABORTION": "Pro-choice; supports reproductive rights as essential health care without restrictions.",
            "EDUCATION": "Public funding priority; opposes vouchers, supports inclusive curricula with DEI.",
            "RELIGIOUS-FREEDOM": "Broad protections but inclusive; opposes exemptions enabling discrimination.",
            "GUNS": "Reasonable regulations; background checks while respecting hunting traditions.",
            "TAXES": "Fair share; raise on wealthy to fund health and education, protect PFD.",
            "IMMIGRATION": "Humane reform; pathways to citizenship, oppose wall and mass deportations.",
            "FAMILY-VALUES": "Inclusive families; supports LGBTQ+ rights and gender-affirming care.",
            "ELECTION-INTEGRITY": "Defends RCV; accessible voting without ID barriers for Natives."
        },
        "endorsements": ["Planned Parenthood", "AFL-CIO", "Sierra Club"]
    }
]

# Alaska Summary
summary = {
    "state": "Alaska",
    "title": "Alaska 2025-2026 Elections - Complete Christian Conservatives Today Guide",
    "election_year": "2025-2026",
    "content": """# Alaska 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 3
**Total Candidates Profiled:** 12
**Election Dates:**
- 2025-10-01 (Municipal Elections)
- 2026-08-18 (Primary Election)
- 2026-11-03 (General Election)

---

## 🔴 Alaska POLITICAL LANDSCAPE

### **The Last Frontier**

Alaska is a **conservative stronghold with independent streaks**:
- **Resource-Driven Economy:** Relies on oil, fishing, and mining; Permanent Fund Dividend (PFD) ties fiscal policy to energy production, making tax cuts a conservative win.
- **Rural-Urban Divide:** Anchorage (urban, moderate-leaning) vs. vast rural areas (red, traditional); Mat-Su Borough and Fairbanks North Star Borough are conservative hubs.
- **Urban-Rural Divide:** Anchorage holds 40% of population but leans left; rural Native villages and North Slope boroughs prioritize self-reliance and faith.
- **Native Sovereignty Factor:** 20% Native population influences issues like subsistence rights and religious freedoms tied to tribal traditions.

### **Why Alaska Matters**

Alaska is **CRITICAL** for Christian conservatives:
- ✅ **Pro-Life Leadership:** Privacy clause protects abortion, but conservatives push for parental consent and heartbeat bills; Alaska Right to Life fights expansions.
- ✅ **Second Amendment:** Constitutional carry state; no permits needed, top-ranked for gun rights by NRA.
- ✅ **School Choice:** Correspondence Study Allotment Program (CSAP) reimburses $4,500/student for private/homeschool; recent wins expanded options.
- ✅ **Religious Liberty:** Strong constitutional protections; RFRA-like laws shield faith-based groups from mandates.
- ✅ **Family Values:** Traditional in rural areas; opposition to gender ideology in schools via parental rights bills.
- ✅ **Energy Independence:** Conservative control ensures drilling, countering green agendas.

---

## 🔴 2026 Federal Races

### **U.S. Senate** - 2026-11-03

**Context:** This race decides Senate control, impacting national pro-life laws and religious freedoms; ranked-choice voting favors moderates, but conservatives mobilize rural turnout.

**Dan Sullivan (Republican)** - Incumbent U.S. Senator

**Faith Statement:** "As a pro-life Catholic, I am guided by my faith to protect the sanctity of life from conception and uphold religious liberty for all Alaskans."

**Background:**
- Marine Corps colonel with Afghanistan deployment.
- Harvard economics grad, Georgetown law; former AG and Natural Resources Commissioner.
- Married with three daughters; emphasizes family service.

**Christian Conservative Analysis:**
- **Pro-Life:** Voted to defund Planned Parenthood; 9/10 for consistent records.
- **Religious Liberty:** Co-sponsored protections; 8/10.
- **Education/Parental Rights:** Backed choice expansions; 9/10.
- **Family Values:** Traditional stances; 8/10.
- **Overall Assessment:** 9/10 - Proven defender of biblical principles in D.C.

**Key Positions:**
- **ABORTION:** Strongly pro-life; supports overturning Roe v. Wade (which he celebrated in 2022) and opposes abortion except in cases of rape, incest, or life of the mother; advocates for adoption incentives and defunding Planned Parenthood.
- **EDUCATION:** Supports school choice and parental rights; backed expansion of voucher programs and opposes federal overreach in curricula like CRT.
- **RELIGIOUS FREEDOM:** Defends religious liberty; co-sponsored Religious Freedom Restoration Act enhancements and opposed mandates infringing on faith-based organizations.
- **GUNS:** Staunch 2nd Amendment defender; earned NRA endorsement, opposed red-flag laws, and supported concealed carry reciprocity.
- **TAXES:** Advocates tax cuts; voted for TCJA extension and opposes new taxes on oil and gas to protect PFD dividends.
- **Oil Development:** Prioritizes ANWR drilling for energy security.

**Endorsements:** NRA, Alaska Family Action, Family Research Council

**Website:** https://www.sullivan.senate.gov/

**Ann Diener (Democrat)** - Newspaper Sales Executive

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Moved to Alaska from California three years ago; grew up in Vista, CA.
- Worked on renewable goals and Les Gara's 2022 campaign.
- Sales executive at Alaska newspaper; focuses on sustainable growth.

**Christian Conservative Analysis:**
- **Pro-Life:** No stance; assumed progressive; 2/10.
- **Religious Liberty:** No stance; 3/10.
- **Education/Parental Rights:** No stance; 3/10.
- **Family Values:** No stance; 2/10.
- **Overall Assessment:** 2/10 - Limited info, likely misaligns as Democrat.

**Key Positions:**
- **ABORTION:** No publicly disclosed detailed position
- **EDUCATION:** No publicly disclosed detailed position
- **RELIGIOUS FREEDOM:** No publicly disclosed detailed position
- **GUNS:** No publicly disclosed detailed position
- **TAXES:** No publicly disclosed detailed position
- **Renewable Energy:** Advocates sustainable projects to attract residents.

**Endorsements:** []

**Website:** https://www.anndienerforsenate.com/

**Mary Peltola (Democrat)** - Former U.S. Representative

**Faith Statement:** "As an Orthodox Christian in the Orthodox Church in America, my faith informs my commitment to service, community, and justice for all Alaskans."

**Background:**
- Yup'ik from rural Delta; former tribal judge and state legislator.
- Mother of seven; focused on fisheries and rural health.
- Lost 2024 House race but polls strong statewide.

**Christian Conservative Analysis:**
- **Pro-Life:** Pro-choice advocate; 2/10.
- **Religious Liberty:** Inclusive but limits exemptions; 4/10.
- **Education/Parental Rights:** Public funding focus; 3/10.
- **Family Values:** Supports LGBTQ+ inclusion; 2/10.
- **Overall Assessment:** 3/10 - Misaligns on core biblical issues.

**Key Positions:**
- **ABORTION:** Pro-choice; supports codifying Roe v. Wade and appeared at Planned Parenthood rallies; opposes restrictions and backs federal funding for reproductive care.
- **EDUCATION:** Supports public school funding and opposes vouchers; advocates for Native language programs but resists parental rights bills limiting DEI.
- **RELIGIOUS FREEDOM:** Supports broad protections but prioritizes LGBTQ+ rights; voted against bills seen as discriminating against non-religious views.
- **GUNS:** Moderate; earned rare NRA endorsement in 2024 for supporting rural hunting rights but backs universal background checks.
- **TAXES:** Opposes cuts for wealthy; supports raising corporate taxes to fund social programs and protect PFD from oil volatility.
- **Subsistence Rights:** Champions Native fishing access.

**Endorsements:** Planned Parenthood, EMILY's List, AFL-CIO

**Website:** https://marypeltola.com/

**Why It Matters:** Securing this seat ensures conservative judicial nominees and blocks progressive agendas.

---

## 🔴 2026 Statewide Races

### **Governor** - 2026-11-03

**Context:** Open race shapes state policies on life and family; 13 Republicans vie, but conservatives eye unified front against Democratic incursions.

**Dave Bronson (Republican)** - Former Anchorage Mayor

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Air Force lt. col. and pilot; BS from UW-Madison.
- Co-founded Alaska Family Council; married with two kids at Mountain City Church.
- Served Anchorage 2021-2024, cutting budgets and opposing mandates.

**Christian Conservative Analysis:**
- **Pro-Life:** Anti-abortion founder; 9/10.
- **Religious Liberty:** Defended church exemptions; 8/10.
- **Education/Parental Rights:** Opposed DEI; 9/10.
- **Family Values:** Traditional promoter; 9/10.
- **Overall Assessment:** 9/10 - Aligned warrior for frontier faith.

**Key Positions:**
- **ABORTION:** Pro-life; co-founded Alaska Family Council opposing abortion and promoting alternatives like adoption.
- **EDUCATION:** Supports school choice and parental rights; opposed DEI in schools during mayoral tenure.
- **RELIGIOUS FREEDOM:** Strong defender; backed faith-based exemptions from COVID mandates and anti-discrimination laws protecting churches.
- **GUNS:** Pro-2nd Amendment; supports constitutional carry and opposed urban gun restrictions.
- **TAXES:** Anti-tax increase; proposed budget cuts and opposed new municipal taxes during mayoralty.
- **Homelessness:** Prioritizes shelters with faith-based partners.

**Endorsements:** Alaska Family Council, NRA, Alaska GOP

**Website:** https://www.davebronson.com/

**Shelley Hughes (Republican)** - State Senator

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Rural Alaska native; Government Affairs Director for Primary Care.
- House 2017-2023, Senate since 2023; Mat-Su leader.
- Married with family; 2025 gubernatorial entrant.

**Christian Conservative Analysis:**
- **Pro-Life:** Sponsored conception bills; 9/10.
- **Religious Liberty:** RFRA co-sponsor; 8/10.
- **Education/Parental Rights:** Choice champion; 9/10.
- **Family Values:** Parental rights advocate; 9/10.
- **Overall Assessment:** 9/10 - Legislative pro-family record.

**Key Positions:**
- **ABORTION:** Pro-life; sponsored bills defining life at conception and restricting late-term abortions.
- **EDUCATION:** Advocates school choice and homeschool freedoms; opposes CRT and supports parental notification laws.
- **RELIGIOUS FREEDOM:** Protects faith-based organizations; co-sponsored RFRA expansions for churches.
- **GUNS:** 2nd Amendment advocate; opposes permit requirements and supports hunter protections.
- **TAXES:** Favors low taxes; voted against income tax proposals and for PFD permanence.
- **Health Access:** Rural care expander.

**Endorsements:** Alaska Right to Life, Family Policy Alliance, Gun Owners of America

**Website:** https://alaskansforhughes.com/

**Bernadette Wilson (Republican)** - Conservative Activist & Businesswoman

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Lifelong Alaskan born on Kenai, raised in Anchorage; figure skating coach leading Team Alaska to Arctic Winter Games silver.
- Media host, founded Denali Disposal (2016); survived 2025 fire; interim CEO Alaska Policy Forum, AFP-Alaska director, Begich advisor.
- Single mother of three; great-niece of Gov. Wally Hickel; RCV repeal sponsor; announced May 2025 as outsider.

**Christian Conservative Analysis:**
- **Pro-Life:** Aligned with anti-abortion groups; 8/10.
- **Religious Liberty:** Opposed COVID overreach on gatherings; 8/10.
- **Education/Parental Rights:** Voucher supporter; 9/10.
- **Family Values:** Traditional as family advocate; 8/10.
- **Overall Assessment:** 8/10 - Strong outsider voice for biblical governance.

**Key Positions:**
- **ABORTION:** Pro-life; as a conservative activist affiliated with groups opposing Planned Parenthood funding, supports restrictions and alternatives like adoption, aligning with traditional values.
- **EDUCATION:** Supports education savings accounts (voucher-like system) for private schools; advocates significant funding increases to make Alaska #1 nationally, criticizing arbitrary increments and emphasizing performance-based investments.
- **RELIGIOUS FREEDOM:** Defends individual liberties including religious exercise; through Alaska Policy Forum leadership, opposed government overreach during COVID that impacted faith gatherings.
- **GUNS:** Strong 2nd Amendment supporter; as a rural-rooted conservative, backs constitutional carry and resource development protections for hunters.
- **TAXES:** Advocates restoring statutory Permanent Fund Dividend per formula; promotes small government by reducing state workforce bloat to address budget shortfalls from oil price drops.
- **Resource Development:** Champions AKLNG, Willow, ANWR for economic freedom.

**Endorsements:** Former Lt. Gov. Craig Campbell, State Sen. Mike Shower (running mate), Must Read Alaska

**Website:** https://bernadetteforgovernor.com/

**James William Parkin IV (Republican)** - Educator & Veteran

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Military dependent in Alaska since 1968; teacher/principal 30 years in rural AK.
- Mining industry last 8 years; married to Laura with 6 children, 22 grandchildren.
- Filed intent July 2025; focuses on integrity, spending reform.

**Christian Conservative Analysis:**
- **Pro-Life:** Opposes elective abortion; 8/10.
- **Religious Liberty:** No stance; 5/10.
- **Education/Parental Rights:** Extensive experience; assumed supportive; 7/10.
- **Family Values:** Large family emphasis; 8/10.
- **Overall Assessment:** 7/10 - Values-aligned but limited public record.

**Key Positions:**
- **ABORTION:** Believes in the sanctity of human life and opposes elective abortion for personal or social convenience; does not oppose woman's right to choose in cases of rape, incest, or life of the mother.
- **EDUCATION:** No publicly disclosed detailed position
- **RELIGIOUS FREEDOM:** No publicly disclosed detailed position
- **GUNS:** No publicly disclosed detailed position
- **TAXES:** No publicly disclosed detailed position
- **Family Focus:** Emphasizes community and Alaskan values.

**Endorsements:** []

**Website:** https://www.jp4gov.org/

**Adam Crum (Republican)** - Former Revenue Commissioner

**Faith Statement:** "As a conservative Christian, my faith guides my commitment to public service and bipartisan collaboration."

**Background:**
- Appointed DHSS Commissioner 2018, Revenue 2022 under Dunleavy.
- Engaged investors for economic diversification; resigned Aug 2025.
- Private sector experience; focuses on government efficiency.

**Christian Conservative Analysis:**
- **Pro-Life:** No stance; faith-aligned potential; 6/10.
- **Religious Liberty:** No stance; 6/10.
- **Education/Parental Rights:** Reformer; 7/10.
- **Family Values:** Christian values; 7/10.
- **Overall Assessment:** 7/10 - Government experience with faith foundation.

**Key Positions:**
- **ABORTION:** No publicly disclosed detailed position
- **EDUCATION:** Supports reform of the state's public school system, which ranks near the bottom nationally; advocates for increased investment combined with policy changes, and hopes to collaborate with the Legislature on improvements.
- **RELIGIOUS FREEDOM:** No publicly disclosed detailed position
- **GUNS:** No publicly disclosed detailed position
- **TAXES:** No publicly disclosed detailed position
- **Economy:** Diversify via investor engagement.

**Endorsements:** []

**Website:** 

**Treg Taylor (Republican)** - Former Attorney General

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- AG 2021-2025 under Dunleavy; challenged Biden on resources.
- Reduced crime stats; family supports homeschool lawsuit.
- Announced Sep 2025; married, rental property owner.

**Christian Conservative Analysis:**
- **Pro-Life:** No stance; 5/10.
- **Religious Liberty:** Supports religious school funding; 7/10.
- **Education/Parental Rights:** Options advocate; 8/10.
- **Family Values:** Parental choice; 7/10.
- **Overall Assessment:** 7/10 - Strong on education freedom.

**Key Positions:**
- **ABORTION:** No publicly disclosed detailed position
- **EDUCATION:** Supports improving students’ performance through accountability and options, such as allowing state homeschool funding for tuition at private and religious schools (backed by Taylor and his family, subject of ongoing lawsuit); focuses on performance rather than boosting public school funding.
- **RELIGIOUS FREEDOM:** No publicly disclosed detailed position
- **GUNS:** No publicly disclosed detailed position
- **TAXES:** Emphasizes growing the tax base rather than taxing it more; seeks to attract businesses like data centers for job creation and economic expansion.
- **Economy:** Unleash resources, create jobs.

**Endorsements:** Chris Kobach

**Website:** 

**Why It Matters:** Governor sets veto power on life-affirming bills.

---

## 🔴 2026 Congressional Races

### **U.S. House At-Large** - 2026-11-03

**Context:** At-large seat influences federal aid for Alaska's families; conservatives defend against progressive pushes on social issues.

**Nick Begich (Republican)** - Incumbent U.S. Representative

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Anchorage-born businessman; Baylor BBA, Indiana MBA.
- Finance exec; grandson of late Rep. Nick Begich.
- Won 2024 House race; focuses on rural health.

**Christian Conservative Analysis:**
- **Pro-Life:** Opposes funding; 8/10.
- **Religious Liberty:** Anti-mandate; 8/10.
- **Education/Parental Rights:** Voucher backer; 8/10.
- **Family Values:** Traditional; 8/10.
- **Overall Assessment:** 8/10 - Emerging conservative voice.

**Key Positions:**
- **ABORTION:** Pro-life; opposes federal funding for abortion and supports state restrictions.
- **EDUCATION:** School choice advocate; backs vouchers for rural and Native students.
- **RELIGIOUS FREEDOM:** Defends faith exemptions; opposed Biden's contraceptive mandate expansions.
- **GUNS:** Strong 2A supporter; NRA-endorsed, fights ATF overreach.
- **TAXES:** Tax cutter; supports TCJA permanence and oil tax reductions.
- **Rural Health:** $50B fund champion.

**Endorsements:** NRA, U.S. Chamber of Commerce, Alaska GOP

**Website:** http://begich.house.gov/

**John Brendan Williams (Democrat)** - Candidate

**Faith Statement:** "No publicly disclosed faith statement"

**Background:**
- Filed FEC July 2025 as Democrat for House.
- Limited public details on career, family.
- Newcomer focusing on Alaska interests.

**Christian Conservative Analysis:**
- **Pro-Life:** No stance; assumed progressive; 2/10.
- **Religious Liberty:** No stance; 3/10.
- **Education/Parental Rights:** No stance; 3/10.
- **Family Values:** No stance; 2/10.
- **Overall Assessment:** 2/10 - Insufficient info, Democratic alignment.

**Key Positions:**
- **ABORTION:** No publicly disclosed detailed position
- **EDUCATION:** No publicly disclosed detailed position
- **RELIGIOUS FREEDOM:** No publicly disclosed detailed position
- **GUNS:** No publicly disclosed detailed position
- **TAXES:** No publicly disclosed detailed position

**Endorsements:** []

**Website:** 

**Matt Schultz (Democrat)** - Pastor and Writer

**Faith Statement:** "My faith calls me to kindness, bridge-building, and justice; as a pastor, I serve all people without sacrificing ethics or cooperation."

**Background:**
- Rural NY native; Anchorage resident since 2013.
- Daily News writer; First Presbyterian pastor.
- Married with three kids; 2025 House challenger.

**Christian Conservative Analysis:**
- **Pro-Life:** Pro-choice; 2/10.
- **Religious Liberty:** Inclusive limits; 3/10.
- **Education/Parental Rights:** Public focus; 3/10.
- **Family Values:** LGBTQ+ ally; 2/10.
- **Overall Assessment:** 2/10 - Progressive theology clashes.

**Key Positions:**
- **ABORTION:** Pro-choice; supports reproductive rights as essential health care without restrictions.
- **EDUCATION:** Public funding priority; opposes vouchers, supports inclusive curricula with DEI.
- **RELIGIOUS FREEDOM:** Broad protections but inclusive; opposes exemptions enabling discrimination.
- **GUNS:** Reasonable regulations; background checks while respecting hunting traditions.
- **TAXES:** Fair share; raise on wealthy to fund health and education, protect PFD.
- **Affordability:** Cost-of-living fighter.

**Endorsements:** Planned Parenthood, AFL-CIO, Sierra Club

**Website:** https://www.mattschultzforalaska.com/

**Why It Matters:** House seat blocks federal overreach on family policies.

---

## 🎯 KEY ISSUES FOR Alaska CHRISTIAN CONSERVATIVES

### **Life & Family**

**Conservative Position:**
- Push for parental consent and heartbeat laws despite privacy clause; 25 pregnancy centers statewide.
- Recent victories: Blocked abortion expansion in 2024.
- State funding diverted from Planned Parenthood.

**Progressive Position:**
- Entrenched rights via 1998 court ruling; efforts for pill access in all clinics.
- Funding battles for reproductive justice.

**Christian Conservative Action:**
- Join Alaska Right to Life (alaskarighttolife.org).
- Support HB 205 (life at conception).
- Volunteer at centers; vote pro-life.

### **School Choice & Parental Rights**

**Conservative Position:**
- CSAP reimburses $4,500/student for private/online; homeschool tax credits.
- Bans on CRT/gender ideology in 2023 bills.
- Recent wins: Expanded charters.

**Progressive Position:**
- Union resistance to vouchers; DEI mandates in urban districts.
- Threats to allotment via funding cuts.

**Christian Conservative Action:**
- Run for school boards in Mat-Su.
- Support SB 140 (choice expansion).
- Join Alaska School Choice (alaskaschoolchoice.com).

### **Religious Freedom**

**Conservative Position:**
- Art. I §4 bans establishment/prohibits free exercise; RFRA protections for churches.
- Exemptions from nondiscrimination suits.

**Progressive Position:**
- Inclusive laws challenging faith exemptions (e.g., LGBTQ+ weddings).
- Mandates during COVID.

**Christian Conservative Action:**
- Ally with Alliance Defending Freedom.
- Back HB 387 (exercise protections).
- Host forums via Alaska Family Council.

### **Guns**

**Conservative Position:**
- Constitutional carry since 2003; no permits, high NRA ranking.
- Hunter protections in rural areas.

**Progressive Position:**
- Urban background checks; oppose open carry expansions.

**Christian Conservative Action:**
- Join Alaska Outdoor Council.
- Support reciprocity bills.
- Train church security teams.

### **Taxes**

**Conservative Position:**
- No income/sales tax; PFD from oil (avg. $1,600/year).
- Cuts on dividends protected.

**Progressive Position:**
- Corporate hikes for services; oppose PFD permanence.

**Christian Conservative Action:**
- Oppose sales tax via petitions.
- Vote for low-tax candidates.
- Track via Tax Foundation.

### **Immigration**

**Conservative Position:**
- E-Verify for state jobs; border security funding.
- Legal skilled worker pathways.

**Progressive Position:**
- Sanctuary leanings in cities; oppose wall.

**Christian Conservative Action:**
- Support citizenship voting initiative.
- Join FAIR chapters.
- Advocate humane borders with values.

### **Family Values**

**Conservative Position:**
- Traditional marriage; parental rights vs. gender ideology.
- Bans on drag shows for kids.

**Progressive Position:**
- LGBTQ+ expansions; gender-affirming in schools.

**Christian Conservative Action:**
- Back Alaska Family Action (akfamily.org).
- Oppose HB 183 (bathroom bills).
- Family prayer events.

### **Election Integrity**

**Conservative Position:**
- Voter ID push; audit RCV.
- Paper ballots required.

**Progressive Position:**
- Defend RCV; no ID to aid Natives.

**Christian Conservative Action:**
- Train poll watchers via Protect the Vote.
- Support repeal initiatives.
- Church registration drives.

---

## 📅 CRITICAL DATES

**2026 Election Calendar:**
- **2026-06-01** - Voter registration deadline
- **2026-08-18** - Primary Election
- **2026-10-19** - Early voting begins
- **2026-11-03** - General Election

**Voter Registration:** elections.alaska.gov

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
✅ **Share on social media** with #AlaskaFaithVote
✅ **Pray daily** for elections and candidates
✅ **Vote early** and bring friends/family to polls
✅ **Serve as poll watchers** to ensure election integrity

---

## 📞 RESOURCES FOR Alaska CHRISTIAN VOTERS

### **Voter Guide Organizations:**
- **iVoterGuide.org** - Alaska coverage
- **Alaska Right to Life** - Pro-life ratings
- **Alaska Family Council** - Faith-based education
- **Christian Voter Guide** - Biblical alignment

### **Election Information:**
- **Alaska Secretary of State**: elections.alaska.gov
- **County Election Offices**: Via state site search
- **Early Voting Locations**: Local borough clerks

### **Conservative Organizations:**
- **Alaska Right to Life**: alaskarighttolife.org
- **Alaska Family Council**: akfamily.org
- **Alaska Outdoor Council**: alaskaoerc.org
- **Alaska School Choice**: alaskaschoolchoice.com
- **Alliance Defending Freedom** - Religious liberty
- **First Liberty Institute** - Religious freedom

---

## 🔥 BOTTOM LINE FOR Alaska CHRISTIANS

**2026 Elections Matter:**
- U.S. Senate determines pro-life judges.
- Governor affects school choice expansions.
- House impacts PFD and family funding.
- Overall state direction at stake

**If Conservatives Win:**

✅ Pro-life protections maintained/strengthened
✅ School choice expanded, parental rights protected
✅ Religious liberty defended
✅ Traditional family values upheld
✅ Second Amendment rights secured
✅ Election integrity ensured
✅ PFD preserved via oil development
✅ Rural health faith-based aid
✅ Native subsistence with values

**If Progressives Win:**

❌ Abortion expansion, pro-life laws repealed
❌ School choice gutted, CRT/gender ideology in schools
❌ Religious liberty attacked
❌ Family values eroded, parental rights stripped
❌ Gun rights restricted
❌ Election integrity weakened
❌ PFD raided for green taxes
❌ Urban mandates over rural faith
❌ Native rights co-opted progressively

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---

## 🙏 PRAYER POINTS

**Pray for:**
- Dan Sullivan and his family
- Dave Bronson, Shelley Hughes, Bernadette Wilson, James William Parkin IV, Adam Crum, Treg Taylor, Nick Begich
- Alaska Governor/leadership
- Conservative candidates in all races
- Church mobilization and Christian voter turnout
- Protection from voter fraud
- Wisdom for Christian voters in Alaska
- Revival and awakening in Alaska
- God's will in Alaska elections

**Scripture for Alaska Elections:**

*\"Righteousness exalts a nation, but sin condemns any people.\"* - *Proverbs 14:34*

*\"When the righteous thrive, the people rejoice; when the wicked rule, the people groan.\"* - *Proverbs 29:2*

*\"If my people, who are called by my name, will humble themselves and pray and seek my face and turn from their wicked ways, then I will hear from heaven, and I will forgive their sin and will heal their land.\"* - *2 Chronicles 7:14*

---

**Last Updated:** October 2025
**Source:** Christian Conservatives Today Election Coverage
**Contact:** For questions or to contribute Alaska coverage, email contact@ekewaka.com

**Alaska CHRISTIANS: YOUR VOTE IS YOUR VOICE. USE IT FOR RIGHTEOUSNESS.**""",
    "updated_at": datetime.now().isoformat(),
    "created_by": "system"
}

# DUPLICATE-SAFE UPLOAD CODE
import uuid

print(f"Checking for existing Alaska races...")
existing_races = races_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Alaska'}
)['Items']
existing_race_map = {r['office']: r['race_id'] for r in existing_races}
print(f"Found {len(existing_races)} existing races")

print(f"\nProcessing {len(races)} Alaska races...")
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

print(f"\nChecking for existing Alaska candidates...")
existing_candidates = candidates_table.scan(
    FilterExpression='#s = :state',
    ExpressionAttributeNames={'#s': 'state'},
    ExpressionAttributeValues={':state': 'Alaska'}
)['Items']
existing_candidate_map = {(c['name'], c.get('office', '')): c['candidate_id'] for c in existing_candidates if 'name' in c}
print(f"Found {len(existing_candidates)} existing candidates")

print(f"\nProcessing {len(candidates)} Alaska candidates...")
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

print("\nProcessing Alaska summary...")
try:
    existing_summary = summaries_table.get_item(Key={'state': 'Alaska'})['Item']
    print("  Updating existing summary...")
except:
    print("  Creating new summary...")
summaries_table.put_item(Item=summary)
print(f"[SUCCESS] Summary uploaded: {len(summary['content']):,} chars")
print("\n[SUCCESS] Alaska data upload complete!")