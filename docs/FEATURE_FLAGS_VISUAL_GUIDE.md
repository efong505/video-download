# Feature Flags - User Experience Guide

## Visual Guide: What Users See

### Scenario 1: Election Feature ENABLED ✅

#### Homepage (index.html)
```
┌─────────────────────────────────────────────────────────┐
│  ✅ Election Coverage is Active (15 volunteers)         │
│                                                          │
│  🗳️ Election Tracking System                           │
│                                                          │
│  Tracking races in all 50 states thanks to our 15       │
│  volunteer correspondents!                               │
│                                                          │
│  [View Election Map]                                     │
└─────────────────────────────────────────────────────────┘
```

#### Navigation Bar
```
Home | Videos | Articles | News | Resources | 🗳️ Election Map | Login
                                              ↑
                                         VISIBLE
```

#### Election Map Page (election-map.html)
```
┌─────────────────────────────────────────────────────────┐
│  🗺️ Christian Conservative Election Map                 │
│  Find Pro-Life, Pro-Family, Pro-Freedom Candidates      │
│                                                          │
│  [Interactive US Map]                                    │
│  [State Details]                                         │
│  [Candidate Profiles]                                    │
│                                                          │
│  NO BANNERS - Full Access                               │
└─────────────────────────────────────────────────────────┘
```

---

### Scenario 2: Election Feature DISABLED - Public User ⚠️

#### Homepage (index.html)
```
┌─────────────────────────────────────────────────────────┐
│  ⚠️ Election Coverage is Currently Inactive             │
│                                                          │
│  🗳️ Election Tracking System                           │
│  [Seasonal - Currently Inactive]                         │
│                                                          │
│  Between election cycles                                 │
│                                                          │
│  Our election tracking returns during active election    │
│  cycles with volunteer support.                          │
│                                                          │
│  Next activation: January 2027                           │
│                                                          │
│  [Volunteer to Help Maintain This Feature]              │
└─────────────────────────────────────────────────────────┘
```

#### Navigation Bar
```
Home | Videos | Articles | News | Resources | Login
                                              ↑
                                    NO ELECTION LINK
```

#### Election Map Page (election-map.html)
```
┌─────────────────────────────────────────────────────────┐
│  [Alert Dialog]                                          │
│                                                          │
│  This feature is currently unavailable.                  │
│                                                          │
│  [OK]                                                    │
│                                                          │
│  → Redirects to index.html                              │
└─────────────────────────────────────────────────────────┘
```

---

### Scenario 3: Election Feature DISABLED - Admin User 🔧

#### Homepage (index.html)
```
┌─────────────────────────────────────────────────────────┐
│  ⚠️ Election Coverage is Currently Inactive             │
│                                                          │
│  🗳️ Election Tracking System                           │
│  [Seasonal - Currently Inactive]                         │
│                                                          │
│  Between election cycles                                 │
│                                                          │
│  Our election tracking returns during active election    │
│  cycles with volunteer support.                          │
│                                                          │
│  Next activation: January 2027                           │
│                                                          │
│  [Volunteer to Help Maintain This Feature]              │
└─────────────────────────────────────────────────────────┘
```

#### Navigation Bar
```
Home | Videos | Articles | News | Resources | 🗳️ Election Map [Preview] | Admin
                                              ↑
                                    VISIBLE WITH BADGE
```

#### Election Map Page (election-map.html)
```
┌─────────────────────────────────────────────────────────┐
│  ⚠️ Admin Preview Mode                                  │
│  This feature is currently disabled for public users.    │
│  You're viewing it as an administrator.                  │
│  [Manage Feature Flags]                                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  🗺️ Christian Conservative Election Map                 │
│  Find Pro-Life, Pro-Family, Pro-Freedom Candidates      │
│                                                          │
│  [Interactive US Map]                                    │
│  [State Details]                                         │
│  [Candidate Profiles]                                    │
│                                                          │
│  FULL ACCESS - Can develop and test                     │
└─────────────────────────────────────────────────────────┘
```

---

## Admin Interface (admin-feature-flags.html)

