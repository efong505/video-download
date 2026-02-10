# CSS and JavaScript Consolidation Plan

## Executive Summary

**Audit Results:**
- 31 production pages analyzed
- 4 unique external CSS files
- 11 unique external JavaScript files
- Every page has 1-3 inline `<style>` blocks
- Every page has 1-3 inline `<script>` blocks

**Key Finding:** Bootstrap 5.3.8 is used in 64.5% of pages, but there's version inconsistency (some pages use 5.3.0).

---

## Phase 1: Standardize Bootstrap Version

### Problem
- 20 pages use Bootstrap 5.3.8
- 4 pages use Bootstrap 5.3.0 (news.html, news-article.html, create-news.html, edit-news.html)

### Action
Update these 4 pages to Bootstrap 5.3.8 for consistency:
- news.html
- news-article.html
- create-news.html
- edit-news.html

### Risk: LOW
Bootstrap 5.3.0 → 5.3.8 is a patch update, minimal breaking changes expected.

---

## Phase 2: Extract Common Inline CSS

### Current State
All 31 pages have inline `<style>` blocks with page-specific styles.

### Analysis Needed
Compare inline CSS across pages to identify:
1. **Truly shared styles** (same CSS in multiple pages)
2. **Similar patterns** (same structure, different values)
3. **Page-specific styles** (unique to one page)

### Proposed Structure
```
common-styles.css          # Shared styles used across multiple pages
admin-styles.css           # Admin-specific shared styles
article-editor-styles.css  # Article/news editor shared styles
```

### Next Step
Create detailed comparison of inline CSS blocks to identify exact duplicates.

---

## Phase 3: Extract Common Inline JavaScript

### Current State
All pages have inline `<script>` blocks with page-specific logic.

### Analysis Needed
Compare inline JavaScript to identify:
1. **Utility functions** (used in multiple pages)
2. **API configuration** (DynamoDB, S3 config)
3. **Authentication logic** (JWT handling)
4. **Common UI interactions** (modals, alerts, etc.)

### Proposed Structure
```
common-utils.js       # Shared utility functions
api-config.js         # AWS SDK configuration
auth-handler.js       # JWT authentication logic
ui-helpers.js         # Common UI interactions
```

### Next Step
Create detailed comparison of inline JavaScript blocks to identify reusable code.

---

## Phase 4: Consolidation Strategy

### External Dependencies (Already Optimized)
✅ Bootstrap 5.3.8 CSS - Used in 64.5% of pages (keep as CDN)
✅ Bootstrap 5.3.8 JS - Used in 51.6% of pages (keep as CDN)
✅ Font Awesome - Used in 22.6% of pages (keep as CDN, page-specific)
✅ Quill.js - Used in 19.4% of pages (keep as CDN, editor pages only)
✅ navbar.js - Already extracted (41.9% of pages)

### What NOT to Consolidate
- **Page-specific libraries:** D3.js, jsPDF, html2canvas (election-map.html only)
- **Quill.js:** Only needed on editor pages (5 pages)
- **Font Awesome:** Only needed on pages with icons (7 pages)
- **Google Analytics:** Only on public-facing pages (2 pages)

---

## Detailed Analysis Required

### Step 1: Compare Inline CSS Blocks
Create script to extract and compare all inline `<style>` blocks:
- Identify exact duplicates
- Identify similar patterns
- Calculate consolidation potential

### Step 2: Compare Inline JavaScript Blocks
Create script to extract and compare all inline `<script>` blocks:
- Identify duplicate functions
- Identify common patterns (AWS SDK init, auth checks, etc.)
- Calculate consolidation potential

### Step 3: Create Shared Files
Based on analysis, create:
- `common-styles.css` - Shared CSS
- `common-utils.js` - Shared JavaScript utilities
- `api-config.js` - AWS configuration
- `auth-handler.js` - Authentication logic

### Step 4: Update Pages Incrementally
Update pages one at a time:
1. Replace inline code with external file references
2. Test thoroughly
3. Deploy to S3
4. Verify live site
5. Move to next page

---

## Risk Assessment

### High Risk Areas
1. **Authentication Logic:** Used across many pages, critical functionality
2. **AWS SDK Configuration:** Different pages use different services
3. **Page-specific Styles:** May break layout if consolidated incorrectly

### Mitigation Strategy
1. **Test locally first** - Open each page in browser after changes
2. **One page at a time** - Don't update multiple pages simultaneously
3. **Keep backups** - Use .backup files before major changes
4. **Incremental deployment** - Deploy and test each page individually
5. **Rollback plan** - Keep original inline code commented out initially

---

## Success Metrics

### Code Reduction
- Target: Reduce total inline CSS by 30-50%
- Target: Reduce total inline JavaScript by 40-60%

### Maintainability
- Shared code in one place (easier to update)
- Consistent patterns across pages
- Reduced duplication

### Performance
- Shared files cached by browser
- Reduced page size
- Faster subsequent page loads

---

## Implementation Timeline

### Week 1: Analysis
- [ ] Run CSS comparison script
- [ ] Run JavaScript comparison script
- [ ] Document findings
- [ ] Create consolidation recommendations

### Week 2: Create Shared Files
- [ ] Create common-styles.css
- [ ] Create common-utils.js
- [ ] Create api-config.js
- [ ] Create auth-handler.js

### Week 3: Update Pages (Batch 1)
- [ ] Update 5-10 pages
- [ ] Test locally
- [ ] Deploy to S3
- [ ] Verify live

### Week 4: Update Pages (Batch 2)
- [ ] Update remaining pages
- [ ] Test locally
- [ ] Deploy to S3
- [ ] Verify live

### Week 5: Cleanup
- [ ] Remove commented-out code
- [ ] Update documentation
- [ ] Final testing
- [ ] Performance benchmarking

---

## Next Immediate Steps

1. **Create CSS comparison script** to analyze inline `<style>` blocks
2. **Create JavaScript comparison script** to analyze inline `<script>` blocks
3. **Generate detailed comparison reports** showing exact duplicates
4. **Make consolidation decisions** based on data, not assumptions

---

## Questions to Answer

1. How much CSS is truly duplicated across pages?
2. How much JavaScript is truly duplicated across pages?
3. What are the common patterns in inline styles?
4. What are the common patterns in inline scripts?
5. Which pages can share code without breaking?
6. What's the optimal file structure for shared code?

---

## Tools Created

- [x] `audit-css-js.py` - Analyzes external dependencies
- [ ] `compare-inline-css.py` - Compares inline CSS blocks
- [ ] `compare-inline-js.py` - Compares inline JavaScript blocks
- [ ] `extract-common-code.py` - Extracts shared code automatically

---

## Notes

- **Don't rush:** Consolidation done wrong can break the entire site
- **Test thoroughly:** Every page must be tested after changes
- **Document everything:** Keep track of what was changed and why
- **Incremental approach:** Small changes, frequent testing, gradual rollout
- **Backup everything:** Keep .backup files until consolidation is complete
