import boto3
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

georgia_summary = """# 🍑 Georgia 2025-2026 Conservative Voter Guide

## 📊 Election Overview

Georgia features **critical 2026 races** including a competitive U.S. Senate seat defense and Governor Brian Kemp's re-election. With Trump winning Georgia by narrow margins, every conservative vote matters to maintain Republican leadership and advance faith-based values.

**Key Races:**
- 🔴 **U.S. Senate**: Jon Ossoff (D) defense - FLIP OPPORTUNITY
- 🔴 **Governor**: Brian Kemp (R) re-election with primary challengers
- 🔴 **U.S. House**: Multiple competitive districts

---

## 🎯 Top Priority Races

### U.S. Senate - FLIP OPPORTUNITY
**Incumbent**: Jon Ossoff (D) - Liberal voting record, supports Biden agenda

**Republican Challengers**:
- **Buddy Carter** (R) - U.S. Representative, strong conservative record
- **Mike Collins** (R) - U.S. Representative, America First conservative
- **Derek Dooley** (R) - Former football coach, outsider candidate

**Why This Matters**: Flipping this seat is CRITICAL for Senate Republican majority. Ossoff votes with Biden 95%+ of the time. Georgia conservatives must unite behind the Republican nominee to restore conservative leadership.

### Governor - Republican Primary
**Incumbent**: Brian Kemp (R) - Popular governor, strong economy, election integrity

**Primary Challengers**:
- **Chris Carr** (R) - Attorney General, law and order conservative
- **Burt Jones** (R) - Lt. Governor, strong conservative record

**Democrat Challengers**:
- Keisha Lance Bottoms (D) - Former Atlanta Mayor
- Jason Esteves (D) - Atlanta City Council
- Derrick Jackson (D)

**Why This Matters**: Kemp has delivered conservative results - strong economy, election integrity reforms, pro-life protections. Primary voters should support proven conservative leadership.

### U.S. House Competitive Districts

**District 6** (North Atlanta suburbs):
- Justin Pinker (R)
- Chris Capparell (D)
- Sonya Halpern (D)

**District 7** (Gwinnett County):
- Lucy McBath (D) - Incumbent, gun control advocate

---

## 🔥 8 Key Issues for Georgia Conservatives

### 1️⃣ Pro-Life Protections
Georgia passed the **"Heartbeat Bill"** protecting unborn babies after 6 weeks. Democrats like Ossoff want to codify Roe v. Wade nationally and eliminate Georgia's pro-life protections. **Vote for candidates who will defend life from conception.**

### 2️⃣ School Choice & Parental Rights
Georgia needs **universal school choice** and protection from radical gender ideology in schools. Support candidates who back Education Savings Accounts, oppose CRT indoctrination, and defend parental rights over children's education and healthcare decisions.

### 3️⃣ Religious Liberty
Georgia's faith communities need protection from government overreach. Support candidates who defend:
- Church autonomy and pastoral freedom
- Christian business owners' conscience rights
- Prayer in schools and public spaces
- Faith-based adoption agencies

**IRS Guidance**: Pastors CAN endorse candidates from the pulpit under updated IRS guidance. Churches should not be silenced.

### 4️⃣ Traditional Family Values
Defend biblical marriage, protect children from transgender procedures, and oppose radical LGBTQ+ curriculum in schools. Support candidates who will:
- Ban child gender transitions
- Keep biological males out of girls' sports and bathrooms
- Protect parental notification rights
- Defend traditional family structure

### 5️⃣ Second Amendment Rights
Georgia is a strong 2A state with constitutional carry. Oppose Democrats like Ossoff and McBath who support:
- "Assault weapon" bans
- Magazine capacity limits
- Red flag laws without due process
- National gun registries

**Vote for candidates with A+ NRA ratings who will protect your God-given right to self-defense.**

### 6️⃣ Election Integrity
Georgia passed **SB 202** strengthening voter ID and ballot security. Democrats sued to block it, calling it "Jim Crow 2.0." Support candidates who will:
- Require photo ID for all voting
- Ban ballot harvesting
- Clean voter rolls of dead/moved voters
- Oppose federal takeover of elections (HR 1)

### 7️⃣ Border Security & Immigration
Georgia faces illegal immigration impacts - drugs, crime, human trafficking. Support candidates who will:
- Finish the border wall
- End sanctuary cities
- Mandate E-Verify for employers
- Deport criminal illegal aliens
- Oppose amnesty programs

### 8️⃣ Economic Freedom & Lower Taxes
Georgia's economy thrives under Republican leadership. Oppose Democrats who support:
- Massive tax increases
- Green New Deal job-killing regulations
- Inflation-causing spending bills
- Small business crushing mandates

**Support candidates who will cut taxes, reduce regulations, and let Georgia businesses prosper.**

---

## 📅 Important Dates

- **Voter Registration Deadline**: Check Georgia Secretary of State website
- **Early Voting**: Begins 3 weeks before Election Day
- **Primary Election Day**: May 2026 (date TBD)
- **General Election Day**: November 3, 2026

**Register to vote**: https://registertovote.sos.ga.gov/

---

## 🗳️ How to Vote Biblically

**Prayer**: Ask God for wisdom in selecting leaders who honor Him (James 1:5)

**Research**: Review candidates' positions on life, family, and religious liberty

**Vote**: Participate in primaries AND general election - every race matters

**Encourage**: Bring fellow believers to the polls - your church family's votes can change Georgia

---

## 📞 Take Action Now

1. **Register to vote** - Deadline is 4 weeks before Election Day
2. **Request absentee ballot** if needed - Don't let Democrats out-organize us
3. **Volunteer** for conservative candidates - Knock doors, make calls, donate
4. **Pray** for Georgia and our nation - 2 Chronicles 7:14
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

**Bottom Line**: Pastors have FREEDOM to speak truth. Don't let fear silence the Church. Georgia needs bold pastoral leadership to mobilize conservative voters.

---

## 🔥 Final Word

Georgia is a **BATTLEGROUND STATE** where conservative Christians can determine the outcome. The Senate seat is FLIPPABLE if we unite. Governor Kemp needs our support against Democrat challengers. House races will be decided by hundreds of votes.

**Your vote is your voice. Your silence is surrender.**

Don't sit out 2026. Georgia's future - and America's Senate majority - depends on YOU showing up and voting biblical values.

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information and positions before voting. May God guide Georgia in 2026.*"""

# Upload summary
summary_item = {
    'summary_id': str(uuid.uuid4()),
    'state': 'Georgia',
    'election_cycle': '2025-2026',
    'summary': georgia_summary,
    'last_updated': '2025-01-01'
}

summaries_table.put_item(Item=summary_item)
print(f"Georgia summary uploaded: {len(georgia_summary)} characters")
