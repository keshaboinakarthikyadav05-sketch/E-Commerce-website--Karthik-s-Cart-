import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate, Link } from 'react-router-dom';
import {
  ShieldCheck,
  CreditCard,
  Banknote,
  MapPin,
  Phone,
  User,
  CheckCircle2,
  AlertCircle,
  Lock,
  ArrowRight,
  Truck,
  Smartphone,
  Building2,
  X,
  Sparkles,
  Loader2
} from 'lucide-react';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { ordersApi, paymentsApi, authApi } from '../services/api';
import { Address } from '../types';

declare global {
  interface Window {
    Razorpay: any;
  }
}

export const CheckoutPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { cart, clearCart } = useCart();
  const { user, isAuthenticated } = useAuth();

  // Buy now item if navigated directly from product page
  const buyNowItem = location.state?.buyNowItem;

  // Address state
  const [savedAddresses, setSavedAddresses] = useState<Address[]>([]);
  const [selectedAddressId, setSelectedAddressId] = useState<number | 'new'>('new');

  // Address Form state
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [mobileNumber, setMobileNumber] = useState(user?.mobile_number || '');
  const [addressLine1, setAddressLine1] = useState('');
  const [addressLine2, setAddressLine2] = useState('');
  const [city, setCity] = useState('');
  const [state, setState] = useState('');
  const [postalCode, setPostalCode] = useState('');

  // Payment method
  const [paymentMethod, setPaymentMethod] = useState<'razorpay' | 'cod'>('razorpay');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // In-app Payment Gateway Modal state (Razorpay test / sandbox integration)
  const [paymentModalOpen, setPaymentModalOpen] = useState(false);
  const [pendingOrder, setPendingOrder] = useState<any>(null);
  const [pendingRazorpayData, setPendingRazorpayData] = useState<any>(null);
  const [activePaymentTab, setActivePaymentTab] = useState<'upi' | 'card' | 'netbanking'>('upi');
  const [upiId, setUpiId] = useState('karthik@okhdfcbank');
  const [cardNumber, setCardNumber] = useState('4532 8901 2345 8821');
  const [cardExpiry, setCardExpiry] = useState('08/29');
  const [cardCvv, setCardCvv] = useState('739');
  const [selectedBank, setSelectedBank] = useState('HDFC Bank');
  const [verifyingPayment, setVerifyingPayment] = useState(false);

  // Fetch saved addresses
  useEffect(() => {
    if (isAuthenticated) {
      authApi.getAddresses().then((res) => {
        if (res.data?.success && res.data.addresses?.length > 0) {
          const list = res.data.addresses;
          setSavedAddresses(list);
          const defaultAddr = list.find((a: Address) => a.is_default) || list[0];
          setSelectedAddressId(defaultAddr.id || 'new');
          setFullName(defaultAddr.full_name);
          setMobileNumber(defaultAddr.mobile_number);
          setAddressLine1(defaultAddr.address_line1);
          setAddressLine2(defaultAddr.address_line2 || '');
          setCity(defaultAddr.city);
          setState(defaultAddr.state);
          setPostalCode(defaultAddr.postal_code);
        }
      }).catch(() => {});
    }
  }, [isAuthenticated]);

  if (!isAuthenticated) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-4">
        <h2 className="text-2xl font-bold text-slate-900">Authentication Required</h2>
        <p className="text-xs text-slate-500">Please sign in to proceed with secure checkout.</p>
        <Link to="/login" className="inline-block bg-indigo-600 text-white font-semibold text-xs px-6 py-2.5 rounded-full">
          Sign In to Continue
        </Link>
      </div>
    );
  }

  // Calculate items and pricing
  const isBuyNow = !!buyNowItem;
  const items = isBuyNow ? [buyNowItem] : (cart?.items || []);

  const subtotal = isBuyNow
    ? buyNowItem.price * buyNowItem.quantity
    : (cart?.subtotal || 0);

  const discount = isBuyNow ? 0 : (cart?.discount || 0);
  const deliveryCharge = (subtotal >= 999 || subtotal === 0) ? 0 : 99;
  const finalTotal = Math.max(0, subtotal - discount + deliveryCharge);

  if (items.length === 0) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-4">
        <h2 className="text-2xl font-bold text-slate-900">No Items to Checkout</h2>
        <p className="text-xs text-slate-500">Your cart is empty. Please select products to purchase.</p>
        <Link to="/products" className="inline-block bg-indigo-600 text-white font-semibold text-xs px-6 py-2.5 rounded-full">
          Browse Catalog
        </Link>
      </div>
    );
  }

  const handleAddressSelect = (id: number | 'new') => {
    setSelectedAddressId(id);
    if (id === 'new') {
      setFullName(user?.full_name || '');
      setMobileNumber(user?.mobile_number || '');
      setAddressLine1('');
      setAddressLine2('');
      setCity('');
      setState('');
      setPostalCode('');
    } else {
      const addr = savedAddresses.find((a) => a.id === id);
      if (addr) {
        setFullName(addr.full_name);
        setMobileNumber(addr.mobile_number);
        setAddressLine1(addr.address_line1);
        setAddressLine2(addr.address_line2 || '');
        setCity(addr.city);
        setState(addr.state);
        setPostalCode(addr.postal_code);
      }
    }
  };

  const handlePlaceOrder = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!fullName || !mobileNumber || !addressLine1 || !city || !state || !postalCode) {
      setErrorMessage('Please fill out all required shipping address fields');
      return;
    }

    setLoading(true);

    try {
      const orderPayload: any = {
        shipping_address: {
          full_name: fullName,
          mobile_number: mobileNumber,
          address_line1: addressLine1,
          address_line2: addressLine2,
          city,
          state,
          postal_code: postalCode,
        },
        payment_method: paymentMethod,
        coupon_code: isBuyNow ? undefined : cart?.applied_coupon?.code,
      };

      if (isBuyNow) {
        orderPayload.buy_now_item = {
          product_id: buyNowItem.product_id,
          quantity: buyNowItem.quantity,
          size: buyNowItem.size,
          color: buyNowItem.color,
        };
      }

      // 1. Create order on backend (strictly calculates pricing & validates stock)
      const res = await ordersApi.createOrder(orderPayload);

      if (!res.data?.success) {
        setErrorMessage(res.data?.message || 'Could not create order');
        setLoading(false);
        return;
      }

      const order = res.data.order;

      // 2. Handle Cash on Delivery (COD)
      if (paymentMethod === 'cod') {
        if (!isBuyNow) clearCart();
        setLoading(false);
        navigate(`/order-success/${order.id}`, { state: { order } });
        return;
      }

      // 3. Handle Online Payment Flow
      const razorpayData = res.data.razorpay;
      setPendingOrder(order);
      setPendingRazorpayData(razorpayData);

      // If user has provided real merchant Razorpay keys (not placeholder), open standard SDK
      const hasRealKeys = razorpayData.key_id &&
        !razorpayData.key_id.includes('shopora') &&
        !razorpayData.key_id.includes('karthik') &&
        window.Razorpay;

      if (hasRealKeys) {
        const options = {
          key: razorpayData.key_id,
          amount: razorpayData.amount_paise,
          currency: razorpayData.currency,
          name: "Karthik's Cart",
          description: `Order #${order.order_number}`,
          order_id: razorpayData.order_id,
          prefill: {
            name: fullName,
            contact: mobileNumber,
            email: user?.email || '',
          },
          theme: {
            color: '#4f46e5',
          },
          handler: async function (response: any) {
            await completePaymentVerification(
              order.id,
              response.razorpay_order_id,
              response.razorpay_payment_id,
              response.razorpay_signature
            );
          },
          modal: {
            ondismiss: function () {
              setLoading(false);
              setErrorMessage('Payment cancelled. You can try again or select Cash on Delivery.');
            },
          },
        };

        const rzp = new window.Razorpay(options);
        rzp.on('payment.failed', function (resp: any) {
          setLoading(false);
          setErrorMessage(`Payment Failed: ${resp.error?.description || 'Transaction declined'}`);
        });
        rzp.open();
      } else {
        // Open the interactive Karthik's Cart Payment Gateway (Razorpay Test Mode)
        setLoading(false);
        setPaymentModalOpen(true);
      }

    } catch (err: any) {
      setErrorMessage(err.response?.data?.message || 'Failed to initialize order');
      setLoading(false);
    }
  };

  // Complete cryptographic payment verification with backend
  const completePaymentVerification = async (
    orderId: number,
    rzpOrderId: string,
    paymentId: string,
    signature: string
  ) => {
    setVerifyingPayment(true);
    setErrorMessage(null);

    try {
      const verifyRes = await paymentsApi.verifyPayment({
        order_id: orderId,
        razorpay_order_id: rzpOrderId,
        razorpay_payment_id: paymentId,
        razorpay_signature: signature,
      });

      if (verifyRes.data?.success) {
        if (!isBuyNow) clearCart();
        setPaymentModalOpen(false);
        navigate(`/order-success/${orderId}`, { state: { order: verifyRes.data.order } });
      } else {
        setErrorMessage(verifyRes.data?.message || 'Payment verification failed');
      }
    } catch (err: any) {
      setErrorMessage(err.response?.data?.message || 'Payment verification failed');
    } finally {
      setVerifyingPayment(false);
      setLoading(false);
    }
  };

  // Trigger simulated successful payment
  const handleAuthorizePayment = async () => {
    if (!pendingOrder || !pendingRazorpayData) return;
    const simulatedPaymentId = `pay_${Date.now()}`;
    const testSignature = `test_sig_${pendingRazorpayData.order_id}`;

    await completePaymentVerification(
      pendingOrder.id,
      pendingRazorpayData.order_id,
      simulatedPaymentId,
      testSignature
    );
  };

  // Simulate failed payment
  const handleSimulateFailure = () => {
    setPaymentModalOpen(false);
    setLoading(false);
    setErrorMessage('Payment simulation failed: Transaction declined by bank. You can retry payment or switch to Cash on Delivery.');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Title */}
      <div className="pb-4 border-b border-slate-200">
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Secure Checkout
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Review shipping address and choose your preferred payment method on Karthik's Cart
        </p>
      </div>

      {errorMessage && (
        <div className="flex items-center gap-2 p-4 bg-rose-50 border border-rose-200 text-rose-700 rounded-2xl text-xs font-semibold">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      <form onSubmit={handlePlaceOrder} className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        {/* Left Column: Delivery Address & Payment Method */}
        <div className="lg:col-span-2 space-y-6">
          {/* Section 1: Delivery Address */}
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-4">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2 pb-3 border-b border-slate-100">
              <MapPin className="w-4 h-4 text-indigo-600" />
              1. Delivery Address
            </h3>

            {/* Saved Addresses Selector */}
            {savedAddresses.length > 0 && (
              <div className="space-y-2 mb-4">
                <p className="text-xs font-semibold text-slate-500">Choose saved address:</p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {savedAddresses.map((addr) => (
                    <div
                      key={addr.id}
                      onClick={() => handleAddressSelect(addr.id!)}
                      className={`p-3 rounded-2xl border text-xs cursor-pointer transition-all ${
                        selectedAddressId === addr.id
                          ? 'border-indigo-600 bg-indigo-50/60 ring-2 ring-indigo-600/20'
                          : 'border-slate-200 hover:border-slate-300'
                      }`}
                    >
                      <p className="font-bold text-slate-800">{addr.full_name}</p>
                      <p className="text-slate-500 truncate">{addr.address_line1}, {addr.city}</p>
                      <p className="text-slate-400 mt-1">{addr.mobile_number}</p>
                    </div>
                  ))}
                  <div
                    onClick={() => handleAddressSelect('new')}
                    className={`p-3 rounded-2xl border border-dashed text-xs cursor-pointer flex items-center justify-center font-semibold transition-all ${
                      selectedAddressId === 'new'
                        ? 'border-indigo-600 bg-indigo-50/60 text-indigo-700'
                        : 'border-slate-300 text-slate-500 hover:border-slate-400'
                    }`}
                  >
                    + Enter New Address
                  </div>
                </div>
              </div>
            )}

            {/* Address Input Fields */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
                <div className="relative">
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Recipient's Name"
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 pl-9 text-xs text-slate-800 focus:outline-none focus:border-indigo-600"
                  />
                  <User className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">Mobile Number</label>
                <div className="relative">
                  <input
                    type="tel"
                    required
                    value={mobileNumber}
                    onChange={(e) => setMobileNumber(e.target.value)}
                    placeholder="10-digit mobile number"
                    className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 pl-9 text-xs text-slate-800 focus:outline-none focus:border-indigo-600"
                  />
                  <Phone className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                </div>
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-700 mb-1">Street Address</label>
                <input
                  type="text"
                  required
                  value={addressLine1}
                  onChange={(e) => setAddressLine1(e.target.value)}
                  placeholder="Street address, area or sector"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-800 focus:outline-none focus:border-indigo-600"
                />
              </div>

              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-700 mb-1">Address Line 2 / Landmark (Optional)</label>
                <input
                  type="text"
                  value={addressLine2}
                  onChange={(e) => setAddressLine2(e.target.value)}
                  placeholder="Near landmark or apartment name"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-800 focus:outline-none focus:border-indigo-600"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">City</label>
                <input
                  type="text"
                  required
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  placeholder="City"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-800 focus:outline-none focus:border-indigo-600"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">State</label>
                <input
                  type="text"
                  required
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  placeholder="State"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-800 focus:outline-none focus:border-indigo-600"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">PIN Code</label>
                <input
                  type="text"
                  required
                  value={postalCode}
                  onChange={(e) => setPostalCode(e.target.value)}
                  placeholder="6-digit PIN code"
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs text-slate-800 focus:outline-none focus:border-indigo-600"
                />
              </div>
            </div>
          </div>

          {/* Section 2: Payment Method */}
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-4">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2 pb-3 border-b border-slate-100">
              <CreditCard className="w-4 h-4 text-indigo-600" />
              2. Payment Method
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {/* Online Payment (Razorpay) */}
              <label
                className={`p-4 rounded-2xl border-2 flex items-start space-x-3 cursor-pointer transition-all ${
                  paymentMethod === 'razorpay'
                    ? 'border-indigo-600 bg-indigo-50/50 shadow-sm'
                    : 'border-slate-200 hover:border-slate-300'
                }`}
              >
                <input
                  type="radio"
                  name="payment_method"
                  value="razorpay"
                  checked={paymentMethod === 'razorpay'}
                  onChange={() => setPaymentMethod('razorpay')}
                  className="mt-1 text-indigo-600 focus:ring-indigo-500"
                />
                <div className="space-y-1">
                  <div className="flex items-center gap-1.5">
                    <span className="text-sm font-bold text-slate-900">Online Payment</span>
                    <span className="bg-indigo-600 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">
                      Razorpay Verified
                    </span>
                  </div>
                  <p className="text-xs text-slate-500">
                    UPI, Credit/Debit Cards, NetBanking & Wallets. 100% Encrypted.
                  </p>
                </div>
              </label>

              {/* Cash on Delivery */}
              <label
                className={`p-4 rounded-2xl border-2 flex items-start space-x-3 cursor-pointer transition-all ${
                  paymentMethod === 'cod'
                    ? 'border-indigo-600 bg-indigo-50/50 shadow-sm'
                    : 'border-slate-200 hover:border-slate-300'
                }`}
              >
                <input
                  type="radio"
                  name="payment_method"
                  value="cod"
                  checked={paymentMethod === 'cod'}
                  onChange={() => setPaymentMethod('cod')}
                  className="mt-1 text-indigo-600 focus:ring-indigo-500"
                />
                <div className="space-y-1">
                  <div className="flex items-center gap-1.5">
                    <span className="text-sm font-bold text-slate-900">Cash on Delivery (COD)</span>
                  </div>
                  <p className="text-xs text-slate-500">
                    Pay securely with cash or UPI at your doorstep upon delivery.
                  </p>
                </div>
              </label>
            </div>
          </div>
        </div>

        {/* Right Column: Order Review & Final Pay Button */}
        <div className="space-y-6">
          <div className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-4">
            <h3 className="text-base font-bold text-slate-900 pb-3 border-b border-slate-100">
              Items in Order ({items.length})
            </h3>

            {/* Items summary preview */}
            <div className="space-y-3 max-h-56 overflow-y-auto pr-1">
              {items.map((it, idx) => (
                <div key={idx} className="flex items-center space-x-3 text-xs">
                  <img
                    src={it.product?.primary_image || it.product_image || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=80'}
                    alt=""
                    className="w-12 h-12 object-cover rounded-xl border border-slate-200"
                  />
                  <div className="flex-1 min-w-0">
                    <p className="font-semibold text-slate-900 truncate">
                      {it.product?.name || it.product_name}
                    </p>
                    <p className="text-slate-400">Qty: {it.quantity} {it.size ? `• Size: ${it.size}` : ''}</p>
                  </div>
                  <span className="font-bold text-slate-800">
                    ₹{((it.unit_price || it.price) * it.quantity).toLocaleString('en-IN')}
                  </span>
                </div>
              ))}
            </div>

            {/* Financials */}
            <div className="pt-3 border-t border-slate-100 space-y-2 text-xs">
              <div className="flex justify-between text-slate-600">
                <span>Subtotal</span>
                <span className="font-semibold">₹{subtotal.toLocaleString('en-IN')}</span>
              </div>
              {discount > 0 && (
                <div className="flex justify-between text-emerald-600 font-semibold">
                  <span>Coupon Discount</span>
                  <span>- ₹{discount.toLocaleString('en-IN')}</span>
                </div>
              )}
              <div className="flex justify-between text-slate-600">
                <span>Delivery Charges</span>
                <span>{deliveryCharge === 0 ? <span className="text-emerald-600 font-bold">FREE</span> : `₹${deliveryCharge}`}</span>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-100 flex items-baseline justify-between">
              <span className="text-sm font-bold text-slate-900">Total Amount</span>
              <span className="text-2xl font-black text-indigo-600">
                ₹{finalTotal.toLocaleString('en-IN')}
              </span>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-3.5 rounded-2xl shadow-md hover:shadow-lg transition-all text-xs sm:text-sm flex items-center justify-center gap-2 disabled:opacity-60"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Processing Order...</span>
                </>
              ) : paymentMethod === 'razorpay' ? (
                <>
                  <Lock className="w-4 h-4" />
                  <span>Pay ₹{finalTotal.toLocaleString('en-IN')} Online</span>
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Place COD Order</span>
                </>
              )}
            </button>

            <p className="text-[11px] text-center text-slate-400">
              By confirming, you agree to Karthik's Cart's Terms & Conditions.
            </p>
          </div>
        </div>
      </form>

      {/* 4. Interactive Payment Gateway Modal (Razorpay Online Checkout) */}
      {paymentModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/70 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="relative w-full max-w-lg bg-white rounded-3xl shadow-2xl border border-slate-200 overflow-hidden">
            {/* Modal Header */}
            <div className="bg-slate-900 text-white p-5 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center font-black text-lg text-white">
                  K
                </div>
                <div>
                  <h3 className="text-base font-extrabold tracking-tight">
                    Karthik's Cart Payment Gateway
                  </h3>
                  <p className="text-[11px] text-slate-400 flex items-center gap-1.5">
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                    Powered by Razorpay • 256-bit Encrypted
                  </p>
                </div>
              </div>
              <button
                onClick={() => setPaymentModalOpen(false)}
                className="text-slate-400 hover:text-white p-1 rounded-full hover:bg-slate-800 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Payable Amount Highlight */}
            <div className="bg-indigo-50/80 px-6 py-4 flex items-center justify-between border-b border-indigo-100">
              <div>
                <p className="text-xs text-slate-500 font-medium">Payable Order Amount</p>
                <p className="text-xs text-indigo-700 font-bold">Order #{pendingOrder?.order_number}</p>
              </div>
              <div className="text-2xl font-black text-slate-900">
                ₹{finalTotal.toLocaleString('en-IN')}
              </div>
            </div>

            {/* Payment Method Selector Tabs */}
            <div className="p-6 space-y-5">
              <div className="grid grid-cols-3 gap-2 bg-slate-100 p-1.5 rounded-2xl text-xs font-bold text-slate-600">
                <button
                  type="button"
                  onClick={() => setActivePaymentTab('upi')}
                  className={`py-2 px-3 rounded-xl flex items-center justify-center gap-1.5 transition-all ${
                    activePaymentTab === 'upi' ? 'bg-white text-indigo-600 shadow-sm' : 'hover:text-slate-900'
                  }`}
                >
                  <Smartphone className="w-3.5 h-3.5" />
                  <span>UPI</span>
                </button>
                <button
                  type="button"
                  onClick={() => setActivePaymentTab('card')}
                  className={`py-2 px-3 rounded-xl flex items-center justify-center gap-1.5 transition-all ${
                    activePaymentTab === 'card' ? 'bg-white text-indigo-600 shadow-sm' : 'hover:text-slate-900'
                  }`}
                >
                  <CreditCard className="w-3.5 h-3.5" />
                  <span>Card</span>
                </button>
                <button
                  type="button"
                  onClick={() => setActivePaymentTab('netbanking')}
                  className={`py-2 px-3 rounded-xl flex items-center justify-center gap-1.5 transition-all ${
                    activePaymentTab === 'netbanking' ? 'bg-white text-indigo-600 shadow-sm' : 'hover:text-slate-900'
                  }`}
                >
                  <Building2 className="w-3.5 h-3.5" />
                  <span>NetBanking</span>
                </button>
              </div>

              {/* Tab 1: UPI */}
              {activePaymentTab === 'upi' && (
                <div className="space-y-3.5">
                  <label className="block text-xs font-semibold text-slate-700">Enter UPI ID / VPA</label>
                  <div className="relative">
                    <input
                      type="text"
                      value={upiId}
                      onChange={(e) => setUpiId(e.target.value)}
                      placeholder="mobileNumber@upi"
                      className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm font-semibold text-slate-900 focus:outline-none focus:border-indigo-600"
                    />
                    <span className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[11px] font-bold text-emerald-600">
                      Verified
                    </span>
                  </div>
                  <div className="flex flex-wrap gap-2 pt-1 text-xs">
                    {['Google Pay', 'PhonePe', 'Paytm', 'BHIM'].map((app) => (
                      <button
                        key={app}
                        type="button"
                        onClick={() => setUpiId(`karthik@${app.toLowerCase().replace(/\s+/g, '')}`)}
                        className="bg-slate-100 hover:bg-indigo-50 hover:text-indigo-600 px-3 py-1.5 rounded-lg border border-slate-200 font-medium transition-colors"
                      >
                        {app}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Tab 2: Credit / Debit Card */}
              {activePaymentTab === 'card' && (
                <div className="space-y-3">
                  <div>
                    <label className="block text-xs font-semibold text-slate-700 mb-1">Card Number</label>
                    <input
                      type="text"
                      value={cardNumber}
                      onChange={(e) => setCardNumber(e.target.value)}
                      className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs sm:text-sm font-semibold text-slate-900 focus:outline-none focus:border-indigo-600"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">Expiry</label>
                      <input
                        type="text"
                        value={cardExpiry}
                        onChange={(e) => setCardExpiry(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs sm:text-sm font-semibold text-slate-900 focus:outline-none focus:border-indigo-600"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-semibold text-slate-700 mb-1">CVV</label>
                      <input
                        type="password"
                        maxLength={4}
                        value={cardCvv}
                        onChange={(e) => setCardCvv(e.target.value)}
                        className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2 text-xs sm:text-sm font-semibold text-slate-900 focus:outline-none focus:border-indigo-600"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* Tab 3: Net Banking */}
              {activePaymentTab === 'netbanking' && (
                <div className="space-y-3">
                  <label className="block text-xs font-semibold text-slate-700">Select Popular Bank</label>
                  <div className="grid grid-cols-2 gap-2">
                    {['HDFC Bank', 'ICICI Bank', 'State Bank of India', 'Axis Bank', 'Kotak Mahindra', 'Punjab National Bank'].map((b) => (
                      <button
                        key={b}
                        type="button"
                        onClick={() => setSelectedBank(b)}
                        className={`text-xs p-2.5 rounded-xl border text-left font-semibold transition-all ${
                          selectedBank === b
                            ? 'border-indigo-600 bg-indigo-50/70 text-indigo-700 ring-2 ring-indigo-600/20'
                            : 'border-slate-200 hover:border-slate-300 text-slate-700'
                        }`}
                      >
                        {b}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Verification & Pay Action Buttons */}
              <div className="pt-2 space-y-2.5">
                <button
                  type="button"
                  disabled={verifyingPayment}
                  onClick={handleAuthorizePayment}
                  className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3.5 rounded-2xl shadow-md hover:shadow-lg transition-all text-xs sm:text-sm flex items-center justify-center gap-2 disabled:opacity-60"
                >
                  {verifyingPayment ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Verifying & Completing Order...</span>
                    </>
                  ) : (
                    <>
                      <Lock className="w-4 h-4" />
                      <span>Authorize Payment of ₹{finalTotal.toLocaleString('en-IN')}</span>
                    </>
                  )}
                </button>

                <div className="flex items-center justify-between text-xs pt-1">
                  <button
                    type="button"
                    onClick={handleSimulateFailure}
                    className="text-rose-600 hover:underline text-[11px] font-semibold"
                  >
                    Test Payment Failure
                  </button>
                  <button
                    type="button"
                    onClick={() => setPaymentModalOpen(false)}
                    className="text-slate-400 hover:text-slate-600 text-[11px] font-medium"
                  >
                    Cancel Transaction
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
