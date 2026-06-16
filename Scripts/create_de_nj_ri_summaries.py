import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

de_summary = """# 🗳️ Delaware 2026 Voter Guide

## 📊 Election Overview

**Primary Election**: September 15, 2026  
**General Election**: November 3, 2026

⚠️ **CANDIDATE UPDATE**: Major party candidates for the 2026 U.S. Senate race have not yet been officially declared. This guide will be updated as candidates announce their campaigns.

Delaware features a **U.S. Senate race** with incumbent Chris Coons (D) expected to seek re-election. This safe Democrat seat provides an opportunity for conservative engagement and grassroots mobilization.

---

## 🔴 Key Races

### U.S. Senate
**Incumbent**: Chris Coons (D) - Expected to seek re-election

**🔵 Democrat**:
- **Chris Coons** (Incumbent) - Progressive voting record, Biden ally

**🔴 Republican Candidates**:
- **TBD** - Candidates have not yet declared

**Rating**: SAFE DEMOCRAT

⚠️ **Note**: Republican candidates are expected to announce in early 2026. Check back for updates on the GOP primary field.

---

## 🎯 8 Key Issues for Conservative Voters

### 1️⃣ Pro-Life Values
Delaware has minimal abortion restrictions. Conservative candidates will support protecting life, parental notification, informed consent laws, and conscience protections for healthcare workers.

### 2️⃣ School Choice & Parental Rights
Republicans support education freedom, school choice programs, charter schools, oppose CRT and gender ideology in schools, defend parental rights in education decisions.

### 3️⃣ Religious Liberty
Conservatives protect First Amendment rights, defend churches from government overreach, oppose mandates that violate conscience, support faith-based organizations.

### 4️⃣ Family Values & Parental Authority
Republican candidates oppose radical gender ideology, defend biological sex definitions, protect children from harmful procedures, support parental authority, defend traditional family values.

### 5️⃣ 2nd Amendment Rights
Conservatives defend gun rights, oppose gun control measures, protect concealed carry rights, defend against red flag laws, support constitutional carry.

### 6️⃣ Election Integrity
Republicans support voter ID requirements, oppose ballot harvesting, defend election security measures, ensure accurate voter rolls, protect against fraud.

### 7️⃣ Border Security & Immigration
Conservative candidates support completing border wall, ending sanctuary policies, enforcing immigration laws, opposing amnesty, protecting American workers.

### 8️⃣ Economic Freedom & Limited Government
Republicans support lower taxes, reduced regulations, free market principles, fiscal responsibility, oppose socialist policies, defend small businesses.

---

## 📅 Important Dates

- **Voter Registration Deadline**: Contact Delaware Election Commissioner
- **Absentee Ballot Request Deadline**: Check with local election office
- **Early Voting**: Available before Election Day
- **Primary Election**: September 15, 2026
- **General Election**: November 3, 2026

---

## 🗳️ How to Vote

1. **Register to Vote**: Visit [Delaware Elections](https://elections.delaware.gov)
2. **Find Your Polling Location**: Check elections.delaware.gov
3. **Request Absentee Ballot**: If unable to vote in person
4. **Bring ID**: Photo ID recommended

---

## 📞 Get Involved

- **Volunteer**: Contact Delaware Republican Party when candidates announce
- **Donate**: Support conservative candidates once declared
- **Pray**: Lift up candidates, voters, and election integrity
- **Vote**: Participate in primary (Sept 15) and general election (Nov 3)

---

## 🔥 Why This Election Matters

While Delaware is a safe Democrat state, **every vote matters** for building conservative momentum and holding incumbents accountable. Chris Coons has been a reliable vote for the Biden-Harris agenda, supporting radical abortion policies, open borders, and big government spending.

A strong Republican challenge can force Democrats to defend their record and energize the conservative base for future elections.

---

## 🙏 Pastoral Endorsements & IRS Guidance

**Pastors CAN endorse candidates from the pulpit.** The IRS allows churches to maintain tax-exempt status while pastors speak on political issues and endorse candidates **in their personal capacity**. Churches cannot make institutional endorsements or use church resources for campaigns, but pastoral speech is protected.

For guidance: [Alliance Defending Freedom - Pulpit Freedom](https://adflegal.org/pulpit-freedom)

---

**Vote for life. Vote for liberty. Vote for family values.**

🗳️ **Primary: September 15, 2026 | General: November 3, 2026** 🗳️

⚠️ **This guide will be updated as candidates officially declare their campaigns.**"""

