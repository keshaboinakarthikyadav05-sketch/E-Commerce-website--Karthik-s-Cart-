import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { WishlistItem } from '../types';
import { wishlistApi } from '../services/api';
import { useAuth } from './AuthContext';
import { useCart } from './CartContext';

interface WishlistContextType {
  wishlist: WishlistItem[];
  wishlistCount: number;
  loading: boolean;
  isInWishlist: (productId: number) => boolean;
  toggleWishlist: (productId: number) => Promise<{ added: boolean; message: string }>;
  removeFromWishlist: (productId: number) => Promise<boolean>;
  moveToCart: (productId: number, size?: string, color?: string) => Promise<{ success: boolean; message: string }>;
  fetchWishlist: () => Promise<void>;
}

const WishlistContext = createContext<WishlistContextType | undefined>(undefined);

export const WishlistProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  const { fetchCart } = useCart();
  const [wishlist, setWishlist] = useState<WishlistItem[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchWishlist = useCallback(async () => {
    if (!isAuthenticated) {
      setWishlist([]);
      return;
    }
    try {
      setLoading(true);
      const res = await wishlistApi.getWishlist();
      if (res.data?.success) {
        setWishlist(res.data.wishlist || []);
      }
    } catch (err) {
      console.error('Failed to fetch wishlist:', err);
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    fetchWishlist();
  }, [fetchWishlist]);

  const isInWishlist = (productId: number) => {
    return wishlist.some((item) => item.product_id === productId || item.product?.id === productId);
  };

  const toggleWishlist = async (productId: number) => {
    if (!isAuthenticated) {
      return { added: false, message: 'Please sign in to save items to your wishlist' };
    }

    const alreadyIn = isInWishlist(productId);

    try {
      if (alreadyIn) {
        await wishlistApi.removeFromWishlist(productId);
        setWishlist((prev) => prev.filter((item) => item.product_id !== productId && item.product?.id !== productId));
        return { added: false, message: 'Removed from wishlist' };
      } else {
        const res = await wishlistApi.addToWishlist(productId);
        if (res.data?.success) {
          fetchWishlist();
          return { added: true, message: 'Added to wishlist' };
        }
      }
      return { added: false, message: 'Failed to update wishlist' };
    } catch (err: any) {
      return { added: false, message: err.response?.data?.message || 'Error updating wishlist' };
    }
  };

  const removeFromWishlist = async (productId: number) => {
    try {
      await wishlistApi.removeFromWishlist(productId);
      setWishlist((prev) => prev.filter((item) => item.product_id !== productId && item.product?.id !== productId));
      return true;
    } catch {
      return false;
    }
  };

  const moveToCart = async (productId: number, size?: string, color?: string) => {
    try {
      const res = await wishlistApi.moveToCart(productId, size, color);
      if (res.data?.success) {
        await fetchWishlist();
        await fetchCart();
        return { success: true, message: res.data.message || 'Moved to cart' };
      }
      return { success: false, message: res.data?.message || 'Could not move to cart' };
    } catch (err: any) {
      const msg = err.response?.data?.message || 'Could not move to cart';
      return { success: false, message: msg };
    }
  };

  return (
    <WishlistContext.Provider
      value={{
        wishlist,
        wishlistCount: wishlist.length,
        loading,
        isInWishlist,
        toggleWishlist,
        removeFromWishlist,
        moveToCart,
        fetchWishlist,
      }}
    >
      {children}
    </WishlistContext.Provider>
  );
};

export const useWishlist = () => {
  const context = useContext(WishlistContext);
  if (!context) {
    throw new Error('useWishlist must be used within a WishlistProvider');
  }
  return context;
};
