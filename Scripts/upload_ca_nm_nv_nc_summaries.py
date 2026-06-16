import boto3
from boto3.dynamodb.conditions import Attr
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

# Check and delete existing summaries
states = ['California', 'New Mexico', 'Nevada', 'North Carolina']
for state in states:
    response = summaries_table.scan(FilterExpression=Attr('state').eq(state))
    for item in response['Items']:
        try:
            key = {'summary_id': item.get('summary_id')} if 'summary_id' in item else {'state': item['state']}
            summaries_table.delete_item(Key=key)
            print(f"Deleted old {state} summary")
        except:
            pass

# California Summary
california_summary = """# 🌴 California 2026 Conservative Voter Guide

## 📊 Election Overview

California features **critical 2026 statewide races** with Governor Gavin Newsom term-limited, creating an **OPEN SEAT** for Governor. **NO U.S. Senate race in 2026** - both senators (Padilla and Schiff) are not up until 2028/2030. Focus on flipping the governorship and electing conservative leaders to statewide offices.

**Key Races:**
- 🔴 **Governor**: OPEN SEAT (Newsom term-limited) - FLIP OPPORTUNITY
- 🔴 **Lieutenant Governor**: Eleni Kounalakis (D) re-election
- 🔴 **Attorney General**: Rob Bonta (D) re-election
- 🔴 **State Treasurer**: Toni Atkins (D) running
- 🔴 **Superintendent**: OPEN SEAT (Thurmond not seeking re-election)

---

## 🎯 Top Priority Races

### Governor - OPEN SEAT (CRITICAL FLIP OPPORTUNITY)
**Status**: Gavin Newsom is **TERM-LIMITED** and cannot run for a third consecutive term. This is California's best chance to elect a conservative governor in decades.

**Top Republican Candidate**:
- **Chad Bianco** (R) - Riverside County Sheriff, strong Christian conservative, refused COVID mandates, 30+ years law enforcement

**Other Republican Candidates**:
- **Steve Hilton** (R) - Fox News contributor, polling at 12%, conservative reformer
- **Leo Zacky** (R) - Business owner, traditional values

**Leading Democrats**:
- **Katie Porter** (D) - Leading at 18%, progressive, Elizabeth Warren protégé
- **Xavier Becerra** (D) - Former HHS Secretary, 10% in polls
- **Antonio Villaraigosa** (D) - Former LA Mayor, 5% in polls

**Why This Matters**: California's governor controls the nation's largest state economy, sets education policy for millions of children, and influences national politics. Electing a conservative governor would transform California and inspire the nation.

### Superintendent of Public Instruction - OPEN SEAT
**Status**: Tony Thurmond (D) is not seeking re-election - **OPEN SEAT**

**Why This Matters**: This is California's best opportunity to elect a conservative Superintendent who will defend parental rights, oppose CRT and gender ideology, and support school choice. Nonpartisan race means no party labels on ballot - organized Christians can win.

### Attorney General - Rob Bonta (D)
**Incumbent**: Rob Bonta (D) - Progressive prosecutor, sanctuary state advocate

**Why This Matters**: Attorney General enforces (or refuses to enforce) California's laws. Bonta has blocked conservative policies and enabled sanctuary policies. Flipping this seat is critical for enforcing immigration laws and protecting religious liberty.

---

## 🔥 8 Key Issues for California Conservatives

### 1️⃣ Pro-Life Protections
California has the most extreme abortion laws in America - abortion legal through all 9 months. Democrats want to enshrine abortion as a "constitutional right." Support candidates who will:
- Oppose late-term abortion
- Require parental notification for minors
- Protect healthcare workers' conscience rights
- Defund Planned Parenthood
- Support pregnancy resource centers

**The next Governor and Attorney General will determine if California becomes an abortion sanctuary or protects life.**

### 2️⃣ School Choice & Parental Rights
California's public schools push CRT, gender ideology, and radical sex education. Support candidates who will:
- Expand charter schools and homeschool freedom
- Defend parental rights over curriculum
- Ban CRT and gender ideology in schools
- Protect children from inappropriate sexual content
- Support Education Savings Accounts
- Oppose teacher union control

**The Superintendent race is CRITICAL for protecting children and parental rights.**

### 3️⃣ Religious Liberty
California has attacked churches, Christian businesses, and faith-based organizations. Support candidates who defend:
- Church autonomy and pastoral freedom
- Christian business owners' conscience rights
- Prayer in schools and public spaces
- Faith-based adoption agencies
- Religious exemptions from mandates

**IRS Guidance**: Pastors CAN endorse candidates from the pulpit under updated IRS guidance.

### 4️⃣ Traditional Family Values
California promotes LGBTQ+ agenda in schools and attacks traditional marriage. Support candidates who will:
- Ban child gender transitions
- Keep biological males out of girls' sports and bathrooms
- Protect parental notification rights
- Defend traditional marriage and family structure
- Oppose LGBTQ+ indoctrination in schools

**California leads the nation in attacking family values. Conservative leaders can reverse this.**

### 5️⃣ Second Amendment Rights
California has the strictest gun control laws in America. Support candidates who will:
- Oppose "assault weapon" bans
- Defend concealed carry rights
- Oppose magazine capacity limits
- Protect gun manufacturers from lawsuits
- Defend constitutional carry

**Chad Bianco is the strongest Second Amendment candidate - "shall not be infringed."**

### 6️⃣ Election Integrity
California's election system lacks basic security measures. Support candidates who will:
- Require voter ID
- Ban ballot harvesting
- Clean voter rolls of dead/moved voters
- Require signature verification
- Oppose automatic voter registration
- Defend against election fraud

**California's elections need reform to restore voter confidence.**

### 7️⃣ Border Security & Immigration
California is a sanctuary state that shields illegal aliens from deportation. Support candidates who will:
- End sanctuary state policies
- Mandate E-Verify for employers
- Support deportation of criminal illegal aliens
- Oppose driver's licenses for illegal aliens
- Support border wall construction
- Crack down on human trafficking

**California's sanctuary policies endanger citizens and encourage illegal immigration.**

### 8️⃣ Economic Freedom & Lower Taxes
California has the highest taxes and most regulations in America. Support candidates who will:
- Cut income taxes and property taxes
- Reduce regulations on businesses
- Oppose gas tax increases
- Defend Proposition 13 (property tax limits)
- Reject Green New Deal mandates
- Keep California business-friendly

**California's high taxes and regulations drive families and businesses out of state.**

---

## 📅 Important Dates

- **Voter Registration Deadline**: 15 days before Election Day
- **Early Voting**: Vote-by-mail starts October 5, 2026
- **Primary Election**: June 2, 2026
- **General Election**: November 3, 2026

**Register to vote**: https://registertovote.ca.gov/

---

## 🗳️ How to Vote Biblically

**Prayer**: Ask God for wisdom in selecting leaders who honor Him (James 1:5)

**Research**: Review candidates' positions on life, family, and religious liberty

**Vote**: Participate in primaries AND general election - the Governor primary is CRITICAL

**Encourage**: Bring fellow believers to the polls - California's future depends on Christian voter turnout

---

## 📞 Take Action Now

1. **Register to vote** - Deadline is 15 days before Election Day
2. **Vote in the June 2 primary** - Choosing the right Governor candidate is CRITICAL
3. **Request mail ballot** if needed - Don't let Democrats out-organize us
4. **Volunteer** for Chad Bianco and conservative candidates
5. **Pray** for California and our nation - 2 Chronicles 7:14
6. **Share** this guide with your church, family, and friends

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

**Bottom Line**: Pastors have FREEDOM to speak truth. California needs bold pastoral leadership to mobilize conservative voters.

---

## 🔥 Final Word

California's **OPEN Governor race** is the most important election in 2026. Gavin Newsom has destroyed California with radical policies, but his term limit gives conservatives a once-in-a-generation opportunity.

**NO U.S. SENATE RACE IN 2026** - Focus on Governor and statewide offices.

Chad Bianco is California's best hope - a constitutional sheriff who refused COVID mandates, defends the Second Amendment, and stands for Christian values. The Superintendent race is also OPEN - a chance to protect children from radical indoctrination.

**Your vote will determine if California remains a progressive wasteland or becomes a beacon of conservative leadership.**

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information before voting. May God guide California in 2026.*"""

