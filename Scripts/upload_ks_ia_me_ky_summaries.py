import boto3
from boto3.dynamodb.conditions import Attr
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

# Delete existing summaries
states = ['Kansas', 'Iowa', 'Maine', 'Kentucky']
for state in states:
    response = summaries_table.scan(FilterExpression=Attr('state').eq(state))
    for item in response['Items']:
        try:
            key = {'summary_id': item.get('summary_id')} if 'summary_id' in item else {'state': item['state']}
            summaries_table.delete_item(Key=key)
            print(f"Deleted old {state} summary")
        except:
            pass

# Kansas Summary - CORRECTED with OPEN SEAT
kansas_summary = """# 🌾 Kansas 2026 Conservative Voter Guide

## 📊 Election Overview

Kansas features **critical 2026 statewide races** with Governor Laura Kelly TERM-LIMITED, creating an **OPEN SEAT** for Governor. **NO U.S. Senate race in 2026** - Senator Jerry Moran is not up until 2028. Focus on electing a conservative governor to replace term-limited Democrat Laura Kelly.

**Key Races:**
- 🔴 **Governor**: OPEN SEAT (Kelly term-limited) - FLIP OPPORTUNITY
- 🔴 **Statewide Offices**: Multiple competitive races

**Election Date:**
- November 3, 2026 - General election

---

## 🎯 Top Priority Races

### Governor - OPEN SEAT (CRITICAL FLIP OPPORTUNITY)
**Status**: Governor Laura Kelly (D) is **TERM-LIMITED** and cannot run for a third consecutive term. This is Kansas's best chance to elect a conservative governor.

**Republican Candidates**:
- **Jeff Colyer** (R) - Former Governor, physician, strong conservative record
- **Ty Masterson** (R) - Senate President, proven legislative leader

**Democrat Candidates**:
- **Ethan Corson** (D) - State Senator
- **Cindy Holscher** (D) - State Senator

**Why This Matters**: Laura Kelly has blocked conservative legislation for 8 years. With her term-limited, Kansas can elect a governor who will defend life, protect parental rights, and advance biblical values. This is a MUST-WIN race.

---

## 🔥 8 Key Issues for Kansas Conservatives

### 1️⃣ Pro-Life Protections
Kansas voters rejected abortion expansion in 2022. Support candidates who will:
- Defend Kansas's pro-life laws
- Require parental notification for minors
- Protect healthcare workers' conscience rights
- Defund Planned Parenthood

**The next Governor will determine if Kansas remains pro-life or becomes an abortion destination.**

### 2️⃣ School Choice & Parental Rights
Support candidates who back:
- Education Savings Accounts
- Charter school expansion
- Parental rights over curriculum
- Opposition to CRT and gender ideology

### 3️⃣ Religious Liberty
Protect Kansas's faith communities. Support candidates who defend:
- Church autonomy
- Christian business owners' rights
- Prayer in schools
- Faith-based adoption agencies

**IRS Guidance**: Pastors CAN endorse candidates from the pulpit.

### 4️⃣ Traditional Family Values
Defend biblical marriage and protect children. Support candidates who will:
- Ban child gender transitions
- Keep biological males out of girls' sports
- Protect parental notification rights
- Defend traditional family structure

### 5️⃣ Second Amendment Rights
Kansas needs strong gun rights protection. Support candidates who will:
- Oppose "assault weapon" bans
- Defend concealed carry
- Protect constitutional rights

### 6️⃣ Election Integrity
Support candidates who will:
- Require voter ID
- Ban ballot harvesting
- Clean voter rolls
- Oppose federal election takeover

### 7️⃣ Border Security & Immigration
Support candidates who will:
- Secure the border
- End sanctuary policies
- Mandate E-Verify
- Deport criminal illegal aliens

### 8️⃣ Economic Freedom & Lower Taxes
Support candidates who will:
- Cut taxes and reduce regulations
- Oppose Green New Deal mandates
- Protect small businesses
- Stop wasteful spending

---

## 📅 Important Dates

- **Primary Election**: August 2026 (date TBD)
- **General Election**: November 3, 2026

**Register to vote**: https://www.kdor.ks.gov/apps/voterreg/

---

## 🗳️ How to Vote Biblically

**Prayer**: Ask God for wisdom (James 1:5)

**Research**: Review candidates' positions on biblical values

**Vote**: Participate in primary AND general election - the Governor primary is CRITICAL

**Encourage**: Bring fellow believers to the polls

---

## 📞 Take Action Now

1. **Register to vote**
2. **Vote in Republican primary** - Choose between Colyer and Masterson
3. **Support conservative Governor candidate** in general election
4. **Volunteer** for conservative candidates
5. **Pray** for Kansas - 2 Chronicles 7:14
6. **Share** this guide with your church

---

## 🙏 Final Word

Kansas's **OPEN Governor race** is the most important election in 2026. Laura Kelly is TERM-LIMITED - this is our chance to elect a conservative governor who will defend life, protect children, and advance biblical values.

**NO U.S. SENATE RACE IN 2026** - Focus on Governor race.

**Your vote will determine if Kansas elects a conservative governor or another Democrat who blocks pro-life legislation.**

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information before voting. May God guide Kansas in 2026.*"""

