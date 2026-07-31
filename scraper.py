import asyncio
import json
import hashlib
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import sqlite3
from pathlib import Path
from db import get_db

class AffiliateScrapers:
    """Universal scraper for affiliate programs"""
    
    @staticmethod
    def scrape_html(url, selectors):
        """BeautifulSoup scraper for static HTML"""
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            products = []
            
            # Example: selectors = {'container': '.product', 'name': '.title', 'price': '.price'}
            containers = soup.select(selectors.get('container', '.product'))
            
            for container in containers:
                try:
                    product = {
                        'product_name': container.select_one(selectors.get('name', '.title')).text.strip(),
                        'price': float(container.select_one(selectors.get('price', '.price')).text.replace('$', '').strip()),
                        'url': container.select_one(selectors.get('url', 'a')).get('href', ''),
                        'image_url': container.select_one(selectors.get('image', 'img')).get('src', ''),
                        'description': container.select_one(selectors.get('description', '.desc')).text.strip() if container.select_one(selectors.get('description', '.desc')) else '',
                    }
                    products.append(product)
                except Exception as e:
                    print(f"Error parsing product: {e}")
            
            return products
        except Exception as e:
            print(f"Scrape error: {e}")
            return []
    
    @staticmethod
    def scrape_json_api(url, api_key=None, headers=None):
        """JSON API scraper"""
        try:
            h = headers or {}
            if api_key:
                h['Authorization'] = f'Bearer {api_key}'
            
            response = requests.get(url, headers=h, timeout=10)
            data = response.json()
            
            # Flatten if needed
            products = data.get('products', data.get('items', []))
            return products
        except Exception as e:
            print(f"API scrape error: {e}")
            return []
    
    @staticmethod
    def generate_sku(product_name, price):
        """Generate unique SKU"""
        hash_input = f"{product_name}-{price}-{datetime.now().timestamp()}"
        return hashlib.md5(hash_input.encode()).hexdigest()[:12].upper()

class ScrapeManager:
    """Manages scraping pipeline"""
    
    def __init__(self):
        self.scrapers = AffiliateScrapers()
    
    def scrape_and_store(self, program_id, scrape_config):
        """Scrape affiliate program and store in affiliate_sources"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Get affiliate program
        cursor.execute('SELECT * FROM affiliate_programs WHERE id = ?', (program_id,))
        program = dict(cursor.fetchone())
        
        # Get scrape job
        cursor.execute('''
            INSERT INTO scrape_queue (affiliate_program_id, status, started_at)
            VALUES (?, 'running', CURRENT_TIMESTAMP)
        ''', (program_id,))
        conn.commit()
        job_id = cursor.lastrowid
        
        try:
            products = []
            
            if program['api_type'] == 'html_scrape':
                products = self.scrapers.scrape_html(
                    program['url'],
                    scrape_config.get('selectors', {})
                )
            elif program['api_type'] == 'json':
                products = self.scrapers.scrape_json_api(
                    program['url'],
                    api_key=program.get('api_key'),
                    headers=scrape_config.get('headers')
                )
            
            # Store products as affiliate_sources (immutable)
            inserted_count = 0
            for product in products:
                sku = self.scrapers.generate_sku(product['product_name'], product.get('price', 0))
                
                try:
                    cursor.execute('''
                        INSERT INTO affiliate_sources 
                        (affiliate_program_id, sku, product_name, description, price, 
                         url, image_url, category, raw_data)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (program_id, sku, product.get('product_name'),
                          product.get('description'), product.get('price'),
                          product.get('url'), product.get('image_url'),
                          product.get('category'), json.dumps(product)))
                    conn.commit()
                    inserted_count += 1
                except sqlite3.IntegrityError:
                    # SKU already exists, skip
                    pass
            
            # Update scrape job
            cursor.execute('''
                UPDATE scrape_queue
                SET status = 'completed', completed_at = CURRENT_TIMESTAMP, products_scraped = ?
                WHERE id = ?
            ''', (inserted_count, job_id))
            conn.commit()
            
            print(f"✓ Scraped {inserted_count} products from {program['name']}")
            
        except Exception as e:
            cursor.execute('''
                UPDATE scrape_queue
                SET status = 'failed', error_log = ?, completed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (str(e), job_id))
            conn.commit()
            print(f"✗ Scrape failed: {e}")
        
        finally:
            conn.close()
        
        return job_id

if __name__ == '__main__':
    manager = ScrapeManager()
    # Example: manager.scrape_and_store(1, {'selectors': {'container': '.product', 'name': '.title'}})
