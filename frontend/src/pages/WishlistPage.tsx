import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { Heart, ShoppingBag, Trash2, ArrowRight, AlertCircle, CheckCircle2 } from 'lucide-react';
import { useWishlist } from '../context/WishlistContext';
import { useAuth } from '../context/AuthContext';

interface WishlistPageProps {
  onOpenAuth: () => void;
}

export const WishlistPage: React.FC<WishlistPageProps> = ({ onOpenAuth }) => {
  const { wishlist, removeFromWishlist, moveToCart, loading } = useWishlist();
  const { isAuthenticated } = useAuth();
  const [feedback, setFeedback] = useState<{ message: string; isError?: boolean } | null>(null);
  const [movingId, setMovingId] = useState<number | null>(null);

  if (!isAuthenticated) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-4">
        <div className="w-16 h-16 rounded-full bg-rose-50 text-rose-500 flex items-center justify-center mx-auto">
          <Heart className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-slate-900">Sign in to view your Wishlist</h2>
        <p className="text-xs text-slate-500">Save products you love and track price drops across sessions.</p>
        <button
          onClick={onOpenAuth}
          className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs px-6 py-2.5 rounded-full"
        >
          Sign In / Register
        </button>
      </div>
    );
  }

  const handleMoveToCart = async (productId: number) => {
    setMovingId(productId);
    const res = await moveToCart(productId);
    setMovingId(null);
    if (res.success) {
      setFeedback({ message: res.message, isError: false });
    } else {
      setFeedback({ message: res.message, isError: true });
    }
    setTimeout(() => setFeedback(null), 4000);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      <div className="pb-4 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            My Wishlist
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            {wishlist.length} item{wishlist.length === 1 ? '' : 's'} saved for later
          </p>
        </div>
      </div>

      {feedback && (
        <div
          className={`flex items-center gap-2 p-3.5 rounded-2xl text-xs font-semibold ${
            feedback.isError
              ? 'bg-rose-50 text-rose-700 border border-rose-200'
              : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
          }`}
        >
          {feedback.isError ? (
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
          ) : (
            <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          )}
          <span>{feedback.message}</span>
        </div>
      )}

      {wishlist.length === 0 ? (
        <div className="max-w-md mx-auto px-4 py-16 text-center space-y-4">
          <div className="w-16 h-16 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
            <Heart className="w-8 h-8" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">Your wishlist is empty</h3>
          <p className="text-xs text-slate-500">
            Tap the heart icon on any product card to save your favorite items here.
          </p>
          <Link
            to="/products"
            className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs px-6 py-2.5 rounded-full"
          >
            <span>Explore Catalog</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
          {wishlist.map((item) => {
            const p = item.product;
            if (!p) return null;
            const isOutOfStock = Boolean(item.is_out_of_stock || (p.stock !== undefined && p.stock <= 0));
            const isLowStock = !isOutOfStock && p.stock !== undefined && p.stock > 0 && p.stock <= 5;

            return (
              <div
                key={item.id}
                className={`bg-white rounded-2xl border ${
                  isOutOfStock ? 'border-rose-200 bg-rose-50/10' : 'border-slate-200/80'
                } overflow-hidden shadow-subtle hover:shadow-card transition-all flex flex-col justify-between`}
              >
                <div className="relative aspect-square overflow-hidden bg-slate-100">
                  <Link to={`/products/${p.id}`}>
                    <img
                      src={p.primary_image || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400'}
                      alt={p.name}
                      className={`w-full h-full object-cover ${isOutOfStock ? 'opacity-60 grayscale' : ''}`}
                    />
                  </Link>

                  {isOutOfStock && (
                    <span className="absolute top-2.5 left-2.5 bg-rose-600 text-white text-[10px] font-extrabold px-2.5 py-0.5 rounded-full uppercase tracking-wider shadow-sm">
                      Out of Stock
                    </span>
                  )}

                  <button
                    onClick={() => removeFromWishlist(p.id)}
                    title="Remove from wishlist"
                    className="absolute top-2.5 right-2.5 w-8 h-8 rounded-full bg-white/90 text-rose-500 hover:bg-white flex items-center justify-center shadow-sm transition-transform active:scale-90"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>

                <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
                  <div>
                    <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-wider block">
                      {p.brand}
                    </span>
                    <Link
                      to={`/products/${p.id}`}
                      className="text-xs sm:text-sm font-semibold text-slate-900 hover:text-indigo-600 line-clamp-2 transition-colors"
                    >
                      {p.name}
                    </Link>
                    <div className="mt-1 flex items-baseline gap-2">
                      <p className="text-sm font-extrabold text-slate-900">
                        ₹{p.discounted_price.toLocaleString('en-IN')}
                      </p>
                      {p.original_price > p.discounted_price && (
                        <p className="text-[11px] text-slate-400 line-through">
                          ₹{p.original_price.toLocaleString('en-IN')}
                        </p>
                      )}
                    </div>

                    {isLowStock && (
                      <p className="text-[11px] font-semibold text-amber-600 mt-1">
                        Only {p.stock} left in stock!
                      </p>
                    )}
                  </div>

                  <button
                    onClick={() => handleMoveToCart(p.id)}
                    disabled={isOutOfStock || movingId === p.id}
                    className={`w-full font-semibold py-2 px-3 rounded-xl text-xs flex items-center justify-center gap-1.5 transition-all shadow-sm ${
                      isOutOfStock
                        ? 'bg-slate-100 text-slate-400 border border-slate-200 cursor-not-allowed'
                        : 'bg-indigo-600 hover:bg-indigo-700 active:scale-95 text-white'
                    }`}
                  >
                    <ShoppingBag className="w-3.5 h-3.5" />
                    <span>
                      {movingId === p.id
                        ? 'Moving...'
                        : isOutOfStock
                        ? 'Unavailable'
                        : 'Move to Cart'}
                    </span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
