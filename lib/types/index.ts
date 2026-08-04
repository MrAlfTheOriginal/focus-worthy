// Type definitions for Focus Worthy

export interface CategoryItem {
  id: string;
  name: string;
}

export interface SubCategory extends CategoryItem {
  items: CategoryItem[];
}

export interface Category extends CategoryItem {
  subcategories: SubCategory[];
}

export interface ProductSpecs {
  [key: string]: string;
}

export interface Product {
  id: string;
  name: string;
  categoryId: string;
  price: number;
  salePrice: number;
  image: string;
  description: string;
  specs: ProductSpecs;
}

export interface AuthState {
  isLoggedIn: boolean;
  user?: string;
}
