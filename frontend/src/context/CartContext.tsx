import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { CartSummary, Product } from '../types';
import { cartApi } from '../services/api';
import { useAuth } from './AuthContext';

interface CartContextType {
  cart: CartSummary | null;
  loading: boolean;
  totalItems: number;
  fetchCart: (coupon?: string) => Promise<void>;
  addToCart: (productId: number, quantity?: number, size?: string, color?: string) => Promise<{ success: boolean; message: string }>;
  updateQuantity: (cartItemId: number, quantity: number) => Promise<{ success: boolean; message?: string }>;
  updateCartItem: (cartItemId: number, data: { quantity?: number; size?: string; color?: string }) => Promise<{ success: boolean; message?: string }>;
  removeFromCart: (cartItemId: number) => Promise<boolean>;
  moveToWishlist: (cartItemId: number) => Promise<{ success: boolean; message: string }>;
  clearCart: () => Promise<boolean>;
  applyCoupon: (code: string) => Promise<{ success: boolean; message: string }>;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const [cart, setCart] = useState<CartSummary | null>({
    items: [],
    items_count: 0,
    subtotal: 0,
    discount: 0,
    delivery_charge: 0,
    final_total: 0,
  });
  const [loading, setLoading] = useState(false);

  const fetchCart = useCallback(async (coupon?: string) => {
    if (!isAuthenticated) {
      // Guest cart from localStorage
      const localCart = localStorage.getItem('shopora_guest_cart');
      if (localCart) {
        try {
          const parsed = JSON.parse(localCart);
          setCart(parsed);
        } catch {
          // ignore
        }
      }
      return;
    }

    try {
      setLoading(true);
      const res = await cartApi.getCart(coupon);
      if (res.data?.success) {
        setCart(res.data.cart);
      }
    } catch (err) {
      console.error('Failed to fetch cart:', err);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  const addToCart = async (productId: number, quantity = 1, size?: string, color?: string) => {
    if (!isAuthenticated) {
      return { success: false, message: 'Please sign in to add items to your cart' };
    }

    try {
      const res = await cartApi.addToCart({ product_id: productId, quantity, size, color });
      if (res.data?.success) {
        setCart(res.data.cart);
        return { success: true, message: res.data.message || 'Added to cart' };
      }
      return { success: false, message: res.data?.message || 'Could not add to cart' };
    } catch (err: any) {
      const msg = err.response?.data?.message || 'Could not add to cart';
      return { success: false, message: msg };
    }
  };

  const updateQuantity = async (cartItemId: number, quantity: number) => {
    try {
      const res = await cartApi.updateCartItem(cartItemId, quantity);
      if (res.data?.success) {
        setCart(res.data.cart);
        return { success: true, message: res.data.message };
      }
      return { success: false, message: res.data?.message || 'Failed to update quantity' };
    } catch (err: any) {
      const msg = err.response?.data?.message || 'Failed to update cart quantity';
      console.error('Failed to update cart quantity:', err);
      return { success: false, message: msg };
    }
  };

  const updateCartItem = async (cartItemId: number, data: { quantity?: number; size?: string; color?: string }) => {
    try {
      const res = await cartApi.updateCartItem(cartItemId, data);
      if (res.data?.success) {
        setCart(res.data.cart);
        return { success: true, message: res.data.message };
      }
      return { success: false, message: res.data?.message || 'Failed to update item' };
    } catch (err: any) {
      const msg = err.response?.data?.message || 'Failed to update item';
      console.error('Failed to update cart item:', err);
      return { success: false, message: msg };
    }
  };

  const removeFromCart = async (cartItemId: number) => {
    try {
      const res = await cartApi.removeFromCart(cartItemId);
      if (res.data?.success) {
        setCart(res.data.cart);
        return true;
      }
      return false;
    } catch (err) {
      console.error('Failed to remove cart item:', err);
      return false;
    }
  };

  const moveToWishlist = async (cartItemId: number) => {
    try {
      const res = await cartApi.moveToWishlist(cartItemId);
      if (res.data?.success) {
        setCart(res.data.cart);
        return { success: true, message: res.data.message };
      }
      return { success: false, message: res.data?.message || 'Failed to move to wishlist' };
    } catch (err: any) {
      const msg = err.response?.data?.message || 'Failed to move to wishlist';
      return { success: false, message: msg };
    }
  };

  const clearCart = async () => {
    try {
      const res = await cartApi.clearCart();
      if (res.data?.success) {
        setCart(res.data.cart);
        return true;
      }
      return false;
    } catch (err) {
      console.error('Failed to clear cart:', err);
      return false;
    }
  };

  const applyCoupon = async (code: string) => {
    try {
      const res = await cartApi.applyCoupon(code);
      if (res.data?.success) {
        setCart(res.data.cart);
        return { success: true, message: res.data.message };
      }
      return { success: false, message: res.data?.message || 'Invalid coupon' };
    } catch (err: any) {
      const msg = err.response?.data?.message || 'Could not apply coupon';
      return { success: false, message: msg };
    }
  };

  return (
    <CartContext.Provider
      value={{
        cart,
        loading,
        totalItems: cart?.items_count || 0,
        fetchCart,
        addToCart,
        updateQuantity,
        updateCartItem,
        removeFromCart,
        moveToWishlist,
        clearCart,
        applyCoupon,
      }}
    >
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error('useCart must be used within a CartProvider');
  }
  return context;
};
