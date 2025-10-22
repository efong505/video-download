import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

# LOUISIANA
la_summary = """# 🗳️ Louisiana 2025-2026 Christian Conservative Voter Guide

## 📊 Overview: Bayou State - Safe Senate Hold

Louisiana is **DEEP RED STATE** with Senator John Kennedy seeking re-election. Trump won Louisiana by 18 points in 2020. Kennedy is safe hold for Senate majority. Strong pro-life, pro-gun, pro-family conservative culture.

**Why Louisiana Matters:**
- 🔴 **Senate Hold**: Kennedy must win for Senate control
- 🎯 **Trump +18 State**: Solid Republican advantage
- 🗳️ **Conservative Values**: Pro-life, pro-gun, pro-family
- 🔥 **Senate Control**: Every seat matters

---

## 🔥 Top Priority: U.S. Senate

**John Kennedy (R)** ⭐⭐⭐⭐⭐ - Incumbent Senator
- Former State Treasurer, strong conservative
- 100% pro-life, A-rating NRA
- Fiscal conservative, defender of Louisiana values

---

## 🙏 8 Key Issues

### 1️⃣ PRO-LIFE ✝️
- Louisiana has strong pro-life laws
- Kennedy votes 100% pro-life in Senate

### 2️⃣ SCHOOL CHOICE 📚
- Expanding educational freedom
- Parental rights protected

### 3️⃣ RELIGIOUS LIBERTY 🙏
- Strong faith protections
- Pastors CAN endorse candidates (IRS permits)

### 4️⃣ FAMILY VALUES 👨👩👧👦
- Traditional values upheld
- Parental rights defended

### 5️⃣ 2ND AMENDMENT 🔫
- Constitutional carry
- Kennedy A-rating from NRA

### 6️⃣ ELECTION INTEGRITY 🗳️
- Voter ID required
- Clean voter rolls

### 7️⃣ BORDER SECURITY 🛡️
- Kennedy votes for border security
- Stop fentanyl crisis

### 8️⃣ ECONOMIC FREEDOM 💼
- Energy jobs (oil & gas)
- Lower taxes, pro-business

---

## 📅 Important Dates
- **Election Day:** November 3, 2026
- **Register:** [sos.la.gov](https://sos.la.gov)

---

## 🎯 Action Plan
1. ✅ Support John Kennedy
2. ✅ Vote November 3, 2026
3. ✅ Pray for Louisiana

---

*Louisiana Christians: Re-elect John Kennedy for Senate majority.*
"""

# TENNESSEE
tn_summary = """# 🗳️ Tennessee 2025-2026 Christian Conservative Voter Guide

## 📊 Overview: Volunteer State - Safe Senate Hold

Tennessee is **DEEP RED STATE** with Senator Bill Hagerty seeking re-election. Trump won Tennessee by 23 points in 2020. Hagerty is safe hold for Senate majority. Strong pro-life, pro-gun, pro-family conservative culture.

**Why Tennessee Matters:**
- 🔴 **Senate Hold**: Hagerty must win for Senate control
- 🎯 **Trump +23 State**: Solid Republican advantage
- 🗳️ **Conservative Values**: Pro-life, pro-gun, pro-family
- 🔥 **Senate Control**: Every seat matters

---

## 🔥 Top Priority: U.S. Senate

**Bill Hagerty (R)** ⭐⭐⭐⭐⭐ - Incumbent Senator
- Former Ambassador to Japan, businessman
- 100% pro-life, A-rating NRA
- Pro-business, fiscal conservative

---

## 🙏 8 Key Issues

### 1️⃣ PRO-LIFE ✝️
- Tennessee has strong pro-life laws
- Hagerty votes 100% pro-life in Senate

### 2️⃣ SCHOOL CHOICE 📚
- Expanding educational freedom
- Parental rights protected

### 3️⃣ RELIGIOUS LIBERTY 🙏
- Strong faith protections
- Pastors CAN endorse candidates (IRS permits)

### 4️⃣ FAMILY VALUES 👨👩👧👦
- Traditional values upheld
- Parental rights defended

### 5️⃣ 2ND AMENDMENT 🔫
- Constitutional carry
- Hagerty A-rating from NRA

### 6️⃣ ELECTION INTEGRITY 🗳️
- Voter ID required
- Clean voter rolls

### 7️⃣ BORDER SECURITY 🛡️
- Hagerty votes for border security
- Stop fentanyl crisis

### 8️⃣ ECONOMIC FREEDOM 💼
- Pro-business policies
- Lower taxes, job growth

---

## 📅 Important Dates
- **Election Day:** November 3, 2026
- **Register:** [sos.tn.gov](https://sos.tn.gov)

---

## 🎯 Action Plan
1. ✅ Support Bill Hagerty
2. ✅ Vote November 3, 2026
3. ✅ Pray for Tennessee

---

*Tennessee Christians: Re-elect Bill Hagerty for Senate majority.*
"""

