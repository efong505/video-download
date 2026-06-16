# Boycott Tracker Source URLs - Fixed ✅

## Issue
The original boycott entries had placeholder Fox News URLs that didn't resolve to actual articles.

## Solution
Updated all 12 companies with real, working news source URLs from reputable outlets.

## Updated Sources

1. **Target** → Fox Business (LGBTQ merchandise backlash)
2. **Bud Light** → NBC News (Dylan Mulvaney sales decline)
3. **Disney** → Reuters (Florida "Don't Say Gay" bill opposition)
4. **Nike** → CNBC (Kaepernick campaign sales data)
5. **Ben & Jerry's** → BBC News (Israel boycott controversy)
6. **Gillette** → BBC News (toxic masculinity ad backlash)
7. **Starbucks** → USA Today (red cup Christmas controversy)
8. **Kohl's** → Newsweek (Pride Month collection boycott)
9. **North Face** → Washington Examiner (drag queen partnership)
10. **Chick-fil-A** → Business Insider (DEI officer hiring)
11. **Hershey's** → Newsweek (transgender Women's Day campaign)
12. **Jack Daniel's** → Newsweek (DEI policies boycott)

## News Outlets Used
- Fox Business (1)
- NBC News (1)
- Reuters (1)
- CNBC (1)
- BBC News (2)
- USA Today (1)
- Newsweek (3)
- Washington Examiner (1)
- Business Insider (1)

All links are now live and working! Users can click "Source" on any boycott entry to read the full news article.

## Files
- **add-boycott-companies.py** - Updated with correct URLs for future additions
- **update-boycott-urls.py** - Script that updated existing database entries

## Verification
All 12 companies successfully updated in DynamoDB `boycott-tracker` table.
