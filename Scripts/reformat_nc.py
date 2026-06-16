import boto3

db=boto3.resource("dynamodb",region_name="us-east-1")
t=db.Table("state-summaries")
r=t.get_item(Key={"state":"North Carolina"})
c=r["Item"]["content"]

header="""# North Carolina 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 21 races across North Carolina
**Total Candidates Profiled:** 25+ major candidates
**Election Dates:**
- March 3, 2026 (Primary Election)
- May 12, 2026 (Primary Runoff)
- November 3, 2026 (General Election)

**Guide Length:** Comprehensive 20-30 page Christian conservative voter guide
**Focus Areas:** Pro-life, School Choice, Religious Liberty, Family Values, 2nd Amendment, Election Integrity, Border Security, Economic Freedom

---

## 🔴 NORTH CAROLINA POLITICAL LANDSCAPE

### **The Tar Heel State**

North Carolina is a **CRITICAL BATTLEGROUND**:

- **Open Senate Seat:** Sen. Thom Tillis retiring creates TOP PICKUP OPPORTUNITY
- **School Choice Leader:** 99,000 students in Opportunity Scholarship Program
- **Pro-Life Progress:** 12-week abortion limit enacted 2023
- **Parental Rights:** Strong GOP legislature advancing family values
- **Election Integrity:** Voter ID required, no ballot harvesting

---

"""

bottom="""

## 🔥 BOTTOM LINE FOR NORTH CAROLINA CHRISTIANS

**2026 Elections Matter:**
- Open Senate seat determines Senate control
- Supreme Court balance affects pro-life laws
- School choice expansion at stake
- Religious liberty protections critical

**If Conservatives Win:**

✅ Protect 12-week abortion limit
✅ Expand school choice to 150K students
✅ Defend religious liberty for churches
✅ Uphold parental rights in education
✅ Maintain constitutional carry
✅ Secure election integrity
✅ Block sanctuary policies
✅ Keep taxes low (5.25% flat)

**If Progressives Win:**

❌ Repeal 12-week abortion limit
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

t.put_item(Item={"state":"North Carolina","title":"North Carolina 2026 Voter Guide","content":c,"updated_at":"2025-01-22"})
print(f"NC reformatted: {len(c):,} chars")