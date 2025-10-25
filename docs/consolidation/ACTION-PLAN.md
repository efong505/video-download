# CSS/JS Consolidation - Action Plan

## Current Status: Analysis Complete ✅

**Analysis Results:**
- 42 pages analyzed
- 333 unique CSS selectors found
- 58 common selectors (used in 3+ pages)
- 48 exact duplicate CSS rules
- **23.6% potential CSS reduction**

---

## Immediate Action Items

### ✅ COMPLETED
1. Created `audit-css-js.py` - External dependency analysis
2. Created `compare-inline-css.py` - Inline CSS comparison
3. Generated `CSS-JS-AUDIT-REPORT.md` - External dependencies report
4. Generated `CSS-INLINE-COMPARISON.md` - Inline CSS analysis

### 🎯 NEXT STEPS (In Order)

#### Step 1: Create Shared CSS File (THIS WEEK)
**File:** `css/common-styles.css`

**Include (High Priority - 50%+ usage):**
- `body` base styles (21 pages)

**Include (Medium Priority - 25-50% usage):**
- `.dashboard-header` (13 pages)
- `.nav-link` and `.nav-link:hover` (13 pages)
- `.nav-link.logout` and `.nav-link.logout:hover` (13 pages)
- `.dashboard-nav` (11 pages)
- `.nav-links` (11 pages)
- `.nav-brand` (9 pages)
- Media queries for responsive nav (11 pages)

**Estimated Impact:** Remove ~160 duplicate CSS rules across pages

#### Step 2: Create Shared Navigation CSS (THIS WEEK)
**File:** `css/nav-styles.css`

**Include:**
- All navigation-related styles (`.nav-*` classes)
- Dashboard header styles
- Mobile responsive breakpoints
- Logout button styles

**Pages to Update:** 13 pages (articles.html, videos.html, resources.html, etc.)

#### Step 3: Analyze JavaScript (NEXT WEEK)
**Create:** `compare-inline-js.py`
**Generate:** `JS-INLINE-COMPARISON.md`

**Look for:**
- Authentication logic (JWT handling)
- AWS SDK initialization
- Common utility functions
- API endpoint constants

#### Step 4: Create Shared JS Files (WEEK 3)
**Files to create:**
- `js/auth-handler.js` - JWT authentication
- `js/api-config.js` - API endpoints
- `js/common-utils.js` - Shared utilities

#### Step 5: Incremental Page Updates (WEEK 4-5)
**Update pages in batches:**
- Batch 1: Main pages (index, videos, articles, resources)
- Batch 2: Admin pages (admin, admin-templates, admin-resources)
- Batch 3: Article/News editors
- Batch 4: Remaining pages

---

## Detailed Implementation Plan

### Phase 1: Create common-styles.css

**Location:** `Downloader/css/common-styles.css`

**Contents:**
```css
/* Base body styles - used in 21 pages */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    background: #f5f5f5;
}

/* Dashboard header - used in 13 pages */
.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px 0;
    margin-bottom: 30px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* Navigation styles - used in 13 pages */
.nav-link {
    color: white;
    text-decoration: none;
    padding: 10px 20px;
    border-radius: 25px;
    background: rgba(255,255,255,0.1);
    transition: all 0.3s ease;
    border: 1px solid rgba(255,255,255,0.2);
}

.nav-link:hover {
    background: rgba(255,255,255,0.2);
    color: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.nav-link.logout {
    background: rgba(220,53,69,0.8);
    border-color: rgba(220,53,69,0.9);
}

.nav-link.logout:hover {
    background: rgba(220,53,69,1);
}

/* Dashboard navigation - used in 11 pages */
.dashboard-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
}

.nav-links {
    display: flex;
    gap: 20px;
    align-items: center;
    flex-wrap: wrap;
}

.nav-brand {
    font-size: 1.8rem;
    font-weight: bold;
    margin: 0;
}

/* Mobile responsive - used in 11 pages */
@media (max-width: 768px) {
    .nav-brand {
        font-size: 1.4rem;
    }
    .nav-links {
        gap: 8px;
        justify-content: center;
        width: 100%;
        margin-top: 10px;
    }
    .nav-link {
        padding: 6px 12px;
        font-size: 0.8rem;
        white-space: nowrap;
    }
    .dashboard-nav {
        justify-content: center;
        text-align: center;
    }
}

@media (max-width: 576px) {
    .nav-links {
        gap: 5px;
    }
    .nav-link {
        padding: 5px 8px;
        font-size: 0.75rem;
    }
    .nav-brand {
        font-size: 1.2rem;
    }
}

/* Android mobile fix */
@media (max-width: 422px) {
    .dashboard-header {
        padding-top: 80px;
    }
}
```

