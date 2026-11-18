import React, { useEffect, useState } from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';
import {
  CheckCircle,
  Package,
  Calendar,
  MapPin,
  CreditCard,
  ArrowRight,
  ShoppingBag,
  Sparkles
} from 'lucide-react';
import { ordersApi } from '../services/api';
import { Order } from '../types';

export const OrderSuccessPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const location = useLocation();

  const [order, setOrder] = useState<Order | null>(location.state?.order || null);
  const [loading, setLoading] = useState(!order);

  useEffect(() => {
    if (!order && id) {
      ordersApi.getOrderById(id).then((res) => {
        if (res.data?.success) setOrder(res.data.order);
      }).catch(console.error).finally(() => setLoading(false));
    }
  }, [id, order]);

  // Estimated delivery date (3-5 days ahead)
  const deliveryDate = new Date();
  deliveryDate.setDate(deliveryDate.getDate() + 4);
  const formattedDelivery = deliveryDate.toLocaleDateString('en-IN', {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });

  if (loading) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center">
        <div className="inline-block w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mb-3" />
        <p className="text-xs text-slate-500 font-medium">Fetching order confirmation...</p>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="max-w-md mx-auto px-4 py-20 text-center space-y-4">
        <h2 className="text-xl font-bold text-slate-900">Order not found</h2>
        <Link to="/" className="inline-block bg-indigo-600 text-white text-xs font-semibold px-6 py-2.5 rounded-full">
          Return Home
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-12 space-y-8">
      {/* 1. Success Hero Card */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-8 shadow-card text-center space-y-4">
        <div className="w-16 h-16 rounded-full bg-emerald-50 text-emerald-600 flex items-center justify-center mx-auto ring-8 ring-emerald-50/50">
          <CheckCircle className="w-10 h-10" />
        </div>

        <div className="space-y-1">
          <span className="inline-flex items-center gap-1 text-[11px] font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full">
            <Sparkles className="w-3.5 h-3.5" /> Order Placed Successfully
          </span>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight pt-1">
            Thank you for your order!
          </h1>
          <p className="text-xs sm:text-sm text-slate-500">
            A confirmation notification has been recorded for Order <span className="font-bold text-slate-800">#{order.order_number}</span>.
          </p>
        </div>

        <div className="pt-2 flex flex-wrap items-center justify-center gap-4 text-xs">
          <div className="flex items-center gap-1.5 text-slate-600 bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-200">
            <Calendar className="w-4 h-4 text-indigo-600" />
            <span>Estimated Delivery: <strong className="text-slate-900">{formattedDelivery}</strong></span>
          </div>

          <div className="flex items-center gap-1.5 text-slate-600 bg-slate-50 px-3 py-1.5 rounded-xl border border-slate-200">
            <CreditCard className="w-4 h-4 text-emerald-600" />
            <span>Payment: <strong className="text-slate-900 uppercase">{order.payment_method}</strong> ({order.payment_status})</span>
          </div>
        </div>
      </div>

      {/* 2. Order Details & Purchased Items Card */}
      <div className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-subtle space-y-6">
        <h3 className="text-base font-bold text-slate-900 pb-3 border-b border-slate-100 flex items-center gap-2">
          <Package className="w-4 h-4 text-indigo-600" />
          Items in this Order ({order.items.length})
        </h3>

        <div className="divide-y divide-slate-100">
          {order.items.map((item) => (
            <div key={item.id} className="py-3.5 flex items-center justify-between gap-4 first:pt-0 last:pb-0">
              <div className="flex items-center space-x-3.5 min-w-0 flex-1">
                <img
                  src={item.product_image || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=100'}
                  alt={item.product_name}
                  className="w-14 h-14 object-cover rounded-xl border border-slate-200 flex-shrink-0"
                />
                <div className="min-w-0">
                  <p className="text-xs sm:text-sm font-bold text-slate-900 truncate">
                    {item.product_name}
                  </p>
                  <p className="text-[11px] text-slate-400 mt-0.5">
                    Qty: {item.quantity} {item.size ? `• Size: ${item.size}` : ''} {item.color ? `• Color: ${item.color}` : ''}
                  </p>
                </div>
              </div>

              <div className="text-right">
                <p className="text-xs sm:text-sm font-bold text-slate-900">
                  ₹{item.total_price.toLocaleString('en-IN')}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Cost Summary */}
        <div className="pt-4 border-t border-slate-100 space-y-2 text-xs">
          <div className="flex justify-between text-slate-600">
            <span>Subtotal</span>
            <span>₹{order.subtotal.toLocaleString('en-IN')}</span>
          </div>
          {order.discount > 0 && (
            <div className="flex justify-between text-emerald-600 font-semibold">
              <span>Discount</span>
              <span>- ₹{order.discount.toLocaleString('en-IN')}</span>
            </div>
          )}
          <div className="flex justify-between text-slate-600">
            <span>Shipping</span>
            <span>{order.delivery_charge === 0 ? 'FREE' : `₹${order.delivery_charge}`}</span>
          </div>
          <div className="pt-2 border-t border-slate-100 flex justify-between text-sm font-black text-slate-900">
            <span>Total Paid</span>
            <span className="text-indigo-600">₹{order.total_amount.toLocaleString('en-IN')}</span>
          </div>
        </div>

        {/* Delivery Address Card */}
        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100 space-y-1 text-xs">
          <p className="font-bold text-slate-800 flex items-center gap-1.5">
            <MapPin className="w-3.5 h-3.5 text-indigo-600" />
            Shipping To: {order.shipping_name} ({order.shipping_mobile})
          </p>
          <p className="text-slate-500 pl-5">
            {order.shipping_address.address}, {order.shipping_address.city}, {order.shipping_address.state} - {order.shipping_address.postal_code}
          </p>
        </div>
      </div>

      {/* 3. Action Buttons */}
      <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
        <Link
          to="/orders"
          className="w-full sm:w-auto bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs sm:text-sm px-8 py-3 rounded-full shadow-sm text-center"
        >
          View My Orders
        </Link>
        <Link
          to="/products"
          className="w-full sm:w-auto bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs sm:text-sm px-8 py-3 rounded-full shadow-md text-center flex items-center justify-center gap-2"
        >
          <span>Continue Shopping</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
};
