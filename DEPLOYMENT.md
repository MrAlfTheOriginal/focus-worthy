# Focus Worthy MVP - Deployment & Execution Guide

## Quick Start (3 Commands)

```bash
# 1. Setup
cd /home/alf/focus-worthy
bash setup.sh

# 2. Run tests
python3 test_workflow.py

# 3. Start services
# Terminal 1
python3 api.py
# Terminal 2
python3 website_receiver.py
# Terminal 3
python3 ui.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 Desktop UI (PyQt6)                      │
│  Layer 1: Affiliate Programs | Layer 2: Workspace      │
└────────────────┬────────────────────────────────────────┘
                 │ REST API
                 ▼
┌─────────────────────────────────────────────────────────┐
│              Backend API (Flask)                        │
│  :5000 - Affiliate & COP management                     │
│  - Affiliate Programs CRUD                              │
│  - Affiliate Sources (immutable)                        │
│  - COP Products (editable)                              │
│  - LAUNCH Jobs Queue                                    │
│  - Scraper Queue Management                             │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP POST
                 ▼
┌─────────────────────────────────────────────────────────┐
│           Website Receiver API (Flask)                  │
│  :5001 - Auto-receive & publish products               │
│  - POST /api/products (receive)                         │
│  - Auto-generate category pages                         │
│  - Auto-organize by category/subcategory               │
└─────────────────────────────────────────────────────────┘

Database Layer:
├── focus_worthy.db   (Platform DB - SQLite)
└── website.db        (Website DB - SQLite)
```

## Data Flow: Affiliate → Website

```
1. SCRAPE (Layer 1)
   - User adds affiliate program (name, URL, API type)
   - User clicks "Scrape"
   - Products stored in affiliate_sources (IMMUTABLE)

2. MOVE TO COP (Layer 2)
   - User browses affiliate_sources
   - User clicks "→ COP"
   - Product copied to cop_products (EDITABLE)

3. EDIT (Layer 2)
   - User edits: name, description, price, category, subcategory
   - Changes saved in cop_products table

4. SUBMIT FOR LAUNCH (Layer 3→4)
   - User submits COP product for LAUNCH
   - POST /api/launch/submit {cop_product_id}

5. AI REVIEW (Layer 4)
   - AI auto-categorizes using keyword matching
   - AI scores quality (0-100):
     * Name quality +15
     * Description quality +15+10
     * Price validity +15
     * Image +15
     * Baseline +50
   - Auto-approves if quality >= 70
   - Updates publish_job status

6. HUMAN APPROVAL (Layer 4)
   - Human reviews LAUNCH job
   - Approves or rejects
   - POST /api/launch/{job_id}/approve

7. AUTO-PUBLISH (Layer 4)
   - Approved products auto-publish to website
   - POST http://localhost:5001/api/products
   - Website auto-creates category page
   - Status: published

8. WEBSITE
   - Product visible on /category/{category_slug}
   - Auto-generated landing page
   - Links to affiliate URL
```

## Core Modules

### 1. `db.py` - Database
- `init_db()` - Creates/initializes SQLite database
- `get_db()` - Returns connection with row factory

**Tables:**
- `affiliate_programs` - Connected accounts
- `affiliate_sources` - Scraped products (immutable)
- `sales_sources` - Sales/commission data (immutable)
- `image_supplementals` - Extra images (immutable)
- `cop_products` - Editable combined output
- `publish_jobs` - LAUNCH tracking
- `categories` - Category definitions
- `subcategories` - Subcategory definitions
- `scrape_queue` - Job queue
- `audit_log` - All changes

### 2. `scraper.py` - Web Scraper
- `AffiliateScrapers.scrape_html()` - BeautifulSoup scraper
- `AffiliateScrapers.scrape_json_api()` - JSON API fetcher
- `AffiliateScrapers.generate_sku()` - Unique SKU generation
- `ScrapeManager.scrape_and_store()` - Full pipeline

Supports:
- HTML scraping with CSS selectors
- JSON API with headers & API keys
- XML (placeholder)

### 3. `ai_reviewer.py` - AI Logic
- `AIReviewer.categorize_product()` - Auto-categorize by keywords
- `AIReviewer.score_quality()` - Quality scoring
- `AIReviewer.review_and_auto_approve()` - Full review
- `PublishEngine.publish_product()` - Publishing

Quality scoring:
- 50-100 points based on completeness
- Auto-approve if >= 70
- Keywords: electronics, fashion, home, sports, beauty, books, toys

### 4. `launch_controller.py` - LAUNCH Stage
- `submit_for_launch()` - AI review + create job
- `human_approve()` - Human approval
- `auto_publish()` - Publish to website
- `batch_launch()` - Publish multiple jobs

Status flow: pending → ai_approved/needs_review → human_approved → published

### 5. `api.py` - REST API (Port 5000)

**Affiliate Programs:**
- `GET /api/affiliate-programs`
- `POST /api/affiliate-programs`

**Affiliate Sources:**
- `GET /api/affiliate-sources`
- `POST /api/affiliate-sources`

**COP Products:**
- `GET /api/cop-products?status=draft`
- `POST /api/cop-products`
- `PUT /api/cop-products/{id}`

