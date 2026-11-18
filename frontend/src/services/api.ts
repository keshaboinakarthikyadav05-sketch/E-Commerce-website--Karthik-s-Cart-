import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to inject JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('shopora_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token expiry
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if invalid or expired
      const isAuthRoute = error.config?.url?.includes('/auth/login') || error.config?.url?.includes('/auth/register');
      if (!isAuthRoute) {
        localStorage.removeItem('shopora_token');
        localStorage.removeItem('shopora_user');
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  register: (data: any) => api.post('/auth/register', data),
  login: (data: any) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/auth/me'),
  getAddresses: () => api.get('/auth/addresses'),
  addAddress: (data: any) => api.post('/auth/addresses', data),
};

export const productsApi = {
  getProducts: (params?: Record<string, any>) => api.get('/products', { params }),
  getProductById: (id: number | string) => api.get(`/products/${id}`),
  getSearchSuggestions: (q: string) => api.get('/products/search/suggestions', { params: { q } }),
  createProduct: (data: any) => api.post('/products', data),
  updateProduct: (id: number | string, data: any) => api.put(`/products/${id}`, data),
  deleteProduct: (id: number | string) => api.delete(`/products/${id}`),
  addReview: (productId: number | string, data: any) => api.post(`/products/${productId}/reviews`, data),
};

export const categoriesApi = {
  getCategories: () => api.get('/categories'),
  getCategoryBySlug: (slug: string) => api.get(`/categories/${slug}`),
  createCategory: (data: any) => api.post('/categories', data),
  updateCategory: (id: number, data: any) => api.put(`/categories/${id}`, data),
  deleteCategory: (id: number) => api.delete(`/categories/${id}`),
};

export const cartApi = {
  getCart: (coupon?: string) => api.get('/cart', { params: coupon ? { coupon } : {} }),
  addToCart: (data: { product_id: number; quantity?: number; size?: string; color?: string }) => api.post('/cart', data),
  updateCartItem: (id: number, data: { quantity?: number; size?: string; color?: string } | number) => {
    const payload = typeof data === 'number' ? { quantity: data } : data;
    return api.put(`/cart/${id}`, payload);
  },
  removeFromCart: (id: number) => api.delete(`/cart/${id}`),
  moveToWishlist: (id: number) => api.post(`/cart/${id}/move-to-wishlist`),
  clearCart: () => api.post('/cart/clear'),
  applyCoupon: (code: string) => api.post('/cart/apply-coupon', { code }),
};

export const wishlistApi = {
  getWishlist: () => api.get('/wishlist'),
  addToWishlist: (product_id: number) => api.post('/wishlist', { product_id }),
  removeFromWishlist: (product_id: number) => api.delete(`/wishlist/${product_id}`),
  moveToCart: (product_id: number, size?: string, color?: string) => api.post('/wishlist/move-to-cart', { product_id, size, color }),
};

export const ordersApi = {
  createOrder: (data: any) => api.post('/orders', data),
  getUserOrders: () => api.get('/orders'),
  getOrderById: (id: number | string) => api.get(`/orders/${id}`),
  cancelOrder: (id: number | string) => api.put(`/orders/${id}/cancel`),
};

export const paymentsApi = {
  createPaymentOrder: (order_id: number) => api.post('/payments/create-order', { order_id }),
  verifyPayment: (data: {
    order_id: number;
    razorpay_order_id: string;
    razorpay_payment_id: string;
    razorpay_signature: string;
  }) => api.post('/payments/verify', data),
  getPaymentDetails: (id: number) => api.get(`/payments/${id}`),
};

export const adminApi = {
  getDashboard: () => api.get('/admin/dashboard'),
  getOrders: (params?: { page?: number; limit?: number; status?: string }) => api.get('/admin/orders', { params }),
  updateOrderStatus: (id: number, data: { status: string; payment_status?: string }) => api.put(`/admin/orders/${id}/status`, data),
  getUsers: () => api.get('/admin/users'),
  toggleUserStatus: (id: number) => api.put(`/admin/users/${id}/toggle-status`),
};

export default api;