**Test Plan:**
1. Create the file
2. Update articles.html to use it
3. Test locally
4. Compare before/after
5. If successful, update other pages

### Phase 2: Update Pages to Use Shared CSS

**Template for updating pages:**

**BEFORE:**
```html
<style>
    .dashboard-header { ... }
    .nav-link { ... }
    /* etc */
</style>
```

**AFTER:**
```html
<link rel="stylesheet" href="css/common-styles.css">
<style>
    /* Only page-specific styles here */
</style>
```

**Pages to Update (Priority Order):**
1. articles.html
2. videos.html
3. resources.html
4. authors.html
5. create-article.html
6. edit-article.html
7. admin-templates.html
8. admin-resources.html
9. (Continue with remaining pages)

### Phase 3: JavaScript Analysis

**Create:** `docs/consolidation/compare-inline-js.py`

**Analyze for:**
- API endpoint constants (AUTH_API, ARTICLES_API, etc.)
- JWT token handling (localStorage.getItem('auth_token'))
- User authentication checks
- Common utility functions (logout, viewMyPage, etc.)
- AWS SDK initialization

**Expected findings:**
- API endpoints duplicated across 20+ pages
- Auth logic duplicated across 15+ pages
- Utility functions duplicated across 10+ pages

### Phase 4: Create Shared JS Files

**File 1: `js/api-config.js`**
```javascript
// API endpoint configuration
const API_ENDPOINTS = {
    AUTH: 'https://r6l0z3605f.execute-api.us-east-1.amazonaws.com/prod/auth',
    ARTICLES: 'https://fr3hh94h4a.execute-api.us-east-1.amazonaws.com/prod/articles',
    NEWS: 'https://xr1xcc83bj.execute-api.us-east-1.amazonaws.com/prod/news',
    // ... etc
};
```

**File 2: `js/auth-handler.js`**
```javascript
// Authentication utilities
function checkAuth() {
    const token = localStorage.getItem('auth_token');
    const userData = localStorage.getItem('user_data');
    if (!token || !userData) {
        window.location.href = 'login.html';
        return null;
    }
    return JSON.parse(userData);
}

function logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_data');
    window.location.href = 'login.html';
}
```

---

## Risk Mitigation

### Before Making Changes
1. ✅ Create backup of current working state
2. ✅ Test all pages locally
3. ✅ Document current functionality

### During Changes
1. Update ONE page at a time
2. Test immediately after each change
3. Keep original code commented out initially
4. Deploy to S3 and test live
5. Only proceed if successful

### Rollback Plan
1. Keep .backup files for all modified pages
2. If issues arise, restore from backup
3. Document what went wrong
4. Fix issue before continuing

---

## Success Metrics

### Code Reduction
- **Target:** 23.6% CSS reduction (160 duplicate rules)
- **Target:** 30-40% JS reduction (estimated)

### Maintainability
- Shared styles in one location
- Easier to update navigation across all pages
- Consistent look and feel

### Performance
- Shared CSS file cached by browser
- Reduced page load size
- Faster subsequent page loads

---

## Timeline

### Week 1 (Current)
- [x] Complete CSS analysis
- [ ] Create common-styles.css
- [ ] Update 3-5 test pages
- [ ] Verify functionality

### Week 2
- [ ] Complete JavaScript analysis
- [ ] Create shared JS files
- [ ] Update remaining CSS pages

### Week 3
- [ ] Update pages to use shared JS
- [ ] Test all pages thoroughly
- [ ] Deploy to S3

### Week 4
- [ ] Final testing
- [ ] Remove commented code
- [ ] Update documentation
- [ ] Performance benchmarking

---

## Tools & Scripts

**Location:** `docs/consolidation/`

1. `audit-css-js.py` - External dependency analysis
2. `compare-inline-css.py` - Inline CSS comparison
3. `compare-inline-js.py` - Inline JavaScript comparison (TO CREATE)
4. `extract-css.py` - Auto-extract common CSS (TO CREATE)
5. `update-pages.py` - Batch update pages (TO CREATE)

---

## Notes

- Start with CSS (easier, less risky)
- Test thoroughly at each step
- Don't rush - quality over speed
- Document all changes
- Keep backups until fully verified
