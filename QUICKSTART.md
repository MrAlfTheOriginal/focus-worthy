# Focus Worthy - Quick Start Guide

## Running Locally

```bash
# Navigate to project
cd /home/alf/Desktop/focus-worthy-website

# Install dependencies (if not already done)
npm install

# Start development server
npm run dev

# Open browser
# http://localhost:3000
```

The site will be live at `http://localhost:3000` with hot reload enabled.

## Project Structure at a Glance

```
Components (reusable)
├── Sidebar.tsx           → Left navigation + Login button
├── SearchBar.tsx         → Search input (logs to console)
├── CategoryTree.tsx      → Multi-level category menu
├── ProductGrid.tsx       → 3-column product display
└── ProductModal.tsx      → Full-screen product details

Pages (routes)
├── / (Welcome)           → Homepage with intro
├── /products             → Products with category filter
├── /offers               → Special offers/discounts
├── /trending             → Popular/trending products
└── /about                → Company information

Data
├── public/data/categories.json → Category structure
├── public/data/products.json   → 18 sample products
└── lib/types/index.ts          → TypeScript interfaces
```

## Key Features

### 🎨 Dark Theme
- Black background, cream text
- Dark grey boxes with light grey hover
- Blue hover effects, purple active states
- Fully customizable in `app/globals.css`

### 🔍 Search
- Searches within current category
- Logs all queries to browser console
- Ready for scraper integration

### 🔑 Authentication
- Click "Login" button in sidebar
- State persists in localStorage
- Simple to integrate with real auth system

### 🛍️ Product Discovery
- Expand categories to view subcategories
- Select items to see filtered products
- Click products to view full details
- 3-column responsive grid

## Making Changes

### Add More Products
Edit `public/data/products.json`:
```json
{
  "id": "unique-id",
  "name": "Product Name",
  "categoryId": "phones",
  "price": 999.99,
  "salePrice": 799.99,
  "image": "/images/placeholder.svg",
  "description": "Product description",
  "specs": { "key": "value" }
}
```

### Customize Colors
Edit `app/globals.css`:
```css
:root {
  --background: #000000;
  --foreground: #fef5e7;
  --color-blue: #3b82f6;
  --color-purple: #9333ea;
}
```

### Add Categories
Edit `public/data/categories.json`:
```json
{
  "id": "electronics",
  "name": "Electronics",
  "subcategories": [
    {
      "id": "phones",
      "name": "Phones",
      "items": [
        { "id": "phone-1", "name": "Smartphone Pro" }
      ]
    }
  ]
}
```

## Switching to Production API

The code is already set up for easy API integration. Look for this pattern in:
- `app/products/page.tsx`
- `app/offers/page.tsx`
- `app/trending/page.tsx`

```typescript
// LOCAL TESTING: Using JSON files
const response = await fetch('/data/categories.json');

// PRODUCTION: Uncomment below and comment out above
// const response = await fetch('http://localhost:5000/api/categories');
```

**To activate:** Simply comment out the local JSON call and uncomment the API call.

## Building for Production

```bash
# Build optimized version
npm run build

# Test production build locally
npm start

# Vercel deployment (automatic from GitHub)
git push origin main
```

## Browser Console

Open the browser console (F12) to see search logs:
```
[WELCOME SEARCH] Searching entire site for: "phone"
[CATEGORY SEARCH] Query: "smartphone" - Found 2 results
[OFFERS SEARCH] Query: "gaming" - Found 1 results
[TRENDING SEARCH] Query: "laptop" - Found 2 results
```

## Troubleshooting

**Port 3000 already in use?**
```bash
npm run dev -- -p 3001
```

**Clear cache:**
```bash
rm -rf .next
npm run dev
```

**TypeScript errors?**
```bash
npm run build
# Shows detailed errors
```

## Testing Checklist

- [ ] Homepage loads with search bar
- [ ] Sidebar navigation works
- [ ] Products page shows category tree
- [ ] Clicking category shows products
- [ ] Clicking product opens modal
- [ ] Search bar filters products
- [ ] Login button toggles to Logout
- [ ] About page displays info
- [ ] Special Offers shows discounted items
- [ ] Trending page shows curated selection

## Next Steps

1. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/MrAlfTheOriginal/focus-worthy
   git push -u origin master
   ```

2. **Connect to Vercel**
   - Go to vercel.com
   - Import GitHub repo
   - One-click deploy

3. **Customize**
   - Update product data
   - Change colors
   - Add more categories
   - Integrate real auth

4. **Scale**
   - Replace JSON with API
   - Add shopping cart
   - Integrate payments
   - Add user accounts

## Support

All code is documented with comments explaining:
- What each component does
- Where to add API calls
- How data flows
- Why styles are applied

No external dependencies needed beyond Next.js and Tailwind CSS.

Enjoy building! 🚀
