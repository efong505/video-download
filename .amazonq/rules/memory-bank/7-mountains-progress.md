# 7 Mountains Project - Persistent Memory

## Last Updated: Session ending with commit (pending - live-event + docs update)

---

## Current Status: Phase 6 - Hub-by-Hub Testing & New Features

### Hub Testing Progress
Testing each mountain hub page for broken links, misleading buttons, and UX issues.

| Hub | Status | Notes |
|-----|--------|-------|
| Economics & Business | ✅ Tested & Fixed | Commit 2d66d1b (overhaul), 2e22b9f (dynamic resources), 7d0cab2 (bug fixes) |
| Family | ⏳ NOT STARTED | Needs same treatment as Economics |
| Religion | ⏳ NOT STARTED | Needs same treatment as Economics |
| Education | ⏳ NOT STARTED | Needs same treatment as Economics |
| Media | ⏳ NOT STARTED | Needs same treatment as Economics |
| Art & Entertainment | ⏳ NOT STARTED | Needs same treatment as Economics |
| Government | ⏳ NOT STARTED | Needs same treatment as Economics |

### What "Same Treatment" Means for Each Hub
1. Category-filtered links (`articles.html?category=X`, `videos.html?category=X`)
2. Dual upload options (Upload Video + Write Article buttons)
3. Tab persistence via URL hash (`#promote`, `#expose`, `#involved`, `#resources`)
4. Working resource links pointing to actual pages
5. Dynamic resources from API on Resources tab
6. Honest buttons — "Coming Soon" badges on features that don't exist yet
7. `?mountain=X` param on upload links

---

## Email Marketing System (Complete Pipeline)

### Infrastructure
- **Subscription Handler Lambda:** `email-subscription-handler` — handles subscriptions, tracking, campaigns, enrollments, analytics
- **Email Sender Lambda:** `email-sender` — SQS-triggered, sends emails via SES with open pixel + click tracking
- **Drip Processor Lambda:** `email-drip-processor` — EventBridge-triggered daily, processes active enrollments
- **SQS Queue:** `email-sending-queue` — decouples drip processor from email sender
- **CloudFront:** `E3N00R2D2NE9C5` — has `/track/open/*` and `/track/click/*` behaviors → API Gateway

### Tracking Pipeline (Fixed & Working)
- **Open tracking:** 1x1 pixel embedded in emails → `/track/open/{base64}` → logs to `user-email-events`
- **Click tracking:** All `<a href>` links rewritten to `/track/click/{base64}` → logs click + URL → 302 redirect to destination
- **Format:** `email_sender` uses `user_id:campaign_id:email` (colons), subscription handler uses `email|campaign_id` (pipes) — decoder handles both
- **Single-write:** Events only write to `user-email-events` (not dual-write) to prevent double-counting

### Campaign Groups
- `pre-purchase-book-sequence` — 7 emails for book survival kit signups
- `post-purchase-sequence` — 7 emails for book purchasers

### Campaign Manager (`campaign-manager.html`)
- Create/edit/delete campaigns with HTML content editor
- Campaign group tabs for filtering
- **Enrollments view** — see who's enrolled in what, progress (X/7), status, last sent date
- **⚡ Send Next Now** — manually trigger next drip email bypassing delay timer
- **👤 Manual Enroll** — enroll any email in any campaign group
- Per-campaign analytics (sent, opens, clicks, rates)

### Advanced Analytics (`advanced-email-analytics.html`)
- Overview stats (sent, delivered, opens, clicks, bounces, complaints)
- **Campaigns tab** with group dropdown filter
- **Subscribers tab** with per-subscriber engagement
- **Recent Events tab** — shows campaign NAME (not UUID), click URLs, timestamps
- Charts: performance over time, engagement funnel

### Post-Purchase Enrollment
- Book page PayPal `onApprove` callbacks auto-enroll buyers
- "Already Purchased?" section on book page collects email for enrollment
- `enroll_post_purchase` Lambda action with idempotency check + SNS notification

### Live Event Page (`live-event.html`) — NEW
- Signup page for "How Christians Should Respond to AI" live session
- Email + first name collection form
- Pre-fills email/name from URL params (from drip email click-through)
- Registers user via book subscription API with `live_event_signup` source
- Post-purchase email #6 now links here instead of resources.html

---

## New Features Built (Economics Hub Testing)

### 1. Forum/Discussion System — ✅ COMPLETE (Commit 6599ad9)
- **Infrastructure:** DynamoDB `forum-posts`, Lambda `forum-api`, API Gateway `/forum` on `diz6ceeb22`
- **Frontend:** `forum.html` with mountain tabs, threaded replies, upvotes, delete own posts

### 2. Business Directory — ✅ COMPLETE (Commit 6645eb0)
- **Infrastructure:** DynamoDB `business-directory`, Lambda `business-api`, API Gateway `/businesses`
- **Frontend:** `business-directory.html` with category pills, search, submit form

### 3. Boycott Tracker — ✅ COMPLETE (Commit 4e0171d)
- **Infrastructure:** DynamoDB `boycott-tracker`, Lambda `boycott-api`, API Gateway `/boycotts`
- **Frontend:** `boycott-tracker.html` with status tabs, voting, report form, alternatives