# New Mexico Summary
new_mexico_summary = """# 🌶️ New Mexico 2026 Conservative Voter Guide

## 📊 Election Overview

New Mexico features **critical 2026 statewide races** including Governor and statewide offices. **NO U.S. Senate race in 2026** - both senators (Lujan and Heinrich) are not up until 2028/2030. Focus on flipping the governorship and electing conservative leaders.

**Key Races:**
- 🔴 **Governor**: Competitive race
- 🔴 **Statewide Offices**: Multiple races
- 🔴 **Albuquerque Municipal**: November 4, 2025 (Mayor and City Council)

**Election Dates:**
- November 4, 2025 - Albuquerque municipal elections
- November 3, 2026 - General election (Federal and Statewide)

---

## 🎯 Top Priority Races

### Governor - 2026
**Why This Matters**: New Mexico's governor controls state policy on life, education, border security, and religious liberty. Electing a conservative governor would transform New Mexico.

### Albuquerque Mayor - November 4, 2025
**Why This Matters**: Albuquerque is New Mexico's largest city. The mayor controls crime policy, homelessness response, and city budget. Conservative leadership needed.

---

## 🔥 8 Key Issues for New Mexico Conservatives

### 1️⃣ Pro-Life Protections
New Mexico has no gestational limits on abortion. Support candidates who will:
- Restrict late-term abortions
- Require parental notification for minors
- Protect healthcare workers' conscience rights
- Defund Planned Parenthood

### 2️⃣ School Choice & Parental Rights
Support candidates who back:
- Education Savings Accounts
- Charter school expansion
- Parental rights over curriculum
- Opposition to CRT and gender ideology

### 3️⃣ Religious Liberty
Protect New Mexico's faith communities. Support candidates who defend:
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
New Mexico needs strong gun rights protection. Support candidates who will:
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
New Mexico faces border crisis impacts. Support candidates who will:
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

- **Albuquerque Municipal Election**: November 4, 2025
- **Primary Election**: June 2026 (date TBD)
- **General Election**: November 3, 2026

**Register to vote**: https://portal.sos.state.nm.us/OVR/

---

## 🗳️ How to Vote Biblically

**Prayer**: Ask God for wisdom (James 1:5)

**Research**: Review candidates' positions on biblical values

**Vote**: Participate in ALL elections - municipal, primary, and general

**Encourage**: Bring fellow believers to the polls

---

## 📞 Take Action Now

1. **Register to vote**
2. **Vote in Albuquerque municipal election** (November 4, 2025)
3. **Vote in primary and general elections** (2026)
4. **Volunteer** for conservative candidates
5. **Pray** for New Mexico - 2 Chronicles 7:14
6. **Share** this guide with your church

---

## 🙏 Final Word

New Mexico needs conservative Christian leadership. The Governor race in 2026 and Albuquerque Mayor race in 2025 are critical opportunities to elect leaders who honor God and defend biblical values.

**Your vote is your voice. Your silence is surrender.**

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information before voting. May God guide New Mexico in 2025-2026.*"""

