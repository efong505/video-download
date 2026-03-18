# Missing Media & Script Files Analysis

## FILES IN S3 ROOT (Missing Locally)

### 📄 PDF Files (3 files):
1. book-teaser.pdf
2. the-necessary-evil-full.pdf
3. the-necessary-evil-full-second-edition-E-book.pdf

### 🖼️ Image Files (10 files):
1. apple-touch-icon.png
2. author-photo.jpg
3. book-cover.jpg
4. favicon-16x16.png
5. favicon-32x32.png
6. second-edition-book-cover-front.png
7. section1.png
8. section1-alt.png
9. section3-victory.png
10. techcrosslogo.jpg
11. techcrosslogo.svg

### 📜 JavaScript Files (4 files):
1. common-utils.js
2. navbar.js
3. pwa-install.js
4. service-worker.js

### 📋 JSON Files (1 file):
1. manifest.json

### 🎨 CSS Files (3 files - in assets/css/):
1. assets/css/card-styles.css
2. assets/css/common-styles.css
3. assets/css/form-styles.css

## TOTAL MISSING FILES: 21 files

### File Size Summary:
- **Large PDFs**: 
  - the-necessary-evil-full.pdf (~3.5 MB)
  - the-necessary-evil-full-second-edition-E-book.pdf (~3.3 MB)
  - book-teaser.pdf (~762 KB)

- **Large Images**:
  - section1.png (~26.9 MB)
  - section1-alt.png (~27.4 MB)
  - section3-victory.png (~28.2 MB)
  - book-cover.jpg (~10.8 MB)
  - second-edition-book-cover-front.png (~5.8 MB)

- **Small Images**:
  - apple-touch-icon.png (~351 KB)
  - author-photo.jpg (~315 KB)
  - techcrosslogo.jpg (~193 KB)
  - favicon-32x32.png (~45 KB)
  - favicon-16x16.png (~4 KB)
  - techcrosslogo.svg (~1 KB)

- **Scripts & Config**:
  - All JS/JSON/CSS files are small (<10 KB each)

## RECOVERY COMMANDS

### Download All Missing Files:
```powershell
# Download PDFs
aws s3 sync s3://my-video-downloads-bucket/ . --profile ekewaka --exclude "*" --include "*.pdf" --exclude "*/*"

# Download Images
aws s3 sync s3://my-video-downloads-bucket/ . --profile ekewaka --exclude "*" --include "*.jpg" --include "*.png" --include "*.svg" --exclude "*/*"

# Download JS/JSON files
aws s3 sync s3://my-video-downloads-bucket/ . --profile ekewaka --exclude "*" --include "*.js" --include "*.json" --exclude "*/*"

# Download CSS files (in assets/css/)
aws s3 sync s3://my-video-downloads-bucket/assets/css/ ./assets/css/ --profile ekewaka
```

### Or Download All at Once:
```powershell
aws s3 sync s3://my-video-downloads-bucket/ . --profile ekewaka --exclude "*" --include "*.pdf" --include "*.jpg" --include "*.png" --include "*.svg" --include "*.js" --include "*.json" --exclude "*/*"
```

## NOTES:
- CSS files are in subdirectory (assets/css/) so need separate command
- Large image files (section*.png) are ~27-28 MB each
- Total download size: ~110 MB
