# Feature Flags System

A complete feature flag system for enabling/disabling platform features (like the election system) without code deployment, with support for seasonal features and volunteer tracking.

## Quick Links

📚 **Documentation** (all in `docs/` folder):
- **[Implementation Summary](docs/FEATURE_FLAGS_IMPLEMENTATION_SUMMARY.md)** - Start here! Complete overview
- **[Complete Guide](docs/FEATURE_FLAGS_GUIDE.md)** - Full documentation (500+ lines)
- **[Quick Start](docs/FEATURE_FLAGS_QUICK_START.md)** - Copy-paste code examples
- **[Visual Guide](docs/FEATURE_FLAGS_VISUAL_GUIDE.md)** - What users will see
- **[Deployment Checklist](docs/FEATURE_FLAGS_DEPLOYMENT_CHECKLIST.md)** - Step-by-step deployment

## Files Created

### Backend
- `feature_flags_api/index.py` - Lambda function
- `create_feature_flags_table.py` - DynamoDB setup
- `deploy-feature-flags-api.ps1` - Deployment script

### Frontend
- `admin-feature-flags.html` - Admin interface
- `feature-flags.js` - Helper library

## Quick Start (30 minutes)

1. **Deploy Backend**
   ```bash
   python create_feature_flags_table.py
   .\deploy-feature-flags-api.ps1
   ```

2. **Create API Gateway** (AWS Console)
   - Copy the API Gateway URL

3. **Update Frontend**
   - Replace `YOUR_API_GATEWAY_URL` in `feature-flags.js` and `admin-feature-flags.html`

4. **Upload to S3**
   ```bash
   aws s3 cp admin-feature-flags.html s3://your-bucket/
   aws s3 cp feature-flags.js s3://your-bucket/
   ```

5. **Integrate into Pages**
   - See `docs/FEATURE_FLAGS_QUICK_START.md` for code snippets

## What It Does

### When Election Feature is ENABLED:
✅ Public users see "Election Map" link  
✅ Full access to election pages  
✅ Green "Active" status on homepage  

### When Election Feature is DISABLED:
❌ Public users: Link hidden, redirects to homepage  
✅ Admins: Full access with "Preview" banner  
⚠️ Shows volunteer recruitment message  

## Key Features

- **Seasonal Support** - Set election season dates
- **Volunteer Tracking** - Automatic count from contributors table
- **Admin Preview** - Work on disabled features privately
- **Public Messaging** - Clear status with volunteer recruitment
- **Easy Toggle** - No code deployment needed

## Documentation

All documentation is in the `docs/` folder. Start with:
👉 **[docs/FEATURE_FLAGS_IMPLEMENTATION_SUMMARY.md](docs/FEATURE_FLAGS_IMPLEMENTATION_SUMMARY.md)**

---

**Status**: ✅ Ready for Deployment  
**Setup Time**: ~30 minutes  
**Created**: January 2025