# Nevada Summary
nevada_summary = """# 🎰 Nevada 2026 Conservative Voter Guide

## 📊 Election Overview

Nevada features **critical 2026 statewide races** including Governor Joe Lombardo's re-election. **NO U.S. Senate race in 2026** - both senators (Rosen-2028, Cortez Masto-2030) are not up until later cycles. Focus on maintaining Republican governorship and flipping statewide offices.

**Key Races:**
- 🔴 **Governor**: Joe Lombardo (R) re-election
- 🔴 **Statewide Offices**: Multiple competitive races

**Election Date:**
- November 3, 2026 - General election

---

## 🎯 Top Priority Races

### Governor - Joe Lombardo (R) Re-election
**Incumbent**: Joe Lombardo (R) - Former Las Vegas Metropolitan Police Sheriff

**Why This Matters**: Lombardo is Nevada's first Republican governor in 20 years. He defeated Democrat Steve Sisolak in 2022. Keeping Nevada's governorship Republican is CRITICAL for conservative policies on life, education, and border security.

**Lombardo's Record**:
- Strong law enforcement background
- Pro-business policies
- Education reform advocate
- Border security supporter

---

## 🔥 8 Key Issues for Nevada Conservatives

### 1️⃣ Pro-Life Protections
Nevada allows abortion up to 24 weeks. Support candidates who will:
- Restrict late-term abortions
- Require parental notification for minors
- Protect healthcare workers' conscience rights
- Defund Planned Parenthood

### 2️⃣ School Choice & Parental Rights
Support candidates who back:
- Education Savings Accounts
- Charter school expansion
- Parental rights over curriculum
- Opposition to CRT and gender ideology

### 3️⃣ Religious Liberty
Protect Nevada's faith communities. Support candidates who defend:
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
Nevada needs strong gun rights protection. Support candidates who will:
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
Nevada faces illegal immigration impacts. Support candidates who will:
- Secure the border
- End sanctuary policies
- Mandate E-Verify
- Deport criminal illegal aliens

### 8️⃣ Economic Freedom & Lower Taxes
Support candidates who will:
- Maintain no state income tax
- Cut regulations
- Oppose Green New Deal mandates
- Protect gaming and tourism industries

---

## 📅 Important Dates

- **Primary Election**: August 2026 (date TBD)
- **General Election**: November 3, 2026

**Register to vote**: https://www.nvsos.gov/sos/elections/voters

---

## 🗳️ How to Vote Biblically

**Prayer**: Ask God for wisdom (James 1:5)

**Research**: Review candidates' positions on biblical values

**Vote**: Participate in primary AND general election

**Encourage**: Bring fellow believers to the polls

---

## 📞 Take Action Now

1. **Register to vote**
2. **Support Joe Lombardo** for Governor re-election
3. **Vote in primary and general elections**
4. **Volunteer** for conservative candidates
5. **Pray** for Nevada - 2 Chronicles 7:14
6. **Share** this guide with your church

---

## 🙏 Final Word

Nevada's **Governor race** is critical for maintaining Republican leadership. Joe Lombardo broke 20 years of Democrat control in 2022 - we must keep Nevada red in 2026.

**NO U.S. SENATE RACE IN 2026** - Focus on Governor and statewide offices.

**Your vote will determine if Nevada remains under conservative leadership or returns to Democrat control.**

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information before voting. May God guide Nevada in 2026.*"""