# OKLAHOMA
ok_summary = """# 🗳️ Oklahoma 2025-2026 Christian Conservative Voter Guide

## 📊 Overview: Sooner State - Safe Senate Hold

Oklahoma is **DEEP RED STATE** with Senator James Lankford seeking re-election. Trump won Oklahoma by 33 points in 2020. Lankford is safe hold for Senate majority. Former Baptist youth minister with strong conservative record.

**Why Oklahoma Matters:**
- 🔴 **Senate Hold**: Lankford must win for Senate control
- 🎯 **Trump +33 State**: Solid Republican advantage
- 🗳️ **Conservative Values**: Pro-life, pro-gun, pro-family
- 🔥 **Senate Control**: Every seat matters

---

## 🔥 Top Priority: U.S. Senate

**James Lankford (R)** ⭐⭐⭐⭐⭐ - Incumbent Senator
- Former Baptist youth minister
- 100% pro-life, A-rating NRA
- Strong defender of religious liberty

---

## 🔥 Governor Race

**Kevin Stitt (R)** ⭐⭐⭐⭐⭐ - Incumbent Governor
- Businessman, strong conservative
- Pro-life, school choice champion
- A-rating from NRA

---

## 🙏 8 Key Issues

### 1️⃣ PRO-LIFE ✝️
- Oklahoma has strong pro-life laws
- Lankford votes 100% pro-life
- Stitt signed pro-life legislation

### 2️⃣ SCHOOL CHOICE 📚
- Stitt championing school choice
- Parental rights protected

### 3️⃣ RELIGIOUS LIBERTY 🙏
- Lankford former minister, strong defender
- Pastors CAN endorse candidates (IRS permits)

### 4️⃣ FAMILY VALUES 👨👩👧👦
- Traditional values upheld
- Parental rights defended

### 5️⃣ 2ND AMENDMENT 🔫
- Constitutional carry
- Lankford & Stitt A-rating from NRA

### 6️⃣ ELECTION INTEGRITY 🗳️
- Voter ID required
- Clean voter rolls

### 7️⃣ BORDER SECURITY 🛡️
- Lankford votes for border security
- Stop fentanyl crisis

### 8️⃣ ECONOMIC FREEDOM 💼
- Energy jobs (oil & gas)
- Lower taxes, pro-business

---

## 📅 Important Dates
- **Election Day:** November 3, 2026
- **Register:** [ok.gov/elections](https://ok.gov/elections)

---

## 🎯 Action Plan
1. ✅ Support James Lankford (Senate)
2. ✅ Support Kevin Stitt (Governor)
3. ✅ Vote November 3, 2026
4. ✅ Pray for Oklahoma

---

*Oklahoma Christians: Re-elect Lankford and Stitt for conservative leadership.*
"""

# Upload all three
print("Uploading Louisiana summary...")
summaries_table.put_item(Item={"state": "Louisiana", "title": "Louisiana 2025-2026 Elections - Christian Conservatives Today Guide", "election_year": "2025-2026", "content": la_summary, "last_updated": datetime.utcnow().isoformat(), "updated_by": "system"})
print(f"[SUCCESS] Louisiana: {len(la_summary)} characters")

print("\nUploading Tennessee summary...")
summaries_table.put_item(Item={"state": "Tennessee", "title": "Tennessee 2025-2026 Elections - Christian Conservatives Today Guide", "election_year": "2025-2026", "content": tn_summary, "last_updated": datetime.utcnow().isoformat(), "updated_by": "system"})
print(f"[SUCCESS] Tennessee: {len(tn_summary)} characters")

print("\nUploading Oklahoma summary...")
summaries_table.put_item(Item={"state": "Oklahoma", "title": "Oklahoma 2025-2026 Elections - Christian Conservatives Today Guide", "election_year": "2025-2026", "content": ok_summary, "last_updated": datetime.utcnow().isoformat(), "updated_by": "system"})
print(f"[SUCCESS] Oklahoma: {len(ok_summary)} characters")

print("\n[SUCCESS] All three summaries uploaded!")
