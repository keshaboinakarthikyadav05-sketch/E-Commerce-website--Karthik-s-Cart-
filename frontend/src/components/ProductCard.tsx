import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Heart, Star, ShoppingBag, Check } from 'lucide-react';
import { Product } from '../types';
import { useCart } from '../context/CartContext';
import { useWishlist } from '../context/WishlistContext';

interface ProductCardProps {
  product: Product;
  onOpenAuth?: () => void;
}

export const ProductCard: React.FC<ProductCardProps> = ({ product, onOpenAuth }) => {
  const { addToCart } = useCart();
  const { isInWishlist, toggleWishlist } = useWishlist();

  const [adding, setAdding] = useState(false);
  const [justAdded, setJustAdded] = useState(false);
  const isWishlisted = isInWishlist(product.id);

  const handleAddToCart = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();

    // Default to first variant's size/color if available
    const firstSize = product.available_sizes?.[0];
    const firstColor = product.available_colors?.[0];

    setAdding(true);
    const res = await addToCart(product.id, 1, firstSize, firstColor);
    setAdding(false);

    if (res.success) {
      setJustAdded(true);
      setTimeout(() => setJustAdded(false), 1800);
    } else if (onOpenAuth && res.message.includes('sign in')) {
      onOpenAuth();
    }
  };

  const handleToggleWishlist = async (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    const res = await toggleWishlist(product.id);
    if (!res.added && onOpenAuth && res.message?.includes('sign in')) {
      onOpenAuth();
    }
  };

  return (
    <div className="group relative bg-white rounded-2xl border border-slate-200/80 hover:border-slate-300 hover:shadow-card transition-all duration-300 flex flex-col overflow-hidden">
      {/* Product Image Area */}
      <Link to={`/products/${product.id}`} className="block relative aspect-square overflow-hidden bg-slate-100">
        <img
          src={product.primary_image}
          alt={product.name}
          className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500 ease-out"
          loading="lazy"
        />

        {/* Badges Overlay */}
        <div className="absolute top-2.5 left-2.5 flex flex-col gap-1.5 z-10">
          {product.discount_percent > 0 && (
            <span className="bg-rose-500 text-white text-[11px] font-bold px-2 py-0.5 rounded-full shadow-sm">
              {product.discount_percent}% OFF
            </span>
          )}
          {product.is_bestseller && (
            <span className="bg-amber-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-sm uppercase tracking-wide">
              Bestseller
            </span>
          )}
          {product.is_trending && !product.is_bestseller && (
            <span className="bg-indigo-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-sm uppercase tracking-wide">
              Trending
            </span>
          )}
        </div>

        {/* Wishlist Button */}
        <button
          onClick={handleToggleWishlist}
          title={isWishlisted ? 'Remove from wishlist' : 'Add to wishlist'}
          className={`absolute top-2.5 right-2.5 w-9 h-9 rounded-full flex items-center justify-center transition-all shadow-sm z-10 ${
            isWishlisted
              ? 'bg-rose-50 text-rose-500 hover:bg-rose-100'
              : 'bg-white/90 text-slate-500 hover:text-rose-500 hover:bg-white backdrop-blur-sm'
          }`}
        >
          <Heart className={`w-4 h-4 ${isWishlisted ? 'fill-rose-500' : ''}`} />
        </button>
      </Link>

      {/* Product Info */}
      <div className="p-4 flex-1 flex flex-col justify-between">
        <div>
          {/* Brand & Category */}
          <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
            <span className="font-semibold uppercase tracking-wider text-indigo-600/90 text-[11px]">
              {product.brand}
            </span>
            {product.category_name && (
              <span className="truncate max-w-[100px] text-[11px]">{product.category_name}</span>
            )}
          </div>

          {/* Title */}
          <Link
            to={`/products/${product.id}`}
            className="block text-sm font-semibold text-slate-800 hover:text-indigo-600 transition-colors line-clamp-2 leading-snug mb-2"
          >
            {product.name}
          </Link>

          {/* Ratings */}
          <div className="flex items-center space-x-1 mb-2">
            <div className="flex items-center gap-1 bg-amber-50 text-amber-800 border border-amber-200/60 px-1.5 py-0.5 rounded text-[11px] font-bold">
              <span>{product.rating.toFixed(1)}</span>
              <Star className="w-3 h-3 fill-amber-400 text-amber-400" />
            </div>
            <span className="text-[11px] text-slate-400">({product.num_reviews})</span>
          </div>
        </div>

        {/* Price & Action */}
        <div className="pt-2 border-t border-slate-100 flex items-center justify-between gap-2 mt-auto">
          <div>
            <div className="flex items-baseline space-x-1.5">
              <span className="text-base sm:text-lg font-bold text-slate-900">
                ₹{product.discounted_price.toLocaleString('en-IN')}
              </span>
              {product.original_price > product.discounted_price && (
                <span className="text-xs text-slate-400 line-through">
                  ₹{product.original_price.toLocaleString('en-IN')}
                </span>
              )}
            </div>
          </div>

          {/* Quick Add to Cart Button */}
          <button
            onClick={handleAddToCart}
            disabled={adding || product.stock <= 0}
            className={`px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all ${
              product.stock <= 0
                ? 'bg-slate-100 text-slate-400 cursor-not-allowed'
                : justAdded
                ? 'bg-emerald-600 text-white'
                : 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-sm hover:shadow'
            }`}
          >
            {justAdded ? (
              <>
                <Check className="w-3.5 h-3.5" />
                <span>Added</span>
              </>
            ) : product.stock <= 0 ? (
              <span>Out of Stock</span>
            ) : (
              <>
                <ShoppingBag className="w-3.5 h-3.5" />
                <span>Add</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};
