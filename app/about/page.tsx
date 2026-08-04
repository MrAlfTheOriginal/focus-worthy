'use client';

/**
 * About Us Page
 * - Static page with placeholder text
 * - Information about Focus Worthy
 */
export default function AboutPage() {
  return (
    <div className="p-8 max-w-4xl">
      {/* Header */}
      <h1 className="text-4xl font-bold text-cream mb-8">About Focus Worthy</h1>

      {/* Introduction */}
      <section className="mb-12 space-y-4">
        <p className="text-lg text-gray-300 leading-relaxed">
          Focus Worthy is a premier affiliate marketplace dedicated to bringing
          you the best products across multiple categories. Founded with the
          mission to simplify shopping and connect consumers with quality items,
          we've built a curated platform that prioritizes your needs.
        </p>
        <p className="text-lg text-gray-300 leading-relaxed">
          Whether you're searching for cutting-edge electronics, trendy fashion,
          home & garden essentials, or any other product category, Focus Worthy
          serves as your trusted gateway to quality, value, and convenience.
        </p>
      </section>

      {/* Mission Section */}
      <section className="mb-12 bg-gray-900 rounded-lg p-8">
        <h2 className="text-2xl font-bold text-cream mb-4">Our Mission</h2>
        <p className="text-gray-300 leading-relaxed">
          At Focus Worthy, our mission is to empower consumers by providing
          access to carefully selected products from reputable brands and
          sellers. We focus on quality, value, and transparency in every
          transaction. Our goal is to make online shopping easier, more
          enjoyable, and more rewarding for everyone.
        </p>
      </section>

      {/* Values Section */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-cream mb-6">Our Values</h2>
        <div className="grid grid-cols-2 gap-6">
          {/* Quality */}
          <div className="bg-gray-900 rounded-lg p-6">
            <h3 className="text-cream font-bold mb-2 text-lg">Quality First</h3>
            <p className="text-gray-400">
              We meticulously curate every product to ensure it meets our high
              standards for quality and durability.
            </p>
          </div>

          {/* Trust */}
          <div className="bg-gray-900 rounded-lg p-6">
            <h3 className="text-cream font-bold mb-2 text-lg">Trust & Transparency</h3>
            <p className="text-gray-400">
              We believe in honest communication and transparent dealings with
              our customers. Your trust is our priority.
            </p>
          </div>

          {/* Value */}
          <div className="bg-gray-900 rounded-lg p-6">
            <h3 className="text-cream font-bold mb-2 text-lg">Best Value</h3>
            <p className="text-gray-400">
              We continuously seek out the best deals and exclusive offers to
              ensure you get the most value for your money.
            </p>
          </div>

          {/* Innovation */}
          <div className="bg-gray-900 rounded-lg p-6">
            <h3 className="text-cream font-bold mb-2 text-lg">Innovation</h3>
            <p className="text-gray-400">
              We're constantly improving our platform and expanding our product
              selection to meet evolving customer needs.
            </p>
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="mb-12">
        <h2 className="text-2xl font-bold text-cream mb-6">
          Why Choose Focus Worthy?
        </h2>
        <ul className="space-y-4">
          <li className="flex gap-3 items-start">
            <span className="text-blue-500 font-bold mt-1">✓</span>
            <span className="text-gray-300">
              <strong className="text-cream">Wide Selection:</strong> Access thousands of
              products across multiple categories, all in one place.
            </span>
          </li>
          <li className="flex gap-3 items-start">
            <span className="text-blue-500 font-bold mt-1">✓</span>
            <span className="text-gray-300">
              <strong className="text-cream">Competitive Pricing:</strong> We work with
              trusted partners to bring you competitive prices and exclusive deals.
            </span>
          </li>
          <li className="flex gap-3 items-start">
            <span className="text-blue-500 font-bold mt-1">✓</span>
            <span className="text-gray-300">
              <strong className="text-cream">Easy Navigation:</strong> Our intuitive
              interface makes it easy to find exactly what you're looking for.
            </span>
          </li>
          <li className="flex gap-3 items-start">
            <span className="text-blue-500 font-bold mt-1">✓</span>
            <span className="text-gray-300">
              <strong className="text-cream">Secure Shopping:</strong> Your security and
              privacy are paramount. We implement industry-leading security measures.
            </span>
          </li>
          <li className="flex gap-3 items-start">
            <span className="text-blue-500 font-bold mt-1">✓</span>
            <span className="text-gray-300">
              <strong className="text-cream">Dedicated Support:</strong> Our customer
              service team is always ready to help with any questions or concerns.
            </span>
          </li>
        </ul>
      </section>

      {/* Contact Section */}
      <section className="bg-blue-600 rounded-lg p-8 text-cream">
        <h2 className="text-2xl font-bold mb-4">Get in Touch</h2>
        <p className="mb-4">
          Have questions or feedback? We'd love to hear from you. Contact our
          team anytime.
        </p>
        <div className="space-y-2">
          <p>Email: info@focusworthy.com</p>
          <p>Phone: 1-800-FOCUS-WORTHY</p>
          <p>Address: 123 Commerce Street, Digital City, DC 12345</p>
        </div>
      </section>
    </div>
  );
}