### Feature List View
```
┌─────────────────────────────────────────────────────────────────┐
│  🚩 Feature Flags Management                [+ Create] [Back]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Election Tracking System  [✅ Enabled] [Seasonal] [👥]     │ │
│  │                                                             │ │
│  │ 50-state election coverage with candidates, races, and     │ │
│  │ voter guides. Seasonal feature active during election      │ │
│  │ cycles.                                                     │ │
│  │                                                             │ │
│  │ Feature ID: election_system                                │ │
│  │ Season: Jan 1, 2025 - Nov 30, 2026                        │ │
│  │                                                             │ │
│  │ Active Volunteers: 15 / 10 required                        │ │
│  │ [████████████████████] 150%                                │ │
│  │                                                             │ │
│  │ Last updated: Jan 15, 2025 by super@admin.com             │ │
│  │                                                             │ │
│  │ [Disable] [Edit] [Delete]                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Edit Feature Modal
```
┌─────────────────────────────────────────────────────────┐
│  Edit Feature Flag                                  [X]  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Feature ID: election_system (read-only)                │
│                                                          │
│  Feature Name: Election Tracking System                 │
│                                                          │
│  Description:                                            │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 50-state election coverage with candidates...      │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  [✓] Enabled - Feature visible to users                │
│  [✓] Admin Only Access - Admins can access when off    │
│                                                          │
│  [✓] Seasonal Feature                                   │
│  [✓] Volunteer Dependent                                │
│                                                          │
│  ┌─ Seasonal Settings ─────────────────────────────┐   │
│  │ Season Start: 2025-01-01 00:00                  │   │
│  │ Season End:   2026-11-30 23:59                  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  ┌─ Volunteer Settings ────────────────────────────┐   │
│  │ Min Volunteers: 10                              │   │
│  │ Signup URL: /apply-correspondent.html           │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
│  Disable Reason: Between election cycles                │
│                                                          │
│  [Cancel] [Save Feature Flag]                           │
└─────────────────────────────────────────────────────────┘
```

---

## Volunteer Progress Indicators

### When Below Threshold (5/10 volunteers)
```
Active Volunteers: 5 / 10 required
[██████░░░░░░░░░░░░░░] 50%
         ↑
    RED PROGRESS BAR
```

### When At Threshold (10/10 volunteers)
```
Active Volunteers: 10 / 10 required
[████████████████████] 100%
         ↑
   YELLOW PROGRESS BAR
```

### When Above Threshold (15/10 volunteers)
```
Active Volunteers: 15 / 10 required
[████████████████████] 150%
         ↑
   GREEN PROGRESS BAR
```

---

## Status Messages by Scenario

### Feature Enabled + Sufficient Volunteers
```
✅ Election Coverage is active (15 volunteers)
Tracking races in all 50 states thanks to our volunteer correspondents!
```

### Feature Disabled + In Season
```
⚠️ Election Coverage is currently inactive: Between election cycles
Our election tracking returns during active election cycles with volunteer support.
Next activation: 2027 election cycle
```

### Feature Disabled + Out of Season
```
⚠️ Election Coverage is currently inactive: Off-season
Our election tracking returns during active election cycles.
Next activation: January 2027
```

### Feature Disabled + Low Volunteers
```
⚠️ Election Coverage is currently inactive: Seeking volunteers
We need 5 more volunteers to reactivate this feature.
[Volunteer to Help Maintain This Feature]
```

---

## Toggle Workflow

### Disabling a Feature
```
1. Admin visits admin-feature-flags.html
2. Finds "Election Tracking System"
3. Clicks [Disable] button
4. Confirms action
5. Optionally updates "Disable Reason"
6. Feature immediately hidden from public
7. Admins can still access with preview banner
```

### Re-enabling a Feature
```
1. Admin visits admin-feature-flags.html
2. Finds "Election Tracking System"
3. Clicks [Enable] button
4. Confirms action
5. Feature immediately visible to all users
6. No preview banners shown
```

---

## Color Coding

### Status Badges
- **Green** (Enabled): Feature is active and available
- **Red** (Disabled): Feature is inactive
- **Yellow** (Seasonal): Feature is seasonal/volunteer-dependent
- **Blue** (Volunteer): Feature requires volunteer support

### Progress Bars
- **Red** (0-49%): Below minimum threshold
- **Yellow** (50-99%): At or near threshold
- **Green** (100%+): Above threshold

### Alert Boxes
- **Green** (Success): Feature is active
- **Yellow** (Warning): Feature is inactive but will return
- **Red** (Danger): Feature is unavailable

---

## Summary

This visual guide shows exactly what users will see in each scenario:

✅ **Enabled**: Full access for everyone, green status cards
⚠️ **Disabled (Public)**: Hidden links, yellow status cards, volunteer recruitment
🔧 **Disabled (Admin)**: Preview access, warning banners, full functionality

The system provides clear communication to users about feature availability while allowing admins to continue development privately.
