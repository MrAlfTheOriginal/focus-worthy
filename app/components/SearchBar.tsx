'use client';

import { useState } from 'react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  placeholder?: string;
}

/**
 * Search Bar Component
 * - Logs all searches to console for scraper logging
 * - For Products/Offers/Trending: searches only current category
 * - For Welcome: searches entire site
 */
export default function SearchBar({
  onSearch,
  placeholder = 'Search...',
}: SearchBarProps) {
  const [query, setQuery] = useState('');

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    
    // Log search to console for scraper logging later
    if (value.trim()) {
      console.log(`[SEARCH LOG] Query: "${value}" at ${new Date().toISOString()}`);
    }
    
    // Trigger search callback
    onSearch(value);
  };

  const handleClear = () => {
    setQuery('');
    onSearch('');
  };

  return (
    <div className="w-full bg-gray-800 rounded-lg p-3 flex items-center gap-2 border border-gray-700">
      {/* Search Icon */}
      <svg
        className="w-5 h-5 text-gray-500"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
        />
      </svg>

      {/* Input */}
      <input
        type="text"
        value={query}
        onChange={handleSearch}
        placeholder={placeholder}
        className="flex-1 bg-transparent text-cream outline-none placeholder-gray-500"
      />

      {/* Clear Button */}
      {query && (
        <button
          onClick={handleClear}
          className="text-gray-500 hover:text-cream transition-colors"
          aria-label="Clear search"
        >
          ✕
        </button>
      )}
    </div>
  );
}
