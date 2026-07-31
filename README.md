# Focus Worthy MVP - 3-Day Affiliate Scraping & Auto-Publishing Platform

## Overview

Focus Worthy is a desktop + web platform for scraping affiliate products, curating them through an AI + human review pipeline (ASISCOP), and auto-publishing to a website.

### Architecture Layers

- **Layer 1**: Affiliate Program Workspace (login, category discovery, scrape controls)
- **Layer 2**: Affiliate Workspace (browser, category selector, scraped products, queue)
- **Layer 3**: ASISCOP Pipeline
  - **A**: Affiliate Source (immutable)
  - **S**: Sales Source (immutable)
  - **IS**: Image Supplementals (immutable)
  - **COP**: Combined Output Product (only editable layer)
- **Layer 4**: LAUNCH (AI + human review, then auto-publish to website)
- **Website**: Auto-receives products, organizes by category/subcategory, generates landing pages

## Quick Start

### 1. Setup

```bash
cd /home/alf/focus-worthy
bash setup.sh
```

This will:
- Install Python dependencies
- Initialize SQLite databases
- Display project structure

### 2. Start Services (in separate terminals)

**Terminal 1 - Backend API (Layer 1-3)**
```bash
cd /home/alf/focus-worthy
python3 api.py
```
Runs on `http://localhost:5000`

**Terminal 2 - Website Receiver (Layer 4+ publishing)**
```bash
cd /home/alf/focus-worthy
python3 website_receiver.py
```
Runs on `http://localhost:5001`

**Terminal 3 - Desktop UI**
```bash
cd /home/alf/focus-worthy
python3 ui.py
```
PyQt6 desktop app launches. Provides Layer 1 & Layer 2 UI.

### 3. Workflow

#### Step 1: Add Affiliate Programs (Layer 1)
1. Open "Layer 1: Affiliate Programs" window
2. Add program (name, URL, API type: `html_scrape` or `json`)
3. Click "Scrape" to fetch products → stored in `affiliate_sources` (immutable)

#### Step 2: Browse & Move to COP (Layer 2)
1. Open "Layer 2: Affiliate Workspace"
2. Browse "Browse Products" tab → see all `affiliate_sources`
3. Click "→ COP" to move to `cop_products` (editable layer)

#### Step 3: Edit & Categorize in COP (Layer 2)
1. Go to "COP Products" tab
2. Click "Edit" on any product
3. Modify name, description, price, category, subcategory
4. Change status: `draft` → `ready_for_launch`

#### Step 4: Submit for LAUNCH (Layer 4)
1. API call: `POST /api/launch/submit` with `cop_product_id`
2. AI auto-reviews:
   - Quality score (0-100)
   - Auto-category suggestion
   - Auto-approval if score >= 70

#### Step 5: Human Approves (Layer 4)
1. Check LAUNCH jobs via UI or API
2. API call: `POST /api/launch/{job_id}/approve`
3. Triggers auto-publish if AI approved

#### Step 6: Auto-Publish to Website
1. Product auto-publishes to website API (`localhost:5001`)
2. Website creates category page if needed
3. Product goes live immediately

## API Reference

### Affiliate Programs
- `GET /api/affiliate-programs` - List programs
- `POST /api/affiliate-programs` - Create program
- `POST /api/scrape-queue` - Trigger scrape

### Affiliate Sources (Immutable)
- `GET /api/affiliate-sources` - List all scraped products

### COP Products (Editable)
- `GET /api/cop-products?status=draft` - List by status
- `POST /api/cop-products` - Create from affiliate source
- `PUT /api/cop-products/{id}` - Edit product

### LAUNCH Stage
- `POST /api/launch/submit` - AI review + create publish job
- `POST /api/launch/{job_id}/approve` - Human approval
- `POST /api/launch/{job_id}/publish` - Publish to website
- `POST /api/launch/batch-publish` - Publish all approved jobs

### Website API (Port 5001)
- `GET /api/products` - List products (with `?category=slug` filter)
- `POST /api/products` - Receive published product
- `GET /category/{category_slug}` - Auto-generated category page

## Database Schema

### Platform DB (`focus_worthy.db`)
- `affiliate_programs` - Connected accounts
- `affiliate_sources` - Immutable scraped data
- `sales_sources` - Immutable sales/commission data
- `image_supplementals` - Immutable extra images
- `cop_products` - Editable combined output products
- `publish_jobs` - LAUNCH stage tracking
- `categories` - Category definitions (auto-created from COP)
- `subcategories` - Subcategory definitions
- `scrape_queue` - Job queue
- `audit_log` - All changes

### Website DB (`website.db`)
- `products` - Published products
- `categories` - Category slugs
- `category_pages` - Auto-generated HTML pages

## Features

✅ Multi-layer pipeline (Layers 1-4)
✅ Immutable source tracking (ASISCOP)
✅ Editable COP layer
✅ AI auto-categorization & quality scoring
✅ Human approval workflow
✅ Auto-publish to website
✅ Auto-generate category pages
✅ SQLite for fast MVP
✅ Desktop UI (PyQt6)
✅ REST API for programmatic access
✅ Audit log for compliance

## Known Limitations (MVP)

- **Scraper**: Basic BeautifulSoup/requests. Add Playwright for JS-heavy sites.
- **Categories**: Auto-created from COP. Manual categorization coming.
- **Images**: Basic URL storage. Add local caching.
- **Credentials**: Stored in plaintext (use encryption in production).
- **Auth**: None yet. Add JWT/OAuth for multi-user.
- **Website**: Basic HTML generation. Add custom theme support.

## Next Steps (Post-MVP)

1. Add Playwright for JS-rendering sites
2. Implement credential encryption
3. Multi-user auth + permissions
4. SEO optimization (sitemaps, meta tags)
5. Product image caching + optimization
6. PostgreSQL migration for scale
7. Admin dashboard for analytics
8. Email notifications for reviews
9. CSV/XML bulk import
10. Advanced AI filtering (duplicate detection, brand compliance)

## Troubleshooting

### Database locked
- Ensure only one process accesses `focus_worthy.db` at a time
- Close all UI windows before restarting API

### API not responding
- Check if running on `localhost:5000` and `localhost:5001`
- Restart: `pkill -f 'python3 api.py'`

### UI won't start
- Ensure PyQt6 installed: `pip install PyQt6`
- Check X11/display settings on headless systems

### Products not publishing
- Check website API running on `:5001`
- View error log in `publish_jobs` table

## File Structure

```
/home/alf/focus-worthy/
├── schema.sql              # Database schema
├── db.py                   # Database initialization
├── api.py                  # REST API (Layer 1-3, LAUNCH endpoints)
├── website_receiver.py     # Website receiver API (Layer 4+)
├── scraper.py              # Web scraper module
├── ai_reviewer.py          # AI categorization & quality scoring
├── launch_controller.py    # LAUNCH stage orchestration
├── ui.py                   # PyQt6 desktop app
├── requirements.txt        # Python dependencies
├── setup.sh                # Setup script
└── README.md               # This file

Generated:
├── focus_worthy.db         # Platform database
└── website.db              # Website database
```

## Support

For blockers or feature requests during MVP development, check logs:
```bash
# Platform logs
sqlite3 focus_worthy.db "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT 20;"

# Website logs
sqlite3 website.db "SELECT * FROM products ORDER BY published_at DESC LIMIT 10;"
```

---

**Status**: MVP in progress (Day 1)
**Deadline**: 3 days to launch
