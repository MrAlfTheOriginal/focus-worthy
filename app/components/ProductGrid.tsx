'use client';

import Image from 'next/image';
import { Product } from '@/lib/types';

interface ProductGridProps {
  products: Product[];
  onSelectProduct: (product: Product) => void;
}

/**
 * Product Grid Component
 * - 3-column responsive grid
 * - Each product shows: Name (above) + Square image + Sale price (below)
 * - Scrollable
 * - Click product to open full-screen modal
 */
export default function ProductGrid({
  products,
  onSelectProduct,
}: ProductGridProps) {
  if (products.length === 0) {
    return (
      <div className="col-span-3 text-center py-12">
        <p className="text-gray-500">No products found</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-3 gap-6">
      {products.map((product) => (
        <button
          key={product.id}
          onClick={() => onSelectProduct(product)}
          className="group cursor-pointer transition-transform hover:scale-105 text-left"
        >
          {/* Product Name (above image) */}
          <h3 className="text-cream font-medium mb-2 text-sm line-clamp-2 group-hover:text-blue-400 transition-colors">
            {product.name}
          </h3>

          {/* Product Image - Square */}
          <div className="relative w-full aspect-square bg-gray-800 rounded-lg overflow-hidden border border-gray-700 group-hover:border-blue-500 transition-colors">
            <Image
              src={product.image}
              alt={product.name}
              fill
              className="object-cover"
              sizes="(max-width: 1200px) 33vw, 25vw"
            />
          </div>

          {/* Sale Price (below image) */}
          <div className="mt-2">
            <p className="text-cream text-lg font-bold">
              ${product.salePrice.toFixed(2)}
            </p>
            {product.price !== product.salePrice && (
              <p className="text-gray-500 text-sm line-through">
                ${product.price.toFixed(2)}
              </p>
            )}
          </div>
        </button>
      ))}
    </div>
  );
}
