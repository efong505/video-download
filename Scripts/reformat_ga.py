import boto3

db=boto3.resource("dynamodb",region_name="us-east-1")
t=db.Table("state-summaries")
r=t.get_item(Key={"state":"Georgia"})
c=r["Item"]["content"]

header="""# Georgia 2025-2026 Elections - Complete Christian Conservatives Today Guide

## 📊 Database Summary

**Total Races Documented:** 28 races across Georgia
**Total Candidates Profiled:** 30+ major candidates
**Election Dates:**
- May 19, 2026 (Primary Election)
- June 16, 2026 (Primary Runoff)
- November 3, 2026 (General Election)
- December 1, 2026 (General Runoff if needed)

**Guide Length:** Comprehensive 20-30 page Christian conservative voter guide
**Focus Areas:** Pro-life, School Choice, Religious Liberty, Family Values, 2nd Amendment, Election Integrity, Border Security, Economic Freedom

---

## 🔴 GEORGIA POLITICAL LANDSCAPE

### **The Peach State**

Georgia is a **TOSS-UP BATTLEGROUND**:

- **Senate Toss-Up:** Jon Ossoff vulnerable, GOP strong challengers
- **Open Governor:** Brian Kemp term-limited, crowded GOP field
- **Heartbeat Law:** 6-week abortion ban in legal limbo
- **Election Integrity:** 2020/2022 controversies, ongoing reforms
- **School Choice:** QB1 vouchers expanding under GOP

---

"""

bottom="""

## 🔥 BOTTOM LINE FOR GEORGIA CHRISTIANS

**2026 Elections Matter:**
- Senate toss-up determines chamber control
- Open Governor seat shapes state direction
- Heartbeat law defense critical
- School choice expansion at stake

**If Conservatives Win:**

✅ Flip Senate seat, secure majority
✅ Defend heartbeat law in courts
✅ Expand QB1 vouchers to 50K students
✅ Protect religious liberty for churches
✅ Uphold parental rights in education
✅ Maintain constitutional carry
✅ Strengthen election integrity
✅ Block sanctuary policies
✅ Keep taxes low (5.75% flat)

**If Progressives Win:**

❌ Lose Senate seat, Democrat control
❌ Repeal heartbeat law protections
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

t.put_item(Item={"state":"Georgia","title":"Georgia 2026 Voter Guide","content":c,"updated_at":"2025-01-22"})
print(f"GA reformatted: {len(c):,} chars")