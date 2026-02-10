# Social Share Preview - Quick Setup (15 Minutes)

## ✅ What I Already Did For You:

Added all necessary meta tags to `election-map.html`:
- Open Graph tags (Facebook, LinkedIn)
- Twitter Card tags
- Image dimensions
- Alt text for accessibility

---

## 🎯 What You Need to Do:

### 1. Create Preview Image (5 min)

**Go to Canva.com:**
- Create custom size: **1200 x 630 pixels**
- Use purple/blue gradient background (#667eea to #764ba2)
- Add white text:
  - "CHRISTIAN CONSERVATIVE ELECTION MAP"
  - "Find Pro-Life, Pro-Family Candidates in Your State"
  - "✓ All 50 States  ✓ Free Voter Guides"
- Add 🗳️ emoji or US map graphic
- Download as JPG
- Name it: `election-map-preview.jpg`

---

### 2. Upload Image (2 min)

**Upload to your server:**
- Location: `/images/election-map-preview.jpg`
- Make sure it's publicly accessible
- URL should be: `https://yourdomain.com/images/election-map-preview.jpg`

**If using S3:**
```bash
aws s3 cp election-map-preview.jpg s3://your-bucket/images/election-map-preview.jpg --acl public-read
```

---

### 3. Update URLs in election-map.html (2 min)

**Find these lines and replace with your actual domain:**

```html
<!-- Line ~10-15 in <head> section -->
<meta property="og:url" content="https://yourdomain.com/election-map.html">
<meta property="og:image" content="https://yourdomain.com/images/election-map-preview.jpg">

<meta name="twitter:url" content="https://yourdomain.com/election-map.html">
<meta name="twitter:image" content="https://yourdomain.com/images/election-map-preview.jpg">
```

**Replace `yourdomain.com` with your actual domain!**

---

### 4. Test It (5 min)

**Facebook Debugger:**
1. Go to: https://developers.facebook.com/tools/debug/
2. Paste your URL
3. Click "Debug"
4. Should show your image and description
5. If not, click "Scrape Again"

**Twitter Validator:**
1. Go to: https://cards-dev.twitter.com/validator
2. Paste your URL
3. Should show preview

---

## ✅ Done!

Now when people share your link on:
- Facebook → Shows your image + description
- Twitter → Shows your image + description
- LinkedIn → Shows your image + description
- WhatsApp → Shows preview
- iMessage → Shows preview

---

## 🎨 Image Design Template:

```
┌─────────────────────────────────────────┐
│  [Purple/Blue Gradient Background]      │
│                                         │
│              🗳️                         │
│                                         │
│    CHRISTIAN CONSERVATIVE               │
│       ELECTION MAP                      │
│                                         │
│  Find Pro-Life, Pro-Family              │
│  Candidates in Your State               │
│                                         │
│  ✓ All 50 States                        │
│  ✓ 2025-2026 Elections                  │
│  ✓ Free Voter Guides                    │
│  ✓ Biblical Guidance                    │
│                                         │
└─────────────────────────────────────────┘
     1200 x 630 pixels
```

---

## 🚨 Common Mistakes:

- ❌ Wrong image size (must be 1200x630)
- ❌ Image not publicly accessible
- ❌ Forgot to update URLs from "yourdomain.com"
- ❌ Didn't test on Facebook Debugger
- ❌ Used relative URL instead of absolute URL

---

## 💡 Pro Tip:

After uploading, wait 5 minutes then test. Facebook caches aggressively, so if you update the image, you'll need to "Scrape Again" in the debugger.

---

**Total Time: 15 minutes**
**Result: Professional social share previews that increase clicks by 50-100%!**
