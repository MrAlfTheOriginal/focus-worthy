'use client';

import { useState } from 'react';
import { Category, SubCategory } from '@/lib/types';

interface CategoryTreeProps {
  categories: Category[];
  onSelectCategory: (categoryId: string) => void;
  selectedCategory: string | null;
}

/**
 * Category Tree Menu Component
 * - Multi-level navigation: Categories → Subcategories → Items
 * - Collapsible categories
 * - Click to select and show products
 * - Styling: Dark grey boxes, lighter grey on hover/select
 */
export default function CategoryTree({
  categories,
  onSelectCategory,
  selectedCategory,
}: CategoryTreeProps) {
  const [expandedCategories, setExpandedCategories] = useState<string[]>([]);
  const [expandedSubcategories, setExpandedSubcategories] = useState<string[]>([]);

  const toggleCategory = (categoryId: string) => {
    setExpandedCategories((prev) =>
      prev.includes(categoryId)
        ? prev.filter((id) => id !== categoryId)
        : [...prev, categoryId]
    );
  };

  const toggleSubcategory = (subcategoryId: string) => {
    setExpandedSubcategories((prev) =>
      prev.includes(subcategoryId)
        ? prev.filter((id) => id !== subcategoryId)
        : [...prev, subcategoryId]
    );
  };

  const handleSelectItem = (itemId: string) => {
    onSelectCategory(itemId);
  };

  return (
    <div className="bg-gray-900 rounded-lg p-4 space-y-2 max-h-96 overflow-y-auto">
      {categories.map((category) => (
        <div key={category.id} className="space-y-1">
          {/* Main Category */}
          <button
            onClick={() => toggleCategory(category.id)}
            className={`w-full text-left px-3 py-2 rounded-lg transition-colors flex items-center justify-between ${
              selectedCategory === category.id
                ? 'bg-gray-600 text-cream' // Lighter grey on select
                : 'bg-gray-800 text-cream hover:bg-gray-700'
            }`}
          >
            <span className="font-medium">{category.name}</span>
            <span
              className={`text-sm transition-transform ${
                expandedCategories.includes(category.id) ? 'rotate-180' : ''
              }`}
            >
              ▼
            </span>
          </button>

          {/* Subcategories */}
          {expandedCategories.includes(category.id) && (
            <div className="ml-4 space-y-1">
              {category.subcategories.map((subcategory) => (
                <div key={subcategory.id} className="space-y-1">
                  {/* Subcategory Header */}
                  <button
                    onClick={() => toggleSubcategory(subcategory.id)}
                    className={`w-full text-left px-3 py-2 rounded-lg transition-colors flex items-center justify-between text-sm ${
                      selectedCategory === subcategory.id
                        ? 'bg-gray-600 text-cream'
                        : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
                    }`}
                  >
                    <span>{subcategory.name}</span>
                    <span
                      className={`text-xs transition-transform ${
                        expandedSubcategories.includes(subcategory.id)
                          ? 'rotate-180'
                          : ''
                      }`}
                    >
                      ▼
                    </span>
                  </button>

                  {/* Items */}
                  {expandedSubcategories.includes(subcategory.id) && (
                    <div className="ml-4 space-y-1">
                      {subcategory.items.map((item) => (
                        <button
                          key={item.id}
                          onClick={() => handleSelectItem(item.id)}
                          className={`w-full text-left px-3 py-2 rounded-lg transition-colors text-xs ${
                            selectedCategory === item.id
                              ? 'bg-blue-600 text-cream' // Blue for selected items
                              : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                          }`}
                        >
                          {item.name}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
