'use client';

import Link from 'next/link';
import { useState, useEffect } from 'react';
import { AuthState } from '@/lib/types';

/**
 * Sidebar Navigation Component
 * - Always visible on the left
 * - Contains navigation to all main pages
 * - Includes login/logout button based on auth state
 * - Styling: Cream unselected, blue on hover, purple on click, round corners
 */
export default function Sidebar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentPath, setCurrentPath] = useState('/');

  // Initialize auth state from localStorage
  useEffect(() => {
    const authState = localStorage.getItem('auth');
    if (authState) {
      const parsed: AuthState = JSON.parse(authState);
      setIsLoggedIn(parsed.isLoggedIn);
    }
    setCurrentPath(window.location.pathname);
  }, []);

  const handleLogout = () => {
    setIsLoggedIn(false);
    localStorage.removeItem('auth');
  };

  const handleLogin = () => {
    setIsLoggedIn(true);
    const authState: AuthState = { isLoggedIn: true, user: 'Guest User' };
    localStorage.setItem('auth', JSON.stringify(authState));
  };

  const navItems = [
    { label: 'Welcome', path: '/' },
    { label: 'Products', path: '/products' },
    { label: 'Special Offers', path: '/offers' },
    { label: 'Trending', path: '/trending' },
    { label: 'About Us', path: '/about' },
  ];

  return (
    <aside className="fixed left-0 top-0 h-screen w-48 bg-black border-r border-gray-700 flex flex-col p-4 gap-2">
      {/* Logo/Branding */}
      <div className="mb-4">
        <h1 className="text-cream text-xl font-bold">Focus Worthy</h1>
        <p className="text-gray-500 text-sm">Affiliate Store</p>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 space-y-2">
        {navItems.map((item) => (
          <Link
            key={item.path}
            href={item.path}
            className={`block px-4 py-2 rounded-lg transition-colors ${
              currentPath === item.path
                ? 'bg-purple-600 text-cream' // Purple on click (current page)
                : 'text-cream hover:bg-blue-600 active:bg-purple-600' // Cream unselected, blue hover, purple on click
            }`}
          >
            {item.label}
          </Link>
        ))}
      </nav>

      {/* Auth Button */}
      <div className="border-t border-gray-700 pt-4">
        <button
          onClick={isLoggedIn ? handleLogout : handleLogin}
          className="w-full px-4 py-2 rounded-lg transition-colors text-cream bg-gray-800 hover:bg-blue-600 active:bg-purple-600"
        >
          {isLoggedIn ? 'Logout' : 'Login'}
        </button>
      </div>
    </aside>
  );
}
