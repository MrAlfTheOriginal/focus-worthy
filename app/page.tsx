'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to coming soon page
    router.push('/coming-soon');
  }, [router]);

  return null; // This page redirects, nothing to render
}
