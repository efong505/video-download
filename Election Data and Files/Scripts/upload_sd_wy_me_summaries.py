import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
summaries_table = dynamodb.Table('state-summaries')

sd_summary = """# 🗳️ South Dakota 2025-2026 Christian Conservative Voter Guide

## 📊 Overview: Mount Rushmore State - Safe Senate Hold

South Dakota is **DEEP RED STATE** with Senator Mike Rounds and Governor Kristi Noem seeking re-election. Trump won South Dakota by 26 points in 2020. Both are safe holds for conservative leadership.

**Why South Dakota Matters:**
- 🔴 **Senate Hold**: Rounds must win for Senate control
- 🎯 **Trump +26 State**: Solid Republican advantage
- 🗳️ **Noem Leadership**: Strong conservative governor
- 🔥 **Senate Control**: Every seat matters

---

## 🔥 Top Priorities

**Mike Rounds (R)** ⭐⭐⭐⭐⭐ - U.S. Senator
- Former Governor, businessman
- 100% pro-life, A-rating NRA
- Fiscal conservative

**Kristi Noem (R)** ⭐⭐⭐⭐⭐ - Governor
- Former U.S. Representative
- Pro-life, school choice champion
- Strong conservative leader

---

## 🙏 8 Key Issues
1️⃣ PRO-LIFE: Strong pro-life laws, Rounds & Noem 100% pro-life
2️⃣ SCHOOL CHOICE: Expanding educational freedom
3️⃣ RELIGIOUS LIBERTY: Pastors CAN endorse (IRS permits)
4️⃣ FAMILY VALUES: Traditional values upheld
5️⃣ 2ND AMENDMENT: Constitutional carry, A-ratings
6️⃣ ELECTION INTEGRITY: Voter ID, clean rolls
7️⃣ BORDER SECURITY: Rounds votes for border security
8️⃣ ECONOMIC FREEDOM: Agriculture, lower taxes

---

## 📅 Election Day: November 3, 2026
Register: [sdsos.gov](https://sdsos.gov)

---

*South Dakota Christians: Re-elect Rounds and Noem for conservative leadership.*
"""

wy_summary = """# 🗳️ Wyoming 2025-2026 Christian Conservative Voter Guide

## 📊 Overview: Cowboy State - Safe Senate Hold

Wyoming is **DEEPEST RED STATE** with Senator John Barrasso and Governor Mark Gordon seeking re-election. Trump won Wyoming by 43 points in 2020 - his strongest margin. Both are safe holds.

**Why Wyoming Matters:**
- 🔴 **Senate Hold**: Barrasso must win for Senate control
- 🎯 **Trump +43 State**: Strongest Republican state
- 🗳️ **Energy Jobs**: Coal, oil, gas critical
- 🔥 **Senate Control**: Every seat matters

---

## 🔥 Top Priorities

**John Barrasso (R)** ⭐⭐⭐⭐⭐ - U.S. Senator
- Physician, Senate Republican leadership
- 100% pro-life, A-rating NRA
- Energy jobs champion

**Mark Gordon (R)** ⭐⭐⭐⭐⭐ - Governor
- Rancher, businessman
- Pro-life, pro-gun
- Energy and agriculture supporter

---

## 🙏 8 Key Issues
1️⃣ PRO-LIFE: Strong pro-life laws, Barrasso 100% pro-life
2️⃣ SCHOOL CHOICE: Parental rights protected
3️⃣ RELIGIOUS LIBERTY: Pastors CAN endorse (IRS permits)
4️⃣ FAMILY VALUES: Traditional values upheld
5️⃣ 2ND AMENDMENT: Constitutional carry, A-ratings
6️⃣ ELECTION INTEGRITY: Voter ID, clean rolls
7️⃣ BORDER SECURITY: Barrasso votes for border security
8️⃣ ECONOMIC FREEDOM: Energy jobs (coal, oil, gas), agriculture

---

## 📅 Election Day: November 3, 2026
Register: [sos.wyo.gov](https://sos.wyo.gov)

---

*Wyoming Christians: Re-elect Barrasso and Gordon for conservative leadership.*
"""

