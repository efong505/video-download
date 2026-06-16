import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

nh_summary = """# 🗳️ New Hampshire 2026 Voter Guide

## 📊 Election Overview

**Primary Election**: September 8, 2026  
**General Election**: November 3, 2026

New Hampshire features a **TOSS-UP U.S. Senate race** with Senator Jeanne Shaheen (D) retiring after 18 years, creating the first open Senate seat since 2010. This is a **TOP PICKUP OPPORTUNITY** for conservatives. Governor Kelly Ayotte (R) seeks re-election in a competitive race.

---

## 🔴 Key Races

### U.S. Senate (OPEN SEAT - TOSS-UP)
**Incumbent**: Jeanne Shaheen (D) - NOT SEEKING RE-ELECTION

**🔵 Democrat Candidates**:
- **Chris Pappas** - U.S. Representative (NH-01), progressive voting record
- **Karishma Manzur** - NH Democratic Party Rules Committee Member
- **Jared Sullivan** - State Representative

**🔴 Republican Candidates**:
- **John Sununu** - Former U.S. Senator (2003-2009), strong conservative record
- **Scott Brown** - Former MA Senator, 2014 NH nominee
- **Dan Innis** - State Senator

**Rating**: TOSS-UP - First open seat in 16 years, Republicans have strong recruitment

### Governor
**Incumbent**: Kelly Ayotte (R) - SEEKING RE-ELECTION

**🔴 Republican**:
- **Kelly Ayotte** (Incumbent) - Former U.S. Senator, pro-life, 2nd Amendment defender

**Primary Challenger**:
- **Corey Lewandowski** - Trump 2016 campaign manager

**🔵 Democrat Candidates**:
- **Jon Kiper** - Former Newmarket town councilor
- **Tom Sherman** - Former state senator, 2022 nominee

**Rating**: LEAN REPUBLICAN

---

## 🎯 8 Key Issues for Conservative Voters

### 1️⃣ Pro-Life Values
New Hampshire has minimal abortion restrictions. Conservative candidates support parental notification, informed consent laws, and conscience protections for healthcare workers. The open Senate seat provides opportunity to elect a pro-life champion.

### 2️⃣ School Choice & Parental Rights
NH has Education Freedom Accounts (school vouchers). Republicans defend and expand school choice, oppose CRT and gender ideology in schools, support parental rights in education decisions.

### 3️⃣ Religious Liberty
Conservatives protect First Amendment rights, defend churches from government overreach, oppose mandates that violate conscience, support faith-based adoption agencies.

### 4️⃣ Family Values & Parental Authority
Republican candidates oppose radical gender ideology, defend biological sex definitions, protect parental rights, support traditional marriage values.

### 5️⃣ 2nd Amendment Rights
NH is a constitutional carry state. Conservatives defend gun rights, oppose federal gun control, protect concealed carry reciprocity, defend against red flag laws.

### 6️⃣ Election Integrity
Republicans support voter ID requirements, oppose ballot harvesting, defend election security measures, ensure accurate voter rolls, protect against fraud.

### 7️⃣ Border Security & Immigration
Conservative candidates support completing border wall, ending sanctuary policies, enforcing immigration laws, opposing amnesty, protecting American workers.

### 8️⃣ Economic Freedom & Limited Government
Republicans support lower taxes, reduced regulations, free market principles, fiscal responsibility, oppose socialist policies, defend small businesses.

---

## 📅 Important Dates

- **Voter Registration Deadline**: Varies by municipality (same-day registration available)
- **Absentee Ballot Request Deadline**: Contact local clerk
- **Early Voting**: Limited (absentee voting available)
- **Primary Election**: September 8, 2026
- **General Election**: November 3, 2026

---

## 🗳️ How to Vote

1. **Register to Vote**: Visit [sos.nh.gov](https://sos.nh.gov) or register at polling place
2. **Find Your Polling Location**: Contact local town/city clerk
3. **Bring Photo ID**: Required for voting
4. **Request Absentee Ballot**: If unable to vote in person

---

## 📞 Get Involved

- **Volunteer**: Contact local Republican Party or candidate campaigns
- **Donate**: Support conservative candidates in competitive races
- **Pray**: Lift up candidates, voters, and election integrity
- **Vote**: Participate in primary (Sept 8) and general election (Nov 3)

---

## 🔥 Why This Election Matters

New Hampshire's **OPEN U.S. SENATE SEAT** is a **TOP PICKUP OPPORTUNITY** for conservatives. With Shaheen retiring, Republicans have their best chance in nearly two decades to flip this seat. The Senate race will determine control of the U.S. Senate and the future of pro-life legislation, border security, and constitutional governance.

Governor Ayotte's re-election is critical to maintaining conservative leadership in the Granite State. Every race matters for protecting life, liberty, and family values.

---

## 🙏 Pastoral Endorsements & IRS Guidance

**Pastors CAN endorse candidates from the pulpit.** The IRS allows churches to maintain tax-exempt status while pastors speak on political issues and endorse candidates **in their personal capacity**. Churches cannot make institutional endorsements or use church resources for campaigns, but pastoral speech is protected.

For guidance: [Alliance Defending Freedom - Pulpit Freedom](https://adflegal.org/pulpit-freedom)

---

**Vote for life. Vote for liberty. Vote for family values.**

🗳️ **Primary: September 8, 2026 | General: November 3, 2026** 🗳️"""