nj_summary = """# 🗳️ New Jersey 2026 Voter Guide

## 📊 Election Overview

**Primary Election**: June 2, 2026  
**General Election**: November 3, 2026

⚠️ **CANDIDATE UPDATE**: Major party candidates for the 2026 U.S. Senate race have not yet been officially declared. This guide will be updated as candidates announce their campaigns.

New Jersey features a **U.S. Senate race** with incumbent Cory Booker (D) expected to seek re-election. This competitive state provides opportunities for conservative engagement.

**2025 Governor Race Note**: Phil Murphy (D) was term-limited. The November 4, 2025 gubernatorial election between Mikie Sherrill (D) and Jack Ciattarelli (R) has concluded.

---

## 🔴 Key Races

### U.S. Senate
**Incumbent**: Cory Booker (D) - Expected to seek re-election

**🔵 Democrat**:
- **Cory Booker** (Incumbent) - Progressive voting record, national figure

**🔴 Republican Candidates**:
- **TBD** - Candidates have not yet declared

**Rating**: LIKELY DEMOCRAT (but competitive with strong GOP nominee)

⚠️ **Note**: Republican candidates are expected to announce in early 2026. New Jersey has elected Republican governors and can be competitive in federal races with strong candidates.

---

## 🎯 8 Key Issues for Conservative Voters

### 1️⃣ Pro-Life Values
New Jersey has minimal abortion restrictions after Democrats passed extreme abortion laws. Conservative candidates will support protecting life, parental notification, informed consent, and reversing radical pro-abortion legislation.

### 2️⃣ School Choice & Parental Rights
Republicans support education freedom, school choice, charter schools, oppose CRT and gender ideology in schools, defend parental rights against government overreach.

### 3️⃣ Religious Liberty
Conservatives protect First Amendment rights, defend churches from discrimination, oppose mandates violating conscience, support faith-based organizations.

### 4️⃣ Family Values & Parental Authority
Republican candidates oppose radical gender ideology, defend biological sex definitions, protect children from harmful procedures, support parental authority, defend traditional family values.

### 5️⃣ 2nd Amendment Rights
Conservatives defend gun rights, oppose New Jersey's strict gun control laws, protect concealed carry rights, defend against unconstitutional restrictions.

### 6️⃣ Election Integrity
Republicans support voter ID, oppose ballot harvesting, defend election security, ensure accurate voter rolls, protect against fraud.

### 7️⃣ Border Security & Immigration
Conservative candidates support border wall, ending sanctuary policies, enforcing immigration laws, opposing amnesty, protecting American workers.

### 8️⃣ Economic Freedom & Limited Government
Republicans support lower taxes, reduced regulations, free market principles, fiscal responsibility, oppose socialist policies, defend small businesses from high taxes.

---

## 📅 Important Dates

- **Voter Registration Deadline**: 21 days before election
- **Absentee Ballot Request Deadline**: 7 days before election
- **Early Voting**: Available before Election Day
- **Primary Election**: June 2, 2026
- **General Election**: November 3, 2026

---

## 🗳️ How to Vote

1. **Register to Vote**: Visit [NJ Division of Elections](https://nj.gov/state/elections)
2. **Find Your Polling Location**: Check nj.gov/state/elections
3. **Request Mail-In Ballot**: If unable to vote in person
4. **Bring ID**: First-time voters may need ID

---

## 📞 Get Involved

- **Volunteer**: Contact New Jersey Republican Party when candidates announce
- **Donate**: Support conservative candidates once declared
- **Pray**: Lift up candidates, voters, and election integrity
- **Vote**: Participate in primary (June 2) and general election (Nov 3)

---

## 🔥 Why This Election Matters

New Jersey is a **competitive state** that has elected Republican governors. While Cory Booker is favored, a strong Republican nominee can make this race competitive and force Democrats to defend their record.

Booker has been a reliable vote for the Biden-Harris agenda, supporting radical abortion policies, open borders, high taxes, and big government spending. New Jersey voters deserve a senator who will fight for their values.

---

## 🙏 Pastoral Endorsements & IRS Guidance

**Pastors CAN endorse candidates from the pulpit.** The IRS allows churches to maintain tax-exempt status while pastors speak on political issues and endorse candidates **in their personal capacity**. Churches cannot make institutional endorsements or use church resources for campaigns, but pastoral speech is protected.

For guidance: [Alliance Defending Freedom - Pulpit Freedom](https://adflegal.org/pulpit-freedom)

---

**Vote for life. Vote for liberty. Vote for family values.**

🗳️ **Primary: June 2, 2026 | General: November 3, 2026** 🗳️

⚠️ **This guide will be updated as candidates officially declare their campaigns.**"""

