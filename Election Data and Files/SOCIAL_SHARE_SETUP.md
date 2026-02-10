# Social Share Preview Setup Guide
## Get Beautiful Previews on Facebook, Twitter, LinkedIn, etc.

---

## ✅ WHAT WAS ADDED TO YOUR CODE

I've added comprehensive Open Graph and Twitter Card meta tags to `election-map.html`. These tags tell social platforms what image, title, and description to show when someone shares your link.

---

## 📋 WHAT YOU NEED TO DO NOW

### Step 1: Create Preview Image (5 minutes)

**Option A - Canva (Recommended):**

1. Go to **Canva.com** (free account)
2. Click **"Create a design"** → **"Custom size"**
3. Enter: **1200 x 630 pixels**
4. Design your image:

```
Background: Purple/blue gradient (#667eea to #764ba2)

Large Text (white, bold, 72px):
"CHRISTIAN CONSERVATIVE
ELECTION MAP"

Subtitle (white, 36px):
"Find Pro-Life, Pro-Family Candidates in Your State"

Bottom Icons/Text (white, 24px):
✓ All 50 States
✓ 2025-2026 Elections
✓ Free Voter Guides
✓ Biblical Guidance

Add: 🗳️ emoji or US map graphic
```

5. **Download as PNG or JPG**
6. **Name it:** `election-map-preview.jpg`

**Option B - Screenshot Method:**

1. Open your election map
2. Take full-screen screenshot
3. Open in Paint/Photoshop/GIMP
4. Resize to 1200 x 630 pixels
5. Add text overlay: "Christian Conservative Election Map"
6. Save as `election-map-preview.jpg`

---

### Step 2: Upload Image to Your Server

**If using S3:**

```bash
aws s3 cp election-map-preview.jpg s3://your-bucket-name/images/election-map-preview.jpg --acl public-read
```

**If using regular web hosting:**
- Upload to `/images/` folder via FTP or cPanel
- Make sure it's publicly accessible

**Final URL should be:**
- `https://yourdomain.com/images/election-map-preview.jpg`

---

### Step 3: Update Meta Tags with Your Actual URL

In `election-map.html`, replace these placeholders:

**Find and replace:**
```html
<!-- Change this: -->
<meta property="og:url" content="https://yourdomain.com/election-map.html">
<meta property="og:image" content="https://yourdomain.com/images/election-map-preview.jpg">

<!-- To your actual URLs: -->
<meta property="og:url" content="https://your-actual-domain.com/election-map.html">
<meta property="og:image" content="https://your-actual-domain.com/images/election-map-preview.jpg">
```

**Do the same for Twitter meta tags.**

---

### Step 4: Test Your Social Previews

**Facebook Sharing Debugger:**
1. Go to: https://developers.facebook.com/tools/debug/
2. Enter your URL: `https://yourdomain.com/election-map.html`
3. Click **"Debug"**
4. You should see your image and description
5. If not showing, click **"Scrape Again"**

**Twitter Card Validator:**
1. Go to: https://cards-dev.twitter.com/validator
2. Enter your URL
3. Click **"Preview card"**
4. You should see your image and description

**LinkedIn Post Inspector:**
1. Go to: https://www.linkedin.com/post-inspector/
2. Enter your URL
3. Click **"Inspect"**

---

## 🎨 PREVIEW IMAGE DESIGN TIPS

### What Makes a Good Preview Image:

1. **Clear, Bold Text**
   - Large enough to read on mobile
   - High contrast (white text on dark background)
   - 2-3 lines max

2. **Recognizable Branding**
   - Use your color scheme
   - Include logo or icon
   - Consistent with site design

3. **Visual Interest**
   - US map graphic
   - 🗳️ emoji
   - Gradient background
   - Not too cluttered

4. **Key Information**
   - What it is: "Election Map"
   - Who it's for: "Christian Conservative"
   - Value prop: "Find Pro-Life Candidates"

### Bad Examples to Avoid:
- ❌ Too much text (hard to read)
- ❌ Low contrast (text blends in)
- ❌ Generic stock photos
- ❌ Unclear purpose
- ❌ Wrong dimensions (gets cropped)

---

## 📱 HOW IT LOOKS ON DIFFERENT PLATFORMS

### Facebook:
- Shows large image (1200x630)
- Title below image
- Description below title
- "Learn More" button

### Twitter:
- Shows large image (1200x628)
- Title overlaid on image
- Description below
- Domain shown

### LinkedIn:
- Shows image (1200x627)
- Title and description below
- Professional appearance

### Email (Gmail, Outlook):
- Shows small thumbnail
- Title and description
- Depends on email client

### iMessage/WhatsApp:
- Shows image preview
- Title and description
- Clickable link

---

## 🔧 TROUBLESHOOTING

### Image Not Showing?

**1. Check Image URL:**
```bash
# Test if image is accessible
curl -I https://yourdomain.com/images/election-map-preview.jpg

# Should return: HTTP/1.1 200 OK
```

**2. Check Image Permissions:**
- Make sure image is publicly accessible
- No authentication required
- CORS headers set (if on different domain)

**3. Clear Facebook Cache:**
- Go to Facebook Debugger
- Click "Scrape Again"
- May take 24 hours to update

**4. Check Image Size:**
- Must be at least 200x200 pixels
- Recommended: 1200x630 pixels
- Max file size: 8MB
- Format: JPG or PNG

### Wrong Image Showing?

**1. Old Image Cached:**
- Clear Facebook cache (Scrape Again)
- Wait 24 hours
- Try different filename