mn_summary = """# 🗳️ Minnesota 2026 Voter Guide

## 📊 Election Overview

**Primary Election**: August 11, 2026  
**General Election**: November 3, 2026

Minnesota features an **OPEN U.S. Senate race** with Senator Tina Smith (D) retiring, creating the first open Senate seat since 2002. Governor Tim Walz (D), the 2024 VP candidate, seeks an unprecedented third consecutive term. Both races are competitive opportunities for conservatives.

---

## 🔴 Key Races

### U.S. Senate (OPEN SEAT)
**Incumbent**: Tina Smith (D) - NOT SEEKING RE-ELECTION

**🔵 Democrat Candidates**:
- **Peggy Flanagan** - Lieutenant Governor, progressive record
- **Angie Craig** - U.S. Representative (MN-02)
- **Melisa Lopez Franzen** - Former State Senate Minority Leader
- **Melvin Carter** - Mayor of Saint Paul
- **Dave Wellstone** - Son of former Senator Paul Wellstone

**🔴 Republican Candidates**:
- **Royce White** - Former NBA player, 2024 nominee, America First conservative
- **Tom Weiler** - Retired U.S. Navy officer
- **Ray Petersen** - Truck driver, grassroots conservative
- **Julia Coleman** - State Senator
- **Lisa Demuth** - MN House Speaker
- **Zach Duckworth** - State Senator
- **Tom Emmer** - U.S. Representative (MN-06), 2010 gubernatorial nominee
- **Pete Stauber** - U.S. Representative (MN-08)

**Rating**: LIKELY DEMOCRAT (but competitive with strong Republican nominee)

### Governor
**Incumbent**: Tim Walz (D) - SEEKING THIRD TERM

**🔵 Democrat**:
- **Tim Walz** (Incumbent) - 2024 VP candidate, progressive policies

**🔴 Republican Candidates**:
- **Scott Jensen** - Former State Senator, 2022 nominee, physician
- **Kendall Qualls** - Healthcare executive, 2022 candidate
- **Jeff Johnson** - Former St. Cloud city councilor
- **Chris Madel** - Attorney
- **Jim Nash** - State Representative

**Rating**: LEAN DEMOCRAT

---

## 🎯 8 Key Issues for Conservative Voters

### 1️⃣ Pro-Life Values
Minnesota has minimal abortion protections after Democrats passed extreme abortion laws. Conservative candidates support protecting life, parental notification, informed consent, and reversing radical pro-abortion legislation.

### 2️⃣ School Choice & Parental Rights
Republicans support education freedom, school choice, charter schools, oppose CRT and gender ideology in schools, defend parental rights against government overreach.

### 3️⃣ Religious Liberty
Conservatives protect First Amendment rights, defend churches from discrimination, oppose mandates violating conscience, support faith-based organizations.

### 4️⃣ Family Values & Parental Authority
Republican candidates oppose radical gender ideology, defend biological sex, protect children from harmful medical procedures, support parental authority, defend traditional family values.

### 5️⃣ 2nd Amendment Rights
Conservatives defend gun rights, oppose gun control measures, protect concealed carry, defend against red flag laws, support constitutional carry.

### 6️⃣ Election Integrity
Republicans support voter ID, oppose ballot harvesting, defend election security, ensure accurate voter rolls, protect against fraud.

### 7️⃣ Border Security & Immigration
Conservative candidates support border wall, ending sanctuary policies, enforcing immigration laws, opposing amnesty, protecting American workers.

### 8️⃣ Economic Freedom & Limited Government
Republicans support lower taxes, reduced regulations, free market principles, fiscal responsibility, oppose socialist policies, defend small businesses.

---

## 📅 Important Dates

- **Voter Registration Deadline**: 21 days before election (online/mail), Election Day (in-person)
- **Absentee Ballot Request Deadline**: One week before election
- **Early Voting**: 46 days before election
- **Primary Election**: August 11, 2026
- **General Election**: November 3, 2026

---

## 🗳️ How to Vote

1. **Register to Vote**: Visit [mnvotes.org](https://mnvotes.org) or register on Election Day
2. **Find Your Polling Location**: Check mnvotes.org
3. **Request Absentee Ballot**: Apply online or by mail
4. **Early Voting**: Available 46 days before election

---

## 📞 Get Involved

- **Volunteer**: Contact local Republican Party or candidate campaigns
- **Donate**: Support conservative candidates in competitive races
- **Pray**: Lift up candidates, voters, and election integrity
- **Vote**: Participate in primary (Aug 11) and general election (Nov 3)

---

## 🔥 Why This Election Matters

Minnesota's **OPEN U.S. SENATE SEAT** provides a pickup opportunity for conservatives. With Tina Smith retiring, Republicans can compete for this seat with strong recruitment and turnout.

Defeating **Tim Walz**, the 2024 VP candidate seeking a third term, would be a major victory for conservatives. Walz has pushed progressive policies including extreme abortion laws, COVID lockdowns, and support for riots in 2020.

Every race matters for protecting life, liberty, and family values in Minnesota.

---

## 🙏 Pastoral Endorsements & IRS Guidance

**Pastors CAN endorse candidates from the pulpit.** The IRS allows churches to maintain tax-exempt status while pastors speak on political issues and endorse candidates **in their personal capacity**. Churches cannot make institutional endorsements or use church resources for campaigns, but pastoral speech is protected.

For guidance: [Alliance Defending Freedom - Pulpit Freedom](https://adflegal.org/pulpit-freedom)

---

**Vote for life. Vote for liberty. Vote for family values.**

🗳️ **Primary: August 11, 2026 | General: November 3, 2026** 🗳️"""

