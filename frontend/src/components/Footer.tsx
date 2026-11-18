import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  ShoppingBag,
  Mail,
  ShieldCheck,
  Truck,
  RotateCcw,
  Headphones,
  CheckCircle2,
  Lock
} from 'lucide-react';

export const Footer: React.FC = () => {
  const [email, setEmail] = useState('');
  const [subscribed, setSubscribed] = useState(false);

  const handleSubscribe = (e: React.FormEvent) => {
    e.preventDefault();
    if (email.trim()) {
      setSubscribed(true);
      setEmail('');
    }
  };

  return (
    <footer className="bg-slate-900 text-slate-300 pt-16 pb-12 border-t border-slate-800">
      {/* 1. Value Proposition Highlights */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12 border-b border-slate-800">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div className="flex items-center space-x-3.5">
            <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center flex-shrink-0">
              <Truck className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-white text-sm font-semibold">Free Express Shipping</h4>
              <p className="text-xs text-slate-400">On all prepaid orders over ₹999</p>
            </div>
          </div>

          <div className="flex items-center space-x-3.5">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-white text-sm font-semibold">100% Genuine Guarantee</h4>
              <p className="text-xs text-slate-400">Directly sourced authentic brands</p>
            </div>
          </div>

          <div className="flex items-center space-x-3.5">
            <div className="w-12 h-12 rounded-2xl bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center flex-shrink-0">
              <RotateCcw className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-white text-sm font-semibold">7 Days Easy Return</h4>
              <p className="text-xs text-slate-400">Hassle-free doorstep pickup</p>
            </div>
          </div>

          <div className="flex items-center space-x-3.5">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-amber-400 flex items-center justify-center flex-shrink-0">
              <Headphones className="w-6 h-6" />
            </div>
            <div>
              <h4 className="text-white text-sm font-semibold">24/7 Priority Support</h4>
              <p className="text-xs text-slate-400">Dedicated shopping concierge</p>
            </div>
          </div>
        </div>
      </div>

      {/* 2. Main Footer Sitemaps */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-10">
          {/* Brand Info */}
          <div className="lg:col-span-2 space-y-4">
            <Link to="/" className="flex items-center space-x-2.5">
              <div className="w-9 h-9 rounded-xl bg-indigo-600 flex items-center justify-center text-white font-black text-lg">
                K
              </div>
              <span className="text-2xl font-black tracking-tight text-white">
                Karthik's <span className="text-indigo-400">Cart</span>
              </span>
            </Link>
            <p className="text-sm text-slate-400 leading-relaxed max-w-sm">
              India's premier digital shopping destination for trendsetting fashion, cutting-edge electronics, flagship smartphones, and luxury accessories.
            </p>
            <div className="pt-2">
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                Subscribe for Exclusive Previews & VIP Sales
              </p>
              {subscribed ? (
                <div className="flex items-center gap-2 text-xs text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-2 rounded-xl">
                  <CheckCircle2 className="w-4 h-4" /> Thank you for subscribing!
                </div>
              ) : (
                <form onSubmit={handleSubscribe} className="flex gap-2 max-w-sm">
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter your email"
                    className="flex-1 bg-slate-800 border border-slate-700 rounded-xl px-3.5 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500"
                  />
                  <button
                    type="submit"
                    className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold px-4 py-2 rounded-xl transition-colors"
                  >
                    Join
                  </button>
                </form>
              )}
            </div>
          </div>

          {/* Categories */}
          <div>
            <h5 className="text-white text-sm font-semibold mb-4 tracking-wider uppercase">Shop Categories</h5>
            <ul className="space-y-2 text-xs text-slate-400">
              <li><Link to="/products?category=mens-pants" className="hover:text-white transition-colors">Men's Pants & Chinos</Link></li>
              <li><Link to="/products?category=womens-pants" className="hover:text-white transition-colors">Women's Trousers & Denim</Link></li>
              <li><Link to="/products?category=smartphones" className="hover:text-white transition-colors">Flagship 5G Smartphones</Link></li>
              <li><Link to="/products?category=laptops" className="hover:text-white transition-colors">AI & Gaming Laptops</Link></li>
              <li><Link to="/products?category=headphones" className="hover:text-white transition-colors">Wireless Audio & ANC</Link></li>
              <li><Link to="/products?category=watches" className="hover:text-white transition-colors">Luxury & Smart Watches</Link></li>
              <li><Link to="/products?category=shoes" className="hover:text-white transition-colors">Sneakers & Performance Shoes</Link></li>
            </ul>
          </div>

          {/* Quick Links */}
          <div>
            <h5 className="text-white text-sm font-semibold mb-4 tracking-wider uppercase">Customer Service</h5>
            <ul className="space-y-2 text-xs text-slate-400">
              <li><Link to="/orders" className="hover:text-white transition-colors">Track My Order</Link></li>
              <li><Link to="/cart" className="hover:text-white transition-colors">Shopping Cart</Link></li>
              <li><Link to="/wishlist" className="hover:text-white transition-colors">My Wishlist</Link></li>
              <li><a href="#faq" className="hover:text-white transition-colors">Shipping & Delivery Policies</a></li>
              <li><a href="#faq" className="hover:text-white transition-colors">Return & Cancellation Policy</a></li>
              <li><a href="#faq" className="hover:text-white transition-colors">Razorpay Payment Help</a></li>
            </ul>
          </div>

          {/* Trust & Payments */}
          <div>
            <h5 className="text-white text-sm font-semibold mb-4 tracking-wider uppercase">Payment Security</h5>
            <p className="text-xs text-slate-400 mb-3">
              All transactions are encrypted with 256-bit SSL technology. Verified by Razorpay.
            </p>
            <div className="flex items-center gap-1.5 text-xs text-slate-300 font-medium bg-slate-800/80 px-3 py-2 rounded-xl border border-slate-700 mb-3">
              <Lock className="w-3.5 h-3.5 text-emerald-400" />
              <span>Razorpay Verified Gateway</span>
            </div>
            <div className="flex flex-wrap gap-2 text-[10px] text-slate-400">
              <span className="bg-slate-800 px-2 py-1 rounded border border-slate-700">UPI</span>
              <span className="bg-slate-800 px-2 py-1 rounded border border-slate-700">Google Pay</span>
              <span className="bg-slate-800 px-2 py-1 rounded border border-slate-700">Paytm</span>
              <span className="bg-slate-800 px-2 py-1 rounded border border-slate-700">Credit / Debit</span>
              <span className="bg-slate-800 px-2 py-1 rounded border border-slate-700">Cash on Delivery</span>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Bottom Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
        <p>© 2026 Karthik's Cart Technologies Pvt. Ltd. All rights reserved.</p>
        <div className="flex space-x-6">
          <a href="#privacy" className="hover:text-slate-400">Privacy Policy</a>
          <a href="#terms" className="hover:text-slate-400">Terms of Service</a>
          <a href="#security" className="hover:text-slate-400">Security</a>
        </div>
      </div>
    </footer>
  );
};
