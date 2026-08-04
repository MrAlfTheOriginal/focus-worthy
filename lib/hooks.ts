'use client';

import { useEffect, useState } from 'react';
import { Category, Product } from '@/lib/types';

/**
 * Hook to fetch categories
 * Currently uses local JSON file (/public/data/categories.json)
 * 
 * PRODUCTION: Uncomment the API call below and comment out the local file fetch
 * API_URL: http://localhost:5000/api/categories
 * 
 * Replace the fetch call with:
 * const response = await fetch('http://localhost:5000/api/categories');
 */
export const useCategories = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        // LOCAL TESTING: Using JSON file
        const response = await fetch('/data/categories.json');
        
        // PRODUCTION: Uncomment below and comment out above
        // const response = await fetch('http://localhost:5000/api/categories');
        
        if (!response.ok) throw new Error('Failed to fetch categories');
        const data = await response.json();
        setCategories(data.categories);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
        setCategories([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCategories();
  }, []);

  return { categories, loading, error };
};

/**
 * Hook to fetch products
 * Currently uses local JSON file (/public/data/products.json)
 * 
 * PRODUCTION: Uncomment the API call below and comment out the local file fetch
 * API_URL: http://localhost:5000/api/products
 * 
 * Replace the fetch call with:
 * const response = await fetch('http://localhost:5000/api/products');
 */
export const useProducts = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        // LOCAL TESTING: Using JSON file
        const response = await fetch('/data/products.json');
        
        // PRODUCTION: Uncomment below and comment out above
        // const response = await fetch('http://localhost:5000/api/products');
        
        if (!response.ok) throw new Error('Failed to fetch products');
        const data = await response.json();
        setProducts(data);
        setError(null);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return { products, loading, error };
};

/**
 * Filter products by category ID
 */
export const filterProductsByCategory = (
  products: Product[],
  categoryId: string
): Product[] => {
  return products.filter((product) => product.categoryId === categoryId);
};

/**
 * Search products by name (case-insensitive)
 */
export const searchProducts = (
  products: Product[],
  query: string
): Product[] => {
  if (!query.trim()) return products;
  
  const lowerQuery = query.toLowerCase();
  return products.filter((product) =>
    product.name.toLowerCase().includes(lowerQuery)
  );
};
