# Admin Dashboard Mobile Fixes

## Issues to Fix

### 1. Tabs Not Fitting on Mobile Screen
**Problem**: Admin tabs expand page width on mobile, causing horizontal scroll

**Solution**: Add responsive CSS for tabs
```css
@media (max-width: 768px) {
    .tabs {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        flex-wrap: nowrap;
    }
    
    .tab {
        flex-shrink: 0;
        min-width: auto;
        padding: 8px 10px;
        font-size: 0.8rem;
        white-space: nowrap;
    }
}
```

### 2. Drag and Drop Not Working on Mobile
**Problem**: Category ordering drag-and-drop doesn't work on touch devices

**Current Code**: Already has mobile detection that disables drag
```javascript
@media (max-width: 768px) {
    .category-order-item,
    .resource-category-order-item {
        pointer-events: none;
    }
}
```

**Better Solution**: Add touch-friendly up/down buttons for mobile
- Show arrow buttons (↑ ↓) on mobile instead of drag handle
- Hide drag functionality on mobile
- Add click handlers to move items up/down

### 3. Emoji Icons Showing as Folder
**Problem**: "election" and "prophecy" categories showing 📁 instead of proper emojis

**Location**: Line 3933+ in admin.html - getCategoryEmoji() function

**Missing Mappings**:
```javascript
'election': '🗳️',
'prophecy': '📜',
```

**Current Code** returns default '📁' for unmatched categories

## Implementation Priority
1. **Emoji Fix** - Easiest, add 2 lines
2. **Mobile Tabs** - Medium, add CSS media query  
3. **Mobile Drag/Drop** - Complex, requires JavaScript rewrite

## Files to Modify
- admin.html (all 3 fixes)
