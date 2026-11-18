import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  Star,
  Heart,
  ShoppingBag,
  Zap,
  Truck,
  RotateCcw,
  ShieldCheck,
  Check,
  ChevronRight,
  Plus,
  Minus,
  MessageSquarePlus,
  Share2
} from 'lucide-react';
import { ProductCard } from '../components/ProductCard';
import { productsApi } from '../services/api';
import { Product } from '../types';
import { useCart } from '../context/CartContext';
import { useWishlist } from '../context/WishlistContext';
import { useAuth } from '../context/AuthContext';

interface ProductDetailsPageProps {
  onOpenAuth: () => void;
}

export const ProductDetailsPage: React.FC<ProductDetailsPageProps> = ({ onOpenAuth }) => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { addToCart } = useCart();
  const { isInWishlist, toggleWishlist } = useWishlist();
  const { isAuthenticated, user } = useAuth();

  const [product, setProduct] = useState<Product | null>(null);
  const [selectedImage, setSelectedImage] = useState<string>('');
  const [selectedSize, setSelectedSize] = useState<string>('');
  const [selectedColor, setSelectedColor] = useState<string>('');
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);

  const [addingToCart, setAddingToCart] = useState(false);
  const [addedToast, setAddedToast] = useState(false);

  // Review form state
  const [reviewRating, setReviewRating] = useState(5);
  const [reviewTitle, setReviewTitle] = useState('');
  const [reviewComment, setReviewComment] = useState('');
  const [submittingReview, setSubmittingReview] = useState(false);
  const [reviewSuccess, setReviewSuccess] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      if (!id) return;
      try {
        setLoading(true);
        const res = await productsApi.getProductById(id);
        if (res.data?.success) {
          const p = res.data.product;
          setProduct(p);
          setSelectedImage(p.primary_image || (p.images?.[0]?.image_url ?? ''));
          if (p.available_sizes?.length) setSelectedSize(p.available_sizes[0]);
          if (p.available_colors?.length) setSelectedColor(p.available_colors[0]);
          setQuantity(1);
        }
      } catch (err) {
        console.error('Failed to load product:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [id]);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center">
        <div className="inline-block w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mb-4" />
        <p className="text-sm text-slate-500 font-medium">Loading product details...</p>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-16 text-center space-y-4">
        <h2 className="text-2xl font-bold text-slate-900">Product not found</h2>
        <Link to="/products" className="inline-block bg-indigo-600 text-white text-sm font-semibold px-6 py-2.5 rounded-full">
          Back to Products
        </Link>
      </div>
    );
  }

  const isWishlisted = isInWishlist(product.id);

  const handleAddToCart = async () => {
    setAddingToCart(true);
    const res = await addToCart(product.id, quantity, selectedSize, selectedColor);
    setAddingToCart(false);

    if (res.success) {
      setAddedToast(true);
      setTimeout(() => setAddedToast(false), 2000);
    } else if (res.message?.includes('sign in')) {
      onOpenAuth();
    }
  };

  const handleBuyNow = async () => {
    if (!isAuthenticated) {
      onOpenAuth();
      return;
    }
    // Navigate straight to checkout with single-item buy payload
    navigate('/checkout', {
      state: {
        buyNowItem: {
          product_id: product.id,
          quantity,
          size: selectedSize,
          color: selectedColor,
          price: product.discounted_price,
          product,
        }
      }
    });
  };

  const handleReviewSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isAuthenticated) {
      onOpenAuth();
      return;
    }
    if (!reviewComment.trim()) return;

    try {
      setSubmittingReview(true);
      const res = await productsApi.addReview(product.id, {
        rating: reviewRating,
        title: reviewTitle,
        comment: reviewComment,
      });
      if (res.data?.success) {
        setReviewSuccess(true);
        // Refresh product to show updated review
        const updated = await productsApi.getProductById(product.id);
        if (updated.data?.success) setProduct(updated.data.product);
        setReviewTitle('');
        setReviewComment('');
      }
    } catch (err) {
      console.error('Failed to submit review:', err);
    } finally {
      setSubmittingReview(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
      {/* 1. Breadcrumbs */}
      <nav className="flex items-center space-x-2 text-xs text-slate-500">
        <Link to="/" className="hover:text-indigo-600">Home</Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
        <Link to="/products" className="hover:text-indigo-600">Products</Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
        {product.category_slug && (
          <>
            <Link to={`/products?category=${product.category_slug}`} className="hover:text-indigo-600">
              {product.category_name}
            </Link>
            <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
          </>
        )}
        <span className="text-slate-800 font-medium truncate max-w-xs">{product.name}</span>
      </nav>

      {/* 2. Main Product Details View */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-start">
        {/* Left: Gallery (Thumbnails + Large Hero View) */}
        <div className="space-y-4">
          <div className="relative aspect-square rounded-3xl overflow-hidden bg-slate-100 border border-slate-200/80 shadow-subtle group">
            <img
              src={selectedImage || product.primary_image}
              alt={product.name}
              className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500"
            />
            {product.discount_percent > 0 && (
              <span className="absolute top-4 left-4 bg-rose-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-sm">
                {product.discount_percent}% OFF
              </span>
            )}
          </div>

          {/* Thumbnail list */}
          {product.images && product.images.length > 1 && (
            <div className="flex items-center space-x-3 overflow-x-auto pb-2">
              {product.images.map((img, i) => (
                <button
                  key={i}
                  onClick={() => setSelectedImage(img.image_url)}
                  className={`relative w-20 h-20 rounded-2xl overflow-hidden border-2 flex-shrink-0 transition-all ${
                    selectedImage === img.image_url ? 'border-indigo-600 shadow-md' : 'border-slate-200 hover:border-slate-300'
                  }`}
                >
                  <img src={img.image_url} alt="" className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Right: Product Actions & Specs */}
        <div className="space-y-6">
          <div>
            <span className="text-xs font-bold uppercase tracking-widest text-indigo-600">
              {product.brand}
            </span>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight mt-1">
              {product.name}
            </h1>

            {/* Rating & Review summary */}
            <div className="flex items-center space-x-3 mt-3">
              <div className="flex items-center gap-1 bg-amber-50 text-amber-900 border border-amber-200 px-2 py-0.5 rounded-lg text-xs font-bold">
                <span>{product.rating.toFixed(1)}</span>
                <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
              </div>
              <span className="text-xs text-slate-500 underline cursor-pointer">
                {product.num_reviews} Verified Ratings
              </span>
              <span className="text-slate-300">|</span>
              <span className={`text-xs font-semibold ${product.stock > 0 ? 'text-emerald-600' : 'text-rose-600'}`}>
                {product.stock > 10 ? 'In Stock' : product.stock > 0 ? `Only ${product.stock} Left` : 'Currently Out of Stock'}
              </span>
            </div>
          </div>

          {/* Price breakdown */}
          <div className="p-4 bg-slate-50/80 rounded-2xl border border-slate-200/80 space-y-1">
            <div className="flex items-baseline space-x-3">
              <span className="text-3xl font-extrabold text-slate-900">
                ₹{product.discounted_price.toLocaleString('en-IN')}
              </span>
              {product.original_price > product.discounted_price && (
                <>
                  <span className="text-base text-slate-400 line-through">
                    ₹{product.original_price.toLocaleString('en-IN')}
                  </span>
                  <span className="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-100">
                    Save ₹{(product.original_price - product.discounted_price).toLocaleString('en-IN')}
                  </span>
                </>
              )}
            </div>
            <p className="text-[11px] text-slate-400">Inclusive of all taxes & doorstep delivery insurance</p>
          </div>

          {/* Size Selector */}
          {product.available_sizes && product.available_sizes.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                  Select Size
                </span>
                <span className="text-xs text-indigo-600 hover:underline cursor-pointer">
                  Size Guide
                </span>
              </div>
              <div className="flex flex-wrap gap-2">
                {product.available_sizes.map((s) => (
                  <button
                    key={s}
                    onClick={() => setSelectedSize(s)}
                    className={`min-w-[48px] px-3.5 py-2 text-xs font-bold rounded-xl border transition-all ${
                      selectedSize === s
                        ? 'border-indigo-600 bg-indigo-50 text-indigo-700 ring-2 ring-indigo-600/20'
                        : 'border-slate-200 text-slate-700 hover:border-slate-300 bg-white'
                    }`}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Color Selector */}
          {product.available_colors && product.available_colors.length > 0 && (
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-slate-700 block mb-2">
                Select Color: <span className="font-semibold text-indigo-600">{selectedColor}</span>
              </span>
              <div className="flex flex-wrap gap-2">
                {product.available_colors.map((c) => (
                  <button
                    key={c}
                    onClick={() => setSelectedColor(c)}
                    className={`px-3 py-1.5 text-xs font-medium rounded-xl border transition-all ${
                      selectedColor === c
                        ? 'border-indigo-600 bg-indigo-50 text-indigo-700 font-bold'
                        : 'border-slate-200 text-slate-600 hover:border-slate-300 bg-white'
                    }`}
                  >
                    {c}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Quantity selector */}
          <div className="flex items-center space-x-4">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
              Quantity:
            </span>
            <div className="flex items-center border border-slate-200 rounded-xl bg-white shadow-sm overflow-hidden">
              <button
                onClick={() => setQuantity((q) => Math.max(1, q - 1))}
                className="px-3 py-2 text-slate-600 hover:bg-slate-100 transition-colors"
                disabled={quantity <= 1}
              >
                <Minus className="w-3.5 h-3.5" />
              </button>
              <span className="px-4 py-1 text-xs font-bold text-slate-900">{quantity}</span>
              <button
                onClick={() => setQuantity((q) => Math.min(product.stock, q + 1))}
                className="px-3 py-2 text-slate-600 hover:bg-slate-100 transition-colors"
                disabled={quantity >= product.stock}
              >
                <Plus className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>

          {/* Primary Action Buttons: Add to Cart & Buy Now & Wishlist */}
          <div className="flex flex-col sm:flex-row items-center gap-3 pt-2">
            <button
              onClick={handleAddToCart}
              disabled={addingToCart || product.stock <= 0}
              className={`flex-1 w-full py-3.5 px-6 rounded-2xl text-xs sm:text-sm font-bold flex items-center justify-center gap-2 shadow-md hover:shadow-lg transition-all ${
                addedToast
                  ? 'bg-emerald-600 text-white'
                  : 'bg-indigo-600 hover:bg-indigo-700 text-white'
              }`}
            >
              {addedToast ? (
                <>
                  <Check className="w-4 h-4" /> Added to Cart!
                </>
              ) : (
                <>
                  <ShoppingBag className="w-4 h-4" /> Add to Cart
                </>
              )}
            </button>

            <button
              onClick={handleBuyNow}
              disabled={product.stock <= 0}
              className="flex-1 w-full py-3.5 px-6 rounded-2xl text-xs sm:text-sm font-bold bg-slate-900 hover:bg-slate-800 text-white flex items-center justify-center gap-2 shadow-md hover:shadow-lg transition-all"
            >
              <Zap className="w-4 h-4 text-amber-400 fill-amber-400" /> Buy Now
            </button>

            <button
              onClick={async () => {
                const res = await toggleWishlist(product.id);
                if (!res.added && res.message?.includes('sign in')) onOpenAuth();
              }}
              title={isWishlisted ? 'In Wishlist' : 'Add to Wishlist'}
              className={`p-3.5 rounded-2xl border flex items-center justify-center transition-all ${
                isWishlisted
                  ? 'bg-rose-50 border-rose-200 text-rose-500'
                  : 'bg-white border-slate-200 text-slate-600 hover:text-rose-500'
              }`}
            >
              <Heart className={`w-5 h-5 ${isWishlisted ? 'fill-rose-500' : ''}`} />
            </button>
          </div>

          {/* Trust Guarantees */}
          <div className="grid grid-cols-3 gap-2 pt-4 border-t border-slate-100 text-center">
            <div className="p-3 bg-slate-50 rounded-2xl space-y-1">
              <Truck className="w-4 h-4 text-indigo-600 mx-auto" />
              <p className="text-[11px] font-bold text-slate-800">Free Express Delivery</p>
              <p className="text-[10px] text-slate-400">Within 2-4 days</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-2xl space-y-1">
              <ShieldCheck className="w-4 h-4 text-emerald-600 mx-auto" />
              <p className="text-[11px] font-bold text-slate-800">100% Genuine</p>
              <p className="text-[10px] text-slate-400">Directly from Brand</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-2xl space-y-1">
              <RotateCcw className="w-4 h-4 text-blue-600 mx-auto" />
              <p className="text-[11px] font-bold text-slate-800">7 Days Return</p>
              <p className="text-[10px] text-slate-400">Doorstep Pickup</p>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Description & Technical Specifications */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 space-y-6 shadow-subtle">
        <h3 className="text-lg font-bold text-slate-900 border-b border-slate-100 pb-3">
          Product Overview & Description
        </h3>
        <p className="text-sm text-slate-600 leading-relaxed">
          {product.description}
        </p>

        {product.specifications && Object.keys(product.specifications).length > 0 && (
          <div className="pt-4 border-t border-slate-100">
            <h4 className="text-sm font-bold text-slate-900 mb-4">Technical Specifications</h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              {Object.entries(product.specifications).map(([key, val]) => (
                <div key={key} className="flex items-center justify-between p-3 bg-slate-50 rounded-xl text-xs">
                  <span className="font-semibold text-slate-500">{key}</span>
                  <span className="font-bold text-slate-800">{String(val)}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* 4. Customer Reviews Section */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 space-y-8 shadow-subtle">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-lg font-bold text-slate-900">Customer Reviews & Ratings</h3>
            <p className="text-xs text-slate-500 mt-0.5">Ground truth feedback from verified purchasers</p>
          </div>

          <div className="flex items-center gap-2">
            <div className="flex items-center text-amber-400">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`w-4 h-4 ${i < Math.round(product.rating) ? 'fill-amber-400' : 'text-slate-300'}`}
                />
              ))}
            </div>
            <span className="text-sm font-extrabold text-slate-900">{product.rating.toFixed(1)} / 5</span>
          </div>
        </div>

        {/* Existing Reviews List */}
        <div className="space-y-4">
          {product.reviews && product.reviews.length > 0 ? (
            product.reviews.map((rev) => (
              <div key={rev.id} className="p-4 bg-slate-50/70 rounded-2xl border border-slate-100 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="text-xs font-bold text-slate-900">{rev.user_name}</span>
                    {rev.is_verified_purchase && (
                      <span className="text-[10px] text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full font-semibold">
                        Verified Purchase
                      </span>
                    )}
                  </div>
                  <div className="flex items-center text-amber-400">
                    {[...Array(rev.rating)].map((_, i) => (
                      <Star key={i} className="w-3 h-3 fill-amber-400" />
                    ))}
                  </div>
                </div>
                {rev.title && <p className="text-xs font-bold text-slate-800">{rev.title}</p>}
                <p className="text-xs text-slate-600 leading-relaxed">{rev.comment}</p>
              </div>
            ))
          ) : (
            <p className="text-xs text-slate-400 text-center py-4">No reviews yet. Be the first to share your thoughts!</p>
          )}
        </div>

        {/* Write a review form */}
        <div className="pt-6 border-t border-slate-100">
          <h4 className="text-sm font-bold text-slate-900 mb-3 flex items-center gap-2">
            <MessageSquarePlus className="w-4 h-4 text-indigo-600" />
            Write a Review
          </h4>

          {reviewSuccess ? (
            <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-700 rounded-2xl text-xs font-semibold">
              Thank you! Your verified review has been submitted successfully.
            </div>
          ) : (
            <form onSubmit={handleReviewSubmit} className="space-y-4 max-w-xl">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Your Rating</label>
                <div className="flex items-center space-x-1">
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      type="button"
                      key={star}
                      onClick={() => setReviewRating(star)}
                      className="p-1 hover:scale-110 transition-transform"
                    >
                      <Star
                        className={`w-6 h-6 ${
                          star <= reviewRating ? 'fill-amber-400 text-amber-400' : 'text-slate-300'
                        }`}
                      />
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Headline / Title</label>
                <input
                  type="text"
                  value={reviewTitle}
                  onChange={(e) => setReviewTitle(e.target.value)}
                  placeholder="e.g. Incredible fit and build quality"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-800 focus:outline-none focus:border-indigo-600 focus:bg-white"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Review Comments</label>
                <textarea
                  rows={3}
                  required
                  value={reviewComment}
                  onChange={(e) => setReviewComment(e.target.value)}
                  placeholder="Describe what you liked, sizing accuracy, delivery experience..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-800 focus:outline-none focus:border-indigo-600 focus:bg-white"
                />
              </div>

              <button
                type="submit"
                disabled={submittingReview}
                className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold px-5 py-2.5 rounded-xl shadow-sm transition-colors"
              >
                {submittingReview ? 'Submitting...' : 'Submit Review'}
              </button>
            </form>
          )}
        </div>
      </div>

      {/* 5. Related Products */}
      {product.related_products && product.related_products.length > 0 && (
        <div className="space-y-6 pt-4">
          <div className="flex items-center justify-between">
            <h3 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
              You May Also Like
            </h3>
            <Link
              to={`/products?category=${product.category_slug}`}
              className="text-xs sm:text-sm font-semibold text-indigo-600 hover:underline"
            >
              View More in Category →
            </Link>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
            {product.related_products.slice(0, 4).map((rel) => (
              <ProductCard key={rel.id} product={rel} onOpenAuth={onOpenAuth} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
