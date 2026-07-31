"""
LAUNCH Stage: Final pipeline before publishing to website
Orchestrates: AI Review → Human Approval → Website Publishing
"""

import json
import requests
from db import get_db
from ai_reviewer import AIReviewer, PublishEngine

WEBSITE_API = "http://localhost:5001"

class LaunchController:
    """Coordinates LAUNCH stage (Layer 4)"""
    
    @staticmethod
    def submit_for_launch(cop_product_id):
        """Submit COP product for LAUNCH review"""
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            # Get COP product
            cursor.execute('SELECT * FROM cop_products WHERE id = ?', (cop_product_id,))
            product = dict(cursor.fetchone())
            
            # Create publish job
            cursor.execute('''
                INSERT INTO publish_jobs (cop_product_id, status)
                VALUES (?, 'pending')
            ''', (cop_product_id,))
            conn.commit()
            job_id = cursor.lastrowid
            
            # AI review
            ai_result = AIReviewer.review_and_auto_approve(cop_product_id)
            
            # Update product with AI review
            cursor.execute('''
                UPDATE cop_products
                SET ai_quality_score = ?, ai_category_suggestion = ?
                WHERE id = ?
            ''', (ai_result['quality_score'], ai_result['category'], cop_product_id))
            conn.commit()
            
            # Update job status
            if ai_result['quality_score'] >= 70:
                cursor.execute('''
                    UPDATE publish_jobs
                    SET status = 'ai_approved', ai_approved = 1
                    WHERE id = ?
                ''', (job_id,))
                conn.commit()
                print(f"✓ AI approved job {job_id} (quality: {ai_result['quality_score']}/100)")
            else:
                cursor.execute('''
                    UPDATE publish_jobs
                    SET status = 'needs_review', ai_approved = 0
                    WHERE id = ?
                ''', (job_id,))
                conn.commit()
                print(f"⚠ AI review needed: quality {ai_result['quality_score']}/100")
            
            return {
                'job_id': job_id,
                'status': 'ai_approved' if ai_result['quality_score'] >= 70 else 'needs_review',
                'quality_score': ai_result['quality_score'],
                'category': ai_result['category']
            }
        
        finally:
            conn.close()
    
    @staticmethod
    def human_approve(job_id):
        """Human approves publish job"""
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE publish_jobs
                SET status = 'human_approved', human_approved = 1
                WHERE id = ?
            ''', (job_id,))
            conn.commit()
            print(f"✓ Human approved job {job_id}")
            
            # Auto-publish if AI also approved
            cursor.execute('SELECT * FROM publish_jobs WHERE id = ?', (job_id,))
            job = dict(cursor.fetchone())
            
            if job['ai_approved']:
                return LaunchController.auto_publish(job_id)
            else:
                return {'status': 'human_approved', 'next_step': 'awaiting_ai_review'}
        
        finally:
            conn.close()
    
    @staticmethod
    def auto_publish(job_id):
        """Auto-publish to website"""
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT pj.*, cp.* FROM publish_jobs pj
                JOIN cop_products cp ON pj.cop_product_id = cp.id
                WHERE pj.id = ?
            ''', (job_id,))
            
            result = cursor.fetchone()
            if not result:
                return {'error': 'Job not found'}
            
            product = dict(result)
            
            # Prepare payload for website
            payload = {
                'sku': product['sku'],
                'name': product['product_name'],
                'description': product['description'],
                'price': product['price'],
                'category': product['ai_category_suggestion'] or product['category'],
                'subcategory': product['subcategory'],
                'image_url': product['main_image_url'],
                'affiliate_url': product['affiliate_url'],
                'commission_rate': product['commission_rate']
            }
            
            # POST to website API
            try:
                response = requests.post(f'{WEBSITE_API}/api/products', json=payload, timeout=10)
                response.raise_for_status()
                website_data = response.json()
                
                # Update publish job
                cursor.execute('''
                    UPDATE publish_jobs
                    SET status = 'published', published_at = CURRENT_TIMESTAMP, website_url = ?
                    WHERE id = ?
                ''', (website_data.get('category_url'), job_id))
                
                # Update COP product status
                cursor.execute('''
                    UPDATE cop_products
                    SET status = 'published'
                    WHERE id = ?
                ''', (product['cop_product_id'],))
                
                conn.commit()
                
                print(f"✓ Published to website: {website_data.get('category_url')}")
                
                return {
                    'status': 'published',
                    'website_url': website_data.get('category_url'),
                    'category': payload['category']
                }
            
            except requests.RequestException as e:
                cursor.execute('''
                    UPDATE publish_jobs
                    SET status = 'failed', error_log = ?
                    WHERE id = ?
                ''', (str(e), job_id))
                conn.commit()
                return {'status': 'failed', 'error': str(e)}
        
        finally:
            conn.close()
    
    @staticmethod
    def batch_launch(status_filter='ai_approved'):
        """Batch process LAUNCH jobs"""
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT id FROM publish_jobs WHERE status = ?', (status_filter,))
            jobs = [row['id'] for row in cursor.fetchall()]
            
            results = []
            for job_id in jobs:
                result = LaunchController.auto_publish(job_id)
                results.append({'job_id': job_id, 'result': result})
            
            return results
        
        finally:
            conn.close()

if __name__ == '__main__':
    # Example workflow
    # 1. Submit for launch
    result = LaunchController.submit_for_launch(1)
    print(f"LAUNCH submission: {result}")
    
    # 2. Get job ID from result
    job_id = result['job_id']
    
    # 3. Human approves (would be triggered from UI)
    # approve_result = LaunchController.human_approve(job_id)
    # print(f"Human approval result: {approve_result}")
