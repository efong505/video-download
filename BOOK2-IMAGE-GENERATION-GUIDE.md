# Book 2 Email Campaign - Image Generation Guide

## Images Needed

You'll need **4 lifestyle images** featuring the book. Generate these in ChatGPT (DALL-E) or your preferred AI image generator.

---

### Image 1: Hero Book Shot
**Filename**: `book2-hero-desk.jpg`
**Dimensions**: 1200x800px (landscape)
**Used in**: Email 1, Email 7

**Prompt for ChatGPT/DALL-E**:
```
Create a professional lifestyle photograph of a paperback book titled "The Necessary Evil: AI Prompting for Everyday People" by Edward Fong. The book should be placed on a clean, modern desk with soft natural lighting from a window. Include a laptop partially visible in the background, a coffee cup, and a notebook. The scene should feel peaceful, productive, and approachable. The book cover should be clearly visible with "The Necessary Evil" as the main title and "AI Prompting for Everyday People" as the subtitle. Use a warm, inviting color palette with blues and whites. Professional photography style, shallow depth of field, realistic textures.
```

**Where it goes in HTML**:
```html
<!-- Add after the opening div in Email 1 and Email 7 -->
<img src="https://christianconservativestoday.com/images/book2-hero-desk.jpg" 
     alt="The Necessary Evil: AI Prompting for Everyday People" 
     style="max-width: 100%; height: auto; border-radius: 8px; margin-bottom: 20px;">
```

---

### Image 2: Book with Framework Graphic
**Filename**: `book2-framework-mockup.jpg`
**Dimensions**: 800x600px (landscape)
**Used in**: Email 2, Email 4

**Prompt for ChatGPT/DALL-E**:
```
Create a lifestyle photograph showing the book "The Necessary Evil: AI Prompting for Everyday People" open on a table, with a hand-drawn diagram visible showing the seven-step framework: "Aim. Inform. Direct. Shape. Refine. Verify. Apply." written in neat handwriting on the page. Include a pen, highlighter, and reading glasses nearby. Bright, clean lighting. Professional photography. The scene should suggest active learning and practical application. Top-down angle, realistic paper texture.
```

**Where it goes in HTML**:
```html
<!-- Add after the framework box in Email 2 and Email 4 -->
<img src="https://christianconservativestoday.com/images/book2-framework-mockup.jpg" 
     alt="AI Direction Framework" 
     style="max-width: 100%; height: auto; border-radius: 8px; margin: 22px 0;">
```

---

### Image 3: Book Stack with Coffee
**Filename**: `book2-reading-corner.jpg`
**Dimensions**: 1000x750px (landscape)
**Used in**: Email 3, Email 5

**Prompt for ChatGPT/DALL-E**:
```
Create a cozy, inviting photograph of "The Necessary Evil: AI Prompting for Everyday People" book resting on a comfortable reading chair or couch armrest. Include a warm coffee mug on a side table, soft throw blanket, and warm lighting from a nearby lamp. The atmosphere should feel peaceful, thoughtful, and contemplative - suggesting careful reading and consideration. The book cover should be clearly visible. Use warm browns, soft whites, and gentle blues. Realistic home setting, professional photography, soft focus on background.
```

**Where it goes in HTML**:
```html
<!-- Add after the main headline in Email 3 and Email 5 -->
<img src="https://christianconservativestoday.com/images/book2-reading-corner.jpg" 
     alt="The Necessary Evil Book" 
     style="max-width: 100%; height: auto; border-radius: 8px; margin: 20px 0;">
```

---

### Image 4: Book with Workbook Companion
**Filename**: `book2-with-workbook.jpg`
**Dimensions**: 1000x700px (landscape)
**Used in**: Email 4, Email 6

