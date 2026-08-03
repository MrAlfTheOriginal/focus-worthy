from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from db import init_db, get_db
from launch_controller import LaunchController

app = Flask(__name__)
CORS(app)

# Initialize DB on startup
if not Path("focus_worthy.db").exists():
    init_db()

# ==================== AFFILIATE PROGRAMS ====================
@app.route('/api/affiliate-programs', methods=['GET'])
def list_affiliate_programs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, url, api_type FROM affiliate_programs')
    programs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(programs)

@app.route('/api/affiliate-programs', methods=['POST'])
def create_affiliate_program():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO affiliate_programs (name, url, api_type, login_username, login_password, api_key)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['name'], data.get('url'), data.get('api_type'), 
              data.get('login_username'), data.get('login_password'), data.get('api_key')))
        conn.commit()
        program_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': program_id, 'status': 'created'}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

# ==================== AFFILIATE SOURCES (IMMUTABLE) ====================
@app.route('/api/affiliate-sources', methods=['GET'])
def list_affiliate_sources():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, sku, product_name, price, category, scraped_at 
        FROM affiliate_sources
        ORDER BY scraped_at DESC
    ''')
    sources = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(sources)

@app.route('/api/affiliate-sources', methods=['POST'])
def create_affiliate_source():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO affiliate_sources 
            (affiliate_program_id, sku, product_name, description, price, url, image_url, category, raw_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['affiliate_program_id'], data['sku'], data['product_name'],
              data.get('description'), data.get('price'), data.get('url'),
              data.get('image_url'), data.get('category'), json.dumps(data.get('raw_data', {}))))
        conn.commit()
        source_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': source_id, 'status': 'created'}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

# ==================== COP PRODUCTS (EDITABLE) ====================
@app.route('/api/cop-products', methods=['GET'])
def list_cop_products():
    status = request.args.get('status', 'draft')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, sku, product_name, price, category, subcategory, status, 
               ai_quality_score, human_approved, created_at
        FROM cop_products
        WHERE status = ?
        ORDER BY created_at DESC
    ''', (status,))
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(products)

@app.route('/api/cop-products', methods=['POST'])
def create_cop_product():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO cop_products 
            (sku, product_name, description, price, commission_rate, category, subcategory, 
             main_image_url, affiliate_url, affiliate_source_id, sales_source_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['sku'], data['product_name'], data.get('description'),
              data.get('price'), data.get('commission_rate'), data.get('category'),
              data.get('subcategory'), data.get('main_image_url'), data.get('affiliate_url'),
              data.get('affiliate_source_id'), data.get('sales_source_id')))
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': product_id, 'status': 'created'}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/cop-products/<int:product_id>', methods=['PUT'])
def update_cop_product(product_id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        # Log the change
        cursor.execute('SELECT * FROM cop_products WHERE id = ?', (product_id,))
        old_data = dict(cursor.fetchone())
        
        cursor.execute('''
            UPDATE cop_products
            SET product_name = COALESCE(?, product_name),
                description = COALESCE(?, description),
                price = COALESCE(?, price),
                category = COALESCE(?, category),
                subcategory = COALESCE(?, subcategory),
                status = COALESCE(?, status),
                ai_quality_score = COALESCE(?, ai_quality_score),
                ai_category_suggestion = COALESCE(?, ai_category_suggestion),
                ai_notes = COALESCE(?, ai_notes),
                human_approved = COALESCE(?, human_approved),
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (data.get('product_name'), data.get('description'), data.get('price'),
              data.get('category'), data.get('subcategory'), data.get('status'),
              data.get('ai_quality_score'), data.get('ai_category_suggestion'),
              data.get('ai_notes'), data.get('human_approved'), product_id))
        
        conn.commit()
        conn.close()
        return jsonify({'status': 'updated'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

# ==================== PUBLISH JOBS (LAUNCH STAGE) ====================
@app.route('/api/publish-jobs', methods=['GET'])
def list_publish_jobs():
    status = request.args.get('status', 'pending')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pj.id, pj.cop_product_id, cp.product_name, pj.status, 
               pj.ai_approved, pj.human_approved, pj.created_at
        FROM publish_jobs pj
        JOIN cop_products cp ON pj.cop_product_id = cp.id
        WHERE pj.status = ?
        ORDER BY pj.created_at DESC
    ''', (status,))
    jobs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(jobs)

@app.route('/api/publish-jobs', methods=['POST'])
def create_publish_job():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO publish_jobs (cop_product_id, status)
            VALUES (?, 'pending')
        ''', (data['cop_product_id'],))
        conn.commit()
        job_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': job_id, 'status': 'created'}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/publish-jobs/<int:job_id>/approve', methods=['POST'])
def approve_publish_job(job_id):
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE publish_jobs
            SET status = ?, ai_approved = ?, human_approved = ?
            WHERE id = ?
        ''', (data.get('status', 'ai_review'), data.get('ai_approved', 0), 
              data.get('human_approved', 0), job_id))
        conn.commit()
        conn.close()
        return jsonify({'status': 'updated'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

# ==================== LAUNCH STAGE (Layer 4) ====================
@app.route('/api/launch/submit', methods=['POST'])
def launch_submit():
    """Submit COP product for LAUNCH"""
    data = request.json
    result = LaunchController.submit_for_launch(data['cop_product_id'])
    return jsonify(result), 201

@app.route('/api/launch/<int:job_id>/approve', methods=['POST'])
def launch_approve(job_id):
    """Human approves LAUNCH job"""
    result = LaunchController.human_approve(job_id)
    return jsonify(result)

@app.route('/api/launch/<int:job_id>/publish', methods=['POST'])
def launch_publish(job_id):
    """Auto-publish to website"""
    result = LaunchController.auto_publish(job_id)
    return jsonify(result)

@app.route('/api/launch/batch-publish', methods=['POST'])
def launch_batch_publish():
    """Batch publish approved jobs"""
    status_filter = request.json.get('status', 'ai_approved')
    results = LaunchController.batch_launch(status_filter)
    return jsonify({'total': len(results), 'jobs': results})

# ==================== SCRAPE QUEUE ====================
@app.route('/api/scrape-queue', methods=['POST'])
def create_scrape_job():
    data = request.json
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO scrape_queue (affiliate_program_id, status)
            VALUES (?, 'pending')
        ''', (data['affiliate_program_id'],))
        conn.commit()
        job_id = cursor.lastrowid
        conn.close()
        return jsonify({'id': job_id, 'status': 'pending'}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/scrape-queue/<int:job_id>/status', methods=['GET'])
def get_scrape_status(job_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scrape_queue WHERE id = ?', (job_id,))
    job = dict(cursor.fetchone())
    conn.close()
    return jsonify(job)

# ==================== CATEGORIES & SUBCATEGORIES ====================
@app.route('/api/categories', methods=['GET'])
def list_categories():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, slug FROM categories')
    categories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(categories)

@app.route('/api/categories/<int:category_id>/subcategories', methods=['GET'])
def list_subcategories(category_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, slug FROM subcategories WHERE category_id = ?', (category_id,))
    subcategories = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(subcategories)

# ==================== HEALTH CHECK ====================
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
