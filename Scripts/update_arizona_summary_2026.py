import boto3
from boto3.dynamodb.conditions import Attr
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

# Delete old summary
response = summaries_table.scan(FilterExpression=Attr('state').eq('Arizona'))
for item in response['Items']:
    try:
        key = {'summary_id': item.get('summary_id')} if 'summary_id' in item else {'state': item['state']}
        summaries_table.delete_item(Key=key)
        print("Deleted old Arizona summary")
    except:
        pass

# New correct Arizona summary
arizona_summary = """# 🌵 Arizona 2026 Conservative Voter Guide

## 📊 Election Overview

Arizona features **critical 2026 statewide races** including Governor, Attorney General, Secretary of State, and State Treasurer. **NO U.S. Senate race in 2026** - both senators (Kelly and Gallego) are not up until 2028/2030. Focus on flipping statewide offices from Democrat control.

**Key Races:**
- 🔴 **Governor**: Katie Hobbs (D) vs. 3 Republicans - FLIP OPPORTUNITY
- 🔴 **Attorney General**: Kris Mayes (D) - FLIP TARGET
- 🔴 **Secretary of State**: Adrian Fontes (D) - FLIP TARGET  
- 🔴 **State Treasurer**: OPEN SEAT (Yee term-limited)
- 🔴 **Superintendent**: Tom Horne (R) vs. Kimberly Yee (R) primary

---

## 🎯 Top Priority Races

### Governor - FLIP OPPORTUNITY
**Incumbent**: Katie Hobbs (D) - Liberal policies, weak border security

**Republican Candidates**:
- **Andy Biggs** (R) - U.S. Representative, Freedom Caucus, strong conservative
- **David Schweikert** (R) - U.S. Representative, fiscal conservative
- **Karrin Taylor Robson** (R) - Former Regent, businesswoman

**Why This Matters**: Hobbs has pushed liberal agenda, weak border enforcement, and opposed election integrity reforms. Arizona needs conservative leadership to secure the border, protect life, and defend parental rights.

### Attorney General - FLIP TARGET
**Incumbent**: Kris Mayes (D) - Won by 280 votes in 2022, refuses to enforce border laws

**Why This Matters**: Mayes blocks conservative policies, refuses to defend election integrity laws, and enables sanctuary policies. Flipping this seat is CRITICAL for enforcing Arizona's conservative laws.

### Secretary of State - FLIP TARGET
**Incumbent**: Adrian Fontes (D) - Opposes election integrity reforms

**Why This Matters**: Secretary of State oversees elections. Fontes opposes voter ID enforcement, ballot security measures, and clean voter rolls. Arizona needs a conservative Secretary of State to ensure election integrity.

### State Treasurer - OPEN SEAT
**Status**: Kimberly Yee (R) is term-limited - OPEN SEAT

**Why This Matters**: Must hold this Republican seat to maintain fiscal conservatism in state finances. Critical for protecting taxpayer dollars and opposing wasteful spending.

### Superintendent of Public Instruction - REPUBLICAN PRIMARY
**Incumbent**: Tom Horne (R)

**Primary Challenger**: Kimberly Yee (R) - State Treasurer challenging incumbent

**Why This Matters**: Both are Republicans. Primary voters must choose between incumbent Horne and Treasurer Yee. Winner will defend parental rights and oppose CRT/gender ideology in schools.

---

## 🔥 8 Key Issues for Arizona Conservatives

### 1️⃣ Pro-Life Protections
Arizona has strong pro-life laws protecting unborn babies. Democrats like Hobbs want to eliminate these protections. Support candidates who will:
- Defend Arizona's pro-life laws
- Defund Planned Parenthood
- Protect healthcare workers' conscience rights
- Require parental notification for minors

### 2️⃣ School Choice & Parental Rights
Arizona leads the nation in school choice with universal ESAs. Protect and expand:
- Education Savings Accounts for all families
- Parental rights over curriculum decisions
- Opposition to CRT and gender ideology
- Protection from radical sex education

### 3️⃣ Religious Liberty
Protect Arizona's faith communities from government overreach. Support candidates who defend:
- Church autonomy and pastoral freedom
- Christian business owners' conscience rights
- Prayer in schools and public spaces
- Faith-based adoption agencies

**IRS Guidance**: Pastors CAN endorse candidates from the pulpit under updated IRS guidance.

### 4️⃣ Traditional Family Values
Defend biblical marriage and protect children. Support candidates who will:
- Ban child gender transitions
- Keep biological males out of girls' sports and bathrooms
- Protect parental notification rights
- Defend traditional family structure

### 5️⃣ Second Amendment Rights
Arizona is a constitutional carry state. Protect gun rights and oppose:
- "Assault weapon" bans
- Magazine capacity limits
- Red flag laws without due process
- Federal gun registries

### 6️⃣ Election Integrity
Arizona passed strong election integrity laws. Democrats like Fontes oppose them. Support candidates who will:
- Enforce voter ID requirements
- Ban ballot harvesting
- Clean voter rolls of dead/moved voters
- Require signature verification
- Oppose mail-in ballot abuse

### 7️⃣ Border Security & Immigration
**MOST CRITICAL ISSUE**: Arizona faces border crisis with drugs, cartels, human trafficking. Support candidates who will:
- Finish the border wall
- Deploy National Guard to border
- End sanctuary policies
- Mandate E-Verify for employers
- Deport criminal illegal aliens
- Oppose amnesty programs
- Prosecute cartel members

**Katie Hobbs has FAILED on border security. Arizona needs a governor who will protect our border.**

### 8️⃣ Economic Freedom & Lower Taxes
Arizona's economy needs conservative leadership. Support candidates who will:
- Cut taxes and reduce regulations
- Oppose Green New Deal mandates
- Protect small businesses
- Defend property rights
- Stop wasteful government spending

---

## 📅 Important Dates

- **Voter Registration Deadline**: Check Arizona Secretary of State website
- **Early Voting**: Begins 27 days before Election Day
- **Primary Election**: August 2026 (date TBD)
- **General Election**: November 3, 2026

**Register to vote**: https://servicearizona.com/

---

## 🗳️ How to Vote Biblically

**Prayer**: Ask God for wisdom in selecting leaders who honor Him (James 1:5)

**Research**: Review candidates' positions on life, family, and religious liberty

**Vote**: Participate in primaries AND general election - every race matters

**Encourage**: Bring fellow believers to the polls - your church family's votes can flip Arizona

---

## 📞 Take Action Now

1. **Register to vote** - Deadline is 29 days before Election Day
2. **Request early ballot** if needed - Don't let Democrats out-organize us
3. **Volunteer** for conservative candidates - Knock doors, make calls, donate
4. **Pray** for Arizona and our nation - 2 Chronicles 7:14
5. **Share** this guide with your church, family, and friends

---

## 🙏 Pastoral Endorsement Guidance

**Pastors CAN legally**:
- Endorse candidates from the pulpit (updated IRS guidance)
- Distribute voter guides showing candidates' positions
- Host candidate forums with all candidates invited
- Encourage congregation to vote for biblical values
- Speak on moral issues that align with political positions

**Churches should NOT**:
- Make direct campaign contributions
- Coordinate with campaigns using church resources
- Distribute materials that favor one party exclusively

**Bottom Line**: Pastors have FREEDOM to speak truth. Arizona needs bold pastoral leadership to mobilize conservative voters.

---

## 🔥 Final Word

Arizona is a **BATTLEGROUND STATE** where conservative Christians can flip statewide offices from Democrat control. Katie Hobbs, Kris Mayes, and Adrian Fontes have pushed liberal agendas and failed on border security.

**NO U.S. SENATE RACE IN 2026** - Focus on Governor, Attorney General, and Secretary of State races.

The border crisis demands conservative leadership. School choice needs protection. Election integrity requires enforcement. Arizona's future depends on YOU showing up and voting biblical values.

**Your vote is your voice. Your silence is surrender.**

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information before voting. May God guide Arizona in 2026.*"""

summary_item = {
    'summary_id': str(uuid.uuid4()),
    'state': 'Arizona',
    'election_cycle': '2025-2026',
    'summary': arizona_summary,
    'last_updated': '2025-01-01'
}

summaries_table.put_item(Item=summary_item)
print(f"Arizona summary updated: {len(arizona_summary)} characters")
