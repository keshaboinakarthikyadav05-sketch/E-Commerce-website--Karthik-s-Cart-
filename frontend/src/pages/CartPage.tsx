import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ShoppingBag,
  Trash2,
  Heart,
  Plus,
  Minus,
  ArrowRight,
  ShieldCheck,
  Tag,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  AlertCircle,
  Loader2
} from 'lucide-react';
import { useCart } from '../context/CartContext';
import { useWishlist } from '../context/WishlistContext';
import { useAuth } from '../context/AuthContext';

interface CartPageProps {
  onOpenAuth: () => void;
}

export const CartPage: React.FC<CartPageProps> = ({ onOpenAuth }) => {
  const navigate = useNavigate();
  const {
    cart,
    updateQuantity,
    updateCartItem,
    removeFromCart,
    moveToWishlist,
    clearCart,
    applyCoupon,
    loading
  } = useCart();
  const { fetchWishlist } = useWishlist();
  const { isAuthenticated } = useAuth();

  const [couponCode, setCouponCode] = useState('');
  const [couponFeedback, setCouponFeedback] = useState<{ success: boolean; message: string } | null>(null);
  const [applyingCoupon, setApplyingCoupon] = useState(false);
  const [actionFeedback, setActionFeedback] = useState<{ message: string; isError?: boolean } | null>(null);
  const [busyItemId, setBusyItemId] = useState<number | null>(null);

  if (!isAuthenticated) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-4">
        <div className="w-16 h-16 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center mx-auto">
          <ShoppingBag className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-slate-900">Sign in to view your cart</h2>
        <p className="text-xs text-slate-500">
          Your saved items, coupons, and orders sync across all your devices once you log in.
        </p>
        <button
          onClick={onOpenAuth}
          className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm px-6 py-3 rounded-full transition-colors shadow-sm"
        >
          Sign In / Register
        </button>
      </div>
    );
  }

  const items = cart?.items || [];

  if (loading && items.length === 0) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-4">
        <div className="w-12 h-12 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mx-auto" />
        <p className="text-sm font-semibold text-slate-600">Loading your shopping cart...</p>
      </div>
    );
  }

  if (items.length === 0) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-5">
        <div className="w-20 h-20 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
          <ShoppingBag className="w-10 h-10" />
        </div>
        <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Your Cart is Empty</h2>
        <p className="text-xs sm:text-sm text-slate-500 leading-relaxed">
          Looks like you haven't added anything to your cart yet. Explore our 10+ categories and discover trending deals!
        </p>
        <Link
          to="/products"
          className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm px-6 py-3 rounded-full transition-all shadow-md shadow-indigo-200"
        >
          <span>Start Shopping</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    );
  }

  const handleApplyCoupon = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!couponCode.trim()) return;

    setApplyingCoupon(true);
    const res = await applyCoupon(couponCode.trim());
    setApplyingCoupon(false);
    setCouponFeedback(res);
  };

  const handleMoveToWishlist = async (itemId: number) => {
    setBusyItemId(itemId);
    const res = await moveToWishlist(itemId);
    await fetchWishlist();
    setBusyItemId(null);

    if (res.success) {
      setActionFeedback({ message: res.message, isError: false });
    } else {
      setActionFeedback({ message: res.message, isError: true });
    }
    setTimeout(() => setActionFeedback(null), 4000);
  };

  const handleUpdateQuantity = async (itemId: number, newQty: number) => {
    setBusyItemId(itemId);
    const res = await updateQuantity(itemId, newQty);
    setBusyItemId(null);

    if (!res.success && res.message) {
      setActionFeedback({ message: res.message, isError: true });
      setTimeout(() => setActionFeedback(null), 4000);
    }
  };

  const handleVariantChange = async (itemId: number, field: 'size' | 'color', val: string) => {
    setBusyItemId(itemId);
    const payload = field === 'size' ? { size: val } : { color: val };
    const res = await updateCartItem(itemId, payload);
    setBusyItemId(null);

    if (!res.success && res.message) {
      setActionFeedback({ message: res.message, isError: true });
      setTimeout(() => setActionFeedback(null), 4000);
    }
  };

  const hasStockIssues = Boolean(cart?.has_out_of_stock || cart?.has_exceeded_stock);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Title */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-200">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Shopping Cart
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            You have <span className="font-semibold text-slate-800">{cart?.items_count} items</span> in your cart
          </p>
        </div>
        <button
          onClick={clearCart}
          className="text-xs font-semibold text-rose-600 hover:text-rose-700 hover:underline"
        >
          Clear Cart
        </button>
      </div>

      {/* Global Alert Banners */}
      {actionFeedback && (
        <div
          className={`flex items-center gap-2 p-3.5 rounded-2xl text-xs font-semibold ${
            actionFeedback.isError
              ? 'bg-rose-50 text-rose-700 border border-rose-200'
              : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
          }`}
        >
          {actionFeedback.isError ? (
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
          ) : (
            <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          )}
          <span>{actionFeedback.message}</span>
        </div>
      )}

      {hasStockIssues && (
        <div className="bg-amber-50 border border-amber-200 text-amber-900 p-4 rounded-2xl flex items-start gap-3 text-xs sm:text-sm shadow-sm">
          <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div>
            <p className="font-bold text-slate-900">Some items require your attention</p>
            <p className="text-slate-600 text-xs mt-0.5">
              Items marked as out of stock or with quantities exceeding current inventory cannot be purchased. Please adjust quantities or remove them to proceed.
            </p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        {/* Left: Cart Items List */}
        <div className="lg:col-span-2 space-y-4">
          {items.map((item) => {
            const isOut = Boolean(item.is_out_of_stock);
            const isExceeded = Boolean(item.exceeds_stock);
            const maxStock = item.available_stock !== undefined ? item.available_stock : 999;
            const canIncrease = !isOut && item.quantity < maxStock;
            const isBusy = busyItemId === item.id;

            return (
              <div
                key={item.id}
                className={`bg-white rounded-3xl border transition-all p-4 sm:p-5 shadow-subtle flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between ${
                  isOut
                    ? 'border-rose-300 bg-rose-50/20'
                    : isExceeded
                    ? 'border-amber-300 bg-amber-50/20'
                    : 'border-slate-200/80 hover:border-slate-300'
                }`}
              >
                {/* Image & Title */}
                <div className="flex items-center space-x-4 flex-1 min-w-0">
                  <Link
                    to={`/products/${item.product_id}`}
                    className="w-20 h-20 rounded-2xl overflow-hidden bg-slate-100 flex-shrink-0 border border-slate-200 relative"
                  >
                    <img
                      src={item.product?.primary_image || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=120'}
                      alt={item.product?.name || 'Product'}
                      className={`w-full h-full object-cover ${isOut ? 'grayscale opacity-60' : ''}`}
                    />
                    {isOut && (
                      <span className="absolute inset-0 bg-slate-950/40 flex items-center justify-center text-[9px] font-black uppercase text-white px-1 text-center">
                        Out of stock
                      </span>
                    )}
                  </Link>

                  <div className="flex-1 min-w-0 space-y-1">
                    <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-wider block">
                      {item.product?.brand}
                    </span>
                    <Link
                      to={`/products/${item.product_id}`}
                      className="text-sm font-bold text-slate-900 hover:text-indigo-600 line-clamp-1 transition-colors"
                    >
                      {item.product?.name}
                    </Link>

                    {/* Stock Badges */}
                    <div className="flex flex-wrap items-center gap-1.5 pt-0.5">
                      {isOut && (
                        <span className="inline-flex items-center gap-1 text-[10px] font-extrabold uppercase bg-rose-100 text-rose-700 px-2 py-0.5 rounded-full">
                          Out of Stock
                        </span>
                      )}
                      {isExceeded && !isOut && (
                        <span className="inline-flex items-center gap-1 text-[10px] font-bold bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full">
                          Only {item.available_stock} in stock
                        </span>
                      )}
                      {item.is_low_stock && !isOut && !isExceeded && (
                        <span className="text-[11px] font-semibold text-amber-600">
                          Only {item.available_stock} left!
                        </span>
                      )}
                    </div>

                    {/* Size & Color Variant Selectors */}
                    <div className="flex flex-wrap items-center gap-2 pt-1 text-xs">
                      {item.available_sizes && item.available_sizes.length > 0 ? (
                        <div className="flex items-center gap-1">
                          <label className="text-[10px] text-slate-400 font-bold uppercase">Size:</label>
                          <select
                            value={item.size || ''}
                            disabled={isBusy}
                            onChange={(e) => handleVariantChange(item.id, 'size', e.target.value)}
                            className="bg-slate-100 hover:bg-slate-200 border border-slate-200 rounded-lg px-2 py-0.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-500 cursor-pointer"
                          >
                            {item.available_sizes.map((s) => (
                              <option key={s} value={s}>
                                {s}
                              </option>
                            ))}
                          </select>
                        </div>
                      ) : item.size ? (
                        <span className="bg-slate-100 px-2 py-0.5 rounded-md font-medium text-slate-600">
                          Size: {item.size}
                        </span>
                      ) : null}

                      {item.available_colors && item.available_colors.length > 0 ? (
                        <div className="flex items-center gap-1">
                          <label className="text-[10px] text-slate-400 font-bold uppercase">Color:</label>
                          <select
                            value={item.color || ''}
                            disabled={isBusy}
                            onChange={(e) => handleVariantChange(item.id, 'color', e.target.value)}
                            className="bg-slate-100 hover:bg-slate-200 border border-slate-200 rounded-lg px-2 py-0.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-500 cursor-pointer"
                          >
                            {item.available_colors.map((c) => (
                              <option key={c} value={c}>
                                {c}
                              </option>
                            ))}
                          </select>
                        </div>
                      ) : item.color ? (
                        <span className="bg-slate-100 px-2 py-0.5 rounded-md font-medium text-slate-600">
                          Color: {item.color}
                        </span>
                      ) : null}
                    </div>

                    {/* Unit Price */}
                    <div className="text-xs text-slate-500 font-medium pt-0.5">
                      ₹{item.unit_price.toLocaleString('en-IN')} each
                    </div>
                  </div>
                </div>

                {/* Quantity Controls & Line Total */}
                <div className="flex items-center justify-between w-full sm:w-auto sm:space-x-6 pt-3 sm:pt-0 border-t sm:border-0 border-slate-100">
                  {/* Quantity Buttons */}
                  <div className="flex items-center border border-slate-200 rounded-xl bg-white shadow-sm overflow-hidden">
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity - 1)}
                      disabled={isBusy}
                      title="Decrease quantity"
                      className="px-2.5 py-1.5 text-slate-600 hover:bg-slate-100 transition-colors disabled:opacity-40"
                    >
                      <Minus className="w-3.5 h-3.5" />
                    </button>
                    <span className="px-3 py-1 text-xs font-bold text-slate-900 min-w-[28px] text-center">
                      {isBusy ? <Loader2 className="w-3.5 h-3.5 animate-spin mx-auto text-indigo-600" /> : item.quantity}
                    </span>
                    <button
                      onClick={() => handleUpdateQuantity(item.id, item.quantity + 1)}
                      disabled={isBusy || !canIncrease}
                      title={!canIncrease ? 'Reached max available stock' : 'Increase quantity'}
                      className="px-2.5 py-1.5 text-slate-600 hover:bg-slate-100 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
                    >
                      <Plus className="w-3.5 h-3.5" />
                    </button>
                  </div>

                  {/* Total Price for item */}
                  <div className="text-right min-w-[90px]">
                    <span className="text-sm font-extrabold text-slate-900 block">
                      ₹{item.total_price.toLocaleString('en-IN')}
                    </span>
                  </div>

                  {/* Actions: Move to Wishlist & Remove */}
                  <div className="flex items-center space-x-1">
                    <button
                      onClick={() => handleMoveToWishlist(item.id)}
                      disabled={isBusy}
                      title="Move to Wishlist"
                      className="p-2 text-slate-400 hover:text-rose-500 rounded-lg hover:bg-rose-50 transition-colors"
                    >
                      <Heart className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => removeFromCart(item.id)}
                      disabled={isBusy}
                      title="Remove item"
                      className="p-2 text-slate-400 hover:text-rose-600 rounded-lg hover:bg-slate-100 transition-colors"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}

          <div className="pt-2">
            <Link
              to="/products"
              className="text-xs font-semibold text-indigo-600 hover:text-indigo-700 flex items-center gap-1.5"
            >
              ← Continue Shopping
            </Link>
          </div>
        </div>

        {/* Right: Order Financial Summary & Coupons */}
        <div className="space-y-6">
          {/* Coupon Code Input */}
          <div className="bg-white rounded-3xl border border-slate-200/80 p-5 shadow-subtle space-y-3">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center gap-2">
              <Tag className="w-3.5 h-3.5 text-indigo-600" />
              Apply Discount Coupon
            </h4>
            <form onSubmit={handleApplyCoupon} className="flex gap-2">
              <input
                type="text"
                value={couponCode}
                onChange={(e) => setCouponCode(e.target.value.toUpperCase())}
                placeholder="e.g. KARTHIK10"
                className="flex-1 bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs font-bold uppercase tracking-wider text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-600 focus:bg-white"
              />
              <button
                type="submit"
                disabled={applyingCoupon || !couponCode.trim()}
                className="bg-slate-900 hover:bg-indigo-600 text-white text-xs font-semibold px-4 py-2 rounded-xl transition-colors disabled:opacity-50"
              >
                {applyingCoupon ? 'Checking...' : 'Apply'}
              </button>
            </form>

            {couponFeedback && (
              <div
                className={`flex items-center gap-1.5 text-xs p-2.5 rounded-xl ${
                  couponFeedback.success
                    ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                    : 'bg-rose-50 text-rose-700 border border-rose-200'
                }`}
              >
                {couponFeedback.success ? (
                  <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
                ) : (
                  <XCircle className="w-4 h-4 flex-shrink-0" />
                )}
                <span>{couponFeedback.message}</span>
              </div>
            )}

            <div className="text-[11px] text-slate-400 pt-1 space-y-1">
              <p>
                Available codes:{' '}
                <button
                  type="button"
                  onClick={() => setCouponCode('KARTHIK10')}
                  className="font-bold text-indigo-600 hover:underline"
                >
                  KARTHIK10
                </button>{' '}
                (10% off),{' '}
                <button
                  type="button"
                  onClick={() => setCouponCode('WELCOME200')}
                  className="font-bold text-indigo-600 hover:underline"
                >
                  WELCOME200
                </button>{' '}
                (₹200 off),{' '}
                <button
                  type="button"
                  onClick={() => setCouponCode('FESTIVE500')}
                  className="font-bold text-indigo-600 hover:underline"
                >
                  FESTIVE500
                </button>
              </p>
            </div>
          </div>

          {/* Cost Breakdown Card */}
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-4">
            <h3 className="text-base font-bold text-slate-900 pb-3 border-b border-slate-100">
              Order Summary
            </h3>

            <div className="space-y-2.5 text-xs">
              <div className="flex justify-between text-slate-600">
                <span>Subtotal ({cart?.items_count} items)</span>
                <span className="font-semibold text-slate-800">
                  ₹{cart?.subtotal.toLocaleString('en-IN')}
                </span>
              </div>

              {cart?.discount && cart.discount > 0 ? (
                <div className="flex justify-between text-emerald-600 font-semibold">
                  <span>Coupon Discount</span>
                  <span>- ₹{cart.discount.toLocaleString('en-IN')}</span>
                </div>
              ) : null}

              <div className="flex justify-between text-slate-600">
                <span>Delivery Charges</span>
                <span>
                  {cart?.delivery_charge === 0 ? (
                    <span className="text-emerald-600 font-bold">FREE</span>
                  ) : (
                    `₹${cart?.delivery_charge}`
                  )}
                </span>
              </div>

              {cart?.subtotal && cart.subtotal < 999 && cart.subtotal > 0 ? (
                <p className="text-[11px] text-indigo-600 bg-indigo-50 p-2 rounded-xl">
                  Add ₹{(999 - cart.subtotal).toFixed(0)} more to get FREE Delivery!
                </p>
              ) : null}
            </div>

            <div className="pt-3 border-t border-slate-100 flex items-baseline justify-between">
              <span className="text-sm font-bold text-slate-900">Total Payable</span>
              <span className="text-2xl font-black text-indigo-600">
                ₹{cart?.final_total.toLocaleString('en-IN')}
              </span>
            </div>

            <button
              disabled={!cart?.can_checkout}
              onClick={() => navigate('/checkout')}
              className={`w-full font-bold py-3.5 rounded-2xl transition-all text-xs sm:text-sm flex items-center justify-center gap-2 ${
                cart?.can_checkout
                  ? 'bg-indigo-600 hover:bg-indigo-700 text-white shadow-md hover:shadow-lg active:scale-98'
                  : 'bg-slate-200 text-slate-400 cursor-not-allowed shadow-none'
              }`}
            >
              <span>Proceed to Checkout</span>
              <ArrowRight className="w-4 h-4" />
            </button>

            {!cart?.can_checkout && (
              <p className="text-[11px] text-rose-600 font-medium text-center">
                {hasStockIssues
                  ? 'Please resolve out-of-stock items before checkout'
                  : 'Your cart is not ready for checkout'}
              </p>
            )}

            <div className="flex items-center justify-center gap-2 text-[11px] text-slate-400 pt-2">
              <ShieldCheck className="w-4 h-4 text-emerald-500" />
              <span>Safe & Secure 256-bit Encrypted Checkout</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
