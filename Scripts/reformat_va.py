import boto3

db=boto3.resource("dynamodb",region_name="us-east-1")
t=db.Table("state-summaries")
r=t.get_item(Key={"state":"Virginia"})
c=r["Item"]["content"]

header="""# Virginia 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 17 races across Virginia
**Total Candidates Profiled:** 20+ major candidates
**Election Dates:**
- November 4, 2025 (Governor, Lt Gov, AG, House of Delegates)
- November 3, 2026 (U.S. Senate, U.S. House)

**Guide Length:** Comprehensive 20-30 page Christian conservative voter guide
**Focus Areas:** Pro-life, School Choice, Religious Liberty, Family Values, 2nd Amendment, Election Integrity, Border Security, Economic Freedom

---

## 🔴 VIRGINIA POLITICAL LANDSCAPE

### **The Old Dominion**

Virginia is a **COMPETITIVE BATTLEGROUND**:

- **2025 Governor Toss-Up:** Earle-Sears vs Spanberger
- **Parental Rights Leader:** Youngkin legacy, school choice expansion
- **Pro-Life Battles:** HJ 1 amendment threatens 15-week limit
- **Religious Liberty:** Strong protections, AG Miyares defending
- **School Choice:** $7,500 vouchers for 5K students, expanding

---

"""

bottom="""

## 🔥 BOTTOM LINE FOR VIRGINIA CHRISTIANS

**2025-2026 Elections Matter:**
- Governor race shapes parental rights future
- HJ 1 amendment threatens pro-life laws
- School choice expansion at stake
- Religious liberty protections critical

**If Conservatives Win:**

✅ Block HJ 1 abortion amendment
✅ Expand school vouchers to 50K students
✅ Defend religious liberty for churches
✅ Uphold parental rights in education
✅ Maintain permitless carry
✅ Secure election integrity
✅ Block sanctuary policies
✅ Keep taxes low (5.75% top rate)

**If Progressives Win:**

❌ Pass HJ 1 unlimited abortion
❌ Gut school choice programs
❌ Threaten faith-based organizations
❌ Push gender ideology in schools
❌ Add red flag gun laws
❌ Weaken voter ID requirements
❌ Create sanctuary policies
❌ Raise taxes for equity

**THE CHOICE IS CLEAR. VOTE CONSERVATIVE.**

---
"""

if "Database Summary" not in c:
    idx=c.find("State-Specific Context")
    if idx>0:
        c=header+c[idx:]
if "BOTTOM LINE" not in c:
    idx=c.find("Detailed Resources")
    if idx>0:
        c=c[:idx]+bottom+c[idx:]

t.put_item(Item={"state":"Virginia","title":"Virginia 2026 Voter Guide","content":c,"updated_at":"2025-01-22"})
print(f"VA reformatted: {len(c):,} chars")