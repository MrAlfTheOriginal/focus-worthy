'use client';

import { useState } from 'react';
import SearchBar from '@/app/components/SearchBar';

/**
 * Welcome (Homepage)
 * - Full-width text explaining Focus Worthy (placeholder Lorem ipsum)
 * - Placeholder images inline with margin
 * - Search bar at top (searches entire site, logs searches to console)
 */
export default function WelcomePage() {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    // In a real implementation, this would search all products
    console.log(`[WELCOME SEARCH] Searching entire site for: "${query}"`);
  };

  return (
    <div className="p-8">
      {/* Search Bar */}
      <div className="mb-8">
        <SearchBar
          onSearch={handleSearch}
          placeholder="Search entire site..."
        />
      </div>

      {/* Hero Section */}
      <section className="mb-12">
        <h1 className="text-4xl font-bold text-cream mb-6">
          Welcome to Focus Worthy
        </h1>
        <p className="text-lg text-gray-300 leading-relaxed mb-4">
          Focus Worthy is your premier destination for quality products across
          multiple categories. We bring together the best electronics, fashion,
          home & garden items, and more - all curated with your needs in mind.
        </p>
        <p className="text-lg text-gray-300 leading-relaxed">
          Our affiliate platform connects you with trusted products and exclusive
          deals. Whether you're looking for the latest tech gadgets, stylish
          clothing, or home decor, Focus Worthy has something for everyone.
        </p>
      </section>

      {/* Featured Sections with Images */}
      <div className="grid grid-cols-3 gap-8 mb-12">
        {/* Electronics Section */}
        <div className="space-y-4">
          <div className="w-full aspect-video bg-gray-800 rounded-lg border border-gray-700 flex items-center justify-center overflow-hidden">
            <svg
              className="w-full h-full text-gray-600"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-cream">Electronics</h2>
          <p className="text-gray-400 text-sm">
            Discover cutting-edge gadgets and devices from phones to laptops.
          </p>
        </div>

        {/* Fashion Section */}
        <div className="space-y-4">
          <div className="w-full aspect-video bg-gray-800 rounded-lg border border-gray-700 flex items-center justify-center overflow-hidden">
            <svg
              className="w-full h-full text-gray-600"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M6 4h12v2H6V4zm1 3h10l1.5 9h-13L7 7z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-cream">Fashion</h2>
          <p className="text-gray-400 text-sm">
            Explore trendy clothing and accessories for men and women.
          </p>
        </div>

        {/* Home & Garden Section */}
        <div className="space-y-4">
          <div className="w-full aspect-video bg-gray-800 rounded-lg border border-gray-700 flex items-center justify-center overflow-hidden">
            <svg
              className="w-full h-full text-gray-600"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" />
            </svg>
          </div>
          <h2 className="text-xl font-bold text-cream">Home & Garden</h2>
          <p className="text-gray-400 text-sm">
            Transform your space with quality furniture and decor items.
          </p>
        </div>
      </div>

      {/* Content Section */}
      <section className="space-y-6 bg-gray-900 rounded-lg p-8">
        <h2 className="text-2xl font-bold text-cream">Why Choose Focus Worthy?</h2>

        <div className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
              <span className="text-cream font-bold">✓</span>
            </div>
            <div>
              <h3 className="text-cream font-semibold mb-1">Curated Selection</h3>
              <p className="text-gray-400">
                We carefully select products that meet our quality standards and
                offer genuine value to our customers.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
              <span className="text-cream font-bold">✓</span>
            </div>
            <div>
              <h3 className="text-cream font-semibold mb-1">Best Prices</h3>
              <p className="text-gray-400">
                Find exclusive deals and special offers on products you love.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center">
              <span className="text-cream font-bold">✓</span>
            </div>
            <div>
              <h3 className="text-cream font-semibold mb-1">Trusted Partners</h3>
              <p className="text-gray-400">
                We partner with reputable brands and sellers to ensure quality
                and reliability.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
