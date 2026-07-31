-- Focus Worthy MVP Database Schema
-- ASISCOP Pipeline: Affiliate Source | Sales Source | Image Supplementals | Combined Output Product

CREATE TABLE IF NOT EXISTS affiliate_programs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    url TEXT,
    api_type TEXT, -- 'xml', 'json', 'html_scrape'
    login_username TEXT,
    login_password TEXT, -- Consider encryption in production
    api_key TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Layer 3: ASISCOP Immutable Sources
CREATE TABLE IF NOT EXISTS affiliate_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    affiliate_program_id INTEGER NOT NULL,
    sku TEXT UNIQUE NOT NULL,
    product_name TEXT NOT NULL,
    description TEXT,
    price REAL,
    url TEXT,
    image_url TEXT,
    category TEXT,
    raw_data TEXT, -- JSON dump of full affiliate data
    source_hash TEXT, -- For deduplication
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (affiliate_program_id) REFERENCES affiliate_programs(id)
);

CREATE TABLE IF NOT EXISTS sales_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    affiliate_source_id INTEGER,
    sku TEXT UNIQUE,
    product_name TEXT,
    price REAL,
    commission_rate REAL,
    url TEXT,
    source TEXT, -- 'affiliate_api', 'manual_upload'
    raw_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (affiliate_source_id) REFERENCES affiliate_sources(id)
);

CREATE TABLE IF NOT EXISTS image_supplementals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT,
    image_url TEXT,
    alt_text TEXT,
    source TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sku) REFERENCES affiliate_sources(sku)
);

-- Layer 3: COP (Combined Output Product) - ONLY editable layer
CREATE TABLE IF NOT EXISTS cop_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku TEXT UNIQUE NOT NULL,
    product_name TEXT NOT NULL,
    description TEXT,
    price REAL,
    commission_rate REAL,
    category TEXT,
    subcategory TEXT,
    main_image_url TEXT,
    affiliate_url TEXT,
    status TEXT DEFAULT 'draft', -- 'draft', 'ready_for_launch', 'published'
    ai_quality_score REAL, -- 0-100
    ai_category_suggestion TEXT,
    ai_notes TEXT,
    human_approved BOOLEAN DEFAULT 0,
    affiliate_source_id INTEGER,
    sales_source_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (affiliate_source_id) REFERENCES affiliate_sources(id),
    FOREIGN KEY (sales_source_id) REFERENCES sales_sources(id)
);

-- Layer 4: LAUNCH stage
CREATE TABLE IF NOT EXISTS publish_jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cop_product_id INTEGER NOT NULL,
    status TEXT DEFAULT 'pending', -- 'pending', 'ai_review', 'human_review', 'published', 'failed'
    ai_approved BOOLEAN DEFAULT 0,
    human_approved BOOLEAN DEFAULT 0,
    published_at TIMESTAMP,
    website_url TEXT,
    error_log TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cop_product_id) REFERENCES cop_products(id)
);

-- Categories & Subcategories (auto-created from COP)
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    slug TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS subcategories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    slug TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    UNIQUE(category_id, name)
);

-- Audit Log
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_type TEXT, -- 'cop_product', 'affiliate_source', 'publish_job'
    entity_id INTEGER,
    action TEXT, -- 'created', 'updated', 'published'
    user TEXT,
    changes TEXT, -- JSON diff
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Scraping Queue
CREATE TABLE IF NOT EXISTS scrape_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    affiliate_program_id INTEGER NOT NULL,
    status TEXT DEFAULT 'pending', -- 'pending', 'running', 'completed', 'failed'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    products_scraped INTEGER DEFAULT 0,
    error_log TEXT,
    FOREIGN KEY (affiliate_program_id) REFERENCES affiliate_programs(id)
);

CREATE INDEX idx_affiliate_sources_sku ON affiliate_sources(sku);
CREATE INDEX idx_cop_products_status ON cop_products(status);
CREATE INDEX idx_cop_products_sku ON cop_products(sku);
CREATE INDEX idx_publish_jobs_status ON publish_jobs(status);
CREATE INDEX idx_audit_log_entity ON audit_log(entity_type, entity_id);
