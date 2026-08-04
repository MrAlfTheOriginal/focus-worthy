import React from 'react';

export default function ComingSoon() {
  return (
    <div className="min-h-screen bg-black text-cream flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl text-center space-y-8">
        {/* Logo/Branding */}
        <div className="space-y-4">
          <h1 className="text-5xl font-bold text-cream">Focus Worthy</h1>
          <p className="text-xl text-light-grey">A Review Site With Integrity</p>
        </div>

        {/* Main Message */}
        <div className="space-y-6 border border-dark-grey rounded-lg p-8 bg-gray-900">
          <h2 className="text-3xl font-bold text-cream">Coming Soon</h2>
          
          <p className="text-lg text-gray-300 leading-relaxed">
            We're building a review site with integrity to help you shop for the products you love with full transparency about what you're buying.
          </p>

          <div className="space-y-4 text-gray-400">
            <div className="flex gap-4">
              <span className="text-blue-500 text-2xl">✓</span>
              <p>Honest, unbiased product reviews</p>
            </div>
            <div className="flex gap-4">
              <span className="text-blue-500 text-2xl">✓</span>
              <p>Full transparency on what you're buying</p>
            </div>
            <div className="flex gap-4">
              <span className="text-blue-500 text-2xl">✓</span>
              <p>Curated deals from trusted sources</p>
            </div>
            <div className="flex gap-4">
              <span className="text-blue-500 text-2xl">✓</span>
              <p>Shop with confidence</p>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-gray-500 text-sm">
          <p>We're working hard to launch. Check back soon.</p>
        </div>
      </div>
    </div>
  );
}
