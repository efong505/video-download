import boto3

db=boto3.resource("dynamodb",region_name="us-east-1")
t=db.Table("state-summaries")
r=t.get_item(Key={"state":"New Hampshire"})
c=r["Item"]["content"]

header="""# New Hampshire 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 4 major races across New Hampshire
**Total Candidates Profiled:** 15+ major candidates
**Election Dates:**
- September 8, 2026 (Primary Election)
- November 3, 2026 (General Election)

**Guide Length:** Comprehensive 20-30 page Christian conservative voter guide
**Focus Areas:** Pro-life, School Choice, Religious Liberty, Family Values, 2nd Amendment, Election Integrity, Border Security, Economic Freedom

---

## 🔴 NEW HAMPSHIRE POLITICAL LANDSCAPE

### **The Granite State**

New Hampshire is a **TOSS-UP BATTLEGROUND**:

- **Open Senate Seat:** Sen. Shaheen retiring, first open seat since 2010
- **School Choice Explosion:** EFAs for all 180K students, income caps removed
- **Pro-Life Push:** 24-week limit, GOP pushing 15-week ban
- **Religious Liberty:** Strong protections, high on 20 metrics
- **Constitutional Carry:** Permitless carry since 2021

---

"""

bottom="""

## 🔥 BOTTOM LINE FOR NEW HAMPSHIRE CHRISTIANS

**2026 Elections Matter:**
- Open Senate seat determines chamber control
- Governor race shapes school choice future
- Pro-life restrictions at stake
- Religious liberty protections critical

**If Conservatives Win:**

✅ Flip Senate seat, secure majority
✅ Enact 15-week abortion ban
✅ Expand EFAs to 20K+ students
✅ Defend religious liberty for churches
✅ Uphold parental rights in education
✅ Maintain constitutional carry
✅ Secure election integrity
✅ Block sanctuary policies
✅ Keep no income/sales tax

**If Progressives Win:**

❌ Lose Senate seat, Democrat control
❌ Block pro-life restrictions
❌ Cap school choice programs
❌ Threaten faith-based organizations
❌ Push gender ideology in schools
❌ Add red flag gun laws
❌ Weaken voter ID requirements
❌ Create sanctuary policies
❌ Impose new taxes

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

t.put_item(Item={"state":"New Hampshire","title":"New Hampshire 2026 Voter Guide","content":c,"updated_at":"2025-01-22"})
print(f"NH reformatted: {len(c):,} chars")