# North Carolina Summary
north_carolina_summary = """# 🌲 North Carolina 2026 Conservative Voter Guide

## 📊 Election Overview

North Carolina features **critical 2026 statewide races** including Governor and statewide offices. **NO U.S. Senate race in 2026** - both senators (Tillis-2028, Budd-2030) are not up until later cycles. Focus on maintaining Republican leadership in statewide offices.

**Key Races:**
- 🔴 **Governor**: Competitive race
- 🔴 **Statewide Offices**: Multiple races

**Election Date:**
- November 3, 2026 - General election (NOT November 4)

---

## 🎯 Top Priority Races

### Governor - 2026
**Why This Matters**: North Carolina's governor controls state policy on life, education, and religious liberty. Electing a conservative governor is critical for advancing biblical values.

---

## 🔥 8 Key Issues for North Carolina Conservatives

### 1️⃣ Pro-Life Protections
North Carolina has 12-week abortion limit. Support candidates who will:
- Defend current pro-life protections
- Require parental notification for minors
- Protect healthcare workers' conscience rights
- Defund Planned Parenthood

### 2️⃣ School Choice & Parental Rights
Support candidates who back:
- Education Savings Accounts
- Charter school expansion
- Parental rights over curriculum
- Opposition to CRT and gender ideology

### 3️⃣ Religious Liberty
Protect North Carolina's faith communities. Support candidates who defend:
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
North Carolina needs strong gun rights protection. Support candidates who will:
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

- **Primary Election**: May 2026 (date TBD)
- **General Election**: November 3, 2026 (NOT November 4)

**Register to vote**: https://www.ncsbe.gov/registering

---

## 🗳️ How to Vote Biblically

**Prayer**: Ask God for wisdom (James 1:5)

**Research**: Review candidates' positions on biblical values

**Vote**: Participate in primary AND general election

**Encourage**: Bring fellow believers to the polls

---

## 📞 Take Action Now

1. **Register to vote**
2. **Vote in primary and general elections**
3. **Volunteer** for conservative candidates
4. **Pray** for North Carolina - 2 Chronicles 7:14
5. **Share** this guide with your church

---

## 🙏 Final Word

North Carolina's **Governor race** is critical for maintaining conservative leadership. The state needs leaders who honor God and defend biblical values.

**NO U.S. SENATE RACE IN 2026** - Focus on Governor and statewide offices.

**Your vote will determine if North Carolina remains under conservative leadership.**

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information before voting. May God guide North Carolina in 2026.*"""

# Upload all summaries
summaries = [
    {'state': 'California', 'summary': california_summary},
    {'state': 'New Mexico', 'summary': new_mexico_summary},
    {'state': 'Nevada', 'summary': nevada_summary},
    {'state': 'North Carolina', 'summary': north_carolina_summary}
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

print(f"\nAll 4 state summaries uploaded successfully!")
