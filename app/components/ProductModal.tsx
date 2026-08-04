'use client';

import Image from 'next/image';
import { Product } from '@/lib/types';

interface ProductModalProps {
  product: Product | null;
  onClose: () => void;
}

/**
 * Product Detail Modal Component
 * - Full-screen modal showing complete product details
 * - Menu stays visible behind modal (handled by parent)
 * - Shows all specs and pricing
 * - Click outside or close button to dismiss
 */
export default function ProductModal({ product, onClose }: ProductModalProps) {
  if (!product) return null;

  return (
    <div
      className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
      onClick={onClose}
    >
      {/* Modal Content */}
      <div
        className="bg-gray-900 rounded-lg max-w-2xl w-full max-h-96 overflow-y-auto relative"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-400 hover:text-cream transition-colors z-10"
        >
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>

        {/* Content Grid */}
        <div className="grid grid-cols-2 gap-6 p-8">
          {/* Image */}
          <div className="relative aspect-square">
            <Image
              src={product.image}
              alt={product.name}
              fill
              className="object-cover rounded-lg"
              sizes="(max-width: 768px) 100vw, 50vw"
            />
          </div>

          {/* Details */}
          <div className="flex flex-col gap-4">
            {/* Name */}
            <div>
              <h2 className="text-cream text-3xl font-bold mb-2">
                {product.name}
              </h2>
            </div>

            {/* Price */}
            <div className="border-b border-gray-700 pb-4">
              <div className="flex items-baseline gap-2 mb-2">
                <p className="text-cream text-4xl font-bold">
                  ${product.salePrice.toFixed(2)}
                </p>
                {product.price !== product.salePrice && (
                  <p className="text-gray-500 text-lg line-through">
                    ${product.price.toFixed(2)}
                  </p>
                )}
              </div>
              {product.price !== product.salePrice && (
                <p className="text-blue-400 text-sm font-medium">
                  Save ${(product.price - product.salePrice).toFixed(2)}!
                </p>
              )}
            </div>

            {/* Description */}
            <div>
              <h3 className="text-cream text-sm font-semibold mb-2">
                Description
              </h3>
              <p className="text-gray-300 text-sm">{product.description}</p>
            </div>

            {/* Specs */}
            <div>
              <h3 className="text-cream text-sm font-semibold mb-2">
                Specifications
              </h3>
              <ul className="space-y-1 text-sm text-gray-300">
                {Object.entries(product.specs).map(([key, value]) => (
                  <li key={key} className="flex justify-between">
                    <span className="text-gray-500">{key}:</span>
                    <span className="text-cream">{value}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Action Button */}
            <div className="mt-auto pt-4 border-t border-gray-700">
              <button className="w-full bg-blue-600 hover:bg-blue-700 text-cream font-medium py-2 rounded-lg transition-colors">
                Add to Cart
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
