# Focus Worthy MVP - Quick Reference

## 30-Second Overview

**What**: Affiliate product scraper + AI reviewer + auto-publisher
**Where**: Desktop UI + Web APIs
**How**: Scrape → Store (immutable) → Edit (editable COP) → AI Review → Human Approve → Auto-Publish
**Status**: MVP Complete, Tested, Ready to Use

## 3-Minute Quick Start

```bash
# Terminal 1: Setup
cd /home/alf/focus-worthy
python3 db.py

# Terminal 2: Run test (5 min)
python3 test_workflow.py

# Then start services (3 separate terminals):
python3 api.py                # :5000
python3 website_receiver.py   # :5001
python3 ui.py                 # Desktop app
```

## 4 Layers

| Layer | Name | What | Where |
|-------|------|------|-------|
| 1 | Affiliate Programs | Connect accounts & scrape | UI: "Layer 1 Window" |
| 2 | Affiliate Workspace | Browse & edit products | UI: "Layer 2 Window" |
| 3 | ASISCOP | Store data immutably | DB: affiliate_sources, cop_products |
| 4 | LAUNCH | AI review & human approve | API: /api/launch/* |

## Key APIs

```bash
# Add program
POST /api/affiliate-programs
{"name": "Amazon", "url": "...", "api_type": "json"}

# Submit for LAUNCH
POST /api/launch/submit
{"cop_product_id": 1}

# Approve & publish
POST /api/launch/{job_id}/approve
{"status": "human_approved"}

# Check website
GET http://localhost:5001/api/products
GET http://localhost:5001/category/electronics
```

## Database Tables (11 Total)

**Immutable Sources:**
- affiliate_programs
- affiliate_sources ← scraped products
- sales_sources
- image_supplementals

**Editable:**
- cop_products ← EDIT HERE

**Workflow:**
- publish_jobs (LAUNCH tracking)
- scrape_queue

**Org:**
- categories, subcategories
- audit_log

## AI Scoring

Quality = 50 base +
- Name quality: +15
- Description: +25
- Price: +15
- Image: +15

**Auto-approve if >= 70**

## Files (14 Total)

**Code (8)**:
- db.py, scraper.py, ai_reviewer.py, launch_controller.py
- api.py, website_receiver.py, ui.py

**Docs (4)**:
- README.md, DEPLOYMENT.md, BUILD_SUMMARY.md, this file

**Config (2)**:
- requirements.txt, setup.sh

**Data (2)**:
- schema.sql, database files

## Status Checks

```bash
# Is DB ok?
python3 -c "from db import get_db; print('✓')"

# Is API up?
curl http://localhost:5000/health

# Is website up?
curl http://localhost:5001/health

# Products published?
curl http://localhost:5001/api/products

# View logs
python3 -c "from db import get_db; c=get_db().cursor(); c.execute('SELECT COUNT(*) FROM cop_products'); print('COP products:', c.fetchone()[0])"
```

## Troubleshooting

**Port already in use**:
```bash
pkill -f 'python3 api.py'
lsof -i :5000
```

**Database locked**:
```bash
rm focus_worthy.db
python3 db.py
```

**UI won't open**:
- PyQt6 needs display. Test API directly or use X11 forwarding.

**Products not appearing**:
1. Check LAUNCH job status: `GET /api/publish-jobs?status=published`
2. Check website: `GET http://localhost:5001/api/products`
3. View logs: Check database audit_log table

## Full Workflow (7 Steps)

1. **Scrape** (Layer 1) → affiliate_sources
2. **Move** (Layer 2) → cop_products
3. **Edit** (Layer 2) → update COP fields
4. **Submit** (API) → POST /api/launch/submit
5. **AI Review** (Auto) → quality score + category
6. **Approve** (Human) → POST /api/launch/{id}/approve
7. **Publish** (Auto) → website, category page live

## Next Use After Setup

```bash
# If already running:

# Browser: http://localhost:5001/category/electronics
# CLI: curl http://localhost:5001/api/products
# Python: 
#   from db import get_db
#   c = get_db().cursor()
#   c.execute('SELECT COUNT(*) FROM cop_products WHERE status="published"')
#   print(c.fetchone())
```

## Important Paths

```
Code:      /home/alf/focus-worthy/*.py
Docs:      /home/alf/focus-worthy/*.md
Database:  /home/alf/focus-worthy/focus_worthy.db
Website:   /home/alf/focus-worthy/website.db
```

## Success Indicators

- ✅ `test_workflow.py` runs without errors
- ✅ Logs: "✓ WORKFLOW COMPLETE"
- ✅ 2 products published
- ✅ Database: 104KB focus_worthy.db
- ✅ APIs: :5000 and :5001 responding

---

**Ready to use. Read README.md for full guide.**