me_summary = """# 🗳️ Maine 2025-2026 Christian Conservative Voter Guide

## 📊 Overview: Pine Tree State - CRITICAL Senate Hold

Maine is **COMPETITIVE BATTLEGROUND** with Senator Susan Collins seeking re-election. Biden won Maine by 9 points in 2020. Collins is **MOST VULNERABLE REPUBLICAN SENATOR** - **MUST HOLD** for Senate majority.

**Why Maine Matters:**
- 🔴 **CRITICAL Senate Hold**: Collins most vulnerable R senator
- 🎯 **Biden +9 State**: Difficult but winnable
- 🗳️ **Senate Control**: This seat could determine majority
- 🔥 **Must Win**: Cannot lose Collins seat

---

## 🔥 #1 PRIORITY: U.S. Senate

**Susan Collins (R)** ⭐⭐⭐ - U.S. Senator (MUST HOLD)
- Moderate Republican since 1997
- Critical hold for Senate majority
- Votes with Republicans on judges
- **Rating**: MODERATE - But CRITICAL hold

**Why This Matters:**
Collins is moderate but votes for conservative judges and Senate control. Losing her seat = Democrat Senate majority = Biden agenda passes. **MUST HOLD** despite moderate record.

---

## 🙏 8 Key Issues
1️⃣ PRO-LIFE: Collins moderate, but better than Democrat
2️⃣ SCHOOL CHOICE: Supports parental rights
3️⃣ RELIGIOUS LIBERTY: Pastors CAN endorse (IRS permits)
4️⃣ FAMILY VALUES: Moderate positions
5️⃣ 2ND AMENDMENT: Moderate on guns
6️⃣ ELECTION INTEGRITY: Supports election security
7️⃣ BORDER SECURITY: Votes for border funding
8️⃣ ECONOMIC FREEDOM: Fiscal moderate

---

## 📅 Election Day: November 3, 2026
Register: [maine.gov/sos](https://maine.gov/sos)

---

## 🔥 Bottom Line

**Collins is moderate BUT this is MUST HOLD seat for Senate majority.**

If Collins loses:
❌ Democrat Senate majority
❌ Biden agenda passes
❌ Liberal judges confirmed
❌ Conservative agenda blocked

If Collins wins:
✅ Republican Senate majority
✅ Stop Biden agenda
✅ Confirm conservative judges
✅ Advance conservative priorities

**Every Maine conservative MUST vote for Collins despite moderate record. Senate control depends on it.**

---

*Maine Christians: Hold your nose if needed, but VOTE COLLINS. Senate majority depends on this seat.*
"""

print("Uploading South Dakota summary...")
summaries_table.put_item(Item={"state": "South Dakota", "title": "South Dakota 2025-2026 Elections - Christian Conservatives Today Guide", "election_year": "2025-2026", "content": sd_summary, "last_updated": datetime.utcnow().isoformat(), "updated_by": "system"})
print(f"[SUCCESS] South Dakota: {len(sd_summary)} characters")

print("\nUploading Wyoming summary...")
summaries_table.put_item(Item={"state": "Wyoming", "title": "Wyoming 2025-2026 Elections - Christian Conservatives Today Guide", "election_year": "2025-2026", "content": wy_summary, "last_updated": datetime.utcnow().isoformat(), "updated_by": "system"})
print(f"[SUCCESS] Wyoming: {len(wy_summary)} characters")

print("\nUploading Maine summary...")
summaries_table.put_item(Item={"state": "Maine", "title": "Maine 2025-2026 Elections - Christian Conservatives Today Guide", "election_year": "2025-2026", "content": me_summary, "last_updated": datetime.utcnow().isoformat(), "updated_by": "system"})
print(f"[SUCCESS] Maine: {len(me_summary)} characters")

print("\n[SUCCESS] All three summaries uploaded!")
