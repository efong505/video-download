# Dashboard Update - Name Management

## Changes Made:

### API (dashboard_api.py):
- Added `POST /api/subscribers` - Manually add subscriber
- Added `PUT /api/subscribers/<email>` - Edit subscriber names
- Added `DELETE /api/subscribers/<email>` - Delete subscriber

### Dashboard (dashboard_simple.html):
- Added "Name" column to subscriber table
- Added "Add New Subscriber" form with first/last name fields
- Added "Edit" button to update names
- Added "Delete" button to remove subscribers
- Updated search to include names
- Updated CSV export to include names

## To Apply Changes:

1. Restart dashboard API:
```powershell
cd "c:\Users\Ed\Documents\Programming\AWS\Downloader\Election Data and Files\Email and Tracking"
python dashboard_api.py
```

2. Refresh dashboard in browser

## New Features:
- ✅ Display first/last names in table
- ✅ Add subscribers manually with names
- ✅ Edit existing subscriber names
- ✅ Delete subscribers permanently
- ✅ Names shown in detail modal
