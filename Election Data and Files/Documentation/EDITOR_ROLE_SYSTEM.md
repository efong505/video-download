# Editor/Contributor Role System

## Overview

The platform now supports three user roles with different permission levels:

1. **Super User / Admin** - Full access to create, edit, delete all data
2. **Editor** - Can create and edit races/candidates for their assigned state(s), requires approval
3. **Regular User** - Read-only access

## How It Works

### Editor Permissions

When a user is added as a **contributor** for a state:
- They gain **editor** role for that specific state
- Can create new candidates and races for their state
- Can edit existing candidates and races for their state
- All changes go to **pending approval** queue
- Cannot make direct changes to live data

### Approval Workflow

1. **Editor submits change** → Stored in `pending-changes` table
2. **Admins notified** → Email sent to all admins/super users
3. **Admin reviews** → Views change in admin dashboard
4. **Admin approves/denies** → Change applied or rejected
5. **Editor notified** → (Future: email notification)

## Setting Up Editors

### 1. Create Pending Changes Table

```bash
python "Election Data and Files/Scripts/create_pending_changes_table.py"
```

### 2. Add Contributor as Editor

In `admin-contributors.html`:
- Add contributor with their email and state
- Set status to "active"
- They automatically become editor for that state

### 3. Assign Editor Role in Users Table

Run the script to assign editor role:
```bash
python "Election Data and Files/Scripts/assign_editor_role.py" editor@example.com
```

The user must already exist in the `users` table (they need to have registered/logged in at least once).

## Editor Workflow

### For Editors:

1. **Login** to admin dashboard with editor credentials
2. **Navigate** to Candidates or Races section
3. **Create/Edit** data for your assigned state
4. **Submit** - Change goes to pending queue
5. **Wait** for admin approval
6. **Notification** when approved/denied (future feature)

### For Admins:

1. **Receive email** when new change submitted
2. **Open** `admin-pending-changes.html`
3. **Review** change details
4. **Approve** or **Deny** with one click
5. **Change applied** immediately if approved

## API Endpoints

### Submit Change (Editors)
```
POST /contributors?resource=pending-changes
Body: {
  "change_type": "create_candidate",
  "data": { candidate data }
}
```

### List Pending Changes (Admins)
```
GET /contributors?resource=pending-changes
```

### Review Change (Admins)
```
PUT /contributors?resource=pending-changes
Body: {
  "change_id": "uuid",
  "action": "approve" | "deny"
}
```

## Change Types

- `create_candidate` - New candidate submission
- `update_candidate` - Edit existing candidate
- `create_race` - New race submission
- `update_race` - Edit existing race

## Database Schema

### pending-changes Table

```
{
  "change_id": "uuid",
  "change_type": "create_candidate",
  "data": { ... },
  "submitted_by": "editor@example.com",
  "submitted_at": "2024-01-15T10:30:00Z",
  "status": "pending" | "approved" | "denied",
  "state": "Texas",
  "reviewed_by": "admin@example.com",
  "reviewed_at": "2024-01-15T11:00:00Z"
}
```

## Security

- Editors can only submit changes for their assigned state(s)
- All changes require admin approval before going live
- Editors cannot delete data
- Editors cannot approve their own changes
- All changes tracked with submitter and reviewer info

## Notifications

### Current:
- Email sent to all admins when change submitted

### Future Enhancements:
- Email to editor when change approved/denied
- In-app notification system
- Slack/Discord integration
- Weekly digest of pending changes

## Benefits

1. **Scalability** - State correspondents can contribute without admin bottleneck
2. **Quality Control** - All changes reviewed before going live
3. **Accountability** - Full audit trail of who submitted/approved what
4. **Security** - Editors limited to their state, can't break other data
5. **Efficiency** - Admins focus on review, not data entry

## Future Features

- [ ] Bulk approve/deny
- [ ] Change comments/feedback
- [ ] Editor dashboard showing pending status
- [ ] Auto-approve trusted editors after X approved changes
- [ ] Change history/audit log
- [ ] Revert approved changes
- [ ] Editor performance metrics