ri_summary = """# 🗳️ Rhode Island 2026 Voter Guide

## 📊 Election Overview

**Primary Election**: September 8, 2026  
**General Election**: November 3, 2026

⚠️ **CANDIDATE UPDATE**: Republican candidates for the 2026 U.S. Senate and Governor races have not yet been officially declared. This guide will be updated as candidates announce their campaigns.

Rhode Island features a **U.S. Senate race** with incumbent Jack Reed (D) seeking re-election and a **Governor race** with incumbent Dan McKee (D) facing a Democratic primary challenge from Helena Foulkes.

---

## 🔴 Key Races

### U.S. Senate
**Incumbent**: Jack Reed (D) - Seeking re-election

**🔵 Democrat**:
- **Jack Reed** (Incumbent) - Long-serving senator, progressive voting record

**🔴 Republican Candidates**:
- **TBD** - Candidates have not yet declared

**Rating**: SAFE DEMOCRAT

### Governor
**Incumbent**: Dan McKee (D) - Seeking re-election

**🔵 Democrat Candidates**:
- **Dan McKee** (Incumbent) - Current Governor
- **Helena Foulkes** - Democratic primary challenger

**🔴 Republican Candidates**:
- **TBD** - Candidates have not yet declared

**Rating**: LIKELY DEMOCRAT

⚠️ **Note**: Republican candidates are expected to announce in early 2026. Check back for updates on the GOP primary fields.

---

## 🎯 8 Key Issues for Conservative Voters

### 1️⃣ Pro-Life Values
Rhode Island has minimal abortion restrictions. Conservative candidates will support protecting life, parental notification, informed consent laws, and conscience protections for healthcare workers.

### 2️⃣ School Choice & Parental Rights
Republicans support education freedom, school choice programs, charter schools, oppose CRT and gender ideology in schools, defend parental rights in education decisions.

### 3️⃣ Religious Liberty
Conservatives protect First Amendment rights, defend churches from government overreach, oppose mandates that violate conscience, support faith-based organizations.

### 4️⃣ Family Values & Parental Authority
Republican candidates oppose radical gender ideology, defend biological sex definitions, protect children from harmful procedures, support parental authority, defend traditional family values.

### 5️⃣ 2nd Amendment Rights
Conservatives defend gun rights, oppose gun control measures, protect concealed carry rights, defend against red flag laws, support constitutional carry.

### 6️⃣ Election Integrity
Republicans support voter ID requirements, oppose ballot harvesting, defend election security measures, ensure accurate voter rolls, protect against fraud.

### 7️⃣ Border Security & Immigration
Conservative candidates support completing border wall, ending sanctuary policies, enforcing immigration laws, opposing amnesty, protecting American workers.

### 8️⃣ Economic Freedom & Limited Government
Republicans support lower taxes, reduced regulations, free market principles, fiscal responsibility, oppose socialist policies, defend small businesses.

---

## 📅 Important Dates

- **Voter Registration Deadline**: 30 days before election (online), Election Day (in-person)
- **Absentee Ballot Request Deadline**: Contact local board of canvassers
- **Early Voting**: Available before Election Day
- **Primary Election**: September 8, 2026
- **General Election**: November 3, 2026

---

## 🗳️ How to Vote

1. **Register to Vote**: Visit [RI Board of Elections](https://vote.sos.ri.gov)
2. **Find Your Polling Location**: Check vote.sos.ri.gov
3. **Request Mail Ballot**: If unable to vote in person
4. **Bring ID**: Photo ID required for voting

---

## 📞 Get Involved

- **Volunteer**: Contact Rhode Island Republican Party when candidates announce
- **Donate**: Support conservative candidates once declared
- **Pray**: Lift up candidates, voters, and election integrity
- **Vote**: Participate in primary (Sept 8) and general election (Nov 3)

---

## 🔥 Why This Election Matters

While Rhode Island is a safe Democrat state, **every vote matters** for building conservative momentum and holding incumbents accountable. Jack Reed has been in the Senate since 1997, supporting progressive policies including radical abortion laws, open borders, and big government spending.

Dan McKee faces a Democratic primary challenge, showing vulnerability. A strong Republican nominee can compete in the general election and force Democrats to defend their record.

---

## 🙏 Pastoral Endorsements & IRS Guidance

**Pastors CAN endorse candidates from the pulpit.** The IRS allows churches to maintain tax-exempt status while pastors speak on political issues and endorse candidates **in their personal capacity**. Churches cannot make institutional endorsements or use church resources for campaigns, but pastoral speech is protected.

For guidance: [Alliance Defending Freedom - Pulpit Freedom](https://adflegal.org/pulpit-freedom)

---

**Vote for life. Vote for liberty. Vote for family values.**

🗳️ **Primary: September 8, 2026 | General: November 3, 2026** 🗳️

⚠️ **This guide will be updated as candidates officially declare their campaigns.**"""

print("Uploading state summaries...")

summaries_table.put_item(Item={
    'state': 'Delaware',
    'title': 'Delaware 2026 Voter Guide',
    'content': de_summary,
    'updated_at': '2025-01-XX'
})
print(f"Delaware: {len(de_summary)} characters")

summaries_table.put_item(Item={
    'state': 'New Jersey',
    'title': 'New Jersey 2026 Voter Guide',
    'content': nj_summary,
    'updated_at': '2025-01-XX'
})
print(f"New Jersey: {len(nj_summary)} characters")

summaries_table.put_item(Item={
    'state': 'Rhode Island',
    'title': 'Rhode Island 2026 Voter Guide',
    'content': ri_summary,
    'updated_at': '2025-01-XX'
})
print(f"Rhode Island: {len(ri_summary)} characters")

print("\n" + "="*60)
print("SUMMARIES UPLOADED SUCCESSFULLY")
print("="*60)
