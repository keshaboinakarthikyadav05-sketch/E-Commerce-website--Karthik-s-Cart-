export interface User {
  id: number;
  full_name: string;
  email: string;
  mobile_number: string;
  role: 'customer' | 'admin';
  is_active: boolean;
  created_at?: string;
  addresses?: Address[];
}

export interface Address {
  id?: number;
  user_id?: number;
  full_name: string;
  mobile_number: string;
  address_line1: string;
  address_line2?: string;
  city: string;
  state: string;
  postal_code: string;
  country?: string;
  is_default?: boolean;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  image_url?: string;
  product_count?: number;
}

export interface ProductImage {
  id: number;
  image_url: string;
  is_primary: boolean;
  display_order: number;
}

export interface ProductVariant {
  id: number;
  size?: string;
  color?: string;
  sku?: string;
  additional_price: number;
  stock: number;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  category_id: number;
  category_name?: string;
  category_slug?: string;
  brand: string;
  original_price: number;
  discounted_price: number;
  discount_percent: number;
  stock: number;
  rating: number;
  num_reviews: number;
  primary_image: string;
  is_featured?: boolean;
  is_trending?: boolean;
  is_bestseller?: boolean;
  created_at?: string;
  images?: ProductImage[];
  variants?: ProductVariant[];
  specifications?: Record<string, string>;
  available_sizes?: string[];
  available_colors?: string[];
  related_products?: Product[];
  reviews?: Review[];
}

export interface CartItem {
  id: number;
  user_id: number;
  product_id: number;
  variant_id?: number;
  size?: string;
  color?: string;
  quantity: number;
  unit_price: number;
  total_price: number;
  product?: Product;
  is_out_of_stock?: boolean;
  exceeds_stock?: boolean;
  available_stock?: number;
  is_low_stock?: boolean;
  available_sizes?: string[];
  available_colors?: string[];
}

export interface Coupon {
  id: number;
  code: string;
  description?: string;
  discount_type: 'percentage' | 'fixed';
  discount_value: number;
  min_order_amount: number;
  max_discount?: number;
}

export interface CartSummary {
  items: CartItem[];
  items_count: number;
  subtotal: number;
  discount: number;
  delivery_charge: number;
  final_total: number;
  has_out_of_stock?: boolean;
  has_exceeded_stock?: boolean;
  can_checkout?: boolean;
  applied_coupon?: Coupon | null;
}

export interface WishlistItem {
  id: number;
  user_id: number;
  product_id: number;
  product: Product;
  is_out_of_stock?: boolean;
  stock?: number;
  created_at?: string;
}

export interface OrderItem {
  id: number;
  order_id: number;
  product_id: number;
  product_name: string;
  product_image?: string;
  price: number;
  quantity: number;
  size?: string;
  color?: string;
  total_price: number;
}

export interface Order {
  id: number;
  order_number: string;
  user_id: number;
  user_name?: string;
  user_email?: string;
  shipping_name: string;
  shipping_mobile: string;
  shipping_address: {
    address: string;
    city: string;
    state: string;
    postal_code: string;
  };
  subtotal: number;
  discount: number;
  delivery_charge: number;
  total_amount: number;
  payment_method: 'razorpay' | 'cod';
  payment_status: 'pending' | 'paid' | 'failed' | 'refunded';
  order_status: 'placed' | 'confirmed' | 'processing' | 'shipped' | 'delivered' | 'cancelled';
  razorpay_order_id?: string;
  razorpay_payment_id?: string;
  created_at: string;
  items: OrderItem[];
}

export interface Review {
  id: number;
  product_id: number;
  user_id: number;
  user_name: string;
  rating: number;
  title?: string;
  comment: string;
  is_verified_purchase?: boolean;
  created_at?: string;
}

export interface AdminDashboardStats {
  total_users: number;
  total_products: number;
  total_orders: number;
  total_sales: number;
  low_stock_count: number;
  status_distribution: Record<string, number>;
  category_distribution: { category: string; count: number }[];
  sales_chart: { date: string; sales: number; orders: number }[];
  recent_orders: Order[];
}
