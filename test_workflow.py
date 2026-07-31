#!/usr/bin/env python3
"""
Focus Worthy MVP - Full Workflow Test
Tests: Scrape → Store → COP → LAUNCH → Publish (without API servers)
"""

import json
from db import get_db
from ai_reviewer import AIReviewer

def print_section(title):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)
    print()

def demo_affiliate_programs():
    """Layer 1: Setup affiliate programs"""
    print_section("LAYER 1: AFFILIATE PROGRAMS")
    
    conn = get_db()
    cursor = conn.cursor()
    
    programs = [
        ("Amazon Associates", "https://amazon.com/products", "json"),
        ("eBay Partners", "https://ebay.com/api/products", "json"),
        ("Shopify Store", "https://shop.example.com/products", "html_scrape"),
    ]
    
    for name, url, api_type in programs:
        cursor.execute('''
            INSERT OR IGNORE INTO affiliate_programs (name, url, api_type)
            VALUES (?, ?, ?)
        ''', (name, url, api_type))
    conn.commit()
    
    cursor.execute('SELECT id, name, api_type FROM affiliate_programs')
    for row in cursor.fetchall():
        print(f"✓ {row['name']} ({row['api_type']})")
    
    conn.close()

def demo_affiliate_sources():
    """Layer 3A: Create affiliate sources (immutable)"""
    print_section("LAYER 3A: AFFILIATE SOURCES (Immutable)")
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Sample products from affiliate programs
    products = [
        {
            'affiliate_program_id': 1,
            'sku': 'IPHONE15PRO',
            'product_name': 'iPhone 15 Pro Max',
            'description': 'Latest Apple flagship smartphone with advanced camera system',
            'price': 999.99,
            'url': 'https://amazon.com/iPhone-15-Pro',
            'category': 'electronics'
        },
        {
            'affiliate_program_id': 1,
            'sku': 'MACBOOK14',
            'product_name': 'MacBook Pro 14" 2024',
            'description': 'Powerful laptop for professionals',
            'price': 1999.99,
            'url': 'https://amazon.com/MacBook-Pro-14',
            'category': 'electronics'
        },
        {
            'affiliate_program_id': 2,
            'sku': 'YOGA-MAT-001',
            'product_name': 'Premium Yoga Mat',
            'description': 'Non-slip eco-friendly yoga mat',
            'price': 49.99,
            'url': 'https://ebay.com/yoga-mat',
            'category': 'sports'
        },
        {
            'affiliate_program_id': 3,
            'sku': 'DRESS-BLUE-M',
            'product_name': 'Blue Summer Dress',
            'description': 'Comfortable and stylish summer wear',
            'price': 79.99,
            'url': 'https://shop.example.com/dress-blue',
            'category': 'fashion'
        }
    ]
    
    for prod in products:
        try:
            cursor.execute('''
                INSERT INTO affiliate_sources 
                (affiliate_program_id, sku, product_name, description, price, url, category)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (prod['affiliate_program_id'], prod['sku'], prod['product_name'],
                  prod['description'], prod['price'], prod['url'], prod['category']))
            conn.commit()
            print(f"✓ {prod['product_name']} (${prod['price']}) - {prod['category']}")
        except Exception as e:
            print(f"  (skipped: {e})")
    
    conn.close()

def demo_cop_products():
    """Layer 3: COP products (editable)"""
    print_section("LAYER 3C: COP PRODUCTS (Combined Output - Editable)")
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Move affiliate sources to COP
    cursor.execute('SELECT id, sku, product_name, description, price, category FROM affiliate_sources')
    sources = cursor.fetchall()
    
    for src in sources:
        try:
            cursor.execute('''
                INSERT INTO cop_products 
                (sku, product_name, description, price, category, affiliate_source_id, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (src['sku'], src['product_name'], src['description'],
                  src['price'], src['category'], src['id'], 'draft'))
            conn.commit()
            print(f"✓ COP: {src['product_name']} ({src['sku']})")
        except Exception as e:
            print(f"  (skipped: {e})")
    
    conn.close()

def demo_ai_review():
    """AI review of COP products"""
    print_section("LAYER 4: AI REVIEW & QUALITY SCORING")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, product_name, description, price FROM cop_products')
    products = cursor.fetchall()
    
    for prod in products:
        # AI review
        category = AIReviewer.categorize_product(prod['product_name'], prod['description'])
        quality = AIReviewer.score_quality(prod['product_name'], prod['description'], 
                                          prod['price'], 'https://example.com/img.jpg')
        
        # Update COP with AI results
        cursor.execute('''
            UPDATE cop_products
            SET ai_quality_score = ?, ai_category_suggestion = ?
            WHERE id = ?
        ''', (quality, category, prod['id']))
        conn.commit()
        
        status = "✓ PASS" if quality >= 70 else "⚠ REVIEW"
        print(f"{status} | {prod['product_name']}")
        print(f"       Quality: {quality}/100 | Category: {category}")
    
    conn.close()

def demo_launch_jobs():
    """Create LAUNCH jobs"""
    print_section("LAYER 4: LAUNCH JOBS (Publish Queue)")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM cop_products')
    cop_ids = [row['id'] for row in cursor.fetchall()]
    
    for cop_id in cop_ids:
        cursor.execute('''
            INSERT INTO publish_jobs (cop_product_id, status)
            VALUES (?, ?)
        ''', (cop_id, 'pending'))
        conn.commit()
        job_id = cursor.lastrowid
        print(f"✓ Job {job_id} created for COP #{cop_id}")
    
    # Simulate AI approval
    print()
    print("Running AI approvals...")
    cursor.execute('''
        UPDATE publish_jobs
        SET status = 'ai_approved', ai_approved = 1
        WHERE cop_product_id IN (
            SELECT id FROM cop_products WHERE ai_quality_score >= 70
        )
    ''')
    conn.commit()
    
    # Show results
    cursor.execute('''
        SELECT pj.id, cp.product_name, pj.status, pj.ai_approved
        FROM publish_jobs pj
        JOIN cop_products cp ON pj.cop_product_id = cp.id
    ''')
    
    print()
    for job in cursor.fetchall():
        status = "✓ AI APPROVED" if job['ai_approved'] else "⏳ PENDING"
        print(f"{status} | Job {job['id']}: {job['product_name']}")
    
    conn.close()

def demo_human_approval():
    """Simulate human approval"""
    print_section("LAYER 4: HUMAN APPROVAL")
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Approve first 2 jobs
    cursor.execute('''
        UPDATE publish_jobs
        SET status = 'human_approved', human_approved = 1
        WHERE ai_approved = 1
        LIMIT 2
    ''')
    conn.commit()
    
    cursor.execute('''
        SELECT pj.id, cp.product_name, pj.status, pj.human_approved
        FROM publish_jobs pj
        JOIN cop_products cp ON pj.cop_product_id = cp.id
    ''')
    
    for job in cursor.fetchall():
        status = "✓ HUMAN APPROVED" if job['human_approved'] else "⏳ WAITING"
        print(f"{status} | Job {job['id']}: {job['product_name']}")
    
    conn.close()

def demo_publish_to_website():
    """Simulate publishing to website"""
    print_section("LAYER 4: AUTO-PUBLISH TO WEBSITE")
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get human-approved jobs
    cursor.execute('''
        SELECT pj.id, pj.cop_product_id, cp.product_name, cp.ai_category_suggestion, 
               cp.category, cp.subcategory, cp.status
        FROM publish_jobs pj
        JOIN cop_products cp ON pj.cop_product_id = cp.id
        WHERE pj.human_approved = 1 AND pj.status = 'human_approved'
    ''')
    
    jobs = cursor.fetchall()
    
    for job in jobs:
        job_id = job['id']
        cop_id = job['cop_product_id']
        # Update status
        cursor.execute('''
            UPDATE publish_jobs
            SET status = 'published', published_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (job_id,))
        
        cursor.execute('''
            UPDATE cop_products
            SET status = 'published'
            WHERE id = ?
        ''', (cop_id,))
        
        conn.commit()
        
        print(f"✓ PUBLISHED | {job['product_name']}")
        print(f"  Category: {job['ai_category_suggestion'] or job['category']}")
        print(f"  Subcategory: {job['subcategory'] or 'N/A'}")
        print(f"  Status: {job['status']}")
    
    conn.close()

def demo_audit_trail():
    """Show audit log"""
    print_section("AUDIT LOG")
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT COUNT(*) as total FROM cop_products
    ''')
    print(f"✓ Total COP products: {cursor.fetchone()['total']}")
    
    cursor.execute('''
        SELECT COUNT(*) as total FROM cop_products WHERE status = 'published'
    ''')
    print(f"✓ Published products: {cursor.fetchone()['total']}")
    
    cursor.execute('''
        SELECT COUNT(*) as total FROM publish_jobs WHERE status = 'published'
    ''')
    print(f"✓ Published jobs: {cursor.fetchone()['total']}")
    
    conn.close()

def main():
    print("\n" + "=" * 60)
    print("  FOCUS WORTHY MVP - FULL WORKFLOW DEMONSTRATION")
    print("  Without API servers (testing core logic)")
    print("=" * 60)
    
    demo_affiliate_programs()
    demo_affiliate_sources()
    demo_cop_products()
    demo_ai_review()
    demo_launch_jobs()
    demo_human_approval()
    demo_publish_to_website()
    demo_audit_trail()
    
    print()
    print("=" * 60)
    print("  ✓ WORKFLOW COMPLETE")
    print("=" * 60)
    print()
    print("SUMMARY:")
    print("  1. Affiliate programs connected")
    print("  2. Products scraped → affiliate_sources (immutable)")
    print("  3. Products moved → cop_products (editable)")
    print("  4. AI reviewed & scored each product")
    print("  5. LAUNCH jobs created & AI-approved")
    print("  6. Human approved selected products")
    print("  7. Products published to website")
    print()
    print("NEXT STEPS:")
    print("  - Start Flask API (api.py on :5000)")
    print("  - Start Website API (website_receiver.py on :5001)")
    print("  - Launch PyQt desktop UI (ui.py)")
    print("  - Test via REST endpoints")
    print()

if __name__ == '__main__':
    main()
