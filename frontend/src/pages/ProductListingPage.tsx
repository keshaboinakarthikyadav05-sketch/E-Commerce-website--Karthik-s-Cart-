import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  Filter,
  X,
  SlidersHorizontal,
  ChevronDown,
  Star,
  Search,
  RotateCcw,
  Sparkles,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import { ProductCard } from '../components/ProductCard';
import { SkeletonCard } from '../components/SkeletonCard';
import { productsApi, categoriesApi } from '../services/api';
import { Product, Category } from '../types';

interface ProductListingPageProps {
  onOpenAuth: () => void;
}

export const ProductListingPage: React.FC<ProductListingPageProps> = ({ onOpenAuth }) => {
  const [searchParams, setSearchParams] = useSearchParams();

  // URL state
  const querySearch = searchParams.get('q') || '';
  const queryCategory = searchParams.get('category') || '';
  const queryBrand = searchParams.get('brand') || '';
  const querySort = searchParams.get('sort') || 'newest';
  const queryMinPrice = searchParams.get('min_price') || '';
  const queryMaxPrice = searchParams.get('max_price') || '';
  const queryRating = searchParams.get('rating') || '';
  const queryPage = parseInt(searchParams.get('page') || '1', 10);

  // Component state
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [pagination, setPagination] = useState({
    total: 0,
    page: 1,
    pages: 1,
    limit: 12,
    has_prev: false,
    has_next: false,
  });
  const [loading, setLoading] = useState(true);
  const [mobileFilterOpen, setMobileFilterOpen] = useState(false);

  // Local filter inputs
  const [minPriceInput, setMinPriceInput] = useState(queryMinPrice);
  const [maxPriceInput, setMaxPriceInput] = useState(queryMaxPrice);
  const [brandSearchInput, setBrandSearchInput] = useState('');

  // Extract unique brands from current category or all
  const availableBrands = [
    "Apple", "Samsung", "Sony", "Dell", "ASUS", "Nike", "Adidas",
    "Levi's", "Zara", "H&M", "Tommy Hilfiger", "Bose", "Puma",
    "Fossil", "Seiko", "New Balance", "Uniqlo", "Google"
  ];

  // Load categories
  useEffect(() => {
    categoriesApi.getCategories().then((res) => {
      if (res.data?.success) setCategories(res.data.categories);
    }).catch(() => {});
  }, []);

  // Fetch products whenever search params change
  useEffect(() => {
    const fetchProducts = async () => {
      setLoading(true);
      try {
        const params: Record<string, any> = {
          page: queryPage,
          limit: 12,
          sort: querySort,
        };
        if (querySearch) params.q = querySearch;
        if (queryCategory) params.category = queryCategory;
        if (queryBrand) params.brand = queryBrand;
        if (queryMinPrice) params.min_price = queryMinPrice;
        if (queryMaxPrice) params.max_price = queryMaxPrice;
        if (queryRating) params.rating = queryRating;
        if (searchParams.get('trending')) params.trending = 'true';
        if (searchParams.get('bestseller')) params.bestseller = 'true';

        const res = await productsApi.getProducts(params);
        if (res.data?.success) {
          setProducts(res.data.products);
          setPagination(res.data.pagination);
        }
      } catch (err) {
        console.error('Failed to fetch products:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [
    querySearch,
    queryCategory,
    queryBrand,
    querySort,
    queryMinPrice,
    queryMaxPrice,
    queryRating,
    queryPage,
    searchParams
  ]);

  // Update query params helper
  const updateFilters = (updates: Record<string, string | null>) => {
    const nextParams = new URLSearchParams(searchParams);
    Object.entries(updates).forEach(([key, val]) => {
      if (val === null || val === '') {
        nextParams.delete(key);
      } else {
        nextParams.set(key, val);
      }
    });
    // Reset to page 1 on filter modification (unless updating page itself)
    if (!updates.page) {
      nextParams.set('page', '1');
    }
    setSearchParams(nextParams);
  };

  const clearAllFilters = () => {
    setMinPriceInput('');
    setMaxPriceInput('');
    setBrandSearchInput('');
    setSearchParams(new URLSearchParams());
  };

  const handlePriceApply = (e: React.FormEvent) => {
    e.preventDefault();
    updateFilters({
      min_price: minPriceInput || null,
      max_price: maxPriceInput || null,
    });
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* 1. Header & Active Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-slate-200 gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            {queryCategory
              ? categories.find((c) => c.slug === queryCategory)?.name || 'Products'
              : querySearch
              ? `Search Results for "${querySearch}"`
              : 'All Products'}
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Showing <span className="font-semibold text-slate-800">{pagination.total}</span> authentic products
          </p>
        </div>

        {/* Sort & Mobile Filter Toggle */}
        <div className="flex items-center space-x-3 self-end md:self-auto w-full md:w-auto justify-between md:justify-end">
          <button
            onClick={() => setMobileFilterOpen(true)}
            className="lg:hidden flex items-center gap-1.5 px-4 py-2 bg-white border border-slate-200 rounded-xl text-xs font-semibold text-slate-700 shadow-sm"
          >
            <SlidersHorizontal className="w-4 h-4 text-indigo-600" />
            <span>Filters</span>
          </button>

          {/* Sort Dropdown */}
          <div className="flex items-center space-x-2 text-xs">
            <span className="text-slate-400 font-medium hidden sm:inline">Sort By:</span>
            <select
              value={querySort}
              onChange={(e) => updateFilters({ sort: e.target.value })}
              className="bg-white border border-slate-200 rounded-xl px-3.5 py-2 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm cursor-pointer"
            >
              <option value="newest">Newest Arrivals</option>
              <option value="popularity">Popularity & Rating</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
              <option value="discount">Highest Discount</option>
            </select>
          </div>
        </div>
      </div>

      {/* 2. Active Filter Pills */}
      {(queryCategory || queryBrand || queryMinPrice || queryMaxPrice || queryRating || querySearch) && (
        <div className="flex flex-wrap items-center gap-2 pt-1 pb-2">
          <span className="text-xs font-semibold text-slate-400 mr-1">Active Filters:</span>
          {querySearch && (
            <span className="inline-flex items-center gap-1 text-xs bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full font-medium border border-indigo-100">
              Query: "{querySearch}"
              <button onClick={() => updateFilters({ q: null })}><X className="w-3.5 h-3.5 hover:text-indigo-900" /></button>
            </span>
          )}
          {queryCategory && (
            <span className="inline-flex items-center gap-1 text-xs bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full font-medium border border-indigo-100">
              Category: {categories.find((c) => c.slug === queryCategory)?.name || queryCategory}
              <button onClick={() => updateFilters({ category: null })}><X className="w-3.5 h-3.5 hover:text-indigo-900" /></button>
            </span>
          )}
          {queryBrand && (
            <span className="inline-flex items-center gap-1 text-xs bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full font-medium border border-indigo-100">
              Brand: {queryBrand}
              <button onClick={() => updateFilters({ brand: null })}><X className="w-3.5 h-3.5 hover:text-indigo-900" /></button>
            </span>
          )}
          {(queryMinPrice || queryMaxPrice) && (
            <span className="inline-flex items-center gap-1 text-xs bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full font-medium border border-indigo-100">
              Price: ₹{queryMinPrice || '0'} - ₹{queryMaxPrice || 'Max'}
              <button onClick={() => { setMinPriceInput(''); setMaxPriceInput(''); updateFilters({ min_price: null, max_price: null }); }}><X className="w-3.5 h-3.5 hover:text-indigo-900" /></button>
            </span>
          )}
          {queryRating && (
            <span className="inline-flex items-center gap-1 text-xs bg-indigo-50 text-indigo-700 px-3 py-1 rounded-full font-medium border border-indigo-100">
              Rating: {queryRating}★ & above
              <button onClick={() => updateFilters({ rating: null })}><X className="w-3.5 h-3.5 hover:text-indigo-900" /></button>
            </span>
          )}
          <button
            onClick={clearAllFilters}
            className="text-xs text-rose-600 hover:text-rose-700 font-semibold underline ml-2 flex items-center gap-1"
          >
            <RotateCcw className="w-3 h-3" /> Clear All
          </button>
        </div>
      )}

      {/* 3. Main Content: Sidebar + Products Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
        {/* Desktop Sidebar Filters */}
        <aside className="hidden lg:block space-y-6 bg-white p-6 rounded-3xl border border-slate-200/80 shadow-subtle sticky top-28">
          <div className="flex items-center justify-between pb-3 border-b border-slate-100">
            <span className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Filter className="w-4 h-4 text-indigo-600" />
              Filter By
            </span>
            <button
              onClick={clearAllFilters}
              className="text-[11px] font-semibold text-slate-400 hover:text-rose-600 transition-colors"
            >
              Reset
            </button>
          </div>

          {/* Categories */}
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-3">
              Categories
            </h4>
            <div className="space-y-1.5 max-h-52 overflow-y-auto pr-1">
              <button
                onClick={() => updateFilters({ category: null })}
                className={`w-full text-left text-xs py-1.5 px-2 rounded-lg transition-colors flex items-center justify-between ${
                  !queryCategory ? 'bg-indigo-50 text-indigo-600 font-bold' : 'text-slate-600 hover:bg-slate-50'
                }`}
              >
                <span>All Categories</span>
              </button>
              {categories.map((c) => (
                <button
                  key={c.id}
                  onClick={() => updateFilters({ category: c.slug === queryCategory ? null : c.slug })}
                  className={`w-full text-left text-xs py-1.5 px-2 rounded-lg transition-colors flex items-center justify-between ${
                    queryCategory === c.slug
                      ? 'bg-indigo-50 text-indigo-600 font-bold'
                      : 'text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <span className="truncate">{c.name}</span>
                  <span className="text-[10px] text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded-full">
                    {c.product_count || 10}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Price Range */}
          <div className="pt-4 border-t border-slate-100">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-3">
              Price Range (₹)
            </h4>
            <form onSubmit={handlePriceApply} className="space-y-2">
              <div className="flex items-center gap-2">
                <input
                  type="number"
                  placeholder="Min"
                  value={minPriceInput}
                  onChange={(e) => setMinPriceInput(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-2.5 py-1.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-600"
                />
                <span className="text-xs text-slate-400">-</span>
                <input
                  type="number"
                  placeholder="Max"
                  value={maxPriceInput}
                  onChange={(e) => setMaxPriceInput(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-2.5 py-1.5 text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-600"
                />
              </div>
              <button
                type="submit"
                className="w-full bg-slate-900 hover:bg-indigo-600 text-white text-xs font-semibold py-1.5 rounded-xl transition-colors"
              >
                Apply Range
              </button>
            </form>
          </div>

          {/* Brands */}
          <div className="pt-4 border-t border-slate-100">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
              Brand
            </h4>
            <div className="space-y-1.5 max-h-40 overflow-y-auto pr-1">
              {availableBrands.map((b) => (
                <button
                  key={b}
                  onClick={() => updateFilters({ brand: queryBrand === b ? null : b })}
                  className={`w-full text-left text-xs py-1.5 px-2 rounded-lg transition-colors flex items-center justify-between ${
                    queryBrand === b ? 'bg-indigo-50 text-indigo-600 font-bold' : 'text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <span>{b}</span>
                  {queryBrand === b && <span className="text-indigo-600 font-bold">✓</span>}
                </button>
              ))}
            </div>
          </div>

          {/* Customer Rating */}
          <div className="pt-4 border-t border-slate-100">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
              Customer Rating
            </h4>
            <div className="space-y-1">
              {[4.5, 4.0, 3.5].map((stars) => (
                <button
                  key={stars}
                  onClick={() => updateFilters({ rating: queryRating === String(stars) ? null : String(stars) })}
                  className={`w-full text-left text-xs py-1.5 px-2 rounded-lg transition-colors flex items-center gap-1.5 ${
                    queryRating === String(stars)
                      ? 'bg-amber-50 text-amber-900 font-bold'
                      : 'text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center text-amber-400">
                    <Star className="w-3.5 h-3.5 fill-amber-400" />
                  </div>
                  <span>{stars}★ & above</span>
                </button>
              ))}
            </div>
          </div>
        </aside>

        {/* Products Grid */}
        <div className="lg:col-span-3 space-y-8">
          {loading ? (
            <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
              {Array.from({ length: 9 }).map((_, i) => (
                <SkeletonCard key={i} />
              ))}
            </div>
          ) : products.length > 0 ? (
            <div className="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6">
              {products.map((p) => (
                <ProductCard key={p.id} product={p} onOpenAuth={onOpenAuth} />
              ))}
            </div>
          ) : (
            <div className="bg-white rounded-3xl border border-slate-200 p-12 text-center space-y-4">
              <div className="w-16 h-16 rounded-full bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
                <Search className="w-8 h-8" />
              </div>
              <h3 className="text-lg font-bold text-slate-900">No matching products found</h3>
              <p className="text-xs sm:text-sm text-slate-500 max-w-sm mx-auto">
                Try removing some filters or search for another term like "pants", "shirt", or "iphone".
              </p>
              <button
                onClick={clearAllFilters}
                className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold px-5 py-2.5 rounded-full transition-colors"
              >
                Reset All Filters
              </button>
            </div>
          )}

          {/* Pagination Controls */}
          {pagination.pages > 1 && (
            <div className="flex items-center justify-center space-x-2 pt-6 border-t border-slate-200">
              <button
                onClick={() => updateFilters({ page: String(pagination.page - 1) })}
                disabled={!pagination.has_prev}
                className="p-2.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>

              {Array.from({ length: pagination.pages }).map((_, i) => {
                const pageNum = i + 1;
                return (
                  <button
                    key={pageNum}
                    onClick={() => updateFilters({ page: String(pageNum) })}
                    className={`w-9 h-9 rounded-xl text-xs font-bold transition-all ${
                      pagination.page === pageNum
                        ? 'bg-indigo-600 text-white shadow-sm'
                        : 'border border-slate-200 text-slate-700 hover:bg-slate-50'
                    }`}
                  >
                    {pageNum}
                  </button>
                );
              })}

              <button
                onClick={() => updateFilters({ page: String(pagination.page + 1) })}
                disabled={!pagination.has_next}
                className="p-2.5 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Mobile Filters Drawer Modal */}
      {mobileFilterOpen && (
        <div className="fixed inset-0 z-50 flex bg-slate-900/60 backdrop-blur-sm lg:hidden animate-in fade-in duration-200">
          <div className="w-4/5 max-w-sm bg-white h-full overflow-y-auto p-6 space-y-6 shadow-2xl ml-auto">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h3 className="text-base font-bold text-slate-900">Filter Products</h3>
              <button onClick={() => setMobileFilterOpen(false)} className="p-1 rounded-full text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Categories */}
            <div>
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">Categories</h4>
              <div className="space-y-1">
                {categories.map((c) => (
                  <button
                    key={c.id}
                    onClick={() => {
                      updateFilters({ category: queryCategory === c.slug ? null : c.slug });
                      setMobileFilterOpen(false);
                    }}
                    className={`w-full text-left text-xs py-1.5 px-2 rounded-lg ${
                      queryCategory === c.slug ? 'bg-indigo-50 text-indigo-600 font-bold' : 'text-slate-600'
                    }`}
                  >
                    {c.name}
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={() => {
                clearAllFilters();
                setMobileFilterOpen(false);
              }}
              className="w-full bg-slate-100 text-slate-700 text-xs font-bold py-2.5 rounded-xl"
            >
              Reset Filters
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