# Iowa Summary - CORRECTED (Reynolds NOT term-limited, voluntarily not running)
iowa_summary = """# 🌽 Iowa 2026 Conservative Voter Guide

## 📊 Election Overview

Iowa features **critical 2026 statewide races** with Governor Kim Reynolds voluntarily not seeking re-election, creating an **OPEN SEAT** for Governor. **NO U.S. Senate race in 2026** - both senators are not up until later cycles. Focus on maintaining Republican governorship.

**Key Races:**
- 🔴 **Governor**: OPEN SEAT (Reynolds not seeking re-election) - MUST HOLD
- 🔴 **Statewide Offices**: Multiple races

**Election Date:**
- November 3, 2026 - General election

---

## 🎯 Top Priority Races

### Governor - OPEN SEAT (MUST HOLD)
**Status**: Governor Kim Reynolds (R) announced on April 11, 2025, that she **will not seek re-election**. Note: Iowa has NO gubernatorial term limits - Reynolds is voluntarily stepping down.

**Republican Candidates**:
- **Brad Sherman** (R) - Leading Republican candidate

**Democrat Candidates**:
- **Rob Sand** (D) - State Auditor
- **Julie Stauch** (D)

**Why This Matters**: Kim Reynolds transformed Iowa with conservative policies - school choice, pro-life protections, parental rights. Iowa MUST elect another conservative governor to continue this legacy and prevent Democrat takeover.

---

## 🔥 8 Key Issues for Iowa Conservatives

### 1️⃣ Pro-Life Protections
Iowa has strong pro-life laws. Support candidates who will:
- Defend Iowa's pro-life protections
- Require parental notification for minors
- Protect healthcare workers' conscience rights
- Defund Planned Parenthood

### 2️⃣ School Choice & Parental Rights
Iowa leads the nation in school choice under Reynolds. Support candidates who will:
- Maintain universal Education Savings Accounts
- Defend parental rights over curriculum
- Oppose CRT and gender ideology
- Protect homeschool freedom

**The next Governor must protect Iowa's school choice leadership.**

### 3️⃣ Religious Liberty
Protect Iowa's faith communities. Support candidates who defend:
- Church autonomy
- Christian business owners' rights
- Prayer in schools
- Faith-based adoption agencies

**IRS Guidance**: Pastors CAN endorse candidates from the pulpit.

### 4️⃣ Traditional Family Values
Defend biblical marriage and protect children. Support candidates who will:
- Ban child gender transitions
- Keep biological males out of girls' sports
- Protect parental notification rights
- Defend traditional family structure

### 5️⃣ Second Amendment Rights
Iowa needs strong gun rights protection. Support candidates who will:
- Oppose "assault weapon" bans
- Defend concealed carry
- Protect constitutional rights

### 6️⃣ Election Integrity
Support candidates who will:
- Require voter ID
- Ban ballot harvesting
- Clean voter rolls
- Oppose federal election takeover

### 7️⃣ Border Security & Immigration
Support candidates who will:
- Secure the border
- End sanctuary policies
- Mandate E-Verify
- Deport criminal illegal aliens

### 8️⃣ Economic Freedom & Lower Taxes
Support candidates who will:
- Cut taxes and reduce regulations
- Oppose Green New Deal mandates
- Protect small businesses
- Stop wasteful spending

---

## 📅 Important Dates

- **Primary Election**: June 2026 (date TBD)
- **General Election**: November 3, 2026

**Register to vote**: https://sos.iowa.gov/elections/voterinformation/voterregistration.html

---

## 🗳️ How to Vote Biblically

**Prayer**: Ask God for wisdom (James 1:5)

**Research**: Review candidates' positions on biblical values

**Vote**: Participate in primary AND general election

**Encourage**: Bring fellow believers to the polls

---

## 📞 Take Action Now

1. **Register to vote**
2. **Support Brad Sherman** or conservative Republican in primary
3. **Vote in general election** to keep Iowa red
4. **Volunteer** for conservative candidates
5. **Pray** for Iowa - 2 Chronicles 7:14
6. **Share** this guide with your church

---

## 🙏 Final Word

Iowa's **OPEN Governor race** is critical for maintaining Republican leadership. Kim Reynolds is voluntarily not seeking re-election (Iowa has NO term limits) - we must elect another conservative to continue her legacy.

**NO U.S. SENATE RACE IN 2026** - Focus on Governor race.

**Your vote will determine if Iowa remains a conservative leader or falls to Democrat control.**

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information before voting. May God guide Iowa in 2026.*"""

