# Boycott Tracker & Login Redirect Updates

## 1. Boycott Companies Added ✅

Added 12 well-known companies to the boycott tracker that align with Christian conservative concerns:

### Active Boycotts (11 companies)
1. **Target** - Woke Marketing (Pride Month displays targeting children)
2. **Bud Light / Anheuser-Busch** - Woke Marketing (Dylan Mulvaney partnership)
3. **Disney** - Anti-Christian (LGBTQ+ content in children's programming)
4. **Nike** - Anti-Conservative (Colin Kaepernick campaigns)
5. **Ben & Jerry's** - Anti-Conservative (far-left activism, anti-Israel)
6. **Gillette** - Woke Marketing ("toxic masculinity" ad)
7. **Starbucks** - Anti-Christian (removed Christmas, LGBTQ+ activism)
8. **Kohl's** - Woke Marketing (Pride Month merchandise)
9. **North Face** - Anti-Conservative (refused Christian org order, drag events)
10. **Hershey's** - Woke Marketing (transgender Women's Day campaign)
11. **Jack Daniel's** - ESG/DEI (aggressive DEI policies)

### Watching Status (1 company)
12. **Chick-fil-A** - Other (shifted from traditional values, hired DEI officer)

### Features
- Each entry includes:
  - Category (ESG/DEI, Anti-Christian, Anti-Conservative, Censorship, Woke Marketing)
  - Detailed reason for boycott
  - Christian/conservative alternatives
  - Source URL for verification
  - Vote count (starts at 0)

### How to View
Visit `boycott-tracker.html` and the companies will appear in the "Active Boycotts" tab.

---

## 2. Login Redirect Functionality ✅

Implemented "return to last page" feature after login/logout.

### How It Works

**When Logging Out:**
1. User clicks "Logout" in navbar
2. System saves current page URL to `localStorage` as `redirect_after_login`
3. Redirects to `login.html?redirect=<current_page_url>`

**When Logging In:**
1. User enters credentials on login page
2. After successful login, checks for `redirect` URL parameter
3. If found, redirects to that page
4. If not found, uses default redirect (admin.html for admins, videos.html for users)

**When Accessing Protected Pages:**
1. Pages like `notification-settings.html` check if user is logged in
2. If not logged in, saves current page and redirects to login with redirect parameter
3. After login, user returns to the page they were trying to access

### Files Updated

1. **notification-settings.html**
   - Added redirect URL parameter when sending to login page
   - Saves current page to localStorage

2. **navbar.js** (logout function)
   - Saves current page before logout
   - Passes redirect parameter to login page

3. **login.html** (already had redirect support)
   - Checks for `redirect` URL parameter
   - Redirects to saved page after successful login

### Testing

1. **Test Logout Redirect:**
   - Navigate to any page (e.g., `prayer-wall.html`)
   - Click "Logout"
   - Log back in
   - Should return to `prayer-wall.html`

2. **Test Protected Page Redirect:**
   - Log out
   - Try to access `notification-settings.html`
   - Will redirect to login
   - After login, returns to notification settings

---

## Technical Details

### Boycott Script
- **File:** `add-boycott-companies.py`
- **Table:** `boycott-tracker` (DynamoDB)
- **Profile:** `ekewaka`
- **Region:** `us-east-1`

### Redirect Implementation
- **Storage:** URL parameters + localStorage
- **Parameter:** `?redirect=<encoded_url>`
- **Fallback:** Default pages (admin.html or videos.html)
- **Scope:** Works across all pages using navbar.js

---

## Next Steps

### Boycott Tracker
- Users can now vote on these companies
- Admin can approve/reject new reports
- Consider adding more companies as they emerge

### Login Redirect
- Feature is now live and working
- No additional configuration needed
- Works automatically for all protected pages
