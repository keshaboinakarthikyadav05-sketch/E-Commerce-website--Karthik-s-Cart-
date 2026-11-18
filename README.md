# Karthik's Cart — Full-Stack E-Commerce Platform

Karthik's Cart is a complete, modern, multi-category e-commerce web platform engineered with **React (TypeScript + Vite + Tailwind CSS)** on the frontend, **Python (Flask REST API + SQLAlchemy)** on the backend, **PostgreSQL** relational database, and **Razorpay** payment gateway integration (online payment with cryptographic HMAC-SHA256 signature verification and Cash on Delivery).

---

## 🌟 Key Features

1. **Multi-Category Catalog (100+ Authentic Products)**
   - 10 distinct categories with 10 unique, non-duplicated products each:
     - Men's Pants
     - Women's Pants
     - T-Shirts
     - Shirts
     - Smartphones
     - Laptops
     - Electronics
     - Headphones
     - Watches
     - Shoes
   - Rich product models with multiple high-definition images, brand specifications, variant sizes, color swatches, stock counts, and verified ratings.

2. **Search & Multi-Dimensional Filtering**
   - Real-time instant autocomplete search suggestions bar.
   - Dynamic filtering by category, brand checklist, price range slider/inputs, customer star rating (4★+, 3★+), and sizes.
   - Dynamic sorting: Price Low-to-High, High-to-Low, Popularity & Rating, Newest Arrivals, Highest Discount.
   - Clean active filter tags with one-click removal and full pagination.

3. **Cart & Wishlist Engine**
   - Persistent user cart with real-time quantity controls (+ / -).
   - Instant move-to-wishlist and move-to-cart operations.
   - Promotional coupon code engine (`SHOPORA10`, `WELCOME200`, `FESTIVE500`).
   - Free shipping calculation threshold (Orders above ₹999).

4. **Secure Checkout & Razorpay Integration**
   - Multi-step address selection and creation with full validation.
   - Razorpay Online Checkout (UPI, Cards, NetBanking) & Cash on Delivery.
   - **Critical Backend Payment Security**:
     - Payment orders created server-side via Razorpay API.
     - Strict cryptographic HMAC-SHA256 signature verification on backend.
     - Orders marked paid ONLY after successful verification.
     - Safe inventory deduction upon verified purchase or confirmed COD.
     - Inventory restoration upon order cancellation.

5. **Customer Orders & Account Management**
   - Order history tracking with live status progression: `Placed` → `Confirmed` → `Processing` → `Shipped` → `Delivered`.
   - Cancellation of eligible orders with automated stock replenishment.
   - Order invoice details and shipping breakdown.

6. **Executive Admin Dashboard**
   - Role-protected admin portal (`role === 'admin'`).
   - Live KPI overview: Total Sales (₹), Total Orders, Live Products, Active Customers, Low Stock Alert.
   - Orders pipeline with instant status updates.
   - Product Management: Add new products with multiple images, edit, delete, stock updates.
   - Category Management: Create new departments with slug generation.
   - User Management: List registered shoppers and toggle active/suspended status.

---

## 🏗️ Architecture & Project Structure

```
E-Commerce/
├── backend/
│   ├── app/
│   │   ├── models/           # SQLAlchemy Models (users, addresses, categories, products, orders, payments, etc.)
│   │   ├── routes/           # REST Blueprints (auth, products, categories, cart, wishlist, orders, payments, admin)
│   │   ├── services/         # Razorpay cryptographic service & utilities
│   │   ├── utils/            # JWT authentication & admin decorators
│   │   ├── config.py         # App configuration & environment variables
│   │   └── __init__.py       # Application factory & CORS
│   ├── seed/
│   │   ├── sample_products.py# 100 uniquely curated realistic products across 10 categories
│   │   └── seed_data.py      # Database initialization & automated seeding script
│   ├── run.py                # Server entrypoint (Port 5000)
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Environment variables template
│   └── .env                  # Active environment settings
├── frontend/
│   ├── src/
│   │   ├── components/       # Navbar, Footer, ProductCard, SkeletonCard, AuthModal
│   │   ├── pages/            # Home, ProductListing, ProductDetails, Cart, Checkout, OrderSuccess, MyOrders, Wishlist, AdminDashboard
│   │   ├── context/          # AuthContext, CartContext, WishlistContext
│   │   ├── services/         # Axios API client
│   │   ├── types/            # TypeScript interfaces
│   │   ├── App.tsx           # Route layout & providers
│   │   └── main.tsx          # React 18 bootstrap
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
└── README.md
```

---

## 🗄️ Database Design (PostgreSQL Relational Schema)

The database consists of 13 normalized relational tables:
1. `users` — Customer & admin accounts with bcrypt password hashes.
2. `addresses` — Shipping destinations with user foreign key.
3. `categories` — Product categories with unique indexed slugs.
4. `products` — Core inventory with pricing, discounts, stock, specs (JSON), and timestamps.
5. `product_images` — Multiple image gallery per product with primary flag.
6. `product_variants` — Sizes, colors, SKUs, and stock per variant.
7. `cart_items` — Shopping cart lines per user with variant FK.
8. `wishlists` — Saved items per user with unique composite constraint.
9. `orders` — Finalized customer orders with shipping snapshot, financial totals, and statuses.
10. `order_items` — Line items per order with snapshot pricing.
11. `payments` — Transaction records with Razorpay order/payment IDs and HMAC signatures.
12. `reviews` — Verified customer ratings & reviews.
13. `coupons` — Promotional discount rules and minimum order thresholds.

---

## 🚀 Getting Started & Running the Application

### 1. PostgreSQL Database Setup

Make sure your PostgreSQL server is running (default port 5432).
Create the database `shopora_db`:
```bash
# Using psql:
psql -U postgres -c "CREATE DATABASE shopora_db;"
```
*(If your PostgreSQL password is not default `postgres`, update `DATABASE_URL` in `backend/.env`)*.

### 2. Backend Setup & Seeding

```bash
cd backend

# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize tables & seed 100+ sample products, admin & customer users
python -m seed.seed_data

# 3. Start backend Flask server (http://localhost:5000)
python run.py
```

### 3. Frontend Setup & Launch

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Start Vite development server (http://localhost:3000)
npm run dev
```

Visit **`http://localhost:3000`** in your browser!

---

## 🔑 Demo Credentials

| Role | Email | Password | Access |
|---|---|---|---|
| **Customer** | `customer@shopora.com` | `Customer@123` | Cart, Wishlist, Checkout, Orders, Reviews |
| **Store Admin** | `admin@shopora.com` | `Admin@123` | Full Admin Dashboard (`/admin`), Manage Products, Orders, Users |

*(Note: The login modal features convenient 1-Click Demo buttons to auto-fill these credentials)*.

---

## 🎟️ Active Discount Coupons

- `SHOPORA10` — Flat 10% instant discount on all orders above ₹500.
- `WELCOME200` — Flat ₹200 off on your first order above ₹1,000.
- `FESTIVE500` — Special festive ₹500 off on orders above ₹2,500.

---

## 💳 Razorpay Configuration

In `backend/.env`:
```env
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
```
- In development/test mode, standard test credentials can be generated at [https://dashboard.razorpay.com/app/keys](https://dashboard.razorpay.com/app/keys).
- If API keys are not supplied, the backend seamlessly runs simulated test checkout mode with cryptographic signature validation to facilitate immediate end-to-end testing without blocking.