# Maine Summary - UPDATED with Janet Mills
maine_summary = """# 🦞 Maine 2026 Conservative Voter Guide

## 📊 Election Overview

Maine features **CRITICAL 2026 Senate race** with Senator Susan Collins (R) facing her toughest challenge yet from Governor Janet Mills (D). **NO Governor race in 2026**. This Senate seat is ESSENTIAL for Republican majority.

**Key Races:**
- 🔴 **U.S. Senate**: Susan Collins (R) vs. Janet Mills (D) - TOSS-UP, MUST HOLD

**Election Date:**
- November 3, 2026 - General election

---

## 🎯 Top Priority Race

### U.S. Senate - TOSS-UP (MOST CRITICAL HOLD)
**Incumbent**: Susan Collins (R) - Moderate Republican, most vulnerable GOP senator

**Major Challenger**: **Governor Janet Mills (D)** - Announced candidacy October 14, 2025

**Race Status**: Moved from "Leans Republican" to **"TOSS-UP"** after Mills entered

**Why This Matters**: This is the MOST VULNERABLE Republican Senate seat in 2026. Losing Collins means Democrats control the Senate and pass Biden's radical agenda. Collins is moderate but ESSENTIAL for Senate majority.

**Susan Collins Record**:
- Moderate Republican, sometimes votes with Democrats
- Pro-choice on abortion
- Supports some gun control measures
- BUT: Critical vote for Republican Senate control

**Janet Mills Threat**:
- Popular Democrat Governor
- Strong fundraising ability
- Name recognition across Maine
- Pro-choice, gun control advocate
- Would give Democrats Senate majority

**Conservative Strategy**: "Hold your nose and vote" - Collins is moderate but losing her means Democrat Senate control, which means:
- Codifying Roe v. Wade nationally
- Packing the Supreme Court
- Eliminating the filibuster
- Passing radical gun control
- Open borders legislation

---

## 🔥 8 Key Issues for Maine Conservatives

### 1️⃣ Pro-Life Protections
Collins is pro-choice, but Democrat control means codifying Roe v. Wade. Support Collins to:
- Prevent national abortion mandate
- Block taxpayer-funded abortion
- Protect conscience rights
- Maintain pro-life judges

**Losing Collins = National abortion mandate passes**

### 2️⃣ School Choice & Parental Rights
Support candidates who back:
- Education Savings Accounts
- Charter school expansion
- Parental rights over curriculum
- Opposition to CRT and gender ideology

### 3️⃣ Religious Liberty
Protect Maine's faith communities. Support candidates who defend:
- Church autonomy
- Christian business owners' rights
- Prayer in schools
- Faith-based adoption agencies

**IRS Guidance**: Pastors CAN endorse candidates from the pulpit.

### 4️⃣ Traditional Family Values
Defend biblical marriage and protect children. Support candidates who will:
- Ban child gender transitions
- Keep biological males out of girls' sports
- Protect parental notification rights
- Defend traditional family structure

### 5️⃣ Second Amendment Rights
Maine needs gun rights protection. Support candidates who will:
- Oppose "assault weapon" bans
- Defend concealed carry
- Protect constitutional rights

### 6️⃣ Election Integrity
Support candidates who will:
- Require voter ID
- Ban ballot harvesting
- Clean voter rolls
- Oppose federal election takeover

### 7️⃣ Border Security & Immigration
Support candidates who will:
- Secure the border
- End sanctuary policies
- Mandate E-Verify
- Deport criminal illegal aliens

### 8️⃣ Economic Freedom & Lower Taxes
Support candidates who will:
- Cut taxes and reduce regulations
- Oppose Green New Deal mandates
- Protect small businesses
- Stop wasteful spending

---

## 📅 Important Dates

- **Primary Election**: June 2026 (date TBD)
- **General Election**: November 3, 2026

**Register to vote**: https://www.maine.gov/sos/cec/elec/voter-info/voterguide.html

---

## 🗳️ How to Vote Biblically

**Prayer**: Ask God for wisdom (James 1:5)

**Research**: Understand what's at stake - Senate control

**Vote**: Collins is moderate but ESSENTIAL for Republican majority

**Encourage**: Bring fellow believers to the polls - this race will be decided by hundreds of votes

---

## 📞 Take Action Now

1. **Register to vote**
2. **Support Susan Collins** despite her moderate record
3. **Understand the stakes** - Senate control depends on Maine
4. **Volunteer** for Collins campaign
5. **Pray** for Maine - 2 Chronicles 7:14
6. **Share** this guide with your church

---

## 🙏 Final Word

Maine's **Senate race is a TOSS-UP** and the MOST CRITICAL Republican defense in 2026. Governor Janet Mills entering the race makes this Collins's toughest challenge yet.

**Collins is moderate, but losing her means:**
- Democrat Senate control
- Codified Roe v. Wade
- Packed Supreme Court
- Radical gun control
- Open borders

**"Hold your nose and vote" - Senate control depends on keeping Collins.**

**Your vote will determine if Republicans control the Senate or Democrats pass their radical agenda.**

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information before voting. May God guide Maine in 2026.*"""