### 4. Specialized Mountain Hub Pages — ✅ COMPLETE

#### Media Mountain
- **media-bias-tracker.html** — Track/report bias in news outlets with voting, status tabs, evidence links
- **fake-news-reporter.html** — Report false narratives with claim/truth format, status tracking

#### Economics Mountain
- **corporate-wokeness-tracker.html** — Track ESG/DEI/anti-Christian corporate policies
- **financial-stewardship.html** — Curated biblical finance resources (Dave Ramsey, Crown, etc.)

#### Government Mountain
- **political-corruption-tracker.html** — Document corruption, constitutional violations, overreach

**CRITICAL BUG FIX:** `hub-cards-loader.js` dynamically overwrites hardcoded HTML cards from API. When adding new specialized pages to hub "Expose & Fight" tabs, must comment out `loadHubCards()` call in the hub page's DOMContentLoaded event to prevent API from overwriting hardcoded links. See commits for media-mountain.html, economics-mountain.html, government-mountain.html where `loadHubCards()` is disabled with comment explaining why.

---

## Completed Phases Summary

### Phase 1-3: Landing Page + 7 Hub Pages + Navigation (Feb 2025)
- All complete. See `7-MOUNTAINS-IMPLEMENTATION.md` for details.

### Phase 4: Backend Infrastructure (Complete)
- 3 DynamoDB tables: `mountain-pledges`, `mountain-badges`, `mountain-contributions`
- Lambda: `mountains-api` with 6 endpoints
- API Gateway: REST API `lcmogvl3v2` deployed to `prod`

### Phase 5: Ministry Templates (Complete)
- 7 mountain-specific article templates in `articles_api/index.py`

### Phase 6: Hub Testing & Polish (IN PROGRESS)
- Economics hub fully tested and fixed
- Next: Family → Religion → Education → Media → Art → Government

---

## Key Technical Details

### AWS
- **Profile:** `ekewaka` (account 371751795928) — ALWAYS use `--profile ekewaka`
- **S3 Bucket:** `my-video-downloads-bucket`
- **Region:** `us-east-1`
- **CloudFront:** `E3N00R2D2NE9C5` (`d271vky579caz9.cloudfront.net` → `christianconservativestoday.com`)
- **PLATFORM_OWNER_ID:** `effa3242-cf64-4021-b2b0-c8a5a9dfd6d2`
- **APIs:**
  - Subscription/Tracking: `niexv1rw75.execute-api.us-east-1.amazonaws.com`
  - Articles/Resources: `diz6ceeb22.execute-api.us-east-1.amazonaws.com/prod`
  - Mountains: `lcmogvl3v2.execute-api.us-east-1.amazonaws.com/prod/mountains`

### DynamoDB Tables (Email System)
- `user-email-campaigns` (PK: user_id, SK: campaign_id) — 14 items (7 pre + 7 post)
- `user-email-drip-enrollments` (PK: user_id, SK: enrollment_id)
- `user-email-events` (PK: user_id, SK: event_id) — PRIMARY event store
- `user-email-subscribers` (PK: user_id, SK: subscriber_email)
- `email-events` (PK: event_id) — LEGACY, still read for historical data
- `email-subscribers`, `book-subscribers`

### Git
- **Remote:** `https://github.com/efong505/video-download.git`
- **Branch:** `main`
- **Recent commits:**
  - `bfe787a` — Fix double-counting: stop dual-write of open/click events
  - `ecd95c0` — Email sender: add click tracking for drip emails
  - `59cdf06` — Analytics: campaign group dropdown filter on Campaigns tab
  - `36f63da` — Analytics: show campaign name instead of UUID in Recent Events
  - `9d06fd4` — Enrollments view + Send Next Now in Campaign Manager
  - `05e5bf0` — Post-purchase campaigns + manual enroll + enroll bafrench33

### Active Subscribers
- `bafrench33@yahoo.com` — enrolled in pre-purchase (step 1) + post-purchase (step 1, manually triggered)
- `efong505@protonmail.com` — pre-purchase (step 1)
- `hawaiianintucson@gmail.com` — pre-purchase (step 4, has duplicate enrollment with _ separator at step 4)
- `juliahinojos@protonmail.com` — pre-purchase (step 2)
- `waianaeboy702@aol.com` — pre-purchase (step 2)

### Windows Gotchas
- Python emoji → use `sys.stdout.reconfigure(encoding='utf-8')`
- pip install freezes in terminal — copy deps from other Lambda folders
- cmd.exe: no `%%f` loops, no `head` command, use `&&` chains
- `findstr` garbles UTF-8 — use PowerShell with `-Encoding UTF8`
- PowerShell JSON escaping is painful — use Python scripts for complex API calls

---

## Resume Point
**Next hub to test:** Family Mountain (`family-mountain.html`)
→ Apply same fixes as Economics: category-filtered links, dual upload, tab persistence, dynamic resources, honest buttons
→ Then: Religion → Education → Media → Art → Government