co_summary = """# 🗳️ Colorado 2026 Voter Guide

## 📊 Election Overview

**Primary Election**: June 30, 2026  
**General Election**: November 3, 2026

Colorado features a **U.S. Senate race** with incumbent John Hickenlooper (D) seeking re-election and an **OPEN GOVERNOR race** with Jared Polis (D) term-limited. Both races provide opportunities for conservatives to compete in this increasingly purple state.

---

## 🔴 Key Races

### U.S. Senate
**Incumbent**: John Hickenlooper (D) - SEEKING RE-ELECTION

**🔵 Democrat**:
- **John Hickenlooper** (Incumbent) - Former Governor, progressive voting record

**🔴 Republican Candidates**:
- **Janak Joshi** - Former State Representative, physician, conservative leader
- **Heidi Ganahl** - Former CU Board of Regents, 2022 gubernatorial nominee

**Rating**: LIKELY DEMOCRAT (but competitive)

### Governor (OPEN SEAT)
**Incumbent**: Jared Polis (D) - TERM-LIMITED

**🔵 Democrat Candidates**:
- **Michael Bennet** - U.S. Senator, 2020 presidential candidate
- **Phil Weiser** - Attorney General
- **Jason Crow** - U.S. Representative (CO-06)
- **Mike Johnston** - Mayor of Denver, 2018 candidate

**🔴 Republican Candidates**:
- **Barbara Kirkmeyer** - State Senator, 2022 CO-08 nominee
- **Greg Lopez** - Former U.S. Representative (CO-04), 2018 & 2022 candidate
- **Plus 14 additional Republican candidates**

**Rating**: LEAN DEMOCRAT

---

## 🎯 8 Key Issues for Conservative Voters

### 1️⃣ Pro-Life Values
Colorado has minimal abortion restrictions after Democrats passed extreme abortion laws. Conservative candidates support protecting life, parental notification, informed consent, and reversing radical pro-abortion legislation.

### 2️⃣ School Choice & Parental Rights
Republicans support education freedom, school choice, charter schools, oppose CRT and gender ideology in schools, defend parental rights in education decisions.

### 3️⃣ Religious Liberty
Conservatives protect First Amendment rights, defend religious business owners (like Masterpiece Cakeshop), oppose mandates violating conscience, support faith-based organizations.

### 4️⃣ Family Values & Parental Authority
Republican candidates oppose radical gender ideology, defend biological sex definitions, protect children from harmful procedures, support parental authority, defend traditional family values.

### 5️⃣ 2nd Amendment Rights
Conservatives defend gun rights, oppose gun control measures including red flag laws, protect concealed carry, support constitutional carry, defend against magazine bans.

### 6️⃣ Election Integrity
Republicans support voter ID, oppose universal mail-in voting vulnerabilities, defend election security, ensure accurate voter rolls, protect against fraud.

### 7️⃣ Border Security & Immigration
Conservative candidates support border wall, ending sanctuary policies, enforcing immigration laws, opposing amnesty, protecting American workers from illegal immigration.

### 8️⃣ Economic Freedom & Limited Government
Republicans support lower taxes, reduced regulations, free market principles, fiscal responsibility, oppose socialist policies, defend small businesses, protect energy jobs.

---

## 📅 Important Dates

- **Voter Registration Deadline**: 8 days before election (online), 7 days before (mail), Election Day (in-person)
- **Mail Ballot Deadline**: Ballots mailed to all registered voters
- **Ballot Return Deadline**: 7:00 PM on Election Day
- **Primary Election**: June 30, 2026
- **General Election**: November 3, 2026

---

## 🗳️ How to Vote

1. **Register to Vote**: Visit [GoVoteColorado.gov](https://www.govotecolorado.gov)
2. **Receive Mail Ballot**: Automatically mailed to all registered voters
3. **Return Ballot**: Mail (postmarked by Election Day) or drop at secure drop box by 7 PM
4. **In-Person Voting**: Available at voter service centers

---

## 📞 Get Involved

- **Volunteer**: Contact local Republican Party or candidate campaigns
- **Donate**: Support conservative candidates in competitive races
- **Pray**: Lift up candidates, voters, and election integrity
- **Vote**: Participate in primary (June 30) and general election (Nov 3)

---

## 🔥 Why This Election Matters

Colorado's **OPEN GOVERNOR race** with Polis term-limited provides an opportunity for conservatives to compete for executive leadership. With a crowded Republican primary, grassroots engagement is critical.

The **U.S. Senate race** against Hickenlooper is competitive with strong Republican recruitment. Flipping this seat would help secure Senate control and advance conservative priorities.

Every race matters for protecting life, liberty, and family values in Colorado.

---

## 🙏 Pastoral Endorsements & IRS Guidance

**Pastors CAN endorse candidates from the pulpit.** The IRS allows churches to maintain tax-exempt status while pastors speak on political issues and endorse candidates **in their personal capacity**. Churches cannot make institutional endorsements or use church resources for campaigns, but pastoral speech is protected.

For guidance: [Alliance Defending Freedom - Pulpit Freedom](https://adflegal.org/pulpit-freedom)

---

**Vote for life. Vote for liberty. Vote for family values.**

🗳️ **Primary: June 30, 2026 | General: November 3, 2026** 🗳️"""

print("Uploading state summaries...")

summaries_table.put_item(Item={
    'state': 'New Hampshire',
    'title': 'New Hampshire 2026 Voter Guide',
    'content': nh_summary,
    'updated_at': '2025-01-XX'
})
print(f"New Hampshire: {len(nh_summary)} characters")

summaries_table.put_item(Item={
    'state': 'Minnesota',
    'title': 'Minnesota 2026 Voter Guide',
    'content': mn_summary,
    'updated_at': '2025-01-XX'
})
print(f"Minnesota: {len(mn_summary)} characters")

summaries_table.put_item(Item={
    'state': 'Colorado',
    'title': 'Colorado 2026 Voter Guide',
    'content': co_summary,
    'updated_at': '2025-01-XX'
})
print(f"Colorado: {len(co_summary)} characters")

print("\n" + "="*60)
print("SUMMARIES UPLOADED SUCCESSFULLY")
print("="*60)