**Prompt for ChatGPT/DALL-E**:
```
Create a professional photograph showing "The Necessary Evil: AI Prompting for Everyday People" book next to printed workbook pages. The workbook pages should show blank exercise templates and frameworks for practice. Include a pen, highlighter, and laptop in the background. The scene should suggest practical application and active learning. Clean, bright, organized workspace. Professional photography with good lighting. The book should be the focal point with workbook pages slightly overlapping or adjacent.
```

**Where it goes in HTML**:
```html
<!-- Add before the workbook CTA button in Email 4 and Email 6 -->
<img src="https://christianconservativestoday.com/images/book2-with-workbook.jpg" 
     alt="Book 2 with Free Workbook" 
     style="max-width: 100%; height: auto; border-radius: 8px; margin: 20px 0;">
```

---

## Image Hosting Instructions

### Option 1: Host on christianconservativestoday.com
1. Upload images to S3: `my-video-downloads-bucket/images/`
2. Images will be accessible via CloudFront at:
   - `https://christianconservativestoday.com/images/book2-hero-desk.jpg`
   - `https://christianconservativestoday.com/images/book2-framework-mockup.jpg`
   - `https://christianconservativestoday.com/images/book2-reading-corner.jpg`
   - `https://christianconservativestoday.com/images/book2-with-workbook.jpg`

### Option 2: Host on necessaryevilbooks.com
If you have that domain set up for hosting images.

---

## Upload Command (after generating images)

```powershell
# Upload to S3
aws s3 cp book2-hero-desk.jpg s3://my-video-downloads-bucket/images/ --profile ekewaka --content-type image/jpeg
aws s3 cp book2-framework-mockup.jpg s3://my-video-downloads-bucket/images/ --profile ekewaka --content-type image/jpeg
aws s3 cp book2-reading-corner.jpg s3://my-video-downloads-bucket/images/ --profile ekewaka --content-type image/jpeg
aws s3 cp book2-with-workbook.jpg s3://my-video-downloads-bucket/images/ --profile ekewaka --content-type image/jpeg
```

---

## Email-Specific Image Placement

### Email 1: AI Is Here — But Who Is Directing It?
- **Image**: `book2-hero-desk.jpg`
- **Placement**: Right after opening `<div>`, before "Hello {{FIRST_NAME}}"

### Email 2: Prompting Is Not Magic Wording
- **Image**: `book2-framework-mockup.jpg`
- **Placement**: After the framework callout box

### Email 3: AI Should Be Assistance, Not Authority
- **Image**: `book2-reading-corner.jpg`
- **Placement**: After the headline

### Email 4: The Free AI Direction Workbook Is Live
- **Image**: `book2-with-workbook.jpg`
- **Placement**: Before the workbook CTA button

### Email 5: Polished Does Not Mean True
- **Image**: `book2-reading-corner.jpg` (reuse)
- **Placement**: After the headline

### Email 6: From Warning to Practical Response
- **Image**: `book2-with-workbook.jpg` (reuse)
- **Placement**: After the blue callout box

### Email 7: Final Reminder
- **Image**: `book2-hero-desk.jpg` (reuse)
- **Placement**: Right after opening `<div>`, before "Hello {{FIRST_NAME}}"

---

## Mobile Optimization

All images include this responsive styling:
```html
style="max-width: 100%; height: auto; border-radius: 8px; margin: 20px 0;"
```

This ensures:
- Images scale down on mobile
- Rounded corners for modern look
- Proper spacing around images
- No horizontal scrolling

---

## Alternative: Generate Images Later

If you want to launch the campaign first WITHOUT images:
1. Deploy the emails as-is
2. Generate images later
3. Update the campaign HTML in DynamoDB
4. New subscribers will see images automatically

---

## Next Steps

1. **Generate images in ChatGPT** using the 4 prompts above
2. **Download and rename** them to the exact filenames
3. **Upload to S3** using the command provided
4. **Update HTML** in the campaign records with the `<img>` tags
5. **Test** by sending yourself Email 1

OR skip images for now and add them later after initial launch.
