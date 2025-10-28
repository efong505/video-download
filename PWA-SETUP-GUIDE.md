# PWA Setup Guide - Christian Conservative Platform

## What You've Created

Your website is now a **Progressive Web App (PWA)** that users can install on their devices like a native app!

## Files Created

1. **manifest.json** - App configuration and metadata
2. **service-worker.js** - Offline caching and push notifications
3. **pwa-install.js** - Installation prompt and service worker registration
4. **index.html** - Updated with PWA meta tags

## Next Steps

### Step 1: Create App Icons

You need to create app icons in these sizes and place them in `/icons/` folder:

- icon-72x72.png
- icon-96x96.png
- icon-128x128.png
- icon-144x144.png
- icon-152x152.png
- icon-192x192.png
- icon-384x384.png
- icon-512x512.png

**Quick Way:** Use an online tool like:
- https://realfavicongenerator.net/
- https://www.pwabuilder.com/imageGenerator

Upload your logo (techcrosslogo.jpg) and it will generate all sizes.

### Step 2: Upload to S3

Upload these new files to your S3 bucket:

```powershell
aws s3 cp manifest.json s3://techcross-videos/
aws s3 cp service-worker.js s3://techcross-videos/
aws s3 cp pwa-install.js s3://techcross-videos/
aws s3 cp index.html s3://techcross-videos/
aws s3 sync icons/ s3://techcross-videos/icons/
```

### Step 3: Update Other Pages

Add PWA meta tags to all your HTML pages (videos.html, articles.html, etc.):

```html
<!-- Add to <head> section -->
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#667eea">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="CC Platform">

<!-- Add before </body> -->
<script src="pwa-install.js"></script>
```

### Step 4: Test Your PWA

1. **Desktop (Chrome/Edge):**
   - Open your website
   - Look for install icon in address bar
   - Click to install

2. **Mobile (iOS Safari):**
   - Open website in Safari
   - Tap Share button
   - Tap "Add to Home Screen"

3. **Mobile (Android Chrome):**
   - Open website in Chrome
   - Tap menu (3 dots)
   - Tap "Install app" or "Add to Home Screen"

### Step 5: Enable HTTPS (Required)

PWAs require HTTPS. Your CloudFront distribution should already have this enabled.

Verify at: https://your-domain.com

### Step 6: Test Offline Mode

1. Install the PWA
2. Open DevTools (F12)
3. Go to Network tab
4. Check "Offline" checkbox
5. Refresh page - it should still work!

## Features Now Available

✅ **Install to Home Screen** - Users can add your app to their device
✅ **Offline Access** - Cached pages work without internet
✅ **App-Like Experience** - Runs in standalone mode (no browser UI)
✅ **Push Notifications** - Ready for breaking news alerts (needs backend setup)
✅ **Fast Loading** - Service worker caches resources

## Customization Options

### Change App Colors

Edit `manifest.json`:
```json
"background_color": "#667eea",  // Splash screen color
"theme_color": "#667eea"        // Status bar color
```

### Add More Cached Pages

Edit `service-worker.js`:
```javascript
var urlsToCache = [
  '/',
  '/index.html',
  '/videos.html',
  '/articles.html',
  '/news.html',  // Add more pages
  '/resources.html'
];
```

### Customize Install Banner

Edit `pwa-install.js` - Change the banner text and styling in `showInstallBanner()` function.

## Push Notifications Setup (Optional)

To enable push notifications for breaking news:

1. **Get VAPID Keys:**
```bash
npm install web-push -g
web-push generate-vapid-keys
```

2. **Update pwa-install.js:**
Replace `YOUR_PUBLIC_VAPID_KEY_HERE` with your public key

3. **Backend Setup:**
Create Lambda function to send push notifications using AWS SNS

## Testing Checklist

- [ ] Icons display correctly
- [ ] Install prompt appears
- [ ] App installs successfully
- [ ] Offline mode works
- [ ] Theme colors match branding
- [ ] All pages cached properly
- [ ] Service worker registers without errors

## Troubleshooting

**Install button doesn't appear:**
- Check HTTPS is enabled
- Clear browser cache
- Check console for errors
- Verify manifest.json is accessible

**Offline mode not working:**
- Check service worker registration in DevTools
- Verify files are being cached
- Check Network tab for cache hits

**Icons not showing:**
- Verify icon files exist in /icons/ folder
- Check file paths in manifest.json
- Clear cache and reinstall

## Browser Support

✅ Chrome/Edge (Desktop & Mobile)
✅ Safari (iOS 11.3+)
✅ Firefox (Desktop & Mobile)
✅ Samsung Internet
✅ Opera

## Next Phase: React Native

After PWA is working, you can build native apps with React Native that use the same backend APIs!

## Resources

- [PWA Builder](https://www.pwabuilder.com/)
- [Google PWA Checklist](https://web.dev/pwa-checklist/)
- [MDN PWA Guide](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
- [Service Worker Cookbook](https://serviceworke.rs/)

## Support

Questions? Check the console for errors or test at:
- https://www.pwabuilder.com/ (PWA validator)
- Chrome DevTools > Application > Manifest
- Chrome DevTools > Application > Service Workers
