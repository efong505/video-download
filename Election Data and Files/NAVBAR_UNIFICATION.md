# Navbar Unification Plan

## Problem
Inconsistent navigation bars across HTML pages:
- **index.html**: Working logo (techcrosslogo.jpg), Font Awesome icons, dynamic auth dropdown
- **election-map.html**: Broken logo (emoji 🗺️), no icons, simple auth link
- **Other pages**: Likely have similar inconsistencies

## Solution Created

### 1. Unified Navbar Component
Created `navbar.html` with:
- ✅ Working logo: `techcrosslogo.jpg`
- ✅ Font Awesome icons for all links
- ✅ Dynamic authentication (Login → User dropdown when logged in)
- ✅ Consistent styling matching index.html
- ✅ Responsive design with Bootstrap
- ✅ Admin dashboard link for admin/super_user roles

### 2. Smart Features
- ✅ Hides current page link (no "Videos" link on videos.html)
- ✅ Shows only public links when logged out (Videos, Articles, Election Map)
- ✅ Shows all links when logged in (adds Resources)
- ✅ Shows Admin link only for admin/super_user roles
- ✅ Page-specific branding (custom icon instead of logo)
- ✅ Dynamic auth dropdown with user name

### 3. Usage Examples

#### Index Page (default logo)
```html
<div id="navbar-container" data-page="index"></div>
<script>
    fetch('navbar.html')
        .then(r => r.text())
        .then(html => document.getElementById('navbar-container').innerHTML = html);
</script>
```

#### Election Map (custom icon)
```html
<div id="navbar-container" data-page="election-map" data-icon="🗺️"></div>
<script>
    fetch('navbar.html')
        .then(r => r.text())
        .then(html => document.getElementById('navbar-container').innerHTML = html);
</script>
```

#### Videos Page
```html
<div id="navbar-container" data-page="videos"></div>
<script>
    fetch('navbar.html')
        .then(r => r.text())
        .then(html => document.getElementById('navbar-container').innerHTML = html);
</script>
```

### 4. Required Dependencies
All pages must include:
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
```

### 4. Pages to Update
- ✅ navbar.html (created)
- ⏳ election-map.html (needs update)
- ⏳ videos.html
- ⏳ articles.html
- ⏳ resources.html
- ⏳ confirm.html
- ⏳ unsubscribe.html
- ⏳ Any other public pages

### 5. Benefits
- Consistent branding across all pages
- Single source of truth for navigation
- Easier maintenance (update once, applies everywhere)
- Better user experience
- Working authentication state management

### 6. Next Steps
1. Choose implementation method (A, B, or C)
2. Update election-map.html to use unified navbar
3. Update remaining pages
4. Test authentication flow on all pages
5. Verify logo displays correctly on all pages
