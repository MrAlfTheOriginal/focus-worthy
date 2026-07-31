from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import sqlite3
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Website SQLite database
WEBSITE_DB = Path(__file__).parent / "website.db"

def init_website_db():
    """Initialize website database"""
    conn = sqlite3.connect(str(WEBSITE_DB))
    cursor = conn.cursor()
    
    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            price REAL,
            category TEXT,
            subcategory TEXT,
            image_url TEXT,
            affiliate_url TEXT,
            commission_rate REAL,
            published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS category_pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_slug TEXT UNIQUE,
            content TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_slug) REFERENCES categories(slug)
        );
    ''')
    
    conn.commit()
    conn.close()

if not WEBSITE_DB.exists():
    init_website_db()

# ==================== WEBSITE API ====================
@app.route('/api/products', methods=['POST'])
def receive_product():
    """Receive published product from affiliate platform"""
    data = request.json
    
    conn = sqlite3.connect(str(WEBSITE_DB))
    cursor = conn.cursor()
    
    try:
        # Create category if not exists
        category_name = data.get('category', 'uncategorized')
        category_slug = category_name.lower().replace(' ', '-')
        
        cursor.execute('INSERT OR IGNORE INTO categories (slug, name) VALUES (?, ?)',
                      (category_slug, category_name))
        conn.commit()
        
        # Insert product
        cursor.execute('''
            INSERT INTO products 
            (sku, name, description, price, category, subcategory, image_url, affiliate_url, commission_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data['sku'], data['name'], data.get('description'),
              data.get('price'), category_slug, data.get('subcategory'),
              data.get('image_url'), data.get('affiliate_url'), data.get('commission_rate')))
        
        conn.commit()
        product_id = cursor.lastrowid
        
        # Generate/update category page
        generate_category_page(cursor, category_slug)
        conn.commit()
        
        conn.close()
        
        return jsonify({
            'id': product_id,
            'status': 'received',
            'category_url': f'/category/{category_slug}'
        }), 201
    
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400

@app.route('/api/products', methods=['GET'])
def list_products():
    """List products by category"""
    category = request.args.get('category')
    
    conn = sqlite3.connect(str(WEBSITE_DB))
    cursor = conn.cursor()
    
    if category:
        cursor.execute('SELECT * FROM products WHERE category = ? ORDER BY published_at DESC',
                      (category,))
    else:
        cursor.execute('SELECT * FROM products ORDER BY published_at DESC')
    
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(products)

@app.route('/category/<category_slug>', methods=['GET'])
def category_page(category_slug):
    """Auto-generated category landing page"""
    conn = sqlite3.connect(str(WEBSITE_DB))
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM category_pages WHERE category_slug = ?', (category_slug,))
    page = cursor.fetchone()
    
    if page:
        conn.close()
        return page['content'], 200, {'Content-Type': 'text/html'}
    
    conn.close()
    return jsonify({'error': 'Category not found'}), 404

@app.route('/api/categories', methods=['GET'])
def list_categories():
    """List all categories"""
    conn = sqlite3.connect(str(WEBSITE_DB))
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM categories ORDER BY name')
    categories = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify(categories)

def generate_category_page(cursor, category_slug):
    """Generate HTML category page"""
    cursor.execute('SELECT name FROM categories WHERE slug = ?', (category_slug,))
    category = cursor.fetchone()
    
    if not category:
        return
    
    category_name = category['name']
    
    # Get products in category
    cursor.execute('SELECT * FROM products WHERE category = ? ORDER BY published_at DESC',
                  (category_slug,))
    products = [dict(row) for row in cursor.fetchall()]
    
    # Generate HTML
    product_html = ''.join([f'''
        <div class="product-card">
            <img src="{p['image_url']}" alt="{p['name']}">
            <h3>{p['name']}</h3>
            <p>{p.get('description', '')[:100]}...</p>
            <p class="price">${p['price']:.2f}</p>
            <a href="{p['affiliate_url']}" target="_blank" class="btn">View</a>
        </div>
    ''' for p in products])
    
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>{category_name} - Focus Worthy</title>
        <meta name="description" content="{category_name} products curated by Focus Worthy">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .products {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px; }}
            .product-card {{ border: 1px solid #ddd; padding: 15px; border-radius: 8px; }}
            .product-card img {{ width: 100%; height: 200px; object-fit: cover; }}
            .price {{ font-size: 18px; font-weight: bold; color: #27ae60; }}
            .btn {{ background: #3498db; color: white; padding: 10px 20px; border-radius: 4px; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{category_name}</h1>
            <div class="products">
                {product_html}
            </div>
        </div>
    </body>
    </html>
    '''
    
    cursor.execute('INSERT OR REPLACE INTO category_pages (category_slug, content) VALUES (?, ?)',
                  (category_slug, html))

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
