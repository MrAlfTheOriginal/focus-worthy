import json
from db import get_db
import hashlib

class AIReviewer:
    """AI-driven product review and categorization"""
    
    CATEGORY_KEYWORDS = {
        'electronics': ['phone', 'laptop', 'tablet', 'headphones', 'speaker', 'camera', 'monitor'],
        'fashion': ['dress', 'shirt', 'pants', 'jacket', 'shoes', 'hat', 'bag', 'watch'],
        'home': ['furniture', 'lamp', 'rug', 'bedding', 'pillow', 'towel', 'kitchenware'],
        'sports': ['running', 'yoga', 'gym', 'bike', 'skateboard', 'soccer', 'basketball'],
        'beauty': ['skincare', 'makeup', 'shampoo', 'lotion', 'perfume', 'cosmetics'],
        'books': ['book', 'novel', 'ebook', 'audiobook'],
        'toys': ['toy', 'game', 'puzzle', 'lego', 'doll'],
    }
    
    @staticmethod
    def categorize_product(product_name, description):
        """Auto-categorize based on keywords"""
        text = f"{product_name} {description}".lower()
        scores = {}
        
        for category, keywords in AIReviewer.CATEGORY_KEYWORDS.items():
            matches = sum(1 for kw in keywords if kw.lower() in text)
            scores[category] = matches
        
        best_category = max(scores, key=scores.get) if max(scores.values()) > 0 else 'uncategorized'
        return best_category
    
    @staticmethod
    def score_quality(product_name, description, price, image_url):
        """Score product quality 0-100"""
        score = 50  # baseline
        
        # Name quality
        if product_name and len(product_name) > 5 and len(product_name) < 200:
            score += 15
        
        # Description quality
        if description and len(description) > 20:
            score += 15
        if description and len(description) > 100:
            score += 10
        
        # Price validity
        if price and 0.99 < price < 100000:
            score += 15
        
        # Image
        if image_url:
            score += 15
        
        # Cap at 100
        return min(score, 100)
    
    @staticmethod
    def review_and_auto_approve(cop_product_id):
        """AI review of COP product"""
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM cop_products WHERE id = ?', (cop_product_id,))
            product = dict(cursor.fetchone())
            
            # Auto-categorize
            category = AIReviewer.categorize_product(
                product['product_name'],
                product.get('description', '')
            )
            
            # Score quality
            quality_score = AIReviewer.score_quality(
                product['product_name'],
                product.get('description', ''),
                product.get('price'),
                product.get('main_image_url')
            )
            
            # Auto-approve if quality >= 70
            ai_approved = quality_score >= 70
            
            # Update COP product
            cursor.execute('''
                UPDATE cop_products
                SET ai_quality_score = ?, 
                    ai_category_suggestion = ?,
                    ai_notes = ?
                WHERE id = ?
            ''', (quality_score, category, f'Quality: {quality_score}/100. Category: {category}', cop_product_id))
            
            conn.commit()
            
            return {
                'quality_score': quality_score,
                'category': category,
                'ai_approved': ai_approved
            }
        
        finally:
            conn.close()

class PublishEngine:
    """Handles publishing to website"""
    
    @staticmethod
    def publish_product(cop_product_id, website_api_url):
        """Publish approved product to website"""
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT * FROM cop_products WHERE id = ?', (cop_product_id,))
            product = dict(cursor.fetchone())
            
            # Prepare payload
            payload = {
                'sku': product['sku'],
                'name': product['product_name'],
                'description': product['description'],
                'price': product['price'],
                'category': product['category'],
                'subcategory': product['subcategory'],
                'image_url': product['main_image_url'],
                'affiliate_url': product['affiliate_url'],
                'commission_rate': product['commission_rate']
            }
            
            # TODO: POST to website_api_url/api/products
            # For MVP, just mark as published
            
            cursor.execute('''
                UPDATE cop_products
                SET status = 'published'
                WHERE id = ?
            ''', (cop_product_id,))
            
            cursor.execute('''
                UPDATE publish_jobs
                SET status = 'published', published_at = CURRENT_TIMESTAMP
                WHERE cop_product_id = ?
            ''', (cop_product_id,))
            
            conn.commit()
            
            return {
                'status': 'published',
                'payload': payload
            }
        
        finally:
            conn.close()

if __name__ == '__main__':
    # Test
    print(AIReviewer.categorize_product('iPhone 15 Pro Max', 'Latest Apple smartphone'))
    print(AIReviewer.score_quality('iPhone 15 Pro Max', 'Latest Apple smartphone with great camera', 999.99, 'https://example.com/iphone.jpg'))
