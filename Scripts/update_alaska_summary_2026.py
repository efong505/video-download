import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

# Delete old Alaska summary
response = summaries_table.scan(FilterExpression=Attr('state').eq('Alaska'))
for item in response['Items']:
    key = {'summary_id': item.get('summary_id')} if 'summary_id' in item else {'state': item['state']}
    try:
        summaries_table.delete_item(Key=key)
        print(f"Deleted old Alaska summary")
    except:
        pass

# New correct Alaska summary
alaska_summary = """# ❄️ Alaska 2025-2026 Conservative Voter Guide

## 📊 Election Overview

Alaska features **critical 2026 races** including a safe U.S. Senate seat hold and an **OPEN Governor race** with Mike Dunleavy term-limited. Alaska uses **ranked choice voting** - conservatives MUST rank multiple Republicans to prevent Democrat victories.

**Key Races:**
- 🔴 **U.S. Senate**: Dan Sullivan (R) safe hold
- 🔴 **Governor**: OPEN SEAT - Dunleavy term-limited, 8 Republicans + 1 Democrat
- 🔴 **U.S. House At-Large**: Nick Begich III (R) likely hold

---

## 🎯 Top Priority Races

### U.S. Senate - SAFE HOLD
**Incumbent**: Dan Sullivan (R) - Strong conservative, military veteran

**Challengers**:
- Christopher Miklos (R) - Primary challenger
- Ann Diener (D)

**Why This Matters**: Sullivan is a reliable conservative vote. Safe Republican hold in Trump +10 state. Primary voters should support Sullivan's proven leadership.

### Governor - OPEN SEAT (CRITICAL)
**Status**: Mike Dunleavy is **TERM-LIMITED** and cannot run for a third consecutive term. This is an **OPEN SEAT** with a crowded Republican primary.

**Republican Candidates** (8 total):
- **Nancy Dahlstrom** - Lt. Governor (frontrunner)
- **Treg Taylor** - Former Attorney General
- **Dave Bronson** - Anchorage Mayor
- **Shelley Hughes** - State Representative
- **Bernadette Wilson**
- **Edna DeVries**
- **Adam Crum**
- **James Parkin**

**Democrat Candidate**:
- Tom Begich - Former State Senator

**RANKED CHOICE VOTING WARNING**: With 8 Republicans running, conservatives MUST rank multiple Republicans to prevent Democrat Tom Begich from winning through vote splitting. **Rank ALL Republicans above the Democrat.**

### U.S. House At-Large - LIKELY HOLD
**Incumbent**: Nick Begich III (R) - Elected in 2024, defeated Mary Peltola (D)

**Challengers**:
- John Brendan Williams (D)
- Matt Schultz (D) - Pastor

**Why This Matters**: Begich flipped this seat from Democrat control in 2024. Must hold to maintain Republican House majority.

---

## 🔥 8 Key Issues for Alaska Conservatives

### 1️⃣ Pro-Life Protections
Alaska needs stronger pro-life laws. Support candidates who will:
- Restrict late-term abortions
- Require parental notification for minors
- Protect healthcare workers' conscience rights
- Defund Planned Parenthood

### 2️⃣ School Choice & Parental Rights
Alaska's rural communities need education freedom. Support candidates who back:
- Homeschool protections
- Charter school expansion
- Parental rights over curriculum
- Opposition to CRT and gender ideology

### 3️⃣ Religious Liberty
Protect Alaska's faith communities from government overreach. Support candidates who defend:
- Church autonomy
- Christian business owners' rights
- Prayer in schools
- Faith-based adoption agencies

**IRS Guidance**: Pastors CAN endorse candidates from the pulpit under updated IRS guidance.

### 4️⃣ Traditional Family Values
Defend biblical marriage and protect children. Support candidates who will:
- Ban child gender transitions
- Keep biological males out of girls' sports
- Protect parental notification rights
- Defend traditional family structure

### 5️⃣ Second Amendment Rights
Alaska has strong gun rights culture. Protect constitutional carry and oppose:
- "Assault weapon" bans
- Magazine capacity limits
- Red flag laws without due process
- Federal gun registries

### 6️⃣ Election Integrity
**CRITICAL**: Alaska's ranked choice voting system helped Democrats. Support candidates who will:
- REPEAL ranked choice voting
- Require voter ID
- Clean voter rolls
- Restore traditional runoff elections

### 7️⃣ Border Security & Immigration
Alaska faces unique border challenges with Canada and maritime borders. Support candidates who will:
- Secure borders
- Oppose sanctuary policies
- Mandate E-Verify
- Deport criminal illegal aliens

### 8️⃣ Energy Independence & Jobs
Alaska's economy depends on oil, gas, and mining. Support candidates who will:
- Open ANWR for drilling
- Approve pipeline projects
- Oppose Green New Deal regulations
- Protect resource extraction jobs
- Defend Permanent Fund Dividend

---

## 🗳️ RANKED CHOICE VOTING STRATEGY

Alaska uses **ranked choice voting** - this is CRITICAL to understand:

**How It Works**:
1. Rank candidates in order of preference (1st, 2nd, 3rd, etc.)
2. If no candidate gets 50%+, lowest candidate is eliminated
3. Their votes transfer to voters' next choice
4. Process repeats until someone gets 50%+

**Conservative Strategy**:
- **RANK ALL REPUBLICANS** before any Democrat
- Don't leave rankings blank - use all options
- In Governor race with 8 Republicans, rank ALL 8 above Tom Begich (D)
- This prevents vote splitting that could elect a Democrat

**Example Governor Ballot**:
1. Nancy Dahlstrom (R)
2. Treg Taylor (R)
3. Dave Bronson (R)
4. Shelley Hughes (R)
5. [Other Republicans]
...
9. Tom Begich (D) - LEAVE UNRANKED or rank last

---

## 📅 Important Dates

- **Voter Registration Deadline**: 30 days before Election Day
- **Early Voting**: Begins 15 days before Election Day
- **Primary Election**: August 2026
- **General Election**: November 3, 2026

**Register to vote**: https://voterregistration.alaska.gov/

---

## 📞 Take Action Now

1. **Register to vote** - Deadline is 30 days before Election Day
2. **Learn ranked choice voting** - Practice ranking candidates
3. **Volunteer** for conservative candidates
4. **Pray** for Alaska and our nation
5. **Share** this guide with your church and family

---

## 🙏 Final Word

Alaska's **OPEN Governor race** is the top priority. With 8 Republicans running, conservatives MUST use ranked choice voting strategically to prevent Democrat victory. **Rank ALL Republicans above the Democrat.**

Dan Sullivan's Senate seat is safe, but Nick Begich's House seat needs support to maintain Republican control.

**Your rankings matter. Vote strategically. Alaska's future depends on YOU.**

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information before voting. May God guide Alaska in 2026.*"""

import uuid
summary_item = {
    'summary_id': str(uuid.uuid4()),
    'state': 'Alaska',
    'election_cycle': '2025-2026',
    'summary': alaska_summary,
    'last_updated': '2025-01-01'
}

summaries_table.put_item(Item=summary_item)
print(f"Alaska summary updated: {len(alaska_summary)} characters")
