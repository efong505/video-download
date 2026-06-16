import boto3
from boto3.dynamodb.conditions import Attr
import uuid

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

# Check for existing Florida summary
response = summaries_table.scan(FilterExpression=Attr('state').eq('Florida'))
if response['Items']:
    print("Florida summary already exists. Deleting old version...")
    for item in response['Items']:
        try:
            key = {'summary_id': item.get('summary_id')} if 'summary_id' in item else {'state': item['state']}
            summaries_table.delete_item(Key=key)
            print("  Deleted old summary")
        except:
            pass

# Create Florida 2026 summary
florida_summary = """# 🌴 Florida 2026 Conservative Voter Guide

## 📊 Election Overview

Florida features **critical 2026 statewide races** with Governor Ron DeSantis term-limited, creating an **OPEN SEAT** for Governor. **NO U.S. Senate race in 2026** - Senator Rick Scott is not up until 2028. Focus on maintaining Republican control of all statewide offices.

**Key Races:**
- 🔴 **Governor**: OPEN SEAT (DeSantis term-limited) - MUST HOLD
- 🔴 **Attorney General**: Ashley Moody (R) re-election
- 🔴 **Chief Financial Officer**: Jimmy Patronis (R) re-election
- 🔴 **Agriculture Commissioner**: Wilton Simpson (R) re-election

---

## 🎯 Top Priority Races

### Governor - OPEN SEAT (CRITICAL)
**Status**: Ron DeSantis is **TERM-LIMITED** and cannot run for a third consecutive term. This is an **OPEN SEAT** - the most important race in Florida 2026.

**Why This Matters**: DeSantis transformed Florida into America's freest state - strong economy, school choice, parental rights, election integrity, and pro-life protections. Florida MUST elect a conservative governor to continue this legacy and prevent Democrat takeover.

**Republican Primary**: Multiple candidates expected to run for this critical open seat. Primary voters must choose a proven conservative who will continue DeSantis's policies.

**Democrat Threat**: Democrats will pour millions into flipping Florida's governorship. Cannot let them undo 8 years of conservative progress.

### Attorney General - Ashley Moody (R)
**Incumbent**: Ashley Moody (R) - Strong conservative record

**Why This Matters**: Moody has defended Florida's conservative laws, fought human trafficking, protected election integrity, and stood against federal overreach. She's been a warrior for Florida families and must be re-elected.

### Chief Financial Officer - Jimmy Patronis (R)
**Incumbent**: Jimmy Patronis (R) - Fiscal conservative

**Why This Matters**: Patronis manages Florida's finances with conservative principles - low taxes, fiscal responsibility, and protecting taxpayer dollars. His leadership keeps Florida's economy strong.

### Commissioner of Agriculture - Wilton Simpson (R)
**Incumbent**: Wilton Simpson (R) - Strong agricultural advocate

**Why This Matters**: Simpson protects Florida's agriculture industry, supports farmers and ranchers, and defends rural communities. Critical for Florida's economy and food security.

---

## 🔥 8 Key Issues for Florida Conservatives

### 1️⃣ Pro-Life Protections
Florida passed the **Heartbeat Protection Act** banning most abortions after 6 weeks. Democrats want to eliminate these protections through ballot measures. Support candidates who will:
- Defend the Heartbeat Protection Act
- Oppose abortion ballot initiatives
- Defund Planned Parenthood
- Protect healthcare workers' conscience rights
- Require parental consent for minors

**The next Governor MUST defend Florida's pro-life laws against Democrat attacks.**

### 2️⃣ School Choice & Parental Rights
Florida leads the nation in school choice and parental rights. Support candidates who will:
- Expand universal school choice and ESAs
- Defend Parental Rights in Education Act ("Don't Say Gay" bill)
- Ban CRT and radical gender ideology in schools
- Protect children from inappropriate sexual content
- Oppose teacher union control
- Defend homeschool freedom

**Florida's education freedom is under attack. The next Governor must protect parental rights.**

### 3️⃣ Religious Liberty
Florida protects faith communities from government overreach. Support candidates who defend:
- Church autonomy and pastoral freedom
- Christian business owners' conscience rights
- Prayer in schools and public spaces
- Faith-based adoption agencies
- Religious exemptions from mandates

**IRS Guidance**: Pastors CAN endorse candidates from the pulpit under updated IRS guidance. Churches should not be silenced.

### 4️⃣ Traditional Family Values
Florida banned child gender transitions and protects children. Support candidates who will:
- Maintain ban on child gender surgeries and puberty blockers
- Keep biological males out of girls' sports and bathrooms
- Protect parental notification rights
- Defend traditional marriage and family structure
- Oppose LGBTQ+ indoctrination in schools

**Florida leads the nation in protecting children. Cannot let Democrats reverse this.**

### 5️⃣ Second Amendment Rights
Florida is a constitutional carry state with strong gun rights. Support candidates who will:
- Protect constitutional carry
- Oppose "assault weapon" bans
- Defend concealed carry rights
- Oppose red flag laws without due process
- Protect gun manufacturers from lawsuits

**Florida's gun rights are the strongest in the nation. Must elect leaders who will keep them that way.**

### 6️⃣ Election Integrity
Florida has the nation's strongest election integrity laws. Support candidates who will:
- Maintain voter ID requirements
- Ban ballot harvesting
- Clean voter rolls of dead/moved voters
- Require signature verification
- Oppose mail-in ballot abuse
- Defend against federal election takeover

**Florida's elections are secure because of Republican leadership. Cannot let Democrats weaken these protections.**

### 7️⃣ Border Security & Immigration
Florida faces illegal immigration impacts from southern border crisis. Support candidates who will:
- Ban sanctuary cities (already done - must maintain)
- Mandate E-Verify for employers
- Deport criminal illegal aliens
- Support border wall construction
- Oppose amnesty programs
- Crack down on human trafficking

**Florida has led the nation in fighting illegal immigration. The next Governor must continue this fight.**

### 8️⃣ Economic Freedom & Lower Taxes
Florida has NO state income tax and a booming economy. Support candidates who will:
- Maintain NO state income tax
- Cut regulations and red tape
- Oppose property tax increases
- Defend business freedom
- Reject Green New Deal mandates
- Keep Florida business-friendly

**Florida's economy is the envy of the nation. Must elect leaders who will keep taxes low and businesses free.**

---

## 📅 Important Dates

- **Voter Registration Deadline**: 29 days before Election Day
- **Early Voting**: Varies by county (typically 10-15 days before)
- **Primary Election**: August 2026 (date TBD)
- **General Election**: November 3, 2026

**Register to vote**: https://registertovoteflorida.gov/

---

## 🗳️ How to Vote Biblically

**Prayer**: Ask God for wisdom in selecting leaders who honor Him (James 1:5)

**Research**: Review candidates' positions on life, family, and religious liberty

**Vote**: Participate in primaries AND general election - the Governor primary is CRITICAL

**Encourage**: Bring fellow believers to the polls - your church family's votes will determine Florida's future

---

## 📞 Take Action Now

1. **Register to vote** - Deadline is 29 days before Election Day
2. **Vote in the Republican primary** - Choosing the right Governor candidate is CRITICAL
3. **Request mail ballot** if needed - Don't let Democrats out-organize us
4. **Volunteer** for conservative candidates - Knock doors, make calls, donate
5. **Pray** for Florida and our nation - 2 Chronicles 7:14
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

**Bottom Line**: Pastors have FREEDOM to speak truth. Florida needs bold pastoral leadership to mobilize conservative voters and protect our freedoms.

---

## 🔥 Final Word

Florida's **OPEN Governor race** is the most important election in 2026. Ron DeSantis transformed Florida into America's freest state, but Democrats want to undo everything he accomplished.

**NO U.S. SENATE RACE IN 2026** - Focus on Governor and statewide offices.

The Governor primary will determine Florida's future. Conservative Christians MUST unite behind a proven conservative who will:
- Defend pro-life protections
- Protect parental rights and school choice
- Maintain election integrity
- Keep Florida free from government overreach

Ashley Moody, Jimmy Patronis, and Wilton Simpson have served Florida well and deserve re-election.

**Your vote will determine if Florida remains free or falls to Democrat control.**

**"When the righteous are in authority, the people rejoice; But when a wicked man rules, the people groan." - Proverbs 29:2**

---

*This guide is for educational purposes. Verify all candidate information before voting. May God guide Florida in 2026.*"""

summary_item = {
    'summary_id': str(uuid.uuid4()),
    'state': 'Florida',
    'election_cycle': '2025-2026',
    'summary': florida_summary,
    'last_updated': '2025-01-01'
}

summaries_table.put_item(Item=summary_item)
print(f"\nFlorida summary created: {len(florida_summary)} characters")