# Kentucky Summary - CORRECTED candidates
kentucky_summary = """# 🐴 Kentucky 2026 Conservative Voter Guide

## 📊 Election Overview

Kentucky features **CRITICAL 2026 Senate race** with Senator Mitch McConnell retiring, creating an **OPEN SEAT**. This is a MUST-WIN race to maintain Republican Senate majority.

**Key Races:**
- 🔴 **U.S. Senate**: OPEN SEAT (McConnell retiring) - MUST HOLD

**Election Date:**
- November 3, 2026 - General election

---

## 🎯 Top Priority Race

### U.S. Senate - OPEN SEAT (MUST HOLD)
**Status**: Senator Mitch McConnell (R) announced his retirement on February 20, 2025. This is an OPEN SEAT with crowded primary fields.

**Republican Candidates**:
- **Daniel Cameron** (R) - Former Attorney General, strong conservative
- **Thomas Massie** (R) - U.S. Representative, Freedom Caucus member

**Democrat Candidates**:
- **Logan Forsythe** (D)
- **Pamela Stevenson** (D)
- **Joel Willett** (D)

**Why This Matters**: McConnell's retirement creates an open seat in a Trump +26 state. This should be a safe Republican hold, but conservatives must unite behind a strong candidate in the primary. Losing this seat would be catastrophic for Senate control.

---

## 🔥 8 Key Issues for Kentucky Conservatives

### 1️⃣ Pro-Life Protections
Kentucky has strong pro-life laws. Support candidates who will:
- Defend Kentucky's pro-life protections
- Oppose national abortion mandate
- Protect healthcare workers' conscience rights
- Defund Planned Parenthood

### 2️⃣ School Choice & Parental Rights
Support candidates who back:
- Education Savings Accounts
- Charter school expansion
- Parental rights over curriculum
- Opposition to CRT and gender ideology

### 3️⃣ Religious Liberty
Protect Kentucky's faith communities. Support candidates who defend:
- Church autonomy
- Christian business owners' rights
- Prayer in schools
- Faith-based adoption agencies

**IRS Guidance**: Pastors CAN endorse candidates from the pulpit.

### 4️⃣ Traditional Family Values
Defend biblical marriage and protect children. Support candidates who will:
- Ban child gender transitions
- Keep biological males out of girls' sports
- Protect parental notification rights
- Defend traditional family structure

### 5️⃣ Second Amendment Rights
Kentucky needs strong gun rights protection. Support candidates who will:
- Oppose "assault weapon" bans
- Defend concealed carry
- Protect constitutional rights

### 6️⃣ Election Integrity
Support candidates who will:
- Require voter ID
- Ban ballot harvesting
- Clean voter rolls
- Oppose federal election takeover

### 7️⃣ Border Security & Immigration
Support candidates who will:
- Secure the border
- End sanctuary policies
- Mandate E-Verify
- Deport criminal illegal aliens

### 8️⃣ Economic Freedom & Lower Taxes
Support candidates who will:
- Cut taxes and reduce regulations
- Oppose Green New Deal mandates
- Protect coal industry jobs
- Stop wasteful spending

---

## 📅 Important Dates

- **Primary Election**: May 2026 (date TBD)
- **General Election**: November 3, 2026

**Register to vote**: https://elect.ky.gov/registertovote/

---

## 🗳️ How to Vote Biblically

**Prayer**: Ask God for wisdom (James 1:5)

**Research**: Review candidates' positions on biblical values

**Vote**: Participate in primary AND general election - the primary is CRITICAL

**Encourage**: Bring fellow believers to the polls

---

## 📞 Take Action Now

1. **Register to vote**
2. **Vote in Republican primary** - Choose strong conservative
3. **Support Republican nominee** in general election
4. **Volunteer** for conservative candidates
5. **Pray** for Kentucky - 2 Chronicles 7:14
6. **Share** this guide with your church

---

## 🙏 Final Word

Kentucky's **OPEN Senate seat** is a MUST-WIN for Republicans. McConnell's retirement creates opportunity to elect a strong conservative in a Trump +26 state.

**The primary is CRITICAL** - conservatives must unite behind the strongest candidate to ensure Republican victory in November.

**Your vote will determine if Kentucky sends a strong conservative or a Democrat to the Senate.**

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information before voting. May God guide Kentucky in 2026.*"""

# Upload all summaries
summaries = [
    {'state': 'Kansas', 'summary': kansas_summary},
    {'state': 'Iowa', 'summary': iowa_summary},
    {'state': 'Maine', 'summary': maine_summary},
    {'state': 'Kentucky', 'summary': kentucky_summary}
]

for item in summaries:
    summary_item = {
        'summary_id': str(uuid.uuid4()),
        'state': item['state'],
        'election_cycle': '2025-2026',
        'summary': item['summary'],
        'last_updated': '2025-01-01'
    }
    summaries_table.put_item(Item=summary_item)
    print(f"{item['state']} summary uploaded: {len(item['summary']):,} characters")

print(f"\nAll 4 state summaries uploaded successfully with corrected data!")
