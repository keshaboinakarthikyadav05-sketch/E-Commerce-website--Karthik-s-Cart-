import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Package,
  Calendar,
  CreditCard,
  MapPin,
  Clock,
  CheckCircle2,
  XCircle,
  Truck,
  ArrowRight,
  AlertTriangle
} from 'lucide-react';
import { ordersApi } from '../services/api';
import { Order } from '../types';
import { useAuth } from '../context/AuthContext';

export const MyOrdersPage: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [cancellingId, setCancellingId] = useState<number | null>(null);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      const res = await ordersApi.getUserOrders();
      if (res.data?.success) {
        setOrders(res.data.orders);
      }
    } catch (err) {
      console.error('Failed to fetch orders:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isAuthenticated) {
      fetchOrders();
    }
  }, [isAuthenticated]);

  const handleCancelOrder = async (orderId: number) => {
    if (!window.confirm('Are you sure you want to cancel this order?')) return;

    try {
      setCancellingId(orderId);
      const res = await ordersApi.cancelOrder(orderId);
      if (res.data?.success) {
        fetchOrders();
      }
    } catch (err: any) {
      alert(err.response?.data?.message || 'Could not cancel order');
    } finally {
      setCancellingId(null);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'delivered':
        return <span className="bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider">Delivered</span>;
      case 'shipped':
        return <span className="bg-blue-50 text-blue-700 border border-blue-200 px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider">Shipped</span>;
      case 'processing':
      case 'confirmed':
        return <span className="bg-indigo-50 text-indigo-700 border border-indigo-200 px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider">{status}</span>;
      case 'cancelled':
        return <span className="bg-rose-50 text-rose-700 border border-rose-200 px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider">Cancelled</span>;
      default:
        return <span className="bg-amber-50 text-amber-800 border border-amber-200 px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase tracking-wider">{status}</span>;
    }
  };

  if (loading) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <div className="inline-block w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin mb-4" />
        <p className="text-xs text-slate-500 font-medium">Loading your order history...</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 space-y-8">
      <div className="pb-4 border-b border-slate-200 flex items-center justify-between">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            My Orders
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Track shipments, review past purchases, or manage cancellations
          </p>
        </div>
      </div>

      {orders.length === 0 ? (
        <div className="bg-white rounded-3xl border border-slate-200 p-12 text-center space-y-4">
          <div className="w-16 h-16 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
            <Package className="w-8 h-8" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">No orders placed yet</h3>
          <p className="text-xs sm:text-sm text-slate-500 max-w-sm mx-auto">
            Once you place an order, you will be able to track live delivery status and receipts right here.
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
        <div className="space-y-6">
          {orders.map((ord) => (
            <div
              key={ord.id}
              className="bg-white rounded-3xl border border-slate-200/80 p-6 shadow-subtle space-y-4"
            >
              {/* Order Card Header */}
              <div className="flex flex-wrap items-center justify-between pb-3 border-b border-slate-100 gap-2">
                <div className="space-y-0.5">
                  <p className="text-xs font-bold text-slate-900">
                    Order <span className="text-indigo-600">#{ord.order_number}</span>
                  </p>
                  <p className="text-[11px] text-slate-400">
                    Placed on {new Date(ord.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>

                <div className="flex items-center space-x-3">
                  {getStatusBadge(ord.order_status)}
                  <span className="text-sm font-black text-slate-900">
                    ₹{ord.total_amount.toLocaleString('en-IN')}
                  </span>
                </div>
              </div>

              {/* Items List */}
              <div className="divide-y divide-slate-100">
                {ord.items.map((it) => (
                  <div key={it.id} className="py-3 flex items-center justify-between gap-4">
                    <div className="flex items-center space-x-3 min-w-0">
                      <img
                        src={it.product_image || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=100'}
                        alt=""
                        className="w-12 h-12 object-cover rounded-xl border border-slate-200 flex-shrink-0"
                      />
                      <div className="min-w-0">
                        <p className="text-xs font-bold text-slate-900 truncate">
                          {it.product_name}
                        </p>
                        <p className="text-[11px] text-slate-400">
                          Qty: {it.quantity} {it.size ? `• Size: ${it.size}` : ''} {it.color ? `• Color: ${it.color}` : ''}
                        </p>
                      </div>
                    </div>
                    <span className="text-xs font-bold text-slate-800">
                      ₹{it.total_price.toLocaleString('en-IN')}
                    </span>
                  </div>
                ))}
              </div>

              {/* Delivery and Action Footer */}
              <div className="pt-3 border-t border-slate-100 flex flex-wrap items-center justify-between gap-3 text-xs">
                <div className="text-slate-500">
                  <span className="font-semibold text-slate-700">Delivery Address:</span> {ord.shipping_name}, {ord.shipping_address.city} ({ord.shipping_mobile})
                </div>

                <div className="flex items-center space-x-3">
                  {(ord.order_status === 'placed' || ord.order_status === 'confirmed') && (
                    <button
                      onClick={() => handleCancelOrder(ord.id)}
                      disabled={cancellingId === ord.id}
                      className="text-xs font-semibold text-rose-600 hover:text-rose-700 border border-rose-200 hover:bg-rose-50 px-3.5 py-1.5 rounded-xl transition-colors"
                    >
                      {cancellingId === ord.id ? 'Cancelling...' : 'Cancel Order'}
                    </button>
                  )}

                  <Link
                    to={`/order-success/${ord.id}`}
                    className="text-xs font-semibold text-indigo-600 hover:underline"
                  >
                    View Invoice →
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
