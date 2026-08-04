'use client';

import { useState, useEffect } from 'react';
import SearchBar from '@/app/components/SearchBar';
import CategoryTree from '@/app/components/CategoryTree';
import ProductGrid from '@/app/components/ProductGrid';
import ProductModal from '@/app/components/ProductModal';
import { Category, Product } from '@/lib/types';

/**
 * Trending Page
 * - Same structure as Products page
 * - Shows trending/popular products (demo: items in phones, mens, furniture categories)
 * - Dynamic category tree + grid layout
 * - Search within trending
 */
export default function TrendingPage() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [selectedCategoryId, setSelectedCategoryId] = useState<string | null>(
    null
  );
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);

  // Fetch categories and products
  useEffect(() => {
    const fetchData = async () => {
      try {
        // LOCAL TESTING: Using JSON files
        const [categoriesRes, productsRes] = await Promise.all([
          fetch('/data/categories.json'),
          fetch('/data/products.json'),
        ]);

        // PRODUCTION: Uncomment below and comment out above
        // const [categoriesRes, productsRes] = await Promise.all([
        //   fetch('http://localhost:5000/api/categories'),
        //   fetch('http://localhost:5000/api/products'),
        // ]);

        if (!categoriesRes.ok || !productsRes.ok) {
          throw new Error('Failed to fetch data');
        }

        const categoriesData = await categoriesRes.json();
        let productsData = await productsRes.json();

        // Filter to trending products (demo: high-price items and selected categories)
        const trendingCategories = ['phones', 'mens', 'furniture', 'decor'];
        productsData = productsData.filter((p: Product) =>
          trendingCategories.includes(p.categoryId)
        );

        setCategories(categoriesData.categories);
        setProducts(productsData);
      } catch (err) {
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Find products for selected category
  const getProductsForCategory = (): Product[] => {
    if (!selectedCategoryId) return products;

    return products.filter(
      (p) =>
        p.categoryId === selectedCategoryId ||
        categories
          .flatMap((c) => c.subcategories)
          .some(
            (s) =>
              s.id === selectedCategoryId &&
              s.items.some((i) => i.id === p.categoryId)
          )
    );
  };

  let displayedProducts = getProductsForCategory();

  // Search within category
  if (searchQuery.trim()) {
    const lowerQuery = searchQuery.toLowerCase();
    displayedProducts = displayedProducts.filter((p) =>
      p.name.toLowerCase().includes(lowerQuery)
    );
    console.log(
      `[TRENDING SEARCH] Query: "${searchQuery}" - Found ${displayedProducts.length} results`
    );
  }

  const handleSearch = (query: string) => {
    setSearchQuery(query);
  };

  if (loading) {
    return (
      <div className="p-8 text-center text-gray-400">
        Loading trending products...
      </div>
    );
  }

  return (
    <div className="p-8">
      {/* Search Bar */}
      <div className="mb-8">
        <SearchBar
          onSearch={handleSearch}
          placeholder="Search trending..."
        />
      </div>

      {/* Main Layout: Category Tree + Grid */}
      <div className="grid grid-cols-4 gap-8">
        {/* Category Tree Sidebar */}
        <div>
          <h2 className="text-cream text-lg font-bold mb-4">Categories</h2>
          <CategoryTree
            categories={categories}
            onSelectCategory={setSelectedCategoryId}
            selectedCategory={selectedCategoryId}
          />
        </div>

        {/* Product Grid */}
        <div className="col-span-3">
          {selectedCategoryId ? (
            <div>
              <h2 className="text-cream text-2xl font-bold mb-2">
                Trending Now
              </h2>
              <p className="text-gray-400 mb-6">
                {displayedProducts.length} trending item{displayedProducts.length !== 1 ? 's' : ''} in this category
              </p>
              <ProductGrid
                products={displayedProducts}
                onSelectProduct={setSelectedProduct}
              />
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-400 text-lg">
                Select a category to view trending products
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Product Modal */}
      <ProductModal
        product={selectedProduct}
        onClose={() => setSelectedProduct(null)}
      />
    </div>
  );
}