**LAUNCH (Layer 4):**
- `POST /api/launch/submit` - Submit for AI review
- `POST /api/launch/{job_id}/approve` - Human approve
- `POST /api/launch/{job_id}/publish` - Auto-publish
- `POST /api/launch/batch-publish` - Batch publish

**Scrape Queue:**
- `POST /api/scrape-queue` - Create scrape job
- `GET /api/scrape-queue/{job_id}/status`

**Categories:**
- `GET /api/categories`
- `GET /api/categories/{id}/subcategories`

### 6. `website_receiver.py` - Website API (Port 5001)

**Products:**
- `GET /api/products?category={slug}`
- `POST /api/products` - Receive from LAUNCH

**Categories:**
- `GET /api/categories`

**Pages:**
- `GET /category/{category_slug}` - Auto-generated page

### 7. `ui.py` - PyQt6 Desktop App

**Main Window:**
- Launch controls for Layer 1 & 2

**Layer 1 Window:**
- Add affiliate programs
- List programs with API type
- Scrape button for each

**Layer 2 Window:**
- Tab 1: Browse affiliate sources (immutable)
- Tab 2: COP products (editable) with editor
- Tab 3: Scrape queue status

### 8. `test_workflow.py` - Integration Test
- Tests all layers without API servers
- Demonstrates full workflow
- Verifies database operations
- Shows audit trail

## Testing

### Run Workflow Test
```bash
cd /home/alf/focus-worthy
python3 test_workflow.py
```

Output shows:
1. Affiliate programs created
2. Products scraped → affiliate_sources
3. Products moved → cop_products
4. AI review & scoring
5. LAUNCH jobs created
6. Human approvals
7. Auto-publish
8. Audit summary

### Manual Testing with cURL

```bash
# Add affiliate program
curl -X POST http://localhost:5000/api/affiliate-programs \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Shop",
    "url": "https://shop.test.com",
    "api_type": "json"
  }'

# List COP products
curl http://localhost:5000/api/cop-products?status=draft

# Submit for LAUNCH
curl -X POST http://localhost:5000/api/launch/submit \
  -H "Content-Type: application/json" \
  -d '{"cop_product_id": 1}'

# Batch publish
curl -X POST http://localhost:5000/api/launch/batch-publish \
  -H "Content-Type: application/json" \
  -d '{"status": "ai_approved"}'

# Check website products
curl http://localhost:5001/api/products

# View category page
curl http://localhost:5001/category/electronics
```

## Troubleshooting

### API not starting
```bash
# Check port availability
lsof -i :5000  # Should be empty or kill existing process
lsof -i :5001

# Restart
pkill -f 'python3 api.py'
pkill -f 'python3 website_receiver.py'
python3 api.py
python3 website_receiver.py
```

### Database issues
```bash
# Reset database
rm focus_worthy.db
python3 db.py

# Check schema
python3 -c "from db import get_db; c = get_db().cursor(); c.execute(\"SELECT name FROM sqlite_master WHERE type='table'\"); print([t[0] for t in c.fetchall()])"

# View audit log
python3 -c "from db import get_db; c = get_db().cursor(); c.execute('SELECT * FROM audit_log LIMIT 10'); print(c.fetchall())"
```

### UI not launching
```bash
# Check PyQt6
python3 -c "import PyQt6; print('OK')"

# For headless systems, use X11 forwarding or test API directly
```

## Performance Notes

- **SQLite**: Fine for MVP, handles ~10k products easily
- **Scraper**: BeautifulSoup is synchronous, add asyncio for speed
- **AI**: Keyword-based, not ML. Upgrade to ML later.
- **Publishing**: Synchronous. Add celery task queue for async.

## Known Limitations

1. No duplicate detection (add hash-based dedup)
2. Credentials stored plaintext (encrypt in production)
3. No user authentication (add JWT)
4. No rate limiting (add Flask-Limiter)
5. Basic category auto-generation (add ML)
6. No image caching (add local CDN)
7. No error recovery (add retry logic)
8. No analytics (add tracking)

## Deployment Checklist

- [ ] Database initialized
- [ ] All Python modules importable
- [ ] API running on :5000
- [ ] Website API running on :5001
- [ ] Desktop UI launches
- [ ] Test workflow passes
- [ ] Can add affiliate programs
- [ ] Can scrape products
- [ ] Can move to COP
- [ ] Can edit COP products
- [ ] Can submit for LAUNCH
- [ ] Can approve LAUNCH jobs
- [ ] Products publish to website
- [ ] Category pages auto-generate

## Next Steps (Post-MVP)

1. **Selenium/Playwright** - JS-heavy site support
2. **PostgreSQL** - Scale to millions
3. **Async Scraper** - Speed up bulk scrapes
4. **ML Categorization** - Better auto-classification
5. **Image Caching** - Local storage + CDN
6. **User Auth** - Multi-user + permissions
7. **Admin Dashboard** - Analytics + monitoring
8. **Webhook Notifications** - Email on approvals
9. **CSV/XML Import** - Bulk operations
10. **Advanced Filtering** - Duplicate detection, brand compliance

---

**Status**: MVP Ready (Day 1)
**Files**: 14 Python modules + database schema
**Database**: SQLite (focus_worthy.db, website.db)
**APIs**: 2 REST endpoints (Flask on :5000 & :5001)
**UI**: PyQt6 desktop app
**Test Coverage**: Full workflow test included