**2. Multiple og:image Tags:**
- Make sure only one og:image tag
- Remove duplicates

**3. Image Path Wrong:**
- Check for typos in URL
- Use absolute URL (not relative)
- Include https://

---

## 📊 WHAT EACH META TAG DOES

### Open Graph (Facebook, LinkedIn, etc.):

```html
<!-- Type of content -->
<meta property="og:type" content="website">

<!-- URL of the page -->
<meta property="og:url" content="https://yourdomain.com/election-map.html">

<!-- Title shown in preview -->
<meta property="og:title" content="Christian Conservative Election Map">

<!-- Description shown in preview -->
<meta property="og:description" content="Find pro-life candidates...">

<!-- Image shown in preview -->
<meta property="og:image" content="https://yourdomain.com/images/preview.jpg">

<!-- Image dimensions (helps platforms optimize) -->
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">

<!-- Alt text for accessibility -->
<meta property="og:image:alt" content="Election map showing US states">
```

### Twitter Card:

```html
<!-- Type of card (summary_large_image shows big image) -->
<meta name="twitter:card" content="summary_large_image">

<!-- Same as Open Graph but for Twitter -->
<meta name="twitter:url" content="...">
<meta name="twitter:title" content="...">
<meta name="twitter:description" content="...">
<meta name="twitter:image" content="...">
```

---

## ✅ VERIFICATION CHECKLIST

Before launching, verify:

- [ ] Preview image created (1200x630 pixels)
- [ ] Image uploaded to server
- [ ] Image is publicly accessible
- [ ] Meta tags updated with actual URLs
- [ ] Tested on Facebook Debugger
- [ ] Tested on Twitter Card Validator
- [ ] Image shows correctly on Facebook
- [ ] Image shows correctly on Twitter
- [ ] Title and description are correct
- [ ] No typos in meta tags

---

## 🎯 EXPECTED RESULTS

### When Someone Shares Your Link:

**On Facebook:**
```
┌─────────────────────────────────────┐
│                                     │
│  [Your Preview Image - 1200x630]    │
│                                     │
├─────────────────────────────────────┤
│ Christian Conservative Election Map │
│                                     │
│ Interactive election map for        │
│ Christian voters. Find pro-life...  │
│                                     │
│ yourdomain.com                      │
└─────────────────────────────────────┘
```

**On Twitter:**
```
┌─────────────────────────────────────┐
│                                     │
│  [Your Preview Image - 1200x628]    │
│                                     │
│  Christian Conservative Election... │
│  Interactive election map for...    │
│  yourdomain.com                     │
└─────────────────────────────────────┘
```

**On LinkedIn:**
```
┌─────────────────────────────────────┐
│  [Your Preview Image - 1200x627]    │
├─────────────────────────────────────┤
│ Christian Conservative Election Map │
│ Interactive election map for        │
│ Christian voters...                 │
│ yourdomain.com                      │
└─────────────────────────────────────┘
```

---

## 💡 PRO TIPS

### 1. Create Multiple Images for Different Contexts:

**General Share:**
- `election-map-preview.jpg` (default)

**State-Specific Shares:**
- `virginia-election-preview.jpg`
- `texas-election-preview.jpg`
- Update og:image dynamically per state

### 2. A/B Test Different Images:

Try different designs and see which gets more clicks:
- Version A: Map-focused
- Version B: Text-focused
- Version C: Candidate photos

### 3. Update Seasonally:

- "2025 Elections" → "2026 Elections"
- Add urgency: "Election Day: Nov 5, 2025"
- Highlight featured races

### 4. Add Branding:

- Include your logo
- Consistent color scheme
- Recognizable style

---

## 🚀 ADVANCED: Dynamic Preview Images

If you want different images for different states:

```html
<!-- In your state-specific pages -->
<meta property="og:image" content="https://yourdomain.com/images/virginia-preview.jpg">
<meta property="og:title" content="Virginia 2025 Elections - Christian Voter Guide">
<meta property="og:description" content="Complete guide to Virginia's 2025 elections. Governor race, 140 legislature seats, and more.">
```

---

## 📈 MEASURE SUCCESS

Track these metrics:

1. **Click-Through Rate:**
   - How many people click shared links?
   - Compare with/without preview image

2. **Share Count:**
   - How many times is it shared?
   - Which platforms get most shares?

3. **Engagement:**
   - Do people stay on site longer?
   - Do they explore more states?

**Expected Improvement with Good Preview:**
- Click-through rate: +50-100%
- Share rate: +30-50%
- Engagement: +20-30%

---

## 🎉 SUMMARY

**What You Need to Do:**

1. ✅ Create 1200x630 preview image (5 min)
2. ✅ Upload to `/images/` folder (2 min)
3. ✅ Update meta tags with actual URLs (2 min)
4. ✅ Test on Facebook Debugger (2 min)
5. ✅ Test on Twitter Validator (2 min)

**Total Time: 15 minutes**

**Result:**
- Beautiful previews on all social platforms
- Higher click-through rates
- More professional appearance
- Better viral potential

---

## 📞 NEED HELP?

**Common Issues:**

1. **"Image not showing"**
   - Check URL is correct
   - Make sure image is public
   - Clear Facebook cache

2. **"Wrong image showing"**
   - Clear cache and scrape again
   - Wait 24 hours
   - Check for duplicate tags

3. **"Image is cropped weird"**
   - Use exact dimensions: 1200x630
   - Keep important content in center
   - Test on multiple platforms

---

**Once you complete these steps, your social shares will look professional and get much higher engagement!** 🎉

