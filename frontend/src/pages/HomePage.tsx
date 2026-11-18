import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  ArrowRight,
  TrendingUp,
  Sparkles,
  Award,
  Zap,
  Star,
  ChevronLeft,
  ChevronRight,
  ShieldCheck,
  Clock,
  Flame,
  BadgePercent
} from 'lucide-react';
import { ProductCard } from '../components/ProductCard';
import { SkeletonCard } from '../components/SkeletonCard';
import { productsApi, categoriesApi } from '../services/api';
import { Product, Category } from '../types';

interface HomePageProps {
  onOpenAuth: () => void;
}

export const HomePage: React.FC<HomePageProps> = ({ onOpenAuth }) => {
  const navigate = useNavigate();

  const [categories, setCategories] = useState<Category[]>([]);
  const [trendingProducts, setTrendingProducts] = useState<Product[]>([]);
  const [bestsellerProducts, setBestsellerProducts] = useState<Product[]>([]);
  const [newArrivals, setNewArrivals] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  // Hero carousel state
  const [currentSlide, setCurrentSlide] = useState(0);

  const heroSlides = [
    {
      badge: "Winter & Festive Collection 2026",
      title: "Elevate Your Style With Modern Essentials",
      description: "Discover handcrafted luxury denim, tailored trousers, and premium casuals engineered for unmatched comfort and presence.",
      cta: "Shop Men's & Women's",
      link: "/products?category=mens-pants",
      bgGradient: "from-slate-950 via-slate-900 to-indigo-950",
      accentPill: "bg-indigo-500/20 text-indigo-300 border-indigo-500/30",
      image: "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=1000&auto=format&fit=crop&q=80"
    },
    {
      badge: "Flagship Tech Season",
      title: "Next-Gen 5G Smartphones & AI Laptops",
      description: "Power your productivity and creativity with the world's most cutting-edge displays, processors, and camera systems.",
      cta: "Explore Flagships",
      link: "/products?category=smartphones",
      bgGradient: "from-slate-950 via-blue-950 to-slate-900",
      accentPill: "bg-blue-500/20 text-blue-300 border-blue-500/30",
      image: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=1000&auto=format&fit=crop&q=80"
    },
    {
      badge: "Acoustic Immersion",
      title: "Audiophile Noise Cancelling & Horology",
      description: "Experience spatial soundscapes and Swiss automatic horological perfection crafted for the discerning connoisseur.",
      cta: "Discover Audio & Watches",
      link: "/products?category=headphones",
      bgGradient: "from-zinc-950 via-neutral-900 to-slate-950",
      accentPill: "bg-amber-500/20 text-amber-300 border-amber-500/30",
      image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=1000&auto=format&fit=crop&q=80"
    }
  ];

  // Auto-slide hero
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
    }, 6000);
    return () => clearInterval(timer);
  }, [heroSlides.length]);

  // Flash Sale Countdown state
  const [timeLeft, setTimeLeft] = useState({ hours: 14, minutes: 32, seconds: 45 });
  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev.seconds > 0) return { ...prev, seconds: prev.seconds - 1 };
        if (prev.minutes > 0) return { ...prev, minutes: 59, seconds: 59 };
        if (prev.hours > 0) return { hours: prev.hours - 1, minutes: 59, seconds: 59 };
        return { hours: 24, minutes: 0, seconds: 0 };
      });
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  // Fetch data
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const [catsRes, trendRes, bestRes, newRes] = await Promise.all([
          categoriesApi.getCategories(),
          productsApi.getProducts({ trending: 'true', limit: 8 }),
          productsApi.getProducts({ bestseller: 'true', limit: 8 }),
          productsApi.getProducts({ sort: 'newest', limit: 8 }),
        ]);

        if (catsRes.data?.success) setCategories(catsRes.data.categories);
        if (trendRes.data?.success) setTrendingProducts(trendRes.data.products);
        if (bestRes.data?.success) setBestsellerProducts(bestRes.data.products);
        if (newRes.data?.success) setNewArrivals(newRes.data.products);
      } catch (err) {
        console.error('Failed to load homepage data:', err);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  return (
    <div className="space-y-16 pb-16">
      {/* 1. Hero Promotional Banner Carousel */}
      <section className="relative overflow-hidden bg-slate-950 text-white min-h-[480px] sm:min-h-[540px] lg:min-h-[580px] flex items-center">
        {heroSlides.map((slide, idx) => (
          <div
            key={idx}
            className={`absolute inset-0 transition-opacity duration-1000 flex items-center bg-gradient-to-r ${slide.bgGradient} ${
              idx === currentSlide ? 'opacity-100 z-10 pointer-events-auto' : 'opacity-0 z-0 pointer-events-none'
            }`}
          >
            {/* Background Image Ambient Glow */}
            <div className="absolute right-0 top-0 bottom-0 w-full lg:w-1/2 opacity-35 lg:opacity-60 overflow-hidden">
              <img
                src={slide.image}
                alt={slide.title}
                className="w-full h-full object-cover object-center filter saturate-150 transform scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-r from-slate-950 via-slate-950/70 to-transparent" />
            </div>

            {/* Slide Content */}
            <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 z-20">
              <div className="max-w-xl space-y-6">
                <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold tracking-wide uppercase border ${slide.accentPill}`}>
                  <Sparkles className="w-3.5 h-3.5" />
                  {slide.badge}
                </span>

                <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-white leading-tight">
                  {slide.title}
                </h1>

                <p className="text-sm sm:text-base text-slate-300 leading-relaxed">
                  {slide.description}
                </p>

                <div className="flex flex-wrap items-center gap-4 pt-2">
                  <Link
                    to={slide.link}
                    className="inline-flex items-center gap-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm px-6 py-3.5 rounded-full shadow-lg shadow-indigo-600/30 hover:scale-105 transition-all"
                  >
                    <span>{slide.cta}</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>

                  <Link
                    to="/products"
                    className="inline-flex items-center gap-2 bg-white/10 hover:bg-white/20 text-white font-semibold text-sm px-6 py-3.5 rounded-full border border-white/20 backdrop-blur-sm transition-colors"
                  >
                    View All Categories
                  </Link>
                </div>
              </div>
            </div>
          </div>
        ))}

        {/* Carousel Navigation Arrows */}
        <button
          onClick={() => setCurrentSlide((prev) => (prev === 0 ? heroSlides.length - 1 : prev - 1))}
          className="absolute left-4 top-1/2 -translate-y-1/2 z-30 w-10 h-10 rounded-full bg-white/10 hover:bg-white/25 text-white flex items-center justify-center backdrop-blur-md transition-colors"
          aria-label="Previous Slide"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>
        <button
          onClick={() => setCurrentSlide((prev) => (prev + 1) % heroSlides.length)}
          className="absolute right-4 top-1/2 -translate-y-1/2 z-30 w-10 h-10 rounded-full bg-white/10 hover:bg-white/25 text-white flex items-center justify-center backdrop-blur-md transition-colors"
          aria-label="Next Slide"
        >
          <ChevronRight className="w-5 h-5" />
        </button>

        {/* Carousel Dots */}
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-30 flex space-x-2">
          {heroSlides.map((_, i) => (
            <button
              key={i}
              onClick={() => setCurrentSlide(i)}
              className={`h-2 rounded-full transition-all ${
                i === currentSlide ? 'w-8 bg-indigo-500' : 'w-2 bg-white/30 hover:bg-white/60'
              }`}
              aria-label={`Slide ${i + 1}`}
            />
          ))}
        </div>
      </section>

      {/* 2. Shop By Category Section (10 Categories) */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row items-start sm:items-end justify-between mb-8 gap-4">
          <div>
            <div className="flex items-center gap-2 text-indigo-600 text-xs font-bold uppercase tracking-wider mb-1">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Curated Collections</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Shop By Category
            </h2>
            <p className="text-xs sm:text-sm text-slate-500 mt-1">
              Explore 10 curated departments covering lifestyle fashion, flagship electronics, and accessories.
            </p>
          </div>
          <Link
            to="/products"
            className="inline-flex items-center gap-1.5 text-xs sm:text-sm font-semibold text-indigo-600 hover:text-indigo-700 hover:underline"
          >
            Explore All Catalog <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {categories.map((cat) => (
            <Link
              key={cat.id}
              to={`/products?category=${cat.slug}`}
              className="group relative bg-white rounded-2xl border border-slate-200/80 overflow-hidden shadow-subtle hover:shadow-card hover:border-indigo-300 transition-all duration-300"
            >
              <div className="aspect-[4/3] w-full overflow-hidden bg-slate-100">
                <img
                  src={cat.image_url || 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500'}
                  alt={cat.name}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                  loading="lazy"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-slate-950/20 to-transparent" />
              </div>
              <div className="absolute bottom-0 left-0 right-0 p-3.5 text-white">
                <h3 className="text-sm font-bold truncate group-hover:text-indigo-300 transition-colors">
                  {cat.name}
                </h3>
                <p className="text-[11px] text-slate-300">
                  {cat.product_count || 10}+ Products
                </p>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* 3. Limited Time Flash Sale Countdown Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="relative rounded-3xl bg-gradient-to-r from-indigo-900 via-indigo-800 to-blue-900 text-white p-6 sm:p-10 overflow-hidden shadow-xl">
          <div className="absolute -right-10 -bottom-10 w-64 h-64 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />
          <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
            <div className="space-y-2 text-center md:text-left">
              <span className="inline-flex items-center gap-1.5 bg-rose-500/20 text-rose-300 border border-rose-500/30 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider">
                <Flame className="w-3.5 h-3.5 fill-rose-400" />
                Limited Time Flash Deals
              </span>
              <h3 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
                Up to 50% Off On Bestselling Electronics & Apparel
              </h3>
              <p className="text-xs sm:text-sm text-indigo-200 max-w-xl">
                Claim extra ₹500 discount with code <span className="font-bold text-amber-300">FESTIVE500</span> at checkout. Valid till stocks last.
              </p>
            </div>

            {/* Countdown timer */}
            <div className="flex items-center gap-3">
              <div className="bg-slate-950/60 backdrop-blur-md border border-white/10 px-3.5 py-2.5 rounded-2xl text-center min-w-[64px]">
                <span className="text-2xl font-black text-amber-400">{String(timeLeft.hours).padStart(2, '0')}</span>
                <span className="block text-[10px] text-slate-300 uppercase tracking-wider font-semibold">Hours</span>
              </div>
              <span className="text-xl font-bold text-amber-400">:</span>
              <div className="bg-slate-950/60 backdrop-blur-md border border-white/10 px-3.5 py-2.5 rounded-2xl text-center min-w-[64px]">
                <span className="text-2xl font-black text-amber-400">{String(timeLeft.minutes).padStart(2, '0')}</span>
                <span className="block text-[10px] text-slate-300 uppercase tracking-wider font-semibold">Mins</span>
              </div>
              <span className="text-xl font-bold text-amber-400">:</span>
              <div className="bg-slate-950/60 backdrop-blur-md border border-white/10 px-3.5 py-2.5 rounded-2xl text-center min-w-[64px]">
                <span className="text-2xl font-black text-amber-400">{String(timeLeft.seconds).padStart(2, '0')}</span>
                <span className="block text-[10px] text-slate-300 uppercase tracking-wider font-semibold">Secs</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. Trending Products Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="flex items-center gap-1.5 text-rose-600 text-xs font-bold uppercase tracking-wider mb-1">
              <TrendingUp className="w-3.5 h-3.5" />
              <span>Hottest Drops</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Trending Right Now
            </h2>
          </div>
          <Link
            to="/products?trending=true"
            className="text-xs sm:text-sm font-semibold text-indigo-600 hover:text-indigo-700 hover:underline flex items-center gap-1"
          >
            See All <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
          {loading ? (
            Array.from({ length: 8 }).map((_, i) => <SkeletonCard key={i} />)
          ) : trendingProducts.length > 0 ? (
            trendingProducts.map((p) => (
              <ProductCard key={p.id} product={p} onOpenAuth={onOpenAuth} />
            ))
          ) : (
            <div className="col-span-full py-12 text-center text-slate-400 text-sm">
              No products found.
            </div>
          )}
        </div>
      </section>

      {/* 5. Best-Selling Products Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="flex items-center gap-1.5 text-amber-600 text-xs font-bold uppercase tracking-wider mb-1">
              <Award className="w-3.5 h-3.5" />
              <span>Customer Favorites</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              Best-Selling Products
            </h2>
          </div>
          <Link
            to="/products?bestseller=true"
            className="text-xs sm:text-sm font-semibold text-indigo-600 hover:text-indigo-700 hover:underline flex items-center gap-1"
          >
            See All <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
          {loading ? (
            Array.from({ length: 8 }).map((_, i) => <SkeletonCard key={i} />)
          ) : (
            bestsellerProducts.map((p) => (
              <ProductCard key={p.id} product={p} onOpenAuth={onOpenAuth} />
            ))
          )}
        </div>
      </section>

      {/* 6. New Arrivals Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <div>
            <div className="flex items-center gap-1.5 text-emerald-600 text-xs font-bold uppercase tracking-wider mb-1">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Fresh Off The Runway</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
              New Arrivals
            </h2>
          </div>
          <Link
            to="/products?sort=newest"
            className="text-xs sm:text-sm font-semibold text-indigo-600 hover:text-indigo-700 hover:underline flex items-center gap-1"
          >
            See All <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
          {loading ? (
            Array.from({ length: 8 }).map((_, i) => <SkeletonCard key={i} />)
          ) : (
            newArrivals.map((p) => (
              <ProductCard key={p.id} product={p} onOpenAuth={onOpenAuth} />
            ))
          )}
        </div>
      </section>

      {/* 7. Customer Reviews & Testimonials Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-12">
          <span className="text-xs font-bold uppercase tracking-widest text-indigo-600">
            Real Customer Feedback
          </span>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1">
            Loved By Over 50,000+ Happy Shoppers
          </h2>
          <p className="text-xs sm:text-sm text-slate-500 mt-2">
            See what verified customers across India say about Karthik's Cart's premium quality, fast shipping, and seamless Razorpay checkout.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-subtle space-y-4">
            <div className="flex items-center text-amber-400">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="w-4 h-4 fill-amber-400" />
              ))}
            </div>
            <p className="text-xs sm:text-sm text-slate-700 leading-relaxed italic">
              "Ordered the iPhone 16 Pro Max and Levi's 511 stretch jeans. Arrived within 48 hours in immaculate tamper-proof packaging. The Razorpay checkout was lightning fast with UPI!"
            </p>
            <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
              <div>
                <p className="text-xs font-bold text-slate-900">Rohan Malhotra</p>
                <p className="text-[11px] text-slate-400">Mumbai, Maharashtra</p>
              </div>
              <span className="text-[10px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full flex items-center gap-1">
                <ShieldCheck className="w-3 h-3" /> Verified Buyer
              </span>
            </div>
          </div>

          <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-subtle space-y-4">
            <div className="flex items-center text-amber-400">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="w-4 h-4 fill-amber-400" />
              ))}
            </div>
            <p className="text-xs sm:text-sm text-slate-700 leading-relaxed italic">
              "The Sony WH-1000XM5 headphones are 100% authentic and sound phenomenal. The discount coupon WELCOME200 worked instantly. Best e-commerce UI I have used in India."
            </p>
            <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
              <div>
                <p className="text-xs font-bold text-slate-900">Pooja Krishnan</p>
                <p className="text-[11px] text-slate-400">Bengaluru, Karnataka</p>
              </div>
              <span className="text-[10px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full flex items-center gap-1">
                <ShieldCheck className="w-3 h-3" /> Verified Buyer
              </span>
            </div>
          </div>

          <div className="bg-white p-6 rounded-3xl border border-slate-200/80 shadow-subtle space-y-4">
            <div className="flex items-center text-amber-400">
              {[...Array(5)].map((_, i) => (
                <Star key={i} className="w-4 h-4 fill-amber-400" />
              ))}
            </div>
            <p className="text-xs sm:text-sm text-slate-700 leading-relaxed italic">
              "Zara tailored trousers and Nike Jordans arrived in pristine condition. Easy tracking and updates at every step. Karthik's Cart has become my go-to luxury shopping app!"
            </p>
            <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
              <div>
                <p className="text-xs font-bold text-slate-900">Vikramaditya Rao</p>
                <p className="text-[11px] text-slate-400">New Delhi</p>
              </div>
              <span className="text-[10px] font-semibold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full flex items-center gap-1">
                <ShieldCheck className="w-3 h-3" /> Verified Buyer
              </span>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};
