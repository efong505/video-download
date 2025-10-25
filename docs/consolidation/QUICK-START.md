# Quick Start - CSS Consolidation

## ✅ What's Done

1. Created `assets/css/common-styles.css` with shared navigation styles
2. Created `update-page-css.py` script with automatic backup/revert
3. **TEST CASE:** Updated articles.html (backup created)

## 🧪 Test Now

1. Open `articles.html` in your browser
2. Check if navigation looks correct
3. Test all navigation links
4. Check mobile responsive (resize browser)

## ✅ If It Works

Keep the changes and update more pages:

```bash
# Update more pages
python docs/consolidation/update-page-css.py videos.html
python docs/consolidation/update-page-css.py resources.html
python docs/consolidation/update-page-css.py authors.html
```

## ❌ If It's Broken

Revert immediately:

```bash
python docs/consolidation/update-page-css.py revert articles.html.backup_20251024_155750
```

## 📋 Pages to Update (Priority Order)

1. ✅ articles.html (DONE - TEST THIS FIRST)
2. videos.html
3. resources.html
4. authors.html
5. create-article.html
6. edit-article.html
7. create-news.html
8. edit-news.html
9. admin-templates.html
10. admin-resources.html
11. index.html
12. news.html
13. profile.html

## 🔄 Workflow

For each page:
1. Run: `python docs/consolidation/update-page-css.py <filename>`
2. Test in browser
3. If good: Continue to next page
4. If broken: Revert and investigate

## 📊 Expected Results

- Navigation should look identical
- Mobile responsive should work
- Page load slightly faster (cached CSS)
- Inline CSS reduced by ~16 rules per page

## 🚨 Troubleshooting

**Problem:** Navigation looks different
**Solution:** Check if page has custom nav styles not in common-styles.css

**Problem:** Mobile layout broken
**Solution:** Revert and check media queries

**Problem:** Script fails
**Solution:** Check file path and permissions

## 📁 File Locations

- Shared CSS: `assets/css/common-styles.css`
- Update script: `docs/consolidation/update-page-css.py`
- Backups: `<filename>.backup_YYYYMMDD_HHMMSS`

## 💾 Backup Safety

- Every update creates timestamped backup
- Backups never overwritten
- Can revert anytime
- Original code commented out (not deleted)
