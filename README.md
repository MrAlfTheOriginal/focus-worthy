# Focus Worthy - Affiliate Platform Website

A modern Next.js 15 website for the Focus Worthy affiliate platform, built with React, TypeScript, and Tailwind CSS.

## Features

- **Dark Theme Design**: Black background with cream text, dark grey boxes, and custom color scheme
- **Multi-Page Application**: Welcome, Products, Special Offers, Trending, About Us
- **Dynamic Category Navigation**: Multi-level category tree with collapsible subcategories
- **Product Grid**: 3-column responsive grid with product details
- **Full-Screen Product Modal**: Detailed product view with specifications
- **Search Functionality**: Category-specific search with console logging
- **Authentication**: Basic login/logout with localStorage persistence
- **Sidebar Navigation**: Always-visible navigation menu with active state styling

## Tech Stack

- **Next.js 15** - React framework with App Router
- **React 19** - UI library
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling with custom color scheme
- **Next.js Image** - Optimized image handling

## Project Structure

```
focus-worthy-website/
├── app/
│   ├── components/
│   │   ├── Sidebar.tsx          # Main navigation sidebar
│   │   ├── SearchBar.tsx        # Search input component
│   │   ├── CategoryTree.tsx     # Category navigation menu
│   │   ├── ProductGrid.tsx      # 3-column product grid
│   │   └── ProductModal.tsx     # Full-screen product detail
│   ├── about/
│   │   └── page.tsx             # About Us page
│   ├── products/
│   │   └── page.tsx             # Products page with category filter
│   ├── offers/
│   │   └── page.tsx             # Special Offers page
│   ├── trending/
│   │   └── page.tsx             # Trending products page
│   ├── layout.tsx               # Root layout with sidebar
│   ├── page.tsx                 # Welcome/Homepage
│   └── globals.css              # Global styles + custom colors
├── public/
│   ├── data/
│   │   ├── categories.json      # Mock category data
│   │   └── products.json        # Mock product data
│   └── images/
│       ├── placeholder-*.svg    # Placeholder images
├── lib/
│   ├── types/
│   │   └── index.ts             # TypeScript type definitions
│   └── hooks.ts                 # Custom React hooks (data fetching)
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

## Color Scheme

| Purpose | Color | Hex |
|---------|-------|-----|
| Background | Black | #000000 |
| Text | Cream | #fef5e7 |
| Boxes | Dark Grey | #3a3a3a |
| Hover | Light Grey | #5a5a5a |
| Hover Links | Blue | #3b82f6 |
| Active/Click | Purple | #9333ea |

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Navigate to the project directory:
```bash
cd focus-worthy-website
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Data Sources

### Local Testing (Current Setup)

The project uses JSON files stored in `/public/data/`:
- `categories.json` - Category structure with multi-level hierarchy
- `products.json` - Product catalog with pricing and specifications

### Production API (Ready to Uncomment)

The codebase includes commented-out API calls ready for production:

**Categories API:**
```
GET http://localhost:5000/api/categories
```

**Products API:**
```
GET http://localhost:5000/api/products
```

To switch to API mode:
1. Open `app/products/page.tsx`, `app/offers/page.tsx`, and `app/trending/page.tsx`
2. Find the commented `fetch()` calls marked with `// PRODUCTION`
3. Uncomment the API calls and comment out the local file fetches
4. Ensure your backend server is running on `http://localhost:5000`

## Search & Logging

All searches are logged to the browser console for scraper integration:

- **Welcome page**: `[WELCOME SEARCH] Searching entire site for: "query"`
- **Products page**: `[CATEGORY SEARCH] Query: "query" - Found X results`
- **Special Offers**: `[OFFERS SEARCH] Query: "query" - Found X results`
- **Trending page**: `[TRENDING SEARCH] Query: "query" - Found X results`

Open browser console (F12) to view search logs.

## Authentication

- Login/Logout state stored in `localStorage` with key `auth`
- Simple placeholder implementation ready for real auth system
- Button text changes based on authentication state

## Responsive Design

- 3-column product grid on desktop
- Automatically wraps on smaller screens
- Sidebar remains visible with proper spacing
- Full-screen modal for product details

## Styling Notes

- All colors use Tailwind's extended color palette
- Custom CSS variables defined in `app/globals.css`
- Rounded corners on dropdowns, buttons, and cards
- Hover and active states clearly defined
- Consistent spacing and padding throughout

## Building for Production

```bash
npm run build
npm run start
```

## Deployment

The project is ready to deploy to Vercel:

1. Push to GitHub: `https://github.com/MrAlfTheOriginal/focus-worthy`
2. Connect to Vercel
3. Deploy with automatic builds on push

## Future Enhancements

- [ ] Real authentication system
- [ ] Shopping cart functionality
- [ ] User reviews and ratings
- [ ] Product comparison
- [ ] Wishlist feature
- [ ] Payment integration
- [ ] Order tracking
- [ ] Admin dashboard

## License

Private project for Focus Worthy

## Support

For issues or questions, contact the development team.
